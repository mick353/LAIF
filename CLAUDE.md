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
├── README.md                                      # Project description and contents
├── CLAUDE.md                                      # This file — AI assistant guidance
│
│  # Governance corpus (each .docx has a matching .txt export for search/programmatic access)
├── LAIF_Executive_Brief.docx / .txt   # 2-min overview; START HERE for new readers
├── LAIF_Public_Article.docx / .txt    # 5–7 min public-facing governance audit article
├── LAIF_v1.2.docx / .txt              # CORE: The principal framework text (the "constitution")
├── LAIF_PDCA_GPT4_Clinical.docx / .txt        # Applied PDCA: GPT-4 Clinical Documentation Assistant
├── LAIF_Case_Analysis.docx / .txt             # Retrospective analysis across 8 AI governance failures
├── LAIF_Compliance_Toolkit.docx / .txt        # Operational definitions and standards (v1.1)
├── LAIF_Policy_Paper.docx / .txt              # Academic/policy paper: Coupling, Consistency, Reversibility
├── LAIF REGULATORY INTEGRATION GUIDE.docx     # Step-by-step EU AI Act + US federal integration
│   └── LAIF_Regulatory_Integration_Guide.txt
│
│  # Enforcement toolchain (Python 3, stdlib only)
├── laif_spec.py             # Canonical spec: terms, forbidden paraphrases, Integrity Layer, tiers, provenance classes
├── validate.py              # Validation harness over the .txt corpus (exit 1 on rule failure)
├── assessment_engine.py     # Scoring engine, functional-alignment layer, governance-repair reporting
├── sample_documents.py      # Assessment corpus tier 2: REPRESENTATIVE_EXCERPT (illustrative)
├── official_documents.py    # Assessment corpus tier 1: OFFICIAL_EXCERPT (verbatim, SHA-256-pinned; citable)
├── corpus_manifest.md       # Provenance rules and per-document manifest for both corpus tiers
├── test_adversarial.py      # Adversarial tests against the guards and depth checks
├── test_provenance.py       # Provenance checks enforcing citability claims
├── test_semantic_fidelity.py # Semantic-fidelity invariants (substance vs vocabulary; no false accusations)
├── test_real_world.py       # Assessment run over both corpora → reports/laif_real_world_assessment.md
├── scripts/                 # Batch document processing + governance tooling
├── tests/                   # Governance, fragility, and processing-runner suites
│
├── docs/supporting/         # Verbatim ingested source texts (EO 14110, OECD, NIST AI 100-1, NHS DTAC)
├── docs/governance/         # Contributor-facing process policy (merge, rollback, protected artifacts)
├── docs/verified/           # Evidence traces and verified ingestion manifests
├── laif_inputs/             # Batch-processing input/processed queues
└── reports/                 # Generated assessment reports (deterministic; regenerate, don't hand-edit)
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

- **Q1 — Coupling**: Does the deployment identify and protect the specific human interest at risk? (Most commonly failed.) Under the **refined model v1.1**, Q1 is assessed on two sub-dimensions:
  - **Q1a — Structural Pairing** (`NONE` / `IMPLICIT` / `EXPLICIT`): Does the instrument's architecture pair each restriction with the specific human interest it protects?
  - **Q1b — Enforcement Strength** (`NONE` / `SOFT` / `HARD`): Does the pairing carry enforceable normative force equivalent to the restriction imposed?
- **Q2 — Consistency**: Would the governance logic produce just and workable outcomes if applied across all comparable actors and scales?
- **Q3 — Reversibility**: Does the deployment preserve the capacity of future actors to reverse or modify its consequences?

A deployment must pass all three questions. Failure at Q1 constitutes automatic failure of the full Coherence Test. The Q1a/Q1b split is an **interpretation-layer refinement only** — it does not alter the detection logic or the pass/fail structure of the Coherence Test.

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

### Commands — The Pre-Commit Gate

The toolchain is plain Python 3 standard library (no package manager needed);
CI (.github/workflows/ci.yml) runs the same gate. All of these must exit 0
before any commit:

```bash
python3 validate.py                 # validation harness over the .txt corpus (rule failures = exit 1)
python3 test_adversarial.py         # adversarial tests on guards and structural-depth checks
python3 test_provenance.py          # provenance checks enforcing corpus citability claims
python3 test_semantic_fidelity.py   # semantic-fidelity invariants: substance never outranked by vocabulary
python3 tests/test_governance.py    # governance/reporting suite
python3 tests/test_assessment_fragility.py          # fragility suite
python3 tests/test_document_processing_runner.py    # batch runner suite
python3 tests/test_github_actions_document_processing.py  # CI processing suite
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
- `LAIF-Law-Aligned_Intelligence_Framework.txt` is the navigation index; `README.md` is the public-facing project description.
- `docs/supporting/` holds verbatim ingested source texts (strict, no transformation). Editing these files breaks pinned hashes in `official_documents.py` by design — any change there must be re-verified against the authoritative source and re-pinned.

### Running Assessment Tools

The Python tooling (`assessment_engine.py`, `validate.py`, test suites, `scripts/`) requires no build step — run directly with `python3`. `corpus_manifest.md` documents provenance classifications for both corpus tiers (`official_documents.py`, `sample_documents.py`).

---

## Repository Governance

See `CONTRIBUTING.md` and `docs/governance/` for contributor-facing review policy, protected artifact awareness, semantic-boundary definitions, merge expectations, and rollback procedures. These governance documents are process guidance and do not alter LAIF semantics, scoring logic, detector logic, interpretation logic, or assessment artifacts.

### Authoritative Branch Policy

**`main` is the sole authoritative branch.** No assessment artifact, scoring result, or interpretation refinement is canonical until it has been merged into `main`.

- Feature branches are temporary working branches. They hold work in progress and are deleted or left inactive after merge.
- All changes — including reporting-layer and interpretation-layer changes — are repository changes and must be committed and merged to `main` to take effect.
- Force-pushing to `main` is prohibited. Merge via standard merge commit, not rebase.

### Assessment Workflow

The standard workflow for producing a LAIF assessment:

1. **Source ingestion** — extract full text from supplied documents into `docs/supporting/` using Strict Source Mode (no training-derived content; all factual claims must be traceable to the ingested file).
2. **Assessment** — apply LAIF v1.2 framework using only ingested source files and `LAIF_v1.2.txt`. Record verbatim quotes for all findings.
3. **Write artifact** — write the complete assessment to `reports/laif_full_assessment.md` (or a named variant for a new corpus).
4. **Merge to main** — commit and push. The artifact is not authoritative until on `main`.

### Merge Discipline

- Merge feature branches into `main` before writing the final assessment artifact. This ensures the ingested source files referenced in the assessment are present on `main` when the assessment is committed.
- Do not write assessment artifacts on feature branches and then push separately — the source documents and assessment must arrive on `main` together.

### Interpretation-Layer vs Detection-Layer Distinction

These two layers are **independently revisable**:

| Layer | What it governs | Can be changed without |
|-------|----------------|------------------------|
| **Detection layer** | Whether Q1/Q2/Q3 pass or fail; Integrity Layer thresholds; what counts as PASS/FAIL | Changing the Coherence Test definitions in LAIF v1.2 |
| **Interpretation layer** | How results are expressed, sub-classified, or contextualised (e.g. Q1a/Q1b split; Governance Durability; Reflexivity) | Changing detection logic or pass/fail outcomes |

Interpretation-layer refinements (adding dimensions, splitting classifications) are reporting changes. They must not alter: detection verdicts, Coherence Test pass/fail results, Integrity Layer assessments, or sourced reasoning. Any change that would reverse a PASS to FAIL or vice versa is a detection-layer change and requires explicit justification against LAIF v1.2.

### Publication Artifact Locations

| Artifact | Location | Status |
|----------|----------|--------|
| Authoritative full corpus assessment | `reports/laif_full_assessment.md` | Canonical once on `main` |
| Ingested source documents | `docs/supporting/` | Primary evidence; do not modify after ingestion |
| Framework corpus (assessment engine inputs) | `sample_documents.py` + `corpus_manifest.md` | See provenance classifications before citing |

### Reproducibility

Any assessment produced from the ingested files in `docs/supporting/` and `LAIF_v1.2.txt` should reproduce the same PASS/FAIL verdicts under LAIF v1.2 detection logic. Interpretation-layer dimensions (Durability, Reflexivity, Q1a/Q1b) may be refined by future reviewers provided they are labelled as such and do not alter the underlying Coherence Test results.

### Commit Style

Commits are descriptive, scoped to one coherent change, and name the affected
layer (corpus, toolchain, reporting, docs):

```
Add OFFICIAL_EXCERPT corpus with machine-verified verbatim provenance
LAIF: full source ingestion (strict, no transformation)
LAIF: publication-prep pass — formatting, README, governance docs
```

---


### Verified Corpus Acquisition Channels

Verified corpus provenance must distinguish custody from authority. Supported acquisition channels are:

- `AUTOMATED_URL_RETRIEVAL` — tooling fetches directly from the authoritative origin URL.
- `HUMAN_GITHUB_DEPOSIT` — a human downloads the authoritative source and deposits it into `docs/verified/manual_ingest/` through GitHub or commit.
- `HUMAN_SESSION_UPLOAD` — a human supplies the authoritative source through the active session and the agent writes the exact supplied file into `docs/verified/manual_ingest/`.

The acquisition channel does not itself prove authority. Authority requires `authoritative_origin_url`, acquisition metadata, SHA256 hash records, a transformation chain, citation status, provenance classification, and verification status. `HUMAN_ATTESTED_AUTHORITATIVE` means a human supplied the file and asserted its authoritative origin; `HASH_VERIFIED_LOCAL_ONLY` means only local repository integrity is proven; `NETWORK_BLOCKED_PENDING_HUMAN_SOURCE` is non-terminal and must not be treated as a failed or fabricated source.

No assessment may be performed from memory, reconstructed missing text, paraphrased substitute text, or screenshots unless explicitly marked non-citable.

## Key Substantive Notes for AI Assistants

1. **Precision over fluency**: LAIF terminology is legal/constitutional in register. Do not paraphrase defined terms. "Coupling" is not the same as "alignment" or "connection."

2. **Hierarchy is load-bearing**: Operational Standards (Toolkit) can be revised without amending Foundational Principles; Provisions cannot contradict Principles. Any new content must respect this hierarchy.

3. **The Coherence Test is not a checklist**: The three questions are structurally interdependent — a provision that passes Q1 and Q2 but fails Q3 is not "mostly coherent." It fails.

4. **Self-application matters**: Regulatory bodies and governance actors are subject to LAIF, not only AI operators. This is not a minor note — it is Part Seven of the framework.

5. **Case analysis follows a fixed structure**: Each case in `LAIF_Case_Analysis.docx` has: factual summary → governance failure → Coherence Test application (Q1/Q2/Q3) → structural verdict → LAIF provisions that would have applied → adequacy of existing governance responses.

6. **The Integrity Layer is a threshold, not a score**: A system that partially satisfies A.1 does not receive partial credit — it fails A.1, and therefore fails the Integrity Layer precondition entirely.

7. **"Materially affects interests" is an objective test**: It does not depend on operator intent. The standard is whether a reasonable person in the affected person's situation would regard the output as material.
