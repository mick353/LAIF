# Protected Artifacts

Protected artifacts are repository files that record assessment conclusions or evidentiary outputs. They require stricter review than ordinary documentation because accidental edits can change the public record of an assessment.

## Protected Artifact Philosophy

Protected artifacts should be stable, traceable, and reviewable. They should not change as a side effect of documentation cleanup, CI maintenance, provenance metadata work, or local test execution.

Protection does not mean the files can never change. It means changes must be intentional, isolated, and reviewed for their assessment effect.

## Ordinary Documentation vs Assessment Artifacts

Ordinary documentation explains how to use or understand the repository. Examples include README material, contribution guidance, governance procedures, and manual ingestion instructions.

Assessment artifacts record assessment findings, conclusions, or evidence outputs. They are closer to a published record than to general documentation.

The distinction matters because ordinary documentation can be clarified without changing assessment results, while artifact edits may alter the recorded outcome or evidentiary basis of an assessment.

## Configured Protected Artifact Scope

The configured protected artifact is:

- `reports/laif_full_assessment.md`

This file records the full corpus assessment. Do not edit or regenerate it in ordinary pull requests. Governance config validation also enforces that configured protected-artifact paths exist, so a missing configured path is a governance configuration failure rather than an assessment revision.

The protected-artifact check is blocking when configured protected artifacts drift. This blocking status does not mean artifacts can never change; it means intentional changes must use a dedicated assessment-artifact review path.

## Expected Handling

If a pull request does not intentionally change an assessment artifact, it should leave protected artifacts unchanged.

If a protected artifact changes accidentally:

1. Revert the artifact file.
2. Re-run validation if applicable.
3. Confirm the artifact is absent from the final diff.
4. Note the correction in the pull request if reviewers need context.

If a protected artifact must change intentionally:

1. Use a dedicated assessment-artifact pull request.
2. Explain why the artifact is changing.
3. Explain the source inputs and process used to produce the change.
4. Run applicable validation commands.
5. Request review focused on assessment impact.

## Future Optional Protections

Maintainers may later choose to protect additional files, such as generated real-world reports, verified raw corpus files, evidence trace files, or artifact hash records. Those are informational possibilities only. They are not active policy unless separately adopted in the governance configuration.

## Human Review

Human reviewers remain responsible for approving assessment artifact changes. Repository documentation can define expectations, and future automation may detect drift, but automation should not approve assessment conclusions by itself.
