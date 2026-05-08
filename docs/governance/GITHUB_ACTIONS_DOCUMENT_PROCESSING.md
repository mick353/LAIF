# GitHub Actions Document Processing

## Purpose

The **LAIF Process Pending Documents** workflow provides GitHub-native batch orchestration around the Phase 3T document processing runner. It lets a user upload supported documents into `laif_inputs/pending/`, manually run one GitHub Actions workflow, and receive organized processed or failed outputs without using a local terminal.

This workflow does **not** change LAIF assessment, scoring, certification, formal compliance, evidence trace, remediation, sector, calibration, governance, or protected-artifact behavior. It shells to the existing `scripts/laif_process_document.py` runner for each pending document.

## User Workflow

1. Upload one or more supported documents to `laif_inputs/pending/`.
2. Open **Actions** in GitHub.
3. Select **LAIF Process Pending Documents**.
4. Choose **Run workflow** and confirm inputs.
5. Download the `laif-batch-output` artifact, or explicitly set `commit_outputs=true` if repository history should store the outputs.

## Folder Structure

```text
laif_inputs/
├── pending/     # User-uploaded input documents
├── processed/   # Successful batch runs, grouped by run_id
└── failed/      # Failed batch runs, grouped by run_id
```

The `.gitkeep` files keep the empty folders visible in Git.

## How to Upload Documents

In GitHub, browse to `laif_inputs/pending/`, choose **Add file**, and upload the documents to assess. Do not upload documents into `laif_inputs/processed/` or `laif_inputs/failed/`; those folders are workflow outputs.

## How to Run the Workflow

Go to **Actions → LAIF Process Pending Documents → Run workflow**. Leave the defaults unless you need a different LAIF assessment mode, sector profile, extractor, commit mode, reprocessing rule, or maximum file count.

## Workflow Inputs

- `mode`: `external_framework` by default; `laif_native` is also available.
- `sector`: `auto` by default, with the same sector choices accepted by the Phase 3T runner.
- `extractor`: `auto` by default. Lightweight `python-docx` and `pypdf` dependencies are installed by the workflow.
- `commit_outputs`: `false` by default and the safest default.
- `commit_mode`: `copy` by default; `move` removes processed pending files, and `archive` copies plus writes an archive manifest.
- `reprocess`: `false` by default, so duplicate source SHA-256 values are skipped.
- `max_files`: `20` by default, limiting how many supported pending files are processed in one run.

## Output Artifacts

Every workflow run uploads a `laif-batch-output` artifact containing:

- `laif_inputs/processed/**`
- `laif_inputs/failed/**`
- `laif_batch_summary.json`

When `commit_outputs=false`, the artifact is the normal way to retrieve the output without adding processed files to repository history.

## Commit Outputs Option

`commit_outputs=false` is the safest default. If `commit_outputs=true`, GitHub Actions commits `laif_inputs/processed`, `laif_inputs/failed`, and `laif_batch_summary.json` back to the repository.

If `commit_outputs=true`, processed outputs become repository history. Do not enable it for sensitive, confidential, personal, regulated, or private documents unless the repository and retention model are appropriate.

## Processed / Failed Folder Layout

Successful files are written under `laif_inputs/processed/<run_id>/`:

```text
processed/<run_id>/
├── source/       # Original source document copy, or moved source in move mode
├── reports/      # .laif.md, .laif.json, and laif_processing_index.jsonl from the Phase 3T runner
└── metadata/     # run_metadata.json and optional archive_manifest.json
```

Failed files are written under `laif_inputs/failed/<run_id>/`:

```text
failed/<run_id>/
├── source/       # Original source document copy, or moved source in move mode
├── error.txt     # Runner command, return code, stdout, and stderr
└── metadata/     # run_metadata.json and optional archive_manifest.json
```

## Reprocessing Rules

The batch script computes the SHA-256 hash of each source document. With `reprocess=false`, a pending file is skipped when the same source SHA-256 already appears in processed or failed `run_metadata.json`. The skip reason is `skipped_duplicate` in `laif_batch_summary.json`.

With `reprocess=true`, the same source can be processed again and receives a new `<UTC compact timestamp>__<safe original stem>` run ID.

## Privacy and Public Repository Warning

Public repositories should not receive sensitive documents. Do not upload private, personal, confidential, legally privileged, regulated, proprietary, or otherwise sensitive files into a public repo.

For private or sensitive use, use a private repository with appropriate access controls or use the local Phase 3T runner instead. If `commit_outputs=true`, outputs and copied source files may remain in repository history even after later deletion.

## Supported File Types

The batch processor accepts:

- `.txt`
- `.md`
- `.markdown`
- `.docx`
- `.pdf`

`.gitkeep` is ignored. Unsupported files are skipped deterministically and recorded in `laif_batch_summary.json`.

## Optional Extractors

The workflow installs lightweight ingestion dependencies `python-docx` and `pypdf`. Heavy Docling is not installed by default. If scanned PDFs fail because they require OCR, do not hallucinate document content; use an OCR-capable local process or custom workflow before running LAIF.

## Limits and Failure Modes

- The workflow processes no more than `max_files` supported pending files.
- Failed files are organized under `laif_inputs/failed/<run_id>/` with `error.txt` and metadata.
- Extraction failures, unsupported encrypted PDFs, missing optional extractor packages, and scanned PDFs without OCR may fail or be skipped depending on the case.
- The workflow does not write under the repository-level `reports/` directory.

## Relationship to LAIF Runner

This is batch orchestration around `scripts/laif_process_document.py`, the Phase 3T final document ingestion runner. The batch layer creates run folders, shells to that runner, copies or moves source documents, writes run metadata, writes a batch summary, uploads artifacts, and optionally commits outputs.

## Non-Goals

- No changes to `assessment_engine.py`.
- No changes to `validate.py`.
- No changes to scoring, certification, formal compliance, evidence trace behavior, remediation behavior, sector logic, calibration logic, governance scripts/config, protected artifacts, verified corpus files, manifests, or committed generated reports under `reports/`.
- No OCR for scanned PDFs.
- No automatic commits unless `commit_outputs=true`.
