# LAIF Result Taxonomy

LAIF uses several result channels. They must not be collapsed into a single generic verdict. In particular, **FAIL must always be mode-scoped**: a repository workflow failure, a LAIF-native certification failure, and an external diagnostic gap mean different things.

## Summary Table

| Result channel | What it answers | What it does not answer |
|---|---|---|
| Infrastructure PASS/FAIL | Did a script, test, validation job, or CI gate complete under repository rules? | Whether an external law, policy, or standard is legally valid or substantively worthless. |
| LAIF-native certification PASS/FAIL | Does a document claiming or seeking LAIF-native status satisfy strict LAIF-native criteria? | Whether a non-LAIF external framework is legally invalid, unsafe, or valueless. |
| External framework diagnostic finding | What governance-force strengths, ambiguities, and gaps appear when an external document is reviewed through the LAIF model? | Certification, legal validity, or authoritative regulatory compliance. |
| Governance-force gap | Which obligation lacks sufficient mandate, actor, trigger, protected interest, control, evidence, reversibility, escalation, consequence, or auditability? | Proof that the source has no governance value under its own framework. |
| Remediation priority | Which additions or patches would most improve LAIF alignment or operational force? | A mandatory legal amendment unless an adopting institution makes it one. |
| Semantic-boundary advisory | Did a change touch wording that may affect LAIF-sensitive terms or public interpretation? | A governance judgment on an external document. |
| Protected-artifact block | Did repository rules block modification of protected files, reports, manifests, or source artifacts? | Whether the blocked content is correct or legally authoritative. |
| Evidence/provenance verification | Are source artifacts, manifests, hashes, citations, or evidence traces internally verifiable? | Whether the upstream legal instrument is valid or complete beyond the recorded provenance. |
| Generated report output | What did the reporting layer render from current assessment data? | Independent authority beyond the underlying assessment mode and source provenance. |
| Legal validity non-determination | Explicit boundary that LAIF does not decide legal validity. | A legal opinion, court finding, regulator decision, or jurisdictional compliance rating. |

## Result Definitions

### Infrastructure PASS/FAIL

Infrastructure PASS/FAIL is a repository or execution result. Examples include Python compilation, governance checks, validation commands, and test suites. An infrastructure `FAIL` means the repository workflow or command did not satisfy its expected condition. It is not a governance judgment on any external law, policy, procurement rule, or vendor document.

### LAIF-native certification PASS/FAIL

LAIF-native certification PASS/FAIL is strict and binary. It applies when a document claims or seeks LAIF-native certification, LAIF adoption, or formal LAIF compliance. Canonical LAIF terms and structures are load-bearing in this mode. A `FAIL` in this channel means the document did not satisfy LAIF-native criteria; the result is model-bound to LAIF-native certification.

### External framework diagnostic finding

An external framework diagnostic finding is a model-relative observation about an external law, standard, policy, departmental document, procurement rule, vendor policy, or operational AI governance instrument. It does not require the source to use LAIF vocabulary. It identifies how the source appears under the LAIF model, especially around governance force, ambiguity, reversibility, auditability, enforceability, accountability, evidence, and remediation gaps.

### Governance-force gap

A governance-force gap identifies a missing or weak operational element. Typical gaps include unclear mandatory language, no responsible actor, no activation trigger, no protected interest, no control, no evidence artifact, no reversal path, no escalation path, no consequence, or insufficient independent auditability. A governance-force gap is a remediation signal, not a declaration that the external framework is invalid on its own authority.

### Remediation priority

A remediation priority ranks additions or patches that would improve LAIF-native alignment or governance force. It may point to clauses, controls, evidence artifacts, verification tests, accountability structures, or escalation rules. Remediation priorities are additive adoption guidance unless a regulator, institution, contract, or policy separately makes them binding.

### Semantic-boundary advisory

A semantic-boundary advisory is an internal repository-governance result. It warns that a change may affect LAIF-sensitive terms, public wording, certification semantics, or assessment boundaries. Advisory status supports human review; it is not a finding about an external document.

### Protected-artifact block

A protected-artifact block is an internal repository-governance result. It blocks unauthorized changes to protected artifacts, verified manifests, raw sources, generated reports, or other guarded files according to repository policy. The block protects provenance and review integrity; it does not say that an external framework is legally valid or invalid.

### Evidence/provenance verification

Evidence/provenance verification checks whether recorded sources, hashes, manifests, citations, and evidence traces are internally consistent and reproducible. A verification failure is a provenance or repository-integrity problem. It is not a legal-validity determination about the upstream instrument.

### Generated report output

Generated report output is the rendered expression of current assessment data. Reports inherit the limits of their source corpus, assessment mode, rubric, and provenance status. A generated report should preserve mode labels so that LAIF-native certification results, external diagnostic findings, and repository workflow results are not confused.

### Legal validity non-determination

Legal validity non-determination is a standing boundary on all LAIF outputs. LAIF does not determine whether an external law, regulation, policy, departmental rule, procurement instrument, vendor policy, standard, or operational control is legally valid, enforceable under its own jurisdiction, or authoritative for any external institution.

## Required Interpretation Rules

1. **FAIL must always be mode-scoped.** Use labels such as `LAIF-native certification FAIL`, `infrastructure FAIL`, or `protected-artifact block` rather than unscoped failure language.
2. **Not LAIF-native is not legal invalidity.** A document can fail LAIF-native certification while remaining legally valid, institutionally useful, enforceable under its own authority, or valuable for governance.
3. **External diagnostic findings are model-relative.** They describe what LAIF detects or does not detect under its current rubric and governance-force model.
4. **CI and protected-artifact failures are repository workflow results.** They must not be presented as governance judgments on external documents.
5. **Generated reports must preserve result boundaries.** Report headings and summaries should distinguish certification, diagnostic, remediation, evidence/provenance, and repository-governance results.

## Phase 3N Structured Remediation Patch Schema

Structured remediation records are defined in [REMEDIATION_PATCH_SCHEMA.md](REMEDIATION_PATCH_SCHEMA.md). They convert existing diagnostic findings into machine-readable patches, controls, evidence artifacts, verification tests, and responsible-actor guidance. These records are diagnostic unless separately adopted by a regulator, institution, contract, procurement process, or other authority, and they do not determine legal validity or certify LAIF-native compliance.

## Phase 3P Evidence Trace Reference

Phase 3P evidence traces are deterministic source-support metadata only. Exact or deterministic traces require direct source-text presence; otherwise the reviewer-confirmation fallback is used. See [Evidence Trace Model](EVIDENCE_TRACE_MODEL.md).

## Phase 3Q Calibration and Score Justification Reference

See [CALIBRATION_SCORE_JUSTIFICATION.md](CALIBRATION_SCORE_JUSTIFICATION.md) for the shared boundary governing score bands, score justification metadata, dimension justifications, calibration cautions, gaming-risk notes, evidence/sector/remediation relationships, and the rule that LAIF-model signal strength does not determine legal validity or certify LAIF-native compliance.

## Public report template reference

Public-facing rendering requirements are defined in [Public Report Template](PUBLIC_REPORT_TEMPLATE.md). That template is presentation-only and does not change scoring, validation, certification, evidence, remediation, sector-profile, calibration, or governance invariants.

## Phase 3S System QA Release Audit Reference

See [SYSTEM_QA_RELEASE_AUDIT.md](SYSTEM_QA_RELEASE_AUDIT.md) for the release-readiness audit boundary covering validation/certification separation, diagnostic modes, evidence, remediation, sector profiles, calibration, public reporting, protected artifacts, and verified corpus limits. That audit is documentation/test-only and does not change runtime behavior.


## Phase 3V governance repair fields

External-framework JSON and markdown outputs include a governance repair profile: `document_type`, `recommended_use`, `not_sufficient_for`, `governance_force_profile`, `systemic_repair_value`, `operational_closure_rating`, `evidence_sufficiency_rating`, `accountability_closure_rating`, `lifecycle_control_rating`, `residual_risk_control_rating`, `implementation_gap_rating`, `failure_pathway_risk`, and `priority_repair_actions`. These fields are deterministic presentation mappings from existing diagnostic scores, evidence traces, remediation patches, formal flags, sector signals, and detected gaps; they do not alter scoring weights or formal validation. See `GOVERNANCE_REPAIR_REPORTING.md` and the Phase 3S System QA Release Audit Reference in `SYSTEM_QA_RELEASE_AUDIT.md`.
