# LAIF Verified Corpus Manifest

**Framework:** Law-Aligned Intelligence Framework v1.2  
**Manifest version:** 1.0  
**Original index:** May 2026; EU source status updated 30 October 2026
**Schema:** `verified_manifest_schema.json`

This manifest provides a human-readable index of all documents in the LAIF verified corpus. Machine-readable provenance records are in `docs/verified/manifests/*.json`.

---

## Corpus Status Overview

| # | Document | Jurisdiction | Provenance | Hash | Assessment |
|---|---|---|---|---|---|
| 1 | OECD Recommendation on AI (OECD/LEGAL/0449) | International | AUTHORITATIVE_PRIMARY_SOURCE | Verified | ASSESSED |
| 2 | EO 14110 (Federal Register Vol. 88 No. 210) | US Federal | AUTHORITATIVE_GOVERNMENT_PUBLICATION | Verified | ASSESSED |
| 3 | NIST AI 100-1 (AI RMF 1.0) | US Federal | AUTHORITATIVE_GOVERNMENT_PUBLICATION | Verified | ASSESSED |
| 4 | DTAC v2.0 (NHS England, Feb 2026) | UK (NHS England) | REGULATORY_PUBLICATION | Verified | ASSESSED |
| 5 | EU AI Act (Regulation 2024/1689), original OJ edition | European Union | AUTHORITATIVE_PRIMARY_SOURCE | PDF and raw extract hash-verified | PENDING_ASSESSMENT |

---

## Document Records

### 1. OECD Recommendation on Artificial Intelligence

| Field | Value |
|---|---|
| document_id | `51a29205-OECD_Legal_Instruments` |
| title | Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449) |
| jurisdiction | International (OECD member states and adherents — 46 as of 2024) |
| source_type | international_recommendation |
| authoritative_url | https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449 |
| retrieval_method | user_supplied_document_strict_source_mode |
| publication_date | 2024 (2019 original; 2024 revision) |
| version_identifier | OECD/LEGAL/0449 (2024 revision) |
| sha256_hash | `f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6` |
| raw_filename | `51a29205-OECD_Legal_Instruments.md` |
| extraction_boundaries | Full document |
| transformation_status | NORMALISED_FORMATTING_ONLY |
| citation_status | PRIMARY_CITABLE |
| provenance_classification | AUTHORITATIVE_PRIMARY_SOURCE |
| assessment_status | ASSESSED |
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 1 (narrative analysis, 5 May 2026, Refined Model v1.1 — historical; see `reports/README.md`) |

**Provenance notes:** Ingested from user-supplied document in Strict Source Mode. No training-derived content used. URL verification against authoritative source not performed (no network access during ingestion). SHA256 is of the extracted markdown file at `docs/verified/raw/51a29205-OECD_Legal_Instruments.md`.

---

### 2. Executive Order 14110

| Field | Value |
|---|---|
| document_id | `b0ef43db-202324283` |
| title | Executive Order 14110: Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence |
| jurisdiction | United States (Federal) |
| source_type | executive_directive |
| authoritative_url | https://www.federalregister.gov/documents/2023/11/01/2023-24283/ |
| retrieval_method | user_supplied_document_strict_source_mode |
| publication_date | 2023-10-30 |
| version_identifier | Federal Register Vol. 88 No. 210 |
| sha256_hash | `2cbab055409a522549028185c017fa6e450e86bb8fc305a7d0048ad1f6d341c5` |
| raw_filename | `b0ef43db-202324283.md` |
| extraction_boundaries | Full document |
| transformation_status | NORMALISED_FORMATTING_ONLY |
| citation_status | PRIMARY_CITABLE |
| provenance_classification | AUTHORITATIVE_GOVERNMENT_PUBLICATION |
| assessment_status | ASSESSED |
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 2 (narrative analysis, 5 May 2026, Refined Model v1.1 — historical; see `reports/README.md`) |

**Provenance notes:** Revoked by Presidential action on 20 January 2025. Assessment reflects the instrument as in force at publication date (30 October 2023). SHA256 is of the extracted markdown. URL verification not performed during ingestion session.

---

### 3. NIST AI 100-1 (AI Risk Management Framework 1.0)

| Field | Value |
|---|---|
| document_id | `5f667a6f-NIST.AI.1001` |
| title | Artificial Intelligence Risk Management Framework (AI RMF 1.0) — NIST AI 100-1 |
| jurisdiction | United States (Federal) |
| source_type | voluntary_framework |
| authoritative_url | https://doi.org/10.6028/NIST.AI.100-1 |
| retrieval_method | user_supplied_docx_strict_source_mode |
| publication_date | 2023-01 |
| version_identifier | NIST AI 100-1 (January 2023) |
| sha256_hash | `44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509` |
| raw_filename | `5f667a6f-NIST.AI.1001.md` |
| extraction_boundaries | Full document |
| transformation_status | NORMALISED_FORMATTING_ONLY |
| citation_status | PRIMARY_CITABLE |
| provenance_classification | AUTHORITATIVE_GOVERNMENT_PUBLICATION |
| assessment_status | ASSESSED |
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 3 (narrative analysis, 5 May 2026, Refined Model v1.1 — historical; see `reports/README.md`) |

**Provenance notes:** Original PDF was unextractable (no PDF tooling available in ingestion session). User supplied a DOCX replacement. Extracted using python-docx with namespace-aware heading detection (`w:pStyle`). Content is verbatim from the DOCX; DOCX accuracy against the authoritative PDF was not independently verified. SHA256 is of the extracted markdown.

---

### 4. Digital Technology Assessment Criteria v2.0 (DTAC)

| Field | Value |
|---|---|
| document_id | `55eccce3-DTAC_Form_2.0_February_2026` |
| title | Digital Technology Assessment Criteria (DTAC) v2.0 |
| jurisdiction | United Kingdom (NHS England) |
| source_type | procurement_standard |
| authoritative_url | https://transform.england.nhs.uk/key-tools-and-info/digital-technology-assessment-criteria-dtac/ |
| retrieval_method | user_supplied_document_strict_source_mode |
| publication_date | 2026-02-24 |
| version_identifier | DTAC Form 2.0 (February 2026) |
| sha256_hash | `d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811` |
| raw_filename | `55eccce3-DTAC_Form_2.0_February_2026.md` |
| extraction_boundaries | Full document |
| transformation_status | NORMALISED_FORMATTING_ONLY |
| citation_status | PRIMARY_CITABLE |
| provenance_classification | REGULATORY_PUBLICATION |
| assessment_status | ASSESSED |
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 4 (narrative analysis, 5 May 2026, Refined Model v1.1 — historical; see `reports/README.md`) |

**Provenance notes:** NHS England procurement standard operative within the NHS England digital procurement process. Ingested from user-supplied document in Strict Source Mode. URL verification not performed. SHA256 is of the extracted markdown.

---

### 5. EU AI Act — Regulation (EU) 2024/1689 *(source verified; assessment pending)*

| Field | Value |
|---|---|
| document_id | `eu-ai-act-2024-1689` |
| title | Regulation (EU) 2024/1689 of the European Parliament and of the Council |
| jurisdiction | European Union |
| source_type | binding_regulation |
| authoritative_url | https://op.europa.eu/en/publication-detail/-/publication/dc8116a1-3fe6-11ef-865a-01aa75ed71a1/language-en |
| publication_date | 2024-07-12 |
| source_file_sha256 | `bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e` |
| sha256_hash | `7fb1ae279b6353a9da6bf7dd82218f3cfb2329cc1f9f1512aa269bc4985fe697` |
| raw_filename | `eu_ai_act_2024_1689.md` |
| extraction_boundaries | All 144 pages of the original Official Journal edition |
| transformation_status | NORMALISED_FORMATTING_ONLY |
| citation_status | PRIMARY_CITABLE for the original source; verify quoted clauses against PDF pages |
| provenance_classification | AUTHORITATIVE_PRIMARY_SOURCE |
| verification_status | AUTOMATED_VERIFIED; official PDF exactly matches preserved custody PDF |
| assessment_status | **PENDING_ASSESSMENT** |

**Provenance notes:** The official Publications Office original-edition PDF was downloaded on 30 October 2026 and matched the preserved May custody PDF byte for byte. All pages were extracted without intentional wording changes. See the [ingestion trace](docs/verified/extracted/eu-ai-act-2024-1689-ingestion-trace.md). The extract has not been proofread line by line; no full-document LAIF assessment is recorded. Later consolidated editions are distinct. The `sample_documents.py` excerpt remains non-citable regardless of this source admission.

---

## Corpus Limitations

1. **Legacy URL verification gap** — the four previously assessed documents came from user-supplied files. Their assessed raw-text upstream equivalence remains unproven. The EU AI Act original PDF was independently byte-matched to an official download on 30 October 2026.

2. **NIST DOCX provenance** — the NIST AI 100-1 ingestion relied on a user-supplied DOCX. The DOCX accuracy against the authoritative PDF has not been independently verified.

3. **EU AI Act assessment gap** — the original OJ full text is admitted as a source, but no reviewed full-document LAIF assessment exists. Existing representative-excerpt results remain non-citable and must not be promoted.

4. **SHA256 scope** — raw-file hashes are of the extracted Markdown. The EU AI Act manifest additionally records an original PDF hash matched to an official download; other raw-file hashes alone do not certify source-byte identity.

---

*LAIF v1.2 · Verified Corpus Manifest v1.0 · May 2026, EU source update October 2026*


## EU AI Act Source Admission

The original OJ edition of Regulation (EU) 2024/1689 is `SOURCE_VERIFIED_PENDING_ASSESSMENT`. The former readiness record at `docs/verified/pending/eu_ai_act_ingestion_ready.md` is retained as history. Source verification and ingestion do not constitute a reviewed full-document assessment or current-law determination.


## Current Verification Taxonomy

| Document | acquisition_channel | verification_status | network_status | Notes |
|---|---|---|---|---|
| OECD Recommendation | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Local raw markdown hash verified; upstream equivalence not claimed |
| EO 14110 | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Local raw markdown hash verified; upstream equivalence not claimed |
| NIST AI 100-1 | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Local raw markdown hash verified; PDF-vs-DOCX remains unresolved |
| DTAC v2.0 | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Local raw markdown hash verified; upstream equivalence not claimed |
| EU AI Act original OJ edition | AUTOMATED_URL_RETRIEVAL | AUTOMATED_VERIFIED | AUTOMATED_URL_RETRIEVED | Official PDF matched preserved custody file; full assessment pending |
