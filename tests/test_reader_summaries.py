"""Full-discovery plain-language gate, scoped only to reader summaries."""
import copy
import itertools
import json
from pathlib import Path
import runpy
import unittest

from scripts.laif_auto_criteria import judge
from scripts.laif_reader_summaries import (
    QUESTIONS, OUTCOMES, add_reader_summaries, prohibited_terms,
    reader_summary, validate_reader_summary, validate_summary_fields,
)
from scripts import laif_process_document as processor

ROOT = Path(__file__).resolve().parents[1]


class ReaderSummaryTests(unittest.TestCase):
    def test_every_authored_status_and_criterion_is_plain_and_two_sentences(self):
        for criterion, status in itertools.product(QUESTIONS, OUTCOMES):
            with self.subTest(criterion=criterion, status=status):
                summary = reader_summary(criterion, status)
                self.assertEqual(summary.count("."), 2)
                validate_reader_summary(summary)

    def test_each_maintained_jargon_term_fails_only_in_summary(self):
        for term in prohibited_terms():
            with self.subTest(term=term):
                with self.assertRaisesRegex(ValueError, "jargon"):
                    validate_summary_fields({"outer": [{"reader_summary": "Review " + term.upper() + "."}]})
                validate_summary_fields({"reasoning": term, "framework_basis": term})

    def test_all_automatic_summary_branches_and_component_combinations(self):
        fixtures = runpy.run_path(str(ROOT / "tests/test_auto_criteria.py"))["COMPLETE"]
        seen = set()
        for text in fixtures.values():
            parts = text.rstrip(".").split(". ")
            for mask in itertools.product((False, True), repeat=len(parts)):
                sample = ". ".join(p for p, keep in zip(parts, mask) if keep) + "."
                for variant in (sample, sample.replace("must", "should"), sample + " " + sample.replace("must", "not required")):
                    result = judge(variant)
                    validate_summary_fields(result)
                    seen.update(row["determination"] for row in result["criteria"])
        result = judge("", evidence_eligible=False)
        validate_summary_fields(result)
        seen.update(row["determination"] for row in result["criteria"])
        self.assertEqual(seen, {"PROVISIONALLY_SUPPORTED", "PARTIAL_SUPPORT", "NOT_ESTABLISHED", "SOURCE_CONFLICT", "REVIEW_REQUIRED"})

    def test_current_generated_report_summary_fields(self):
        report = json.loads((ROOT / "reports/laif_assessment_data.json").read_text(encoding="utf-8"))
        self.assertIn('"reader_summary"', json.dumps(report), "The gate must inspect actual summary fields")
        validate_summary_fields(report)

    def test_authored_reasoning_and_input_are_unchanged(self):
        text = "All three normative-force limbs; section 2.5 trigger; inseparability."
        original = {"criteria": [{"criterion_id": "Q1", "determination": "PARTIAL_SUPPORT", "reasoning": text}]}
        before = copy.deepcopy(original)
        result = add_reader_summaries(original)
        self.assertEqual(original, before)
        self.assertEqual(result["criteria"][0]["reasoning"], text)
        self.assertIn("reader_summary", result["criteria"][0])
        validate_summary_fields(result)
        with self.assertRaisesRegex(ValueError, "Unknown"):
            reader_summary("Q1", "NEW_UNREVIEWED_STATUS")

    def test_canonical_records_unchanged_and_rendered_separately(self):
        for key in ("au_dta_policy_v2_1", "eu_ai_act_amendment_2026_1744"):
            path = ROOT / f"docs/verification/2026-11-07/regulatory/{key}.decisions.json"
            original = path.read_bytes()
            result = processor.source_reasoning_record({"document_id": key, "manifest": f"docs/verified/manifests/{key}.json"})
            self.assertEqual(result["record"], json.loads(original))
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(set(result["reader_summaries"]), set(QUESTIONS))
            validate_summary_fields(result)
            rendered = "\n".join(processor.attributed_reasoning_sections(result))
            self.assertEqual(rendered.count("Reader summary (automatic reading aid):"), 8)
            for row in result["record"]["criteria_findings"]:
                self.assertIn("Reasoning: " + processor._safe_report_text(row["reasoning"]), rendered)

    def test_research_and_submitted_review_carry_same_summary(self):
        fixture_class = runpy.run_path(str(ROOT / "tests/test_substantive_review.py"))["SubstantiveReviewTests"]
        fixture = fixture_class()
        try:
            fixture.setUp()
            original = copy.deepcopy(fixture.review["criteria_review"])
            result = fixture.load()["criteria_review"]
            for before, after in zip(original["criteria"], result["criteria"]):
                self.assertEqual(before["reasoning"], after["reasoning"])
                self.assertEqual(after["reader_summary"], reader_summary(before["criterion_id"], before["determination"]))
            rendered = "\n".join(processor.criteria_review_sections(result))
            self.assertEqual(rendered.count("Reader summary (automatic reading aid):"), 8)
            validate_summary_fields(result)
        finally:
            fixture.doCleanups()


if __name__ == "__main__":
    unittest.main()
