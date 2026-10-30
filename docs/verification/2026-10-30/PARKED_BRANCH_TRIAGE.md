# Parked Windows branch triage — 30 October 2026

The local `codex/reconcile-windows-portability` branch has two October 3 commits (`453aa50`, `7e3d76b`) based on older `bf09fd3`. It was inspected against current `main` without cherry-picking either commit. The branch remains available as history; `.tmp.driveupload/` was untouched.

| Old-branch area | Disposition against current main |
|---|---|
| `.gitattributes` source LF rules | Superseded: current main has broader explicit LF rules for text, JSON and Markdown plus binary DOCX/PDF handling. |
| `validate.py` CRLF-to-LF hash normalization and `test_provenance.py` fixtures | Deliberately not adopted: current verified-corpus checks compare file bytes to manifest hashes; changing the verifier to normalize bytes would weaken detection of a local source-byte change. LF checkout rules and the Windows release verification resolve transport consistency. |
| `scripts/laif_process_document.py` explicit extractor exception handling | Merged by a narrower current implementation in [PR #87](https://github.com/mick353/LAIF/pull/87), including direct and CLI invalid-UTF-8 regression tests. |
| `scripts/laif_process_document.py` `input_path_original` POSIX conversion | Deliberately deferred: this field records the caller's original path spelling, including Windows separators. Converting it would change identity metadata. Portable presentation paths can be handled separately if a consumer demonstrates a need. |
| `tests/test_document_processing_runner.py` portable report-path assertion | Superseded for the current generated report link, which already uses `.as_posix()`; the old assertion is tied to a helper absent from current main. |
| `test_real_world.py` display-only path helper | Deferred: the generated executive-summary link already uses `.as_posix()`, and the remaining changes would only alter console path display. No failing release check or downstream consumer was found. |
| `validate.py` header date check and `tests/test_assessment_fragility.py` fixtures | Merged by [PR #88](https://github.com/mick353/LAIF/pull/88), with an opening-line boundary and regression for a date outside that boundary. |
| `validate.py` broad alignment-context exemption | Superseded by PR #88's narrower matched-prefix exemption. The old version could suppress a genuine Coupling substitution merely because an external artefact name appeared nearby. |
| `test_adversarial.py` old group additions | Covered by current focused regression tests and full adversarial run for PR #88; the old test-only rewrites are not needed for this fix. |
| `reports/laif_assessment_data.json` old fingerprint | Superseded by regenerated, drift-checked report identity in PRs #87 and #88; the old artifact must not be copied over current output. |
| `MANUAL_INGESTION_WORKFLOW.md`, `REPRODUCIBILITY.md`, `docs/verified/README.md`, `verified_corpus_manifest.md`, `PUBLICATION_STATUS.md` LF and readiness wording | Superseded by current LF policy, Windows verification, and later publication/source-custody records. Their old EU `PENDING_INGESTION` wording is being updated through the separate [PR #90](https://github.com/mick353/LAIF/pull/90). |

The two code fixes identified as necessary have passed the full local release gate and are on GitHub `main` through PRs #87 and #88. This record closes the old-branch investigation; publication cross-references and EU source admission retain their own review gates. No GitHub Actions run was used.
