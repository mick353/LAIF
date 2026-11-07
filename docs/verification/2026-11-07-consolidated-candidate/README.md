# Consolidated LAIF assessment candidate — 7 November 2026

This is an unmerged integration and assessment-quality candidate, not the canonical release. It combines the exact inspected heads of PRs #89, #90 and #94–#99 on main `09f8687b58d1c5547cfe58bcf4e38aa7da3619a2`. The eight original PR branches remain unchanged and open. No GitHub main merge or PR closure is authorised by this record. Exact inputs are in [integration-inputs.json](integration-inputs.json).

**Subsequent reasoning pass:** [the assessment follow-up](REASONING_REVIEW.md) corrects specific EU transition/citation issues, explicitly addresses the remaining two principles and adds source-bound authored findings. Its full gate passed **483 tests**; the curated evidence now contains **45 quotes and eight original-Act contextual passages**. The execution counts below preserve the earlier integration checkpoint.

**Generated reporting follow-up:** [processor and report-quality repairs](../2026-11-07-generated-report-quality/README.md) now pass **496 tests**. This changes the actual output pipeline and includes fresh generated reports; it supersedes earlier descriptions of the automatic reporting defects.

## What the system can now do

The candidate contains two separate, substantive, source-bounded assessments: [Australian DTA Policy v2.1](../2026-11-07/regulatory/au_dta_policy_v2_1.assessment.md) and [EU Regulation 2026/1744](../2026-11-07/regulatory/eu_ai_act_amendment_2026_1744.assessment.md). They assess the Integrity Layer, Q1a/Q1b, consistency, reversibility, self-application, changes and applicability. They recognise positive protections and identify the evidence needed to close specific gaps. Complete Coherence Test satisfaction is **not demonstrated** by the mapped evidence; that does not establish unlawful government conduct or operational failure.

The machine processor retrieves and checks evidence and produces deterministic rubric diagnostics. It does not independently perform the full substantive reasoning in those authored reports. The new research dossiers supplement that reasoning with explicit review coverage and method identity. They are labelled inventories, not replacement assessments. Their eight `NOT_ASSESSED` rows describe their own unpopulated review forms, not a retraction or automated judgement about the separate authored assessments.

## Repairs and integration decisions

- Corrected CLAUDE.md's invented three-principle summary against the five actual Part One principles. Corrected false Principle 3/hierarchy attributions and removed unsupported prevalence claims in engine/validator commentary.
- Exposed all four Integrity Layer review areas, all three Coherence Test questions and self-application in research dossiers. Calibration remains conditional under §2.5; Q1 explicitly requires inseparable pairing and equivalent enforceability. Coverage means a claim is attached, not that a criterion passes.
- Bound new annotations to source and quotation-manifest hashes, principal and Toolkit hashes, and the internal toolchain fingerprint. Unknown/duplicate criteria and stale/partial method identities fail. Legacy annotations remain readable with an explicit unbound status.
- Reconciled the principal Word-document conflict by retaining the four-property correction and adding the exact cross-reference paragraph. Reconciled the corpus index and README so the original EU Act remains admitted separately from its amendment.
- Corrected the Regulatory Integration Guide's remaining three-property instruction in both formats. Preserved the historical clinical PDCA unchanged; its missing calibration assessment is disclosed in [legacy-result boundaries](../../research/LEGACY_RESULT_BOUNDARIES.md), not silently invented.
- Recognised the truthful `AUTOMATED_URL_FAILED_HTTP_503` status. DTA remains human-attested; this taxonomy addition does not promote it to automated upstream verification.
- Retained PR #99's quotation-completeness and inference repairs and PR #98's full sources, manifests, page indexes and authored reasoning. The optional frontier-assurance and study-comparison tools remain diagnostic proposals, not adopted LAIF policy or external validation.

## Actual executed results

Code checkpoint: `111edc2e2c581c2671d71c4055a04fb832f6e5f1`; code tree before this documentation record: `9d64732d27a02155c0b7e350a50176f9d7382688`. Toolchain fingerprint: `353082c7f580ce76`.

| Executed check | Result |
|---|---|
| `python scripts/laif_verify.py --full --base-ref origin/main` | PASS; **478 discovered tests**, plus all additional gates; exit 0. [Complete log](full-local-verification.log). |
| Governance configuration, protected-artifact diff and semantic advisory | PASS. Semantic warnings identify review-sensitive work; they do not constitute semantic approval. |
| All four validation modes | PASS: standard, verified corpus, evidence traces and DOCX/TXT formats. No cross-reference warning remains. |
| Standalone adversarial, provenance and semantic-fidelity checks | PASS as executed by the full verifier. Expected fixture failures are not harness failures. |
| Generated baseline reports | PASS: two regeneration runs identical, committed report-drift check clean. All ten baseline scores, formal categories, functional evidence and source identities preserved; see [regression comparison](baseline-regression.json). Explanatory wording intentionally changes. |
| `python -S scripts/laif_verify_regulatory_ingestion.py --reextract` | PASS: both PDF/raw hashes, complete page maps, 44 exact page-bounded quotations, original-Act contextual PDF and six passage hashes; Poppler reproduced both raw extracts byte for byte. [Log](source-verification.log). |
| `python -S scripts/laif_process_regulatory_sources.py --verified-text ...` | PASS for both sources with site packages disabled. [Run manifest](stdlib-run-manifest.json). |
| Direct PDF processor with installed pypdf | PASS for both sources. [Run manifest](pdf-run-manifest.json). Extraction-quality limitations still apply; the reviewed-text route is preferable. |
| Actual reviewed-text quotation spans | PASS: DTA 10 and EU 12 primary quotations matched exact normalised source slices. [Record](actual-source-regression.json). |
| Research dossier and second-reader template preparation on both real sources | PASS: eight exact candidate passages per source, eight explicit review areas, method/source binding and blank second-reader templates. No reviewer or independent result fabricated. Files under `review-dossiers/`. |
| New integration regressions | PASS: six tests covering principle drift, coverage overclaim, annotation mapping, stale/partial method identity, legacy status and malformed criteria; included in 478. |
| Comparative-study CLI | PASS on clearly synthetic input; `--require-human` correctly rejected it with exit 2. [Synthetic-only output](synthetic-comparison.json) is software exercise, not measured field accuracy. |
| DOCX package and rendering checks | PASS: principal 47 pages; revised guide 24 pages, changed table visually inspected on page 17. Only `word/document.xml` changed relative to the stated source DOCX packages; see [comparison](document-package-comparison.json). |
| Preservation | Both protected narrative reports, historical clinical PDCA, source PDF bytes and historical evidence remain unchanged; no file deleted relative to main. |

Environment: Work cloud, Linux, Python 3.12. No user's PC, paid model API, GitHub Actions run or hosted inference service was used. Recorded absolute output paths identify this execution; they are not runtime dependencies. The reviewed-text path uses the Python standard library. Direct PDF processing additionally needs pypdf; re-extraction checks need Poppler. Windows and a Python 3.10 interpreter were not available for a fresh runtime check in this pass.

## Remaining work and readiness

1. **Review the substantive conclusions.** Independent reviewers have not established whether the reasoning and evidence support every determination. The prepared templates do not count as completed independent review.
2. **Measure real accuracy.** The comparative-study harness exists, but no independently labelled, prespecified held-out study has been executed. No sensitivity, specificity, comparative superiority or scientific validity claim follows from 478 software tests.
3. **Complete legal and operational evidence where a deployment decision requires it.** The DTA policy's linked law/tools and the EU amendment's transition protections are not a complete jurisdiction-wide rights/enforcement map. Actual system calibration, containment, honesty and oversight effectiveness require deployment evidence. The original EU Act's separate full-document assessment remains pending; contextual passages are not that assessment.
4. **Resolve historical/current use explicitly.** A new clinical PDCA needs a calibration-applicability determination and evidence where required. Historical protected assessments and their dates remain records rather than current certificates.
5. **Retain source/runtime limits.** DTA upstream byte equivalence remains unverified after HTTP 503; pypdf spacing damage remains a reason to prefer pinned reviewed text. Software quotation gates are not perfect semantic understanding. Fresh Windows/Python 3.10 runtime checks remain unexecuted.

Software integration checks pass. The candidate is ready for focused human semantic and assessment review; canonical adoption and any merge remain pending Mike's approval. No claim of perfection, legal certification, model safety or independent validity is made.
