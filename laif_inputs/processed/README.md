# Processed batch outputs — historical

Everything under this directory is **output**, not source, and is committed only
when a batch run is invoked with `commit_outputs=true` (the workflow default is
`false`; see `docs/governance/GITHUB_ACTIONS_DOCUMENT_PROCESSING.md`).

**The outputs currently committed here were produced in May 2026 and do not
reflect the current engine.** Detection, scoring, and report wording have all
changed since. They are retained as a record of what was run, not as current
assessments, and must not be cited as findings about the instruments they name.

Every artifact generated from this point carries a `toolchain_fingerprint` in
its processing metadata and in `laif_processing_index.jsonl` — a content hash of
`assessment_engine.py`, `validate.py`, `laif_spec.py`, and
`scripts/laif_process_document.py`. To check whether an artifact reflects the
current code:

```bash
python3 -c "import assessment_engine; print(assessment_engine.toolchain_fingerprint())"
```

If the value differs from the one in the artifact, the artifact is stale.
Regenerate it by re-running the source through
`scripts/laif_process_document.py`.

The authoritative, CI-verified assessment artifacts are in `reports/`. Those are
regenerated on every engine change and checked against the committed copies by
CI.
