# EXTRACTION FAILURE NOTICE

**File:** 5f667a6f-NIST.AI.1001.pdf  
**Document:** NIST AI 100-1 — Artificial Intelligence Risk Management Framework (AI RMF 1.0)  
**Publisher:** National Institute of Standards and Technology (NIST), U.S. Department of Commerce  
**Status:** EXTRACTION FAILED — content not ingested  

---

## Failure Reason

PDF text extraction failed. No PDF extraction tools are available in this environment:

- `pdftotext` (poppler-utils) — NOT INSTALLED  
- `PyPDF2` — NOT AVAILABLE  
- `pdfplumber` — NOT AVAILABLE  
- `pymupdf` / `fitz` — NOT AVAILABLE  
- `ghostscript` — NOT INSTALLED  

The file is a 1.9 MB, 20-page PDF. Stream-level binary extraction retrieved only 49 fragmented text segments (non-contiguous, insufficient for faithful transcription).

## Strict Source Mode Compliance

Per task rules: **NO content has been inferred, reconstructed, or sourced from training data.**  
This file must be re-ingested once an appropriate extraction tool is available.

## Required Action

To complete ingestion of this document:

1. Install `poppler-utils` (`apt-get install poppler-utils`) — provides `pdftotext`  
   OR install `pdfplumber` (`pip install pdfplumber`)
2. Re-run ingestion for this file only
3. Place output at: `docs/supporting/5f667a6f-NIST.AI.1001.md`
4. Remove this failure notice file

## Document Metadata (From Filename/Context)

- **Title:** Artificial Intelligence Risk Management Framework (AI RMF 1.0)  
- **NIST Identifier:** NIST AI 100-1  
- **Publisher:** National Institute of Standards and Technology  
- **Relevance to LAIF:** LAIF v1.2 integrates with NIST AI RMF; mapped function-by-function in Regulatory Integration Guide Part Two  
