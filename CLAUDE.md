# CLAUDE.md — Law-Aligned Intelligence Framework (LAIF)

## Repository Overview

This repository holds the Law-Aligned Intelligence Framework (LAIF), a constitutional-level governance standard for AI systems, in two layers:

1. **The governance corpus** — the framework documents in `.docx` and `.txt` format (the "constitution" and its applied instruments).
2. **A Python enforcement toolchain** — a validation harness, an assessment engine that scores external governance documents against LAIF, a two-tier assessment corpus with machine-verified provenance, and test suites. Plain Python 3, standard library only — no third-party dependencies.

- **Version**: LAIF v1.2 | Compliance Toolkit v1.1
- **Date**: April 2026
- **Purpose**: Governance Audit Series — provides a unified, constitutional-level reasoning structure for evaluating AI deployments, policies, and regulatory decisions.

---

## Repository Structure

```
LAIF/
├── LAIF-Law-Aligned_Intelligence_Framework.txt   # Navigation index / START HERE
├── README.md                                      # Project overview
│
│  # Governance corpus (each .docx has a matching .txt export for search/programmatic access)
├── LAIF_Executive_Brief.docx          # 2-min overview; START HERE for new readers
├── LAIF_Public_Article.docx           # 5–7 min public-facing governance audit article
├── LAIF_v1.2.docx                     # CORE: The principal framework text (the "constitution")
├── LAIF_PDCA_GPT4_Clinical.docx       # Applied PDCA: GPT-4 Clinical Documentation Assistant
├── LAIF_Case_Analysis.docx            # Retrospective analysis across 8 AI governance failures
├── LAIF_Compliance_Toolkit.docx       # Operational definitions and standards (v1.1)
├── LAIF_Policy_Paper.docx             # Academic/policy paper: Coupling, Consistency, Reversibility
├── LAIF REGULATORY INTEGRATION GUIDE.docx  # Step-by-step EU AI Act + US federal integration
│
│  # Enforcement toolchain (Python 3, stdlib only)
├── laif_spec.py             # Canonical spec: terms, forbidden paraphrases, Integrity Layer, tiers
├── validate.py              # 9-check validation harness over the .txt corpus (exit 1 on rule failure)
├── assessment_engine.py     # 5-dimension scoring engine + markdown report generator
├── sample_documents.py      # Assessment corpus tier 2: REPRESENTATIVE_EXCERPT (illustrative)
├── official_documents.py    # Assessment corpus tier 1: OFFICIAL_EXCERPT (verbatim, SHA-256-pinned; citable)
├── corpus_manifest.md       # Provenance rules and per-document manifest for both corpus tiers
├── test_adversarial.py      # 82 adversarial tests against the guards and depth checks
├── test_provenance.py       # 48 provenance checks enforcing citability claims
├── test_semantic_fidelity.py # 41 checks against false negatives (substance w/o vocabulary) and false positives
├── test_real_world.py       # Assessment run over both corpora → reports/laif_real_world_assessment.md
│
├── docs/supporting/         # Verbatim ingested source texts (EO 14110, OECD, NIST AI 100-1, NHS DTAC)
└── reports/                 # Generated assessment report (deterministic; regenerate, don't hand-edit)
```

### Conceptual Document Hierarchy

The `.txt` index maps documents into three tiers:

| Tier | Purpose | Documents |
|------|---------|-----------|
| `01_START_HERE` | Orientation for new readers | Executive Brief, Public Article |
| `02_CORE_FRAMEWORK` | The authoritative framework text | LAIF v1.2 |
| `03_APPLICATIONS_AND_INTEGRATION` | Applied instruments and regulatory integration | PDCA, Regulatory Integration Guide, Case Analysis, Compliance Toolkit, Policy Paper |

---

## Core Framework Concepts

### The Three Foundational Principles (LAIF v1.2, Part One)

These are non-amendable and underpin every provision:

1. **Coherence Standard** — A governance provision is structurally coherent only if it is simultaneously:
   - **Coupled**: The restriction identifies and protects the specific human interest it serves. Neither can be weakened in isolation.
   - **Consistent**: The reasoning justifying the provision at one scale would also justify comparable provisions at significantly smaller and larger scales.
   - **Revisable**: Future actors can modify or reverse the provision without dismantling the broader governance architecture.

2. **Framework Hierarchy** — Operational standards (Toolkit) are subordinate to Provisions; Provisions are subordinate to Foundational Principles.

3. **Self-Application** — The framework applies to regulatory bodies and governance actors themselves, not only to AI system operators.

### The Coherence Test (Three Questions)

The primary decision instrument applied in the PDCA and case analyses:

- **Q1 — Coupling**: Does the deployment identify and protect the specific human interest at risk? (Most commonly failed.)
- **Q2 — Consistency**: Would the governance logic produce just and workable outcomes if applied across all comparable actors and scales?
- **Q3 — Reversibility**: Does the deployment preserve the capacity of future actors to reverse or modify its consequences?

A deployment must pass all three questions. Failure at Q1 constitutes automatic failure of the full Coherence Test.

### The Integrity Layer (LAIF v1.2, Part Two)

Three properties required as a **precondition of lawful deployment** — all must be satisfied simultaneously:

- **A.1 Structural Transparency**: The system can produce, on request, a comprehensible account of the basis for its outputs, including confidence/uncertainty and material limitations.
- **A.2 Structural Honesty**: Stated optimisation objectives correspond to actual implemented objectives. System performs consistently whether or not it is being evaluated.
- **A.3 Structural Containment**: The system operates within documented operational boundaries in all tested conditions (including edge cases) and does not initiate materially irreversible actions without triggering the appropriate authorisation process.

### The Pre-Deployment Coherence Assessment (PDCA)

The PDCA is the primary **operational instrument** of LAIF. It is a structured audit process applied before system deployment. It is structured into:

- **Section A** — Integrity Layer Verification (A.1–A.3 above)
- **Section B** — Coherence Test Documentation (Q1–Q3)
- Additional sections assess specific provision compliance

The applied PDCA in this repository (`LAIF_PDCA_GPT4_Clinical.docx`) assesses GPT-4-based clinical documentation assistants deployed in acute hospital settings (2023–2025).

---

## Document Conventions

### Terminology — Use Precisely

LAIF uses standardised terminology throughout. AI assistants working in this repository must use these terms exactly as defined:

| Term | Definition |
|------|-----------|
| **Coherence Test** | The three-question test (Coupling, Consistency, Reversibility) — always capitalised |
| **PDCA** | Pre-Deployment Coherence Assessment — the operational audit instrument |
| **Integrity Layer** | The three preconditions (Transparency, Honesty, Containment) |
| **Coupling** | The structural pairing of a restriction with the human interest it protects |
| **Provision** | A specific governance requirement derived from Foundational Principles (e.g. Provision A1, A2) |
| **Operational Standard** | A Toolkit-level definition subordinate to Provisions |
| **Materially Affects Interests** | An objective test — would a reasonable person regard the output as having legal, financial, health, reputational, or liberty consequences? |

### Document Format

Each document follows this pattern:
1. Title block (ALL CAPS framework name + document type + version + date)
2. Subtitle / scope statement
3. Cross-reference to related LAIF documents
4. Structured sections with decimal numbering (1.1, 1.2, A.1, A.2, etc.)

### Version Numbering

- Framework versions: `v1.2` (major.minor)
- Toolkit versions: `v1.1`
- Always include version and "April 2026" date in document headers when creating or updating documents

### Cross-References

Documents are explicitly cross-referenced. When referencing documents, use the standard citation format used throughout the corpus:

> `LAIF v1.2 Principal Text · PDCA-Full Assessment (GPT-4 Clinical) · Compliance Toolkit v1.1 · Regulatory Integration Guide · Case Analysis · Policy Paper`

---

## External Framework Integrations

LAIF v1.2 explicitly incorporates and integrates with:

| Framework | Integration Point |
|-----------|------------------|
| EU AI Act (Regulation 2024/1689) | Provision-by-provision mapping in Regulatory Integration Guide Part One |
| NIST AI RMF | Function-by-function mapping in Regulatory Integration Guide Part Two |
| OECD AI Principles | Cited throughout as background governance instrument |
| UNESCO AI Ethics Recommendation | Cited throughout as background governance instrument |
| Anthropic Constitutional AI | Incorporated feedback cited in v1.2 header |
| OMB M-24-18 (US federal procurement) | Integration workflow in Regulatory Integration Guide §2.3 |

---

## Working in This Repository

### Commands — Run All Three Before Any Commit

There is no build step, package manager, or CI pipeline — the toolchain is plain
Python 3 standard library. The pre-commit gate is these three commands, all of
which must exit 0:

```bash
python3 validate.py                 # 9-check harness over the .txt corpus (rule failures = exit 1)
python3 test_adversarial.py         # 82 adversarial tests on guards and structural-depth checks
python3 test_provenance.py          # 48 checks enforcing corpus citability claims
python3 test_semantic_fidelity.py   # 41 checks: substance never outranked by vocabulary; no false accusations
```

To regenerate the assessment report (also acts as an integration test):

```bash
python3 test_real_world.py    # writes reports/laif_real_world_assessment.md
```

The report must be deterministic: running it twice must produce no diff. Never
hand-edit `reports/` output — change the engine or corpus and regenerate.

### Corpus Provenance Rules (Machine-Enforced)

The assessment corpus has two evidence tiers (full rules in `corpus_manifest.md`):

- **`official_documents.py` (OFFICIAL_EXCERPT, citable)** — text is extracted
  verbatim at import from committed source files in `docs/supporting/` via unique
  start/end markers and pinned by SHA-256. Import fails if provenance cannot be
  proven. To add a document: commit the full verbatim source text to
  `docs/supporting/` first, then add markers and pin hashes (run the module's
  `__main__` to compute them).
- **`sample_documents.py` (REPRESENTATIVE_EXCERPT / SYNTHETIC_TEST_DOCUMENT,
  not citable)** — every entry must carry all four provenance fields
  (`provenance`, `source_url`, `source_note`, `intended_use`). Never classify an
  entry here as OFFICIAL_EXCERPT — `test_provenance.py` fails the build if you do.

Never present results computed from REPRESENTATIVE_EXCERPT text as findings about
the official source instrument. This is the reporting layer's own A.2 Structural
Honesty obligation.

### Semantic Fidelity Rules (Machine-Enforced)

LAIF is the measuring instrument, not an authority over other instruments'
vocabulary. `assessment_engine.py` therefore measures on two independent axes,
and both must be preserved by any change:

- **LAIF-native form** (formal gate, binary) — is the document written as a
  LAIF instrument? External frameworks are expected to fail this; that verdict
  says nothing about their substance.
- **Functional alignment** (per-construct) — is the *substance* of Coupling,
  the Integrity Layer, Consistency, Reversibility, and Self-Application
  expressed in the document's own vocabulary? Grounded in LAIF v1.2 Part Eight
  (equivalent structural diligence) and the Regulatory Integration Guide's
  SATISFIES/EXTENDS methodology.

Hard invariants (enforced by `test_semantic_fidelity.py`):
1. A document expressing LAIF's structural substance in its own vocabulary is
   never described as lacking protection, and never ranked below a
   vocabulary-only shell on any substance axis.
2. Language that *regulates* a hazard ("no irreversible action without
   authorisation") is never flagged as a Structural Honesty contradiction.
3. Paraphrase detections on documents that neither use nor claim LAIF
   vocabulary are informational divergence notes, not violations
   (validate.py's strict enforcement over LAIF's own corpus is unchanged).
4. Register never suppresses substance: "must"/"we will" carry the same
   signal weight as "shall".

### Editing Documents

- `.docx` files are Microsoft Word format. Edit with Word, LibreOffice, or programmatically with `python-docx`.
- Each governance document also has a `.txt` export; `validate.py` runs against the `.txt` corpus, so keep both formats in sync when editing.
- `LAIF-Law-Aligned_Intelligence_Framework.txt` is the navigation index.
- `docs/supporting/` holds verbatim ingested source texts (strict, no transformation). Editing these files breaks pinned hashes in `official_documents.py` by design — any change there must be re-verified against the authoritative source and re-pinned.

### Branch Conventions

The repository uses a `main` branch for stable releases. Feature work is done on named branches (e.g., `claude/add-claude-documentation-14U7T`).

### Commit Style

Commits are descriptive, scoped to one coherent change, and name the affected
layer (corpus, toolchain, reporting, docs):
```
Add OFFICIAL_EXCERPT corpus with machine-verified verbatim provenance
LAIF phase 2 tightening: implicit clarity + primary structural failure line
```

---

## Key Substantive Notes for AI Assistants

1. **Precision over fluency**: LAIF terminology is legal/constitutional in register. Do not paraphrase defined terms. "Coupling" is not the same as "alignment" or "connection."

2. **Hierarchy is load-bearing**: Operational Standards (Toolkit) can be revised without amending Foundational Principles; Provisions cannot contradict Principles. Any new content must respect this hierarchy.

3. **The Coherence Test is not a checklist**: The three questions are structurally interdependent — a provision that passes Q1 and Q2 but fails Q3 is not "mostly coherent." It fails.

4. **Self-application matters**: Regulatory bodies and governance actors are subject to LAIF, not only AI operators. This is not a minor note — it is Part Seven of the framework.

5. **Case analysis follows a fixed structure**: Each case in `LAIF_Case_Analysis.docx` has: factual summary → governance failure → Coherence Test application (Q1/Q2/Q3) → structural verdict → LAIF provisions that would have applied → adequacy of existing governance responses.

6. **The Integrity Layer is a threshold, not a score**: A system that partially satisfies A.1 does not receive partial credit — it fails A.1, and therefore fails the Integrity Layer precondition entirely.

7. **"Materially affects interests" is an objective test**: It does not depend on operator intent. The standard is whether a reasonable person in the affected person's situation would regard the output as material.
