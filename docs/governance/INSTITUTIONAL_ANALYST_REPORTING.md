# Institutional Analyst Reporting

Phase 3W adds deterministic institutional analyst outputs to the local LAIF document-processing runner. The layer is designed for senior governance, legal, procurement, public-sector, clinical safety, and AI assurance reviewers who need a practical governance assessment rather than a developer diagnostic dump.

For each processed document, the runner writes:

- `<safe_stem>.institutional_report.md`
- `<safe_stem>.technical_appendix.md`
Analyst outputs are namespaced by document stem, so processing several
documents into one `--output-dir` never overwrites an earlier document's
register, controls, pathways, or quotes:

- `analyst/<document>/analyst_bundle.json`
- `analyst/<document>/quote_bank.jsonl`
- `analyst/<document>/quote_bank.md`
- `analyst/<document>/governance_gap_register.json`
- `analyst/<document>/failure_pathways.json`
- `analyst/<document>/control_recommendations.json`
- `analyst/<document>/AI_ANALYST_PROMPT.md`
- `analyst/<document>/AI_ANALYST_INPUT_BUNDLE.json`
- `analyst/<document>/AI_REPORT_VALIDATION_RULES.md`

The institutional report answers what kind of governance document was processed, what force it appears to have, what it controls well, what it does not control, where systemic failure may still occur, and what operational controls are required next.

The report does not lead with LAIF-native failure for external-framework assessments. Formal LAIF-native certification remains available in LAIF-native mode and in the technical appendix boundary, but external-framework reports lead with governance repair, source-force interpretation, evidence sufficiency, and operational closure.

The quote bank is deterministic. Primary quote records are exact substrings of the extracted source text and include source hash, document type, sector profile, signal category, quote offsets, extraction confidence, linked gap IDs, and reviewer cautions about what the quote does not prove.

The gap register, failure pathways, and control recommendations translate source-language evidence into practical reviewer actions. Major gaps map to controls with owner, required artifact, minimum evidence, trigger, threshold, cadence, decision consequence, and residual risk.

## Whole-source evidence and reporting — 7 November 2026

Source-backed prose, structured rows requiring context and attributed analyst judgements are separate. The bundle includes `source_control_observations`, `source_evidence_requests`, `source_scan_coverage` and recorded `source_provenance`. Structured rows retain available column headings; “Provided / Not provided” choices are not inferred answers. Recommendations identified by “should” are labelled separately from other control wording; neither label establishes legal force.

The complete candidate stream is scanned; up to three spatially distributed witnesses per mechanism type are retained. One per type appears in the main report. Counts, omitted oversized candidates and retrieval limits remain explicit. The retained inventory is not complete semantic coverage. Exact source spans, cross-artifact evidence references and coverage counts are checked before writes. Original source/version qualifications remain visible; legacy local-hash verification is not promoted to official-origin equivalence.

See the [whole-source execution record](../verification/2026-11-07-real-source-assurance/README.md) and [plain-English use cases](../product/USE_CASES.md). This reporting follow-up was released through merged PR #103; scoring weights and formal verdict rules are unchanged.
