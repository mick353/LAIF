"""LAIF engine: evidence. Moved without changing assessment rules."""

import re
from .detection import (
    AUDITABILITY_RUBRIC,
    CONCEPTUAL_RUBRIC,
    ENFORCEABILITY_RUBRIC,
    STRUCTURAL_RUBRIC,
    TERMINOLOGY_RUBRIC,
    _sector_profile_metadata,
    _sector_profile_patch_adjustments,
)


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


def _first_regex_match(text, pattern, *, search=None):
    match = search(pattern, re.IGNORECASE) if search is not None else re.search(pattern, text or "", re.IGNORECASE)
    if not match:
        return None
    return match.group(0)


def _extract_profile_signal_traces(text, result, *, search=None):
    traces = []
    profile = _sector_profile_metadata(result.get("sector_profile", result.get("sector_used")))
    signal_specs = []
    signal_specs.extend((pat, label, "sector_profile_signal") for pat, label in profile.get("risk_indicators", []))
    signal_specs.extend((pat, label, "provenance_signal") for pat, label in profile.get("expected_evidence", []))
    for pat, label, evidence_type in signal_specs:
        matched = _first_regex_match(text, pat, search=search)
        if matched:
            traces.append((evidence_type, matched, f"regex:{pat}", f"sector profile signal: {label}"))
    return traces


def _extract_governance_force_traces(text, result, *, search=None):
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
            matched = _first_regex_match(text, pat, search=search)
            if matched:
                traces.append((evidence_type, matched, f"regex:{pat}", f"{prefix}: {label}"))
    return traces


def _extract_remediation_anchor_traces(text, result, *, search=None):
    traces = []
    for construct, present in result.get("construct_coverage", {}).items():
        if not present:
            continue
        matched = _first_regex_match(text, re.escape(construct), search=search)
        if matched:
            traces.append(("remediation_anchor", matched, f"regex:{re.escape(construct)}", f"remediation anchor: {construct}"))
    return traces


def _build_evidence_traces(text, result, *, search=None):
    """Build capped deterministic source-support traces without changing scores."""
    source_document = result.get("document_name", "unknown document")
    source_type = result.get("source_type", "unknown_source_type")
    assessment_mode = result.get("assessment_mode", "external_framework")
    candidates = []
    candidates.extend(_extract_profile_signal_traces(text, result, search=search))
    candidates.extend(_extract_governance_force_traces(text, result, search=search))
    candidates.extend(_extract_remediation_anchor_traces(text, result, search=search))

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
    # Distance from LAIF's own vocabulary, where the substance is present or the
    # construct is LAIF's own named instrument. Never a governance defect, so it
    # must not be ranked above the gaps that are.
    if "certification channel" in text:
        return "low"
    # A terminology gap names the LAIF terms it did not find, so it must be
    # classified before the construct-name check — otherwise listing "Coupling,
    # Coherence Test, Integrity Layer" as MISSED VOCABULARY was rated as high as
    # missing the constructs themselves.
    if "terminology score" in text or text.startswith("terminological"):
        return "low" if result.get("assessment_mode") == "external_framework" else "medium"
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
    if "certification channel" in gap_text.lower():
        return ("No governance action is required. This records distance from the "
                "assessing framework's own vocabulary, which matters only if the "
                "organisation chooses to seek LAIF-native certification; the "
                "substance it names is either already expressed in the document's "
                "own words or belongs to that framework alone.")
    if "no precedence rule between" in gap_text.lower():
        return ("State the order of precedence among this document's own provisions: "
                "which prevails if two conflict, which cannot be waived or changed "
                "except by a named authority, and what this document is subordinate "
                "to. A conflicts clause, a 'without prejudice to' clause, a waiver "
                "bar, or a stated parent framework each satisfies this.")
    if "partially expressed construct" in gap_text.lower():
        return ("Carry the substance already present through to every provision it "
                "should govern, so the property holds across the document rather "
                "than in the clauses where it happens to appear.")
    if construct == "Coupling":
        return "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing."
    if construct == "Coherence Test":
        return "Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger."
    if construct == "Integrity Layer":
        return "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use."
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
    subject = "control" if component == "control" else f"{component} control"
    return (
        f"Create a verification test that samples this {subject}, confirms the named "
        f"owner, trigger, evidence artifact, escalation route, and review outcome, "
        f"and records pass/follow-up status."
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
    # construct_coverage is a LAIF-VOCABULARY check. Calling a construct
    # "missing" on that basis contradicts the same run's functional-alignment
    # verdict: a document whose obligations are demonstrably bound to the
    # interests they protect, in its own words, is not missing Coupling. Where
    # the substance is present, the only thing absent is LAIF's wording, and
    # that is a certification-channel item, not a governance gap.
    _functional = result.get("functional_alignment", {}) or {}
    # The vocabulary-only constructs (Structural Transparency/Honesty/Containment)
    # are components of the Integrity Layer; the Coherence Test is LAIF's named
    # instrument. Map each coverage key to the construct whose substance covers it.
    _covered_by = {
        "Structural Transparency": "Integrity Layer",
        "Structural Honesty": "Integrity Layer",
        "Structural Containment": "Integrity Layer",
    }
    for construct, present in (result.get("construct_coverage", {}) or {}).items():
        if present:
            continue
        substance_key = _covered_by.get(construct, construct)
        verdict = (_functional.get(substance_key) or {}).get("verdict")
        external = result.get("assessment_mode") == "external_framework"
        if verdict in ("DECLARED", "FUNCTIONAL"):
            entries.append(
                f"Certification channel — {construct} is expressed functionally in "
                f"the document's own vocabulary; only LAIF-native wording is absent")
        elif construct == "Coherence Test" and external:
            # LAIF's own named decision instrument. An external instrument has
            # never claimed to contain it; its absence is adoption distance.
            entries.append(
                "Certification channel — the Coherence Test is LAIF's named decision "
                "instrument; an external document is not expected to contain it")
        elif verdict == "PARTIAL":
            entries.append(
                f"Partially expressed construct: {construct} — some of its substance is "
                f"present in the document's own vocabulary, but not enough to carry it")
        else:
            entries.append(f"Missing LAIF construct: {construct}")
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
