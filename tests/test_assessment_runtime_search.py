"""Regression tests for the assessment engine's per-document searches."""

import re
import unittest
from unittest.mock import patch

from laif_engine.assessment import assess
from laif_engine.detection import CONCEPTUAL_RUBRIC, CONTRADICTION_PROXIMITY, _contradiction_check


class AssessmentSearchTests(unittest.TestCase):
    def test_assessment_reuses_searches_without_mixing_flags_or_source_text(self):
        label = "transparency"
        pattern = next(pattern for _, pattern, term in CONCEPTUAL_RUBRIC if term == label)
        first_document = "The supplier discloses\nits basis for the decision."
        other_document = "The supplier records the date of its decision."
        self.assertIsNotNone(re.search(pattern, first_document, re.IGNORECASE | re.DOTALL))
        self.assertIsNone(re.search(pattern, first_document, re.IGNORECASE))

        with patch.object(re, "search", wraps=re.search) as observed:
            result = assess("Supplier", "policy", first_document)
            later = assess("Supplier", "policy", other_document)

        for document in (first_document, other_document):
            with self.subTest(document=document):
                calls = [call.args[2] for call in observed.call_args_list
                         if len(call.args) == 3 and call.args[0] == pattern and call.args[1] is document]
                self.assertCountEqual(calls, [re.IGNORECASE, re.IGNORECASE | re.DOTALL])

        self.assertIn(label, [row["label"] for row in result["signal_locations"]["conceptual"]])
        self.assertNotIn("Expresses: transparency", result["strengths"])
        self.assertNotIn(label, [row["label"] for row in later["signal_locations"]["conceptual"]])

    def test_contradiction_window_keeps_both_inclusive_edges_and_ignores_far_matches(self):
        check = {"property": "window test", "trigger": r"trigger",
                 "adversaries": [(r"hazard", "adverse clause")]}
        limit = CONTRADICTION_PROXIMITY
        with patch("laif_engine.detection.CONTRADICTION_CHECKS", [check]):
            for first, second in (("trigger", "hazard"), ("hazard", "trigger")):
                for distance, expected in ((limit, 1), (limit + 1, 0)):
                    with self.subTest(first=first, distance=distance):
                        text = first + " " * (distance - len(first)) + second
                        self.assertEqual(len(_contradiction_check(text)), expected)

            text = "trigger" + " " * (limit + 1) + "hazard trigger"
            self.assertEqual(len(_contradiction_check(text)), 1)
