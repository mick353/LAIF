"""LAIF engine: assessment. Moved without changing assessment rules."""

import hashlib
import re
from validate import find_paraphrase_violations, PARAPHRASE_GUARDS
from .classification import (
    _assessment_mode_fields,
    _build_governance_repair_fields,
    _filter_paraphrase_violations,
    _resolve_assessment_mode,
    classify_document_type,
    dominant_sector_for_document,
    known_instrument_profile,
)
from .detection import (
    AUDITABILITY_RUBRIC,
    CONCEPTUAL_RUBRIC,
    CONSTRUCT_COVERAGE_CHECKS,
    ENFORCEABILITY_RUBRIC,
    FORMAL_REQUIREMENTS,
    STRUCTURAL_RUBRIC,
    TERMINOLOGY_RUBRIC,
    _achievable_ceiling_external,
    _contradiction_check,
    _coupling_quality,
    _coupling_state,
    _english_coverage,
    _functional_alignment,
    _implicit_coupling_signals,
    _laif_alignment_verdict,
    _sector_gaming_risk,
    _sector_profile_key,
    _sector_profile_metadata,
    _sector_profile_signals,
    _structural_depth,
    _vocabulary_enumeration,
    integrity_requirement_diagnostics,
)
from .evidence import (
    _build_evidence_traces,
    _build_remediation_patches,
)
from .findings import (
    _build_score_trace,
    _compliance_summary,
    _deployment_risk_tier,
    _directionality_penalty,
    _executive_summary,
    _governance_signal_strength,
    _remediation,
    _score_signals,
    _structured_findings,
    _structured_remediation,
)
from .report_helpers import (
    _calibration_cautions,
    _dimension_justification_records,
    _score_gaming_risk_notes,
    _score_interpretation_label,
    _score_justification_summary,
)
from .source_display import (
    _located_signals,
    _obligation_anchors,
    _plain_reading,
)
from .source_spans import (
    _document_outline,
    _locate_offset,
)


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

    # The mode decides how several findings are worded, so it must be resolved
    # before they are written. Using the raw parameter here meant every caller
    # that relied on auto-detection got the LAIF-native wording.
    resolved_assessment_mode = _resolve_assessment_mode(
        assessment_mode, name, source_type, formal_pass
    )

    # Primary failure modes
    failure_modes = []
    if not any(p for lbl, p in formal_checks
               if any(x in lbl for x in ("PART ONE", "non-amendable", "self-application"))):
        failure_modes.append(
            "structural — no precedence rule between the document's own provisions")
    if t == 0:
        failure_modes.append(
            "certification channel — LAIF-native vocabulary not used (expected for "
            "an external instrument; not a governance deficiency)"
            if resolved_assessment_mode == "external_framework" and not claims_laif
            else "terminological — no canonical LAIF terms present")
    if paraphrase and paraphrase_classification == "VIOLATION":
        failure_modes.append("terminological (paraphrase) — forbidden substitutions detected")
    if c < 40:
        failure_modes.append("conceptual — governance concepts insufficiently expressed")
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
    gaming_level, gaming_reason = _sector_gaming_risk(
        sector_risk_alignment, overall, c, early_document_type)
    _english_readable, _english_ratio = _english_coverage(text)
    enum_risk, enum_ratio, enum_examples = _vocabulary_enumeration(text)
    depth                = _structural_depth(cq, contradictions, gaming_level, formal_pass,
                                             enum_risk)

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
                                              contradictions, enum_risk)

    # LAIF-native distance notes — deferred from the gap builder above so
    # they can be worded per channel and per functional verdict. For
    # documents that use or claim LAIF vocabulary these are compliance
    # gaps; for external instruments they are certification-distance
    # diagnostics, never deficiency claims (fair-reading bound 1).
    if missing_terms:
        if claims_laif:
            gaps.insert(0, "Canonical LAIF terms absent: " + ", ".join(missing_terms))
        else:
            gaps.append(
                "LAIF-native vocabulary not used — expected for an external "
                "instrument; certification-channel distance, not a deficiency: "
                + ", ".join(missing_terms)
            )
    _signal_construct = {
        "threshold gate conditions (all must pass simultaneously)": "Integrity Layer",
        "governing body bound by its own rules (self-application)": "Self-Application",
        "named decision instrument (Coherence Test / PDCA)":        "__branding__",
    }
    _native_gap_lines = []
    _CHANNEL_MARKERS = ("certification-channel", "LAIF-native vocabulary not used",
                        "LAIF-native marker not present")
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
    gaps.extend(_native_gap_lines)

    def _is_channel_note(line):
        return any(marker in line for marker in _CHANNEL_MARKERS)

    # Substantive findings first, certification-channel notes last, each group in
    # the order it was produced. A note about not using LAIF's vocabulary led
    # every external document's gap list, which is the reverse of its importance.
    gaps[:] = ([g for g in gaps if not _is_channel_note(g)]
               + [g for g in gaps if _is_channel_note(g)])

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
        # Length of the text actually assessed. Consumers need it to know when
        # document-level signal detection has saturated (every signal present
        # somewhere) and can no longer discriminate.
        "assessed_character_count":   len(text or ""),
        "english_language_readable":  _english_readable,
        "english_function_word_ratio": _english_ratio,
        "language_coverage_note": (
            "Detection patterns are written against English governance drafting. "
            f"This text's English function-word ratio is {_english_ratio}, far below "
            "anything English drafting produces, so the scores below reflect what "
            "this engine can read rather than what the document contains. Assess it "
            "with an instrument built for its language, or with a certified "
            "translation."
            if not _english_readable else
            "Text is readable by the engine's English-language detection patterns."),
        "vocabulary_enumeration_risk": enum_risk,
        "vocabulary_enumeration_ratio": enum_ratio,
        "vocabulary_enumeration_examples": enum_examples,
        "vocabulary_enumeration_reason": (
            f"{int(enum_ratio * 100)}% of substantive sentences list governance terms "
            f"without binding any of them to an actor or an action. The document "
            f"names the machinery of governance rather than instituting it, so its "
            f"signals reflect vocabulary rather than duties (LAIF v1.2 A.2 "
            f"Structural Honesty: stated and implemented objectives must correspond)."
            if enum_risk == "HIGH" else
            "Governance language is expressed as operative sentences, not as term lists."),
        "coupling_quality":           cq,
        "coupling_quality_reason":    cq_reason,
        "coupling_quality_evidence":  cq_evidence,
        "implicit_coupling":          implicit_coupling,
        "coupling_state":             _coupling_state(cq, implicit_coupling,
                                                      func_coupling),
        "functional_alignment":       functional,
        "laif_alignment":             laif_alignment,
        "assessed_text_sha256":       hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "known_instrument_profile":   known_instrument_profile(text, name, source_type),
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
    result["integrity_requirement_diagnostics"] = integrity_requirement_diagnostics(text)
    from scripts.laif_auto_criteria import judge
    result["automatic_criteria"] = judge(text)
    result["substantive_coherence_determination"] = "REQUIRES_SOURCE_BASED_REVIEW"
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
