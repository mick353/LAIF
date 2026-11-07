# Executed verification — PR #98

**Date:** 7 November 2026, Australia/Sydney. **Environment:** Work cloud, Python 3.12; pypdf 6.10.0 and Poppler 24.02.0 already present. Python 3.10+ is the repository target, not a claim of an executed 3.10 runtime test. No GitHub Actions, paid model APIs or user-PC execution was used.

| Executed command/check | Actual result | Evidence |
|---|---|---|
| `python3 scripts/laif_process_regulatory_sources.py --output-dir ../final-pypdf-run` | Exit 0, both PDFs processed | `pypdf-run.log`, `pypdf-diagnostic/run_manifest.json` |
| `python3 scripts/laif_process_regulatory_sources.py --verified-text --output-dir ../final-regulatory-run` | Exit 0, both reviewed extractions processed | `verified-text-run.log`, `reviewed-text/run_manifest.json` |
| `python -S scripts/laif_process_regulatory_sources.py --verified-text --output-dir ../stdlib-regulatory-run` | Exit 0 with site packages disabled | `stdlib-regression.log`; complete assessment-result dictionaries matched the previous run excluding execution timestamp only |
| `python3 scripts/laif_verify_regulatory_ingestion.py --reextract` | Exit 0; both PDF/raw hashes, 67 pages, 44 exact page-bounded quotation traces; Poppler reconstruction identical | `source-verification.log` and discovered regression tests |
| `python3 tests/test_regulatory_pdf_runner.py` | Exit 0; 4 tests | Includes changed PDF rejection before processing and evidence/report/Git output-directory rejection; also included in full discovery |
| `python3 tests/test_regulatory_ingestion.py` | Exit 0; 5 tests | Includes actual snapshots, raw corruption, invented quotation, wrong-page rejection and assessed-text/evidence-span identities; also included in full discovery |
| `python3 scripts/laif_verify.py` | Exit 0 | `quick-verification.log` |
| `python3 scripts/laif_verify.py --full --base-ref origin/main` | Exit 0; **382 discovered tests**, plus additional direct suites and gates | `full-verification.log` |
| `git diff --cached --check` | Exit 0 after removing trailing whitespace from snapshot Markdown only | Original JSON, PDF and verified raw source bytes unchanged by formatting cleanup |
| Protected historical reports, baseline generated reports and four fingerprinted engine files | No diff | Source additions and wrapper hardening only; fingerprint remains `e0e3292e34444f18` |

The full verifier actually ran governance configuration, protected-artifact and semantic-diff checks; `validate.py`, `--verified-corpus`, `--check-evidence-traces`, `--check-corpus-formats`; all discovered test modules; adversarial, provenance and semantic-fidelity scripts; and two consecutive `test_real_world.py` regenerations. The regenerated baseline reports matched each other and the committed baseline. No full-gate command was skipped. The original 2024 EU Act manifest remains `PENDING_INGESTION`; its own file/hash checks are intentionally skipped by existing manifest logic, not claimed as passed.

## Warnings and corrected failures

- The normal corpus validation reports five pre-existing advisory warnings. These are not hidden or reclassified as failures.
- Verified-corpus validation passes with one new advisory warning: the legacy optional `network_status` vocabulary does not recognise the accurately recorded DTA `AUTOMATED_URL_FAILED_HTTP_503`. Its supported `verification_status` is `HUMAN_ATTESTED_AUTHORITATIVE`. No enum or admission gate was relaxed to silence the warning.
- Existing evidence-trace mode checks 39 citations over the four historical documents, not the new trace JSON. The new dedicated verifier and tests check the new 44 exact quotations.
- Initial cleaner-text CLI calls used unsupported short sector aliases and exited 2; rerunning with the canonical `government_service_delivery` and `general_ai_governance` choices succeeded. No result is reported from those rejected calls.
- Initial staged whitespace check found Markdown hard breaks and trailing spaces in generated snapshots. Markdown-only whitespace was trimmed; source/raw/JSON evidence was retained, and the staged check passed.
- pypdf extraction damage, document-level saturation, narrow functional-family detection, inherited report dates and some incomplete machine-selected quote propositions remain disclosed software limitations. Fixing these broader engine/reporting issues would change the preserved semantics or fingerprint and requires focused follow-up review; they are not represented as resolved here.

## Review readiness

The execution/source-processing work is complete and locally verified. These are separate **draft source-scoped assessments**, not replacements for protected reports. The PR is ready for source/policy/legal/semantic review, not automatically approved for merge. DTA upstream-byte equivalence, human review and a fully joined/consolidated EU-law assessment remain limitations. Original-Act admission stays with PR #90. No unrelated PR was changed and no merge was performed.
