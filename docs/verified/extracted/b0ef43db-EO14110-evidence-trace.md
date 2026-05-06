# Evidence Trace — Executive Order 14110

**Assessment:** LAIF Full Corpus Assessment — Assessment 2  
**Raw source:** `docs/verified/raw/b0ef43db-202324283.md`  
**Assessment output:** `reports/laif_full_assessment.md` §§ Assessment 2  
**Extraction boundary:** Full document  
**Transformation:** NORMALISED_FORMATTING_ONLY

---

## Purpose

This file documents which sections of the raw source were used as primary evidence for each LAIF v1.2 assessment finding. It is an evidence trail for reproducibility — not an excerpt of the source text. To verify any finding, read the raw source at the section listed.

---

## Section A — Integrity Layer

### A.1 Structural Transparency — WEAK

**Primary evidence sections:**
- §4.1(a)(i)(C) — NIST initiative on guidance and benchmarks for evaluating and auditing AI capabilities
- §4.5 — Synthetic content labelling and watermarking
- §10.1(b)(viii) — OMB guidance direction (recommendations on external testing, discriminatory-output safeguards, watermarking, risk-management practices, independent evaluation, documentation)
- §10.1(b)(v) — Agencies to identify AI uses presumed to impact rights or safety

**Finding basis:** The order directs agencies to develop transparency infrastructure but does not operationalise transparency obligations. No provision creates a mechanism by which an affected person can obtain an account of an AI system's outputs (LAIF §2.1). Assessment: WEAK — institutional mandate to build transparency, not transparency itself.

---

### A.2 Structural Honesty — MODERATE

**Primary evidence sections:**
- §4.2(a)(i)(C) — Companies to report results of red-team testing and safety measures
- §4.6 — Dual-use foundation models with widely available weights; consultation on risks

**Finding basis:** The red-team reporting requirement (§4.2) maps to LAIF §2.2's adversarial consistency requirement. This is the strongest Structural Honesty proxy in the order. Correspondence between stated and implemented objectives is not directly required. Assessment: MODERATE.

---

### A.3 Structural Containment — WEAK

**Primary evidence sections:**
- §3(k) — Definition of "dual-use foundation model" (includes capability to permit evasion of human control through deception/obfuscation)
- §2(a) — Safety and security goals (robust, reliable, repeatable, standardised evaluations)

**Finding basis:** Containment is conceptually referenced but not operationalised. No provision establishes scope limitation, action logging, or interrupt mechanisms as defined in LAIF §2.3. Assessment: WEAK.

---

## Section B — Coherence Test

### Q1 Coupling — Q1a EXPLICIT / Q1b NONE

**Q1a (EXPLICIT) basis:**
- §1 — Purpose declaration: names safety, security, equity, civil rights, privacy, consumer protection, workers' rights, innovation, American leadership as the protected interests
- §4 — Each safety directive pairs a restriction (reporting, evaluation, disclosure) with a named risk (unsafe AI development, dual-use capabilities, discriminatory outputs)
- §7 — Workers section pairs AI-related obligations with specific worker interests

**Q1b (NONE) basis — critical provision:**
- §13(c) — "This order is not intended to, and does not, create any right or benefit, substantive or procedural, enforceable at law or in equity by any party against the United States."

This provision is dispositive for Q1b. It explicitly bars any affected person from enforcing any right or benefit created by the order. No external enforcement mechanism exists. Q1b = NONE.

**LAIF §2.4 reference:** Equivalent normative force requires enforceable rights accessible to affected persons. §13(c) is a direct and explicit bar. The structural pairing is present (Q1a EXPLICIT); the enforcement force is explicitly negated (Q1b NONE).

---

### Q2 Consistency — PARTIAL PASS

**Primary evidence sections:**
- §2(a) — Equal treatment of comparable AI risks across government and private sector
- §10 — Scope limited to federal agencies and their AI use

**Finding basis:** The governance logic applies primarily to federal agency AI use and large-model developers. At smaller scales (small developers, state-level AI), the obligations do not apply. The consistency argument is PARTIAL — the logic holds within scope but the scope is a carve-out by actor size and sector.

---

### Q3 Reversibility — CONDITIONAL PASS

**Primary evidence sections:**
- §1 (purpose structure) — order as executive action, not statute
- Revocation: Presidential Memorandum, 20 January 2025

**Finding basis:** Executive orders are inherently reversible by subsequent executive action. The reversibility is structurally unconstrained — no future actor is prevented from reverting. The conditional qualification reflects that the governance infrastructure built under the order (agency AI policies, NIST frameworks) may be harder to reverse than the order itself.

---

## New Dimensions (Refined Model v1.1)

### Governance Durability — FRAGILE

**Evidence:** Revoked 20 January 2025 — approximately 15 months after signing. Executive order architecture provides no institutional durability beyond the signing administration.

### Reflexivity — PARTIAL

**Evidence:** §§10–11 apply AI governance requirements to federal agencies using AI. The order acknowledges government actors as subjects of AI governance. However, the governance logic is not fully applied to the President or EOP as AI governance actors.

---

*Evidence trace generated: May 2026. All findings sourced exclusively from the raw source file listed above.*
