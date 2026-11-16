"""LAIF engine: classification. Moved without changing assessment rules."""

import re
from .detection import (
    CONTROL_REGISTER_POPULATED_PAT,
)


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
    # Weakest instrument form: it must never outrank a document that actually
    # imposes duties, so it sits last before "unknown".
    "values_charter",
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
    # Internal policy also covers the corporate "standard"/"procedure" register:
    # an owner line, an approving body, an entity-wide binding clause, and a
    # breach consequence are the institutional form of the same instrument.
    ("internal_policy", (r"\binternal policy\b", r"\bdepartment(?:al)? policy\b", r"\bcompany policy\b", r"\borganitational policy\b", r"\borganisational policy\b", r"\borganizational policy\b", r"\bthis policy (?:sets out|applies|governs|covers)\b", r"\bapplies to all (?:staff|employees|personnel)\b", r"\bstaff(?:,| and) contractors\b", r"\bfor board approval\b", r"\bpolicy will be reviewed\b", r"\bversion \d", r"\bthis (?:standard|procedure|framework|instruction|directive|register|guideline)\s+(?:binds|applies to|sets out|governs|covers)\b", r"^\s*owner\s*:", r"\bapproved by\s*:", r"\bnon.compliance\b.{0,100}\b(?:reportable|disciplinary|breach|sanction)", r"\b(?:group|enterprise|corporate|firm.wide|bank.wide|company.wide)\s+(?:policy|standard|framework|procedure)\b", r"\bbinds all\b.{0,60}\b(?:entities|units|divisions|subsidiaries|functions)\b", r"\breview\s*:\s*(?:annual|biennial|quarterly)", r"\bchange control\b",
                        # A populated control register with named owners is an
                        # institutional operating instrument in table form.
                        CONTROL_REGISTER_POPULATED_PAT)),
    ("vendor_compliance_submission", (r"\bvendor submission\b", r"\bcompliance submission\b", r"\battestation\b", r"\bsupplier response\b")),
    # A statement of values and intent. Naming it correctly matters: its
    # assurance value is not "low", it is absent until the values are converted
    # into duties, and a reviewer told this can stop looking for controls.
    ("values_charter", (r"\bcharter\b", r"\bour values\b", r"\bwe believe\b", r"\bwe are committed to\b",
                        r"\bstatement of (?:principles|values|intent)\b", r"\bcode of ethics\b",
                        r"\bwe (?:strive|aspire|aim) to\b", r"\bguiding principles\b",
                        r"\bresponsible ai principles\b", r"\bmanifesto\b")),
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
    "values_charter": "Statement of values and intent; it creates no duty, no owner, and no evidence obligation, so it carries no assurance force until its values are expressed as operative commitments.",
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
    "values_charter": ("Communicating institutional intent, and identifying which values still need to be converted into duties.", "Not sufficient as assurance for any decision: it states intent without duties, owners, evidence, or consequences. Ask for the policy or procedure that implements it."),
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
        if not any(anchor in haystack for anchor in ("regulation laying down", "harmonised rules", "artificial intelligence act", "eu ai act", "official journal")):
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
    if doc_type == "procurement_assessment_form":
        # A passing mention of "supplier" or "contract" inside an institutional
        # policy must not classify that policy as a procurement instrument:
        # require a genuine procurement-instrument anchor.
        # Response-side anchors ("supplier response", "vendor submission")
        # belong to vendor_compliance_submission, not to the buyer's instrument.
        anchors = ("assessment form",
                   "invitation to tender", "request for proposal", "tender",
                   "procurement questionnaire", "pre-acquisition", "contract schedule",
                   "supplier assurance questionnaire")
        if any(a in haystack for a in anchors):
            return max(hits, 2)
        # Otherwise demand a procurement-led document, not an incidental mention.
        return hits if hits >= 3 and "procurement" in haystack else 0
    if doc_type == "vendor_compliance_submission":
        anchors = ("vendor submission", "compliance submission", "supplier response",
                   "attestation")
        return max(hits, 2) if any(a in haystack for a in anchors) else 0
    if doc_type == "implementation_guide":
        anchors = ("implementation guide", "playbook", "guidance for implementing",
                   "how to implement")
        return max(hits, 2) if any(a in haystack for a in anchors) else 0
    if doc_type == "internal_policy":
        # A populated control register with named owners is decisive on its own:
        # it is an institutional operating instrument written in table form.
        if re.search(CONTROL_REGISTER_POPULATED_PAT, haystack, re.IGNORECASE):
            return max(hits, 2)
        # Otherwise two independent policy signals, so a single stray phrase
        # cannot classify.
        return hits if hits >= 2 else 0
    if doc_type == "values_charter":
        # Values vocabulary alone is not enough: a policy can open with values
        # and then impose duties. The distinguishing property is the ABSENCE of
        # sustained mandatory language — a charter that says "shall" repeatedly
        # is a policy that happens to be called a charter.
        mandatory = len(re.findall(r"\b(?:shall|must)\b", haystack))
        return hits if hits >= 2 and mandatory <= 1 else 0
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
        # "human review" removed: a generic governance phrase common to
        # employment, clinical, and commercial policies. As a public-sector
        # marker it misclassified an employment framework as government policy.
        "accountable official",
        "accountable officials",
        "digital transformation agency",
        "public sector policy",
    )
    hits = sum(haystack.count(term) for term in strong_terms)
    if re.search(r"\bdta\b", haystack):
        hits += 1
    return hits


def known_instrument_profile(text, name="", source_type=""):
    """Identify the document as a *specific named instrument*, or return "".

    Corpus-specific naming (DTAC control names, EU AI Act obligation registers,
    NIST register names) may only be applied to the instrument it belongs to.
    Inferring it from sector or document class alone labelled unrelated
    documents with standards they are not — an NHS Trust's own policy was
    described as a DTAC submission. Identity requires an anchor in the text or
    title, never a category match.
    """
    hay = f"{name or ''} {source_type or ''} {text or ''}".lower()
    if any(a in hay for a in ("dtac", "digital technology assessment criteria",
                              "dcb0129", "dcb0160")):
        return "dtac"
    if any(a in hay for a in ("eu ai act", "artificial intelligence act",
                              "regulation laying down harmonised rules",
                              "oj_l_202401689", "2024/1689")):
        return "eu_ai_act"
    if any(a in hay for a in ("executive order 14110", "2023-24283",
                              "safe, secure, and trustworthy artificial intelligence")):
        return "eo_14110"
    if any(a in hay for a in ("nist ai 100-1", "ai risk management framework",
                              "ai rmf")):
        return "nist"
    if any(a in hay for a in ("policy for the responsible use of ai in government",
                              "responsible use of ai in government",
                              "digital transformation agency")):
        return "australian_policy"
    return ""


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
    # Instrument-form anchors outrank sector vocabulary. A tender that buys a
    # clinical system is a procurement instrument whose subject happens to be
    # clinical; classifying it as a clinical assurance checklist misstates who
    # the document binds and how its force arises. The clinical dimension is
    # carried by the sector profile, which is a separate axis.
    # Issuing side: the buyer's instrument, which imposes the requirements.
    _PROCUREMENT_ISSUING_ANCHORS = (
        "invitation to tender", "request for proposal", "request for tender",
        "supplier assurance questionnaire", "procurement questionnaire",
        "contract schedule", "pre-qualification questionnaire",
    )
    # Responding side: the supplier's answer to it, which asserts compliance.
    # These are different instruments with different force and different
    # reviewer duties — an attestation needs independent verification, a tender
    # needs contract conditions — so they must never be conflated.
    _VENDOR_RESPONSE_ANCHORS = (
        "supplier response", "vendor submission", "compliance submission",
        "tender response", "attestation", "we attest", "submitted by:",
    )
    if any(anchor in haystack for anchor in _PROCUREMENT_ISSUING_ANCHORS):
        return "procurement_assessment_form"
    if any(anchor in haystack for anchor in _VENDOR_RESPONSE_ANCHORS):
        return "vendor_compliance_submission"
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
    return _keyword_sector_fallback(lowered)


# Documents whose type does not itself determine a sector (internal policies,
# guides, procurement instruments, unclassified documents) still deserve their
# sector profile. Whole-word counting only: substring matching routed documents
# on fragments such as "hr" inside "through". A single incidental mention is
# never a sector — a clear signal or a clear margin is required.
_SECTOR_KEYWORDS = (
    ("clinical_ai", ("clinical", "clinician", "patient", "patients", "diagnosis",
                     "medical", "healthcare", "nhs", "dcb0129", "hazard log")),
    # "worker"/"workers" deliberately excluded: they are common in general AI
    # governance texts (labour-market passages) and would misroute them.
    ("employment_hr_ai", ("employee", "employees", "hiring", "recruitment",
                          "candidate", "candidates", "workforce management",
                          "human resources", "dismissal", "promotion",
                          "employment decision", "employment decisions")),
    ("education_ai", ("student", "students", "pupil", "school", "curriculum",
                      "academic", "learner", "learners")),
    # "customer"/"model" deliberately excluded: both are common in general AI
    # governance texts and would misroute them. The terms below name financial
    # decisions and financial-supervisory machinery specifically.
    ("financial_services_ai", ("credit", "lending", "loan", "mortgage",
                               "underwriting", "borrower", "applicant",
                               "policyholder", "premium", "affordability",
                               "anti-money-laundering", "aml", "model risk",
                               "model validation", "financial crime", "bank")),
    ("procurement_vendor_governance", ("procurement", "tender", "supplier",
                                       "suppliers", "vendor", "vendors",
                                       "contract", "contracts")),
    ("government_service_delivery", ("public service", "public sector",
                                     "citizen", "citizens", "caseworker",
                                     "service delivery", "public benefits",
                                     "government agency", "government agencies",
                                     "claimant", "claimants", "council",
                                     "local authority", "entitlement")),
    ("departmental_ai_development", ("model register", "deployment pipeline",
                                     "rollback", "release management",
                                     "software development")),
)


def _keyword_sector_fallback(lowered):
    def count(term):
        if " " in term:
            return lowered.count(term)
        return len(re.findall(rf"\b{re.escape(term)}\b", lowered))

    scores = sorted(
        ((sum(count(term) for term in terms), sector)
         for sector, terms in _SECTOR_KEYWORDS),
        reverse=True,
    )
    if not scores:
        return "general_ai_governance"
    best, best_sector = scores[0]
    runner_up = scores[1][0] if len(scores) > 1 else 0
    if best >= 4 or (best >= 2 and best >= runner_up * 2):
        return best_sector
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
