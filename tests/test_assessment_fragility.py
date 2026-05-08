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

from assessment_engine import assess, generate_markdown_report, _safe_executive_risk_text
from test_real_world import _print_scorecard
from validate import CONTEXT_WINDOW, PARAPHRASE_GUARDS, find_paraphrase_violations


def _legacy_public_phrase(*parts):
    """Assemble legacy blocked public-output phrases without source literals."""
    return "".join(parts)


LEGACY_FINAL_LABEL = _legacy_public_phrase("Final ", "verdict")
LEGACY_FAILURE_LABEL = _legacy_public_phrase("Primary ", "Failure Modes")
LEGACY_FORMAL_GATE = _legacy_public_phrase(
    "This document fails formal ",
    "LAIF v1.2 compliance",
)
LEGACY_FORMAL_GATE_SENTENCE = LEGACY_FORMAL_GATE + "."
LEGACY_CONSTRUCT_GATE = _legacy_public_phrase(
    "Missing any single ",
    "construct = ",
    "FAIL",
)

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
        self.assertNotIn(LEGACY_FORMAL_GATE_SENTENCE, report)
        self.assertNotIn(LEGACY_CONSTRUCT_GATE, report)
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
        self.assertIn("Each required LAIF-native construct remains necessary for certification", report)
        self.assertNotIn("#### Gaps", report)
        for unsafe_phrase in (
            LEGACY_FINAL_LABEL,
            LEGACY_FAILURE_LABEL,
            LEGACY_FORMAL_GATE,
            LEGACY_CONSTRUCT_GATE,
            "legally invalid",
            "governance-invalid",
            "governance-worthless",
            "structurally incoherent",
        ):
            with self.subTest(unsafe_phrase=unsafe_phrase):
                self.assertNotIn(unsafe_phrase, report)
        self.assertNotIn("Common Failure Modes", report)
        self.assertNotIn("Primary structural failure", report)
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


    def test_safe_executive_risk_text_removes_unsafe_public_phrases(self):
        """Executive risk rendering is safe without changing underlying scoring fields."""
        unsafe = (
            f"{LEGACY_FINAL_LABEL}: {LEGACY_FORMAL_GATE_SENTENCE} "
            f"{LEGACY_FAILURE_LABEL}: {LEGACY_CONSTRUCT_GATE}; "
            "legally invalid; governance-invalid; governance-worthless; structurally incoherent"
        )
        rendered = _safe_executive_risk_text(unsafe)

        self.assertIn("Executive diagnostic detail", rendered)
        self.assertIn("formal LAIF-native certification gate", rendered)
        self.assertIn("Primary LAIF diagnostic gaps", rendered)
        self.assertIn("Each required LAIF-native construct remains necessary for certification", rendered)
        for unsafe_phrase in (
            LEGACY_FINAL_LABEL,
            LEGACY_FAILURE_LABEL,
            LEGACY_FORMAL_GATE,
            LEGACY_CONSTRUCT_GATE,
            "legally invalid",
            "governance-invalid",
            "governance-worthless",
            "structurally incoherent",
        ):
            with self.subTest(unsafe_phrase=unsafe_phrase):
                self.assertNotIn(unsafe_phrase, rendered)


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


    def test_structured_remediation_patches_are_present_and_schema_complete(self):
        """External framework assessments expose deterministic remediation patch records."""
        result = assess(
            "structured patch external fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        required_keys = {
            "patch_id",
            "assessment_mode",
            "source_document",
            "finding_type",
            "severity",
            "laif_construct",
            "governance_force_component",
            "diagnostic_gap",
            "source_evidence",
            "evidence_trace_ids",
            "recommended_patch",
            "canonical_clause_if_adopting_laif",
            "operational_control",
            "evidence_artifact",
            "verification_test",
            "responsible_actor",
            "implementation_priority",
            "legal_authority_boundary",
        }

        self.assertIn("remediation_patches", result)
        self.assertIsInstance(result["remediation_patches"], list)
        self.assertGreater(len(result["remediation_patches"]), 0)
        self.assertLessEqual(len(result["remediation_patches"]), 12)
        for patch in result["remediation_patches"]:
            with self.subTest(patch=patch.get("patch_id")):
                self.assertIsInstance(patch, dict)
                self.assertTrue(required_keys.issubset(patch))
                self.assertEqual(patch["assessment_mode"], "external_framework")
                self.assertEqual(patch["source_document"], "structured patch external fixture")
                self.assertEqual(patch["legal_authority_boundary"], "diagnostic_only")
                self.assertNotIn("legally invalid", patch["recommended_patch"].lower())
                self.assertNotIn("legal invalidity", patch["recommended_patch"].lower())

    def test_external_construct_gap_priorities_are_not_automatically_optional(self):
        """External construct gaps use severity unless explicitly canonical/adoption-focused."""
        result = assess(
            "construct priority external fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        by_gap = {patch["diagnostic_gap"]: patch for patch in result["remediation_patches"]}

        for gap in (
            "Missing LAIF construct: Coupling",
            "Missing LAIF construct: Coherence Test",
        ):
            with self.subTest(gap=gap):
                self.assertIn(gap, by_gap)
                self.assertNotEqual(
                    by_gap[gap]["implementation_priority"],
                    "optional_laif_adoption",
                )
                self.assertEqual(by_gap[gap]["legal_authority_boundary"], "diagnostic_only")

        canonical_gap = "terminological — no canonical LAIF terms present"
        self.assertIn(canonical_gap, by_gap)
        self.assertEqual(
            by_gap[canonical_gap]["implementation_priority"],
            "optional_laif_adoption",
        )
        self.assertEqual(by_gap[canonical_gap]["legal_authority_boundary"], "diagnostic_only")

    def test_structured_remediation_patch_generation_is_deterministic(self):
        """Repeated assessments produce identical remediation patch payloads."""
        first = assess(
            "repeatable patch fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        second = assess(
            "repeatable patch fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        self.assertEqual(first["remediation_patches"], second["remediation_patches"])

    def test_markdown_renders_structured_remediation_patch_set_safely(self):
        """Generated markdown includes structured patches and boundary language."""
        result = assess(
            "markdown patch fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        report = generate_markdown_report([result], report_date="May 2026")

        self.assertIn("Structured Remediation Patch Set", report)
        self.assertIn(
            "These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.",
            report,
        )
        for unsafe_phrase in (
            "legally invalid",
            "governance-invalid",
            "governance-worthless",
            "structurally incoherent",
            "Final verdict",
            "Primary Failure Modes",
        ):
            with self.subTest(unsafe_phrase=unsafe_phrase):
                self.assertNotIn(unsafe_phrase, report)

    def test_remediation_patch_schema_document_exists_and_declares_boundaries(self):
        """Schema documentation contains required field names and boundary language."""
        schema_path = Path(__file__).resolve().parents[1] / "docs" / "governance" / "REMEDIATION_PATCH_SCHEMA.md"
        self.assertTrue(schema_path.exists())
        text = schema_path.read_text(encoding="utf-8")
        for field in (
            "patch_id",
            "assessment_mode",
            "source_document",
            "finding_type",
            "severity",
            "laif_construct",
            "governance_force_component",
            "diagnostic_gap",
            "source_evidence",
            "evidence_trace_ids",
            "recommended_patch",
            "canonical_clause_if_adopting_laif",
            "operational_control",
            "evidence_artifact",
            "verification_test",
            "responsible_actor",
            "implementation_priority",
            "legal_authority_boundary",
        ):
            with self.subTest(field=field):
                self.assertIn(field, text)
        self.assertIn("Remediation patches are diagnostic guidance", text)
        self.assertIn("Patches do not determine legal validity", text)
        self.assertIn("Patches do not certify LAIF-native compliance", text)

    def test_console_output_reports_structured_patch_count_safely(self):
        """Console scorecard stays concise while surfacing structured patch counts."""
        result = assess(
            "console patch fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            _print_scorecard(result)
        output = buf.getvalue()

        self.assertIn("Structured remediation patches:", output)
        self.assertIn("LAIF-PATCH-", output)
        for unsafe_phrase in (
            "legally invalid",
            "governance-invalid",
            "governance-worthless",
            "structurally incoherent",
            "Final verdict",
            "Primary Failure Modes",
        ):
            with self.subTest(unsafe_phrase=unsafe_phrase):
                self.assertNotIn(unsafe_phrase, output)


    def test_sector_profile_clinical_external_metadata(self):
        """Clinical sector profile fields are returned as diagnostic metadata."""
        text = "Clinical AI supports patient safety with clinician override, incident log, and clinical fallback."
        result = assess(
            "clinical profile fixture",
            "external_framework",
            text,
            sector="clinical_ai",
            assessment_mode="external_framework",
        )
        self.assertEqual(result["sector_profile"], "clinical_ai")
        self.assertEqual(result["sector_profile_label"], "Clinical AI Deployment")
        self.assertGreater(len(result["sector_profile_diagnostic_signals"]), 0)

    def test_unknown_sector_profile_falls_back_to_general(self):
        """Unknown sector values resolve to the general diagnostic overlay."""
        result = assess(
            "unknown sector fixture",
            "external_framework",
            GENERIC_REGULATORY_DOCUMENT,
            sector="unknown_sector",
            assessment_mode="external_framework",
        )
        self.assertEqual(result["sector_profile"], "general_ai_governance")
        self.assertEqual(result["sector_profile_label"], "General AI Governance")

    def test_sector_profile_signals_are_present_for_relevant_text(self):
        """Sector-relevant vocabulary creates diagnostic signals only."""
        text = "Procurement requires a vendor contract clause, audit access, vendor disclosure, and assurance artefact."
        result = assess(
            "procurement profile fixture",
            "external_framework",
            text,
            sector="procurement_vendor_governance",
            assessment_mode="external_framework",
        )
        signals = result["sector_profile_diagnostic_signals"]
        self.assertIn("procurement", signals)
        self.assertIn("vendor", signals)
        self.assertIn("contract clause", signals)

    def test_sector_profiles_do_not_change_formal_compliance_or_verdict(self):
        """Profile metadata cannot convert formal failure into pass status."""
        clinical_text = "Clinical patient safety clinician override incident log clinical fallback patient treatment."
        general = assess(
            "profile invariant general fixture",
            "external_framework",
            clinical_text,
            sector="general_ai_governance",
            assessment_mode="external_framework",
        )
        clinical = assess(
            "profile invariant clinical fixture",
            "external_framework",
            clinical_text,
            sector="clinical_ai",
            assessment_mode="external_framework",
        )
        self.assertEqual(general["formal_laif_native_compliance"], clinical["formal_laif_native_compliance"])
        self.assertEqual(clinical["formal_laif_native_compliance"], "FAIL")
        self.assertEqual(clinical["strong_laif_compliance"], "FAIL")
        self.assertNotEqual(clinical["strong_laif_compliance"], "STRONG PASS")

    def test_sector_profiles_do_not_change_score_weights_or_certification_pathways(self):
        """Profile fields leave the weighted score model and certification mode boundaries intact."""
        text = GENERIC_REGULATORY_DOCUMENT + " Patient clinician clinical fallback incident log."
        result = assess(
            "score weight profile fixture",
            "external_framework",
            text,
            sector="clinical_ai",
            assessment_mode="external_framework",
        )
        expected = round(
            0.25 * result["structural_score"]
            + 0.15 * result["terminology_score"]
            + 0.20 * result["conceptual_proximity_score"]
            + 0.20 * result["auditability_score"]
            + 0.20 * result["enforceability_score"]
        )
        self.assertEqual(result["overall_readiness_score"], expected)
        self.assertTrue(result["external_framework_assessment"]["not_laif_native_certification"])
        self.assertEqual(result["external_framework_assessment"]["type"], "diagnostic")

    def test_external_framework_profile_legal_boundary_remains_diagnostic_only(self):
        """External-framework profile patches remain diagnostic-only."""
        result = assess(
            "profile legal boundary fixture",
            "external_framework",
            GENERIC_REGULATORY_DOCUMENT,
            sector="government_service_delivery",
            assessment_mode="external_framework",
        )
        self.assertGreater(len(result["remediation_patches"]), 0)
        for patch in result["remediation_patches"]:
            self.assertEqual(patch["legal_authority_boundary"], "diagnostic_only")

    def test_markdown_includes_sector_profile_context_and_boundary_note(self):
        """Report sector context includes profile metadata and non-authority boundary."""
        result = assess(
            "sector report fixture",
            "external_framework",
            "Student grading assessment requires accessibility record, appeal pathway, and student-impact review.",
            sector="education_ai",
            assessment_mode="external_framework",
        )
        report = generate_markdown_report([result], report_date="May 2026")
        self.assertIn("Education AI", report)
        self.assertIn("Profile-specific remediation themes", report)
        self.assertIn("Profile-specific evidence cautions", report)
        self.assertIn("Profile diagnostics do not determine legal validity, LAIF-native certification, or sector compliance", report)

    def test_console_output_includes_sector_profile_safely(self):
        """Console scorecard reports concise profile metadata without unsafe phrases."""
        result = assess(
            "console profile fixture",
            "external_framework",
            "Clinical patient safety clinician override incident log.",
            sector="clinical_ai",
            assessment_mode="external_framework",
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            _print_scorecard(result)
        output = buf.getvalue()
        self.assertIn("Sector profile:", output)
        self.assertIn("Profile signals:", output)
        for unsafe_phrase in (
            "legally invalid",
            "governance-invalid",
            "governance-worthless",
            "structurally incoherent",
            "Final verdict",
            "Primary Failure Modes",
        ):
            with self.subTest(unsafe_phrase=unsafe_phrase):
                self.assertNotIn(unsafe_phrase, output)

    def test_sector_profiles_document_exists_and_lists_supported_keys_and_boundaries(self):
        """Sector profile documentation declares supported profiles and boundaries."""
        doc_path = Path(__file__).resolve().parents[1] / "docs" / "governance" / "SECTOR_PROFILES.md"
        self.assertTrue(doc_path.exists())
        text = doc_path.read_text(encoding="utf-8")
        for key in (
            "government_service_delivery",
            "departmental_ai_development",
            "procurement_vendor_governance",
            "clinical_ai",
            "employment_hr_ai",
            "education_ai",
            "general_ai_governance",
        ):
            with self.subTest(key=key):
                self.assertIn(key, text)
        for phrase in (
            "Profiles do not alter `validate.py`",
            "Profiles do not alter formal LAIF-native certification",
            "Profiles do not alter scoring weights",
            "Profiles do not determine legal validity",
            "Profiles do not create sector-specific compliance gates",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_sector_profile_unsafe_grep_gates_remain_clear(self):
        """Unsafe source-string cleanup gates remain protected."""
        engine_text = (Path(__file__).resolve().parents[1] / "assessment_engine.py").read_text(encoding="utf-8")
        console_text = (Path(__file__).resolve().parents[1] / "test_real_world.py").read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_FINAL_LABEL, engine_text)
        self.assertNotIn(LEGACY_FAILURE_LABEL, engine_text)
        self.assertNotIn(LEGACY_FORMAL_GATE, engine_text)
        self.assertNotIn(LEGACY_CONSTRUCT_GATE, engine_text)
        self.assertNotIn("md.replace", console_text)


    def test_evidence_traces_are_returned_with_required_keys_and_offsets(self):
        """Evidence traces are deterministic dict records with exact source spans."""
        result = assess(
            "evidence trace fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        self.assertIn("evidence_traces", result)
        self.assertIsInstance(result["evidence_traces"], list)
        self.assertGreater(len(result["evidence_traces"]), 0)
        required = {
            "trace_id",
            "source_document",
            "source_type",
            "assessment_mode",
            "evidence_type",
            "matched_text",
            "normalized_match",
            "start_char",
            "end_char",
            "match_rule",
            "confidence",
            "supports",
            "legal_authority_boundary",
        }
        for trace in result["evidence_traces"]:
            self.assertIsInstance(trace, dict)
            self.assertTrue(required.issubset(trace.keys()))
            if trace["confidence"] in ("exact", "deterministic_pattern"):
                self.assertEqual(
                    trace["matched_text"],
                    GENERIC_REGULATORY_DOCUMENT[trace["start_char"]:trace["end_char"]],
                )
            elif trace["confidence"] == "fallback_required":
                self.assertEqual(trace["matched_text"], "")
                self.assertIsNone(trace["start_char"])
                self.assertIsNone(trace["end_char"])

    def test_evidence_trace_fallback_records_do_not_invent_evidence(self):
        """Fallback traces carry no quoted text or source offsets."""
        result = assess(
            "fallback evidence trace fixture",
            "external_framework",
            "No meaningful governance source terms here.",
            assessment_mode="external_framework",
        )
        fallback_traces = [t for t in result["evidence_traces"] if t["confidence"] == "fallback_required"]
        self.assertGreater(len(fallback_traces), 0)
        for trace in fallback_traces:
            self.assertEqual(trace["evidence_type"], "reviewer_confirmation_required")
            self.assertEqual(trace["matched_text"], "")
            self.assertIsNone(trace["start_char"])
            self.assertIsNone(trace["end_char"])
            self.assertEqual(trace["confidence"], "fallback_required")

    def test_evidence_traces_do_not_change_formal_compliance_or_convert_fail(self):
        """Trace metadata does not affect formal LAIF-native certification."""
        result = assess(
            "formal fail evidence trace fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        self.assertIn("evidence_traces", result)
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")
        self.assertEqual(result["formal_laif_compliance"], "FAIL")
        self.assertNotEqual(result["formal_laif_native_compliance"], "PASS")

    def test_remediation_patches_include_evidence_trace_ids_key(self):
        """Structured patches include optional evidence trace links."""
        result = assess(
            "patch trace link fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        self.assertGreater(len(result["remediation_patches"]), 0)
        for patch in result["remediation_patches"]:
            self.assertIn("evidence_trace_ids", patch)
            self.assertIsInstance(patch["evidence_trace_ids"], list)

    def test_markdown_includes_evidence_trace_summary_and_boundary_note(self):
        """Generated markdown surfaces compact trace counts and authority boundary."""
        result = assess(
            "markdown evidence trace fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        report = generate_markdown_report([result], report_date="May 2026")
        self.assertIn("Evidence Trace Summary", report)
        self.assertIn(
            "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
            report,
        )
        self.assertIn("Evidence trace IDs:", report)

    def test_console_output_includes_evidence_trace_counts(self):
        """Console output reports concise evidence-trace counts only."""
        result = assess(
            "console evidence trace fixture",
            "binding_regulation",
            GENERIC_REGULATORY_DOCUMENT,
            assessment_mode="external_framework",
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            _print_scorecard(result)
        output = buf.getvalue()
        self.assertIn("Evidence traces:", output)
        self.assertIn("Exact/deterministic traces:", output)
        self.assertIn("Fallback-required traces:", output)

    def test_evidence_trace_model_document_exists_and_declares_required_boundaries(self):
        """Evidence trace model documentation declares non-hallucination boundaries."""
        doc_path = Path(__file__).resolve().parents[1] / "docs" / "governance" / "EVIDENCE_TRACE_MODEL.md"
        self.assertTrue(doc_path.exists())
        text = doc_path.read_text(encoding="utf-8")
        for phrase in (
            "Non-Hallucination Rule",
            "Exact Text Presence Requirement",
            "Reviewer-Confirmation Fallback",
            "Legal / Authority Boundary",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_evidence_trace_count_cap_and_determinism(self):
        """Trace extraction is capped and stable across repeated assessments."""
        text = (GENERIC_REGULATORY_DOCUMENT + "\n") * 10
        first = assess(
            "trace cap fixture",
            "binding_regulation",
            text,
            assessment_mode="external_framework",
        )
        second = assess(
            "trace cap fixture",
            "binding_regulation",
            text,
            assessment_mode="external_framework",
        )
        self.assertLessEqual(len(first["evidence_traces"]), 20)
        self.assertEqual(first["evidence_traces"], second["evidence_traces"])



class Phase3QCalibrationScoreJustificationTests(unittest.TestCase):
    """Phase 3Q calibration metadata remains interpretive and deterministic."""

    def _external_result(self, text=GENERIC_REGULATORY_DOCUMENT, sector="high_impact_employment"):
        return assess(
            "phase 3q fixture",
            "binding_regulation",
            text,
            sector=sector,
            assessment_mode="external_framework",
        )

    def test_phase_3q_assess_returns_calibration_metadata_fields(self):
        result = self._external_result()
        for key in (
            "score_interpretation",
            "score_justification",
            "dimension_justifications",
            "calibration_cautions",
            "gaming_risk_notes",
        ):
            self.assertIn(key, result)

    def test_phase_3q_score_interpretation_uses_laif_model_signal_language(self):
        result = self._external_result()
        interp = result["score_interpretation"]
        self.assertIn("LAIF-model signal", interp)
        self.assertIn("diagnostic interpretation", interp)
        self.assertIn("not a legal verdict", interp)
        self.assertNotIn("legal compliance rating", interp.lower())
        self.assertNotIn("valid under law", interp.lower())

    def test_phase_3q_dimension_justifications_schema_is_complete(self):
        result = self._external_result()
        required = {
            "dimension",
            "score",
            "band",
            "interpretation",
            "fired_signal_count",
            "missed_signal_count",
            "dominant_strengths",
            "dominant_gaps",
            "calibration_note",
            "gaming_caution",
        }
        self.assertEqual(len(result["dimension_justifications"]), 5)
        for record in result["dimension_justifications"]:
            self.assertTrue(required.issubset(record))

    def test_phase_3q_dimension_justifications_do_not_expose_raw_regex_patterns(self):
        result = self._external_result()
        blob = repr(result["dimension_justifications"])
        self.assertNotIn(r"\b", blob)
        self.assertNotIn("(?:", blob)
        self.assertNotIn(".{0,", blob)

    def test_phase_3q_metadata_preserves_existing_score_values(self):
        result = self._external_result()
        expected_overall = round(
            result["structural_score"] * 0.25
            + result["terminology_score"] * 0.15
            + result["conceptual_proximity_score"] * 0.20
            + result["auditability_score"] * 0.20
            + result["enforceability_score"] * 0.20
        )
        self.assertEqual(result["overall_readiness_score"], expected_overall)
        self.assertEqual(result["score_justification"]["overall_score"], result["overall_readiness_score"])
        for dim in result["dimension_justifications"]:
            score_key = {
                "structural": "structural_score",
                "terminology": "terminology_score",
                "conceptual": "conceptual_proximity_score",
                "auditability": "auditability_score",
                "enforceability": "enforceability_score",
            }[dim["dimension"]]
            self.assertEqual(dim["score"], result[score_key])

    def test_phase_3q_metadata_preserves_formal_laif_native_compliance(self):
        result = self._external_result()
        expected_native = result["formal_laif_compliance"]
        self.assertEqual(result["formal_laif_native_compliance"], expected_native)
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")

    def test_phase_3q_high_conceptual_low_terminology_creates_caution(self):
        result = self._external_result()
        caution_ids = {c["caution_id"] for c in result["calibration_cautions"]}
        self.assertIn("conceptual-high-terminology-low", caution_ids)

    def test_phase_3q_high_sector_alignment_low_readiness_creates_gaming_note(self):
        result = self._external_result()
        note_ids = {n["note_id"] for n in result["gaming_risk_notes"]}
        self.assertIn("sector-density-over-readiness", note_ids)
        note_blob = " ".join(n["message"] for n in result["gaming_risk_notes"])
        self.assertIn("possible keyword or signal density risk", note_blob.lower())
        self.assertIn("requires structural evidence review", note_blob.lower())
        self.assertIn("not a finding of bad faith", note_blob.lower())
        self.assertIn("not a legal invalidity claim", note_blob.lower())

    def test_phase_3q_generated_markdown_includes_calibration_section(self):
        result = self._external_result()
        report = generate_markdown_report([result], report_date="May 2026")
        self.assertIn("Score Calibration and Justification", report)

    def test_phase_3q_generated_markdown_includes_boundary_note(self):
        result = self._external_result()
        report = generate_markdown_report([result], report_date="May 2026")
        self.assertIn(
            "Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.",
            report,
        )

    def test_phase_3q_generated_markdown_does_not_expose_raw_regex_syntax(self):
        result = self._external_result()
        report = generate_markdown_report([result], report_date="May 2026")
        self.assertNotIn(r"\b", report)
        self.assertNotIn("(?:", report)

    def test_phase_3q_console_output_includes_score_band_and_counts(self):
        result = self._external_result()
        buf = io.StringIO()
        with redirect_stdout(buf):
            _print_scorecard(result)
        output = buf.getvalue()
        self.assertIn("Score band:", output)
        self.assertIn("Calibration cautions:", output)
        self.assertIn("Gaming risk notes:", output)

    def test_phase_3q_calibration_doc_exists_with_required_sections_and_boundaries(self):
        path = Path("docs/governance/CALIBRATION_SCORE_JUSTIFICATION.md")
        self.assertTrue(path.exists())
        text = path.read_text()
        for heading in (
            "## Purpose",
            "## What LAIF Scores Are",
            "## What LAIF Scores Are Not",
            "## Assessment Mode Boundary",
            "## Score Components",
            "## Fired and Missed Signal Interpretation",
            "## Calibration Limits",
            "## False Positive / False Negative Risks",
            "## Anti-Gaming Boundary",
            "## Evidence Trace Relationship",
            "## Sector Profile Relationship",
            "## Remediation Patch Relationship",
            "## Reporting Boundary",
            "## Future Calibration Work",
        ):
            self.assertIn(heading, text)
        for phrase in (
            "Scores do not certify LAIF-native compliance",
            "High conceptual, sector, or evidence proximity cannot override formal LAIF-native failure",
            "Keyword stuffing without structural evidence is a gaming risk",
            "Evidence traces do not prove implementation",
            "Sector profiles contextualize diagnostics",
            "Remediation patches are diagnostic unless separately adopted by an authority",
        ):
            self.assertIn(phrase, text)

    def test_phase_3q_unsafe_grep_gates_still_pass(self):
        evidence_doc = Path("docs/governance/EVIDENCE_TRACE_MODEL.md").read_text()
        engine = Path("assessment_engine.py").read_text()
        real_world = Path("test_real_world.py").read_text()
        self.assertIn("matched_text must equal", evidence_doc)
        self.assertNotIn(LEGACY_FINAL_LABEL, engine)
        self.assertNotIn(LEGACY_FAILURE_LABEL, engine)
        self.assertNotIn(LEGACY_FORMAL_GATE, engine)
        self.assertNotIn(LEGACY_CONSTRUCT_GATE, engine)
        self.assertNotIn("md.replace", real_world)

    def test_phase_3q_repeated_assess_calls_are_deterministic_for_calibration_metadata(self):
        first = self._external_result()
        second = self._external_result()
        for key in (
            "score_interpretation",
            "score_justification",
            "dimension_justifications",
            "calibration_cautions",
            "gaming_risk_notes",
        ):
            self.assertEqual(first[key], second[key])


if __name__ == "__main__":
    unittest.main(verbosity=2)
