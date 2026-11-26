"""LAIF engine: detection. Moved without changing assessment rules."""

from bisect import bisect_left
import re
from laif_spec import INTEGRITY_LAYER
from .source_spans import (
    _quote_at,
)


def integrity_requirement_diagnostics(text):
    """Locate requirement signals, not proof of behavioural properties.

    Non-matches mean NOT_DETECTED, never that a protection is absent. This
    reporting-only map does not contribute to scores or formal verdicts.
    """
    families = dict(FUNCTIONAL_CONSTRUCT_FAMILIES["Integrity Layer"])
    patterns = {
        "Structural Transparency": families["meaningful account of outputs"],
        "Structural Honesty": families["stated-vs-implemented correspondence"],
        "Structural Containment": families["bounded operation with escalation"],
        "Structural Calibration": [
            r"(?:confidence|uncertainty|probabilit\w*)\b.{0,180}\b(?:calibrat\w*|observed accuracy|empirical\w*|real.world performance)\b",
            r"(?:calibrat\w*|observed accuracy|empirical\w*|real.world performance)\b.{0,180}\b(?:confidence|uncertainty|probabilit\w*)\b",
        ],
    }
    records = []
    for identifier, name in INTEGRITY_LAYER.items():
        match = next((m for pattern in patterns[name]
                      if (m := re.search(pattern, text, re.I | re.S))), None)
        records.append({
            "property_id": identifier, "property": name,
            "source_section": "2.5" if identifier == "A.4" else "2." + identifier[-1],
            "signal_status": "DETECTED_REQUIRES_REVIEW" if match else "NOT_DETECTED_REQUIRES_REVIEW",
            "matched_text": match.group(0) if match else "",
            "start_char": match.start() if match else None,
            "end_char": match.end() if match else None,
            "applicability": "Section 2.5 trigger must be established" if identifier == "A.4" else "Assess instrument requirements separately from deployment behaviour",
            "determination": "NOT_ASSESSED_BY_PATTERN_MATCHING",
        })
    return records


# ── Scoring rubrics ────────────────────────────────────────────────────────────
# Each rubric is a list of (weight, pattern, label) tuples.
# Weights within each rubric sum to 100.
# Source comments link each signal to the LAIF section that requires it.

# Control registers, RACI tables, DPIA matrices and assurance schedules express
# obligations in table form rather than in sentences. A row that pairs a control
# with an owner — and often a trigger, a threshold, and a consequence — binds an
# actor to an action exactly as an operative sentence does, and is frequently a
# more precise specification than prose. Detection must recognise that form:
# these documents carry no "shall" and would otherwise read as having no
# obligations at all.
_CONTROL_REGISTER_HEADER = (
    r"\|[^\n|]{0,60}\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\b"
    r"[^\n]{0,200}\|[^\n|]{0,60}\b(?:owner|accountable|responsible|role|lead)\b"
)
# The same header the other way round (owner column before control column).
_CONTROL_REGISTER_HEADER_ALT = (
    r"\|[^\n|]{0,60}\b(?:owner|accountable|responsible|role|lead)\b"
    r"[^\n]{0,200}\|[^\n|]{0,60}\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\b"
)
CONTROL_REGISTER_PAT = f"(?:{_CONTROL_REGISTER_HEADER}|{_CONTROL_REGISTER_HEADER_ALT})"
# A populated register: the header plus at least two data rows beneath it.
CONTROL_REGISTER_POPULATED_PAT = (
    CONTROL_REGISTER_PAT + r"[^\n]*\n(?:\|[^\n]*\n){3,}"
)

# Source: LAIF v1.2 Part One — Foundational Principles define the structural
# requirements; Part Two defines Integrity Layer threshold conditions;
# Part Three defines Provision Layer; Part Seven defines Self-Application.
STRUCTURAL_RUBRIC = [
    # ── General governance architecture (external frameworks can score here) ──
    (8,  r"\bArticle\s+\d+|GOVERN\s+\d+\.\d+|Section\s+\d+\.?\d*",
         "numbered sub-requirements"),
    (8,  r"\bshall\b|\bmust\b|" + CONTROL_REGISTER_PAT,
         "mandatory obligation language (shall/must)"),
    (6,  r"\blifecycle\b|\blife.cycle\b|\bchange\s+control\b|\bre.approval\b|\bpost.deployment\b|\bpost.implementation\b|\bretrain\w*\b|\b(?:decommission|retire|withdraw)\w*\b.{0,60}\b(?:system|model|service|tool)\b|\bmaterial\s+change\b",
         "full lifecycle scope declared"),
    (7,  r"\bproportionat|\bhigh.risk\b|\brisk.{0,5}(?:level|categor|classif)",
         "risk stratification / proportionality"),
    (6,  r"\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\b|\b(?:deployment|approval|assurance)\s+gate\b|\bconditions?\s+of\s+use\b|\bconditions\b.{0,60}\bmust\s+be\s+(?:satisfied|met)\b",
         "operational mechanisms defined"),
    (6,  r"\b(?:monitor|audit|review|inspect|evaluat)\b",
         "review / monitoring mechanisms"),
    # ── LAIF-specific structural elements ─────────────────────────────────────
    # Source: LAIF v1.2 Part Two — Integrity Layer threshold: all three
    # preconditions must be satisfied simultaneously; partial = failure.
    (15, r"\bprecondition\b|all\s+(?:three|four|five)\s+(?:must|shall)\b|\bsimultaneously\b|\bat\s+the\s+same\s+time\b|all\s+of\s+the\s+following\b.{0,80}\b(?:are\s+satisfied|hold|apply|must)|(?:some\s+but\s+not\s+all|partial\s+(?:satisfaction|compliance))\b.{0,80}\bis\s+not\s+approval\b",
         "threshold gate conditions (all must pass simultaneously)"),
    # Source: LAIF v1.2 Part Two operationalisation note and Part Eight — hierarchy; non-amendable clause
    # prevents operational revision from eroding Foundational Principles.
    (18, r"\bPART ONE\b|FOUNDATIONAL PRINCIPLES|cannot be amended|non.amendable"
         r"|\bin the event of (?:any\s+)?(?:a\s+)?conflict\b.{0,140}\b(?:prevail|take[s]?\s+precedence|govern)"
         r"|\bnothing in this\b.{0,140}\b(?:derogat|limit|override|affect|prejudice)"
         r"|\b(?:is|are|shall be)\s+subordinate to\b|\btakes?\s+precedence over\b|\bprevails?\s+over\b"
         r"|\bshall not be (?:waived|derogated from|disapplied)\b|\bnot subject to waiver\b"
         r"|\bmay only be amended by\b|\bwithout prejudice to\b"
         r"|\bhierarchy of\b.{0,60}\b(?:documents|policies|standards|provisions|instruments)\b"
         r"|\b(?:issued|made|established)\s+under\s+the\b.{0,60}\b(?:framework|policy|charter|constitution|act|regulation)\b",
         "provision hierarchy / precedence rule"),
    # Source: LAIF v1.2 Part Seven — Self-Application: governance actors and
    # regulatory bodies are subject to the framework, not only AI operators.
    # Function: the document binds the body that issued it, not only the systems
    # it governs. LAIF states this in Part Seven; a bank standard writes "Group
    # Risk is itself subject to this Standard"; a university policy writes
    # "Academic Board are themselves subject to this policy"; a regulator writes
    # "this authority documents its own compliance". All bind the governing actor.
    (12, r"self.application|applies to regulatory|applies to governance actors"
         r"|\b(?:is|are)\s+(?:itself|themselves)\s+(?:subject\s+to|bound\s+by)\b"
         r"|\bapplies?\s+to\s+(?:this\s+\w+|us|the\s+\w+\s+function|the\s+authority)\s+itself\b"
         r"|\b(?:evidence|demonstrate|document|report|prove)\s+(?:its|their)\s+own\s+compliance\b"
         r"|\bsame\s+(?:evidentiary\s+)?standard\s+it\s+(?:demands|requires|applies)\b",
         "governing body bound by its own rules (self-application)"),
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
    (10, r"\bhuman rights\b|\bfundamental rights\b|\bhuman interests?\b|\bperson.level stakes?\b|\baffected persons?\b|\bbeneficiar|\bcivil rights\b|\bdata subjects?\b|\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\u2019)?s?\s+(?:interest|right)s?\b|\brights?\s+of\s+(?:the\s+)?(?:applicant|customer|patient|employee|individual|person)\b",
         "human rights / fundamental interests"),
    # Integrity Layer A.1 proxy — transparency requirements
    (8,  r"\btransparency\b|\btransparent\b|\bmeaningful account\b|\bshows? its work\b|\bdisclos\w+\b.{0,80}\b(?:limitation|basis|logic|criteria|use\s+of\s+ai)\b|\b(?:publish|state|record)\w*\b.{0,60}\bbasis\s+(?:for|of)\s+(?:the\s+)?(?:decision|output|determination)\b|\binformed\s+that\b.{0,80}\bautomated\b|\bplain.(?:language|english)\b.{0,60}\b(?:account|explanation|statement|information)\b",
         "transparency"),
    # Integrity Layer A.1 proxy — explainability / meaningful account
    (8,  r"\bexplainability\b|\binterpret\b|\bmeaningful\s+(?:explanation|information)\b|explain (?:any|each|every) decision|\bin plain language\b|words you can understand|\bexplanation\s+of\s+(?:any|each|every|an?|the)\b.{0,50}\bdecision\b|\bexplain\w*\b.{0,60}\b(?:individual|specific|each)\s+(?:decision|output|determination)\b|\breasons?\s+for\s+(?:the|any|each|its)\s+(?:decision|outcome|determination)\b|\bunderstand\s+and\s+contest\b|\baccount\s+of\s+(?:why|how)\b.{0,80}\b(?:output|decision|result|determination)\b",
         "explainability / interpretability"),
    # Q1 Coupling proxy — accountability for decisions affecting interests
    (8,  r"\baccountability\b|\baccountable\b|records? sufficient for audit|\bauditors?\b|\binternal\s+audit\b|\bowner\s*:|\b(?:model|system|product|risk|service|process|data|business)\s+owners?\b|\bsenior\s+responsible\s+owner\b|\breportable\s+(?:control\s+)?breach\b|\bresponsible\s+for\b.{0,80}\b(?:compliance|discharg\w+|the\s+decision)\b|\|\s*(?:owner|accountable|responsible)\s*\|",
         "accountability"),
    # Integrity Layer A.3 + Q1 Coupling — human oversight of AI decisions
    (8,  r"\boversight\b|\bhuman determination\b|\bhuman.in.the.loop\b|escalat\w+ to a human|human (?:being )?must approve|independent review\w*|\bhuman\s+review\b|\bhuman\s+decision.?maker\b|\bhuman\s+intervention\b|\bmanual\s+review\b|\breview\w*\s+by\s+a\s+(?:human|person|clinician|officer|manager|reviewer)\b|\b(?:routed|referred)\s+to\s+a\s+human\b",
         "human oversight"),
    # Q2 Consistency proxy — proportionality across scales and actors
    (8,  r"\bproportionat|\brisk.{0,5}(?:level|proportion)",
         "proportionality"),
    # Q1 Coupling proxy — safety as a named human interest
    (7,  r"\bsafety\b",
         "safety"),
    # Q1 Coupling proxy — contestability and redress (Provision A, D)
    (9,  r"\bcontest\w*\b|\bappeal\b|\bchallenge\b|\bredress\b|\bremedies\b|\brequest\s+(?:\w+\s+){0,2}review\s+of\s+(?:any|the|a)\s+decision\b|\bright\s+(?:to|of)\s+(?:human|academic|independent|manual)?\s*review\b|\bcomplaints?\s+(?:process|procedure|route|handling)\b",
         "contestability / redress"),
    # Q3 Reversibility proxy — modifiability of decisions and consequences
    (8,  r"\b(?:revers|modif|correct)\w*\b.{0,80}\b(?:decision|outcome|consequence|policy)\b|power to reverse|can always appeal|\b(?:overturn|rescind|quash|set\s+aside)\w*\b.{0,60}\b(?:decision|outcome|determination)\b|\b(?:suspend|withdraw|revoke|roll\s*back|decommission|disable)\w*\b.{0,60}\b(?:use|system|model|deployment|service|tool)\b|\buse\s+(?:is\s+|to\s+be\s+|must\s+be\s+)?(?:suspended|paused|halted)\b|\bsubstitute\s+(?:their|its)\s+own\s+(?:decision|determination|judgement|judgment)\b",
         "reversibility / modifiability"),
    # Q1/Q2 proxy — risk governance as structured process
    (8,  r"\brisk\s+(?:management|assessment|governance|control|framework|committee|appetite|register|tolerance|owner)\w*\b|\b(?:model|operational|clinical|credit|conduct)\s+risk\b|\brisk.based\b",
         "risk governance"),
    # Integrity Layer A.1 proxy — traceability of outputs and decisions
    (10, r"\btraceability\b|\btraceable\b|\bresponsibility\b.{0,30}\b(?:outcome|system|decision)\b|\baudit\s+trail\b|\bchain\s+of\s+custody\b|\b(?:record|log|register)\w*\b.{0,60}\b(?:each|every|all|the)\s+(?:decision|outcome|change|override)s?\b|\bversion\s+control\b",
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
    (20, r"\bshall\b.{1,300}\bshall\b|\bmust\b.{1,300}\bmust\b|" + CONTROL_REGISTER_POPULATED_PAT,
         "multiple mandatory obligations (shall/must pairs)"),
    (20, r"\bArticle\s+\d+|GOVERN\s+\d+\.\d+|Section\s+\d+|Part\s+\d+\b",
         "numbered traceable requirements"),
    (20, r"\b(?:document|record|evidence|technical documentation|certif|report)\b",
         "evidence / documentation requirements"),
    (20, r"\b(?:review|audit|monitor|evaluat|inspect|post.market)\b",
         "review / monitoring mechanisms"),
    (20, r"\b(?:specific|targeted|defined|identif|concrete|measur)\b.{0,80}\b(?:requirement|obligation|measure|standard|criterion)\b|\bwithin\s+\d+\s+(?:working\s+|business\s+|calendar\s+)?(?:day|hour|week|month|year)s?\b|\b(?:above|below|exceed\w*|outside|greater\s+than|less\s+than)\b.{0,40}\d+\s*%|\b(?:monthly|quarterly|annual(?:ly)?|weekly|biannual\w*)\b.{0,80}\b(?:review|monitor|report|assess|audit|attest)\w*|\b(?:review|monitor|report|assess|audit|attest)\w*\b.{0,60}\b(?:monthly|quarterly|annual(?:ly)?|weekly)\b",
         "specific, measurable obligations"),
]

ENFORCEABILITY_RUBRIC = [
    (20, r"\bshall\b|\bmust\b|\bwe\s+will\s+(?:never|not)\b|" + CONTROL_REGISTER_PAT,
         "mandatory language (shall/must)"),
    (20, r"\b(?:provider|deployer|operator|agenc(?:y|ies)|responsible\s+part(?:y|ies)|actors?|authorit(?:y|ies)|organisations?)\b|\b(?:chief|group|senior|head)\s+[\w-]+\s+(?:officer|executive)\b|\b[\w-]+\s+committee\b|\bboard\s+of\s+[\w-]+\b|\binternal\s+audit\b|\b(?:model|system|product|risk|service|process|data|business)\s+owners?\b|\bowner\s*:|\bsenior\s+responsible\s+owner\b|\b(?:data\s+)?controller\b|\bsuppliers?\b|\bvendors?\b|\bcontractors?\b|\bhead\s+of\s+[\w-]+\b",
         "named responsible parties"),
    (20, r"\bproportionate\b|\bdegree\s+of\s+risk\b|\blevel\s+of\s+risk\b|\bhigher.risk\b|commensurate\s+with\b|\bthresholds?\b|\btolerances?\b|\bmaterialit(?:y|ies)\b|\b(?:above|below|exceed\w*|outside|breach\w*|falls?\s+below)\b.{0,40}(?:\d+\s*%|\b(?:tolerances?|limits?|thresholds?)\b)|\brisk.(?:based|tier\w*|rat\w+)\b",
         "risk-proportionate thresholds"),
    (20, r"\b(?:penalty|sanction|fine|infringement|non.complian|consequence|suspension|suspended|revok|terminat|disqualif|forfeit|withdraw|paused?|halt|cease)\w*\b|\bmaterial breach\b|\bbreach of (?:contract|this \w+)\b|\breportable (?:control )?breach\b|\b(?:rejected|refused|not accepted)\b.{0,60}\b(?:evidence|response|submission|application)\b|\b(?:evidence|response|submission)\b.{0,60}\b(?:will be |shall be )?rejected\b",
         "enforcement consequences / penalties"),
    (20, CONTROL_REGISTER_POPULATED_PAT + r"|\b(?:shall|must)\s+(?:not\s+)?(?:ensure|establish|implement|maintain|provide|design|develop|assess|approve|produce|operate|name|document|monitor|report|escalate|evidence|record|review|verify|notify|suspend|obtain|submit|demonstrate|comply|retain|publish|test|validate|apply|complete|register)\b|\b(?:shall|must)\s+be\s+\w+ed\b|\brequires?\s+(?:re.)?(?:approval|authoris\w+|authoriz\w+|sign.off)\b|\bno\s+\w+(?:\s+\w+)?\s+(?:enters?|proceeds?|may|shall|is\s+\w+ed)\b.{0,80}\bunless\b",
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
# Frames in which a "Coupling: not satisfied" statement is the framework or an
# assessor APPLYING the Coherence Test to a case, rather than a document
# disclaiming Coupling for itself.
_ANALYTICAL_FRAME_PAT = re.compile(
    # The Coherence Test being applied to a case, in any of its three questions.
    r"\bQ[123]\b\s*(?:[—–:-]|\u2014)|\bQ[123]\b.{0,60}\b(?:Coupling|Consistency|Reversibility)\b|"
    r"\bCoherence\s+Test\b|\bScale\s*:|\bCase\s+\d|\b(?:worked\s+)?example\b|"
    r"\billustrat\w+|\bapplying\b|\bassessment\s+of\b|\bverdict\b|"
    r"\bFINDING\b|\bwould\s+(?:fail|not\s+satisfy)\b|\bfail(?:s|ed)?\s+Q[123]\b|"
    r"\bstructural\s+verdict\b|\bretrospective\b|"
    # An assessment record describing the instrument it is assessing: the
    # provisions a case engages, the thresholds a documented failure mode
    # satisfies, and the configuration under assessment. A document that is
    # genuinely refusing disclosure does not write in this register.
    r"\bProvisions?\s+Engaged\b|\bLAIF\s+Provisions?\b|"
    r"\bdocumented\s+failure\s+modes?\b|\bfailure\s+modes?\s+documented\b|"
    r"\bProvision\s+[A-D]\d\b.{0,60}\bthreshold\b|"
    r"\bas\s+assessed\b|\bassessed\s+configuration\b|"
    r"\bSection\s+[A-D]\b.{0,40}\bidentif\w+|\bunder\s+assessment\b",
    re.IGNORECASE | re.DOTALL,
)

# A document is an assessment instrument only if it writes in that register
# throughout, not once. Requiring several markers means a document that
# disclaims a protection cannot escape the contradiction finding by dropping a
# single analytical phrase near it.
_ANALYTICAL_INSTRUMENT_MIN_MARKERS = 3

# "cannot be undone" is an assertion of irreversibility; "does not permanently
# foreclose" is an assertion of the opposite. The first is already negative and
# must be read as written; the second is an adversary word under a negation.
_NEGATIVE_CONSTRUCTION_PAT = re.compile(
    r"\b(?:cannot|can\s?not|no|not|never|without)\b", re.IGNORECASE)
_NEGATION_PREFIX_PAT = re.compile(
    r"\b(?:does|do|shall|will|must|may|can|is|are|would)\s+not\s+(?:\w+\s+){0,3}$"
    r"|\bnot\s+(?:\w+\s+){0,3}$|\bnever\s+(?:\w+\s+){0,3}$",
    re.IGNORECASE)

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

    # A document that declares Coupling structurally AND separately works
    # through a case where Coupling is not satisfied is APPLYING the test, not
    # disclaiming it. LAIF's own principal text, its case analyses, and any
    # PDCA that records a Q1 failure all read that way. Analysing a failure is
    # not committing it — the same rule the contradiction layer applies to
    # language that regulates a hazard.
    _declares_structurally = any(
        re.search(pat, text, re.IGNORECASE | re.DOTALL)
        for pat in COUPLING_STRUCTURAL_INDICATORS
    )

    # Negation takes priority — most adversarial case
    for pat in COUPLING_NEGATION_INDICATORS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            frame = text[max(0, m.start() - 160):m.start() + 60]
            analytical = bool(_ANALYTICAL_FRAME_PAT.search(frame))
            if _declares_structurally and analytical:
                continue
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
            r"(?:may|can|shall)\s*not\s+be\s+(?:varied|changed|amended|altered|weakened|removed)\s+independently\b",
            r"neither\b.{0,120}\bmay\s+be\s+(?:varied|changed|amended|removed|weakened)\b.{0,80}\b(?:without|independently)\b",
            r"either\s+change\s+requires\b|both\s+require\b.{0,80}\bapproval\s+to\s+amend\b",
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
            r"all\s+of\s+the\s+following\b.{0,80}\b(?:hold|holds|apply|applies|are\s+(?:true|met|satisfied|in\s+place))",
            r"(?:unless|until|only\s+(?:if|where|when))\b.{0,60}\ball\s+of\s+the\s+following\b",
            r"\b(?:three|four)\s+things\s+must\s+all\s+be\s+true\b",
            r"partial\s+satisfaction\b.{0,100}\b(?:failure|fails)",
            r"partial\s+(?:satisfaction|compliance|conformance)\b.{0,80}\b(?:is\s+not|does\s+not\s+constitute|is\s+insufficient)\b",
            r"\bsatisfied\s+simultaneously\b|\bsimultaneously\b.{0,140}\bbefore\s+(?:any\s+)?deployment",
            r"\b(?:hold|holds|apply|applies|are\s+met)\s+simultaneously\b",
            r"no\s+(?:model|system|tool)\b.{0,80}\b(?:enters?|goes?)\s+(?:into\s+)?production\b.{0,80}\bunless\b",
            r"must\s+meet\s+(?:these|all)\s+criteria\s+to\s+pass\b",
        ]),
        ("meaningful account of outputs", [
            r"(?:produce|provide|give)\w*\b.{0,80}\b(?:meaningful|comprehensible)\s+account\b",
            r"explain\s+(?:any|each|every)\s+decision\b",
            r"explanation\s+of\s+(?:any|each|every|an?)\b.{0,40}\bdecision\b",
            r"\bshow(?:s)?\s+its\s+work\b",
            r"(?:confidence|uncertainty)\b.{0,140}\b(?:material\s+)?limitations\b",
            r"interpret\s+the\s+system.s\s+outputs?\b|meaningful\s+(?:explanations?|information)\b",
            r"disclos\w+\b.{0,120}\bmaterial\s+limitations\b",
        ]),
        ("stated-vs-implemented correspondence", [
            r"(?:stated|documented)\b.{0,80}\bobjectives?\b.{0,140}\bcorrespond\b",
            r"(?:stated|documented|declared)\s+objectives?\b.{0,60}\b(?:match|matches|equal|align\s+with)\b.{0,60}\b(?:implemented|actual|deployed)\b",
            r"verified\s+by\b.{0,80}\bindependent(?:ly)?\s+(?:of|from)\s+the\s+(?:build|development|delivery)\s+team\b",
            r"really\s+does\s+what\s+we\s+say\s+it\s+does\b",
            r"perform\w*\s+consistently\s+whether\s+or\s+not\b",
            r"verified\s+by\s+independent\s+review\w*\b|checked\s+by\s+independent\s+review\w*\b",
        ]),
        ("bounded operation with escalation", [
            r"operate\w*\s+within\s+documented\s+bound",
            r"stays?\s+inside\s+the\s+limits\b",
            r"(?:surface|escalat|refer)\w*\b.{0,100}\bout.of.scope\b",
            r"escalat\w+\s+to\s+a\s+human\b",
            r"(?:routed|referred|escalated|passed|handed)\s+to\s+a\s+human\b",
            r"shall\s+not\s+autonomously\s+initiate\b",
            r"within\s+(?:its|their)\s+(?:validated|approved|defined|intended|authorised|authorized)\s+(?:indication|purpose|scope|use\s+bound\w*|bound\w*)\b",
            r"out.of.bound\w*\b.{0,120}\b(?:human|escalat|refer|rout)",
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
            r"\bbinds?\s+all\s+\w+\s+(?:entities|units|divisions|subsidiaries|functions|teams|business\w*)\b",
            r"applies?\s+(?:equally\s+)?to\s+all\b.{0,80}\bwithout\s+exception\b",
            r"applies?\s+to\s+all\b.{0,140}\b(?:across\s+all|regardless\s+of|irrespective\s+of|in\s+every)\b",
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
            r"(?:material|significant|any)\s+change\b.{0,180}\brequires?\s+(?:re.approval|re.authoris|re.authoriz|approval\s+through|approval\s+under)\b",
        ]),
        ("reversal capacity preserved", [
            r"(?:capacity|power|right|authority)\s+to\s+(?:reverse|overturn|modify)\b",
            r"appeal\s+to\b.{0,100}\b(?:person|reviewer|body)\b.{0,100}\b(?:reverse|overturn)",
            r"future\s+(?:actors|decision.makers)\b.{0,140}\b(?:reverse|modify)",
            r"can\s+be\s+(?:overridden|reversed|repaired)\b|overridden,\s+repaired",
            r"(?:may|can|shall\s+be\s+able\s+to)\s+(?:overturn|reverse|rescind|set\s+aside|quash)\s+(?:the|that|any)\s+(?:decision|outcome|determination)\b",
            r"(?:may|can)\s+substitute\s+(?:their|its|his|her)\s+own\s+(?:decision|determination|judgement|judgment)\b",
            r"(?:use|deployment|operation)\s+(?:is\s+|to\s+be\s+|must\s+be\s+)?(?:suspended|paused|halted|withdrawn)\b",
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
            r"same\s+(?:evidentiary\s+)?standard\s+it\s+demands\b",
            r"\b(?:is|are)\s+(?:itself|themselves|himself|herself)\s+(?:subject\s+to|bound\s+by)\b",
            r"\b(?:we|this\s+\w+)\s+(?:are|is)\s+bound\s+by\s+(?:this|the\s+same)\b",
        ]),
        ("governing actor evidences its own compliance", [
            r"(?:authority|regulator)\b.{0,140}\b(?:document|demonstrate)\w*\s+its\s+own\s+compliance\b",
            r"\b(?:evidence|demonstrate|document|report|prove|attest\s+to)\s+(?:its|their)\s+own\s+compliance\b",
            r"\bown\s+compliance\b.{0,120}\b(?:internal\s+audit|independent\s+review|external\s+audit|oversight\s+body|senate|board|committee|regulator)\b",
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
                    # Sentence-anchored, like every other public quotation. A
                    # fixed offset window produced exemplar passages beginning
                    # mid-word ("«rs, maintaining the connection between…»"),
                    # which is exactly the evidence a reader is asked to adapt.
                    evidence.append(_quote_at(text, m.start(), m.end(), max_len=160))
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


def _laif_alignment_verdict(formal_pass, depth, functional, contradictions,
                            enumeration_risk="LOW"):
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
    # Functional verdicts are evidence-based, but where the evidence is a list of
    # governance nouns rather than sentences that bind anyone, the constructs
    # have not been shown to be present. Alignment cannot be certified from a
    # word list, however many signals it fires.
    if ok("Coupling") and n_ok >= 4 and not contradictions and enumeration_risk != "HIGH":
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
        "trigger":     r"\b(?:can\s+be\s+(?:reversed|modified|appealed|changed)|right\s+(?:to\s+)?(?:appeal|contest|review)\b|subject\s+to\s+(?:appeal|review)|(?:decisions?|outcomes?)\s+(?:are|shall\s+be)\s+(?:reversible|modifiable)|supports?\s+the\s+ability\s+to\s+(?:correct|reverse|amend)|(?:outcomes?|decisions?)\s+(?:can|may)\s+be\s+corrected)\b",
        "adversaries": [
            (r"\b(?:permanently?|irrevocabl[ey]|irreversible|final\s+and\s+binding|cannot\s+be\s+(?:undone|reversed|changed|appealed|modified)|no\s+(?:right\s+of\s+)?(?:appeal|review|recourse))\b",
             "irreversibility language co-present with expressed reversibility intent (non-canonical)"),
        ],
    },
    {
        "property":    "Structural Transparency (non-canonical)",
        "trigger":     r"\b(?:system\s+(?:transparency|explainability)|outputs?\s+(?:are\s+)?(?:transparent|explainable|interpretable)|model\s+transparency|explainability\s+(?:is\s+)?(?:provided|ensured|maintained)|committed\s+to\s+(?:full\s+|complete\s+)?transparency|(?:we|our\s+\w+)\s+(?:are|is)\s+transparent\b|transparency\s+(?:is|shall\s+be|will\s+be)\s+(?:maintained|ensured|provided|our)|(?:given|provided\s+with)\s+meaningful\s+information|open\s+about\s+how\b)\b",
        "adversaries": [
            (r"\b(?:proprietary|trade\s+secret|cannot\s+(?:be\s+)?(?:disclosed|explained|accessed|revealed)|withheld|black.?box|opaque)\b",
             "non-disclosure/opacity language co-present with expressed transparency intent (non-canonical)"),
        ],
    },
    {
        "property":    "Structural Containment (non-canonical)",
        "trigger":     r"\b(?:operates?\s+within\b|system\s+boundaries?\b|operational\s+(?:boundaries?|scope|limits?)\b|confined\s+to\s+(?:its\s+)?(?:scope|boundaries?|purpose)|human\s+(?:oversight|review|involvement)\s+(?:is|shall\s+be|will\s+be|remains?)\s+(?:maintained|ensured|retained|provided|required)|human.in.the.loop\s+(?:at\s+all\s+times|throughout))\b",
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
    r"(?:human|senior)\s+(?:being\s+)?must\s+approve|"
    r"(?:no|not|never)\s+\w+(?:\s+\w+){0,4}\s+without\s+human\s+(?:oversight|review|approval)|"
    r"only\s+(?:with|after)\s+human\s+(?:oversight|review|approval)|"
    # The adversary vocabulary naming the hazard a clause forbids: "the
    # restriction on automated decisioning without human review", "use of X
    # without human approval is prohibited". Regulating a hazard is not
    # committing it.
    r"(?:restrict\w*|prohibit\w*|forbid\w*|ban(?:ned|s)?|bar(?:red)?|not\s+permitted)\b[^.]{0,160}\bwithout\s+human\s+(?:oversight|review|approval)|"
    r"\bwithout\s+human\s+(?:oversight|review|approval)\b[^.]{0,160}\b(?:is|are)\s+(?:prohibited|not\s+permitted|forbidden)|"
    r"(?:is\s+|are\s+)?prohibited\s+without|"
    r"irreversib\w+\b[^.]{0,160}\b(?:explicit|prior|documented|requires?)\s+(?:authoris|authoriz|approval)|"
    r"(?:authoris|authoriz)\w+\b[^.]{0,120}\birreversib)",
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
    analytical_instrument = (
        len(_ANALYTICAL_FRAME_PAT.findall(text or ""))
        >= _ANALYTICAL_INSTRUMENT_MIN_MARKERS
    )
    for check in CONTRADICTION_CHECKS:
        trigger_positions = [
            m.start() for m in re.finditer(check["trigger"], text, re.IGNORECASE)
        ]
        if not trigger_positions:
            continue
        for pat, desc in check["adversaries"]:
            for m in re.finditer(pat, text, re.IGNORECASE):
                pos = m.start()
                # finditer produces sorted offsets. Only the first trigger
                # inside the lower limit can decide whether this window is empty.
                nearest = bisect_left(trigger_positions, pos - CONTRADICTION_PROXIMITY)
                if nearest == len(trigger_positions) or trigger_positions[nearest] > pos + CONTRADICTION_PROXIMITY:
                    continue
                lo = max(0, m.start() - 160)
                hi = min(len(text), m.end() + 160)
                if _GOVERNING_CONTEXT_PAT.search(text[lo:hi]):
                    continue
                # Analysing a failure is not committing it. A case analysis
                # recording "Q3 — Reversibility: FAIL … cannot be reversed", or a
                # PDCA recording "clinical errors … cannot be undone", is
                # describing the deployment it assesses. Suppressed only where
                # the adversary sits in an analytical frame AND the document
                # writes as an assessment instrument throughout — the same
                # two-condition structure the coupling guard uses, so a bare
                # disclaimer with one analytical phrase is still caught.
                if analytical_instrument and _ANALYTICAL_FRAME_PAT.search(
                        text[max(0, m.start() - 330):m.start() + 120]):
                    continue
                # The adversary term is itself negated: "the decision does not
                # permanently foreclose future revision" asserts reversibility,
                # not irreversibility. Applied only where the matched text is
                # not already a negative construction ("cannot be undone"),
                # which must never be double-negated away.
                matched = m.group(0)
                if not _NEGATIVE_CONSTRUCTION_PAT.search(matched):
                    preceding = text[max(0, m.start() - 40):m.start()]
                    if _NEGATION_PREFIX_PAT.search(preceding):
                        continue
                start = max(0, m.start() - 100)
                end   = min(len(text), m.end() + 100)
                ctx   = text[start:end].replace("\n", " ").strip()
                findings.append((check["property"], desc, ctx[:200]))
                break
    return findings


# ── Language coverage ──────────────────────────────────────────────────────────
# Every pattern in this engine is written against English governance drafting.
# A French, German, or Spanish instrument therefore scores near zero — not
# because it lacks governance, but because the detector cannot read it. Saying
# "this document does not express the load-bearing governance structures in any
# vocabulary" about such a text is false, and it is the reporting layer's own
# A.2 Structural Honesty obligation to state the limit instead.
#
# Detection is a function-word ratio, which separates cleanly and deterministically:
# across the whole assessment corpus and every institutional fixture, English
# governance prose measures 0.15-0.37; French, German, Spanish and Dutch samples
# measure 0.000. The threshold sits well clear of both.
_ENGLISH_FUNCTION_WORDS = frozenset((
    "the", "of", "and", "to", "in", "that", "is", "for", "shall", "must",
    "with", "be", "are", "this", "by", "or", "as", "not", "any", "may",
    "on", "an", "which", "it", "from", "at", "have", "has",
))
ENGLISH_RATIO_THRESHOLD = 0.06
ENGLISH_MIN_WORDS = 40


def _english_coverage(text):
    """Whether the engine's English-language patterns can read this text.

    Returns (readable, ratio). `readable` is False only where there is enough
    text to judge and the function-word ratio is far below anything English
    governance drafting produces.
    """
    words = re.findall(r"[A-Za-z]+", text or "")
    if len(words) < ENGLISH_MIN_WORDS:
        # Too short to judge: a brief English clause and a brief French one are
        # not reliably separable, and the thin-document findings already apply.
        return True, None
    ratio = sum(1 for w in words if w.lower() in _ENGLISH_FUNCTION_WORDS) / len(words)
    return ratio >= ENGLISH_RATIO_THRESHOLD, round(ratio, 3)


# ── Vocabulary enumeration detection ───────────────────────────────────────────
# Source: LAIF v1.2 Integrity Layer A.2 (Structural Honesty) — stated objectives
# must correspond to implemented objectives. A document that LISTS governance
# machinery rather than INSTITUTING it states an objective it does not implement.
#
# Why this detector exists: every rubric signal is keyed to the function its
# language performs rather than to one institution's word for it, so that a
# document is not penalised for its drafting register. The mirror risk of that
# breadth is a document assembled from the vocabulary itself — a term list that
# fires many signals while creating no duty. The two are separable at the
# sentence level: an operative sentence binds an actor to an action; an
# enumeration is a dense run of governance nouns with nothing bound to anyone.
#
# Measured over the assessment corpus, genuine instruments (EU AI Act, NIST AI
# RMF, EO 14110, OECD, NHS DTAC, TUC/CIPD, and institutional policies in bank,
# university, and procurement register) score 0.00-0.06; a document built purely
# from governance vocabulary scores 0.24. The threshold sits well clear of both.

_ENUMERATION_GOVERNANCE_TERM = re.compile(
    r"\b(?:control|procedure|protocol|safeguard|mechanism|threshold|tolerance|"
    r"materiality|lifecycle|retraining|oversight|review|escalation|explanation|"
    r"transparency|interpretability|accountability|traceability|audit|risk|"
    r"termination|breach|suspension|sanction|penalty|compliance|fairness|"
    r"discrimination|contestability|appeal|redress|governance|evidence|"
    r"monitoring|owner|register|approval)\w*\b",
    re.IGNORECASE,
)
_ENUMERATION_MODAL = re.compile(r"\b(?:shall|must|may|will)\s+\w+", re.IGNORECASE)
ENUMERATION_RATIO_THRESHOLD = 0.15
ENUMERATION_MIN_SENTENCES = 3


def _vocabulary_enumeration(text):
    """Detect governance vocabulary listed rather than made operative.

    Returns (risk, ratio, examples). A sentence counts as an enumeration when it
    packs distinct governance terms densely (>28% of its words, at least four
    distinct terms) and either runs them as a comma-separated list or binds none
    of them to an actor with a modal verb.
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text or "")
                 if len(s.strip()) > 25]
    if not sentences:
        return "LOW", 0.0, []
    examples = []
    for sentence in sentences:
        terms = {m.group(0).lower() for m in _ENUMERATION_GOVERNANCE_TERM.finditer(sentence)}
        words = len(sentence.split())
        dense = len(terms) >= 4 and (len(terms) / max(words, 1)) > 0.28
        if not dense:
            continue
        if sentence.count(",") >= 3 or not _ENUMERATION_MODAL.search(sentence):
            examples.append(" ".join(sentence.split())[:180])
    ratio = len(examples) / len(sentences)
    risk = ("HIGH" if ratio >= ENUMERATION_RATIO_THRESHOLD
            and len(examples) >= ENUMERATION_MIN_SENTENCES else "LOW")
    return risk, round(ratio, 3), examples[:5]


# ── Sector gaming detection ────────────────────────────────────────────────────
# Source: LAIF v1.2 Principle 5 (Consistency / Q2) — governance logic must hold
# across all scales. A document optimised for sector keywords without substantive
# governance cannot satisfy Q2: the reasoning would not hold at the individual-
# decision level, only at the keyword-density level.

def _sector_gaming_risk(sector_alignment, overall, conceptual, document_type=""):
    """
    Detect potential sector gaming: high sector keyword alignment with low
    substantive governance content.

    HIGH   — sector alignment ≥80% AND overall readiness <30 (keyword stuffing)
    HIGH   — sector alignment ≥40% AND overall readiness <15 (vocabulary, no document)
    MEDIUM — sector alignment ≥70% AND conceptual proximity <25 (keywords without intent)
    LOW    — no gaming indicators detected

    The second HIGH branch exists because sector alignment is a percentage of a
    profile's risk indicators, and a well-specified profile has enough indicators
    that a keyword list rarely reaches 80% of them. Sector vocabulary genuinely
    present alongside a near-zero readiness score is the same finding at a lower
    alignment figure: the text names a regulated activity without carrying any of
    the governance architecture that activity requires.
    """
    # A values charter openly declares itself a statement of intent. Sector
    # vocabulary without architecture is what that document type IS, not a
    # discrepancy between what it claims and what it carries — and "gaming"
    # implies a concealment the document is not attempting. The declaratory gap
    # characterises it accurately and without that implication.
    if document_type == "values_charter":
        return "LOW", ("Values statement: sector vocabulary without operating "
                       "machinery is the declared nature of this document type, "
                       "not a discrepancy. See the declaratory finding.")
    if sector_alignment >= 40 and overall < 15:
        return "HIGH", (
            f"Sector risk alignment {sector_alignment}% vs overall readiness {overall}/100. "
            "The text uses sector-specific vocabulary but carries almost no governance "
            "architecture — no obligations, owners, evidence duties, or consequences. "
            "Sector language alone cannot support a governance claim "
            "(LAIF v1.2 Q2 Consistency)."
        )
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

def _structural_depth(coupling_quality, contradictions, gaming_risk, formal_pass,
                      enumeration_risk="LOW"):
    """
    Synthesise overall structural depth from diagnostic layers.

    STRONG — Structural Coupling + no contradictions + formal PASS + no gaming
    WEAK   — Shallow Coupling OR minor contradictions OR formal PASS with caveats
    HOLLOW — Negated/absent Coupling OR major contradictions OR high gaming risk
             OR governance vocabulary enumerated rather than made operative
    """
    if enumeration_risk == "HIGH":
        return "HOLLOW"
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
            "Bind each restriction to the specific interest it protects, so neither can be "
            "weakened without the other and the protection is as enforceable as the "
            "restriction (LAIF's canonical form for this is Coupling — v1.2 Principle 2, "
            "Toolkit §2 B.1 — but the document's own wording carries the same structure).",
            "Test each provision before issuing it: does it name and protect a specific "
            "interest; would its reasoning hold at much smaller and much larger scale; can "
            "a future decision-maker reverse what it sets in motion. A provision that fails "
            "the first question fails outright (LAIF states this as the Coherence Test — "
            "v1.2 Part One).",
            "Make deployment conditional on all of the following holding at once, with "
            "partial satisfaction counting as failure: the system can produce a "
            "comprehensible account of any decision including its limits; its stated "
            "objectives match its implemented ones, verified independently; and it operates "
            "within documented boundaries, escalating anything outside them (LAIF's "
            "Integrity Layer — v1.2 Part Two, Toolkit §1.3–§1.5).",
            "Bind the body that issues the rules to the rules themselves, and say what "
            "evidence it must produce of its own compliance and to whom (LAIF states this "
            "as self-application — v1.2 Part Seven).",
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
    "financial_services_ai": {
        "label": "Financial Services AI",
        "purpose": "Diagnose AI governance for credit, lending, insurance underwriting and pricing, fraud and AML screening, collections, and customer-facing financial decisions.",
        "relevant_interests": ["fair access to credit, insurance, and financial services", "the customer's ability to understand and contest an automated financial decision", "protection from wrongful account restriction, denial, or adverse pricing"],
        "diagnostic_terms": ("credit", "lending", "underwriting", "applicant", "customer", "adverse decision", "affordability", "fraud", "AML", "model risk", "model validation"),
        "risk_indicators": [(r"\b(?:credit|lending|loan|mortgage|underwrit\w+|affordability)\b", "credit / underwriting decision"), (r"\b(?:applicant|borrower|policyholder|account\s+holder)\b", "financial customer population"), (r"\b(?:fraud|aml|anti.money.laundering|sanctions screening|financial crime)\b", "fraud / financial-crime screening"), (r"\b(?:pricing|premium|risk.based pricing|rate setting)\b", "pricing / premium setting"), (r"\b(?:account (?:closure|restriction|freeze)|de.risking|collections)\b", "account restriction / collections action")],
        "expected_evidence": [(r"\bmodel validation\b|\bindependent validation\b", "independent model validation"), (r"\badverse (?:action|decision) notice\b|\breasons? for (?:the )?(?:decline|refusal|decision)\b", "adverse-decision reasons record"), (r"\bhuman review\b|\bappeal\b|\bcomplaint\b", "human review / complaint record"), (r"\bfair(?:ness)? (?:testing|metric|outcome)\w*\b|\bdisparate impact\b", "fairness / disparate-impact testing"), (r"\bmodel risk (?:policy|framework|committee)\b|\bmodel inventory\b", "model risk governance record")],
        "governance_force_emphasis": ("protected interest", "actor", "control", "evidence", "reversibility", "escalation", "consequence"),
        "remediation_themes": ("Assign model risk ownership with validation independent of the build team.", "Require adverse-decision reasons, human review, and fairness testing evidence for customer-impacting models.", "Tie monitoring breaches to a defined suspension or escalation decision, not observation alone."),
        "evidence_cautions": ("Financial-services vocabulary does not establish regulatory compliance, capital adequacy, or conduct-rule satisfaction.", "Do not infer that validation, fairness testing, or adverse-decision records exist unless the source text states them."),
        "remediation_focus": ["Assign model risk ownership with validation performed independently of the model build team.", "Require adverse-decision reasons, human review routes, and fairness testing evidence for every customer-impacting model."],
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

_SECTOR_PROFILE_ALIASES = {"public_sector_automation": "government_service_delivery", "public_sector_ai": "government_service_delivery", "government_ai": "government_service_delivery", "departmental_ai": "departmental_ai_development", "internal_ai_development": "departmental_ai_development", "procurement_ai": "procurement_vendor_governance", "vendor_governance": "procurement_vendor_governance", "employment_ai": "employment_hr_ai", "hr_ai": "employment_hr_ai", "workforce_ai": "employment_hr_ai", "financial_services": "financial_services_ai", "banking_ai": "financial_services_ai", "credit_ai": "financial_services_ai", "insurance_ai": "financial_services_ai"}

_SECTOR_PROFILE_PATCH_CONTEXT = {
    "government_service_delivery": {"responsible_actor": "Service-delivery policy owner with administrative review / records authority support", "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.", "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation."},
    "departmental_ai_development": {"responsible_actor": "AI project owner with architecture, security, privacy, and release governance reviewers", "evidence_artifact": "Model register, risk assessment, release approval, monitoring record, or rollback plan.", "operational_control": "Require architecture, security, privacy, release, monitoring, and rollback checkpoints before operational AI release."},
    "procurement_vendor_governance": {"responsible_actor": "Procurement lead with legal/compliance and vendor-management support", "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.", "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences."},
    "clinical_ai": {"responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway", "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.", "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation."},
    "employment_hr_ai": {"responsible_actor": "HR policy owner with legal/compliance and bias-review support", "evidence_artifact": "Adverse-action review, bias evidence, human review/appeal record, or accommodation record.", "operational_control": "Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls."},
    "financial_services_ai": {"responsible_actor": "Model risk owner with validation independent of the build team and conduct/compliance support", "evidence_artifact": "Independent model validation report, adverse-decision reasons record, human review or complaint log, or fairness testing evidence.", "operational_control": "Tie each customer-impacting model to independent validation, adverse-decision reasons, a human review route, fairness monitoring with thresholds, and a suspension decision on breach."},
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
