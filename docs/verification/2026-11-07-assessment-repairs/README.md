# Assessment integrity repairs arising from PR 98

This repair branch is based on main `09f8687b58d1c5547cfe58bcf4e38aa7da3619a2`. It is separate from PR #98's source admission and authored assessments. No merge is performed. Open work #89/#90/#94/#95/#96/#97 was inspected; #95's scholarly report wrapper and #96's documentation reconciliation remain independent. This branch fixes the existing canonical processor rather than adding another assessment service.

## Defects and resulting behaviour

| Defect observed | Repair |
|---|---|
| Principal §2.4 said three properties while §2.5/§9.4 required four | Reconcile §2.4 with the existing calibration requirement and its applicability trigger, in both DOCX and TXT. No new calibration trigger or numerical threshold is introduced. |
| Toolkit PDCA Section A and specification registry omitted calibration | Add operational standard 1.8 and A.4 to the paired Toolkit sources; list A.4 in `INTEGRITY_LAYER` and contributor guidance. |
| Detector misses became claims of absent protections or automatic substantive failure | Correct the affected executive, finding and risk wording to describe detector limits and require source-based review. Legacy detector categories remain compatible; no weights or formal verdict rules are changed. |
| An empty gap register produced “no remediation required” and declared drafting risk closed | Empty-path sections now explicitly withhold those conclusions, including on long saturated documents. |
| Document reports used a fixed September date and claimed generation by the corpus script | Document processing supplies its actual UTC execution date and processor name; the baseline corpus renderer retains an explicit deterministic date. |
| No visible per-property record included all four Integrity Layer properties | Add an unscored four-property requirement-signal map with exact matched-text offsets, explicit non-detection and no pattern-derived substantive pass. Calibration applicability is stated. Export it in JSON and render it in the reports. |

The behavioural changes to report interpretation are deliberate. These are not presented as wording-only changes with no effect on meaning. They remove unsupported inference; they do not convert the deterministic tool into an autonomous source-based legal or scientific assessor.

## Preserved behaviour and evidence

A direct comparison with the main-branch engine across all ten baseline documents preserved all five component scores, aggregate scores, formal verdicts, alignment detector categories, functional evidence and score traces. No protected historical narrative or original regulatory source bytes were changed. Generated baseline artefacts are regenerated because the toolchain fingerprint changes.

The DOCX edits preserve every original archive entry except `word/document.xml`. Paired source-format validation passes. Both documents were rendered; the principal remains 47 pages and the Toolkit 18. Page comparisons isolate principal changes to pages 9–11; adding Toolkit material changes subsequent pagination from page 5. Contact sheets were reviewed for all rendered pages and changed material inspected at full resolution. There is no claim that software rendering verifies the governance reasoning.

## Verification

See the committed validation logs for executed checks. Six new regressions cover the four-property inventory, exact calibration spans, mention-only non-proof, detector-miss wording, saturated empty registers and actual document-report date/generator. The existing empty-register test was corrected because it explicitly required the unsafe “no remediation” wording.

This branch contains an intentional framework clarification, reporting interpretation repairs and additive diagnostics. Review those effects before merge. Historical assessments on PR #98 retain the source hashes and framework wording used when authored; this branch does not silently recast them under the corrected principal text.


## Actual completed validation

- Full local verification: PASS, **379 discovered tests**, plus governance/protected-artifact, source/format/provenance, adversarial, semantic and deterministic-report gates. No full-gate command was skipped.
- Six new evidence-boundary regressions: PASS; document-processing suite: 148 tests PASS. The targeted suite was followed by the full gate.
- Both actual PR #98 DTA/EU reviewed source texts were processed with the repaired processor. Component/aggregate scores, formal verdicts and detector categories match the earlier runs. Four-property output, actual execution date/processor attribution and absence of the identified overclaims were checked. See `actual-source-regression.json`.
- Full log: `full-local-verification.log`. Advisory validation warnings remain disclosed there. No GitHub Actions or paid model API was used.
- Protected historical reports remained byte-identical; generated baseline reports matched consecutive regeneration.

These checks verify the implemented boundaries and reproducibility. They do not independently validate the framework’s theory, the full source-based reasoning or an institution’s actual compliance.
