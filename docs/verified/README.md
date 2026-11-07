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
| EU AI Act | Not present | Custody PDF held; PENDING_INGESTION |

The `docs/supporting/` files are the **primary source** of the four instruments assessed in `reports/laif_full_assessment.md`. The `docs/verified/` tree adds provenance manifests and hash verification around those same sources.


## Manual Ingestion

When automated URL retrieval is blocked, authoritative sources may be supplied through `HUMAN_GITHUB_DEPOSIT` or `HUMAN_SESSION_UPLOAD`. Exact supplied files are staged in `docs/verified/manual_ingest/`; authority is established by the manifest record, SHA256 hashes, transformation chain, citation status, provenance classification, and verification status. See `MANUAL_INGESTION_WORKFLOW.md`.

## Portable processing of newly deposited sources

The DTA v2.1 and EU Regulation 2026/1744 PDFs are held in `manual_ingest/` on PR #98. Source-specific manifests, full page-delimited extractions, exact quotation traces and separate assessments are now recorded in the [7 November review](../verification/2026-11-07/regulatory/README.md). Until merged, these are review artefacts, not canonical `main` results.

From **any Python 3.10+ environment with a clone of this branch**, the reviewed-text route requires only the standard library:

```bash
python3 scripts/laif_verify_regulatory_ingestion.py
python3 scripts/laif_process_regulatory_sources.py --verified-text --output-dir /tmp/laif-regulatory-review
```

For direct PDF extraction, install optional `pypdf` in a virtual environment and run:

```bash
python3 -m pip install pypdf
python3 scripts/laif_process_regulatory_sources.py --output-dir /tmp/laif-regulatory-review
```

The runner uses the canonical `laif_process_document.py` engine for both files and writes source SHA-256 identities, assessment outputs and a JSON run manifest. It fails on missing/invalid PDFs and processor errors. This is a **documentary processing entry point**, not an automated admission to `PRIMARY_CITABLE` or a legal-compliance verdict. Source admission is recorded separately under `MANUAL_INGESTION_WORKFLOW.md`; the runner itself does not promote sources. `--verified-text` checks pinned raw/PDF hashes and uses explicit instrument context, avoiding the documented pypdf spacing damage. Its assessment source hash identifies extracted text; the run manifest links it to the PDF hash. The script does not create a hosted execution service or require GitHub Actions.

## Ingestion Constraints

All documents in this corpus were ingested under the following constraints:

- No paraphrasing
- No summarisation
- No semantic rewriting
- No content derived from training data
- Formatting normalisation only (markdown structure, heading levels)
- SHA256 hash recorded at ingestion time

## Limitations

- Legacy sources retain their historical URL-verification limitations. The 2026 EU amendment has automated upstream byte equivalence; DTA v2.1 is human-attested after two HTTP 503 responses.
- Legacy hashes are of extracted markdown. The two new regulatory records separately pin original PDF and extracted-text SHA-256 hashes.
- EU AI Act full text not yet ingested — marked PENDING_INGESTION in manifest

---

*LAIF v1.2 · April 2026*
