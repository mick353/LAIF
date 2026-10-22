# Complete local verification (without GitHub Actions)

LAIF's governance, assessment, document-processing and deterministic-report
checks run directly in Python. No GitHub Actions runner, network account, API
key or remote service is required to execute them. This is useful for Codex,
ChatGPT execution environments, developers and machines without available
GitHub-hosted Actions minutes.

## Full verification

1. Use Python 3.10 where possible (the version configured in GitHub CI), Git,
   and a complete LAIF checkout with any optional parsers being tested.
2. Work on a feature branch with changes **committed** and no uncommitted or
   untracked files. Governance's protected-artifact comparison examines
   committed changes against a Git base, not uncommitted edits.
3. From the repository root, run:

   ```bash
   python3 -B scripts/verify_local.py --base-ref origin/main --receipt /tmp/laif-local-verification.json
   ```

   If `origin/main` is not available, supply a verified comparison ref such as
   `main`. The tool can also determine a local comparison ref automatically;
   it reports the exact ref selected. An invalid ref fails rather than
   silently skipping governance diff checks.

4. Retain the receipt with the reviewed commit SHA, comparison-base SHA,
   Python version, command results, and report SHA-256 digests.

The runner follows CI's ordered gates: governance compilation/config,
protected-artifact and semantic-boundary checks, governance tests, four
validation modes, adversarial tests, provenance, semantic fidelity,
assessment fragility, document processing, batch processing-path tests,
real-world regeneration, comparison with committed `reports/` and a second
independent regeneration to detect nondeterminism.

It stops on the first failure and exits nonzero. An incomplete run is **not**
reported as PASS. Generated reports must match the committed versions.

## Scope and current repository policy

- This process is entirely independent of GitHub Actions for execution.
- **The existing GitHub Actions workflow still triggers automatically on pull
  requests and pushes to `main`.** Running the local tool does not disable
  that workflow or prevent GitHub-hosted usage if those events occur.
- The repository's existing CI-first review and merge instructions remain in
  force until changed through a separately approved governance decision.
- Passing either local or CI tests verifies the checked software behaviour,
  not legal authority, empirical validity or the truth of assessment claims.
- A run on Python other than 3.10 is useful evidence but does not establish
  exact compatibility with the CI target interpreter.

For targeted checks during development, run individual repository test scripts
listed in `CONTRIBUTING.md`. After the intended changes are committed and the
worktree is clean, run the full local gate again.
