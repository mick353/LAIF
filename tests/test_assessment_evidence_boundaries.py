"""Regressions for defects observed while assessing the PR #98 sources."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from assessment_engine import assess, integrity_requirement_diagnostics
from laif_spec import INTEGRITY_LAYER
from scripts import laif_process_document as runner


class AssessmentEvidenceBoundaryTests(unittest.TestCase):
    def test_json_remediation_does_not_turn_missing_patterns_into_failure(self):
        result = assess("Policy", "policy", "Agencies must identify AI risks and assign an owner.", assessment_mode="external_framework")
        narrative = json.dumps({k: result[k] for k in ("plain_reading", "structured_findings", "structured_remediation_steps", "score_trace")})
        self.assertNotIn("This dimension is absent from the document", narrative)
        self.assertNotIn("no governance restriction is bound", narrative)
        self.assertNotIn("restrictions not bound to human interests", narrative)
        self.assertNotIn("Q1 (Coupling) failure = automatic", narrative)
        self.assertIn("source", narrative.lower())

    def test_dangling_complement_cannot_be_primary_evidence(self):
        incomplete = "That technical documentation shall demonstrate that the high-risk AI system"
        complete = incomplete + " complies with the applicable requirements."
        self.assertFalse(runner.quote_has_complete_evidence_proposition(incomplete)[0])
        self.assertTrue(runner.quote_has_complete_evidence_proposition(complete)[0])
        self.assertTrue(runner._incomplete_quote_reason("The AI Office shall review systems referred to in"))

    def test_pdf_line_prefix_expands_to_retain_source_qualifier(self):
        prefix = "Providers shall train their staff"
        text = prefix + "\nand other persons using AI on their behalf, taking account of the use context."
        start, end, quote = runner._expand_incomplete_candidate(text, 0, len(prefix), prefix)
        self.assertEqual(text[start:end], quote)
        self.assertIn("other persons", quote)
        self.assertIn("use context.", quote)

    def test_all_four_properties_reported_without_inventing_passes(self):
        text = "Agencies must name an accountable official and maintain a register."
        result = assess("Government policy", "sector_policy", text, assessment_mode="external_framework")
        records = result["integrity_requirement_diagnostics"]
        self.assertEqual({r["property"] for r in records}, set(INTEGRITY_LAYER.values()))
        self.assertEqual(len(records), 4)
        self.assertEqual(result["substantive_coherence_determination"], "REQUIRES_SOURCE_BASED_REVIEW")
        self.assertTrue(all(r["determination"] == "NOT_ASSESSED_BY_PATTERN_MATCHING" for r in records))

    def test_calibration_evidence_has_exact_trace_and_no_score_claim(self):
        text = "Providers must verify expressed confidence against observed accuracy in deployment."
        record = integrity_requirement_diagnostics(text)[3]
        self.assertEqual(record["signal_status"], "DETECTED_REQUIRES_REVIEW")
        self.assertEqual(text[record["start_char"]:record["end_char"]], record["matched_text"])
        self.assertIn("2.5 trigger", record["applicability"])
        self.assertNotIn("score", record)

    def test_calibration_name_alone_does_not_establish_the_property(self):
        record = integrity_requirement_diagnostics("Structural Calibration is important.")[3]
        self.assertEqual(record["signal_status"], "NOT_DETECTED_REQUIRES_REVIEW")
        self.assertEqual(record["determination"], "NOT_ASSESSED_BY_PATTERN_MATCHING")

    def test_detector_miss_does_not_claim_absent_protection(self):
        result = assess("Policy", "sector_policy", "Agencies must record AI risks and appoint an owner.", assessment_mode="external_framework")
        report = runner.build_institutional_report({"safe_output_stem": "policy"}, {}, result, [], [], [], [])
        self.assertNotIn("missing machinery, not missing terminology", report)
        self.assertNotIn("does not express the load-bearing", report)
        self.assertIn("not proof", report)
        self.assertIn("Structural Calibration", report)

    def test_saturated_empty_register_cannot_certify_no_repair(self):
        result = assess("Long policy", "policy", "Agencies must monitor risks and review controls. " * 600, assessment_mode="external_framework")
        report = runner.build_institutional_report({"safe_output_stem": "long"}, {}, result, [], [], [], [])
        self.assertIn("section by section", report)
        self.assertIn("not evidence that no repair is needed", report)
        self.assertNotIn("No remediation is required", report)
        self.assertNotIn("residual risk is no longer in the drafting", report)

    def test_document_report_uses_execution_date_and_actual_generator(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "policy.txt"
            source.write_text("Agencies must record AI risks and appoint an accountable owner.")
            args = runner.build_parser().parse_args([str(source), "--output-dir", str(root / "out"), "--extractor", "builtin"])
            runner.run(args)
            payload = json.loads((root / "out/policy.laif.json").read_text())
            report = (root / "out/policy.laif.md").read_text()
            date = payload["processing_metadata"]["processed_at_utc"][:10]
            self.assertIn("**Report date:** " + date, report)
            self.assertNotIn("September 2026", report)
            self.assertIn("Generated by `python3 scripts/laif_process_document.py`", report)
            self.assertNotIn("Generated by `test_real_world.py`", report)


if __name__ == "__main__":
    unittest.main()
