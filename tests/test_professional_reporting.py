"""Actual-source and adversarial acceptance tests for generated external reports.

These cases check identified reporting defects, not general legal accuracy.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import laif_process_document as runner


class ProfessionalReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.outputs = {}
        for key in ("au_dta_policy_v2_1", "eu_ai_act_amendment_2026_1744"):
            source = ROOT / "docs/verified/raw" / (key + ".md")
            out = Path(cls.temp.name) / key
            subprocess.run([sys.executable, "-S", str(ROOT / "scripts/laif_process_document.py"),
                            str(source), "--extractor", "builtin", "--sector", "general_ai_governance",
                            "--output-dir", str(out)], check=True, capture_output=True, text=True)
            data = json.loads((out / (key + ".laif.json")).read_text())
            bundle = json.loads((out / "analyst" / key / "analyst_bundle.json").read_text())
            report = (out / (key + ".laif.md")).read_text()
            cls.outputs[key] = (data, bundle, report, runner.extract_document(source, "builtin").text)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_dta_gate_is_recognised_and_absence_claim_removed(self):
        data, bundle, report, text = self.outputs["au_dta_policy_v2_1"]
        gates = [r for r in data["assessment_result"]["source_control_observations"] if r["control_type"] == "deployment_gate"]
        self.assertTrue(gates)
        self.assertIn("must finalise the assessment", " ".join(gates[0]["exact_quote"].split()))
        self.assertNotIn("risk_without_closure_gate", [g["gap_type"] for g in bundle["gap_register"]])
        self.assertNotIn("sets no precondition", report)
        self.assertNotIn("Risk is discussed without a gate", report)

    def test_all_witnesses_and_primary_quotes_retain_exact_offsets(self):
        for key, (data, bundle, report, text) in self.outputs.items():
            for row in data["assessment_result"]["source_control_observations"]:
                self.assertEqual(text[row["start_char"]:row["end_char"]], row["exact_quote"])
            for row in bundle["quote_bank"]:
                self.assertEqual(text[row["start_offset"]:row["end_offset"]], row["exact_quote"])
                self.assertTrue(runner.quote_has_complete_evidence_proposition(row["display_quote"])[0])
                self.assertFalse(row["exact_quote"].endswith("of this policy"))
                self.assertFalse(row["exact_quote"].endswith("AI adoption"))

    def test_full_verified_source_is_not_rendered_as_illustrative(self):
        data, bundle, report, _ = self.outputs["eu_ai_act_amendment_2026_1744"]
        self.assertEqual(data["assessment_result"]["source_provenance"]["verification_status"], "AUTOMATED_VERIFIED")
        self.assertIn("RECORDED_MANIFEST_MATCH", report)
        self.assertNotIn("illustrative document", report)
        self.assertNotIn("Across this corpus", report)
        self.assertIn("not a new authority or current-law verification", report)

    def test_dta_human_attestation_remains_distinct(self):
        data, _, report, _ = self.outputs["au_dta_policy_v2_1"]
        self.assertEqual(data["assessment_result"]["source_provenance"]["verification_status"], "HUMAN_ATTESTED_AUTHORITATIVE")
        self.assertIn("HUMAN_ATTESTED_AUTHORITATIVE", report)

    def test_attributed_judgements_are_exported_with_evidence_and_limits(self):
        for data, bundle, report, _ in self.outputs.values():
            review = bundle["attributed_reasoning"]
            self.assertEqual(len(review["record"]["criteria_findings"]), 8)
            self.assertIn("not produced by pattern matching or independently reviewed", report)
            allowed = {r["trace_id"] for r in review["curated_source_evidence"]}
            for row in review["record"]["criteria_findings"]:
                self.assertTrue(set(row["trace_ids"]) <= allowed)
            self.assertEqual(review, data["assessment_result"]["attributed_reasoning"])

    def test_review_questions_never_invent_confirmed_failures_or_evidence(self):
        for _, bundle, report, _ in self.outputs.values():
            for gap in bundle["gap_register"]:
                self.assertEqual(gap["review_status"], "UNVERIFIED_REVIEW_QUESTION")
                self.assertIn("non-match does not establish absence", gap["operational_meaning"])
                for qid in gap["source_evidence_quote_ids"]:
                    q = next(q for q in bundle["quote_bank"] if q["quote_id"] == qid)
                    self.assertIn(q["exact_quote"], gap["source_evidence_quote"])
            for pathway in bundle["failure_pathways"]:
                self.assertEqual(pathway["scenario_status"], "HYPOTHETICAL_NOT_OBSERVED")
            for control in bundle["control_recommendations"]:
                self.assertFalse(control["source_requirement"])
                self.assertNotIn("quarterly", control["cadence"])

    def test_pdf_wraps_preserve_subject_and_continuation(self):
        text = ("All agencies governed by the Performance and Accountability Act 2013,\n"
                "must apply this policy.\n\nAgencies must make a publicly available statement\n"
                "outlining AI adoption and use, including stated exceptions.")
        spans = runner._sentence_spans(text)
        self.assertEqual(len(spans), 2)
        self.assertTrue(spans[0][2].startswith("All agencies"))
        self.assertTrue(spans[1][2].endswith("stated exceptions."))

    def test_negative_example_and_disconnected_words_do_not_create_gate(self):
        for text in (
            "Before deployment staff must not complete an assessment.",
            "Hypothetical example: Before deployment agencies must complete an assessment.",
            "Before deployment staff meet for lunch. Providers must assess insurance after incidents.",
        ):
            with self.subTest(text=text):
                self.assertFalse(any(row["control_type"] == "deployment_gate" for row in runner.source_control_observations(text)))

    def test_recital_is_not_presented_as_an_operative_gate(self):
        text = ("Before deployment providers shall assess risks.\n\nHAVE ADOPTED THIS REGULATION:\n\n"
                "Article 1\nProviders may supply goods.")
        self.assertFalse(any(row["control_type"] == "deployment_gate" for row in runner.source_control_observations(text)))

    def test_local_filename_and_copied_text_do_not_grant_authority(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "official-EU-Regulation.md"
            path.write_text("Providers shall assess risks before deployment.")
            provenance = runner.source_provenance(path, runner.sha256_file(path))
            self.assertEqual(provenance["status"], "LOCAL_SOURCE_AUTHORITY_UNVERIFIED")
            self.assertIsNone(runner.source_reasoning_record(provenance))

    def test_registered_source_tampering_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / "docs/verified/manifests"
            folder.mkdir(parents=True)
            raw = root / "docs/verified/raw/test.md"
            raw.parent.mkdir(); raw.write_text("changed source")
            (folder / "test.json").write_text(json.dumps({"raw_filename": "test.md", "sha256_hash": "0" * 64}))
            with patch.object(runner, "REPO_ROOT", root), self.assertRaisesRegex(runner.ExtractionError, "hash differs"):
                runner.source_provenance(raw, runner.sha256_file(raw))

    def test_preview_uses_same_professional_surface_without_writes(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "policy.md"
            path.write_text("Before deployment agencies must complete a risk assessment.")
            out = Path(td) / "not-created"
            run = subprocess.run([sys.executable, str(ROOT / "scripts/laif_process_document.py"), str(path),
                                  "--no-write", "--print-report", "--output-dir", str(out)],
                                 capture_output=True, text=True, check=True)
            self.assertIn("Source-backed control observations", run.stdout)
            self.assertNotIn("Across this corpus", run.stdout)
            self.assertFalse(out.exists())

    def test_source_markup_is_not_active_in_observation_rendering(self):
        text = "Before deployment agencies must assess risks ![tracking](https://example.test/pixel)."
        report = "\n".join(runner.source_review_sections({"source_control_observations": runner.source_control_observations(text)}))
        self.assertNotIn("![tracking]", report)
