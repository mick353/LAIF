# Portable analyst-review integration — 7 November 2026

## Merged release

Mike approved merging PR #101. GitHub merged the expected head `9f49622ea5032e1dda1605ae2deed1c701aeed93` to main as **`13e828688e35082228714c7c405abd5cc8de9b69`**. The fetched main tree matches the previously verified 502-test candidate, `5bbb3ac74e5dba302ba9af6d44cda659262e4dd4`.

This enhancement started from that main on a fresh branch with `HEAD...origin/main` equal to `0 0`. It is a separate proposal, not an automatic extension of the approval to merge #101.

## System enhancement

The ordinary document processor now accepts **`--review-file`** using the existing scholarly analyst-template format. Source-linked findings can therefore be carried into normal reports for arbitrary local documents. A new document does not need a hard-coded regulatory record or a paid model API.

This closes a workflow gap: the existing research CLI could validate analyst annotations, but normal processing could include substantive source-linked analysis only through the two registered regulatory decision records. The processor now reuses the research validation path rather than introducing another annotation schema.

The imported review retains its supporting passages, alternatives, limitations, self-identified analyst and optional criterion mapping in the primary report, JSON assessment and analyst bundle. E-style review evidence IDs remain distinct from machine Q-style IDs and the curated regulatory trace IDs. Unmapped review areas remain `NOT_ASSESSED`; attached findings remain claims requiring review.

The import checks original source identity, exact normalised extraction, quotation-inventory identity, framework/Toolkit hashes and toolchain identity before output writing. It rejects empty templates, legacy method-unbound submissions, stale or foreign evidence, duplicate/ambiguous JSON, non-finite constants, changed inputs and native-certification overrides. Rendered submitted text is escaped. Observed review-file changes during validation are rejected, and the source identity must match the processor's extraction snapshot.

Source provenance does not come from the review. An unverified upload remains unverified. Analyst identity, independence, correctness and real control effectiveness are not authenticated by matching hashes. Existing separately attributed repository analysis is not overwritten.

## Executed verification

Code checkpoint: `aed17d43b03b400bb6c74e947fc996061500a7f5`; tree before this verification record: `301e407524567b5ad6ac5c53bc3f6dea141b54ee`.

| Check | Actual result |
|---|---|
| Full local verifier against merged main | **PASS, exit 0: 515 discovered tests**, plus governance, protected artifacts, all corpus/format/evidence modes, standalone adversarial/provenance/semantic checks and deterministic committed-report regeneration. [Final log](full-local-verification.log). |
| New portable-review tests | **13 PASS**, covering generic end-to-end output, source/method/inventory drift, legacy unbound and empty submissions, extraction mismatch, invalid references/duplicates, ambiguous JSON/non-finite constants, inert markup, unchanged authority, certification boundaries, changing input snapshots and no-write preview. [Targeted log](targeted-tests.log). |
| Existing workflows | Existing runner and scholarly-review suites passed targeted checks and were included again in the full gate. Default regulatory reporting remains available without the new flag. |
| Actual standard-library demonstration | **PASS, exit 0:** the source-locked completed review was imported with `python -S`; its finding appeared in report/JSON/bundle, unmapped criteria stayed unassessed and source authority was not promoted. [Execution log](demonstration-run.log) and [result](demonstration-result.json). |
| DTA and EU reviewed-text runs | **PASS with `python -S`**, with no submitted review. Existing attributed findings remain intact. [Run manifest](regulatory-run-manifest.json). |
| Regulatory source re-extraction | **PASS:** 45 curated page-bounded quotations, eight original-Act contextual passages and 16 authored findings; both raw extracts reproduce byte for byte. [Log](regulatory-source-verification.log). |
| Baseline preservation | All ten baseline scores, formal categories, functional results, source identities and provenance unchanged; generated JSON fingerprint updated. [Record](baseline-preservation.json). |

An intermediate test used unnormalised fixture text in the changing-input test. That fixture was corrected to use the processor's actual normalised extraction; the targeted suite and full gate were rerun successfully. The PASS above refers to the final successful run.

## Reproducible example

The [synthetic source](demonstration/vendor-policy.md), [completed review](demonstration/completed-review.json), [actual generated report](demonstration/vendor-policy.laif.md) and [technical appendix](demonstration/vendor-policy.technical_appendix.md) demonstrate the complete path. They do not describe a real supplier or establish assessment accuracy.

From the repository root, using a fresh output directory:

```bash
python3 -S scripts/laif_process_document.py docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md --extractor builtin --review-file docs/verification/2026-11-07-portable-review/demonstration/completed-review.json --output-dir /path/to/output
```

For a new document, first generate its template with `scripts/laif_research_report.py`, then complete and submit that template. Preserve the available evidence IDs and all hashes. A changed source, extraction or toolchain needs a new template and review. The optional import revalidates the source through the existing scholarly pipeline; it does not call a model or fetch evidence online.

## Limits and readiness

This provides a reusable professional assisted-assessment workflow for new documents. It does not make unreviewed software outputs into expert judgements. A completed form or source-matching passage cannot prove that an interpretation follows logically, that legal scope is correct, or that a control works. Independent assessment-accuracy evaluation remains outstanding.

Work cloud Linux/Python 3.12 was used. No paid model API, user's PC or GitHub Actions was required. Markdown/text input, template validation and reporting use standard-library Python. Optional PDF/DOCX extraction still requires the applicable local package; Poppler is used only for the separately executed re-extraction check. Windows/Python 3.10 runtime verification was not performed in this pass.

Protected historical reports, source PDF/raw bytes and framework texts remain unchanged. The merged #101 release remains on main; this enhancement is ready for focused review as a separate change.
