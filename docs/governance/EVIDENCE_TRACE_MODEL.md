# Evidence Trace Model

## Purpose

Evidence trace enrichment adds deterministic source-support metadata to LAIF diagnostic findings, remediation patches, and reports. A trace record identifies source text that the current extractor actually found in the assessed document, or records that reviewer confirmation is required when no direct quote was extracted.

Evidence traces are diagnostic/source-support metadata only. They do not certify LAIF-native compliance, do not change scoring, do not change formal compliance, and do not determine legal validity.

## Non-Hallucination Rule

Trace records must not invent source evidence. A trace may only anchor to source text when the extractor has a deterministic match in the assessed document. The extractor must not use paraphrased source evidence as if it were quoted source text.

## Exact Text Presence Requirement

When `confidence` is `exact` or `deterministic_pattern`, matched_text must equal `assessed_text[start_char:end_char]`. The `start_char` and `end_char` offsets must point into that same assessed text, and `matched_text` must be a direct substring of the assessed document.

If no direct quote was extracted, the trace must use the reviewer-confirmation fallback rather than creating a source anchor.

## Trace Record Fields

Each evidence trace record contains:

| Field | Meaning |
| --- | --- |
| `trace_id` | Stable deterministic identifier for the trace record. |
| `source_document` | Assessed document identifier. |
| `source_type` | Source classification supplied to the assessment engine. |
| `assessment_mode` | Assessment channel, such as external-framework diagnostic or LAIF-native certification. |
| `evidence_type` | Type of source-support signal. |
| `matched_text` | Exact source text when present; empty string for fallback-required traces. |
| `normalized_match` | Normalized comparison metadata derived from `matched_text`; empty for fallback-required traces. |
| `start_char` | Start offset into the assessed source text, or `null` for fallback-required traces. |
| `end_char` | End offset into the assessed source text, or `null` for fallback-required traces. |
| `match_rule` | Deterministic rule that produced the match, or fallback reason. |
| `confidence` | Match confidence category. |
| `supports` | Diagnostic finding, profile signal, governance-force signal, remediation anchor, or provenance signal supported by the trace. |
| `legal_authority_boundary` | Boundary statement preserving diagnostic/legal separation. |

Allowed `evidence_type` values are:

- `source_quote`
- `diagnostic_term`
- `governance_force_signal`
- `sector_profile_signal`
- `remediation_anchor`
- `provenance_signal`
- `reviewer_confirmation_required`

Allowed `confidence` values are:

- `exact`
- `deterministic_pattern`
- `fallback_required`

## Relationship to Remediation Patches

Remediation patches may include optional `evidence_trace_ids` when deterministic source support can be safely linked to the patch. If no exact or deterministic trace can be linked, `evidence_trace_ids` remains empty and `source_evidence` uses the reviewer-confirmation fallback.

Patch `source_evidence` may use a trace's `matched_text` only when that text is an exact substring of the assessed document. It must not contain paraphrased source evidence.

## Relationship to Verified Corpus / Manifests

Evidence traces do not replace verified corpus or manifest verification. Verified corpus / manifest verification remains separate and must not be silently mutated by evidence trace enrichment.

The trace model does not authorize edits to verified raw files, manifests, manifest schemas, protected artifacts, or validation gates.

## Reviewer-Confirmation Fallback

When the deterministic extractor cannot locate exact source text, the fallback is:

`Not directly quoted by current deterministic extractor; reviewer confirmation required.`

`fallback_required` means no direct quote was extracted. Fallback traces must have `matched_text` as an empty string and `start_char` / `end_char` as `null`.

## Legal / Authority Boundary

Evidence traces do not determine legal validity, enforceability, safety, external regulatory compliance, or institutional authority. They do not certify LAIF-native compliance and do not change the binary formal LAIF-native certification gate.

## Anti-Gaming Boundary

Evidence traces are not a new scoring surface. They must not reward documents for keyword stuffing, and they must not alter score weights, formal compliance, governance checks, protected-artifact checks, or verified-corpus handling.

A document with FORMAL FAIL plus high semantic, sector, or evidence proximity remains FORMAL FAIL.

## Future Expansion

Future work may add richer deterministic span extraction, source-page references, richer provenance records, or manifest-linked evidence maps. Any expansion must preserve the exact text presence requirement, reviewer-confirmation fallback, legal/authority boundary, and separation from verified corpus / manifest mutation.

## Phase 3Q Calibration and Score Justification Reference

See [CALIBRATION_SCORE_JUSTIFICATION.md](CALIBRATION_SCORE_JUSTIFICATION.md) for the shared boundary governing score bands, score justification metadata, dimension justifications, calibration cautions, gaming-risk notes, evidence/sector/remediation relationships, and the rule that LAIF-model signal strength does not determine legal validity or certify LAIF-native compliance.

## Public report template reference

Public-facing rendering requirements are defined in [Public Report Template](PUBLIC_REPORT_TEMPLATE.md). That template is presentation-only and does not change scoring, validation, certification, evidence, remediation, sector-profile, calibration, or governance invariants.

## Phase 3S System QA Release Audit Reference

See [SYSTEM_QA_RELEASE_AUDIT.md](SYSTEM_QA_RELEASE_AUDIT.md) for the release-readiness audit boundary covering validation/certification separation, diagnostic modes, evidence, remediation, sector profiles, calibration, public reporting, protected artifacts, and verified corpus limits. That audit is documentation/test-only and does not change runtime behavior.

## Document Ingestion Source Boundary

When the Phase 3T document processing runner is used, evidence traces are based on the extracted text that is passed into the assessment engine. Reviewers must inspect extraction metadata when source fidelity matters, because poor extraction, missing OCR, table-order changes, or parser limitations can affect the assessed text and therefore the trace spans. The existing invariant still applies: `matched_text` must equal the assessed source slice at `source[start_char:end_char]`.
