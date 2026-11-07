"""Whole-document workflow regression over every retained raw corpus source.

Known, curated development cases; neither blinded nor an accuracy benchmark.
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from scripts import laif_process_document as processor
from real_source_support import CASES, case_review


class RealSourceReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.records = {}
        for key in CASES:
            manifest, source, review = case_review(key)
            folder = Path(cls.temp.name) / key
            folder.mkdir()
            review_path = folder / 'review.json'
            review_path.write_text(json.dumps(review), encoding='utf-8')
            common = [sys.executable, '-S', str(ROOT / 'scripts/laif_process_document.py'), str(source),
                      '--extractor', 'builtin', '--document-name', manifest['title'], '--source-type', manifest['source_type']]
            results = {}
            for mode in ('default', 'reviewed'):
                out = folder / mode
                args = common + ['--output-dir', str(out)]
                if mode == 'reviewed': args += ['--review-file', str(review_path)]
                result = subprocess.run(args, capture_output=True, text=True)
                if result.returncode:
                    raise AssertionError(f'{key}/{mode}: {result.stderr}')
                data = json.loads((out / (source.stem + '.laif.json')).read_text(encoding='utf-8'))
                bundle = json.loads((out / 'analyst' / source.stem / 'analyst_bundle.json').read_text(encoding='utf-8'))
                report = (out / (source.stem + '.laif.md')).read_text(encoding='utf-8')
                results[mode] = (data['assessment_result'], bundle, report)
            cls.records[key] = (manifest, source, review, common, folder, results)

    def test_every_manifest_is_exercised_without_changing_admission(self):
        self.assertEqual(set(CASES), {p.stem for p in (ROOT / 'docs/verified/manifests').glob('*.json')})
        for key, (manifest, source, _, _, _, results) in self.records.items():
            with self.subTest(key=key):
                a, bundle, report = results['default']
                self.assertEqual(processor.sha256_file(source), manifest['sha256_hash'])
                self.assertEqual(a['source_provenance']['verification_status'], manifest['verification_status'])
                self.assertEqual(a['source_provenance'], bundle['source_provenance'])
                self.assertIn(manifest['verification_status'], report)
                self.assertIn(manifest['provenance_notes'].split('.')[0], report.replace('\\', ''))

    def test_real_source_annotations_reach_all_three_outputs(self):
        for key, (_, _, review, _, _, results) in self.records.items():
            with self.subTest(key=key):
                a, bundle, report = results['reviewed']
                self.assertEqual(a['submitted_review'], bundle['submitted_review'])
                self.assertIn('NOT_INDEPENDENTLY_VERIFIED', a['submitted_review']['status'])
                for finding in review['findings']:
                    self.assertIn(finding['statement'], report)
                covered = {c for f in review['findings'] for c in f['criterion_ids']}
                self.assertEqual(len(a['submitted_review']['criteria_coverage']), 8)
                for row in a['submitted_review']['criteria_coverage']:
                    self.assertEqual(row['status'] == 'NOT_ASSESSED', row['criterion_id'] not in covered)

    def test_every_retained_quote_and_control_matches_whole_source(self):
        for key, (_, source, _, _, _, results) in self.records.items():
            text = processor.extract_document(source, 'builtin').text
            with self.subTest(key=key):
                a, bundle, _ = results['reviewed']
                materials = {'quote_bank': bundle['quote_bank'], 'gaps': bundle['gap_register']}
                processor.validate_report_materials(text, a, materials)
                for row in bundle['quote_bank']:
                    self.assertNotIn('|', row['exact_quote'])
                for row in a['source_control_observations']:
                    self.assertNotIn('|', row['exact_quote'])
                for row in a['submitted_review']['evidence']:
                    self.assertEqual(text[row['start_char']:row['end_char']], row['exact_quote'])

    def test_review_does_not_override_scores_or_existing_attributed_reasoning(self):
        for key, (_, _, _, _, _, results) in self.records.items():
            with self.subTest(key=key):
                default, _, _ = results['default']; reviewed, _, _ = results['reviewed']
                for field in ('overall_readiness_score', 'structural_score', 'formal_category', 'source_provenance', 'attributed_reasoning'):
                    self.assertEqual(default.get(field), reviewed.get(field))

    def test_source_specific_table_version_and_scope_boundaries(self):
        dtac = self.records['55eccce3-DTAC_Form_2.0_February_2026'][-1]['default'][0]
        self.assertFalse(dtac['source_control_observations'])
        self.assertGreater(dtac['source_scan_coverage']['request_rows_found'], 12)
        self.assertTrue(any(row['column_context'] for row in dtac['source_evidence_requests']))
        self.assertTrue(all(row['response_status'].startswith('NOT_INFERRED') for row in dtac['source_evidence_requests']))
        nist = self.records['5f667a6f-NIST.AI.1001'][-1]['default'][0]
        self.assertTrue(any(row['row_kind'] == 'framework_practice' for row in nist['source_evidence_requests']))
        self.assertTrue(any(row['language_signal'] == 'recommendation' for row in nist['source_control_observations']))
        eo = self.records['b0ef43db-202324283'][-1]['default']
        self.assertIn('HISTORICAL_REVOKED', eo[2].replace('\\', ''))
        eu = self.records['eu-ai-act-2024-1689'][-1]['default']
        self.assertIn('ORIGINAL_EDITION_NOT_CONSOLIDATED', eu[2].replace('\\', ''))
        self.assertEqual(eu[0]['source_scan_coverage']['complete_semantic_coverage'], 'NOT_ESTABLISHED')
        self.assertGreater(eu[0]['source_scan_coverage']['recital_candidates_excluded'], 0)
        self.assertTrue(any(n > eu[0]['source_scan_coverage']['selection_limit_per_type'] for n in eu[0]['source_scan_coverage']['matched_by_type'].values()))
        self.assertEqual(json.loads((ROOT / 'docs/verified/manifests/eu-ai-act-2024-1689.json').read_text())['assessment_status'], 'PENDING_ASSESSMENT')

    def test_all_real_sources_preview_same_findings_without_writes(self):
        for key, (_, _, review, common, folder, _) in self.records.items():
            with self.subTest(key=key):
                out = folder / 'preview'
                result = subprocess.run(common + ['--review-file', str(folder / 'review.json'), '--no-write', '--print-report', '--output-dir', str(out)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(out.exists())
                for finding in review['findings']: self.assertIn(finding['statement'], result.stdout)

    def test_all_real_sources_reject_foreign_evidence_before_writes(self):
        for key, (_, _, review, common, folder, _) in self.records.items():
            with self.subTest(key=key):
                invalid = copy.deepcopy(review)
                invalid['findings'][0]['evidence_ids'] = ['E999']
                path = folder / 'invalid.json'; path.write_text(json.dumps(invalid), encoding='utf-8')
                out = folder / 'invalid-output'
                result = subprocess.run(common + ['--review-file', str(path), '--output-dir', str(out)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(out.exists())
                self.assertIn('existing evidence IDs', result.stderr)
