# Overhaul: exploratory discrimination checkpoint

Owner: LAIF delivery lead. Predictions and analysis: **Codex**, at Mick's
explicit request. This is model-authored exploration, not Mick's QA sign-off,
independent validation or a blinded known-answer study.

## Status and evidence

| Workstream | Status | Next step / dependency |
|---|---|---|
| WS3 extractor | Released in [PR #118](https://github.com/mick353/LAIF/pull/118), main `362a5be` | 67 focused checks; committed full gate 622 tests, two Windows symlink skips; merged tree identical and quick readback passed |
| WS1 discrimination | Preliminary hypotheses tested; acceptance **not established** | Obtain strong-comparator source bytes; review criterion interpretation and remaining overlapping evidence before any detector change |
| WS4 engine split | Pending stable WS1 baseline | Preserve substantive bytes but update code identity honestly; exact old fingerprint cannot identify changed source |
| WS2 plain summaries | Pending WS4 under requested sequence | Add separate summaries; retain authored reasoning exactly |
| WS5 documentation | Pending WS2 | Inventory inbound links and protected/history identities before moving records |
| WS6 public Site | Pending; no visibility change made | Separate public read-only content from private workspace; inspect upload implementation before publishing privacy claims |

The original owner attachment remains outside Git under `.codex-attachments`.
The requested sequence is WS3, WS1, WS4, WS2, WS5, WS6. This checkpoint does
not claim the six-workstream overhaul is complete.

## Preregistration and scope

[Predictions](predictions.json) and [their hash](predictions.sha256) were
committed and pushed at `abee53c` **before** running this comparison.
The predictions contain all eight provisional documentary determinations per
source, reasoning, four diagnostic comparisons and three clause deletions.
Existing corpus reports and DTA/NIST authored reviews were already known;
this is not a holdout and no statistical accuracy estimate follows.

The source bytes are pinned in the protocol. NIST and OECD retain their
`HASH_VERIFIED_LOCAL_ONLY` provenance limitations. NIST is the provisional
more operationally detailed source and OECD the less operationally detailed
principles instrument. That ordering is a hypothesis about document detail,
not about legal merit or real-world effectiveness. No source was promoted.

The [Commonwealth Ombudsman March 2025 guide](https://www.ombudsman.gov.au/__data/assets/pdf_file/0025/317437/Automated-Decision-Making-Better-Practice-Guide-March-2025.pdf)
was found at its official origin, but direct PC retrieval encountered a
Cloudflare challenge; no original bytes were admitted. The
[current NSW AIAF](https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/nsw-ai-assessment-framework)
uses a platform; an older PDF was not silently substituted. These candidates
remain intake work, not completed comparison evidence.

## Results

These are the existing engine's diagnostic dimensions, not the eight authored
criterion determinations or operational assurance scores.

| Retained source | Auditability | Enforcement | Overall diagnostic |
|---|---:|---:|---:|
| OECD | 80 | 40 | 53 |
| NIST | 80 | 80 | 64 |
| DTA | 100 | 80 | 59 |
| Original EU Act | 100 | 100 | 78 |
| LAIF v1.2 (native channel) | 100 | 100 | 98 |
| Clinical PDCA (native channel) | 80 | 100 | 76 |

Three of four registered ranking predictions held: NIST exceeds OECD on
enforcement and overall; LAIF exceeds OECD on native terminology. The predicted
NIST auditability advantage failed (80 versus 80). Native-channel scores are
not directly comparable measures of external-instrument legal quality.

None of three registered mutation predictions held. Removing GOVERN 2.1
(roles), MANAGE 2.4 (deactivation authority), or MANAGE 4.3 (incident response)
from NIST changed any numeric dimension by **zero**. The removed exact text,
locations, derivative hashes and deltas are in [results.json](results.json).
Original source files were not edited.

The engine uses document-wide presence signals. Other passages can retain the
same signal after one clause is removed, and a score may already be saturated.
Thus unchanged scores do not establish that a control is unimportant or that
the remaining document lacks it. The finding is narrower: these scores do not
measure the marginal contribution of these three clauses. Before modifying
scoring, inspect every remaining supporting span and distinguish legitimate
redundancy from an insensitive signal. Do not remove valid evidence merely to
make a prespecified score decrease.

Eight-criterion agreement is **not computable** from this run. The engine emits
diagnostics and `REQUIRES_SOURCE_BASED_REVIEW`; the eight determinations are
authored review inputs. Importing Codex's own predictions would create circular
agreement. Results retain nulls rather than treating missing author results as
disagreements or as `NOT_ESTABLISHED`. No claim that a source beats DTA on three
authored criteria has been established. No successful comparison was deployed
to the Site.

## Reproduce and regression boundary

Run `py -3 -X utf8 scripts/laif_exploratory_comparison.py --verify`.
The runner checks the prediction and source hashes, reruns the six originals
and three exact derivatives, and compares with the retained JSON. It refuses
to overwrite an existing receipt. The full suite includes this reproduction.
A passing reproduction test preserves the observed **failed hypotheses**; it
does not turn those hypotheses into successful discrimination evidence.

The probe uses a uniform `exploratory_retained_source` classification to avoid
mixing document-type choices into the ranking, with explicitly selected native
versus external channels. It is not a source-specific legal assessment. No
authored canonical reasoning or scoring implementation changed.
