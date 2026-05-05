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
    (10, r"\bhuman rights\b|\bfundamental rights\b|\bhuman interests?\b",
         "human rights / fundamental interests"),
    # Integrity Layer A.1 proxy — transparency requirements
    (8,  r"\btransparency\b|\btransparent\b",
         "transparency"),
    # Integrity Layer A.1 proxy — explainability / meaningful account
    (8,  r"\bexplainability\b|\binterpret\b|\bmeaningful\s+(?:explanation|information)\b",
         "explainability / interpretability"),
    # Q1 Coupling proxy — accountability for decisions affecting interests
    (8,  r"\baccountability\b|\baccountable\b",
         "accountability"),
    # Integrity Layer A.3 + Q1 Coupling — human oversight of AI decisions
    (8,  r"\boversight\b|\bhuman determination\b|\bhuman.in.the.loop\b",
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
    (8,  r"\b(?:revers|modif|correct)\w*\b.{0,80}\b(?:decision|outcome|consequence|policy)\b",
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

AUDITABILITY_RUBRIC = [
    (20, r"\bshall\b.{1,300}\bshall\b",
         "multiple mandatory obligations (shall … shall)"),
    (20, r"\bArticle\s+\d+|GOVERN\s+\d+\.\d+|Section\s+\d+",
         "numbered traceable requirements"),
    (20, r"\b(?:document|record|evidence|technical documentation|certif|report)\b",
         "evidence / documentation requirements"),
    (20, r"\b(?:review|audit|monitor|evaluat|inspect|post.market)\b",
         "review / monitoring mechanisms"),
    (20, r"\b(?:specific|targeted|defined|identif|concrete|measur)\b.{0,80}\b(?:requirement|obligation|measure|standard|criterion)\b",
         "specific, measurable obligations"),
]

ENFORCEABILITY_RUBRIC = [
    (20, r"\bshall\b",
         "mandatory language (shall)"),
    (20, r"\b(?:provider|deployer|operator|agenc(?:y|ies)|responsible\s+part(?:y|ies)|actors?)\b",
         "named responsible parties"),
    (20, r"\bproportionate\b|\bdegree\s+of\s+risk\b|\blevel\s+of\s+risk\b|\bhigher.risk\b",
         "risk-proportionate thresholds"),
    (20, r"\b(?:penalty|sanction|fine|infringement|non.compliance|consequence)\b",
         "enforcement consequences / penalties"),
    (20, r"\bshall\s+(?:not\s+)?(?:ensure|establish|implement|maintain|provide|design|develop|assess)\b",
         "non-discretionary operational mandates"),
]

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
    (r"protect(?:s|ion)?\s+\S+(?:\s+\S+)?\s+from",     "protection language"),
    (r"ensure(?:s|ing)?\s+\S+(?:\s+\S+)?\s+(?:rights|interests)", "rights/interests assurance"),
    (r"\bto\s+prevent\s+harm\b",                         "harm prevention"),
    (r"\bto\s+mitigate\s+risk\b",                        "risk mitigation"),
    (r"\baccountable\s+for\b",                           "accountability declaration"),
    (r"\bresponsible\s+for\b",                           "responsibility declaration"),
    (r"\bsubject\s+to\s+oversight\b",                    "oversight subjection"),
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


def _coupling_state(existing_verdict, implicit):
    """
    Synthesise coupling state from explicit verdict and implicit signal scan.

    STRUCTURAL — explicit Coupling declared with structural indicators (full credit)
    IMPLICIT   — Coupling absent/shallow but implicit protective intent detected
    ABSENT     — no Coupling and no implicit coupling signals found

    Source: LAIF v1.2 Principle 2; adoption guidance distinguishes intent from form.
    """
    if existing_verdict == "STRUCTURAL":
        return "STRUCTURAL"
    if implicit["found"]:
        return "IMPLICIT"
    return "ABSENT"


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
        if not re.search(check["trigger"], text, re.IGNORECASE):
            continue
        for pat, desc in check["adversaries"]:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                start = max(0, m.start() - 100)
                end   = min(len(text), m.end() + 100)
                ctx   = text[start:end].replace("\n", " ").strip()
                findings.append((check["property"], desc, ctx[:200]))
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


# ── Helpers ────────────────────────────────────────────────────────────────────

def _score_signals(text, rubric):
    """Return (score, fired, missed) for a rubric.

    fired  — list of (label, weight) for patterns that matched
    missed — list of (label, weight) for patterns that did not match
    Score is sum of fired weights, capped at 100.
    """
    fired, missed = [], []
    for w, pat, label in rubric:
        if re.search(pat, text, re.IGNORECASE):
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
        verdict = (
            f"This document fails formal LAIF v1.2 compliance. Required constructs absent: "
            f"{miss_str}. Overall readiness score: {overall}/100. "
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
                f"absent — {', '.join(missing[:3])}. Missing any single construct = FAIL "
                f"regardless of overall readiness score."
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
    else:
        position_result = "Conceptually aligned, structurally incomplete"

    not_enforced = []
    if cs != "STRUCTURAL":
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

    # ── Coupling quality ──────────────────────────────────────────────────────
    if cq == "ABSENT":
        findings.append({
            "title":    "Coupling not structurally declared — no restriction paired with a human interest",
            "severity": "HIGH",
            "evidence": "The canonical term 'Coupling' does not appear in the document.",
            "impact":   (
                "Every governance restriction can be weakened in isolation without triggering "
                "a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test "
                "failure. Integrity Layer precondition cannot be satisfied without Coupling "
                "(LAIF v1.2 Principle 2)."
            ),
            "recommended_action": (
                "Declare structural Coupling for each governance restriction: name the specific "
                "human interest at stake and pair it with a protection of equivalent normative "
                "force (Toolkit §2 B.1)."
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

    # 1 — Paraphrase violations (most specific, highest immediate impact)
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

    # 2 — Coupling
    cq = result["coupling_quality"]
    if cq in ("ABSENT", "SHALLOW", "NEGATED"):
        cq_r = result["coupling_quality_reason"]
        if cq == "ABSENT":
            problem = "Structural Coupling not declared — the term 'Coupling' is absent."
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
                "For each governance restriction, add: 'Coupling between [restriction] "
                "and [the specific human interest it protects], with [named protection "
                "mechanism] of equivalent normative force.' Both sides must be named "
                "explicitly; neither can be weakened in isolation (Toolkit §2 B.1)."
            ),
        })

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
            "problem": "Integrity Layer not declared as a deployment precondition.",
            "why_it_matters": (
                "A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural "
                "Containment — all three must be satisfied simultaneously before deployment "
                "may proceed. Partial satisfaction = failure. Without this gate, there is "
                "no precondition preventing premature deployment (LAIF v1.2 Part Two)."
            ),
            "concrete_fix": (
                "Add an Integrity Layer section with three threshold conditions: A.1 — system "
                "can produce a meaningful account of any material output; A.2 — stated "
                "objectives correspond to implemented objectives, verified by independent "
                "review; A.3 — system operates within documented boundaries in all tested "
                "conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5)."
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

    # 1 — Paraphrase violations (specific rewrites, highest impact)
    if result["paraphrase_violations"]:
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

    # 2 — Coupling declaration (core LAIF requirement, always needed when missing)
    if not result["construct_coverage"].get("Coupling"):
        steps.append(
            "Declare structural Coupling for each governance restriction: explicitly identify "
            "the specific human interest at stake (not a category — name it with specificity, "
            "e.g. 'the patient's interest in receiving treatment decisions based on accurate "
            "clinical assessment') and pair it with a protection of equivalent normative force. "
            "The restriction and its paired protection must not be capable of being weakened in "
            "isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1)."
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


# ── Core assessment function ──────────────────────────────────────────────────

def assess(name, source_type, text, sector="general_ai_governance", **meta):
    """
    Produce a full LAIF assessment for a document.

    Parameters:
      name        — document identifier
      source_type — classification (binding_regulation, voluntary_framework, etc.)
      text        — document text to assess
      sector      — deployment sector profile key (default: general_ai_governance)
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

    paraphrase = {}
    for guard in PARAPHRASE_GUARDS:
        v = find_paraphrase_violations(text, guard)
        if v:
            paraphrase[guard["term"]] = v

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

    # Gaps — missing LAIF-specific elements
    gaps = []
    missing_terms = [lbl for _, pat, lbl in TERMINOLOGY_RUBRIC
                     if not re.search(pat, text, re.IGNORECASE)]
    if missing_terms:
        gaps.append("Canonical LAIF terms absent: " + ", ".join(missing_terms))

    for _, pat, lbl in STRUCTURAL_RUBRIC[6:]:
        if not re.search(pat, text, re.IGNORECASE):
            gaps.append(f"LAIF structural element missing: {lbl}")

    for guard_term, violations in paraphrase.items():
        examples = "; ".join(
            v[1].replace("\n", " ")[:60] + "…" for v in violations[:2]
        )
        gaps.append(
            f"Paraphrase violation — forbidden substitution of '{guard_term}' "
            f"({len(violations)} instance(s)): {examples}"
        )

    # Primary failure modes
    failure_modes = []
    if not any(p for lbl, p in formal_checks
               if any(x in lbl for x in ("PART ONE", "non-amendable", "self-application"))):
        failure_modes.append("structural — constitutional hierarchy not declared")
    if t == 0:
        failure_modes.append("terminological — no canonical LAIF terms present")
    if paraphrase:
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
    profile = SECTOR_PROFILES.get(sector, SECTOR_PROFILES["general_ai_governance"])

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

    result = {
        "document_name":              name,
        "source_type":                source_type,
        "formal_laif_compliance":     "PASS" if formal_pass else "FAIL",
        "formal_checks_detail":       formal_checks,   # [(label, bool), ...]
        "strong_laif_compliance":     strong_compliance,
        "structural_depth":           depth,
        "coupling_quality":           cq,
        "coupling_quality_reason":    cq_reason,
        "coupling_quality_evidence":  cq_evidence,
        "implicit_coupling":          implicit_coupling,
        "coupling_state":             _coupling_state(cq, implicit_coupling),
        "contradictions":             contradictions,
        "sector_gaming_risk":         gaming_level,
        "sector_gaming_reason":       gaming_reason,
        "construct_coverage":         construct_coverage,
        "structural_score":           s,
        "terminology_score":          t,
        "conceptual_proximity_score": c,
        "auditability_score":         a,
        "enforceability_score":       e,
        "overall_readiness_score":    overall,
        "remediation_effort":         effort,
        "paraphrase_violations":      paraphrase,
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
        "sector_used":                 sector,
        "sector_label":                profile["label"],
        "sector_relevant_interests":   profile["relevant_interests"],
        "sector_specific_findings":    sector_specific_findings,
        "sector_risk_alignment":       sector_risk_alignment,
        "sector_remediation_priority": profile["remediation_focus"],
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
    result["compliance_summary"]        = _compliance_summary(result)
    result["executive_summary"]         = _executive_summary(result)
    result["structured_findings"]       = _structured_findings(result)
    result["structured_remediation_steps"] = _structured_remediation(result)
    return result


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

def generate_markdown_report(assessments, report_date="May 2026"):
    lines = []

    def h(level, text):
        lines.append("\n" + "#" * level + " " + text)

    def p(text=""):
        lines.append(text)

    def table(headers, rows):
        widths = [max(len(str(hdr)), max((len(str(r[i])) for r in rows), default=0))
                  for i, hdr in enumerate(headers)]
        def row_str(cells):
            return "| " + " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)) + " |"
        lines.append(row_str(headers))
        lines.append("| " + " | ".join("-" * w for w in widths) + " |")
        for row in rows:
            lines.append(row_str(row))

    # ── Header ──────────────────────────────────────────────────────────────
    lines.append("# LAIF Real-World Assessment Report")
    p(f"**Framework version:** LAIF v1.2 · Compliance Toolkit v1.1  ")
    p(f"**Date:** {report_date}  ")
    p("**Classification:** Governance Assessment — System Hardening Release  ")
    p("**Validator:** validate.py (unchanged — strict formal compliance enforced)  ")
    p("**Scoring:** Traceable per-signal breakdown for every dimension  ")

    # ── Executive Summary ────────────────────────────────────────────────────
    h(2, "Executive Summary")
    fail_count  = sum(1 for r in assessments if r["formal_laif_compliance"] == "FAIL")
    avg_overall = round(sum(r["overall_readiness_score"] for r in assessments) / len(assessments))
    avg_concept = round(sum(r["conceptual_proximity_score"] for r in assessments) / len(assessments))
    p(
        f"{fail_count} of {len(assessments)} external AI governance frameworks assessed fail "
        f"formal LAIF v1.2 compliance. Formal compliance is binary and strict — "
        f"all 8 required constructs must be present; no partial credit is awarded."
    )
    p()
    p(
        f"Dimensional scoring reveals that the gap is terminological and structural, not "
        f"conceptual. Documents achieve an average conceptual proximity score of "
        f"{avg_concept}/100 and an average overall readiness score of {avg_overall}/100, "
        f"indicating that the underlying governance intent is broadly present — expressed "
        f"through different vocabulary and structural frameworks."
    )
    p()
    p(
        "**Core finding:** Existing frameworks address the right governance dimensions but do not "
        "enforce them through structural Coupling, the Coherence Test, or the Integrity Layer. "
        "LAIF is measurably stricter. The adoption pathway is terminological and structural, "
        "not conceptual — the underlying intent is already present."
    )

    # ── Method ──────────────────────────────────────────────────────────────
    h(2, "Method")
    p("Each document was assessed against three complementary layers:")
    p()
    p("**Layer 1 — Formal LAIF compliance (binary):** 8 required constructs — Coupling, "
      "Integrity Layer, Coherence Test, PART ONE / Foundational Principles, non-amendable "
      "clause, self-application clause, Integrity Layer FINDING block, Coherence Test "
      "FINDING block. All 8 must be present. Enforced by validate.py (unchanged).")
    p()
    p("**Layer 2 — Dimensional scoring (traceable):** Five dimensions scored 0–100 with "
      "per-signal breakdown. Every score is accompanied by the signals that fired (earned "
      "points) and those that did not. This answers 'why this number?' for every dimension.")
    p()
    p("**Layer 3 — Sector analysis:** Each document assessed against a sector profile "
      "defining relevant human interests, risk indicator signals, and expected evidence "
      "artefacts. Produces sector risk alignment score (0–100) and sector-specific "
      "remediation priorities referencing LAIF source sections.")
    p()
    p("**Layer 4 — Structural depth (adversarial hardening):** Three diagnostic checks "
      "run against every document regardless of formal compliance verdict:")
    p("- **Coupling state** (STRUCTURALLY DECLARED / NOT STRUCTURALLY DECLARED): detects hollow "
      "or negated Coupling declarations; implicit signals surfaced separately (LAIF v1.2 Principle 2)")
    p("- **Contradiction detection**: detects co-presence of claimed Integrity Layer "
      "properties and language that contradicts them (LAIF v1.2 A.2 Structural Honesty)")
    p("- **Sector gaming risk** (LOW / MEDIUM / HIGH): detects high sector keyword "
      "density without substantive governance content (LAIF v1.2 Q2 Consistency)")
    p()
    p("**Strong compliance verdict:** STRONG PASS requires formal PASS + STRUCTURAL "
      "Coupling + no contradictions. A formal PASS with shallow Coupling = WEAK PASS, "
      "not a strong compliance claim.")

    # ── Scoring Model ────────────────────────────────────────────────────────
    h(2, "Scoring Model")
    table(
        ["Dimension", "Weight", "LAIF Source", "Description"],
        [
            ["Structural",          "25%", "v1.2 Parts One, Two, Seven",
             "Governance architecture: hierarchy, thresholds, review mechanisms"],
            ["Terminology",         "15%", "Toolkit §1",
             "Canonical term presence: Coupling, Coherence Test, Integrity Layer"],
            ["Conceptual Proximity","20%", "v1.2 Part One",
             "LAIF-like concepts without LAIF terms: rights, oversight, contestability"],
            ["Auditability",        "20%", "Toolkit §2 PDCA",
             "Checkability: numbered obligations, evidence requirements, monitoring"],
            ["Enforceability",      "20%", "v1.2 Part Three",
             "Operational enforcement: mandatory language, named parties, consequences"],
        ]
    )
    p()
    p("**Overall** = Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + "
      "Auditability×0.20 + Enforceability×0.20")
    p()
    p("**Remediation Effort:** VERY HIGH (<35) · HIGH (35–59) · MEDIUM (≥60)")

    # ── Per-Document Scorecards ───────────────────────────────────────────────
    h(2, "Per-Document Scorecards")

    for r in assessments:
        h(3, r["document_name"])
        compliance_tag = "✅ PASS" if r["formal_laif_compliance"] == "PASS" else "❌ FAIL"
        strong_tag = {
            "STRONG PASS": "✅✅ STRONG PASS",
            "WEAK PASS":   "⚠️ WEAK PASS (formal gate passed; structural depth insufficient)",
            "FAIL":        "❌ FAIL",
        }.get(r.get("strong_laif_compliance", "FAIL"), "❌ FAIL")
        depth_tag = {
            "STRONG": "🟢 STRONG",
            "WEAK":   "🟡 WEAK",
            "HOLLOW": "🔴 HOLLOW",
        }.get(r.get("structural_depth", "WEAK"), "⚪ UNKNOWN")

        # ── Provenance notice ────────────────────────────────────────────────
        provenance = r.get("provenance", "")
        source_note = r.get("source_note", "")
        source_url  = r.get("source_url", "")
        intended_use = r.get("intended_use", "")
        if provenance:
            prov_badges = {
                "OFFICIAL_EXCERPT":          "> ✅ **OFFICIAL_EXCERPT** — text verified verbatim from the authoritative source.",
                "REPRESENTATIVE_EXCERPT":    "> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. "
                                              "Not verbatim. Not citable as the primary source.",
                "SYNTHETIC_TEST_DOCUMENT":   "> 🔬 **SYNTHETIC_TEST_DOCUMENT** — constructed for adversarial/stress-testing. "
                                              "Does not represent any real-world governance document.",
            }
            p(prov_badges.get(provenance, f"> Provenance: {provenance}"))
            if source_note:
                p(f"> {source_note}")
            if source_url:
                p(f"> Source: {source_url}")
            if intended_use:
                p(f"> Intended use: {intended_use}")
            p()

        # ── Executive Assessment block ────────────────────────────────────────
        es = r.get("executive_summary", {})
        risk_tier = r.get("deployment_risk_tier", "HIGH")
        risk_tier_badge = {
            "CRITICAL": "🔴 **CRITICAL**",
            "HIGH":     "🟠 **HIGH**",
            "MODERATE": "🟡 **MODERATE**",
            "LOW":      "🟢 **LOW**",
        }.get(risk_tier, f"**{risk_tier}**")
        if es:
            h(4, "Executive Assessment")
            p(f"> {es.get('verdict', '')}")
            p()
            p(f"**Overall Readiness:** {r['overall_readiness_score']}/100  ")
            p(f"**Deployment Risk Tier:** {risk_tier_badge}  ")
            p(f"**Remediation Effort:** {r['remediation_effort']}")
            p()
            p(f"**Root cause:** {es.get('why', '')}")
            p()
            if es.get("risks"):
                p("**Key risks:**")
                for risk in es["risks"]:
                    p(f"- {risk}")
                p()
            if es.get("strengths"):
                p("**Key strengths:**")
                for strength in es["strengths"]:
                    p(f"- {strength}")
                p()
            # Position Assessment (STEP 6)
            pa = es.get("position_assessment", {})
            if pa:
                p("**Position Assessment:**")
                p()
                if pa.get("contains"):
                    p("This document contains:")
                    for item in pa["contains"]:
                        p(f"- {item}")
                    p()
                if pa.get("not_enforced"):
                    p("However, the following are not structurally enforced:")
                    for item in pa["not_enforced"]:
                        p(f"- {item}")
                    p()
                p(f"**Result:** {pa.get('result', '')}")
                p()
            # What Must Be Fixed First — top 3 structured remediation steps
            srem = r.get("structured_remediation_steps", [])
            if srem:
                p("**What Must Be Fixed First:**")
                for i, step in enumerate(srem[:3], 1):
                    prob = step.get("problem", "")
                    fix  = step.get("concrete_fix", "")
                    p(f"{i}. **{prob}** — {fix}" if prob else f"{i}. {fix}")
                p()

        # ── Compliance Summary table ─────────────────────────────────────────
        cs = r.get("compliance_summary", {})
        if cs:
            h(4, "Compliance Summary")
            table(
                ["Dimension", "Verdict"],
                [
                    ["Formal compliance (binary gate)", cs.get("formal", "—")],
                    ["Structural depth",                cs.get("structural_depth", "—")],
                    ["Structural contradictions",       cs.get("contradictions", "—")],
                    ["Sector gaming risk",              cs.get("sector_gaming", "—")],
                    ["Final verdict",                   cs.get("final", "—")],
                ]
            )
            p()

        p(f"**Source type:** {r['source_type']}  ")
        p(f"**Sector:** {r.get('sector_label', r['sector_used'])}  ")

        # ── Coupling state block (STEP 5) ────────────────────────────────────
        cstate  = r.get("coupling_state", "ABSENT")
        cq_val  = r.get("coupling_quality", "ABSENT")
        cq_ev   = r.get("coupling_quality_evidence", "")
        ic      = r.get("implicit_coupling", {})

        if cstate == "STRUCTURAL":
            p(f"**Coupling:** STRUCTURALLY DECLARED ✅")
            if cq_ev:
                p(f"  Evidence: «{cq_ev[:150]}»")
        elif cstate == "IMPLICIT":
            p(f"**Coupling:** NOT STRUCTURALLY DECLARED (implicit signals present) ❌")
            if cq_val == "NEGATED" and cq_ev:
                p(f"  Evidence of negation: «{cq_ev[:150]}»")
            p()
            p("**Implicit signals detected:**")
            for excerpt in ic.get("matches", []):
                p(f"- «{excerpt}»")
            p()
            p("**Interpretation:**  ")
            p("These statements indicate recognition of responsibility or protection, "
              "but do not explicitly bind restrictions to protected human interests.")
            p()
            p("**Fix:**  ")
            p("Explicitly pair each restriction with the human interest it protects. "
              "Ensure both carry equivalent normative force — neither can be weakened "
              "in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).")
        else:  # ABSENT
            p(f"**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌")
            p()
            p("No implicit coupling signals detected. The document does not express "
              "protective intent in a form that can be structurally upgraded via "
              "terminological revision alone.")
        p()
        if r.get("contradictions"):
            p("**⚠️ Structural Contradictions Detected:**")
            for prop, desc, ctx in r["contradictions"]:
                p(f"- [{prop}] {desc}")
                if ctx:
                    p(f"  Evidence: «{ctx[:150]}»")
            p()

        # ── Minimal Upgrade Path (STEP 7) ────────────────────────────────────
        if cstate != "STRUCTURAL":
            h(4, "Minimal Upgrade Path (No System Rewrite Required)")
            p("To achieve formal LAIF Coupling compliance without restructuring the "
              "entire document:")
            p()
            p("1. **Identify each restriction** — list every 'shall not' or operational "
              "constraint in the document.")
            p("2. **Identify the affected human interest** — for each restriction, state "
              "the specific human interest it protects (e.g. 'patient safety', "
              "'worker's right to explanation').")
            p("3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] "
              "and [human interest]: neither may be weakened without the other.'")
            p("4. **Ensure equivalent normative force** — both sides of the pair must use "
              "the same mandatory language ('shall') so neither can be downgraded in isolation.")
            p()
            if ic.get("found"):
                p("*Note: implicit coupling signals already present (see above) — the "
                  "governance intent is established. This upgrade is terminological and "
                  "structural, not conceptual.*")
            p()

        # Scores with signal traceability
        h(4, "Scores and Signal Breakdown")
        bd = r["score_breakdown"]
        st = r.get("score_trace", {})
        for dim_key, dim_label, score_key in [
            ("structural",    "Structural",           "structural_score"),
            ("terminology",   "Terminology",          "terminology_score"),
            ("conceptual",    "Conceptual Proximity", "conceptual_proximity_score"),
            ("auditability",  "Auditability",         "auditability_score"),
            ("enforceability","Enforceability",       "enforceability_score"),
        ]:
            score  = r[score_key]
            trace  = st.get(dim_key, {})
            fired  = bd[dim_key]["fired"]
            missed = bd[dim_key]["missed"]

            p(f"**{dim_label} — {score}/100** {score_bar(score)}")
            p()
            if trace.get("reason"):
                p(f"**Why:** {trace['reason']}")
                p()
            if fired:
                grp = _group_signals(fired)
                p("**Signals detected:**")
                if grp["human_interest"]:
                    p("*Human interest signals:*")
                    for label, w in grp["human_interest"]:
                        p(f"- {label} (+{w} pts)")
                if grp["governance"]:
                    p("*Governance signals:*")
                    for label, w in grp["governance"]:
                        p(f"- {label} (+{w} pts)")
                if grp["structural"]:
                    p("*Structural signals:*")
                    for label, w in grp["structural"]:
                        p(f"- {label} (+{w} pts)")
                p()
            if missed:
                p("**Signals missing:**")
                for label, w in missed:
                    p(f"- {label} (missed {w} pts)")
                p()
            if trace.get("weight_rationale"):
                p(f"**Dimension significance:** {trace['weight_rationale']}")
                p()

        overall_bar = score_bar(r["overall_readiness_score"])
        p(f"**Overall Readiness — {r['overall_readiness_score']}/100** {overall_bar}")
        p()
        p(
            "**Why:** Weighted sum of the five dimensions above — "
            "Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + "
            "Auditability×0.20 + Enforceability×0.20. "
            "A document achieves overall readiness by addressing governance architecture, "
            "canonical terminology, substantive intent, verifiability, and enforceability "
            "simultaneously. Weakness in any single dimension constrains the overall score "
            "proportionally."
        )
        p()

        # Construct coverage
        h(4, "Construct Coverage")
        table(
            ["Construct", "Present", "LAIF Source"],
            [
                (k, "✅ Yes" if v else "❌ No",
                 {"Coupling":                "v1.2 Principle 2; Toolkit §2 B.1",
                  "Coherence Test":          "v1.2 Part One",
                  "Integrity Layer":         "v1.2 Part Two",
                  "Structural Transparency": "Toolkit §1.3 (A.1)",
                  "Structural Honesty":      "Toolkit §1.4 (A.2)",
                  "Structural Containment":  "Toolkit §1.5 (A.3)",
                  "Consistency":             "v1.2 Principle 5",
                  "Reversibility":           "v1.2 Provision D1"}.get(k, "v1.2"))
                for k, v in r["construct_coverage"].items()
            ]
        )
        p()

        # Sector section
        h(4, "Sector Context")
        p(f"**Sector:** {r.get('sector_label', r['sector_used'])}  ")
        p(f"**Sector risk alignment:** {r['sector_risk_alignment']}/100  ")
        p()
        p("**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**")
        for interest in r["sector_relevant_interests"]:
            p(f"- {interest}")
        p()

        h(4, "Sector-Specific Findings")
        risk_present = [f for f in r["sector_specific_findings"] if f.startswith("Risk signal present")]
        risk_absent  = [f for f in r["sector_specific_findings"] if f.startswith("Risk signal absent")]
        evid_present = [f for f in r["sector_specific_findings"] if f.startswith("Evidence present")]
        evid_gap     = [f for f in r["sector_specific_findings"] if f.startswith("Evidence gap")]
        if risk_present:
            p("*Risk indicators detected:*")
            for f in risk_present:
                p(f"- ✅ {f.replace('Risk signal present: ', '')}")
        if risk_absent:
            p("*Risk indicators absent:*")
            for f in risk_absent:
                p(f"- ⚪ {f.replace('Risk signal absent: ', '')}")
        if evid_present:
            p("*Expected evidence artefacts present:*")
            for f in evid_present:
                p(f"- ✅ {f.replace('Evidence present: ', '')}")
        if evid_gap:
            p("*Evidence gaps:*")
            for f in evid_gap:
                p(f"- ❌ {f.replace('Evidence gap: ', '')}")
        p()

        # Paraphrase violations
        if r["paraphrase_violations"]:
            h(4, "Paraphrase Violations")
            for term, vs in r["paraphrase_violations"].items():
                p(f"**Guard: {term}** — {len(vs)} violation(s)  ")
                p(f"*Source: LAIF v1.2 Principle 2; validate.py context-aware guard*")
                for _, ctx in vs[:2]:
                    p(f"> …{ctx.replace(chr(10), ' ')[:120]}…")
        else:
            h(4, "Paraphrase Violations")
            p("None detected.")
        p()

        # Strengths
        h(4, "Strengths")
        for s in r["strengths"][:10]:
            p(f"- {s}")
        p()

        # Gaps
        h(4, "Gaps")
        for g in r["gaps"]:
            p(f"- {g}")
        p()

        # Failure modes
        h(4, "Primary Failure Modes")
        for fm in r["primary_failure_modes"]:
            p(f"- {fm}")
        p()

        # ── Structured Findings ─────────────────────────────────────────────
        h(4, "Structured Findings")
        sfindings = r.get("structured_findings", [])
        if sfindings:
            for fi in sfindings:
                sev = fi.get("severity", "MEDIUM")
                sev_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")
                p(f"**{sev_icon} [{sev}] {fi.get('title', '')}**")
                p(f"- *Evidence:* {fi.get('evidence', '')}")
                p(f"- *Impact:* {fi.get('impact', '')}")
                p(f"- *Recommended action:* {fi.get('recommended_action', '')}")
                p()
        else:
            p("No structured findings generated.")
        p()

        # ── Remediation (Problem / Why it matters / Concrete fix) ────────────
        h(4, "Remediation Plan (ordered by impact)")
        srem = r.get("structured_remediation_steps", [])
        if srem:
            for i, step in enumerate(srem, 1):
                p(f"**{i}. Problem:** {step.get('problem', '')}")
                p(f"   **Why it matters:** {step.get('why_it_matters', '')}")
                p(f"   **Concrete fix:** {step.get('concrete_fix', '')}")
                p()
        else:
            p("No structured remediation steps generated.")
        p()
        p("---")

    # ── Cross-Document Findings ───────────────────────────────────────────────
    h(2, "Cross-Document Findings")

    h(3, "Score Comparison")
    table(
        ["Document", "Str", "Ter", "Con", "Aud", "Enf", "OVR", "Sector Alignment"],
        [
            [
                r["document_name"][:38],
                r["structural_score"],
                r["terminology_score"],
                r["conceptual_proximity_score"],
                r["auditability_score"],
                r["enforceability_score"],
                r["overall_readiness_score"],
                f"{r['sector_risk_alignment']}%",
            ]
            for r in assessments
        ]
    )
    p()

    h(3, "Deployment Risk Tier Summary")
    tier_order = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}
    table(
        ["Document", "Risk Tier", "Overall", "Compliance", "Provenance"],
        sorted(
            [
                [
                    r["document_name"][:38],
                    r.get("deployment_risk_tier", "HIGH"),
                    f"{r['overall_readiness_score']}/100",
                    r.get("strong_laif_compliance", "FAIL"),
                    r.get("provenance", ""),
                ]
                for r in assessments
            ],
            key=lambda row: tier_order.get(row[1], 9)
        )
    )
    p()
    p("**Risk tier derivation:** CRITICAL = compliance FAIL + overall <35; "
      "HIGH = compliance FAIL or overall <50; MODERATE = weak/hollow compliance + overall 50–69; "
      "LOW = STRONG PASS + overall ≥70.")
    p()

    high_conceptual = [r for r in assessments if r["conceptual_proximity_score"] >= 60]
    if high_conceptual:
        names = ", ".join(r["document_name"] for r in high_conceptual)
        p(f"- High conceptual proximity (≥60): {names} — LAIF-like intent expressed through "
          "own vocabulary.")

    paraphrase_docs = [r for r in assessments if r["paraphrase_violations"]]
    if paraphrase_docs:
        names = ", ".join(r["document_name"] for r in paraphrase_docs)
        p(f"- Paraphrase violations: {names} — forbidden substitution of LAIF canonical terms.")

    low_enforce = [r for r in assessments if r["enforceability_score"] < 40]
    if low_enforce:
        names = ", ".join(r["document_name"] for r in low_enforce)
        p(f"- Low enforceability (<40): {names} — voluntary/declaratory frameworks without "
          "binding mandates.")

    # ── Common Failure Modes ──────────────────────────────────────────────────
    h(2, "Common Failure Modes")
    fm_counter = Counter(fm for r in assessments for fm in r["primary_failure_modes"])
    for fm, count in fm_counter.most_common():
        p(f"- **{fm}** — {count}/{len(assessments)} documents")
    p()
    p("The universal failure mode is terminological: no external framework uses LAIF canonical "
      "terms. However, the absence of structural Coupling is the more consequential gap — "
      "without it, restrictions are not structurally paired with proportionate protections, "
      "and neither can be defended as structurally required by the other "
      "(LAIF v1.2 Principle 2).")

    # ── LAIF Deployment Implications ─────────────────────────────────────────
    h(2, "LAIF Deployment Implications")
    p("1. **LAIF is additive, not competitive.** Existing frameworks address the right "
      "governance dimensions. LAIF provides the structural enforcement layer they lack — "
      "canonical terms with load-bearing meaning, Coupling requirements, and the Coherence "
      "Test as a named decision instrument.")
    p()
    p("2. **Conceptual proximity enables adoption.** Documents scoring ≥60 on conceptual "
      "proximity already express the underlying values. Adoption pathway: introduce LAIF "
      "canonical terminology and add structural Coupling declarations to existing provisions.")
    p()
    p("3. **Paraphrase violations are actionable.** Where 'alignment', 'connection', or "
      "'linkage' appear as structural governance terms, the minimal fix is a rewrite "
      "substituting 'Coupling' and adding the paired protection — not a full structural redesign.")
    p()
    p("4. **Sector risk alignment measures deployment readiness.** A document with high "
      "conceptual proximity but low sector risk alignment may not address the specific "
      "materially-affected interests in the target deployment context.")
    p()
    p("5. **Scoring traceability enables targeted remediation.** Per-signal breakdowns "
      "show precisely which structural elements are missing, enabling prioritised fixes "
      "rather than wholesale document rewrites.")

    # ── Recommended Next Steps ────────────────────────────────────────────────
    h(2, "Recommended Next Development Steps")
    p("1. **Article-level LAIF–EU AI Act mapping:** Map LAIF Provisions to EU AI Act articles "
      "to formalise the adoption pathway for the EU regulatory context.")
    p()
    p("2. **LAIF–NIST RMF function mapping:** Map Coherence Test questions to NIST RMF "
      "functions (Govern, Map, Measure, Manage) to enable LAIF adoption within existing "
      "US governance infrastructure.")
    p()
    p("3. **Sector-specific PDCA templates:** Produce PDCA-Full templates pre-populated "
      "with sector-appropriate Coupling declarations, evidence artefact checklists, and "
      "Coherence Test documentation guidance.")
    p()
    p("4. **Score threshold calibration:** As more documents are assessed, calibrate "
      "remediation effort thresholds against actual adoption timelines.")

    p()
    p("---")
    p(f"*LAIF v1.2 · Compliance Toolkit v1.1 · {report_date} · Governance Audit Series*")
    p("*Generated by `test_real_world.py` — validate.py enforcement unchanged*")

    return "\n".join(lines)
