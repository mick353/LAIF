# LAIF Document Processing Runner

The Phase 3T document processing runner is a local ingestion wrapper around the existing LAIF assessment engine. It extracts text from a local input document, passes the extracted text to `assess(...)`, renders the actual LAIF markdown report with `generate_markdown_report([result])`, and writes optional markdown, JSON, and JSONL index artifacts.

The runner is intentionally a wrapper. It does not change scoring, formal LAIF-native compliance, certification gates, validation behavior, governance scripts, protected artifacts, verified corpus files, manifests, or generated reports under `reports/`.

## Basic Usage

```bash
python3 scripts/laif_process_document.py INPUT_FILE
```

Default behavior:

- assessment mode: `external_framework`
- sector: `auto`
- output directory: `laif_outputs`
- markdown output: enabled
- JSON output: enabled
- extractor: `auto`
- processing index: `laif_processing_index.jsonl` appended in the selected output directory for write-enabled successful runs

Use `--no-write` to run extraction and assessment without writing markdown, JSON, or index outputs. Use `--print-report` to print the generated markdown report to stdout.

## CLI Flags

The runner supports:

- `--mode external_framework|laif_native` — defaults to `external_framework`; `laif_native` maps into the existing strict LAIF-native certification channel.
- `--sector auto|general_ai_governance|government_service_delivery|departmental_ai_development|procurement_vendor_governance|clinical_ai|employment_hr_ai|education_ai` — defaults to `auto`.
- `--source-type` — source-type metadata passed into assessment.
- `--document-name` — assessment document name; defaults to the input file stem.
- `--output-dir` — selected output directory; defaults to `laif_outputs`.
- `--markdown` / `--no-markdown` — enable or disable markdown artifact writing.
- `--json` / `--no-json` — enable or disable JSON artifact writing.
- `--extractor auto|builtin|docling|markitdown|python-docx|pypdf` — select extraction strategy.
- `--fail-on-warnings` — fail if extraction succeeds but records warnings.
- `--print-report` — print the generated LAIF markdown report.
- `--no-write` — do not create markdown, JSON, or index outputs.

## Extractor Strategy

The runner never performs network calls and never performs silent OCR. Extraction is local-only and must produce non-empty text above a safe minimum character threshold before assessment proceeds.

Extraction support:

1. Built-in extractor for `.txt`, `.md`, and `.markdown` files.
2. Optional Docling extraction when `docling` is installed.
3. Optional MarkItDown extraction when `markitdown` is installed.
4. Optional `python-docx` fallback for `.docx` files when installed.
5. Optional `pypdf` / `PyPDF2` fallback for `.pdf` files when installed.

`--extractor auto` tries the deterministic built-in path first for supported text/markdown files, then optional local extractors where available, and finally format-specific fallbacks for DOCX/PDF. Unsupported file types, missing explicit extractor dependencies, parser failures, and empty extraction fail clearly instead of silently producing incomplete assessment artifacts.

## Auto-Sector Heuristic

When `--sector auto` is used, a deterministic keyword heuristic selects a diagnostic sector profile from the extracted text. Clinical, procurement/vendor, employment/HR, education, government service delivery, and departmental development signals are considered before falling back to `general_ai_governance`.

Auto-sector selection is diagnostic metadata only. It does not change formal LAIF-native compliance, scoring weights, certification behavior, validation, or governance boundaries.

## Processing Identity and Output Naming

Output filenames use a filesystem-safe stem derived from the original input stem:

- markdown: `<safe_output_stem>.laif.md`
- JSON: `<safe_output_stem>.laif.json`
- index: `laif_processing_index.jsonl`

The original source identity is preserved separately in metadata so safe filenames do not erase provenance. Each run records:

- `processed_at_utc`
- `source_sha256`
- `input_file_name`
- `original_file_name`
- `original_file_stem`
- `safe_output_stem`
- markdown output path
- JSON output path

The markdown report begins with a processing metadata block containing Processed at UTC, Original file name, Source SHA-256, Extractor used, Extracted characters, Assessment mode, Sector profile, Safe output stem, Markdown output path, and JSON output path.

## JSON Output Shape

Write-enabled JSON output has this top-level structure:

```json
{
  "processing_metadata": {
    "processed_at_utc": "...",
    "original_file_name": "...",
    "source_sha256": "...",
    "safe_output_stem": "...",
    "markdown_output_path": "...",
    "json_output_path": "..."
  },
  "extraction_metadata": {
    "extractor_used": "...",
    "extracted_characters": 0
  },
  "assessment_result": {}
}
```

`extraction_metadata` retains extractor details, warning/error counts, no-OCR/no-network declarations, and the same identity fields (`input_file_name`, `original_file_name`, `original_file_stem`, `source_sha256`, `safe_output_stem`) used for processing identity.

## Processing Index JSONL

For each successful write-enabled run, the runner appends one line to `laif_processing_index.jsonl` in the selected output directory. `--no-write` does not create or append the index.

Each JSONL record contains:

- `processed_at_utc`
- `original_file_name`
- `input_path`
- `source_sha256`
- `safe_output_stem`
- `markdown_output_path`
- `json_output_path`
- `document_name`
- `assessment_mode`
- `sector_profile`
- `formal_laif_native_compliance`
- `overall_readiness_score`
- `evidence_trace_count`
- `remediation_patch_count`
- `calibration_caution_count`
- `gaming_risk_note_count`
- `extractor_used`
- `extracted_characters`
- `extraction_confidence`
- `warning_count`
- `error_count`

## Boundary Statement

The document runner is an ingestion and reporting convenience layer. It assesses extracted text using the existing assessment engine and renders existing report logic. It does not modify `assessment_engine.py`, `validate.py`, scoring/certification behavior, formal compliance behavior, governance scripts/config, protected artifacts, verified corpus/manifests, or committed generated reports.

## Phase 3U GitHub Actions batch workflow

For repository-hosted batch operation, Phase 3U provides the manual **LAIF Process Pending Documents** GitHub Actions workflow. Operators place supported documents in `laif_inputs/pending/`, choose workflow inputs for mode, sector, extractor, commit behavior, reprocessing, and maximum attempts, then download the workflow artifact.

The batch workflow is an orchestration wrapper around this Phase 3T runner. It shells to `scripts/laif_process_document.py` for each supported file and preserves the same extraction, assessment, output, and boundary behavior documented above. It does not import or alter the assessment engine, and it does not write to repository-root `reports/`.

Each batch writes a latest summary pointer at `laif_batch_summary.json` and a permanent timestamped history file at `laif_inputs/batch_summaries/<batch_run_id>.json`. The timestamped summaries record successes, failures, skips, duplicate SHA-256 decisions, workflow input values, and output locations.
