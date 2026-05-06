# Rollback and Recovery

This document describes recovery procedures for accidental artifact changes, CI failures, governance mistakes, and semantic drift. The goal is to restore a clear repository state with minimal additional change.

## General Recovery Principles

- Prefer narrow reverts over broad rewrites.
- Preserve evidence of what changed and why.
- Do not combine rollback with unrelated cleanup.
- Separate governance fixes from semantic fixes.
- Re-run applicable validation after recovery.

## Accidental Protected Artifact Modification

Initial protected artifact:

- `reports/laif_full_assessment.md`

If this file changes unintentionally:

1. Revert only the protected artifact file.
2. Confirm it is no longer in the diff.
3. Re-run applicable validation commands.
4. State in the pull request that accidental artifact drift was reverted.

Do not edit the artifact manually to approximate its prior state. Use version control to restore the exact prior content.

## Intentional Protected Artifact Change

If an assessment artifact must change:

1. Stop ordinary review of the mixed pull request.
2. Open or split into a dedicated assessment-artifact pull request.
3. Document the reason for the artifact change.
4. Document the inputs and process used to produce the artifact.
5. Request review focused on assessment impact.

## CI Failures

When CI fails:

1. Identify the failing command or job.
2. Reproduce locally if possible.
3. Determine whether the failure is caused by the proposed change, environment assumptions, or existing repository state.
4. Apply the smallest fix that addresses the failure.
5. Re-run the failed command and any related validation.

Do not weaken validation to make a failure pass unless the pull request is dedicated to changing validation behavior and receives semantic review where appropriate.

## Bad Governance Checks

Future governance checks may produce false positives or block legitimate work. If that happens:

1. Confirm the failure mode and affected files.
2. Avoid changing LAIF semantic logic as part of the governance fix.
3. Open a governance-only corrective pull request when possible.
4. Narrow the check or clarify documentation instead of disabling broad protections.
5. Re-run CI after the governance fix.

Phase 2A does not add enforcement scripts, but these procedures define how later governance tooling should be repaired if needed.

## Semantic Drift Mistakes

If a change is discovered to have altered LAIF semantics, scoring logic, detector logic, interpretation logic, or assessment artifacts unintentionally:

1. Revert the change if possible.
2. Confirm validation behavior has returned to the prior expected state.
3. Open a dedicated corrective pull request if a replacement change is still needed.
4. Explain the drift and the correction in the pull request.
5. Request semantic review for the corrective change.

## Revert Workflow

Preferred revert workflow:

1. Identify the commit or file-level change to revert.
2. Revert the smallest necessary scope.
3. Run relevant validation commands.
4. Confirm no unrelated files changed.
5. Commit the revert with a descriptive message.

For squash-merged pull requests, reverting the single squash commit is usually the cleanest recovery path.

## When to Open Dedicated Corrective PRs

Open a dedicated corrective pull request when:

- a semantic-sensitive change needs replacement rather than simple removal;
- an assessment artifact must be regenerated or corrected;
- governance documentation or future governance checks need adjustment;
- a CI failure reveals a repository-wide assumption that should be documented.

## Governance Rollback Philosophy

Governance exists to make sensitive changes visible and reviewable. If governance itself causes problems, fix the governance layer narrowly. Do not use governance failures as a reason to weaken semantic review or protected artifact discipline.
