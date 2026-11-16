# LAIF product and Site readiness

**Reading this programme today:** the dated checkpoints below are historical.
Use [Current verified state](../verification/CURRENT.md) for later release and
acceptance evidence. Browser instructions are in [Getting started](../GETTING_STARTED.md);
commands are in [Local setup](../LOCAL_SETUP.md). The Site accepts PDF, Markdown
and text; Word input in this programme applies to the local toolkit, or requires
export to a supported format before Site intake.

**Working programme — 14 November 2026.** Owner: LAIF delivery lead. Baseline:
`main` at `975e39cb6cfa24da440253364cad5b8f13f69b54`. This is a delivery
record and research plan, not a claim that the product or Site has passed the
acceptance checks below. Recheck GitHub, the private Site source and production
before using this record as a current status report.

**15 November checkpoint:** GitHub and Windows `main` match at `7eec1a5`.
[Issue #110](https://github.com/mick353/LAIF/issues/110) records the merged
guided local start (PR #112) and the owner-private Research Workspace deployed
at Site v10. The local full gate passed 605 tests with two skips on the exact
PR #112 candidate, followed by merged-tree and quick readback. Site v10 source,
storage/API, type and build checks passed, and deployment readback succeeded.
These checks do not supply an observed signed-in save/reload or complete Site
intake-to-export session. Browser, phone and assistive-technology acceptance
remain open. [Issue #93](https://github.com/mick353/LAIF/issues/93) retains the
source and legal gates, including the limited NIST PDF fidelity result, DTAC
upstream byte identity and full EU Act assessment. Recheck both issues and the
deployed build before reporting a later status.

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
| Review workflow | [Local setup](../LOCAL_SETUP.md) describes document commands, authored eight-criterion JSON review and the separate neutral research path. [Getting started](../GETTING_STARTED.md) covers the browser journey. | Observe intended users completing mode, scope, extraction, finding decisions, save/resume and export. Confirm that source changes invalidate stale reviews. |
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

## Owner-journey acceptance matrix

Use this matrix for the **current product release**, before any external
accuracy study. The owner must test the exact local revision and deployed Site
version, record the device/browser and supplied source, and preserve screenshots
or a redacted interaction record. A source check, unit test, build, deployment
receipt and observed user journey are separate evidence types.

| Priority / owner | Scenario on the current release | Observable pass condition | Evidence to retain |
| --- | --- | --- | --- |
| **P0 — product owner** | A first-time policy owner opens the private Site, tries the synthetic sample, then reviews an unfamiliar authorised document. | Without a command reference, the owner can identify the task and document scope, inspect extraction, open the supporting passage for each proposed finding, decide *accept*, *reject*, *needs evidence* or *outside scope*, save, reopen and export a readable report plus review record. They can say which statements are source observations and which are LAIF suggestions. | Named build; observed steps, time, wrong turns and comprehension questions; final report and review record. A facilitator must not silently complete steps for the owner. |
| **P0 — Site owner** | Sign in, edit a review, save, sign out/reload, resume and export; repeat after a failed or conflicting save. | Visible saved/pending/failed state matches server readback; no decision silently disappears; retry, conflict resolution and backup export work; stale source or method identity returns decisions to unresolved. | Live owner-only session, exact deployment/source revision, redacted before/after records and failure receipts. |
| **P0 — extraction owner** | Use each format the path advertises (local text, Word and searchable PDF; Site-supported text and PDF), then try an image-only, damaged, empty or partly extracted file. | Original file and extracted-text identities and extractor/version are visible. The owner checks source coverage before decisions. Warnings specify the limit and a recovery action; the interface does not turn missing or corrupted text into a confident omission finding. | Input type and permitted fixture, byte/text hashes, preview, warning and recovery outcome. |
| **P0 — source custodian** | Open a finding and its source citation, including an edition with qualified provenance or a stale catalogue fallback. | The user can navigate to exact quoted context, distinguish official source, locally verified bytes and proposal status, and see edition, date, excerpt coverage, retrieval and unresolved origin where applicable. Catalogue refresh cannot imply that the pinned engine or legal interpretation changed. | Source/citation status, source hash, passage location, catalogue and engine versions, recorded discrepancy or missingness. |
| **P0 — legal/research reviewer** | Review a purported law or framework conclusion. | The report distinguishes binding authority, LAIF method and software diagnostic; names jurisdiction, actor, source edition, operative date, exception and relevant passage or explicitly says unresolved. An absent statement in one document is not a legal-breach finding. NIST table matches and DTAC's unresolved upstream identity retain their published limits. | Reviewed claim with primary passage and applicability note; explicit human disposition and limits. |
| **P0 — privacy/access owner** | Add a private document, export a contribution package and attempt an unauthorised visit. | The owner sees where the input and report are stored, what an export would publish, and a deliberate acknowledgement before public-source contribution. Owner-only access and cross-origin/anonymous rejection are confirmed on the live release; no confidential bytes appear in public GitHub. | Access readback, redacted storage/export inspection and publication acknowledgement. |
| **P0 — accessibility owner** | Complete the same journey by keyboard and screen reader, at 200% zoom and on a physical phone. Include upload, source comparison, decision controls, save status, errors and export. | Focus order and visible focus make sense; controls have names and states; errors are identified in text; content reflows without loss; evidence, decisions and save status remain perceivable and operable. Evaluate against relevant WCAG 2.2 AA criteria; automated checks alone do not establish conformance. | Device, browser, assistive technology, WCAG criterion mapping, observed failures, fixes and retest on deployed version. |
| **P1 — UX owner** | Observe intended policy owners and governance reviewers, including a participant with access needs, completing the journey without coaching. | Record completion, incorrect dispositions, source-navigation mistakes, recovery, effort and satisfaction by participant and build; fix severe confusion and repeat the affected tasks. No universal usability or accuracy percentage follows from a small formative sample. | Task script, consented observations, anonymised results, issue links and retest. |
| **P2 — engineering owner** | Link supplied policy, procedure, contract, test and incident records after the one-document path is sound. | Reviewers can follow each documented relationship, date and version; a missing link says *not supplied* or *not found in supplied records*, with contradictory evidence preserved. | Versioned source graph and reviewed examples, including missing and conflicting links. |

**Release decision:** keep issue #110 open until every P0 row has an observed
pass on each applicable path and the named deployed build, and P1 intended-user
acceptance has recorded results and resolved blocking defects.
Record each unmet row with an owner and next action. Issue #93 separately owns
source/legal completion; its open gates must remain visible in product copy.

## Design and research rules

Usability concerns effectiveness, efficiency and satisfaction for specified
users, tasks and contexts, as framed by [ISO 9241-11](https://www.iso.org/standard/63500.html).
[ISO 9241-210](https://www.iso.org/standard/77520.html) frames human-centred
design across the interactive system's lifecycle. For the Site, use
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) as the detailed accessibility test
reference and [W3C's evaluation guidance](https://www.w3.org/WAI/test-evaluate/)
to combine checks with human assessment. The Australian Digital Transformation
Agency's [Know your user criterion](https://www.digital.gov.au/policy/digital-experience/digital-service-standard/criterion-2)
is a useful local analogy for observing tasks and revising the journey. Its
Digital Service Standard is Australian Government digital-service policy and
does not apply to this private LAIF research Site by itself. The
[GOV.UK Service Manual](https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs)
is likewise optional comparative public-service guidance. LAIF's users,
source-review task and governance boundaries determine the actual acceptance
cases above. Naming any of these sources does not establish conformance.

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
