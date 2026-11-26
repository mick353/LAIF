"""Source evidence shown by an assessment must include its actual match."""

from pathlib import Path
import re
import unittest

from laif_engine.assessment import assess
from laif_engine.source_spans import _quote_at


class AssessmentQuoteTests(unittest.TestCase):
    def test_long_introduction_cannot_push_trigger_out_of_excerpt(self):
        text = ("The office reviews a range of administrative issues and maintains a register "
                "for relevant planned activities before the department asks that members' safety "
                "be protected by the published rule.")
        start = text.index("safety")
        excerpt = _quote_at(text, start, start + len("safety"), max_len=90)
        self.assertIn("members' safety be protected", excerpt)
        self.assertIn(excerpt, text)
        self.assertLessEqual(len(excerpt), 90)

    def test_earlier_identical_phrase_cannot_stand_in_for_selected_occurrence(self):
        text = "safety " + "background " * 13 + "this particular safety requirement applies to staff"
        start = text.rindex("safety")
        excerpt = _quote_at(text, start, start + len("safety"), max_len=94)
        self.assertIn("this particular safety requirement applies to staff", excerpt)
        self.assertEqual(excerpt.count("safety"), 1)

    def test_long_wrapped_match_keeps_all_words_and_complete_end_token(self):
        text = "The office explains that " + "this obligation continues\nfor years " * 8 + "beneficiaries retain rights."
        start = text.index("this obligation")
        end = text.index("beneficiar") + len("beneficiar")
        excerpt = _quote_at(text, start, end, max_len=85)
        self.assertIn(" ".join(text[start:end].split()), excerpt)
        self.assertTrue(excerpt.endswith("beneficiaries"))
        self.assertIn(excerpt, " ".join(text.split()))
        self.assertGreater(len(excerpt), 85)

    def test_retained_assessments_show_the_terms_that_triggered_findings(self):
        root = Path(__file__).resolve().parents[1] / "docs/verified/raw"
        for name, label, matched in (
            ("5f667a6f-NIST.AI.1001.md", "safety", "safety"),
            ("5f667a6f-NIST.AI.1001.md", "contestability / redress", "challenge"),
            ("au_dta_policy_v2_1.md", "human oversight", "oversight"),
        ):
            with self.subTest(name=name, label=label):
                text = (root / name).read_text(encoding="utf-8")
                result = assess(name, "uploaded_document", text, assessment_mode="external_framework")
                row = next(row for row in result["signal_locations"]["conceptual"] if row["label"] == label)
                self.assertRegex(row["quote"], rf"\b{re.escape(matched)}\b")
