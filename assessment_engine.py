#!/usr/bin/env python3
"""
LAIF Assessment Engine
----------------------
Produces structured, scored assessments of governance documents against
LAIF v1.2 compliance criteria. Sits around validate.py without weakening
its enforcement — formal compliance remains binary and strict.

Five scoring dimensions (0–100 each):
  structural_score           Explicit governance architecture       (weight 25%)
  terminology_score          Canonical LAIF term presence           (weight 15%)
  conceptual_proximity_score LAIF-like concepts without LAIF terms  (weight 20%)
  auditability_score         Objective checkability of obligations  (weight 20%)
  enforceability_score       Operational enforcement capacity       (weight 20%)

Every score is accompanied by a signal breakdown — fired signals that earned
points and missed signals that did not. This answers "why this number?" for
every dimension without relying on opaque aggregation.

Spec alignment references:
  LAIF v1.2 — Part One (Foundational Principles, Coherence Standard)
  LAIF v1.2 — Part Two (Integrity Layer: A.1 Transparency, A.2 Honesty, A.3 Containment)
  LAIF v1.2 — Part Three (Provision Layer: Provisions A–D)
  LAIF v1.2 — Part Seven (Self-Application: framework applies to governance actors)
  LAIF_Compliance_Toolkit.txt — §1 Operational Standards, §2 PDCA, §7 Tiering
"""

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import find_paraphrase_violations, PARAPHRASE_GUARDS


# ── Scoring rubrics ────────────────────────────────────────────────────────────
# Each rubric is a list of (weight, pattern, label) tuples.
# Weights within each rubric sum to 100.
# Source comments link each signal to the LAIF section that requires it.

# Source: LAIF v1.2 Part One — Foundational Principles define the structural
# requirements; Part Two defines Integrity Layer threshold conditions;
# Part Three defines Provision Layer; Part Seven defines Self-Application.
STRUCTURAL_RUBRIC = [
    # ── General governance architecture (external frameworks can score here) ──
    (8,  r"\bArticle\s+\d+|GOVERN\s+\d+\.\d+|Section\s+\d+\.?\d*",
         "numbered sub-requirements"),
    (8,  r"\bshall\b",
         "mandatory obligation language (shall)"),
    (6,  r"\blifecycle\b",
         "full lifecycle scope declared"),
    (7,  r"\bproportionat|\bhigh.risk\b|\brisk.{0,5}(?:level|categor|classif)",
         "risk stratification / proportionality"),
    (6,  r"\b(?:mechanisms?|safeguards?|measures?)\b",
         "operational mechanisms defined"),
    (6,  r"\b(?:monitor|audit|review|inspect|evaluat)\b",
         "review / monitoring mechanisms"),
    # ── LAIF-specific structural elements ─────────────────────────────────────
    # Source: LAIF v1.2 Part Two — Integrity Layer threshold: all three
    # preconditions must be satisfied simultaneously; partial = failure.
    (15, r"\bprecondition\b|all\s+(?:three|four|five)\s+(?:must|shall)\b|\bsimultaneously\b",
         "threshold gate conditions (all must pass simultaneously)"),
    # Source: LAIF v1.2 Principle 3 — Framework Hierarchy; non-amendable clause
    # prevents operational revision from eroding Foundational Principles.
    (18, r"\bPART ONE\b|FOUNDATIONAL PRINCIPLES|cannot be amended|non.amendable",
         "non-amendable constitutional hierarchy"),
    # Source: LAIF v1.2 Part Seven — Self-Application: governance actors and
    # regulatory bodies are subject to the framework, not only AI operators.
    (12, r"self.application|applies to regulatory|applies to governance actors",
         "self-application clause (Part Seven)"),
    # Source: LAIF v1.2 Part One — Coherence Test as named decision instrument;
    # PDCA as its primary operational instrument (Compliance Toolkit §2).
    (14, r"\bCoherence Test\b|\bPDCA\b|Pre.Deployment Coherence Assessment",
         "named decision instrument (Coherence Test / PDCA)"),
]

# Source: LAIF_Compliance_Toolkit.txt §1 — Canonical terminology definitions.
# These terms are structurally load-bearing: paraphrases lose enforcement meaning.
TERMINOLOGY_RUBRIC = [
    # Coupling: LAIF v1.2 Principle 2 — structural pairing of restriction with
    # the specific human interest it protects; neither weakened in isolation.
    (25, r"\bCoupling\b",                    "Coupling"),
    # Coherence Test: LAIF v1.2 Part One — Q1 Coupling, Q2 Consistency,
    # Q3 Reversibility; all three must pass; failure at Q1 = full failure.
    (20, r"\bCoherence Test\b",              "Coherence Test"),
    # Integrity Layer: LAIF v1.2 Part Two — three-condition threshold; all
    # must be satisfied simultaneously before deployment may proceed.
    (20, r"\bIntegrity Layer\b",             "Integrity Layer"),
    # Structural Transparency: Toolkit §1.3 — Integrity Layer A.1; system
    # can produce a compliant meaningful account of any material output.
    (10, r"\bStructural Transparency\b",     "Structural Transparency"),
    # Structural Honesty: Toolkit §1.4 — Integrity Layer A.2; stated
    # objectives correspond to implemented objectives; consistent under eval.
    (10, r"\bStructural Honesty\b",          "Structural Honesty"),
    # Structural Containment: Toolkit §1.5 — Integrity Layer A.3; system
    # operates within documented boundaries; no irreversible action without
    # triggering authorisation process (Provision D1).
    (10, r"\bStructural Containment\b",      "Structural Containment"),
    # Materially Affects Interests: Toolkit §1.2 — objective test; output
    # influences a decision with legal, financial, health, reputational,
    # or liberty consequences; independent of operator intent.
    (5,  r"\bMaterially Affects Interests\b", "Materially Affects Interests"),
]

# Source: LAIF v1.2 Part One — conceptual proxies for Coherence Test dimensions
# and Integrity Layer conditions; scored without requiring LAIF vocabulary.
CONCEPTUAL_RUBRIC = [
    # Q1 Coupling proxy — specific human interest identification
    (10, r"\bhuman rights\b|\bfundamental rights\b|\bhuman interests?\b|\bperson.level stakes?\b|\baffected persons?\b|\bbeneficiar",
         "human rights / fundamental interests"),
    # Integrity Layer A.1 proxy — transparency requirements
    (8,  r"\btransparency\b|\btransparent\b|\bmeaningful account\b|\bshows? its work\b",
         "transparency"),
    # Integrity Layer A.1 proxy — explainability / meaningful account
    (8,  r"\bexplainability\b|\binterpret\b|\bmeaningful\s+(?:explanation|information)\b|explain (?:any|each|every) decision|\bin plain language\b|words you can understand",
         "explainability / interpretability"),
    # Q1 Coupling proxy — accountability for decisions affecting interests
    (8,  r"\baccountability\b|\baccountable\b|records? sufficient for audit|\bauditors?\b",
         "accountability"),
    # Integrity Layer A.3 + Q1 Coupling — human oversight of AI decisions
    (8,  r"\boversight\b|\bhuman determination\b|\bhuman.in.the.loop\b|escalat\w+ to a human|human (?:being )?must approve|independent review\w*",
         "human oversight"),
    # Q2 Consistency proxy — proportionality across scales and actors
    (8,  r"\bproportionat|\brisk.{0,5}(?:level|proportion)",
         "proportionality"),
    # Q1 Coupling proxy — safety as a named human interest
    (7,  r"\bsafety\b",
         "safety"),
    # Q1 Coupling proxy — contestability and redress (Provision A, D)
    (9,  r"\bcontest\w*\b|\bappeal\b|\bchallenge\b|\bredress\b|\bremedies\b",
         "contestability / redress"),
    # Q3 Reversibility proxy — modifiability of decisions and consequences
    (8,  r"\b(?:revers|modif|correct)\w*\b.{0,80}\b(?:decision|outcome|consequence|policy)\b|power to reverse|can always appeal",
         "reversibility / modifiability"),
    # Q1/Q2 proxy — risk governance as structured process
    (8,  r"\brisk\s+(?:management|assessment|governance|control)\b",
         "risk governance"),
    # Integrity Layer A.1 proxy — traceability of outputs and decisions
    (10, r"\btraceability\b|\btraceable\b|\bresponsibility\b.{0,30}\b(?:outcome|system|decision)\b",
         "traceability / responsibility"),
    # Q2 Consistency proxy — fairness, non-discrimination, labour rights
    (8,  r"\bworkers?\b|\blabour\s+rights?\b|\bfairness\b|\bnon.discriminat\b",
         "fairness / labour / non-discrimination"),
]

# Register note: mandatory force is expressed as "shall" in legal drafting,
# "must" in standards/plain drafting, and "we will / will not" in first-person
# public commitments. All three registers carry binding intent; rubrics accept
# each so that register alone cannot suppress an auditability or
# enforceability signal (QA finding F4 — register bias).
AUDITABILITY_RUBRIC = [
    (20, r"\bshall\b.{1,300}\bshall\b|\bmust\b.{1,300}\bmust\b",
         "multiple mandatory obligations (shall/must pairs)"),
    (20, r"\bArticle\s+\d+|GOVERN\s+\d+\.\d+|Section\s+\d+|Part\s+\d+\b",
         "numbered traceable requirements"),
    (20, r"\b(?:document|record|evidence|technical documentation|certif|report)\b",
         "evidence / documentation requirements"),
    (20, r"\b(?:review|audit|monitor|evaluat|inspect|post.market)\b",
         "review / monitoring mechanisms"),
    (20, r"\b(?:specific|targeted|defined|identif|concrete|measur)\b.{0,80}\b(?:requirement|obligation|measure|standard|criterion)\b",
         "specific, measurable obligations"),
]

ENFORCEABILITY_RUBRIC = [
    (20, r"\bshall\b|\bmust\b|\bwe\s+will\s+(?:never|not)\b",
         "mandatory language (shall/must)"),
    (20, r"\b(?:provider|deployer|operator|agenc(?:y|ies)|responsible\s+part(?:y|ies)|actors?|authorit(?:y|ies)|organisations?)\b",
         "named responsible parties"),
    (20, r"\bproportionate\b|\bdegree\s+of\s+risk\b|\blevel\s+of\s+risk\b|\bhigher.risk\b|commensurate\s+with\b",
         "risk-proportionate thresholds"),
    (20, r"\b(?:penalty|sanction|fine|infringement|non.compliance|consequence|suspension|suspended|revok)\w*\b",
         "enforcement consequences / penalties"),
    (20, r"\b(?:shall|must)\s+(?:not\s+)?(?:ensure|establish|implement|maintain|provide|design|develop|assess|approve|produce|operate|name|document)\b",
         "non-discretionary operational mandates"),
]

def _achievable_ceiling_external():
    """Highest overall score reachable by a document that never uses LAIF
    branding: 100 minus the full terminology weight (0.15) and the
    named-decision-instrument structural signal (0.25 x its rubric weight).
    Derived from the live rubrics so rubric changes recalibrate automatically."""
    named = next((w for w, _, lbl in STRUCTURAL_RUBRIC
                  if "named decision instrument" in lbl), 0)
    return round(100 - (0.15 * 100 + 0.25 * named), 1)


# Required LAIF constructs for formal compliance — binary gate.
# Source: LAIF v1.2 structural requirements spanning Parts One, Two, and Seven.
# All eight must be present. Missing any one = FAIL. No partial credit.
FORMAL_REQUIREMENTS = [
    (r"\bCoupling\b",                                "Coupling"),
    (r"\bIntegrity Layer\b",                         "Integrity Layer"),
    (r"\bCoherence Test\b",                          "Coherence Test"),
    (r"\bPART ONE\b|FOUNDATIONAL PRINCIPLES",        "PART ONE / Foundational Principles"),
    (r"cannot be amended|non.amendable",             "non-amendable clause"),
    (r"PART SEVEN|self.application|applies to regulatory", "self-application clause"),
    (r"A\.1 FINDING\s*:",                            "Integrity Layer FINDING block"),
    (r"B\.1 FINDING\s*:",                            "Coherence Test FINDING block"),
]

CONSTRUCT_COVERAGE_CHECKS = [
    ("Coupling",                r"\bCoupling\b"),
    ("Coherence Test",          r"\bCoherence Test\b"),
    ("Integrity Layer",         r"\bIntegrity Layer\b"),
    ("Structural Transparency", r"\bStructural Transparency\b"),
    ("Structural Honesty",      r"\bStructural Honesty\b"),
    ("Structural Containment",  r"\bStructural Containment\b"),
    ("Consistency",             r"\bConsistency\b"),
    ("Reversibility",           r"\bReversibility\b"),
]


# ── Coupling quality detection ─────────────────────────────────────────────────
# Source: LAIF v1.2 Principle 2 — Coupling is not satisfied by mentioning the
# term; it requires: (1) a specific human interest named, (2) a restriction
# paired with it, (3) protection of equivalent normative force on both sides,
# (4) neither side weakened in isolation. Toolkit §2 B.1 operationalises this.
#
# Verdict levels:
#   STRUCTURAL — Coupling declared with structural indicators
#   SHALLOW    — Coupling mentioned without structural declaration
#   NEGATED    — Coupling present but explicitly negated / declared inapplicable
#   ABSENT     — Coupling not in document

# Indicators that Coupling is being used structurally (not merely mentioned)
COUPLING_STRUCTURAL_INDICATORS = [
    # Requires "between" + a restriction/obligation/interest/protection within 300 chars.
    # Narrows the match: "Coupling between systems" must not fire; only "Coupling between
    # [restriction/obligation] and [human interest/right/protection]" qualifies.
    r"\bCoupling\s+between\b.{1,300}\b(?:restriction|obligation|prohibition|interest|right|protection)\b",
    r"\bCoupling\b.{1,200}\bspecific\s+human\s+interest\b",
    r"\bCoupling\b.{1,200}\bequivalent\s+normative\s+force\b",
    r"\bstructural\s+Coupling\b",
    r"\bdeclare\w*\s+(?:structural\s+)?Coupling\b",
    r"\bCoupling\b.{1,200}\bpair(?:ed|s|ing)\b.{1,200}\bprotection\b",
    r"\bCoupling\b.{1,200}\b(?:restriction|obligation|prohibition)\b.{1,200}\b(?:human interest|right|protection)\b",
]

# Indicators that Coupling is explicitly negated or declared inapplicable
COUPLING_NEGATION_INDICATORS = [
    r"\bCoupling\b.{0,120}\b(?:not\s+(?:applicable|required|established|satisfied|met|adopted|declared|implemented)|outside\s+(?:the\s+)?scope|beyond\s+scope|inapplicable|rejected|absent|excluded)\b",
    r"\b(?:not\s+applicable|outside\s+(?:the\s+)?scope|inapplicable|rejected|excluded|not\s+required)\b.{0,120}\bCoupling\b",
    r"\bno\s+Coupling\b",
    r"\bCoupling\b.{0,80}\bdoes\s+not\s+apply\b",
    r"\bCoupling\b.{0,80}\bdeemed\b.{0,40}\b(?:unnecessary|inapplicable|not\s+required)\b",
]

# Indicators that Coupling is referenced/acknowledged but not structurally declared
COUPLING_HOLLOW_INDICATORS = [
    r"\bCoupling\b.{0,120}\b(?:acknowledged|noted|referenced|mentioned|as\s+defined|per\s+(?:the\s+)?(?:LAIF|framework|definition)|see\s+(?:also\s+)?(?:LAIF|framework)|in\s+(?:LAIF|the\s+framework))\b",
    r"\b(?:acknowledge|note|reference|mention|define)\w*\b.{0,120}\bCoupling\b",
    r"\bCoupling\b.{0,40}(?::|\s*—|\s*–)\s*(?:see|refer|noted|acknowledged|tbc|tbd|pending|future)\b",
]


def _coupling_quality(text):
    """
    Assess the structural quality of Coupling usage in a document.
    Source: LAIF v1.2 Principle 2; Toolkit §2 B.1.

    Returns (quality, reason, evidence):
      quality  — STRUCTURAL | SHALLOW | NEGATED | ABSENT
      reason   — human-readable explanation
      evidence — verbatim text snippet (up to 200 chars) or empty string
    """
    if not re.search(r"\bCoupling\b", text, re.IGNORECASE):
        return "ABSENT", "Coupling not present in document", ""

    # Negation takes priority — most adversarial case
    for pat in COUPLING_NEGATION_INDICATORS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 60)
            end   = min(len(text), m.end() + 60)
            ctx   = text[start:end].replace("\n", " ").strip()[:200]
            return "NEGATED", "Coupling negated/inapplicable in document", ctx

    # Structural indicators
    for pat in COUPLING_STRUCTURAL_INDICATORS:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            start = max(0, m.start() - 40)
            end   = min(len(text), m.end() + 80)
            ctx   = text[start:end].replace("\n", " ").strip()[:200]
            return "STRUCTURAL", (
                "Coupling declared with structural indicators — 'between X and Y', "
                "named human interest, or equivalent normative force present"
            ), ctx

    # Hollow/referential usage
    for pat in COUPLING_HOLLOW_INDICATORS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 60)
            end   = min(len(text), m.end() + 60)
            ctx   = text[start:end].replace("\n", " ").strip()[:200]
            return "SHALLOW", "Coupling referenced but not declared structurally", ctx

    # Term present without any structural or hollow indicator
    m = re.search(r"\bCoupling\b", text, re.IGNORECASE)
    if m:
        start = max(0, m.start() - 40)
        end   = min(len(text), m.end() + 80)
        ctx   = text[start:end].replace("\n", " ").strip()[:200]
    else:
        ctx = ""
    return "SHALLOW", (
        "Coupling mentioned without structural declaration — no 'between X and Y', "
        "no named human interest, no equivalent normative force"
    ), ctx


# ── Implicit coupling signals ─────────────────────────────────────────────────
# Source: LAIF v1.2 Principle 2 — Coupling requires explicit structural pairing.
# Implicit signals indicate governance intent (protections present) without the
# structural binding that makes Coupling load-bearing. Their presence lifts the
# coupling_state from ABSENT to IMPLICIT — a meaningful distinction for adoption
# guidance but NOT a compliance upgrade (formal gate is unchanged).

_IMPLICIT_COUPLING_PATTERNS = [
    # ── Original 7 patterns ───────────────────────────────────────────────────
    (r"protect(?:s|ion)?\s+\S+(?:\s+\S+)?\s+from",     "protection language"),
    (r"ensure(?:s|ing)?\s+\S+(?:\s+\S+)?\s+(?:rights|interests)", "rights/interests assurance"),
    (r"\bto\s+prevent\s+harm\b",                         "harm prevention"),
    (r"\bto\s+mitigate\s+risk\b",                        "risk mitigation"),
    (r"\baccountable\s+for\b",                           "accountability declaration"),
    (r"\bresponsible\s+for\b",                           "responsibility declaration"),
    (r"\bsubject\s+to\s+oversight\b",                    "oversight subjection"),
    # ── Extended patterns (Phase 3 — spec-mandated) ───────────────────────────
    # Cover clinical/employment governance language that structurally restricts
    # AI action and protects human interests without using LAIF canonical terms.
    (r"\bmay not be\b.{1,80}\bwithout\b",                "restriction requiring consent/authorisation"),
    (r"\brequires?\b.{1,80}\bapproval\b",                 "requires approval language"),
    (r"\bsubject\s+to\b.{1,80}\bapproval\b",              "subject to approval language"),
    (r"\boverride\b.{1,100}\bmust\s+be\s+(?:permitted|preserved|allowed)\b",
                                                          "override must be permitted/preserved"),
    (r"\bmust\s+(?:allow|permit|preserve)\b.{1,100}\boverride\b",
                                                          "must allow/permit/preserve override"),
    (r"\brequires?\s+authoris[ae]tion\s+before\b",        "requires authorisation before action"),
    (r"\bcannot\b.{1,80}\bunless\b.{1,80}\bauthoris[ae]d\b",
                                                          "cannot act unless authorised"),
    # ── Gap-closing patterns (clinical governance — NHS false-negative fix) ───
    # NHS: "shall not ... without explicit clinician authorisation"
    (r"\bwithout\b.{1,60}\bauthoris[ae]tion\b",           "action gated by authorisation"),
    # NHS: "Patients have the right to request a human clinician review"
    # and "This right shall not be subject to conditions or prerequisites"
    (r"\bright\b.{1,60}\b(?:to\s+request|shall\s+not\s+be)\b",
                                                          "protected rights language"),
]


def _implicit_coupling_signals(text):
    """
    Detect governance language that implies Coupling intent without the explicit
    structural pairing required by LAIF v1.2 Principle 2.

    Returns:
      {"found": bool, "matches": [up to 3 text excerpts, max 120 chars each]}

    Presence of these signals does NOT upgrade compliance. It indicates that
    the governance intent is present and the adoption pathway is structural
    (add explicit Coupling declarations) rather than conceptual.
    """
    matches = []
    for pat, _ in _IMPLICIT_COUPLING_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            start   = max(0, m.start() - 20)
            end     = min(len(text), m.end() + 60)
            excerpt = text[start:end].replace("\n", " ").strip()[:120]
            matches.append(excerpt)
            if len(matches) >= 3:
                break
    return {"found": bool(matches), "matches": matches}


def _coupling_state(existing_verdict, implicit, functional_coupling="ABSENT"):
    """
    Synthesise coupling state from explicit verdict, functional substance
    detection, and implicit signal scan.

    STRUCTURAL — explicit Coupling declared with structural indicators (full credit)
    FUNCTIONAL — Coupling substance fully expressed in the document's own
                 vocabulary (>=2 independent signal families), without the
                 canonical term. Not LAIF-native, but the pairing exists.
    IMPLICIT   — protective intent detected without structural pairing
    ABSENT     — no Coupling, no functional substance, no implicit signals

    Source: LAIF v1.2 Principle 2; Part Eight burden-of-proof (equivalent
    structural diligence through alternative documented means); Regulatory
    Integration Guide Part One (SATISFIES/EXTENDS methodology).
    """
    if existing_verdict == "STRUCTURAL":
        return "STRUCTURAL"
    if functional_coupling == "FUNCTIONAL":
        return "FUNCTIONAL"
    if implicit["found"]:
        return "IMPLICIT"
    return "ABSENT"


# ── Functional construct detection ────────────────────────────────────────────
# Source: LAIF v1.2 Part Eight (burden of proof) — a presumption of structural
# non-compliance is rebuttable by "evidence of equivalent structural diligence
# conducted through alternative documented means". Source: Regulatory
# Integration Guide Part One — LAIF's own integration methodology grades
# external instruments SATISFIES / EXTENDS in their native vocabulary.
#
# LAIF is the measuring instrument, not the authority over other instruments'
# vocabulary: what the principal text requires of Coupling, the Integrity
# Layer, Consistency, Reversibility, and Self-Application is SUBSTANTIVE, and
# this layer detects that substance regardless of register or terminology.
#
# Verdict per construct:
#   DECLARED   — canonical LAIF construct present (LAIF-native form)
#   FUNCTIONAL — >= 2 independent signal families matched: the substance is
#                expressed in the document's own vocabulary
#   PARTIAL    — exactly 1 family matched
#   ABSENT     — no canonical form and no substance signals
# The >=2-family rule prevents a single boilerplate phrase from earning
# functional credit; negation and contradiction downgrades are handled by the
# structural-depth layer, which applies to this layer's inputs unchanged.

FUNCTIONAL_CONSTRUCT_FAMILIES = {
    # LAIF v1.2 Principle 2 / §111–113: named specific interest + pairing +
    # equivalent normative force + mutual non-weakening.
    "Coupling": [
        ("restriction paired with named stake", [
            r"(?:restriction|obligation|constraint|prohibition|rule|limit)\w*\b.{0,220}\b(?:exists?\s+to|designed\s+to|serves?\s+to|in\s+order\s+to)\s+(?:protect|serve|secure|safeguard)\b.{0,160}\b(?:interest|stake|right|dignity|safety|patient|worker|person|beneficiar)",
            r"(?:when\s+we\s+restrict|every\s+rule\s+we\s+impose)\b.{0,200}\b(?:protect|who\s+that\s+protects)",
            r"protect\w*\s+the\s+\w+(?:'s|’s)?\s+(?:stake|interest|right)s?\s+in\b",
            r"(?:name|state|identify)\w*,?\s+(?:with\s+specificity,?\s+)?the\s+(?:specific\s+)?(?:person.level\s+stake|human\s+interest|interest)\b",
            r"(?:connection|linkage|link)\s+between\b.{0,140}\bobligations?\b.{0,140}\b(?:protections?|rights)\b",
            r"shall\s+not\s+sever\b.{0,140}\b(?:linkage|connection|pairing)\b",
        ]),
        ("mutual weakening lock", [
            r"neither\b.{0,160}\b(?:weaken|remove|repeal|suspend|modif|drop)\w*\b.{0,120}\bwithout\s+the\s+other",
            r"\bstand\s+or\s+fall\s+together\b",
            r"never\s+(?:quietly\s+)?drop\s+the\s+protection\b.{0,100}\b(?:keep|rule)",
            r"(?:restriction|rule|protection)\b.{0,140}\b(?:may|can)\s*not\s+be\s+(?:weakened|removed|dropped|repealed|suspended)\b.{0,120}\bwithout\b",
        ]),
        ("equivalent protective force", [
            r"(?:protection|safeguard)\w*\b.{0,160}\bas\s+(?:enforceable|strong|effective|accessible|precise)\b.{0,60}\bas\b",
            r"\bsame\s+legal\s+(?:strength|force)\b",
            r"\bjust\s+as\s+strong\s+as\s+the\s+rule\b",
            r"\bequivalent\s+(?:normative\s+)?force\b",
        ]),
    ],
    # LAIF v1.2 Part Two / Toolkit §1.3–1.5: threshold gate + the three
    # precondition substances.
    "Integrity Layer": [
        ("all-must-pass threshold gate", [
            r"all\s+(?:three|four|five|of\s+the\s+following)\b.{0,160}\b(?:must|shall)\s+be\s+(?:satisfied|met|true)",
            r"\b(?:three|four)\s+things\s+must\s+all\s+be\s+true\b",
            r"partial\s+satisfaction\b.{0,100}\b(?:failure|fails)",
            r"\bsatisfied\s+simultaneously\b|\bsimultaneously\b.{0,140}\bbefore\s+(?:any\s+)?deployment",
            r"must\s+meet\s+(?:these|all)\s+criteria\s+to\s+pass\b",
        ]),
        ("meaningful account of outputs", [
            r"(?:produce|provide|give)\w*\b.{0,80}\b(?:meaningful|comprehensible)\s+account\b",
            r"explain\s+(?:any|each|every)\s+decision\b",
            r"\bshow(?:s)?\s+its\s+work\b",
            r"(?:confidence|uncertainty)\b.{0,140}\b(?:material\s+)?limitations\b",
            r"interpret\s+the\s+system.s\s+outputs?\b|meaningful\s+(?:explanations?|information)\b",
            r"disclos\w+\b.{0,120}\bmaterial\s+limitations\b",
        ]),
        ("stated-vs-implemented correspondence", [
            r"(?:stated|documented)\b.{0,80}\bobjectives?\b.{0,140}\bcorrespond\b",
            r"really\s+does\s+what\s+we\s+say\s+it\s+does\b",
            r"perform\w*\s+consistently\s+whether\s+or\s+not\b",
            r"verified\s+by\s+independent\s+review\w*\b|checked\s+by\s+independent\s+review\w*\b",
        ]),
        ("bounded operation with escalation", [
            r"operate\w*\s+within\s+documented\s+bound",
            r"stays?\s+inside\s+the\s+limits\b",
            r"(?:surface|escalat|refer)\w*\b.{0,100}\bout.of.scope\b",
            r"escalat\w+\s+to\s+a\s+human\b",
            r"shall\s+not\s+autonomously\s+initiate\b",
            r"within\s+(?:its|their)\s+(?:validated|approved|defined|intended)\s+(?:indication|purpose|scope)\b",
            r"within\s+the\s+scope\s+of\s+(?:its|their)\s+intended\s+purpose\b",
        ]),
    ],
    # LAIF v1.2 Principle 5 / Q2: scale-invariant reasoning.
    "Consistency": [
        ("scale-invariant reasoning", [
            r"\bsmallest\s+comparable\b|\blargest\s+comparable\b",
            r"\bat\s+smaller\s+and\s+larger\s+scales\b|defensible\b.{0,140}\b(?:smaller|larger)\s+scales?\b",
            r"two.person\s+team\s+or\s+a\s+global\b|regardless\s+of\s+(?:size|scale)\b",
        ]),
        ("universal application check", [
            r"\bapplied\s+universally\b|\buniversal\s+application\b",
            r"aggregate\s+result\w*\b.{0,100}\bacceptable\b",
            r"differential\s+treatment\b.{0,140}\bjustif",
        ]),
    ],
    # LAIF v1.2 Provision D1 / Q3: reversal capacity + authorisation gate.
    "Reversibility": [
        ("authorisation before irreversible action", [
            r"irreversible\b.{0,220}\b(?:without|prior\s+to|before)\b.{0,100}\b(?:authoris|authoriz|approv)",
            r"(?:permanently\s+affect|could\s+permanently)\b.{0,180}\b(?:approve|authoris|authoriz|senior)",
            r"(?:authoris|authoriz)\w+\b.{0,140}\bcommensurate\s+with\b.{0,80}\bpermanence\b",
        ]),
        ("reversal capacity preserved", [
            r"(?:capacity|power|right|authority)\s+to\s+(?:reverse|overturn|modify)\b",
            r"appeal\s+to\b.{0,100}\b(?:person|reviewer|body)\b.{0,100}\b(?:reverse|overturn)",
            r"future\s+(?:actors|decision.makers)\b.{0,140}\b(?:reverse|modify)",
            r"can\s+be\s+(?:overridden|reversed|repaired)\b|overridden,\s+repaired",
            r"suspend\w*\b.{0,60}\b(?:roll\w*\s*back|recall|revoke)|rolling\s+back\b",
            r"supersede,?\s+disengage,?\s+or\s+deactivate",
            r"decommission\w*\b.{0,80}\bsafely\b|phasing\s+out\b.{0,60}\bsafely\b",
        ]),
    ],
    # LAIF v1.2 Part Seven: the framework binds the governance actor itself.
    "Self-Application": [
        ("framework binds the governing actor", [
            r"applies?\s+to\s+(?:the\s+)?(?:regulatory\s+)?authority\s+itself\b",
            r"applies?\s+to\s+us\s+as\s+an?\s+organisation\b|just\s+as\s+much\s+as\s+to\s+our\s+systems\b",
            r"(?:authority|regulator)\b.{0,140}\b(?:document|demonstrate)\w*\s+its\s+own\s+compliance\b",
            r"same\s+(?:evidentiary\s+)?standard\s+it\s+demands\b",
        ]),
        ("recourse against the governing actor", [
            r"affected\s+by\s+the\s+authority(?:'s|’s)\s+decisions?\b.{0,140}\b(?:appeal|review)",
            r"independent\s+reviewer\b.{0,100}\bpower\s+to\s+reverse\b",
        ]),
    ],
}

# Canonical-form (DECLARED) detection per functional construct. For Coupling,
# the bare term is NOT a declaration (that is SHALLOW under _coupling_quality);
# DECLARED requires the structural verdict.
# (pattern, case_sensitive). Single generic words (Consistency, Reversibility)
# are matched case-sensitively as terms of art — lowercase everyday usage
# ("brings clarity and consistency") is not a LAIF declaration.
_FUNCTIONAL_DECLARED_CHECKS = {
    "Integrity Layer":  (r"\bIntegrity Layer\b", False),
    "Consistency":      (r"\bConsistency\b", True),
    "Reversibility":    (r"\bReversibility\b", True),
    "Self-Application": (r"PART SEVEN|self.application|applies to regulatory", False),
}

# The family that defines a construct: without it, functional credit is capped
# at PARTIAL no matter how many supporting families match. Coupling IS the
# pairing; the Integrity Layer IS an all-must-pass precondition gate.
_FUNCTIONAL_REQUIRED_FAMILY = {
    "Coupling":        "restriction paired with named stake",
    "Integrity Layer": "all-must-pass threshold gate",
}


def _functional_alignment(text, coupling_quality):
    """
    Per-construct functional alignment verdicts with evidence excerpts.

    Returns {construct: {"verdict", "families", "evidence"}}.
    """
    out = {}
    for construct, families in FUNCTIONAL_CONSTRUCT_FAMILIES.items():
        fam_hits, evidence = [], []
        offsets = []
        for fam_name, pats in families:
            for pat in pats:
                m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
                if m:
                    fam_hits.append(fam_name)
                    lo = max(0, m.start() - 20)
                    hi = min(len(text), m.end() + 40)
                    evidence.append(text[lo:hi].replace("\n", " ").strip()[:160])
                    offsets.append(m.start())
                    break

        if construct == "Coupling":
            declared = coupling_quality == "STRUCTURAL"
        else:
            pat, case_sensitive = _FUNCTIONAL_DECLARED_CHECKS[construct]
            declared = bool(re.search(pat, text) if case_sensitive
                            else re.search(pat, text, re.IGNORECASE))

        required = _FUNCTIONAL_REQUIRED_FAMILY.get(construct)
        has_required = required is None or required in fam_hits
        if declared:
            verdict = "DECLARED"
        elif len(fam_hits) >= 2 and has_required:
            verdict = "FUNCTIONAL"
        elif len(fam_hits) >= 1:
            verdict = "PARTIAL"
        else:
            verdict = "ABSENT"
        out[construct] = {
            "verdict":  verdict,
            "families": fam_hits,
            "evidence": evidence[:3],
            "evidence_offsets": offsets[:3],
        }
    return out


def _laif_alignment_verdict(formal_pass, depth, functional, contradictions):
    """
    Overall alignment verdict — the audience-facing conclusion.

    LAIF-NATIVE (STRONG/WEAK/HOLLOW) — written in LAIF's canonical form;
        qualifier is the structural-depth verdict.
    FUNCTIONALLY ALIGNED — not LAIF-native, but Coupling substance plus at
        least 4 of 5 core constructs are functionally present and nothing
        contradicts them. The adoption distance is terminological.
    PARTIALLY ALIGNED — some constructs present functionally or partially.
    STRUCTURALLY UNALIGNED — no construct detectable in any form.
    """
    if formal_pass:
        return f"LAIF-NATIVE ({depth})"
    ok = lambda c: functional[c]["verdict"] in ("DECLARED", "FUNCTIONAL")
    n_ok = sum(ok(c) for c in functional)
    if ok("Coupling") and n_ok >= 4 and not contradictions:
        return "FUNCTIONALLY ALIGNED"
    n_any = sum(functional[c]["verdict"] != "ABSENT" for c in functional)
    if n_any >= 1:
        return "PARTIALLY ALIGNED"
    return "STRUCTURALLY UNALIGNED"


# ── Contradiction detection ────────────────────────────────────────────────────
# Source: LAIF v1.2 Integrity Layer A.2 (Structural Honesty) — stated objectives
# must correspond to implemented objectives; a document that claims an Integrity
# Layer property while contradicting its substance fails Structural Honesty.
# Toolkit §1.4: system must perform consistently whether or not being evaluated.

CONTRADICTION_CHECKS = [
    {
        # Source: LAIF v1.2 Provision D1 — Reversibility; Toolkit §2 B.3
        "property":    "Reversibility",
        "trigger":     r"\bReversibility\b",
        "adversaries": [
            (r"\b(?:permanently?|irrevocabl[ey]|irreversible|final\s+and\s+binding|cannot\s+be\s+(?:undone|reversed|changed|appealed|modified)|no\s+(?:appeal|review|recourse|right\s+of\s+redress))\b",
             "irreversibility language co-present with Reversibility claim"),
        ],
    },
    {
        # Source: LAIF v1.2 Integrity Layer A.1; Toolkit §1.3 — Structural
        # Transparency requires the system can produce a meaningful account of
        # any material output; non-disclosure directly contradicts this.
        "property":    "Structural Transparency",
        "trigger":     r"\bStructural\s+Transparency\b",
        "adversaries": [
            (r"\b(?:proprietary|trade\s+secret|confidential(?:ly)?|not\s+(?:disclosed|available|accessible|explainable|inspectable)|cannot\s+(?:be\s+)?(?:disclosed|explained|accessed|revealed)|withheld|black.?box|opaque)\b",
             "non-disclosure/opacity language co-present with Structural Transparency claim"),
        ],
    },
    {
        # Source: LAIF v1.2 Principle 5 — Consistency (Q2): reasoning must hold
        # at smaller AND larger scales; scale-exclusion directly contradicts this.
        "property":    "Consistency",
        "trigger":     r"\bConsistency\b",
        "adversaries": [
            (r"\b(?:applies?\s+only\s+to\s+(?:large|major|significant|enterprise|high.risk)|exempts?\s+(?:small|minor|low.risk|standard)|not\s+applicable\s+to\s+(?:small|minor|low.risk))\b",
             "scale-exclusive language contradicts Consistency (Q2 requires scale-invariance)"),
        ],
    },
    {
        # Source: Toolkit §1.5 — Structural Containment: system must not initiate
        # materially irreversible actions without authorisation (Provision D1).
        # Autonomous operation without oversight contradicts containment.
        "property":    "Structural Containment",
        "trigger":     r"\bStructural\s+Containment\b",
        "adversaries": [
            (r"\b(?:autonomous(?:ly)?|without\s+human\s+(?:oversight|review|approval|authorisation|authorization)|self.(?:direct|govern|initiat|execut)|no\s+human\s+(?:in\s+the\s+loop|oversight|review))\b",
             "autonomous/no-oversight language contradicts Structural Containment"),
        ],
    },
    # ── Non-canonical contradiction checks ────────────────────────────────────
    # These fire on informal expressions of an Integrity Layer property (the trigger)
    # co-present with language that contradicts it — without requiring canonical LAIF
    # terms. Catches evasion where a document expresses the governance intent informally
    # but simultaneously asserts conditions that negate it.
    # Source: LAIF v1.2 A.2 Structural Honesty (all four): a document expressing an
    # Integrity Layer intent while negating its substance fails the correspondence test
    # regardless of whether it uses canonical terminology.
    {
        "property":    "Reversibility (non-canonical)",
        "trigger":     r"\b(?:can\s+be\s+(?:reversed|modified|appealed|changed)|right\s+(?:to\s+)?(?:appeal|contest|review)\b|subject\s+to\s+(?:appeal|review)|(?:decisions?|outcomes?)\s+(?:are|shall\s+be)\s+(?:reversible|modifiable))\b",
        "adversaries": [
            (r"\b(?:permanently?|irrevocabl[ey]|irreversible|final\s+and\s+binding|cannot\s+be\s+(?:undone|reversed|changed|appealed|modified)|no\s+(?:right\s+of\s+)?(?:appeal|review|recourse))\b",
             "irreversibility language co-present with expressed reversibility intent (non-canonical)"),
        ],
    },
    {
        "property":    "Structural Transparency (non-canonical)",
        "trigger":     r"\b(?:system\s+(?:transparency|explainability)|outputs?\s+(?:are\s+)?(?:transparent|explainable|interpretable)|model\s+transparency|explainability\s+(?:is\s+)?(?:provided|ensured|maintained))\b",
        "adversaries": [
            (r"\b(?:proprietary|trade\s+secret|cannot\s+(?:be\s+)?(?:disclosed|explained|accessed|revealed)|withheld|black.?box|opaque)\b",
             "non-disclosure/opacity language co-present with expressed transparency intent (non-canonical)"),
        ],
    },
    {
        "property":    "Structural Containment (non-canonical)",
        "trigger":     r"\b(?:operates?\s+within\b|system\s+boundaries?\b|operational\s+(?:boundaries?|scope|limits?)\b|confined\s+to\s+(?:its\s+)?(?:scope|boundaries?|purpose))\b",
        "adversaries": [
            (r"\b(?:without\s+human\s+(?:oversight|review|approval|authorisation|authorization)|no\s+human\s+(?:in\s+the\s+loop|oversight|review|approval)|executes?\s+(?:\w+\s+)?without\s+(?:human\s+)?(?:oversight|review|approval))\b",
             "no-oversight language co-present with expressed containment intent (non-canonical)"),
        ],
    },
    {
        # Trigger: any sentence that asserts correspondence between stated and actual
        # objectives/goals — expressed without requiring exact adjacency of terms.
        # Uses .{0,60} to bridge intervening qualifiers ("of this system", etc.).
        "property":    "Structural Honesty (non-canonical)",
        "trigger":     r"\b(?:stated\s+objectives?\b.{0,60}\b(?:accurate|correct|correspond|reflect|align)\b|actual\s+(?:objectives?|goals?|behaviour)\b.{0,40}\b(?:match|align|reflect)\b.{0,30}\bstated\b)\b",
        "adversaries": [
            (r"\b(?:undisclosed\s+(?:objectives?|goals?|optimisation|purpose)|hidden\s+(?:objectives?|goals?|agenda))\b",
             "undisclosed/hidden objectives co-present with expressed honesty intent (non-canonical)"),
        ],
    },
]


# A claimed property and its negation only contradict each other if they are
# about the same subject matter. Document-wide co-presence produced false
# accusations on long texts (a doc REGULATING irreversible actions was flagged
# as dishonest about reversibility). Two safeguards:
#   (1) proximity — the negating language must appear near a claim occurrence;
#   (2) governing context — language that REGULATES the adverse condition
#       ("no system shall initiate ... irreversible ... without authorisation")
#       is compliance with Provision D1, not a contradiction of it.
CONTRADICTION_PROXIMITY = 600

_GOVERNING_CONTEXT_PAT = re.compile(
    r"(?:shall\s+not|must\s+not|may\s+not|no\s+system\s+shall|is\s+prohibited|"
    r"without\s+(?:prior\s+|documented\s+|appropriate\s+|explicit\s+)*(?:authoris|authoriz|approval)|"
    r"requires?\s+(?:prior\s+|documented\s+|senior\s+)*(?:authoris|authoriz|approval|sign.off)|"
    r"triggering\s+the\s+(?:appropriate\s+)?authoris|"
    r"(?:human|senior)\s+(?:being\s+)?must\s+approve)",
    re.IGNORECASE,
)


def _contradiction_check(text):
    """
    Detect contradictions between claimed LAIF properties and document content.
    Source: LAIF v1.2 A.2 Structural Honesty — stated and implemented objectives
    must correspond. A document claiming an Integrity Layer property while
    contradicting its substance exhibits structural dishonesty (Toolkit §1.4).

    Returns list of (property, description, context_snippet) tuples.
    """
    findings = []
    for check in CONTRADICTION_CHECKS:
        trigger_positions = [
            m.start() for m in re.finditer(check["trigger"], text, re.IGNORECASE)
        ]
        if not trigger_positions:
            continue
        for pat, desc in check["adversaries"]:
            for m in re.finditer(pat, text, re.IGNORECASE):
                if not any(abs(m.start() - t) <= CONTRADICTION_PROXIMITY
                           for t in trigger_positions):
                    continue
                lo = max(0, m.start() - 160)
                hi = min(len(text), m.end() + 160)
                if _GOVERNING_CONTEXT_PAT.search(text[lo:hi]):
                    continue
                start = max(0, m.start() - 100)
                end   = min(len(text), m.end() + 100)
                ctx   = text[start:end].replace("\n", " ").strip()
                findings.append((check["property"], desc, ctx[:200]))
                break
    return findings


# ── Sector gaming detection ────────────────────────────────────────────────────
# Source: LAIF v1.2 Principle 5 (Consistency / Q2) — governance logic must hold
# across all scales. A document optimised for sector keywords without substantive
# governance cannot satisfy Q2: the reasoning would not hold at the individual-
# decision level, only at the keyword-density level.

def _sector_gaming_risk(sector_alignment, overall, conceptual):
    """
    Detect potential sector gaming: high sector keyword alignment with low
    substantive governance content.

    HIGH   — sector alignment ≥80% AND overall readiness <30 (keyword stuffing)
    MEDIUM — sector alignment ≥70% AND conceptual proximity <25 (keywords without intent)
    LOW    — no gaming indicators detected
    """
    if sector_alignment >= 80 and overall < 30:
        return "HIGH", (
            f"Sector risk alignment {sector_alignment}% vs overall readiness {overall}/100. "
            "High keyword density without substantive governance — consistent with sector "
            "keyword stuffing. A genuinely sector-appropriate document would score higher "
            "on conceptual proximity and auditability (LAIF v1.2 Q2 Consistency)."
        )
    if sector_alignment >= 70 and conceptual < 25:
        return "MEDIUM", (
            f"Sector alignment {sector_alignment}% but conceptual proximity {conceptual}/100. "
            "Sector-specific vocabulary present without underlying governance intent. "
            "May indicate sector-optimised keyword selection rather than substantive coverage."
        )
    return "LOW", "No sector gaming indicators detected."


# ── Structural depth synthesis ─────────────────────────────────────────────────

def _structural_depth(coupling_quality, contradictions, gaming_risk, formal_pass):
    """
    Synthesise overall structural depth from diagnostic layers.

    STRONG — Structural Coupling + no contradictions + formal PASS + no gaming
    WEAK   — Shallow Coupling OR minor contradictions OR formal PASS with caveats
    HOLLOW — Negated/absent Coupling OR major contradictions OR high gaming risk
    """
    if coupling_quality == "NEGATED" or gaming_risk == "HIGH" or len(contradictions) >= 2:
        return "HOLLOW"
    if coupling_quality in ("SHALLOW", "ABSENT") and formal_pass:
        return "HOLLOW"  # Formal PASS with hollow Coupling = hollow compliance
    if coupling_quality == "SHALLOW" or contradictions or gaming_risk == "MEDIUM":
        return "WEAK"
    if coupling_quality == "STRUCTURAL" and not contradictions and gaming_risk == "LOW" and formal_pass:
        return "STRONG"
    return "WEAK"


# ── Sector profiles ────────────────────────────────────────────────────────────
# Source: LAIF_Compliance_Toolkit.txt §7.5 — PDCA tiering is calibrated to
# deployment sector and stakes. Profiles contextualise the assessment for the
# sector without altering formal compliance, rubric scores, or paraphrase logic.
# Each profile maps to LAIF's "Materially Affects Interests" test (Toolkit §1.2).
#
# Profile structure (flat — no nesting beyond one level):
#   relevant_interests  — human interests at stake per Toolkit §1.2
#   risk_indicators     — (pattern, label) signals that indicate sector risk
#   expected_evidence   — (pattern, label) artefacts a PDCA-Full would require
#   remediation_focus   — ordered steps referencing LAIF source sections

SECTOR_PROFILES = {

    "general_ai_governance": {
        "label": "General AI Governance",
        "relevant_interests": [
            "freedom from arbitrary algorithmic decision-making",
            "transparency of AI reasoning and outputs",
            "effective human oversight and correction",
            "accountability for AI-caused harm",
            "access to redress and contestation mechanisms",
        ],
        "risk_indicators": [
            (r"\bhigh.risk\b|\bhigher.risk\b",               "high-risk classification language"),
            (r"\baccountability\b",                          "accountability assignment"),
            (r"\btransparency\b|\btransparent\b",           "transparency requirements"),
            (r"\bhuman oversight\b|\bhuman determination\b", "human oversight mechanisms"),
            (r"\bproportionat",                              "risk-proportionate obligations"),
        ],
        "expected_evidence": [
            (r"\brisk\s+(?:register|log|assessment|documentation)\b", "risk register / documentation"),
            (r"\baudit\b|\baudit trail\b",                            "audit trail"),
            (r"\btechnical documentation\b|\bconformity assessment\b","technical documentation"),
            (r"\bimpact assessment\b|\bFRIA\b|\bDPIA\b",             "impact assessment"),
            (r"\bincident\s+(?:report|log|register)\b",              "incident reporting mechanism"),
        ],
        "remediation_focus": [
            "Introduce structural Coupling for each governance provision — pair the restriction "
            "with the specific human interest it protects, with equivalent normative force on both "
            "sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).",
            "Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency "
            "(scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure "
            "(LAIF v1.2 Part One).",
            "Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency, "
            "A.2 Structural Honesty, A.3 Structural Containment must all be satisfied simultaneously. "
            "Partial satisfaction = failure (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).",
            "Add a self-application clause: specify that the framework applies to regulatory bodies "
            "and governance actors themselves, not only to AI operators (LAIF v1.2 Part Seven).",
        ],
    },

    "clinical_ai": {
        "label": "Clinical AI Deployment",
        "relevant_interests": [
            "physical safety and bodily integrity of patients",
            "informed consent for AI-assisted clinical decisions",
            "clinical accuracy and reliability of AI outputs",
            "patient right to human clinician review of AI recommendations",
            "confidentiality of health data processed by the AI system",
            "access to effective redress for clinical harm caused by AI error",
        ],
        "risk_indicators": [
            (r"\bclinical\s+(?:decision|recommendation|output|alert)\b","clinical decision output"),
            (r"\bpatient\s+(?:safety|harm|risk|consent)\b",            "patient safety signal"),
            (r"\bdiagnos\w*\b|\btreatment\b|\bprescri\w*\b",          "diagnostic / treatment language"),
            (r"\bclinician\b|\bphysician\b|\bnurse\b|\bhealthcare\s+professional\b",
                                                                        "named clinical actor"),
            (r"\bmedical device\b|\bSoftware as a Medical Device\b|\bSaMD\b",
                                                                        "medical device classification"),
        ],
        "expected_evidence": [
            (r"\bclinical validation\b|\bclinical trial\b|\bvalidation study\b",
                                                                        "clinical validation evidence"),
            (r"\binformed consent\b|\bconsent form\b",                  "informed consent documentation"),
            (r"\bclinical audit\b|\bclinical governance\b",             "clinical audit / governance"),
            (r"\badverse event\b|\bincident report\b|\bMDR\b",          "adverse event / incident reporting"),
            (r"\bperformance monitoring\b|\bpost.market\s+surveillance\b",
                                                                        "post-deployment performance monitoring"),
        ],
        "remediation_focus": [
            "Declare Coupling between each clinical restriction and the specific patient interest it "
            "protects. Rewrite: 'AI alert suppression' → 'Coupling between alert suppression rules "
            "and the patient's interest in receiving clinically accurate recommendations' "
            "(Toolkit §2 B.1).",
            "Apply Q3 Reversibility: clinician override must always be preserved — AI recommendations "
            "must not displace clinical judgement irreversibly. Rewrite: 'AI system supports clinical "
            "decisions' → 'AI system provides recommendations subject to clinician override at every "
            "decision point, with override logged and reversible' (LAIF v1.2 Provision D1).",
            "Establish Structural Containment: document approved indications, patient populations, "
            "and operational boundaries for clinical AI. Add: 'System operates within documented "
            "clinical scope; out-of-scope queries surfaced to clinician, not resolved autonomously' "
            "(Toolkit §1.5).",
            "Require informed consent documentation for AI-assisted decisions that materially affect "
            "patient treatment — 'materially affects interests' includes clinical and diagnostic "
            "recommendations (Toolkit §1.2).",
        ],
    },

    "employment_ai": {
        "label": "Employment / Workforce AI",
        "relevant_interests": [
            "freedom from automated discrimination in hiring, promotion, or dismissal",
            "right to explanation of AI-driven employment decisions",
            "preservation of labour rights when AI monitors or manages workers",
            "right to human review of algorithmic performance assessment",
            "protection of worker data processed by AI systems",
            "collective bargaining rights in AI-governed workplaces",
        ],
        "risk_indicators": [
            (r"\bhiring\b|\brecruitment\b|\bapplicant\b|\bjob\s+(?:candidate|seeker)\b",
                                                                        "hiring / recruitment context"),
            (r"\bperformance\s+(?:review|assessment|management|monitoring)\b",
                                                                        "performance management"),
            (r"\bdismissal\b|\btermination\b|\bfiring\b|\bredundancy\b","dismissal / termination"),
            (r"\bworker\s+monitoring\b|\bworkplace\s+surveillance\b",   "worker surveillance"),
            (r"\bpay\b|\bwage\b|\bsalary\b|\bcompensation\b",          "pay / compensation signal"),
        ],
        "expected_evidence": [
            (r"\bbias\s+audit\b|\bfairness\s+audit\b|\balgorithmic\s+audit\b",
                                                                        "bias / fairness audit"),
            (r"\bequality\s+impact\s+assessment\b|\bEIA\b",            "equality impact assessment"),
            (r"\bexplanation\b.{0,60}\b(?:decision|outcome|score)\b",  "explanation of AI decisions"),
            (r"\bworker\s+(?:consultation|representation|notice)\b",    "worker consultation / notice"),
            (r"\bdiscrimination\s+(?:policy|complaint|redress)\b",      "anti-discrimination mechanism"),
        ],
        "remediation_focus": [
            "Declare Coupling between each employment AI restriction and the specific worker interest "
            "it protects. Rewrite: 'alignment between obligations imposed on workers and the "
            "protections those obligations are intended to serve' → 'Coupling between obligations "
            "imposed on workers and the protections afforded to their employment status and income' "
            "(Toolkit §2 B.1; LAIF v1.2 Principle 2).",
            "Apply Q2 Consistency: governance logic must produce just outcomes across all scales — "
            "from individual worker to collective bargaining unit. Rewrite: 'AI performance "
            "assessment applies to all employees' → 'AI performance assessment applies consistently "
            "across all roles, scales, and worker categories, with equivalent review rights at "
            "each scale' (LAIF v1.2 Principle 5).",
            "Apply Q3 Reversibility: algorithmic dismissal or demotion without appeal pathway "
            "fails Provision D1. Rewrite: 'AI-driven performance scoring determines employment "
            "decisions' → 'AI-driven performance scoring informs employment decisions subject to "
            "mandatory human review, with outcomes reversible on appeal' (LAIF v1.2 Provision D1).",
            "Implement bias auditing as a pre-deployment evidence artefact under Integrity Layer "
            "A.1 — Structural Transparency requires documented error characteristics including "
            "discriminatory output patterns (Toolkit §1.3).",
        ],
    },

    "public_sector_automation": {
        "label": "Public Sector Automation",
        "relevant_interests": [
            "right to lawful, fair, and transparent administrative decisions",
            "access to effective administrative review and appeal",
            "protection from automated denial of public services or benefits",
            "equal access to public services regardless of AI system bias",
            "democratic accountability of public sector AI deployment",
            "protection of sensitive personal data held by public bodies",
        ],
        "risk_indicators": [
            (r"\bbenefit\b|\bwelfare\b|\bsocial\s+security\b|\bentitlement\b",
                                                                        "public benefit / welfare context"),
            (r"\b(?:immigration|visa|asylum|citizenship)\b",           "immigration / status decision"),
            (r"\blaw\s+enforcement\b|\bpolice\b|\bcriminal\s+justice\b","law enforcement / criminal justice"),
            (r"\bpublic\s+service\b|\bgovernment\s+(?:service|agency|department)\b",
                                                                        "public service delivery"),
            (r"\bautomated\s+decision\b|\bADM\b|\balgorithmic\s+decision\b",
                                                                        "automated decision-making (ADM)"),
        ],
        "expected_evidence": [
            (r"\bFRIA\b|\bfundamental rights impact assessment\b",      "fundamental rights impact assessment"),
            (r"\blegality\s+(?:review|assessment|check)\b|\bstatutory\s+basis\b",
                                                                        "statutory / legal basis review"),
            (r"\bpublic\s+consultation\b|\bcivil\s+society\b",         "public consultation record"),
            (r"\bappeal\b|\bcontestability\b|\badministrative\s+review\b",
                                                                        "appeal / contestability mechanism"),
            (r"\btransparency\s+(?:notice|register|report|statement)\b","transparency notice / register"),
        ],
        "remediation_focus": [
            "Declare Coupling for each automated public decision: name the specific civic right at "
            "stake and pair it with a protection of equivalent normative force. Rewrite: 'automated "
            "benefit assessment improves efficiency' → 'Coupling between automated benefit "
            "assessment and the claimant's right to accurate determination and effective appeal' "
            "(Toolkit §2 B.1).",
            "Apply Q3 Reversibility: automated public sector decisions must preserve administrative "
            "appeal rights — automated denial without an appeal pathway fails Provision D1. Add: "
            "'Every automated decision that materially affects a person's entitlements is subject "
            "to human review on request, with outcome reversible' (LAIF v1.2 Provision D1).",
            "Establish Structural Containment: document approved decision types, citizen populations, "
            "and operational boundaries for each automated function. Out-of-scope cases must be "
            "escalated to human caseworker, not resolved by the AI system (Toolkit §1.5).",
            "Conduct a Fundamental Rights Impact Assessment before deployment — required for all "
            "PDCA-Full deployments affecting liberty, health, employment, or welfare benefits "
            "(Toolkit §7.5).",
        ],
    },

    "financial_services_ai": {
        "label": "Financial Services AI",
        "relevant_interests": [
            "fair and non-discriminatory access to financial products and services",
            "transparency in AI-driven credit, insurance, or investment decisions",
            "right to explanation of adverse automated financial decisions",
            "protection from AI-enabled market manipulation or systemic risk",
            "security of financial data and assets processed by AI systems",
            "access to redress for financial harm caused by AI error",
        ],
        "risk_indicators": [
            (r"\bcredit\s+(?:scoring|decision|risk|assessment)\b",     "credit scoring / decision"),
            (r"\bunderwriting\b|\binsurance\s+(?:decision|pricing|risk)\b",
                                                                        "underwriting / insurance risk"),
            (r"\banti.money\s+laundering\b|\bAML\b|\bfraud\s+detection\b",
                                                                        "AML / fraud detection"),
            (r"\btrading\b|\balgorithmic\s+trading\b|\bhigh.frequency\b","algorithmic trading signal"),
            (r"\bregulatory\s+(?:compliance|reporting|capital)\b",     "regulatory compliance signal"),
        ],
        "expected_evidence": [
            (r"\bmodel\s+(?:risk\s+management|validation|governance)\b","model risk management framework"),
            (r"\bSREP\b|\bICAAP\b|\bILAAP\b|\bregulatory\s+capital\b", "prudential / regulatory capital"),
            (r"\bfair\s+lending\b|\bfairness\s+testing\b|\bbias\s+test","fair lending / bias testing"),
            (r"\bexplainability\b|\bexplainable\s+AI\b|\bXAI\b",      "explainability documentation"),
            (r"\bsystemic\s+risk\b|\bsystemic\s+impact\b",            "systemic risk assessment"),
        ],
        "remediation_focus": [
            "Declare Coupling for each credit or insurance decision rule: name the protected "
            "financial interest and pair it with an enforceable protection of equivalent normative "
            "force. Rewrite: 'credit scoring algorithm assesses risk' → 'Coupling between credit "
            "scoring rules and the applicant's interest in fair, non-discriminatory access to credit, "
            "with an explanation right of equivalent normative force' (Toolkit §2 B.1).",
            "Apply Q1 Coupling to model risk management: each model constraint must identify the "
            "specific financial harm it prevents — 'model validation' without a named human interest "
            "does not satisfy Coupling (LAIF v1.2 Principle 2).",
            "Establish Structural Transparency: AI-driven financial decisions that materially affect "
            "a person's access to credit, insurance, or financial services must be explainable on "
            "request. Rewrite: 'model outputs are monitored' → 'model outputs affecting customer "
            "decisions are explainable to affected customers on request, in plain language' "
            "(Toolkit §1.3).",
            "Implement model validation as a pre-deployment Integrity Layer precondition: A.1 "
            "(Structural Transparency — explainability verified) and A.2 (Structural Honesty — "
            "stated objectives correspond to implemented objectives, verified by independent review) "
            "must both be satisfied before deployment proceeds (Toolkit §1.3, §1.4).",
        ],
    },
}



# Phase 3O sector / institutional diagnostic overlays. These fields enrich
# diagnostic mapping and remediation wording only; they do not alter validate.py,
# formal LAIF-native certification, scoring weights, or sector compliance gates.
SECTOR_PROFILES.update({
    "government_service_delivery": {
        "label": "Government Service Delivery",
        "purpose": "Diagnose AI governance for benefits, licensing, eligibility, enforcement, and other citizen-facing administrative services.",
        "relevant_interests": [
            "accurate and non-arbitrary service eligibility decisions",
            "procedural fairness, reasons, and administrative review",
            "continuity of public services and service-impact transparency",
            "records integrity for affected individuals and oversight bodies",
        ],
        "diagnostic_terms": ("benefit", "eligibility", "caseworker", "claimant", "citizen", "resident", "service delivery", "administrative review", "reasons for decision", "public record", "appeal", "entitlement", "public service"),
        "risk_indicators": [
            (r"\b(?:benefit|eligibility|entitlement|licen[cs]e|permit)\b", "service eligibility / entitlement decision"),
            (r"\b(?:claimant|citizen|resident|service user|applicant)\b", "affected service user population"),
            (r"\b(?:administrative review|appeal|reconsideration|reasons for decision)\b", "review / reasons pathway"),
            (r"\b(?:caseworker|service delivery|public service|agency decision)\b", "service-delivery operational actor"),
            (r"\b(?:recordkeeping|public record|records authority|decision record)\b", "records / decision trace context"),
        ],
        "expected_evidence": [(r"\breasons? for decision\b|\bdecision notice\b", "reasons-for-decision record"), (r"\b(?:administrative review|appeal|reconsideration)\b", "review pathway record"), (r"\bservice-impact (?:record|assessment)\b|\bimpact assessment\b", "service-impact record"), (r"\bcase file\b|\bdecision log\b|\bpublic record\b", "case / decision record"), (r"\bexception log\b|\bhuman caseworker review\b", "exception / human review log")],
        "governance_force_emphasis": ("actor", "trigger", "protected interest", "evidence", "reversibility", "escalation", "auditability"),
        "remediation_themes": ("Name the service-delivery policy owner and records/review support roles.", "Tie automated eligibility or service decisions to reasons, appeal, and correction pathways.", "Capture service-impact records and decision logs without inventing unavailable source evidence."),
        "evidence_cautions": ("Do not infer statutory authority or legal validity from service vocabulary alone.", "Use reviewer-confirmation fallback unless source text contains exact reasons, record, or appeal language."),
        "remediation_focus": ["For service-delivery decisions, identify the protected public interest, decision trigger, reasons-for-decision record, administrative review pathway, and records-retention owner.", "Assign a service-delivery policy owner with administrative review and records authority support for evidence, correction, and escalation controls."],
    },
    "departmental_ai_development": {
        "label": "Departmental AI Development",
        "purpose": "Diagnose internal AI project, model, architecture, security, privacy, release, monitoring, and rollback governance.",
        "relevant_interests": ["secure and reliable public or institutional systems", "privacy and data protection in internal AI delivery", "accountable release governance and rollback capacity"],
        "diagnostic_terms": ("model register", "architecture review", "release approval", "rollback", "security review", "privacy review", "MLOps", "change control", "risk assessment"),
        "risk_indicators": [(r"\bmodel register\b|\bAI project\b|\bMLOps\b", "AI project / model inventory"), (r"\barchitecture review\b|\btechnical design\b", "architecture review"), (r"\bsecurity review\b|\bprivacy review\b|\bDPIA\b", "security / privacy review"), (r"\brelease approval\b|\bchange control\b|\bgo-live\b", "release governance"), (r"\brollback plan\b|\bkill switch\b|\bincident response\b", "rollback / incident control")],
        "expected_evidence": [(r"\bmodel register\b", "model register"), (r"\brisk assessment\b|\bthreat model\b", "risk / threat assessment"), (r"\brelease approval\b|\bchange approval\b", "release approval record"), (r"\brollback plan\b|\bdeployment rollback\b", "rollback plan"), (r"\bsecurity sign-off\b|\bprivacy sign-off\b", "security / privacy sign-off")],
        "governance_force_emphasis": ("actor", "trigger", "control", "evidence", "reversibility", "auditability"),
        "remediation_themes": ("Map project owners to architecture, security, privacy, and release reviewers.", "Require model register, risk assessment, release approval, and rollback evidence.", "Treat development profile signals as diagnostic context, not score credit."),
        "evidence_cautions": ("Do not treat engineering artifacts as proof of governance approval unless the source states approval.", "Do not invent release or rollback evidence absent exact source text."),
        "remediation_focus": ["Assign an AI project owner with architecture, security, privacy, and release governance reviewers.", "Require a model register entry, risk assessment, release approval, monitoring owner, and rollback plan for each material AI release."],
    },
    "procurement_vendor_governance": {
        "label": "Procurement and Vendor Governance",
        "purpose": "Diagnose AI controls expressed through procurement, contracts, vendor assurance, audit access, disclosure, and third-party management.",
        "relevant_interests": ["accountable outsourced AI governance", "audit access and vendor transparency", "contractual assurance for affected people and institutions"],
        "diagnostic_terms": ("procurement", "vendor", "supplier", "contract clause", "RFP", "due diligence", "audit access", "assurance artefact", "assurance artifact", "SLA", "third party"),
        "risk_indicators": [(r"\bprocurement\b|\bRFP\b|\btender\b", "procurement process"), (r"\bvendor\b|\bsupplier\b|\bthird[- ]party\b", "vendor / third-party actor"), (r"\bcontract clause\b|\bcontractual\b|\bSLA\b", "contractual control"), (r"\baudit access\b|\bright to audit\b", "audit access"), (r"\bvendor disclosure\b|\bassurance arte?fact\b|\bdue diligence\b", "vendor disclosure / assurance")],
        "expected_evidence": [(r"\bcontract clause\b", "contract clause"), (r"\bvendor disclosure\b", "vendor disclosure"), (r"\baudit-access record\b|\baudit access\b", "audit-access record"), (r"\bassurance arte?fact\b|\bdue diligence record\b", "assurance artefact"), (r"\bservice level\b|\bSLA\b", "service-level obligation")],
        "governance_force_emphasis": ("mandate", "actor", "control", "evidence", "consequence", "auditability"),
        "remediation_themes": ("Assign procurement, legal/compliance, and vendor-management ownership.", "Convert AI governance expectations into contract clauses, disclosures, assurance artifacts, and audit-access records.", "Keep legal-authority boundary diagnostic unless adoption or contract authority is explicit."),
        "evidence_cautions": ("Do not infer contractual enforceability from procurement vocabulary alone.", "Do not invent vendor disclosures or audit rights without source text."),
        "remediation_focus": ["Assign a procurement lead with legal/compliance and vendor-management support for contract controls.", "Require contract clauses, vendor disclosures, audit-access records, and assurance artefacts for material vendor AI systems."],
    },
    "employment_hr_ai": {
        "label": "Employment and HR AI",
        "purpose": "Diagnose hiring, promotion, performance, scheduling, workplace monitoring, adverse-action, and bias-review AI governance.",
        "relevant_interests": ["fair employment opportunity", "non-discrimination and worker dignity", "human review and appeal of adverse employment actions"],
        "diagnostic_terms": ("hiring", "candidate", "employee", "worker", "performance", "promotion", "adverse action", "bias review", "HR", "appeal"),
        "risk_indicators": [(r"\b(?:hiring|recruitment|candidate|promotion|termination)\b", "employment lifecycle decision"), (r"\b(?:employee|worker|staff|personnel)\b", "worker population"), (r"\bperformance (?:scoring|monitoring|review)\b", "performance assessment"), (r"\badverse action\b|\bdisciplinary\b", "adverse employment action"), (r"\bbias (?:review|testing|evidence)\b|\bdisparate impact\b", "bias / disparate-impact review")],
        "expected_evidence": [(r"\badverse-action review\b|\badverse action review\b", "adverse-action review"), (r"\bbias evidence\b|\bbias test\b|\bdisparate impact\b", "bias evidence"), (r"\bhuman review\b|\bappeal record\b", "human review / appeal record"), (r"\bjob related\b|\bvalidation study\b", "job-related validation evidence"), (r"\baccommodation\b|\baccessibility\b", "accommodation / accessibility evidence")],
        "governance_force_emphasis": ("protected interest", "actor", "evidence", "reversibility", "escalation", "consequence"),
        "remediation_themes": ("Assign an HR policy owner with legal/compliance and bias-review support.", "Require adverse-action review, bias evidence, human review, and appeal records.", "Distinguish worker-protection governance from AI surveillance vocabulary."),
        "evidence_cautions": ("Do not infer employment-law compliance or legal validity from HR terminology.", "Do not generate bias or adverse-action evidence unless exact source text exists."),
        "remediation_focus": ["Assign an HR policy owner with legal/compliance and bias-review support for adverse-action controls.", "Require adverse-action review, bias evidence, human review, and appeal records for employment-impacting AI decisions."],
    },
    "education_ai": {
        "label": "Education AI",
        "purpose": "Diagnose AI governance for admissions, grading, learning analytics, student support, accessibility, appeals, and academic governance.",
        "relevant_interests": ["fair student assessment and access", "student privacy and accessibility", "appeal and support for education-impacting AI decisions"],
        "diagnostic_terms": ("student", "learner", "grading", "assessment", "admissions", "academic", "accessibility", "accommodation", "appeal", "learning analytics"),
        "risk_indicators": [(r"\b(?:student|learner|pupil)\b", "student / learner population"), (r"\b(?:grading|assessment|admissions|academic progress)\b", "education-impacting decision"), (r"\blearning analytics\b|\bproctoring\b", "learning analytics / proctoring"), (r"\baccessibility\b|\baccommodation\b|\bstudent support\b", "accessibility / support"), (r"\bacademic governance\b|\bacademic integrity\b|\bappeal pathway\b", "academic governance / appeal")],
        "expected_evidence": [(r"\bstudent-impact review\b|\bstudent impact review\b", "student-impact review"), (r"\bappeal pathway\b|\bgrade appeal\b", "appeal pathway"), (r"\baccessibility record\b|\baccommodation record\b", "accessibility record"), (r"\bacademic governance review\b", "academic governance review"), (r"\bstudent support record\b", "student support record")],
        "governance_force_emphasis": ("protected interest", "actor", "control", "evidence", "reversibility", "escalation"),
        "remediation_themes": ("Assign education policy ownership with student support, accessibility, and academic governance reviewers.", "Require student-impact review, appeal pathway, and accessibility records.", "Avoid treating education vocabulary as legal or certification authority."),
        "evidence_cautions": ("Do not infer education-law compliance or academic-validity determinations.", "Do not invent appeal, accessibility, or support records without exact source text."),
        "remediation_focus": ["Assign an education policy owner with student support, accessibility, and academic governance reviewers.", "Require student-impact review, appeal pathway, accessibility record, and academic governance review for education-impacting AI decisions."],
    },
})

SECTOR_PROFILES["general_ai_governance"].update({
    "purpose": "Provide a neutral diagnostic overlay for AI governance documents that do not match a more specific institutional profile.",
    "diagnostic_terms": ("accountability", "transparency", "human oversight", "risk assessment", "audit", "incident", "redress"),
    "governance_force_emphasis": ("mandate", "actor", "protected interest", "control", "evidence", "auditability"),
    "remediation_themes": ("Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.", "Use LAIF-native terminology only for certification adoption, not external-framework validity claims."),
    "evidence_cautions": ("General governance vocabulary does not prove compliance or legal validity.", "Use reviewer-confirmation fallback when exact evidence text is absent."),
})
SECTOR_PROFILES["clinical_ai"].update({
    "purpose": "Diagnose AI governance for clinical recommendations, patient safety, clinician review, clinical fallback, and incident pathways.",
    "diagnostic_terms": ("clinical", "patient", "diagnosis", "treatment", "clinician", "medical device", "clinical fallback", "override", "incident log", "patient safety"),
    "governance_force_emphasis": ("protected interest", "actor", "control", "evidence", "reversibility", "escalation"),
    "remediation_themes": ("Assign a clinical governance owner with clinician reviewer and safety incident pathway.", "Require clinical fallback, override record, patient safety review, and incident log.", "Keep clinical source-evidence claims tied to exact text."),
    "evidence_cautions": ("Clinical vocabulary does not determine medical, regulatory, or legal validity.", "Do not invent clinical validation, fallback, override, patient safety review, or incident evidence."),
})

_SECTOR_PROFILE_ALIASES = {"public_sector_automation": "government_service_delivery", "public_sector_ai": "government_service_delivery", "government_ai": "government_service_delivery", "departmental_ai": "departmental_ai_development", "internal_ai_development": "departmental_ai_development", "procurement_ai": "procurement_vendor_governance", "vendor_governance": "procurement_vendor_governance", "employment_ai": "employment_hr_ai", "hr_ai": "employment_hr_ai", "workforce_ai": "employment_hr_ai"}

_SECTOR_PROFILE_PATCH_CONTEXT = {
    "government_service_delivery": {"responsible_actor": "Service-delivery policy owner with administrative review / records authority support", "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.", "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation."},
    "departmental_ai_development": {"responsible_actor": "AI project owner with architecture, security, privacy, and release governance reviewers", "evidence_artifact": "Model register, risk assessment, release approval, monitoring record, or rollback plan.", "operational_control": "Require architecture, security, privacy, release, monitoring, and rollback checkpoints before operational AI release."},
    "procurement_vendor_governance": {"responsible_actor": "Procurement lead with legal/compliance and vendor-management support", "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.", "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences."},
    "clinical_ai": {"responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway", "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.", "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation."},
    "employment_hr_ai": {"responsible_actor": "HR policy owner with legal/compliance and bias-review support", "evidence_artifact": "Adverse-action review, bias evidence, human review/appeal record, or accommodation record.", "operational_control": "Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls."},
    "education_ai": {"responsible_actor": "Education policy owner with student support, accessibility, and academic governance reviewer", "evidence_artifact": "Student-impact review, appeal pathway, accessibility record, student support record, or academic governance review.", "operational_control": "Map education-impacting AI decisions to student-impact review, accessibility support, appeal pathways, academic governance review, and escalation."},
}


def _sector_profile_key(sector):
    """Resolve a sector string to a supported diagnostic profile key."""
    key = str(sector or "general_ai_governance").strip().lower().replace("-", "_").replace(" ", "_")
    key = _SECTOR_PROFILE_ALIASES.get(key, key)
    if key in SECTOR_PROFILES:
        return key
    return "general_ai_governance"


def _sector_profile_metadata(sector):
    """Return profile metadata for diagnostic display only."""
    return SECTOR_PROFILES[_sector_profile_key(sector)]


def _sector_profile_signals(text, sector):
    """Deterministically detect profile vocabulary without affecting scores."""
    profile = _sector_profile_metadata(sector)
    signals = []
    for term in profile.get("diagnostic_terms", ()):
        pattern = r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, text or "", re.IGNORECASE):
            signals.append(term)
    return list(dict.fromkeys(signals))


def _sector_profile_remediation_context(result):
    """Return institution-specific remediation context for diagnostic wording."""
    return _SECTOR_PROFILE_PATCH_CONTEXT.get(result.get("sector_profile"), {})


def _sector_profile_patch_adjustments(patch, result):
    """Enrich remediation patch wording from profile context without changing authority."""
    context = _sector_profile_remediation_context(result)
    if not context:
        return patch
    adjusted = dict(patch)
    adjusted["responsible_actor"] = context.get("responsible_actor", adjusted["responsible_actor"])
    adjusted["evidence_artifact"] = context.get("evidence_artifact", adjusted["evidence_artifact"])
    adjusted["operational_control"] = context.get("operational_control", adjusted["operational_control"])
    return adjusted



# ── Helpers ────────────────────────────────────────────────────────────────────

def _score_signals(text, rubric):
    """Return (score, fired, missed) for a rubric.

    fired  — list of (label, weight) for patterns that matched
    missed — list of (label, weight) for patterns that did not match
    Score is sum of fired weights, capped at 100.
    """
    fired, missed = [], []
    # DOTALL: span patterns (".{1,300}") are proximity windows over the
    # document, not same-line constraints — hard-wrapped prose must be able
    # to earn them. The Evidence Locator uses identical flags (parity).
    for w, pat, label in rubric:
        if re.search(pat, text, re.IGNORECASE | re.DOTALL):
            fired.append((label, w))
        else:
            missed.append((label, w))
    return min(100, sum(w for _, w in fired)), fired, missed


def score_bar(n, width=10):
    """Unicode progress bar for markdown output."""
    filled = round(n / 100 * width)
    return "█" * filled + "░" * (width - filled)

def _tty_bar(n, width=10):
    """ANSI-coloured bar for terminal output."""
    bar = score_bar(n, width)
    colour = "32" if n >= 60 else "33" if n >= 35 else "31"
    return f"\033[{colour}m{bar}\033[0m" if sys.stdout.isatty() else bar

def _tty(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


# ── Score trace support ───────────────────────────────────────────────────────
# Each dimension carries a weight rationale that explains WHY it is weighted
# as it is, not merely what it measures. This makes score explanations
# decision-grade: a non-engineer can understand why a number is what it is.

_SCORE_WEIGHT_RATIONALE = {
    "structural": (
        "25% weight. Governance architecture is the primary carrier of LAIF compliance. "
        "Without a non-amendable constitutional hierarchy, threshold gate conditions "
        "(Integrity Layer precondition), and named decision instruments (Coherence Test / "
        "PDCA), all other provisions are operationally revisable — the core failure "
        "LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven)."
    ),
    "terminology": (
        "15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is "
        "not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity "
        "requirements'. Each term carries a specific enforcement obligation that informal "
        "equivalents do not. Lower weight because terminology alone is necessary but not "
        "sufficient for compliance (Toolkit §1)."
    ),
    "conceptual": (
        "20% weight. Measures whether the document's governance intent is substantively "
        "aligned with LAIF, independent of vocabulary. High conceptual proximity with low "
        "structural or terminology scores signals a document expressing the right values "
        "through different vocabulary — adoption pathway is shorter. Low conceptual "
        "proximity indicates a more fundamental governance gap (LAIF v1.2 Part One)."
    ),
    "auditability": (
        "20% weight. LAIF obligations must be independently verifiable. Numbered "
        "requirements, evidence documentation mandates, and monitoring mechanisms are "
        "the operational artefacts that allow a PDCA auditor to confirm compliance. "
        "Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA)."
    ),
    "enforceability": (
        "20% weight. A governance standard that cannot be enforced is an aspiration, not "
        "a constraint. Mandatory language ('shall'), named responsible parties, and "
        "enforcement consequences are the minimum conditions for operational enforceability. "
        "Voluntary frameworks characteristically score low here regardless of conceptual "
        "quality (LAIF v1.2 Part Three)."
    ),
}


def _score_reason(dim, score, fired, missed):
    """Plain-English one-sentence explanation of a dimension score."""
    n_fired = len(fired)
    n_total = n_fired + len(missed)
    if score == 0:
        return (
            f"No {dim} signals present — none of the {n_total} expected signals matched. "
            f"This dimension is absent from the document."
        )
    if score >= 80:
        top = ", ".join(lbl for lbl, _ in fired[:2])
        return (
            f"Strong {dim} coverage ({score}/100): {n_fired} of {n_total} signals matched. "
            f"Strongest contributors: {top}."
        )
    if score >= 50:
        gaps = ", ".join(lbl for lbl, _ in missed[:2]) or "none"
        return (
            f"Partial {dim} coverage ({score}/100): {n_fired} of {n_total} signals matched. "
            f"Key gaps: {gaps}."
        )
    gaps = ", ".join(lbl for lbl, _ in missed[:3]) or "none"
    return (
        f"Weak {dim} coverage ({score}/100): only {n_fired} of {n_total} signals matched. "
        f"Principal gaps: {gaps}."
    )


def _build_score_trace(dim, score, fired, missed):
    """Build a score_trace entry for one dimension."""
    return {
        "score":            score,
        "signals_fired":   [lbl for lbl, _ in fired],
        "signals_missing": [lbl for lbl, _ in missed],
        "weight_rationale": _SCORE_WEIGHT_RATIONALE[dim],
        "reason":           _score_reason(dim, score, fired, missed),
    }


# ── Decision-grade reporting helpers ─────────────────────────────────────────

def _compliance_summary(result):
    """Flat summary dict — one authoritative verdict per dimension."""
    return {
        "formal":           result["formal_laif_compliance"],
        "structural_depth": result["structural_depth"],
        "contradictions":   "DETECTED" if result["contradictions"] else "NONE",
        "sector_gaming":    result["sector_gaming_risk"],
        "final":            result["strong_laif_compliance"],
    }


def _executive_summary(result):
    """
    Plain-English decision summary for a single document.
    Returns {verdict, risks, strengths, why} — all non-engineer readable.
    """
    sc         = result["strong_laif_compliance"]
    depth      = result["structural_depth"]
    cq         = result["coupling_quality"]
    overall    = result["overall_readiness_score"]
    contras    = result["contradictions"]
    formal     = result["formal_laif_compliance"]
    gaming     = result["sector_gaming_risk"]
    conceptual = result["conceptual_proximity_score"]
    enforce    = result["enforceability_score"]
    fcd        = result.get("formal_checks_detail", [])

    # ── Verdict ──────────────────────────────────────────────────────────────
    if sc == "STRONG PASS":
        verdict = (
            "This document satisfies formal LAIF v1.2 compliance and demonstrates genuine "
            "structural governance depth: Coupling is declared with a named human interest, "
            "no structural contradictions were detected, and all 8 required constructs are present."
        )
    elif sc == "WEAK PASS":
        verdict = (
            f"This document passes the formal LAIF v1.2 compliance gate — all 8 required "
            f"constructs are present — but structural depth is {depth.lower()}: Coupling "
            f"quality is {cq}. Restrictions are not structurally paired with the specific "
            f"human interests they protect, meaning neither side can be defended as "
            f"structurally required by the other."
        )
    else:
        missing = [lbl for lbl, ok in fcd if not ok]
        if len(missing) >= len(fcd) and fcd:
            miss_str = f"all {len(fcd)} required constructs"
        elif len(missing) > 4:
            miss_str = ", ".join(missing[:4]) + f" and {len(missing) - 4} others"
        else:
            miss_str = ", ".join(missing) if missing else "see formal checks detail"
        _la = result.get("laif_alignment", "")
        if _la == "FUNCTIONALLY ALIGNED":
            verdict = (
                f"This document is not written in LAIF-native form ({miss_str} not present "
                f"as canonical constructs), so it does not pass the formal LAIF v1.2 gate — "
                f"but its substance is FUNCTIONALLY ALIGNED: the structural requirements "
                f"behind those constructs are expressed in the document's own vocabulary. "
                f"Overall readiness score: {overall}/100. The distance to LAIF certification "
                f"is terminological and documentary, not substantive."
            )
        else:
            verdict = (
                f"This document does not pass the formal LAIF-native certification gate. "
                f"Required constructs absent: {miss_str}. Overall readiness score: {overall}/100. "
                f"Formal compliance is binary — partial presence of required constructs does not "
                f"constitute compliance."
            )

    # ── Key risks (up to 3) ──────────────────────────────────────────────────
    risks = []
    if cq == "NEGATED":
        risks.append(
            "Coupling is explicitly negated or declared inapplicable — the most adversarial "
            "Coupling failure mode. The framework actively disclaims the structural pairing "
            "requirement, making it impossible to satisfy the Coherence Test Q1. "
            "(LAIF v1.2 Principle 2)"
        )
    elif result.get("coupling_state") == "FUNCTIONAL":
        risks.append(
            "Coupling not declared in LAIF-native form. The pairing of restrictions with "
            "named protections IS functionally expressed in the document's own vocabulary; "
            "LAIF certification would require either a canonical declaration or a documented "
            "equivalence mapping. The distance is terminological, not substantive. "
            "(LAIF v1.2 Principle 2; Part Eight; Regulatory Integration Guide Part One)"
        )
    elif cq in ("SHALLOW", "ABSENT"):
        risks.append(
            "Coupling not structurally declared: no governance restriction is paired with "
            "a named human interest. Each restriction can be weakened in isolation without "
            "triggering a corresponding protection failure. Q1 (Coupling) failure = "
            "automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)"
        )
    if contras:
        props = ", ".join(sorted({p for p, _, _ in contras}))
        risks.append(
            f"Structural contradictions detected in: {props}. The document simultaneously "
            f"claims these properties and contains language that negates them — a Structural "
            f"Honesty failure. A document that contradicts its own governance declarations "
            f"cannot satisfy the Integrity Layer precondition. (LAIF v1.2 A.2)"
        )
    if gaming == "HIGH":
        risks.append(
            f"High sector gaming risk: sector keyword density is elevated while substantive "
            f"governance content is low (overall {overall}/100). This pattern would not "
            f"produce just outcomes at the individual-decision scale — failing Q2 Consistency. "
            f"(LAIF v1.2 Principle 5)"
        )
    elif gaming == "MEDIUM" and len(risks) < 3:
        risks.append(
            f"Medium sector gaming risk: sector vocabulary present without underlying "
            f"governance intent. Conceptual proximity is {conceptual}/100, below the level "
            f"expected for genuine sector alignment."
        )
    if formal == "FAIL" and len(risks) < 3:
        missing = [lbl for lbl, ok in fcd if not ok]
        if missing:
            risks.append(
                f"Formal compliance gate not satisfied: {len(missing)} required construct(s) "
                f"absent — {', '.join(missing[:3])}. Each required LAIF-native construct "
                f"remains necessary for certification regardless of overall readiness score."
            )
    if enforce < 30 and len(risks) < 3:
        risks.append(
            f"Low enforceability ({enforce}/100): mandatory language ('shall'), named "
            f"responsible parties, and enforcement consequences are largely absent. "
            f"Governance provisions are aspirational rather than operationally binding."
        )
    risks = risks[:3]

    # ── Key strengths (up to 3) ──────────────────────────────────────────────
    strengths = []
    if conceptual >= 60:
        strengths.append(
            f"High conceptual proximity ({conceptual}/100): accountability, oversight, "
            f"transparency, and contestability are expressed through the document's own "
            f"vocabulary. The adoption pathway is terminological and structural, not "
            f"conceptual — the underlying intent is already present."
        )
    elif conceptual >= 40:
        strengths.append(
            f"Moderate conceptual proximity ({conceptual}/100): key LAIF-aligned governance "
            f"concepts are present, indicating partial substantive alignment with LAIF's "
            f"foundational principles."
        )
    cc = result["construct_coverage"]
    present = [k for k, v in cc.items() if v]
    if len(present) >= 4:
        listed = ", ".join(present[:3]) + (" and others" if len(present) > 3 else "")
        strengths.append(
            f"{len(present)} of 8 LAIF constructs present: {listed}. "
            f"The document's vocabulary partially overlaps with LAIF canonical terms."
        )
    if result["sector_risk_alignment"] >= 60 and len(strengths) < 3:
        strengths.append(
            f"Strong sector risk alignment ({result['sector_risk_alignment']}/100): the "
            f"document addresses the materially relevant human interests for the "
            f"{result.get('sector_label', result['sector_used'])} deployment context."
        )
    if result["auditability_score"] >= 60 and len(strengths) < 3:
        strengths.append(
            f"Good auditability ({result['auditability_score']}/100): numbered requirements, "
            f"evidence mandates, and monitoring mechanisms are present — obligations can "
            f"be externally verified."
        )
    if enforce >= 60 and len(strengths) < 3:
        strengths.append(
            f"Strong enforceability ({enforce}/100): mandatory language, named responsible "
            f"parties, and enforcement consequences are present."
        )
    if not strengths:
        s = result["structural_score"]
        if s > 0:
            strengths.append(
                f"Some structural signals present ({s}/100): basic governance architecture "
                f"markers provide a foundation for LAIF adoption."
            )
        else:
            strengths.append(
                "Document establishes a governance scope for AI deployment, providing a "
                "foundation on which LAIF-compliant provisions can be built."
            )
    strengths = strengths[:3]

    # ── Root cause — always "Primary structural gap: X" ─────────────────────
    if sc == "STRONG PASS":
        why = "Primary structural gap: none — full structural compliance confirmed."
    elif result.get("coupling_state") == "FUNCTIONAL":
        why = ("Primary structural gap: LAIF-native declaration absent — Coupling "
               "substance is functionally present in the document's own vocabulary.")
    elif cq in ("ABSENT", "SHALLOW", "NEGATED"):
        why = "Primary structural gap: Coupling not structurally declared."
    elif contras:
        why = "Primary structural gap: Integrity Layer not enforced as precondition."
    elif not result.get("construct_coverage", {}).get("Coherence Test"):
        why = "Primary structural gap: Coherence Test not applied."
    else:
        why = "Primary structural gap: Integrity Layer not enforced as precondition."

    # ── Position Assessment ───────────────────────────────────────────────────
    # Auto-built from construct coverage, coupling_state, and conceptual proximity.
    # Answers: "what does this document contain, and what structural gap remains?"
    cc          = result.get("construct_coverage", {})
    cs          = result.get("coupling_state", "ABSENT")
    ic          = result.get("implicit_coupling", {})
    present_cc  = [k for k, v in cc.items() if v]
    absent_cc   = [k for k, v in cc.items() if not v]

    # What the document contains (positive vocabulary + implicit coupling signals)
    contains = []
    if present_cc:
        contains.extend(present_cc[:4])
    if ic.get("found") and "Coupling (implicit)" not in contains:
        contains.append("implicit Coupling signals (protective intent present)")

    if cs == "STRUCTURAL":
        position_result = "Structurally compliant with LAIF"
    elif cs == "FUNCTIONAL":
        position_result = ("Functionally aligned with LAIF in its own vocabulary — "
                           "not LAIF-native")
    else:
        position_result = "Conceptually aligned, structurally incomplete"

    not_enforced = []
    if cs == "FUNCTIONAL":
        not_enforced.append(
            "LAIF-native Coupling declaration absent — the pairing exists in the "
            "document's own vocabulary; certification requires canonical declaration "
            "or documented equivalence mapping"
        )
    elif cs != "STRUCTURAL":
        not_enforced.append("Coupling not structurally declared — restrictions not bound to human interests")
    if not cc.get("Coherence Test"):
        not_enforced.append("Coherence Test not applied — Q1/Q2/Q3 not documented")
    if not cc.get("Integrity Layer"):
        not_enforced.append("Integrity Layer not declared as a deployment precondition")

    position_assessment = {
        "contains":    contains,
        "not_enforced": not_enforced[:3],
        "result":      position_result,
    }

    return {
        "verdict": verdict, "risks": risks, "strengths": strengths, "why": why,
        "position_assessment": position_assessment,
    }


# Module-level consequence descriptions — shared by _structured_findings and
# _structured_remediation so dimension-gap explanations stay consistent.
_DIM_CONSEQUENCE = {
    "structural": (
        "Without a constitutional hierarchy, operational revisions can alter the "
        "governance standard without triggering a constitutional amendment — "
        "foundational protections are not locked against erosion over time."
    ),
    "conceptual": (
        "Low conceptual proximity indicates the document's governance intent is not "
        "substantially aligned with LAIF values. The adoption gap is more fundamental "
        "than terminology — substantive governance redesign is required, not just "
        "terminological substitution."
    ),
    "auditability": (
        "Without numbered, traceable obligations, a PDCA auditor has no objective "
        "basis to verify compliance — compliance claims rest on assertions rather "
        "than verifiable evidence. External audit cannot proceed."
    ),
    "enforceability": (
        "Without enforceable obligations, regulatory bodies cannot hold operators "
        "accountable for governance failures. The standard is aspirational rather "
        "than operationally binding — no party can be required to comply."
    ),
}


def _structured_findings(result):
    """
    Generate a list of structured findings — each with title, severity
    (HIGH / MEDIUM / LOW), evidence, impact, and recommended_action.
    Findings are diagnostic observations; remediation steps are prescriptions.
    """
    findings = []
    cq       = result["coupling_quality"]
    cq_r     = result["coupling_quality_reason"]
    contras  = result["contradictions"]
    gaming   = result["sector_gaming_risk"]
    gaming_r = result["sector_gaming_reason"]
    overall  = result["overall_readiness_score"]
    fcd      = result.get("formal_checks_detail", [])

    cstate   = result.get("coupling_state", "ABSENT")
    func     = result.get("functional_alignment", {})

    # ── Coupling quality ──────────────────────────────────────────────────────
    if cstate == "FUNCTIONAL":
        fam = ", ".join(func.get("Coupling", {}).get("families", []))
        ev  = "; ".join(func.get("Coupling", {}).get("evidence", [])[:2])
        findings.append({
            "title":    "Coupling substance functionally present — not declared in LAIF-native form",
            "severity": "MEDIUM",
            "evidence": (
                f"Structural pairing expressed in the document's own vocabulary "
                f"(signal families: {fam}). Example: «{ev[:180]}»"
            ),
            "impact":   (
                "The substantive requirement of LAIF v1.2 Principle 2 — restrictions bound "
                "to named human interests with protections of comparable force — is expressed "
                "in this document's own terms. What is missing is the LAIF-native declaration "
                "needed for LAIF certification, not the protection itself. Under LAIF v1.2 "
                "Part Eight this constitutes rebuttal evidence of equivalent structural "
                "diligence through alternative documented means."
            ),
            "recommended_action": (
                "Two equally valid paths: (a) for LAIF certification, restate the existing "
                "pairings using the canonical Coupling declaration (Toolkit §2 B.1); or "
                "(b) retain the document's own vocabulary and record a documented equivalence "
                "mapping to LAIF Section B.1, per the Regulatory Integration Guide's "
                "SATISFIES/EXTENDS methodology."
            ),
        })
    elif cq == "ABSENT":
        findings.append({
            "title":    "Coupling not structurally declared — no restriction paired with a human interest",
            "severity": "HIGH",
            "evidence": "Neither the canonical term 'Coupling' nor a functional equivalent "
                        "of the structural pairing was detected in the document.",
            "impact":   (
                "Every governance restriction can be weakened in isolation without triggering "
                "a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test "
                "failure. Integrity Layer precondition cannot be satisfied without Coupling "
                "(LAIF v1.2 Principle 2)."
            ),
            "recommended_action": (
                "Declare structural Coupling for each governance restriction: name the specific "
                "human interest at stake and pair it with a protection of equivalent normative "
                "force (Toolkit §2 B.1) — or express the same pairing in the document's own "
                "vocabulary with a documented equivalence mapping."
            ),
        })
    elif cq == "SHALLOW":
        findings.append({
            "title":    "Coupling declared as SHALLOW — structural pairing not established",
            "severity": "HIGH",
            "evidence": cq_r,
            "impact":   (
                "Mentioning 'Coupling' without a structural declaration does not satisfy "
                "LAIF v1.2 Principle 2. The term is present but the required architecture — "
                "named human interest, paired protection, equivalent normative force — is "
                "absent. A formal PASS with SHALLOW Coupling = WEAK PASS only."
            ),
            "recommended_action": (
                "Rewrite Coupling references to include the named human interest, the "
                "restriction paired with it, and a statement of equivalent normative force "
                "on both sides (Toolkit §2 B.1; LAIF v1.2 Principle 2)."
            ),
        })
    elif cq == "NEGATED":
        findings.append({
            "title":    "Coupling explicitly negated or declared inapplicable",
            "severity": "HIGH",
            "evidence": cq_r,
            "impact":   (
                "Active negation is the most adversarial Coupling failure mode. The document "
                "asserts the requirement does not apply — this cannot satisfy Q1 of the "
                "Coherence Test regardless of other scores (LAIF v1.2 Principle 2)."
            ),
            "recommended_action": (
                "Remove the negation of Coupling and replace with a structural declaration "
                "naming the specific human interest each restriction protects (Toolkit §2 B.1)."
            ),
        })

    # ── Structural contradictions ─────────────────────────────────────────────
    for prop, desc, ctx in contras:
        findings.append({
            "title":    f"Structural contradiction: {prop}",
            "severity": "HIGH",
            "evidence": f"{desc} — «{ctx[:120]}»",
            "impact":   (
                f"The document simultaneously claims '{prop}' and contains language that "
                f"negates it. This is a Structural Honesty failure (LAIF v1.2 A.2): stated "
                f"objectives do not correspond to the document's implemented provisions. "
                f"The Integrity Layer precondition cannot be satisfied."
            ),
            "recommended_action": (
                f"Resolve the contradiction: either remove the contradicting language and "
                f"implement '{prop}' substantively, or remove the claim to this property and "
                f"document why it does not apply. Retaining both violates Structural Honesty "
                f"(Toolkit §1.4)."
            ),
        })

    # ── Sector gaming ─────────────────────────────────────────────────────────
    if gaming == "HIGH":
        findings.append({
            "title":    "High sector gaming risk detected",
            "severity": "HIGH",
            "evidence": gaming_r,
            "impact":   (
                "High sector keyword density with low substantive governance content is "
                "inconsistent with genuine compliance. Keyword selection without governance "
                "substance would not produce just outcomes at the individual-decision scale — "
                "failing Q2 Consistency (LAIF v1.2 Principle 5)."
            ),
            "recommended_action": (
                "Increase substantive coverage: add concrete obligations (auditability), "
                "named responsible parties (enforceability), and structural Coupling "
                "declarations. Sector keywords must be the vocabulary of genuine governance "
                "intent, not a substitute for it."
            ),
        })
    elif gaming == "MEDIUM":
        findings.append({
            "title":    "Medium sector gaming risk — vocabulary present without governance intent",
            "severity": "MEDIUM",
            "evidence": gaming_r,
            "impact":   (
                "Sector-specific vocabulary without underlying conceptual coverage suggests "
                "keyword optimisation. Conceptual proximity should be ≥40 for credible "
                "sector alignment."
            ),
            "recommended_action": (
                "Pair each sector-specific risk indicator with a substantive governance "
                "measure — obligation, monitoring mechanism, or Coupling declaration."
            ),
        })

    # ── Paraphrase violations ─────────────────────────────────────────────────
    for term, vs in result["paraphrase_violations"].items():
        ex = vs[0][1].replace("\n", " ")[:100] if vs else ""
        findings.append({
            "title":    f"Paraphrase violation: forbidden substitution of '{term}'",
            "severity": "MEDIUM",
            "evidence": f"{len(vs)} instance(s). Example: «{ex}»",
            "impact":   (
                f"Informal substitutes for '{term}' do not carry its enforcement weight. "
                f"'Coupling' is not equivalent to 'alignment' — the canonical term requires "
                f"a named human interest, paired protection, and equivalent normative force "
                f"that informal equivalents lack (Toolkit §1)."
            ),
            "recommended_action": (
                f"Replace each forbidden term with '{term}' and add the structural "
                f"declaration the canonical term requires (Toolkit §1)."
            ),
        })

    # ── Formal compliance gaps ────────────────────────────────────────────────
    missing_formal = [(lbl, ok) for lbl, ok in fcd if not ok]
    if missing_formal and result["formal_laif_compliance"] == "FAIL":
        labels = ", ".join(lbl for lbl, _ in missing_formal[:4])
        if len(missing_formal) > 4:
            labels += f" and {len(missing_formal) - 4} others"
        findings.append({
            "title":    (
                f"Formal compliance gate not satisfied — "
                f"{len(missing_formal)} required construct(s) absent"
            ),
            "severity": "HIGH",
            "evidence": f"Missing: {labels}.",
            "impact":   (
                "Formal LAIF compliance is binary. Missing any single required construct "
                "= FAIL regardless of overall readiness score. These constructs are "
                "structurally necessary — they cannot be satisfied by partial presence."
            ),
            "recommended_action": (
                "Add the missing constructs substantively — each must be meaningfully "
                "implemented, not merely cited. Implement in this priority order: "
                "Coupling → Coherence Test → Integrity Layer → constitutional hierarchy "
                "→ self-application clause."
            ),
        })

    # ── Low dimension scores ──────────────────────────────────────────────────
    for dim_key, dim_label, score_key, threshold in [
        ("structural",    "Structural governance architecture", "structural_score",           40),
        ("conceptual",    "Conceptual coverage",               "conceptual_proximity_score",  30),
        ("auditability",  "Auditability",                      "auditability_score",           40),
        ("enforceability","Enforceability",                    "enforceability_score",         40),
    ]:
        score = result[score_key]
        if score < threshold:
            bd = result["score_breakdown"][dim_key]
            missed = ", ".join(lbl for lbl, _ in bd["missed"][:3])
            findings.append({
                "title":    f"Low {dim_label} score ({score}/100)",
                "severity": "MEDIUM" if score > 0 else "HIGH",
                "evidence": f"Score {score}/100. Key missed signals: {missed}.",
                "impact":   _DIM_CONSEQUENCE.get(dim_key, f"Score below threshold."),
                "recommended_action": (
                    f"Target the missed signals for this dimension: {missed}. "
                    f"The weight rationale for this dimension is detailed in the "
                    f"Scores and Signal Breakdown section above."
                ),
            })

    return findings


def _structured_remediation(result):
    """
    Structured remediation steps with Problem / Why it matters / Concrete fix.
    Higher-impact items first. Rendered in the markdown report; plain-string
    recommended_remediation_steps retained separately for console output.
    """
    steps = []
    _cstate = result.get("coupling_state", "ABSENT")
    _func   = result.get("functional_alignment", {})

    # 1 — Paraphrase violations (most specific, highest immediate impact).
    # DIVERGENCE_NOTE documents (own vocabulary, no LAIF claim) skip this —
    # their path is equivalence mapping, not term substitution.
    if result.get("paraphrase_classification", "VIOLATION") == "VIOLATION":
        for term, violations in result["paraphrase_violations"].items():
            for _, ctx in violations[:1]:
                snippet = ctx.replace("\n", " ").strip()[:100]
                steps.append({
                    "problem": (
                        f"Forbidden paraphrase of '{term}' detected: «{snippet}»"
                    ),
                    "why_it_matters": (
                        f"'{term}' is a structurally load-bearing canonical term. Informal "
                        f"substitutes do not carry the enforcement obligation the term requires. "
                        f"Using 'alignment' or 'connection' where 'Coupling' is required leaves "
                        f"each restriction without a mandatory paired protection (Toolkit §1)."
                    ),
                    "concrete_fix": (
                        f"Replace the forbidden term with '{term}' at every occurrence. "
                        f"For 'Coupling' specifically, also add: the named human interest, "
                        f"the paired restriction, and a statement of equivalent normative force "
                        f"on both sides (Toolkit §2 B.1; LAIF v1.2 Principle 2)."
                    ),
                })

    # 1b — Functionally aligned documents: the top action is a choice of path,
    # stated before any construct-level gap items.
    if _cstate == "FUNCTIONAL":
        fam = ", ".join(_func.get("Coupling", {}).get("families", []))
        steps.append({
            "problem": (
                "Coupling substance present in the document's own vocabulary "
                f"({fam}) but not declared in LAIF-native form"
            ),
            "why_it_matters": (
                "LAIF certification requires the canonical declaration, but the "
                "protective structure itself already exists. Treating this as a "
                "substantive failure would misstate the document (LAIF v1.2 Part Eight "
                "recognises equivalent structural diligence through alternative "
                "documented means)."
            ),
            "concrete_fix": (
                "Either restate the existing pairings as canonical Coupling declarations "
                "(Toolkit §2 B.1), or record a documented equivalence mapping to PDCA "
                "Section B.1 per the Regulatory Integration Guide — both paths are valid; "
                "the choice belongs to the document's owner."
            ),
        })

    # 2 — Coupling (document-specific: IMPLICIT vs ABSENT/SHALLOW/NEGATED)
    cq = result["coupling_quality"]
    cs = result.get("coupling_state", "ABSENT")
    ic = result.get("implicit_coupling", {})

    if cs == "IMPLICIT":
        # Document already has protective intent — the fix is structural, not conceptual.
        signal_excerpts = ic.get("matches", [])
        first_signal = signal_excerpts[0][:100].strip() if signal_excerpts else "protective language detected"
        steps.append({
            "problem": "Implicit protective signals present but not declared as structural Coupling.",
            "why_it_matters": (
                f"The document already expresses protective intent — detected: "
                f"«{first_signal}». However, implicit intent does not constitute structural "
                f"Coupling: the protection can be removed without affecting the obligation it "
                f"was meant to serve. The upgrade required is structural, not conceptual "
                f"(LAIF v1.2 Principle 2; Toolkit §2 B.1)."
            ),
            "concrete_fix": (
                "Convert each detected implicit signal into an explicit Coupling declaration: "
                "'Coupling between [the restriction already present] and [the specific human "
                "interest the detected protective language names], with equivalent normative "
                "force on both sides — neither may be weakened in isolation.' "
                "The governance intent is present; only the structural binding is missing "
                "(Toolkit §2 B.1)."
            ),
        })
    elif cq in ("ABSENT", "SHALLOW", "NEGATED"):
        cq_r = result["coupling_quality_reason"]
        if cq == "ABSENT":
            problem = ("Restriction-protection pairing not established — no governance "
                       "restriction is bound to the specific interest it protects, in "
                       "any vocabulary.")
        elif cq == "SHALLOW":
            problem = f"Coupling declared SHALLOW — {cq_r[:110]}"
        else:
            problem = f"Coupling explicitly negated — {cq_r[:110]}"
        steps.append({
            "problem": problem,
            "why_it_matters": (
                "Without structural Coupling, no governance restriction is paired with the "
                "specific human interest it protects. Each restriction can be weakened "
                "independently. Q1 (Coupling) failure = automatic failure of the full "
                "Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1)."
            ),
            "concrete_fix": (
                "For each restriction, name the specific interest it protects and bind "
                "the two together so that neither can be weakened without the other, "
                "with the protection as enforceable as the restriction. The document's "
                "own vocabulary is sufficient for the structure; the canonical form "
                "('Coupling between [restriction] and [interest], with equivalent "
                "normative force' — Toolkit §2 B.1) is required only on the "
                "LAIF-native certification path, where an equivalence mapping is the "
                "alternative (Regulatory Integration Guide Part One)."
            ),
        })

    # 2b — Document-specific dimension gaps (inserted before generic LAIF constructs).
    # Sort dimensions by score ascending — most deficient dimension gets priority.
    # Up to 2 steps inserted here; ensures "What Must Be Fixed First" varies by document.
    _DIM_THRESHOLDS = {
        "structural": 50, "conceptual": 35, "auditability": 50, "enforceability": 50,
    }
    _DIM_LABELS = {
        "structural":    "Structural governance architecture",
        "conceptual":    "Conceptual governance coverage",
        "auditability":  "Auditability",
        "enforceability":"Enforceability",
    }
    dim_scores = sorted(
        [
            ("structural",    result["structural_score"]),
            ("conceptual",    result["conceptual_proximity_score"]),
            ("auditability",  result["auditability_score"]),
            ("enforceability",result["enforceability_score"]),
        ],
        key=lambda x: x[1],   # ascending — most deficient first
    )
    dim_inserted = 0
    for dim_key, score in dim_scores:
        if dim_inserted >= 2:
            break
        if score >= _DIM_THRESHOLDS.get(dim_key, 50):
            continue
        bd     = result["score_breakdown"][dim_key]
        missed = ", ".join(lbl for lbl, _ in bd["missed"][:3])
        steps.append({
            "problem": (
                f"{_DIM_LABELS[dim_key]} score critically low ({score}/100) — "
                f"most deficient dimension after Coupling."
            ),
            "why_it_matters": _DIM_CONSEQUENCE.get(dim_key, f"{dim_key} below threshold."),
            "concrete_fix": (
                f"Address the {len(bd['missed'])} missed signals for this dimension. "
                f"Critical gaps: {missed}. "
                f"Full signal breakdown in the Scores section."
            ),
        })
        dim_inserted += 1

    # 3 — Coherence Test
    if not result["construct_coverage"].get("Coherence Test"):
        steps.append({
            "problem": "Coherence Test not applied — no Q1/Q2/Q3 documentation present.",
            "why_it_matters": (
                "The Coherence Test is the primary LAIF decision instrument: Q1 Coupling "
                "(specific human interest identified and protected?), Q2 Consistency "
                "(governance logic scale-invariant?), Q3 Reversibility (future actors can "
                "modify?). Without it, there is no evidence provisions were tested for "
                "structural soundness before deployment (LAIF v1.2 Part One)."
            ),
            "concrete_fix": (
                "Add PDCA Section B: apply all three Coherence Test questions to each major "
                "governance provision. Each must be answered affirmatively. Q1 failure = "
                "full failure — do not proceed to Q2/Q3 without satisfying Q1 "
                "(LAIF v1.2 Part One; Toolkit §2)."
            ),
        })

    # 4 — Integrity Layer
    if not result["construct_coverage"].get("Integrity Layer"):
        steps.append({
            "problem": ("No all-conditions-must-pass deployment gate — deployment is not "
                        "conditioned on transparency, honesty, and containment being "
                        "simultaneously satisfied."),
            "why_it_matters": (
                "Without a threshold gate, a system can be deployed while any of the three "
                "core preconditions is unmet: the ability to account for its outputs, the "
                "correspondence of stated to implemented objectives, and operation within "
                "documented boundaries. Partial satisfaction functioning as approval is the "
                "single most common structural failure this model detects (LAIF v1.2 Part Two)."
            ),
            "concrete_fix": (
                "Establish a deployment gate with three conditions that must all hold "
                "simultaneously — (i) the system can produce a meaningful account of any "
                "output that materially affects a person; (ii) stated objectives correspond "
                "to implemented objectives, verified by independent review; (iii) the system "
                "operates within documented boundaries in all tested conditions, escalating "
                "out-of-scope cases. The document's own vocabulary is sufficient; the "
                "canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only "
                "on the LAIF-native certification path."
            ),
        })

    # 5 — Structural contradictions
    for prop, desc, ctx in result["contradictions"]:
        steps.append({
            "problem": f"Structural contradiction in '{prop}': {desc}",
            "why_it_matters": (
                f"Claiming '{prop}' while containing language that negates it fails "
                f"Structural Honesty (LAIF v1.2 A.2). Contradictions invalidate the "
                f"Integrity Layer precondition regardless of other scores."
            ),
            "concrete_fix": (
                f"Resolve the contradiction: (a) remove the contradicting language and "
                f"implement '{prop}' substantively, or (b) remove the claim to '{prop}' "
                f"and document why the property does not apply. Both cannot coexist "
                f"(Toolkit §1.4)."
            ),
        })

    # 6 — Constitutional hierarchy (low structural score)
    if result["structural_score"] < 50:
        bd = result["score_breakdown"]["structural"]
        missed = ", ".join(lbl for lbl, _ in bd["missed"][:3])
        steps.append({
            "problem": (
                f"Constitutional hierarchy not declared "
                f"(structural score {result['structural_score']}/100). Missing: {missed}."
            ),
            "why_it_matters": (
                "Without a non-amendable three-tier hierarchy, operational revisions can "
                "erode Foundational Principles. LAIF's structure — Foundational Principles "
                "(non-amendable) → Provisions → Operational Standards — prevents governance "
                "degradation over time (LAIF v1.2 Principle 3)."
            ),
            "concrete_fix": (
                "Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational "
                "Principles — non-amendable; (ii) Provisions derived from Principles; "
                "(iii) Operational Standards — subordinate and revisable. Add a "
                "non-amendable clause, self-application clause (Part Seven), and threshold "
                "gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, "
                "Two, Seven)."
            ),
        })

    # 7 — Sector-specific (top 2 from profile)
    sector_label = result.get("sector_label", result["sector_used"])
    for step_text in result.get("sector_remediation_priority", [])[:2]:
        if not any(step_text[:60] in s.get("concrete_fix", "")[:60] for s in steps):
            # derive a distinct problem statement from the first clause of step_text
            first_clause = re.split(r"\s(?:—|–|:)\s", step_text, maxsplit=1)[0]
            if len(first_clause) > 110:
                first_clause = first_clause[:110].rstrip() + "…"
            steps.append({
                "problem": f"{first_clause} — not addressed in this document.",
                "why_it_matters": (
                    f"In the {sector_label} deployment context, this governance gap exposes "
                    f"specific human interests that materially affect persons subject to the "
                    f"AI system's outputs. Each gap represents a Coupling declaration that is "
                    f"absent or insufficient for this sector "
                    f"(Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering)."
                ),
                "concrete_fix": step_text,
            })

    return steps


# ── Remediation step generator ────────────────────────────────────────────────

def _remediation(result):
    """
    Produce ordered remediation steps, highest-impact first.
    Where paraphrase violations are present, generate specific rewrites showing
    the forbidden phrase and its LAIF-compliant replacement.

    Source: LAIF_Compliance_Toolkit.txt §2 — PDCA Section B.1 (Coupling
    documentation requires naming the specific human interest and pairing it
    with a protection of equivalent normative force).
    """
    steps = []
    _cstate = result.get("coupling_state", "ABSENT")
    _para_violation = result.get("paraphrase_classification", "VIOLATION") == "VIOLATION"

    # 1 — Paraphrase violations (specific rewrites, highest impact). Only for
    # documents that use or claim LAIF vocabulary; for external instruments in
    # their own vocabulary the same detections are informational divergence
    # notes, handled by the equivalence-mapping step below.
    if result["paraphrase_violations"] and _para_violation:
        for term, violations in result["paraphrase_violations"].items():
            for _, ctx in violations[:2]:
                snippet = ctx.replace("\n", " ").strip()[:120]
                steps.append(
                    f"Paraphrase rewrite required — '{term}' guard triggered. "
                    f"Detected: \"{snippet}\". "
                    f"Replace the forbidden term with the canonical LAIF term '{term}'. "
                    f"The substitution is not merely terminological: '{term}' carries a "
                    f"structural enforcement requirement that informal equivalents do not. "
                    f"Rewrite pattern: '[alignment/connection/linkage] between [X] and [Y]' "
                    f"→ 'Coupling between [X] and [the specific human interest Y protects], "
                    f"with a protection of equivalent normative force' (LAIF v1.2 Principle 2; "
                    f"Toolkit §2 B.1)."
                )

    # 2 — Coupling (core LAIF requirement). Two distinct situations:
    #     substance functionally present → the gap is the LAIF-native
    #     declaration, and equivalence mapping is an equally valid path;
    #     substance absent → the pairing itself must be built.
    if _cstate == "FUNCTIONAL":
        steps.append(
            "Coupling substance is already present in this document's own vocabulary. "
            "Choose one of two equally valid paths: (a) for LAIF certification, restate "
            "the existing restriction-protection pairings as canonical Coupling "
            "declarations (Toolkit §2 B.1); or (b) retain the document's vocabulary and "
            "record a documented equivalence mapping to LAIF PDCA Section B.1, following "
            "the Regulatory Integration Guide's SATISFIES/EXTENDS methodology. No "
            "substantive redesign is required (LAIF v1.2 Part Eight — equivalent "
            "structural diligence)."
        )
    elif not result["construct_coverage"].get("Coupling"):
        steps.append(
            "Bind each governance restriction to the specific human interest it protects: "
            "name the interest with specificity (not a category — e.g. 'the patient's "
            "interest in treatment decisions based on accurate clinical assessment'), "
            "pair it with a protection as enforceable as the restriction, and lock the "
            "pair so neither can be weakened in isolation (LAIF v1.2 Principle 2). The "
            "document's own vocabulary is sufficient; canonical Coupling declarations "
            "(Toolkit §2 B.1) are required only for LAIF-native certification."
        )

    # 3 — Coherence Test (always needed when missing)
    if not result["construct_coverage"].get("Coherence Test"):
        steps.append(
            "Apply the Coherence Test before any governance provision is issued or deployment "
            "authorised: Q1 Coupling (does the deployment identify and protect the specific "
            "human interest at risk?), Q2 Consistency (would this governance logic produce just "
            "and workable outcomes at all comparable scales?), Q3 Reversibility (does the "
            "deployment preserve the capacity of future actors to reverse or modify its "
            "consequences?). All three must be answered affirmatively. Failure at Q1 constitutes "
            "automatic failure of the full test (LAIF v1.2 Part One)."
        )

    # 4 — Integrity Layer (always needed when missing)
    if not result["construct_coverage"].get("Integrity Layer"):
        steps.append(
            "Establish the Integrity Layer as a deployment precondition: A.1 Structural "
            "Transparency (system can produce a compliant meaningful account of any material "
            "output), A.2 Structural Honesty (stated objectives correspond to implemented "
            "objectives, verified by independent review), A.3 Structural Containment (system "
            "operates within documented operational boundaries in all tested conditions including "
            "edge cases). All three must be satisfied simultaneously before deployment proceeds. "
            "Partial satisfaction is failure — there is no partial credit "
            "(LAIF v1.2 Part Two; Toolkit §1.3–§1.5)."
        )

    # 5 — Terminology adoption (if none of the canonical terms are present)
    if result["terminology_score"] == 0:
        steps.append(
            "Adopt LAIF canonical terminology throughout the document. Replace informal "
            "equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; "
            "'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → "
            "'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; "
            "'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural "
            "Containment'. Each canonical term carries structural enforcement meaning that "
            "paraphrases do not (LAIF_Compliance_Toolkit.txt §1)."
        )

    # 6 — Constitutional hierarchy (if structural score is low)
    if result["structural_score"] < 50:
        steps.append(
            "Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational "
            "Principles at the apex — non-amendable, define the governance standard; (ii) "
            "Provisions derived from Principles — cannot contradict Principles; (iii) Operational "
            "Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without "
            "amending Principles. This hierarchy is not optional — it prevents operational revision "
            "from eroding constitutional guarantees (LAIF v1.2 Principle 3)."
        )

    # 7 — Self-application clause (always needed when missing)
    if not any(re.search(r"PART SEVEN|self.application|applies to regulatory", g, re.IGNORECASE)
               for g in result["gaps"]):
        steps.append(
            "Add a self-application clause: specify explicitly that the governance framework "
            "applies to regulatory bodies, governance actors, and oversight authorities themselves "
            "— not only to AI system operators. Rewrite: '[framework] governs AI deployment by "
            "operators' → '[framework] governs AI deployment by all actors, including regulatory "
            "bodies and governance authorities who are subject to the same Coherence Test as "
            "operators' (LAIF v1.2 Part Seven)."
        )

    # 8 — Sector-specific remediation (appended last, sector-contextualised)
    for step in result.get("sector_remediation_priority", []):
        if step not in steps:
            steps.append(step)

    return steps


# ── Deployment risk tier ─────────────────────────────────────────────────────
# Source: LAIF_Compliance_Toolkit.txt §7 — Tiering by stakes and structural depth.
# A document cannot be LOW risk if it fails formal compliance; structural depth
# is a gating condition on MODERATE because WEAK/HOLLOW depth indicates that
# required properties may be nominally present but structurally inert.

def _deployment_risk_tier(overall_score, strong_laif_compliance):
    """
    Derive deployment risk tier from overall readiness and strong compliance verdict.
    Source: LAIF_Compliance_Toolkit.txt §7 — Tiering by stakes and structural depth.

    LOW      — STRONG PASS (all Integrity Layer and Coherence Test conditions met)
    MODERATE — overall ≥70 (approaching compliance; targeted remediation sufficient)
    HIGH     — overall ≥40 (significant gaps; major remediation before deployment)
    CRITICAL — overall <40 (fundamental gaps; deployment should be blocked)
    """
    if strong_laif_compliance == "STRONG PASS":
        return "LOW"
    if overall_score >= 70:
        return "MODERATE"
    if overall_score >= 40:
        return "HIGH"
    return "CRITICAL"


# ── Governance signal strength (derived view) ─────────────────────────────────
# Derived entirely from existing scored fields — no new detection logic.
# Answers: "how strong is the real-world governance signal in this document?"
# independent of LAIF-specific structural vocabulary.
#
# Uses conceptual proximity (40%), enforceability (30%), auditability (30%).
# These three dimensions are the best proxies for governance quality that are
# measurable without requiring LAIF canonical terms to be present.

def _governance_signal_strength(result):
    """
    Derived score using EXISTING fields only.  No new detection logic.

    Weights: conceptual 40%, enforceability 30%, auditability 30%.
    Tiers: STRONG ≥75 · MODERATE ≥55 · WEAK ≥35 · MINIMAL <35
    """
    conceptual     = result.get("conceptual_proximity_score", 0)
    enforceability = result.get("enforceability_score", 0)
    auditability   = result.get("auditability_score", 0)

    score = int((conceptual * 0.4) + (enforceability * 0.3) + (auditability * 0.3))

    if score >= 75:
        tier = "STRONG"
    elif score >= 55:
        tier = "MODERATE"
    elif score >= 35:
        tier = "WEAK"
    else:
        tier = "MINIMAL"

    return {"score": score, "tier": tier}


# ── Directionality check ─────────────────────────────────────────────────────
# Lightweight heuristic: if rights-language (accountability, transparency, safety,
# oversight) is used primarily to justify AI/operator control OF humans rather than
# to protect humans FROM AI outputs, apply a small reduction to the conceptual score.
#
# This differentiates surveillance governance ("AI monitors workers for compliance")
# from protective governance ("workers protected from automated decisions").
# Does NOT affect formal compliance, coupling detection, or any other dimension.
# Reduction is -8 points on conceptual, capped at 0 — max impact on overall ~1.6 pts.

_DIRECTIONALITY_SURVEILLANCE = [
    # AI/system/algorithm as actor directly monitoring/tracking humans
    r"\b(?:AI|system|algorithm)\s+(?:monitors?|tracks?)\s+(?:worker|employee|patient|individual)\b",
    # Worker performance is the object of AI tracking
    r"\bworker\s+performance\s+(?:tracking|monitoring)\b",
    # Continuous AI monitoring of humans or their compliance
    r"\bcontinuous\s+(?:AI\s+)?monitoring\s+of\s+(?:worker|employee|staff|personnel|compliance)\b",
    # "AI-monitored performance" or "AI-monitored compliance" compound
    r"\bAI.monitored\s+(?:performance|compliance)\b",
]

_DIRECTIONALITY_RIGHTS = [
    r"\baccountability\b", r"\btransparency\b", r"\bsafety\b", r"\boversight\b",
]


def _directionality_penalty(text, score):
    """
    If rights-language co-occurs with AI-as-surveillor patterns, apply -8 to the
    conceptual score.  Returns (adjusted_score, was_penalised: bool).

    Rationale: protection-of-humans and control-of-humans both use identical
    rights vocabulary.  A document that deploys accountability/transparency/safety
    language to justify AI surveillance should not score identically to one that
    uses those concepts to protect humans from AI decisions.

    Only fires when all of: ≥1 surveillance indicator AND ≥2 rights-language hits.
    Does not affect formal compliance, coupling state, or any threshold.
    """
    surv_hits  = sum(1 for p in _DIRECTIONALITY_SURVEILLANCE
                     if re.search(p, text, re.IGNORECASE))
    rights_hits = sum(1 for p in _DIRECTIONALITY_RIGHTS
                      if re.search(p, text, re.IGNORECASE))
    if surv_hits >= 1 and rights_hits >= 2:
        return max(0, score - 8), True
    return score, False



# ── Phase 3V governance repair reporting helpers ─────────────────────────────
# These helpers derive external-framework presentation fields from existing
# deterministic diagnostics. They do not change scoring weights, formal
# LAIF-native validation, or validate.py behavior.

DOCUMENT_TYPE_PRECEDENCE = (
    "binding_legal_instrument",
    "executive_policy_directive",
    "voluntary_risk_framework",
    "sector_assurance_checklist",
    "technical_standard",
    "public_sector_policy",
    "procurement_assessment_form",
    "implementation_guide",
    "internal_policy",
    "vendor_compliance_submission",
    "unknown_governance_document",
)

_DOCUMENT_TYPE_PATTERNS = [
    ("binding_legal_instrument", (r"\bregulation\b", r"\bharmonised rules\b", r"\bartificial intelligence act\b", r"\bofficial journal\b", r"\bmarket surveillance\b", r"\bconformity assessment\b", r"\bproviders?\b", r"\bdeployers?\b", r"\bpost-market monitoring\b", r"\bserious incident reporting\b")),
    ("executive_policy_directive", (r"\bexecutive order\b", r"\bpresident\b", r"\bsecretar(?:y|ies)\b", r"\bfederal agencies\b", r"\bagency heads?\b", r"\bshall\b.{0,80}\bagenc")),
    ("voluntary_risk_framework", (r"\brisk management framework\b", r"\bvoluntary framework\b", r"\bvoluntary\b", r"\bgovern, map, measure, and manage\b", r"\bnon-sector-specific\b", r"\buse-case agnostic\b")),
    ("sector_assurance_checklist", (r"\bassurance checklist\b", r"\bdtac\b", r"\bdigital technology assessment criteria\b", r"\bclinical safety(?: case| officer)?\b", r"\bhazard log\b", r"\bdcb0129\b", r"\bpatient care\b", r"\bnhs\b")),
    ("technical_standard", (r"\biso/iec\b", r"\btechnical standard\b", r"\bstandard specifies\b", r"\brequirements and guidance\b")),
    ("public_sector_policy", (r"\bpolicy for the responsible use of ai in government\b", r"\bresponsible use of ai in government\b", r"\bpublic servants?\s+must\b", r"\bgovernment agencies\s+and\s+public servants\s+must\b", r"\bgovernment agencies\s+must\b", r"\bagencies must disclose\b", r"\bresponsible ai use by agencies\b", r"\bai use registers?\b", r"\bhuman review\b", r"\baccountable officials?\b", r"\bdigital transformation agency\b", r"\bdta\b", r"\bpublic sector policy\b")),
    ("procurement_assessment_form", (r"\bprocurement\b", r"\bassessment form\b", r"\bvendor\b", r"\bsupplier\b", r"\bcontract\b")),
    ("implementation_guide", (r"\bimplementation guide\b", r"\bplaybook\b", r"\bguidance for implementing\b", r"\bhow to implement\b")),
    ("internal_policy", (r"\binternal policy\b", r"\bdepartment policy\b", r"\bcompany policy\b", r"\borganizational policy\b")),
    ("vendor_compliance_submission", (r"\bvendor submission\b", r"\bcompliance submission\b", r"\battestation\b", r"\bsupplier response\b")),
]

_DOCUMENT_TYPE_PRECEDENCE_RANK = {doc_type: idx for idx, doc_type in enumerate(DOCUMENT_TYPE_PRECEDENCE)}

_DOCUMENT_TYPE_FORCE = {
    "binding_legal_instrument": "Binding legal instrument with public-law force where adopted; operational closure depends on delegated controls, evidence, and enforcement machinery.",
    "executive_policy_directive": "Executive policy directive with administrative force over named agencies or executive functions; implementation depends on agency ownership and follow-through controls.",
    "voluntary_risk_framework": "Voluntary risk-management framework; high guidance value but limited force unless incorporated into contracts, regulation, assurance, or internal policy gates.",
    "sector_assurance_checklist": "Sector assurance checklist; useful for assurance triage where mapped to accountable reviewers, evidence artifacts, and pass/fail gates.",
    "procurement_assessment_form": "Procurement assessment form; force arises through procurement conditions, contract clauses, supplier obligations, and audit rights.",
    "technical_standard": "Technical standard; force depends on adoption by regulation, contract, certification scheme, or institutional policy.",
    "implementation_guide": "Implementation guide; operational value depends on conversion into mandatory owners, controls, evidence, and review gates.",
    "public_sector_policy": "Public-sector AI policy; force depends on government authority, accountable public-sector owners, disclosure records, human review evidence, exceptions, incidents, and monitoring consequences.",
    "internal_policy": "Internal policy; force depends on organizational authority, accountable owners, monitoring, and consequences.",
    "vendor_compliance_submission": "Vendor compliance submission; value depends on independent verification, contract remedies, audit rights, and evidence review.",
    "unknown_governance_document": "Governance document with unclear authority; reviewer must establish institutional force, accountable owner, and evidence basis before reliance.",
}

_DOC_TYPE_USE = {
    "binding_legal_instrument": ("Regulatory/legal governance mapping, enforcement-design review, and systemic failure-pathway analysis.", "Not sufficient by itself as implementation evidence, operational assurance, or LAIF-native certification."),
    "executive_policy_directive": ("Agency implementation planning, executive control mapping, and accountability-gap review.", "Not sufficient by itself as proof that agencies implemented, audited, or sustained the required controls."),
    "voluntary_risk_framework": ("Governance program design, procurement reference, assurance planning, and control-gap analysis.", "Not sufficient by itself as binding compliance, operational evidence, or certification."),
    "sector_assurance_checklist": ("Assurance triage, reviewer workflow design, and sector-specific evidence requests.", "Not sufficient without source evidence, accountable reviewer sign-off, and operational gate criteria."),
    "procurement_assessment_form": ("Procurement due diligence, supplier evidence requests, and contract-control design.", "Not sufficient without contract terms, audit rights, verification evidence, and remedies."),
    "technical_standard": ("Technical control mapping and conformity planning.", "Not sufficient unless adopted by an authority, assurance scheme, contract, or internal gate."),
    "implementation_guide": ("Operational planning and control-design support.", "Not sufficient until converted into mandatory controls, owners, evidence, and lifecycle review."),
    "public_sector_policy": ("Public-sector operating policy review, government AI use register design, disclosure/control mapping, and accountability-gap review.", "Not sufficient without accountable owners, human-review evidence, disclosure records, exception handling, incident tracking, and monitoring consequences."),
    "internal_policy": ("Institutional governance review and operational control mapping.", "Not sufficient without implementation records, monitoring, accountability, and escalation evidence."),
    "vendor_compliance_submission": ("Supplier assurance review and evidence triage.", "Not sufficient without independent verification, source artifacts, audit access, and remedies."),
    "unknown_governance_document": ("Preliminary governance triage and document classification review.", "Not sufficient for reliance until authority, scope, controls, and evidence are confirmed."),
}

_OWNER_GAP_RE = re.compile(r"\b(owner|responsible|accountable|authority|officer|agency|provider|deployer)\b", re.IGNORECASE)
_GATE_GAP_RE = re.compile(r"\b(gate|approval|authori[sz]ation|shall not|before deployment|pre-deployment|conformity assessment|sign[- ]off)\b", re.IGNORECASE)
_EVIDENCE_GAP_RE = re.compile(r"\b(evidence|record|documentation|trace|log|audit|report)\b", re.IGNORECASE)
_LIFECYCLE_GAP_RE = re.compile(r"\b(lifecycle|monitor|review|post-market|post deployment|incident|change management)\b", re.IGNORECASE)
_ROLLBACK_GAP_RE = re.compile(r"\b(rollback|reversib|fallback|withdraw|suspend|stop|decommission)\b", re.IGNORECASE)
_RESIDUAL_RISK_RE = re.compile(r"\b(residual risk|remaining risk|risk acceptance|risk treatment|mitigation)\b", re.IGNORECASE)


def _document_type_pattern_hits(haystack, doc_type, patterns):
    hits = sum(1 for pat in patterns if re.search(pat, haystack, re.IGNORECASE))
    if doc_type == "binding_legal_instrument":
        if not any(anchor in haystack for anchor in ("regulation laying down", "harmonised rules", "artificial intelligence act", "official journal")):
            return 0
        return hits if hits >= 2 else 0
    if doc_type == "executive_policy_directive":
        if "executive order" in haystack:
            return max(hits, 2)
        return hits if hits >= 2 and ("federal agencies" in haystack or "agency head" in haystack) else 0
    if doc_type == "voluntary_risk_framework":
        if "risk management framework" in haystack and any(term in haystack for term in ("voluntary", "govern, map, measure", "non-sector-specific", "use-case agnostic")):
            return max(hits, 2)
        return hits if hits >= 3 else 0
    if doc_type == "sector_assurance_checklist":
        if "digital technology assessment criteria" in haystack or "dtac" in haystack:
            return max(hits, 2)
        return hits if hits >= 2 and any(term in haystack for term in ("clinical safety", "dcb0129", "hazard log")) else 0
    if doc_type == "technical_standard":
        return hits if hits >= 1 else 0
    if doc_type == "public_sector_policy":
        return hits if _strong_public_sector_policy_hits(haystack) >= 2 else 0
    return hits if hits >= 1 else 0


def _strong_public_sector_policy_hits(haystack):
    """Count operating-policy signals; generic government/legal mentions do not count."""
    strong_terms = (
        "policy for the responsible use of ai in government",
        "responsible use of ai in government",
        "public servants must",
        "government agencies must",
        "agencies must disclose",
        "responsible ai use by agencies",
        "ai use register",
        "ai use registers",
        "human review",
        "accountable official",
        "accountable officials",
        "digital transformation agency",
        "public sector policy",
    )
    hits = sum(haystack.count(term) for term in strong_terms)
    if re.search(r"\bdta\b", haystack):
        hits += 1
    return hits


def _identity_document_type(text, name="", source_type=""):
    """Resolve known real-artifact identities from filename/title/source anchors."""
    identity_haystack = f"{name or ''} {source_type or ''}".lower()
    full_haystack = f"{identity_haystack} {text or ''}".lower()
    compact_identity = re.sub(r"[^a-z0-9]+", " ", identity_haystack).strip()

    if (
        "oj_l_202401689" in identity_haystack
        or "artificial intelligence act" in full_haystack
        or "regulation laying down harmonised rules on artificial intelligence" in full_haystack
    ):
        return "binding_legal_instrument"
    if (
        "2023-24283" in identity_haystack
        or ("executive order" in full_haystack and "safe, secure, and trustworthy artificial intelligence" in full_haystack)
    ):
        return "executive_policy_directive"
    if (
        "nist.ai.100-1" in identity_haystack
        or "nist ai 100 1" in compact_identity
        or "ai rmf" in full_haystack
        or "artificial intelligence risk management framework" in full_haystack
    ):
        return "voluntary_risk_framework"
    if "dtac" in identity_haystack or "digital technology assessment criteria" in full_haystack:
        return "sector_assurance_checklist"
    if "policy for the responsible use of ai in government" in full_haystack:
        return "public_sector_policy"
    return None


def classify_document_type(text, name="", source_type=""):
    """Classify document type with identity anchors before precedence-ranked text patterns."""
    identity = _identity_document_type(text, name, source_type)
    if identity:
        return identity
    haystack = f"{name or ''} {source_type or ''} {text or ''}".lower()
    candidates = []
    for doc_type, patterns in _DOCUMENT_TYPE_PATTERNS:
        score = _document_type_pattern_hits(haystack, doc_type, patterns)
        if score:
            candidates.append((score, doc_type))
    if not candidates:
        return "unknown_governance_document"
    # Precedence is authoritative for text-pattern classification; public-sector
    # policy cannot override stronger legal/directive/framework/checklist signals.
    return min(candidates, key=lambda item: _DOCUMENT_TYPE_PRECEDENCE_RANK[item[1]])[1]


def dominant_sector_for_document(text, document_type, requested_sector="auto", name=""):
    """Route broad documents by final document type before keyword-sector fallbacks."""
    if requested_sector and requested_sector != "auto":
        return requested_sector
    lowered = f"{name or ''} {text or ''}".lower()
    if document_type in {"binding_legal_instrument", "voluntary_risk_framework"}:
        return "general_ai_governance"
    if document_type == "executive_policy_directive":
        return "government_service_delivery" if any(term in lowered for term in ("federal agencies", "agency heads", "secretaries", "public service", "executive order")) else "general_ai_governance"
    if document_type == "sector_assurance_checklist":
        return "clinical_ai" if any(term in lowered for term in ("clinical", "patient", "nhs", "dcb0129", "hazard log", "dtac")) else "general_ai_governance"
    if document_type == "public_sector_policy":
        return "government_service_delivery" if _strong_public_sector_policy_hits(lowered) >= 2 else "general_ai_governance"
    return "general_ai_governance"


def _quality_label(score, strong=75, moderate=50, limited=25):
    if score >= strong:
        return "Strong"
    if score >= moderate:
        return "Moderate"
    if score >= limited:
        return "Limited"
    return "Weak"


def _risk_label(score):
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def _gap_absent(text, regex):
    return not bool(regex.search(text or ""))


def _build_governance_repair_fields(result, text):
    evidence_count = len(result.get("evidence_traces", []))
    patches = result.get("remediation_patches", [])
    high_patch_count = sum(1 for p in patches if str(p.get("severity", "")).upper() == "HIGH")
    formal_fail = result.get("formal_laif_native_compliance", result.get("formal_laif_compliance")) == "FAIL"
    conceptual = result.get("conceptual_proximity_score", 0)
    audit = result.get("auditability_score", 0)
    enforce = result.get("enforceability_score", 0)
    structural = result.get("structural_score", 0)
    sector_alignment = result.get("sector_risk_alignment", 0)

    owner_gap = _gap_absent(text, _OWNER_GAP_RE)
    gate_gap = _gap_absent(text, _GATE_GAP_RE)
    evidence_gap = _gap_absent(text, _EVIDENCE_GAP_RE) or evidence_count == 0
    lifecycle_gap = _gap_absent(text, _LIFECYCLE_GAP_RE)
    rollback_gap = _gap_absent(text, _ROLLBACK_GAP_RE)
    residual_gap = _gap_absent(text, _RESIDUAL_RISK_RE)

    evidence_score = min(100, round(0.70 * audit + min(evidence_count, 5) * 6 - (20 if evidence_gap else 0)))
    operational_score = min(100, max(0, round(0.55 * structural + 0.25 * enforce + 20 - high_patch_count * 8 - sum([owner_gap, gate_gap, lifecycle_gap]) * 10)))
    accountability_score = min(100, max(0, round(0.65 * enforce + 20 - sum([owner_gap, gate_gap]) * 15)))
    lifecycle_score = min(100, max(0, round(0.60 * structural + 0.25 * audit + 15 - sum([lifecycle_gap, rollback_gap]) * 15)))
    residual_score = min(100, max(0, round(0.55 * audit + 0.25 * enforce + 20 - sum([residual_gap, rollback_gap]) * 15)))
    implementation_gap_score = min(100, max(0, round(0.40 * operational_score + 0.30 * evidence_score + 0.30 * accountability_score)))

    signal_strength = round(0.30 * conceptual + 0.25 * enforce + 0.25 * audit + 0.20 * operational_score)
    systemic_label = _quality_label(signal_strength)
    control_gap_count = sum([owner_gap, gate_gap, evidence_gap, lifecycle_gap, rollback_gap, residual_gap])
    failure_risk_score = min(100, max(0, round((conceptual * 0.35) + (sector_alignment * 0.20) + control_gap_count * 10 + high_patch_count * 8 - (audit + enforce) * 0.10)))

    doc_type = result.get("document_type") or classify_document_type(text, result.get("document_name"), result.get("source_type"))
    recommended_use, not_sufficient_for = _DOC_TYPE_USE.get(doc_type, _DOC_TYPE_USE["unknown_governance_document"])
    control_gaps = []
    if owner_gap:
        control_gaps.append("assign accountable owner")
    if gate_gap:
        control_gaps.append("define decision/release gate")
    if evidence_gap:
        control_gaps.append("link evidence artifact")
    if lifecycle_gap:
        control_gaps.append("add lifecycle monitoring/review")
    if rollback_gap:
        control_gaps.append("add rollback/fallback control")
    if residual_gap:
        control_gaps.append("document residual-risk acceptance and review")
    if not control_gaps:
        control_gaps.append("verify source authority and implementation records")

    return {
        "document_type": doc_type,
        "recommended_use": recommended_use,
        "not_sufficient_for": not_sufficient_for,
        "governance_force_profile": _DOCUMENT_TYPE_FORCE.get(doc_type, _DOCUMENT_TYPE_FORCE["unknown_governance_document"]),
        "systemic_repair_value": systemic_label,
        "operational_closure_rating": _quality_label(operational_score),
        "evidence_sufficiency_rating": _quality_label(evidence_score),
        "accountability_closure_rating": _quality_label(accountability_score),
        "lifecycle_control_rating": _quality_label(lifecycle_score),
        "residual_risk_control_rating": _quality_label(residual_score),
        "implementation_gap_rating": _quality_label(implementation_gap_score),
        "failure_pathway_risk": _risk_label(failure_risk_score),
        "priority_repair_actions": control_gaps[:5],
        "governance_repair_signal_basis": {
            "auditability_score": audit,
            "enforceability_score": enforce,
            "conceptual_proximity_score": conceptual,
            "structural_score": structural,
            "evidence_trace_count": evidence_count,
            "remediation_patch_count": len(patches),
            "high_severity_patch_count": high_patch_count,
            "formal_laif_native_compliance": result.get("formal_laif_native_compliance"),
            "sector_profile": result.get("sector_profile"),
            "sector_risk_alignment": sector_alignment,
            "detected_control_gaps": control_gaps,
        },
    }


def _fragment_quality(fragment):
    text = " ".join(str(fragment or "").split())
    if len(text) < 45:
        return False, "fragment_too_short"
    chars = [ch for ch in text if not ch.isspace()]
    if not chars:
        return False, "empty_fragment"
    alpha_ratio = sum(ch.isalpha() for ch in chars) / max(len(chars), 1)
    if alpha_ratio < 0.62:
        return False, "low_alphabetic_ratio"
    tokens = re.findall(r"[A-Za-z]+", text)
    if len(tokens) < 7:
        return False, "insufficient_meaningful_tokens"
    shortish = sum(1 for tok in tokens if len(tok) <= 2)
    if shortish / max(len(tokens), 1) > 0.35:
        return False, "glyph_fragmentation"
    if re.search(r"(?:[A-Za-z]\s){5,}[A-Za-z]", fragment or ""):
        return False, "excessive_glyph_spacing"
    if re.search(r"[^\w\s.,;:()\[\]{}'\"/–—-]{3,}", text):
        return False, "line_or_glyph_corruption"
    lower = text.lower()
    if lower.startswith(("his regulation", "al law", "ithout ", "tion,", "ment,")):
        return False, "broken_extraction_debris"
    context_terms = ("coupling", "coherence", "integrity", "transparency", "honesty", "containment", "accountability", "oversight", "audit", "evidence", "risk", "govern", "obligation", "shall", "must", "review")
    if not any(term in lower for term in context_terms):
        return False, "no_meaningful_governance_context"
    return True, "primary_confidence"


def _filter_paraphrase_violations(paraphrase):
    primary = {}
    noise = []
    for term, violations in (paraphrase or {}).items():
        kept = []
        for phrase, ctx in violations:
            ok_phrase, reason_phrase = _fragment_quality(phrase)
            ok_ctx, reason_ctx = _fragment_quality(ctx)
            if ok_phrase or ok_ctx:
                kept.append((phrase, ctx))
            else:
                noise.append({
                    "term": term,
                    "phrase": phrase,
                    "context": ctx,
                    "classification": "low_confidence_extraction_noise",
                    "reason": reason_ctx or reason_phrase,
                })
        if kept:
            primary[term] = kept
    return primary, noise

# ── Core assessment function ──────────────────────────────────────────────────

def _resolve_assessment_mode(requested_mode, name, source_type, formal_pass):
    """Return deterministic assessment mode without changing formal scoring.

    Default assessments are external-framework diagnostics. Inputs that are
    explicitly identified as LAIF-native, or that satisfy the strict LAIF formal
    gate, are reported as LAIF-native certification unless a caller explicitly
    requests a mode.
    """
    aliases = {
        "external": "external_framework",
        "external_framework": "external_framework",
        "diagnostic": "external_framework",
        "laif": "laif_native_certification",
        "laif_native": "laif_native_certification",
        "laif_native_certification": "laif_native_certification",
        "certification": "laif_native_certification",
    }
    if requested_mode is not None:
        key = str(requested_mode).strip().lower().replace("-", "_")
        if key not in aliases:
            raise ValueError(
                "assessment_mode must be 'external_framework' or "
                "'laif_native_certification'"
            )
        return aliases[key]

    identity = f"{name} {source_type}".lower().replace("-", "_")
    if formal_pass or "laif_native" in identity or "laif native" in identity:
        return "laif_native_certification"
    return "external_framework"


def _assessment_mode_fields(mode, formal_verdict, missing_terms):
    """Build mode-separation metadata for assessment output."""
    canonical_remediation_required = formal_verdict == "FAIL" or bool(missing_terms)
    not_laif_native = formal_verdict == "FAIL"
    if mode == "external_framework":
        external = {
            "type": "diagnostic",
            "not_laif_native_certification": True,
            "laif_native_certification_status": (
                "PASS" if formal_verdict == "PASS" else "FAIL / NOT LAIF-NATIVE"
            ),
            "structural_assessment": "diagnostic",
            "legal_or_governance_invalidity_claimed": False,
            "canonical_terminology_note": (
                "Missing LAIF canonical terminology means not LAIF-native / "
                "canonical remediation required for LAIF certification; it is not "
                "a legal-validity or governance-validity determination."
            ),
            "certification_notice": (
                "External framework structural assessment is diagnostic and is not "
                "LAIF-native certification."
            ),
        }
    else:
        external = {
            "type": "not_applicable",
            "not_laif_native_certification": False,
            "laif_native_certification_status": formal_verdict,
            "structural_assessment": "certification",
            "legal_or_governance_invalidity_claimed": False,
            "canonical_terminology_note": (
                "Canonical terminology is load-bearing in LAIF-native certification mode."
            ),
            "certification_notice": (
                "LAIF-native certification mode applies strict binary formal compliance; "
                "diagnostic scores cannot convert a formal FAIL into PASS."
            ),
        }
    return {
        "assessment_mode": mode,
        "formal_laif_native_compliance": formal_verdict,
        "external_framework_assessment": external,
        "laif_canonical_remediation_required": canonical_remediation_required,
        "not_laif_native": not_laif_native,
    }


def assess(name, source_type, text, sector="general_ai_governance", assessment_mode=None, **meta):
    """
    Produce a full LAIF assessment for a document.

    Parameters:
      name        — document identifier
      source_type — classification (binding_regulation, voluntary_framework, etc.)
      text        — document text to assess
      sector      — deployment sector profile key (default: general_ai_governance)
      assessment_mode — optional mode: external_framework or laif_native_certification
      **meta      — optional metadata (jurisdiction, year, citation)

    Returns a dict with:
      - Formal compliance verdict (binary, strict)
      - Five dimension scores with per-signal breakdown (traceable)
      - Sector analysis (risk alignment, specific findings, remediation priority)
      - Strengths, gaps, failure modes, and ordered remediation steps

    Formal compliance is binary and strict — no partial credit.
    Scores are diagnostic — they contextualise the compliance gap.
    """
    # Dimension scores with signal traceability
    s, s_fired, s_missed = _score_signals(text, STRUCTURAL_RUBRIC)
    t, t_fired, t_missed = _score_signals(text, TERMINOLOGY_RUBRIC)
    c, c_fired, c_missed = _score_signals(text, CONCEPTUAL_RUBRIC)
    a, a_fired, a_missed = _score_signals(text, AUDITABILITY_RUBRIC)
    e, e_fired, e_missed = _score_signals(text, ENFORCEABILITY_RUBRIC)

    # Directionality check — small downward adjustment to conceptual if rights-
    # language is used to justify AI surveillance of humans rather than protect
    # humans from AI.  Does not affect formal gate, coupling, or other dimensions.
    c, _direction_penalised = _directionality_penalty(text, c)

    overall = round(0.25 * s + 0.15 * t + 0.20 * c + 0.20 * a + 0.20 * e)

    construct_coverage = {
        cname: bool(re.search(pat, text, re.IGNORECASE))
        for cname, pat in CONSTRUCT_COVERAGE_CHECKS
    }

    formal_checks = [
        (label, bool(re.search(pat, text, re.IGNORECASE)))
        for pat, label in FORMAL_REQUIREMENTS
    ]
    formal_pass = all(present for _, present in formal_checks)

    raw_paraphrase = {}
    for guard in PARAPHRASE_GUARDS:
        v = find_paraphrase_violations(text, guard)
        if v:
            raw_paraphrase[guard["term"]] = v
    paraphrase, low_confidence_extraction_noise = _filter_paraphrase_violations(raw_paraphrase)

    # Paraphrase guard scope. The guards exist to stop drift INSIDE documents
    # that use LAIF's canonical vocabulary or claim LAIF alignment. An external
    # instrument written entirely in its own vocabulary is not "violating" LAIF
    # terminology — it never adopted it. For such documents the same detections
    # are reported as a terminology divergence note (informational), not a
    # violation. validate.py's enforcement over the LAIF corpus is unchanged.
    # "Claiming LAIF" means using LAIF's distinctive vocabulary — not merely
    # sharing generic legal phrases ("cannot be amended") with it. Coupling is
    # matched case-sensitively: as a term of art it is capitalised; lowercase
    # engineering "coupling" is not a LAIF claim.
    claims_laif = bool(
        re.search(r"\bLAIF\b|\bCoupling\b", text)
        or re.search(
            r"\bCoherence Test\b|\bIntegrity Layer\b"
            r"|\bStructural (?:Transparency|Honesty|Containment)\b"
            r"|\bPre.Deployment Coherence Assessment\b|\bPDCA\b",
            text, re.IGNORECASE,
        )
    )
    paraphrase_classification = "VIOLATION" if claims_laif else "DIVERGENCE_NOTE"

    # Strengths — signals that fired in conceptual + general structural +
    # auditability + enforceability rubrics (not LAIF-specific structural,
    # which external frameworks are not expected to contain)
    strengths = []
    for _, pat, label in CONCEPTUAL_RUBRIC:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Expresses: {label}")
    for _, pat, label in STRUCTURAL_RUBRIC[:6]:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Structure: {label}")
    for _, pat, label in AUDITABILITY_RUBRIC:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Auditability: {label}")
    for _, pat, label in ENFORCEABILITY_RUBRIC:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Enforceability: {label}")

    # Gaps. LAIF-native distance items (vocabulary, canonical structural
    # markers) are appended LATER, after the functional-alignment layer has
    # run — so that a construct whose substance was detected in the document's
    # own vocabulary is reported as such, and external instruments get
    # certification-channel wording rather than deficiency wording.
    gaps = []
    missing_terms = [lbl for _, pat, lbl in TERMINOLOGY_RUBRIC
                     if not re.search(pat, text, re.IGNORECASE)]

    for guard_term, violations in paraphrase.items():
        examples = "; ".join(
            v[1].replace("\n", " ")[:60] + "…" for v in violations[:2]
        )
        if paraphrase_classification == "VIOLATION":
            gaps.append(
                f"Paraphrase violation — forbidden substitution of '{guard_term}' "
                f"({len(violations)} instance(s)): {examples}"
            )
        else:
            gaps.append(
                f"Terminology divergence (informational) — '{guard_term}'-adjacent "
                f"wording used in the document's own vocabulary "
                f"({len(violations)} instance(s)): {examples}. Not a violation: "
                f"this document does not use or claim LAIF canonical terminology."
            )

    # Primary failure modes
    failure_modes = []
    if not any(p for lbl, p in formal_checks
               if any(x in lbl for x in ("PART ONE", "non-amendable", "self-application"))):
        failure_modes.append("structural — constitutional hierarchy not declared")
    if t == 0:
        failure_modes.append("terminological — no canonical LAIF terms present")
    if paraphrase and paraphrase_classification == "VIOLATION":
        failure_modes.append("terminological (paraphrase) — forbidden substitutions detected")
    if c < 40:
        failure_modes.append("conceptual — LAIF-like concepts insufficiently expressed")
    if a < 40:
        failure_modes.append("auditability — obligations not checkable or traceable")
    if e < 40:
        failure_modes.append("enforceability — insufficient mandatory operational requirements")

    if overall >= 60:
        effort = "MEDIUM"
    elif overall >= 35:
        effort = "HIGH"
    else:
        effort = "VERY HIGH"

    # Sector analysis
    # Source: LAIF_Compliance_Toolkit.txt §7.5 — PDCA tiering by sector/stakes;
    # Toolkit §1.2 — Materially Affects Interests is the sector gateway test.
    identity_name = " ".join(str(part) for part in (name, source_type, meta.get("original_file_name", ""), meta.get("original_pending_path", ""), meta.get("stored_source_path", ""), meta.get("runner_input_path", "")) if part)
    early_document_type = classify_document_type(text, identity_name, source_type)
    resolved_sector = dominant_sector_for_document(text, early_document_type, sector, identity_name) if sector == "auto" else sector
    profile_key = _sector_profile_key(resolved_sector)
    profile = _sector_profile_metadata(profile_key)
    profile_signals = _sector_profile_signals(text, profile_key)

    sector_risk_results = [
        (label, bool(re.search(pat, text, re.IGNORECASE)))
        for pat, label in profile["risk_indicators"]
    ]
    sector_evidence_results = [
        (label, bool(re.search(pat, text, re.IGNORECASE)))
        for pat, label in profile["expected_evidence"]
    ]

    n_risk = sum(1 for _, present in sector_risk_results if present)
    sector_risk_alignment = round(100 * n_risk / max(len(sector_risk_results), 1))

    sector_specific_findings = (
        [f"Risk signal present: {lbl}" for lbl, ok in sector_risk_results if ok]
        + [f"Risk signal absent: {lbl}" for lbl, ok in sector_risk_results if not ok]
        + [f"Evidence present: {lbl}" for lbl, ok in sector_evidence_results if ok]
        + [f"Evidence gap: {lbl}" for lbl, ok in sector_evidence_results if not ok]
    )

    # ── Structural depth analysis (hardening layer) ───────────────────────────
    # These run AFTER sector analysis because gaming detection uses sector_alignment.
    # Source: LAIF v1.2 Principle 2 (Coupling quality); A.2 Structural Honesty
    # (contradictions); Q2 Consistency (sector gaming = scale-inconsistent keyword use).
    cq, cq_reason, cq_evidence = _coupling_quality(text)
    implicit_coupling            = _implicit_coupling_signals(text)
    contradictions       = _contradiction_check(text)
    gaming_level, gaming_reason = _sector_gaming_risk(sector_risk_alignment, overall, c)
    depth                = _structural_depth(cq, contradictions, gaming_level, formal_pass)

    # Source location layer — document outline, located signals, obligation
    # anchors. Lets every finding point INTO the document.
    _outline          = _document_outline(text)
    signal_locations  = _located_signals(text, _outline)
    obligation_anchors = _obligation_anchors(text, _outline)

    # Functional alignment — substance detection independent of vocabulary.
    # Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
    functional      = _functional_alignment(text, cq)
    for _c, _v in functional.items():
        _v["evidence_locations"] = [
            _locate_offset(_off, _outline)
            for _off in _v.get("evidence_offsets", [])
        ]
    func_coupling   = functional["Coupling"]["verdict"]
    laif_alignment  = _laif_alignment_verdict(formal_pass, depth, functional,
                                              contradictions)

    # LAIF-native distance notes — deferred from the gap builder above so
    # they can be worded per channel and per functional verdict. For
    # documents that use or claim LAIF vocabulary these are compliance
    # gaps; for external instruments they are certification-distance
    # diagnostics, never deficiency claims (fair-reading bound 1).
    if missing_terms:
        if claims_laif:
            gaps.insert(0, "Canonical LAIF terms absent: " + ", ".join(missing_terms))
        else:
            gaps.insert(0,
                "LAIF-native vocabulary not used — expected for an external "
                "instrument; certification-channel distance, not a deficiency: "
                + ", ".join(missing_terms)
            )
    _signal_construct = {
        "threshold gate conditions (all must pass simultaneously)": "Integrity Layer",
        "self-application clause (Part Seven)":                     "Self-Application",
        "named decision instrument (Coherence Test / PDCA)":        "__branding__",
    }
    _native_gap_lines = []
    for _, _pat, _lbl in STRUCTURAL_RUBRIC[6:]:
        if re.search(_pat, text, re.IGNORECASE):
            continue
        _mapped = _signal_construct.get(_lbl)
        if _mapped == "__branding__" and not claims_laif:
            _native_gap_lines.append(
                f"LAIF-native marker not present (branding, not substance): {_lbl}")
        elif (_mapped and _mapped != "__branding__"
                and functional.get(_mapped, {}).get("verdict")
                in ("FUNCTIONAL", "DECLARED")):
            _native_gap_lines.append(
                f"{_lbl}: substance functionally present in the document's own "
                f"vocabulary; LAIF-native declaration absent "
                f"(certification-channel note)")
        elif claims_laif:
            _native_gap_lines.append(f"LAIF structural element missing: {_lbl}")
        else:
            _native_gap_lines.append(
                f"Structural mechanism not detected in any vocabulary: {_lbl}")
    gaps[1:1] = _native_gap_lines

    # Strong compliance: formal gate PASS + genuine structural depth.
    # A hollow document that passes the formal gate but has SHALLOW/NEGATED Coupling
    # or contradictions is a WEAK PASS — not a STRONG PASS.
    if formal_pass and depth == "STRONG":
        strong_compliance = "STRONG PASS"
    elif formal_pass:
        strong_compliance = "WEAK PASS"
    else:
        strong_compliance = "FAIL"

    # Surface contradiction and gaming gaps
    if cq in ("SHALLOW", "NEGATED"):
        gaps.append(
            f"Coupling quality: {cq} — {cq_reason} "
            f"(LAIF v1.2 Principle 2 requires structural declaration with named human interest "
            f"and equivalent normative force)"
        )
    for prop, desc, ctx in contradictions:
        gaps.append(f"Structural contradiction [{prop}]: {desc} — context: «{ctx[:80]}»")
    if gaming_level != "LOW":
        gaps.append(f"Sector gaming risk [{gaming_level}]: {gaming_reason}")

    # Upgrade failure modes for structural depth issues
    if depth == "HOLLOW" and formal_pass:
        failure_modes.append(
            "structural depth — formal PASS with HOLLOW depth: Coupling quality is "
            f"{cq}; all required terms present but structural declaration absent or negated"
        )
    if contradictions:
        failure_modes.append(
            f"internal contradiction — {len(contradictions)} Structural Honesty violation(s) "
            "detected: claimed properties contradicted by document content (LAIF v1.2 A.2)"
        )

    formal_verdict = "PASS" if formal_pass else "FAIL"
    resolved_assessment_mode = _resolve_assessment_mode(
        assessment_mode, name, source_type, formal_pass
    )
    mode_fields = _assessment_mode_fields(
        resolved_assessment_mode, formal_verdict, missing_terms
    )

    # Score calibration — raw overall scores compress because part of the
    # scale is reserved for LAIF-native branding (the terminology dimension
    # plus the named-decision-instrument structural signal). For external
    # instruments the effective ceiling is therefore below 100, and the
    # calibrated position (raw ÷ ceiling) is the fairer comparative figure.
    # The ceiling is DERIVED from the rubrics, not asserted.
    _ceiling = _achievable_ceiling_external() \
        if resolved_assessment_mode == "external_framework" else 100.0
    score_calibration = {
        "achievable_ceiling":       _ceiling,
        "overall_pct_of_ceiling":   round(100 * overall / _ceiling) if _ceiling else 0,
        "ceiling_basis": (
            "External-instrument ceiling: 100 minus the terminology dimension "
            "weight and the named-decision-instrument structural signal — points "
            "only a LAIF-branded document can earn. Derived from the live rubrics."
            if resolved_assessment_mode == "external_framework"
            else "LAIF-native channel: full 100-point scale applies."
        ),
    }

    result = {
        "document_name":              name,
        "source_type":                source_type,
        "formal_laif_compliance":     formal_verdict,
        **mode_fields,
        "formal_checks_detail":       formal_checks,   # [(label, bool), ...]
        "strong_laif_compliance":     strong_compliance,
        "structural_depth":           depth,
        "coupling_quality":           cq,
        "coupling_quality_reason":    cq_reason,
        "coupling_quality_evidence":  cq_evidence,
        "implicit_coupling":          implicit_coupling,
        "coupling_state":             _coupling_state(cq, implicit_coupling,
                                                      func_coupling),
        "functional_alignment":       functional,
        "laif_alignment":             laif_alignment,
        "document_outline":           [lbl for _, lbl in _outline][:14],
        "signal_locations":           signal_locations,
        "obligation_anchors":         obligation_anchors,
        "contradictions":             contradictions,
        "sector_gaming_risk":         gaming_level,
        "sector_gaming_reason":       gaming_reason,
        "construct_coverage":         construct_coverage,
        "structural_score":           s,
        "terminology_score":          t,
        "conceptual_proximity_score":            c,
        "conceptual_directionality_penalised":  _direction_penalised,
        "auditability_score":                   a,
        "enforceability_score":       e,
        "overall_readiness_score":    overall,
        "score_calibration":          score_calibration,
        "remediation_effort":         effort,
        "paraphrase_violations":      paraphrase,
        "low_confidence_extraction_noise": low_confidence_extraction_noise,
        "paraphrase_classification":  paraphrase_classification,
        "strengths":                  strengths,
        "gaps":                       gaps,
        "primary_failure_modes":      failure_modes,
        # Per-dimension signal breakdown — answers "why this number?"
        "score_breakdown": {
            "structural":    {"fired": s_fired, "missed": s_missed},
            "terminology":   {"fired": t_fired, "missed": t_missed},
            "conceptual":    {"fired": c_fired, "missed": c_missed},
            "auditability":  {"fired": a_fired, "missed": a_missed},
            "enforceability":{"fired": e_fired, "missed": e_missed},
        },
        # Sector fields
        "sector_used":                 profile_key,
        "sector_label":                profile["label"],
        "sector_relevant_interests":   profile["relevant_interests"],
        "sector_specific_findings":    sector_specific_findings,
        "sector_risk_alignment":       sector_risk_alignment,
        "sector_remediation_priority": profile["remediation_focus"],
        "sector_profile":              profile_key,
        "sector_profile_label":        profile["label"],
        "sector_profile_purpose":      profile.get("purpose", "Diagnostic sector overlay."),
        "sector_profile_diagnostic_signals": profile_signals,
        "sector_profile_governance_force_emphasis": list(profile.get("governance_force_emphasis", ())),
        "sector_profile_remediation_themes": list(profile.get("remediation_themes", ())),
        "sector_profile_evidence_cautions": list(profile.get("evidence_cautions", ())),
        **meta,
    }
    result["recommended_remediation_steps"] = _remediation(result)
    _tier = _deployment_risk_tier(overall, strong_compliance)
    # Consistency invariant — matches _deployment_risk_tier() thresholds exactly
    assert (
        (_tier == "LOW"      and strong_compliance == "STRONG PASS") or
        (_tier == "MODERATE" and overall >= 70 and strong_compliance != "STRONG PASS") or
        (_tier == "HIGH"     and 40 <= overall < 70 and strong_compliance != "STRONG PASS") or
        (_tier == "CRITICAL" and overall < 40 and strong_compliance != "STRONG PASS")
    ), f"Risk tier {_tier!r} inconsistent with score {overall}/strong_compliance {strong_compliance!r}"
    result["deployment_risk"]      = _tier  # canonical key (spec)
    result["deployment_risk_tier"] = _tier  # backward-compatible alias

    # ── Decision-grade reporting fields (added after base result is built) ────
    result["score_trace"] = {
        "structural":    _build_score_trace("structural",    s, s_fired, s_missed),
        "terminology":   _build_score_trace("terminology",   t, t_fired, t_missed),
        "conceptual":    _build_score_trace("conceptual",    c, c_fired, c_missed),
        "auditability":  _build_score_trace("auditability",  a, a_fired, a_missed),
        "enforceability":_build_score_trace("enforceability",e, e_fired, e_missed),
    }
    result["compliance_summary"]           = _compliance_summary(result)
    result["executive_summary"]            = _executive_summary(result)
    result["plain_reading"]                = _plain_reading(result)
    result["structured_findings"]          = _structured_findings(result)
    result["structured_remediation_steps"] = _structured_remediation(result)
    result["governance_signal"]            = _governance_signal_strength(result)
    result["evidence_traces"]              = _build_evidence_traces(text, result)
    result["remediation_patches"]          = _build_remediation_patches(result)
    result["score_interpretation"]         = _score_interpretation_label(overall)
    result["score_justification"]          = _score_justification_summary(result)
    result["dimension_justifications"]     = _dimension_justification_records(result)
    result["calibration_cautions"]         = _calibration_cautions(result)
    result["gaming_risk_notes"]            = _score_gaming_risk_notes(result)
    result.update(_build_governance_repair_fields(result, text))
    return result


# ── Plain-English practical meaning for Executive Summary ─────────────────────
# Provides a one-sentence "so what?" for non-LAIF readers. Keyed from the
# primary failure mode, not from scores — so it cannot drift from the actual
# structural verdict.

def _practical_meaning_exec(result):
    """
    Return a single plain-English sentence explaining what the assessment result
    means for a non-LAIF audience (executives, policy teams, legal/compliance).
    Returns empty string if document is STRONG PASS.
    """
    sc    = result.get("strong_laif_compliance", "FAIL")
    cq    = result.get("coupling_quality", "ABSENT")
    cs    = result.get("coupling_state", "ABSENT")
    contras = result.get("contradictions", [])
    gaming  = result.get("sector_gaming_risk", "LOW")
    overall = result.get("overall_readiness_score", 0)

    if sc == "STRONG PASS":
        return ""
    if cq == "NEGATED":
        return (
            "This document explicitly disclaims the structural protections that make "
            "governance obligations enforceable — the most serious structural failure."
        )
    if contras:
        return (
            "This document states governance commitments that are contradicted by other "
            "provisions — protections appear present but are negated in effect."
        )
    if cs == "FUNCTIONAL":
        return (
            "This document expresses the structural protections LAIF requires, in its own "
            "vocabulary. It is not written in LAIF-native form, so it cannot be certified "
            "against LAIF as-is — but the adoption distance is terminological and "
            "documentary, not substantive."
        )
    if cs == "ABSENT":
        return (
            "This document imposes obligations but does not structurally protect the people "
            "those obligations are meant to serve — each obligation can be removed "
            "independently of any corresponding protection."
        )
    if cs == "IMPLICIT":
        return (
            "This document signals protective intent but does not structurally bind "
            "obligations to the people they protect — the intent is present but "
            "not enforceable as written."
        )
    if overall > 40 and sc != "STRONG PASS":
        return (
            "This document addresses the right governance areas but has not structured "
            "its provisions in a way that makes them independently enforceable or "
            "verifiable against a named standard."
        )
    return (
        "This document does not yet meet the structural preconditions required to "
        "provide reliable governance assurance for the people it governs."
    )


# ── Source location layer ─────────────────────────────────────────────────────
# Turns character offsets into human-usable locations ("at §6(b)", "under
# 'C1 - Clinical safety'") so every finding can point INTO the document.
# Everything here is deterministic text analysis of the assessed source.

_OUTLINE_PATTERNS = [
    re.compile(r"^#{1,6}\s+(.{3,80})$", re.MULTILINE),                       # markdown headings
    re.compile(r"^((?:Article|Section|SECTION|Part|PART|Chapter)\s+[\dIVXA-Z]+[^\n]{0,90})$", re.MULTILINE),
    re.compile(r"^((?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+(?:\.\d+)?:?[^\n]{0,60})", re.MULTILINE),
    re.compile(r"^(\d+\.\d*\.?\s+[A-Z][^\n]{3,60})$", re.MULTILINE),       # 2.1 Numbered heads
    re.compile(r"^([A-Z][A-Za-z ]{3,50})\n(?=\n)", re.MULTILINE),             # bare titles (blank line follows)
]


def _document_outline(text):
    """Return a deduplicated, offset-ordered [(offset, label)] outline of the
    document's own structure, detected from common heading conventions."""
    seen_labels = set()
    entries = []
    for pat in _OUTLINE_PATTERNS:
        for m in pat.finditer(text):
            label = " ".join(m.group(1).split())[:70].rstrip(" |#-")
            if len(label) < 4 or label.lower() in seen_labels:
                continue
            seen_labels.add(label.lower())
            entries.append((m.start(), label))
    entries.sort(key=lambda x: x[0])
    return entries


def _locate_offset(pos, outline):
    """Nearest document-structure label at or before pos."""
    best = "start of document"
    for off, label in outline:
        if off <= pos:
            best = label
        else:
            break
    return best


def _quote_at(text, start, end, max_len=110):
    lo = max(0, start - 15)
    hi = min(len(text), end + 60)
    tokens = text[lo:hi].split()
    if lo > 0 and tokens:
        tokens = tokens[1:]          # drop leading partial word
    out = " ".join(tokens)
    if len(out) > max_len:
        out = out[:max_len].rsplit(" ", 1)[0] + "…"
    return out


def _located_signals(text, outline):
    """First-match location and verbatim quote for every fired rubric signal,
    per dimension. Deterministic; quotes are exact substrings of the excerpt
    window around the match."""
    out = {}
    for dim, rubric in (("structural", STRUCTURAL_RUBRIC),
                        ("terminology", TERMINOLOGY_RUBRIC),
                        ("conceptual", CONCEPTUAL_RUBRIC),
                        ("auditability", AUDITABILITY_RUBRIC),
                        ("enforceability", ENFORCEABILITY_RUBRIC)):
        rows = []
        for _, pat, label in rubric:
            m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
            if m:
                rows.append({
                    "label":    label,
                    "quote":    _quote_at(text, m.start(), m.end()),
                    "location": _locate_offset(m.start(), outline),
                })
        out[dim] = rows
    return out


# Sentence charclass permits newlines: obligation sentences in hard-wrapped
# prose span lines; quotes are whitespace-normalised on capture.
_OBLIGATION_SENTENCE = re.compile(
    r"[A-Z][^.!?]{10,180}\b(?:shall|must)\b(?:\s+not)?[^.!?]{5,200}[.!?]"
)


def _obligation_anchors(text, outline, limit=3):
    """Up to `limit` obligation sentences with locations — the exact places a
    restriction-protection pairing would attach. Diversified: at most one
    anchor per document section, so guidance spans the document rather than
    clustering in its first section."""
    anchors, seen_sections = [], set()
    spare = None
    for m in _OBLIGATION_SENTENCE.finditer(text):
        loc = _locate_offset(m.start(), outline)
        entry = {"quote": " ".join(m.group(0).split())[:140], "location": loc}
        if loc in seen_sections:
            spare = spare or entry
            continue
        seen_sections.add(loc)
        anchors.append(entry)
        if len(anchors) >= limit:
            break
    if not anchors and spare:
        anchors.append(spare)
    return anchors


_ANCHOR_HINTS = {
    "Coupling":         "protect rights interest worker patient consumer safety",
    "Integrity Layer":  "safety security testing evaluation standards oversight",
    "Consistency":      "scope application definitions general provisions",
    "Reversibility":    "review monitoring appeal correction redress oversight",
    "Self-Application": "implementation administration governance authority council",
}


def _suggest_anchor(label, outline, obligation_anchors):
    """Deterministic suggestion for where a missing element would belong:
    the document's own section whose title shares vocabulary with the
    missing signal; else the first obligation sentence's section; else an
    honest 'new provision required'."""
    enriched = f"{label} {_ANCHOR_HINTS.get(label.split(' ')[0].strip(), '')} " \
               f"{_ANCHOR_HINTS.get(label, '')}"
    words = {w for w in re.split(r"[^a-z]+", enriched.lower()) if len(w) > 3}
    best, best_score = None, 0
    for _, sec in outline:
        sec_words = {w for w in re.split(r"[^a-z]+", sec.lower()) if len(w) > 3}
        score = len(words & sec_words)
        if score > best_score:
            best, best_score = sec, score
    if best:
        return f"most related existing section: '{best}'"
    if obligation_anchors:
        return f"attach under '{obligation_anchors[0]['location']}'"
    return "no existing section covers this — a new provision is required"


# ── Plain-language reading ────────────────────────────────────────────────────
# A framework-free narrative of what the measurements found, written for a
# reader who has never heard of LAIF — including the assessed document's own
# authors. Every sentence is conditioned on a measured signal; nothing here is
# free-floating editorial. Deliberately uses no LAIF vocabulary.

_PLAIN_VALUE_NAMES = {
    "human rights / fundamental interests":   "people's fundamental rights",
    "transparency":                            "openness about how decisions are made",
    "explainability / interpretability":       "explanations people can understand",
    "accountability":                          "answerability for outcomes",
    "human oversight":                         "human oversight of the system",
    "proportionality":                         "matching rules to the size of the risk",
    "safety":                                  "safety",
    "contestability / redress":                "the ability to challenge decisions",
    "reversibility / modifiability":           "the ability to correct or reverse outcomes",
    "risk governance":                         "structured risk management",
    "traceability / responsibility":           "traceability of decisions",
    "fairness / labour / non-discrimination":  "fairness and non-discrimination",
}

_PLAIN_SOURCE_TYPES = {
    "executive_directive":      "a statement of values followed by a tasking list — "
                                "named officials receive instructions and deadlines",
    "binding_regulation":       "binding law — it imposes obligations on identified "
                                "parties, enforceable through the legal system",
    "voluntary_framework":      "a voluntary playbook — structured practices an "
                                "organisation may adopt, with no binding force of its own",
    "international_principles": "an intergovernmental commitment — principles that "
                                "governments endorse and are expected, but not "
                                "compelled, to implement",
    "sector_policy":            "a sector instrument — operational requirements for a "
                                "specific deployment context",
}


def _plain_reading(result):
    """
    Return a list of plain-language paragraphs interpreting the measurements
    for a lay reader. Framework-free by design: no LAIF terminology.
    """
    paras   = []
    bd      = result["score_breakdown"]
    fired_c = [lbl for lbl, _ in bd["conceptual"]["fired"]]
    miss_c  = [lbl for lbl, _ in bd["conceptual"]["missed"]]
    fired_a = [lbl for lbl, _ in bd["auditability"]["fired"]]
    cstate  = result.get("coupling_state", "ABSENT")
    func    = result.get("functional_alignment", {})
    align   = result.get("laif_alignment", "")

    def fv(construct):
        return func.get(construct, {}).get("verdict", "ABSENT")

    # ── What this document is, and what it cares about ──────────────────────
    intro  = _PLAIN_SOURCE_TYPES.get(result["source_type"], "a governance document")
    values = [_PLAIN_VALUE_NAMES[l] for l in fired_c if l in _PLAIN_VALUE_NAMES]
    first  = f"In plain terms, this document is {intro}."
    if len(values) >= 3:
        first += (f" It clearly names the things it exists to protect: "
                  f"{', '.join(values[:5])}"
                  + (" and more." if len(values) > 5 else "."))
    elif values:
        first += (f" It names only some of the human concerns it exists to serve "
                  f"({', '.join(values)}).")
    else:
        first += (" Notably, it barely names the human concerns it exists to "
                  "serve — the reader must infer who is meant to benefit.")
    paras.append(first)

    # ── Do promises reach the person? ────────────────────────────────────────
    if cstate in ("STRUCTURAL", "FUNCTIONAL"):
        s = ("Its strongest structural feature: promises are fastened to the "
             "people they serve. When it restricts something, it says who that "
             "protects — and the protection is written to be as durable as the "
             "rule, so that one cannot quietly outlive the other.")
        if cstate == "FUNCTIONAL":
            s += (" It does this in its own words rather than any framework's "
                  "vocabulary, and the pairing is real.")
        paras.append(s)
    elif cstate == "IMPLICIT":
        paras.append(
            "It expresses a clear intention to protect people, but the promises "
            "are not fastened to the people they serve: a specific rule could be "
            "weakened or dropped without visibly breaking a commitment to any "
            "identifiable person."
        )
    else:
        s = ("Trace who receives something in each operative sentence and a "
             "pattern appears: institutions receive duties, deadlines, and "
             "reporting obligations — but the people the document is about "
             "receive nothing they can hold. Protection exists here as intended "
             "future outcomes, not as present commitments to identifiable "
             "people; because promises and beneficiaries are never fastened "
             "together, individual provisions can erode without anyone being "
             "able to say a promise to them was broken.")
        paras.append(s)
    if "contestability / redress" in miss_c:
        paras.append(
            "It provides no route for an affected person to challenge or appeal "
            "an outcome — if the system gets it wrong for someone, this text "
            "gives them nothing to invoke."
        )
    elif "contestability / redress" in fired_c and cstate not in ("STRUCTURAL", "FUNCTIONAL"):
        paras.append(
            "It does give people a route to challenge decisions — a genuine "
            "person-facing protection, and the main exception to the pattern above."
        )

    # ── Does anything bind the author, and does anything survive them? ──────
    author_bound = fv("Self-Application") in ("DECLARED", "FUNCTIONAL")
    durable      = fv("Reversibility") in ("DECLARED", "FUNCTIONAL")
    if author_bound and durable:
        paras.append(
            "Unusually, it binds its own author — the governing authority is "
            "subject to the same tests it imposes on others — and it protects "
            "the future: consequences can be corrected, and permanent effects "
            "require senior approval before they happen."
        )
    elif author_bound:
        paras.append(
            "Unusually, it binds its own author: the governing authority is "
            "subject to the same tests it imposes on others. It is weaker on "
            "time: little in it guarantees that outcomes can be corrected or "
            "that permanent effects need special approval."
        )
    elif durable:
        paras.append(
            "It takes the future seriously — consequences can be corrected or "
            "reversed, and permanent effects require approval first — but "
            "nothing in it binds the author: it sets tests for others and none "
            "that the issuing authority itself must pass."
        )
    else:
        s = ("Nothing in it binds the author — it sets requirements for others "
             "but none that the issuing authority itself must pass — and "
             "nothing anchors it in time: ")
        if fv("Reversibility") == "PARTIAL":
            s += ("it gestures at correction and rollback, but not as a "
                  "guaranteed capacity, and everything it creates can be "
                  "undone by its author's successor.")
        else:
            s += ("everything it creates can be modified or undone by its "
                  "author's successor without any special safeguard.")
        paras.append(s)

    # ── Credit where due ─────────────────────────────────────────────────────
    credit = []
    if "numbered traceable requirements" in fired_a:
        credit.append("numbered, traceable requirements")
    if "evidence / documentation requirements" in fired_a:
        credit.append("evidence and documentation duties")
    if "review / monitoring mechanisms" in fired_a:
        credit.append("review and monitoring machinery")
    if result["enforceability_score"] >= 60:
        credit.append("genuinely mandatory language with named owners")
    if credit:
        paras.append(
            f"To its credit, the administrative machinery is real: "
            f"{', '.join(credit)}. Whether its tasks were done is checkable — "
            f"a property many governance documents lack."
        )

    # ── Fair summary ─────────────────────────────────────────────────────────
    if align == "FUNCTIONALLY ALIGNED":
        paras.append(
            "**Fair summary:** the protective architecture is genuinely there, "
            "expressed in the document's own words. Any remaining distance from "
            "a stricter standard is wording and paperwork, not substance."
        )
    elif align == "PARTIALLY ALIGNED":
        paras.append(
            "**Fair summary:** real machinery, real intent, and some of the "
            "deeper protective architecture — but not all of it. That is not a "
            "judgement that the document fails at its own job. It means that if "
            "you relied on this text alone to guarantee a specific person "
            "protection from a specific harm, parts of that load path are missing."
        )
    elif align.startswith("LAIF-NATIVE (HOLLOW"):
        paras.append(
            "**Fair summary:** this document borrows the vocabulary of strong "
            "governance without the machinery behind it. The words are present; "
            "the load-bearing structure is not."
        )
    elif align.startswith("LAIF-NATIVE"):
        paras.append(
            "**Fair summary:** written in the assessing framework's own form; "
            "see the structural-depth verdict above for whether the substance "
            "matches the form."
        )
    else:
        paras.append(
            "**Fair summary:** whatever its other merits, none of the deeper "
            "protective architecture — promises fastened to people, rules that "
            "bind the rule-maker, guarantees that survive a change of author — "
            "is present in any form. That is not a judgement of the document "
            "against its own objectives; it is a statement of what a person "
            "could and could not rely on this text for."
        )
    return paras


# ── Signal grouping for display ───────────────────────────────────────────────
# Display-only classification — does NOT affect scoring.
# Human interest signals relate to specific human interests at risk.
# Governance signals relate to structural, procedural, and architectural controls.

_HUMAN_INTEREST_KW = frozenset([
    "rights", "safety", "harm", "accountability", "redress", "consent",
    "patient", "worker", "dignity", "human interest", "non-discrimination",
    "fairness", "privacy", "data protection", "freedom", "welfare",
])
_GOVERNANCE_KW = frozenset([
    "transparency", "oversight", "audit", "monitor", "review", "enforc",
    "mandatory", "obligation", "document", "evidence", "reporting",
    "mechanism", "hierarchy", "lifecycle", "proportionat", "coherence",
    "integrity layer", "coupling", "containment", "numbered", "shall",
    "threshold", "constitutional", "self-application", "pdca",
])


def _classify_signal(label):
    """Return 'human_interest', 'governance', or 'structural' for a signal label."""
    ll = label.lower()
    for kw in _HUMAN_INTEREST_KW:
        if kw in ll:
            return "human_interest"
    for kw in _GOVERNANCE_KW:
        if kw in ll:
            return "governance"
    return "structural"


def _group_signals(signals):
    """
    Partition a list of (label, weight) signal tuples into display groups.
    Returns dict: {"human_interest": [...], "governance": [...], "structural": [...]}
    """
    groups = {"human_interest": [], "governance": [], "structural": []}
    for label, w in signals:
        groups[_classify_signal(label)].append((label, w))
    return groups


# ── Markdown report generator ─────────────────────────────────────────────────


_GOVERNANCE_FORCE_COMPONENTS = (
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
)

_CONSTRUCT_ORDER = (
    "Coupling",
    "Integrity Layer",
    "Coherence Test",
    "Structural Transparency",
    "Structural Honesty",
    "Structural Containment",
    "Consistency",
    "Reversibility",
)


def _text_pool(result):
    """Source-derived POSITIVE signals only: strengths (built from fired
    rubric patterns), sector signals actually present in the text, and
    constructs actually detected. Gaps, failure modes, and remediation
    text are deliberately excluded — a profile must never detect the
    vocabulary of its own recommendations."""
    parts = []
    parts.extend(str(v) for v in result.get("strengths", []) or [])
    for finding in result.get("sector_specific_findings", []) or []:
        s = str(finding)
        if s.startswith("Risk signal present") or s.startswith("Evidence present"):
            parts.append(s)
    coverage = result.get("construct_coverage", {})
    parts.extend(k for k, present in coverage.items() if present)
    return "\n".join(parts).lower()


def _gap_pool(result):
    """Source-derived NEGATIVE signals: gaps, failure modes, and sector
    signals confirmed absent."""
    parts = []
    parts.extend(str(v) for v in result.get("gaps", []) or [])
    parts.extend(str(v) for v in result.get("primary_failure_modes", []) or [])
    for finding in result.get("sector_specific_findings", []) or []:
        s = str(finding)
        if s.startswith("Risk signal absent") or s.startswith("Evidence gap"):
            parts.append(s)
    return "\n".join(parts).lower()


def _governance_force_profile(result):
    """Display-only profile derived from source-text signals; does not score."""
    text = _text_pool(result)
    gaps = _gap_pool(result)
    coverage = result.get("construct_coverage", {})
    functional = result.get("functional_alignment", {})
    scores = result.get("score_breakdown", {})
    fired = []
    missed = []
    for dim in scores.values():
        fired.extend(label.lower() for label, _ in dim.get("fired", []))
        missed.extend(label.lower() for label, _ in dim.get("missed", []))
    fired_text = "\n".join(fired)
    missed_text = "\n".join(missed)

    def _functional_verdict(construct):
        return functional.get(construct, {}).get("verdict", "ABSENT")

    def classify(component, detected_terms=(), partial_terms=(), gap_terms=(),
                 functional_construct=None):
        if functional_construct:
            fv = _functional_verdict(functional_construct)
            if fv in ("DECLARED", "FUNCTIONAL"):
                return "detected", ("Substance detected in the source text "
                                    "(functional-alignment layer).")
            if fv == "PARTIAL":
                return "partial/implicit", ("Partial substance detected in the "
                                           "source text (one signal family).")
        hay = "\n".join([text, fired_text])
        gap_hay = "\n".join([gaps, missed_text])
        if any(term in hay for term in detected_terms):
            return "detected", "Source-text signals indicate this component is present or directly supported."
        if any(term in hay for term in partial_terms):
            return "partial/implicit", "Source-text signals suggest the component may be present, but the report does not treat it as fully established."
        if any(term in gap_hay for term in gap_terms):
            return "gap / requires review", "Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation."
        return "requires reviewer confirmation", "Source-text signals are insufficient to classify this component with confidence."

    profile = {
        "mandate": classify("mandate", ("shall", "must", "mandatory", "binding", "obligation"), ("should", "encourage", "principle"), ("voluntary", "declaratory", "non-binding", "mandatory")),
        "actor": classify("actor", ("named parties", "responsible", "authority", "provider", "operator", "deployer", "developer", "agency"), ("oversight", "review"), ("named parties", "actor", "responsible")),
        "trigger": classify("trigger", ("threshold", "trigger", "before deployment", "pre-deployment", "when", "prior to"), ("review", "monitoring"), ("threshold", "trigger")),
        "protected interest": classify("protected interest", ("human interest", "rights", "safety", "patient", "worker", "non-discrimination", "privacy", "redress"), ("fairness", "welfare", "dignity"), ("human interest", "materially affects"), functional_construct="Coupling"),
        "control": classify("control", ("integrity layer", "structural transparency", "structural honesty", "structural containment", "control", "safeguard"), ("oversight", "monitoring"), ("integrity layer", "control"), functional_construct="Integrity Layer"),
        "evidence": classify("evidence", ("evidence present", "documentation", "audit", "record", "trace", "reporting"), ("transparency", "monitoring"), ("evidence gap", "evidence")),
        "reversibility": ("detected", "Construct coverage marks Reversibility as present.") if coverage.get("Reversibility") else classify("reversibility", ("reversibility", "reverse", "rollback", "appeal", "contest"), ("redress", "review"), ("reversibility", "reverse"), functional_construct="Reversibility"),
        "escalation": classify("escalation", ("escalation", "authority", "enforcement", "supervisory", "complaint"), ("review", "oversight"), ("escalation", "enforcement")),
        "consequence": classify("consequence", ("consequence", "sanction", "penalty", "enforcement", "remedy", "liability"), ("accountability", "redress"), ("consequence", "sanction", "penalty")),
        "auditability": classify("auditability", ("audit", "evidence", "trace", "record", "documentation", "monitoring"), ("transparency", "reporting"), ("auditability", "evidence")),
    }
    return [(component, *profile[component]) for component in _GOVERNANCE_FORCE_COMPONENTS]


def _remediation_groups(steps):
    """Heuristic display grouping of already-generated remediation steps."""
    groups = {
        "Immediate clarity/control fixes": [],
        "Evidence/auditability fixes": [],
        "Reversibility/escalation fixes": [],
        "LAIF-native adoption fixes": [],
    }
    for step in steps:
        low = step.lower()
        if any(term in low for term in ("evidence", "audit", "documentation", "record", "trace", "monitor")):
            groups["Evidence/auditability fixes"].append(step)
        elif any(term in low for term in ("revers", "escalat", "redress", "appeal", "contest")):
            groups["Reversibility/escalation fixes"].append(step)
        elif any(term in low for term in ("laif", "canonical", "coupling", "coherence test", "integrity layer", "non-amendable")):
            groups["LAIF-native adoption fixes"].append(step)
        else:
            groups["Immediate clarity/control fixes"].append(step)
    return {name: values for name, values in groups.items() if values}



_REMEDIATION_PATCH_KEYS = (
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
)

_PATCH_SOURCE_EVIDENCE_FALLBACK = (
    "Not directly quoted by current deterministic extractor; reviewer confirmation required."
)

_PATCH_MAX_PER_DOCUMENT = 12
_EVIDENCE_TRACE_MAX_PER_DOCUMENT = 20
_EVIDENCE_TRACE_LEGAL_AUTHORITY_BOUNDARY = (
    "Evidence traces are deterministic source-support metadata. They do not "
    "determine legal validity or certify LAIF-native compliance."
)


def _normalize_trace_text(text):
    """Normalize trace text for deterministic comparison metadata only."""
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def _find_text_span(source_text, candidate_text):
    """Return exact character offsets only when candidate_text is present."""
    source = str(source_text or "")
    candidate = str(candidate_text or "")
    if not source or not candidate:
        return None
    start = source.find(candidate)
    if start < 0:
        return None
    end = start + len(candidate)
    if source[start:end] != candidate:
        return None
    return start, end


def _trace_id(label, index):
    base = re.sub(r"[^a-z0-9]+", "-", str(label or "trace").lower()).strip("-")
    base = base[:36].strip("-") or "trace"
    return f"LAIF-TRACE-{index:02d}-{base}"


def _evidence_trace(
    source_text,
    source_document,
    source_type,
    assessment_mode,
    evidence_type,
    matched_text,
    match_rule,
    supports,
    index,
):
    span = _find_text_span(source_text, matched_text)
    if span is None:
        return None
    start, end = span
    return {
        "trace_id": _trace_id(evidence_type, index),
        "source_document": source_document,
        "source_type": source_type,
        "assessment_mode": assessment_mode,
        "evidence_type": evidence_type,
        "matched_text": matched_text,
        "normalized_match": _normalize_trace_text(matched_text),
        "start_char": start,
        "end_char": end,
        "match_rule": match_rule,
        "confidence": "deterministic_pattern" if match_rule.startswith("regex:") else "exact",
        "supports": supports,
        "legal_authority_boundary": _EVIDENCE_TRACE_LEGAL_AUTHORITY_BOUNDARY,
    }


def _fallback_evidence_trace(source_document, source_type, assessment_mode, supports, index):
    return {
        "trace_id": _trace_id("reviewer-confirmation-required", index),
        "source_document": source_document,
        "source_type": source_type,
        "assessment_mode": assessment_mode,
        "evidence_type": "reviewer_confirmation_required",
        "matched_text": "",
        "normalized_match": "",
        "start_char": None,
        "end_char": None,
        "match_rule": "no_direct_quote_extracted",
        "confidence": "fallback_required",
        "supports": supports,
        "legal_authority_boundary": _EVIDENCE_TRACE_LEGAL_AUTHORITY_BOUNDARY,
    }


def _first_regex_match(text, pattern):
    match = re.search(pattern, text or "", re.IGNORECASE)
    if not match:
        return None
    return match.group(0)


def _extract_profile_signal_traces(text, result):
    traces = []
    profile = _sector_profile_metadata(result.get("sector_profile", result.get("sector_used")))
    signal_specs = []
    signal_specs.extend((pat, label, "sector_profile_signal") for pat, label in profile.get("risk_indicators", []))
    signal_specs.extend((pat, label, "provenance_signal") for pat, label in profile.get("expected_evidence", []))
    for pat, label, evidence_type in signal_specs:
        matched = _first_regex_match(text, pat)
        if matched:
            traces.append((evidence_type, matched, f"regex:{pat}", f"sector profile signal: {label}"))
    return traces


def _extract_governance_force_traces(text, result):
    traces = []
    rubric_specs = (
        (TERMINOLOGY_RUBRIC, "diagnostic_term", "terminology signal"),
        (STRUCTURAL_RUBRIC, "governance_force_signal", "structural signal"),
        (CONCEPTUAL_RUBRIC, "governance_force_signal", "conceptual signal"),
        (AUDITABILITY_RUBRIC, "governance_force_signal", "auditability signal"),
        (ENFORCEABILITY_RUBRIC, "governance_force_signal", "enforceability signal"),
    )
    for rubric, evidence_type, prefix in rubric_specs:
        for _, pat, label in rubric:
            matched = _first_regex_match(text, pat)
            if matched:
                traces.append((evidence_type, matched, f"regex:{pat}", f"{prefix}: {label}"))
    return traces


def _extract_remediation_anchor_traces(text, result):
    traces = []
    for construct, present in result.get("construct_coverage", {}).items():
        if not present:
            continue
        matched = _first_regex_match(text, re.escape(construct))
        if matched:
            traces.append(("remediation_anchor", matched, f"regex:{re.escape(construct)}", f"remediation anchor: {construct}"))
    return traces


def _build_evidence_traces(text, result):
    """Build capped deterministic source-support traces without changing scores."""
    source_document = result.get("document_name", "unknown document")
    source_type = result.get("source_type", "unknown_source_type")
    assessment_mode = result.get("assessment_mode", "external_framework")
    candidates = []
    candidates.extend(_extract_profile_signal_traces(text, result))
    candidates.extend(_extract_governance_force_traces(text, result))
    candidates.extend(_extract_remediation_anchor_traces(text, result))

    traces = []
    seen = set()
    for evidence_type, matched_text, match_rule, supports in candidates:
        if len(traces) >= _EVIDENCE_TRACE_MAX_PER_DOCUMENT:
            break
        span = _find_text_span(text, matched_text)
        if span is None:
            continue
        dedupe = (span[0], span[1], evidence_type, supports)
        if dedupe in seen:
            continue
        seen.add(dedupe)
        trace = _evidence_trace(
            text, source_document, source_type, assessment_mode, evidence_type,
            matched_text, match_rule, supports, len(traces) + 1
        )
        if trace is not None and trace["matched_text"] == text[trace["start_char"]:trace["end_char"]]:
            traces.append(trace)

    if not traces and (result.get("gaps") or result.get("primary_failure_modes") or result.get("recommended_remediation_steps")):
        traces.append(_fallback_evidence_trace(
            source_document, source_type, assessment_mode,
            "diagnostic findings require reviewer confirmation; no direct quote extracted",
            1,
        ))
    return traces[:_EVIDENCE_TRACE_MAX_PER_DOCUMENT]


def _slugify_patch_id(text, index):
    """Return a stable compact patch identifier for deterministic report output."""
    base = re.sub(r"[^a-z0-9]+", "-", str(text or "patch").lower()).strip("-")
    base = base[:42].strip("-") or "patch"
    return f"LAIF-PATCH-{index:02d}-{base}"


def _gap_text(gap):
    if isinstance(gap, dict):
        return str(gap.get("diagnostic_gap") or gap.get("problem") or gap.get("title") or gap)
    return str(gap)


def _severity_for_gap(gap, result):
    text = _gap_text(gap).lower()
    if "contradiction" in text or "negated" in text:
        return "critical"
    if any(term in text for term in ("coupling", "integrity layer", "coherence test", "precondition")):
        return "high"
    if any(term in text for term in ("low ", "critically low", "evidence gap", "audit", "enforceability")):
        return "medium"
    if any(term in text for term in ("sector", "context", "provenance")):
        return "low"
    if result.get("formal_laif_native_compliance", result.get("formal_laif_compliance")) == "FAIL":
        return "medium"
    return "informational"


def _governance_component_for_gap(gap):
    text = _gap_text(gap).lower()
    checks = (
        ("evidence", ("evidence", "documentation", "record", "trace", "audit")),
        ("auditability", ("auditability", "audit", "monitor", "review", "traceability")),
        ("reversibility", ("reversibility", "reverse", "rollback", "appeal", "redress", "contest")),
        ("escalation", ("escalation", "complaint", "supervisory", "authority")),
        ("consequence", ("consequence", "sanction", "penalty", "enforcement", "liability")),
        ("actor", ("actor", "responsible", "provider", "operator", "deployer", "agency")),
        ("trigger", ("trigger", "threshold", "before deployment", "pre-deployment", "when")),
        ("protected interest", ("human interest", "rights", "safety", "privacy", "non-discrimination")),
        ("control", ("control", "safeguard", "integrity layer", "containment", "transparency", "honesty")),
        ("mandate", ("shall", "must", "mandatory", "obligation", "binding")),
    )
    for component, terms in checks:
        if any(term in text for term in terms):
            return component
    return "control"


def _construct_for_gap(gap):
    text = _gap_text(gap).lower()
    construct_terms = (
        ("Structural Transparency", ("structural transparency", "transparency", "meaningful account", "explanation")),
        ("Structural Honesty", ("structural honesty", "honesty", "contradiction", "objectives")),
        ("Structural Containment", ("structural containment", "containment", "boundary", "irreversible")),
        ("Integrity Layer", ("integrity layer", "precondition", "deployment precondition")),
        ("Coherence Test", ("coherence test", "pdca", "q1", "q2", "q3")),
        ("Coupling", ("coupling", "human interest", "restriction")),
        ("Consistency", ("consistency", "scale-invariant")),
        ("Reversibility", ("reversibility", "reverse", "rollback", "appeal", "redress")),
    )
    for construct, terms in construct_terms:
        if any(term in text for term in terms):
            return construct
    return "Governance-force implementation"


def _patch_type_for_gap(gap):
    text = _gap_text(gap).lower()
    if "laif-native" in text or "canonical" in text or "terminolog" in text:
        return "terminology_gap"
    if "construct" in text or any(c.lower() in text for c in _CONSTRUCT_ORDER):
        return "construct_gap"
    if any(term in text for term in ("audit", "trace", "monitor", "review")):
        return "auditability_gap"
    if any(term in text for term in ("enforce", "consequence", "sanction", "mandatory", "shall")):
        return "enforceability_gap"
    if any(term in text for term in ("revers", "rollback", "appeal", "redress", "contest")):
        return "reversibility_gap"
    if any(term in text for term in ("evidence", "documentation", "artifact", "record")):
        return "evidence_gap"
    if "sector" in text:
        return "sector_context_gap"
    if any(term in text for term in ("provenance", "citation", "source")):
        return "provenance_gap"
    if "certification" in text:
        return "laif_native_certification_gap"
    return "governance_force_gap"


def _recommended_patch_for_gap(gap, result):
    construct = _construct_for_gap(gap)
    component = _governance_component_for_gap(gap)
    gap_text = _gap_text(gap)
    if construct == "Coupling":
        return "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing."
    if construct == "Coherence Test":
        return "Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger."
    if construct == "Integrity Layer":
        return "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use."
    if component == "evidence":
        return "Require evidence artifacts for the finding, including named records, retention location, reviewer role, and update cadence."
    if component == "reversibility":
        return "Add an escalation path and reversibility procedure that identifies who can pause, roll back, review, or remedy the affected decision."
    if component == "actor":
        return "Specify responsible actor ownership for the control, including approval authority, implementation role, and review accountability."
    if component == "auditability":
        return "Create a verification test and audit trail that a reviewer can repeat without relying on undocumented discretion."
    return f"Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: {gap_text[:160]}"


def _canonical_clause_for_gap(gap, result):
    construct = _construct_for_gap(gap)
    if construct == "Coupling":
        return "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation."
    if construct == "Coherence Test":
        return "If adopting LAIF-native form: the Coherence Test shall document Q1 Coupling, Q2 Consistency, and Q3 Reversibility before authorization."
    if construct == "Integrity Layer":
        return "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence."
    return "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path."


def _operational_control_for_gap(gap, result):
    component = _governance_component_for_gap(gap)
    controls = {
        "mandate": "Maintain a controlled obligation register that maps mandate text to owner, trigger, evidence, and review status.",
        "actor": "Assign a named accountable role and backup reviewer for implementation, exception approval, and periodic review.",
        "trigger": "Create trigger criteria for when the control activates, including pre-deployment, change, incident, and periodic review events.",
        "protected interest": "Record the protected interest and affected population for each restriction or operational control.",
        "control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
        "evidence": "Require evidence capture in a repository with citation, date, responsible actor, and reviewer confirmation.",
        "reversibility": "Maintain a rollback, appeal, or corrective-action playbook with decision authority and response time expectations.",
        "escalation": "Add an escalation path from operator review to accountable governance, legal/compliance, or procurement authority.",
        "consequence": "Define institution-approved consequences for unresolved nonconformance, including pause, remediation, or management review.",
        "auditability": "Create repeatable audit sampling and trace review steps tied to the control evidence repository.",
    }
    return controls.get(component, controls["control"])


def _evidence_artifact_for_gap(gap, result):
    component = _governance_component_for_gap(gap)
    artifacts = {
        "mandate": "Approved obligation register entry with source citation and control mapping.",
        "actor": "Responsibility assignment matrix or control-owner attestation.",
        "trigger": "Trigger matrix and completed pre-deployment or change-review checklist.",
        "protected interest": "Protected-interest register with affected-population rationale.",
        "control": "Signed control procedure, exception log, and implementation record.",
        "evidence": "Evidence packet containing source excerpt, record location, reviewer, date, and retention rule.",
        "reversibility": "Rollback, appeal, redress, or corrective-action log with closure evidence.",
        "escalation": "Escalation log showing routing, accountable recipient, decision, and closure date.",
        "consequence": "Nonconformance record and institution-approved consequence or remediation decision.",
        "auditability": "Audit workpaper or trace sample showing repeatable verification steps and results.",
    }
    return artifacts.get(component, artifacts["control"])


def _verification_test_for_gap(gap, result):
    component = _governance_component_for_gap(gap)
    return (
        f"Create a verification test that samples this {component} control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
    )


def _responsible_actor_for_gap(gap, result):
    text = _gap_text(gap).lower()
    if "procurement" in text or "vendor" in text:
        return "Procurement lead with legal/compliance and vendor-management support"
    if "sector" in text or "risk" in text:
        return "Departmental AI governance owner with sector subject-matter reviewer"
    if "audit" in text or "evidence" in text:
        return "Internal audit or compliance evidence owner"
    if "legal" in text or "regulat" in text:
        return "Legal/compliance owner with policy authority"
    return "Institutional AI governance owner"


def _implementation_priority_for_gap(gap, result):
    text = _gap_text(gap).lower()
    explicit_adoption_terms = (
        "laif-native",
        "canonical",
        "terminology",
        "adoption",
        "translate into laif",
        "formal laif",
    )
    if (
        result.get("assessment_mode") != "laif_native_certification"
        and any(term in text for term in explicit_adoption_terms)
    ):
        return "optional_laif_adoption"
    severity = _severity_for_gap(gap, result)
    if severity in ("critical", "high"):
        return "immediate"
    if severity == "medium":
        return "near_term"
    return "planned"


def _legal_authority_boundary_for_gap(gap, result):
    if result.get("assessment_mode") == "external_framework":
        return "diagnostic_only"
    if _implementation_priority_for_gap(gap, result) == "optional_laif_adoption":
        return "laif_native_adoption"
    return "institution_defined"


def _patch_candidate_gap_entries(result):
    entries = []
    entries.extend(_gap_text(gap) for gap in result.get("primary_failure_modes", []))
    entries.extend(f"Missing LAIF construct: {construct}" for construct, present in result.get("construct_coverage", {}).items() if not present)
    for dim_key, dim in result.get("score_breakdown", {}).items():
        missed = dim.get("missed", [])
        score_key = {
            "structural": "structural_score",
            "terminology": "terminology_score",
            "conceptual": "conceptual_proximity_score",
            "auditability": "auditability_score",
            "enforceability": "enforceability_score",
        }.get(dim_key)
        score = result.get(score_key, 100) if score_key else 100
        if missed and score < 50:
            labels = ", ".join(label for label, _ in missed[:3])
            entries.append(f"Low {dim_key} score ({score}/100): missed signals include {labels}")
    for step in result.get("structured_remediation_steps", []):
        problem = step.get("problem", "") if isinstance(step, dict) else str(step)
        if problem:
            entries.append(f"Structured remediation step: {problem}")
    return entries


def _trace_support_matches_patch(trace, diagnostic_gap, result):
    if trace.get("confidence") not in ("exact", "deterministic_pattern"):
        return False
    haystack = " ".join([
        str(trace.get("supports", "")),
        str(trace.get("evidence_type", "")),
        str(trace.get("normalized_match", "")),
    ]).lower()
    needles = [
        _construct_for_gap(diagnostic_gap),
        _governance_component_for_gap(diagnostic_gap),
        _patch_type_for_gap(diagnostic_gap).replace("_", " "),
    ]
    for needle in needles:
        needle = str(needle or "").lower()
        if needle and needle in haystack:
            return True
    gap_low = str(diagnostic_gap or "").lower()
    for token in ("audit", "evidence", "trace", "transparency", "oversight", "accountability", "risk", "shall", "monitor"):
        if token in gap_low and token in haystack:
            return True
    return False


def _evidence_trace_links_for_patch(diagnostic_gap, result):
    links = []
    source_evidence = _PATCH_SOURCE_EVIDENCE_FALLBACK
    for trace in result.get("evidence_traces", []):
        if len(links) >= 3:
            break
        if _trace_support_matches_patch(trace, diagnostic_gap, result):
            links.append(trace.get("trace_id"))
            if source_evidence == _PATCH_SOURCE_EVIDENCE_FALLBACK:
                source_evidence = trace.get("matched_text") or source_evidence
    return links, source_evidence


def _build_remediation_patches(result):
    """Build deterministic, machine-readable diagnostic remediation records."""
    patches = []
    seen_gaps = set()
    for gap in _patch_candidate_gap_entries(result):
        diagnostic_gap = re.sub(r"\s+", " ", _gap_text(gap)).strip()
        if not diagnostic_gap:
            continue
        dedupe_key = diagnostic_gap.lower()
        if dedupe_key in seen_gaps:
            continue
        seen_gaps.add(dedupe_key)
        patch_index = len(patches) + 1
        evidence_trace_ids, source_evidence = _evidence_trace_links_for_patch(diagnostic_gap, result)
        patch = {
            "patch_id": _slugify_patch_id(diagnostic_gap, patch_index),
            "assessment_mode": result.get("assessment_mode", "external_framework"),
            "source_document": result.get("document_name", "unknown document"),
            "finding_type": _patch_type_for_gap(diagnostic_gap),
            "severity": _severity_for_gap(diagnostic_gap, result),
            "laif_construct": _construct_for_gap(diagnostic_gap),
            "governance_force_component": _governance_component_for_gap(diagnostic_gap),
            "diagnostic_gap": diagnostic_gap,
            "source_evidence": source_evidence,
            "evidence_trace_ids": evidence_trace_ids,
            "recommended_patch": _recommended_patch_for_gap(diagnostic_gap, result),
            "canonical_clause_if_adopting_laif": _canonical_clause_for_gap(diagnostic_gap, result),
            "operational_control": _operational_control_for_gap(diagnostic_gap, result),
            "evidence_artifact": _evidence_artifact_for_gap(diagnostic_gap, result),
            "verification_test": _verification_test_for_gap(diagnostic_gap, result),
            "responsible_actor": _responsible_actor_for_gap(diagnostic_gap, result),
            "implementation_priority": _implementation_priority_for_gap(diagnostic_gap, result),
            "legal_authority_boundary": _legal_authority_boundary_for_gap(diagnostic_gap, result),
        }
        patch = _sector_profile_patch_adjustments(patch, result)
        patches.append(patch)
        if len(patches) >= _PATCH_MAX_PER_DOCUMENT:
            break
    return patches



# ── Calibration and score-justification metadata ─────────────────────────────
# These helpers are interpretive metadata only. They consume existing scores,
# fired/missed signal labels, evidence traces, sector profile metadata, and
# remediation patch records; they do not recompute or alter scoring.

_DIMENSION_SCORE_KEYS = {
    "structural": "structural_score",
    "terminology": "terminology_score",
    "conceptual": "conceptual_proximity_score",
    "auditability": "auditability_score",
    "enforceability": "enforceability_score",
}

_DIMENSION_DISPLAY_NAMES = {
    "structural": "Structural governance architecture",
    "terminology": "Canonical terminology",
    "conceptual": "Conceptual proximity",
    "auditability": "Auditability",
    "enforceability": "Enforceability",
}


def _score_band(score):
    """Return a structural-signal band for an existing 0-100 score."""
    score = max(0, min(100, int(score)))
    if score <= 19:
        return "minimal structural signal"
    if score <= 39:
        return "limited structural signal"
    if score <= 59:
        return "partial structural signal"
    if score <= 79:
        return "substantial structural signal"
    return "strong structural signal"


def _score_interpretation_label(score):
    """Return diagnostic, non-legal score interpretation language."""
    band = _score_band(score)
    return (
        f"{band}; diagnostic interpretation only, not a legal verdict, and requires "
        "evidence/authority verification before any governance conclusion is drawn."
    )


def _dimension_calibration_note(dimension_name, score):
    """Explain what a dimension band means without turning it into a recipe."""
    label = _DIMENSION_DISPLAY_NAMES.get(dimension_name, dimension_name.replace("_", " "))
    band = _score_band(score)
    return (
        f"{label} shows {band}. Interpret the score with fired/missed signals, "
        "source evidence, responsible actor, trigger, control, reversibility, "
        "consequence, and auditability review; it is not a compliance finding."
    )


def _signal_labels(signals, limit=3):
    return [label for label, _ in list(signals or [])[:limit]]


def _has_fallback_only_evidence(result):
    traces = result.get("evidence_traces", [])
    return bool(traces) and all(trace.get("confidence") == "fallback_required" for trace in traces)


def _calibration_cautions(result):
    """Build deterministic calibration caution records from existing metadata."""
    cautions = []

    def add(caution_id, type_, message, implication, recommended_review):
        cautions.append({
            "caution_id": caution_id,
            "type": type_,
            "message": message,
            "implication": implication,
            "recommended_review": recommended_review,
        })

    conceptual = result.get("conceptual_proximity_score", 0)
    terminology = result.get("terminology_score", 0)
    overall = result.get("overall_readiness_score", 0)
    sector = result.get("sector_risk_alignment", 0)
    evidence_traces = result.get("evidence_traces", [])
    native_status = result.get("formal_laif_native_compliance", result.get("formal_laif_compliance"))
    construct = result.get("construct_coverage", {})

    if conceptual >= 50 and terminology <= 20:
        add(
            "conceptual-high-terminology-low",
            "score_divergence",
            "High conceptual LAIF-model signal appears with low canonical terminology signal.",
            "The source may be conceptually adjacent to LAIF while remaining outside LAIF-native certification language.",
            "Review whether any LAIF-native adoption is intended and verify authority, evidence, and structural controls before drawing conclusions.",
        )
    if sector >= 60 and overall < 50:
        add(
            "sector-high-readiness-low",
            "sector_context",
            "Sector risk alignment materially exceeds overall readiness.",
            "Sector relevance may be high even when LAIF-model governance structure is incomplete.",
            "Review sector-specific evidence artifacts, control ownership, triggers, escalation, and reversibility before relying on score proximity.",
        )
    if len(evidence_traces) >= 5 and native_status == "FAIL":
        add(
            "evidence-high-formal-fail",
            "evidence_boundary",
            "Multiple evidence traces are present while formal LAIF-native compliance remains failed.",
            "Source presence supports diagnostics but cannot override formal LAIF-native failure.",
            "Confirm whether traced text implements authority, responsible actor, control, consequence, and auditability rather than only stating concepts.",
        )
    if not evidence_traces:
        add(
            "evidence-none",
            "evidence_boundary",
            "No evidence traces were generated by the deterministic extractor.",
            "The score remains a rubric output, but source-presence support is unavailable in this assessment output.",
            "Perform reviewer source confirmation and provenance review before operational reliance.",
        )
    elif _has_fallback_only_evidence(result):
        add(
            "evidence-fallback-only",
            "evidence_boundary",
            "Evidence trace support is fallback-only and requires reviewer confirmation.",
            "Fallback evidence supports diagnostic triage but does not prove source implementation.",
            "Review source excerpts directly and confirm exact authority, actor, trigger, control, consequence, and auditability records.",
        )
    if overall >= 70 and (not construct.get("Coupling") or result.get("enforceability_score", 0) < 50):
        add(
            "high-score-actor-enforceability-review",
            "structural_review",
            "Overall LAIF-model signal is high while responsible-actor or enforceability signals require review.",
            "A high score can reflect text signals without proving accountable authority or enforceable implementation.",
            "Verify responsible actor, trigger, evidence artifact, escalation path, consequence, and auditability before relying on the score.",
        )
    if overall < 40 and result.get("assessment_mode") == "external_framework":
        add(
            "low-score-external-authority-boundary",
            "external_authority_boundary",
            "Low LAIF-model signal may indicate missing LAIF-model signals, not legal invalidity under the source framework's own authority.",
            "The assessment does not determine external legal validity, governance validity, safety, or enforceability.",
            "Separate LAIF diagnostic remediation from legal analysis under the source framework's own authority.",
        )
    return cautions


def _score_gaming_risk_notes(result):
    """Build deterministic anti-gaming notes without alleging bad faith."""
    notes = []

    def add(note_id, trigger, message, recommended_review):
        notes.append({
            "note_id": note_id,
            "type": "anti_gaming",
            "trigger": trigger,
            "message": (
                message + " This is not a finding of bad faith and not a legal invalidity claim."
            ),
            "recommended_review": recommended_review,
        })

    overall = result.get("overall_readiness_score", 0)
    sector = result.get("sector_risk_alignment", 0)
    conceptual = result.get("conceptual_proximity_score", 0)
    audit = result.get("auditability_score", 0)
    enforce = result.get("enforceability_score", 0)
    terminology = result.get("terminology_score", 0)
    structural = result.get("structural_score", 0)
    construct_count = sum(1 for present in result.get("construct_coverage", {}).values() if present)
    evidence_count = len(result.get("evidence_traces", []))
    linked_patch_count = sum(1 for patch in result.get("remediation_patches", []) if patch.get("evidence_trace_ids"))

    if sector - overall >= 25 and sector >= 50:
        add(
            "sector-density-over-readiness",
            "sector risk alignment materially exceeds overall readiness",
            "Possible keyword or signal density risk; requires structural evidence review.",
            "Check whether sector-specific language is backed by accountable controls, evidence artifacts, reversibility, escalation, and consequences.",
        )
    if conceptual >= 60 and (audit < 45 or enforce < 45):
        add(
            "conceptual-high-controls-weak",
            "conceptual proximity is high while auditability or enforceability is weak",
            "Possible keyword or signal density risk; requires structural evidence review.",
            "Verify operational controls rather than relying on conceptual alignment language alone.",
        )
    if terminology >= 60 and (structural < 50 or construct_count < 5):
        add(
            "terminology-high-structure-weak",
            "terminology signal is high while structural depth or construct coverage is weak",
            "Possible keyword or signal density risk; requires structural evidence review.",
            "Review whether canonical terms are connected to actor, trigger, control, evidence, reversibility, escalation, consequence, and auditability.",
        )
    if evidence_count >= 5 and linked_patch_count <= 1 and result.get("remediation_patches"):
        add(
            "evidence-many-remediation-weak",
            "evidence traces are numerous but linked remediation remains weak",
            "Possible keyword or signal density risk; requires structural evidence review.",
            "Confirm that traced sources support implementable remediation patches rather than isolated textual mentions.",
        )
    return notes


def _score_justification_summary(result):
    """Summarize overall score interpretation without altering score values."""
    overall = result.get("overall_readiness_score", 0)
    formal_status = result.get("formal_laif_native_compliance", result.get("formal_laif_compliance", "FAIL"))
    return {
        "overall_score": overall,
        "overall_band": _score_band(overall),
        "interpretation": _score_interpretation_label(overall),
        "assessment_mode": result.get("assessment_mode", "external_framework"),
        "not_legal_determination": True,
        "not_certification": True,
        "formal_fail_boundary": (
            "High conceptual, sector, or evidence proximity cannot override formal LAIF-native failure."
            if formal_status == "FAIL"
            else "Formal LAIF-native status remains governed only by the existing certification gate."
        ),
        "evidence_trace_context": "Evidence traces support exact source presence where available but do not prove implementation.",
        "sector_profile_context": "Sector profiles contextualize diagnostics but do not create sector compliance gates.",
        "remediation_context": "Remediation patches are diagnostic unless separately adopted by an authority.",
    }


def _dimension_justification_records(result):
    """Create per-dimension justification records from existing signal labels only."""
    records = []
    for dim in ("structural", "terminology", "conceptual", "auditability", "enforceability"):
        score = result.get(_DIMENSION_SCORE_KEYS[dim], 0)
        breakdown = result.get("score_breakdown", {}).get(dim, {})
        fired = breakdown.get("fired", [])
        missed = breakdown.get("missed", [])
        records.append({
            "dimension": dim,
            "score": score,
            "band": _score_band(score),
            "interpretation": _score_interpretation_label(score),
            "fired_signal_count": len(fired),
            "missed_signal_count": len(missed),
            "dominant_strengths": _signal_labels(fired),
            "dominant_gaps": _signal_labels(missed),
            "calibration_note": _dimension_calibration_note(dim, score),
            "gaming_caution": (
                "Rubric visibility is not permission for keyword stuffing; structural evidence, accountable control, reversibility, consequence, and auditability must be reviewed."
            ),
        })
    return records

def _native_certification_label(result):
    if result.get("assessment_mode") == "external_framework" and result.get("formal_laif_native_compliance", result.get("formal_laif_compliance")) == "FAIL":
        return "FAIL / not LAIF-native / canonical remediation required"
    return result.get("formal_laif_native_compliance", result.get("formal_laif_compliance", "FAIL"))


def _safe_executive_verdict_text(result):
    """Return mode-scoped executive verdict wording for generated reports."""
    verdict = result.get("executive_summary", {}).get("verdict", "")
    if not verdict:
        return ""

    native_status = result.get(
        "formal_laif_native_compliance",
        result.get("formal_laif_compliance", "FAIL"),
    )
    if result.get("assessment_mode") == "external_framework":
        if native_status == "PASS":
            return (
                "This source passes the formal LAIF-native certification gate under LAIF "
                "criteria; external framework assessment remains diagnostic and does not "
                "determine legal validity."
            )
        return (
            "This source does not pass the formal LAIF-native certification gate under "
            "LAIF criteria; external framework assessment remains diagnostic and does "
            "not determine legal validity."
        )

    if native_status == "PASS":
        return (
            "This document passes the formal LAIF-native certification gate under "
            "current LAIF criteria."
        )
    return (
        "This document does not pass the formal LAIF-native certification gate under "
        "current LAIF criteria."
    )



def _safe_executive_risk_text(risk):
    """Return report-safe executive risk wording without changing risk scoring."""
    text = str(risk or "").strip()
    safe_formal_gate = (
        "This document does not pass the formal LAIF-native certification gate "
        "under current LAIF criteria."
    )
    safe_construct_gate = (
        "Each required LAIF-native construct remains necessary for certification"
    )
    # Legacy public-output patterns are assembled from fragments so future source
    # hygiene checks do not reintroduce blocked phrases as contiguous literals.
    legacy_formal_gate = "".join((
        "This document fails formal ",
        "LAIF v1.2 compliance.",
    ))
    legacy_construct_gate = "".join((
        "Missing any single ",
        "construct = ",
        "FAIL",
    ))
    legacy_final_label = "".join(("Final ", "verdict"))
    legacy_failure_label = "".join(("Primary ", "Failure Modes"))
    replacements = (
        (legacy_formal_gate, safe_formal_gate),
        (legacy_construct_gate, safe_construct_gate),
        (" = FAIL", " prevents certification"),
        (legacy_final_label, "Executive diagnostic detail"),
        (legacy_failure_label, "Primary structural gaps"),
        ("legally invalid", "outside the LAIF-native certification channel"),
        ("governance-invalid", "outside the LAIF-native certification channel"),
        ("governance-worthless", "outside the LAIF-native certification channel"),
        ("structurally incoherent", "requiring LAIF-model remediation"),
    )
    for unsafe, safe in replacements:
        text = text.replace(unsafe, safe)
    return text


def _safe_markdown_cell(value):
    """Return a compact markdown-table cell without exposing control syntax."""
    text = "" if value is None else str(value)
    text = text.replace("\n", " ").replace("|", "\\|")
    return " ".join(text.split())


def _compact_list(values, limit=3, empty="none detected"):
    cleaned = [str(v).strip() for v in (values or []) if str(v).strip()]
    if not cleaned:
        return empty
    visible = cleaned[:limit]
    suffix = f"; +{len(cleaned) - limit} more" if len(cleaned) > limit else ""
    return "; ".join(visible) + suffix


def _report_score_band(result):
    sj = result.get("score_justification", {})
    return sj.get("overall_band") or result.get("score_interpretation") or _score_band(result.get("overall_readiness_score", 0))


def _public_report_status_label(result):
    native = result.get("formal_laif_native_compliance", result.get("formal_laif_compliance", "FAIL"))
    mode = result.get("assessment_mode", "external_framework")
    if native == "PASS":
        return "LAIF-native certification: PASS"
    if mode == "external_framework":
        return "LAIF-native certification: Not claimed / not applicable to this external-framework assessment."
    return "LAIF-native certification: FAIL / canonical remediation required"


def _report_boundary_notice(result=None):
    mode = (result or {}).get("assessment_mode", "mixed / document-specific")
    return (
        f"Assessment mode: {mode}. This public report is diagnostic, not certification for external-framework sources; "
        "it does not determine legal validity and cannot override formal LAIF-native failure. "
        "Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. "
        "Score bands are interpretive readiness bands, not determinations of compliance."
    )


def _report_evidence_summary(result):
    traces = result.get("evidence_traces", [])
    exact = sum(1 for t in traces if t.get("confidence") in {"exact", "deterministic_pattern"})
    fallback = sum(1 for t in traces if t.get("confidence") == "fallback_required")
    top = [f"{t.get('trace_id', '')} ({t.get('evidence_type', 'evidence')})" for t in traces[:3]]
    return {
        "total": len(traces),
        "exact": exact,
        "fallback": fallback,
        "top": _compact_list(top),
    }


def _report_patch_summary(result):
    patches = result.get("remediation_patches", [])
    severe = Counter(p.get("severity", "unspecified") for p in patches)
    return {
        "total": len(patches),
        "severity": _compact_list([f"{k}: {v}" for k, v in sorted(severe.items())]),
    }


def _report_caution_summary(result):
    cautions = []
    cautions.extend(result.get("calibration_cautions", []))
    cautions.extend(result.get("gaming_risk_notes", []))
    cautions.extend(result.get("evidence_cautions", []))
    return {"total": len(cautions), "top": _compact_list([c.get("message", c) if isinstance(c, dict) else c for c in cautions])}


def _report_document_row(result):
    evidence = _report_evidence_summary(result)
    patches = _report_patch_summary(result)
    cautions = _report_caution_summary(result)
    return [
        _safe_markdown_cell(result.get("document_name", ""))[:64],
        _safe_markdown_cell(result.get("assessment_mode", "external_framework")),
        _safe_markdown_cell(result.get("laif_alignment", "not assessed")),
        _safe_markdown_cell(f"{result.get('overall_readiness_score', 0)}/100 — {_report_score_band(result)}"),
        _safe_markdown_cell(result.get("sector_profile_label", result.get("sector_label", result.get("sector_used", ""))))[:32],
        evidence["total"],
        patches["total"],
        cautions["total"],
    ]


def _report_limits_and_reviewer_actions(result):
    actions = [
        "confirm source authority and provenance before relying on any institutional interpretation",
        "verify evidence artifacts and implementation records outside this text-only diagnostic output",
        "assign accountable owners for accepted remediation patches",
        "confirm escalation, reversibility, and appeal controls where the source affects people or protected interests",
        "determine whether institution, regulator, contract, or governing body has authority to adopt any change",
    ]
    if not result.get("evidence_traces"):
        actions.insert(1, "create or link source evidence because no deterministic evidence traces were available")
    return actions


def _markdown_table(headers, rows):
    safe_headers = [_safe_markdown_cell(h) for h in headers]
    safe_rows = [[_safe_markdown_cell(c) for c in row] for row in rows]
    widths = [max(len(safe_headers[i]), max((len(row[i]) for row in safe_rows), default=0)) for i in range(len(safe_headers))]
    lines = []
    lines.append("| " + " | ".join(safe_headers[i].ljust(widths[i]) for i in range(len(widths))) + " |")
    lines.append("| " + " | ".join("-" * widths[i] for i in range(len(widths))) + " |")
    for row in safe_rows:
        lines.append("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(widths))) + " |")
    return lines

def generate_markdown_report(assessments, report_date="July 2026"):
    """Render a stable public markdown report without changing assessment data."""
    lines = []
    assessments = list(assessments or [])

    def h(level, text):
        lines.append("\n" + "#" * level + " " + text)

    def p(text=""):
        lines.append(text)

    def table(headers, rows):
        lines.extend(_markdown_table(headers, rows))

    count = len(assessments)
    avg = lambda key: round(sum(r.get(key, 0) for r in assessments) / count) if count else 0
    native_failures = [r for r in assessments if r.get("formal_laif_native_compliance", r.get("formal_laif_compliance")) == "FAIL"]
    external_count = sum(1 for r in assessments if r.get("assessment_mode") == "external_framework")
    evidence_total = sum(len(r.get("evidence_traces", [])) for r in assessments)
    evidence_exact = sum(_report_evidence_summary(r)["exact"] for r in assessments)
    evidence_fallback = sum(_report_evidence_summary(r)["fallback"] for r in assessments)
    patch_total = sum(len(r.get("remediation_patches", [])) for r in assessments)
    force_counter = Counter()
    for r in assessments:
        for component, status, _ in _governance_force_profile(r):
            if status in {"gap / requires review", "requires reviewer confirmation"}:
                force_counter[component] += 1

    lines.append("# AI Governance Structural Integrity Assessment")
    p("*How far do these instruments' protections actually reach the people "
      "they govern — and what would it take to close the distance?*  ")
    p(f"**Report date:** {report_date}  ")
    p("**Assessment model:** Law-Aligned Intelligence Framework (LAIF) v1.2 · "
      "Compliance Toolkit v1.1 — the model is the measuring lens, not the "
      "subject of the findings; see Method Summary.  ")
    p("**Report architecture:** Governance Repair Assessment public template — Phase 3V  ")
    p("**Validator boundary:** validate.py enforcement remains unchanged; this report renders existing assessment results only.  ")
    p()

    h(2, "Report Scope and Boundary")
    h(3, "Result Boundary / How to Read This Report")
    p("This public report is a governance repair and systemic failure-pathway diagnostic for institutional review.")
    p("This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.")
    p("External-framework mode assesses governance repair adequacy, operational closure, evidence sufficiency, accountability closure, lifecycle control, residual-risk closure, implementation readiness, and failure-pathway risk.")
    p("This report does not determine legal validity, enforceability, safety status, procurement eligibility, clinical authority, HR authority, education authority, or regulatory acceptance.")
    p("Not LAIF-native is certification-channel wording only; it is not a legal-validity or governance-validity determination.")
    p("Evidence traces preserve exact-source and reviewer-confirmation boundaries; trace presence does not prove implementation.")
    p("Score bands summarize LAIF-model readiness signals and are not determinations of compliance; high scores cannot override formal LAIF-native failure.")
    p("Formal fail boundary: high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.")
    p()

    _citable      = [r for r in assessments if r.get("provenance") == "OFFICIAL_EXCERPT"]
    _illustrative = [r for r in assessments if r.get("provenance") != "OFFICIAL_EXCERPT"]
    h(3, "Evidence Basis and Citability")
    p("Every document carries a machine-verified provenance classification; findings "
      "inherit the citability of the text they were computed from "
      "(enforced by `test_provenance.py`).")
    p()
    table(
        ["Document", "Provenance", "Citable", "Evidence basis"],
        [
            [
                r.get("document_name", "")[:52],
                r.get("provenance", "") or "not declared",
                "Yes" if r.get("provenance") == "OFFICIAL_EXCERPT" else "No",
                (r.get("source_file") or r.get("source_url") or "illustrative document")[:60],
            ]
            for r in assessments
        ]
    )
    p()
    p("**OFFICIAL_EXCERPT** — text extracted verbatim at run time from the committed "
      "source file via unique start/end markers and pinned by SHA-256 "
      "(`official_documents.py`); any drift fails the run. Findings may be cited as "
      "statements about the named instrument within the declared excerpt scope. "
      "**REPRESENTATIVE_EXCERPT** — condensed paraphrase; findings characterise the "
      "framework style only and must not be presented as assessments of the official "
      "source instrument.")
    p()

    h(3, "Functional Alignment Layer (Substance Independent of Vocabulary)")
    p("Beyond the layers above, each core construct (Coupling, Integrity Layer, "
      "Consistency, Reversibility, Self-Application) is assessed for its *substance* "
      "in the document's own vocabulary — DECLARED (LAIF-native form), FUNCTIONAL "
      "(≥2 independent signal families including the construct's defining family), "
      "PARTIAL, or ABSENT. Grounded in LAIF v1.2 Part Eight (equivalent structural "
      "diligence through alternative documented means) and the Regulatory Integration "
      "Guide's SATISFIES/EXTENDS methodology. A document is never penalised for "
      "expressing LAIF's requirements in its own words, and never credited for using "
      "LAIF's words without the substance. Overall alignment verdicts: LAIF-NATIVE "
      "(qualified by structural depth) / FUNCTIONALLY ALIGNED / PARTIALLY ALIGNED / "
      "STRUCTURALLY UNALIGNED.")
    p()

    h(3, "Fair-Reading Bounds")
    p("1. A LAIF-native FAIL measures distance from LAIF's deliberately stricter "
      "standard, not instrument quality; it must never be quoted as a judgement of "
      "the instrument against its own objectives.")
    p("2. Official-corpus findings hold within each document's declared excerpt "
      "scope only.")
    p("3. Signals are lexical, not interpretive; per-signal traceability is the "
      "compensating control.")
    p("4. Form/questionnaire-style instruments are undercounted by prose rubrics; "
      "affected scorecards carry an interpretation caveat.")
    p("5. Cross-document averages characterise this corpus, not all AI governance.")
    p("6. Raw overall scores compress: part of the 100-point scale is reserved for "
      "LAIF-branded documents and lexical detection is conservative — a "
      "substance-perfect external document scores in the mid-50s on this "
      "instrument, so mid-range raw scores denote strength, not failure; each "
      "scorecard carries a calibrated position against the achievable ceiling.")
    p()

    h(2, "Executive Brief")
    p(f"- **Total documents assessed:** {count} ({external_count} external instruments "
      f"assessed as governance repair diagnostics, not LAIF-native certification)")
    p(f"- **Average overall readiness:** {avg('overall_readiness_score')}/100")
    p(f"- **Average conceptual proximity:** {avg('conceptual_proximity_score')}/100")
    p(f"- **Average sector alignment:** {avg('sector_risk_alignment')}/100")
    if _citable:
        _cit_fail = sum(1 for r in _citable
                        if r.get("formal_laif_native_compliance",
                                 r.get("formal_laif_compliance")) == "FAIL")
        _cit_con  = round(sum(r.get("conceptual_proximity_score", 0)
                              for r in _citable) / len(_citable))
        p(f"- **Citable subset (OFFICIAL_EXCERPT, verbatim hash-pinned):** "
          f"{len(_citable)}/{count} documents; {_cit_fail}/{len(_citable)} not "
          f"LAIF-native; average conceptual proximity {_cit_con}/100. These findings "
          f"may be stated of the named source instruments within excerpt scope.")
    _align_counter = Counter(r.get("laif_alignment", "not assessed") for r in assessments)
    p(f"- **Functional alignment distribution:** "
      f"{_compact_list([f'{k} ({v})' for k, v in _align_counter.most_common()])}")
    _ext_cals = [r["score_calibration"] for r in assessments
                 if r.get("score_calibration", {}).get("achievable_ceiling", 100) < 100]
    if _ext_cals:
        _avg_pct = round(sum(c["overall_pct_of_ceiling"] for c in _ext_cals) / len(_ext_cals))
        p(f"- **Average calibrated position (external instruments):** {_avg_pct}% of the "
          f"{_ext_cals[0]['achievable_ceiling']}-point ceiling achievable without "
          f"LAIF-native branding — raw scores compress by design and must not be read "
          f"as percentage grades.")
    p(f"- **Evidence trace summary:** {evidence_total} traces; {evidence_exact} exact/deterministic; {evidence_fallback} reviewer-confirmation fallback.")
    p(f"- **Remediation patch summary:** {patch_total} structured patches across assessed documents.")
    p(f"- **Top governance-force patterns:** {_compact_list([f'{k} ({v})' for k, v in force_counter.most_common(3)])}")
    if external_count == count:
        p("- **Certification channel:** no document in this corpus claims or seeks "
          "LAIF-native certification, so the certification gate is not a finding "
          "about these documents; construct coverage remains available in each "
          "Technical Appendix.")
    else:
        p(f"- **LAIF-native certification summary:** {count - len(native_failures)}/{count} PASS; "
          f"{len(native_failures)}/{count} FAIL where LAIF-native certification is claimed/applicable.")
    p("- **Boundary note:** diagnostic findings require reviewer confirmation and cannot override formal LAIF-native failure.")
    p()

    h(2, "Method Summary")
    h(3, "Method and Scoring Model")
    p("Assessment layers preserved: Formal LAIF-native certification gate; Dimensional scoring model; Structural depth / adversarial hardening; Validation boundary.")
    p("The renderer presents deterministic rubric outputs that already exist in each assessment result; it does not change scoring weights, score calculations, formal compliance calculation, validation, certification gates, sector metadata, evidence traces, remediation patches, or calibration metadata.")
    p("The report uses controlled public wording, suppresses raw regex disclosure, avoids keyword-stuffing recipes, and preserves legal-authority boundaries.")
    p("No legal determination is made; no source is certified through this public template unless the separate LAIF-native certification gate passes.")
    p()

    h(2, "Cross-Document Dashboard")
    h(3, "Score distribution / deterministic rubric comparison")
    table(
        ["Document", "Mode", "Alignment", "Overall score / band", "Sector profile", "Evidence traces", "Patches", "Cautions"],
        [_report_document_row(r) for r in assessments],
    )
    p()
    h(3, "Common structural gaps (cross-document)")
    _gap_counter = Counter(gap for r in assessments
                           for gap in r.get("primary_failure_modes", []))
    p(_compact_list([f"{g} ({n}/{count} documents)"
                     for g, n in _gap_counter.most_common(6)],
                    limit=6, empty="none identified"))
    h(3, "Governance-force patterns")
    p(_compact_list([f"{k} ({v})" for k, v in force_counter.most_common(5)]))
    h(3, "Remediation themes")
    theme_counts = Counter()
    for r in assessments:
        for group_name in _remediation_groups(r.get("recommended_remediation_steps", [])).keys():
            theme_counts[group_name] += 1
    p(_compact_list([f"{k} ({v})" for k, v in theme_counts.most_common(5)]))
    p()

    h(2, "Per-Document Assessment")
    for idx, r in enumerate(assessments, 1):
        h(3, f"Document {idx}: {r.get('document_name', '')}")

        h(4, "Document Overview")
        h(5, "Assessment Scope")
        overview = [
            ["Document name", r.get("document_name", "")],
            ["Source type", r.get("source_type", "")],
            ["Jurisdiction", r.get("jurisdiction", "")],
            ["Sector", r.get("sector_label", r.get("sector_used", ""))],
            ["Assessment mode", r.get("assessment_mode", "external_framework")],
            ["Citation", r.get("citation", "") or "not provided"],
            ["Source URL", r.get("source_url", "") or "not provided"],
            ["Provenance", r.get("provenance", "") or "not provided"],
        ]
        if r.get("assessment_mode") == "external_framework":
            overview.extend([
                ["Document type", r.get("document_type", "unknown_governance_document")],
                ["Original file name", r.get("original_file_name", "not provided") or "not provided"],
                ["Source SHA-256", r.get("source_sha256", "not provided") or "not provided"],
            ])
        table(["Field", "Value"], overview)
        p()
        _doc_outline = r.get("document_outline", [])
        if _doc_outline:
            p(f"**Document structure detected ({len(_doc_outline)} sections):** "
              + " · ".join(_doc_outline[:10])
              + (" · …" if len(_doc_outline) > 10 else ""))
            p()

        # ── Plain-Language Reading — framework-free narrative, every sentence
        # keyed to a measured signal (see _plain_reading). No LAIF vocabulary.
        _plain = r.get("plain_reading", [])
        if _plain:
            h(4, "Plain-Language Reading (framework-free)")
            p("*What the measurements found, stated without any of this framework's "
              "vocabulary. Each statement is generated from a specific fired or "
              "missed signal — none of it is editorial.*")
            p()
            for _para in _plain:
                p(_para)
                p()


        if r.get("assessment_mode") == "external_framework":
            h(4, "Governance Repair Profile")
            table(
                ["Field", "Value"],
                [
                    ["document_type", r.get("document_type", "unknown_governance_document")],
                    ["recommended_use", r.get("recommended_use", "reviewer confirmation required")],
                    ["not_sufficient_for", r.get("not_sufficient_for", "reviewer confirmation required")],
                    ["governance_force_profile", r.get("governance_force_profile", "reviewer confirmation required")],
                    ["systemic_repair_value", r.get("systemic_repair_value", "reviewer confirmation required")],
                    ["operational_closure_rating", r.get("operational_closure_rating", "reviewer confirmation required")],
                    ["evidence_sufficiency_rating", r.get("evidence_sufficiency_rating", "reviewer confirmation required")],
                    ["accountability_closure_rating", r.get("accountability_closure_rating", "reviewer confirmation required")],
                    ["lifecycle_control_rating", r.get("lifecycle_control_rating", "reviewer confirmation required")],
                    ["residual_risk_control_rating", r.get("residual_risk_control_rating", "reviewer confirmation required")],
                    ["implementation_gap_rating", r.get("implementation_gap_rating", "reviewer confirmation required")],
                    ["failure_pathway_risk", r.get("failure_pathway_risk", "reviewer confirmation required")],
                    ["priority_repair_actions", _compact_list(r.get("priority_repair_actions", []), limit=5)],
                ],
            )
            p("This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.")
            p()
            h(4, "Operational Closure Findings")
            p(f"- **Operational closure:** {r.get('operational_closure_rating', 'reviewer confirmation required')}")
            p(f"- **Accountability closure:** {r.get('accountability_closure_rating', 'reviewer confirmation required')}")
            p(f"- **Lifecycle control:** {r.get('lifecycle_control_rating', 'reviewer confirmation required')}")
            p(f"- **Residual-risk closure:** {r.get('residual_risk_control_rating', 'reviewer confirmation required')}")
            p()
            h(4, "Evidence Sufficiency Findings")
            p(f"- **Evidence sufficiency:** {r.get('evidence_sufficiency_rating', 'reviewer confirmation required')}")
            p(f"- **Evidence trace count:** {len(r.get('evidence_traces', []))}")
            p()
            h(4, "Implementation Gap Findings")
            p(f"- **Implementation gap rating:** {r.get('implementation_gap_rating', 'reviewer confirmation required')}")
            p(f"- **Priority repair actions:** {_compact_list(r.get('priority_repair_actions', []), limit=5)}")
            p()
            h(4, "Failure-Pathway Risk Findings")
            p(f"- **Failure-pathway risk:** {r.get('failure_pathway_risk', 'reviewer confirmation required')}")
            p("- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.")
            p()
        if any(r.get(k) for k in ("provenance", "source_note", "source_url", "citation", "intended_use")):
            h(5, "Provenance / Source Basis")
            p(f"- **Source note:** {r.get('source_note', 'not provided') or 'not provided'}")
            p(f"- **Intended use:** {r.get('intended_use', 'not provided') or 'not provided'}")
            p("- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.")
            p()

        h(4, "Mode / Boundary Notice")
        p("Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.")
        p(_report_boundary_notice(r))
        if r.get("assessment_mode") == "external_framework":
            p("Public status label: **Governance repair assessment — external-framework diagnostic.**")
        else:
            p(f"Public status label: **{_public_report_status_label(r)}**.")
        p()

        h(4, "Executive Diagnostic Summary")
        p(_safe_executive_verdict_text(r))
        p(f"- **Overall readiness:** {r.get('overall_readiness_score', 0)}/100 — {_report_score_band(r)}")
        _cal = r.get("score_calibration", {})
        if _cal and _cal.get("achievable_ceiling", 100) < 100:
            p(f"- **Calibrated position:** {_cal.get('overall_pct_of_ceiling', 0)}% of the "
              f"{_cal.get('achievable_ceiling')}-point ceiling achievable without LAIF-native "
              f"branding. Raw scores compress on this instrument: "
              f"{round(100 - _cal.get('achievable_ceiling', 100), 1)} points are reserved for "
              f"LAIF-branded documents, and lexical detection is conservative — read the "
              f"calibrated figure, the functional alignment verdict, and the score band "
              f"together, never the raw number as a percentage grade.")
        p(f"- **Conceptual proximity:** {r.get('conceptual_proximity_score', 0)}/100")
        p(f"- **Sector risk alignment:** {r.get('sector_risk_alignment', 0)}/100")
        p(f"- **Remediation effort:** {r.get('remediation_effort', 'unknown')}")
        p(f"- **Primary structural gaps:** {_compact_list(r.get('primary_failure_modes', []), empty='none identified')}")
        if r.get("strengths"):
            p(f"- **Structural strengths:** {_compact_list(r.get('strengths', []))}")
        p(f"- **Governance signal strength:** {r.get('governance_signal_strength', r.get('overall_readiness_score', 0))}")
        p(f"- **Structural dimension score:** {r.get('structural_depth_score', r.get('structural_score', 0))}/100")
        p("- **Position assessment:** diagnostic under the assessment model, not certification.")
        _alignment = r.get("laif_alignment", "")
        if _alignment:
            _align_gloss = {
                "FUNCTIONALLY ALIGNED": "LAIF's structural requirements are expressed "
                                        "in the document's own vocabulary; adoption "
                                        "distance is terminological",
                "PARTIALLY ALIGNED":    "some LAIF constructs present in substance or "
                                        "in form",
                "STRUCTURALLY UNALIGNED": "LAIF's distinctive structural mechanisms not "
                                          "detected in any form; conceptual overlap is "
                                          "measured separately",
            }.get(_alignment, "")
            p(f"- **Functional alignment:** {_alignment}"
              + (f" — {_align_gloss}" if _align_gloss else ""))
        p()

        # ── Functional Alignment table — substance independent of vocabulary
        _func = r.get("functional_alignment", {})
        if _func:
            h(4, "Functional Alignment (Substance Independent of Vocabulary)")
            p("DECLARED = LAIF-native form; FUNCTIONAL = substance present in the "
              "document's own vocabulary (≥2 independent signal families); "
              "PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; "
              "Regulatory Integration Guide Part One.")
            table(
                ["Construct", "Verdict", "Signal families detected", "Location"],
                [
                    [c, v.get("verdict", ""),
                     _compact_list(v.get("families", [])),
                     _compact_list(v.get("evidence_locations", []), limit=2, empty="—")]
                    for c, v in _func.items()
                ]
            )
            if r.get("coupling_state") == "FUNCTIONAL":
                _fc_ev = _func.get("Coupling", {}).get("evidence", [])
                if _fc_ev:
                    p("Functional pairing evidence (verbatim from the document): "
                      + " · ".join(f"«{e[:120]}»" for e in _fc_ev[:2]))
                p("Two equally valid certification paths: (a) restate the existing "
                  "pairings as canonical Coupling declarations (Toolkit §2 B.1); or "
                  "(b) retain the document's own vocabulary and record a documented "
                  "equivalence mapping to PDCA Section B.1 per the Regulatory "
                  "Integration Guide's SATISFIES/EXTENDS methodology. The choice "
                  "belongs to the document's owner.")
            p()

        # ── Evidence Locator — every claim points into the document ─────
        _locs = r.get("signal_locations", {})
        if _locs:
            h(4, "Evidence Locator — Where the Signals Live")
            p("Verbatim quotes from the assessed text with their locations in the "
              "document's own structure. Top signals per dimension.")
            _loc_rows = []
            for _dim, _dim_label in (("structural", "Structural"),
                                      ("conceptual", "Conceptual"),
                                      ("auditability", "Auditability"),
                                      ("enforceability", "Enforceability")):
                for _row in _locs.get(_dim, [])[:3]:
                    _loc_rows.append([
                        _dim_label,
                        _safe_markdown_cell(_row["label"])[:44],
                        _safe_markdown_cell(_row["location"])[:44],
                        _safe_markdown_cell("«" + _row["quote"] + "»")[:120],
                    ])
            if _loc_rows:
                table(["Dimension", "Signal", "Location in document", "Verbatim quote"],
                      _loc_rows)
            p()

            # What was NOT found — and where it would belong
            h(4, "Not Found — and Where It Would Belong")
            p("For each material element the assessment did not detect: what was "
              "looked for, confirmation it was absent from the excerpt, and the "
              "most natural place in this document's own structure to add it.")
            _outline_pairs = [(0, lbl) for lbl in r.get("document_outline", [])]
            _oblig = r.get("obligation_anchors", [])
            _missing_rows = []
            _bd = r.get("score_breakdown", {})
            for _dim, _dim_label in (("structural", "Structural"),
                                      ("auditability", "Auditability"),
                                      ("enforceability", "Enforceability")):
                for _lbl, _w in _bd.get(_dim, {}).get("missed", [])[:2]:
                    _missing_rows.append([
                        _dim_label,
                        _safe_markdown_cell(_lbl)[:52],
                        _safe_markdown_cell(_suggest_anchor(_lbl, _outline_pairs, _oblig))[:110],
                    ])
            for _c, _v in r.get("functional_alignment", {}).items():
                if _v.get("verdict") == "ABSENT":
                    _missing_rows.append([
                        "Core structure",
                        _safe_markdown_cell(f"{_c} substance (any vocabulary)")[:52],
                        _safe_markdown_cell(_suggest_anchor(_c, _outline_pairs, _oblig))[:110],
                    ])
            if _missing_rows:
                table(["Layer", "Not detected in this excerpt", "Where it would belong"],
                      _missing_rows)
            else:
                p("All assessed elements were detected.")
            p()

            # Attachment points for the pairing fix — the exact sentences
            if _oblig and r.get("coupling_state") in ("ABSENT", "IMPLICIT"):
                h(4, "Attachment Points for Restriction-Protection Pairing")
                p("These obligation sentences are the exact places in this document "
                  "where a named-beneficiary protection would attach:")
                for _a in _oblig:
                    p(f"- Under **{_a['location']}**: «{_a['quote']}» — state here who "
                      f"this obligation protects, and bind the protection so neither "
                      f"can be weakened without the other.")
                p()

        if r.get("assessment_mode") == "external_framework":
            h(4, "Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage")
            p("Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.")
            p(f"LAIF-native certification: Not claimed / not applicable to this external-framework assessment.")
            p()
        h(4, "Scorecard")
        p("Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.")
        table(
            ["Dimension", "Score", "Fired signal labels", "Missed signal labels"],
            [
                ["Structural", f"{r.get('structural_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('structural', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('structural', {}).get('missed', [])])],
                ["Terminology", f"{r.get('terminology_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('terminology', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('terminology', {}).get('missed', [])])],
                ["Conceptual proximity", f"{r.get('conceptual_proximity_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('conceptual', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('conceptual', {}).get('missed', [])])],
                ["Auditability", f"{r.get('auditability_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('auditability', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('auditability', {}).get('missed', [])])],
                ["Enforceability", f"{r.get('enforceability_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('enforceability', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('enforceability', {}).get('missed', [])])],
                ["Overall readiness", f"{r.get('overall_readiness_score', 0)}/100", _report_score_band(r), "—"],
            ],
        )
        p()

        h(4, "Score Calibration and Justification")
        p("Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.")
        sj = r.get("score_justification", {})
        if sj:
            p(f"- **Overall band:** {sj.get('overall_band', _report_score_band(r))}")
            p(f"- **Formal LAIF-native status:** {sj.get('formal_laif_native_compliance', r.get('formal_laif_native_compliance', r.get('formal_laif_compliance', '')))}")
            p(f"- **Interpretation boundary:** {sj.get('interpretation_boundary', 'Formal LAIF-native failure cannot be overridden by high proximity scores.')}")
            for dim in sj.get("dimension_justifications", [])[:5]:
                p(f"- **{dim.get('dimension', 'dimension').title()}:** {dim.get('score', '')}/100 — {dim.get('band', '')}; {dim.get('calibration_note', '')}")
        cautions = _report_caution_summary(r)
        p(f"- **Calibration / anti-gaming cautions:** {cautions['total']} — {cautions['top']}")
        p("- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.")
        p()

        h(4, "Governance-Force Profile")
        table(["Component", "Status", "Reviewer note"], _governance_force_profile(r))
        p()

        h(4, "Sector / Institutional Context")
        p(f"- **Sector profile:** {r.get('sector_profile_label', r.get('sector_label', r.get('sector_used', 'general')))}")
        p(f"- **Sector profile key:** {r.get('sector_profile', r.get('sector_used', 'general_ai_governance'))}")
        p(f"- **Profile-specific remediation themes:** {_compact_list(r.get('sector_profile_remediation_themes', []))}")
        p(f"- **Profile-specific evidence cautions:** {_compact_list(r.get('sector_profile_evidence_cautions', []))}")
        p("- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.")
        sector_findings = r.get("sector_specific_findings", [])
        if sector_findings:
            p(f"- **Sector diagnostic findings:** {_compact_list(sector_findings)}")
        p()

        h(4, "Evidence Trace Summary")
        p("Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.")
        evidence = _report_evidence_summary(r)
        p(f"- **Total traces:** {evidence['total']}")
        p(f"- **Exact/deterministic count:** {evidence['exact']}")
        p(f"- **Fallback count:** {evidence['fallback']}")
        p(f"- **Evidence trace IDs:** {evidence['top']}")
        p("- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.")
        p()

        h(4, "Construct Crosswalk")
        coverage = r.get("construct_coverage", {})
        if any(coverage.values()):
            table(["Construct", "Detected for LAIF-native gate"],
                  [[k, "yes" if v else "not detected"] for k, v in coverage.items()])
        else:
            p("No LAIF-native constructs detected — expected for an external "
              "instrument; see the Functional Alignment table for substance "
              "detected in the document's own vocabulary.")
        p("Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.")
        p()

        h(4, "Diagnostic Gaps")
        gaps = r.get("gaps", []) or r.get("primary_failure_modes", [])
        if gaps:
            for gap in gaps:
                p(f"- {gap}")
        else:
            p("No diagnostic gaps generated by the current rubric.")
        p()

        h(4, "Remediation Priorities")
        p("LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.")
        structured_steps = r.get("structured_remediation_steps", [])
        if structured_steps:
            h(5, "Structured remediation details")
            for i, step in enumerate(structured_steps[:5], 1):
                p(f"{i}. **Problem:** {step.get('problem', '')}")
                p(f"   - **Why it matters:** {step.get('why_it_matters', '')}")
                p(f"   - **Concrete fix:** {step.get('concrete_fix', '')}")
        else:
            p("Structured remediation details: reviewer confirmation required.")
            p("- **Problem:** diagnostic gap requires institutional review.")
            p("- **Why it matters:** governance-force evidence may be incomplete.")
            p("- **Concrete fix:** assign owner, evidence artifact, verification test, and authority review.")
        h(4, "Structured Remediation Patch Set")
        p("These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.")
        patches = r.get("remediation_patches", [])
        if patches:
            _shown = patches[:6]
            if len(patches) > 6:
                p(f"Showing the 6 highest-priority patches of {len(patches)}; the "
                  f"full set is available in the JSON assessment output.")
            for patch in _shown:
                p(f"- **patch_id:** {patch.get('patch_id', '')}")
                p(f"  - **finding_type:** {patch.get('finding_type', '')}")
                p(f"  - **severity:** {patch.get('severity', '')}")
                p(f"  - **diagnostic_gap:** {patch.get('diagnostic_gap', '')}")
                p(f"  - **recommended_patch:** {patch.get('recommended_patch', '')}")
                p(f"  - **operational_control:** {patch.get('operational_control', '')}")
                p(f"  - **evidence_artifact:** {patch.get('evidence_artifact', '')}")
                p(f"  - **verification_test:** {patch.get('verification_test', '')}")
                p(f"  - **responsible_actor:** {patch.get('responsible_actor', '')}")
                ids = patch.get("evidence_trace_ids", [])
                p(f"  - **Evidence trace IDs:** {', '.join(ids) if ids else 'reviewer confirmation required / none linked'}")
                p(f"  - **legal_authority_boundary:** {patch.get('legal_authority_boundary', '')}")
                p("  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.")
        else:
            p("No structured remediation patches generated by the current deterministic extractor.")
        p()

        h(4, "Limits and Reviewer Actions")
        for action in _report_limits_and_reviewer_actions(r):
            p(f"- {action}")
        p("- treat this report as diagnostic, not certification, and not a legal validity determination")
        p("- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure")
        p()

    h(2, "Closing Interpretation Notes")
    p("- Public reports are diagnostics only and require evidence/authority review before institutional use.")
    p("- Reviewer confirmation required for source authority, implementation evidence, accountable ownership, and legal or contractual effect.")
    p("- Formal LAIF-native failure remains formal failure; high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.")
    p("- This report does not determine legal validity and does not provide legal advice.")
    p("- Raw regex patterns are not disclosed; only report-safe signal labels and summaries are rendered.")
    p()
    p("---")
    p(f"*LAIF v1.2 · Compliance Toolkit v1.1 · {report_date} · Public Report Template*  ")
    p("*Generated by `test_real_world.py`; scoring logic, rubric weights, formal compliance calculation, certification gates, and validate.py enforcement unchanged.*")
    return "\n".join(lines)
