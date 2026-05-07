# LAIF Score Interpretation

LAIF scores are **deterministic LAIF rubric outputs**. They are generated from configured rubric signals and should be read as structured interpretation-layer data, not as legal authority.

Scores are not:

- legal determinations;
- statistical confidence values;
- external regulatory compliance ratings;
- proof that an external framework is valid, invalid, safe, unsafe, enforceable, or unenforceable under its own authority.

Scores support triage, comparison, review, and remediation prioritisation. They help reviewers identify which governance dimensions appear stronger or weaker under the LAIF model.

## Score Definitions

### `structural_score`

**Measures:** The extent to which the document expresses LAIF-relevant structural governance elements such as duties, controls, review mechanisms, accountability structures, and decision constraints.

**Does not measure:** Legal validity, full institutional effectiveness, or every possible governance safeguard outside the LAIF rubric.

**LAIF-native mode:** A useful signal for where the candidate document is structurally strong or weak, but it does not override strict LAIF-native PASS/FAIL requirements.

**External framework assessment mode:** A diagnostic indicator of structural proximity to LAIF governance expectations, without requiring LAIF vocabulary and without certifying the external framework.

### `terminology_score`

**Measures:** Presence of canonical LAIF terminology and explicitly recognized LAIF constructs.

**Does not measure:** Whether an external framework uses different language to create legally meaningful or operationally useful controls.

**LAIF-native mode:** Highly load-bearing. Missing canonical terminology can support LAIF-native certification failure because LAIF-native adoption requires canonical terms and structures.

**External framework assessment mode:** Diagnostic only. A low score means LAIF vocabulary is absent or limited; it does not mean the external framework is legally invalid, unsafe, valueless, or governance-worthless.

### `conceptual_proximity_score`

**Measures:** Whether the document addresses concepts similar to LAIF concerns, such as oversight, accountability, transparency, monitoring, risk management, redress, documentation, human interests, and lifecycle controls.

**Does not measure:** Formal LAIF compliance or certification readiness by itself.

**LAIF-native mode:** Helpful for remediation context, but conceptual proximity cannot convert a formal LAIF-native `FAIL` into a `PASS`.

**External framework assessment mode:** A diagnostic bridge showing substantive overlap with LAIF concerns even where canonical LAIF vocabulary is absent.

### `auditability_score`

**Measures:** Whether the document creates reviewable records, evidence artifacts, monitoring duties, logging, reporting, or independent verification hooks.

**Does not measure:** Whether an actual audit has been performed, whether evidence is truthful in practice, or whether an external auditor would reach a legal compliance conclusion.

**LAIF-native mode:** Indicates whether the document supports LAIF-native verification expectations, subject to strict certification requirements.

**External framework assessment mode:** Identifies how readily an independent reviewer could verify obligations under the LAIF model.

### `enforceability_score`

**Measures:** Whether obligations are framed with operational force: mandatory language, responsible actors, triggers, consequences, escalation, and remedies.

**Does not measure:** Court enforceability, regulator enforcement likelihood, contractual enforceability, or jurisdiction-specific legal authority.

**LAIF-native mode:** Supports review of whether LAIF-native obligations are stated with enough force to satisfy the framework.

**External framework assessment mode:** Diagnoses whether commitments appear aspirational or institutionally enforceable under the LAIF lens.

### `overall_readiness_score`

**Measures:** A deterministic aggregate readiness signal derived from current model weights across scoring dimensions.

**Does not measure:** Legal readiness, deployment approval, statistical confidence, or external regulatory compliance.

**LAIF-native mode:** Triage metadata only. A high readiness score cannot override a strict LAIF-native certification failure.

**External framework assessment mode:** Comparative diagnostic metadata for prioritising review and remediation across documents.

### `sector_risk_alignment`

**Measures:** Whether a document addresses sector-specific risk signals and evidence expectations for its assessed context, such as clinical, employment, procurement, government, or operational AI settings.

**Does not measure:** Complete sector compliance, real-world safety performance, or regulator acceptance.

**LAIF-native mode:** Helps reviewers see whether a LAIF-native candidate addresses the risk profile relevant to its deployment context.

**External framework assessment mode:** Shows whether the external document addresses sector risks that LAIF expects to see, without turning the result into certification.

## Score Weights and Calibration

Current score weights are deterministic model weights. They are reviewable and calibration-sensitive. A weight expresses how the current LAIF rubric values a signal for diagnostic and remediation purposes; it should not be presented as empirically validated or statistically validated unless future validation work supports that claim.

When score weights change, reviewers should treat the change as interpretation-layer or assessment-sensitive work depending on whether it affects outputs, thresholds, or public meaning. Score-weight changes should be documented so historical comparisons remain understandable.

## Phase 3N Structured Remediation Patch Schema

Structured remediation records are defined in [REMEDIATION_PATCH_SCHEMA.md](REMEDIATION_PATCH_SCHEMA.md). They convert existing diagnostic findings into machine-readable patches, controls, evidence artifacts, verification tests, and responsible-actor guidance. These records are diagnostic unless separately adopted by a regulator, institution, contract, procurement process, or other authority, and they do not determine legal validity or certify LAIF-native compliance.

## Phase 3P Evidence Trace Reference

Phase 3P evidence traces are deterministic source-support metadata only. Exact or deterministic traces require direct source-text presence; otherwise the reviewer-confirmation fallback is used. See [Evidence Trace Model](EVIDENCE_TRACE_MODEL.md).
