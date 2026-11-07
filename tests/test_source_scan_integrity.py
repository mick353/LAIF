"""Evidence retrieval boundaries and the pre-write cross-artifact gate."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import laif_process_document as p


class SourceScanIntegrityTests(unittest.TestCase):
    def test_full_stream_counts_and_spatially_diverse_witnesses(self):
        text = '\n\n'.join(f'Agency {i} must publish a public disclosure of its AI use.' for i in range(9))
        scan = p.source_control_scan(text)
        rows = [r for r in scan['observations'] if r['control_type'] == 'public_disclosure']
        self.assertEqual(scan['coverage']['matched_by_type']['public_disclosure'], 9)
        self.assertEqual(len(rows), 3)
        self.assertEqual([r['exact_quote'].split()[1] for r in rows], ['0', '4', '8'])
        self.assertEqual(scan['coverage']['complete_semantic_coverage'], 'NOT_ESTABLISHED')

    def test_recommendation_is_retained_without_mandatory_gate(self):
        scan = p.source_control_scan('Agencies should publish performance metrics.\n\nBefore deployment agencies should complete an assessment.')
        self.assertTrue(scan['observations'])
        self.assertTrue(all(row['language_signal'] == 'recommendation' for row in scan['observations']))
        self.assertFalse(any(row['control_type'] == 'deployment_gate' for row in scan['observations']))

    def test_table_choices_are_not_answers_or_clean_prose(self):
        text = '| Code | Question | Options |\n| --- | --- | --- |\n| C1 | Please provide safety evidence. | Provided | Not provided |\n| C2 | The manufacturer must publish performance metrics. | Yes | No |'
        scan = p.source_control_scan(text)
        self.assertFalse(scan['observations'])
        self.assertEqual(len(scan['requests']), 2)
        self.assertEqual(scan['requests'][0]['column_context']['exact_quote'], '| Code | Question | Options |')
        self.assertTrue(all(r['response_status'].startswith('NOT_INFERRED') for r in scan['requests']))
        for row in scan['requests']:
            self.assertEqual(text[row['start_char']:row['end_char']], row['exact_quote'])

    def test_framework_rows_and_late_requests_are_retained_with_limits(self):
        text = '\n'.join('| MEASURE 1.%s | Please provide evidence? | Yes | No |' % i for i in range(20))
        scan = p.source_control_scan(text)
        self.assertEqual(scan['coverage']['structured_rows_found'], 20)
        self.assertEqual(len(scan['requests']), 12)
        self.assertIn('MEASURE 1.19', scan['requests'][-1]['exact_quote'])
        self.assertEqual(len({r['request_id'] for r in scan['requests']}), 12)

    def test_oversized_candidate_is_disclosed_and_not_clipped(self):
        text = 'Agencies must publish ' + 'information ' * 400 + '.'
        scan = p.source_control_scan(text)
        self.assertEqual(scan['coverage']['oversized_candidates_requiring_review'], 1)
        self.assertFalse(scan['observations'])

    def test_recital_exclusion_and_pdf_page_mapping(self):
        text = 'Agencies shall publish a public disclosure.\n\nHAVE ADOPTED THIS REGULATION:\n\n<!-- PDF page 22 -->\nAgencies shall publish performance metrics.'
        scan = p.source_control_scan(text)
        self.assertTrue(scan['coverage']['recital_candidates_excluded'])
        self.assertTrue(scan['observations'])
        self.assertTrue(all(row['pdf_page'] == 22 for row in scan['observations']))

    def test_responsible_adjective_is_not_a_responsibility_assignment(self):
        text = 'Technology advances should be monitored towards AI that is trustworthy and responsible.'
        self.assertFalse(any(r['control_type'] == 'accountability' for r in p.source_control_scan(text)['observations']))
        text = 'AI actors should be accountable for the proper functioning of their systems.'
        self.assertTrue(any(r['control_type'] == 'accountability' for r in p.source_control_scan(text)['observations']))

    def test_invalid_witness_limit_rejected(self):
        for n in (0, 11):
            with self.subTest(n=n), self.assertRaises(ValueError): p.source_control_scan('Text.', n)

    def materials(self):
        text = 'Agencies must publish performance metrics.'
        scan = p.source_control_scan(text)
        assessment = {'source_control_observations': scan['observations'], 'source_evidence_requests': [], 'source_scan_coverage': scan['coverage']}
        materials = {'quote_bank': [{'quote_id': 'Q001', 'start_offset': 0, 'end_offset': len(text), 'exact_quote': text}],
                     'gaps': [{'source_evidence_quote_ids': ['Q001'], 'counterevidence_control_ids': [scan['observations'][0]['control_id']]}]}
        return text, assessment, materials

    def test_valid_materials_pass_gate(self):
        self.assertIsNone(p.validate_report_materials(*self.materials()))

    def test_corrupt_span_or_quote_rejected(self):
        for key, value in (('start_offset', -1), ('end_offset', True), ('exact_quote', 'invented')):
            text, a, m = self.materials(); m['quote_bank'][0][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(p.ExtractionError, 'source span'):
                p.validate_report_materials(text, a, m)

    def test_duplicate_ids_and_unresolved_references_rejected(self):
        text, a, m = self.materials(); m['quote_bank'].append(copy.deepcopy(m['quote_bank'][0]))
        with self.assertRaisesRegex(p.ExtractionError, 'duplicated'): p.validate_report_materials(text, a, m)
        for key in ('source_evidence_quote_ids', 'counterevidence_control_ids'):
            text, a, m = self.materials(); m['gaps'][0][key] = ['UNKNOWN']
            with self.subTest(key=key), self.assertRaisesRegex(p.ExtractionError, 'unknown evidence'):
                p.validate_report_materials(text, a, m)

    def test_coverage_overclaim_or_count_mismatch_rejected(self):
        for key, value in (('complete_semantic_coverage', 'COMPLETE'), ('retained_by_type', {})):
            text, a, m = self.materials(); a['source_scan_coverage'][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(p.ExtractionError, 'coverage metadata'):
                p.validate_report_materials(text, a, m)

    def test_partial_roman_list_is_not_complete_evidence(self):
        self.assertIsNotNone(p._incomplete_quote_reason('(v) when appropriate, its performance shall be recorded.'))
