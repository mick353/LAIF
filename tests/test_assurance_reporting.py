"""Readable policy-to-evidence reports and strict JSON ingestion boundaries."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
from test_assurance import AssuranceFixture
from laif_assurance import assess_assurance, render_assurance_report
from laif_evidence_checks import read_json_object
from laif_calibration import calibrate, make_synthetic_corpus


class AssuranceReportingTests(AssuranceFixture):
    def report(self, **kw):
        return render_assurance_report(assess_assurance(self.manifest, self.root, **kw))

    def cli(self, *extra):
        path = self.root / 'manifest.json'
        path.write_bytes(json.dumps(self.manifest).encode('utf-8'))
        return subprocess.run([sys.executable, '-S', str(ROOT / 'scripts/laif_assurance.py'), str(path), *extra], capture_output=True, text=True)

    def test_claim_receipts_and_limits_are_readable(self):
        report = self.report(strict_scope=True, strict_actions=True)
        for expected in (self.policy.strip(), 'EXECUTION_RECEIPT_CHECKED', 'simulated', 'test-positive-run', 'not independently observed execution', 'Operational review and remedy'):
            self.assertIn(expected, report.replace("\\", ""))
        self.assertIn(self.policy_sha, report)
        self.assertEqual(self.run_assurance()['operational_annex']['status'], 'NOT_SUPPLIED')

    def test_source_only_does_not_look_operationally_verified(self):
        self.control['execution_tests'] = []
        report = self.report(strict_scope=True, strict_actions=True)
        self.assertIn('POLICY_CLAIM_ONLY', report.replace('\\', ''))
        self.assertIn('INCOMPLETE_CONTROLS', report.replace('\\', ''))
        self.assertIn('No validated action receipts', report)
        self.assertIn('NOT_SUPPLIED', report.replace('\\', ''))

    def test_adverse_record_cannot_be_hidden_by_passing_operational_annex(self):
        entry = self.control['execution_tests'][1]
        receipt = json.loads((self.root / entry['receipt_file']).read_text()); receipt['decision'] = 'ALLOW'
        entry['receipt_sha256'] = self.write(entry['receipt_file'], receipt)
        report = self.report(annex=self.annex(), strict_scope=True, strict_actions=True)
        self.assertIn('OBSERVED_FAILURE', report.replace('\\', ''))
        self.assertIn('REVIEW_RECORDED', report.replace('\\', ''))
        self.assertIn('Resolve the source or test evidence gaps', report)

    def test_operational_remedy_need_and_attribution_visible(self):
        report = self.report(annex=self.annex(outcome='FAIL'))
        self.assertIn('RETEST_REQUIRED', report.replace('\\', ''))
        self.assertIn('operator-A', report)
        self.assertIn('reviewer-B', report)
        self.assertIn('deploy-0001', report)
        self.assertIn('recorded', report)

    def test_source_inventory_failure_is_explicit(self):
        self.manifest['source_inventory'][0]['sha256'] = '0'*64
        report = self.report(strict_scope=True)
        self.assertIn('SHA-256 mismatch', report)
        self.assertIn('NOT_ESTABLISHED', report.replace('\\', ''))

    def test_missing_scope_and_empty_controls_are_not_ready_claims(self):
        del self.manifest['source_inventory']; self.manifest['controls'] = []
        report = self.report(strict_scope=True)
        self.assertIn('No controls supplied', report)
        self.assertIn('No supporting source inventory', report)
        self.assertIn('Controls supplied: 0', report)

    def test_untrusted_source_markup_does_not_become_active_markup(self):
        claim = '<script>run()</script> ![pixel](https://example.test/pixel)'
        self.manifest['policy_sha256'] = self.write('policy.md', claim)
        self.control['claim_quote'] = claim
        report = self.report()
        self.assertNotIn('<script>', report)
        self.assertNotIn('![pixel]', report)
        self.assertIn('&lt;script&gt;', report)

    def test_default_stdout_is_json_and_report_option_preserves_outcome(self):
        first = self.cli(); out = self.root / 'out/report.md'
        second = self.cli('--markdown-report', str(out))
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(first.stdout), json.loads(second.stdout))
        self.assertIn('# Control evidence review', out.read_text())

    def test_print_report_is_no_write_and_deterministic(self):
        self.cli(); before = {p.name:p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        first = self.cli('--print-report'); second = self.cli('--print-report')
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.root.iterdir() if p.is_file()})

    def test_failure_gate_still_writes_honest_diagnostic(self):
        self.control['execution_tests'] = []
        out = self.root / 'failure.md'
        result = self.cli('--require-review-ready', '--markdown-report', str(out))
        self.assertEqual(result.returncode, 1)
        self.assertIn('INCOMPLETE_CONTROLS', out.read_text().replace('\\', ''))

    def test_report_cannot_overwrite_inputs_or_hardlink_to_them(self):
        for name in ('manifest.json', 'policy.md', 'test-positive.json'):
            with self.subTest(name=name):
                target = self.root / name
                self.cli(); before = target.read_bytes()
                result = self.cli('--markdown-report', str(target))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(before, target.read_bytes())
        target = self.root / 'alias.md'; os.link(self.root / 'policy.md', target)
        result = self.cli('--markdown-report', str(target))
        self.assertEqual(result.returncode, 2)
        self.assertIn('overwrite an input', result.stderr)

    def test_duplicate_receipt_fields_are_invalid_even_with_matching_hash(self):
        entry = self.control['execution_tests'][0]
        raw = (self.root / entry['receipt_file']).read_text().replace('"decision": "ALLOW"', '"decision": "BLOCK", "decision": "ALLOW"')
        entry['receipt_sha256'] = self.write(entry['receipt_file'], raw)
        row = self.run_assurance()
        self.assertEqual(row['status'], 'EVIDENCE_INVALID')
        self.assertTrue(any('duplicate key' in issue for issue in row['issues']))

    def test_nonfinite_receipt_field_invalidates_receipt(self):
        entry = self.control['execution_tests'][0]
        raw = (self.root / entry['receipt_file']).read_text().rstrip().replace('{', '{"untrusted":1e999,', 1)
        entry['receipt_sha256'] = self.write(entry['receipt_file'], raw)
        self.assertEqual(self.run_assurance()['status'], 'EVIDENCE_INVALID')

    def test_nested_ambiguity_nonfinite_and_nonobject_inputs_rejected(self):
        for raw in ('{"x":{"outcome":"FAIL","outcome":"PASS"}}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}', '{"x":1e999}', '[]'):
            with self.subTest(raw=raw), self.assertRaises(ValueError): read_json_object(raw)
        self.assertEqual(read_json_object('{"threshold":0.05,"count":3}'), {'threshold':0.05,'count':3})

    def test_all_assurance_clis_reject_ambiguous_top_level_json(self):
        path = self.root / 'ambiguous.json'; path.write_text('{"controls":[],"controls":[]}')
        for script in ('laif_assurance.py', 'laif_evidence_checks.py', 'laif_calibration.py', 'laif_frontier_assurance.py'):
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, '-S', str(ROOT / 'scripts' / script), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn('duplicate key', result.stderr)

    def test_invalid_manifest_writes_no_report(self):
        path = self.root / 'invalid.json';path.write_text('{"controls":[],"controls":[]}')
        out = self.root / 'report.md'
        result = subprocess.run([sys.executable, '-S', str(ROOT / 'scripts/laif_assurance.py'), str(path), '--markdown-report', str(out)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(out.exists())

    def test_calibration_pinned_case_manifest_rejects_duplicate_fields(self):
        path = make_synthetic_corpus(self.root / 'calibration')
        dataset = json.loads(path.read_text()); case = dataset['cases'][0]
        manifest_path = path.parent / case['manifest_file']
        raw = manifest_path.read_text().replace('{', '{"duplicate":1,"duplicate":2,', 1)
        case['manifest_sha256'] = self.write(str(manifest_path.relative_to(self.root)), raw)
        with self.assertRaisesRegex(ValueError, 'duplicate key'):
            calibrate(dataset, path.parent)

    def test_explicit_root_supports_nested_manifest_and_confines_paths(self):
        nested = self.root / 'records'; nested.mkdir()
        path = nested / 'manifest.json';path.write_bytes(json.dumps(self.manifest).encode('utf-8'))
        common = [sys.executable, '-S', str(ROOT / 'scripts/laif_assurance.py'), str(path)]
        missing = subprocess.run(common, capture_output=True, text=True)
        valid = subprocess.run(common + ['--evidence-root', str(self.root), '--print-report'], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertIn('Control evidence review', valid.stdout)
        self.manifest['policy_file'] = '../outside.md'
        path.write_bytes(json.dumps(self.manifest).encode('utf-8'))
        invalid = subprocess.run(common + ['--evidence-root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 2)
        self.assertIn('escapes evidence directory', invalid.stderr)

    def test_actual_dta_policy_claim_stays_policy_only(self):
        path = ROOT / 'docs/verification/2026-11-07-control-evidence-reporting/actual-dta-policy-only.manifest.json'
        result = assess_assurance(read_json_object(path.read_text()), ROOT, strict_scope=True, strict_actions=True)
        row = result['controls'][0]
        self.assertEqual(row['evidence_grade'], 'POLICY_CLAIM_ONLY')
        self.assertEqual(row['status'], 'SCOPE_UNDECLARED')
        self.assertEqual(row['evidence_trace']['claim_status'], 'EXACT_POLICY_TEXT_CHECKED')
        self.assertEqual(row['operational_annex']['status'], 'NOT_SUPPLIED')

    def test_actual_release_records_are_not_action_receipts(self):
        path = ROOT / 'docs/verification/2026-11-07-control-evidence-reporting/actual-release-records.manifest.json'
        result = assess_assurance(read_json_object(path.read_text()), ROOT, strict_scope=True, strict_actions=True)
        row = result['controls'][0]
        self.assertEqual(row['original_status'], 'REVIEW_READY')
        self.assertEqual(row['status'], 'EXECUTION_UNTESTED')
        self.assertEqual(row['evidence_grade'], 'DECLARED_TEST_RECORDS')
        self.assertFalse(row['execution_cases'])
        self.assertTrue(all(s['validation_status'] == 'EXACT_SOURCE_CHECKED' for s in result['source_inventory']))
