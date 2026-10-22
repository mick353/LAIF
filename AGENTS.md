# Repository agent instructions

## Local-first verification (GitHub Actions not used)

LAIF operates with local/manual Python checks. Do not initiate GitHub Actions
runs, rely on status badges, or report a CI result as evidence of verification.
The legacy workflow is not triggered by push or pull requests.

1. Inspect current main, open pull requests, governance docs and relevant code.
   Use a fresh branch from current main; compare before making changes.
2. Run the smallest targeted tests during development; avoid duplicating full
   test runs when no shared files or scoring semantics have changed.
3. Run local verification for release/merge:
   - quick: `python3 scripts/laif_verify.py`
   - full: `python3 scripts/laif_verify.py --full --base-ref origin/main`
4. The full local check is the recommended repository gate; if not runnable,
   disclose exactly what was not run. Neither an unrun gate nor a historical
   GitHub Actions status is a PASS.
5. Preserve governance, protected artefact, source provenance, semantic fidelity,
   exact-source checks and deterministic report identity.
6. Changes to assessment_engine.py, validate.py, laif_spec.py or the document
   processor require the generated-report fingerprint/reproducibility discipline
   documented in CLAUDE.md.
7. Never treat a software gate as legal certification or proof of LAIF validity.

## Semantic and provenance discipline

Read CLAUDE.md, CONTRIBUTING.md and relevant docs/governance/ material before
changing scoring, detection, reporting, source corpora or protected artefacts.
Preserve LAIF-native certification versus external-framework diagnostic
assessment, functional alignment versus terminology, and legal authority
boundaries. The new evidence diagnostic is optional and does not alter those
boundaries.
