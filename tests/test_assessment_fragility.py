#!/usr/bin/env python3
"""Characterization tests for LAIF assessment fragility calibration.

These tests intentionally document current false-negative and regex-boundary
behavior. They are diagnostic coverage, not policy changes: failing formal
terminology, low conceptual proximity, or paraphrase findings here should be
read as current engine behavior unless the engine crashes or misreports the
failure channel.
"""

from __future__ import annotations

import io
import re
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from assessment_engine import assess, generate_markdown_report
from test_real_world import _print_scorecard
from validate import CONTEXT_WINDOW, PARAPHRASE_GUARDS, find_paraphrase_violations


COUPLING_GUARD = next(g for g in PARAPHRASE_GUARDS if g["term"] == "Coupling")


CANONICAL_LAIF_DOCUMENT = """
PART ONE — FOUNDATIONAL PRINCIPLES cannot be amended.
PART SEVEN self-application applies to regulatory bodies and governance actors.
The Integrity Layer requires Structural Transparency, Structural Honesty, and
Structural Containment. The Coherence Test requires Coupling, Consistency, and
Reversibility. A.1 FINDING: Structural Transparency is satisfied by a meaningful
explanation. A.2 FINDING: Structural Honesty is satisfied when stated objectives
match implementation. A.3 FINDING: Structural Containment is satisfied by
documented operational boundaries. B.1 FINDING: Coupling pairs each restriction
with a specific human interest and equivalent normative force. B.2 FINDING:
Consistency is satisfied across actors. B.3 FINDING: Reversibility is satisfied
through corrective decision remedies.
"""

GENERIC_REGULATORY_DOCUMENT = """
Article 12. Providers shall implement risk management, transparency,
accountability, human oversight, safety, redress, traceability, and
non-discrimination measures for high-risk systems. Technical documentation shall
identify specific requirements and review obligations.
"""

PLAUSIBLE_UNMATCHED_LEGAL_SENTENCE = """
The competent authority may require the provider to put in place appropriate
technical and organisational measures to ensure compliance with this Regulation,
taking into account the nature, context, and intended purpose of the system.
"""


class AssessmentFragilityCharacterizationTests(unittest.TestCase):
    """Diagnostic tests preserving current assessment/validation separation."""

    def test_canonical_terms_formally_differ_from_generic_regulatory_language(self):
        """Canonical terminology changes formal/scalar behavior; this is characterization."""
        canonical = assess("canonical fixture", "diagnostic_fixture", CANONICAL_LAIF_DOCUMENT)
        generic = assess("generic fixture", "diagnostic_fixture", GENERIC_REGULATORY_DOCUMENT)

        self.assertEqual(canonical["formal_laif_compliance"], "PASS")
        self.assertEqual(generic["formal_laif_compliance"], "FAIL")
        self.assertGreater(canonical["terminology_score"], generic["terminology_score"])
        self.assertGreater(canonical["terminology_score"], 0)
        self.assertEqual(generic["terminology_score"], 0)
        self.assertTrue(canonical["construct_coverage"]["Coupling"])
        self.assertFalse(generic["construct_coverage"]["Coupling"])

    def test_conceptual_proximity_can_be_nonzero_without_formal_laif_terms(self):
        """Absence of LAIF terms is a formal terminology failure, not engine failure."""
        result = assess("generic conceptual fixture", "diagnostic_fixture", GENERIC_REGULATORY_DOCUMENT)

        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertEqual(result["terminology_score"], 0)
        self.assertGreater(result["conceptual_proximity_score"], 0)
        self.assertIn(
            "terminological — no canonical LAIF terms present",
            result["primary_failure_modes"],
        )
        self.assertTrue(any(gap.startswith("Canonical LAIF terms absent:") for gap in result["gaps"]))
        self.assertIn("score_breakdown", result)
        self.assertGreater(len(result["score_breakdown"]["conceptual"]["fired"]), 0)

    def test_paraphrase_guard_catches_standalone_coupling_substitutes(self):
        """Standalone alignment/connection/linkage remain prohibited substitutes."""
        for substitute in ("alignment", "connection", "linkage"):
            with self.subTest(substitute=substitute):
                text = (
                    f"The framework requires a documented {substitute} between "
                    "the restriction and the protected human interest."
                )
                violations = find_paraphrase_violations(text, COUPLING_GUARD)
                self.assertEqual(len(violations), 1)

    def test_paraphrase_guard_allows_documented_contrast_phrases_within_window(self):
        """Contrast phrasing is allowed when the documented context-window rule sees it."""
        allowed_examples = [
            "Unlike alignment, Coupling imposes a bidirectional structural requirement.",
            "The framework uses Coupling rather than alignment as its organising concept.",
        ]
        for text in allowed_examples:
            with self.subTest(text=text):
                self.assertEqual(find_paraphrase_violations(text, COUPLING_GUARD), [])

    def test_paraphrase_guard_context_window_boundary_is_characterized(self):
        """Near-threshold fixture documents the current ±CONTEXT_WINDOW behavior."""
        # With this implementation, the whole canonical term must fit inside the
        # right-side slice ending at match.end() + CONTEXT_WINDOW. The 190-char
        # filler is therefore allowed, while the 191-char filler is currently not.
        allowed_near_boundary = "alignment " + ("x" * 190) + " Coupling"
        outside_boundary = "alignment " + ("x" * 191) + " Coupling"

        self.assertEqual(CONTEXT_WINDOW, 200)
        self.assertEqual(find_paraphrase_violations(allowed_near_boundary, COUPLING_GUARD), [])
        self.assertEqual(len(find_paraphrase_violations(outside_boundary, COUPLING_GUARD)), 1)

    def test_plausible_unmatched_legal_sentence_does_not_crash_assessment(self):
        """Regex false negatives are labelled expected low conceptual score, not runtime failure."""
        result = assess(
            "plausible unmatched legal phrasing",
            "diagnostic_fixture",
            PLAUSIBLE_UNMATCHED_LEGAL_SENTENCE,
        )

        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertEqual(result["terminology_score"], 0)
        self.assertEqual(result["conceptual_proximity_score"], 0)
        self.assertEqual(result["score_breakdown"]["conceptual"]["fired"], [])
        self.assertIn(
            "conceptual — LAIF-like concepts insufficiently expressed",
            result["primary_failure_modes"],
        )

    def test_scalar_proximity_does_not_convert_formal_fail_to_pass(self):
        """Assessment scoring remains separate from strict formal compliance gates."""
        result = assess("high scalar generic fixture", "diagnostic_fixture", GENERIC_REGULATORY_DOCUMENT)

        self.assertGreaterEqual(result["overall_readiness_score"], 40)
        self.assertGreaterEqual(result["conceptual_proximity_score"], 40)
        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertEqual(result["strong_laif_compliance"], "FAIL")

    def test_formal_terminology_failure_does_not_block_independent_scalar_testing(self):
        """A formal FAIL still exposes deterministic scalar scores and traces for calibration."""
        result = assess("formal fail scalar fixture", "diagnostic_fixture", GENERIC_REGULATORY_DOCUMENT)

        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        for key in (
            "structural_score",
            "terminology_score",
            "conceptual_proximity_score",
            "auditability_score",
            "enforceability_score",
            "overall_readiness_score",
        ):
            self.assertIsInstance(result[key], int)
        self.assertEqual(
            set(result["score_breakdown"]),
            {"structural", "terminology", "conceptual", "auditability", "enforceability"},
        )

    def test_external_framework_public_output_uses_mode_context_for_fail_wording(self):
        """Public external output labels LAIF-native failures without bare compliance wording."""
        result = assess(
            "public output external fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )

        buf = io.StringIO()
        with redirect_stdout(buf):
            _print_scorecard(result)
        output = buf.getvalue()

        self.assertNotRegex(
            output,
            re.compile(r"FORMAL\s+LAIF\s+COMPLIANCE:\s*\[?FAIL\]?", re.IGNORECASE),
        )
        self.assertIn("Assessment mode", output)
        self.assertIn("LAIF-native certification", output)
        self.assertIn("External framework structural assessment", output)
        self.assertIn("diagnostic", output)
        self.assertIn("not certification", output)
        self.assertIn("not LAIF-native / canonical remediation required", output)
        self.assertNotIn("PRIMARY FAILURE MODES", output)
        self.assertIn("PRIMARY LAIF DIAGNOSTIC GAPS", output)
        self.assertIn("DIAGNOSTIC GAPS", output)
        self.assertNotIn("governance-worthless", output.lower())
        self.assertNotIn("structurally incoherent", output.lower())
        self.assertNotIn("legally invalid solely", output.lower())

    def test_real_world_markdown_report_contains_public_mode_separation_notice(self):
        """Generated real-world markdown describes external frameworks diagnostically."""
        result = assess(
            "public report external fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
            citation="Example Citation §1",
            provenance="OFFICIAL_EXCERPT",
            source_url="https://example.test/source",
            source_note="Example source note",
            intended_use="Regression test source basis",
        )
        report = generate_markdown_report([result], report_date="May 2026")

        self.assertNotRegex(
            report,
            re.compile(r"FORMAL\s+LAIF\s+COMPLIANCE:\s*\[?FAIL\]?", re.IGNORECASE),
        )
        self.assertNotIn("This document fails formal LAIF v1.2 compliance.", report)
        self.assertNotIn("Missing any single construct = FAIL", report)
        self.assertIn("formal LAIF-native certification gate", report)
        self.assertIn(
            "external framework assessment remains diagnostic and does not determine legal validity",
            report,
        )
        for phrase in (
            "Assessment Scope",
            "Result Boundary / How to Read This Report",
            "Method and Scoring Model",
            "Formal LAIF-native certification gate",
            "Dimensional scoring model",
            "Structural depth / adversarial hardening",
            "Validation boundary",
            "Provenance / Source Basis",
            "Executive Diagnostic Summary",
            "Governance-Force Profile",
            "Construct Crosswalk",
            "Remediation Priorities",
            "Limits",
            "Legal / authority boundary",
            "LAIF-native certification",
            "External framework structural assessment",
            "diagnostic",
            "not LAIF-native / canonical remediation required",
            "not certification",
            "Common LAIF diagnostic gaps",
            "Governance-force patterns",
            "Remediation themes",
            "Score distribution / deterministic rubric comparison",
            "Governance signal strength",
            "Structural depth",
            "Key LAIF-model risks",
            "Key LAIF-model strengths",
            "Position assessment under LAIF diagnostic model",
            "LAIF structural remediation priorities",
            "Structured remediation details",
            "Problem:",
            "Why it matters:",
            "Concrete fix:",
            "Signals detected",
            "Signals not detected",
            "Example Citation §1",
            "OFFICIAL_EXCERPT",
            "https://example.test/source",
            "Example source note",
            "Regression test source basis",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)
        for component in (
            "mandate",
            "actor",
            "trigger",
            "protected interest",
            "control",
            "evidence",
            "reversibility",
            "escalation",
            "consequence",
            "auditability",
        ):
            with self.subTest(component=component):
                self.assertIn(component, report)
        self.assertNotIn("#### Gaps", report)
        self.assertNotIn("Primary Failure Modes", report)
        self.assertNotIn("Common Failure Modes", report)
        self.assertNotIn("Primary structural failure", report)
        self.assertNotIn("Final verdict", report)
        self.assertNotIn("**Deployment Risk Tier:**", report)
        self.assertNotIn("**What Must Be Fixed First:**", report)
        self.assertNotIn("**Result:**", report)
        self.assertNotIn("However, the following are not structurally enforced:", report)
        self.assertNotIn(
            "lacks the structural guarantees required for reliable governance",
            report,
        )
        self.assertNotIn(
            "required LAIF constructs are absent from the governance structure",
            report,
        )
        self.assertNotIn("governance-worthless", report.lower())
        self.assertNotIn("means structurally incoherent", report.lower())
        self.assertNotIn("are structurally incoherent", report.lower())
        self.assertNotIn("not LAIF-native means legally invalid", report)
        self.assertNotIn("not LAIF-native means governance-invalid", report)


    def test_readme_contains_product_mode_and_authority_boundaries(self):
        """README states Phase 3L product baseline and legal authority limits."""
        readme = Path("README.md").read_text(encoding="utf-8")

        for phrase in (
            "structural governance integrity framework",
            "LAIF-native certification",
            "External framework diagnostic assessment",
            "Remediation / patch guidance",
            "Repository governance / CI validation",
            "does not determine legal validity",
            "does not claim authority over external jurisdictions",
            "does not require external frameworks to use LAIF vocabulary",
            "not LAIF-native",
            "deterministic rubric outputs",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme)

    def test_result_taxonomy_defines_mode_scoped_result_channels(self):
        """Result taxonomy distinguishes certification, diagnostics, and repo governance."""
        taxonomy_path = Path("docs/governance/RESULT_TAXONOMY.md")
        self.assertTrue(taxonomy_path.exists())
        taxonomy = taxonomy_path.read_text(encoding="utf-8")

        for phrase in (
            "LAIF-native certification",
            "External framework diagnostic finding",
            "Protected-artifact block",
            "Semantic-boundary advisory",
            "Legal validity non-determination",
            "FAIL must always be mode-scoped",
            "Not LAIF-native is not legal invalidity",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, taxonomy)

    def test_score_interpretation_defines_deterministic_nonlegal_scores(self):
        """Score interpretation states deterministic score boundaries."""
        score_path = Path("docs/governance/SCORE_INTERPRETATION.md")
        self.assertTrue(score_path.exists())
        score_doc = score_path.read_text(encoding="utf-8")

        for phrase in (
            "deterministic LAIF rubric outputs",
            "legal determinations",
            "statistical confidence values",
            "external regulatory compliance ratings",
            "structural_score",
            "terminology_score",
            "conceptual_proximity_score",
            "auditability_score",
            "enforceability_score",
            "overall_readiness_score",
            "sector_risk_alignment",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, score_doc)

    def test_governance_force_model_defines_required_components(self):
        """Governance-force model defines stable institutional-assessment components."""
        force_path = Path("docs/governance/GOVERNANCE_FORCE_MODEL.md")
        self.assertTrue(force_path.exists())
        force_doc = force_path.read_text(encoding="utf-8")

        for phrase in (
            "governance principles are operationalised into governance force",
            "mandate",
            "actor",
            "trigger",
            "protected interest",
            "control",
            "evidence",
            "reversibility",
            "escalation",
            "consequence",
            "auditability",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, force_doc)

    def test_external_framework_mode_labels_missing_laif_vocabulary_as_not_laif_native(self):
        """External diagnostics do not equate missing LAIF terms with legal invalidity."""
        result = assess(
            "generic external framework",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )

        self.assertEqual(result["assessment_mode"], "external_framework")
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")
        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertTrue(result["laif_canonical_remediation_required"])
        diagnostic = result["external_framework_assessment"]
        self.assertEqual(diagnostic["type"], "diagnostic")
        self.assertEqual(diagnostic["structural_assessment"], "diagnostic")
        self.assertTrue(diagnostic["not_laif_native_certification"])
        self.assertEqual(
            diagnostic["laif_native_certification_status"],
            "FAIL / NOT LAIF-NATIVE",
        )
        self.assertFalse(diagnostic["legal_or_governance_invalidity_claimed"])
        self.assertIn("not LAIF-native", diagnostic["canonical_terminology_note"])
        self.assertIn("not LAIF-native", " ".join(result["gaps"]) + diagnostic["canonical_terminology_note"])

    def test_conceptual_proximity_is_diagnostic_and_cannot_override_external_formal_fail(self):
        """Diagnostic proximity remains separate from LAIF-native certification."""
        result = assess(
            "high scalar external fixture",
            "voluntary_framework",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )

        self.assertGreaterEqual(result["conceptual_proximity_score"], 40)
        self.assertGreaterEqual(result["overall_readiness_score"], 40)
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")
        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertEqual(result["strong_laif_compliance"], "FAIL")
        self.assertEqual(
            result["external_framework_assessment"]["structural_assessment"],
            "diagnostic",
        )

    def test_laif_native_mode_preserves_strict_terminology_behavior(self):
        """LAIF-native certification remains strict when canonical terms are absent."""
        result = assess(
            "native claim without canonical vocabulary",
            "laif_native_candidate",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="laif_native_certification",
        )

        self.assertEqual(result["assessment_mode"], "laif_native_certification")
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")
        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertEqual(result["strong_laif_compliance"], "FAIL")
        self.assertTrue(result["laif_canonical_remediation_required"])
        self.assertEqual(result["terminology_score"], 0)
        self.assertIn(
            "Canonical terminology is load-bearing",
            result["external_framework_assessment"]["canonical_terminology_note"],
        )

    def test_new_assessment_mode_fields_are_present_and_deterministic(self):
        """Mode-separation output is stable across repeated assessments."""
        first = assess(
            "deterministic external fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        second = assess(
            "deterministic external fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        keys = (
            "assessment_mode",
            "formal_laif_native_compliance",
            "external_framework_assessment",
            "laif_canonical_remediation_required",
        )
        for key in keys:
            self.assertIn(key, first)
            self.assertEqual(first[key], second[key])
        self.assertIn("formal_laif_compliance", first)
        self.assertIn("strong_laif_compliance", first)
        self.assertIn("score_breakdown", first)

    def test_default_mode_is_external_unless_input_is_explicitly_laif_native(self):
        """Existing call sites default to diagnostic external framework mode."""
        generic = assess("generic fixture", "diagnostic_fixture", GENERIC_REGULATORY_DOCUMENT)
        canonical = assess("canonical fixture", "diagnostic_fixture", CANONICAL_LAIF_DOCUMENT)

        self.assertEqual(generic["assessment_mode"], "external_framework")
        self.assertEqual(canonical["assessment_mode"], "laif_native_certification")
        self.assertEqual(canonical["formal_laif_native_compliance"], "PASS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
