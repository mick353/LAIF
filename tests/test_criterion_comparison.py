"""Regression boundaries for the real-source exploratory comparison."""
import json
from pathlib import Path
import unittest

from scripts.laif_criterion_comparison import PACKET, ROOT, compare, remove_spans


class CriterionComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((PACKET / "results.json").read_text(encoding="utf-8"))

    def test_reproduce_retained_receipt(self):
        self.assertEqual(self.receipt, compare())

    def test_exact_witnesses_and_operational_boundary(self):
        for document in self.receipt["documents"].values():
            text = (ROOT / document["path"]).read_text(encoding="utf-8")
            for row in document["judgment"]["criteria"]:
                self.assertEqual(row["operational_status"], "NOT_ESTABLISHED")
                for component in row["components"]:
                    for witness in component["witnesses"]:
                        self.assertEqual(witness["exact_quote"], text[witness["start_char"]:witness["end_char"]])

    def test_negative_results_and_unavailable_cases_preserved(self):
        comparisons = [c for d in self.receipt["documents"].values() for c in d["prediction_comparison"].values()]
        self.assertEqual(sum(not c["expectation_met"] for c in comparisons), 11)
        skipped = [c for c in self.receipt["systematic_ablations"] if c["status"] == "NOT_APPLICABLE"]
        self.assertEqual(len(skipped), 18)
        self.assertFalse(self.receipt["independent_validation"])

    def test_removal_does_not_synthesize_adjacent_clause(self):
        self.assertEqual(remove_spans("alpha X beta", [(6, 8), (6, 7)]), "alpha \nbeta")
        with self.assertRaises(ValueError):
            remove_spans("abc", [(0, 4)])


if __name__ == "__main__":
    unittest.main()
