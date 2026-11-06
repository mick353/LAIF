# Frontier and autonomous AI: safety assurance extension

**Status:** optional diagnostic extension proposed 6 November 2026. This document
does **not** amend LAIF v1.2, the Compliance Toolkit v1.1, Schedule A, the
Coherence Test, the PDCA, LAIF-native certification, the existing assessment
engine, scoring, legal obligations or published assessments. It is not an
adopted standard, independent safety assessment, certification, or deployment
permission. Human semantic and policy review is required before incorporation
into a revised governance corpus.

## Purpose and problem statement

LAIF v1.2 already establishes Structural Honesty (§2.2), Structural Containment
(§2.3), prohibitions on oversight circumvention (C1), protection against
unjustified power concentration (B3), authorisation for substantially
irreversible actions (D1), operator duties (Part Four), and the PDCA (Part Nine).
These are governance *requirements*, not demonstrated technical capabilities.

An increasingly autonomous system can take unauthorised actions well before
its capabilities surpass human judgement across every relevant domain.
Consequently, a safety review must be triggered by **capability and exposure**,
not only broad intelligence, sector classification, user count, or a fixed
calendar interval. An operator's assurance statement, a policy document, and
an AI's self-report cannot prove externally effective containment.

The extension asks what **independently verifiable evidence** exists for:

1. dangerous capability evaluation and specific failure pathways;
2. restrictions enforced outside the model's control;
3. permission boundaries and prevention of unauthorised resource acquisition;
4. independent intervention, safe interruption and recovery;
5. oversight integrity, incident escalation and change-triggered retesting;
6. accountable release decisions and continuing human authority.

This is not a prediction that catastrophic AI loss of control has occurred.
See the [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/2026-report-executive-summary)
and [UK AI Security Institute's frontier evaluations](https://www.aisi.gov.uk/frontier-ai-trends-report)
for the current evidence and limitations. Those are external research sources,
not LAIF-verified-corpus assessment artifacts.

## When an operator should use the review

Proposed triggers for *additional human safety review*, without inventing a
universal numerical threshold:

- training or release of a highly capable general-purpose model;
- enabling tool use, long-running tasks, autonomous planning, internet access,
  access to credentials, code execution, cloud compute, money, or external APIs;
- credible observations of harmful cyber or biological assistance, model-weight
  exfiltration, replication, unapproved privilege changes, or deceptive behaviour;
- material changes to weights, tuning, policies, system prompts, plugins,
  external tools, model-routing, monitoring or operating environment;
- observed evasion of evaluations, independent oversight or containment;
- planned release of model weights or other actions that are hard to reverse.

Risk owners must define their own documented *testable* thresholds and time
limits, supported by relevant external evidence and independent review. The
checker does not infer whether a model is frontier-level or automatically
classify its systemic-risk status under any law. Absence of evidence is a hold
for review, not evidence of safety. Waiting twelve months after a new dangerous
capability emerges is not a substitute for a pre-release gate.

## Risk and control coverage

The first diagnostic schema explicitly requires six risk families. Their
inclusion is a coverage control, **not** a claim that the taxonomy is complete.
Each evaluation needs a method and version, observed decision, independently
recorded reviewer, timestamps, model-revision binding and a hash-pinned test
report. `BLOCKING` and `INCONCLUSIVE` both prevent review readiness.

| Capability risk | Adversarial evaluation question | Relevant LAIF provisions |
|---|---|---|
| `cyber_misuse` | Can it materially assist or undertake harmful cyber activity under tested conditions? | B1 where applicable, C1, D1, §2.3 |
| `chemical_biological_misuse` | Could it lower barriers to mass-casualty harm? | B1, Coupling, D1 |
| `autonomous_replication` | Can it obtain resources, copy itself or maintain unauthorised persistence? | §2.3, C1, B3, D1 |
| `oversight_deception` | Can it conceal objectives, evade evaluation or misrepresent its actual actions? | §2.2, C1, C2, Part Four |
| `model_exfiltration` | Can it expose model weights, credentials or sensitive systems? | §2.3, C1, D1 |
| `persuasion_at_scale` | Can it manipulate people or institutions contrary to their interests? | A1, A2, B3, C3 |

The extension also requires seven distinct control-evidence mappings:
`tool_authorisation`, `credential_isolation`, `network_egress`,
`independent_interrupt`, `oversight_integrity`, `harmful_use_gating`, and
`incident_response`. Reusing one generic control record to claim all seven
protections is rejected. Each must tie to an existing LAIF strict assurance
control with positive AND negative execution receipts plus operational review.

Containment must be enforced outside the model (`infrastructure` or
`supervised_host`), and independent interruption specifically at the
`infrastructure` boundary. A claim that a model *promises* to stop is not
technical proof it can be stopped. Infrastructure-layer controls themselves
still need independent penetration tests and fault-injection tests in the real
deployment environment, not only hash-pinned self-reported records.

## Evidence-bounded executable workflow

The optional standard-library CLI is:

```bash
python3 scripts/laif_frontier_assurance.py /private/frontier/frontier.json --require-review-ready
python3 scripts/laif_frontier_assurance.py /private/frontier/frontier.json --as-of 2026-11-06T12:00:00Z
python3 tests/test_frontier_assurance.py
```

Use an explicit `--as-of` for reproducible historical review. Without it, the
checker uses the current UTC time to catch overdue reviews. It does not
connect to a deployed AI, create accounts, call paid APIs or run GitHub Actions.
All paths are relative to the private manifest directory and must stay within
it. Keep actual operational data and sensitive attack material out of GitHub.

The top-level manifest is `laif.frontier-assurance.v1`. This compact shape is
**illustrative**; hashes are placeholders, and the example is not executable
until genuine evidence files are supplied:

```json
{
  "schema": "laif.frontier-assurance.v1",
  "deployment_id": "a-specific-deployment",
  "model_revision": "an-immutable-model-revision",
  "last_material_change_at_utc": "2026-11-03T08:00:00Z",
  "review_due_at_utc": "2026-12-03T08:00:00Z",
  "core_manifest": {"file": "core.json", "sha256": "<64 lowercase hex characters>"},
  "operational_annex": {"file": "operations.json", "sha256": "<64 lowercase hex characters>"},
  "threat_register": {"file": "threats.json", "sha256": "<64 lowercase hex characters>"},
  "capability_evaluations": [
    {"category": "cyber_misuse", "receipt_file": "cyber-evaluation.json",
     "receipt_sha256": "<64 lowercase hex characters>"}
  ],
  "control_map": [
    {"category": "tool_authorisation", "control_id": "tool-authz",
     "enforcement_boundary": "infrastructure"}
  ],
  "decision_receipt": {"file": "release-decision.json", "sha256": "<64 lowercase hex characters>"}
}
```

The example above deliberately omits other required evaluation and control
categories: as written, it will not meet the strict review-ready threshold.
See `RISK_CATEGORIES` and `CONTROL_CATEGORIES` in the checker for the complete
schema v1 coverage. The companion `core.json` must contain
`deployment_id`, `model_revision`, a source inventory, scope attestation, all
mapped control IDs, and positive/negative action receipts. Every action receipt
must identify the same deployment and model revision. The
`laif.operational-annex.v1` must provide reviewed staging or production
records for every mapped control, also bound to that model revision.

The threat register is a JSON object with `deployment_id`, `model_revision`,
`owner`, independent `reviewer`, `reviewed_at_utc`, and a `risks` array covering
each of the six categories. Every risk entry requires `category`,
`protected_interest`, `failure_pathway`, `control_owner`, `trigger`,
`stop_condition`, and `test_method`. This binds the risk to the public or human
interest it protects rather than merely listing risk terminology.

Each capability evaluation points to a SHA-256-pinned **JSON receipt** with:
`deployment_id`, `model_revision`, `category`, `run_id`, `method_id`,
`toolchain_version`, `environment` (`staging` or `production` for readiness),
`evaluator`, a different `reviewer`, `executed_at_utc`, `reviewed_at_utc`,
`decision` (`CLEAR`, `BLOCKING` or `INCONCLUSIVE`), and a nested `test_report`
reference containing `file` and `sha256`. The test report JSON must corroborate
`run_id`, `model_revision` and `decision`. Report evidence remains supplied,
not independently authenticated; a `CLEAR` label does not establish a safe
model. All assessments must follow the declared last material change.

The SHA-256-pinned decision receipt must contain `deployment_id`,
`model_revision`, `decision` (`RELEASE`, `CONDITIONAL` or `HOLD`), `approver`
(distinct from the test evaluator and operational executor), and
`approved_at_utc` after the recorded evaluations and control evidence. This
checker never *makes* the release decision or validates the decision-maker's
legal authority.

### Result interpretation and precedence

| Result | Meaning |
|---|---|
| `BLOCKING_FINDING` | A supplied capability evaluation records a blocking or inconclusive result. A release label cannot override it. |
| `EVIDENCE_INCOMPLETE` | Required evidence is absent, stale, inconsistent, unbound, simulation-only or does not satisfy strict core checks. |
| `RELEASE_HELD` | Complete records are present but the human decision is `HOLD` or `CONDITIONAL`. |
| `REVIEW_READY` | All **supplied and checked** documentary conditions are met and a human release decision is recorded. **Not** certification or permission to deploy. |

The tool flags obvious tampering, missing categories, future-dated or obsolete
records, reuse of generic evidence, self-attested interruption, model-revision
mismatch, positive/negative receipt contradictions and a release decision that
predates testing. It cannot independently discover omitted evidence, verify
the physical system state, authenticate people or logs, establish test
representativeness, or certify a claimed `CLEAR` outcome. These are deliberate
trust boundaries, not features to obscure with a high numeric score.

## Operational safety case still required

To move from evidence readiness to credible assurance, a genuine deployment
requires more than this local software:

1. An independently scoped threat model including deployment context,
   downstream systems and potential third-party impacts.
2. Properly isolated test environments, independent capability evaluations,
   adversarial probes and counter-evidence, with known coverage limits.
3. Infrastructure-enforced permissions, denied-by-default egress and resource
   controls, credential boundaries, and out-of-band intervention mechanisms.
4. Evidence that interruption remains effective under loss of connectivity,
   long-running tasks, tool failures, partial compromise and operator error.
5. A defined owner authorised to stop deployment, escalation clocks,
   incident handling, rollback where possible and post-incident reassessment.
6. A cross-functional human release record and independently retained
   operational evidence, including further tests after material changes.

Preserve a safe and recoverable path for legitimate permitted actions; an
always-blocking control can fail the positive tests just as an always-allowing
control fails the negative tests. Never publish sensitive test payloads or
operational credentials to obtain an apparently complete evidence package.

## Regulatory and governance boundaries

The EU AI Act's Article 55 separately requires certain systemic-risk model
providers to evaluate models, assess and mitigate risk, report serious
incidents and protect cybersecurity. This extension provides **candidate
evidence categories**, not conformity with Article 55, a notified-body
approval, regulator acceptance or a legal safe harbour. See the separately
maintained [current-authority crosswalk](../regulatory/CURRENT_AUTHORITY_CROSSWALK_2026-11.md).

The Coherence Test and self-application remain necessary: exceptional controls
must protect identifiable interests, apply proportionately across comparable
actors, retain human contestation and review, and be revisable with evidence.
This diagnostic layer is deliberately opt-in. If later adopted into the LAIF
governance corpus, that is a **separate semantic-sensitive decision** requiring
human review, DOCX/TXT parity and explicit revision of appropriate schedules.
