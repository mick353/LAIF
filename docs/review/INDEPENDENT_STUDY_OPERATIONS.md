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
| `protocol_sha256` | Lowercase SHA-256 of the externally preserved study protocol. The CLI checks format, **not the referenced file's bytes**. |
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

`--require-human` refuses `SYNTHETIC` files. It does not verify whether a
`HUMAN_ADJUDICATED` assertion is true. Retain signed reviewer and adjudication
evidence separately and arrange independent audit of input custody. Use
`--format json` to preserve the entire statistical report outside the public
repository (for example, through a privately controlled output redirection).

## Read results correctly

- `development` and `holdout` remain separate. The tool does not optimise any
  thresholds or choose a favourable split.
- Each system receives a confusion matrix (TP, TN, FP, FN), **answered**
  and **abstained** totals, coverage, accuracy on answered cases, precision,
  recall, F1 and conditional false-positive/false-negative rates.
- Undefined denominators produce JSON `null`, **not** zero. Abstentions are
  excluded from class-error counts but still reduce coverage.
- Approximate Wilson 95% intervals accompany precision and recall; they
  assume independent labelled units. They do **not** account for multiple
  attributes per document, correlated case families, non-random selection or
  multiple comparisons. No interval is claimed for F1.
- Human pre-adjudication pairwise agreement and Cohen's kappa are separate
  from tool-versus-consensus performance. Kappa can be undefined for
  constant labels or insufficient shared observations.
- LAIF-versus-checklist and LAIF-versus-keyword comparisons use **only cases
  answered by both**; the report includes the common denominator and paired
  correct/wrong counts. Do not turn these counts into significance claims.
- Case identifiers with errors or abstentions remain visible for traceable
  error analysis. Do not publish identifying source data or sensitive IDs.
- Output reports include a canonical input digest, a holdout snapshot digest
  and the comparator-script digest. These support **reproducibility**, not
  proof that the study was preregistered or blinded.

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
