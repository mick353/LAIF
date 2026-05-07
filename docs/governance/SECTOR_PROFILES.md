# Sector / Institutional Profiles

## Purpose

Sector profiles are deterministic diagnostic overlays for LAIF external-framework assessment. They help the assessment engine recognize institutional language, operational patterns, likely governance-force gaps, and remediation context across real document types.

Profiles improve diagnostic mapping and remediation guidance only. They do not create an alternate compliance path.

## Non-Authority Boundary

Sector profiles do not determine legal validity. They do not state that a document is valid, invalid, binding, non-binding, sector-compliant, or sector-noncompliant.

Profiles do not alter `validate.py`. Profiles do not alter formal LAIF-native certification. Profiles do not alter scoring weights. Profiles do not determine legal validity. Profiles do not create sector-specific compliance gates. Profiles do not make sector law, procurement terms, clinical rules, employment rules, education rules, or government-administration requirements binding unless a separate authority does so.

## Relationship to LAIF-native Certification

LAIF-native certification remains the strict formal gate. A document that fails formal LAIF-native requirements remains a formal fail even when it has high semantic proximity or sector profile proximity.

Formal invariant: **FORMAL FAIL + HIGH SEMANTIC / SECTOR PROXIMITY = FORMAL FAIL.**

Profile signals are secondary diagnostic context. They do not alter binary LAIF-native certification, canonical terminology gates, formal compliance calculation, governance checks, protected artifacts, verified corpus handling, or score weights.

## Profile Fields

Each profile may define:

- `label`: human-readable profile name.
- `purpose`: profile intent and institutional scope.
- `diagnostic_terms`: vocabulary examples used to surface diagnostic signals.
- `risk_indicators`: deterministic sector-risk patterns used for context.
- `expected_evidence`: deterministic artifact patterns used for evidence-gap context.
- `governance_force_emphasis`: governance-force components likely to matter most.
- `remediation_themes`: likely remediation themes for patch wording.
- `evidence_cautions`: source-evidence and authority cautions.
- `remediation_focus`: profile-aware remediation prompts.

These fields are diagnostic metadata only.

## Supported Profiles

### `government_service_delivery`

- **Purpose:** Diagnose AI governance for benefits, licensing, eligibility, enforcement, casework, and citizen-facing public services.
- **Diagnostic vocabulary/examples:** benefit, eligibility, entitlement, claimant, citizen, resident, caseworker, service delivery, administrative review, reasons for decision, public record, appeal.
- **Governance-force emphasis:** actor, trigger, protected interest, evidence, reversibility, escalation, auditability.
- **Likely remediation themes:** identify the service-delivery policy owner; preserve reasons-for-decision, review pathway, and service-impact records; bind automated decisions to human review and records authority support.
- **Source-evidence caution:** do not infer statutory authority, administrative-law compliance, or legal validity from service vocabulary alone; use reviewer-confirmation fallback when exact source text is unavailable.

### `departmental_ai_development`

- **Purpose:** Diagnose internal AI project, model, architecture, security, privacy, release, monitoring, and rollback governance.
- **Diagnostic vocabulary/examples:** model register, AI project owner, architecture review, security review, privacy review, risk assessment, release approval, change control, rollback plan, MLOps.
- **Governance-force emphasis:** actor, trigger, control, evidence, reversibility, auditability.
- **Likely remediation themes:** map AI project ownership to architecture, security, privacy, release governance, monitoring, and rollback reviewers; require model-register and release-approval evidence.
- **Source-evidence caution:** engineering artifacts are not proof of governance approval unless the source says so; do not invent release, approval, or rollback evidence.

### `procurement_vendor_governance`

- **Purpose:** Diagnose AI controls expressed through procurement, contract, vendor assurance, audit access, disclosure, and third-party management language.
- **Diagnostic vocabulary/examples:** procurement, tender, RFP, vendor, supplier, third party, contract clause, due diligence, audit access, assurance artefact, service-level obligation.
- **Governance-force emphasis:** mandate, actor, control, evidence, consequence, auditability.
- **Likely remediation themes:** assign procurement lead with legal/compliance and vendor-management support; translate AI governance into contract clauses, vendor disclosures, audit-access records, and assurance artefacts.
- **Source-evidence caution:** procurement vocabulary does not establish contractual enforceability; do not invent vendor disclosures, audit rights, assurance artifacts, or contract terms.

### `clinical_ai`

- **Purpose:** Diagnose AI governance for clinical recommendations, patient safety, clinician review, clinical fallback, override, and incident pathways.
- **Diagnostic vocabulary/examples:** clinical decision, patient safety, diagnosis, treatment, clinician, physician, medical device, clinical fallback, override record, patient safety review, incident log.
- **Governance-force emphasis:** protected interest, actor, control, evidence, reversibility, escalation.
- **Likely remediation themes:** assign clinical governance owner with clinician reviewer and safety incident pathway; require clinical fallback, override record, patient safety review, and incident log.
- **Source-evidence caution:** clinical vocabulary does not determine medical, regulatory, or legal validity; do not invent clinical validation, safety, override, fallback, or incident evidence.

### `employment_hr_ai`

- **Purpose:** Diagnose hiring, promotion, performance, scheduling, workplace monitoring, adverse-action, and bias-review AI governance.
- **Diagnostic vocabulary/examples:** hiring, recruitment, candidate, employee, worker, performance monitoring, promotion, termination, adverse action, bias review, human review, appeal.
- **Governance-force emphasis:** protected interest, actor, evidence, reversibility, escalation, consequence.
- **Likely remediation themes:** assign HR policy owner with legal/compliance and bias-review support; require adverse-action review, bias evidence, human review, and appeal records.
- **Source-evidence caution:** HR vocabulary does not establish employment-law compliance or legal validity; do not invent bias evidence, adverse-action evidence, or appeal records.

### `education_ai`

- **Purpose:** Diagnose AI governance for admissions, grading, learning analytics, student support, accessibility, appeal pathways, and academic governance.
- **Diagnostic vocabulary/examples:** student, learner, grading, assessment, admissions, learning analytics, proctoring, accessibility, accommodation, appeal pathway, academic governance.
- **Governance-force emphasis:** protected interest, actor, control, evidence, reversibility, escalation.
- **Likely remediation themes:** assign education policy owner with student support, accessibility, and academic governance reviewer; require student-impact review, appeal pathway, and accessibility records.
- **Source-evidence caution:** education vocabulary does not determine education-law compliance, academic validity, or legal validity; do not invent appeal, accessibility, student-support, or academic-governance evidence.

### `general_ai_governance`

- **Purpose:** Provide a neutral diagnostic overlay for AI governance documents that do not match a more specific institutional profile.
- **Diagnostic vocabulary/examples:** accountability, transparency, human oversight, risk assessment, audit, incident, redress, risk management.
- **Governance-force emphasis:** mandate, actor, protected interest, control, evidence, auditability.
- **Likely remediation themes:** translate principles into mandate, actor, trigger, protected interest, control, evidence, reversibility, escalation, consequence, and auditability.
- **Source-evidence caution:** general governance vocabulary does not prove formal compliance, sector compliance, or legal validity; use reviewer-confirmation fallback when exact evidence text is absent.

## Profile-Specific Diagnostic Signals

Profile diagnostic signals are deterministic vocabulary matches. They help reviewers see why a document was mapped to an institutional context. They are not score credit, not compliance evidence, and not proof of legal authority.

## Profile-Specific Remediation Guidance

Profiles may enrich remediation patches with institutionally specific actors and evidence artifacts, such as service-delivery records, model registers, contract clauses, clinical fallback records, adverse-action reviews, or student-impact reviews.

This enrichment is wording context only. It does not assert that the source document contains those artifacts unless exact source text is available.

## Anti-Gaming / Keyword Arbitrage Boundary

Profile signals must not become keyword-stuffing shortcuts. A document can mention many sector terms and still fail formal LAIF-native certification or score poorly on substantive governance dimensions.

Profiles do not alter scoring weights. Profiles do not add new certification pathways. Profiles do not create sector-specific compliance gates.

## Evidence Trace Boundary

Profile output must not generate source evidence unless exact source text is available. Where exact quoted evidence is unavailable, remediation patches retain a reviewer-confirmation fallback.

Profile diagnostics do not replace source evidence, legal review, institutional authority, or LAIF-native certification review.

## Future Profile Expansion

Future profiles may add vocabulary, diagnostic hints, remediation themes, and evidence cautions. Future expansion must preserve the same non-authority boundary: no changes to `validate.py`, formal LAIF-native certification, scoring weights, legal-validity determinations, or sector-specific compliance gates.
