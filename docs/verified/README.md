# LAIF Verified Corpus

**Framework:** Law-Aligned Intelligence Framework v1.2  
**Corpus type:** Authoritative source documents — full-text ingestion, Strict Source Mode  
**Status:** Distinct from `docs/supporting/` (representative baseline corpus)

---

## Directory Structure

```
docs/verified/
├── README.md              — this file
├── raw/                   — full-text ingestions from user-supplied authoritative sources
├── extracted/             — bounded evidence traces documenting assessment citations
├── manifests/             — provenance JSON manifests, one per document
├── manual_ingest/         — exact human-supplied authoritative files awaiting processing
├── pending/               — readiness records for documents awaiting manual ingestion
└── url_verification/      — automated URL verification attempt records
```

## Corpus vs Representative Baseline

| Property | `docs/supporting/` | `docs/verified/` |
|---|---|---|
| Purpose | Representative baseline corpus | Authoritative source corpus |
| Provenance | Strict Source Mode ingestion | Strict Source Mode + manifest |
| Citeability | PRIMARY_CITABLE (full text, no paraphrase) | PRIMARY_CITABLE + hash-verified |
| Hash recorded | No | Yes (SHA256 of extracted markdown) |
| EU AI Act | Not ingested | PENDING_INGESTION |

The `docs/supporting/` files are the **primary source** of the four instruments assessed in `reports/laif_full_assessment.md`. The `docs/verified/` tree adds provenance manifests and hash verification around those same sources.


## Manual Ingestion

When automated URL retrieval is blocked, authoritative sources may be supplied through `HUMAN_GITHUB_DEPOSIT` or `HUMAN_SESSION_UPLOAD`. Exact supplied files are staged in `docs/verified/manual_ingest/`; authority is established by the manifest record, SHA256 hashes, transformation chain, citation status, provenance classification, and verification status. See `MANUAL_INGESTION_WORKFLOW.md`.

## Ingestion Constraints

All documents in this corpus were ingested under the following constraints:

- No paraphrasing
- No summarisation
- No semantic rewriting
- No content derived from training data
- Formatting normalisation only (markdown structure, heading levels)
- SHA256 hash recorded at ingestion time

## Limitations

- URL verification against authoritative online sources was not performed during ingestion (no network access in ingestion session)
- SHA256 hashes are of the extracted markdown files, not the original PDF/DOCX source files
- EU AI Act full text not yet ingested — marked PENDING_INGESTION in manifest

---

*LAIF v1.2 · April 2026*
