# LAIF Real-World Assessment Report
**Framework version:** LAIF v1.2 · Compliance Toolkit v1.1  
**Date:** May 2026  
**Classification:** Governance Assessment — Controlled Exploration Phase  
**Validator:** validate.py (unchanged — strict formal compliance enforced)  

## Executive Summary
4 of 4 external AI governance frameworks assessed fail formal LAIF v1.2 compliance. Formal compliance is binary and strict — no partial credit is awarded for proximity to LAIF requirements.

However, the dimensional scoring reveals a more nuanced picture. Documents achieve an average conceptual proximity score of 58/100 and an average overall readiness score of 36/100, indicating that the underlying governance intent is broadly present — expressed through different vocabulary and structural frameworks.

**Core finding:** The gap between real-world governance language and formal LAIF compliance is terminological and structural, not conceptual. These frameworks address the right problems but do not enforce them through structural Coupling, the Coherence Test, or the Integrity Layer. LAIF is measurably stricter than current governance language.

## Method
Each document was assessed against two complementary layers:

**Layer 1 — Formal LAIF compliance (binary):** Checks for 8 required constructs:
Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles, non-amendable clause, self-application clause (Part Seven), Integrity Layer FINDING block, and Coherence Test FINDING block. All 8 must be present. This check is strict and is performed by the existing validate.py harness without modification.

**Layer 2 — Dimensional scoring (diagnostic):** Five dimensions scored 0–100 independently to identify strengths, gaps, and remediation priorities. A document may fail formal compliance while scoring high on conceptual proximity — this is expected and meaningful.

Documents analysed:
- **EU AI Act — Art. 9, 13 & 14** (Regulation (EU) 2024/1689 of the European Parliament and of the Council)
- **NIST AI RMF — Govern & Map Functions** (NIST AI Risk Management Framework 1.0 (NIST AI 100-1))
- **OECD AI Principles (2019, rev. 2024)** (OECD Principles on AI, adopted May 2019, revised 2024)
- **US Executive Order 14110 — §4 Safety & §7 Workers** (Executive Order 14110 on Safe, Secure, and Trustworthy AI (Oct 30, 2023))

## Scoring Model
| Dimension            | Weight | Description                                                                                         |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------- |
| Structural           | 25%    | Explicit governance architecture: named tests, hierarchy, thresholds, review mechanisms             |
| Terminology          | 15%    | Canonical LAIF term presence: Coupling, Coherence Test, Integrity Layer, etc.                       |
| Conceptual Proximity | 20%    | LAIF-like concepts expressed without LAIF terms: rights, oversight, proportionality, contestability |
| Auditability         | 20%    | Objective checkability: numbered obligations, evidence requirements, review mechanisms              |
| Enforceability       | 20%    | Operational enforcement: mandatory language, assignable duties, thresholds, consequences            |

**Overall Readiness Score** = Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20

**Remediation Effort:** VERY HIGH (<35) · HIGH (35–59) · MEDIUM (60–74) · LOW (≥75)

## Per-Document Scorecards

### EU AI Act — Art. 9, 13 & 14
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** binding_regulation  
**Remediation Effort:** HIGH


#### Scores
| Dimension             | Score      | Visual     |
| --------------------- | ---------- | ---------- |
| Structural            | 41/100     | ████░░░░░░ |
| Terminology           | 0/100      | ░░░░░░░░░░ |
| Conceptual Proximity  | 49/100     | █████░░░░░ |
| Auditability          | 60/100     | ██████░░░░ |
| Enforceability        | 60/100     | ██████░░░░ |
| **Overall Readiness** | **44/100** | ████░░░░░░ |


#### Construct Coverage
| Construct               | Present |
| ----------------------- | ------- |
| Coupling                | ❌ No    |
| Coherence Test          | ❌ No    |
| Integrity Layer         | ❌ No    |
| Structural Transparency | ❌ No    |
| Structural Honesty      | ❌ No    |
| Structural Containment  | ❌ No    |
| Consistency             | ❌ No    |
| Reversibility           | ❌ No    |


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: human rights / fundamental rights
- Expresses: transparency
- Expresses: explainability / interpretability
- Expresses: human oversight
- Expresses: safety
- Expresses: risk governance
- Structure: numbered sub-requirements
- Structure: mandatory obligation language (shall)
- Structure: full lifecycle scope declared
- Structure: risk stratification / proportionality


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven equivalent)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present


#### Recommended Remediation
1. Adopt LAIF canonical terminology: replace informal equivalents with the precise terms Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, and Structural Containment. Each term carries structural enforcement meaning that paraphrases do not.
2. Declare structural Coupling for each restriction: explicitly identify the specific human interest at stake and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation.
3. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test.
4. Establish the Integrity Layer as a deployment precondition: Structural Transparency, Structural Honesty, and Structural Containment must all be satisfied simultaneously before deployment may proceed. Partial satisfaction is failure — there is no partial credit.
5. Declare a non-amendable constitutional hierarchy: foundational principles at the apex (non-amendable), Provisions derived from them (cannot contradict Principles), and Operational Standards subordinate to Provisions (revisable without amending Principles).
6. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves — not only to AI operators. This is Part Seven of LAIF and is not optional.

---

### NIST AI RMF — Govern & Map Functions
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** voluntary_framework  
**Remediation Effort:** VERY HIGH


#### Scores
| Dimension             | Score      | Visual     |
| --------------------- | ---------- | ---------- |
| Structural            | 26/100     | ███░░░░░░░ |
| Terminology           | 0/100      | ░░░░░░░░░░ |
| Conceptual Proximity  | 39/100     | ████░░░░░░ |
| Auditability          | 60/100     | ██████░░░░ |
| Enforceability        | 20/100     | ██░░░░░░░░ |
| **Overall Readiness** | **30/100** | ███░░░░░░░ |


#### Construct Coverage
| Construct               | Present |
| ----------------------- | ------- |
| Coupling                | ❌ No    |
| Coherence Test          | ❌ No    |
| Integrity Layer         | ❌ No    |
| Structural Transparency | ❌ No    |
| Structural Honesty      | ❌ No    |
| Structural Containment  | ❌ No    |
| Consistency             | ❌ No    |
| Reversibility           | ❌ No    |


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: transparency
- Expresses: accountability
- Expresses: human oversight
- Expresses: safety
- Expresses: risk governance
- Structure: numbered sub-requirements
- Structure: full lifecycle scope declared
- Structure: operational mechanisms defined
- Structure: review / monitoring mechanisms
- Auditability: numbered traceable requirements


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven equivalent)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- conceptual — LAIF-like concepts insufficiently expressed
- enforceability — insufficient mandatory operational requirements


#### Recommended Remediation
1. Adopt LAIF canonical terminology: replace informal equivalents with the precise terms Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, and Structural Containment. Each term carries structural enforcement meaning that paraphrases do not.
2. Declare structural Coupling for each restriction: explicitly identify the specific human interest at stake and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation.
3. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test.
4. Establish the Integrity Layer as a deployment precondition: Structural Transparency, Structural Honesty, and Structural Containment must all be satisfied simultaneously before deployment may proceed. Partial satisfaction is failure — there is no partial credit.
5. Declare a non-amendable constitutional hierarchy: foundational principles at the apex (non-amendable), Provisions derived from them (cannot contradict Principles), and Operational Standards subordinate to Provisions (revisable without amending Principles).
6. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves — not only to AI operators. This is Part Seven of LAIF and is not optional.

---

### OECD AI Principles (2019, rev. 2024)
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** international_principles  
**Remediation Effort:** VERY HIGH


#### Scores
| Dimension             | Score      | Visual     |
| --------------------- | ---------- | ---------- |
| Structural            | 12/100     | █░░░░░░░░░ |
| Terminology           | 0/100      | ░░░░░░░░░░ |
| Conceptual Proximity  | 76/100     | ████████░░ |
| Auditability          | 0/100      | ░░░░░░░░░░ |
| Enforceability        | 20/100     | ██░░░░░░░░ |
| **Overall Readiness** | **22/100** | ██░░░░░░░░ |


#### Construct Coverage
| Construct               | Present |
| ----------------------- | ------- |
| Coupling                | ❌ No    |
| Coherence Test          | ❌ No    |
| Integrity Layer         | ❌ No    |
| Structural Transparency | ❌ No    |
| Structural Honesty      | ❌ No    |
| Structural Containment  | ❌ No    |
| Consistency             | ❌ No    |
| Reversibility           | ❌ No    |


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: human rights / fundamental rights
- Expresses: transparency
- Expresses: explainability / interpretability
- Expresses: accountability
- Expresses: human oversight
- Expresses: safety
- Expresses: contestability / redress
- Expresses: traceability / responsibility
- Expresses: fairness / labour / non-discrimination
- Structure: full lifecycle scope declared


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven equivalent)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- auditability — obligations not checkable or traceable
- enforceability — insufficient mandatory operational requirements


#### Recommended Remediation
1. Adopt LAIF canonical terminology: replace informal equivalents with the precise terms Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, and Structural Containment. Each term carries structural enforcement meaning that paraphrases do not.
2. Declare structural Coupling for each restriction: explicitly identify the specific human interest at stake and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation.
3. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test.
4. Establish the Integrity Layer as a deployment precondition: Structural Transparency, Structural Honesty, and Structural Containment must all be satisfied simultaneously before deployment may proceed. Partial satisfaction is failure — there is no partial credit.
5. Declare a non-amendable constitutional hierarchy: foundational principles at the apex (non-amendable), Provisions derived from them (cannot contradict Principles), and Operational Standards subordinate to Provisions (revisable without amending Principles).
6. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves — not only to AI operators. This is Part Seven of LAIF and is not optional.

---

### US Executive Order 14110 — §4 Safety & §7 Workers
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** executive_directive  
**Remediation Effort:** HIGH


#### Scores
| Dimension             | Score      | Visual     |
| --------------------- | ---------- | ---------- |
| Structural            | 35/100     | ████░░░░░░ |
| Terminology           | 0/100      | ░░░░░░░░░░ |
| Conceptual Proximity  | 66/100     | ███████░░░ |
| Auditability          | 60/100     | ██████░░░░ |
| Enforceability        | 80/100     | ████████░░ |
| **Overall Readiness** | **50/100** | █████░░░░░ |


#### Construct Coverage
| Construct               | Present |
| ----------------------- | ------- |
| Coupling                | ❌ No    |
| Coherence Test          | ❌ No    |
| Integrity Layer         | ❌ No    |
| Structural Transparency | ❌ No    |
| Structural Honesty      | ❌ No    |
| Structural Containment  | ❌ No    |
| Consistency             | ❌ No    |
| Reversibility           | ❌ No    |


#### Paraphrase Violations
**Guard: Coupling** — 3 violation(s)
> …engage with industry, civil society, and other stakeholders to develop guidelines, standards, methodologies, and related…
> …orrection, and redress for affected individuals.  Section 7 — Supporting Workers  Agencies shall ensure that AI deployme…


#### Strengths
- Expresses: human rights / fundamental rights
- Expresses: transparency
- Expresses: accountability
- Expresses: human oversight
- Expresses: proportionality
- Expresses: safety
- Expresses: contestability / redress
- Expresses: fairness / labour / non-discrimination
- Structure: numbered sub-requirements
- Structure: mandatory obligation language (shall)


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven equivalent)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)
- Paraphrase violation — forbidden substitution of 'Coupling' (3 instance(s)): engage with industry, civil society, and other stakeholders …; orrection, and redress for affected individuals.  Section 7 …


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- terminological (paraphrase) — forbidden substitutions detected


#### Recommended Remediation
1. Adopt LAIF canonical terminology: replace informal equivalents with the precise terms Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, and Structural Containment. Each term carries structural enforcement meaning that paraphrases do not.
2. Eliminate paraphrase violations ('Coupling' detected): these terms deploy alignment/connection/linkage language where LAIF requires the canonical term Coupling. The substitution loses the bidirectional structural enforcement requirement that Coupling carries.
3. Declare structural Coupling for each restriction: explicitly identify the specific human interest at stake and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation.
4. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test.
5. Establish the Integrity Layer as a deployment precondition: Structural Transparency, Structural Honesty, and Structural Containment must all be satisfied simultaneously before deployment may proceed. Partial satisfaction is failure — there is no partial credit.
6. Declare a non-amendable constitutional hierarchy: foundational principles at the apex (non-amendable), Provisions derived from them (cannot contradict Principles), and Operational Standards subordinate to Provisions (revisable without amending Principles).
7. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves — not only to AI operators. This is Part Seven of LAIF and is not optional.

---

## Cross-Document Findings

### Score Comparison
| Document                                 | Structural | Terminology | Conceptual | Auditability | Enforceability | Overall |
| ---------------------------------------- | ---------- | ----------- | ---------- | ------------ | -------------- | ------- |
| EU AI Act — Art. 9, 13 & 14              | 41         | 0           | 49         | 60           | 60             | 44      |
| NIST AI RMF — Govern & Map Functions     | 26         | 0           | 39         | 60           | 20             | 30      |
| OECD AI Principles (2019, rev. 2024)     | 12         | 0           | 76         | 0            | 20             | 22      |
| US Executive Order 14110 — §4 Safety & § | 35         | 0           | 66         | 60           | 80             | 50      |

**Notable patterns:**
- High conceptual proximity (≥60): OECD AI Principles (2019, rev. 2024), US Executive Order 14110 — §4 Safety & §7 Workers — these frameworks express LAIF-like intent through their own vocabulary.
- Paraphrase violations detected in: US Executive Order 14110 — §4 Safety & §7 Workers — explicit forbidden substitution of LAIF canonical terms.
- Low enforceability (<40): NIST AI RMF — Govern & Map Functions, OECD AI Principles (2019, rev. 2024) — voluntary or declaratory frameworks without binding operational mandates.

## Common Failure Modes
- **structural — constitutional hierarchy not declared** — 4/4 documents
- **terminological — no canonical LAIF terms present** — 4/4 documents
- **enforceability — insufficient mandatory operational requirements** — 2/4 documents
- **conceptual — LAIF-like concepts insufficiently expressed** — 1/4 documents
- **auditability — obligations not checkable or traceable** — 1/4 documents
- **terminological (paraphrase) — forbidden substitutions detected** — 1/4 documents

The universal failure mode is terminological: no external framework uses LAIF canonical terms. This is expected — LAIF is a new framework. However, the absence of structural Coupling is the more consequential gap: without it, governance restrictions are not structurally paired with proportionate protections, and neither can be defended as structurally required by the other.

## LAIF Deployment Implications
1. **LAIF is additive, not competitive.** Existing frameworks address the right governance dimensions. LAIF provides the structural enforcement layer they lack — canonical terms with load-bearing meaning, Coupling requirements, and the Coherence Test as a named decision instrument.

2. **Conceptual proximity enables adoption.** Documents scoring ≥60 on conceptual proximity already express the underlying values. Adoption pathway: introduce LAIF canonical terminology and add structural Coupling declarations to existing provisions.

3. **Paraphrase violations are actionable.** Where 'alignment', 'connection', or 'linkage' appear as structural governance terms, substituting 'Coupling' is the minimal change. This is a terminology fix, not a structural redesign.

4. **Auditability is a relative strength.** Binding regulations (EU AI Act) score highly on auditability — their obligations are traceable, documented, and reviewable. This auditability infrastructure is exactly what LAIF-compliant Coupling declarations would need to be enforced through.

5. **Voluntary frameworks require the most work.** NIST AI RMF and OECD Principles score low on enforceability because they use aspirational ('should') rather than mandatory ('shall') language. LAIF's Integrity Layer threshold requires mandatory language to function as a deployment precondition.

## Recommended Next Development Steps
1. **LAIF–EU AI Act mapping:** Article-by-article mapping of LAIF Provisions to EU AI Act requirements. Many EU AI Act articles can be interpreted as partially implementing LAIF provisions — formalising this mapping would accelerate EU adoption.

2. **LAIF–NIST RMF function mapping:** Map LAIF's Coherence Test questions to NIST RMF functions (Govern, Map, Measure, Manage). The RMF's operational structure could carry LAIF Coupling requirements within its existing governance architecture.

3. **Paraphrase violation remediation guide:** Produce a short guidance document for each violating framework showing specifically where 'alignment', 'connection', 'linkage' appear and what structural declaration is required to replace them with LAIF-compliant Coupling language.

4. **Extend real-world corpus:** Add sector-specific governance documents (clinical AI guidelines, financial AI regulations, autonomous vehicle frameworks) to extend the baseline beyond general AI governance.

5. **Score threshold calibration:** As more documents are assessed, calibrate the remediation effort thresholds (VERY HIGH / HIGH / MEDIUM / LOW) against actual adoption timelines to make them operationally predictive.

---
*LAIF v1.2 · Compliance Toolkit v1.1 · May 2026 · Governance Audit Series*
*Generated by `test_real_world.py` — validate.py enforcement unchanged*