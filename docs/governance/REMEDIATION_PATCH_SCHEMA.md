# LAIF Remediation Patch Schema

The remediation patch schema is the machine-readable output model for converting LAIF diagnostic findings into practical institutional remediation artifacts. It is additive to the existing assessment result and does not change scoring logic, rubric weights, formal compliance calculation, validation behavior, or governance checks.

## Boundary Statement

Remediation patches are diagnostic guidance unless a regulator, institution, contract, procurement process, policy owner, or other authority separately makes them binding. Patches do not determine legal validity. Patches do not certify LAIF-native compliance. LAIF-native compliance remains governed by the strict certification channel and must be separately adopted and verified where applicable.

Patch records are intended to make governance principles operational through mandate, actor, trigger, protected interest, control, evidence, reversibility, escalation, consequence, and auditability.

## Patch Record Fields

Every remediation patch record contains the following fields:

| Field | Meaning |
|---|---|
| `patch_id` | Stable deterministic identifier for the patch within an assessment result. |
| `assessment_mode` | Assessment channel that produced the patch, such as external framework assessment or LAIF-native certification mode. |
| `source_document` | Name of the assessed source document. |
| `finding_type` | Controlled classification of the diagnostic finding. |
| `severity` | Controlled severity value for remediation triage. |
| `laif_construct` | LAIF construct or governance-force construct associated with the gap. |
| `governance_force_component` | Operational force component implicated by the gap. |
| `diagnostic_gap` | Human-readable diagnostic gap derived from existing assessment result fields. |
| `source_evidence` | Source evidence available to the deterministic extractor, or reviewer-confirmation fallback language when no direct quote is available. |
| `evidence_trace_ids` | Optional list of deterministic evidence trace IDs linked to this patch; empty when reviewer confirmation is required or no safe link exists. |
| `recommended_patch` | Practical institution-facing remediation action. |
| `canonical_clause_if_adopting_laif` | Optional canonical-style clause guidance for organizations choosing LAIF-native adoption. |
| `operational_control` | Control procedure or mechanism that would operationalize the patch. |
| `evidence_artifact` | Artifact a reviewer should expect after implementation. |
| `verification_test` | Repeatable test used to verify that the patch was implemented. |
| `responsible_actor` | Institutional role expected to own implementation or review. |
| `implementation_priority` | Controlled priority for implementation sequencing. |
| `legal_authority_boundary` | Controlled boundary describing whether the patch is diagnostic, LAIF-adoption guidance, or authority-defined. |

## Allowed `finding_type` Values

- `terminology_gap`
- `construct_gap`
- `auditability_gap`
- `enforceability_gap`
- `reversibility_gap`
- `governance_force_gap`
- `evidence_gap`
- `sector_context_gap`
- `provenance_gap`
- `laif_native_certification_gap`

## Allowed `severity` Values

- `critical`
- `high`
- `medium`
- `low`
- `informational`

## Allowed `implementation_priority` Values

- `immediate`
- `near_term`
- `planned`
- `optional_laif_adoption`

`optional_laif_adoption` is used when the patch is LAIF-native adoption guidance for an external framework unless a separate authority has adopted LAIF-native obligations.

## Allowed `legal_authority_boundary` Values

- `diagnostic_only`
- `laif_native_adoption`
- `institution_defined`
- `regulator_defined`
- `contract_defined`

`diagnostic_only` means the patch is model-relative remediation guidance and does not create a legal obligation by itself. `laif_native_adoption` means the patch supports optional LAIF-native adoption unless an authority separately makes it binding. `institution_defined`, `regulator_defined`, and `contract_defined` are reserved for contexts where the responsible authority, not the diagnostic assessment engine, defines binding force.

## Deterministic Generation Principles

Patch generation uses existing assessment result fields only, including diagnostic gaps, primary diagnostic gaps, recommended remediation steps, structured remediation steps, construct coverage, score breakdown, governance signal metadata, sector findings, sector risk alignment, and available source/provenance metadata.

The generator must not invent source evidence. If no direct source quotation is available to the deterministic extractor, `source_evidence` is set to:

> Not directly quoted by current deterministic extractor; reviewer confirmation required.

Patch text should be practical and institutional: define the gap, assign an owner, require evidence, add escalation or reversibility where needed, create a verification test, and specify the responsible actor. External-framework findings must remain diagnostic-only unless the patch is specifically framed as optional LAIF-native adoption guidance or a separate authority makes it binding.

## Phase 3P Evidence Trace Links

Remediation patches may include optional `evidence_trace_ids` when deterministic source support can be safely linked to the patch. If no exact or deterministic source text can be linked, `evidence_trace_ids` remains empty and `source_evidence` keeps the reviewer-confirmation fallback. See [Evidence Trace Model](EVIDENCE_TRACE_MODEL.md).
