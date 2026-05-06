# Evidence Trace — NIST AI 100-1 (AI Risk Management Framework 1.0)

**Assessment:** LAIF Full Corpus Assessment — Assessment 3  
**Raw source:** `docs/verified/raw/5f667a6f-NIST.AI.1001.md`  
**Assessment output:** `reports/laif_full_assessment.md` §§ Assessment 3  
**Extraction boundary:** Full document  
**Transformation:** NORMALISED_FORMATTING_ONLY

---

## Purpose

This file documents which sections of the raw source were used as primary evidence for each LAIF v1.2 assessment finding. It is an evidence trail for reproducibility — not an excerpt of the source text. To verify any finding, read the raw source at the section listed.

---

## Section A — Integrity Layer

### A.1 Structural Transparency — STRONG

**Primary evidence sections:**
- GOVERN 1.1 — Policies, processes, procedures, and practices for AI risk management
- GOVERN 1.7 — Organizational roles and responsibilities (including documentation requirements)
- GOVERN 6.1 — Policies for transparency and explainability
- MAP 5.1 — AI risks to individuals and groups documented and quantified
- MEASURE 2.5 — AI system performance (including explainability, interpretability)

**Finding basis:** The GOVERN and MEASURE functions explicitly address transparency documentation requirements. GOVERN 6.1 directly mandates transparency and explainability as documented organisational commitments. This maps strongly to LAIF §2.1 Structural Transparency.

---

### A.2 Structural Honesty — STRONG

**Primary evidence sections:**
- MEASURE 2.5 — Systematic testing of AI performance including adversarial conditions
- MEASURE 2.6 — Adversarial testing (red-teaming requirements)
- GOVERN 1.4 — Organisational AI risk tolerance documented
- MAP 1.6 — AI risk documentation (including stated vs. implemented objectives)

**Finding basis:** MEASURE 2.5 and 2.6 directly address adversarial performance consistency — the core of LAIF §2.2 Structural Honesty. The requirement that AI systems perform consistently under testing conditions maps to the correspondence between stated and implemented objectives. Assessment: STRONG.

---

### A.3 Structural Containment — MODERATE

**Primary evidence sections:**
- GOVERN 1.2 — Roles and responsibilities for operational boundaries
- MANAGE 1.3 — Deployment scope and operational boundaries
- MANAGE 2.2 — Ongoing monitoring obligations
- MANAGE 4.1 — AI response and incident management

**Finding basis:** The MANAGE function addresses operational boundary definition and monitoring. However, the AI RMF does not operationalise interrupt mechanisms or agentic AI containment as specified in LAIF §2.3. Assessment: MODERATE — strong on boundary documentation, limited on technical interrupt requirements.

---

## Section B — Coherence Test

### Q1 Coupling — Q1a EXPLICIT / Q1b NONE

**Q1a (EXPLICIT) basis:**
- GOVERN 1.1-1.7 — Each governance subcategory pairs an organisational obligation with a documented risk or harm
- MAP function — coupling between risk identification (specific harms) and governance responses
- MEASURE 2.5 — Coupling between performance requirement and specific failure modes

The AI RMF's subcategory structure explicitly pairs each organisational practice with the class of AI risk it addresses. Q1a = EXPLICIT.

**Q1b (NONE) basis:**
- AI RMF Preface/Introduction — explicitly describes the framework as voluntary
- GOVERN 1.1 — "AI organizations are encouraged to..."
- No enforcement mechanism exists in the document or by reference

The voluntary design is by deliberate architecture, not constitutional necessity (contrast EO 14110 §13(c)). The AI RMF explicitly states it does not create legal obligations. No affected person can enforce any AI RMF requirement. Q1b = NONE.

**Q1b NONE type distinction:** EO 14110's NONE arises from an explicit enforcement bar in a document that otherwise creates obligations. The AI RMF's NONE arises from voluntary design — the framework never creates obligations in the first place. Both produce Q1b = NONE, but for different architectural reasons.

---

### Q2 Consistency — PASS

**Primary evidence sections:**
- AI RMF Scope and Applicability sections (framework applies to all AI across sectors and scales)
- GOVERN 6.2 — Considerations for AI deployment across different organisational contexts

**Finding basis:** The AI RMF applies the same governance logic across all scales, sectors, and actor types. Small and large organisations, government and private sector, are all addressed by the same subcategory structure. The framework does not exempt any actor class. Q2 = PASS.

---

### Q3 Reversibility — PASS

**Primary evidence sections:**
- AI RMF Preface — explicit statement that the framework is a living document
- Version identification: AI RMF 1.0 (January 2023), with subsequent playbooks and updates referenced

**Finding basis:** The AI RMF explicitly commits to iterative revision. It is a living document with ongoing update mechanisms. No provision creates structural irreversibility. Q3 = PASS.

---

## New Dimensions (Refined Model v1.1)

### Governance Durability — ADAPTIVE

**Evidence:** Living document design; AI RMF 1.0 followed by Playbooks, Generative AI Profile (AI 600-1), ongoing NIST AI programme. Institutional commitment to revision demonstrated through follow-on publications.

### Reflexivity — NONE

**Evidence:** The AI RMF does not apply its governance requirements to NIST itself as an AI governance actor. NIST is positioned as the framework author, not a subject of the framework's own governance logic. The framework's scope is AI deployers and developers, not standard-setting bodies.

---

## Schedule B.2 Cross-Reference (LAIF)

LAIF Schedule B.2 explicitly maps LAIF to NIST AI RMF functions. The evidence trace confirms alignment:

| NIST AI RMF Function | LAIF Mapping | Evidence Sections |
|---|---|---|
| Govern | Obligation Layer / PDCA sign-off | GOVERN 1.1-1.7 |
| Map | Coupling documentation | MAP 1.1-5.2 |
| Measure | Integrity Layer verification | MEASURE 2.5, 2.6 |
| Manage | §9.5 monitoring + Part 7 | MANAGE 1.3, 2.2, 4.1 |

---

*Evidence trace generated: May 2026. All findings sourced exclusively from the raw source file listed above.*
