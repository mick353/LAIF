# Assessment Fragility Characterization

Phase 3H added assessment fragility characterization tests. Those tests document current assessment and validation behavior so that future changes are deliberate, reviewable, and easy to distinguish from accidental scoring drift.

The tests are diagnostic coverage only. They do not change LAIF scoring, validation behavior, assessment-engine behavior, policy requirements, protected artifacts, generated reports, verified-source manifests, or the verified corpus.

## Diagnostic Meaning

Formal LAIF compliance remains binary and strict. A document either satisfies the formal LAIF terminology and compliance gates currently implemented by the repository, or it does not. Conceptual similarity to LAIF concerns does not itself create formal compliance.

Scalar assessment scoring remains separate from formal PASS/FAIL outcomes. A document can receive nonzero structural, conceptual, auditability, enforceability, or readiness scores while still receiving formal LAIF compliance `FAIL`. Those scalar signals are calibration data; they are not substitutes for the formal compliance gate.

Conceptual proximity can therefore be nonzero while formal compliance fails. The current rubrics may detect risk-management, oversight, transparency, redress, documentation, or related governance ideas in a source without finding the canonical LAIF terms or construct coverage required for formal LAIF compliance.

Canonical LAIF terminology is intentionally load-bearing. Terms such as Coherence Test, Integrity Layer, Coupling, Consistency, Reversibility, Structural Transparency, Structural Honesty, and Structural Containment are not cosmetic labels in the current assessment model. They carry formal meaning and affect both terminology scoring and construct coverage.

The characterization tests also document known regex and context-window limitations. These limitations are calibration risks, not runtime failures. Plausible legal or regulatory phrasing may express operationally relevant governance ideas while still producing low or zero conceptual matches under the current rubric implementation.

## Known Calibration Risks

### Regex Fragility

Current rubric matching depends on explicit patterns. Plausible phrasing that is legally meaningful, operationally equivalent, or semantically close to a LAIF concept may not match a configured expression. A false negative in that situation means the current rubric did not recognize the phrasing; it does not prove that the source lacks governance substance.

### Context-Window Boundary Behavior

Paraphrase and contrast handling depends on finite context windows. Near-boundary examples can change classification when a canonical term or contrast phrase falls just inside or just outside the implemented window. Characterization coverage preserves this behavior so any later window adjustment is visible in review.

### Lexical Precision vs Operational Equivalence

The current model intentionally distinguishes canonical LAIF terminology from adjacent regulatory wording. This protects formal LAIF semantics, but it can also under-recognize source text that uses different legal language to express a similar operational control, duty, remedy, or accountability mechanism.

### Conceptual False Negatives

Some plausible legal or regulatory sentences may receive low or zero conceptual proximity because their phrasing does not activate the current conceptual rubrics. These are known calibration risks and potential future fixture candidates, not evidence that the assessment engine crashed or silently changed policy.

### Separation of Formal Compliance and Scalar Scoring

Formal compliance and scalar scoring answer different questions. Formal PASS/FAIL remains a strict LAIF gate, while scalar scores expose deterministic calibration signals for review. Nonzero conceptual or readiness scores must not be interpreted as converting a formal `FAIL` into formal `PASS`.

## Non-Goals

This documentation does not:

- change `validate.py`;
- change `assessment_engine.py`;
- loosen terminology requirements;
- convert conceptual proximity into formal compliance;
- modify reports, protected artifacts, or verified-source manifests;
- change governance checks;
- change tests;
- change scoring, detector, validation, or assessment semantics.

## Future Remediation Candidates

The following items are possible future work only. They are not implemented by this document:

- an optional richer semantic proximity layer that can be evaluated separately from formal LAIF compliance;
- expanded legal-phrase rubric fixtures covering plausible regulatory formulations and expected current outcomes;
- configurable context-window tests that make boundary behavior easier to review before any window-size change;
- stronger reporting labels for characterization failures so diagnostic false negatives are easier to distinguish from runtime failures;
- regression tests before any scoring adjustment, terminology adjustment, detector adjustment, or conceptual-rubric expansion.

## Review Discipline

Assessment fragility documentation should preserve the distinction between three categories:

1. current-engine behavior that is intentionally characterized by tests;
2. known false-negative calibration risk under existing regex and context-window rules;
3. future remediation candidates that require explicit review before implementation.

Any future change that alters scoring, validation, assessment logic, canonical terminology requirements, reports, protected artifacts, manifests, or tests should be reviewed as a behavior-changing or governance-sensitive change rather than as documentation-only work.
