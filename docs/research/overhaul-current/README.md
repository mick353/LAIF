# Eight-criterion comparison: Codex exploratory result

Owner: Codex. Status: real retained-source comparison complete; independent accuracy validation and proposed strong-source PDF intake are not complete. No scoring or detection rules were changed. This is one model's unblinded exploration, not Mick's assurance or an independent review.

## Locked protocol and provenance

Predictions were committed at `fa17c8f` (published as `6f8627d` in PR #126) before running any automatic judgments in this experiment. [Predictions](predictions.json), [fingerprint](predictions.sha256), and the complete [results and exact witnesses](results.json) preserve all disagreements. The baseline is `dde0f77`; the result embeds the automatic module's SHA-256. Source byte hashes and normalized extracted-text hashes are separately retained. The five full retained texts are assessed, not selected snippets. NIST and OECD remain `HASH_VERIFIED_LOCAL_ONLY`: this run does not promote their user-supplied conversions to authenticated publisher bytes.

NIST AI RMF 1.0 (January 2023) is the provisional stronger operational-detail comparator; OECD/LEGAL/0449 (2024 revision) is the less operationally detailed comparator. Stronger/weaker is a prespecified hypothesis about document detail, not legal merit, effectiveness or an independent quality label. DTA version 2.1 is an additional real source. LAIF v1.2 and its clinical PDCA are circular positive controls because the criteria were defined by LAIF.

The [Commonwealth Ombudsman official guide](https://www.ombudsman.gov.au/__data/assets/pdf_file/0025/317437/Automated-Decision-Making-Better-Practice-Guide-March-2025.pdf) was checked through web retrieval on 16 November 2026: its cover says March 2025 and the PDF has 61 pages. It is the 2025 update of the 2007 guide. Direct PC retrieval still returned HTTP 403, including the ordinary non-www and download variants; no PDF bytes or extraction were admitted. This is an identified alternative comparator, not a completed intake. The [current NSW assessment framework](https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/nsw-ai-assessment-framework) uses a platform mandatory from 30 September 2026. An older PDF was not substituted. These current-source observations do not replace normal source custody and page-level extraction verification.

## Results

P = PARTIAL_SUPPORT; N = NOT_ESTABLISHED; S = PROVISIONALLY_SUPPORTED. These are automatic documentary labels; none establishes implementation. Inspect the actual witness clauses and missing components before relying on a label.

| Document | A.1 | A.2 | A.3 | A.4 | Q1 | Q2 | Q3 | G.1 |
|---|---|---|---|---|---|---|---|---|
| nist | P | N | P | N | N | P | P | P |
| oecd | N | N | P | N | N | N | P | N |
| dta | N | N | P | N | N | N | N | N |
| laif | P | P | S | P | P | P | P | P |
| clinical | P | P | P | N | N | P | P | P |

NIST has matches in five criteria and three explicitly supported components; OECD has matches in two criteria and zero explicitly supported components. Both prespecified descriptive comparisons held. These counts are not engineering scores, accuracy measures or evidence of better outcomes. NIST exceeds DTA on four categorical labels (A.1, Q2, Q3, G.1), but Q2/G.1 have qualified mentions and zero explicitly supported components. That difference must not be promoted to four substantively established safeguards.

Of 40 predicted labels, 29 matched and 11 did not. The 11 mismatches remain in the result file; no predictions were revised. This fraction is agreement with Codex's guesses on a known, unblinded convenience sample, not measured accuracy. In particular the detector missed expected A.1 support in DTA and OECD; expectation itself is not ground truth. Low matches may reflect wording, extraction boundaries, narrow rules, genuinely missing requirements, or a mixture. The rules do not resolve these alternatives.

## Real-text deletion checks

Three exact NIST clause deletions were registered before execution. Removing MANAGE 2.4 removed one A.3 interruption/deactivation witness, while the A.3 label remained PARTIAL_SUPPORT. Removing GOVERN 2.1 left G.1 unchanged, as expected: assigning roles is not the same as independently reviewing governance actors. Removing MANAGE 4.3 left the A.3 authorised-escalation component unchanged, as expected: incident communication does not itself establish authorisation. All three prespecified witness-level expectations held. Exact deleted text, offsets, hashes, before/after judgments and all remaining witnesses are retained.

A separate, explicitly rule-guided sensitivity check removed the union of every matched clause for each source/criterion pair. Twenty-two eligible pairs became NOT_ESTABLISHED as predicted; eighteen had no matched clause to remove and are NOT_APPLICABLE, not passes. Derivatives stay in memory; original sources are untouched. This exercise tests dependence on quoted text, not human construct validity. It is not a realistic replacement policy: deletion can affect multiple criteria that share clauses. Every other criterion's label and witness-count change is retained rather than hidden. No evidence was removed from the production system to improve the comparison.

## Document-only ceilings

All eight automatic checks can at most reach PROVISIONALLY_SUPPORTED for written requirements. A separate authored review may reach SUPPORTED_IN_SCOPE with sufficient exact evidence and a scoped argument. For policy promises alone, operational status remains NOT_ESTABLISHED for every criterion. These are different channels, not synonyms. A document containing actual empirical records requires separate evaluation of those records and is not limited merely by being a document.

| Criterion | What written text can support | What text alone cannot establish |
|---|---|---|
| A.1 | Required explanations, limits and affected-person access | Actual understandable explanations and usable access |
| A.2 | Required objective/implementation consistency and misleading-behaviour checks | Actual behaviour, honesty or absence of deception |
| A.3 | Operating limits, interruption and authorised escalation | Working containment or safe interruption under real conditions |
| A.4 | Calibration evaluation, population, thresholds and correction requirements | Measured accuracy, calibration or applicability without empirical evidence |
| Q1 | Protected-interest pairing, equivalent-force requirements and remedies | Legal applicability or effective enforcement of the protection |
| Q2 | Smallest-actor reasoning, consistency and justified exceptions | Proportionate consequences in all actual contexts |
| Q3 | Revision, safe decommissioning and irreversible-action authority | Exercised rollback or reversal of irreversible effects |
| G.1 | Review, challenge and transparency of governors themselves | Independent oversight functioning effectively |

## Earlier failures remain failures

The earlier [committed probe](https://github.com/mick353/LAIF/tree/6649b1e/docs/research/overhaul-2026-11) at `6649b1e` tested numeric diagnostic dimensions before automatic eight-criterion judgments existed. Its predicted auditability ranking failed, and all three predicted numeric decreases failed (zero deltas). The new witness-level experiment does not rewrite or turn those failures into passes. It asks a different, narrower question using the released automatic module. No independent validation, empirical calibration or legal certification is claimed.

## Reproduction and remaining acceptance

Run `python scripts/laif_criterion_comparison.py --verify` from the repository root. The runner checks the prediction lock and original bytes, reruns all five full texts and exact deletion derivatives, and compares the complete receipt. It refuses to overwrite an existing result. Focused checks: `python -m unittest discover -s tests -p test_criterion_comparison.py`.

Completed: locked exploratory predictions, full retained-source eight-criterion comparison, exact real-text sensitivity results, ceilings, negative results, reproducible receipt. Pending: admission of the preferred Ombudsman comparator bytes; independent source/criterion adjudication; independent acceptance described in the [current checkpoint](../../verification/CURRENT.md). PR #126 integrated this work after a 635-test local gate with two explicit skips. The public reading room presents the comparison; the current checkpoint records Site versions and live readback.
