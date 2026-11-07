# Scholarly evidence reviews: neutral method and publication discipline

**Audience:** policy researchers, AI assurance teams, regulators, safety evaluators,
legal scholars and independent reviewers. **Status:** research protocol, not an
independently validated measurement instrument, legal opinion or safety certificate.

LAIF may be used as an **openly identified analytical lens**; the audience need not
adopt, agree with or endorse LAIF. The subject of each report is the **source and
research question**, not the framework's branding, vocabulary or score.

For publication drafting, use the [neutral research-report template](SCHOLARLY_REPORT_TEMPLATE.md).
For historical score interpretation, first read the [legacy-result boundaries](LEGACY_RESULT_BOUNDARIES.md).

## Start: the neutral path

From the repository root with Python 3:

~~~bash
python3 scripts/laif_research_report.py docs/examples/vendor-policy.md --scope excerpt --date 2026-11-07
~~~

This uses the bundled **synthetic** document, a local text extractor and no
hosted model, API key or GitHub Actions. It prints three files written into the
ignored local `laif_outputs/research/` folder:

1. `*.research_report.md`: conservative, human-readable source inventory.
2. `*.research_data.json`: source hashes, exact passages, source coverage,
   method fingerprint, uncertainty and review status.
3. `*.review_template.json`: empty, source-locked **analyst interpretation**
   template for later manual completion.

All three share a source-and-dossier-specific name so separate study questions,
review dates and annotations do not overwrite one another. Every source is
identified by its original-byte SHA-256, extracted-text SHA-256 and admitted
evidence-manifest SHA-256; the code and underlying engine have recorded fingerprints.

For a private real-world review:

~~~bash
python3 scripts/laif_research_report.py /path/to/policy.md --scope unknown --instrument-status unknown --question "What source-visible evidence supports the proposed safety controls?" --preview
~~~

`--preview` prints without writing. Omit it when ready to save. Support for
`.txt`, `.md`, `.markdown` is standard-library-only. `.docx` needs locally
installed `python-docx`; `.pdf` needs locally installed `pypdf`. No automatic
downloads, online document retrieval, OCR or page-citation verification occur.
Inspect extraction warnings and compare quoted passages with the actual
original, especially for PDFs. The supplied HTTPS `--source-url` is metadata
**only** and is not fetched or authenticated.

### Source-scope declarations

- `--scope unknown` is the default and safest when completeness is unverified.
- `--scope excerpt` expressly limits claims to supplied pages or text.
- `--scope declared_full_document` is a **claim by the operator**, not proof
  that all annexes, revisions, implementing instruments or procedures exist.
- `--instrument-status unknown|historical|asserted_current` is likewise an
  operator declaration. Verify effective dates, amendments, repeal,
  jurisdiction and territorial applicability against primary sources.

**Do not use a partial excerpt to declare that an organisation has no control,
redress mechanism, audit power or legal duty.** Failure to retrieve a passage
is not evidence that the relevant protection is absent.

## Scholarly pass sequence

### Pass 1 — Research question, corpus and provenance

1. Pose a falsifiable, source-bounded question. Record which legal
   provisions, technical controls, people, jurisdictions and dates matter.
2. Predefine the corpus and its completeness. Separate binding primary law,
   regulatory guidance, corporate policy, technical logs, supplier assurances,
   journalism and analyst commentary. They have different authority.
3. Record official URLs, source versions and original hashes. Inspect the
   source directly; this software does not independently authenticate URLs.
4. For a comparative study, select documents *before* reading the results;
   preserve selection rules and omitted candidates to expose cherry-picking.

### Pass 2 — Exact observations and explicit limits

The CLI supplies an **illustrative candidate quote inventory**, not a random
sample, document-wide search result, or validated diagnostic test. Candidate
retrieval depends on heuristics from LAIF's existing engine; it may miss relevant
clauses and reflect the tool's choice of concepts. Offsets refer to **extracted
text**, not source PDF pages or byte locations. No claim is automatically
promoted from a quote to an operational conclusion.

Check every selected passage **against the source in context**. Search for
countervailing provisions, definitions, exceptions and surrounding instruments.
Document the findings that *support* the source as carefully as possible
deficiencies. Do not confuse absence of a keyword with absence of a duty.

### Pass 3 — Interpretation, competing explanations and falsification

Populate a copy of the generated `*.review_template.json` with a `findings`
array only after checking the source. Each proposed finding must provide:

| Required field | Purpose |
|---|---|
| `finding_id` | Stable identifier, e.g. `F001` |
| `claim_type` | `OBSERVATION`, `INFERENCE` or `HYPOTHESIS` |
| `statement` | Narrow, falsifiable claim; not a blanket compliance verdict |
| `evidence_ids` | One or more admitted `E001`-style exact passages |
| `counterevidence_ids` | Known quoted contradictory/qualifying passages, if any |
| `alternative_explanations` | At least one real competing reading or mechanism |
| `limitations` | Evidence, scope, legal or measurement boundaries |
| `analyst_id` | Attribution; identity is not authenticated by the tool |
| `criterion_ids` (optional) | Map findings to A.1–A.4, Q1–Q3 or G.1; these are review coverage, not pass labels |

The template is tied to both the original source SHA-256 **and the exact
admitted evidence-ID/quotation manifest**; altered sources, changed candidate
inventories or unrecognised quotation IDs cause explicit errors. New templates also bind both principal-text and Toolkit SHA-256 hashes and the internal toolchain fingerprint; stale or partial method hashes are rejected. Legacy annotations without any of these method identifiers remain readable but are explicitly labelled `UNBOUND_LEGACY_ANNOTATION`.

Every dossier lists eight review areas: the four Integrity Layer properties (with §2.5 calibration applicability), all three Coherence Test questions and self-application. Areas without mapped analyst findings remain `NOT_ASSESSED`. Attached claims remain `ANALYST_CLAIMS_ATTACHED_REVIEW_REQUIRED`; neither retrieval nor form completion establishes coherence. The source references guide review rather than replacing the full principal text and Toolkit.

Submit the completed template as:

~~~bash
python3 scripts/laif_research_report.py docs/examples/vendor-policy.md --scope excerpt --date 2026-11-07 --review-file /path/to/completed.review_template.json
~~~

Even with annotations, the output says `ANALYST_ANNOTATED_DRAFT`, not
peer-reviewed, legally sufficient or verified.

For each hypothesis, identify what **independent primary evidence could
disconfirm it**. A reported safeguard may be confirmed by live logs,
configuration, operating instructions and tested escalation paths; it cannot be
confirmed by a policy paragraph alone. Conversely, an omitted paragraph may
be supplied by binding external law or a separate operational document.

### Pass 4 — Independent source checking and disagreement

The optional second-reader command does **not** generate or simulate reviews:

~~~bash
python3 scripts/laif_research_review.py /path/to/the.research_data.json --template
~~~

Save **separate copies** for two actual reviewers. They must inspect the
original source and choose `source_matched`, `source_disagrees` or `unverified`
for each extracted passage; for analyst findings choose `supported`,
`challenged` or `uncertain`. Each decision needs a reason. They must disclose
whether they inspected the original and whether they consider their review
independent. Run:

~~~bash
python3 scripts/laif_research_review.py /path/to/the.research_data.json --review /path/to/reviewer_a.json --review /path/to/reviewer_b.json
~~~

The output records target-level agreement and disagreements, raw paired
agreement only where both reviewed the same target, missing assessments and
uncertainty. Different reviewer IDs are enforced, but identities and
independence **cannot** be verified by software. A 100% agreement figure
means only that submitted labels match; it is **not** ground-truth validity,
calibration, peer-review acceptance or certification. Conflicts require
human adjudication.

### Pass 5 — Critical synthesis and publishability

Prepare a research report with these sections, in order:

1. Neutral research title and an abstract answering the actual question.
2. Primary-source identifiers, scope, versions and dates.
3. Predefined method, sampling/selection biases and exact quotations.
4. Evidence **for and against** each interpretation, and alternatives.
5. Effects of missing documents or independent operational evidence.
6. Safety or legal consequences clearly distinguished from observed facts.
7. Limitations, unresolved disagreements and tests that could overturn it.
8. Reproduction instructions, version hashes and reviewer disclosures.

**Hold publication** if source identity, quotation fidelity, legal applicability,
counterevidence, independence or central assumptions remain materially
unresolved. A draft may be shared for review with its caveats, but neither
the analyst template nor second-reader status grants publication clearance.

## Regulation and frontier-AI safety: avoid category errors

Regulatory **applicability**, written **governance design**, demonstrable
**control operation** and overall **safety** are four different propositions.
They need different evidence and must never be inferred from a single
policy-document score.

For frontier or highly autonomous AI risk, investigate at least:

- **Capability and threat model:** actual model/system version, tools, access,
  operator privileges, autonomy, misuse routes, safety-critical dependencies.
- **Evaluations:** predefined dangerous-capability and misuse tests,
  adversarial testing, evaluation blind spots, evaluator independence, measured
  false negatives and distribution shift.
- **Control boundaries:** least privilege, human approval, tool isolation,
  access revocation, monitoring, containment and tested shutdown/recovery.
- **Escalation and accountability:** named risk owners, stop/deploy authority,
  trigger thresholds, incident records and external reporting channels.
- **Evidence of operation:** signed evaluations, reproducible test logs,
  change histories, red-team findings, exercises, observed failure rates and
  attempts to bypass safeguards.
- **Uncertainty:** plausible severe scenarios and epistemic unknowns versus
  demonstrated incidents. Speculative loss-of-control scenarios are not
  presented as established events or quantified probabilities.

Use sector-specific standards and **current** law only when applicable. Two
primary examples illustrating the difference between method and enforceable
duties:

- [NIST AI RMF: Measure](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
  emphasises documented measurements, uncertainty, benchmarks and
  independent assessments as risk-management practices; the RMF is not a
  blanket legal compliance certificate.
- [EU AI Act, Article 55, in its consolidated legal text](https://eur-lex.europa.eu/eli/reg/2024/1689)
  sets obligations for **providers of general-purpose AI models with systemic
  risk**, including evaluations, adversarial testing, systemic-risk mitigation,
  serious-incident information and cybersecurity. Assess applicability and
  operative legal dates for each provider; do not generalise these obligations
  to all AI systems.

The [US National Academies' distinction between reproducibility and
replicability](https://nap.nationalacademies.org/resource/25303/Combined%20Reproducibility%20Brief%20vs2.pdf)
is reflected in the labels here: a second deterministic run of the same code
is **not** an independent empirical replication.

## Validation, benchmarking and publication claims

Automated tests can show that the renderer does not invent citations or
silently promote heuristic scores into legal conclusions. They **cannot**
establish that the underlying concept detectors find all relevant safeguards.
To claim empirical effectiveness, conduct and document a separate,
pre-registered, independently labelled evaluation:

1. Define target constructs and adjudication rules, including what counts as
   genuine absence versus not in scope or not observable.
2. Freeze a versioned, legally verified dataset with complete primary sources,
   sectors, dates and known negative/positive cases.
3. Blind at least two suitably qualified reviewers to the model's
   classifications, preserve their disagreements and adjudications.
4. Compare against direct human review and a simple non-LAIF baseline,
   including false negatives, false positives and confidence intervals.
5. Test unseen sectors, obsolete law, incomplete excerpts, synonyms,
   adversarial counterexamples and model/version drift.
6. Publish methods, corpus licensing limits, failures and uncertainties.
   Do **not** cite synthetic fixtures or unit-test pass rates as field accuracy.

There is presently **no verified external gold-standard corpus or measured
real-world sensitivity/specificity** for this new reporting path. Its value is
source traceability and disciplined human review, not proof of LAIF superiority.

### Publication language that passes the neutrality check

- Acceptable: “In the supplied excerpt, passage E003 assigns final eligibility
  approval to a human reviewer. Operational adherence was not tested.”
- Acceptable: “The provided text did not establish a numerical intervention
  threshold; this does not rule out a threshold in other instruments.”
- Not acceptable without much more evidence: “The institution has no
  accountability”, “the law is non-compliant”, “all current AI is unsafe”,
  “LAIF proves the best regulatory model”, or a probability of future
  loss of control derived from wording alone.

## Verification (offline)

~~~bash
python3 -m unittest tests/test_research_scholarly.py
python3 scripts/laif_verify.py --full --base-ref origin/main
~~~

The new tests are synthetic and verify no-write previews, reproducible
outputs, source-offset checks, low-confidence abstention, annotation
provenance, invalid JSON/URLs, independent-review limitations, disputed
assessments and non-promotional reporting. The full local gate also checks
protected artefacts and existing deterministic report regeneration. It does
not send anything to GitHub Actions or an external AI API.

## Substantive criterion reviews

The --criteria-template flag creates unfilled records for all eight LAIF criteria. The completed criteria_review carries authored determinations, explicit Q1a/Q1b, applicability, alternatives, closing evidence and exact curated source spans beyond the automatic inventory. Its protocol is hash-bound. The processor --require-complete-review gate requires all eight records before writes. Partial reviews preserve unassessed areas; coverage is not satisfaction. Second-reader targets include every criterion and curated quotation. [Schema and boundaries](../governance/SUBSTANTIVE_REVIEW.md).
