"""Retain failed research hypotheses without promoting them to passing findings."""
import json
import unittest
from scripts import laif_exploratory_comparison as comparison


class ExploratoryComparisonTests(unittest.TestCase):
    def test_locked_real_source_and_mutation_receipt_reproduces(self):
        expected = json.loads((comparison.PACKET / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(comparison.compare(), expected)
        self.assertEqual(expected["ws1_acceptance"], "NOT_ESTABLISHED")
        self.assertIsNone(expected["eight_criterion_agreement"])
        for row in expected["documents"].values():
            self.assertIsNone(row["actual_authored_criteria"])
        self.assertEqual(len(expected["mutations"]), 3)


if __name__ == "__main__":
    unittest.main()
