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
