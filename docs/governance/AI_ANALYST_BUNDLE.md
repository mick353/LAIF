# AI Analyst Bundle

Phase 3W creates an AI-ready analyst bundle without adding any paid or external model API integration. LAIF does not call OpenAI, Anthropic, Gemini, Google, Claude, or other model APIs. The generated files are local deterministic artifacts that a user may manually upload to an external model if they choose.

Per-document bundle files are written under `analyst/<document>/` (namespaced by document stem, so several documents processed into one output directory never overwrite each other):

- `AI_ANALYST_PROMPT.md`
- `AI_ANALYST_INPUT_BUNDLE.json`
- `AI_REPORT_VALIDATION_RULES.md`
- `analyst_bundle.json`
- `quote_bank.jsonl` and `quote_bank.md`
- `governance_gap_register.json`
- `failure_pathways.json`
- `control_recommendations.json`

The prompt instructs any downstream model to use only the provided quote bank, deterministic diagnostics, and source excerpts; to preserve quote IDs, gap IDs, and control IDs; and to avoid invented quotes, legal claims, obligations, scores, documents, actors, controls, certification, or legal-validity conclusions.

The input bundle includes document metadata, processing metadata, extraction metadata, governance repair fields, scores, quote bank, gap register, failure pathways, control recommendations, extraction warnings, low-confidence evidence flags, and technical appendix data.

The validation rules require every quote to exist in the quote bank, every recommendation to map to deterministic gap/control IDs, required sections to be present, the technical appendix to be preserved, and low-confidence evidence not to be used as primary support.

## Whole-source evidence and reporting — 7 November 2026

Source-backed prose, structured rows requiring context and attributed analyst judgements are separate. The bundle includes `source_control_observations`, `source_evidence_requests`, `source_scan_coverage` and recorded `source_provenance`. Structured rows retain available column headings; “Provided / Not provided” choices are not inferred answers. Recommendations identified by “should” are labelled separately from other control wording; neither label establishes legal force.

The complete candidate stream is scanned; up to three spatially distributed witnesses per mechanism type are retained. One per type appears in the main report. Counts, omitted oversized candidates and retrieval limits remain explicit. The retained inventory is not complete semantic coverage. Exact source spans, cross-artifact evidence references and coverage counts are checked before writes. Original source/version qualifications remain visible; legacy local-hash verification is not promoted to official-origin equivalence.

See the [whole-source execution record](../verification/2026-11-07-real-source-assurance/README.md) and [plain-English use cases](../product/USE_CASES.md). This reporting follow-up was released through merged PR #103; scoring weights and formal verdict rules are unchanged.
