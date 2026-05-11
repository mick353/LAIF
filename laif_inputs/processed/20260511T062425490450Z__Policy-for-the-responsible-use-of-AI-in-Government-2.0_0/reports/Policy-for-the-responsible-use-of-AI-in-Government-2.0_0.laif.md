## Document Processing Metadata

- **Processed at UTC / processed_at_utc:** 2026-05-11T06:24:25Z
- **Original input path:** laif_inputs/processed/20260511T062425490450Z__Policy-for-the-responsible-use-of-AI-in-Government-2.0_0/source/Policy for the responsible use of AI in Government 2.0_0.pdf
- **Original file name:** Policy for the responsible use of AI in Government 2.0_0.pdf
- **Source SHA-256:** 94beda4e6e9f61e0dd5d5f17b45b18cf6015b20fd9aabe41d20318f725273c11
- **Extractor used:** pypdf
- **Extracted characters:** 33440
- **Assessment mode:** external_framework
- **Sector profile:** government_service_delivery
- **Safe output stem:** Policy-for-the-responsible-use-of-AI-in-Government-2.0_0

---
# LAIF Institutional Structural Governance Assessment Report
**Report date:** May 2026  
**Framework:** LAIF v1.2 · Compliance Toolkit v1.1  
**Report architecture:** Public report template — Phase 3R  

## Executive Brief
- **Total documents assessed:** 1
- **LAIF-native certification summary:** 0/1 PASS; 1/1 FAIL / not LAIF-native / canonical remediation required where applicable.
- **Average overall readiness:** 41/100
- **Average conceptual proximity:** 65/100
- **Average sector alignment:** 40/100
- **Evidence trace summary:** 20 traces; 20 exact/deterministic; 0 reviewer-confirmation fallback.
- **Remediation patch summary:** 12 structured patches across assessed documents.

## Cross-Document Dashboard
| Document                                   | Mode               | LAIF-native status                                      | Overall score / band               | Sector profile              | Evidence traces | Patches | Cautions |
| ------------------------------------------ | ------------------ | ------------------------------------------------------- | ---------------------------------- | --------------------------- | --------------- | ------- | -------- |
| Policy for the responsible use of AI in Go | external_framework | FAIL / not LAIF-native / canonical remediation required | 41/100 — partial LAIF-model signal | Government Service Delivery | 20              | 12      | 4        |

### Common LAIF diagnostic gaps
structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present

## Per-Document Assessment

### Document 1: Policy for the responsible use of AI in Government 2.0 (Australia, DTA)

#### Executive Diagnostic Summary
- **Overall readiness:** 41/100 — partial LAIF-model signal
- **Conceptual proximity:** 65/100
- **Sector risk alignment:** 40/100
- **Remediation effort:** HIGH
- **Key LAIF-model risks:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Key LAIF-model strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: accountability; +15 more
- **Governance signal strength:** 41
- **Structural depth:** 33

#### Scorecard
| Dimension            | Score  | Fired signal labels                                                                                      | Missed signal labels                                                                                                                             |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Structural           | 33/100 | numbered sub-requirements; full lifecycle scope declared; risk stratification / proportionality; +2 more | mandatory obligation language (shall); threshold gate conditions (all must pass simultaneously); non-amendable constitutional hierarchy; +2 more |
| Terminology          | 0/100  | reviewer confirmation required                                                                           | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                               |
| Conceptual proximity | 65/100 | human rights / fundamental interests; transparency; accountability; +5 more                              | explainability / interpretability; contestability / redress; reversibility / modifiability; +1 more                                              |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms   | multiple mandatory obligations (shall … shall); specific, measurable obligations                                                                 |
| Enforceability       | 40/100 | named responsible parties; risk-proportionate thresholds                                                 | mandatory language (shall); enforcement consequences / penalties; non-discretionary operational mandates                                         |
| Overall readiness    | 41/100 | partial LAIF-model signal                                                                                | reviewer confirmation required                                                                                                                   |

#### Diagnostic Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)

#### Remediation Priorities
1. Implicit protective signals present but not declared as structural Coupling — detected: «ibly. Principles • Protect Australians from AI harms. • APS officers need to be able to explain, ju».
2. Structural governance architecture score critically low (33/100) — add mandatory obligation language (shall), threshold gate conditions, non-amendable constitutional hierarchy.
3. Enforceability score critically low (40/100) — add mandatory language (shall), enforcement consequences / penalties, non-discretionary operational mandates.
4. Coherence Test not applied — add PDCA Section B with Q1/Q2/Q3 documentation.
5. Integrity Layer not declared as a deployment precondition — add A.1/A.2/A.3 threshold conditions.

## Closing Interpretation Notes
- Public reports are diagnostics only and require evidence/authority review before institutional use.
- Formal LAIF-native failure remains formal failure; high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.
- This report does not determine legal validity and does not provide legal advice.
- See also: manual LAIF v1.2 assessment at reports/laif_assessment_aus_ai_policy_v2.md (Q1a IMPLICIT, Q1b SOFT, Coherence Test FAIL).

---
*LAIF v1.2 · Compliance Toolkit v1.1 · May 2026 · Public Report Template*  
*Generated by `test_real_world.py`; scoring logic, rubric weights, formal compliance calculation, certification gates, and validate.py enforcement unchanged.*