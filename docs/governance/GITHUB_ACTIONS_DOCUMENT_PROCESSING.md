# GitHub Actions Document Processing

The LAIF document-processing workflow batches files from `laif_inputs/pending` through the local document runner and publishes the resulting processing artifacts. It is a workflow wrapper only: it does not change scoring, certification, assessment semantics, validation behavior, privacy warnings, duplicate/reprocess rules, or report generation under `reports/`.

## Batch Summary History

Each workflow batch invocation receives a `batch_run_id` in this form:

```text
<UTC compact timestamp>__batch
```

The batch processor writes two summary files for the same payload:

- `laif_batch_summary.json` — the latest-run pointer. Repeated runs update this file so consumers can find the most recent batch result quickly.
- `laif_inputs/batch_summaries/<batch_run_id>.json` — the permanent per-run summary history. Repeated runs must not overwrite historical summaries because each batch receives a unique timestamped `batch_run_id`.

Both JSON summaries include `batch_run_id` and `timestamped_summary_path` so the latest summary can be traced back to its immutable per-run history file.

## Workflow Outputs

The workflow uploads these artifact paths:

```text
laif_inputs/processed/**
laif_inputs/failed/**
laif_inputs/batch_summaries/**
laif_batch_summary.json
```

The `laif_inputs/batch_summaries/**` artifact path preserves timestamped batch summary history alongside timestamped processed and failed document outputs.

## Commit Behavior

`commit_outputs` defaults to `false`. When an operator explicitly sets `commit_outputs == true`, the workflow commits only the document-processing output surfaces:

```text
laif_inputs/processed
laif_inputs/failed
laif_inputs/batch_summaries
laif_batch_summary.json
```

This keeps the latest summary pointer and the permanent per-run batch summary history together when outputs are committed.

## Privacy and Operational Boundary

Only place documents in `laif_inputs/pending` when they are appropriate for repository-hosted GitHub Actions processing and artifact upload. The workflow can upload and optionally commit processed outputs, failed-output diagnostics, and batch summaries. Do not place confidential, privileged, personal, or regulated data in the pending directory unless the repository, workflow permissions, retention policy, and artifact/commit behavior have been reviewed and approved.
