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

## CI Expectations

The existing Phase 1 CI workflow is expected to run the repository validation and test suites. Pull requests should also be validated locally before review with:

```bash
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

## Rollback Philosophy

Rollback should be simple and conservative:

- revert unintended artifact drift rather than editing around it;
- revert a bad semantic change before adding new corrective behavior;
- isolate governance fixes in governance-only pull requests;
- avoid combining rollback with unrelated improvements.

## No Automatic Semantic Approval

Automated checks can identify failures or likely-sensitive changes, but they do not approve LAIF meaning. Human reviewers remain responsible for deciding whether a semantic-sensitive change is acceptable.

## Phase 3 Governance Merge Lifecycle

Phase 3A governance stabilization and Phase 3B deterministic governance test coverage have been merged. The active CI lifecycle is:

1. Run the governance job.
2. Compile governance helper/check files.
3. Validate the governance path configuration.
4. Run protected-artifact drift detection.
5. Run semantic-boundary advisory detection.
6. Run the deterministic governance test suite.
7. Allow downstream validation, adversarial, and real-world jobs to run only after governance succeeds.

Protected-artifact detection is blocking: a configured protected artifact in the pull-request diff must be reverted or intentionally handled in a dedicated assessment-artifact pull request before merge.

Semantic-boundary detection is advisory-only. It highlights configured semantic-sensitive files or configured exact-term hunk matches for reviewer attention, but it does not issue a semantic verdict and does not block merge by itself.

Governance config validation is blocking for malformed configuration, missing required keys, duplicate or invalid entries, non-repository-relative paths, and configured path entries that do not exist. Governance helper/check files are themselves semantic-sensitive because changing them can change how repository-governance signals are generated.

## Stale Branch and Contamination Discipline

After each merge to `main`, start follow-up work from the latest `origin/main`:

1. `git fetch origin main --prune`
2. create a fresh phase branch from `origin/main`
3. reset hard to `origin/main`
4. verify `git rev-list --left-right --count HEAD...origin/main` reports `0 0` before edits
5. verify the branch is ahead-only before PR review
6. verify `git diff --name-only origin/main...HEAD` lists exactly the intended files

Never reuse stale PR branches for a new phase. Stale or contaminated PRs must be closed and ignored. Do not use "Copy git apply" from a contaminated branch, because the copied patch carries the contaminated diff into the fresh branch.
