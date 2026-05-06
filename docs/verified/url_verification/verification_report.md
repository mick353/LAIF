# URL Verification Report

**Framework:** Law-Aligned Intelligence Framework v1.2  
**Verification attempt date:** May 2026  
**Verification method:** Automated HTTP GET from assessment session  
**Verification scope:** Existence and accessibility of authoritative source URLs

---

## Summary

| Document | URL | HTTP Status | Content Accessible | Byte-Hash Comparable | Action Required |
|---|---|---|---|---|---|
| OECD Recommendation | legalinstruments.oecd.org | 403 Forbidden | No | No | Human browser access |
| EO 14110 | federalregister.gov | 403 Forbidden | No | No | Human browser access |
| NIST AI 100-1 | doi.org/10.6028/NIST.AI.100-1 | 403 Forbidden | No | No | Human browser access |
| DTAC v2.0 | transform.england.nhs.uk | 403 Forbidden | No | No | Human browser access |
| EU AI Act | eur-lex.europa.eu | 403 Forbidden | No | No | Human browser access |

---

## Interpretation of HTTP 403

**HTTP 403 Forbidden** means:
- The URL exists and the server is reachable (not a DNS failure or connection timeout)
- The server is actively denying access to the automated requester
- This is consistent with bot-blocking, rate-limiting, or geographic/agent restrictions
- It does **not** mean the URL is invalid or the document has moved

**What 403 does NOT verify:**
- That the document content at the URL matches our extracted markdown
- That the document has not been updated since our ingestion
- Byte-identical equivalence between our corpus files and the live URL

**What 403 DOES establish:**
- The authoritative URL is structurally valid (server responds)
- The server actively blocks automated retrieval from this environment
- Human-initiated browser access is required for content verification

---

## Individual Verification Records

### 1. OECD Recommendation on AI

**URL tested:** https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449  
**HTTP status:** 403 Forbidden  
**Timestamp:** May 2026 (automated session)  
**Content retrieved:** None  
**Byte comparison performed:** No  
**Hash comparison performed:** No  

**Corpus file:** `docs/verified/raw/51a29205-OECD_Legal_Instruments.md`  
**Corpus SHA256:** `f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6`  
**Corpus provenance:** User-supplied document; strict source mode ingestion  

**Verification status:** URL CONFIRMED RESPONSIVE — CONTENT NOT ACCESSIBLE FROM THIS SESSION  
**Gap:** Byte-identical equivalence between corpus file and live URL not verified.  
**Action:** Human maintainer to access URL via browser, download document, and compare SHA256 against corpus SHA256.

---

### 2. Executive Order 14110

**URL tested:** https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence  
**HTTP status:** 403 Forbidden  
**Timestamp:** May 2026 (automated session)  
**Content retrieved:** None  
**Byte comparison performed:** No  
**Hash comparison performed:** No  

**Corpus file:** `docs/verified/raw/b0ef43db-202324283.md`  
**Corpus SHA256:** `2cbab055409a522549028185c017fa6e450e86bb8fc305a7d0048ad1f6d341c5`  
**Corpus provenance:** User-supplied document; strict source mode ingestion  
**Note:** EO 14110 was revoked 20 January 2025. The Federal Register record is an archival document.  

**Verification status:** URL CONFIRMED RESPONSIVE — CONTENT NOT ACCESSIBLE FROM THIS SESSION  
**Gap:** Byte-identical equivalence not verified.  
**Action:** Human maintainer to access Federal Register URL; download plain text; compare SHA256.

---

### 3. NIST AI 100-1

**URL tested:** https://doi.org/10.6028/NIST.AI.100-1  
**HTTP status:** 403 Forbidden  
**Timestamp:** May 2026 (automated session)  
**Content retrieved:** None  
**Byte comparison performed:** No  
**Hash comparison performed:** No  

**Corpus file:** `docs/verified/raw/5f667a6f-NIST.AI.1001.md`  
**Corpus SHA256:** `44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509`  
**Corpus provenance:** User-supplied DOCX; python-docx extraction; strict source mode  
**Additional gap:** Corpus derived from DOCX, not from the authoritative PDF. Two-step verification needed: (1) confirm PDF content matches DOCX; (2) confirm extracted markdown matches PDF content.

**Verification status:** URL CONFIRMED RESPONSIVE — CONTENT NOT ACCESSIBLE FROM THIS SESSION  
**Gap:** Both DOCX-vs-PDF and markdown-vs-PDF equivalence unverified.  
**Action:** Human maintainer to download PDF from doi.org/10.6028/NIST.AI.100-1; extract text; compare against corpus markdown.

---

### 4. DTAC v2.0

**URL tested:** https://transform.england.nhs.uk/key-tools-and-info/digital-technology-assessment-criteria-dtac/  
**HTTP status:** 403 Forbidden  
**Timestamp:** May 2026 (automated session)  
**Content retrieved:** None  
**Byte comparison performed:** No  
**Hash comparison performed:** No  

**Corpus file:** `docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md`  
**Corpus SHA256:** `d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811`  
**Corpus provenance:** User-supplied document; strict source mode ingestion  
**Note:** NHS England may update DTAC without version change. Verification should confirm DTAC Form 2.0 dated February 2026 is still the current version.

**Verification status:** URL CONFIRMED RESPONSIVE — CONTENT NOT ACCESSIBLE FROM THIS SESSION  
**Gap:** Byte-identical equivalence not verified; current version status not confirmed.  
**Action:** Human maintainer to access NHS England URL; download DTAC Form 2.0 (February 2026); compare SHA256.

---

### 5. EU AI Act

**URL tested:** https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689  
**URL tested (HTML):** https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689  
**HTTP status:** 403 Forbidden (both variants)  
**Timestamp:** May 2026 (automated session)  
**Content retrieved:** None  

**Corpus file:** None — ingestion BLOCKED  
**Verification status:** URL CONFIRMED RESPONSIVE — CONTENT NOT ACCESSIBLE FROM THIS SESSION  
**Note:** This document is not yet in the corpus. URL verification here confirms the authoritative source URL is structurally valid.

---

## Verification Methodology for Human Maintainer

To complete URL verification for each document:

1. Access the authoritative URL via a standard browser session
2. Download the document in its canonical format (PDF for NIST; HTML or PDF for OECD/EO/DTAC)
3. If PDF: extract plain text using `pdftotext` or equivalent; save as `.txt`
4. Compute SHA256 of the downloaded/extracted text file
5. Compare against the SHA256 recorded in `docs/verified/manifests/<document_id>.json`
6. Record: retrieval date, SHA256 of downloaded file, comparison result, any discrepancies
7. Update the manifest with `retrieval_date_utc` and verification outcome
8. Update this report with actual comparison results

**Note on transformation chain:** Our corpus files are NORMALISED_FORMATTING_ONLY — plain text with markdown heading syntax and pipe tables. A byte-identical comparison against a raw PDF extraction will not succeed. The comparison is structural and textual: same content, same section ordering, no omissions, no insertions.

---

## Outstanding Status

This verification pass established that all five authoritative URLs are server-responsive (HTTP 403 is a server response, not a network failure). Content verification requires human-initiated access. No byte-identical equivalence claims are made.

**Date of next required verification:** Before any publication claim that corpus files are equivalent to live authoritative sources.

---

*Generated: May 2026 · LAIF v1.2 · Verified Corpus URL Verification Report*
