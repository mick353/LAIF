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
| EU AI Act original OJ edition | Full 144-page extract | Official PDF byte-matched; PENDING_ASSESSMENT |

The `docs/supporting/` files are the **primary source** of the four instruments assessed in `reports/laif_full_assessment.md`. The `docs/verified/` tree adds provenance manifests and hash verification around those same sources.


## Manual Ingestion

When automated URL retrieval is blocked, authoritative sources may be supplied through `HUMAN_GITHUB_DEPOSIT` or `HUMAN_SESSION_UPLOAD`. Exact supplied files are staged in `docs/verified/manual_ingest/`; authority is established by the manifest record, SHA256 hashes, transformation chain, citation status, provenance classification, and verification status. See [the manual ingestion workflow](../../MANUAL_INGESTION_WORKFLOW.md).

## Portable processing of newly deposited sources

The DTA v2.1 and EU Regulation 2026/1744 PDFs are held in `manual_ingest/` and were released with their source records and assessments through merged PR #100. Source-specific manifests, full page-delimited extractions, exact quotation traces and separate assessments are now recorded in the [7 November review](../verification/2026-11-07/regulatory/README.md). They are available on `main`. Human-attested DTA origin remains distinct from independently byte-matched EU origin; assessment publication does not prove implementation or legal compliance.

From **any Python 3.10+ environment with a clone of the repository**, the reviewed-text route requires only the standard library:

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

- The four legacy assessed sources retain their historical upstream-equivalence limitations. The original 2024 EU Act is ingested and byte-matched to an official Publications Office PDF; the 2026 amendment also matches official bytes. DTA v2.1 remains human-attested after HTTP 503 responses.
- Legacy raw hashes identify extracted markdown. The original EU Act and both newer regulatory records separately identify original PDF and extracted-text SHA-256 hashes.
- The original EU Act's full-document assessment remains pending. The 2026 amendment assessment is separate, not a consolidated-law certificate. Extracted source text is not an exhaustive manually proofread transcription.

---

*LAIF v1.2 · April 2026*
