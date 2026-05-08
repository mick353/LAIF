# LAIF Document Processing Runner

`scripts/laif_process_document.py` converts a local source document into generated LAIF assessment outputs. By default it writes to `laif_outputs/` and creates one markdown report, one JSON report, and a local processing index in the selected output directory.

## Processing identity metadata

Each run records processing identity metadata so generated reports remain traceable to the source file over time:

- `processed_at_utc` records the UTC processing timestamp for the run.
- `source_sha256` records the SHA-256 digest of the original input file bytes.
- The original file name is retained in extraction metadata, markdown metadata, JSON `processing_metadata`, and the local processing index.
- Output files use safe stems derived from the input stem, while metadata preserves original names that may contain spaces or punctuation.

The markdown metadata block includes processed time, original file name, source SHA-256, extractor used, extracted character count, assessment mode, and sector profile. The JSON output has top-level `processing_metadata`, `extraction_metadata`, and `assessment_result` objects.

## Output-directory index

Write-enabled runs append one JSON object per line to:

```text
laif_outputs/laif_processing_index.jsonl
```

or to the same file name inside the directory selected with `--output-dir`. The index summarizes source identity, output paths, assessment mode, sector profile, formal LAIF-native compliance status, overall readiness score, evidence trace count, remediation patch count, calibration caution count, gaming risk note count, extractor used, extracted characters, extraction confidence, warning count, and error count.

`laif_processing_index.jsonl` is local generated output. It is not a protected artifact, verified corpus file, manifest, or committed report. The runner writes the index only in the selected output directory; it does not write the index under `reports/` or any protected path by default.

## No-write mode

`--no-write` runs extraction and assessment without writing markdown, JSON, or appending `laif_processing_index.jsonl`. Use this mode for dry-run checks where generated output should not be created.

## Example

```bash
python3 scripts/laif_process_document.py policy.txt --output-dir laif_outputs
```
