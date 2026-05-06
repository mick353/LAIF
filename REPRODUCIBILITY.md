# LAIF Assessment Reproducibility

**Framework:** Law-Aligned Intelligence Framework v1.2  
**Assessment model:** Refined Model v1.1  
**Date:** May 2026

---

## Purpose

This document specifies the conditions under which a LAIF corpus assessment can be reproduced, what guarantees apply to each layer of the assessment, and where the limits of reproducibility lie.

LAIF assessments are constitutional-governance analyses and are **not legal determinations**. Reproducibility guarantees apply to the structural reasoning layer; they do not guarantee identical linguistic expression or ordering of sub-findings.

---

## 1. Exact Assessment Workflow

### 1.1 Source Ingestion

**Requirement:** All factual claims in a LAIF assessment must be traceable to an ingested source file. No training-derived content may be used for any factual claim.

**Steps:**
1. Obtain the authoritative source document (PDF, DOCX, or verified text)
2. Extract full text with no transformation beyond formatting normalisation (markdown headings, pipe tables, whitespace)
3. Write to `docs/verified/raw/<document_id>.md`
4. Compute `sha256sum` of the extracted file and record in the manifest
5. Create manifest at `docs/verified/manifests/<document_id>.json` with all required fields
6. Commit raw file and manifest together

**Strict Source Mode** — the constraint that no training-derived content may be used — is enforced at the assessor level, not by tooling. Any factual claim in an assessment that cannot be cited to a verbatim line in an ingested source file is a Strict Source Mode violation.


### 1.1.1 Acquisition Channels

The verified corpus supports three lawful source-acquisition channels:

| Channel | Meaning | Authority limitation |
|---|---|---|
| `AUTOMATED_URL_RETRIEVAL` | Tooling fetches the file directly from `authoritative_origin_url` | Strongest channel only if hash/equivalence verification succeeds |
| `HUMAN_GITHUB_DEPOSIT` | Human downloads the authoritative file and deposits it into `docs/verified/manual_ingest/` via GitHub or commit | Requires human attestation and local hash verification |
| `HUMAN_SESSION_UPLOAD` | Human uploads the file during the session and the agent writes the exact supplied file into `docs/verified/manual_ingest/` | Requires human attestation and local hash verification |

The acquisition channel does not itself prove authority. Authority is established only by the combined manifest record: `authoritative_origin_url`, `acquired_by`, `acquired_at_utc`, `acquisition_note`, `source_file_sha256`, `transformation_chain`, `citation_status`, `provenance_classification`, and `verification_status`.

`HUMAN_ATTESTED_AUTHORITATIVE` means the human operator supplied the file and asserted that it came from the authoritative source. `HASH_VERIFIED_LOCAL_ONLY` means repository integrity is verified, but upstream URL equivalence is not yet proven. `NETWORK_BLOCKED_PENDING_HUMAN_SOURCE` is a non-terminal state that should trigger manual acquisition or later automated re-verification.

### 1.2 Assessment Execution

**Step 1 — Integrity Layer (Section A):**
Apply LAIF v1.2 §§2.1–2.3 to the ingested source. For each property:
- Read the relevant source sections
- Determine whether the property is structurally satisfied
- Record the determination (STRONG / MODERATE / WEAK) with verbatim citation
- The Integrity Layer is a threshold: partial satisfaction = failure

**Step 2 — Coherence Test (Section B):**
Apply LAIF v1.2 Part One to the ingested source. For each question:
- Q1: Identify whether each restriction names and protects a specific human interest (Q1a), then determine enforcement force (Q1b)
- Q2: Apply the consistency test — would the same logic produce just results at all scales?
- Q3: Determine whether the instrument preserves future actors' capacity to revise
- Record verbatim citations for each finding

**Step 3 — New Dimensions (Section C):**
Apply refined model v1.1 interpretation-layer dimensions:
- Governance Durability: FRAGILE / ADAPTIVE / STABLE / BOUNDED
- Reflexivity: NONE / PARTIAL / FULL
These are classification dimensions only. They do not affect Coherence Test pass/fail results.

**Step 4 — Provision Layer Compliance (Section D):**
Apply LAIF v1.2 Provision Sets A–D and Schedule B.2 where applicable.

**Step 5 — Overall Verdict:**
Summarise findings. Note that Integrity Layer failure does not automatically produce Coherence Test failure — the two sections are assessed independently.

### 1.3 Output

Write the complete assessment to `reports/laif_full_assessment.md` (or a named variant). Commit to `main`. The assessment is not authoritative until on `main`.

---

## 2. Ingestion Assumptions

The following assumptions apply to ingestion of documents into `docs/verified/raw/`:

| Assumption | Consequence if violated |
|---|---|
| Source document is authentic | Provenance_classification and citation_status must be downgraded |
| No content transformation beyond formatting | transformation_status must be STRUCTURALLY_EXTRACTED if headers/structure were inferred |
| No paraphrasing | citation_status must be DERIVED_EXCERPT or NON_CITABLE |
| SHA256 recorded at ingestion time | Hash verification in validate.py --verified-corpus will fail |

---

## 3. Provenance Guarantees

| Guarantee | Scope | Limitation |
|---|---|---|
| Verbatim content | Applies within the extracted markdown | Does not certify identity with the original PDF/DOCX bytes |
| No training-derived content | Applies to all factual claims in the assessment | Cannot be verified by tooling; enforced at assessor level |
| SHA256 integrity | Guarantees the extracted markdown has not been altered since ingestion | Hash is of the markdown, not the original source file |
| URL verification | `network_status` recorded as `AUTOMATED_URL_BLOCKED_HTTP_403`; OECD/EO/NIST/DTAC are `HASH_VERIFIED_LOCAL_ONLY` | Content not accessible from automated session; upstream byte comparison not performed |
| Evidence trace citation integrity | 39/39 citations verified present in raw files | Verifies section existence, not verbatim quote accuracy |

---

## 4. Deterministic Scoring Guarantees

### What is deterministic

- **Detection layer verdicts** are deterministic given the source text and LAIF v1.2 framework text:
  - Q1 PASS/FAIL
  - Q2 PASS/FAIL (and PARTIAL PASS where documented)
  - Q3 PASS/FAIL (and CONDITIONAL PASS where documented)
  - Integrity Layer property assessments (STRONG/MODERATE/WEAK)
  - Overall verdict

- Any assessor reading the same source text and applying LAIF v1.2 Part One and Part Two should produce the same PASS/FAIL verdicts. The evidence supporting these verdicts is documented in the evidence traces at `docs/verified/extracted/`.

### What is not deterministic

- **Linguistic expression**: The exact wording of any given finding may differ between assessors
- **Interpretation-layer dimensions** (Governance Durability, Reflexivity): These involve classification judgements that reasonable assessors may make differently within the defined taxonomy
- **Q2 granularity**: PARTIAL PASS judgements involve a degree of assessor interpretation about scale coverage

### Scoring invariants

These conditions must hold across any reproduction:

1. Q1b = NONE for EO 14110 (§13(c) is explicit and unambiguous)
2. Q1b = NONE for NIST AI RMF (voluntary design, explicitly stated)
3. Q1b = SOFT for OECD Recommendation (non-binding by instrument type)
4. Q1b = HARD for DTAC (procurement gate with market-exclusion consequences)
5. EO 14110 Governance Durability = FRAGILE (revoked January 2025)
6. Integrity Layer = threshold, not score; partial satisfaction = failure

---

## 5. Interpretation-Layer Boundaries

The **interpretation layer** covers how findings are expressed, sub-classified, or contextualised. It is independently revisable from the detection layer.

**Interpretation-layer elements (revisable without changing detection logic):**
- Q1a / Q1b sub-classification of Q1 Coupling
- Governance Durability (FRAGILE / ADAPTIVE / STABLE / BOUNDED)
- Reflexivity (NONE / PARTIAL / FULL)
- Ordering of findings within sections
- Linguistic expression of verdicts

**Constraint:** An interpretation-layer refinement must not alter any detection verdict. If a proposed refinement would change a PASS to FAIL or vice versa, it is a detection-layer change and requires explicit justification against LAIF v1.2.

---

## 6. Detection-Layer Boundaries

The **detection layer** covers whether Q1/Q2/Q3 pass or fail, Integrity Layer thresholds, and what counts as PASS/FAIL. It is fixed by LAIF v1.2 and the Compliance Toolkit v1.1.

**Detection-layer elements (not revisable without amending LAIF v1.2):**
- Q1 PASS/FAIL criteria (LAIF v1.2 Part One, §2.4 equivalent normative force)
- Q2 PASS/FAIL criteria (LAIF v1.2 Part One, consistency standard)
- Q3 PASS/FAIL criteria (LAIF v1.2 Part One, reversibility standard)
- Integrity Layer property thresholds (LAIF v1.2 Part Two, §§2.1–2.3)
- Automatic failure on Integrity Layer non-satisfaction

---

## 7. Representative vs Authoritative Corpus Distinction

**This distinction is critical for any use of LAIF assessment results.**

| Property | Representative corpus (`docs/supporting/` + `sample_documents.py`) | Authoritative corpus (`docs/verified/`) |
|---|---|---|
| Provenance | Strict Source Mode ingestion from user-supplied files | Same — plus SHA256 hash and provenance manifest |
| Citeability | PRIMARY_CITABLE (full text, no paraphrase) | PRIMARY_CITABLE + hash-verified |
| EU AI Act | Not ingested | PENDING_INGESTION (placeholder only) |
| Sample corpus (`sample_documents.py`) | REPRESENTATIVE_EXCERPT — NON_CITABLE | Not present |

**Representative corpus results are NOT equivalent to authoritative-source assessments.**

The `sample_documents.py` corpus contains condensed paraphrases of source documents, labelled REPRESENTATIVE_EXCERPT and classified NON_CITABLE. Assessments produced from this corpus are framework validation tests, not authoritative governance assessments of the actual instruments.

Assessments produced from `docs/verified/raw/` files, with provenance manifests, evidence traces, and hash verification, constitute authoritative LAIF assessments of the actual instruments.

The authoritative assessment for the current corpus is: `reports/laif_full_assessment.md`.

---

## 8. Unresolved Limitations

1. **URL verification gap — partially resolved** — A URL verification attempt was made for all five authoritative URLs (May 2026). All five returned HTTP 403 Forbidden, confirming the URLs are server-responsive but blocking automated retrieval. OECD, EO 14110, NIST, and DTAC are classified `HASH_VERIFIED_LOCAL_ONLY` with `network_status: AUTOMATED_URL_BLOCKED_HTTP_403`; content comparison against upstream sources was not performed and byte-identical equivalence is not claimed. Full verification requires human-initiated browser access. See `docs/verified/url_verification/verification_report.md`.

2. **NIST DOCX provenance** — extracted from user-supplied DOCX; DOCX accuracy against the authoritative PDF at doi.org/10.6028/NIST.AI.100-1 has not been independently verified. The PDF URL also returns HTTP 403 from automated session. See `docs/verified/nist_reconciliation.md`.

3. **EU AI Act gap** — ingestion blocked (EUR-Lex HTTP 403). No LAIF assessment of the EU AI Act can be considered authoritative until full-text ingestion is complete. See `docs/verified/manifests/eu-ai-act-2024-1689.json`.

4. **Agentic AI** — LAIF §2.3 Structural Containment references specific requirements for agentic AI systems. None of the four assessed instruments address this requirement. This is a universal gap, not an assessment limitation.

5. **Evidence trace section verification** — resolved. `python3 validate.py --check-evidence-traces` verifies that section identifiers cited in evidence traces are present in the corresponding raw source files. See Phase 4 implementation.

---

*LAIF v1.2 · Compliance Toolkit v1.1 · April 2026*

## Governance Reproducibility Checks

The merged Phase 3A and Phase 3B governance work adds deterministic repository-governance checks without changing LAIF assessment semantics or scoring. The CI governance job gates downstream validation, adversarial, and real-world jobs so that repository-governance failures are visible before assessment checks run.

For a reproducible governance review, run:

```bash
python3 -m py_compile scripts/governance/*.py
python3 scripts/governance/check_governance_config.py
python3 scripts/governance/check_protected_artifacts.py
python3 scripts/governance/check_semantic_boundaries.py
python3 tests/test_governance.py
```

Local protected-artifact and semantic-boundary checks skip pull-request diff detection when no PR base ref is available. In CI, the PR base comes from the GitHub pull-request context. Locally, set `GOVERNANCE_BASE_REF` or `GITHUB_BASE_REF` when deterministic diff detection is needed.

The Phase 3B suite validates shared governance helpers, governance config validation, protected-artifact blocking behavior, and semantic-boundary advisory behavior using `tests/governance_fixtures/valid_config.json`. Semantic-boundary warnings are not merge blockers. Governance tests do not change assessment scoring, detector behavior, interpretation logic, published reports, or the verified corpus.
