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

    Returns (quality, reason):
      STRUCTURAL — declared with named human interest and paired protection
      SHALLOW    — mentioned without structural declaration
      NEGATED    — present but explicitly negated or declared inapplicable
      ABSENT     — not present in document
    """
    if not re.search(r"\bCoupling\b", text, re.IGNORECASE):
        return "ABSENT", "Coupling not present in document"

    # Negation takes priority — most adversarial case
    for pat in COUPLING_NEGATION_INDICATORS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 60)
            end   = min(len(text), m.end() + 60)
            ctx   = text[start:end].replace("\n", " ").strip()
            return "NEGATED", f"Coupling negated/inapplicable: «{ctx[:120]}»"

    # Structural indicators
    for pat in COUPLING_STRUCTURAL_INDICATORS:
        if re.search(pat, text, re.IGNORECASE | re.DOTALL):
            return "STRUCTURAL", (
                "Coupling declared with structural indicators — 'between X and Y', "
                "named human interest, or equivalent normative force present"
            )

    # Hollow/referential usage
    for pat in COUPLING_HOLLOW_INDICATORS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 60)
            end   = min(len(text), m.end() + 60)
            ctx   = text[start:end].replace("\n", " ").strip()
            return "SHALLOW", f"Coupling referenced but not declared: «{ctx[:120]}»"

    # Term present without any structural or hollow indicator
    return "SHALLOW", (
        "Coupling mentioned without structural declaration — no 'between X and Y', "
        "no named human interest, no equivalent normative force"
    )


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
    cq, cq_reason        = _coupling_quality(text)
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
        "strong_laif_compliance":     strong_compliance,
        "structural_depth":           depth,
        "coupling_quality":           cq,
        "coupling_quality_reason":    cq_reason,
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
    return result


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
    p("- **Coupling quality** (STRUCTURAL / SHALLOW / NEGATED / ABSENT): detects hollow "
      "or negated Coupling declarations (LAIF v1.2 Principle 2)")
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

        p(f"**Formal LAIF Compliance:** {compliance_tag}  ")
        p(f"**Strong Compliance:** {strong_tag}  ")
        p(f"**Structural Depth:** {depth_tag}  ")
        p(f"**Coupling Quality:** {r.get('coupling_quality', 'ABSENT')} — {r.get('coupling_quality_reason', '')}  ")
        p(f"**Source type:** {r['source_type']}  ")
        p(f"**Sector:** {r.get('sector_label', r['sector_used'])}  ")
        p(f"**Sector Gaming Risk:** {r.get('sector_gaming_risk', 'LOW')}  ")
        p(f"**Remediation Effort:** {r['remediation_effort']}")
        if r.get("contradictions"):
            p()
            p("**⚠️ Structural Contradictions Detected:**")
            for prop, desc, ctx in r["contradictions"]:
                p(f"- [{prop}] {desc}: «{ctx[:100]}»")
        p()

        # Scores with signal traceability
        h(4, "Scores and Signal Breakdown")
        bd = r["score_breakdown"]
        for dim_key, dim_label, score_key in [
            ("structural",    "Structural",           "structural_score"),
            ("terminology",   "Terminology",          "terminology_score"),
            ("conceptual",    "Conceptual Proximity", "conceptual_proximity_score"),
            ("auditability",  "Auditability",         "auditability_score"),
            ("enforceability","Enforceability",       "enforceability_score"),
        ]:
            score = r[score_key]
            p(f"**{dim_label}: {score}/100** {score_bar(score)}")
            fired  = bd[dim_key]["fired"]
            missed = bd[dim_key]["missed"]
            if fired:
                for label, w in fired:
                    p(f"  + {label} (+{w})")
            if missed:
                for label, w in missed:
                    p(f"  − {label} (0/{w})")
            p()
        overall_bar = score_bar(r["overall_readiness_score"])
        p(f"**Overall Readiness: {r['overall_readiness_score']}/100** {overall_bar}  "
          f"(Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + "
          f"Enforceability×0.20)")
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

        # Sector-aware remediation
        h(4, "Sector-Aware Remediation (ordered by impact)")
        for i, step in enumerate(r["recommended_remediation_steps"], 1):
            p(f"{i}. {step}")
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
