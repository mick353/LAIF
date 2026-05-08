# Law-Aligned Intelligence Framework (LAIF)

**Version 1.2 · Compliance Toolkit v1.1 · April 2026 · Governance Audit Series**

LAIF is a **structural governance integrity framework for AI-related institutional documents**. It asks whether high-level AI governance principles have been operationalised into enforceable, auditable, reversible, accountable structures that protect identifiable human and public interests.

LAIF can be used diagnostically to examine laws, standards, government policies, departmental AI governance documents, procurement controls, vendor and model-provider policies, development lifecycle controls, and operational AI governance instruments. That diagnostic use does **not** require the source document to use LAIF vocabulary. LAIF is strict only when a document claims or seeks **LAIF-native certification**, where canonical LAIF terms and structures are load-bearing.

The framework's primary practical instrument is the **Pre-Deployment Coherence Assessment (PDCA)**, a structured audit process designed to identify whether governance commitments have enough institutional force to be verified, enforced, escalated, and reversed where necessary. LAIF can integrate with existing regulatory frameworks (EU AI Act, NIST AI RMF, US federal requirements) without claiming to replace their legal authority.

The runner preserves original file name, source hash, processing timestamp, and output paths in JSON/markdown metadata and an output-directory JSONL index.

---

## Assessment Modes

| Mode | Purpose | Result meaning |
|------|---------|----------------|
| **LAIF-native certification** | Strict evaluation of documents that claim or seek LAIF adoption. | PASS/FAIL is valid only under LAIF-native criteria; canonical LAIF terminology and structures are required. |
| **External framework diagnostic assessment** | Model-relative review of external laws, standards, policies, procurement rules, vendor policies, and operational governance documents. | Findings identify governance-force, ambiguity, reversibility, auditability, enforceability, accountability, evidence, and remediation gaps; they are diagnostic, not certification. |
| **Remediation / patch guidance** | Optional adoption pathway for organisations that want to strengthen or LAIF-align an instrument. | Maps diagnostic gaps to LAIF-native clauses, controls, evidence artefacts, and verification tests. |
| **Repository governance / CI validation** | Internal project integrity checks for protected artifacts, semantic boundaries, provenance, and workflow safety. | CI PASS/FAIL describes repository workflow status, not the legal or governance validity of external documents. |

---

## What LAIF Does Not Claim

LAIF does **not** make the following claims:

- It does not determine legal validity or legal enforceability under any jurisdiction;
- it does not claim authority over external jurisdictions, regulators, government departments, industries, standards bodies, or institutions;
- it does not require external frameworks to use LAIF vocabulary to be diagnostically assessed;
- it does not treat **not LAIF-native** as meaning governance-invalid, legally invalid, unsafe, valueless, worthless, or structurally incoherent on the external framework's own authority.

---

## How to Read LAIF Results

- **LAIF-native PASS/FAIL is strict and model-bound.** It applies when a document claims or seeks LAIF-native certification and is evaluated against LAIF-native criteria.
- **External scores and findings are diagnostic.** They show how an external instrument appears under the LAIF model; they do not certify or invalidate the external instrument.
- **Scores are deterministic rubric outputs.** They are not legal findings, statistical confidence values, or external regulatory compliance ratings.
- **Remediation guidance is additive adoption guidance.** It explains what would need to be added, clarified, evidenced, or tested if an institution wants LAIF-native alignment or stronger governance force.

For detailed interpretation rules, see `docs/governance/RESULT_TAXONOMY.md`, `docs/governance/SCORE_INTERPRETATION.md`, and `docs/governance/GOVERNANCE_FORCE_MODEL.md`.

---

## Who This Is For

| Audience | Starting point |
|----------|---------------|
| **Regulators and policy bodies** | Executive Brief → LAIF v1.2 Part Seven (Self-Application) |
| **AI operators and developers** | Executive Brief → PDCA (GPT-4 Clinical) → Compliance Toolkit |
| **Procurement officers (federal)** | Regulatory Integration Guide Part Two (OMB M-24-18) |
| **Legal and compliance counsel** | LAIF v1.2 → Regulatory Integration Guide Part One (EU AI Act) |
| **Researchers and academics** | Policy Paper → Case Analysis → LAIF v1.2 |
| **New readers (any background)** | Executive Brief (2 min) → Public Article (5–7 min) |

---

## The Three Coherence Test Questions

Every LAIF-native certification claim is assessed against three questions. External framework diagnostic assessment uses the same questions as a structural lens without treating different vocabulary as legal invalidity.

**Q1 — Coupling**
Does the deployment authorisation identify and protect the specific human interest at risk — with a protection of equivalent normative force to the restriction imposed? This is the most commonly failed question in existing AI governance.

**Q2 — Consistency**
Would the governance logic produce just and workable results if applied to all comparable actors and at significantly smaller and larger scales? Logic that works only as a carve-out for a specific actor is not a governance principle.

**Q3 — Reversibility**
Does the deployment preserve the capacity of future actors to modify or reverse its consequences? Structural irreversibility requires justification proportionate to its permanence.

---

## Reading Order

```
01  START HERE
    ├── LAIF_Executive_Brief          — 2-minute governance audit summary
    └── LAIF_Public_Article           — 5–7 minute public-facing overview

02  CORE FRAMEWORK
    └── LAIF_v1.2                     — The authoritative framework text

03  APPLICATIONS AND INTEGRATION
    ├── LAIF_PDCA_GPT4_Clinical       — Applied PDCA: clinical AI deployment audit
    ├── LAIF_Regulatory_Integration_Guide  — EU AI Act + US federal step-by-step
    ├── LAIF_Case_Analysis            — Retrospective analysis: 8 governance failures
    ├── LAIF_Compliance_Toolkit       — Operational definitions and standards (v1.1)
    └── LAIF_Policy_Paper             — Academic/policy paper on the framework's design
```

Each document is available in its original `.docx` format and as a plain-text `.txt` export for search and programmatic access.

---

## Core Concepts at a Glance

### The Integrity Layer
Three properties that are **preconditions of lawful deployment** — all must be satisfied simultaneously. Partial satisfaction is failure.

- **A.1 Structural Transparency** — The system can produce, on request, a comprehensible account of its outputs including confidence levels and material limitations.
- **A.2 Structural Honesty** — Stated optimisation objectives correspond to actual implemented objectives. The system performs consistently whether or not it is being evaluated.
- **A.3 Structural Containment** — The system operates within documented boundaries and does not initiate materially irreversible actions without triggering the appropriate authorisation process.

### Framework Hierarchy
```
Foundational Principles  (non-amendable)
        ↓
    Provisions           (derived from Principles; cannot contradict them)
        ↓
Operational Standards    (Compliance Toolkit; revisable without amending Provisions)
```

### Self-Application
LAIF applies to regulatory bodies and governance actors themselves — not only to AI operators. This is Part Seven of the framework, not a footnote.

### External Framework Integrations

| Framework | Integration |
|-----------|------------|
| EU AI Act (2024/1689) | Provision-by-provision mapping — Regulatory Integration Guide Part One |
| NIST AI RMF | Function-by-function mapping — Regulatory Integration Guide Part Two |
| OMB M-24-18 | Step-by-step procurement integration — Regulatory Integration Guide §2.3 |
| OECD AI Principles | Background governance instrument, cited throughout |
| UNESCO AI Ethics | Background governance instrument, cited throughout |
| Anthropic Constitutional AI | Feedback incorporated in v1.2 |

---

## Repository Contents

| File | Format | Description |
|------|--------|-------------|
| `LAIF-Law-Aligned_Intelligence_Framework.txt` | TXT | Navigation index |
| `LAIF_Executive_Brief.docx` / `.txt` | DOCX + TXT | 2-min executive overview |
| `LAIF_Public_Article.docx` / `.txt` | DOCX + TXT | Public-facing governance audit article |
| `LAIF_v1.2.docx` / `.txt` | DOCX + TXT | Core framework document |
| `LAIF_PDCA_GPT4_Clinical.docx` / `.txt` | DOCX + TXT | Applied PDCA assessment |
| `LAIF_Case_Analysis.docx` / `.txt` | DOCX + TXT | Retrospective case analysis (8 failures) |
| `LAIF_Compliance_Toolkit.docx` / `.txt` | DOCX + TXT | Operational definitions v1.1 |
| `LAIF_Policy_Paper.docx` / `.txt` | DOCX + TXT | Academic/policy paper |
| `LAIF REGULATORY INTEGRATION GUIDE.docx` / `LAIF_Regulatory_Integration_Guide.txt` | DOCX + TXT | Regulatory integration guide |
| `CLAUDE.md` | MD | AI assistant guidance for this repository |
| `corpus_manifest.md` | MD | Provenance and citeability classification for all assessed documents |

**Ingested source documents** (`docs/supporting/`):

| File | Description |
|------|-------------|
| `51a29205-OECD_Legal_Instruments.md` | OECD Recommendation on AI (OECD/LEGAL/0449) — full text |
| `b0ef43db-202324283.md` | US Executive Order 14110 (Federal Register Vol. 88 No. 210) — full text |
| `5f667a6f-NIST.AI.1001.md` | NIST AI 100-1 — AI Risk Management Framework 1.0 — full text |
| `55eccce3-DTAC_Form_2.0_February_2026.md` | NHS England Digital Technology Assessment Criteria v2.0 — full text |

**Assessment artifacts** (`reports/`):

| File | Description |
|------|-------------|
| `laif_full_assessment.md` | **Authoritative** — full corpus assessment, refined model v1.1, all four instruments |

## Repository Governance

Contribution and review expectations are documented in `CONTRIBUTING.md` and `docs/governance/`. These documents describe semantic-boundary review, protected artifact awareness, merge expectations, and rollback procedures without changing LAIF assessment semantics or validation behavior.

---

*LAIF v1.2 · Compliance Toolkit v1.1 · April 2026*

## Governance Status

Phase 3A governance stabilization and Phase 3B deterministic governance test coverage have been merged. The repository's CI governance job compiles and runs the governance checks before the validation, adversarial, and real-world CI jobs; those downstream jobs depend on governance completing successfully.

Current governance behavior is deliberately scoped:

- protected-artifact checks are blocking for configured protected artifacts in a pull-request diff;
- semantic-boundary checks are advisory-only and do not block merge;
- governance config validation enforces configured path existence;
- governance helper/check files are semantic-sensitive and require focused review when changed;
- `tests/test_governance.py` validates shared governance helpers, governance config behavior, protected-artifact behavior, and semantic-boundary advisory behavior with `tests/governance_fixtures/valid_config.json`.

Governance documentation and tests do not alter LAIF assessment/scoring semantics, do not change assessment outcomes, and do not imply external legal certification. LAIF remains a structural governance framework rather than a legal determination or certification authority.
