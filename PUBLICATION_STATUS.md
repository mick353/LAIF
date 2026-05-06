# LAIF Publication Status

**Framework:** Law-Aligned Intelligence Framework v1.2  
**Assessment model:** Refined Model v1.1  
**Date:** May 2026

---

> **Scope notice:** LAIF assessments are constitutional-governance analyses and are **not legal determinations**. Nothing in this repository constitutes legal advice, and no finding should be construed as establishing legal liability, regulatory compliance status, or any other legal consequence. The Coherence Test is a structural reasoning instrument applied to governance architecture; it does not determine whether any actor has violated any law.

---

## 1. Current Maturity State

| Component | Status |
|---|---|
| Framework (LAIF v1.2) | Stable — published April 2026 |
| Compliance Toolkit (v1.1) | Stable — published April 2026 |
| Corpus assessment — refined model v1.1 | Complete — `reports/laif_full_assessment.md` on `main` |
| Verified corpus infrastructure | Complete — `docs/verified/` with manifests, raw files, evidence traces |
| Validated corpus mode | Complete — `python3 validate.py --verified-corpus` |
| EU AI Act full-text ingestion | **READY_FOR_MANUAL_AUTHORITATIVE_INGESTION** — automated EUR-Lex retrieval blocked, manual acquisition workflow prepared |

---

## 2. Representative Corpus Limitations

The `sample_documents.py` corpus was designed for framework validation, not authoritative assessment. The following limitations apply to any results derived from it:

**2.1 Citeability**  
All documents in `sample_documents.py` are classified `REPRESENTATIVE_EXCERPT` and `NON_CITABLE`. They are condensed paraphrases of real governance documents. They may not reproduce the exact wording, structure, or provision numbering of their authoritative sources.

**2.2 Assessment validity**  
Assessments produced from `sample_documents.py` documents test the LAIF framework's structural detection logic against representative governance concepts. They do not constitute assessments of the actual instruments.

**2.3 No citation basis**  
No finding from a representative corpus assessment may be presented as a finding about the actual EU AI Act, NIST AI RMF, OECD Recommendation, EO 14110, or DTAC without independently verifying the excerpt accuracy.

---

## 3. Authoritative Corpus Status

| Document | Corpus entry | Hash | Assessment |
|---|---|---|---|
| OECD Recommendation (OECD/LEGAL/0449) | `docs/verified/raw/` | `f35d857...` | ASSESSED |
| EO 14110 (Fed. Reg. Vol. 88 No. 210) | `docs/verified/raw/` | `2cbab05...` | ASSESSED |
| NIST AI 100-1 | `docs/verified/raw/` | `44ac320...` | ASSESSED |
| DTAC v2.0 (NHS England, Feb 2026) | `docs/verified/raw/` | `d727228...` | ASSESSED |
| EU AI Act (Reg. 2024/1689) | READY_FOR_MANUAL_AUTHORITATIVE_INGESTION | — | PENDING_INGESTION |

**Authoritative assessment artifact:** `reports/laif_full_assessment.md` (on `main`, commit `e3a75f1` or later)

**Provenance verification:** `python3 validate.py --verified-corpus` — all 4 ASSESSED documents produce hash-verified PASS.

**EU AI Act readiness state:** EUR-Lex returned HTTP 403 Forbidden on all URL variants tested in automated session (May 2026). This is no longer treated as terminal blocking. The document is `READY_FOR_MANUAL_AUTHORITATIVE_INGESTION`: a human maintainer may download Regulation (EU) 2024/1689 from EUR-Lex and supply it through `HUMAN_GITHUB_DEPOSIT` or `HUMAN_SESSION_UPLOAD`. See `docs/verified/pending/eu_ai_act_ingestion_ready.md` and `docs/verified/manifests/eu-ai-act-2024-1689.json`.


### 3.1 Acquisition and Verification Taxonomy

The verified corpus now distinguishes source custody from source authority. The permitted acquisition channels are `AUTOMATED_URL_RETRIEVAL`, `HUMAN_GITHUB_DEPOSIT`, and `HUMAN_SESSION_UPLOAD`. A manual channel may support authoritative assessment only when the manifest also records the authoritative origin URL, acquisition metadata, SHA256 hashes, transformation chain, citation status, provenance classification, and verification status.

`HUMAN_ATTESTED_AUTHORITATIVE` records a human assertion about origin; it is not byte-identical upstream verification. `HASH_VERIFIED_LOCAL_ONLY` records local repository integrity only. `NETWORK_BLOCKED_PENDING_HUMAN_SOURCE` is not terminal; it means lawful manual acquisition remains the required next step.


### 3.2 Current Verification Classification

| Document | acquisition_channel | verification_status | network_status | Upstream equivalence claim |
|---|---|---|---|---|
| OECD Recommendation | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Not claimed |
| EO 14110 | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Not claimed |
| NIST AI 100-1 | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Not claimed |
| DTAC v2.0 | HUMAN_SESSION_UPLOAD | HASH_VERIFIED_LOCAL_ONLY | AUTOMATED_URL_BLOCKED_HTTP_403 | Not claimed |
| EU AI Act | Not yet acquired | NETWORK_BLOCKED_PENDING_HUMAN_SOURCE | AUTOMATED_URL_BLOCKED_HTTP_403 | Not claimed |

---

## 4. Known Methodological Limits

**4.1 Q1b enforcement assessment**  
The HARD / SOFT / NONE classification of Q1b is based on whether external enforcement mechanisms exist that are accessible to affected persons. This assessment is based on the instrument text; it does not account for how enforcement mechanisms operate in practice, judicial interpretation, or how effectively rights are enforced in specific jurisdictions.

**4.2 Q2 consistency at scale**  
The consistency test assesses whether the governance logic would produce just results if applied at all scales. This is a structural reasoning judgement, not an empirical claim. It reflects how the framework's logic applies, not how regulatory systems in practice handle scale variation.

**4.3 Governance Durability**  
Durability classifications (FRAGILE / ADAPTIVE / STABLE / BOUNDED) are based on observable institutional characteristics at the time of assessment. They do not constitute predictions about future durability.

**4.4 URL verification gap**  
All four ingested documents were sourced from legacy user-supplied files and are classified `HASH_VERIFIED_LOCAL_ONLY` with `network_status: AUTOMATED_URL_BLOCKED_HTTP_403`. SHA256 hashes verify integrity of the extracted markdown within this repository but do not certify identity with the source file bytes at the authoritative URL. Manual re-verification is available through `MANUAL_INGESTION_WORKFLOW.md`.

**4.5 NIST DOCX source**  
The NIST AI RMF ingestion relied on a user-supplied DOCX file. The DOCX accuracy against the authoritative PDF at doi.org/10.6028/NIST.AI.100-1 has not been independently verified.

---

## 5. Adversarial Testing Coverage

| Test type | Coverage | File |
|---|---|---|
| Paraphrase guard | 7 canonical terms, context-aware (allow_if_nearby, allow_if_contrast) | `validate.py` |
| Concept anchoring | PDCA structural blocks + LAIF v1.2 Principle 1 | `validate.py` |
| Semantic substitution detection | Relational phrase + domain noun heuristic | `validate.py` |
| Adversarial document suite | Yes — `test_adversarial.py` | `test_adversarial.py` |
| Real-world document suite | Yes — `test_real_world.py` | `test_real_world.py` |
| Hash verification | Yes — `python3 validate.py --verified-corpus` | `validate.py` |

**Also covered:**
- Evidence trace citation verification — `python3 validate.py --check-evidence-traces` verifies all cited section identifiers (39 citations across 4 documents) are present in the corresponding raw source files. Result: 39/39 PASS.

**Not covered by current tooling:**
- Automated detection of training-derived content (enforced at assessor level; not mechanically verifiable)
- Verbatim quote accuracy against raw source files (evidence trace verification checks section existence, not quote precision)

---

## 6. Reproducibility Guarantees

See `REPRODUCIBILITY.md` for the full reproducibility specification.

**Summary:**

| Claim | Guarantee | Scope |
|---|---|---|
| Detection verdicts are reproducible | Strong | Same source + LAIF v1.2 → same PASS/FAIL |
| Hash integrity | Strong | SHA256 of extracted markdown verified |
| Interpretation dimensions reproducible | Moderate | Same taxonomy; classification judgements may differ |
| URL provenance verified | No | URLs recorded; not verified by URL fetch |
| Training-derived content absent | Asserted | Not mechanically verifiable |

---

## 7. Non-Claims

The following claims are **not made** by this repository:

- That any assessed instrument is legally compliant or non-compliant with any legal requirement
- That any assessed instrument is fit or unfit for any specific deployment purpose
- That any actor has violated any law, regulation, or standard
- That LAIF v1.2 itself is compliant with any external governance standard (it is subject to self-application under Part Seven, not to external validation by this repository)
- That the LAIF assessment verdicts would be sustained under judicial or regulatory scrutiny
- That the four instruments assessed are definitively representative of all relevant AI governance instruments
- That reproducibility guarantees constitute audit certification

---

## 8. Publication Readiness Delta

Changes required before claiming full publication readiness:

| Gap | Priority | Blocking reason | Action |
|---|---|---|---|
| EU AI Act full-text ingestion | High | EUR-Lex HTTP 403 (automated access blocked) | Human download from EUR-Lex; supply as uploaded file |
| URL verification pass | Medium | All authoritative URLs return HTTP 403 from automated session | Human-initiated verification against each listed URL |
| NIST DOCX accuracy verification | Medium | NIST PDF at doi.org/10.6028/NIST.AI.100-1 returns HTTP 403 | Human download of PDF; textual comparison with extracted markdown |
| Evidence trace section verification | **Resolved** | — | `python3 validate.py --check-evidence-traces` — 39/39 PASS |

---

*LAIF v1.2 · Compliance Toolkit v1.1 · April 2026*
