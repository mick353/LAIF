#!/usr/bin/env python3
"""Characterization tests for LAIF assessment fragility calibration.

These tests intentionally document current false-negative and regex-boundary
behavior. They are diagnostic coverage, not policy changes: failing formal
terminology, low conceptual proximity, or paraphrase findings here should be
read as current engine behavior unless the engine crashes or misreports the
failure channel.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from assessment_engine import assess
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
