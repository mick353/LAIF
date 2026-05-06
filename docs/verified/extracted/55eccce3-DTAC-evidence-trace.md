# Evidence Trace — Digital Technology Assessment Criteria v2.0 (DTAC)

**Assessment:** LAIF Full Corpus Assessment — Assessment 4  
**Raw source:** `docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md`  
**Assessment output:** `reports/laif_full_assessment.md` §§ Assessment 4  
**Extraction boundary:** Full document  
**Transformation:** NORMALISED_FORMATTING_ONLY

---

## Purpose

This file documents which sections of the raw source were used as primary evidence for each LAIF v1.2 assessment finding. It is an evidence trail for reproducibility — not an excerpt of the source text. To verify any finding, read the raw source at the section listed.

---

## DTAC Structure

DTAC v2.0 is organised into assessment categories. The primary categories relevant to the LAIF assessment:

- **Category C1** — Clinical Safety
- **Category C2** — Data Protection (UK GDPR compliance)
- **Category C3** — Technical Assurance
- **Category C4** — Cyber Security / DSPT
- **Category D1** — Accessibility and Usability

---

## Section A — Integrity Layer

### A.1 Structural Transparency — MODERATE

**Primary evidence sections:**
- Category C2 — Data Protection requirements (transparency to data subjects under UK GDPR)
- Category C3 — Technical assurance documentation requirements
- Category C1 — Clinical safety case (transparency of clinical risk assessment)

**Finding basis:** DTAC requires documented transparency in specific domains (data protection, clinical safety, technical assurance). This covers a meaningful subset of LAIF §2.1 Structural Transparency, but does not create a general mechanism for any affected person to obtain an account of AI system outputs. Assessment: MODERATE.

---

### A.2 Structural Honesty — STRONG

**Primary evidence sections:**
- Category C1 — Clinical Safety (NHS DCB 0129 clinical safety case requirement)
- Category C1 — Safety case documentation (requires stated clinical purpose to correspond to implemented function)
- Category C3 — Technical assurance (performance claims must be evidenced)

**Finding basis:** The clinical safety case requirement (C1) directly requires that the stated clinical purpose of the technology corresponds to its documented and tested behaviour. This maps to LAIF §2.2 Structural Honesty's requirement that stated objectives correspond to actual implemented objectives. Assessment: STRONG.

---

### A.3 Structural Containment — MODERATE

**Primary evidence sections:**
- Category C1 — Clinical Safety (scope limitations and hazard identification)
- Category C3 — Technical assurance (system boundary documentation)
- Category C4 — Cyber Security (DSPT requirements, access controls)

**Finding basis:** DTAC requires clinical scope documentation and hazard boundary identification (C1), system boundaries in technical assurance (C3), and security boundary controls (C4). These map to elements of LAIF §2.3 Structural Containment. The framework does not address agentic AI or specific interrupt mechanisms. Assessment: MODERATE.

---

## Section B — Coherence Test

### Q1 Coupling — Q1a EXPLICIT (C1-C4) / IMPLICIT (D1) / Q1b HARD

**Q1a basis for C1-C4 (EXPLICIT):**
- Category C1 — Clinical Safety: restriction (clinical safety case) paired with named human interest (patient safety under NHS DCB 0129)
- Category C2 — Data Protection: restriction (UK GDPR compliance) paired with named human interest (data subject rights)
- Category C3 — Technical Assurance: restriction (technical evidence) paired with named human interest (product reliability for clinical users)
- Category C4 — Cyber Security: restriction (DSPT compliance) paired with named human interest (data security)

**Q1a basis for D1 (IMPLICIT):**
- Category D1 — Accessibility: advisory guidance on usability; named human interest (accessibility for disabled users) is identifiable but the restriction is advisory only, not mandated
- The coupling is structurally visible (the interest is named) but the restriction does not carry equivalent normative force even within the DTAC instrument

**Q1b (HARD) basis:**
- DTAC procurement gate: suppliers must achieve DTAC approval before listing on NHS England frameworks
- Non-compliance excludes suppliers from the NHS England market
- This creates market-exclusion consequences that are external, automatic, and enforceable without any affected person needing to assert a right

This is the only instrument in the corpus that produces Q1b = HARD. The enforcement mechanism is the procurement gate itself — it does not require litigation or regulatory action; it is structurally embedded in market access.

**LAIF §2.4 reference:** HARD enforcement satisfies the equivalent normative force requirement because the market-exclusion consequence is accessible to the same class of affected persons (patients, clinical users, NHS) through the procurement process, and the mechanism is as effective as the obligation it enforces.

---

### Q2 Consistency — CONDITIONAL PASS

**Primary evidence sections:**
- Category D1 — Accessibility: advisory-only status despite Equalities Act 2010 obligations
- Category C1 — Clinical Safety: HARD enforcement

**Finding basis:** The inconsistency is within DTAC itself. C1-C4 carry HARD enforcement; D1 (accessibility) carries advisory guidance only, despite the Equalities Act creating an equivalent legal obligation. If the coupling logic applied consistently across all categories, D1 would carry the same enforcement force as C1. The conditional qualification reflects this internal inconsistency. The external consistency (same framework across all NHS England suppliers) is clean.

---

### Q3 Reversibility — PASS

**Primary evidence sections:**
- DTAC Form version history (Form 2.0 supersedes earlier versions)
- NHS England procurement process (framework contracts are time-limited and renewable)

**Finding basis:** DTAC is a procurement standard updated through NHS England's standard governance process. Future actors can amend, revise, or replace DTAC through the same procurement governance channels that produced it. No provision creates structural irreversibility. Q3 = PASS.

---

## New Dimensions (Refined Model v1.1)

### Governance Durability — BOUNDED

**Evidence:** DTAC is operative only within the NHS England procurement process. Its scope is deliberately limited to NHS England digital technology suppliers. The durability within scope is reasonable (procurement standards are routinely revised but maintained); the instrument has no applicability beyond NHS England. BOUNDED reflects this design as a domain-specific enforcement gate.

### Reflexivity — NONE

**Evidence:** DTAC does not apply its own governance requirements to NHS England as a procurer or governance actor. NHS England uses DTAC to assess suppliers but does not subject its own AI procurement decisions to DTAC-equivalent analysis. The framework scope is explicitly the supplier, not the procuring organisation.

---

## Structural Gap: Discrimination and Bias Testing

**Evidence sections:** Category D1 — Accessibility and Usability (advisory only)

The assessment identified a structural gap: DTAC is the only instrument in the corpus with HARD enforcement yet does not require discrimination or bias testing as a mandatory assessment criterion. C1-C4 have no provision requiring assessment of whether the digital technology produces discriminatory outputs. D1 addresses accessibility but is advisory only.

This is the inverse of the corpus-wide pattern: the instruments with the strongest enforcement (DTAC) have the weakest discrimination testing requirements; the instruments with strong discrimination guidance (NIST AI RMF, OECD) have no enforcement.

---

*Evidence trace generated: May 2026. All findings sourced exclusively from the raw source file listed above.*
