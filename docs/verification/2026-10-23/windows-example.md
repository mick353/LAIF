# Focused Windows clone and example verification

This supplements the existing Linux offline verification. It does not repeat or extend its full-platform claim.

Source: `mick353/LAIF` main `258438c2347ff1d0794b5171bb5c89615e6c38c6`, with the documentation/layout change described below. The assessment engine, validator, canonical spec, processor and corpus assessment outputs are unchanged.

Environment: Windows, CPython 3.11.9, Git 2.55.0.windows.5. No packages were installed. The built-in text example also ran with Python `-S`, excluding site packages. Execution used an isolated checkout and required no Mike-specific drive, private structural engine, model API or credential. No GitHub Actions ran.

```powershell
py -3 -X utf8 -S scripts/laif_process_document.py docs/examples/vendor-policy.md --extractor builtin --output-dir laif_outputs/product-demo
py -3 -X utf8 tests/test_evidence_checks.py -v
py -3 -X utf8 tests/test_governance.py -v
py -3 -X utf8 tests/test_github_actions_document_processing.py -v
py -3 -X utf8 validate.py --verified-corpus
```

The local verification harness used an explicit writable temporary directory for Git test fixtures. The managed sandbox's default temporary directory could not support their `git init` calls; those initial fixture errors are recorded separately, not counted as product failures or passes. On a normal installation, use an accessible local temporary directory. `-X utf8` avoids the legacy Windows console encoding error observed when printing Unicode validation output.

Results:

- The supplier example completed twice. Institutional assessment and quote-bank text matched the committed samples and each other after platform newline normalization. All six quote offsets matched exact input slices.
- Policy SHA-256: `e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523`. Toolchain fingerprint: `b9759941d75b8fbe`.
- Evidence suite: 17 tests run, 16 passed, one skipped because symlink creation was unavailable. Governance suite: 48 passed. Local batch suite: 17 passed. These are focused checks, not a new full gate.
- Verified-corpus mode: 75 provenance checks passed, zero failed; four manifests remain assessed and the EU AI Act remains pending ingestion.
- Separate synthetic checker controls produced the expected policy-only, incomplete-coverage, ready-for-review, invalid-hash, unsupported-claim, adverse-outcome and contradictory-record results. Only the complete positive/negative fixture passed the strict review-ready gate. These records demonstrate checker behaviour, not execution of the supplier's safeguards.

The example identifies four missing control mechanisms: precedence, monitoring thresholds/escalation, breach consequences and change control. It retains protections already expressed in the source. Its automatic classification as a procurement assessment form remains a reviewer-checkable heuristic.

## Clone layout and line endings

Git's Windows `core.autocrlf=true` checkout changed the raw input hash and toolchain fingerprint before text processing. The text findings and quote offsets were stable, but an exact source identity differed from the published example. `.gitattributes` now keeps source and report text as LF across checkouts. Runtime-generated Windows files may use CRLF; compare their decoded text with universal-newline handling. JSON timestamps and absolute paths remain run-specific.

Active batch queues now start empty. Original custody files were moved to `docs/verified/manual_ingest/`; prior batch evidence was retained byte-for-byte relative to Git source blobs under [the preserved execution record](../2026-05-11/README.md), with a relocation/hash manifest. One identical duplicate PDF copy was removed. Required root governance documents, paired exports, test fixtures, verified raw texts, manifests and protected assessments were retained.

The existing complete Linux verification is reused because no scoring, extraction implementation or corpus content changed. Python 3.10, the complete Windows gate, real Docling/MarkItDown extraction and production governance effectiveness were not established by this focused run.
