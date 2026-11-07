"""Source-bound all-criterion review structure, output and independent-reader targets."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import laif_research_report as research
import laif_research_review as peer
from laif_criteria_review import criterion_template,validate_criteria_review
from scripts import laif_process_document as processor


class SubstantiveReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.source=self.root/'policy.md';self.source.write_bytes((ROOT/'docs/examples/vendor-policy.md').read_bytes())
        self.text=processor.extract_document(self.source,'builtin').text
        self.dossier=research.build_dossier(self.source);self.review=research.review_template(self.dossier,include_criteria=True)
        cr=self.review['criteria_review']
        cr.update({'analyst_id':'fixture-author','as_at_date':'2026-11-07','jurisdiction':'Synthetic, no legal authority',
          'assessed_role':'Example operator','document_scope':'Synthetic source, no operational evidence',
          'overall_reasoning':'The fixture does not establish deployment assurance.','limitations':'Development case, not independent validation.'})
        e=self.dossier['evidence'][0]
        for i,row in enumerate(cr['criteria'],1):
            row.update({'determination':'NOT_ESTABLISHED','reasoning':'The passage does not establish the complete criterion.',
              'framework_basis':'LAIF v1.2 criterion; synthetic test mapping.','applicability_reason':'An AI-assisted decision is described.',
              'scope_and_exceptions':'Separate controls may exist.','alternative_explanation':'Other evidence may supply the protection.',
              'closure_evidence':'Obtain applicable control and deployment evidence.',
              'source_excerpts':[{'evidence_id':f'C{i:03d}','exact_quote':e['exact_quote'],'start_char':e['start_char'],
                'end_char':e['end_char'],'context':'Shared fixture paragraph, not complete criterion evidence.'}]})
            if row['criterion_id']=='Q1':
                row['coupling']={'q1a':'IMPLICIT','q1b':'SOFT','protected_interest':'Service-user interests',
                  'restriction':'Assistant use in decisions','equivalent_normative_force':'Equivalent force remains unestablished.'}
        self.path=self.root/'review.json'

    def save(self):
        self.path.write_text(json.dumps(self.review),encoding='utf-8')

    def load(self):
        self.save();return processor.load_submitted_review(self.source,self.text,self.path)

    def cli(self,*extra):
        self.save()
        return subprocess.run([sys.executable,'-S',str(ROOT/'scripts/laif_process_document.py'),str(self.source),
          '--review-file',str(self.path),'--output-dir',str(self.root/'out'),*extra],capture_output=True,text=True)

    def test_unfilled_template_is_rejected(self):
        self.assertEqual(len(criterion_template()['criteria']),8)
        with self.assertRaises(ValueError):validate_criteria_review(criterion_template(),self.text)

    def test_all_criteria_addressed_does_not_grant_pass(self):
        r=self.load();self.assertTrue(r['criteria_review']['all_criteria_addressed'])
        self.assertIn('not that the Integrity Layer or Coherence Test passes',r['criteria_review']['boundary'])
        self.assertTrue(all(c['status']=='AUTHOR_DETERMINATION_SUPPLIED' for c in r['criteria_coverage']))

    def test_curated_spans_are_exact_and_distinct(self):
        for row in self.load()['criteria_review']['criteria']:
            e=row['source_excerpts'][0];self.assertEqual(self.text[e['start_char']:e['end_char']],e['exact_quote'])
            self.assertTrue(e['evidence_id'].startswith('C'));self.assertIn('CONTEXT_REQUIRES_REVIEW',e['evidence_status'])

    def test_bad_span_bool_and_fabrication_rejected(self):
        for key,value in (('start_char',-1),('end_char',True),('exact_quote','invented')):
            cr=copy.deepcopy(self.review['criteria_review']);cr['criteria'][0]['source_excerpts'][0][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'source span'):validate_criteria_review(cr,self.text)

    def test_duplicate_foreign_criteria_and_duplicate_evidence_rejected(self):
        for mode in ('duplicate','foreign','evidence'):
            cr=copy.deepcopy(self.review['criteria_review'])
            if mode=='duplicate':cr['criteria'][1]['criterion_id']='A.1'
            elif mode=='foreign':cr['criteria'][0]['criterion_id']='A.99'
            else:cr['criteria'][1]['source_excerpts'][0]['evidence_id']='C001'
            with self.subTest(mode=mode),self.assertRaises(ValueError):validate_criteria_review(cr,self.text)

    def test_reasoning_applicability_alternative_closure_required(self):
        for key in ('reasoning','framework_basis','applicability_reason','scope_and_exceptions','alternative_explanation','closure_evidence'):
            cr=copy.deepcopy(self.review['criteria_review']);cr['criteria'][0][key]=''
            with self.subTest(key=key),self.assertRaises(ValueError):validate_criteria_review(cr,self.text)

    def test_q1_classifications_and_relationship_required(self):
        for key in ('q1a','q1b','protected_interest','restriction','equivalent_normative_force'):
            cr=copy.deepcopy(self.review['criteria_review']);row=next(r for r in cr['criteria'] if r['criterion_id']=='Q1');del row['coupling'][key]
            with self.subTest(key=key),self.assertRaises(ValueError):validate_criteria_review(cr,self.text)

    def test_absent_pairing_cannot_be_affirmative(self):
        cr=self.review['criteria_review'];q=next(r for r in cr['criteria'] if r['criterion_id']=='Q1')
        q['determination']='SUPPORTED_IN_SCOPE';q['coupling']['q1a']='NONE'
        with self.assertRaisesRegex(ValueError,'conflicts'):validate_criteria_review(cr,self.text)

    def test_native_certification_labels_not_imported(self):
        self.review['criteria_review']['criteria'][0]['determination']='PASS'
        with self.assertRaisesRegex(processor.ExtractionError,'certification'):self.load()

    def test_not_applicable_requires_reason_and_source(self):
        row=self.review['criteria_review']['criteria'][3];row['determination']='NOT_APPLICABLE'
        self.assertEqual(self.load()['criteria_review']['criteria'][3]['determination'],'NOT_APPLICABLE')
        row['applicability_reason']=''
        with self.assertRaises(processor.ExtractionError):self.load()

    def test_stale_protocol_and_unbound_review_rejected(self):
        self.review['criteria_review_protocol_sha256']='0'*64
        with self.assertRaisesRegex(processor.ExtractionError,'protocol SHA-256'):self.load()
        self.review['criteria_review_protocol_sha256']=self.dossier['method']['criteria_review_protocol_sha256']
        for k in ('framework_source_sha256','toolkit_source_sha256','toolchain_fingerprint'):self.review.pop(k)
        with self.assertRaisesRegex(processor.ExtractionError,'current framework'):self.load()

    def test_partial_review_keeps_unassessed_and_strict_gate_fails_no_write(self):
        self.review['criteria_review']['criteria']=self.review['criteria_review']['criteria'][:2]
        self.assertEqual(sum(c['status']=='NOT_ASSESSED' for c in self.load()['criteria_coverage']),6)
        r=self.cli('--require-complete-review');self.assertEqual(r.returncode,2,r.stderr);self.assertFalse((self.root/'out').exists())

    def test_full_review_report_json_bundle_and_scores(self):
        r=self.cli('--require-complete-review');self.assertEqual(r.returncode,0,r.stderr)
        a=json.loads((self.root/'out/policy.laif.json').read_text())['assessment_result']
        b=json.loads((self.root/'out/analyst/policy/analyst_bundle.json').read_text())
        self.assertEqual(a['submitted_review'],b['submitted_review'])
        report=(self.root/'out/policy.laif.md').read_text()
        for v in ('Authored substantive LAIF criterion review','Q1a structural pairing','Equivalent normative force','Author-supplied documentary assessment: 8 of 8'):
            self.assertIn(v,report)
        base=subprocess.run([sys.executable,'-S',str(ROOT/'scripts/laif_process_document.py'),str(self.source),'--output-dir',str(self.root/'base')],capture_output=True,text=True)
        self.assertEqual(base.returncode,0,base.stderr)
        old=json.loads((self.root/'base/policy.laif.json').read_text())['assessment_result']
        self.assertEqual(a['overall_readiness_score'],old['overall_readiness_score'])
        self.assertEqual(a['source_provenance']['status'],'LOCAL_SOURCE_AUTHORITY_UNVERIFIED')

    def test_complete_preview_no_write(self):
        r=self.cli('--require-complete-review','--no-write','--print-report')
        self.assertEqual(r.returncode,0,r.stderr);self.assertIn('Authored substantive LAIF criterion review',r.stdout)
        self.assertFalse((self.root/'out').exists())

    def test_complete_gate_requires_file(self):
        r=subprocess.run([sys.executable,'-S',str(ROOT/'scripts/laif_process_document.py'),str(self.source),'--require-complete-review','--output-dir',str(self.root/'out')],capture_output=True,text=True)
        self.assertEqual(r.returncode,2);self.assertIn('needs a completed --review-file',r.stderr);self.assertFalse((self.root/'out').exists())

    def test_native_mode_remains_protected(self):
        r=self.cli('--mode','laif_native','--require-complete-review')
        self.assertEqual(r.returncode,2);self.assertIn('cannot override native certification',r.stderr)

    def test_markup_is_inert(self):
        self.review['criteria_review']['overall_reasoning']='<script>run()</script> ![pixel](https://example.test/p)'
        report='\n'.join(processor.criteria_review_sections(self.load()['criteria_review']))
        self.assertNotIn('<script>',report);self.assertNotIn('![pixel]',report)

    def test_date_author_and_excerpt_context_required(self):
        for mode in ('date','author','context'):
            cr=copy.deepcopy(self.review['criteria_review'])
            if mode=='date':cr['as_at_date']='2026-02-30'
            elif mode=='author':cr['analyst_id']=''
            else:cr['criteria'][0]['source_excerpts'][0]['context']=''
            with self.subTest(mode=mode),self.assertRaises(ValueError):validate_criteria_review(cr,self.text)

    def test_second_readers_receive_criteria_and_curated_evidence(self):
        self.save();d=research.build_dossier(self.source,review_file=self.path)
        p=self.root/'dossier.json';p.write_text(json.dumps(d));_,digest,targets=peer.load_dossier(p)
        self.assertEqual(sum(k.startswith('CR-') for k in targets),8)
        self.assertEqual(sum(k.startswith('C0') for k in targets),8)
        t=peer.review_template(digest,targets)
        self.assertTrue(all(r['verdict']=='uncertain' for r in t['ratings'] if r['target_id'].startswith('CR-')))

    def test_changed_criterion_invalidates_second_reader(self):
        self.save();d=research.build_dossier(self.source,review_file=self.path)
        p=self.root/'dossier.json';p.write_text(json.dumps(d));_,digest,targets=peer.load_dossier(p)
        r=peer.review_template(digest,targets);r['reviewer_id']='fixture-reader';rp=self.root/'second.json';rp.write_text(json.dumps(r))
        d['criteria_review']['criteria'][0]['reasoning']='Changed reasoning';p.write_text(json.dumps(d));_,new_digest,new_targets=peer.load_dossier(p)
        with self.assertRaisesRegex(research.ResearchInputError,'hash mismatch'):peer.validate_review(rp,new_digest,new_targets)


class ActualSubstantiveSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

    def cases(self):
        for key in ('au_dta_policy_v2_1','5f667a6f-NIST.AI.1001'):
            m=json.loads((ROOT/'docs/verified/manifests'/f'{key}.json').read_text())
            yield key,m,ROOT/'docs/verified/raw'/m['raw_filename'],ROOT/'docs/verification/2026-11-07-substantive-review'/key/'completed-review.json'

    def test_actual_sources_all_criteria_coupling_and_limits(self):
        for key,m,source,path in self.cases():
            with self.subTest(key=key):
                out=self.root/key
                r=subprocess.run([sys.executable,'-S',str(ROOT/'scripts/laif_process_document.py'),str(source),'--review-file',str(path),'--require-complete-review','--output-dir',str(out)],capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stderr)
                a=json.loads((out/(source.stem+'.laif.json')).read_text())['assessment_result'];cr=a['submitted_review']['criteria_review']
                self.assertEqual(len(cr['criteria']),8);self.assertTrue(cr['all_criteria_addressed'])
                self.assertEqual(a['source_provenance']['verification_status'],m['verification_status'])
                self.assertIn('Author-supplied documentary assessment: 8 of 8',(out/(source.stem+'.laif.md')).read_text())
                if key.startswith('au_'):self.assertIsNotNone(a['attributed_reasoning'])
                else:self.assertIn('not independently verified',cr['limitations'].lower())

    def test_actual_evidence_second_reader_targets(self):
        for key,_,source,path in self.cases():
            with self.subTest(key=key):
                d=research.build_dossier(source,review_file=path);p=self.root/(key+'.json');p.write_text(json.dumps(d))
                _,_,targets=peer.load_dossier(p);self.assertEqual(sum(k.startswith('CR-') for k in targets),8)
                self.assertGreaterEqual(sum(k.startswith('C0') for k in targets),16)
                self.assertEqual(d['independent_replication'],'NOT_PERFORMED')

    def test_actual_fabricated_curated_quote_rejected_before_write(self):
        for key,_,source,path in self.cases():
            with self.subTest(key=key):
                raw=json.loads(path.read_text());raw['criteria_review']['criteria'][0]['source_excerpts'][0]['exact_quote']='Fabricated proof'
                p=self.root/(key+'.json');p.write_text(json.dumps(raw));out=self.root/(key+'-bad')
                r=subprocess.run([sys.executable,'-S',str(ROOT/'scripts/laif_process_document.py'),str(source),'--review-file',str(p),'--require-complete-review','--output-dir',str(out)],capture_output=True,text=True)
                self.assertEqual(r.returncode,2);self.assertIn('source span',r.stderr);self.assertFalse(out.exists())
