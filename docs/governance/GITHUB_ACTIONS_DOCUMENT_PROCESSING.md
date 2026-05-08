# GitHub Actions Document Processing (Phase 3U)

Phase 3U adds a manual GitHub Actions batch workflow for pending local documents. It is orchestration only: the workflow calls the Phase 3T document runner and does not change LAIF scoring, certification, validation, governance boundaries, protected artifacts, or generated reports under `reports/`.

## User workflow

1. Add input files to `laif_inputs/pending/`.
2. Open **Actions → LAIF Process Pending Documents**.
3. Choose the workflow inputs.
4. Run the workflow.
5. Download the artifact, or set `commit_outputs=true` if repository-history persistence is explicitly desired.

## Exact folder structure

```text
laif_inputs/
  pending/
    .gitkeep
    <documents to process>
  processed/
    .gitkeep
    <run_id>/
      source/<original file>
      reports/<document>.laif.md
      reports/<document>.laif.json
      reports/laif_processing_index.jsonl
      metadata/metadata.json
      archive_manifest.json        # archive mode only
  failed/
    .gitkeep
    <run_id>/
      source/<original file>
      error.txt
      metadata/metadata.json
  batch_summaries/
    .gitkeep
    <batch_run_id>.json
laif_batch_summary.json
```

## Workflow inputs

The workflow is manually triggered by `workflow_dispatch` and exposes the full Phase 3U batch surface:

- `mode`: `external_framework` or `laif_native`; default `external_framework`.
- `sector`: `auto`, `general_ai_governance`, `government_service_delivery`, `departmental_ai_development`, `procurement_vendor_governance`, `clinical_ai`, `employment_hr_ai`, or `education_ai`; default `auto`.
- `extractor`: `auto`, `builtin`, `docling`, `markitdown`, `python-docx`, or `pypdf`; default `auto`.
- `commit_outputs`: boolean; default `false`.
- `commit_mode`: `copy`, `move`, or `archive`; default `copy`.
- `reprocess`: boolean; default `false`.
- `max_files`: string input passed to the batch runner; default `"20"`.

The workflow installs lightweight `python-docx` and `pypdf` support. Heavy optional extractors such as Docling and MarkItDown are not installed by default.

## Output artifacts

Every run uploads a workflow artifact containing:

- `laif_inputs/processed/**`
- `laif_inputs/failed/**`
- `laif_inputs/batch_summaries/**`
- `laif_batch_summary.json`

`commit_outputs=false` is the default. With the default, generated outputs stay in the workflow artifact rather than being committed back to the repository.

## Privacy and repository-history warning for `commit_outputs=true`

Use `commit_outputs=true` only when the organization intentionally wants processed sources, failed sources, metadata, reports, and batch summaries retained in Git history. Git history is durable and difficult to scrub. In a public repository, never place confidential, regulated, privileged, proprietary, personal, or sensitive documents in `laif_inputs/pending/` unless repository publication and artifact exposure have been approved.

When `commit_outputs=true`, the workflow commits:

- `laif_inputs/processed`
- `laif_inputs/failed`
- `laif_inputs/batch_summaries`
- `laif_batch_summary.json`

## Processed and failed layout

Successful files create `laif_inputs/processed/<run_id>/source`, `reports`, and `metadata` folders. Failed files create `laif_inputs/failed/<run_id>/source`, `error.txt`, and `metadata`. The batch runner never writes to the repository-root `reports/` directory.

## Batch summary history

Each batch invocation creates a batch run identifier:

```text
<UTC compact timestamp>__batch
```

The batch writes two summary files:

- `laif_batch_summary.json` — latest pointer for the most recent batch.
- `laif_inputs/batch_summaries/<batch_run_id>.json` — permanent per-run summary history.

Summary payloads include the batch paths, timestamps, mode, sector, extractor, commit mode, reprocess flag, max-files limit, success/failed/skipped counts, and detailed `successes`, `failures`, and `skipped` arrays.

## Duplicate and reprocess rules

For each supported source file, the batch runner computes `source_sha256`. When `reprocess=false`, any file with a SHA-256 already present in prior processed or failed metadata is skipped and recorded as `duplicate_source_sha256`. When `reprocess=true`, the same source content is processed again under a new run ID.

## Copy, move, and archive behavior

- `copy`: default. The pending source remains in `laif_inputs/pending/`, and a copy is stored under the run folder.
- `move`: after a successful run, the pending source is removed from `laif_inputs/pending/`; the run folder retains the stored source.
- `archive`: the pending source remains in place, the run folder stores a source copy, and `archive_manifest.json` records archive metadata.

## Supported file types and optional extractors

The batch runner attempts `.txt`, `.md`, `.markdown`, `.docx`, and `.pdf`. It ignores `.gitkeep`. Unsupported extensions are skipped deterministically and recorded in the batch summary.

Text and markdown use the built-in extractor. DOCX and PDF can use lightweight `python-docx` and `pypdf`; optional `docling` and `markitdown` are available only if an operator installs them in the workflow or environment.

Scanned PDFs that require OCR may fail because the Phase 3T runner does not perform OCR and does not silently call network services.

## Relationship to Phase 3T runner

Phase 3U shells to `scripts/laif_process_document.py` for each supported document. Phase 3T remains the only layer that extracts a single document, calls the assessment engine, and writes LAIF markdown/JSON report artifacts for that document.

## Non-goals

Phase 3U does not change scoring, formal LAIF-native compliance, certification gates, validation behavior, `assessment_engine.py`, `validate.py`, governance scripts, protected artifacts, verified corpus files, manifests, or root-level generated reports.
