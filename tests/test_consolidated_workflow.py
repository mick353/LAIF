"""Source/method drift and overclaim regressions for the combined review workflow."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from laif_spec import FOUNDATIONAL_PRINCIPLES
import laif_research_report as research

SOURCE = ROOT / "docs/examples/vendor-policy.md"


class ConsolidatedWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dossier = research.build_dossier(SOURCE, date="2026-11-07")

    def annotations(self):
        result = research.review_template(self.dossier)
        result["findings"] = [{
            "finding_id": "F001", "claim_type": "INFERENCE",
            "statement": "Synthetic regression claim; operating effectiveness is untested.",
            "evidence_ids": [result["available_evidence_ids"][0]],
            "counterevidence_ids": [], "criterion_ids": ["Q1"],
            "alternative_explanations": ["Another instrument could supply the missing evidence."],
            "limitations": "Synthetic workflow test, no substantive conclusion.",
            "analyst_id": "synthetic-test-analyst",
        }]
        return result

    def build(self, annotations):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "annotations.json"
            path.write_text(json.dumps(annotations), encoding="utf-8")
            return research.build_dossier(SOURCE, date="2026-11-07", review_file=path)

    def test_principle_registry_matches_principal_headings(self):
        principal = (ROOT / "LAIF_v1.2.txt").read_text(encoding="utf-8")
        for number, title in FOUNDATIONAL_PRINCIPLES.items():
            self.assertIn(f"Principle {number} — {title}", principal)
        self.assertEqual(len(FOUNDATIONAL_PRINCIPLES), 5)
        instructions = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertNotIn("The Three Foundational Principles", instructions)

    def test_source_inventory_never_implies_criteria_assessed(self):
        rows = {row["criterion_id"]: row for row in self.dossier["criteria_coverage"]}
        self.assertEqual(set(rows), {"A.1", "A.2", "A.3", "A.4", "Q1", "Q2", "Q3", "G.1"})
        self.assertTrue(all(row["status"] == "NOT_ASSESSED" for row in rows.values()))
        self.assertIn("Where section 2.5 applies", rows["A.4"]["question"])

    def test_annotated_criterion_still_requires_review(self):
        dossier = self.build(self.annotations())
        rows = {row["criterion_id"]: row for row in dossier["criteria_coverage"]}
        self.assertEqual(rows["Q1"]["finding_ids"], ["F001"])
        self.assertEqual(rows["Q1"]["status"], "ANALYST_CLAIMS_ATTACHED_REVIEW_REQUIRED")
        self.assertEqual(rows["Q2"]["status"], "NOT_ASSESSED")
        self.assertEqual(dossier["reviewer_findings"][0]["method_basis_status"], "HASH_BOUND_ANALYST_CLAIM")
        self.assertEqual(dossier["scholarly_validation"], "NOT_ESTABLISHED")

    def test_changed_or_partial_method_hashes_rejected(self):
        for field in ("framework_source_sha256", "toolkit_source_sha256", "toolchain_fingerprint"):
            for mode in ("changed", "missing"):
                data = self.annotations()
                if mode == "changed":
                    data[field] = "0" * 64
                else:
                    del data[field]
                with self.subTest(field=field, mode=mode), self.assertRaisesRegex(
                        research.ResearchInputError, "basis SHA-256 mismatch"):
                    self.build(data)

    def test_legacy_annotation_is_explicitly_unbound(self):
        data = self.annotations()
        del data["framework_source_sha256"]
        del data["toolkit_source_sha256"]
        del data["toolchain_fingerprint"]
        dossier = self.build(data)
        self.assertEqual(dossier["reviewer_findings"][0]["method_basis_status"], "UNBOUND_LEGACY_ANNOTATION")
        self.assertIn("UNBOUND_LEGACY_ANNOTATION", research.render_markdown(dossier).replace("\\", ""))

    def test_malformed_or_duplicate_criterion_ids_rejected(self):
        for criteria in (["Q4"], ["Q1", "Q1"], "Q1", [None], [{}]):
            data = copy.deepcopy(self.annotations())
            data["findings"][0]["criterion_ids"] = criteria
            with self.subTest(criteria=criteria), self.assertRaisesRegex(
                    research.ResearchInputError, "criterion_ids"):
                self.build(data)


if __name__ == "__main__":
    unittest.main()
