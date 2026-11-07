# Regulatory assessment reasoning follow-up — 7 November 2026

This pass improves the substantive DTA and EU assessments in draft PR #100. It is author review and executed source/software verification, **not independent legal or scholarly validation**. No source PDF, historical protected report, scoring weight, detector rule or generated baseline report changed.

## What the reasoning review found and fixed

1. **EU legacy applicability:** Article 111(2), as replaced, addresses application of the Regulation to specified legacy operators. A generic reference to the existence or commencement of Article 86 cannot establish an available explanation route for every legacy system. The assessment now screens placement/service date, design change, public-authority purpose and the separate Annex X category before relying on that route. It does not infer that other Union/national protection is absent. The operative Article 111 wording was also cross-checked against the [official EUR-Lex publication](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601744).
2. **Separate Annex X transition:** unchanged Article 111(1) has its own before-2-August-2027 placement/service condition and 31 December 2030 compliance rule, with Article 5 reserved. It is excluded from paragraph 2. The assessment no longer leaves this category implicit or invites substitution of paragraph 2's August 2030 public-authority date.
3. **A misleading date citation:** the report's new Article 5 prohibition date cited a passage about the separate Article 50(2) synthetic-content deadline. Both dates happen to be 2 December 2026; the underlying rules are different. New trace Q028 retains the complete amended Article 113 application rule, including the Article 6(5) exception. It now supports the prohibition schedule directly.
4. **Complete principle coverage:** both reports now explicitly analyse Non-Accumulation and Temporal Separation alongside the previously applied principles and Coherence Test. The analysis credits distinct governance functions, evidence reuse and accountable revision. It does not invent new LAIF obligations or require external statutes/policies to copy LAIF's principal/schedule format.
5. **Current method basis:** both revised reports now identify the corrected candidate principal text and Toolkit. The older three-property discrepancy is described as the candidate's unmerged correction, rather than falsely attributed to the current text. The calibration discussion preserves §2.5's decision/verification-capacity trigger and avoids imposing a universal new metric or subgroup regime.

The overall findings remain **complete Coherence Test satisfaction not demonstrated by this evidence set**, with real positive protections credited. The specific legacy-rights dependency sharpens that bounded finding; it does not turn uncertainty into a global failure or an allegation of unlawful conduct.

## Reviewable decision records

- [DTA: eight findings and three applicability cases](../2026-11-07/regulatory/au_dta_policy_v2_1.decisions.json).
- [EU: eight findings and six applicability cases](../2026-11-07/regulatory/eu_ai_act_amendment_2026_1744.decisions.json).

These connect the authored assessments to curated trace IDs, exact report/framework/Toolkit/source hashes, reasoning, closure evidence, alternatives and scope limits. They supplement the prose reports; they do not create another scoring engine. The existing regulatory ingestion checker now verifies their identity, eight-area coverage and evidence references. It deliberately cannot certify logical entailment, legal interpretation, operational effectiveness or reviewer independence.

The blank research and second-reader templates from the earlier pass remain blank: no independent reviewer or consensus was fabricated. Their inventory status concerns those forms, not the substantive findings in the linked authored records.

## Executed verification

Code and assessment checkpoint: `fca0902e68a0483f0228670b029bfc23b28eefb9`; tree before this follow-up record: `6fb96aae9ff9a32de1ec3bbd21c367e33cf1a034`.

| Check | Actual result |
|---|---|
| Full local verifier against `origin/main` | **PASS, exit 0: 483 discovered tests**, plus all additional governance, corpus, evidence, format, adversarial, provenance, semantic-fidelity and deterministic committed-report checks. [Full log](reasoning-full-verification.log). |
| Targeted regulatory ingestion suite | **10 tests PASS**, including five new tests for method/report drift, missing or malformed calibration review, cross-document/invented references and distinct transition evidence. [Log](reasoning-targeted-tests.log). |
| Standard-library source check with Poppler re-extraction | **PASS:** both source/raw hashes, full page maps, 45 exact page-bounded quotes, eight original-Act contextual passage hashes, 16 authored finding records and applicability references. Both full regulatory raw extracts reproduced byte for byte. [Log](reasoning-source-verification.log). |
| Generated baseline reports | **Unchanged** from the already verified candidate, including after both full-gate regeneration runs. |
| Protection and portability | Protected historical reports and PDF/raw source bytes unchanged. Work cloud Linux/Python 3.12; no PC, Actions or model API used. Decision-record checking uses the standard library; optional source re-extraction uses Poppler. |

The original and amendment PDF acquisitions are the previously recorded, byte-verified sources; this pass did not perform a fresh PDF download. DTA's upstream-equivalence limitation remains human-attested. New contextual passages are exact extractions from the retained original Act, not a reconstructed consolidated text.

## Remaining boundary

Independent reviewers, a real prespecified held-out accuracy study, relevant additional legal instruments and deployment-specific evidence remain outstanding. A definite actor/product/date decision needs that evidence. This pass resolves concrete reasoning and traceability defects; it does not claim that every remaining source dependency has been closed. PR #100 stays draft and unmerged pending Mike's approval.
