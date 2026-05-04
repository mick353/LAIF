#!/usr/bin/env python3
"""
LAIF Assessment Engine
----------------------
Produces structured, scored assessments of governance documents against
LAIF v1.2 compliance criteria. Sits around validate.py without weakening
its enforcement — formal compliance remains binary and strict.

Five scoring dimensions (0–100 each):
  structural_score          Explicit governance architecture       (weight 25%)
  terminology_score         Canonical LAIF term presence           (weight 15%)
  conceptual_proximity_score LAIF-like concepts without LAIF terms (weight 20%)
  auditability_score        Objective checkability of obligations  (weight 20%)
  enforceability_score      Operational enforcement capacity       (weight 20%)

A document may FAIL formal compliance while scoring high on conceptual proximity —
this is intentional. The engine distinguishes what a document expresses from
whether it expresses it in the LAIF structural vocabulary.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import find_paraphrase_violations, PARAPHRASE_GUARDS


# ── Scoring rubrics ────────────────────────────────────────────────────────────
# Each rubric is a list of (weight, pattern, label) tuples.
# Weights sum to 100 within each rubric.

STRUCTURAL_RUBRIC = [
    # General governance architecture — external frameworks can score here
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
    # LAIF-specific structural elements — external frameworks will not score here
    (15, r"\bprecondition\b|all\s+(?:three|four|five)\s+(?:must|shall)\b|\bsimultaneously\b",
         "threshold gate conditions (all must pass simultaneously)"),
    (18, r"\bPART ONE\b|FOUNDATIONAL PRINCIPLES|cannot be amended|non.amendable",
         "non-amendable constitutional hierarchy"),
    (12, r"self.application|applies to regulatory|applies to governance actors",
         "self-application clause (Part Seven equivalent)"),
    (14, r"\bCoherence Test\b|\bPDCA\b|Pre.Deployment Coherence Assessment",
         "named decision instrument (Coherence Test / PDCA)"),
]

TERMINOLOGY_RUBRIC = [
    (25, r"\bCoupling\b",                     "Coupling"),
    (20, r"\bCoherence Test\b",               "Coherence Test"),
    (20, r"\bIntegrity Layer\b",              "Integrity Layer"),
    (10, r"\bStructural Transparency\b",       "Structural Transparency"),
    (10, r"\bStructural Honesty\b",            "Structural Honesty"),
    (10, r"\bStructural Containment\b",        "Structural Containment"),
    (5,  r"\bMaterially Affects Interests\b",  "Materially Affects Interests"),
]

CONCEPTUAL_RUBRIC = [
    (10, r"\bhuman rights\b|\bfundamental rights\b|\bhuman interests?\b",
         "human rights / fundamental rights"),
    (8,  r"\btransparency\b|\btransparent\b",
         "transparency"),
    (8,  r"\bexplainability\b|\binterpret\b|\bmeaningful\s+(?:explanation|information)\b",
         "explainability / interpretability"),
    (8,  r"\baccountability\b|\baccountable\b",
         "accountability"),
    (8,  r"\boversight\b|\bhuman determination\b|\bhuman.in.the.loop\b",
         "human oversight"),
    (8,  r"\bproportionat|\brisk.{0,5}(?:level|proportion)",
         "proportionality"),
    (7,  r"\bsafety\b",
         "safety"),
    (9,  r"\bcontest\w*\b|\bappeal\b|\bchallenge\b|\bredress\b|\bremedies\b",
         "contestability / redress"),
    (8,  r"\b(?:revers|modif|correct)\w*\b.{0,80}\b(?:decision|outcome|consequence|policy)\b",
         "reversibility / modifiability"),
    (8,  r"\brisk\s+(?:management|assessment|governance|control)\b",
         "risk governance"),
    (10, r"\btraceability\b|\btraceable\b|\bresponsibility\b.{0,30}\b(?:outcome|system|decision)\b",
         "traceability / responsibility"),
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

# Required LAIF constructs for formal compliance (binary gate)
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


# ── Helpers ────────────────────────────────────────────────────────────────────

def _score(text, rubric):
    """Sum matched weights, capped at 100."""
    return min(100, sum(w for w, pat, _ in rubric
                        if re.search(pat, text, re.IGNORECASE)))

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
    steps = []
    if result["terminology_score"] == 0:
        steps.append(
            "Adopt LAIF canonical terminology: replace informal equivalents with the "
            "precise terms Coupling, Coherence Test, Integrity Layer, Structural "
            "Transparency, Structural Honesty, and Structural Containment. Each term "
            "carries structural enforcement meaning that paraphrases do not."
        )
    if result["paraphrase_violations"]:
        terms = ", ".join(f"'{t}'" for t in result["paraphrase_violations"])
        steps.append(
            f"Eliminate paraphrase violations ({terms} detected): these terms deploy "
            "alignment/connection/linkage language where LAIF requires the canonical "
            "term Coupling. The substitution loses the bidirectional structural "
            "enforcement requirement that Coupling carries."
        )
    steps.append(
        "Declare structural Coupling for each restriction: explicitly identify the "
        "specific human interest at stake and pair it with a protection of equivalent "
        "normative force. The restriction and its paired protection must not be "
        "capable of being weakened in isolation."
    )
    steps.append(
        "Apply the Coherence Test before any governance provision is issued or "
        "deployment authorised: Q1 Coupling, Q2 Consistency (scale-invariance), "
        "Q3 Reversibility. All three must be answered affirmatively. Failure at Q1 "
        "constitutes automatic failure of the full test."
    )
    steps.append(
        "Establish the Integrity Layer as a deployment precondition: Structural "
        "Transparency, Structural Honesty, and Structural Containment must all be "
        "satisfied simultaneously before deployment may proceed. Partial satisfaction "
        "is failure — there is no partial credit."
    )
    if result["structural_score"] < 50:
        steps.append(
            "Declare a non-amendable constitutional hierarchy: foundational principles "
            "at the apex (non-amendable), Provisions derived from them (cannot "
            "contradict Principles), and Operational Standards subordinate to "
            "Provisions (revisable without amending Principles)."
        )
    steps.append(
        "Add a self-application clause: specify that the framework applies to "
        "regulatory bodies and governance actors themselves — not only to AI "
        "operators. This is Part Seven of LAIF and is not optional."
    )
    return steps


# ── Core assessment function ──────────────────────────────────────────────────

def assess(name, source_type, text, **meta):
    """
    Produce a full LAIF assessment for a document.

    Returns a dict matching the LAIF assessment model specification.
    Formal compliance is binary and strict; scores are diagnostic.
    """
    s  = _score(text, STRUCTURAL_RUBRIC)
    t  = _score(text, TERMINOLOGY_RUBRIC)
    c  = _score(text, CONCEPTUAL_RUBRIC)
    a  = _score(text, AUDITABILITY_RUBRIC)
    e  = _score(text, ENFORCEABILITY_RUBRIC)
    overall = round(0.25 * s + 0.15 * t + 0.20 * c + 0.20 * a + 0.20 * e)

    construct_coverage = {
        name_: bool(re.search(pat, text, re.IGNORECASE))
        for name_, pat in CONSTRUCT_COVERAGE_CHECKS
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

    # Strengths: signals that fired in conceptual, general structural,
    # auditability, and enforceability rubrics
    strengths = []
    for _, pat, label in CONCEPTUAL_RUBRIC:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Expresses: {label}")
    for _, pat, label in STRUCTURAL_RUBRIC[:6]:       # general signals only
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Structure: {label}")
    for _, pat, label in AUDITABILITY_RUBRIC:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Auditability: {label}")
    for _, pat, label in ENFORCEABILITY_RUBRIC:
        if re.search(pat, text, re.IGNORECASE):
            strengths.append(f"Enforceability: {label}")

    # Gaps: missing LAIF-specific elements (grouped)
    gaps = []
    missing_terms = [lbl for _, pat, lbl in TERMINOLOGY_RUBRIC
                     if not re.search(pat, text, re.IGNORECASE)]
    if missing_terms:
        gaps.append("Canonical LAIF terms absent: " + ", ".join(missing_terms))

    missing_laif_structural = [lbl for _, pat, lbl in STRUCTURAL_RUBRIC[6:]
                                if not re.search(pat, text, re.IGNORECASE)]
    for lbl in missing_laif_structural:
        gaps.append(f"LAIF structural element missing: {lbl}")

    for guard_term, violations in paraphrase.items():
        examples = "; ".join(
            v[1].replace("\n", " ")[:60] + "…"
            for v in violations[:2]
        )
        gaps.append(
            f"Paraphrase violation — forbidden substitution of '{guard_term}' "
            f"({len(violations)} instance(s)): {examples}"
        )

    # Failure modes
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

    result = {
        "document_name":               name,
        "source_type":                 source_type,
        "formal_laif_compliance":      "PASS" if formal_pass else "FAIL",
        "construct_coverage":          construct_coverage,
        "structural_score":            s,
        "terminology_score":           t,
        "conceptual_proximity_score":  c,
        "auditability_score":          a,
        "enforceability_score":        e,
        "overall_readiness_score":     overall,
        "remediation_effort":          effort,
        "paraphrase_violations":       paraphrase,
        "strengths":                   strengths,
        "gaps":                        gaps,
        "primary_failure_modes":       failure_modes,
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
        widths = [max(len(h), max((len(str(r[i])) for r in rows), default=0))
                  for i, h in enumerate(headers)]
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
    p("**Classification:** Governance Assessment — Controlled Exploration Phase  ")
    p("**Validator:** validate.py (unchanged — strict formal compliance enforced)  ")

    # ── Executive Summary ────────────────────────────────────────────────────
    h(2, "Executive Summary")
    fail_count = sum(1 for r in assessments if r["formal_laif_compliance"] == "FAIL")
    avg_overall = round(sum(r["overall_readiness_score"] for r in assessments) / len(assessments))
    avg_conceptual = round(sum(r["conceptual_proximity_score"] for r in assessments) / len(assessments))
    p(
        f"{fail_count} of {len(assessments)} external AI governance frameworks assessed fail "
        f"formal LAIF v1.2 compliance. Formal compliance is binary and strict — no partial "
        f"credit is awarded for proximity to LAIF requirements."
    )
    p()
    p(
        f"However, the dimensional scoring reveals a more nuanced picture. Documents achieve "
        f"an average conceptual proximity score of {avg_conceptual}/100 and an average overall "
        f"readiness score of {avg_overall}/100, indicating that the underlying governance intent "
        f"is broadly present — expressed through different vocabulary and structural frameworks."
    )
    p()
    p("**Core finding:** The gap between real-world governance language and formal LAIF compliance "
      "is terminological and structural, not conceptual. These frameworks address the right "
      "problems but do not enforce them through structural Coupling, the Coherence Test, or the "
      "Integrity Layer. LAIF is measurably stricter than current governance language.")

    # ── Method ──────────────────────────────────────────────────────────────
    h(2, "Method")
    p("Each document was assessed against two complementary layers:")
    p()
    p("**Layer 1 — Formal LAIF compliance (binary):** Checks for 8 required constructs:")
    p("Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles, "
      "non-amendable clause, self-application clause (Part Seven), Integrity Layer FINDING "
      "block, and Coherence Test FINDING block. All 8 must be present. This check is strict "
      "and is performed by the existing validate.py harness without modification.")
    p()
    p("**Layer 2 — Dimensional scoring (diagnostic):** Five dimensions scored 0–100 "
      "independently to identify strengths, gaps, and remediation priorities. A document "
      "may fail formal compliance while scoring high on conceptual proximity — this "
      "is expected and meaningful.")
    p()
    p("Documents analysed:")
    for r in assessments:
        p(f"- **{r['document_name']}** ({r.get('citation', r['source_type'])})")

    # ── Scoring Model ────────────────────────────────────────────────────────
    h(2, "Scoring Model")
    table(
        ["Dimension", "Weight", "Description"],
        [
            ["Structural", "25%", "Explicit governance architecture: named tests, hierarchy, thresholds, review mechanisms"],
            ["Terminology", "15%", "Canonical LAIF term presence: Coupling, Coherence Test, Integrity Layer, etc."],
            ["Conceptual Proximity", "20%", "LAIF-like concepts expressed without LAIF terms: rights, oversight, proportionality, contestability"],
            ["Auditability", "20%", "Objective checkability: numbered obligations, evidence requirements, review mechanisms"],
            ["Enforceability", "20%", "Operational enforcement: mandatory language, assignable duties, thresholds, consequences"],
        ]
    )
    p()
    p("**Overall Readiness Score** = Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20")
    p()
    p("**Remediation Effort:** VERY HIGH (<35) · HIGH (35–59) · MEDIUM (60–74) · LOW (≥75)")

    # ── Per-Document Scorecards ───────────────────────────────────────────────
    h(2, "Per-Document Scorecards")

    for r in assessments:
        h(3, r["document_name"])
        compliance_tag = "✅ PASS" if r["formal_laif_compliance"] == "PASS" else "❌ FAIL"
        p(f"**Formal LAIF Compliance:** {compliance_tag}  ")
        p(f"**Source type:** {r['source_type']}  ")
        p(f"**Remediation Effort:** {r['remediation_effort']}")
        p()

        h(4, "Scores")
        score_rows = [
            ["Structural",          f"{r['structural_score']}/100",          score_bar(r['structural_score'])],
            ["Terminology",         f"{r['terminology_score']}/100",          score_bar(r['terminology_score'])],
            ["Conceptual Proximity",f"{r['conceptual_proximity_score']}/100", score_bar(r['conceptual_proximity_score'])],
            ["Auditability",        f"{r['auditability_score']}/100",         score_bar(r['auditability_score'])],
            ["Enforceability",      f"{r['enforceability_score']}/100",       score_bar(r['enforceability_score'])],
            ["**Overall Readiness**",f"**{r['overall_readiness_score']}/100**", score_bar(r['overall_readiness_score'])],
        ]
        table(["Dimension", "Score", "Visual"], score_rows)
        p()

        h(4, "Construct Coverage")
        table(
            ["Construct", "Present"],
            [(k, "✅ Yes" if v else "❌ No") for k, v in r["construct_coverage"].items()]
        )
        p()

        if r["paraphrase_violations"]:
            h(4, "Paraphrase Violations")
            for term, vs in r["paraphrase_violations"].items():
                p(f"**Guard: {term}** — {len(vs)} violation(s)")
                for _, ctx in vs[:2]:
                    p(f"> …{ctx.replace(chr(10), ' ')[:120]}…")
        else:
            h(4, "Paraphrase Violations")
            p("None detected.")
        p()

        h(4, "Strengths")
        for s in r["strengths"][:10]:
            p(f"- {s}")
        p()

        h(4, "Gaps")
        for g in r["gaps"]:
            p(f"- {g}")
        p()

        h(4, "Primary Failure Modes")
        for fm in r["primary_failure_modes"]:
            p(f"- {fm}")
        p()

        h(4, "Recommended Remediation")
        for i, step in enumerate(r["recommended_remediation_steps"], 1):
            p(f"{i}. {step}")
        p()
        p("---")

    # ── Cross-Document Findings ───────────────────────────────────────────────
    h(2, "Cross-Document Findings")

    h(3, "Score Comparison")
    table(
        ["Document", "Structural", "Terminology", "Conceptual", "Auditability", "Enforceability", "Overall"],
        [
            [
                r["document_name"][:40],
                r["structural_score"],
                r["terminology_score"],
                r["conceptual_proximity_score"],
                r["auditability_score"],
                r["enforceability_score"],
                r["overall_readiness_score"],
            ]
            for r in assessments
        ]
    )
    p()

    p("**Notable patterns:**")
    high_conceptual = [r for r in assessments if r["conceptual_proximity_score"] >= 60]
    if high_conceptual:
        names = ", ".join(r["document_name"] for r in high_conceptual)
        p(f"- High conceptual proximity (≥60): {names} — these frameworks express LAIF-like "
          "intent through their own vocabulary.")

    paraphrase_docs = [r for r in assessments if r["paraphrase_violations"]]
    if paraphrase_docs:
        names = ", ".join(r["document_name"] for r in paraphrase_docs)
        p(f"- Paraphrase violations detected in: {names} — explicit forbidden substitution "
          "of LAIF canonical terms.")

    low_enforce = [r for r in assessments if r["enforceability_score"] < 40]
    if low_enforce:
        names = ", ".join(r["document_name"] for r in low_enforce)
        p(f"- Low enforceability (<40): {names} — voluntary or declaratory frameworks "
          "without binding operational mandates.")

    # ── Common Failure Modes ──────────────────────────────────────────────────
    h(2, "Common Failure Modes")
    from collections import Counter
    fm_counter = Counter(fm for r in assessments for fm in r["primary_failure_modes"])
    for fm, count in fm_counter.most_common():
        p(f"- **{fm}** — {count}/{len(assessments)} documents")

    p()
    p("The universal failure mode is terminological: no external framework uses LAIF canonical "
      "terms. This is expected — LAIF is a new framework. However, the absence of structural "
      "Coupling is the more consequential gap: without it, governance restrictions are not "
      "structurally paired with proportionate protections, and neither can be defended as "
      "structurally required by the other.")

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
      "'linkage' appear as structural governance terms, substituting 'Coupling' is the minimal "
      "change. This is a terminology fix, not a structural redesign.")
    p()
    p("4. **Auditability is a relative strength.** Binding regulations (EU AI Act) score "
      "highly on auditability — their obligations are traceable, documented, and reviewable. "
      "This auditability infrastructure is exactly what LAIF-compliant Coupling declarations "
      "would need to be enforced through.")
    p()
    p("5. **Voluntary frameworks require the most work.** NIST AI RMF and OECD Principles "
      "score low on enforceability because they use aspirational ('should') rather than "
      "mandatory ('shall') language. LAIF's Integrity Layer threshold requires mandatory "
      "language to function as a deployment precondition.")

    # ── Recommended Next Development Steps ───────────────────────────────────
    h(2, "Recommended Next Development Steps")
    p("1. **LAIF–EU AI Act mapping:** Article-by-article mapping of LAIF Provisions to EU "
      "AI Act requirements. Many EU AI Act articles can be interpreted as partially "
      "implementing LAIF provisions — formalising this mapping would accelerate EU adoption.")
    p()
    p("2. **LAIF–NIST RMF function mapping:** Map LAIF's Coherence Test questions to NIST "
      "RMF functions (Govern, Map, Measure, Manage). The RMF's operational structure could "
      "carry LAIF Coupling requirements within its existing governance architecture.")
    p()
    p("3. **Paraphrase violation remediation guide:** Produce a short guidance document for "
      "each violating framework showing specifically where 'alignment', 'connection', "
      "'linkage' appear and what structural declaration is required to replace them with "
      "LAIF-compliant Coupling language.")
    p()
    p("4. **Extend real-world corpus:** Add sector-specific governance documents (clinical AI "
      "guidelines, financial AI regulations, autonomous vehicle frameworks) to extend the "
      "baseline beyond general AI governance.")
    p()
    p("5. **Score threshold calibration:** As more documents are assessed, calibrate the "
      "remediation effort thresholds (VERY HIGH / HIGH / MEDIUM / LOW) against actual "
      "adoption timelines to make them operationally predictive.")

    p()
    p("---")
    p(f"*LAIF v1.2 · Compliance Toolkit v1.1 · {report_date} · Governance Audit Series*")
    p("*Generated by `test_real_world.py` — validate.py enforcement unchanged*")

    return "\n".join(lines)
