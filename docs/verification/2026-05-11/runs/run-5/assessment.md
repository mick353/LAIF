## Document Processing Metadata

- **Processed at UTC / processed_at_utc:** 2026-05-11T06:24:23Z
- **Original input path:** laif_inputs/processed/20260511T062420688877Z__OJ_L_202401689_EN_TXT/source/OJ_L_202401689_EN_TXT.pdf
- **Original file name:** OJ_L_202401689_EN_TXT.pdf
- **Source SHA-256:** bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e
- **Extractor used:** pypdf
- **Extracted characters:** 624119
- **Assessment mode:** external_framework
- **Sector profile:** government_service_delivery
- **Safe output stem:** OJ_L_202401689_EN_TXT

---
# LAIF Institutional Structural Governance Assessment Report
**Report date:** May 2026  
**Framework:** LAIF v1.2 · Compliance Toolkit v1.1  
**Report architecture:** Public report template — Phase 3R  

## Executive Brief
- **Total documents assessed:** 1
- **LAIF-native certification summary:** 0/1 PASS; 1/1 FAIL / not LAIF-native / canonical remediation required where applicable.
- **Average overall readiness:** 60/100
- **Average conceptual proximity:** 76/100
- **Average sector alignment:** 60/100
- **Evidence trace summary:** 20 traces; 20 exact/deterministic; 0 reviewer-confirmation fallback.
- **Remediation patch summary:** 12 structured patches across assessed documents.

## Cross-Document Dashboard
| Document              | Mode               | LAIF-native status                                      | Overall score / band                   | Sector profile              | Evidence traces | Patches | Cautions |
| --------------------- | ------------------ | ------------------------------------------------------- | -------------------------------------- | --------------------------- | --------------- | ------- | -------- |
| OJ_L_202401689_EN_TXT | external_framework | FAIL / not LAIF-native / canonical remediation required | 60/100 — substantial LAIF-model signal | Government Service Delivery | 20              | 12      | 3        |

### Common LAIF diagnostic gaps
structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; terminological (paraphrase) — forbidden substitutions detected

## Per-Document Assessment

### Document 1: OJ_L_202401689_EN_TXT (EU AI Act)

#### Executive Diagnostic Summary
- **Overall readiness:** 60/100 — substantial LAIF-model signal
- **Conceptual proximity:** 76/100
- **Sector risk alignment:** 60/100
- **Remediation effort:** MEDIUM
- **Key LAIF-model risks:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; terminological (paraphrase) — forbidden substitutions detected
- **Key LAIF-model strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: explainability / interpretability; +19 more
- **Governance signal strength:** 60
- **Structural depth:** 50

#### Scorecard
| Dimension            | Score  | Fired signal labels                                                                                                             | Missed signal labels                                                                                                 |
| -------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Structural           | 50/100 | numbered sub-requirements; mandatory obligation language (shall); risk stratification / proportionality; +3 more                | full lifecycle scope declared; non-amendable constitutional hierarchy; self-application clause (Part Seven); +1 more |
| Terminology          | 0/100  | reviewer confirmation required                                                                                                  | Coupling; Coherence Test; Integrity Layer; +4 more                                                                   |
| Conceptual proximity | 76/100 | human rights / fundamental interests; transparency; explainability / interpretability; +6 more                                  | proportionality; reversibility / modifiability; fairness / labour / non-discrimination                               |
| Auditability         | 80/100 | multiple mandatory obligations (shall … shall); numbered traceable requirements; evidence / documentation requirements; +1 more | specific, measurable obligations                                                                                     |
| Enforceability       | 80/100 | mandatory language (shall); named responsible parties; enforcement consequences / penalties; +1 more                            | risk-proportionate thresholds                                                                                        |
| Overall readiness    | 60/100 | substantial LAIF-model signal                                                                                                   | reviewer confirmation required                                                                                       |

#### Diagnostic Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)
- Paraphrase violation — forbidden substitution of 'Coupling' (6 instances): PDF extraction artefact from 'this Regulation' — not a substantive finding

#### Remediation Priorities
1. Structural Coupling not declared — add explicit pairing of each restriction with the specific human interest it protects.
2. Coherence Test not applied — add PDCA Section B with Q1/Q2/Q3 documentation.
3. Integrity Layer not declared as a deployment precondition — add A.1/A.2/A.3 threshold conditions.
4. For service-delivery decisions, identify the protected public interest, decision trigger, reasons-for-decision record, administrative review pathway, and records-retention owner.
5. Constitutional hierarchy not declared — declare three-tier LAIF hierarchy explicitly.

## Closing Interpretation Notes
- Public reports are diagnostics only and require evidence/authority review before institutional use.
- Formal LAIF-native failure remains formal failure; high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.
- This report does not determine legal validity and does not provide legal advice.

---
*LAIF v1.2 · Compliance Toolkit v1.1 · May 2026 · Public Report Template*  
*Generated by `test_real_world.py`; scoring logic, rubric weights, formal compliance calculation, certification gates, and validate.py enforcement unchanged.*