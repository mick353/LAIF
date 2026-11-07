# Control evidence review

This report connects a stated policy claim to supplied sources, recorded tests and operational-review records. It does not authenticate the records or approve deployment.

Controls supplied: 1. Review-ready diagnostics: 0. Read each control's status and issues; a record-level result is not a control-effectiveness finding.

## Input identity and scope

- Policy file: docs/verified/raw/au\_dta\_policy\_v2\_1.md
- Policy SHA-256: 3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b
- Canonical input-manifest digest: b8192f9ed112fced4fdb083db289e51468d873093f07256da046e5116e9d43b3
- Strict source scope: True; strict action receipts: True.
- Source completeness, when attested, is not proven exhaustive. Receipts and reviewer identity are not authenticated. No LAIF certification or operational validation.

No source-scope attestation supplied. An omitted document cannot be discovered from this manifest alone.

| Source | File | Disposition | Reference check | SHA-256 |
|---|---|---|---|---|
| No supporting source inventory supplied | — | — | Not established | — |

## Control: dta-before-deployment-assessment

**Diagnostic status:** SCOPE\_UNDECLARED

**Evidence grade:** POLICY\_CLAIM\_ONLY

### Stated requirement

> Before the solution is deployed, agencies must finalise the assessment and apply any agreed risk treatments.

Quote check: EXACT\_POLICY\_TEXT\_CHECKED. Quotation identity does not establish implementation or legal force.
Required supporting sources: not declared

### Supplied test records

Legacy declared test records: 0. Their PASS/FAIL labels are declarations, not authenticated execution receipts.

Action-receipt check: EXECUTION\_UNTESTED. Recorded environment, version and run identity are supplied metadata, not independently observed execution.

| Test | Kind | Expected | Recorded | Environment | Run | Receipt SHA-256 |
|---|---|---|---|---|---|---|
| No validated action receipts | — | — | — | — | — | — |

### Operational review and remedy

Record status: NOT\_SUPPLIED. A recorded review is not authenticated independent verification.

### Issues and next review

- strict scope requires a source inventory

Resolve the source or test evidence gaps before treating this control as review-ready.

For an operational assurance claim, obtain or correct the review, including authorised execution, a separate recorded reviewer and any necessary remediation/retest.
