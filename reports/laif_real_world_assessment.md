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

**Layer 4 — Structural depth (adversarial hardening):** Three diagnostic checks run against every document regardless of formal compliance verdict:
- **Coupling quality** (STRUCTURAL / SHALLOW / NEGATED / ABSENT): detects hollow or negated Coupling declarations (LAIF v1.2 Principle 2)
- **Contradiction detection**: detects co-presence of claimed Integrity Layer properties and language that contradicts them (LAIF v1.2 A.2 Structural Honesty)
- **Sector gaming risk** (LOW / MEDIUM / HIGH): detects high sector keyword density without substantive governance content (LAIF v1.2 Q2 Consistency)

**Strong compliance verdict:** STRONG PASS requires formal PASS + STRUCTURAL Coupling + no contradictions. A formal PASS with shallow Coupling = WEAK PASS, not a strong compliance claim.

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

#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: Coupling, Integrity Layer, Coherence Test and 5 others. Overall readiness score: 44/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Root cause:** Primary gap: Coupling is absent — no restriction paired with a named human interest. Most common LAIF failure mode (Q1 of Coherence Test).

**Key risks:**
- Coupling quality is ABSENT: no governance restriction is structurally paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Moderate conceptual proximity (49/100): key LAIF-aligned governance concepts are present, indicating partial substantive alignment with LAIF's foundational principles.
- Strong sector risk alignment (60/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | WEAK    |
| Structural contradictions       | NONE    |
| Sector gaming risk              | LOW     |
| Final verdict                   | FAIL    |

**Source type:** binding_regulation  
**Sector:** General AI Governance  
**Coupling Quality:** ABSENT — Coupling not present in document  
**Remediation Effort:** HIGH


#### Scores and Signal Breakdown
**Structural: 41/100** ████░░░░░░
  *Weak structural coverage (41/100): only 6 of 10 signals matched. Principal gaps: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven).*
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
  *Weighting: 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).*

**Terminology: 0/100** ░░░░░░░░░░
  *No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.*
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)
  *Weighting: 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).*

**Conceptual Proximity: 49/100** █████░░░░░
  *Weak conceptual coverage (49/100): only 6 of 12 signals matched. Principal gaps: accountability, proportionality, contestability / redress.*
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
  *Weighting: 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).*

**Auditability: 60/100** ██████░░░░
  *Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.*
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)
  *Weighting: 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).*

**Enforceability: 60/100** ██████░░░░
  *Partial enforceability coverage (60/100): 3 of 5 signals matched. Key gaps: named responsible parties, enforcement consequences / penalties.*
  + mandatory language (shall) (+20)
  + risk-proportionate thresholds (+20)
  + non-discretionary operational mandates (+20)
  − named responsible parties (0/20)
  − enforcement consequences / penalties (0/20)
  *Weighting: 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).*

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


#### Structured Findings
**🔴 [HIGH] Coupling absent — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.



#### Remediation Plan (ordered by impact)
**1. Problem:** Structural Coupling not declared — the term 'Coupling' is absent.
   **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   **Concrete fix:** For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).

**2. Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).

**3. Problem:** Integrity Layer not declared as a deployment precondition.
   **Why it matters:** A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment — all three must be satisfied simultaneously before deployment may proceed. Partial satisfaction = failure. Without this gate, there is no precondition preventing premature deployment (LAIF v1.2 Part Two).
   **Concrete fix:** Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).

**4. Problem:** Constitutional hierarchy not declared (structural score 41/100). Missing: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven).
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**5. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### NIST AI RMF — Govern & Map Functions

#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: Coupling, Integrity Layer, Coherence Test and 5 others. Overall readiness score: 30/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Root cause:** Primary gap: Coupling is absent — no restriction paired with a named human interest. Most common LAIF failure mode (Q1 of Coherence Test).

**Key risks:**
- Coupling quality is ABSENT: no governance restriction is structurally paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.
- Low enforceability (20/100): mandatory language ('shall'), named responsible parties, and enforcement consequences are largely absent. Governance provisions are aspirational rather than operationally binding.

**Key strengths:**
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | WEAK    |
| Structural contradictions       | NONE    |
| Sector gaming risk              | LOW     |
| Final verdict                   | FAIL    |

**Source type:** voluntary_framework  
**Sector:** General AI Governance  
**Coupling Quality:** ABSENT — Coupling not present in document  
**Remediation Effort:** VERY HIGH


#### Scores and Signal Breakdown
**Structural: 26/100** ███░░░░░░░
  *Weak structural coverage (26/100): only 4 of 10 signals matched. Principal gaps: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).*
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
  *Weighting: 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).*

**Terminology: 0/100** ░░░░░░░░░░
  *No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.*
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)
  *Weighting: 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).*

**Conceptual Proximity: 39/100** ████░░░░░░
  *Weak conceptual coverage (39/100): only 5 of 12 signals matched. Principal gaps: human rights / fundamental interests, explainability / interpretability, proportionality.*
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
  *Weighting: 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).*

**Auditability: 60/100** ██████░░░░
  *Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.*
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)
  *Weighting: 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).*

**Enforceability: 20/100** ██░░░░░░░░
  *Weak enforceability coverage (20/100): only 1 of 5 signals matched. Principal gaps: mandatory language (shall), named responsible parties, risk-proportionate thresholds.*
  + enforcement consequences / penalties (+20)
  − mandatory language (shall) (0/20)
  − named responsible parties (0/20)
  − risk-proportionate thresholds (0/20)
  − non-discretionary operational mandates (0/20)
  *Weighting: 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).*

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


#### Structured Findings
**🔴 [HIGH] Coupling absent — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (26/100)**
- *Evidence:* Score 26/100. Key missed signals: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
- *Impact:* A structural governance architecture score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 30/100.
- *Recommended action:* Target the missed signals for this dimension: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). See weight_rationale in score_trace for prioritisation context.

**🟡 [MEDIUM] Low Enforceability score (20/100)**
- *Evidence:* Score 20/100. Key missed signals: mandatory language (shall), named responsible parties, risk-proportionate thresholds.
- *Impact:* A enforceability score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 30/100.
- *Recommended action:* Target the missed signals for this dimension: mandatory language (shall), named responsible parties, risk-proportionate thresholds. See weight_rationale in score_trace for prioritisation context.



#### Remediation Plan (ordered by impact)
**1. Problem:** Structural Coupling not declared — the term 'Coupling' is absent.
   **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   **Concrete fix:** For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).

**2. Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).

**3. Problem:** Integrity Layer not declared as a deployment precondition.
   **Why it matters:** A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment — all three must be satisfied simultaneously before deployment may proceed. Partial satisfaction = failure. Without this gate, there is no precondition preventing premature deployment (LAIF v1.2 Part Two).
   **Concrete fix:** Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).

**4. Problem:** Constitutional hierarchy not declared (structural score 26/100). Missing: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**5. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### OECD AI Principles (2019, rev. 2024)

#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: Coupling, Integrity Layer, Coherence Test and 5 others. Overall readiness score: 22/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Root cause:** Primary gap: Coupling is absent — no restriction paired with a named human interest. Most common LAIF failure mode (Q1 of Coherence Test).

**Key risks:**
- Coupling quality is ABSENT: no governance restriction is structurally paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.
- Low enforceability (20/100): mandatory language ('shall'), named responsible parties, and enforcement consequences are largely absent. Governance provisions are aspirational rather than operationally binding.

**Key strengths:**
- High conceptual proximity (76/100): accountability, oversight, transparency, and contestability are expressed through the document's own vocabulary. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present.
- Strong sector risk alignment (60/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | WEAK    |
| Structural contradictions       | NONE    |
| Sector gaming risk              | LOW     |
| Final verdict                   | FAIL    |

**Source type:** international_principles  
**Sector:** General AI Governance  
**Coupling Quality:** ABSENT — Coupling not present in document  
**Remediation Effort:** VERY HIGH


#### Scores and Signal Breakdown
**Structural: 12/100** █░░░░░░░░░
  *Weak structural coverage (12/100): only 2 of 10 signals matched. Principal gaps: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.*
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
  *Weighting: 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).*

**Terminology: 0/100** ░░░░░░░░░░
  *No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.*
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)
  *Weighting: 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).*

**Conceptual Proximity: 76/100** ████████░░
  *Partial conceptual coverage (76/100): 9 of 12 signals matched. Key gaps: proportionality, reversibility / modifiability.*
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
  *Weighting: 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).*

**Auditability: 0/100** ░░░░░░░░░░
  *No auditability signals present — none of the 5 expected signals matched. This dimension is absent from the document.*
  − multiple mandatory obligations (shall … shall) (0/20)
  − numbered traceable requirements (0/20)
  − evidence / documentation requirements (0/20)
  − review / monitoring mechanisms (0/20)
  − specific, measurable obligations (0/20)
  *Weighting: 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).*

**Enforceability: 20/100** ██░░░░░░░░
  *Weak enforceability coverage (20/100): only 1 of 5 signals matched. Principal gaps: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.*
  + named responsible parties (+20)
  − mandatory language (shall) (0/20)
  − risk-proportionate thresholds (0/20)
  − enforcement consequences / penalties (0/20)
  − non-discretionary operational mandates (0/20)
  *Weighting: 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).*

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


#### Structured Findings
**🔴 [HIGH] Coupling absent — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (12/100)**
- *Evidence:* Score 12/100. Key missed signals: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.
- *Impact:* A structural governance architecture score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 22/100.
- *Recommended action:* Target the missed signals for this dimension: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality. See weight_rationale in score_trace for prioritisation context.

**🔴 [HIGH] Low Auditability score (0/100)**
- *Evidence:* Score 0/100. Key missed signals: multiple mandatory obligations (shall … shall), numbered traceable requirements, evidence / documentation requirements.
- *Impact:* A auditability score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 22/100.
- *Recommended action:* Target the missed signals for this dimension: multiple mandatory obligations (shall … shall), numbered traceable requirements, evidence / documentation requirements. See weight_rationale in score_trace for prioritisation context.

**🟡 [MEDIUM] Low Enforceability score (20/100)**
- *Evidence:* Score 20/100. Key missed signals: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.
- *Impact:* A enforceability score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 22/100.
- *Recommended action:* Target the missed signals for this dimension: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties. See weight_rationale in score_trace for prioritisation context.



#### Remediation Plan (ordered by impact)
**1. Problem:** Structural Coupling not declared — the term 'Coupling' is absent.
   **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   **Concrete fix:** For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).

**2. Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).

**3. Problem:** Integrity Layer not declared as a deployment precondition.
   **Why it matters:** A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment — all three must be satisfied simultaneously before deployment may proceed. Partial satisfaction = failure. Without this gate, there is no precondition preventing premature deployment (LAIF v1.2 Part Two).
   **Concrete fix:** Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).

**4. Problem:** Constitutional hierarchy not declared (structural score 12/100). Missing: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**5. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### US Executive Order 14110 — §4 Safety & §7 Workers

#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: Coupling, Integrity Layer, Coherence Test and 5 others. Overall readiness score: 50/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Root cause:** Primary gap: Coupling is absent — no restriction paired with a named human interest. Most common LAIF failure mode (Q1 of Coherence Test).

**Key risks:**
- Coupling quality is ABSENT: no governance restriction is structurally paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- High conceptual proximity (66/100): accountability, oversight, transparency, and contestability are expressed through the document's own vocabulary. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present.
- Strong sector risk alignment (100/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | WEAK    |
| Structural contradictions       | NONE    |
| Sector gaming risk              | LOW     |
| Final verdict                   | FAIL    |

**Source type:** executive_directive  
**Sector:** General AI Governance  
**Coupling Quality:** ABSENT — Coupling not present in document  
**Remediation Effort:** HIGH


#### Scores and Signal Breakdown
**Structural: 35/100** ████░░░░░░
  *Weak structural coverage (35/100): only 5 of 10 signals matched. Principal gaps: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy.*
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
  *Weighting: 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).*

**Terminology: 0/100** ░░░░░░░░░░
  *No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.*
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)
  *Weighting: 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).*

**Conceptual Proximity: 66/100** ███████░░░
  *Partial conceptual coverage (66/100): 8 of 12 signals matched. Key gaps: explainability / interpretability, reversibility / modifiability.*
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
  *Weighting: 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).*

**Auditability: 60/100** ██████░░░░
  *Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.*
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)
  *Weighting: 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).*

**Enforceability: 80/100** ████████░░
  *Strong enforceability coverage (80/100): 4 of 5 signals matched. Strongest contributors: mandatory language (shall), named responsible parties.*
  + mandatory language (shall) (+20)
  + named responsible parties (+20)
  + risk-proportionate thresholds (+20)
  + non-discretionary operational mandates (+20)
  − enforcement consequences / penalties (0/20)
  *Weighting: 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).*

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


#### Structured Findings
**🔴 [HIGH] Coupling absent — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🟡 [MEDIUM] Paraphrase violation: forbidden substitution of 'Coupling'**
- *Evidence:* 3 instance(s). Example: «engage with industry, civil society, and other stakeholders to develop guidelines, standards, method»
- *Impact:* Informal substitutes for 'Coupling' do not carry its enforcement weight. 'Coupling' is not equivalent to 'alignment' — the canonical term requires a named human interest, paired protection, and equivalent normative force that informal equivalents lack (Toolkit §1).
- *Recommended action:* Replace each forbidden term with 'Coupling' and add the structural declaration the canonical term requires (Toolkit §1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (35/100)**
- *Evidence:* Score 35/100. Key missed signals: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy.
- *Impact:* A structural governance architecture score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 50/100.
- *Recommended action:* Target the missed signals for this dimension: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy. See weight_rationale in score_trace for prioritisation context.



#### Remediation Plan (ordered by impact)
**1. Problem:** Forbidden paraphrase of 'Coupling' detected: «engage with industry, civil society, and other stakeholders to develop guidelines, standards, method»
   **Why it matters:** 'Coupling' is a structurally load-bearing canonical term. Informal substitutes do not carry the enforcement obligation the term requires. Using 'alignment' or 'connection' where 'Coupling' is required leaves each restriction without a mandatory paired protection (Toolkit §1).
   **Concrete fix:** Replace the forbidden term with 'Coupling' at every occurrence. For 'Coupling' specifically, also add: the named human interest, the paired restriction, and a statement of equivalent normative force on both sides (Toolkit §2 B.1; LAIF v1.2 Principle 2).

**2. Problem:** Structural Coupling not declared — the term 'Coupling' is absent.
   **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   **Concrete fix:** For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).

**3. Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).

**4. Problem:** Integrity Layer not declared as a deployment precondition.
   **Why it matters:** A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment — all three must be satisfied simultaneously before deployment may proceed. Partial satisfaction = failure. Without this gate, there is no precondition preventing premature deployment (LAIF v1.2 Part Two).
   **Concrete fix:** Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).

**5. Problem:** Constitutional hierarchy not declared (structural score 35/100). Missing: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy.
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**6. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**7. Problem:** Sector-specific governance gap (General AI Governance).
   **Why it matters:** The General AI Governance deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### NHS England — AI in Clinical Decision Support (Policy Framework)

#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: Coupling, Integrity Layer, Coherence Test and 5 others. Overall readiness score: 29/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Root cause:** Primary gap: Coupling is absent — no restriction paired with a named human interest. Most common LAIF failure mode (Q1 of Coherence Test).

**Key risks:**
- Coupling quality is ABSENT: no governance restriction is structurally paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- High sector gaming risk: sector keyword density is elevated while substantive governance content is low (overall 29/100). This pattern would not produce just outcomes at the individual-decision scale — failing Q2 Consistency. (LAIF v1.2 Principle 5)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Strong sector risk alignment (80/100): the document addresses the materially relevant human interests for the Clinical AI Deployment deployment context.


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | HOLLOW  |
| Structural contradictions       | NONE    |
| Sector gaming risk              | HIGH    |
| Final verdict                   | FAIL    |

**Source type:** sector_policy  
**Sector:** Clinical AI Deployment  
**Coupling Quality:** ABSENT — Coupling not present in document  
**Remediation Effort:** VERY HIGH


#### Scores and Signal Breakdown
**Structural: 35/100** ████░░░░░░
  *Weak structural coverage (35/100): only 4 of 10 signals matched. Principal gaps: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined.*
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
  *Weighting: 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).*

**Terminology: 0/100** ░░░░░░░░░░
  *No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.*
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)
  *Weighting: 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).*

**Conceptual Proximity: 23/100** ██░░░░░░░░
  *Weak conceptual coverage (23/100): only 3 of 12 signals matched. Principal gaps: human rights / fundamental interests, explainability / interpretability, accountability.*
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
  *Weighting: 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).*

**Auditability: 40/100** ████░░░░░░
  *Weak auditability coverage (40/100): only 2 of 5 signals matched. Principal gaps: multiple mandatory obligations (shall … shall), numbered traceable requirements, specific, measurable obligations.*
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − numbered traceable requirements (0/20)
  − specific, measurable obligations (0/20)
  *Weighting: 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).*

**Enforceability: 40/100** ████░░░░░░
  *Weak enforceability coverage (40/100): only 2 of 5 signals matched. Principal gaps: named responsible parties, risk-proportionate thresholds, enforcement consequences / penalties.*
  + mandatory language (shall) (+20)
  + non-discretionary operational mandates (+20)
  − named responsible parties (0/20)
  − risk-proportionate thresholds (0/20)
  − enforcement consequences / penalties (0/20)
  *Weighting: 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).*

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
- Sector gaming risk [HIGH]: Sector risk alignment 80% vs overall readiness 29/100. High keyword density without substantive governance — consistent with sector keyword stuffing. A genuinely sector-appropriate document would score higher on conceptual proximity and auditability (LAIF v1.2 Q2 Consistency).


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- conceptual — LAIF-like concepts insufficiently expressed


#### Structured Findings
**🔴 [HIGH] Coupling absent — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] High sector gaming risk detected**
- *Evidence:* Sector risk alignment 80% vs overall readiness 29/100. High keyword density without substantive governance — consistent with sector keyword stuffing. A genuinely sector-appropriate document would score higher on conceptual proximity and auditability (LAIF v1.2 Q2 Consistency).
- *Impact:* High sector keyword density with low substantive governance content is inconsistent with genuine compliance. Keyword selection without governance substance would not produce just outcomes at the individual-decision scale — failing Q2 Consistency (LAIF v1.2 Principle 5).
- *Recommended action:* Increase substantive coverage: add concrete obligations (auditability), named responsible parties (enforceability), and structural Coupling declarations. Sector keywords must be the vocabulary of genuine governance intent, not a substitute for it.

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (35/100)**
- *Evidence:* Score 35/100. Key missed signals: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined.
- *Impact:* A structural governance architecture score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 29/100.
- *Recommended action:* Target the missed signals for this dimension: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined. See weight_rationale in score_trace for prioritisation context.

**🟡 [MEDIUM] Low Conceptual coverage score (23/100)**
- *Evidence:* Score 23/100. Key missed signals: human rights / fundamental interests, explainability / interpretability, accountability.
- *Impact:* A conceptual coverage score below 30 increases the remediation effort required for LAIF adoption. Current overall readiness: 29/100.
- *Recommended action:* Target the missed signals for this dimension: human rights / fundamental interests, explainability / interpretability, accountability. See weight_rationale in score_trace for prioritisation context.



#### Remediation Plan (ordered by impact)
**1. Problem:** Structural Coupling not declared — the term 'Coupling' is absent.
   **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   **Concrete fix:** For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).

**2. Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).

**3. Problem:** Integrity Layer not declared as a deployment precondition.
   **Why it matters:** A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment — all three must be satisfied simultaneously before deployment may proceed. Partial satisfaction = failure. Without this gate, there is no precondition preventing premature deployment (LAIF v1.2 Part Two).
   **Concrete fix:** Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).

**4. Problem:** Constitutional hierarchy not declared (structural score 35/100). Missing: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined.
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**5. Problem:** Sector-specific governance gap (Clinical AI Deployment).
   **Why it matters:** The Clinical AI Deployment deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Declare Coupling between each clinical restriction and the specific patient interest it protects. Rewrite: 'AI alert suppression' → 'Coupling between alert suppression rules and the patient's interest in receiving clinically accurate recommendations' (Toolkit §2 B.1).

**6. Problem:** Sector-specific governance gap (Clinical AI Deployment).
   **Why it matters:** The Clinical AI Deployment deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply Q3 Reversibility: clinician override must always be preserved — AI recommendations must not displace clinical judgement irreversibly. Rewrite: 'AI system supports clinical decisions' → 'AI system provides recommendations subject to clinician override at every decision point, with override logged and reversible' (LAIF v1.2 Provision D1).


---

### TUC/CIPD — Framework for Fair AI in Employment Decisions

#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: Coupling, Integrity Layer, Coherence Test and 5 others. Overall readiness score: 35/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Root cause:** Primary gap: Coupling is absent — no restriction paired with a named human interest. Most common LAIF failure mode (Q1 of Coherence Test).

**Key risks:**
- Coupling quality is ABSENT: no governance restriction is structurally paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Moderate conceptual proximity (41/100): key LAIF-aligned governance concepts are present, indicating partial substantive alignment with LAIF's foundational principles.
- Strong sector risk alignment (80/100): the document addresses the materially relevant human interests for the Employment / Workforce AI deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | WEAK    |
| Structural contradictions       | NONE    |
| Sector gaming risk              | LOW     |
| Final verdict                   | FAIL    |

**Source type:** sector_policy  
**Sector:** Employment / Workforce AI  
**Coupling Quality:** ABSENT — Coupling not present in document  
**Remediation Effort:** HIGH


#### Scores and Signal Breakdown
**Structural: 28/100** ███░░░░░░░
  *Weak structural coverage (28/100): only 4 of 10 signals matched. Principal gaps: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).*
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
  *Weighting: 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).*

**Terminology: 0/100** ░░░░░░░░░░
  *No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.*
  − Coupling (0/25)
  − Coherence Test (0/20)
  − Integrity Layer (0/20)
  − Structural Transparency (0/10)
  − Structural Honesty (0/10)
  − Structural Containment (0/10)
  − Materially Affects Interests (0/5)
  *Weighting: 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).*

**Conceptual Proximity: 41/100** ████░░░░░░
  *Weak conceptual coverage (41/100): only 5 of 12 signals matched. Principal gaps: human rights / fundamental interests, human oversight, proportionality.*
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
  *Weighting: 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).*

**Auditability: 60/100** ██████░░░░
  *Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.*
  + numbered traceable requirements (+20)
  + evidence / documentation requirements (+20)
  + review / monitoring mechanisms (+20)
  − multiple mandatory obligations (shall … shall) (0/20)
  − specific, measurable obligations (0/20)
  *Weighting: 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).*

**Enforceability: 40/100** ████░░░░░░
  *Weak enforceability coverage (40/100): only 2 of 5 signals matched. Principal gaps: named responsible parties, risk-proportionate thresholds, enforcement consequences / penalties.*
  + mandatory language (shall) (+20)
  + non-discretionary operational mandates (+20)
  − named responsible parties (0/20)
  − risk-proportionate thresholds (0/20)
  − enforcement consequences / penalties (0/20)
  *Weighting: 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).*

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


#### Structured Findings
**🔴 [HIGH] Coupling absent — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (28/100)**
- *Evidence:* Score 28/100. Key missed signals: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
- *Impact:* A structural governance architecture score below 40 increases the remediation effort required for LAIF adoption. Current overall readiness: 35/100.
- *Recommended action:* Target the missed signals for this dimension: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). See weight_rationale in score_trace for prioritisation context.



#### Remediation Plan (ordered by impact)
**1. Problem:** Structural Coupling not declared — the term 'Coupling' is absent.
   **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   **Concrete fix:** For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).

**2. Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).

**3. Problem:** Integrity Layer not declared as a deployment precondition.
   **Why it matters:** A.1 Structural Transparency, A.2 Structural Honesty, A.3 Structural Containment — all three must be satisfied simultaneously before deployment may proceed. Partial satisfaction = failure. Without this gate, there is no precondition preventing premature deployment (LAIF v1.2 Part Two).
   **Concrete fix:** Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).

**4. Problem:** Constitutional hierarchy not declared (structural score 28/100). Missing: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**5. Problem:** Sector-specific governance gap (Employment / Workforce AI).
   **Why it matters:** The Employment / Workforce AI deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Declare Coupling between each employment AI restriction and the specific worker interest it protects. Rewrite: 'alignment between obligations imposed on workers and the protections those obligations are intended to serve' → 'Coupling between obligations imposed on workers and the protections afforded to their employment status and income' (Toolkit §2 B.1; LAIF v1.2 Principle 2).

**6. Problem:** Sector-specific governance gap (Employment / Workforce AI).
   **Why it matters:** The Employment / Workforce AI deployment context exposes specific human interests requiring tailored Coupling declarations and evidence artefacts (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply Q2 Consistency: governance logic must produce just outcomes across all scales — from individual worker to collective bargaining unit. Rewrite: 'AI performance assessment applies to all employees' → 'AI performance assessment applies consistently across all roles, scales, and worker categories, with equivalent review rights at each scale' (LAIF v1.2 Principle 5).


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