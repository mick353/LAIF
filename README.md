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

## Programmatic Assessment Toolchain

Beyond the governance corpus, the repository ships a Python toolchain (stdlib only, no dependencies) that operationalises LAIF:

| Component | Role |
|-----------|------|
| `laif_spec.py` | Canonical spec — terms, forbidden paraphrases, Integrity Layer, Coherence Test, risk tiers |
| `validate.py` | 9-check validation harness over the `.txt` corpus (strict, binary) |
| `assessment_engine.py` | Scores external governance documents on 5 traceable dimensions, with sector profiles, Coupling-quality analysis, contradiction detection, and risk tiering |
| `official_documents.py` | **Citable corpus** — verbatim, SHA-256-pinned excerpts of EO 14110, the OECD AI Recommendation, NIST AI 100-1, and NHS DTAC v2.0, extracted from committed sources in `docs/supporting/` |
| `sample_documents.py` | Illustrative corpus — representative paraphrases (not citable) |
| `test_provenance.py` | 48 machine-enforced checks on every citability claim |
| `test_adversarial.py` | 82 adversarial tests on the guards and depth checks |
| `test_semantic_fidelity.py` | 37 checks guaranteeing substance is never outranked by vocabulary and no document is falsely accused |
| `test_real_world.py` | Runs the full assessment → `reports/laif_real_world_assessment.md` |

The engine measures on two independent axes: **LAIF-native form** (is the document written as a LAIF instrument — external frameworks are expected to fail this) and **functional alignment** (is the *substance* of Coupling, the Integrity Layer, Consistency, Reversibility, and Self-Application expressed in the document's own vocabulary — grounded in LAIF v1.2 Part Eight and the Regulatory Integration Guide's SATISFIES/EXTENDS methodology). A document is never penalised for expressing LAIF's requirements in its own words, and never credited for using LAIF's words without the substance.

**Headline citable finding:** all four official instruments assessed from verbatim text fail the LAIF-native formal gate while averaging 53/100 conceptual proximity, and three of four are PARTIALLY ALIGNED at the construct level — real-world frameworks address the right governance dimensions, and partially express LAIF's structural mechanisms in their own idioms, but none enforces them through structural Coupling, the Coherence Test, or the Integrity Layer.

Run everything:

```bash
python3 validate.py && python3 test_adversarial.py && python3 test_provenance.py && python3 test_semantic_fidelity.py && python3 test_real_world.py
```

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
| `laif_spec.py`, `validate.py`, `assessment_engine.py` | PY | Enforcement and assessment toolchain |
| `official_documents.py`, `sample_documents.py`, `corpus_manifest.md` | PY + MD | Two-tier assessment corpus with provenance manifest |
| `test_provenance.py`, `test_adversarial.py`, `test_real_world.py` | PY | Test suites and report generator |
| `docs/supporting/` | MD | Verbatim ingested source texts (EO 14110, OECD, NIST AI 100-1, NHS DTAC v2.0) |
| `reports/laif_real_world_assessment.md` | MD | Generated real-world assessment report (deterministic) |
| `CLAUDE.md` | MD | AI assistant guidance for this repository |

---

*LAIF v1.2 · Compliance Toolkit v1.1 · April 2026*
