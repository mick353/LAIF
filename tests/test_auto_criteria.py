"""Conjunctive evidence, polarity, real-source mutations and integration."""
import copy
import unittest
from pathlib import Path
from scripts.laif_auto_criteria import judge, markdown

ROOT = Path(__file__).resolve().parents[1]
COMPLETE = {
    "A.1": "The provider must explain each decision output. The provider must disclose uncertainty and limitations. Affected people must obtain an explanation on request.",
    "A.2": "The provider must ensure stated objectives match actual implemented objectives. System behaviour must remain consistent in testing and deployment. The provider must test for deceptive behaviour.",
    "A.3": "The provider must define operating boundaries and resource limits. The operator must deactivate the AI system when necessary. The responsible officer must approve escalation.",
    "A.4": "The provider must compare confidence with observed accuracy. Accuracy tests must use a defined evaluation population. Confidence error thresholds must trigger corrective review.",
    "Q1": "The provider must restrict access only if privacy rights are protected. The protection must have the same enforceable force as the restriction. Breached rights must have a remedy.",
    "Q2": "The policy must assess proportionate burdens on the smallest actor. The same reasoning must apply to all comparable actors. Exceptions must have documented justification.",
    "Q3": "The provider must allow revision of deployment decisions. The operator must decommission systems safely. Irreversible actions must have proportionate justification and approval.",
    "G.1": "The governance committee must undergo independent review. People must be able to challenge governance decisions. The governance board must publish reasons for decisions.",
}


def row(text, cid):
    return next(r for r in judge(text)["criteria"] if r["criterion_id"] == cid)


class AutomaticCriteriaTests(unittest.TestCase):
    def test_all_eight_can_distinguish_complete_partial_and_missing_requirements(self):
        for cid, text in COMPLETE.items():
            with self.subTest(cid=cid):
                result = row(text, cid)
                self.assertEqual(result["determination"], "PROVISIONALLY_SUPPORTED")
                self.assertEqual(result["operational_status"], "NOT_ESTABLISHED")
                partial = row(text.split(". ")[0] + ".", cid)
                self.assertEqual(partial["determination"], "PARTIAL_SUPPORT")
                self.assertEqual(row("Our company sells office furniture.", cid)["determination"], "NOT_ESTABLISHED")

    def test_keywords_and_recommendations_cannot_establish_support(self):
        for cid, text in COMPLETE.items():
            with self.subTest(cid=cid):
                self.assertNotEqual(row(text.replace("must", "should"), cid)["determination"], "PROVISIONALLY_SUPPORTED")
        self.assertEqual(row("Explanation output confidence error affected people.", "A.1")["supported_component_count"], 0)

    def test_each_required_clause_changes_its_criterion_without_moving_others(self):
        all_text = "\n".join(COMPLETE.values())
        baseline = {r["criterion_id"]: r["determination"] for r in judge(all_text)["criteria"]}
        for cid, text in COMPLETE.items():
            for clause in text.split(". "):
                with self.subTest(cid=cid, clause=clause):
                    changed = {r["criterion_id"]: r["determination"] for r in judge(all_text.replace(clause, "", 1))["criteria"]}
                    self.assertNotEqual(changed[cid], baseline[cid])
                    for other in baseline:
                        if other != cid:
                            self.assertEqual(changed[other], baseline[other])

    def test_negation_and_hypotheticals_are_not_positive_evidence(self):
        text = COMPLETE["A.1"] + " Providers need not explain decision outputs."
        result = row(text, "A.1")
        self.assertEqual(result["determination"], "SOURCE_CONFLICT")
        self.assertTrue(any(f["contrary"] for f in result["components"]))
        example = "For example, a provider must explain decision outputs."
        self.assertEqual(row(example, "A.1")["supported_component_count"], 0)

    def test_all_witnesses_are_exact_and_evidence_gate_abstains(self):
        text = "\n\n" + "\n".join(COMPLETE.values())
        result = judge(text)
        for criterion in result["criteria"]:
            for component in criterion["components"]:
                for w in component["witnesses"]:
                    self.assertEqual(text[w["start_char"]:w["end_char"]], w["exact_quote"])
        gated = judge(text, evidence_eligible=False)
        self.assertTrue(all(r["determination"] == "REVIEW_REQUIRED" for r in gated["criteria"]))

    def test_real_nist_deactivation_clause_removal_changes_evidence(self):
        text = (ROOT / "docs/verified/raw/5f667a6f-NIST.AI.1001.md").read_text(encoding="utf-8")
        start = text.index("MANAGE 2.4:")
        end = text.index(" |", start)
        before = row(text, "A.3")
        after = row(text[:start] + text[end:], "A.3")
        def witnesses(r):
            return [w["exact_quote"] for f in r["components"] for w in f["witnesses"]]
        self.assertTrue(any("MANAGE 2.4:" in w for w in witnesses(before)))
        self.assertFalse(any("MANAGE 2.4:" in w for w in witnesses(after)))
        self.assertLess(len(witnesses(after)), len(witnesses(before)))

    def test_markdown_escapes_source_markup_and_does_not_modify_result(self):
        result = judge(COMPLETE["A.1"] + " The provider must explain <script>alert(1)</script> decision outputs.")
        original = copy.deepcopy(result)
        rendered = "\n".join(markdown(result))
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertEqual(result, original)

    def test_engine_outputs_eight_judgments_without_changing_native_channel(self):
        from assessment_engine import assess
        result = assess("fixture", "synthetic", COMPLETE["A.1"], assessment_mode="external_framework")
        self.assertEqual(len(result["automatic_criteria"]["criteria"]), 8)
        self.assertEqual(result["substantive_coherence_determination"], "REQUIRES_SOURCE_BASED_REVIEW")


if __name__ == "__main__":
    unittest.main()
