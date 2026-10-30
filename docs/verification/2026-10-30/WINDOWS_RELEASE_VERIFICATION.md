# Windows local verification, 30 October 2026

**Status:** local software and governance gate passed on `Z:\laif`; external legal or operational acceptance was not assessed. Observed at 20:21 Canberra time (AEDT, UTC+11). No GitHub Actions run was used.

## Checkout and scope

- Base: `origin/main` at `c573e568d37289acf05a1946b3e76517d7975d6d`, containing PRs #79, #80, #81 and #82. No open PRs were listed at the start.
- Verified code commit: `c93105a58572efc0010cda1da40cab93eb5a8da3` on `verify/windows-assurance-20261030`, one commit ahead of that base. The full gate ran on the exact code diff before it was committed; the commit changed no file contents.
- Windows PowerShell 7.6.5, Python 3.13.16 (`py -3`), Git 2.56.0.windows.3. The older `codex/reconcile-windows-portability` branch and untracked `.tmp.driveupload/` remain untouched.
- No Git process or lock was present. `git fsck --no-reflogs --unreachable` exited successfully and listed only unreachable trees/blob; no object corruption was reported. `git fetch origin --prune` completed. No reset, duplicate clone or deletion was used.

## Commands and results

| Check | Result |
| --- | --- |
| `py -3 -X utf8 -m unittest tests.test_assurance tests.test_assessment_fragility tests.test_document_processing_runner` | Initially 287 tests: 1 failure, 1 skip. The JSONL original-path assertion still required a POSIX slash, unlike the corrected JSON and Markdown assertions. The affected test passed after correction. |
| `py -3 -X utf8 .\scripts\laif_verify.py --full --base-ref origin/main` | Final run passed. It included governance config, protected-artifact and semantic-boundary checks; all four `validate.py` modes; 369 discovered tests with 2 skips; standalone adversarial, provenance and semantic-fidelity suites; two real-world report generations; and a clean `git diff --exit-code -- reports/`. |
| Provenance and report details | Verified corpus 75 pass/0 fail; evidence traces 47 pass/0 fail; source-format check 8 pass/0 fail; standalone provenance 52 pass/0 fail; semantic fidelity 68 pass/0 fail. Report regeneration was deterministic and produced no committed-report diff. |

The two skipped discovered tests are symlink-dependent tests whose code skips when symlinks are unavailable in the environment. Optional extractor integration and real institutional effectiveness were not established by this gate.

## Failures resolved during verification

1. The verifier's child Python processes did not inherit the parent `-X utf8` setting. `validate.py` stopped on a Unicode banner under `cp1252`. The verifier now passes `PYTHONIOENCODING=utf-8` to child commands.
2. Four verified raw Markdown files in this existing checkout had CRLF working copies. Each matched its SHA-256-pinned Git blob after CRLF-to-LF conversion. The existing `.gitattributes` already requires LF; the four raw files and four matching `docs/supporting` mirrors were restored byte-for-byte from Git. No source or manifest diff was committed. Provenance then passed.
3. The generated executive summary used a Windows backslash in its report link. The generator now writes a POSIX relative reference. Four code files used by the toolchain fingerprint also had CRLF working copies; restoring their unchanged Git blobs returned the committed fingerprint. The generated reports then matched their committed versions.

The code change is limited to `scripts/laif_verify.py`, `test_real_world.py`, and `tests/test_document_processing_runner.py`. LAIF scoring, corpus contents, manifests and protected assessment artefacts were not changed. The full gate verifies repository behavior; it does not certify LAIF's legal validity, independently authenticate source acquisition, or prove operational control effectiveness.
