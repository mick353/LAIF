# Repository agent instructions

**Verified release base (7 November 2026):** PR #104 merged at ededd1b58afc56dbd06ad0b20f8793b3d1e79e3b with the 555-test tree 2982af0a8f2544be602f3637189a359cca81940d. The [substantive-review execution record](docs/verification/2026-11-07-substantive-review/README.md) records the subsequent enhancement and final verification. Inspect current Git/PR state to distinguish its checkpoint, tested and merged stages. Earlier logs remain historical.

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

## Independent scholarship, legal analysis and frontier-AI safety

- Treat LAIF as a testable analytical method, not as an authority to promote.
  Lead external reports with the research question, sources, method, findings,
  uncertainties and alternatives. Explain LAIF terminology only when necessary.
- Identify the exact branch, revision, corpus, execution mode and evidence tier.
  Draft pull requests are proposals, not canonical features or verified results.
  Do not present remembered conversations or third-party summaries as inspection.
- Distinguish internal software verification and deterministic rubric consistency
  from independently established construct validity, regulatory compliance,
  deployment safety and scientific effectiveness. Never turn a scoring output,
  synthetic fixture or a passing test count into an externally validated claim.
- For legislation, check primary text, jurisdiction, commencement, role,
  qualification, exceptions and legally binding status; report interpretive
  ambiguity. A missing document or control claim is not proof of a legal breach.
- Documentary governance assurance cannot demonstrate adversarial robustness,
  containment effectiveness, deceptive behaviour or catastrophic-risk
  probabilities. Dynamic model evaluations must be separately supplied,
  sourced, scoped and reviewed; no native dynamic testing is implied.
- For empirical-validation proposals specify blinded independent reviewers,
  sampling and exclusions, human agreement before adjudication, target labels,
  prespecified metrics, confidence intervals and error analysis. Distinguish
  inter-human reliability from model-versus-consensus agreement.

See [the external scholarly critique triage](docs/review/2026-11-07-external-scholarly-critique-triage.md)
for a dated, non-canonical research plan and an explicit record of limitations.
