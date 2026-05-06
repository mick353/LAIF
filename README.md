# Law-Aligned Intelligence Framework (LAIF)

**Version 1.2 · Compliance Toolkit v1.1 · April 2026 · Governance Audit Series**

LAIF is a constitutional-level governance standard for AI systems. It provides a single, scale-invariant decision test — the **Coherence Test** — that can be applied consistently across all actors, jurisdictions, and AI capabilities to evaluate whether a deployment, regulation, or policy is structurally sound. Its primary practical instrument is the **Pre-Deployment Coherence Assessment (PDCA)**, a structured audit process designed to integrate with existing regulatory frameworks (EU AI Act, NIST AI RMF, US federal requirements) rather than replace them.

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

Every AI deployment, regulation, and governance decision is assessed against three questions. All three must be answered affirmatively. Failure at any one is failure of the full test.

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

---

*LAIF v1.2 · Compliance Toolkit v1.1 · April 2026*
