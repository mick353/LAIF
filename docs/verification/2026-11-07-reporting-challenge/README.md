# Released baseline and reporting challenge pass — 7 November 2026

## Released to main

Mike explicitly approved merging PR #100. It was marked ready and merged using the expected head `f113e9b48abb3806ee1f1f9129174a406673324d`, preserving commit history. GitHub returned merge commit **`4e9a53ed15db3156a406a54de3748e56001ae30d`**. Its tree matches the previously tested candidate `e5bbb3676bd0b54ed196be9234e299025b16eadc`.

The full local gate was re-executed on that merged main: **496 tests plus all additional checks PASS**. [Post-merge execution log](merged-main-verification.log). No Actions run was used.

The subsequent work below started on a fresh branch with `HEAD...origin/main` equal to `0 0`. It is a separate follow-up proposal; the original merge approval is not treated as permission to merge later changes automatically.

## Findings and changes in the follow-up

Six plainly conditional deployment requirements were missed by the released textual-control retriever, including prohibitions framed as “unless”, “only after” and “must not deploy until”. Their negative grammar was being treated as denial of a control, rather than prohibition of deployment pending a control.

The retriever now recognises those bounded assessment/approval relationships while retaining the negation, hypothetical-example and disconnected-clause exclusions. It still emits textual candidates, not a deployment permission or a full LAIF pass.

The authored synthetic challenge set has 16 declared cases: eight positive and eight negative. The released baseline matched **10 of 16**, with six missed positive wordings; the revised retriever matches **16 of 16**. [Before](challenges-before.json), [after](challenges-after.json), and [committed fixture](../../../tests/fixtures/deployment_gate_challenges.json). These are development cases chosen by the author, not blinded labels, a held-out study or an estimate of field accuracy.

Additional improvements:

- Primary evidence now records its passage role. For recognised EU adoption headers, recitals remain context and operative passages are preferred during quote selection. Both `HAS ADOPTED` and `HAVE ADOPTED` forms are covered. A role label identifies a part of the source, not the legal effect or applicability of every quoted sentence.
- Single-document external reports lead with the assessment. Processing paths and execution metadata remain available at the end. Recorded determinations use readable wording while retaining canonical values in JSON.
- The released assessments and source-manifest references no longer misleadingly say their PR #100 release is unmerged. Only release-status wording changed; the conclusions did not. Decision-record assessment hashes were refreshed and reverified.
- Repository instructions now point to the released checkpoint and explicitly distinguish follow-up work from released main.

## Executed verification

Final code/assessment checkpoint: `f16902f1181d44fbbcc31edb4be57730bbae5e6c`; tree before this record: `f9fcc9003fe4f511697823c6193c1c3340b72b5e`. Toolchain fingerprint: `02a30260635b408a`.

| Check | Actual result |
|---|---|
| Full local verifier against merged `origin/main` | **PASS, exit 0: 502 discovered tests**, plus governance, protected artifacts, all corpus/format/evidence validation modes, standalone adversarial/provenance/semantic checks and deterministic committed-report regeneration. [Final log](full-local-verification.log). |
| New targeted challenge suite | **6 tests PASS**, covering all 16 declared cases with exact spans, recital/operative distinction, singular adoption header, negated completion and report-first preview. [Log](challenge-tests.log). |
| Existing runner and professional-reporting suites | **148 + 13 tests PASS** during targeted development and included again in the final full gate. |
| Released assessment identity tests | **10 tests PASS**, including refreshed report-hash binding; also included in the full gate. |
| Both regulatory sources | **PASS** via standard-library reviewed text with `python -S` and via direct PDF with installed pypdf. [Text manifest](text-run-manifest.json); [PDF manifest](pdf-run-manifest.json). |
| Source and authored-evidence check | **PASS** with Poppler re-extraction: 45 page-bounded curated quotes, eight original-Act contextual passages and 16 authored findings; raw extracts reproduce byte for byte. [Log](source-verification.log). |
| Score and source preservation | All ten baseline scores, formal categories, functional results and source/provenance identities unchanged. Same-source DTA/EU scores and functional results unchanged. Generated JSON fingerprint updated. [Regression record](actual-source-and-baseline-regression.json). |
| Preservation | No protected historical narrative, source PDF, raw ingestion or framework text changed. Release-status changes to the two current author assessments do not change their determinations. |

## Fresh processor outputs

- [DTA report](au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md) and [technical appendix](au_dta_policy_v2_1/au_dta_policy_v2_1.technical_appendix.md): 11 primary quotations, with exact source identity and attributed findings preserved.
- [EU report](eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md) and [technical appendix](eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.technical_appendix.md): all 10 primary quotations in this run are classified as operative text, with scope and judgement limits retained.

These are actual generated files without editorial rewriting. Runtime paths identify the cloud execution, not a dependency on Mike's computer. Work cloud Linux/Python 3.12 was used; no paid model API or GitHub Actions was used. Reviewed-text processing is standard-library Python; direct PDF extraction uses pypdf, and optional re-extraction uses Poppler.

## Quality boundary

This pass improves demonstrated retrieval coverage, source-role clarity, release consistency and report readability. It does not establish world-class accuracy or independent validity. Unknown paraphrases, contextual exceptions, other legal instruments, non-English text and real operational effectiveness remain outside what these development cases prove. Attributed analyst conclusions remain author analysis rather than independently originated software judgements. Independent held-out evaluation and qualified second-reader review remain the next evidence needed to measure general assessment quality.
