# Public Report Template

## Document Runner Metadata

When public reports are generated through `scripts/laif_process_document.py`, the rendered report is preceded by extraction and processing metadata, including extractor used, extracted character count, original file name, source SHA-256, processing timestamp, and output paths. This metadata documents the ingestion wrapper context and does not alter the underlying assessment result.

## Purpose

The public report template defines how LAIF assessment results may be rendered for publication, procurement, departmental, legal/compliance, vendor, clinical, HR, education, and governance audiences. Public reports are diagnostic LAIF-model outputs: they present already-computed assessment data in a stable institutional format without changing scoring, validation, certification, evidence, remediation, sector-profile, or calibration behavior.

## Public Report Boundary

Public reports are diagnostic LAIF-model outputs. Public reports do not determine legal validity. Public reports do not certify LAIF-native compliance unless the LAIF-native certification gate separately passes. External-framework reports must use diagnostic language and must not be presented as LAIF-native certification.

“Not LAIF-native” is certification-channel wording only, not legal/governance invalidity. A report may identify a document as not LAIF-native for LAIF certification purposes while preserving the separate question of legal authority, regulatory acceptance, institutional adoption, procurement suitability, or domain-specific governance effect.

## Audience

The template is written for public and institutional stakeholders who need readable governance diagnostics without source-code or rubric internals. Expected readers include government officials, departmental reviewers, procurement teams, legal and compliance reviewers, vendors, clinical governance teams, HR governance teams, education governance teams, auditors, and policy owners.

## Required Report Sections

A public markdown report should include these stable sections:

1. Title: `LAIF Institutional Structural Governance Assessment Report`.
2. Report Scope and Boundary.
3. Executive Brief.
4. Method Summary.
5. Cross-Document Dashboard.
6. Per-Document Assessment.
7. Closing Interpretation Notes.

Each per-document assessment should include Document Overview, Mode / Boundary Notice, Executive Diagnostic Summary, Scorecard, Score Calibration and Justification, Governance-Force Profile, Sector / Institutional Context, Evidence Trace Summary, Construct Crosswalk, Diagnostic Gaps, Structured Remediation Patch Set, and Limits and Reviewer Actions.

## Executive Brief Rules

The executive brief should be concise and institution-facing. It should summarize document count, LAIF-native certification status, external-framework diagnostic status, average readiness and proximity scores, average sector alignment, evidence trace counts, remediation patch counts, top governance-force patterns, and the boundary that diagnostic proximity cannot override formal LAIF-native failure.

## Mode and Certification Wording

Use mode-scoped wording:

- LAIF-native certification: `PASS`, `FAIL`, `not LAIF-native`, or `canonical remediation required` where applicable.
- External framework structural assessment: diagnostic, not certification.
- External-framework reports must use diagnostic language.
- Do not imply a certification shortcut from a high score, evidence trace, sector profile, or calibration justification.
- Public reports do not certify LAIF-native compliance unless the LAIF-native certification gate separately passes.

## Legal / Authority Boundary Wording

Public reports must state that they do not determine legal validity. They must not present a source as valid or invalid under law. They must explain that remediation guidance becomes binding only if an institution, regulator, contract, statute, policy owner, or other authority separately adopts it.

## Score Presentation Rules

Scores are deterministic LAIF-model rubric outputs. Reports must not present score bands as compliance ratings. Score bands describe readiness or proximity for diagnostic interpretation only. Reports must not say or imply that high scores override formal failure. FORMAL FAIL + HIGH SEMANTIC / SECTOR / EVIDENCE / CALIBRATION PROXIMITY = FORMAL FAIL.

## Evidence Trace Presentation Rules

Reports must preserve exact-source and reviewer-confirmation boundaries. Evidence trace presentation should be concise and should show total traces, exact/deterministic counts, fallback counts, top trace IDs and evidence types, and a reviewer-confirmation fallback when no trace is linked. Reports must not print long quotes and must not imply evidence traces prove implementation, authority, adoption, or operational effectiveness.

## Remediation Patch Presentation Rules

Structured remediation patches should be readable for institutional owners. Reports should show patch_id, finding_type, severity, diagnostic_gap, recommended_patch, operational_control, evidence_artifact, verification_test, responsible_actor, evidence_trace_ids, and legal_authority_boundary. Include reviewer actions to confirm source authority, assign an actor, verify the evidence artifact, confirm escalation and reversibility, and determine institution/regulator/contract authority.

## Sector Profile Presentation Rules

Sector profile material is diagnostic context only. It may identify materially relevant interests, expected evidence artifacts, profile-specific remediation themes, evidence cautions, and sector diagnostic signals. It must not change legal obligations, formal LAIF-native certification, scoring weights, or sector authority.

## Calibration / Anti-Gaming Presentation Rules

Calibration summaries should explain score interpretation, calibration cautions, and anti-gaming boundaries without exposing raw detection internals. Reports must not expose raw regex patterns. Reports must not encourage keyword stuffing. Fired and missed signal labels may be shown as public summaries, but pattern strings and recipe-like optimization instructions must not be disclosed.

## Unsafe Phrases / Prohibited Wording

Public report rendering must avoid unscoped phrases that overclaim legal, governance, or certification status. Avoid wording such as “Final verdict,” “Primary Failure Modes,” “legally invalid,” “governance-invalid,” “governance-worthless,” “structurally incoherent,” “compliance rating,” “certified compliant,” “invalid under law,” “unlawful,” and “must amend law.” Where a formal result is necessary, scope it to the LAIF-native certification channel.

## Report Stability / Snapshot Expectations

Public reports should be deterministic for the same assessment inputs and report date. Rendering changes must not alter score_breakdown, overall_readiness_score, formal_laif_native_compliance, remediation_patches, evidence_traces, score_justification, calibration metadata, or sector profile metadata. Committed generated reports should not be updated as part of template hardening unless a separate release process explicitly requires it.

## Future Report Template Work

Future work may add optional audience-specific front matter, export profiles, accessibility improvements, regulator-specific annexes, and reviewer sign-off workflows. Such work should remain presentation-only unless a separate change explicitly updates scoring, validation, certification, or governance policy.

## Phase 3S System QA Release Audit Reference

See [SYSTEM_QA_RELEASE_AUDIT.md](SYSTEM_QA_RELEASE_AUDIT.md) for the release-readiness audit boundary covering validation/certification separation, diagnostic modes, evidence, remediation, sector profiles, calibration, public reporting, protected artifacts, and verified corpus limits. That audit is documentation/test-only and does not change runtime behavior.
