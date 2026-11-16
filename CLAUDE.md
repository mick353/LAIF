# LAIF agent instructions

Read [current verified state](docs/verification/CURRENT.md),
[delivery tasks](docs/verification/OVERHAUL_TASKS.md), `AGENTS.md`,
[CONTRIBUTING.md](CONTRIBUTING.md) and the relevant source before changing work.
The detailed [engineering and framework reference](docs/governance/ENGINEERING_REFERENCE.md)
retains the terminology, architecture, detection invariants and provenance rules.

## User routes

- Browser users: [Getting started](docs/GETTING_STARTED.md).
- Clone, Python and batch users: [Local setup](docs/LOCAL_SETUP.md).
- [Documentation map](docs/README.md) separates these from research and historical evidence.
- The private Research Workspace has its own version and pinned engine. A local
  gate or merge does not prove deployment or live acceptance.

## Delivery and verification

Inspect current main, open PRs and uncommitted work. Use a fresh branch from
current main; preserve unrelated work. Main is authoritative. Do not force-push.
Use a standard merge commit for release unless the maintainer explicitly chooses
another supported strategy. No GitHub Actions runs or CI badges as evidence.

Run focused tests while developing, then the local release gate:

```bash
python3 scripts/laif_verify.py --full --base-ref origin/main
```

On Windows use `py -3 -X utf8` instead of `python3`. Skipped or unrun checks are
not passes. Record implementation, verification, merge, deployment and observed
acceptance separately. The task record must retain open dependencies.

## Semantic and source boundaries

Before scoring, detection, reporting, corpus or protected-artifact changes, read
[semantic boundaries](docs/governance/SEMANTIC_BOUNDARIES.md),
[merge policy](docs/governance/MERGE_POLICY.md) and
[protected artifacts](docs/governance/PROTECTED_ARTIFACTS.md). Isolate changes
requiring semantic review from unrelated cleanup; automated gates do not approve
meaning. Preserve canonical authored reasoning word for word; reader summaries
are separate fields.

Preserve both LAIF-native form and functional alignment. External documents need
not adopt LAIF vocabulary. Do not mistake a missing stated control for a breach
or an operational failure. The Integrity Layer is a threshold; the Coherence
Test requires all three questions. Defined terms and framework hierarchy remain
as specified by `LAIF_v1.2.txt`. The detailed reference states all detection guards.

Use exact ingested text, quotations and source identities. Never reconstruct
missing evidence from memory. Official excerpts require pinned verbatim sources;
representative excerpts and synthetic fixtures are not findings about the
original instruments. Custody, authoritative origin, extraction fidelity and
verification status are distinct. Keep DOCX/TXT governance exports in sync.

## Generated output and retention

Regenerate with `python3 test_real_world.py`; do not hand-edit generated reports.
Every generated artifact records the toolchain fingerprint. Changes to
`assessment_engine.py`, `validate.py`, `laif_spec.py`,
`scripts/laif_process_document.py`, `scripts/laif_evidence_display.py` or
`scripts/laif_auto_criteria.py`, or any sorted `laif_engine/*.py` source require
regeneration in the same change. The root engine is a compatibility API; moved
implementation remains part of the fingerprint. Two
successive generations must be byte-identical. Do not disguise a changed source
identity to claim reproducibility.

Protected historical narratives remain in `reports/`; see its README. Current
outputs, unique processed-source evidence and files supporting the live system
must stay. The owner permits deletion of confirmed redundant copies; record
retained paths and matching hashes before removal. Historical inventories remain
event evidence. Keep owner attachments and private documents out of commits.

## Claims and publication

LAIF provides document review, not independent scientific validation, legal
certification or model-safety testing. Automatic eight-criterion judgments are
provisional rule outputs with source witnesses. Keep them separate from authored
reasoning and operational proof. Label Codex exploratory predictions honestly;
do not attribute them to the owner or independent reviewers.

Report exact revision, source scope, evidence tier, uncertainties and failures.
Preserve prior failed experiments. Source/legal questions require appropriate
primary evidence and review. Static documentation cannot demonstrate adversarial
robustness or containment effectiveness.

Use the established Sites workflow for Site releases. Preserve the private
working workspace and its audience. A public read-only edition must have its own
content boundary and disclose document handling accurately. Verify published
behavior and downloaded bytes; do not turn responsive emulation into a claim
of physical-device or screen-reader acceptance.
