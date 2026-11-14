# LAIF product and Site readiness

**Working programme — 14 November 2026.** Owner: LAIF delivery lead. Baseline:
`main` at `975e39cb6cfa24da440253364cad5b8f13f69b54`. This is a delivery
record and research plan, not a claim that the product or Site has passed the
acceptance checks below. Recheck GitHub, the private Site source and production
before using this record as a current status report.

## Product question and first complete journey

Can a policy owner or governance reviewer take one authorised document from
intake to an evidence-backed decision about what to keep, investigate or change,
without learning the command line or interpreting a folder of JSON files?

The first journey is **review one governance document**. The user should be able
to try the synthetic example, supply an authorised text, Word or PDF document,
inspect the extracted source and its limits, review each proposed finding beside
the supporting passage, record *accept*, *reject*, *needs evidence* or *outside
scope*, then export a concise report and an auditable review record. A saved
review must reopen with its source, method version and unresolved questions.
This journey is the reference path for both the local toolkit and the private
LAIF Research Workspace. Specialist research and batch workflows remain
available, but they do not define first-use success.

## Verified starting point and gaps

| Area | Present evidence | Remaining product gate |
| --- | --- | --- |
| Local engine | The 14 November Windows checkpoint in [issue #93](https://github.com/mick353/LAIF/issues/93) records main parity and a full local gate of 598 tests, two skipped, plus additional checks. The [7 November readable-evidence record](../verification/2026-11-07-readable-evidence/README.md) shows source quotations beside findings. | A passing software gate does not show that a first-time user can complete a review correctly. Test the whole journey on current Windows and Site builds. |
| Review workflow | [Getting started](../GETTING_STARTED.md) describes a working document command, authored eight-criterion JSON review and separate neutral research path. | Guide users through mode, scope, extraction, finding decisions, save/resume and export in one interface. Confirm that source changes invalidate stale reviews. |
| Site | The [Site bridge](../site/README.md) records a private browser workspace with a pinned engine, source catalogue and governed contribution package. The 8 November production receipt covered catalogue and text intake. | Check the current deployed revision, signed-in save/restore, real PDF intake, physical phone, keyboard, screen reader, zoom and failure recovery. A repository catalogue check is not hosted acceptance. |
| Source and legal context | [Issue #93](https://github.com/mick353/LAIF/issues/93) tracks original EU Act review, NIST assessed-text/PDF fidelity and DTAC upstream identity. | Show edition, authority, role, effective date, excerpt scope and unresolved provenance where a legal or framework claim appears. Keep a source-level finding distinct from a legal determination. |
| Usability evidence | The [September scenario review](../review/USABILITY_REVIEW_2026-09.md) found and corrected report defects using authored fixtures. | Observe intended users completing realistic tasks. Record failures, comprehension, effort and satisfaction on the exact tested build. The scenario review is internal regression evidence. |

## Delivery sequence and acceptance

| Stage and accountable owner | Work and dependency | Acceptance evidence |
| --- | --- | --- |
| **1. Guided review — product owner** | Map the one-document journey and implement a clear task-based start, source/extraction preview, report reading order and visible next action. Build on the current engine and source identity rules. | A novice can complete the synthetic sample and an unfamiliar authorised document from start to export without consulting the command reference. Unsupported formats, image-only PDFs, incomplete text and failed extraction produce a recoverable, accurate state. |
| **2. Review decisions — product owner** | Add a form over the existing source-locked review schema. Provide autosave, resume, explicit unknown/out-of-scope states, source-change detection and a concise decision summary. Preserve author attribution and alternatives. | Reload the review after sign-out/restart. Changed source bytes or method identity require recheck; an unanswered criterion cannot silently become a pass. Every accepted finding links to source context and its reviewer decision. |
| **3. Site quality — Site owner** | Audit and refine content hierarchy, copy, visual design, navigation, interaction states and responsiveness in the private Site source. Keep public-source contribution consent and access controls intact. | On the deployed revision, complete the full journey at desktop and physical-phone sizes. Run keyboard, focus, screen reader, 200% zoom and WCAG 2.2 AA checks; record actual results, screenshots and failures. Confirm production source and pinned-engine revisions by live readback. |
| **4. Multi-document case — engineering owner** | Connect a policy, contract, procedure, test, incident and remedy where supplied; retain each file's authority, date, version and provenance. Start after the single-document journey is sound. | A reviewer can follow a control across supplied records and see missing or contradictory links without the software claiming unseen records do not exist. Version changes never overwrite earlier evidence. |
| **5. Content and domain depth — research owner** | Complete the original EU Act assessment and source-fidelity gates in issue #93; maintain dated primary-source and role-specific crosswalks. Use a small number of real, fully scoped examples to improve explanations. | Every published source claim has an edition, passage and scope. Legal conclusions identify applicable actor, commencement and qualification or remain explicitly unresolved. |
| **6. Iterative user research — UX owner** | Observe policy owners and governance reviewers using the actual product; include participants with access needs. Revise the journey from observed errors. | Record task completion, wrong decisions, evidence-navigation errors, time, comprehension and satisfaction on a named build. Publish limitations and follow-up fixes. This is product research, not an independent accuracy study. |
| **7. Independent study — evaluation owner** | Later, freeze unfamiliar cases, independent reviewers, labels, baselines and metrics after the product and task definition stabilise. | The separate [research protocol](../review/2026-11-07-external-scholarly-critique-triage.md) governs any field-accuracy or comparative claim. No study result is presumed here. |

## Design and research rules

Usability concerns effectiveness, efficiency and satisfaction for specified
users, tasks and contexts, as framed by [ISO 9241-11](https://www.iso.org/standard/63500.html).
The [GOV.UK Service Manual](https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs)
calls for understanding the full user problem and testing assumptions early.
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) provides testable web accessibility
criteria. These sources guide design and tests; naming them does not establish
conformance.

Compare LAIF's workflow with the [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/),
the [ICO AI and data protection risk toolkit](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/ai-and-data-protection-risk-toolkit/)
and [AI Verify](https://www.imda.gov.sg/AI) for useful task patterns and evidence
handling. These instruments have different roles and authority. The product
hypothesis is that LAIF helps users connect a governance promise to exact source
language, accountable actors, records, uncertainty and a practical next action.
It remains a hypothesis until tested with intended users and appropriate evidence.

Keep document observations, software suggestions, authored conclusions, legal
interpretations and operational receipts visibly distinct. Show *unknown* when
the supplied material cannot support a conclusion. Never promote a synthetic
fixture, source hash, test count or attractive screen into proof of real-world
control effectiveness.
