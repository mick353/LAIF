# LAIF Real-World Assessment Report
**Framework version:** LAIF v1.2 · Compliance Toolkit v1.1  
**Date:** May 2026  
**Classification:** Governance Assessment — System Hardening Release  
**Validator:** validate.py (unchanged — strict formal compliance enforced)  
**Scoring:** Traceable per-signal breakdown for every dimension  

## Executive Summary
6 of 6 external AI governance frameworks assessed fail formal LAIF v1.2 compliance. Formal compliance is binary and strict — all 8 required constructs must be present; no partial credit is awarded.

Dimensional scoring reveals that the gap is terminological and structural, not conceptual. Documents achieve an average conceptual proximity score of 49/100 and an average overall readiness score of 35/100, indicating that the underlying governance intent is broadly present — expressed through different vocabulary and structural frameworks.

**Core finding:** Existing frameworks address the right governance dimensions but do not enforce them through structural Coupling, the Coherence Test, or the Integrity Layer. LAIF is measurably stricter. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present.

## Method
Each document was assessed against three complementary layers:

**Layer 1 — Formal LAIF compliance (binary):** 8 required constructs — Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles, non-amendable clause, self-application clause, Integrity Layer FINDING block, Coherence Test FINDING block. All 8 must be present. Enforced by validate.py (unchanged).

**Layer 2 — Dimensional scoring (traceable):** Five dimensions scored 0–100 with per-signal breakdown. Every score is accompanied by the signals that fired (earned points) and those that did not. This answers 'why this number?' for every dimension.

**Layer 3 — Sector analysis:** Each document assessed against a sector profile defining relevant human interests, risk indicator signals, and expected evidence artefacts. Produces sector risk alignment score (0–100) and sector-specific remediation priorities referencing LAIF source sections.

## Scoring Model
| Dimension            | Weight | LAIF Source                | Description                                                              |
| -------------------- | ------ | -------------------------- | ------------------------------------------------------------------------ |
| Structural           | 25%    | v1.2 Parts One, Two, Seven | Governance architecture: hierarchy, thresholds, review mechanisms        |
| Terminology          | 15%    | Toolkit §1                 | Canonical term presence: Coupling, Coherence Test, Integrity Layer       |
| Conceptual Proximity | 20%    | v1.2 Part One              | LAIF-like concepts without LAIF terms: rights, oversight, contestability |
| Auditability         | 20%    | Toolkit §2 PDCA            | Checkability: numbered obligations, evidence requirements, monitoring    |
| Enforceability       | 20%    | v1.2 Part Three            | Operational enforcement: mandatory language, named parties, consequences |

**Overall** = Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20

**Remediation Effort:** VERY HIGH (<35) · HIGH (35–59) · MEDIUM (≥60)

## Per-Document Scorecards

### EU AI Act — Art. 9, 13 & 14
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** binding_regulation  
**Sector:** General AI Governance  
**Remediation Effort:** HIGH


#### Scores and Signal Breakdown
**Structural: 41/100** ████░░░░░░
  + numbered sub-requirements (+8)
  + mandatory obligation language (shall) (+8)
  + full lifecycle scope declared (+6)
  + risk stratification / proportionality (+7)
  + operational mechanisms defined (+6)
  + review / monitoring mechanisms (+6)
  − threshold gate conditions (all must pass simultaneously) (0/15)
  − non-amendable constitutional hierarchy (0/18)
  − self-application clause (Part Seven) (0/12)
  − named decision instrument (Coherence Test / PDCA) (0/14)

**Terminology: 0/100** ░░░░░░░░░░
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)

**Conceptual Proximity: 49/100** █████░░░░░
  + human rights / fundamental interests (+10)
  + transparency (+8)
  + explainability / interpretability (+8)
  + human oversight (+8)
  + safety (+7)
  + risk governance (+8)
  − accountability (0/8)
  − proportionality (0/8)
  − contestability / redress (0/9)
  − reversibility / modifiability (0/8)
  − traceability / responsibility (0/10)
  − fairness / labour / non-discrimination (0/8)

**Auditability: 60/100** ██████░░░░
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)

**Enforceability: 60/100** ██████░░░░
  + mandatory language (shall) (+20)
  + risk-proportionate thresholds (+20)
  + non-discretionary operational mandates (+20)
  − named responsible parties (0/20)
  − enforcement consequences / penalties (0/20)

**Overall Readiness: 44/100** ████░░░░░░  (Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20)


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ❌ No    | v1.2 Principle 5                 |
| Reversibility           | ❌ No    | v1.2 Provision D1                |


#### Sector Context
**Sector:** General AI Governance  
**Sector risk alignment:** 60/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- freedom from arbitrary algorithmic decision-making
- transparency of AI reasoning and outputs
- effective human oversight and correction
- accountability for AI-caused harm
- access to redress and contestation mechanisms


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ high-risk classification language
- ✅ transparency requirements
- ✅ human oversight mechanisms
*Risk indicators absent:*
- ⚪ accountability assignment
- ⚪ risk-proportionate obligations
*Expected evidence artefacts present:*
- ✅ technical documentation
*Evidence gaps:*
- ❌ risk register / documentation
- ❌ audit trail
- ❌ impact assessment
- ❌ incident reporting mechanism


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: human rights / fundamental interests
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
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present


#### Sector-Aware Remediation (ordered by impact)
1. Declare structural Coupling for each governance restriction: explicitly identify the specific human interest at stake (not a category — name it with specificity, e.g. 'the patient's interest in receiving treatment decisions based on accurate clinical assessment') and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).
2. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling (does the deployment identify and protect the specific human interest at risk?), Q2 Consistency (would this governance logic produce just and workable outcomes at all comparable scales?), Q3 Reversibility (does the deployment preserve the capacity of future actors to reverse or modify its consequences?). All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test (LAIF v1.2 Part One).
3. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency (system can produce a compliant meaningful account of any material output), A.2 Structural Honesty (stated objectives correspond to implemented objectives, verified by independent review), A.3 Structural Containment (system operates within documented operational boundaries in all tested conditions including edge cases). All three must be satisfied simultaneously before deployment proceeds. Partial satisfaction is failure — there is no partial credit (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
4. Adopt LAIF canonical terminology throughout the document. Replace informal equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; 'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → 'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; 'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural Containment'. Each canonical term carries structural enforcement meaning that paraphrases do not (LAIF_Compliance_Toolkit.txt §1).
5. Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational Principles at the apex — non-amendable, define the governance standard; (ii) Provisions derived from Principles — cannot contradict Principles; (iii) Operational Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without amending Principles. This hierarchy is not optional — it prevents operational revision from eroding constitutional guarantees (LAIF v1.2 Principle 3).
6. Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).
7. Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).
8. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment must all be satisfied simultaneously. Partial satisfaction = failure (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
9. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves, not only to AI operators (LAIF v1.2 Part Seven).

---

### NIST AI RMF — Govern & Map Functions
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** voluntary_framework  
**Sector:** General AI Governance  
**Remediation Effort:** VERY HIGH


#### Scores and Signal Breakdown
**Structural: 26/100** ███░░░░░░░
  + numbered sub-requirements (+8)
  + full lifecycle scope declared (+6)
  + operational mechanisms defined (+6)
  + review / monitoring mechanisms (+6)
  − mandatory obligation language (shall) (0/8)
  − risk stratification / proportionality (0/7)
  − threshold gate conditions (all must pass simultaneously) (0/15)
  − non-amendable constitutional hierarchy (0/18)
  − self-application clause (Part Seven) (0/12)
  − named decision instrument (Coherence Test / PDCA) (0/14)

**Terminology: 0/100** ░░░░░░░░░░
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)

**Conceptual Proximity: 39/100** ████░░░░░░
  + transparency (+8)
  + accountability (+8)
  + human oversight (+8)
  + safety (+7)
  + risk governance (+8)
  − human rights / fundamental interests (0/10)
  − explainability / interpretability (0/8)
  − proportionality (0/8)
  − contestability / redress (0/9)
  − reversibility / modifiability (0/8)
  − traceability / responsibility (0/10)
  − fairness / labour / non-discrimination (0/8)

**Auditability: 60/100** ██████░░░░
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)

**Enforceability: 20/100** ██░░░░░░░░
  + enforcement consequences / penalties (+20)
  − mandatory language (shall) (0/20)
  − named responsible parties (0/20)
  − risk-proportionate thresholds (0/20)
  − non-discretionary operational mandates (0/20)

**Overall Readiness: 30/100** ███░░░░░░░  (Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20)


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ❌ No    | v1.2 Principle 5                 |
| Reversibility           | ❌ No    | v1.2 Provision D1                |


#### Sector Context
**Sector:** General AI Governance  
**Sector risk alignment:** 40/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- freedom from arbitrary algorithmic decision-making
- transparency of AI reasoning and outputs
- effective human oversight and correction
- accountability for AI-caused harm
- access to redress and contestation mechanisms


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ accountability assignment
- ✅ transparency requirements
*Risk indicators absent:*
- ⚪ high-risk classification language
- ⚪ human oversight mechanisms
- ⚪ risk-proportionate obligations
*Expected evidence artefacts present:*
- ✅ risk register / documentation
- ✅ audit trail
*Evidence gaps:*
- ❌ technical documentation
- ❌ impact assessment
- ❌ incident reporting mechanism


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
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- conceptual — LAIF-like concepts insufficiently expressed
- enforceability — insufficient mandatory operational requirements


#### Sector-Aware Remediation (ordered by impact)
1. Declare structural Coupling for each governance restriction: explicitly identify the specific human interest at stake (not a category — name it with specificity, e.g. 'the patient's interest in receiving treatment decisions based on accurate clinical assessment') and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).
2. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling (does the deployment identify and protect the specific human interest at risk?), Q2 Consistency (would this governance logic produce just and workable outcomes at all comparable scales?), Q3 Reversibility (does the deployment preserve the capacity of future actors to reverse or modify its consequences?). All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test (LAIF v1.2 Part One).
3. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency (system can produce a compliant meaningful account of any material output), A.2 Structural Honesty (stated objectives correspond to implemented objectives, verified by independent review), A.3 Structural Containment (system operates within documented operational boundaries in all tested conditions including edge cases). All three must be satisfied simultaneously before deployment proceeds. Partial satisfaction is failure — there is no partial credit (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
4. Adopt LAIF canonical terminology throughout the document. Replace informal equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; 'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → 'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; 'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural Containment'. Each canonical term carries structural enforcement meaning that paraphrases do not (LAIF_Compliance_Toolkit.txt §1).
5. Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational Principles at the apex — non-amendable, define the governance standard; (ii) Provisions derived from Principles — cannot contradict Principles; (iii) Operational Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without amending Principles. This hierarchy is not optional — it prevents operational revision from eroding constitutional guarantees (LAIF v1.2 Principle 3).
6. Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).
7. Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).
8. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment must all be satisfied simultaneously. Partial satisfaction = failure (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
9. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves, not only to AI operators (LAIF v1.2 Part Seven).

---

### OECD AI Principles (2019, rev. 2024)
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** international_principles  
**Sector:** General AI Governance  
**Remediation Effort:** VERY HIGH


#### Scores and Signal Breakdown
**Structural: 12/100** █░░░░░░░░░
  + full lifecycle scope declared (+6)
  + operational mechanisms defined (+6)
  − numbered sub-requirements (0/8)
  − mandatory obligation language (shall) (0/8)
  − risk stratification / proportionality (0/7)
  − review / monitoring mechanisms (0/6)
  − threshold gate conditions (all must pass simultaneously) (0/15)
  − non-amendable constitutional hierarchy (0/18)
  − self-application clause (Part Seven) (0/12)
  − named decision instrument (Coherence Test / PDCA) (0/14)

**Terminology: 0/100** ░░░░░░░░░░
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)

**Conceptual Proximity: 76/100** ████████░░
  + human rights / fundamental interests (+10)
  + transparency (+8)
  + explainability / interpretability (+8)
  + accountability (+8)
  + human oversight (+8)
  + safety (+7)
  + contestability / redress (+9)
  + traceability / responsibility (+10)
  + fairness / labour / non-discrimination (+8)
  − proportionality (0/8)
  − reversibility / modifiability (0/8)
  − risk governance (0/8)

**Auditability: 0/100** ░░░░░░░░░░
  − multiple mandatory obligations (shall … shall) (0/20)
  − numbered traceable requirements (0/20)
  − evidence / documentation requirements (0/20)
  − review / monitoring mechanisms (0/20)
  − specific, measurable obligations (0/20)

**Enforceability: 20/100** ██░░░░░░░░
  + named responsible parties (+20)
  − mandatory language (shall) (0/20)
  − risk-proportionate thresholds (0/20)
  − enforcement consequences / penalties (0/20)
  − non-discretionary operational mandates (0/20)

**Overall Readiness: 22/100** ██░░░░░░░░  (Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20)


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ❌ No    | v1.2 Principle 5                 |
| Reversibility           | ❌ No    | v1.2 Provision D1                |


#### Sector Context
**Sector:** General AI Governance  
**Sector risk alignment:** 60/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- freedom from arbitrary algorithmic decision-making
- transparency of AI reasoning and outputs
- effective human oversight and correction
- accountability for AI-caused harm
- access to redress and contestation mechanisms


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ accountability assignment
- ✅ transparency requirements
- ✅ human oversight mechanisms
*Risk indicators absent:*
- ⚪ high-risk classification language
- ⚪ risk-proportionate obligations
*Evidence gaps:*
- ❌ risk register / documentation
- ❌ audit trail
- ❌ technical documentation
- ❌ impact assessment
- ❌ incident reporting mechanism


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: human rights / fundamental interests
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
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- auditability — obligations not checkable or traceable
- enforceability — insufficient mandatory operational requirements


#### Sector-Aware Remediation (ordered by impact)
1. Declare structural Coupling for each governance restriction: explicitly identify the specific human interest at stake (not a category — name it with specificity, e.g. 'the patient's interest in receiving treatment decisions based on accurate clinical assessment') and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).
2. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling (does the deployment identify and protect the specific human interest at risk?), Q2 Consistency (would this governance logic produce just and workable outcomes at all comparable scales?), Q3 Reversibility (does the deployment preserve the capacity of future actors to reverse or modify its consequences?). All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test (LAIF v1.2 Part One).
3. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency (system can produce a compliant meaningful account of any material output), A.2 Structural Honesty (stated objectives correspond to implemented objectives, verified by independent review), A.3 Structural Containment (system operates within documented operational boundaries in all tested conditions including edge cases). All three must be satisfied simultaneously before deployment proceeds. Partial satisfaction is failure — there is no partial credit (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
4. Adopt LAIF canonical terminology throughout the document. Replace informal equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; 'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → 'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; 'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural Containment'. Each canonical term carries structural enforcement meaning that paraphrases do not (LAIF_Compliance_Toolkit.txt §1).
5. Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational Principles at the apex — non-amendable, define the governance standard; (ii) Provisions derived from Principles — cannot contradict Principles; (iii) Operational Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without amending Principles. This hierarchy is not optional — it prevents operational revision from eroding constitutional guarantees (LAIF v1.2 Principle 3).
6. Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).
7. Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).
8. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment must all be satisfied simultaneously. Partial satisfaction = failure (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
9. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves, not only to AI operators (LAIF v1.2 Part Seven).

---

### US Executive Order 14110 — §4 Safety & §7 Workers
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** executive_directive  
**Sector:** General AI Governance  
**Remediation Effort:** HIGH


#### Scores and Signal Breakdown
**Structural: 35/100** ████░░░░░░
  + numbered sub-requirements (+8)
  + mandatory obligation language (shall) (+8)
  + risk stratification / proportionality (+7)
  + operational mechanisms defined (+6)
  + review / monitoring mechanisms (+6)
  − full lifecycle scope declared (0/6)
  − threshold gate conditions (all must pass simultaneously) (0/15)
  − non-amendable constitutional hierarchy (0/18)
  − self-application clause (Part Seven) (0/12)
  − named decision instrument (Coherence Test / PDCA) (0/14)

**Terminology: 0/100** ░░░░░░░░░░
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)

**Conceptual Proximity: 66/100** ███████░░░
  + human rights / fundamental interests (+10)
  + transparency (+8)
  + accountability (+8)
  + human oversight (+8)
  + proportionality (+8)
  + safety (+7)
  + contestability / redress (+9)
  + fairness / labour / non-discrimination (+8)
  − explainability / interpretability (0/8)
  − reversibility / modifiability (0/8)
  − risk governance (0/8)
  − traceability / responsibility (0/10)

**Auditability: 60/100** ██████░░░░
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)

**Enforceability: 80/100** ████████░░
  + mandatory language (shall) (+20)
  + named responsible parties (+20)
  + risk-proportionate thresholds (+20)
  + non-discretionary operational mandates (+20)
  − enforcement consequences / penalties (0/20)

**Overall Readiness: 50/100** █████░░░░░  (Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20)


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ❌ No    | v1.2 Principle 5                 |
| Reversibility           | ❌ No    | v1.2 Provision D1                |


#### Sector Context
**Sector:** General AI Governance  
**Sector risk alignment:** 100/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- freedom from arbitrary algorithmic decision-making
- transparency of AI reasoning and outputs
- effective human oversight and correction
- accountability for AI-caused harm
- access to redress and contestation mechanisms


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ high-risk classification language
- ✅ accountability assignment
- ✅ transparency requirements
- ✅ human oversight mechanisms
- ✅ risk-proportionate obligations
*Expected evidence artefacts present:*
- ✅ audit trail
*Evidence gaps:*
- ❌ risk register / documentation
- ❌ technical documentation
- ❌ impact assessment
- ❌ incident reporting mechanism


#### Paraphrase Violations
**Guard: Coupling** — 3 violation(s)  
*Source: LAIF v1.2 Principle 2; validate.py context-aware guard*
> …engage with industry, civil society, and other stakeholders to develop guidelines, standards, methodologies, and related…
> …orrection, and redress for affected individuals.  Section 7 — Supporting Workers  Agencies shall ensure that AI deployme…


#### Strengths
- Expresses: human rights / fundamental interests
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
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)
- Paraphrase violation — forbidden substitution of 'Coupling' (3 instance(s)): engage with industry, civil society, and other stakeholders …; orrection, and redress for affected individuals.  Section 7 …


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- terminological (paraphrase) — forbidden substitutions detected


#### Sector-Aware Remediation (ordered by impact)
1. Paraphrase rewrite required — 'Coupling' guard triggered. Detected: "engage with industry, civil society, and other stakeholders to develop guidelines, standards, methodologies, and related". Replace the forbidden term with the canonical LAIF term 'Coupling'. The substitution is not merely terminological: 'Coupling' carries a structural enforcement requirement that informal equivalents do not. Rewrite pattern: '[alignment/connection/linkage] between [X] and [Y]' → 'Coupling between [X] and [the specific human interest Y protects], with a protection of equivalent normative force' (LAIF v1.2 Principle 2; Toolkit §2 B.1).
2. Paraphrase rewrite required — 'Coupling' guard triggered. Detected: "orrection, and redress for affected individuals.  Section 7 — Supporting Workers  Agencies shall ensure that AI deployme". Replace the forbidden term with the canonical LAIF term 'Coupling'. The substitution is not merely terminological: 'Coupling' carries a structural enforcement requirement that informal equivalents do not. Rewrite pattern: '[alignment/connection/linkage] between [X] and [Y]' → 'Coupling between [X] and [the specific human interest Y protects], with a protection of equivalent normative force' (LAIF v1.2 Principle 2; Toolkit §2 B.1).
3. Declare structural Coupling for each governance restriction: explicitly identify the specific human interest at stake (not a category — name it with specificity, e.g. 'the patient's interest in receiving treatment decisions based on accurate clinical assessment') and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).
4. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling (does the deployment identify and protect the specific human interest at risk?), Q2 Consistency (would this governance logic produce just and workable outcomes at all comparable scales?), Q3 Reversibility (does the deployment preserve the capacity of future actors to reverse or modify its consequences?). All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test (LAIF v1.2 Part One).
5. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency (system can produce a compliant meaningful account of any material output), A.2 Structural Honesty (stated objectives correspond to implemented objectives, verified by independent review), A.3 Structural Containment (system operates within documented operational boundaries in all tested conditions including edge cases). All three must be satisfied simultaneously before deployment proceeds. Partial satisfaction is failure — there is no partial credit (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
6. Adopt LAIF canonical terminology throughout the document. Replace informal equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; 'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → 'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; 'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural Containment'. Each canonical term carries structural enforcement meaning that paraphrases do not (LAIF_Compliance_Toolkit.txt §1).
7. Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational Principles at the apex — non-amendable, define the governance standard; (ii) Provisions derived from Principles — cannot contradict Principles; (iii) Operational Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without amending Principles. This hierarchy is not optional — it prevents operational revision from eroding constitutional guarantees (LAIF v1.2 Principle 3).
8. Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).
9. Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).
10. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment must all be satisfied simultaneously. Partial satisfaction = failure (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
11. Add a self-application clause: specify that the framework applies to regulatory bodies and governance actors themselves, not only to AI operators (LAIF v1.2 Part Seven).

---

### NHS England — AI in Clinical Decision Support (Policy Framework)
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** sector_policy  
**Sector:** Clinical AI Deployment  
**Remediation Effort:** VERY HIGH


#### Scores and Signal Breakdown
**Structural: 35/100** ████░░░░░░
  + mandatory obligation language (shall) (+8)
  + full lifecycle scope declared (+6)
  + review / monitoring mechanisms (+6)
  + threshold gate conditions (all must pass simultaneously) (+15)
  − numbered sub-requirements (0/8)
  − risk stratification / proportionality (0/7)
  − operational mechanisms defined (0/6)
  − non-amendable constitutional hierarchy (0/18)
  − self-application clause (Part Seven) (0/12)
  − named decision instrument (Coherence Test / PDCA) (0/14)

**Terminology: 0/100** ░░░░░░░░░░
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)

**Conceptual Proximity: 23/100** ██░░░░░░░░
  + transparency (+8)
  + human oversight (+8)
  + safety (+7)
  − human rights / fundamental interests (0/10)
  − explainability / interpretability (0/8)
  − accountability (0/8)
  − proportionality (0/8)
  − contestability / redress (0/9)
  − reversibility / modifiability (0/8)
  − risk governance (0/8)
  − traceability / responsibility (0/10)
  − fairness / labour / non-discrimination (0/8)

**Auditability: 40/100** ████░░░░░░
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − numbered traceable requirements (0/20)
  − specific, measurable obligations (0/20)

**Enforceability: 40/100** ████░░░░░░
  + mandatory language (shall) (+20)
  + non-discretionary operational mandates (+20)
  − named responsible parties (0/20)
  − risk-proportionate thresholds (0/20)
  − enforcement consequences / penalties (0/20)

**Overall Readiness: 29/100** ███░░░░░░░  (Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20)


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ❌ No    | v1.2 Principle 5                 |
| Reversibility           | ❌ No    | v1.2 Provision D1                |


#### Sector Context
**Sector:** Clinical AI Deployment  
**Sector risk alignment:** 80/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- physical safety and bodily integrity of patients
- informed consent for AI-assisted clinical decisions
- clinical accuracy and reliability of AI outputs
- patient right to human clinician review of AI recommendations
- confidentiality of health data processed by the AI system
- access to effective redress for clinical harm caused by AI error


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ clinical decision output
- ✅ patient safety signal
- ✅ diagnostic / treatment language
- ✅ named clinical actor
*Risk indicators absent:*
- ⚪ medical device classification
*Expected evidence artefacts present:*
- ✅ clinical validation evidence
- ✅ adverse event / incident reporting
- ✅ post-deployment performance monitoring
*Evidence gaps:*
- ❌ informed consent documentation
- ❌ clinical audit / governance


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: transparency
- Expresses: human oversight
- Expresses: safety
- Structure: mandatory obligation language (shall)
- Structure: full lifecycle scope declared
- Structure: review / monitoring mechanisms
- Auditability: evidence / documentation requirements
- Auditability: review / monitoring mechanisms
- Enforceability: mandatory language (shall)
- Enforceability: non-discretionary operational mandates


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- conceptual — LAIF-like concepts insufficiently expressed


#### Sector-Aware Remediation (ordered by impact)
1. Declare structural Coupling for each governance restriction: explicitly identify the specific human interest at stake (not a category — name it with specificity, e.g. 'the patient's interest in receiving treatment decisions based on accurate clinical assessment') and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).
2. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling (does the deployment identify and protect the specific human interest at risk?), Q2 Consistency (would this governance logic produce just and workable outcomes at all comparable scales?), Q3 Reversibility (does the deployment preserve the capacity of future actors to reverse or modify its consequences?). All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test (LAIF v1.2 Part One).
3. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency (system can produce a compliant meaningful account of any material output), A.2 Structural Honesty (stated objectives correspond to implemented objectives, verified by independent review), A.3 Structural Containment (system operates within documented operational boundaries in all tested conditions including edge cases). All three must be satisfied simultaneously before deployment proceeds. Partial satisfaction is failure — there is no partial credit (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
4. Adopt LAIF canonical terminology throughout the document. Replace informal equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; 'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → 'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; 'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural Containment'. Each canonical term carries structural enforcement meaning that paraphrases do not (LAIF_Compliance_Toolkit.txt §1).
5. Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational Principles at the apex — non-amendable, define the governance standard; (ii) Provisions derived from Principles — cannot contradict Principles; (iii) Operational Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without amending Principles. This hierarchy is not optional — it prevents operational revision from eroding constitutional guarantees (LAIF v1.2 Principle 3).
6. Declare Coupling between each clinical restriction and the specific patient interest it protects. Rewrite: 'AI alert suppression' → 'Coupling between alert suppression rules and the patient's interest in receiving clinically accurate recommendations' (Toolkit §2 B.1).
7. Apply Q3 Reversibility: clinician override must always be preserved — AI recommendations must not displace clinical judgement irreversibly. Rewrite: 'AI system supports clinical decisions' → 'AI system provides recommendations subject to clinician override at every decision point, with override logged and reversible' (LAIF v1.2 Provision D1).
8. Establish Structural Containment: document approved indications, patient populations, and operational boundaries for clinical AI. Add: 'System operates within documented clinical scope; out-of-scope queries surfaced to clinician, not resolved autonomously' (Toolkit §1.5).
9. Require informed consent documentation for AI-assisted decisions that materially affect patient treatment — 'materially affects interests' includes clinical and diagnostic recommendations (Toolkit §1.2).

---

### TUC/CIPD — Framework for Fair AI in Employment Decisions
**Formal LAIF Compliance:** ❌ FAIL  
**Source type:** sector_policy  
**Sector:** Employment / Workforce AI  
**Remediation Effort:** HIGH


#### Scores and Signal Breakdown
**Structural: 28/100** ███░░░░░░░
  + numbered sub-requirements (+8)
  + mandatory obligation language (shall) (+8)
  + operational mechanisms defined (+6)
  + review / monitoring mechanisms (+6)
  − full lifecycle scope declared (0/6)
  − risk stratification / proportionality (0/7)
  − threshold gate conditions (all must pass simultaneously) (0/15)
  − non-amendable constitutional hierarchy (0/18)
  − self-application clause (Part Seven) (0/12)
  − named decision instrument (Coherence Test / PDCA) (0/14)

**Terminology: 0/100** ░░░░░░░░░░
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)

**Conceptual Proximity: 41/100** ████░░░░░░
  + transparency (+8)
  + explainability / interpretability (+8)
  + accountability (+8)
  + contestability / redress (+9)
  + fairness / labour / non-discrimination (+8)
  − human rights / fundamental interests (0/10)
  − human oversight (0/8)
  − proportionality (0/8)
  − safety (0/7)
  − reversibility / modifiability (0/8)
  − risk governance (0/8)
  − traceability / responsibility (0/10)

**Auditability: 60/100** ██████░░░░
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)

**Enforceability: 40/100** ████░░░░░░
  + mandatory language (shall) (+20)
  + non-discretionary operational mandates (+20)
  − named responsible parties (0/20)
  − risk-proportionate thresholds (0/20)
  − enforcement consequences / penalties (0/20)

**Overall Readiness: 35/100** ████░░░░░░  (Structural×0.25 + Terminology×0.15 + Conceptual×0.20 + Auditability×0.20 + Enforceability×0.20)


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ❌ No    | v1.2 Principle 5                 |
| Reversibility           | ❌ No    | v1.2 Provision D1                |


#### Sector Context
**Sector:** Employment / Workforce AI  
**Sector risk alignment:** 80/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- freedom from automated discrimination in hiring, promotion, or dismissal
- right to explanation of AI-driven employment decisions
- preservation of labour rights when AI monitors or manages workers
- right to human review of algorithmic performance assessment
- protection of worker data processed by AI systems
- collective bargaining rights in AI-governed workplaces


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ hiring / recruitment context
- ✅ performance management
- ✅ dismissal / termination
- ✅ pay / compensation signal
*Risk indicators absent:*
- ⚪ worker surveillance
*Expected evidence artefacts present:*
- ✅ bias / fairness audit
- ✅ explanation of AI decisions
- ✅ worker consultation / notice
- ✅ anti-discrimination mechanism
*Evidence gaps:*
- ❌ equality impact assessment


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: transparency
- Expresses: explainability / interpretability
- Expresses: accountability
- Expresses: contestability / redress
- Expresses: fairness / labour / non-discrimination
- Structure: numbered sub-requirements
- Structure: mandatory obligation language (shall)
- Structure: operational mechanisms defined
- Structure: review / monitoring mechanisms
- Auditability: numbered traceable requirements


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present


#### Sector-Aware Remediation (ordered by impact)
1. Declare structural Coupling for each governance restriction: explicitly identify the specific human interest at stake (not a category — name it with specificity, e.g. 'the patient's interest in receiving treatment decisions based on accurate clinical assessment') and pair it with a protection of equivalent normative force. The restriction and its paired protection must not be capable of being weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).
2. Apply the Coherence Test before any governance provision is issued or deployment authorised: Q1 Coupling (does the deployment identify and protect the specific human interest at risk?), Q2 Consistency (would this governance logic produce just and workable outcomes at all comparable scales?), Q3 Reversibility (does the deployment preserve the capacity of future actors to reverse or modify its consequences?). All three must be answered affirmatively. Failure at Q1 constitutes automatic failure of the full test (LAIF v1.2 Part One).
3. Establish the Integrity Layer as a deployment precondition: A.1 Structural Transparency (system can produce a compliant meaningful account of any material output), A.2 Structural Honesty (stated objectives correspond to implemented objectives, verified by independent review), A.3 Structural Containment (system operates within documented operational boundaries in all tested conditions including edge cases). All three must be satisfied simultaneously before deployment proceeds. Partial satisfaction is failure — there is no partial credit (LAIF v1.2 Part Two; Toolkit §1.3–§1.5).
4. Adopt LAIF canonical terminology throughout the document. Replace informal equivalents with precise terms: 'alignment/connection/linkage' → 'Coupling'; 'integrity conditions/requirements' → 'Integrity Layer'; 'coherence check' → 'Coherence Test'; 'transparency requirements' → 'Structural Transparency'; 'honesty requirements' → 'Structural Honesty'; 'boundary controls' → 'Structural Containment'. Each canonical term carries structural enforcement meaning that paraphrases do not (LAIF_Compliance_Toolkit.txt §1).
5. Declare a non-amendable constitutional hierarchy with three tiers: (i) Foundational Principles at the apex — non-amendable, define the governance standard; (ii) Provisions derived from Principles — cannot contradict Principles; (iii) Operational Standards (Toolkit-level definitions) — subordinate to Provisions, revisable without amending Principles. This hierarchy is not optional — it prevents operational revision from eroding constitutional guarantees (LAIF v1.2 Principle 3).
6. Declare Coupling between each employment AI restriction and the specific worker interest it protects. Rewrite: 'alignment between obligations imposed on workers and the protections those obligations are intended to serve' → 'Coupling between obligations imposed on workers and the protections afforded to their employment status and income' (Toolkit §2 B.1; LAIF v1.2 Principle 2).
7. Apply Q2 Consistency: governance logic must produce just outcomes across all scales — from individual worker to collective bargaining unit. Rewrite: 'AI performance assessment applies to all employees' → 'AI performance assessment applies consistently across all roles, scales, and worker categories, with equivalent review rights at each scale' (LAIF v1.2 Principle 5).
8. Apply Q3 Reversibility: algorithmic dismissal or demotion without appeal pathway fails Provision D1. Rewrite: 'AI-driven performance scoring determines employment decisions' → 'AI-driven performance scoring informs employment decisions subject to mandatory human review, with outcomes reversible on appeal' (LAIF v1.2 Provision D1).
9. Implement bias auditing as a pre-deployment evidence artefact under Integrity Layer A.1 — Structural Transparency requires documented error characteristics including discriminatory output patterns (Toolkit §1.3).

---

## Cross-Document Findings

### Score Comparison
| Document                               | Str | Ter | Con | Aud | Enf | OVR | Sector Alignment |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------- |
| EU AI Act — Art. 9, 13 & 14            | 41  | 0   | 49  | 60  | 60  | 44  | 60%              |
| NIST AI RMF — Govern & Map Functions   | 26  | 0   | 39  | 60  | 20  | 30  | 40%              |
| OECD AI Principles (2019, rev. 2024)   | 12  | 0   | 76  | 0   | 20  | 22  | 60%              |
| US Executive Order 14110 — §4 Safety & | 35  | 0   | 66  | 60  | 80  | 50  | 100%             |
| NHS England — AI in Clinical Decision  | 35  | 0   | 23  | 40  | 40  | 29  | 80%              |
| TUC/CIPD — Framework for Fair AI in Em | 28  | 0   | 41  | 60  | 40  | 35  | 80%              |

- High conceptual proximity (≥60): OECD AI Principles (2019, rev. 2024), US Executive Order 14110 — §4 Safety & §7 Workers — LAIF-like intent expressed through own vocabulary.
- Paraphrase violations: US Executive Order 14110 — §4 Safety & §7 Workers — forbidden substitution of LAIF canonical terms.
- Low enforceability (<40): NIST AI RMF — Govern & Map Functions, OECD AI Principles (2019, rev. 2024) — voluntary/declaratory frameworks without binding mandates.

## Common Failure Modes
- **structural — constitutional hierarchy not declared** — 6/6 documents
- **terminological — no canonical LAIF terms present** — 6/6 documents
- **conceptual — LAIF-like concepts insufficiently expressed** — 2/6 documents
- **enforceability — insufficient mandatory operational requirements** — 2/6 documents
- **auditability — obligations not checkable or traceable** — 1/6 documents
- **terminological (paraphrase) — forbidden substitutions detected** — 1/6 documents

The universal failure mode is terminological: no external framework uses LAIF canonical terms. However, the absence of structural Coupling is the more consequential gap — without it, restrictions are not structurally paired with proportionate protections, and neither can be defended as structurally required by the other (LAIF v1.2 Principle 2).

## LAIF Deployment Implications
1. **LAIF is additive, not competitive.** Existing frameworks address the right governance dimensions. LAIF provides the structural enforcement layer they lack — canonical terms with load-bearing meaning, Coupling requirements, and the Coherence Test as a named decision instrument.

2. **Conceptual proximity enables adoption.** Documents scoring ≥60 on conceptual proximity already express the underlying values. Adoption pathway: introduce LAIF canonical terminology and add structural Coupling declarations to existing provisions.

3. **Paraphrase violations are actionable.** Where 'alignment', 'connection', or 'linkage' appear as structural governance terms, the minimal fix is a rewrite substituting 'Coupling' and adding the paired protection — not a full structural redesign.

4. **Sector risk alignment measures deployment readiness.** A document with high conceptual proximity but low sector risk alignment may not address the specific materially-affected interests in the target deployment context.

5. **Scoring traceability enables targeted remediation.** Per-signal breakdowns show precisely which structural elements are missing, enabling prioritised fixes rather than wholesale document rewrites.

## Recommended Next Development Steps
1. **Article-level LAIF–EU AI Act mapping:** Map LAIF Provisions to EU AI Act articles to formalise the adoption pathway for the EU regulatory context.

2. **LAIF–NIST RMF function mapping:** Map Coherence Test questions to NIST RMF functions (Govern, Map, Measure, Manage) to enable LAIF adoption within existing US governance infrastructure.

3. **Sector-specific PDCA templates:** Produce PDCA-Full templates pre-populated with sector-appropriate Coupling declarations, evidence artefact checklists, and Coherence Test documentation guidance.

4. **Score threshold calibration:** As more documents are assessed, calibrate remediation effort thresholds against actual adoption timelines.

---
*LAIF v1.2 · Compliance Toolkit v1.1 · May 2026 · Governance Audit Series*
*Generated by `test_real_world.py` — validate.py enforcement unchanged*