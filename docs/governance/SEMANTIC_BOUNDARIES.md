# Semantic Boundaries

This document defines the repository boundaries that protect LAIF semantics, scoring logic, detector logic, interpretation logic, and assessment artifacts. It is a review policy, not an automated semantic scanner.

## Protected Semantic Categories

### LAIF Semantics

LAIF semantics include the canonical meaning of framework terms and decision structures, including the Coherence Test, Integrity Layer, PDCA, Coupling, Consistency, Reversibility, Structural Transparency, Structural Honesty, and Structural Containment.

Changing these meanings is a governance-sensitive change and requires dedicated review.

### Scoring Logic

Scoring logic includes numeric scores, thresholds, weights, pass/fail criteria, readiness calculations, and verdict calculations used by assessment tooling or reports.

Changes to scoring logic are governance-sensitive because they may alter assessment outcomes even when source text is unchanged.

### Detector Logic

Detector logic includes code or rules that identify framework conditions, paraphrase violations, concept anchoring, evidence-trace validity, manifest validity, verified-corpus integrity, and Coherence Test or Integrity Layer findings.

Changes to detector logic are governance-sensitive because they may alter what the repository recognizes as compliant, non-compliant, present, missing, verified, or unverified.

### Interpretation Logic

Interpretation logic includes the mapping from findings to conclusions, labels, readiness states, compliance descriptions, remediation priorities, report wording, or assessment meaning.

Interpretation refinements may be valid, but they must not be presented as unchanged if they alter the meaning or consequence of a finding.

### Assessment Artifacts

Assessment artifacts record assessment conclusions. They are not ordinary documentation. The initial protected assessment artifact is `reports/laif_full_assessment.md`.

## Semantic-Sensitive Files

Semantic-sensitive files may include:

- `validate.py`
- `assessment_engine.py`
- `test_adversarial.py`
- `test_real_world.py`
- `laif_spec.py`
- `sample_documents.py`
- `reports/laif_full_assessment.md`
- `LAIF_v1.2.txt`
- `LAIF_Compliance_Toolkit.txt`

A change to one of these files is not automatically prohibited. It must be reviewed according to what the change affects.

## Semantic-Sensitive Terminology

Semantic-sensitive terminology includes, at minimum:

- Coherence Test
- PDCA
- Integrity Layer
- Coupling
- Consistency
- Reversibility
- Structural Transparency
- Structural Honesty
- Structural Containment
- PASS / FAIL / PARTIAL
- assessment verdict
- scoring threshold
- detector
- interpretation layer
- detection layer

Terminology edits should preserve canonical meaning unless the pull request is explicitly dedicated to semantic revision.

## What Constitutes Semantic Drift

Semantic drift occurs when a change alters any of the following without being disclosed and reviewed as semantic work:

- the meaning of a LAIF concept;
- the conditions for passing or failing a test;
- a score, threshold, weight, or verdict calculation;
- detection behavior for framework concepts or evidence traces;
- interpretation of a finding or remediation priority;
- a published assessment conclusion;
- the evidentiary basis for an assessment artifact.

Semantic drift can occur through code, documentation, report text, test fixtures, or corpus inputs.

## What Requires Dedicated Review

Dedicated review is required for changes that:

- alter scoring, detector, or interpretation logic;
- change canonical LAIF terminology or definitions;
- update assessment artifacts;
- change source text used as assessment evidence;
- change validation behavior or pass/fail rules;
- change how provenance or verification status affects citation status.

Dedicated review should focus on the semantic effect of the change, not only on whether tests pass.

## What Does Not Usually Require Semantic Review

The following changes do not usually require dedicated semantic review when they preserve meaning and behavior:

- typo fixes in non-assessment documentation;
- navigation or formatting updates;
- provenance notes that do not alter verification status or citation claims;
- CI wiring that runs existing commands without changing them;
- documentation of existing procedures;
- adding governance documentation that describes review process without redefining LAIF concepts.

## Review Discipline

Reviewers should ask:

1. Does this change alter what LAIF means?
2. Does this change alter what passes, fails, or receives a score?
3. Does this change alter what the repository detects?
4. Does this change alter how findings are interpreted?
5. Does this change alter a recorded assessment artifact?

If the answer to any question is yes, the pull request is governance-sensitive and should receive dedicated review.

## Automation Boundary

This policy does not attempt heuristic semantic enforcement. Future automation, if added, should detect likely sensitive changes and route them to human review. Human reviewers remain authoritative for semantic approval decisions.
