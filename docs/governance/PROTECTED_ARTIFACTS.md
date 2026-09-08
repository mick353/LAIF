# Protected Artifacts

Protected artifacts are repository files that record assessment conclusions or evidentiary outputs. They require stricter review than ordinary documentation because accidental edits can change the public record of an assessment.

## Protected Artifact Philosophy

Protected artifacts should be stable, traceable, and reviewable. They should not change as a side effect of documentation cleanup, CI maintenance, provenance metadata work, or local test execution.

Protection does not mean the files can never change. It means changes must be intentional, isolated, and reviewed for their assessment effect.

## Ordinary Documentation vs Assessment Artifacts

Ordinary documentation explains how to use or understand the repository. Examples include README material, contribution guidance, governance procedures, and manual ingestion instructions.

Assessment artifacts record assessment findings, conclusions, or evidence outputs. They are closer to a published record than to general documentation.

The distinction matters because ordinary documentation can be clarified without changing assessment results, while artifact edits may alter the recorded outcome or evidentiary basis of an assessment.

## Initial Protected Artifact Scope

## What is protected, and what deliberately is not

Two kinds of artifact live in `reports/`, and only one kind can be protected by
a path-level hard fail.

**Protected — the narrative analyses.** Authored assessments that record
conclusions at a date. They are a published record: nothing should change them
as a side effect of other work, and an intentional change belongs in its own
pull request with an explanation. These are the protected artifacts.

**Deliberately not protected — the generated assessments.**
`reports/laif_real_world_assessment.md`, `reports/laif_executive_summary.md` and
`reports/laif_assessment_data.json` are a deterministic function of the corpus
and the engine, and each carries a corpus fingerprint and a toolchain
fingerprint. They *must* change whenever detection or reporting changes — CI
fails if the committed copies do not match regenerated output. A path-level
protection on them would block every legitimate engine change while adding no
safety, because their integrity is already established by regeneration rather
than by immutability.

The distinction is the same one the framework applies to other people's
documents: a control has to match the thing it is controlling. Immutability is
the right control for a record; reproducibility is the right control for an
output.

The protected artifacts are:

- `reports/laif_full_assessment.md` — full corpus assessment, authored 5 May 2026 under Refined Model v1.1
- `reports/laif_assessment_aus_ai_policy_v2.md` — Australian government AI policy assessment, authored 11 May 2026

Both record conclusions at a date. Do not edit or regenerate them in ordinary
pull requests. `reports/README.md` describes how each artifact in that directory
is produced and what verification stands behind it; the two lists are checked
against each other by `tests/test_governance.py`, so a new narrative artifact
cannot be added to the manifest without also being protected.

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

Maintainers may later choose to protect additional files, such as generated real-world reports, verified raw corpus files, evidence trace files, or artifact hash records. Those are informational possibilities only. They are not active policy in this Phase 2A documentation layer unless separately adopted.

## Human Review

Human reviewers remain responsible for approving assessment artifact changes. Repository documentation can define expectations, and future automation may detect drift, but automation should not approve assessment conclusions by itself.

## Phase 3 Blocking Behavior

Under the merged Phase 3A/3B governance lifecycle, protected-artifact checks are blocking. If a configured protected artifact appears in the pull-request diff, the governance job fails and downstream CI jobs that depend on governance do not proceed.

The check is deterministic and path-level. It does not inspect semantic meaning, report content, hashes, or assessment conclusions. Its purpose is to stop accidental protected-artifact drift before validation, adversarial, or real-world jobs run.

Governance config validation enforces that configured protected-artifact paths exist in the repository. Changing protected-artifact configuration or governance helper/check files is semantic-sensitive and should be reviewed as governance behavior, not ordinary text cleanup.

Protected-artifact protection does not alter LAIF scoring, detector logic, interpretation logic, or assessment conclusions. It also does not create external legal certification; it is repository-governance control for review discipline.
