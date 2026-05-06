# Merge Policy

This policy defines merge expectations for LAIF repository changes. It is intended to keep ordinary maintenance, provenance work, semantic changes, and assessment artifact updates separate and auditable.

## Merge Readiness Expectations

A pull request is ready for merge when:

- its purpose is clear and focused;
- required validation commands have passed or skipped commands are explained;
- CI checks for the branch have passed when available;
- LAIF semantic impact has been disclosed;
- protected assessment artifacts have not changed unintentionally;
- reviewers understand whether the change is documentation/provenance-only or governance-sensitive.

## Current Governance Status

The current baseline includes Phase 3A governance stabilization and Phase 3B deterministic governance test coverage. The CI governance job gates the validation, adversarial, and real-world jobs, so downstream assessment jobs depend on governance completing successfully.

This governance lifecycle separates blocking and advisory behavior:

- governance config validation is blocking and enforces that configured paths exist;
- protected-artifact checks are blocking when configured protected artifacts drift;
- semantic-boundary checks are advisory-only and identify semantic-sensitive changes for reviewer attention;
- governance helper/check files are semantic-sensitive infrastructure and should be reviewed with the same discipline as other repository behavior that affects governance classification.

These controls safeguard repository process. They do not alter LAIF assessment scoring, detector logic, interpretation logic, published assessment conclusions, or external legal status.

## CI Expectations

CI is expected to run the governance job before the repository validation and test suites. Pull requests should also be validated locally before review with:

```bash
python3 -m py_compile scripts/governance/*.py
python3 scripts/governance/check_governance_config.py
python3 scripts/governance/check_protected_artifacts.py
python3 scripts/governance/check_semantic_boundaries.py
python3 tests/test_governance.py
python3 validate.py
python3 validate.py --verified-corpus
python3 validate.py --check-evidence-traces
python3 test_adversarial.py
python3 test_real_world.py
```

A passing CI run does not by itself approve semantic changes. It confirms that the automated checks completed successfully.

## Reviewer Expectations

Reviewers should verify:

- the diff matches the stated purpose;
- validation results are reported accurately;
- semantic-sensitive changes are disclosed;
- protected artifacts are not modified unless intentionally reviewed;
- documentation/provenance changes do not make new semantic claims beyond the change scope.

Human reviewers remain authoritative for semantic approval decisions.

## Semantic-Sensitive Review Expectations

Changes to scoring logic, detector logic, interpretation logic, canonical LAIF terminology, assessment inputs, or assessment artifacts require dedicated semantic review.

A semantic-sensitive pull request should explain:

- what behavior or meaning changes;
- why the change is needed;
- which files contain the change;
- whether assessment outputs are expected to change;
- which validation commands were run;
- whether any report regeneration is proposed.

## Dedicated Semantic-Change Pull Requests

Do not mix semantic-sensitive changes with unrelated formatting, provenance, CI, or documentation cleanup. Dedicated semantic-change pull requests should be narrow enough that reviewers can inspect the full semantic effect.

Examples of changes that should be isolated:

- scoring threshold changes;
- detector pattern changes;
- verdict calculation changes;
- interpretation-layer mapping changes;
- assessment artifact updates.

## Squash Merge Preference Rationale

When maintainers choose squash merge for an ordinary pull request, the rationale is that one accepted change maps to one auditable commit. This can simplify rollback and provenance review.

The repository's active branch policy and maintainer decision remain controlling for the final merge method. For large semantic or assessment-artifact changes, maintainers may choose a different merge strategy if preserving individual commits is necessary for audit, but that should be intentional.

## Fresh-Branch Discipline

After each merge, contributors should reset to the latest `origin/main`, create a fresh phase branch, and verify `git rev-list --left-right --count HEAD...origin/main` reports `0	0` before edits. Before opening a pull request, verify the branch is ahead-only and that `git diff --name-only origin/main...HEAD` lists exactly the intended files.

Never reuse stale pull-request branches. Stale or contaminated pull requests should be closed and ignored, then replaced from a clean branch based on the current `origin/main`.

## Rollback Philosophy

Rollback should be simple and conservative:

- revert unintended artifact drift rather than editing around it;
- revert a bad semantic change before adding new corrective behavior;
- isolate governance fixes in governance-only pull requests;
- avoid combining rollback with unrelated improvements.

## No Automatic Semantic Approval

Automated checks can identify failures or likely-sensitive changes, but they do not approve LAIF meaning. Human reviewers remain responsible for deciding whether a semantic-sensitive change is acceptable.
