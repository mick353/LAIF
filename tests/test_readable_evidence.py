"""Reader-level checks: quotations accompany claims and every citation is usable."""
import copy
import json
import re
import unittest
from pathlib import Path

from scripts import laif_evidence_display as display
from scripts import laif_process_document as processor
from scripts.laif_criteria_review import validate_criteria_review

ROOT = Path(__file__).resolve().parents[1]


class ReadableEvidenceTests(unittest.TestCase):
    def test_private_text_has_line_reference_without_invented_page(self):
        text = "Private source\nThe owner must approve deployment.\n"
        start = text.index("The owner")
        row = {"source_location": display.locate(text, start, len(text))}
        self.assertEqual(row["source_location"]["extracted_line"], 2)
        self.assertIn("extracted-text line 2", display.location_label(row))
        self.assertNotIn("page", display.location_label(row).lower())

    def test_heading_and_cross_page_markers_are_derived_from_exact_text(self):
        text = "# Duties\n<!-- PDF page 6 -->\nThe owner must\n<!-- PDF page 7 -->\napprove deployment.\n"
        location = display.locate(text, text.index("The owner"), len(text))
        self.assertEqual(location["section"], "Duties")
        self.assertEqual(location["pdf_page_markers"], [6, 7])
        self.assertIn("PDF page markers 6, 7", display.location_label({"source_location": location}))

    def test_invalid_offsets_are_rejected_without_making_a_location(self):
        for start, end in ((-1, 4), (2, 1), (0, 40), (True, 3)):
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                display.locate("a source", start, end)

    def test_source_markup_is_inert_and_paragraphs_remain_quotations(self):
        rendered = display.blockquote('# Claim\n\n<script>x</script>\n![track](https://example.test/x)')
        self.assertEqual(len(rendered.splitlines()), 4)
        self.assertTrue(all(line.startswith("> ") for line in rendered.splitlines()))
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("![track]", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_display_does_not_replace_exact_source_or_offsets(self):
        row = {"exact_quote": "The owner must\napprove.", "display_quote": "The owner must approve.",
               "start_char": 12, "end_char": 36, "extracted_line": 2}
        original = copy.deepcopy(row)
        rendered = "\n".join(display.passage(row, "Q001", "quote", display=True))
        self.assertEqual(row, original)
        self.assertIn("> The owner must approve.", rendered)
        self.assertIn("Display formatting normalised", rendered)
        self.assertNotIn("12–36", rendered)

    def test_each_actual_authored_criterion_carries_its_own_full_quotations(self):
        for key in ("au_dta_policy_v2_1", "5f667a6f-NIST.AI.1001"):
            source = ROOT / "docs/verified/raw" / (key + ".md")
            text = processor.extract_document(source, "builtin").text
            raw = json.loads((ROOT / "docs/verification/2026-11-07-substantive-review" / key / "completed-review.json").read_text(encoding="utf-8"))
            review = validate_criteria_review(raw["criteria_review"], text)
            display.locate_review(review, text)
            report = "\n".join(processor.criteria_review_sections(review, source.name))
            for criterion in review["criteria"]:
                body = report.split("### " + criterion["criterion_id"] + " — authored determination", 1)[1].split("### ", 1)[0]
                for row in criterion["source_excerpts"]:
                    with self.subTest(source=key, criterion=criterion["criterion_id"], evidence=row["evidence_id"]):
                        self.assertIn(display.blockquote(row["exact_quote"]), body)
                        self.assertIn(display.location_label(row), body)
                        self.assertIn(display.safe_text(source.name), body)
                        self.assertEqual(text[row["start_char"]:row["end_char"]], row["exact_quote"])
            self.assertNotIn("extracted characters", report)

    def test_actual_attributed_determinations_quote_their_referenced_traces(self):
        for key in ("au_dta_policy_v2_1", "eu_ai_act_amendment_2026_1744"):
            source = ROOT / "docs/verified/raw" / (key + ".md")
            review = processor.source_reasoning_record(processor.source_provenance(source, processor.sha256_file(source)))
            report = "\n".join(processor.attributed_reasoning_sections(review))
            by_id = {row["trace_id"]: row for row in review["curated_source_evidence"]}
            for criterion in review["record"]["criteria_findings"]:
                body = report.split("#### " + criterion["criterion_id"] + " — supporting source passages", 1)[1].split("#### ", 1)[0]
                for identity in criterion["trace_ids"]:
                    with self.subTest(source=key, criterion=criterion["criterion_id"], trace=identity):
                        self.assertIn(display.blockquote(by_id[identity]["matched_text"]), body)
                        self.assertIn(display.location_label(by_id[identity]), body)
            targets = re.findall(r'<a id="([^"]+)"', report)
            links = re.findall(r'\]\(#([^)]+)\)', report)
            self.assertEqual(len(targets), len(set(targets)))
            self.assertTrue(set(links) <= set(targets))
            self.assertNotIn("extracted characters", report)

    def test_source_control_links_resolve_even_for_later_retained_witnesses(self):
        text = ("# Controls\nBefore deployment the provider must assess risks.\n\n"
                "Before launch the provider must assess risks.\n\n"
                "Before deployment the agency must complete a risk assessment.\n")
        scan = processor.source_control_scan(text)
        report = "\n".join(processor.source_review_sections({"source_control_observations": scan["observations"], "source_scan_coverage": scan["coverage"]}))
        self.assertGreater(len(scan["observations"]), 1)
        for row in scan["observations"]:
            self.assertIn('id="' + display.anchor("source", row["control_id"]) + '"', report)
        targets = set(re.findall(r'<a id="([^"]+)"', report))
        self.assertTrue(set(re.findall(r'\]\(#([^)]+)\)', report)) <= targets)

    def test_support_and_counterevidence_are_quoted_at_the_submitted_finding(self):
        review = {"boundary": "Test-only analyst claim", "review_file_sha256": "test", "evidence_manifest_sha256": "test",
                  "source_name": "private-policy.txt", "criteria_coverage": [],
                  "evidence": [{"evidence_id": "E001", "exact_quote": "An appeal is available.", "extracted_line": 3},
                               {"evidence_id": "E002", "exact_quote": "An exception applies.", "extracted_line": 9}],
                  "findings": [{"finding_id": "F001", "claim_type": "INFERENCE", "statement": "A qualified appeal route is stated.",
                                "analyst_id": "test", "criterion_ids": ["A.1"], "evidence_ids": ["E001"],
                                "counterevidence_ids": ["E002"], "alternative_explanations": ["Other law may qualify this."], "limitations": "No operation tested."}]}
        report = "\n".join(processor.submitted_review_sections(review))
        finding = report.split("### Submitted-review coverage", 1)[0]
        self.assertIn("> An appeal is available.", finding)
        self.assertIn("> An exception applies.", finding)
        self.assertIn("[E002](#submitted-e002)", finding)
        self.assertIn("private-policy.txt; extracted-text line 9", finding)


if __name__ == "__main__":
    unittest.main()
