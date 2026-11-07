import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('site_catalog',Path(__file__).resolve().parents[1]/'scripts/laif_site_catalog.py')
site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)

class SiteCatalogueTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'docs/site').mkdir(parents=True)
  (self.root/site.INDEX).write_text(json.dumps({'schema':site.SCHEMA,'sources':[]}))
  text='# Example source\nA named owner must review material AI decisions.\n';sha=hashlib.sha256(text.encode()).hexdigest()
  self.value={'schema':site.SUBMISSION,'publication_consent':{'repository':'mick353/LAIF','visibility':'public','acknowledged':True},'source':{'name':'Example policy','file_name':'policy.md','text':text,'sha256':sha,'scope':'excerpt'},'assessments':[]}
  self.package=self.root/'package.json';self.write()
 def tearDown(self):self.temp.cleanup()
 def write(self):self.package.write_text(json.dumps(self.value))
 def test_requires_explicit_publication_acknowledgement(self):
  with self.assertRaisesRegex(ValueError,'acknowledge'):site.import_submission(self.root,self.package,False)
  self.assertFalse((self.root/'docs/site/submissions').exists())
 def test_rejects_absent_owner_consent(self):
  self.value['publication_consent']['acknowledged']=False;self.write()
  with self.assertRaisesRegex(ValueError,'acknowledgement'):site.import_submission(self.root,self.package,True)
 def test_import_preserves_bytes_and_unverified_status(self):
  result=site.import_submission(self.root,self.package,True);self.assertEqual(result['status'],'proposal_imported')
  self.assertEqual((self.root/result['source_path']).read_bytes(),self.value['source']['text'].encode())
  record=json.loads((self.root/site.INDEX).read_text())['sources'][0]
  self.assertEqual(record['manifest']['citation_status'],'NOT_ESTABLISHED');self.assertEqual(record['reviewStatus'],'PROPOSED_SOURCE_NOT_VERIFIED_CORPUS')
  self.assertEqual(site.verify(self.root)['sources'],1)
 def test_duplicate_import_is_idempotent(self):
  site.import_submission(self.root,self.package,True);self.assertEqual(site.import_submission(self.root,self.package,True)['status'],'already_indexed')
  self.assertEqual(len(json.loads((self.root/site.INDEX).read_text())['sources']),1)
 def test_hash_mismatch_writes_nothing(self):
  self.value['source']['sha256']='0'*64;self.write()
  with self.assertRaisesRegex(ValueError,'hash'):site.import_submission(self.root,self.package,True)
  self.assertFalse((self.root/'docs/site/submissions').exists())
 def test_path_traversal_writes_nothing(self):
  self.value['source']['file_name']='../../protected.md';self.write()
  with self.assertRaisesRegex(ValueError,'filename'):site.import_submission(self.root,self.package,True)
  self.assertFalse((self.root/'docs/site/submissions').exists())
 def test_mismatched_assessment_source_rejected(self):
  self.value['assessments']=[{'sourceSha256':'0'*64,'revision':'1'*40}];self.write()
  with self.assertRaisesRegex(ValueError,'different source'):site.import_submission(self.root,self.package,True)
 def test_duplicate_json_keys_rejected(self):
  self.package.write_text('{"schema":"a","schema":"b"}')
  with self.assertRaisesRegex(ValueError,'Duplicate'):site.import_submission(self.root,self.package,True)
 def test_pdf_signature_and_original_bytes(self):
  pdf=b'%PDF-1.4\nsynthetic fixture\n';self.value['source'].pop('text');self.value['source'].update(file_name='example.pdf',binary_base64=base64.b64encode(pdf).decode(),sha256=hashlib.sha256(pdf).hexdigest());self.write()
  result=site.import_submission(self.root,self.package,True);self.assertEqual((self.root/result['source_path']).read_bytes(),pdf);self.assertEqual(site.verify(self.root)['sources'],1)
 def test_false_explanation_quote_rejected(self):
  result=site.import_submission(self.root,self.package,True);index=json.loads((self.root/site.INDEX).read_text());record=index['sources'][0]
  record['explainer']={'source_sha256':record['sha256'],'quotes':[{'start_char':0,'end_char':5,'exact_quote':'wrong'}]};(self.root/site.INDEX).write_text(json.dumps(index))
  with self.assertRaisesRegex(ValueError,'quote mismatch'):site.verify(self.root)
 def test_committed_index_and_39_source_quotes(self):
  result=site.verify(Path(__file__).resolve().parents[1]);self.assertEqual(result['sources'],16);self.assertEqual(result['verified_explanation_quotes'],39)

if __name__=='__main__':unittest.main()
