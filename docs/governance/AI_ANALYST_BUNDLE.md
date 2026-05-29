# AI Analyst Bundle

Phase 3W creates an AI-ready analyst bundle without adding any paid or external model API integration. LAIF does not call OpenAI, Anthropic, Gemini, Google, Claude, or other model APIs. The generated files are local deterministic artifacts that a user may manually upload to an external model if they choose.

Per-document bundle files are written under `analyst/`:

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
