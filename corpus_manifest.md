# LAIF Assessment — Corpus Manifest

**Generated:** May 2026 · **Updated:** July 2026
**Framework:** LAIF v1.2 · Compliance Toolkit v1.1

This manifest documents every document in the assessment corpus, its provenance
classification, accuracy status, and intended role. The corpus now has two
evidence tiers held in two modules:

| Module | Tier | Citable? |
|--------|------|----------|
| `official_documents.py` | OFFICIAL_EXCERPT — verbatim, SHA-256-pinned extracts of committed authoritative texts | **Yes** (within stated excerpt scope) |
| `sample_documents.py` | REPRESENTATIVE_EXCERPT — condensed paraphrases / illustrative documents | No |

All provenance claims are machine-enforced by `test_provenance.py` (48 checks;
exit 1 on any failure) and re-verified at import time by `official_documents.py`
itself. An OFFICIAL_EXCERPT that cannot prove verbatim provenance refuses to load.

---

## Provenance Classifications

| Code | Meaning |
|------|---------|
| `OFFICIAL_EXCERPT` | Verified verbatim text from the authoritative source, extracted from a committed source file in `docs/supporting/` via unique start/end markers and pinned by SHA-256. Citable as primary evidence within the stated excerpt scope. |
| `REPRESENTATIVE_EXCERPT` | Condensed paraphrase or illustrative excerpt capturing governance intent of a real framework. **Not verbatim. Not citable as the primary source.** |
| `SYNTHETIC_TEST_DOCUMENT` | Constructed for adversarial or stress-testing; does not represent any real-world governance document. |

---

## Official Corpus (`official_documents.py`) — Citable

| # | Document | Source Type | Jurisdiction | Year | Source File | Excerpt Scope |
|---|----------|-------------|--------------|------|-------------|---------------|
| O1 | US Executive Order 14110 (88 FR 75191) | executive_directive | United States (Federal) | 2023 | `docs/supporting/b0ef43db-202324283.md` | §2 Policy and Principles; §6 Supporting Workers; §7 Advancing Equity and Civil Rights |
| O2 | OECD Recommendation on AI (OECD/LEGAL/0449, amended 2024) | international_principles | International (OECD) | 2024 | `docs/supporting/51a29205-OECD_Legal_Instruments.md` | Section 1 Principles 1.1–1.5; Section 2 Recommendations 2.1–2.5 |
| O3 | NIST AI 100-1 (AI RMF 1.0, January 2023) | voluntary_framework | United States | 2023 | `docs/supporting/5f667a6f-NIST.AI.1001.md` | Part 2 Core: GOVERN function + Table 1; MAP function + Table 2 |
| O4 | NHS England DTAC v2.0 (24 February 2026) | sector_policy | United Kingdom | 2026 | `docs/supporting/55eccce3-DTAC_Form_2.0_February_2026.md` | Introduction; Section C1 Clinical safety (C1.1.1–C1.2.5) |

Non-contiguous excerpt blocks are joined with an explicit `[…]` elision marker —
the assessed text never silently splices passages. Exact SHA-256 pins live in
`official_documents.py`; `test_provenance.py` independently re-computes them.

## Representative Corpus (`sample_documents.py`) — Illustrative Only

| # | Document Name | Source Type | Jurisdiction | Year | Provenance | Citable? | Intended Use |
|---|---------------|-------------|--------------|------|------------|----------|--------------|
| 1 | EU AI Act — Art. 9, 13 & 14 | binding_regulation | European Union | 2024 | REPRESENTATIVE_EXCERPT | No | real-world baseline *(official ingestion pending — see Coverage Notes)* |
| 2 | NIST AI RMF — Govern & Map Functions | voluntary_framework | United States | 2023 | REPRESENTATIVE_EXCERPT | No | real-world baseline; paraphrase contrast for O3 |
| 3 | OECD AI Principles (2019, rev. 2024) | international_principles | International (OECD) | 2024 | REPRESENTATIVE_EXCERPT | No | real-world baseline; paraphrase contrast for O2 |
| 4 | US Executive Order 14110 — §4 Safety & §7 Workers | executive_directive | United States (Federal) | 2023 | REPRESENTATIVE_EXCERPT | No | paraphrase stress-test (embedded 'linkage'/'connection' guard triggers); paraphrase contrast for O1 |
| 5 | NHS England — AI in Clinical Decision Support | sector_policy | United Kingdom | 2024 | REPRESENTATIVE_EXCERPT | No | sector scenario — clinical AI (illustrative; official clinical instrument is O4) |
| 6 | TUC/CIPD — Framework for Fair AI in Employment Decisions | sector_policy | United Kingdom | 2024 | REPRESENTATIVE_EXCERPT | No | sector scenario — employment AI |

## Source URLs

| # | Document | Source URL | Accuracy Note |
|---|----------|-----------|---------------|
| O1 | EO 14110 (official) | https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence | Verbatim, hash-pinned against committed Federal Register text. |
| O2 | OECD Recommendation (official) | https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449 | Verbatim, hash-pinned against committed OECD Legal Instruments snapshot (6 May 2026); snapshot preserves publisher line-wrapping. |
| O3 | NIST AI 100-1 (official) | https://doi.org/10.6028/NIST.AI.100-1 | Verbatim, hash-pinned against committed NIST full text. |
| O4 | NHS DTAC v2.0 (official) | https://transform.england.nhs.uk/key-tools-and-info/digital-technology-assessment-criteria-dtac/ | Verbatim, hash-pinned against committed DTAC v2.0 form text. |
| 1 | EU AI Act | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689 | Condensed paraphrase of Arts. 9, 13, 14. Verify against OJ publication. |
| 2 | NIST AI RMF | https://airc.nist.gov/RMF | British spelling 'organisational' departs from American-English original. |
| 3 | OECD AI Principles | https://oecd.ai/en/ai-principles | Structural numbering preserved; wording is not verbatim. |
| 4 | US EO 14110 | https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence | Paraphrased; contains embedded LAIF paraphrase test terms ('linkage', 'connection'). |
| 5 | NHS England CDSS | *(no official URL — illustrative document)* | Citation text confirms '(illustrative excerpt)'. Not an official NHS England publication. |
| 6 | TUC/CIPD Employment AI | *(no official URL — illustrative document)* | Citation text confirms 'Illustrative...sector assessment document'. Not official TUC/CIPD. |

---

## Corpus Coverage Notes

### What this corpus is designed to test

1. **Citable formal-compliance findings (official tier)** — the four OFFICIAL_EXCERPT
   documents allow the headline finding (real-world governance frameworks fail formal
   LAIF v1.2 compliance) to be stated of the named instruments themselves, verified
   against hash-pinned authoritative text.

2. **Paraphrase-artefact control** — documents 2–4 paraphrase the same instruments as
   O1–O3, so citable and illustrative results can be compared. Convergence confirms
   findings are not artefacts of condensation.

3. **Formal LAIF compliance gate** — all ten documents are expected to FAIL formal
   compliance, demonstrating that real-world governance frameworks use different
   structural vocabulary than LAIF v1.2.

4. **Conceptual proximity scoring** — general-governance documents address equivalent
   governance concerns without LAIF terminology, testing the assessor's ability to
   distinguish intent from form.

5. **Sector-specific risk alignment** — documents 5, 6 and O4 exercise sector profiles
   (clinical_ai, employment_ai). O4 additionally exercises the assessor against a
   form/questionnaire-style official instrument (known heuristic limitation: the
   sector-gaming detector reads form-style density as a format mismatch — see the
   interpretation caveat in the assessment report).

6. **Paraphrase detection** — document 4 (US EO 14110) contains purpose-adapted wording
   using LAIF paraphrase test terms ('linkage', 'connection') to verify that paraphrase
   guards trigger.

### What this corpus does NOT support

- **Verbatim citation of the representative tier** — documents 1–6 are not verbatim;
  results from them cannot be presented as assessments of the official sources.
- **EU AI Act citable claims** — the EU AI Act is only present as a REPRESENTATIVE_EXCERPT.
  Official Journal ingestion (Regulation (EU) 2024/1689) is the top open item.
- **Regulatory compliance evidence** — this corpus validates the LAIF framework and
  assessor; it is not compliance evidence for any assessed organisation.
- **Whole-instrument claims beyond excerpt scope** — official-tier findings hold for the
  excerpted sections declared per entry, not necessarily for unexcerpted parts of the
  instruments.

---

## Adding New Documents

### Representative or synthetic documents (`sample_documents.py`)

Include all four provenance fields:

```python
"provenance":   "REPRESENTATIVE_EXCERPT" | "SYNTHETIC_TEST_DOCUMENT",
"source_url":   "https://...",       # empty string if synthetic or no URL
"source_note":  "Brief accuracy note — condensed paraphrase / synthetic scenario",
"intended_use": "real-world baseline | sector scenario | adversarial test | demonstration",
```

Never classify a document in `sample_documents.py` as `OFFICIAL_EXCERPT` —
`test_provenance.py` P2.1 fails the build if you do.

### Official documents (`official_documents.py`)

1. Commit the full verbatim source text to `docs/supporting/` first
   (strict ingestion, no transformation — see repo commit history for precedent).
2. Add an entry with `source_file`, unique `start`/`end` markers for each excerpt
   block, and the block SHA-256 (run the module's `__main__` to compute hashes).
3. Fill `source_note` with the exact excerpt scope.
4. Run `python3 test_provenance.py` — all P1 checks must pass.

If source accuracy cannot be verified against the primary source, classify as
`REPRESENTATIVE_EXCERPT`. Never pin a hash without reading the committed source text.
