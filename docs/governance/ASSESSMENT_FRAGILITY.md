# Assessment Fragility Characterization

Phase 3H added assessment fragility characterization tests. Those tests document current assessment and validation behavior so that future changes are deliberate, reviewable, and easy to distinguish from accidental scoring drift.

The tests are diagnostic coverage only. Phase 3J adds assessment-mode labels to the assessment-engine output, but it does not change LAIF scoring weights, strict validation behavior, policy requirements, protected artifacts, committed generated reports, verified-source manifests, or the verified corpus.

## Related Interpretation Documents

Phase 3L adds interpretation-layer references that clarify result channels without changing assessment logic. See:

- [`RESULT_TAXONOMY.md`](RESULT_TAXONOMY.md) for the distinction between infrastructure PASS/FAIL, LAIF-native certification PASS/FAIL, external framework diagnostic findings, repository governance checks, and legal validity non-determination;
- [`SCORE_INTERPRETATION.md`](SCORE_INTERPRETATION.md) for how deterministic rubric scores should and should not be read;
- [`GOVERNANCE_FORCE_MODEL.md`](GOVERNANCE_FORCE_MODEL.md) for the practical lens LAIF uses to assess whether institutional AI governance principles become enforceable, auditable, reversible, accountable governance force.

These documents preserve the Phase 3J/3K separation between strict LAIF-native certification and external framework diagnostic assessment. They do not weaken the rule that formal LAIF compliance remains binary and strict, and they do not convert conceptual proximity into certification.

## Diagnostic Meaning

Formal LAIF compliance remains binary and strict. A document either satisfies the formal LAIF terminology and compliance gates currently implemented by the repository, or it does not. Conceptual similarity to LAIF concerns does not itself create formal compliance.

Scalar assessment scoring remains separate from formal PASS/FAIL outcomes. A document can receive nonzero structural, conceptual, auditability, enforceability, or readiness scores while still receiving formal LAIF compliance `FAIL`. Those scalar signals are calibration data; they are not substitutes for the formal compliance gate.

Conceptual proximity can therefore be nonzero while formal compliance fails. The current rubrics may detect risk-management, oversight, transparency, redress, documentation, or related governance ideas in a source without finding the canonical LAIF terms or construct coverage required for formal LAIF compliance.

Canonical LAIF terminology is intentionally load-bearing. Terms such as Coherence Test, Integrity Layer, Coupling, Consistency, Reversibility, Structural Transparency, Structural Honesty, and Structural Containment are not cosmetic labels in the current assessment model. They carry formal meaning and affect both terminology scoring and construct coverage.

The characterization tests also document known regex and context-window limitations. These limitations are calibration risks, not runtime failures. Plausible legal or regulatory phrasing may express operationally relevant governance ideas while still producing low or zero conceptual matches under the current rubric implementation.

## Phase 3J Assessment Modes

Phase 3J separates two questions that previously appeared too close together in public report language:

1. **LAIF-native certification mode** asks whether a document satisfies LAIF's own formal requirements. Canonical terminology remains load-bearing in this mode. A certification claim requires the implemented formal gate to pass; conceptual proximity, readiness, auditability, or enforceability scores cannot convert a formal `FAIL` into `PASS`.
2. **External framework assessment mode** asks how an external law, standard, vendor policy, or governance framework maps diagnostically against LAIF structural expectations. This mode is assessment and remediation metadata only; it is not LAIF-native certification.

The assessment engine now surfaces explicit mode metadata: `assessment_mode`, `formal_laif_native_compliance`, `external_framework_assessment`, and `laif_canonical_remediation_required`. The legacy fields `formal_laif_compliance`, `strong_laif_compliance`, score fields, and `score_breakdown` remain present for compatibility.

In external framework assessment mode, absent LAIF vocabulary should be read as **not LAIF-native / canonical remediation required**. It must not be read as a claim that the external instrument is legally invalid, governance-invalid, unsafe, unenforceable under its own authority, or valueless. External frameworks may express significant governance substance using their own legal or policy vocabulary while still failing LAIF-native certification because they do not adopt LAIF's canonical structures.

Conceptual proximity is diagnostic/remediation metadata. It can show that an external framework addresses related governance concerns such as risk management, oversight, transparency, redress, documentation, monitoring, or accountability. It does not certify LAIF compliance and does not relax the binary formal gate.

Canonical terminology is mandatory only for LAIF-native certification claims. External framework diagnostics may recommend canonical remediation where an organisation wants to adopt LAIF, but those recommendations are additive mapping guidance rather than a judgment that the external framework is structurally or legally invalid on its own terms.

## Phase 3K Public Output Wording Safety

Public console and generated markdown report sections should label external framework outcomes with explicit mode context. Reports should say **LAIF-native certification** for the strict binary gate and **External framework structural assessment** for diagnostic mapping. When an external framework lacks canonical LAIF terminology, public wording should use **not LAIF-native / canonical remediation required** and explain that this is diagnostic, not certification. Public headings should prefer scoped labels such as **Primary LAIF structural remediation gap**, **LAIF-native certification verdict**, **Diagnostic deployment risk tier**, and **LAIF-model interpretation**. Public output must not equate not-LAIF-native status with legal invalidity, governance invalidity, governance worthlessness, or structural incoherence on the framework's own terms.

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
- richer assessment-mode displays for downstream consumers while preserving strict LAIF-native certification semantics;
- regression tests before any scoring adjustment, terminology adjustment, detector adjustment, or conceptual-rubric expansion.

## Review Discipline

Assessment fragility documentation should preserve the distinction between three categories:

1. current-engine behavior that is intentionally characterized by tests;
2. known false-negative calibration risk under existing regex and context-window rules;
3. future remediation candidates that require explicit review before implementation.

Any future change that alters scoring, validation, assessment logic, canonical terminology requirements, reports, protected artifacts, manifests, or tests should be reviewed as a behavior-changing or governance-sensitive change rather than as documentation-only work.

## Phase 3N Structured Remediation Patch Schema

Structured remediation records are defined in [REMEDIATION_PATCH_SCHEMA.md](REMEDIATION_PATCH_SCHEMA.md). They convert existing diagnostic findings into machine-readable patches, controls, evidence artifacts, verification tests, and responsible-actor guidance. These records are diagnostic unless separately adopted by a regulator, institution, contract, procurement process, or other authority, and they do not determine legal validity or certify LAIF-native compliance.

## Phase 3P Evidence Trace Reference

Phase 3P evidence traces are deterministic source-support metadata only. Exact or deterministic traces require direct source-text presence; otherwise the reviewer-confirmation fallback is used. See [Evidence Trace Model](EVIDENCE_TRACE_MODEL.md).

## Phase 3Q Calibration and Score Justification Reference

See [CALIBRATION_SCORE_JUSTIFICATION.md](CALIBRATION_SCORE_JUSTIFICATION.md) for the shared boundary governing score bands, score justification metadata, dimension justifications, calibration cautions, gaming-risk notes, evidence/sector/remediation relationships, and the rule that LAIF-model signal strength does not determine legal validity or certify LAIF-native compliance.
