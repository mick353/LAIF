"""LAIF engine: findings. Moved without changing assessment rules."""

import re
import sys


def _score_signals(text, rubric, *, search=None):
    """Return (score, fired, missed) for a rubric.

    fired  — list of (label, weight) for patterns that matched
    missed — list of (label, weight) for patterns that did not match
    Score is sum of fired weights, capped at 100.
    """
    fired, missed = [], []
    # DOTALL: span patterns (".{1,300}") are proximity windows over the
    # document, not same-line constraints — hard-wrapped prose must be able
    # to earn them. The Evidence Locator uses identical flags (parity).
    flags = re.IGNORECASE | re.DOTALL
    for w, pat, label in rubric:
        match = search(pat, flags) if search is not None else re.search(pat, text, flags)
        if match:
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
            f"No {dim} signals detected — none of the {n_total} expected patterns matched. "
            "This does not establish that the dimension is absent from the document."
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
            "Coupling pairing was not established by current detector rules. Review each "
            "restriction and its protected interest in the complete source before asserting "
            "a protection gap. A detector non-match does not establish Q1 failure or "
            "failure of the complete Coherence Test. (LAIF v1.2 Principle 2)"
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
            f"governance signal scores are low (overall {overall}/100). This pattern warrants "
            f"source review; it does not establish a substantive Q2 Consistency failure. "
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
            f"responsible parties and consequences have few matching signals. "
            "This score does not establish that the instrument is non-binding; verify its authority and incorporated rules."
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
        why = "Strong detector-rubric result; substantive compliance requires source-based review."
    elif result.get("coupling_state") == "FUNCTIONAL":
        why = ("Primary structural gap: LAIF-native declaration absent — Coupling "
               "substance is functionally present in the document's own vocabulary.")
    elif cq in ("ABSENT", "SHALLOW", "NEGATED"):
        why = "Complete Coupling pairing not detected; verify source protections and their force."
    elif contras:
        why = "Complete Integrity Layer precondition not detected; verify the source requirements."
    elif not result.get("construct_coverage", {}).get("Coherence Test"):
        why = "Primary structural gap: Coherence Test not applied."
    else:
        why = "Complete Integrity Layer precondition not detected; verify the source requirements."

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
        position_result = "Explicit Coupling structure detected; complete LAIF compliance is not established"
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
        not_enforced.append("Complete Coupling pairing not detected; review restriction-to-interest mapping")
    if not cc.get("Coherence Test"):
        not_enforced.append("Coherence Test documentation not detected; verify the complete source")
    if not cc.get("Integrity Layer"):
        not_enforced.append("Integrity Layer declaration not detected; verify equivalent deployment requirements")

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
        "Where a document sets no precedence between its own provisions, a routine "
        "operational revision can change what the document actually requires without "
        "anyone treating it as a change of standard — "
        "foundational protections are not locked against erosion over time."
    ),
    "conceptual": (
        "Low conceptual proximity indicates the document's governance intent is not "
        "substantially aligned with LAIF values. The adoption gap is more fundamental "
        "than terminology — substantive governance redesign is required, not just "
        "terminological substitution."
    ),
    "auditability": (
        "If source review confirms inadequate traceable obligations and evidence, "
        "auditability may be limited. A low pattern score does not establish that "
        "external audit is impossible."
    ),
    "enforceability": (
        "If source review confirms no applicable enforceable obligations, accountability "
        "may be limited. Verify legal, contractual and institutional authority; "
        "a missing pattern is not proof that the instrument is voluntary."
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
                "Part Eight this provides candidate evidence for review of equivalent structural "
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
            "title":    "Complete Coupling pairing not detected — source review required",
            "severity": "HIGH",
            "evidence": "Neither the canonical term 'Coupling' nor a functional equivalent "
                        "of the structural pairing was detected in the document.",
            "impact":   (
                "The current detector did not establish the full pairing. This is not proof "
                "that protections are absent, separable or unenforceable. Review the complete "
                "instrument and incorporated controls against all three normative-force limbs "
                "before a substantive Q1 conclusion (LAIF v1.2 Principle 2)."
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
                f"Coupling: verify whether the protection and obligation can be weakened "
                f"independently before concluding a structural repair is required "
                f"(LAIF v1.2 Principle 2; Toolkit §2 B.1)."
            ),
            "concrete_fix": (
                "Convert each detected implicit signal into an explicit Coupling declaration: "
                "'Coupling between [the restriction already present] and [the specific human "
                "interest the detected protective language names], with equivalent normative "
                "force on both sides — neither may be weakened in isolation.' "
                "The protective signal is present; full structural binding requires source review "
                "(Toolkit §2 B.1)."
            ),
        })
    elif cq in ("ABSENT", "SHALLOW", "NEGATED") and _cstate not in ("FUNCTIONAL", "STRUCTURAL"):
        cq_r = result["coupling_quality_reason"]
        if cq == "ABSENT":
            problem = ("Restriction-protection pairing not detected; verify the complete "
                       "instrument and incorporated protections before proposing changes.")
        elif cq == "SHALLOW":
            problem = f"Coupling declared SHALLOW — {cq_r[:110]}"
        else:
            problem = f"Coupling explicitly negated — {cq_r[:110]}"
        steps.append({
            "problem": problem,
            "why_it_matters": (
                "If source-based review confirms absent or separable pairing, the restriction "
                "may lack an adequately bound protection. This is a risk to test, not a "
                "substantive Q1 failure established by a pattern non-match "
                "(LAIF v1.2 Principle 2; Toolkit §2 B.1)."
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

    # 3 — Coherence Test. LAIF's own named decision instrument: for an external
    # document its absence is adoption distance, not a finding, and is reported
    # through the certification channel instead.
    if (not result["construct_coverage"].get("Coherence Test")
            and result.get("assessment_mode") != "external_framework"):
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

    # 4 — Integrity Layer. Skipped where the functional layer found the gate in
    # the document's own words: construct_coverage is a vocabulary check, and a
    # document stating "no model enters production unless all of the following
    # hold simultaneously" plainly has one.
    _integrity_functional = (_func.get("Integrity Layer", {}).get("verdict")
                             in ("DECLARED", "FUNCTIONAL"))
    if not result["construct_coverage"].get("Integrity Layer") and not _integrity_functional:
        steps.append({
            "problem": ("Complete Integrity Layer deployment gate not detected; review transparency, "
                        "honesty, containment and calibration requirements where applicable."),
            "why_it_matters": (
                "Without a threshold gate, a system can be deployed while any applicable Integrity Layer "
                "property is unmet: the ability to account for its outputs, the "
                "correspondence of stated to implemented objectives, and operation within "
                "documented boundaries. Partial satisfaction functioning as approval is the "
                "risk requiring source-based review; its prevalence is not established by these rules (LAIF v1.2 Part Two)."
            ),
            "concrete_fix": (
                "Establish a deployment gate covering all four properties where applicable "
                "simultaneously — (i) the system can produce a meaningful account of any "
                "output that materially affects a person; (ii) stated objectives correspond "
                "to implemented objectives, verified by independent review; (iii) the system "
                "operates within documented boundaries in all tested conditions, escalating "
                "out-of-scope cases; (iv) where section 2.5 applies, expressed confidence "
                "corresponds to observed performance in comparable deployment contexts. "
                "The document's own vocabulary is sufficient; the "
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

    # 6 — Precedence between the document's own provisions. Raised whenever the
    # signal is missing, not only on a low structural score: it is a specific,
    # detected, closable finding and belongs in the remediation list even for a
    # document that scores well everywhere else.
    _precedence_missing = any(
        lbl == "provision hierarchy / precedence rule"
        for lbl, _ in result["score_breakdown"]["structural"]["missed"])
    if _precedence_missing or result["structural_score"] < 50:
        bd = result["score_breakdown"]["structural"]
        missed = ", ".join(lbl for lbl, _ in bd["missed"][:3])
        if _precedence_missing:
            problem = ("No precedence rule between the document's own provisions: nothing "
                       "states which prevails on conflict, what cannot be waived, or what "
                       "this document is subordinate to.")
        else:
            problem = (f"Structural architecture thin (structural score "
                       f"{result['structural_score']}/100). Missing: {missed}.")
        steps.append({
            "problem": problem,
            "why_it_matters": (
                "Where a document sets no precedence between its own provisions, a routine "
                "operational revision can change what it actually requires without anyone "
                "treating it as a change of standard, and a reader facing two provisions "
                "that point different ways has no rule for deciding which governs. LAIF "
                "states this as a three-tier hierarchy with a non-amendable apex "
                "(v1.2 Part Eight); instruments more often state it as a conflicts clause "
                "or a waiver bar. The property is the same."
            ),
            "concrete_fix": (
                "Add three statements the text currently leaves unanswered: which provision "
                "prevails if two conflict; which provisions cannot be waived, disapplied, or "
                "amended except by a named authority; and what instrument this document is "
                "itself subordinate to. A conflicts clause, a 'without prejudice to' clause, "
                "a waiver bar, or a stated parent framework each satisfies this; LAIF's "
                "three-tier form — Foundational Principles (non-amendable) → Provisions → "
                "Operational Standards — is one way of stating all three at once."
            ),
        })

    # 7 — Sector-specific (top 2 from profile). A profile step is a prescription,
    # not a finding: it must never be rendered as "not addressed in this document"
    # for a construct this assessment detected as present.
    sector_label = result.get("sector_label", result["sector_used"])
    _step_construct = (
        ("coupling", "Coupling"),
        ("coherence test", "__external_channel__"),
        ("integrity layer", "Integrity Layer"),
        ("self-application", "Self-Application"),
        ("reversib", "Reversibility"),
        ("scale", "Consistency"),
    )

    def _step_already_satisfied(step_text):
        low = step_text.lower()
        for marker, construct in _step_construct:
            if marker not in low:
                continue
            if construct == "__external_channel__":
                return result.get("assessment_mode") == "external_framework"
            if _func.get(construct, {}).get("verdict") in ("DECLARED", "FUNCTIONAL"):
                return True
        return False

    for step_text in result.get("sector_remediation_priority", [])[:2]:
        if _step_already_satisfied(step_text):
            continue
        if not any(step_text[:60] in s.get("concrete_fix", "")[:60] for s in steps):
            # derive a distinct problem statement from the first clause of step_text
            first_clause = re.split(r"\s(?:—|–|:)\s", step_text, maxsplit=1)[0]
            if len(first_clause) > 110:
                first_clause = first_clause[:110].rstrip() + "…"
            steps.append({
                "problem": f"{first_clause} — not detected in this document.",
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
            "edge cases), and A.4 Structural Calibration (expressed confidence corresponds to "
            "observed accuracy where section 2.5 applies). All four properties must be satisfied where applicable before deployment proceeds, including calibration under section 2.5. "
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

    # 6 — Precedence between the document's own provisions (if structural score is low)
    if result["structural_score"] < 50:
        steps.append(
            "State the order of precedence among this document's own provisions, so a "
            "routine revision cannot quietly change what it requires. Three questions "
            "have to be answerable from the text: which provisions prevail if two "
            "conflict; which cannot be waived, disapplied, or changed except by a named "
            "authority; and what this document is itself subordinate to. Instruments "
            "express this as a conflicts clause, a 'without prejudice to' clause, a "
            "waiver bar, or a stated parent framework; LAIF expresses it as a "
            "three-tier hierarchy — Foundational Principles (non-amendable), Provisions "
            "derived from them, and Operational Standards subordinate to Provisions and "
            "revisable without amending the Principles (LAIF v1.2 Part Eight). Any of "
            "these forms satisfies the requirement."
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
