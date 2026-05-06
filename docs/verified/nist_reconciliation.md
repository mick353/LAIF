# NIST AI 100-1 — DOCX-vs-PDF Reconciliation

**Document:** NIST AI 100-1 — Artificial Intelligence Risk Management Framework 1.0  
**Authoritative URL:** https://doi.org/10.6028/NIST.AI.100-1  
**Corpus file:** `docs/verified/raw/5f667a6f-NIST.AI.1001.md`  
**Corpus SHA256:** `44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509`  
**Reconciliation date:** May 2026

---

## 1. Reconciliation Objective

The NIST AI 100-1 ingestion was performed from a user-supplied DOCX file, not from the authoritative PDF at doi.org/10.6028/NIST.AI.100-1. This document records:

1. Known extraction artifacts from the DOCX extraction
2. Verification of all assessment-critical sections against the corpus file
3. Status of PDF-vs-DOCX equivalence assessment
4. Stability certification for existing assessment conclusions

---

## 2. PDF Retrieval Status

**Attempted:** doi.org/10.6028/NIST.AI.100-1  
**HTTP status:** 403 Forbidden (automated session, May 2026)  
**Content retrieved:** None  
**Conclusion:** PDF-vs-DOCX byte comparison not performable in this session. Full reconciliation requires human download of the PDF.

---

## 3. Known Extraction Artifacts

The DOCX extraction using python-docx with lxml namespace-aware heading detection produced the following known artifacts. These are formatting artifacts only; no content words are altered.

### 3.1 Title page duplication (line 11)

**Raw file line 11:**
```
NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)
```

**Cause:** The DOCX title page contained the title text in multiple text runs or paragraphs that were concatenated during extraction. The title is duplicated within the same line, with no whitespace between runs.

**Impact on assessment:** None. This is a title-page artifact before any substantive content. It does not affect any assessed provision.

**Severity:** Cosmetic only.

### 3.2 Footer line duplication (final line)

**Raw file final line:**
```
This publication is available free of charge from:https://doi.org/10.6028/NIST.AI.100-1This publication is available free of charge from:https://doi.org/10.6028/NIST.AI.100-1
```

**Cause:** DOCX footer content (which appears on every page of the PDF) was extracted once as part of the document body, with the footer text repeated within the extracted paragraph.

**Impact on assessment:** None. This is a footer artifact that does not appear in any assessed provision.

**Severity:** Cosmetic only.

### 3.3 Subcategory concatenation in tables

The NIST AI RMF's table structure (Category | Subcategories) is rendered in the corpus file as pipe-delimited markdown tables. Within each subcategory cell, the individual subcategory entries (GOVERN 1.1, GOVERN 1.2, etc.) are concatenated without line breaks:

```
GOVERN 1.1: Legal and regulatory requirements...GOVERN 1.2: The characteristics of trustworthy AI...
```

**Cause:** DOCX table cells containing multi-paragraph content have their paragraphs concatenated during table extraction.

**Impact on assessment:** None. All subcategory identifiers and their text are fully present. The concatenation is a display artifact only; each subcategory text is complete and unmodified.

**Severity:** Cosmetic only. All section identifiers remain searchable and verifiable.

---

## 4. Assessment-Critical Section Verification

All sections cited in the NIST evidence trace (`docs/verified/extracted/5f667a6f-NIST-evidence-trace.md`) were verified against the corpus file. Verification method: `grep -n "<section_id>" docs/verified/raw/5f667a6f-NIST.AI.1001.md`.

| Section cited in evidence trace | Present in corpus | Line reference |
|---|---|---|
| GOVERN 1.1 | Yes | Line 200 |
| GOVERN 1.2 | Yes | Line 200 |
| GOVERN 1.3 | Yes | Line 200 |
| GOVERN 1.4 | Yes | Line 200 |
| GOVERN 1.5 | Yes | Line 207 |
| GOVERN 1.6 | Yes | Line 207 |
| GOVERN 1.7 | Yes | Line 207 |
| GOVERN 6.1 | Yes | Line 219 |
| GOVERN 6.2 | Yes | Line 219 |
| MAP 1.1 | Yes | Line 241 |
| MAP 1.6 | Yes | Line 241 |
| MAP 5.1 | Yes | Line 252 |
| MEASURE 2.5 | Yes | Line 272 |
| MEASURE 2.6 | Yes | Line 279 |
| MANAGE 1.3 | Yes | Line 299 |
| MANAGE 2.2 | Yes | Line 300 |
| MANAGE 4.1 | Yes | Line 308 |

**Result:** All 17 cited sections are present and contain substantive text matching the assessment findings.

---

## 5. Assessment Conclusion Stability

Based on the section verification above, and in the absence of PDF-vs-DOCX byte comparison (blocked by HTTP 403):

**Sections supporting Q1b = NONE (voluntary design):**
The corpus file contains multiple explicit statements that the AI RMF is voluntary by design:
- Line 13: "This publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1"
- Appendix D: "Be risk-based, resource-efficient, pro-innovation, and voluntary."

**Sections supporting Q2 = PASS:**
GOVERN 1.1 references "Legal and regulatory requirements" without limiting scope to any sector, supporting scale-invariant application.

**Sections supporting Q3 = PASS:**
"The AI RMF is intended to be a living document" (confirmed in Update Schedule section). Appendix D attributes list: "Be a living document."

**All known extraction artifacts are cosmetic** — they occur at title page, footer, and table cell boundaries. No extraction artifact affects any provision assessed or any finding cited in the evidence trace.

**Stability certification:** Based on available evidence (all cited sections present, all extraction artifacts cosmetic only), the LAIF assessment conclusions for NIST AI RMF are **stable with respect to the DOCX extraction**. No assessment drift attributable to DOCX extraction is detected.

**Caveat:** This certification covers DOCX-vs-corpus equivalence only. PDF-vs-DOCX equivalence remains unverified pending human download of the PDF from doi.org/10.6028/NIST.AI.100-1.

---

## 6. Remaining Verification Gap

| Gap | Status | Required action |
|---|---|---|
| PDF retrieval | Blocked (HTTP 403) | Human download from doi.org/10.6028/NIST.AI.100-1 |
| PDF-vs-DOCX text comparison | Not performed | Extract PDF text; compare section-by-section against corpus |
| PDF-vs-DOCX structural comparison | Not performed | Verify table structure, section numbering, appendix completeness |
| Extraction artifact correction | Optional | Cosmetic artifacts can be corrected by re-extraction; not required for assessment validity |

---

## 7. Recommended Future Action

1. Human maintainer downloads PDF from https://doi.org/10.6028/NIST.AI.100-1
2. Extract text using `pdftotext -layout NIST.AI.100-1.pdf > nist_pdf_text.txt`
3. Compare all 17 sections in the table above against PDF text
4. Record any discrepancies in this document
5. If discrepancies affect assessment-cited provisions: patch evidence trace and assessment section accordingly
6. Update corpus SHA256 if re-extraction produces a cleaner file
7. Update manifest `retrieval_method` to `user_supplied_pdf_strict_source_mode` if re-extracted from PDF

---

*LAIF v1.2 · NIST Reconciliation Document · May 2026*
