"""Broader development challenges; deliberately not an independent benchmark."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import laif_process_document as runner
from assessment_engine import assess


class ReportingChallengeTests(unittest.TestCase):
    def test_sixteen_declared_gate_challenges(self):
        fixture = json.loads((ROOT / 'tests/fixtures/deployment_gate_challenges.json').read_text())
        for case in fixture['cases']:
            with self.subTest(case=case['id']):
                rows = runner.source_control_observations(case['text'])
                gates = [r for r in rows if r['control_type'] == 'deployment_gate']
                self.assertEqual(bool(gates), case['gate'])
                for row in gates:
                    self.assertEqual(case['text'][row['start_char']:row['end_char']], row['exact_quote'])

    def test_recital_and_operative_evidence_are_distinguished(self):
        text = ('Providers shall assess risks and maintain documentation of risks before deployment.\n\n'
                'HAVE ADOPTED THIS REGULATION:\n\n'
                'Providers shall complete an independent safety assessment before deployment.')
        result = assess('Test Act', 'binding_regulation', text, assessment_mode='external_framework')
        bank = runner.build_quote_bank(text, {'source_sha256': '0'*64},
                                       {'extractor_used': 'builtin', 'extraction_confidence': 'high'}, result)
        self.assertTrue(bank)
        self.assertEqual(bank[0]['passage_role'], 'operative_text')
        for row in bank:
            self.assertEqual(text[row['start_offset']:row['end_offset']], row['exact_quote'])
            if row['passage_role'] == 'recital_context':
                self.assertIn('not itself an operative duty', row['what_it_does_not_prove'])

    def test_recital_role_is_not_disguised_when_no_operative_quote_is_eligible(self):
        text = ('Providers shall assess risks and maintain documentation before deployment.\n\n'
                'HAVE ADOPTED THIS REGULATION:\n\nArticle 1\nScope.')
        self.assertEqual(runner.source_passage_role(text, 0), 'recital_context')
        self.assertEqual(runner.source_passage_role(text, text.index('Article 1')), 'operative_text')
        self.assertFalse(runner.source_control_observations(text))

    def test_commission_singular_adoption_header_is_also_recognised(self):
        text = ('Providers shall assess risks before deployment.\n\n'
                'HAS ADOPTED THIS REGULATION:\n\nArticle 1\nScope.')
        self.assertEqual(runner.source_passage_role(text, 0), 'recital_context')
        self.assertFalse(runner.source_control_observations(text))

    def test_conditional_gate_with_negated_completion_not_promoted(self):
        text = 'The agency must not deploy until its risk assessment is not complete.'
        self.assertFalse(runner._conditional_deployment_gate(text))

    def test_preview_leads_with_assessment_and_keeps_metadata_available(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td)/'policy.md'
            source.write_text('Deployment is prohibited unless the independent safety assessment is approved.')
            proc = subprocess.run([sys.executable, str(ROOT/'scripts/laif_process_document.py'), str(source),
                                   '--no-write', '--print-report'], capture_output=True, text=True, check=True)
            report = proc.stdout[proc.stdout.index('# Institutional Governance Assessment'):]
            self.assertLess(report.index('## Executive finding'), report.index('## Document Processing Metadata'))
            self.assertIn('Source SHA-256', report)
