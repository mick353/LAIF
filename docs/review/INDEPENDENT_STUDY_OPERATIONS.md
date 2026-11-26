# Comparative study operations: local, source-scoped, not certification

**Status:** proposed research infrastructure. This is not a scientific
validation result and does not replace the project's source- and semantic-review
requirements.

The small standard-library CLI in
`scripts/laif_study_compare.py` compares **caller-supplied** LAIF decisions with
two simple baselines and an independently adjudicated reference. It does not
invoke the LAIF engine, infer labels from documents, authenticate human experts,
inspect source bytes or certify an AI system. Its purpose is to prevent a future
study from hiding abstentions, mismatched case sets or reviewer disagreement.

## Try the synthetic fixture

From the repository root, with Python 3.10 or newer:

```bash
python3 scripts/laif_study_compare.py docs/examples/comparative-study-synthetic.json
```

The example is **entirely invented**. Its revision and SHA-256 fields are
deliberate placeholders; its reviewers, decisions and labels are fictional.
The resulting statistics illustrate arithmetic only and **must not be quoted
as LAIF performance**. Use the supplied file for familiarisation, not research.
No API key, network connection, added package or GitHub Actions run is needed.
Nothing is written to disk: a short, explicitly labelled summary is printed to
the terminal. For the complete machine-readable evidence and error register:

```bash
python3 scripts/laif_study_compare.py docs/examples/comparative-study-synthetic.json --format json
```

## Prepare an independent study file

Use the [synthetic example](../examples/comparative-study-synthetic.json) as a
schema illustration; do **not** modify it into an apparent scientific result.
Create a new private dataset outside the public repository containing:

| Field | Requirement |
| --- | --- |
| `schema` | Exact literal `laif.comparative-study.v1`. |
| `study_id` | Unique nonempty identifier; capture preregistration separately. |
| `label_provenance` | `SYNTHETIC` or self-reported `HUMAN_ADJUDICATED`. This is **not verified** by the tool. |
| `protocol_sha256` | Lowercase SHA-256 of the externally preserved study protocol. With `--protocol`, the CLI checks those bytes. |
| `evaluated_revision` | Declared 40-character Git SHA for the evaluated implementation; externally verify it against the actual run. |
| `cases[]` | Nonempty set including a `holdout` split. Each `id` is unique, each case has one atomic observable `attribute`. |
| `family`, `source_sha256`, `split` | Source-family and source-hash linkage. Identical sources/families may not appear in both development and holdout. |
| `reference` | Boolean expert-adjudicated label; do not convert uncertainty to false. Ambiguous cases need a separate study design or exclusion log. |
| `reviewer_votes` | Independent **pre-adjudication** booleans with reviewer identifiers. At least two different reviewers per case when labelled `HUMAN_ADJUDICATED`. |
| `adjudication_sha256` | Required on each human-labelled case; digest is self-declared and must be checked against an external record. |
| `predictions` | Exact keys `laif`, `checklist` and `keyword`, each `true`, `false` or `null`. `null` is an explicit abstention, **never** an implicit negative. |

All three systems must have a value (including explicit `null`) for **every**
case. Missing or duplicate case IDs, missing comparator keys, mixed source
families across development and holdout, malformed booleans and reviewer
duplicates fail closed. A dataset with no holdout is rejected. These checks
reduce accidental errors; they do **not** establish blinded assignment,
reviewer independence, fair baseline implementation or lack of training leakage.

For a caller-prepared human-labelled file:

```bash
python3 scripts/laif_study_compare.py /path/to/private-study.json --require-human
```

When comparing runs on the same frozen study, supply the preserved protocol
file and the externally recorded holdout SHA-256:

```bash
python3 scripts/laif_study_compare.py /path/to/private-study.json --require-human \
  --protocol /path/to/frozen-protocol.txt --expect-holdout-sha256 YOUR_FROZEN_HOLDOUT_SHA256 \
  --format json
```

Replace `YOUR_FROZEN_HOLDOUT_SHA256` with the saved 64-character digest.
Record the holdout digest after adjudication and before inspecting method
performance. It covers each holdout case ID, family, source SHA-256, attribute
and reference label. Row order and new predictions leave it unchanged. The
full input digest covers predictions and votes as well. The CLI stops before
printing statistics if a supplied protocol or holdout digest fails to match.
Retain the preregistration and the post-adjudication handoff separately.

`--require-human` refuses `SYNTHETIC` files. It does not verify whether a
`HUMAN_ADJUDICATED` assertion is true. Retain signed reviewer and adjudication
evidence separately and arrange independent audit of input custody. Use
`--format json` to preserve the entire statistical report outside the public
repository (for example, through a privately controlled output redirection).

## Read results correctly

- `development` and `holdout` remain separate. The tool does not optimise any
  thresholds or choose a favourable split.
- Each system receives confusion counts, conditional accuracy, precision,
  recall, F1 and conditional false-positive/false-negative rates. The report
  also gives coverage and correct answers per eligible case. Recall over all
  reference positives uses every labelled positive in its denominator.
  Positive and negative abstentions are reported separately.
- Undefined denominators produce JSON `null`, **not** zero. Abstentions are
  excluded from class-error counts but still reduce coverage.
- Approximate Wilson 95% intervals for conditional precision and recall are
  withheld where sources or families repeat. Otherwise interpretation still
  requires independently sampled units. Source and family counts help
  distinguish the number of observations from the number of documents.
  Sampling bias and multiple comparisons require a study-specific analysis.
  [Cameron and Miller on clustered observations](https://escholarship.org/uc/item/1jq5d0pq)
- Human pre-adjudication pairwise agreement and Cohen's kappa are separate
  from tool-versus-consensus performance. Each reviewer pair retains all four
  cells of its before-consensus comparison, including who labelled an item
  positive when the other did not. Kappa can be undefined with constant
  labels or insufficient shared observations.
  [Krippendorff on agreement and information](https://www.tandfonline.com/doi/full/10.1080/19312458.2011.568376)
- For each baseline the comparison gives the accuracy difference on cases both
  systems answered, as well as the difference in correct decisions per
  eligible case and coverage across the full sample. A three-by-three table
  accounts for every case by pairing correct, incorrect and abstained outcomes.
  Read accuracy and coverage together.
  [El-Yaniv and Wiener on selective classification](https://jmlr.org/papers/v11/el-yaniv10a.html)
- The difference in correct decisions per eligible case is recalculated
  after omitting each declared family in turn. Read the range as a
  sensitivity check. A span crossing zero shows that the ordering depends
  on which family is included. The range requires at least two families,
  with each source assigned to one family. It has no confidence level.
- Case identifiers with errors or abstentions remain visible for traceable
  error analysis. Do not publish identifying source data or sensitive IDs.
- Output reports include a canonical input digest, a holdout snapshot digest
  and the comparator-script digest. These support **reproducibility**, not
  proof that the study was preregistered or blinded.

### What the new checks catch

In one six-case synthetic regression, the LAIF-labelled system answered two
cases correctly and skipped four. The baseline answered five correctly.
On just the two common answers, LAIF led by 50 percentage points. Across
all six eligible cases it trailed by 50 percentage points. In a different
synthetic regression, one eight-case family drove a 60-point lead. Omitting
that family reversed the comparison to a 100-point deficit. These examples
are constructed to exercise the arithmetic. They supply no field estimates.

## Scholarly study gate

1. Identify narrow, observable control constructs and pre-register the
   comparison method, exclusion rules, sampling plan and target metrics.
2. Independently recruit appropriate reviewers and establish a blinded
   coding/adjudication process with uncertainty and conflict handling.
3. Assemble lawfully obtained, independently selected documents; inspect
   exact texts, version dates, permission, relevant roles and source hashes.
4. Freeze the actual LAIF revision and the checklist/keyword baseline rules.
   Collect comparator predictions without using the adjudicated labels to
   tune the methods. Keep source families out of both data splits.
5. Preserve pre-consensus votes, decisions, source/quote traces and context.
   Use the tool to compute **descriptive** study statistics.
6. Independently reproduce the reports, analyse hard false positives, false
   negatives and abstentions, and account for clustered cases and uncertainty
   in a separate statistical analysis before any research publication.
7. Run a distinct non-technical usability study: task completion, setup
   failures, comprehension, time-to-insight and observer-rated usefulness.
   Do not infer usability from a successful CLI test.

**Acceptance:** every published performance claim names its frozen source
sample, independent reference process, valid comparisons, uncertainty,
counterexamples, limitations and a reproducible source-level execution record.
This standard applies whether LAIF performs better **or worse** than the
baselines. The report is a diagnostic study, not a legal opinion or deployment
safety certification.
