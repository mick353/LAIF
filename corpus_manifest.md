# LAIF Assessment — Corpus Manifest

**Generated:** May 2026  
**Framework:** LAIF v1.2 · Compliance Toolkit v1.1

This manifest documents every document in `sample_documents.py`, its provenance
classification, accuracy status, and intended role in the LAIF assessment corpus.

---

## Provenance Classifications

| Code | Meaning |
|------|---------|
| `OFFICIAL_EXCERPT` | Verified verbatim text from the authoritative source. Citable as primary evidence. |
| `REPRESENTATIVE_EXCERPT` | Condensed paraphrase or illustrative excerpt capturing governance intent of a real framework. **Not verbatim. Not citable as the primary source.** |
| `SYNTHETIC_TEST_DOCUMENT` | Constructed for adversarial or stress-testing; does not represent any real-world governance document. |

---

## Corpus Documents

| # | Document Name | Source Type | Jurisdiction | Year | Provenance | Citable? | Intended Use |
|---|---------------|-------------|--------------|------|------------|----------|--------------|
| 1 | EU AI Act — Art. 9, 13 & 14 | binding_regulation | European Union | 2024 | REPRESENTATIVE_EXCERPT | No | real-world baseline |
| 2 | NIST AI RMF — Govern & Map Functions | voluntary_framework | United States | 2023 | REPRESENTATIVE_EXCERPT | No | real-world baseline |
| 3 | OECD AI Principles (2019, rev. 2024) | international_principles | International (OECD) | 2024 | REPRESENTATIVE_EXCERPT | No | real-world baseline |
| 4 | US Executive Order 14110 — §4 Safety & §7 Workers | executive_directive | United States (Federal) | 2023 | REPRESENTATIVE_EXCERPT | No | real-world baseline + paraphrase stress-test |
| 5 | NHS England — AI in Clinical Decision Support | sector_policy | United Kingdom | 2024 | REPRESENTATIVE_EXCERPT | No | sector scenario — clinical AI |
| 6 | TUC/CIPD — Framework for Fair AI in Employment Decisions | sector_policy | United Kingdom | 2024 | REPRESENTATIVE_EXCERPT | No | sector scenario — employment AI |

---

## Source URLs

| # | Document | Source URL | Accuracy Note |
|---|----------|-----------|---------------|
| 1 | EU AI Act | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689 | Condensed paraphrase of Arts. 9, 13, 14. Verify against OJ publication. |
| 2 | NIST AI RMF | https://airc.nist.gov/RMF | British spelling 'organisational' departs from American-English original. |
| 3 | OECD AI Principles | https://oecd.ai/en/ai-principles | Structural numbering preserved; wording is not verbatim. |
| 4 | US EO 14110 | https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence | Paraphrased; contains embedded LAIF paraphrase test terms ('linkage', 'connection'). |
| 5 | NHS England CDSS | *(no official URL — illustrative document)* | Citation text confirms '(illustrative excerpt)'. Not an official NHS England publication. |
| 6 | TUC/CIPD Employment AI | *(no official URL — illustrative document)* | Citation text confirms 'Illustrative...sector assessment document'. Not official TUC/CIPD. |

---

## Corpus Coverage Notes

### What this corpus is designed to test

1. **Formal LAIF compliance gate** — all six documents are expected to FAIL formal compliance,
   demonstrating that real-world governance frameworks use different structural vocabulary than LAIF v1.2.

2. **Conceptual proximity scoring** — the four general-governance documents (1–4) address equivalent
   governance concerns without LAIF terminology, testing the assessor's ability to distinguish
   intent from form.

3. **Sector-specific risk alignment** — documents 5 and 6 exercise sector profiles (clinical_ai,
   employment_ai) to confirm sector-aware scoring contextualises assessments correctly.

4. **Paraphrase detection** — document 4 (US EO 14110) contains purpose-adapted wording using
   LAIF paraphrase test terms ('linkage', 'connection') to verify that paraphrase guards trigger.

### What this corpus does NOT support

- **Verbatim citation** — no document in this corpus is verified verbatim; all are REPRESENTATIVE_EXCERPT.
- **External publication claims** — results from this corpus cannot be presented as assessments
  of the official source documents without independently verifying the excerpt accuracy.
- **Regulatory compliance evidence** — this corpus is for framework validation only.

---

## Adding New Documents

When adding documents to `sample_documents.py`, you must include all four provenance fields:

```python
"provenance":   "OFFICIAL_EXCERPT" | "REPRESENTATIVE_EXCERPT" | "SYNTHETIC_TEST_DOCUMENT",
"source_url":   "https://...",       # empty string if synthetic or no URL
"source_note":  "Brief accuracy note — verbatim / condensed paraphrase / synthetic scenario",
"intended_use": "real-world baseline | sector scenario | adversarial test | demonstration",
```

If source accuracy cannot be verified, classify as `REPRESENTATIVE_EXCERPT`.  
Never classify a document as `OFFICIAL_EXCERPT` without verifying the text against the primary source.
