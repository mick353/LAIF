## Document Processing Metadata

- **Processed at UTC / processed_at_utc:** 2026-05-11T06:24:20Z
- **Original input path:** laif_inputs/processed/20260511T062419749446Z__NIST.AI.100-1/source/NIST.AI.100-1.pdf
- **Original file name:** NIST.AI.100-1.pdf
- **Source SHA-256:** 7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1
- **Extractor used:** pypdf
- **Extracted characters:** 106492
- **Assessment mode:** external_framework
- **Sector profile:** government_service_delivery
- **Safe output stem:** NIST.AI.100-1

---
# LAIF Institutional Structural Governance Assessment Report
**Report date:** May 2026  
**Framework:** LAIF v1.2 · Compliance Toolkit v1.1  
**Report architecture:** Public report template — Phase 3R  

## Executive Brief
- **Total documents assessed:** 1
- **LAIF-native certification summary:** 0/1 PASS; 1/1 FAIL / not LAIF-native / canonical remediation required where applicable.
- **Average overall readiness:** 59/100
- **Average conceptual proximity:** 82/100
- **Average sector alignment:** 40/100
- **Evidence trace summary:** 20 traces; 20 exact/deterministic; 0 reviewer-confirmation fallback.
- **Remediation patch summary:** 12 structured patches across assessed documents.

## Cross-Document Dashboard
| Document      | Mode               | LAIF-native status                                      | Overall score / band               | Sector profile              | Evidence traces | Patches | Cautions |
| ------------- | ------------------ | ------------------------------------------------------- | ---------------------------------- | --------------------------- | --------------- | ------- | -------- |
| NIST.AI.100-1 | external_framework | FAIL / not LAIF-native / canonical remediation required | 59/100 — partial LAIF-model signal | Government Service Delivery | 20              | 12      | 3        |

### Common LAIF diagnostic gaps
structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present

## Per-Document Assessment

### Document 1: NIST.AI.100-1 (PDF)

#### Executive Diagnostic Summary
- **Overall readiness:** 59/100 — partial LAIF-model signal
- **Conceptual proximity:** 82/100
- **Sector risk alignment:** 40/100
- **Remediation effort:** HIGH
- **Key LAIF-model risks:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Key LAIF-model strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: explainability / interpretability; +21 more
- **Governance signal strength:** 59
- **Structural depth:** 41

#### Scorecard
| Dimension            | Score  | Fired signal labels                                                                                             | Missed signal labels                                                                                                                            |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 41/100 | numbered sub-requirements; mandatory obligation language (shall); full lifecycle scope declared; +3 more        | threshold gate conditions (all must pass simultaneously); non-amendable constitutional hierarchy; self-application clause (Part Seven); +1 more |
| Terminology          | 0/100  | reviewer confirmation required                                                                                  | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                              |
| Conceptual proximity | 82/100 | human rights / fundamental interests; transparency; explainability / interpretability; +7 more                  | reversibility / modifiability; traceability / responsibility                                                                                    |
| Auditability         | 80/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms; +1 more | multiple mandatory obligations (shall … shall)                                                                                                  |
| Enforceability       | 80/100 | mandatory language (shall); named responsible parties; risk-proportionate thresholds; +1 more                   | non-discretionary operational mandates                                                                                                          |
| Overall readiness    | 59/100 | partial LAIF-model signal                                                                                       | reviewer confirmation required                                                                                                                  |

#### Diagnostic Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)

#### Remediation Priorities
1. Implicit protective signals present but not declared as structural Coupling — detected: «an AI actor who is responsible for deploying that pre-trained model in a specific use case».
2. Structural governance architecture score critically low (41/100) — add threshold gate conditions, non-amendable constitutional hierarchy, self-application clause (Part Seven).
3. Coherence Test not applied — add PDCA Section B with Q1/Q2/Q3 documentation.
4. Integrity Layer not declared as a deployment precondition — add A.1/A.2/A.3 threshold conditions.
5. Constitutional hierarchy not declared — declare three-tier LAIF hierarchy (Foundational Principles → Provisions → Operational Standards).

## Closing Interpretation Notes
- Public reports are diagnostics only and require evidence/authority review before institutional use.
- Formal LAIF-native failure remains formal failure; high semantic proximity cannot override formal LAIF-native failure.
- This report does not determine legal validity and does not provide legal advice.

---
*LAIF v1.2 · Compliance Toolkit v1.1 · May 2026 · Public Report Template*  
*Generated by `test_real_world.py`; scoring logic, rubric weights, formal compliance calculation, certification gates, and validate.py enforcement unchanged.*