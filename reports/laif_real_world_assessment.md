# LAIF Real-World Assessment Report
**Framework version:** LAIF v1.2 · Compliance Toolkit v1.1  
**Date:** July 2026  
**Classification:** Governance Assessment — Evidence-Anchored Release  
**Validator:** validate.py (unchanged — strict formal compliance enforced)  
**Scoring:** Traceable per-signal breakdown for every dimension  
**Corpus:** 10 documents — 4 OFFICIAL_EXCERPT (verbatim, SHA-256-pinned against committed sources; findings citable) · 6 REPRESENTATIVE_EXCERPT (illustrative only)  
**Provenance enforcement:** test_provenance.py — every citability claim is machine-verified  

## Executive Summary
10 of 10 external AI governance frameworks assessed fail formal LAIF v1.2 compliance. Formal compliance is binary and strict — all 8 required constructs must be present; no partial credit is awarded.

**Citable result (official corpus):** 4 of 4 governance instruments assessed from verbatim official text fail formal LAIF v1.2 compliance, with an average conceptual proximity of 53/100 and average overall readiness of 37/100. Because these excerpts are exact, hash-pinned extracts of the committed authoritative texts, this finding can be stated of the source instruments themselves — subject to the excerpt scope declared per document. Instruments assessed: Executive Order 14110, 88 FR 75191 (Nov 1, 2023), FR Doc. 2023-24283; OECD Recommendation of the Council on Artificial Intelligence, OECD/LEGAL/0449, adopted 22 May 2019, amended 3 May 2024; NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0), January 2023, https://doi.org/10.6028/NIST.AI.100-1; Digital Technology Assessment Criteria for Health and Social Care (DTAC) v2.0, NHS England, 24 February 2026.

Dimensional scoring reveals that the gap is terminological and structural, not conceptual. Documents achieve an average conceptual proximity score of 51/100 and an average overall readiness score of 36/100, indicating that the underlying governance intent is broadly present — expressed through different vocabulary and structural frameworks.

**Core finding:** Existing frameworks address the right governance dimensions but do not enforce them through structural Coupling, the Coherence Test, or the Integrity Layer. LAIF is measurably stricter. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present. This finding now rests on two evidence tiers: it was first established on condensed representative excerpts and is now confirmed on verbatim official text, which removes the possibility that the result was an artefact of paraphrasing.

## Evidence Basis and Citability
Every document in the corpus carries a machine-verified provenance classification. Findings inherit the citability of the text they were computed from:

| Document                                             | Provenance             | Citable | Evidence basis                                               |
| ---------------------------------------------------- | ---------------------- | ------- | ------------------------------------------------------------ |
| US Executive Order 14110 — §2 Principles, §6 Workers | OFFICIAL_EXCERPT       | ✅ Yes   | docs/supporting/b0ef43db-202324283.md                        |
| OECD Recommendation on AI (OECD/LEGAL/0449) — Sectio | OFFICIAL_EXCERPT       | ✅ Yes   | docs/supporting/51a29205-OECD_Legal_Instruments.md           |
| NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Funct | OFFICIAL_EXCERPT       | ✅ Yes   | docs/supporting/5f667a6f-NIST.AI.1001.md                     |
| NHS England DTAC v2.0 (February 2026) — Introduction | OFFICIAL_EXCERPT       | ✅ Yes   | docs/supporting/55eccce3-DTAC_Form_2.0_February_2026.md      |
| EU AI Act — Art. 9, 13 & 14                          | REPRESENTATIVE_EXCERPT | ❌ No    | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A |
| NIST AI RMF — Govern & Map Functions                 | REPRESENTATIVE_EXCERPT | ❌ No    | https://airc.nist.gov/RMF                                    |
| OECD AI Principles (2019, rev. 2024)                 | REPRESENTATIVE_EXCERPT | ❌ No    | https://oecd.ai/en/ai-principles                             |
| US Executive Order 14110 — §4 Safety & §7 Workers    | REPRESENTATIVE_EXCERPT | ❌ No    | https://www.federalregister.gov/documents/2023/11/01/2023-24 |
| NHS England — AI in Clinical Decision Support (Polic | REPRESENTATIVE_EXCERPT | ❌ No    | illustrative document                                        |
| TUC/CIPD — Framework for Fair AI in Employment Decis | REPRESENTATIVE_EXCERPT | ❌ No    | illustrative document                                        |

**OFFICIAL_EXCERPT** — text extracted verbatim at run time from the committed source file using unique start/end markers and pinned by SHA-256 (official_documents.py). Any drift in the source file fails the run. Assessment results may be cited as findings about the named instrument, within the excerpt scope stated on the document's scorecard.

**REPRESENTATIVE_EXCERPT** — condensed paraphrase capturing governance intent. Results characterise the framework style, not the instrument's exact text, and must not be presented externally as assessments of the official source.

## Method
Each document was assessed against three complementary layers:

**Layer 1 — Formal LAIF compliance (binary):** 8 required constructs — Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles, non-amendable clause, self-application clause, Integrity Layer FINDING block, Coherence Test FINDING block. All 8 must be present. Enforced by validate.py (unchanged).

**Layer 2 — Dimensional scoring (traceable):** Five dimensions scored 0–100 with per-signal breakdown. Every score is accompanied by the signals that fired (earned points) and those that did not. This answers 'why this number?' for every dimension.

**Layer 3 — Sector analysis:** Each document assessed against a sector profile defining relevant human interests, risk indicator signals, and expected evidence artefacts. Produces sector risk alignment score (0–100) and sector-specific remediation priorities referencing LAIF source sections.

**Layer 4 — Structural depth (adversarial hardening):** Three diagnostic checks run against every document regardless of formal compliance verdict:
- **Coupling state** (STRUCTURALLY DECLARED / NOT STRUCTURALLY DECLARED): detects hollow or negated Coupling declarations; implicit signals surfaced separately (LAIF v1.2 Principle 2)
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

## Per-Document Scorecards — Citable (Official Sources)

### US Executive Order 14110 — §2 Principles, §6 Workers, §7 Civil Rights (official text)
> ✅ **OFFICIAL_EXCERPT** — text verified verbatim from the authoritative source.
> Verbatim text of Section 2 (Policy and Principles, (a)-(h)), Section 6 (Supporting Workers), and Section 7 (Advancing Equity and Civil Rights), extracted from the committed Federal Register full text and pinned by SHA-256. Non-contiguous sections joined with an explicit […] marker.
> Source: https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence
> Intended use: citable real-world baseline


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 42/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 42/100  
**Deployment Risk Tier:** 🟠 **HIGH**  
**Remediation Effort:** HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

> ⚠️ **This document may appear compliant but lacks the structural guarantees required for reliable governance.** A document can score moderately on readiness metrics while still failing every structural precondition that makes governance obligations enforceable.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Moderate conceptual proximity (57/100): key LAIF-aligned governance concepts are present, indicating partial substantive alignment with LAIF's foundational principles.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 43/100** ████░░░░░░

**Why:** Weak structural coverage (43/100): only 5 of 10 signals matched. Principal gaps: full lifecycle scope declared, risk stratification / proportionality, non-amendable constitutional hierarchy.

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- mandatory obligation language (shall) (+8 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)
- threshold gate conditions (all must pass simultaneously) (+15 pts)

**Signals missing:**
- full lifecycle scope declared (missed 6 pts)
- risk stratification / proportionality (missed 7 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 57/100** ██████░░░░

**Why:** Partial conceptual coverage (57/100): 7 of 12 signals matched. Key gaps: explainability / interpretability, proportionality.

**Signals detected:**
*Human interest signals:*
- human rights / fundamental interests (+10 pts)
- accountability (+8 pts)
- safety (+7 pts)
- fairness / labour / non-discrimination (+8 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- risk governance (+8 pts)

**Signals missing:**
- explainability / interpretability (missed 8 pts)
- proportionality (missed 8 pts)
- contestability / redress (missed 9 pts)
- reversibility / modifiability (missed 8 pts)
- traceability / responsibility (missed 10 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 40/100** ████░░░░░░

**Why:** Weak enforceability coverage (40/100): only 2 of 5 signals matched. Principal gaps: risk-proportionate thresholds, enforcement consequences / penalties, non-discretionary operational mandates.

**Signals detected:**
*Governance signals:*
- mandatory language (shall) (+20 pts)
*Structural signals:*
- named responsible parties (+20 pts)

**Signals missing:**
- risk-proportionate thresholds (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)
- non-discretionary operational mandates (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 42/100** ████░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**Sector risk alignment:** 20/100  

**Relevant human interests (Toolkit §1.2 — Materially Affects Interests):**
- freedom from arbitrary algorithmic decision-making
- transparency of AI reasoning and outputs
- effective human oversight and correction
- accountability for AI-caused harm
- access to redress and contestation mechanisms


#### Sector-Specific Findings
*Risk indicators detected:*
- ✅ transparency requirements
*Risk indicators absent:*
- ⚪ high-risk classification language
- ⚪ accountability assignment
- ⚪ human oversight mechanisms
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
- Expresses: accountability
- Expresses: human oversight
- Expresses: safety
- Expresses: risk governance
- Expresses: fairness / labour / non-discrimination
- Structure: numbered sub-requirements
- Structure: mandatory obligation language (shall)
- Structure: operational mechanisms defined


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present


#### Structured Findings
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
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

**4. Problem:** Constitutional hierarchy not declared (structural score 43/100). Missing: full lifecycle scope declared, risk stratification / proportionality, non-amendable constitutional hierarchy.
   **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

**5. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (official text)
> ✅ **OFFICIAL_EXCERPT** — text verified verbatim from the authoritative source.
> Verbatim text of Section 1 (Principles 1.1-1.5 for responsible stewardship of trustworthy AI) and Section 2 (Recommendations 2.1-2.5 for national policies), extracted from the committed OECD Legal Instruments snapshot (6 May 2026) and pinned by SHA-256. Source snapshot preserves the publisher's hard line-wrapping.
> Source: https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449
> Intended use: citable real-world baseline


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 39/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 39/100  
**Deployment Risk Tier:** 🔴 **CRITICAL**  
**Remediation Effort:** HIGH
**Primary structural failure:** protections are suggested but not structurally bound to obligations.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document signals protective intent but does not structurally bind obligations to the people they protect — the intent is present but not enforceable as written.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.
- Low enforceability (20/100): mandatory language ('shall'), named responsible parties, and enforcement consequences are largely absent. Governance provisions are aspirational rather than operationally binding.

**Key strengths:**
- High conceptual proximity (84/100): accountability, oversight, transparency, and contestability are expressed through the document's own vocabulary. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

This document contains:
- implicit Coupling signals (protective intent present)

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (implicit signals present) ❌

**Implicit signals detected:**
- «AI actors should be accountable for the proper functioning of AI systems and for the respect of»

**Interpretation:**  
These statements indicate recognition of responsibility or protection, but do not explicitly bind restrictions to protected human interests.

**Why this matters:**  
IMPLICIT coupling signals indicate intent, but do NOT provide enforceable structural guarantees. The obligations and protections are not formally bound, meaning protections can be removed without affecting obligations. This does not constitute partial compliance — the structural requirement is absent regardless of expressed intent.

**Practical meaning:**  
This document signals protective intent. However, an operator could modify specific obligations without being required to maintain the corresponding protections. The governance intent is present; the structural enforceability is not.

**Fix:**  
Explicitly pair each restriction with the human interest it protects. Ensure both carry equivalent normative force — neither can be weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.

*Note: implicit coupling signals already present (see above) — the governance intent is established. This upgrade is terminological and structural, not conceptual.*


#### Scores and Signal Breakdown
**Structural — 26/100** ███░░░░░░░

**Why:** Weak structural coverage (26/100): only 4 of 10 signals matched. Principal gaps: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- full lifecycle scope declared (+6 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)

**Signals missing:**
- mandatory obligation language (shall) (missed 8 pts)
- risk stratification / proportionality (missed 7 pts)
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 84/100** ████████░░

**Why:** Strong conceptual coverage (84/100): 10 of 12 signals matched. Strongest contributors: human rights / fundamental interests, transparency.

**Signals detected:**
*Human interest signals:*
- human rights / fundamental interests (+10 pts)
- accountability (+8 pts)
- safety (+7 pts)
- contestability / redress (+9 pts)
- fairness / labour / non-discrimination (+8 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- explainability / interpretability (+8 pts)
- risk governance (+8 pts)
- traceability / responsibility (+10 pts)

**Signals missing:**
- proportionality (missed 8 pts)
- reversibility / modifiability (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 20/100** ██░░░░░░░░

**Why:** Weak enforceability coverage (20/100): only 1 of 5 signals matched. Principal gaps: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.

**Signals detected:**
*Structural signals:*
- named responsible parties (+20 pts)

**Signals missing:**
- mandatory language (shall) (missed 20 pts)
- risk-proportionate thresholds (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)
- non-discretionary operational mandates (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 39/100** ████░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
- Expresses: risk governance
- Expresses: traceability / responsibility
- Expresses: fairness / labour / non-discrimination


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- enforceability — insufficient mandatory operational requirements


#### Structured Findings
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (26/100)**
- *Evidence:* Score 26/100. Key missed signals: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🟡 [MEDIUM] Low Enforceability score (20/100)**
- *Evidence:* Score 20/100. Key missed signals: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.
- *Impact:* Without enforceable obligations, regulatory bodies cannot hold operators accountable for governance failures. The standard is aspirational rather than operationally binding — no party can be required to comply.
- *Recommended action:* Target the missed signals for this dimension: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**5. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Functions (official text)
> ✅ **OFFICIAL_EXCERPT** — text verified verbatim from the authoritative source.
> Verbatim text of the Part 2 Core GOVERN function (narrative + Table 1 categories/subcategories) and MAP function (narrative + Table 2), extracted from the committed NIST AI 100-1 full text and pinned by SHA-256. Table text retains the source's markdown table formatting.
> Source: https://doi.org/10.6028/NIST.AI.100-1
> Intended use: citable real-world baseline


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 48/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 48/100  
**Deployment Risk Tier:** 🟠 **HIGH**  
**Remediation Effort:** HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

> ⚠️ **This document may appear compliant but lacks the structural guarantees required for reliable governance.** A document can score moderately on readiness metrics while still failing every structural precondition that makes governance obligations enforceable.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Moderate conceptual proximity (47/100): key LAIF-aligned governance concepts are present, indicating partial substantive alignment with LAIF's foundational principles.
- Strong sector risk alignment (80/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 41/100** ████░░░░░░

**Why:** Weak structural coverage (41/100): only 6 of 10 signals matched. Principal gaps: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven).

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- mandatory obligation language (shall) (+8 pts)
- full lifecycle scope declared (+6 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)
*Structural signals:*
- risk stratification / proportionality (+7 pts)

**Signals missing:**
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 47/100** █████░░░░░

**Why:** Weak conceptual coverage (47/100): only 6 of 12 signals matched. Principal gaps: human rights / fundamental interests, explainability / interpretability, contestability / redress.

**Signals detected:**
*Human interest signals:*
- accountability (+8 pts)
- safety (+7 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- proportionality (+8 pts)
- risk governance (+8 pts)

**Signals missing:**
- human rights / fundamental interests (missed 10 pts)
- explainability / interpretability (missed 8 pts)
- contestability / redress (missed 9 pts)
- reversibility / modifiability (missed 8 pts)
- traceability / responsibility (missed 10 pts)
- fairness / labour / non-discrimination (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 80/100** ████████░░

**Why:** Strong enforceability coverage (80/100): 4 of 5 signals matched. Strongest contributors: mandatory language (shall), named responsible parties.

**Signals detected:**
*Governance signals:*
- mandatory language (shall) (+20 pts)
- risk-proportionate thresholds (+20 pts)
- enforcement consequences / penalties (+20 pts)
*Structural signals:*
- named responsible parties (+20 pts)

**Signals missing:**
- non-discretionary operational mandates (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 48/100** █████░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**Sector risk alignment:** 80/100  

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
*Risk indicators absent:*
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
- Expresses: transparency
- Expresses: accountability
- Expresses: human oversight
- Expresses: proportionality
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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
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

**5. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### NHS England DTAC v2.0 (February 2026) — Introduction & C1 Clinical Safety (official text)
> ✅ **OFFICIAL_EXCERPT** — text verified verbatim from the authoritative source.
> Verbatim text of the DTAC v2.0 Introduction (scope, definitions, assessment structure) and assessed section C1 Clinical safety (criteria C1.1.1-C1.2.5 incl. DCB0129 requirements), extracted from the committed source text and pinned by SHA-256. Non-contiguous sections joined with an explicit […] marker.
> Source: https://transform.england.nhs.uk/key-tools-and-info/digital-technology-assessment-criteria-dtac/
> Intended use: citable sector scenario — clinical AI assurance


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 20/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 20/100  
**Deployment Risk Tier:** 🔴 **CRITICAL**  
**Remediation Effort:** VERY HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- High sector gaming risk: sector keyword density is elevated while substantive governance content is low (overall 20/100). This pattern would not produce just outcomes at the individual-decision scale — failing Q2 Consistency. (LAIF v1.2 Principle 5)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Strong sector risk alignment (80/100): the document addresses the materially relevant human interests for the Clinical AI Deployment deployment context.

**Position Assessment:**

This document contains:
- Consistency

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


#### Compliance Summary
| Dimension                       | Verdict |
| ------------------------------- | ------- |
| Formal compliance (binary gate) | FAIL    |
| Structural depth                | HOLLOW  |
| Structural contradictions       | NONE    |
| Sector gaming risk              | HIGH    |
| Final verdict                   | FAIL    |

> **Interpretation caveat (official instrument):** the sector gaming heuristic detects high sector-keyword density with low prose-style governance content. This document is a verified official instrument, so the flag does not indicate keyword stuffing by its publisher — it indicates a *format mismatch*: questionnaire/form-style instruments carry their governance content in assessed criteria rather than declaratory prose, which the density heuristics undercount. The structural gaps reported below remain real; the gaming attribution should not be cited.

**Source type:** sector_policy  
**Sector:** Clinical AI Deployment  
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 12/100** █░░░░░░░░░

**Why:** Weak structural coverage (12/100): only 2 of 10 signals matched. Principal gaps: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.

**Signals detected:**
*Governance signals:*
- full lifecycle scope declared (+6 pts)
- operational mechanisms defined (+6 pts)

**Signals missing:**
- numbered sub-requirements (missed 8 pts)
- mandatory obligation language (shall) (missed 8 pts)
- risk stratification / proportionality (missed 7 pts)
- review / monitoring mechanisms (missed 6 pts)
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 24/100** ██░░░░░░░░

**Why:** Weak conceptual coverage (24/100): only 3 of 12 signals matched. Principal gaps: human rights / fundamental interests, transparency, explainability / interpretability.

**Signals detected:**
*Human interest signals:*
- safety (+7 pts)
- contestability / redress (+9 pts)
*Structural signals:*
- risk governance (+8 pts)

**Signals missing:**
- human rights / fundamental interests (missed 10 pts)
- transparency (missed 8 pts)
- explainability / interpretability (missed 8 pts)
- accountability (missed 8 pts)
- human oversight (missed 8 pts)
- proportionality (missed 8 pts)
- reversibility / modifiability (missed 8 pts)
- traceability / responsibility (missed 10 pts)
- fairness / labour / non-discrimination (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 40/100** ████░░░░░░

**Why:** Weak auditability coverage (40/100): only 2 of 5 signals matched. Principal gaps: multiple mandatory obligations (shall … shall), numbered traceable requirements, review / monitoring mechanisms.

**Signals detected:**
*Governance signals:*
- evidence / documentation requirements (+20 pts)
- specific, measurable obligations (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- numbered traceable requirements (missed 20 pts)
- review / monitoring mechanisms (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 20/100** ██░░░░░░░░

**Why:** Weak enforceability coverage (20/100): only 1 of 5 signals matched. Principal gaps: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.

**Signals detected:**
*Structural signals:*
- named responsible parties (+20 pts)

**Signals missing:**
- mandatory language (shall) (missed 20 pts)
- risk-proportionate thresholds (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)
- non-discretionary operational mandates (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 20/100** ██░░░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


#### Construct Coverage
| Construct               | Present | LAIF Source                      |
| ----------------------- | ------- | -------------------------------- |
| Coupling                | ❌ No    | v1.2 Principle 2; Toolkit §2 B.1 |
| Coherence Test          | ❌ No    | v1.2 Part One                    |
| Integrity Layer         | ❌ No    | v1.2 Part Two                    |
| Structural Transparency | ❌ No    | Toolkit §1.3 (A.1)               |
| Structural Honesty      | ❌ No    | Toolkit §1.4 (A.2)               |
| Structural Containment  | ❌ No    | Toolkit §1.5 (A.3)               |
| Consistency             | ✅ Yes   | v1.2 Principle 5                 |
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
- ✅ patient safety signal
- ✅ diagnostic / treatment language
- ✅ named clinical actor
- ✅ medical device classification
*Risk indicators absent:*
- ⚪ clinical decision output
*Evidence gaps:*
- ❌ clinical validation evidence
- ❌ informed consent documentation
- ❌ clinical audit / governance
- ❌ adverse event / incident reporting
- ❌ post-deployment performance monitoring


#### Paraphrase Violations
None detected.


#### Strengths
- Expresses: safety
- Expresses: contestability / redress
- Expresses: risk governance
- Structure: full lifecycle scope declared
- Structure: operational mechanisms defined
- Auditability: evidence / documentation requirements
- Auditability: specific, measurable obligations
- Enforceability: named responsible parties


#### Gaps
- Canonical LAIF terms absent: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- LAIF structural element missing: threshold gate conditions (all must pass simultaneously)
- LAIF structural element missing: non-amendable constitutional hierarchy
- LAIF structural element missing: self-application clause (Part Seven)
- LAIF structural element missing: named decision instrument (Coherence Test / PDCA)
- Sector gaming risk [HIGH]: Sector risk alignment 80% vs overall readiness 20/100. High keyword density without substantive governance — consistent with sector keyword stuffing. A genuinely sector-appropriate document would score higher on conceptual proximity and auditability (LAIF v1.2 Q2 Consistency).


#### Primary Failure Modes
- structural — constitutional hierarchy not declared
- terminological — no canonical LAIF terms present
- conceptual — LAIF-like concepts insufficiently expressed
- enforceability — insufficient mandatory operational requirements


#### Structured Findings
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] High sector gaming risk detected**
- *Evidence:* Sector risk alignment 80% vs overall readiness 20/100. High keyword density without substantive governance — consistent with sector keyword stuffing. A genuinely sector-appropriate document would score higher on conceptual proximity and auditability (LAIF v1.2 Q2 Consistency).
- *Impact:* High sector keyword density with low substantive governance content is inconsistent with genuine compliance. Keyword selection without governance substance would not produce just outcomes at the individual-decision scale — failing Q2 Consistency (LAIF v1.2 Principle 5).
- *Recommended action:* Increase substantive coverage: add concrete obligations (auditability), named responsible parties (enforceability), and structural Coupling declarations. Sector keywords must be the vocabulary of genuine governance intent, not a substitute for it.

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (12/100)**
- *Evidence:* Score 12/100. Key missed signals: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🟡 [MEDIUM] Low Conceptual coverage score (24/100)**
- *Evidence:* Score 24/100. Key missed signals: human rights / fundamental interests, transparency, explainability / interpretability.
- *Impact:* Low conceptual proximity indicates the document's governance intent is not substantially aligned with LAIF values. The adoption gap is more fundamental than terminology — substantive governance redesign is required, not just terminological substitution.
- *Recommended action:* Target the missed signals for this dimension: human rights / fundamental interests, transparency, explainability / interpretability. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🟡 [MEDIUM] Low Enforceability score (20/100)**
- *Evidence:* Score 20/100. Key missed signals: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.
- *Impact:* Without enforceable obligations, regulatory bodies cannot hold operators accountable for governance failures. The standard is aspirational rather than operationally binding — no party can be required to comply.
- *Recommended action:* Target the missed signals for this dimension: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**5. Problem:** Declare Coupling between each clinical restriction and the specific patient interest it protects. Rewrite: 'AI… — not addressed in this document.
   **Why it matters:** In the Clinical AI Deployment deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Declare Coupling between each clinical restriction and the specific patient interest it protects. Rewrite: 'AI alert suppression' → 'Coupling between alert suppression rules and the patient's interest in receiving clinically accurate recommendations' (Toolkit §2 B.1).

**6. Problem:** Apply Q3 Reversibility: clinician override must always be preserved — not addressed in this document.
   **Why it matters:** In the Clinical AI Deployment deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply Q3 Reversibility: clinician override must always be preserved — AI recommendations must not displace clinical judgement irreversibly. Rewrite: 'AI system supports clinical decisions' → 'AI system provides recommendations subject to clinician override at every decision point, with override logged and reversible' (LAIF v1.2 Provision D1).


---

## Per-Document Scorecards — Illustrative (Representative Excerpts)

### EU AI Act — Art. 9, 13 & 14
> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. Not verbatim. Not citable as the primary source.
> Condensed paraphrase of Articles 9, 13, and 14; captures governance intent but is not verbatim text. Verify against official OJ publication.
> Source: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689
> Intended use: real-world baseline


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 44/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 44/100  
**Deployment Risk Tier:** 🟠 **HIGH**  
**Remediation Effort:** HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

> ⚠️ **This document may appear compliant but lacks the structural guarantees required for reliable governance.** A document can score moderately on readiness metrics while still failing every structural precondition that makes governance obligations enforceable.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Moderate conceptual proximity (49/100): key LAIF-aligned governance concepts are present, indicating partial substantive alignment with LAIF's foundational principles.
- Strong sector risk alignment (60/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 41/100** ████░░░░░░

**Why:** Weak structural coverage (41/100): only 6 of 10 signals matched. Principal gaps: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven).

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- mandatory obligation language (shall) (+8 pts)
- full lifecycle scope declared (+6 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)
*Structural signals:*
- risk stratification / proportionality (+7 pts)

**Signals missing:**
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 49/100** █████░░░░░

**Why:** Weak conceptual coverage (49/100): only 6 of 12 signals matched. Principal gaps: accountability, proportionality, contestability / redress.

**Signals detected:**
*Human interest signals:*
- human rights / fundamental interests (+10 pts)
- safety (+7 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- explainability / interpretability (+8 pts)
- risk governance (+8 pts)

**Signals missing:**
- accountability (missed 8 pts)
- proportionality (missed 8 pts)
- contestability / redress (missed 9 pts)
- reversibility / modifiability (missed 8 pts)
- traceability / responsibility (missed 10 pts)
- fairness / labour / non-discrimination (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 60/100** ██████░░░░

**Why:** Partial enforceability coverage (60/100): 3 of 5 signals matched. Key gaps: named responsible parties, enforcement consequences / penalties.

**Signals detected:**
*Governance signals:*
- mandatory language (shall) (+20 pts)
- risk-proportionate thresholds (+20 pts)
*Structural signals:*
- non-discretionary operational mandates (+20 pts)

**Signals missing:**
- named responsible parties (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 44/100** ████░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
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

**5. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### NIST AI RMF — Govern & Map Functions
> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. Not verbatim. Not citable as the primary source.
> Condensed paraphrase of GOVERN and MAP functions; note British spelling 'organisational' departs from the American-English original. Not verbatim.
> Source: https://airc.nist.gov/RMF
> Intended use: real-world baseline


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 30/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 30/100  
**Deployment Risk Tier:** 🔴 **CRITICAL**  
**Remediation Effort:** VERY HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.
- Low enforceability (20/100): mandatory language ('shall'), named responsible parties, and enforcement consequences are largely absent. Governance provisions are aspirational rather than operationally binding.

**Key strengths:**
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 26/100** ███░░░░░░░

**Why:** Weak structural coverage (26/100): only 4 of 10 signals matched. Principal gaps: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- full lifecycle scope declared (+6 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)

**Signals missing:**
- mandatory obligation language (shall) (missed 8 pts)
- risk stratification / proportionality (missed 7 pts)
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 39/100** ████░░░░░░

**Why:** Weak conceptual coverage (39/100): only 5 of 12 signals matched. Principal gaps: human rights / fundamental interests, explainability / interpretability, proportionality.

**Signals detected:**
*Human interest signals:*
- accountability (+8 pts)
- safety (+7 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- risk governance (+8 pts)

**Signals missing:**
- human rights / fundamental interests (missed 10 pts)
- explainability / interpretability (missed 8 pts)
- proportionality (missed 8 pts)
- contestability / redress (missed 9 pts)
- reversibility / modifiability (missed 8 pts)
- traceability / responsibility (missed 10 pts)
- fairness / labour / non-discrimination (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 20/100** ██░░░░░░░░

**Why:** Weak enforceability coverage (20/100): only 1 of 5 signals matched. Principal gaps: mandatory language (shall), named responsible parties, risk-proportionate thresholds.

**Signals detected:**
*Governance signals:*
- enforcement consequences / penalties (+20 pts)

**Signals missing:**
- mandatory language (shall) (missed 20 pts)
- named responsible parties (missed 20 pts)
- risk-proportionate thresholds (missed 20 pts)
- non-discretionary operational mandates (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 30/100** ███░░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (26/100)**
- *Evidence:* Score 26/100. Key missed signals: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🟡 [MEDIUM] Low Enforceability score (20/100)**
- *Evidence:* Score 20/100. Key missed signals: mandatory language (shall), named responsible parties, risk-proportionate thresholds.
- *Impact:* Without enforceable obligations, regulatory bodies cannot hold operators accountable for governance failures. The standard is aspirational rather than operationally binding — no party can be required to comply.
- *Recommended action:* Target the missed signals for this dimension: mandatory language (shall), named responsible parties, risk-proportionate thresholds. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**5. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### OECD AI Principles (2019, rev. 2024)
> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. Not verbatim. Not citable as the primary source.
> Condensed paraphrase of the five OECD AI Principles; structural numbering and intent preserved but wording is not verbatim.
> Source: https://oecd.ai/en/ai-principles
> Intended use: real-world baseline


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 22/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 22/100  
**Deployment Risk Tier:** 🔴 **CRITICAL**  
**Remediation Effort:** VERY HIGH
**Primary structural failure:** protections are suggested but not structurally bound to obligations.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document signals protective intent but does not structurally bind obligations to the people they protect — the intent is present but not enforceable as written.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.
- Low enforceability (20/100): mandatory language ('shall'), named responsible parties, and enforcement consequences are largely absent. Governance provisions are aspirational rather than operationally binding.

**Key strengths:**
- High conceptual proximity (76/100): accountability, oversight, transparency, and contestability are expressed through the document's own vocabulary. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present.
- Strong sector risk alignment (60/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.

**Position Assessment:**

This document contains:
- implicit Coupling signals (protective intent present)

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (implicit signals present) ❌

**Implicit signals detected:**
- «AI actors should be accountable for the proper functioning of AI systems and for the respect of»

**Interpretation:**  
These statements indicate recognition of responsibility or protection, but do not explicitly bind restrictions to protected human interests.

**Why this matters:**  
IMPLICIT coupling signals indicate intent, but do NOT provide enforceable structural guarantees. The obligations and protections are not formally bound, meaning protections can be removed without affecting obligations. This does not constitute partial compliance — the structural requirement is absent regardless of expressed intent.

**Practical meaning:**  
This document signals protective intent. However, an operator could modify specific obligations without being required to maintain the corresponding protections. The governance intent is present; the structural enforceability is not.

**Fix:**  
Explicitly pair each restriction with the human interest it protects. Ensure both carry equivalent normative force — neither can be weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.

*Note: implicit coupling signals already present (see above) — the governance intent is established. This upgrade is terminological and structural, not conceptual.*


#### Scores and Signal Breakdown
**Structural — 12/100** █░░░░░░░░░

**Why:** Weak structural coverage (12/100): only 2 of 10 signals matched. Principal gaps: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.

**Signals detected:**
*Governance signals:*
- full lifecycle scope declared (+6 pts)
- operational mechanisms defined (+6 pts)

**Signals missing:**
- numbered sub-requirements (missed 8 pts)
- mandatory obligation language (shall) (missed 8 pts)
- risk stratification / proportionality (missed 7 pts)
- review / monitoring mechanisms (missed 6 pts)
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 76/100** ████████░░

**Why:** Partial conceptual coverage (76/100): 9 of 12 signals matched. Key gaps: proportionality, reversibility / modifiability.

**Signals detected:**
*Human interest signals:*
- human rights / fundamental interests (+10 pts)
- accountability (+8 pts)
- safety (+7 pts)
- contestability / redress (+9 pts)
- fairness / labour / non-discrimination (+8 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- explainability / interpretability (+8 pts)
- traceability / responsibility (+10 pts)

**Signals missing:**
- proportionality (missed 8 pts)
- reversibility / modifiability (missed 8 pts)
- risk governance (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 0/100** ░░░░░░░░░░

**Why:** No auditability signals present — none of the 5 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- numbered traceable requirements (missed 20 pts)
- evidence / documentation requirements (missed 20 pts)
- review / monitoring mechanisms (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 20/100** ██░░░░░░░░

**Why:** Weak enforceability coverage (20/100): only 1 of 5 signals matched. Principal gaps: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.

**Signals detected:**
*Structural signals:*
- named responsible parties (+20 pts)

**Signals missing:**
- mandatory language (shall) (missed 20 pts)
- risk-proportionate thresholds (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)
- non-discretionary operational mandates (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 22/100** ██░░░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (12/100)**
- *Evidence:* Score 12/100. Key missed signals: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality.
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🔴 [HIGH] Low Auditability score (0/100)**
- *Evidence:* Score 0/100. Key missed signals: multiple mandatory obligations (shall … shall), numbered traceable requirements, evidence / documentation requirements.
- *Impact:* Without numbered, traceable obligations, a PDCA auditor has no objective basis to verify compliance — compliance claims rest on assertions rather than verifiable evidence. External audit cannot proceed.
- *Recommended action:* Target the missed signals for this dimension: multiple mandatory obligations (shall … shall), numbered traceable requirements, evidence / documentation requirements. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🟡 [MEDIUM] Low Enforceability score (20/100)**
- *Evidence:* Score 20/100. Key missed signals: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties.
- *Impact:* Without enforceable obligations, regulatory bodies cannot hold operators accountable for governance failures. The standard is aspirational rather than operationally binding — no party can be required to comply.
- *Recommended action:* Target the missed signals for this dimension: mandatory language (shall), risk-proportionate thresholds, enforcement consequences / penalties. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**5. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**6. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### US Executive Order 14110 — §4 Safety & §7 Workers
> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. Not verbatim. Not citable as the primary source.
> Paraphrased and condensed from §4 (Safety/Security) and §7 (Workers); contains purpose-adapted wording including LAIF paraphrase test terms ('linkage', 'connection') to exercise paraphrase detection. Not verbatim.
> Source: https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence
> Intended use: real-world baseline with embedded paraphrase stress-test


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 50/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 50/100  
**Deployment Risk Tier:** 🟠 **HIGH**  
**Remediation Effort:** HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

> ⚠️ **This document may appear compliant but lacks the structural guarantees required for reliable governance.** A document can score moderately on readiness metrics while still failing every structural precondition that makes governance obligations enforceable.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- High conceptual proximity (66/100): accountability, oversight, transparency, and contestability are expressed through the document's own vocabulary. The adoption pathway is terminological and structural, not conceptual — the underlying intent is already present.
- Strong sector risk alignment (100/100): the document addresses the materially relevant human interests for the General AI Governance deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Forbidden paraphrase of 'Coupling' detected: «engage with industry, civil society, and other stakeholders to develop guidelines, standards, method»** — Replace the forbidden term with 'Coupling' at every occurrence. For 'Coupling' specifically, also add: the named human interest, the paired restriction, and a statement of equivalent normative force on both sides (Toolkit §2 B.1; LAIF v1.2 Principle 2).
2. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
3. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).


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
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 35/100** ████░░░░░░

**Why:** Weak structural coverage (35/100): only 5 of 10 signals matched. Principal gaps: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy.

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- mandatory obligation language (shall) (+8 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)
*Structural signals:*
- risk stratification / proportionality (+7 pts)

**Signals missing:**
- full lifecycle scope declared (missed 6 pts)
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 66/100** ███████░░░

**Why:** Partial conceptual coverage (66/100): 8 of 12 signals matched. Key gaps: explainability / interpretability, reversibility / modifiability.

**Signals detected:**
*Human interest signals:*
- human rights / fundamental interests (+10 pts)
- accountability (+8 pts)
- safety (+7 pts)
- contestability / redress (+9 pts)
- fairness / labour / non-discrimination (+8 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)
*Structural signals:*
- proportionality (+8 pts)

**Signals missing:**
- explainability / interpretability (missed 8 pts)
- reversibility / modifiability (missed 8 pts)
- risk governance (missed 8 pts)
- traceability / responsibility (missed 10 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 80/100** ████████░░

**Why:** Strong enforceability coverage (80/100): 4 of 5 signals matched. Strongest contributors: mandatory language (shall), named responsible parties.

**Signals detected:**
*Governance signals:*
- mandatory language (shall) (+20 pts)
- risk-proportionate thresholds (+20 pts)
*Structural signals:*
- named responsible parties (+20 pts)
- non-discretionary operational mandates (+20 pts)

**Signals missing:**
- enforcement consequences / penalties (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 50/100** █████░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
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
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**6. Problem:** Introduce structural Coupling for each governance provision — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Introduce structural Coupling for each governance provision — pair the restriction with the specific human interest it protects, with equivalent normative force on both sides (LAIF v1.2 Principle 2; Toolkit §2 B.1).

**7. Problem:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Re… — not addressed in this document.
   **Why it matters:** In the General AI Governance deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply the Coherence Test before any provision is issued: Q1 Coupling, Q2 Consistency (scale-invariance), Q3 Reversibility. Failure at Q1 = automatic full failure (LAIF v1.2 Part One).


---

### NHS England — AI in Clinical Decision Support (Policy Framework)
> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. Not verbatim. Not citable as the primary source.
> Illustrative sector scenario: structured in the style of NHS England governance documentation but is not an official NHS England publication. Citation text confirms '(illustrative excerpt)'. For sector assessment demonstration only.
> Intended use: sector scenario — clinical AI governance


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 29/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 29/100  
**Deployment Risk Tier:** 🔴 **CRITICAL**  
**Remediation Effort:** VERY HIGH
**Primary structural failure:** obligations are defined without enforceable protections for affected individuals.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document imposes obligations but does not structurally protect the people those obligations are meant to serve — each obligation can be removed independently of any corresponding protection.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- High sector gaming risk: sector keyword density is elevated while substantive governance content is low (overall 29/100). This pattern would not produce just outcomes at the individual-decision scale — failing Q2 Consistency. (LAIF v1.2 Principle 5)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Strong sector risk alignment (80/100): the document addresses the materially relevant human interests for the Clinical AI Deployment deployment context.

**Position Assessment:**

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (no signals detected) ❌

No implicit coupling signals detected. The document does not express protective intent in a form that can be structurally upgraded via terminological revision alone.

**Practical meaning:**  
This document imposes obligations but does not structurally protect the people those obligations are meant to serve. Obligations can be weakened or removed independently of the protections they were intended to provide.


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.



#### Scores and Signal Breakdown
**Structural — 35/100** ████░░░░░░

**Why:** Weak structural coverage (35/100): only 4 of 10 signals matched. Principal gaps: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined.

**Signals detected:**
*Governance signals:*
- mandatory obligation language (shall) (+8 pts)
- full lifecycle scope declared (+6 pts)
- review / monitoring mechanisms (+6 pts)
- threshold gate conditions (all must pass simultaneously) (+15 pts)

**Signals missing:**
- numbered sub-requirements (missed 8 pts)
- risk stratification / proportionality (missed 7 pts)
- operational mechanisms defined (missed 6 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 23/100** ██░░░░░░░░

**Why:** Weak conceptual coverage (23/100): only 3 of 12 signals matched. Principal gaps: human rights / fundamental interests, explainability / interpretability, accountability.

**Signals detected:**
*Human interest signals:*
- safety (+7 pts)
*Governance signals:*
- transparency (+8 pts)
- human oversight (+8 pts)

**Signals missing:**
- human rights / fundamental interests (missed 10 pts)
- explainability / interpretability (missed 8 pts)
- accountability (missed 8 pts)
- proportionality (missed 8 pts)
- contestability / redress (missed 9 pts)
- reversibility / modifiability (missed 8 pts)
- risk governance (missed 8 pts)
- traceability / responsibility (missed 10 pts)
- fairness / labour / non-discrimination (missed 8 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 40/100** ████░░░░░░

**Why:** Weak auditability coverage (40/100): only 2 of 5 signals matched. Principal gaps: multiple mandatory obligations (shall … shall), numbered traceable requirements, specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- numbered traceable requirements (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 40/100** ████░░░░░░

**Why:** Weak enforceability coverage (40/100): only 2 of 5 signals matched. Principal gaps: named responsible parties, risk-proportionate thresholds, enforcement consequences / penalties.

**Signals detected:**
*Governance signals:*
- mandatory language (shall) (+20 pts)
*Structural signals:*
- non-discretionary operational mandates (+20 pts)

**Signals missing:**
- named responsible parties (missed 20 pts)
- risk-proportionate thresholds (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 29/100** ███░░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
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
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.

**🟡 [MEDIUM] Low Conceptual coverage score (23/100)**
- *Evidence:* Score 23/100. Key missed signals: human rights / fundamental interests, explainability / interpretability, accountability.
- *Impact:* Low conceptual proximity indicates the document's governance intent is not substantially aligned with LAIF values. The adoption gap is more fundamental than terminology — substantive governance redesign is required, not just terminological substitution.
- *Recommended action:* Target the missed signals for this dimension: human rights / fundamental interests, explainability / interpretability, accountability. The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**5. Problem:** Declare Coupling between each clinical restriction and the specific patient interest it protects. Rewrite: 'AI… — not addressed in this document.
   **Why it matters:** In the Clinical AI Deployment deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Declare Coupling between each clinical restriction and the specific patient interest it protects. Rewrite: 'AI alert suppression' → 'Coupling between alert suppression rules and the patient's interest in receiving clinically accurate recommendations' (Toolkit §2 B.1).

**6. Problem:** Apply Q3 Reversibility: clinician override must always be preserved — not addressed in this document.
   **Why it matters:** In the Clinical AI Deployment deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply Q3 Reversibility: clinician override must always be preserved — AI recommendations must not displace clinical judgement irreversibly. Rewrite: 'AI system supports clinical decisions' → 'AI system provides recommendations subject to clinician override at every decision point, with override logged and reversible' (LAIF v1.2 Provision D1).


---

### TUC/CIPD — Framework for Fair AI in Employment Decisions
> ⚠️ **REPRESENTATIVE_EXCERPT** — condensed paraphrase or illustrative excerpt. Not verbatim. Not citable as the primary source.
> Illustrative sector scenario: written in the style of TUC/CIPD employment AI guidance but is not an official publication of either body. Citation text confirms 'Illustrative...sector assessment document'. For sector assessment demonstration only.
> Intended use: sector scenario — employment AI governance


#### Executive Assessment
> This document fails formal LAIF v1.2 compliance. Required constructs absent: all 8 required constructs. Overall readiness score: 35/100. Formal compliance is binary — partial presence of required constructs does not constitute compliance.

**Overall Readiness:** 35/100  
**Deployment Risk Tier:** 🔴 **CRITICAL**  
**Remediation Effort:** HIGH
**Primary structural failure:** protections are suggested but not structurally bound to obligations.

**Root cause:** Primary structural gap: Coupling not structurally declared.

**What this means in practice:** This document signals protective intent but does not structurally bind obligations to the people they protect — the intent is present but not enforceable as written.

**Key risks:**
- Coupling not structurally declared: no governance restriction is paired with a named human interest. Each restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) failure = automatic failure of the full Coherence Test. (LAIF v1.2 Principle 2)
- Formal compliance gate not satisfied: 8 required construct(s) absent — Coupling, Integrity Layer, Coherence Test. Missing any single construct = FAIL regardless of overall readiness score.

**Key strengths:**
- Moderate conceptual proximity (41/100): key LAIF-aligned governance concepts are present, indicating partial substantive alignment with LAIF's foundational principles.
- Strong sector risk alignment (80/100): the document addresses the materially relevant human interests for the Employment / Workforce AI deployment context.
- Good auditability (60/100): numbered requirements, evidence mandates, and monitoring mechanisms are present — obligations can be externally verified.

**Position Assessment:**

This document contains:
- implicit Coupling signals (protective intent present)

However, the following are not structurally enforced:
- Coupling not structurally declared — restrictions not bound to human interests
- Coherence Test not applied — Q1/Q2/Q3 not documented
- Integrity Layer not declared as a deployment precondition

**Result:** Conceptually aligned, structurally incomplete

**What Must Be Fixed First:**
1. **Structural Coupling not declared — the term 'Coupling' is absent.** — For each governance restriction, add: 'Coupling between [restriction] and [the specific human interest it protects], with [named protection mechanism] of equivalent normative force.' Both sides must be named explicitly; neither can be weakened in isolation (Toolkit §2 B.1).
2. **Coherence Test not applied — no Q1/Q2/Q3 documentation present.** — Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
3. **Integrity Layer not declared as a deployment precondition.** — Add an Integrity Layer section with three threshold conditions: A.1 — system can produce a meaningful account of any material output; A.2 — stated objectives correspond to implemented objectives, verified by independent review; A.3 — system operates within documented boundaries in all tested conditions. All three must pass before deployment authorisation (Toolkit §1.3–§1.5).


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
**Coupling:** NOT STRUCTURALLY DECLARED (implicit signals present) ❌

**Implicit signals detected:**
- «gnate an individual responsible for compliance with this framework. This individual shall have»

**Interpretation:**  
These statements indicate recognition of responsibility or protection, but do not explicitly bind restrictions to protected human interests.

**Why this matters:**  
IMPLICIT coupling signals indicate intent, but do NOT provide enforceable structural guarantees. The obligations and protections are not formally bound, meaning protections can be removed without affecting obligations. This does not constitute partial compliance — the structural requirement is absent regardless of expressed intent.

**Practical meaning:**  
This document signals protective intent. However, an operator could modify specific obligations without being required to maintain the corresponding protections. The governance intent is present; the structural enforceability is not.

**Fix:**  
Explicitly pair each restriction with the human interest it protects. Ensure both carry equivalent normative force — neither can be weakened in isolation (LAIF v1.2 Principle 2; Toolkit §2 B.1).


#### Minimal Upgrade Path (No System Rewrite Required)
To achieve formal LAIF Coupling compliance without restructuring the entire document:

1. **Identify each restriction** — list every 'shall not' or operational constraint in the document.
2. **Identify the affected human interest** — for each restriction, state the specific human interest it protects (e.g. 'patient safety', 'worker's right to explanation').
3. **Explicitly declare the pairing** — add: 'Coupling between [restriction] and [human interest]: neither may be weakened without the other.'
4. **Ensure equivalent normative force** — both sides of the pair must use the same mandatory language ('shall') so neither can be downgraded in isolation.

*Note: implicit coupling signals already present (see above) — the governance intent is established. This upgrade is terminological and structural, not conceptual.*


#### Scores and Signal Breakdown
**Structural — 28/100** ███░░░░░░░

**Why:** Weak structural coverage (28/100): only 4 of 10 signals matched. Principal gaps: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).

**Signals detected:**
*Governance signals:*
- numbered sub-requirements (+8 pts)
- mandatory obligation language (shall) (+8 pts)
- operational mechanisms defined (+6 pts)
- review / monitoring mechanisms (+6 pts)

**Signals missing:**
- full lifecycle scope declared (missed 6 pts)
- risk stratification / proportionality (missed 7 pts)
- threshold gate conditions (all must pass simultaneously) (missed 15 pts)
- non-amendable constitutional hierarchy (missed 18 pts)
- self-application clause (Part Seven) (missed 12 pts)
- named decision instrument (Coherence Test / PDCA) (missed 14 pts)

**Dimension significance:** 25% weight. Governance architecture is the primary carrier of LAIF compliance. Without a non-amendable constitutional hierarchy, threshold gate conditions (Integrity Layer precondition), and named decision instruments (Coherence Test / PDCA), all other provisions are operationally revisable — the core failure LAIF is designed to prevent (LAIF v1.2 Parts One, Two, Seven).

**Terminology — 0/100** ░░░░░░░░░░

**Why:** No terminology signals present — none of the 7 expected signals matched. This dimension is absent from the document.

**Signals missing:**
- Coupling (missed 25 pts)
- Coherence Test (missed 20 pts)
- Integrity Layer (missed 20 pts)
- Structural Transparency (missed 10 pts)
- Structural Honesty (missed 10 pts)
- Structural Containment (missed 10 pts)
- Materially Affects Interests (missed 5 pts)

**Dimension significance:** 15% weight. Canonical LAIF terms are structurally load-bearing: 'Coupling' is not equivalent to 'alignment'; 'Integrity Layer' is not equivalent to 'integrity requirements'. Each term carries a specific enforcement obligation that informal equivalents do not. Lower weight because terminology alone is necessary but not sufficient for compliance (Toolkit §1).

**Conceptual Proximity — 41/100** ████░░░░░░

**Why:** Weak conceptual coverage (41/100): only 5 of 12 signals matched. Principal gaps: human rights / fundamental interests, human oversight, proportionality.

**Signals detected:**
*Human interest signals:*
- accountability (+8 pts)
- contestability / redress (+9 pts)
- fairness / labour / non-discrimination (+8 pts)
*Governance signals:*
- transparency (+8 pts)
*Structural signals:*
- explainability / interpretability (+8 pts)

**Signals missing:**
- human rights / fundamental interests (missed 10 pts)
- human oversight (missed 8 pts)
- proportionality (missed 8 pts)
- safety (missed 7 pts)
- reversibility / modifiability (missed 8 pts)
- risk governance (missed 8 pts)
- traceability / responsibility (missed 10 pts)

**Dimension significance:** 20% weight. Measures whether the document's governance intent is substantively aligned with LAIF, independent of vocabulary. High conceptual proximity with low structural or terminology scores signals a document expressing the right values through different vocabulary — adoption pathway is shorter. Low conceptual proximity indicates a more fundamental governance gap (LAIF v1.2 Part One).

**Auditability — 60/100** ██████░░░░

**Why:** Partial auditability coverage (60/100): 3 of 5 signals matched. Key gaps: multiple mandatory obligations (shall … shall), specific, measurable obligations.

**Signals detected:**
*Governance signals:*
- numbered traceable requirements (+20 pts)
- evidence / documentation requirements (+20 pts)
- review / monitoring mechanisms (+20 pts)

**Signals missing:**
- multiple mandatory obligations (shall … shall) (missed 20 pts)
- specific, measurable obligations (missed 20 pts)

**Dimension significance:** 20% weight. LAIF obligations must be independently verifiable. Numbered requirements, evidence documentation mandates, and monitoring mechanisms are the operational artefacts that allow a PDCA auditor to confirm compliance. Without them, compliance claims cannot be externally assessed (Toolkit §2 PDCA).

**Enforceability — 40/100** ████░░░░░░

**Why:** Weak enforceability coverage (40/100): only 2 of 5 signals matched. Principal gaps: named responsible parties, risk-proportionate thresholds, enforcement consequences / penalties.

**Signals detected:**
*Governance signals:*
- mandatory language (shall) (+20 pts)
*Structural signals:*
- non-discretionary operational mandates (+20 pts)

**Signals missing:**
- named responsible parties (missed 20 pts)
- risk-proportionate thresholds (missed 20 pts)
- enforcement consequences / penalties (missed 20 pts)

**Dimension significance:** 20% weight. A governance standard that cannot be enforced is an aspiration, not a constraint. Mandatory language ('shall'), named responsible parties, and enforcement consequences are the minimum conditions for operational enforceability. Voluntary frameworks characteristically score low here regardless of conceptual quality (LAIF v1.2 Part Three).

**Overall Readiness — 35/100** ████░░░░░░

**Why:** Weighted sum of the five dimensions above — Structural×0.25 + Terminology×0.15 + Conceptual Proximity×0.20 + Auditability×0.20 + Enforceability×0.20. A document achieves overall readiness by addressing governance architecture, canonical terminology, substantive intent, verifiability, and enforceability simultaneously. Weakness in any single dimension constrains the overall score proportionally.


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
**🔴 [HIGH] Coupling not structurally declared — no restriction paired with a human interest**
- *Evidence:* The canonical term 'Coupling' does not appear in the document.
- *Impact:* Every governance restriction can be weakened in isolation without triggering a corresponding protection failure. Q1 (Coupling) = automatic Coherence Test failure. Integrity Layer precondition cannot be satisfied without Coupling (LAIF v1.2 Principle 2).
- *Recommended action:* Declare structural Coupling for each governance restriction: name the specific human interest at stake and pair it with a protection of equivalent normative force (Toolkit §2 B.1).

**🔴 [HIGH] Formal compliance gate not satisfied — 8 required construct(s) absent**
- *Evidence:* Missing: Coupling, Integrity Layer, Coherence Test, PART ONE / Foundational Principles and 4 others.
- *Impact:* Formal LAIF compliance is binary. Missing any single required construct = FAIL regardless of overall readiness score. These constructs are structurally necessary — they cannot be satisfied by partial presence.
- *Recommended action:* Add the missing constructs substantively — each must be meaningfully implemented, not merely cited. Implement in this priority order: Coupling → Coherence Test → Integrity Layer → constitutional hierarchy → self-application clause.

**🟡 [MEDIUM] Low Structural governance architecture score (28/100)**
- *Evidence:* Score 28/100. Key missed signals: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
- *Impact:* Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
- *Recommended action:* Target the missed signals for this dimension: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). The weight rationale for this dimension is detailed in the Scores and Signal Breakdown section above.



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

**5. Problem:** Declare Coupling between each employment AI restriction and the specific worker interest it protects. Rewrite:… — not addressed in this document.
   **Why it matters:** In the Employment / Workforce AI deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Declare Coupling between each employment AI restriction and the specific worker interest it protects. Rewrite: 'alignment between obligations imposed on workers and the protections those obligations are intended to serve' → 'Coupling between obligations imposed on workers and the protections afforded to their employment status and income' (Toolkit §2 B.1; LAIF v1.2 Principle 2).

**6. Problem:** Apply Q2 Consistency: governance logic must produce just outcomes across all scales — not addressed in this document.
   **Why it matters:** In the Employment / Workforce AI deployment context, this governance gap exposes specific human interests that materially affect persons subject to the AI system's outputs. Each gap represents a Coupling declaration that is absent or insufficient for this sector (Toolkit §1.2 — Materially Affects Interests; §7.5 — PDCA tiering).
   **Concrete fix:** Apply Q2 Consistency: governance logic must produce just outcomes across all scales — from individual worker to collective bargaining unit. Rewrite: 'AI performance assessment applies to all employees' → 'AI performance assessment applies consistently across all roles, scales, and worker categories, with equivalent review rights at each scale' (LAIF v1.2 Principle 5).


---

## Cross-Document Findings

### Citable vs Illustrative Corpus Comparison
Averages by evidence tier. Convergence between tiers indicates the core finding is not an artefact of paraphrasing; divergence localises where condensation altered the signal.

| Evidence tier                         | n | Str | Ter | Con | Aud | Enf | OVR | Formal FAIL |
| ------------------------------------- | - | --- | --- | --- | --- | --- | --- | ----------- |
| OFFICIAL_EXCERPT (citable)            | 4 | 30  | 0   | 53  | 55  | 40  | 37  | 4/4         |
| REPRESENTATIVE_EXCERPT (illustrative) | 6 | 30  | 0   | 49  | 47  | 43  | 35  | 6/6         |

- **Terminology absence confirmed on official text:** every citable document scores 0/100 on LAIF canonical terminology. The terminology gap observed on paraphrased excerpts is a property of the source instruments themselves, not of the paraphrasing.
- **Official full text scores higher on conceptual proximity (+4 avg):** verbatim instruments carry more of their own governance substance than condensed paraphrases preserve — meaning the illustrative corpus, if anything, *understated* how close real frameworks already are to LAIF's conceptual content.
- **Official instruments are more auditable than their paraphrases suggested (+8 avg):** real instruments carry numbered obligations, evidence requirements, and review mechanisms that condensation strips out.
- **Heuristic limitation surfaced by official text (NHS England DTAC v2.0 (February 2026)):** the sector gaming detector flags form/questionnaire-style official instruments because their governance content lives in assessed criteria, not declaratory prose. On verified official instruments the flag must be read as a format-mismatch diagnostic, not a gaming attribution (see the per-document interpretation caveat).


### Score Comparison
| Document                               | Str | Ter | Con | Aud | Enf | OVR | Sector Alignment |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------- |
| US Executive Order 14110 — §2 Principl | 43  | 0   | 57  | 60  | 40  | 42  | 20%              |
| OECD Recommendation on AI (OECD/LEGAL/ | 26  | 0   | 84  | 60  | 20  | 39  | 40%              |
| NIST AI RMF 1.0 (NIST AI 100-1) — GOVE | 41  | 0   | 47  | 60  | 80  | 48  | 80%              |
| NHS England DTAC v2.0 (February 2026)  | 12  | 0   | 24  | 40  | 20  | 20  | 80%              |
| EU AI Act — Art. 9, 13 & 14            | 41  | 0   | 49  | 60  | 60  | 44  | 60%              |
| NIST AI RMF — Govern & Map Functions   | 26  | 0   | 39  | 60  | 20  | 30  | 40%              |
| OECD AI Principles (2019, rev. 2024)   | 12  | 0   | 76  | 0   | 20  | 22  | 60%              |
| US Executive Order 14110 — §4 Safety & | 35  | 0   | 66  | 60  | 80  | 50  | 100%             |
| NHS England — AI in Clinical Decision  | 35  | 0   | 23  | 40  | 40  | 29  | 80%              |
| TUC/CIPD — Framework for Fair AI in Em | 28  | 0   | 41  | 60  | 40  | 35  | 80%              |


### Deployment Risk Tier Summary
| Document                               | Risk Tier | Overall | Compliance | Provenance             |
| -------------------------------------- | --------- | ------- | ---------- | ---------------------- |
| OECD Recommendation on AI (OECD/LEGAL/ | CRITICAL  | 39/100  | FAIL       | OFFICIAL_EXCERPT       |
| NHS England DTAC v2.0 (February 2026)  | CRITICAL  | 20/100  | FAIL       | OFFICIAL_EXCERPT       |
| NIST AI RMF — Govern & Map Functions   | CRITICAL  | 30/100  | FAIL       | REPRESENTATIVE_EXCERPT |
| OECD AI Principles (2019, rev. 2024)   | CRITICAL  | 22/100  | FAIL       | REPRESENTATIVE_EXCERPT |
| NHS England — AI in Clinical Decision  | CRITICAL  | 29/100  | FAIL       | REPRESENTATIVE_EXCERPT |
| TUC/CIPD — Framework for Fair AI in Em | CRITICAL  | 35/100  | FAIL       | REPRESENTATIVE_EXCERPT |
| US Executive Order 14110 — §2 Principl | HIGH      | 42/100  | FAIL       | OFFICIAL_EXCERPT       |
| NIST AI RMF 1.0 (NIST AI 100-1) — GOVE | HIGH      | 48/100  | FAIL       | OFFICIAL_EXCERPT       |
| EU AI Act — Art. 9, 13 & 14            | HIGH      | 44/100  | FAIL       | REPRESENTATIVE_EXCERPT |
| US Executive Order 14110 — §4 Safety & | HIGH      | 50/100  | FAIL       | REPRESENTATIVE_EXCERPT |

**Risk tier derivation** (matches `_deployment_risk_tier()`, Toolkit §7): LOW = STRONG PASS (all Integrity Layer and Coherence Test conditions met); otherwise MODERATE = overall ≥70; HIGH = overall 40–69; CRITICAL = overall <40.

- High conceptual proximity (≥60): OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (official text), OECD AI Principles (2019, rev. 2024), US Executive Order 14110 — §4 Safety & §7 Workers — LAIF-like intent expressed through own vocabulary.
- Paraphrase violations: US Executive Order 14110 — §4 Safety & §7 Workers — forbidden substitution of LAIF canonical terms.
- Low enforceability (<40): OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (official text), NHS England DTAC v2.0 (February 2026) — Introduction & C1 Clinical Safety (official text), NIST AI RMF — Govern & Map Functions, OECD AI Principles (2019, rev. 2024) — voluntary/declaratory frameworks without binding mandates.

## Common Failure Modes
- **structural — constitutional hierarchy not declared** — 10/10 documents
- **terminological — no canonical LAIF terms present** — 10/10 documents
- **enforceability — insufficient mandatory operational requirements** — 4/10 documents
- **conceptual — LAIF-like concepts insufficiently expressed** — 3/10 documents
- **auditability — obligations not checkable or traceable** — 1/10 documents
- **terminological (paraphrase) — forbidden substitutions detected** — 1/10 documents

The universal failure mode is terminological: no external framework uses LAIF canonical terms. However, the absence of structural Coupling is the more consequential gap — without it, restrictions are not structurally paired with proportionate protections, and neither can be defended as structurally required by the other (LAIF v1.2 Principle 2).

## LAIF Deployment Implications
1. **LAIF is additive, not competitive.** Existing frameworks address the right governance dimensions. LAIF provides the structural enforcement layer they lack — canonical terms with load-bearing meaning, Coupling requirements, and the Coherence Test as a named decision instrument.

2. **Conceptual proximity enables adoption.** Documents scoring ≥60 on conceptual proximity already express the underlying values. Adoption pathway: introduce LAIF canonical terminology and add structural Coupling declarations to existing provisions.

3. **Paraphrase violations are actionable.** Where 'alignment', 'connection', or 'linkage' appear as structural governance terms, the minimal fix is a rewrite substituting 'Coupling' and adding the paired protection — not a full structural redesign.

4. **Sector risk alignment measures deployment readiness.** A document with high conceptual proximity but low sector risk alignment may not address the specific materially-affected interests in the target deployment context.

5. **Scoring traceability enables targeted remediation.** Per-signal breakdowns show precisely which structural elements are missing, enabling prioritised fixes rather than wholesale document rewrites.

6. **Evidence tier determines what may be claimed.** Findings from the official corpus may be presented externally as assessments of the named instruments (within the stated excerpt scope); findings from the representative corpus may only characterise framework styles. Conflating the two tiers would itself fail LAIF A.2 Structural Honesty — the reporting layer is held to the same standard it audits.

## Recommended Next Development Steps
1. **Complete the official corpus with the EU AI Act:** the EU AI Act entry is still a REPRESENTATIVE_EXCERPT — its findings are illustrative only. Ingest the Official Journal text of Regulation (EU) 2024/1689 (Articles 9, 13, 14 at minimum) into docs/supporting/ and add a hash-pinned OFFICIAL_EXCERPT entry, making the EU baseline citable like the other four instruments.

2. **Article-level LAIF–EU AI Act mapping:** Map LAIF Provisions to EU AI Act articles to formalise the adoption pathway for the EU regulatory context.

3. **LAIF–NIST RMF function mapping:** Map Coherence Test questions to NIST RMF functions (Govern, Map, Measure, Manage) to enable LAIF adoption within existing US governance infrastructure. The citable NIST AI 100-1 assessment in this report identifies the precise GOVERN/MAP subcategories where Coupling declarations would attach.

4. **Sector-specific PDCA templates:** Produce PDCA-Full templates pre-populated with sector-appropriate Coupling declarations, evidence artefact checklists, and Coherence Test documentation guidance. The DTAC v2.0 assessment shows the natural insertion point for clinical AI: DTAC's C1 clinical-safety gate already operates as a threshold precondition — a Coupling declaration per criterion would upgrade it toward Integrity Layer semantics without restructuring the form.

5. **Score threshold calibration:** As more documents are assessed, calibrate remediation effort thresholds against actual adoption timelines.

6. **Keep provenance enforcement in the pre-commit gate:** run `python3 test_provenance.py` alongside validate.py and the adversarial suite before every release, so no OFFICIAL_EXCERPT claim can silently decay as source files evolve.

---
*LAIF v1.2 · Compliance Toolkit v1.1 · July 2026 · Governance Audit Series*
*Generated by `test_real_world.py` — validate.py enforcement unchanged · provenance verified by `test_provenance.py`*