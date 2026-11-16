# Preserved batch execution record

**16 November retention update:** the redundant `latest_batch_summary.json`
alias was removed. Its unchanged bytes remain in
`batch_summaries/20260511T062417595291Z__batch.json`. The original relocation
manifest describes the earlier event; the
[deduplication manifest](../2026-11-16-deduplication.json) records the current
path and matching SHA-256.

This directory preserves the May 2026 batch outputs and summaries moved out of the active processing queues. Their contents and recorded paths are unchanged. They describe the code used for that execution, not the current toolkit. Use the current [worked example](../../examples/README.md) for a runnable product demonstration and [reports index](../../../reports/README.md) for corpus assessments.

The [relocation manifest](relocation-manifest.json) records each prior path, current path and SHA-256. One pending PDF was an exact duplicate of the original already held in `docs/verified/manual_ingest/`; only that redundant copy was removed. The other pending originals now live in the same custody directory. This relocation does not verify their upstream authenticity or change any ingestion status. The EU AI Act remains pending authoritative ingestion.
