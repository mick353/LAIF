# Source-index bridge verification — 8 November 2026 (AEDT)

Base: canonical `main` at `348b2af9aa6defcf417c44c6ce4dd564722a08ae`.

Executed in an isolated cloud checkout:

- `python3 scripts/laif_site_catalog.py verify`: 16 source hashes and 39 exact explanation-quotation spans passed.
- `python3 -m unittest discover -s tests -p test_site_catalog.py`: 11 tests passed. Coverage includes consent, exact source preservation, unverified proposal classification, duplicate import, changed bytes, traversal, mismatched assessment identity, duplicate JSON, PDF bytes and false quotation rejection.
- `python3 scripts/laif_verify.py --full --base-ref 348b2af9aa6defcf417c44c6ce4dd564722a08ae`: 598 discovered tests passed, with the additional governed source, provenance, semantic and deterministic report checks. Reports regenerated without committed-report drift. [Full execution log](verification/local-full-gate.log).
- Subsequent README-only changes add the bridge links and correct the old statement that no graphical companion exists. The final catalogue verifier and 11 focused tests were rerun successfully. No engine, scoring, source corpus or published assessment content changed.

This verifies software/package behaviour and local source/quotation identity. It does not establish upstream document equivalence, source publication rights, legal compliance, independent validation, hosted visitor writes or measured adoption outcomes. Direct visitor-to-GitHub writing is not supported by the current Sites integration; exported proposals still require an authorised maintainer import and reviewed merge.
