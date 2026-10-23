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

## What a review produces

The main institutional report gives a readable executive finding, quoted evidence, strengths, gaps and next actions. Supporting outputs include a technical appendix, quote bank, governance gap register, failure pathways, control recommendations and structured JSON.

Each report is an aid to professional judgement. A reviewer checks the source context, confirms automatic classifications, and investigates whether supporting controls are documented elsewhere or operate in practice.

## Model-independent by design

LAIF does not depend on a particular AI model or provider. Its core text and Markdown workflow runs locally in Python without a model API key. The tool produces its own structured diagnostic outputs; you may use the analyst bundle with an assistant of your choice for further work.

The product is a command-line toolkit with generated reports. Word and PDF extraction use optional local packages. It does not require a hosted account, GitHub Actions or an external model service to analyse text documents.

## The assessment method

The Coherence Test examines whether restrictions protect identifiable human interests, whether the reasoning works consistently across comparable situations, and whether arrangements and consequences can be revised. The Integrity Layer examines transparency, honesty and authorised boundaries. Self-Application extends scrutiny to governance actors.

External documents can express safeguards in their own vocabulary. The separate LAIF-native mode evaluates documents that explicitly claim or seek LAIF adoption against its stricter internal criteria.

## Start with an actual output

Read the [sample assessment](../examples/sample-assessment.md), inspect its [source policy](../examples/vendor-policy.md), then follow [Getting started](../GETTING_STARTED.md) to reproduce it. The example is synthetic, so you can explore the workflow without uploading private material.

[Product home](../../README.md) · [Assessment method](METHOD.md) · [Technical reference](REFERENCE.md)
