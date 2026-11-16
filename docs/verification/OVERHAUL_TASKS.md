# Overhaul delivery record

Updated 16 November 2026. A release, a deployed version and observed acceptance
are separate states. See [current checkpoint](CURRENT.md).

| Work | Owner | Status | Next step / dependency / evidence |
|---|---|---|---|
| Extractor fallback | Delivery lead | Merged previously | PR #118; retain historical test evidence |
| Redundant-file removal | Delivery lead | Implemented locally | Four exact duplicate aliases, 336,837 bytes; [hashes and retained paths](2026-11-16-deduplication.json); validate and release |
| Strong/weak comparison | Research worker | In progress | Lock Codex exploratory predictions before current automatic judgments; preserve previous failed numeric mutation results |
| Engine modules | Engineering worker | In progress | Isolated worktree; compare all substantive output bytes, record changed source fingerprint honestly |
| Reader summaries | Delivery lead | Partial | Preserve authored reasoning; separate summary field and jargon check |
| Shorter documentation | Delivery lead | In progress | Site guide and local setup already separate in PR #124; shorten entry points without losing technical instructions |
| Public read-only Site | Delivery lead | Pending | Separate public content/build; preserve private working workspace |
| Hosted export acceptance | Delivery lead | Pending | Inspect actual downloaded Markdown/JSON and persisted run |
| User/device acceptance | Product owner | Pending | Physical phone and screen reader observations; not established by browser emulation |

Historical generated assessments are not byte-identical copies. They retain
distinct source/processing evidence and were not deleted. Ten broken anchors
in the current generated report require a renderer correction; four historical
anchor defects do not justify deleting their unique reports.
