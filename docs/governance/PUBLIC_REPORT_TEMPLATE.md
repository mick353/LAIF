# Public Report Template

## Purpose

The public report template defines the presentation boundary for LAIF generated
markdown reports. Public reports are diagnostic LAIF-model outputs intended to
make existing assessment results readable for public-sector, departmental,
procurement, legal/compliance, vendor, clinical, HR, and education governance
audiences without changing assessment semantics.

## Public Report Boundary

Public reports do not determine legal validity. Public reports do not certify LAIF-native compliance unless the LAIF-native certification gate separately passes. Public reports do not certify LAIF-native compliance unless the LAIF-native certification gate separately passes. Report
rendering is presentation-only and must not alter validation, binary
certification, formal compliance calculation, scoring weights, rubric pattern
logic, evidence trace extraction, remediation patch generation, sector profile
metadata, or calibration metadata.

External-framework reports must use diagnostic language. “Not LAIF-native” is
certification-channel wording only, not legal/governance invalidity and not a
finding about a source's authority under its own legal or institutional regime.
Reports must not say or imply that high scores override formal failure. High semantic, sector, evidence, or calibration proximity must not override formal LAIF-native failure. Reports must preserve exact-source and reviewer-confirmation boundaries.

## Audience

Reports should be understandable to government, departmental, procurement,
legal/compliance, vendor, clinical, HR, education, and governance-review
audiences. The template should support stakeholder reading without encouraging
shortcut certification, legal overclaiming, or keyword stuffing.

## Required Report Sections

Generated markdown reports should use these stable public sections:

1. Title: `LAIF Institutional Structural Governance Assessment Report`
2. Report Scope and Boundary
3. Executive Brief
4. Method Summary
5. Cross-Document Dashboard
6. Per-Document Assessment
7. Closing Interpretation Notes

Per-document assessments should include Document Overview, Mode / Boundary
Notice, Executive Diagnostic Summary, Scorecard, Score Calibration and
Justification, Governance-Force Profile, Sector / Institutional Context,
Evidence Trace Summary, Construct Crosswalk, Diagnostic Gaps, Structured
Remediation Patch Set, and Limits and Reviewer Actions.

## Executive Brief Rules

The executive brief should summarize total documents assessed, LAIF-native
certification status, external-framework diagnostic status, average overall
readiness, average conceptual proximity, average sector alignment, evidence
trace totals, remediation patch totals, and top governance-force patterns. It
must include a clear boundary note that the report is diagnostic, not
certification, does not determine legal validity, and requires reviewer
confirmation.

## Mode and Certification Wording

LAIF-native certification may use scoped labels such as `PASS`, `FAIL`, `not
LAIF-native`, and `canonical remediation required`. External-framework reports
must say they are diagnostic, not certification. The phrase “Not LAIF-native”
should appear only as certification-channel wording and must not be framed as
legal invalidity, governance invalidity, institutional worthlessness, or a
shortcut to legal conclusions.

## Legal / Authority Boundary Wording

Reports must state that they do not determine legal validity and are not legal
advice. Remediation guidance becomes binding only if a regulator, institution,
contract, procurement process, policy owner, or other competent authority
separately adopts it. Reviewer actions should include confirmation of source
authority, actor assignment, evidence artifact verification, escalation and
reversibility review, and authority determination.

## Score Presentation Rules

Scores are deterministic LAIF rubric outputs and interpretation aids only.
Reports must not present score bands as compliance ratings or imply that high
scores override formal failure. The formal invariant remains: FORMAL FAIL + HIGH
SEMANTIC / SECTOR / EVIDENCE / CALIBRATION PROXIMITY = FORMAL FAIL.

## Evidence Trace Presentation Rules

Evidence trace output should be concise. It should show total traces,
exact/deterministic count, fallback count, top trace IDs and evidence types, and
reviewer-confirmation fallback where none are linked. Reports must preserve
exact-source and reviewer-confirmation boundaries. Evidence traces do not prove
implementation, authority, operational adoption, or legal effect.

## Remediation Patch Presentation Rules

Structured remediation patches should be institution-facing and readable. Public
reports should show patch_id, finding_type, severity, diagnostic_gap,
recommended_patch, operational_control, evidence_artifact, verification_test,
responsible_actor, evidence_trace_ids, and legal_authority_boundary. A reviewer
action line should prompt confirmation of source authority, actor assignment,
evidence artifacts, escalation/reversibility, and institution/regulator/contract
authority.

## Sector Profile Presentation Rules

Sector profiles contextualize diagnostics and remediation guidance. They do not
create sector compliance gates, determine legal validity, or certify LAIF-native
compliance. Reports should show the selected profile, purpose, diagnostic
signals, governance-force emphasis, evidence cautions, and relevant interests in
compact form.

## Calibration / Anti-Gaming Presentation Rules

Reports must not expose raw regex patterns and reports must not encourage keyword stuffing. Reports must not encourage keyword stuffing. Fired and missed signal labels may be summarized, but pattern syntax,
regex internals, and keyword recipes must not be printed. Calibration language
should reinforce that structural evidence, accountable controls, reversibility,
consequence, auditability, and reviewer confirmation remain necessary.

## Unsafe Phrases / Prohibited Wording

Public report output must avoid unscoped phrases that overclaim failure or legal
status, including: Final verdict; Primary Failure Modes; legally invalid;
governance-invalid; governance-worthless; structurally incoherent; compliance
rating; certified compliant; invalid under law; unlawful; must amend law; and
safe/unsafe as a legal status. Scoped LAIF-native certification wording is
allowed when clearly tied to the certification channel.

## Report Stability / Snapshot Expectations

Public report rendering should be deterministic for a fixed set of assessment
results. Timestamp additions should be avoided unless tests and snapshot rules
explicitly account for them. Rendering must not mutate score_breakdown,
overall_readiness_score, formal_laif_native_compliance, remediation_patches,
evidence_traces, score_justification, or sector profile metadata.

## Future Report Template Work

Future work may add HTML/PDF styling, stakeholder-specific summaries,
accessibility checks, redaction tooling, and versioned template snapshots. Such
work must remain presentation-only unless a separate governance-approved phase
changes assessment semantics.
