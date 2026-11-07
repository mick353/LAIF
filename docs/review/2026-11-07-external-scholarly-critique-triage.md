# Independent scholarly critique: evidence triage and validation plan

- **Recorded:** 7 November 2026 (Australia/Sydney)
- **Status:** research agenda, **not** an independently validated LAIF finding
- **Repository baseline checked:** [`main` at `09f8687`](https://github.com/mick353/LAIF/commit/09f8687b58d1c5547cfe58bcf4e38aa7da3619a2)
- **Audience:** independent researchers, legal reviewers, AI-safety specialists, scholarly report authors and maintainers

This register is a critical review aid, not a promotional case for LAIF. It
separates reproducible repository inspection from questions that require
outside researchers, documents, experiments and professional judgement.
No external validation result is represented as completed here.

## Provenance and disposition of the external critique

On 7 November 2026, the project owner supplied a Gemini Pro response described
as a repository review. Its author subsequently **acknowledged that it had not
retrieved the repository, inspected source files or executed tests**; it had
synthesised a plausible account from prompt metadata. Consequently:

- Its alleged deficiencies and conclusions have **no evidentiary standing as
  findings about LAIF's actual implementation**. Compare hypotheses with
  inspected source, not titles or remembered descriptions.
- Test counts repeated in that account are not independent verification.
- The invented “Generative AI Profile X” facts, asserted EU-law violation and
  proposed `laif-audit --target ... --framework ...` command are **not actual
  source records, legal determinations or verified LAIF commands**. Do not
  publish that example as a real assessment. “Mispar Hechrechi” in the text
  is not substantiated as LAIF terminology.
- Its useful *research questions* concern construct validity, inter-reviewer
  agreement, regulatory interpretation, adversarial robustness and neutral
  reporting; each still requires an independent investigation.

## Repository state and parallel change control

| Workstream | State checked 7 Nov 2026 | Boundary / next review |
| --- | --- | --- |
| [`main`](https://github.com/mick353/LAIF) | `09f8687`, canonical | Published toolkit and corpus. Published local software tests are not scientific validation. |
| [PR #89](https://github.com/mick353/LAIF/pull/89) | Open draft | Corpus cross-reference addition; require source and semantic review, no assumed critical defect. |
| [PR #90](https://github.com/mick353/LAIF/pull/90) | Open draft | EU AI Act source verification; independently check authentic legislation, role, scope and operative date. |
| [PR #94](https://github.com/mick353/LAIF/pull/94) | Open draft | Documentary frontier-AI assurance; no implied live model evaluation or containment proof. |
| [PR #95](https://github.com/mick353/LAIF/pull/95) | Open draft | Scholarly reporting / second-reader proposal; branch tests cover software, not empirical construct validity. |

**Coordination:** An independent Scholar session may review these PRs in
parallel. Its ongoing work is not a published outcome; do not amend its
working branches during this documentation reconciliation. Recheck the live
PRs, human-review their substantive changes, run the local verifier and obtain
semantic approval before merging. No GitHub Actions or paid model APIs required.

## Strict claim boundaries

| Claim class | Source-scoped conclusion possible | Conclusion **not** supported by that source alone |
| --- | --- | --- |
| Software reproducibility | Tested revision, fixture corpus, hashes, local outcomes, deterministic regeneration and defined mutation rejection. | Field accuracy, data truth, scientific validity or control effectiveness. |
| Documentary governance | What supplied policies explicitly state, omit or contradict. | How controls actually operate, whether unprovided records exist, model behaviour. |
| Legal and regulatory | A qualified comparison with primary obligations for identified roles, dates and jurisdiction. | Definitive compliance rulings or a violation inferred from the absence of a specially named artefact in one file. |
| Frontier AI | Provenance and completeness of **supplied** safety cases and test reports. | Native deceptive-alignment, shutdown, jailbreak, autonomy or catastrophic-risk measurements. |
| Independent validation | Future results against pre-registered outside reference standards. | Any unperformed experiment, reviewer identity, accuracy estimate or confidence interval. |

### EU AI Act precision

For Article 9, Article 10 or other provisions, cite the inspected version of
[Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj),
with article, paragraph and source date. Determine whether the use/system is
in scope, who owes the duty (provider/deployer or other actor), which date or
transition applies, and exceptions. Separate **binding legal text** from
guidance, harmonised standards and voluntary practices. A missing statement in
an excerpt is not proof the organisation lacks the control.

For example, Article 10(2)(b) deals with data-collection processes and data
origin within its applicable legal context. It does **not** automatically
require an artefact specifically named “validation data provenance registry”,
nor justify a breach finding on invented facts. Article 9's iterative risk
management requirements cannot be established by one static policy snapshot.
Where facts or interpretation are inadequate, label the outcome **evidence
insufficient / qualified legal review required**, record alternatives and
request appropriate additional evidence.

### Frontier-safety evidence separation

1. **Stated intention**: model card, supplier assertion, safety-case design or
   documented policy. Attribute the author and provenance.
2. **Reported evaluation**: identified evaluator, model/build, date, protocol,
   scenarios, limitations, results and source report. A *claim of having
   tested* is not the same as inspecting test records.
3. **Independently observed dynamic behaviour**: authorised external testing
   under a specified threat model with reproducible safeguards, permissions and
   limitations. A policy score cannot imply this tier.
4. **Operational evidence**: attributable monitored incidents, near misses,
   interventions and corrective action, if lawfully available.

External dynamic tests may be separately ingested as attributed evidence.
Neither PR #94 nor existing static text analysis performs those tests natively.
Any future interface to test suites requires a separate safety review and
explicit implementation authorisation.

## Independent validation protocol — **proposal only**

**Question:** For specified, observable governance-document constructs, how
accurately and usefully does LAIF identify source-supported attributes and
legal-analysis questions compared with independently adjudicated humans?
**Incremental-value question:** Does it do better than a straightforward
structured checklist or a reproducible keyword/obligation extraction baseline
under comparable input, review-time and reviewer conditions? This does not ask
whether LAIF can prove “AI safety” as a single property.

1. **Pre-register constructs and outcomes.** Define labels and abstention:
   e.g. assignment of responsibility, monitoring trigger, incident escalation,
   override authority, documentary contradiction, or role-specific statutory
   issue. State false-positive and false-negative costs. Do not force ambiguous
   law into an artificial binary.
2. **Source an independent held-out corpus.** Start with a pilot, then justify
   a stratified sample by document type, domain, completeness, jurisdiction,
   role and positive/negative prevalence. Fifty documents is a *possible
   pilot*, not a power calculation. Check licences, privacy, historical
   exposure, version and SHA-256. Keep pre-existing fixtures out of the holdout.
3. **Use human independent reviewers.** At least two blinded annotators per
   case; a third adjudicator or larger panel for disputes. Obtain actual legal
   and AI-safety subject-matter review where needed. Record reviewer
   independence, task instructions, qualifications, conflicts and exclusions.
   The language model running the experiment is not an “independent panel”.
4. **Pin execution.** Record the evaluated commit, dependencies, mode,
   thresholds, full input manifests and exact commands. Freeze the method
   before exposing the holdout. Use separate development data for revisions.
5. **Measure human disagreement before consensus.** Report unresolved
   categories and suitable pairwise Cohen kappa or a justified multi-rater
   measure (e.g. Krippendorff alpha). Model-versus-consensus agreement is
   not inter-human reliability. No consensus automatically proves the legal
   answer objectively true.
6. **Compare with adjudicated labels.** For well-defined classifications,
   report per-label precision, recall, F1, confusion matrices, abstentions,
   false positives and negatives, prevalence and uncertainty intervals;
   disaggregate by case type and measure quotation accuracy. Also ask blind
   reviewers whether findings are practically useful and traceable.
7. **Measure incremental value against baselines.** Freeze a plain-language
   checklist based on published governance categories and a transparent local
   keyword/obligation extraction rule. Pre-register matched access to documents,
   time and reviewer instructions. Compare error rates, evidence traceability,
   useful findings not duplicated by the baselines, and time-to-insight. Avoid
   treating checklist categories as an independent legal ground truth.
8. **Use negative and adversarial controls.** Pre-specify document mutations
   involving contradictions, swapped provider/deployer duties, absent control
   evidence, novel synonyms, misleading boilerplate and time-dependent
   obligations; assess sensitivity and unintended verdict flips. Test language
   and translation variants in a separate explicitly supported scope: do not
   assume multilingual capability. Keep fixtures and field outcomes separate.
9. **Usability pilot with non-specialist operators.** Recruit authorised
   policy/procurement participants without Python experience, observe whether
   they can complete the existing local quick-start and correctly interpret
   the limitations, and measure task completion, setup failures, time,
   comprehension and confidence versus actual correctness. Test revisions
   iteratively without changing the held-out validation protocol.
10. **Replicate, criticise and report.** An independent second evaluator
   reproduces selected records from the pinned revision. Publish source
   manifests, exclusions, disagreement, failure cases and limits before any
   efficacy claim; no retroactive optimisation on held-out data.

**Minimum research outputs:** preregistered protocol, corpus/manifest and
legal-scope log, independent annotation manual and agreement, disaggregated
performance/error analysis with intervals, baseline-comparison results,
adversarial results, observed usability findings, reproduction instructions
and external reviewer sign-off. **Not yet executed.**

## Scholarly output acceptance criteria

A report that can stand on its own, even for audiences uninterested in LAIF:

- Leads with the research question, a bounded conclusion, sources and method;
  avoids promoting adoption or claiming novelty from internal terminology.
- Distinguishes directly quoted observations, logical inferences, hypotheses,
  missing evidence and plausible alternatives, with page/section references
  and hashes where possible.
- States branch, commit, tool revision, source and output modes, date, sector,
  external-review roles and uncertainty. Draft PR features cannot appear as
  capabilities of `main`.
- Translates internal categories into understandable legal/governance terms,
  without treating LAIF names as definitions in EU/NIST/OECD instruments.
- Separates executable software tests from independently measured accuracy;
  a model-card claim from witnessed model behaviour; and a source omission
  from a proven legal breach.
- Asks a second reviewer to falsify the major conclusions and records
  disagreements, competing evidence and explicit reasons to abstain.
- Includes commands **only when verified in the tested revision** and clearly
  labels synthetic examples. For future originality claims, compare specific
  mechanisms with established systems-safety, legal-formalisation and
  governance literature before claiming unique discovery.

## Priorities and handoff

| Priority | Work | Completion evidence |
| --- | --- | --- |
| P0 | Correct current guides and source provenance | Main/draft status, latest checked SHA, source links, unvalidated claims and no invented CLI/results. |
| P1 | Semantic review of PRs #89/#90/#94/#95 | Source-level diff, legal and safety boundaries, local tests, human review decision; no automatic merge. |
| P2 | Blinded validation and usability pilot | External reviewers, locked corpus/protocol, independent labels, fair checklist/keyword comparisons, error register, usability findings and replication report. |
| P3 | Extended study or dynamic safety-evidence interface | Independent funding/permission/safety scoping, new approval and external test evidence where appropriate. |

Project authorisation for scholarly review and documentation does **not**
automatically extend to paid evaluation, expert recruitment, a new scoring
algorithm or merge approval. GitHub is the canonical source for code and
research specifications; Notion tracks status and decisions, not independent
proof of a scientific claim.
