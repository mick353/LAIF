# Repository agent instructions

## CI-first verification

LAIF already has a comprehensive GitHub Actions gate in `.github/workflows/ci.yml`. It runs governance checks, corpus validation, adversarial tests, provenance and semantic-fidelity tests, document-processing tests, real-world assessment regeneration, committed-report comparison and determinism checks.

For Codex, ChatGPT and other remote coding agents:

1. Use a feature/fix branch and pull request for substantive changes.
2. During implementation, run the smallest targeted checks needed for the files and layer being changed.
3. Do not automatically repeat the complete LAIF verification suite locally immediately before pushing when GitHub Actions will run the same deterministic checks for that commit.
4. Treat the current PR-head GitHub Actions result as the authoritative full repository software/governance gate.
5. If CI fails, inspect the failing job and exact command first; reproduce only the relevant failure locally unless broader diagnosis is necessary.
6. If a change intentionally affects generated `reports/`, regenerate the required artifacts before push when the repository contract requires those files to accompany the source change.
7. Never weaken governance, protected-artifact, provenance, semantic-fidelity, deterministic-reporting or source-integrity controls merely to make CI pass.
8. CI PASS is repository verification. It is not external legal certification or proof that a governance framework is substantively valid.

Human contributors may still run the full suite locally when desired. This instruction exists to avoid making remote agents consume context and compute by duplicating a full deterministic suite that GitHub will immediately run again.

## Semantic and provenance discipline

Read `CLAUDE.md`, `CONTRIBUTING.md`, and the relevant `docs/governance/` material before modifying scoring, detection, reporting, corpus or protected artifacts. Preserve the distinction between LAIF-native form, external-framework diagnostic assessment, functional alignment, and legal authority.
