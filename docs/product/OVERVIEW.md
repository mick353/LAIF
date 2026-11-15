# LAIF: practical AI governance review

**Turn AI policy promises into controls you can inspect.**

The Law-Aligned Intelligence Framework combines a governance method with a local document-review toolkit. It helps reviewers examine whether an AI policy, supplier response or operating procedure specifies the responsibilities, safeguards and evidence needed to make its commitments actionable.

## The problem it addresses

A document can promise accountability without naming an accountable owner. It can require monitoring without specifying what triggers intervention. It can require approval without saying who has the authority to stop a deployment.

LAIF makes those questions easier to examine systematically. Its outputs connect source quotations to identified gaps, potential failure pathways and proposed controls.

## What you can do with it

| Task | Practical result |
|---|---|
| Review an AI governance policy | Identify protections already expressed and controls that need clarification |
| Assess supplier documentation | Prepare targeted evidence requests and contract-control questions |
| Examine a release procedure | Review approval, monitoring, incident and change-control arrangements |
| Review multiple documents | Identify recurring gaps and organise follow-up work across the portfolio |
| Check a control-evidence manifest | Verify file identity, exact quotations, declared positive/negative tests and contradictory records |

See [uses across fields and expansion opportunities](USE_CASES.md) for concrete tasks, implemented support and remaining field-evidence needs.

## What a review produces

For a single document, an authorised user can open the owner-private **LAIF
Research Workspace**, upload or paste the source, inspect quotations beside
proposed judgments, decide which passages to keep, reject or investigate, and
download a brief with the remaining questions. Use the private access link
provided to you. The **local Python toolkit** is useful for files, specialist
reviews and batches, with reports saved on your computer. The Site has its own
versioned catalogue and assessment runtime; its live acceptance checks remain
in the [product and Site readiness programme](PRODUCT_READINESS_2026-11.md).

For the local first-use path, [guided start](../GETTING_STARTED.md) previews
extraction and produces a research report, evidence JSON and an empty human
review template. It can then open a resumable candidate-passage review. The
separate internal diagnostic produces an institutional report, technical
appendix, quote bank, gap register, proposed controls and structured JSON.
Both paths retain original-source identity; neither automatically validates
the source's authority or a control's real-world operation.

Read the outputs in this order:

| Reader question | What to inspect | What to do |
|---|---|---|
| **What the document wording supports** | Original file, extraction warnings and exact quoted passages | Confirm the quotation and its surrounding context in the original. |
| **What remains unestablished** | Scope and provenance limits; provisional documentary judgments; counterevidence and exceptions | Treat `NOT_ESTABLISHED` as insufficient wording found by this scan, not proof of an absent safeguard or legal breach. Positive wording does not prove implementation. |
| **What to check next** | Passage decisions, owner records and unresolved questions | Keep, reject or request more evidence for a passage; make any substantive criterion determination in a separate attributed author review. |

These passage decisions are recorded as **operator dispositions** for a
**candidate passage**.
The eight **provisional documentary judgments** are automatic rule-based
inferences about supplied wording. An **author review** is a separate human
assessment. None is a legal or operational verdict merely because it appears
in a report or export.

For research publication or regulator-facing analysis, use the
[neutral scholarly reporting path](../research/SCHOLARLY_REPORTING.md).
It separates exact-source observations from human-attributed interpretations,
preserves source scope, versions and code fingerprints, and supports
source-locked second-reader disagreement records without claiming
peer-review completion or scientific validation.

Each report is an aid to professional judgement. A reviewer checks the source context, confirms automatic classifications, and investigates whether supporting controls are documented elsewhere or operate in practice.

A reviewer can supply a [source-bound substantive assessment](../governance/SUBSTANTIVE_REVIEW.md) with all eight criteria, applicability and curated quotations. The executive finding leads with that authored reasoning. Software checks references and coverage; it does not independently validate the judgement.

## Model-independent by design

LAIF does not depend on a particular AI model or provider. Its core text and Markdown workflow runs locally in Python without a model API key. The tool produces its own structured diagnostic outputs; you may use the analyst bundle with an assistant of your choice for further work.

The local toolkit works without a hosted account, GitHub Actions or an external
model service for text documents. Word and PDF extraction use optional local
packages. The separate private Site requires authorised browser access and has
its own deployment and acceptance record; local test results do not establish
the live Site's behaviour.

## The assessment method

The Coherence Test examines whether restrictions protect identifiable human interests, whether the reasoning works consistently across comparable situations, and whether arrangements and consequences can be revised. The Integrity Layer examines transparency, honesty, authorised boundaries and empirically supported calibration where applicable. Self-Application extends scrutiny to governance actors.

External documents can express safeguards in their own vocabulary. The separate LAIF-native mode evaluates documents that explicitly claim or seek LAIF adoption against its stricter internal criteria.

## Start with an actual output

Read the [sample assessment](../examples/sample-assessment.md), inspect its [source policy](../examples/vendor-policy.md), then follow [Getting started](../GETTING_STARTED.md) to reproduce it. The example is synthetic, so you can explore the workflow without uploading private material.

[Product home](../../README.md) · [Assessment method](METHOD.md) · [Technical reference](REFERENCE.md)
