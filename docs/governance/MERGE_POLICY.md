# Merge Policy

This policy defines merge expectations for LAIF repository changes. It is intended to keep ordinary maintenance, provenance work, semantic changes, and assessment artifact updates separate and auditable.

## Merge Readiness Expectations

A pull request is ready for merge when:

- its purpose is clear and focused;
- required validation commands have passed or skipped commands are explained;
- the applicable local verification checks have passed, or every omission is disclosed;
- LAIF semantic impact has been disclosed;
- protected assessment artifacts have not changed unintentionally;
- reviewers understand whether the change is documentation/provenance-only or governance-sensitive.

## Local Verification Expectations

GitHub Actions is not part of the active merge gate. The legacy workflow does not trigger for pushes or pull requests. From the repository root run:

```bash
python3 scripts/laif_verify.py --full --base-ref origin/main
```

This verifies governance paths, protected-artifact diff, semantic-boundary advisory, corpus, source formats, adversarial and semantic tests, document processing, report generation and committed-report drift. Run `python3 scripts/laif_verify.py` for a targeted checkpoint. Disclose unrun checks; an old CI badge is not proof of current validation.

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

## Local Governance Merge Lifecycle

Phase 3 governance tests remain deterministic, but they run locally or in an operator-controlled environment rather than GitHub Actions. First compile and validate governance config, then test protected artefact drift against an explicit base ref and run semantic-boundary advisory checks. Continue with validation, adversarial, provenance and report checks only after those succeed. Protected artefact drift is blocking; semantic-boundary detection is advisory and requires reviewer judgement.

## Stale Branch and Contamination Discipline

After each merge to `main`, start follow-up work from the latest `origin/main`:

1. `git fetch origin main --prune`
2. create a fresh phase branch from `origin/main`
3. reset hard to `origin/main`
4. verify `git rev-list --left-right --count HEAD...origin/main` reports `0 0` before edits
5. verify the branch is ahead-only before PR review
6. verify `git diff --name-only origin/main...HEAD` lists exactly the intended files

Never reuse stale PR branches for a new phase. Stale or contaminated PRs must be closed and ignored. Do not use "Copy git apply" from a contaminated branch, because the copied patch carries the contaminated diff into the fresh branch.
