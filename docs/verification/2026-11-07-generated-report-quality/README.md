# Generated report quality — executed processor repairs

**Date:** 7 November 2026. **Status:** unmerged PR #100 candidate. This pass changes LAIF's actual processing and reporting pipeline. It does not merely revise the two separately authored assessments.

Read the fresh generated outputs:

- [Australian DTA Policy v2.1 — generated report](au_dta_policy_v2_1/au_dta_policy_v2_1.institutional_report.md) and [technical appendix](au_dta_policy_v2_1/au_dta_policy_v2_1.technical_appendix.md).
- [EU Regulation 2026/1744 — generated report](eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.institutional_report.md) and [technical appendix](eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.technical_appendix.md).

These files are copied from actual runs without editorial rewriting. Execution paths identify this run, not dependencies on a user's computer. Exact artifact hashes and acceptance results are in [actual-report-acceptance.json](actual-report-acceptance.json).

## Defects corrected in the system

| Previous generated behaviour | New generated behaviour |
|---|---|
| Claimed DTA discussed risk without a pre-deployment gate | Locates the actual assessment/treatment clause on PDF page 14 and suppresses that false absence claim. |
| Treated PDF line breaks as sentence endings; fallback quotations could omit a subject or continuation | Uses paragraph-aware sentence spans and applies continuation expansion to both selected and fallback quotations. Retains original offsets and raw text. Non-operative table fragments are not promoted as clean primary evidence. |
| Labelled a standalone full EU source as an illustrative corpus document | Uses the source-led single-document report surface. Resolves matching existing provenance manifests and original PDF identities; retains DTA human attestation separately from EU automated verification. Arbitrary uploads remain authority-unverified. |
| Converted missing rubric matches into categorical control failures | Labels gap-register entries as unverified review questions, links only genuinely matching quote IDs and identifies related source mechanisms. Does not attach arbitrary Q001–Q003 as evidence for an absence claim. |
| Presented hypothetical failure pathways and proposed controls as actual failures or mandatory requirements | Marks scenarios as hypothetical and recommendations as conditional. Removes the invented universal quarterly cadence and directs reviewers to existing applicable requirements first. |
| Kept substantive source-based findings separate from generated reports | Includes existing source-bound analyst determinations, closing conditions and applicability cases after identity/reference validation, with explicit authorship and a non-independence statement. Curated source evidence is carried into the analyst bundle. |
| Used a corpus-ranking report for single-document runs and a different preview surface | External `.laif.md`, institutional report and no-write preview use the same source-led report preparation. Baseline corpus reporting retains its existing purpose. |
| Direct PDF processing could select the wrong document/sector context | Both regulatory runner routes now supply the recorded title, source type and sector context. Extraction limitations remain visible. |

The added control observations are bounded, exact-span textual candidates. They do not infer full equivalence or working implementation from scattered keywords. Recital-only, explicitly negated, hypothetical and disconnected-word examples are tested against false gate detection. Narrow detector signals and raw remediation suggestions remain available in the technical appendix with their interpretation limits.

## Actual execution

Tested code checkpoint: `56fbd1d7904c44e8b7bd3809b40ebf48ed71ce82`; tree before this verification record: `af790d454b7e9b17f595719cf1745225e4692443`. Toolchain fingerprint: `00aa209f1e2ef4e5`.

| Executed check | Result |
|---|---|
| Full local verifier against `origin/main` | **PASS, exit 0: 496 discovered tests**, plus governance, all corpus/format/evidence modes, standalone adversarial/provenance/semantic checks and deterministic committed-report regeneration. [Complete final log](full-local-verification.log). |
| New generated-report acceptance tests | **13 PASS**, covering actual DTA/EU output, exact offsets, provenance flow, attributed analysis, non-match boundaries, wrapped statements, negation, disconnected clauses, recital scope, tampered source identity, no-write parity and source markup. [Targeted log](targeted-acceptance.log). |
| Existing document runner tests | **148 PASS** during targeted development; included again in the final full gate. One old assertion demanding an unsupported favourable opinion was replaced with a bounded source-observation assertion; all other existing runner tests retained. |
| Existing evidence-boundary regressions | **9 PASS**, included in the full gate; actual execution date and generator remain correct. |
| Both real sources via reviewed text | **PASS with `python -S`**, site packages disabled. DTA: 6 control candidates and 11 primary quotes; EU: 7 control candidates and 10 primary quotes. Exact source offsets verified. [Run manifest](text-run-manifest.json). |
| Both real PDFs | **PASS** using the installed pypdf route and explicit instrument context. This does not prove perfect extraction. [Run manifest](pdf-run-manifest.json). |
| Regulatory source verification with Poppler re-extraction | **PASS:** 45 curated page-bounded quotations, eight original-Act contextual passages and 16 authored finding records; both committed extracts reproduced byte for byte. [Log](source-verification.log). |
| Baseline and same-source score preservation | **PASS:** all ten baseline documents retain scores, formal categories, functional results, source identity and provenance. The two reviewed regulatory sources also retain scores and functional results. Generated JSON fingerprint regenerated. [Record](baseline-preservation.json). |
| Protected material | Historical narrative reports, framework documents, source PDFs and raw ingestions unchanged in this pass. No source deleted. |

Intermediate verification caught an obsolete helper and a shared-renderer removal during cleanup. Those defects were corrected and the affected checks and complete gate rerun. The PASS above refers to the final successful run, not the earlier failed attempts.

## How good the reporting is now

The known high-impact reporting defects above have executable acceptance coverage. The resulting reports are substantially more suitable for professional **assisted assessment and review**: positive controls are visible, evidence and assumptions can be checked, provenance survives processing, and uncertainty is not presented as failure.

The processor does **not** independently originate the included substantive judgements. It renders validated, attributed author analysis when a matching record exists. For other inputs it produces bounded observations and review questions; it does not manufacture a completed LAIF assessment. The current registered reasoning records are the two regulatory cases, not a universal library of validated conclusions.

Thirteen development acceptance tests on selected known defects are not an independent accuracy benchmark. General precision/recall, legal correctness and reliable full-context reasoning remain unmeasured. Full-document saturation, unrecognised paraphrases, unseen extraction damage and missing external law/operating evidence remain practical limitations. Source-control patterns and quotation gates cannot establish semantic completeness. Windows/Python 3.10 runtime verification and independent human review remain outstanding.

All execution used Work cloud Linux/Python 3.12. No user PC, paid model API or GitHub Actions run was required. The reviewed-text/reporting path is standard-library Python; direct PDF processing additionally uses pypdf and re-extraction checks use Poppler. The candidate remains unmerged pending Mike's approval.
