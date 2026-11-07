"""Source-bound review import on generic local inputs; no reviewer authority implied."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
from scripts import laif_process_document as processor
import laif_research_report as research


class PortableAnalystReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / 'supplier-policy.md'
        self.source.write_bytes((ROOT / 'docs/examples/vendor-policy.md').read_bytes())
        self.dossier = research.build_dossier(self.source)
        self.review = research.review_template(self.dossier)
        self.review['findings'] = [{
            'finding_id': 'F001', 'claim_type': 'INFERENCE',
            'statement': 'Synthetic workflow test: the quoted duty needs implementation evidence.',
            'evidence_ids': [self.review['available_evidence_ids'][0]], 'counterevidence_ids': [],
            'alternative_explanations': ['A separate procedure may provide the implementation evidence.'],
            'limitations': 'Synthetic source; this test does not establish legal or operational validity.',
            'analyst_id': 'synthetic-test-analyst', 'criterion_ids': ['Q1']
        }]
        self.path = self.root / 'review.json'

    def tearDown(self):
        self.temp.cleanup()

    def save(self, value=None):
        self.path.write_text(json.dumps(self.review if value is None else value))

    def load(self, value=None, text=None):
        self.save(value)
        return processor.load_submitted_review(self.source,
            processor.extract_document(self.source, 'builtin').text if text is None else text, self.path)

    def cli(self, *extra):
        return subprocess.run([sys.executable, '-S', str(ROOT / 'scripts/laif_process_document.py'),
                               str(self.source), '--review-file', str(self.path),
                               '--output-dir', str(self.root / 'output'), *extra], capture_output=True, text=True)

    def test_generic_review_reaches_report_json_bundle_and_coverage(self):
        self.save(); result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.root / 'output/supplier-policy.laif.json').read_text())
        review = data['assessment_result']['submitted_review']
        bundle = json.loads((self.root / 'output/analyst/supplier-policy/analyst_bundle.json').read_text())
        self.assertEqual(review, bundle['submitted_review'])
        self.assertIn('NOT_INDEPENDENTLY_VERIFIED', review['status'])
        report = (self.root / 'output/supplier-policy.laif.md').read_text()
        self.assertIn('Submitted analyst findings', report)
        self.assertIn('synthetic-test-analyst', report)
        self.assertIn('A separate procedure', report)
        q2 = next(row for row in review['criteria_coverage'] if row['criterion_id'] == 'Q2')
        self.assertEqual(q2['status'], 'NOT_ASSESSED')
        self.assertEqual(data['assessment_result']['source_provenance']['status'], 'LOCAL_SOURCE_AUTHORITY_UNVERIFIED')
        for row in review['evidence']:
            self.assertEqual(self.source.read_text()[row['start_char']:row['end_char']], row['exact_quote'])

    def test_source_change_rejected_before_outputs(self):
        self.save();self.source.write_text(self.source.read_text() + '\nChanged duty.')
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn('SHA-256', result.stderr)
        self.assertFalse((self.root / 'output').exists())

    def test_stale_method_identity_rejected(self):
        for key in ('framework_source_sha256', 'toolkit_source_sha256', 'toolchain_fingerprint'):
            data=copy.deepcopy(self.review);data[key]='0'*64
            with self.subTest(key=key), self.assertRaisesRegex(processor.ExtractionError, 'SHA-256'):
                self.load(data)

    def test_legacy_unbound_review_cannot_be_promoted(self):
        data=copy.deepcopy(self.review)
        for key in ('framework_source_sha256','toolkit_source_sha256','toolchain_fingerprint'): del data[key]
        with self.assertRaisesRegex(processor.ExtractionError, 'requires current'):
            self.load(data)

    def test_wrong_or_reordered_inventory_rejected(self):
        for mode in ('hash', 'ids'):
            data=copy.deepcopy(self.review)
            if mode=='hash': data['evidence_manifest_sha256']='0'*64
            else:data['available_evidence_ids'].reverse()
            with self.subTest(mode=mode), self.assertRaises(processor.ExtractionError):self.load(data)

    def test_extractor_mismatch_rejected(self):
        with self.assertRaisesRegex(processor.ExtractionError,'extracted texts differ'):
            self.load(text='Different normalised extraction')

    def test_blank_template_is_not_an_assessment(self):
        data=copy.deepcopy(self.review);data['findings']=[]
        with self.assertRaisesRegex(processor.ExtractionError,'no findings'):self.load(data)

    def test_foreign_and_duplicate_finding_ids_rejected(self):
        for mode in ('foreign', 'duplicate'):
            data=copy.deepcopy(self.review)
            if mode=='foreign':data['findings'][0]['evidence_ids']=['E999']
            else:data['findings'].append(copy.deepcopy(data['findings'][0]))
            with self.subTest(mode=mode), self.assertRaises(processor.ExtractionError):self.load(data)

    def test_json_ambiguity_and_nonfinite_values_rejected(self):
        for raw in ('{"findings":[],"findings":[]}', '{"value":NaN}'):
            self.path.write_text(raw)
            with self.subTest(raw=raw), self.assertRaises(processor.ExtractionError):
                processor.load_submitted_review(self.source,self.source.read_text(),self.path)

    def test_submitted_markup_is_inert_and_claim_does_not_gain_authority(self):
        data=copy.deepcopy(self.review)
        data['findings'][0]['statement']='<script>alert(1)</script> ![pixel](https://example.test/pixel)'
        data['independence_declaration']='independently_validated'
        review=self.load(data);report='\n'.join(processor.submitted_review_sections(review))
        self.assertNotIn('<script>',report);self.assertNotIn('![pixel]',report)
        self.assertNotIn('independently_validated',report)
        self.assertIn('not authenticated',report)

    def test_native_certification_cannot_be_overridden(self):
        self.save();result=self.cli('--mode','laif_native')
        self.assertEqual(result.returncode,2)
        self.assertIn('cannot override native certification',result.stderr)
        self.assertFalse((self.root / 'output').exists())

    def test_changed_review_snapshot_and_source_identity_rejected(self):
        self.save()
        text=processor.extract_document(self.source, 'builtin').text
        with patch.object(processor, 'sha256_file', side_effect=['0'*64,'1'*64]), self.assertRaisesRegex(processor.ExtractionError, 'changed during validation'):
            processor.load_submitted_review(self.source,text,self.path)
        with self.assertRaisesRegex(processor.ExtractionError, 'source changed during processing'):
            processor.load_submitted_review(self.source,text,self.path,'0'*64)

    def test_preview_matches_review_surface_without_writes(self):
        self.save();result=self.cli('--no-write','--print-report')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Submitted analyst findings',result.stdout)
        self.assertFalse((self.root / 'output').exists())
