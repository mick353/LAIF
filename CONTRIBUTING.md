# Contributing to LAIF

This repository contains framework texts, assessment tooling, verified-source provenance records, and published assessment artifacts. Contributions must keep those layers separate so that documentation updates do not accidentally alter LAIF semantics, scoring, detector behavior, interpretation logic, or assessment artifacts.

## Contribution Workflow

1. Start from the current repository state and keep changes focused.
2. Prefer small pull requests with one clear purpose.
3. Run the local validation commands listed below before requesting review.
4. Explain whether the change is documentation/provenance-only or governance-sensitive.
5. Do not regenerate or edit assessment artifacts unless the pull request is dedicated to that purpose and reviewers have agreed to review it as an assessment-artifact change.

## Required Local Validation Commands

Run these commands from the repository root before marking a pull request ready for review:

```bash
python3 validate.py
python3 validate.py --verified-corpus
python3 validate.py --check-evidence-traces
python3 test_adversarial.py
python3 test_real_world.py
```

If a command cannot be run, state which command was skipped and why. Do not describe skipped checks as passing.

## Pull Request Expectations

Every pull request should describe:

- files changed and why;
- validation commands run and their results;
- whether LAIF semantics changed;
- whether scoring logic changed;
- whether detector logic changed;
- whether interpretation logic changed;
- whether assessment artifacts changed;
- whether reports or generated artifacts were regenerated.

The expected answer for ordinary documentation, provenance, and CI-maintenance pull requests is that LAIF semantics, scoring logic, detector logic, interpretation logic, and assessment artifacts are preserved.

## Documentation and Provenance Updates

Documentation/provenance updates include changes such as:

- clarifying repository instructions;
- adding provenance notes or manifest metadata;
- documenting manual ingestion procedures;
- updating CI or validation instructions without changing validation behavior;
- improving formatting or navigation in non-assessment documentation.

These changes should not alter scoring, detector behavior, interpretation rules, or published assessment conclusions.

## Governance-Sensitive Semantic Changes

Governance-sensitive changes include changes to:

- LAIF semantic definitions or canonical terminology;
- scoring logic, thresholds, weights, or verdict calculations;
- detector logic for Coherence Test, Integrity Layer, paraphrase, evidence trace, or corpus validation checks;
- interpretation logic that maps findings to conclusions, readiness labels, or compliance outcomes;
- assessment artifacts that record published conclusions.

Governance-sensitive changes should be isolated in dedicated pull requests. They require explicit review of the semantic effect, not only a passing test run.

## Protected Artifact Awareness

The initial protected assessment artifact is:

- `reports/laif_full_assessment.md`

Treat this file as a recorded assessment artifact, not ordinary documentation. Do not edit or regenerate it as part of routine documentation, provenance, or CI work. If an assessment artifact must change, use a dedicated pull request that explains why the artifact is changing and how it was produced.

## Merge Expectations

A pull request should not be merged until:

- applicable local checks and CI checks pass;
- reviewers understand the scope of the change;
- any semantic-sensitive changes have received dedicated review;
- protected assessment artifacts have not drifted unintentionally;
- the pull request description accurately discloses validation results and semantic impact.

When maintainers choose squash merge for an ordinary pull request, the rationale is to keep each accepted change auditable as one logical unit. The repository's active branch policy and maintainer decision remain controlling for the final merge method.

## Governance Philosophy

Repository governance should be deterministic, auditable, and conservative. Controls should identify sensitive changes and require human review; they should not attempt to infer or approve LAIF semantics automatically. Automation may help detect drift, but human reviewers remain responsible for semantic approval decisions.

## Fresh-Branch Governance Workflow

After every merge to `main`, contributors should restart governance work from the latest `origin/main` state instead of continuing on an old pull-request branch. A safe Codex/GitHub workflow is:

1. Fetch and prune the latest main branch: `git fetch origin main --prune`.
2. Create a fresh phase branch from `origin/main`.
3. Reset the worktree hard to `origin/main` before making edits.
4. Confirm `git rev-list --left-right --count HEAD...origin/main` reports `0 0` before edits.
5. Make only the intended changes for that pull request.
6. Before requesting review, confirm the branch is ahead-only relative to `origin/main` and inspect `git diff --name-only origin/main...HEAD` for the exact intended diff.

Never reuse stale pull-request branches for later phases. Stale or contaminated pull requests should be closed and ignored for future work. Do not use GitHub's "Copy git apply" flow from a contaminated branch; applying that patch carries the contaminated diff into the new branch.

## Current Governance Lifecycle

Phase 3A governance stabilization and Phase 3B deterministic governance test coverage have both been merged. The CI governance job now runs before, and gates, the downstream validation, adversarial, and real-world jobs.

The governance lifecycle is intentionally conservative:

- protected-artifact checks are blocking when configured protected artifacts appear in the pull-request diff;
- semantic-boundary checks are advisory-only and warn reviewers without blocking merge;
- governance config validation enforces that configured path entries exist in the repository;
- governance helper/check files are semantic-sensitive and should receive focused review when changed;
- downstream validation, adversarial, and real-world CI jobs depend on the governance job.

The Phase 3B test suite in `tests/test_governance.py` validates the shared governance helpers, config behavior, protected-artifact behavior, and advisory semantic-boundary behavior using `tests/governance_fixtures/valid_config.json`.

These governance tests do not change LAIF assessment scoring, detector semantics, interpretation logic, or assessment conclusions.
