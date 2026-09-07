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
