#!/usr/bin/env python3
"""
LAIF Canonical Specification — laif_spec.py
--------------------------------------------
Single source of truth for LAIF v1.2 canonical terms, their forbidden
paraphrases, and the structural identifiers for the Integrity Layer and
Coherence Test.

Usage:
    from laif_spec import CANONICAL_TERMS, INTEGRITY_LAYER, COHERENCE_TEST

All terms in CANONICAL_TERMS are structurally load-bearing (LAIF v1.2 Part One,
Toolkit §1). Paraphrases lose enforcement meaning because they de-couple the
governance restriction from the specific human interest it protects.

validate.py and assessment_engine.py may import from this module where
safe to do so without altering their validated behaviour.
"""

# ── Canonical terms and their forbidden paraphrases ──────────────────────────
# Each key is the LAIF v1.2 canonical term.
# Each value is a list of forbidden paraphrases (triggers for LAIF paraphrase guards).
# Source: LAIF_Compliance_Toolkit.txt §1 — Operational Standards.

CANONICAL_TERMS = {
    "Coupling": [
        "alignment",
        "connection",
        "linkage",
    ],
    "Structural Transparency": [
        "output transparency",
        "transparency conditions",
    ],
    "Structural Honesty": [
        "model honesty",
        "system honesty",
        "honesty conditions",
    ],
    "Structural Containment": [
        "boundary controls",
        "scope controls",
        "containment conditions",
    ],
    "Reversibility": [
        "rollback requirement",
        "rollback clause",
        "rollback condition",
        "rollback capability",
        "modifiability requirement",
    ],
    "Coherence Test": [
        "coherence check",
        "alignment test",
        "governance test",
    ],
    "Integrity Layer": [
        "precondition layer",
        "baseline conditions",
        "deployment preconditions",
    ],
    "Pre-Deployment Coherence Assessment": [
        "pre-deployment assessment",
        "deployment assessment",
        "PDCA equivalent",
    ],
}

# ── Integrity Layer component identifiers ────────────────────────────────────
# Source: LAIF v1.2 Part Two — all three must be satisfied simultaneously.
# Partial satisfaction = full failure (threshold gate, not checklist).

INTEGRITY_LAYER = {
    "A.1": "Structural Transparency",
    "A.2": "Structural Honesty",
    "A.3": "Structural Containment",
}

# ── Coherence Test questions ──────────────────────────────────────────────────
# Source: LAIF v1.2 Part One — Coherence Standard.
# Failure at Q1 = automatic full failure. All three are structurally interdependent.

COHERENCE_TEST = {
    "Q1": "Coupling — does the deployment identify and protect the specific human interest at risk?",
    "Q2": "Consistency — would the governance logic produce workable outcomes at all comparable scales?",
    "Q3": "Reversibility — does the deployment preserve future actors' capacity to reverse or modify?",
}

# ── Framework hierarchy ───────────────────────────────────────────────────────
# Source: LAIF v1.2 Principle 3 — Framework Hierarchy.
# Tier 1 (Foundational Principles) > Tier 2 (Provisions) > Tier 3 (Operational Standards).
# Tier 3 can be revised; Tier 1 and Tier 2 cannot be contradicted by Tier 3 revisions.

FRAMEWORK_TIERS = {
    1: "Foundational Principles (non-amendable)",
    2: "Provisions (derived from Foundational Principles)",
    3: "Operational Standards (Toolkit — can be revised without amending Tier 1/2)",
}

# ── Deployment risk tier labels ───────────────────────────────────────────────
# Source: LAIF_Compliance_Toolkit.txt §7 — Tiering by stakes and structural depth.
# These are the four tiers produced by _deployment_risk_tier() in assessment_engine.py.

DEPLOYMENT_RISK_TIERS = {
    "CRITICAL": "Fundamental structural gaps present; deployment should be blocked pending remediation.",
    "HIGH":     "Significant compliance gaps; deployment requires major remediation before authorisation.",
    "MODERATE": "Partial alignment; targeted remediation required; deployment conditional.",
    "LOW":      "All preconditions met; standard ongoing monitoring applies.",
}
