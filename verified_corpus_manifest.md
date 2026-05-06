# LAIF Verified Corpus Manifest

**Framework:** Law-Aligned Intelligence Framework v1.2  
**Manifest version:** 1.0  
**Date:** May 2026  
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
| 5 | EU AI Act (Regulation 2024/1689) | European Union | AUTHORITATIVE_PRIMARY_SOURCE | Not ingested | PENDING_INGESTION |

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
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 1 |

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
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 2 |

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
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 3 |

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
| assessment_reference | `reports/laif_full_assessment.md` — Assessment 4 |

**Provenance notes:** NHS England procurement standard operative within the NHS England digital procurement process. Ingested from user-supplied document in Strict Source Mode. URL verification not performed. SHA256 is of the extracted markdown.

---

### 5. EU AI Act — Regulation (EU) 2024/1689 *(PENDING)*

| Field | Value |
|---|---|
| document_id | `eu-ai-act-2024-1689` |
| title | Regulation (EU) 2024/1689 of the European Parliament and of the Council |
| jurisdiction | European Union |
| source_type | binding_regulation |
| authoritative_url | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689 |
| publication_date | 2024-07-12 |
| citation_status | NON_CITABLE |
| provenance_classification | AUTHORITATIVE_PRIMARY_SOURCE |
| assessment_status | **PENDING_INGESTION** |

**Provenance notes:** Not yet ingested as authoritative full text. Currently exists only as a REPRESENTATIVE_EXCERPT in `sample_documents.py` — that excerpt is non-citable and not suitable for authoritative assessment. Full-text ingestion from EUR-Lex is required before a LAIF v1.2 assessment can be conducted against this instrument as a PRIMARY_CITABLE source.

---

## Corpus Limitations

1. **URL verification not performed** — the four ingested documents were sourced from user-supplied files. Verification against the authoritative URLs listed above was not performed during ingestion. A future verification pass should download the documents from their authoritative URLs and compare SHA256 hashes.

2. **NIST DOCX provenance** — the NIST AI 100-1 ingestion relied on a user-supplied DOCX. The DOCX accuracy against the authoritative PDF has not been independently verified.

3. **EU AI Act gap** — the EU AI Act is not represented in the verified corpus. Any assessment claims referencing the EU AI Act draw only on the REPRESENTATIVE_EXCERPT in `sample_documents.py` (which is non-citable).

4. **SHA256 scope** — hashes are of the extracted markdown files, not the original PDF/DOCX source files. They guarantee integrity of the ingested text within this repository but do not certify identity with the source file bytes.

---

*LAIF v1.2 · Verified Corpus Manifest v1.0 · May 2026*
