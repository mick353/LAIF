# AI Governance Structural Integrity Assessment
*How far do these instruments' protections actually reach the people they govern — and what would it take to close the distance?*  
**Report date:** July 2026  
**Assessment model:** Law-Aligned Intelligence Framework (LAIF) v1.2 · Compliance Toolkit v1.1 — the model is the measuring lens, not the subject of the findings; see Method Summary.  
**Report architecture:** Governance Repair Assessment public template — Phase 3V  
**Validator boundary:** validate.py enforcement remains unchanged; this report renders existing assessment results only.  


## Report Scope and Boundary

### Result Boundary / How to Read This Report
This public report is a governance repair and systemic failure-pathway diagnostic for institutional review.
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.
External-framework mode assesses governance repair adequacy, operational closure, evidence sufficiency, accountability closure, lifecycle control, residual-risk closure, implementation readiness, and failure-pathway risk.
This report does not determine legal validity, enforceability, safety status, procurement eligibility, clinical authority, HR authority, education authority, or regulatory acceptance.
Not LAIF-native is certification-channel wording only; it is not a legal-validity or governance-validity determination.
Evidence traces preserve exact-source and reviewer-confirmation boundaries; trace presence does not prove implementation.
Score bands summarize LAIF-model readiness signals and are not determinations of compliance; high scores cannot override formal LAIF-native failure.
Formal fail boundary: high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.


### Evidence Basis and Citability
Every document carries a machine-verified provenance classification; findings inherit the citability of the text they were computed from (enforced by `test_provenance.py`).

| Document                                             | Provenance             | Citable | Evidence basis                                               |
| ---------------------------------------------------- | ---------------------- | ------- | ------------------------------------------------------------ |
| US Executive Order 14110 — §2 Principles, §6 Workers | OFFICIAL_EXCERPT       | Yes     | docs/supporting/b0ef43db-202324283.md                        |
| OECD Recommendation on AI (OECD/LEGAL/0449) — Sectio | OFFICIAL_EXCERPT       | Yes     | docs/supporting/51a29205-OECD_Legal_Instruments.md           |
| NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Funct | OFFICIAL_EXCERPT       | Yes     | docs/supporting/5f667a6f-NIST.AI.1001.md                     |
| NHS England DTAC v2.0 (February 2026) — Introduction | OFFICIAL_EXCERPT       | Yes     | docs/supporting/55eccce3-DTAC_Form_2.0_February_2026.md      |
| EU AI Act — Art. 9, 13 & 14                          | REPRESENTATIVE_EXCERPT | No      | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A |
| NIST AI RMF — Govern & Map Functions                 | REPRESENTATIVE_EXCERPT | No      | https://airc.nist.gov/RMF                                    |
| OECD AI Principles (2019, rev. 2024)                 | REPRESENTATIVE_EXCERPT | No      | https://oecd.ai/en/ai-principles                             |
| US Executive Order 14110 — §4 Safety & §7 Workers    | REPRESENTATIVE_EXCERPT | No      | https://www.federalregister.gov/documents/2023/11/01/2023-24 |
| NHS England — AI in Clinical Decision Support (Polic | REPRESENTATIVE_EXCERPT | No      | illustrative document                                        |
| TUC/CIPD — Framework for Fair AI in Employment Decis | REPRESENTATIVE_EXCERPT | No      | illustrative document                                        |

**OFFICIAL_EXCERPT** — text extracted verbatim at run time from the committed source file via unique start/end markers and pinned by SHA-256 (`official_documents.py`); any drift fails the run. Findings may be cited as statements about the named instrument within the declared excerpt scope. **REPRESENTATIVE_EXCERPT** — condensed paraphrase; findings characterise the framework style only and must not be presented as assessments of the official source instrument.


### Functional Alignment Layer (Substance Independent of Vocabulary)
Beyond the layers above, each core construct (Coupling, Integrity Layer, Consistency, Reversibility, Self-Application) is assessed for its *substance* in the document's own vocabulary — DECLARED (LAIF-native form), FUNCTIONAL (≥2 independent signal families including the construct's defining family), PARTIAL, or ABSENT. Grounded in LAIF v1.2 Part Eight (equivalent structural diligence through alternative documented means) and the Regulatory Integration Guide's SATISFIES/EXTENDS methodology. A document is never penalised for expressing LAIF's requirements in its own words, and never credited for using LAIF's words without the substance. Overall alignment verdicts: LAIF-NATIVE (qualified by structural depth) / FUNCTIONALLY ALIGNED / PARTIALLY ALIGNED / STRUCTURALLY UNALIGNED.


### Fair-Reading Bounds
1. A LAIF-native FAIL measures distance from LAIF's deliberately stricter standard, not instrument quality; it must never be quoted as a judgement of the instrument against its own objectives.
2. Official-corpus findings hold within each document's declared excerpt scope only.
3. Signals are lexical, not interpretive; per-signal traceability is the compensating control.
4. Form/questionnaire-style instruments are undercounted by prose rubrics; affected scorecards carry an interpretation caveat.
5. Cross-document averages characterise this corpus, not all AI governance.
6. Raw overall scores compress: part of the 100-point scale is reserved for LAIF-branded documents and lexical detection is conservative — a substance-perfect external document scores in the mid-50s on this instrument, so mid-range raw scores denote strength, not failure; each scorecard carries a calibrated position against the achievable ceiling.


## Executive Brief
- **Total documents assessed:** 10 (10 external instruments assessed as governance repair diagnostics, not LAIF-native certification)
- **Average overall readiness:** 39/100
- **Average conceptual proximity:** 51/100
- **Average sector alignment:** 62/100
- **Citable subset (OFFICIAL_EXCERPT, verbatim hash-pinned):** 4/10 documents; 4/4 not LAIF-native; average conceptual proximity 53/100. These findings may be stated of the named source instruments within excerpt scope.
- **Functional alignment distribution:** PARTIALLY ALIGNED (8); STRUCTURALLY UNALIGNED (2)
- **Average calibrated position (external instruments):** 48% of the 81.5-point ceiling achievable without LAIF-native branding — raw scores compress by design and must not be read as percentage grades.
- **Evidence trace summary:** 188 traces; 188 exact/deterministic; 0 reviewer-confirmation fallback.
- **Remediation patch summary:** 120 structured patches across assessed documents.
- **Top governance-force patterns:** mandate (3); consequence (2); escalation (1)
- **Certification channel:** no document in this corpus claims or seeks LAIF-native certification, so the certification gate is not a finding about these documents; construct coverage remains available in each Technical Appendix.
- **Boundary note:** diagnostic findings require reviewer confirmation and cannot override formal LAIF-native failure.


## Method Summary

### Method and Scoring Model
Assessment layers preserved: Formal LAIF-native certification gate; Dimensional scoring model; Structural depth / adversarial hardening; Validation boundary.
The renderer presents deterministic rubric outputs that already exist in each assessment result; it does not change scoring weights, score calculations, formal compliance calculation, validation, certification gates, sector metadata, evidence traces, remediation patches, or calibration metadata.
The report uses controlled public wording, suppresses raw regex disclosure, avoids keyword-stuffing recipes, and preserves legal-authority boundaries.
No legal determination is made; no source is certified through this public template unless the separate LAIF-native certification gate passes.


## Cross-Document Dashboard

### Score distribution / deterministic rubric comparison
| Document                                                         | Mode               | Alignment              | Overall score / band               | Sector profile         | Evidence traces | Patches | Cautions |
| ---------------------------------------------------------------- | ------------------ | ---------------------- | ---------------------------------- | ---------------------- | --------------- | ------- | -------- |
| US Executive Order 14110 — §2 Principles, §6 Workers, §7 Civil R | external_framework | STRUCTURALLY UNALIGNED | 46/100 — partial structural signal | General AI Governance  | 19              | 12      | 2        |
| OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (of | external_framework | PARTIALLY ALIGNED      | 39/100 — limited structural signal | General AI Governance  | 20              | 12      | 4        |
| NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Functions (offici | external_framework | PARTIALLY ALIGNED      | 48/100 — partial structural signal | General AI Governance  | 20              | 12      | 4        |
| NHS England DTAC v2.0 (February 2026) — Introduction & C1 Clinic | external_framework | PARTIALLY ALIGNED      | 36/100 — limited structural signal | Clinical AI Deployment | 17              | 12      | 5        |
| EU AI Act — Art. 9, 13 & 14                                      | external_framework | PARTIALLY ALIGNED      | 44/100 — partial structural signal | General AI Governance  | 20              | 12      | 3        |
| NIST AI RMF — Govern & Map Functions                             | external_framework | STRUCTURALLY UNALIGNED | 34/100 — limited structural signal | General AI Governance  | 18              | 12      | 2        |
| OECD AI Principles (2019, rev. 2024)                             | external_framework | PARTIALLY ALIGNED      | 22/100 — limited structural signal | General AI Governance  | 15              | 12      | 6        |
| US Executive Order 14110 — §4 Safety & §7 Workers                | external_framework | PARTIALLY ALIGNED      | 50/100 — partial structural signal | General AI Governance  | 20              | 12      | 4        |
| NHS England — AI in Clinical Decision Support (Policy Framework) | external_framework | PARTIALLY ALIGNED      | 35/100 — limited structural signal | Clinical AI Deployment | 20              | 12      | 5        |
| TUC/CIPD — Framework for Fair AI in Employment Decisions         | external_framework | PARTIALLY ALIGNED      | 39/100 — limited structural signal | Employment and HR AI   | 19              | 12      | 4        |


### Common structural gaps (cross-document)
structural — constitutional hierarchy not declared (10/10 documents); terminological — no canonical LAIF terms present (10/10 documents); conceptual — LAIF-like concepts insufficiently expressed (3/10 documents); enforceability — insufficient mandatory operational requirements (2/10 documents); auditability — obligations not checkable or traceable (1/10 documents)

### Governance-force patterns
mandate (3); consequence (2); escalation (1); +1 more

### Remediation themes
Reversibility/escalation fixes (10); LAIF-native adoption fixes (10); Immediate clarity/control fixes (3); +1 more


## Per-Document Assessment

### Document 1: US Executive Order 14110 — §2 Principles, §6 Workers, §7 Civil Rights (official text)

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Document name      | US Executive Order 14110 — §2 Principles, §6 Workers, §7 Civil Rights (official text)                                                      |
| Source type        | executive_directive                                                                                                                        |
| Jurisdiction       | United States (Federal)                                                                                                                    |
| Sector             | General AI Governance                                                                                                                      |
| Assessment mode    | external_framework                                                                                                                         |
| Citation           | Executive Order 14110, 88 FR 75191 (Nov 1, 2023), FR Doc. 2023-24283                                                                       |
| Source URL         | https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence |
| Provenance         | OFFICIAL_EXCERPT                                                                                                                           |
| Document type      | executive_policy_directive                                                                                                                 |
| Original file name | not provided                                                                                                                               |
| Source SHA-256     | not provided                                                                                                                               |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a statement of values followed by a tasking list — named officials receive instructions and deadlines. It clearly names the things it exists to protect: people's fundamental rights, openness about how decisions are made, answerability for outcomes, human oversight of the system, safety and more.

Trace who receives something in each operative sentence and a pattern appears: institutions receive duties, deadlines, and reporting obligations — but the people the document is about receive nothing they can hold. Protection exists here as intended future outcomes, not as present commitments to identifiable people; because promises and beneficiaries are never fastened together, individual provisions can erode without anyone being able to say a promise to them was broken.

It provides no route for an affected person to challenge or appeal an outcome — if the system gets it wrong for someone, this text gives them nothing to invoke.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: everything it creates can be modified or undone by its author's successor without any special safeguard.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** whatever its other merits, none of the deeper protective architecture — promises fastened to people, rules that bind the rule-maker, guarantees that survive a change of author — is present in any form. That is not a judgement of the document against its own objectives; it is a statement of what a person could and could not rely on this text for.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| document_type                 | executive_policy_directive                                                                                                                                               |
| recommended_use               | Agency implementation planning, executive control mapping, and accountability-gap review.                                                                                |
| not_sufficient_for            | Not sufficient by itself as proof that agencies implemented, audited, or sustained the required controls.                                                                |
| governance_force_profile      | Executive policy directive with administrative force over named agencies or executive functions; implementation depends on agency ownership and follow-through controls. |
| systemic_repair_value         | Moderate                                                                                                                                                                 |
| operational_closure_rating    | Weak                                                                                                                                                                     |
| evidence_sufficiency_rating   | Moderate                                                                                                                                                                 |
| accountability_closure_rating | Limited                                                                                                                                                                  |
| lifecycle_control_rating      | Limited                                                                                                                                                                  |
| residual_risk_control_rating  | Limited                                                                                                                                                                  |
| implementation_gap_rating     | Limited                                                                                                                                                                  |
| failure_pathway_risk          | High                                                                                                                                                                     |
| priority_repair_actions       | define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review                                                                |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Limited
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 19


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** High
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Verbatim text of Section 2 (Policy and Principles, (a)-(h)), Section 6 (Supporting Workers), and Section 7 (Advancing Equity and Civil Rights), extracted from the committed Federal Register full text and pinned by SHA-256. Non-contiguous sections joined with an explicit […] marker.
- **Intended use:** citable real-world baseline
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 46/100 — partial structural signal
- **Calibrated position:** 56% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 57/100
- **Sector risk alignment:** 20/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Structural strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: accountability; +14 more
- **Governance signal strength:** 46
- **Structural dimension score:** 43/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** STRUCTURALLY UNALIGNED — LAIF's distinctive structural mechanisms not detected in any form; conceptual overlap is measured separately


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected |
| ---------------- | ------- | ------------------------ |
| Coupling         | ABSENT  | none detected            |
| Integrity Layer  | ABSENT  | none detected            |
| Consistency      | ABSENT  | none detected            |
| Reversibility    | ABSENT  | none detected            |
| Self-Application | ABSENT  | none detected            |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                       | Missed signal labels                                                                                                  |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Structural           | 43/100 | numbered sub-requirements; mandatory obligation language (shall); operational mechanisms defined; +2 more | full lifecycle scope declared; risk stratification / proportionality; non-amendable constitutional hierarchy; +2 more |
| Terminology          | 0/100  | none detected                                                                                             | Coupling; Coherence Test; Integrity Layer; +4 more                                                                    |
| Conceptual proximity | 57/100 | human rights / fundamental interests; transparency; accountability; +4 more                               | explainability / interpretability; proportionality; contestability / redress; +2 more                                 |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms    | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                   |
| Enforceability       | 60/100 | mandatory language (shall/must); named responsible parties; enforcement consequences / penalties          | risk-proportionate thresholds; non-discretionary operational mandates                                                 |
| Overall readiness    | 46/100 | partial structural signal                                                                                 | —                                                                                                                     |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** partial structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 2 — High conceptual LAIF-model signal appears with low canonical terminology signal.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status           | Reviewer note                                                                                                    |
| ------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| protected interest | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| evidence           | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| escalation         | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| consequence        | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| auditability       | detected         | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: transparency requirements; Risk signal absent: high-risk classification language; Risk signal absent: accountability assignment; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 19
- **Exact/deterministic count:** 19
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-governance-force-signal (governance_force_signal); LAIF-TRACE-03-governance-force-signal (governance_force_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Restriction-protection pairing not established — no governance restriction is bound to the specific interest it protects, in any vocabulary.
   - **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** For each restriction, name the specific interest it protects and bind the two together so that neither can be weakened without the other, with the protection as enforceable as the restriction. The document's own vocabulary is sufficient for the structure; the canonical form ('Coupling between [restriction] and [interest], with equivalent normative force' — Toolkit §2 B.1) is required only on the LAIF-native certification path, where an equivalence mapping is the alternative (Regulatory Integration Guide Part One).
2. **Problem:** Structural governance architecture score critically low (43/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 5 missed signals for this dimension. Critical gaps: full lifecycle scope declared, risk stratification / proportionality, non-amendable constitutional hierarchy. Full signal breakdown in the Scores section.
3. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
4. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.
5. **Problem:** Constitutional hierarchy not declared (structural score 43/100). Missing: full lifecycle scope declared, risk stratification / proportionality, non-amendable constitutional hierarchy.
   - **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   - **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-structural-transpar
  - **finding_type:** construct_gap
  - **severity:** medium
  - **diagnostic_gap:** Missing LAIF construct: Structural Transparency
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal, LAIF-TRACE-08-governance-force-signal
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 2: OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (official text)

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Document name      | OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (official text)                                            |
| Source type        | international_principles                                                                                                |
| Jurisdiction       | International (OECD member states)                                                                                      |
| Sector             | General AI Governance                                                                                                   |
| Assessment mode    | external_framework                                                                                                      |
| Citation           | OECD Recommendation of the Council on Artificial Intelligence, OECD/LEGAL/0449, adopted 22 May 2019, amended 3 May 2024 |
| Source URL         | https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449                                                        |
| Provenance         | OFFICIAL_EXCERPT                                                                                                        |
| Document type      | unknown_governance_document                                                                                             |
| Original file name | not provided                                                                                                            |
| Source SHA-256     | not provided                                                                                                            |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is an intergovernmental commitment — principles that governments endorse and are expected, but not compelled, to implement. It clearly names the things it exists to protect: people's fundamental rights, openness about how decisions are made, explanations people can understand, answerability for outcomes, human oversight of the system and more.

It expresses a clear intention to protect people, but the promises are not fastened to the people they serve: a specific rule could be weakened or dropped without visibly breaking a commitment to any identifiable person.

It does give people a route to challenge decisions — a genuine person-facing protection, and the main exception to the pattern above.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: it gestures at correction and rollback, but not as a guaranteed capacity, and everything it creates can be undone by its author's successor.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | unknown_governance_document                                                                                                                     |
| recommended_use               | Preliminary governance triage and document classification review.                                                                               |
| not_sufficient_for            | Not sufficient for reliance until authority, scope, controls, and evidence are confirmed.                                                       |
| governance_force_profile      | Governance document with unclear authority; reviewer must establish institutional force, accountable owner, and evidence basis before reliance. |
| systemic_repair_value         | Limited                                                                                                                                         |
| operational_closure_rating    | Weak                                                                                                                                            |
| evidence_sufficiency_rating   | Moderate                                                                                                                                        |
| accountability_closure_rating | Weak                                                                                                                                            |
| lifecycle_control_rating      | Limited                                                                                                                                         |
| residual_risk_control_rating  | Limited                                                                                                                                         |
| implementation_gap_rating     | Limited                                                                                                                                         |
| failure_pathway_risk          | High                                                                                                                                            |
| priority_repair_actions       | define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review                                       |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Weak
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 20


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** High
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Verbatim text of Section 1 (Principles 1.1-1.5 for responsible stewardship of trustworthy AI) and Section 2 (Recommendations 2.1-2.5 for national policies), extracted from the committed OECD Legal Instruments snapshot (6 May 2026) and pinned by SHA-256. Source snapshot preserves the publisher's hard line-wrapping.
- **Intended use:** citable real-world baseline
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 39/100 — limited structural signal
- **Calibrated position:** 48% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 84/100
- **Sector risk alignment:** 40/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; enforceability — insufficient mandatory operational requirements
- **Structural strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: explainability / interpretability; +15 more
- **Governance signal strength:** 39
- **Structural dimension score:** 26/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected      |
| ---------------- | ------- | ----------------------------- |
| Coupling         | ABSENT  | none detected                 |
| Integrity Layer  | PARTIAL | meaningful account of outputs |
| Consistency      | ABSENT  | none detected                 |
| Reversibility    | PARTIAL | reversal capacity preserved   |
| Self-Application | ABSENT  | none detected                 |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                    | Missed signal labels                                                                                                                            |
| -------------------- | ------ | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 26/100 | numbered sub-requirements; full lifecycle scope declared; operational mechanisms defined; +1 more      | mandatory obligation language (shall); risk stratification / proportionality; threshold gate conditions (all must pass simultaneously); +3 more |
| Terminology          | 0/100  | none detected                                                                                          | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                              |
| Conceptual proximity | 84/100 | human rights / fundamental interests; transparency; explainability / interpretability; +7 more         | proportionality; reversibility / modifiability                                                                                                  |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                                             |
| Enforceability       | 20/100 | named responsible parties                                                                              | mandatory language (shall/must); risk-proportionate thresholds; enforcement consequences / penalties; +1 more                                   |
| Overall readiness    | 39/100 | limited structural signal                                                                              | —                                                                                                                                               |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** limited structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 4 — High conceptual LAIF-model signal appears with low canonical terminology signal.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Low LAIF-model signal may indicate missing LAIF-model signals, not legal invalidity under the source framework's own authority.; +1 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status                | Reviewer note                                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| actor              | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| protected interest | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| escalation         | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| consequence        | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| auditability       | detected              | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: accountability assignment; Risk signal present: transparency requirements; Risk signal absent: high-risk classification language; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 20
- **Exact/deterministic count:** 20
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-governance-force-signal (governance_force_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Implicit protective signals present but not declared as structural Coupling.
   - **Why it matters:** The document already expresses protective intent — detected: «AI actors should be accountable for the proper functioning of AI systems and for the respect of». However, implicit intent does not constitute structural Coupling: the protection can be removed without affecting the obligation it was meant to serve. The upgrade required is structural, not conceptual (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** Convert each detected implicit signal into an explicit Coupling declaration: 'Coupling between [the restriction already present] and [the specific human interest the detected protective language names], with equivalent normative force on both sides — neither may be weakened in isolation.' The governance intent is present; only the structural binding is missing (Toolkit §2 B.1).
2. **Problem:** Enforceability score critically low (20/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without enforceable obligations, regulatory bodies cannot hold operators accountable for governance failures. The standard is aspirational rather than operationally binding — no party can be required to comply.
   - **Concrete fix:** Address the 4 missed signals for this dimension. Critical gaps: mandatory language (shall/must), risk-proportionate thresholds, enforcement consequences / penalties. Full signal breakdown in the Scores section.
3. **Problem:** Structural governance architecture score critically low (26/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 6 missed signals for this dimension. Critical gaps: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). Full signal breakdown in the Scores section.
4. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
5. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-enforceability-insufficient-mandatory-oper
  - **finding_type:** enforceability_gap
  - **severity:** medium
  - **diagnostic_gap:** enforceability — insufficient mandatory operational requirements
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: enforceability — insufficient mandatory operational requirements
  - **operational_control:** Maintain a controlled obligation register that maps mandate text to owner, trigger, evidence, and review status.
  - **evidence_artifact:** Approved obligation register entry with source citation and control mapping.
  - **verification_test:** Create a verification test that samples this mandate control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 3: NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Functions (official text)

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Document name      | NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Functions (official text)                                                           |
| Source type        | voluntary_framework                                                                                                                |
| Jurisdiction       | United States                                                                                                                      |
| Sector             | General AI Governance                                                                                                              |
| Assessment mode    | external_framework                                                                                                                 |
| Citation           | NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0), January 2023, https://doi.org/10.6028/NIST.AI.100-1 |
| Source URL         | https://doi.org/10.6028/NIST.AI.100-1                                                                                              |
| Provenance         | OFFICIAL_EXCERPT                                                                                                                   |
| Document type      | voluntary_risk_framework                                                                                                           |
| Original file name | not provided                                                                                                                       |
| Source SHA-256     | not provided                                                                                                                       |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a voluntary playbook — structured practices an organisation may adopt, with no binding force of its own. It clearly names the things it exists to protect: openness about how decisions are made, answerability for outcomes, human oversight of the system, matching rules to the size of the risk, safety and more.

Trace who receives something in each operative sentence and a pattern appears: institutions receive duties, deadlines, and reporting obligations — but the people the document is about receive nothing they can hold. Protection exists here as intended future outcomes, not as present commitments to identifiable people; because promises and beneficiaries are never fastened together, individual provisions can erode without anyone being able to say a promise to them was broken.

It provides no route for an affected person to challenge or appeal an outcome — if the system gets it wrong for someone, this text gives them nothing to invoke.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: it gestures at correction and rollback, but not as a guaranteed capacity, and everything it creates can be undone by its author's successor.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                                           |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | voluntary_risk_framework                                                                                                                                        |
| recommended_use               | Governance program design, procurement reference, assurance planning, and control-gap analysis.                                                                 |
| not_sufficient_for            | Not sufficient by itself as binding compliance, operational evidence, or certification.                                                                         |
| governance_force_profile      | Voluntary risk-management framework; high guidance value but limited force unless incorporated into contracts, regulation, assurance, or internal policy gates. |
| systemic_repair_value         | Moderate                                                                                                                                                        |
| operational_closure_rating    | Weak                                                                                                                                                            |
| evidence_sufficiency_rating   | Moderate                                                                                                                                                        |
| accountability_closure_rating | Moderate                                                                                                                                                        |
| lifecycle_control_rating      | Limited                                                                                                                                                         |
| residual_risk_control_rating  | Limited                                                                                                                                                         |
| implementation_gap_rating     | Limited                                                                                                                                                         |
| failure_pathway_risk          | High                                                                                                                                                            |
| priority_repair_actions       | define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review                                                       |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Moderate
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 20


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** High
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Verbatim text of the Part 2 Core GOVERN function (narrative + Table 1 categories/subcategories) and MAP function (narrative + Table 2), extracted from the committed NIST AI 100-1 full text and pinned by SHA-256. Table text retains the source's markdown table formatting.
- **Intended use:** citable real-world baseline
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 48/100 — partial structural signal
- **Calibrated position:** 59% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 47/100
- **Sector risk alignment:** 80/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Structural strengths:** Expresses: transparency; Expresses: accountability; Expresses: human oversight; +16 more
- **Governance signal strength:** 48
- **Structural dimension score:** 41/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected    |
| ---------------- | ------- | --------------------------- |
| Coupling         | ABSENT  | none detected               |
| Integrity Layer  | ABSENT  | none detected               |
| Consistency      | ABSENT  | none detected               |
| Reversibility    | PARTIAL | reversal capacity preserved |
| Self-Application | ABSENT  | none detected               |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                      | Missed signal labels                                                                                                                            |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 41/100 | numbered sub-requirements; mandatory obligation language (shall); full lifecycle scope declared; +3 more | threshold gate conditions (all must pass simultaneously); non-amendable constitutional hierarchy; self-application clause (Part Seven); +1 more |
| Terminology          | 0/100  | none detected                                                                                            | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                              |
| Conceptual proximity | 47/100 | transparency; accountability; human oversight; +3 more                                                   | human rights / fundamental interests; explainability / interpretability; contestability / redress; +3 more                                      |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms   | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                                             |
| Enforceability       | 80/100 | mandatory language (shall/must); named responsible parties; risk-proportionate thresholds; +1 more       | non-discretionary operational mandates                                                                                                          |
| Overall readiness    | 48/100 | partial structural signal                                                                                | —                                                                                                                                               |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** partial structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 4 — Sector risk alignment materially exceeds overall readiness.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Possible keyword or signal density risk; requires structural evidence review. This is not a finding of bad faith and not a legal invalidity claim.; +1 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status           | Reviewer note                                                                                                    |
| ------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| protected interest | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| evidence           | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit | Partial substance detected in the source text (one signal family).                                               |
| escalation         | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| consequence        | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| auditability       | detected         | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: high-risk classification language; Risk signal present: accountability assignment; Risk signal present: transparency requirements; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 20
- **Exact/deterministic count:** 20
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Restriction-protection pairing not established — no governance restriction is bound to the specific interest it protects, in any vocabulary.
   - **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** For each restriction, name the specific interest it protects and bind the two together so that neither can be weakened without the other, with the protection as enforceable as the restriction. The document's own vocabulary is sufficient for the structure; the canonical form ('Coupling between [restriction] and [interest], with equivalent normative force' — Toolkit §2 B.1) is required only on the LAIF-native certification path, where an equivalence mapping is the alternative (Regulatory Integration Guide Part One).
2. **Problem:** Structural governance architecture score critically low (41/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 4 missed signals for this dimension. Critical gaps: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven). Full signal breakdown in the Scores section.
3. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
4. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.
5. **Problem:** Constitutional hierarchy not declared (structural score 41/100). Missing: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven).
   - **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   - **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-structural-transpar
  - **finding_type:** construct_gap
  - **severity:** medium
  - **diagnostic_gap:** Missing LAIF construct: Structural Transparency
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** LAIF-TRACE-03-sector-profile-signal, LAIF-TRACE-11-governance-force-signal
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 4: NHS England DTAC v2.0 (February 2026) — Introduction & C1 Clinical Safety (official text)

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| Document name      | NHS England DTAC v2.0 (February 2026) — Introduction & C1 Clinical Safety (official text)                    |
| Source type        | sector_policy                                                                                                |
| Jurisdiction       | United Kingdom                                                                                               |
| Sector             | Clinical AI Deployment                                                                                       |
| Assessment mode    | external_framework                                                                                           |
| Citation           | Digital Technology Assessment Criteria for Health and Social Care (DTAC) v2.0, NHS England, 24 February 2026 |
| Source URL         | https://transform.england.nhs.uk/key-tools-and-info/digital-technology-assessment-criteria-dtac/             |
| Provenance         | OFFICIAL_EXCERPT                                                                                             |
| Document type      | sector_assurance_checklist                                                                                   |
| Original file name | not provided                                                                                                 |
| Source SHA-256     | not provided                                                                                                 |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a sector instrument — operational requirements for a specific deployment context. It clearly names the things it exists to protect: safety, the ability to challenge decisions, structured risk management.

Trace who receives something in each operative sentence and a pattern appears: institutions receive duties, deadlines, and reporting obligations — but the people the document is about receive nothing they can hold. Protection exists here as intended future outcomes, not as present commitments to identifiable people; because promises and beneficiaries are never fastened together, individual provisions can erode without anyone being able to say a promise to them was broken.

It does give people a route to challenge decisions — a genuine person-facing protection, and the main exception to the pattern above.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: everything it creates can be modified or undone by its author's successor without any special safeguard.

To its credit, the administrative machinery is real: evidence and documentation duties, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | sector_assurance_checklist                                                                                                              |
| recommended_use               | Assurance triage, reviewer workflow design, and sector-specific evidence requests.                                                      |
| not_sufficient_for            | Not sufficient without source evidence, accountable reviewer sign-off, and operational gate criteria.                                   |
| governance_force_profile      | Sector assurance checklist; useful for assurance triage where mapped to accountable reviewers, evidence artifacts, and pass/fail gates. |
| systemic_repair_value         | Limited                                                                                                                                 |
| operational_closure_rating    | Weak                                                                                                                                    |
| evidence_sufficiency_rating   | Moderate                                                                                                                                |
| accountability_closure_rating | Moderate                                                                                                                                |
| lifecycle_control_rating      | Weak                                                                                                                                    |
| residual_risk_control_rating  | Moderate                                                                                                                                |
| implementation_gap_rating     | Limited                                                                                                                                 |
| failure_pathway_risk          | Medium                                                                                                                                  |
| priority_repair_actions       | define decision/release gate; add rollback/fallback control                                                                             |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Moderate
- **Lifecycle control:** Weak
- **Residual-risk closure:** Moderate


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 17


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** define decision/release gate; add rollback/fallback control


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** Medium
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Verbatim text of the DTAC v2.0 Introduction (scope, definitions, assessment structure) and assessed section C1 Clinical safety (criteria C1.1.1-C1.2.5 incl. DCB0129 requirements), extracted from the committed source text and pinned by SHA-256. Non-contiguous sections joined with an explicit […] marker.
- **Intended use:** citable sector scenario — clinical AI assurance
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 36/100 — limited structural signal
- **Calibrated position:** 44% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 24/100
- **Sector risk alignment:** 80/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; conceptual — LAIF-like concepts insufficiently expressed
- **Structural strengths:** Expresses: safety; Expresses: contestability / redress; Expresses: risk governance; +9 more
- **Governance signal strength:** 36
- **Structural dimension score:** 12/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected     |
| ---------------- | ------- | ---------------------------- |
| Coupling         | ABSENT  | none detected                |
| Integrity Layer  | PARTIAL | all-must-pass threshold gate |
| Consistency      | ABSENT  | none detected                |
| Reversibility    | ABSENT  | none detected                |
| Self-Application | ABSENT  | none detected                |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                                        | Missed signal labels                                                                                             |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Structural           | 12/100 | full lifecycle scope declared; operational mechanisms defined                                                              | numbered sub-requirements; mandatory obligation language (shall); risk stratification / proportionality; +5 more |
| Terminology          | 0/100  | none detected                                                                                                              | Coupling; Coherence Test; Integrity Layer; +4 more                                                               |
| Conceptual proximity | 24/100 | safety; contestability / redress; risk governance                                                                          | human rights / fundamental interests; transparency; explainability / interpretability; +6 more                   |
| Auditability         | 60/100 | multiple mandatory obligations (shall/must pairs); evidence / documentation requirements; specific, measurable obligations | numbered traceable requirements; review / monitoring mechanisms                                                  |
| Enforceability       | 80/100 | mandatory language (shall/must); named responsible parties; risk-proportionate thresholds; +1 more                         | enforcement consequences / penalties                                                                             |
| Overall readiness    | 36/100 | limited structural signal                                                                                                  | —                                                                                                                |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** limited structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 5 — Sector risk alignment materially exceeds overall readiness.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Low LAIF-model signal may indicate missing LAIF-model signals, not legal invalidity under the source framework's own authority.; +2 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status                | Reviewer note                                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| protected interest | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| escalation         | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| consequence        | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| auditability       | detected              | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** Clinical AI Deployment
- **Sector profile key:** clinical_ai
- **Profile-specific remediation themes:** Assign a clinical governance owner with clinician reviewer and safety incident pathway.; Require clinical fallback, override record, patient safety review, and incident log.; Keep clinical source-evidence claims tied to exact text.
- **Profile-specific evidence cautions:** Clinical vocabulary does not determine medical, regulatory, or legal validity.; Do not invent clinical validation, fallback, override, patient safety review, or incident evidence.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: patient safety signal; Risk signal present: diagnostic / treatment language; Risk signal present: named clinical actor; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 17
- **Exact/deterministic count:** 17
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
| Construct               | Detected for LAIF-native gate |
| ----------------------- | ----------------------------- |
| Coupling                | not detected                  |
| Coherence Test          | not detected                  |
| Integrity Layer         | not detected                  |
| Structural Transparency | not detected                  |
| Structural Honesty      | not detected                  |
| Structural Containment  | not detected                  |
| Consistency             | yes                           |
| Reversibility           | not detected                  |
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)
- Sector gaming risk [MEDIUM]: Sector alignment 80% but conceptual proximity 24/100. Sector-specific vocabulary present without underlying governance intent. May indicate sector-optimised keyword selection rather than substantive coverage.


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Restriction-protection pairing not established — no governance restriction is bound to the specific interest it protects, in any vocabulary.
   - **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** For each restriction, name the specific interest it protects and bind the two together so that neither can be weakened without the other, with the protection as enforceable as the restriction. The document's own vocabulary is sufficient for the structure; the canonical form ('Coupling between [restriction] and [interest], with equivalent normative force' — Toolkit §2 B.1) is required only on the LAIF-native certification path, where an equivalence mapping is the alternative (Regulatory Integration Guide Part One).
2. **Problem:** Structural governance architecture score critically low (12/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 8 missed signals for this dimension. Critical gaps: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality. Full signal breakdown in the Scores section.
3. **Problem:** Conceptual governance coverage score critically low (24/100) — most deficient dimension after Coupling.
   - **Why it matters:** Low conceptual proximity indicates the document's governance intent is not substantially aligned with LAIF values. The adoption gap is more fundamental than terminology — substantive governance redesign is required, not just terminological substitution.
   - **Concrete fix:** Address the 9 missed signals for this dimension. Critical gaps: human rights / fundamental interests, transparency, explainability / interpretability. Full signal breakdown in the Scores section.
4. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
5. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-conceptual-laif-like-concepts-insufficient
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** conceptual — LAIF-like concepts insufficiently expressed
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: conceptual — LAIF-like concepts insufficiently expressed
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 5: EU AI Act — Art. 9, 13 & 14

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                   |
| ------------------ | ----------------------------------------------------------------------- |
| Document name      | EU AI Act — Art. 9, 13 & 14                                             |
| Source type        | binding_regulation                                                      |
| Jurisdiction       | European Union                                                          |
| Sector             | General AI Governance                                                   |
| Assessment mode    | external_framework                                                      |
| Citation           | Regulation (EU) 2024/1689 of the European Parliament and of the Council |
| Source URL         | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689  |
| Provenance         | REPRESENTATIVE_EXCERPT                                                  |
| Document type      | unknown_governance_document                                             |
| Original file name | not provided                                                            |
| Source SHA-256     | not provided                                                            |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is binding law — it imposes obligations on identified parties, enforceable through the legal system. It clearly names the things it exists to protect: people's fundamental rights, openness about how decisions are made, explanations people can understand, human oversight of the system, safety and more.

Trace who receives something in each operative sentence and a pattern appears: institutions receive duties, deadlines, and reporting obligations — but the people the document is about receive nothing they can hold. Protection exists here as intended future outcomes, not as present commitments to identifiable people; because promises and beneficiaries are never fastened together, individual provisions can erode without anyone being able to say a promise to them was broken.

It provides no route for an affected person to challenge or appeal an outcome — if the system gets it wrong for someone, this text gives them nothing to invoke.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: everything it creates can be modified or undone by its author's successor without any special safeguard.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | unknown_governance_document                                                                                                                     |
| recommended_use               | Preliminary governance triage and document classification review.                                                                               |
| not_sufficient_for            | Not sufficient for reliance until authority, scope, controls, and evidence are confirmed.                                                       |
| governance_force_profile      | Governance document with unclear authority; reviewer must establish institutional force, accountable owner, and evidence basis before reliance. |
| systemic_repair_value         | Limited                                                                                                                                         |
| operational_closure_rating    | Weak                                                                                                                                            |
| evidence_sufficiency_rating   | Moderate                                                                                                                                        |
| accountability_closure_rating | Limited                                                                                                                                         |
| lifecycle_control_rating      | Limited                                                                                                                                         |
| residual_risk_control_rating  | Limited                                                                                                                                         |
| implementation_gap_rating     | Limited                                                                                                                                         |
| failure_pathway_risk          | High                                                                                                                                            |
| priority_repair_actions       | assign accountable owner; define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review             |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Limited
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 20


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** assign accountable owner; define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** High
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Condensed paraphrase of Articles 9, 13, and 14; captures governance intent but is not verbatim text. Verify against official OJ publication.
- **Intended use:** real-world baseline
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 44/100 — partial structural signal
- **Calibrated position:** 54% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 49/100
- **Sector risk alignment:** 60/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Structural strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: explainability / interpretability; +15 more
- **Governance signal strength:** 44
- **Structural dimension score:** 41/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected                                         |
| ---------------- | ------- | ---------------------------------------------------------------- |
| Coupling         | ABSENT  | none detected                                                    |
| Integrity Layer  | PARTIAL | meaningful account of outputs; bounded operation with escalation |
| Consistency      | ABSENT  | none detected                                                    |
| Reversibility    | ABSENT  | none detected                                                    |
| Self-Application | ABSENT  | none detected                                                    |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                      | Missed signal labels                                                                                                                            |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 41/100 | numbered sub-requirements; mandatory obligation language (shall); full lifecycle scope declared; +3 more | threshold gate conditions (all must pass simultaneously); non-amendable constitutional hierarchy; self-application clause (Part Seven); +1 more |
| Terminology          | 0/100  | none detected                                                                                            | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                              |
| Conceptual proximity | 49/100 | human rights / fundamental interests; transparency; explainability / interpretability; +3 more           | accountability; proportionality; contestability / redress; +3 more                                                                              |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms   | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                                             |
| Enforceability       | 60/100 | mandatory language (shall/must); risk-proportionate thresholds; non-discretionary operational mandates   | named responsible parties; enforcement consequences / penalties                                                                                 |
| Overall readiness    | 44/100 | partial structural signal                                                                                | —                                                                                                                                               |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** partial structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 3 — Sector risk alignment materially exceeds overall readiness.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Possible keyword or signal density risk; requires structural evidence review. This is not a finding of bad faith and not a legal invalidity claim.
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status                | Reviewer note                                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| trigger            | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| protected interest | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| escalation         | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| consequence        | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| auditability       | detected              | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: high-risk classification language; Risk signal present: transparency requirements; Risk signal present: human oversight mechanisms; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 20
- **Exact/deterministic count:** 20
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Restriction-protection pairing not established — no governance restriction is bound to the specific interest it protects, in any vocabulary.
   - **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** For each restriction, name the specific interest it protects and bind the two together so that neither can be weakened without the other, with the protection as enforceable as the restriction. The document's own vocabulary is sufficient for the structure; the canonical form ('Coupling between [restriction] and [interest], with equivalent normative force' — Toolkit §2 B.1) is required only on the LAIF-native certification path, where an equivalence mapping is the alternative (Regulatory Integration Guide Part One).
2. **Problem:** Structural governance architecture score critically low (41/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 4 missed signals for this dimension. Critical gaps: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven). Full signal breakdown in the Scores section.
3. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
4. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.
5. **Problem:** Constitutional hierarchy not declared (structural score 41/100). Missing: threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy, self-application clause (Part Seven).
   - **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   - **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-structural-transpar
  - **finding_type:** construct_gap
  - **severity:** medium
  - **diagnostic_gap:** Missing LAIF construct: Structural Transparency
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** LAIF-TRACE-02-sector-profile-signal, LAIF-TRACE-12-governance-force-signal
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 6: NIST AI RMF — Govern & Map Functions

#### Document Overview

##### Assessment Scope
| Field              | Value                                                 |
| ------------------ | ----------------------------------------------------- |
| Document name      | NIST AI RMF — Govern & Map Functions                  |
| Source type        | voluntary_framework                                   |
| Jurisdiction       | United States                                         |
| Sector             | General AI Governance                                 |
| Assessment mode    | external_framework                                    |
| Citation           | NIST AI Risk Management Framework 1.0 (NIST AI 100-1) |
| Source URL         | https://airc.nist.gov/RMF                             |
| Provenance         | REPRESENTATIVE_EXCERPT                                |
| Document type      | voluntary_risk_framework                              |
| Original file name | not provided                                          |
| Source SHA-256     | not provided                                          |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a voluntary playbook — structured practices an organisation may adopt, with no binding force of its own. It clearly names the things it exists to protect: openness about how decisions are made, answerability for outcomes, human oversight of the system, safety, structured risk management.

Trace who receives something in each operative sentence and a pattern appears: institutions receive duties, deadlines, and reporting obligations — but the people the document is about receive nothing they can hold. Protection exists here as intended future outcomes, not as present commitments to identifiable people; because promises and beneficiaries are never fastened together, individual provisions can erode without anyone being able to say a promise to them was broken.

It provides no route for an affected person to challenge or appeal an outcome — if the system gets it wrong for someone, this text gives them nothing to invoke.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: everything it creates can be modified or undone by its author's successor without any special safeguard.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** whatever its other merits, none of the deeper protective architecture — promises fastened to people, rules that bind the rule-maker, guarantees that survive a change of author — is present in any form. That is not a judgement of the document against its own objectives; it is a statement of what a person could and could not rely on this text for.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                                           |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | voluntary_risk_framework                                                                                                                                        |
| recommended_use               | Governance program design, procurement reference, assurance planning, and control-gap analysis.                                                                 |
| not_sufficient_for            | Not sufficient by itself as binding compliance, operational evidence, or certification.                                                                         |
| governance_force_profile      | Voluntary risk-management framework; high guidance value but limited force unless incorporated into contracts, regulation, assurance, or internal policy gates. |
| systemic_repair_value         | Limited                                                                                                                                                         |
| operational_closure_rating    | Weak                                                                                                                                                            |
| evidence_sufficiency_rating   | Moderate                                                                                                                                                        |
| accountability_closure_rating | Limited                                                                                                                                                         |
| lifecycle_control_rating      | Limited                                                                                                                                                         |
| residual_risk_control_rating  | Limited                                                                                                                                                         |
| implementation_gap_rating     | Limited                                                                                                                                                         |
| failure_pathway_risk          | Medium                                                                                                                                                          |
| priority_repair_actions       | add rollback/fallback control                                                                                                                                   |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Limited
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 18


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** add rollback/fallback control


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** Medium
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Condensed paraphrase of GOVERN and MAP functions; note British spelling 'organisational' departs from the American-English original. Not verbatim.
- **Intended use:** real-world baseline
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 34/100 — limited structural signal
- **Calibrated position:** 42% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 39/100
- **Sector risk alignment:** 40/100
- **Remediation effort:** VERY HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; conceptual — LAIF-like concepts insufficiently expressed
- **Structural strengths:** Expresses: transparency; Expresses: accountability; Expresses: human oversight; +11 more
- **Governance signal strength:** 34
- **Structural dimension score:** 26/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** STRUCTURALLY UNALIGNED — LAIF's distinctive structural mechanisms not detected in any form; conceptual overlap is measured separately


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected |
| ---------------- | ------- | ------------------------ |
| Coupling         | ABSENT  | none detected            |
| Integrity Layer  | ABSENT  | none detected            |
| Consistency      | ABSENT  | none detected            |
| Reversibility    | ABSENT  | none detected            |
| Self-Application | ABSENT  | none detected            |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                    | Missed signal labels                                                                                                                            |
| -------------------- | ------ | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 26/100 | numbered sub-requirements; full lifecycle scope declared; operational mechanisms defined; +1 more      | mandatory obligation language (shall); risk stratification / proportionality; threshold gate conditions (all must pass simultaneously); +3 more |
| Terminology          | 0/100  | none detected                                                                                          | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                              |
| Conceptual proximity | 39/100 | transparency; accountability; human oversight; +2 more                                                 | human rights / fundamental interests; explainability / interpretability; proportionality; +4 more                                               |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                                             |
| Enforceability       | 40/100 | named responsible parties; enforcement consequences / penalties                                        | mandatory language (shall/must); risk-proportionate thresholds; non-discretionary operational mandates                                          |
| Overall readiness    | 34/100 | limited structural signal                                                                              | —                                                                                                                                               |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** limited structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 2 — Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Low LAIF-model signal may indicate missing LAIF-model signals, not legal invalidity under the source framework's own authority.
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status                | Reviewer note                                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| actor              | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| protected interest | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| evidence           | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| escalation         | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| consequence        | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| auditability       | detected              | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: accountability assignment; Risk signal present: transparency requirements; Risk signal absent: high-risk classification language; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 18
- **Exact/deterministic count:** 18
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-provenance-signal (provenance_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Restriction-protection pairing not established — no governance restriction is bound to the specific interest it protects, in any vocabulary.
   - **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** For each restriction, name the specific interest it protects and bind the two together so that neither can be weakened without the other, with the protection as enforceable as the restriction. The document's own vocabulary is sufficient for the structure; the canonical form ('Coupling between [restriction] and [interest], with equivalent normative force' — Toolkit §2 B.1) is required only on the LAIF-native certification path, where an equivalence mapping is the alternative (Regulatory Integration Guide Part One).
2. **Problem:** Structural governance architecture score critically low (26/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 6 missed signals for this dimension. Critical gaps: mandatory obligation language (shall), risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). Full signal breakdown in the Scores section.
3. **Problem:** Enforceability score critically low (40/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without enforceable obligations, regulatory bodies cannot hold operators accountable for governance failures. The standard is aspirational rather than operationally binding — no party can be required to comply.
   - **Concrete fix:** Address the 3 missed signals for this dimension. Critical gaps: mandatory language (shall/must), risk-proportionate thresholds, non-discretionary operational mandates. Full signal breakdown in the Scores section.
4. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
5. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-conceptual-laif-like-concepts-insufficient
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** conceptual — LAIF-like concepts insufficiently expressed
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: conceptual — LAIF-like concepts insufficiently expressed
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 7: OECD AI Principles (2019, rev. 2024)

#### Document Overview

##### Assessment Scope
| Field              | Value                                                 |
| ------------------ | ----------------------------------------------------- |
| Document name      | OECD AI Principles (2019, rev. 2024)                  |
| Source type        | international_principles                              |
| Jurisdiction       | International (OECD member states)                    |
| Sector             | General AI Governance                                 |
| Assessment mode    | external_framework                                    |
| Citation           | OECD Principles on AI, adopted May 2019, revised 2024 |
| Source URL         | https://oecd.ai/en/ai-principles                      |
| Provenance         | REPRESENTATIVE_EXCERPT                                |
| Document type      | unknown_governance_document                           |
| Original file name | not provided                                          |
| Source SHA-256     | not provided                                          |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is an intergovernmental commitment — principles that governments endorse and are expected, but not compelled, to implement. It clearly names the things it exists to protect: people's fundamental rights, openness about how decisions are made, explanations people can understand, answerability for outcomes, human oversight of the system and more.

It expresses a clear intention to protect people, but the promises are not fastened to the people they serve: a specific rule could be weakened or dropped without visibly breaking a commitment to any identifiable person.

It does give people a route to challenge decisions — a genuine person-facing protection, and the main exception to the pattern above.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: everything it creates can be modified or undone by its author's successor without any special safeguard.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | unknown_governance_document                                                                                                                     |
| recommended_use               | Preliminary governance triage and document classification review.                                                                               |
| not_sufficient_for            | Not sufficient for reliance until authority, scope, controls, and evidence are confirmed.                                                       |
| governance_force_profile      | Governance document with unclear authority; reviewer must establish institutional force, accountable owner, and evidence basis before reliance. |
| systemic_repair_value         | Limited                                                                                                                                         |
| operational_closure_rating    | Weak                                                                                                                                            |
| evidence_sufficiency_rating   | Weak                                                                                                                                            |
| accountability_closure_rating | Weak                                                                                                                                            |
| lifecycle_control_rating      | Weak                                                                                                                                            |
| residual_risk_control_rating  | Weak                                                                                                                                            |
| implementation_gap_rating     | Weak                                                                                                                                            |
| failure_pathway_risk          | High                                                                                                                                            |
| priority_repair_actions       | define decision/release gate; link evidence artifact; add rollback/fallback control; document residual-risk acceptance and review               |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Weak
- **Lifecycle control:** Weak
- **Residual-risk closure:** Weak


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Weak
- **Evidence trace count:** 15


#### Implementation Gap Findings
- **Implementation gap rating:** Weak
- **Priority repair actions:** define decision/release gate; link evidence artifact; add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** High
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Condensed paraphrase of the five OECD AI Principles; structural numbering and intent preserved but wording is not verbatim.
- **Intended use:** real-world baseline
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 22/100 — limited structural signal
- **Calibrated position:** 27% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 76/100
- **Sector risk alignment:** 60/100
- **Remediation effort:** VERY HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; auditability — obligations not checkable or traceable; +1 more
- **Structural strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: explainability / interpretability; +9 more
- **Governance signal strength:** 22
- **Structural dimension score:** 12/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected      |
| ---------------- | ------- | ----------------------------- |
| Coupling         | ABSENT  | none detected                 |
| Integrity Layer  | PARTIAL | meaningful account of outputs |
| Consistency      | ABSENT  | none detected                 |
| Reversibility    | ABSENT  | none detected                 |
| Self-Application | ABSENT  | none detected                 |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                            | Missed signal labels                                                                                                               |
| -------------------- | ------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 12/100 | full lifecycle scope declared; operational mechanisms defined                                  | numbered sub-requirements; mandatory obligation language (shall); risk stratification / proportionality; +5 more                   |
| Terminology          | 0/100  | none detected                                                                                  | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                 |
| Conceptual proximity | 76/100 | human rights / fundamental interests; transparency; explainability / interpretability; +6 more | proportionality; reversibility / modifiability; risk governance                                                                    |
| Auditability         | 0/100  | none detected                                                                                  | multiple mandatory obligations (shall/must pairs); numbered traceable requirements; evidence / documentation requirements; +2 more |
| Enforceability       | 20/100 | named responsible parties                                                                      | mandatory language (shall/must); risk-proportionate thresholds; enforcement consequences / penalties; +1 more                      |
| Overall readiness    | 22/100 | limited structural signal                                                                      | —                                                                                                                                  |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** limited structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 6 — High conceptual LAIF-model signal appears with low canonical terminology signal.; Sector risk alignment materially exceeds overall readiness.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; +3 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status                | Reviewer note                                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| actor              | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| protected interest | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| escalation         | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| consequence        | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| auditability       | detected              | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: accountability assignment; Risk signal present: transparency requirements; Risk signal present: human oversight mechanisms; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 15
- **Exact/deterministic count:** 15
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Implicit protective signals present but not declared as structural Coupling.
   - **Why it matters:** The document already expresses protective intent — detected: «AI actors should be accountable for the proper functioning of AI systems and for the respect of». However, implicit intent does not constitute structural Coupling: the protection can be removed without affecting the obligation it was meant to serve. The upgrade required is structural, not conceptual (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** Convert each detected implicit signal into an explicit Coupling declaration: 'Coupling between [the restriction already present] and [the specific human interest the detected protective language names], with equivalent normative force on both sides — neither may be weakened in isolation.' The governance intent is present; only the structural binding is missing (Toolkit §2 B.1).
2. **Problem:** Auditability score critically low (0/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without numbered, traceable obligations, a PDCA auditor has no objective basis to verify compliance — compliance claims rest on assertions rather than verifiable evidence. External audit cannot proceed.
   - **Concrete fix:** Address the 5 missed signals for this dimension. Critical gaps: multiple mandatory obligations (shall/must pairs), numbered traceable requirements, evidence / documentation requirements. Full signal breakdown in the Scores section.
3. **Problem:** Structural governance architecture score critically low (12/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 8 missed signals for this dimension. Critical gaps: numbered sub-requirements, mandatory obligation language (shall), risk stratification / proportionality. Full signal breakdown in the Scores section.
4. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
5. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-auditability-obligations-not-checkable-or
  - **finding_type:** auditability_gap
  - **severity:** medium
  - **diagnostic_gap:** auditability — obligations not checkable or traceable
  - **recommended_patch:** Require evidence artifacts for the finding, including named records, retention location, reviewer role, and update cadence.
  - **operational_control:** Require evidence capture in a repository with citation, date, responsible actor, and reviewer confirmation.
  - **evidence_artifact:** Evidence packet containing source excerpt, record location, reviewer, date, and retention rule.
  - **verification_test:** Create a verification test that samples this evidence control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Internal audit or compliance evidence owner
  - **Evidence trace IDs:** LAIF-TRACE-13-governance-force-signal
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-enforceability-insufficient-mandatory-oper
  - **finding_type:** enforceability_gap
  - **severity:** medium
  - **diagnostic_gap:** enforceability — insufficient mandatory operational requirements
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: enforceability — insufficient mandatory operational requirements
  - **operational_control:** Maintain a controlled obligation register that maps mandate text to owner, trigger, evidence, and review status.
  - **evidence_artifact:** Approved obligation register entry with source citation and control mapping.
  - **verification_test:** Create a verification test that samples this mandate control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 8: US Executive Order 14110 — §4 Safety & §7 Workers

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Document name      | US Executive Order 14110 — §4 Safety & §7 Workers                                                                                          |
| Source type        | executive_directive                                                                                                                        |
| Jurisdiction       | United States (Federal)                                                                                                                    |
| Sector             | General AI Governance                                                                                                                      |
| Assessment mode    | external_framework                                                                                                                         |
| Citation           | Executive Order 14110 on Safe, Secure, and Trustworthy AI (Oct 30, 2023)                                                                   |
| Source URL         | https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence |
| Provenance         | REPRESENTATIVE_EXCERPT                                                                                                                     |
| Document type      | executive_policy_directive                                                                                                                 |
| Original file name | not provided                                                                                                                               |
| Source SHA-256     | not provided                                                                                                                               |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a statement of values followed by a tasking list — named officials receive instructions and deadlines. It clearly names the things it exists to protect: people's fundamental rights, openness about how decisions are made, answerability for outcomes, human oversight of the system, matching rules to the size of the risk and more.

Trace who receives something in each operative sentence and a pattern appears: institutions receive duties, deadlines, and reporting obligations — but the people the document is about receive nothing they can hold. Protection exists here as intended future outcomes, not as present commitments to identifiable people; because promises and beneficiaries are never fastened together, individual provisions can erode without anyone being able to say a promise to them was broken.

It does give people a route to challenge decisions — a genuine person-facing protection, and the main exception to the pattern above.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: everything it creates can be modified or undone by its author's successor without any special safeguard.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| document_type                 | executive_policy_directive                                                                                                                                               |
| recommended_use               | Agency implementation planning, executive control mapping, and accountability-gap review.                                                                                |
| not_sufficient_for            | Not sufficient by itself as proof that agencies implemented, audited, or sustained the required controls.                                                                |
| governance_force_profile      | Executive policy directive with administrative force over named agencies or executive functions; implementation depends on agency ownership and follow-through controls. |
| systemic_repair_value         | Moderate                                                                                                                                                                 |
| operational_closure_rating    | Weak                                                                                                                                                                     |
| evidence_sufficiency_rating   | Moderate                                                                                                                                                                 |
| accountability_closure_rating | Limited                                                                                                                                                                  |
| lifecycle_control_rating      | Limited                                                                                                                                                                  |
| residual_risk_control_rating  | Limited                                                                                                                                                                  |
| implementation_gap_rating     | Limited                                                                                                                                                                  |
| failure_pathway_risk          | High                                                                                                                                                                     |
| priority_repair_actions       | assign accountable owner; define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review                                      |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Limited
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 20


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** assign accountable owner; define decision/release gate; add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** High
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Paraphrased and condensed from §4 (Safety/Security) and §7 (Workers); contains purpose-adapted wording including LAIF paraphrase test terms ('linkage', 'connection') to exercise paraphrase detection. Not verbatim.
- **Intended use:** real-world baseline with embedded paraphrase stress-test
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 50/100 — partial structural signal
- **Calibrated position:** 61% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 66/100
- **Sector risk alignment:** 100/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Structural strengths:** Expresses: human rights / fundamental interests; Expresses: transparency; Expresses: accountability; +17 more
- **Governance signal strength:** 50
- **Structural dimension score:** 35/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected            |
| ---------------- | ------- | ----------------------------------- |
| Coupling         | PARTIAL | restriction paired with named stake |
| Integrity Layer  | PARTIAL | meaningful account of outputs       |
| Consistency      | ABSENT  | none detected                       |
| Reversibility    | ABSENT  | none detected                       |
| Self-Application | ABSENT  | none detected                       |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                              | Missed signal labels                                                                                                                     |
| -------------------- | ------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 35/100 | numbered sub-requirements; mandatory obligation language (shall); risk stratification / proportionality; +2 more | full lifecycle scope declared; threshold gate conditions (all must pass simultaneously); non-amendable constitutional hierarchy; +2 more |
| Terminology          | 0/100  | none detected                                                                                                    | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                       |
| Conceptual proximity | 66/100 | human rights / fundamental interests; transparency; accountability; +5 more                                      | explainability / interpretability; reversibility / modifiability; risk governance; +1 more                                               |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms           | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                                      |
| Enforceability       | 80/100 | mandatory language (shall/must); named responsible parties; risk-proportionate thresholds; +1 more               | enforcement consequences / penalties                                                                                                     |
| Overall readiness    | 50/100 | partial structural signal                                                                                        | —                                                                                                                                        |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** partial structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 4 — High conceptual LAIF-model signal appears with low canonical terminology signal.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Possible keyword or signal density risk; requires structural evidence review. This is not a finding of bad faith and not a legal invalidity claim.; +1 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status           | Reviewer note                                                                                                    |
| ------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| protected interest | partial/implicit | Partial substance detected in the source text (one signal family).                                               |
| control            | partial/implicit | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| escalation         | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| consequence        | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| auditability       | detected         | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** General AI Governance
- **Sector profile key:** general_ai_governance
- **Profile-specific remediation themes:** Translate general governance principles into owners, triggers, protected interests, controls, evidence, escalation, and auditability.; Use LAIF-native terminology only for certification adoption, not external-framework validity claims.
- **Profile-specific evidence cautions:** General governance vocabulary does not prove compliance or legal validity.; Use reviewer-confirmation fallback when exact evidence text is absent.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: high-risk classification language; Risk signal present: accountability assignment; Risk signal present: transparency requirements; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 20
- **Exact/deterministic count:** 20
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)
- Terminology divergence (informational) — 'Coupling'-adjacent wording used in the document's own vocabulary (3 instance(s)): engage with industry, civil society, and other stakeholders …; orrection, and redress for affected individuals.  Section 7 …. Not a violation: this document does not use or claim LAIF canonical terminology.


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Restriction-protection pairing not established — no governance restriction is bound to the specific interest it protects, in any vocabulary.
   - **Why it matters:** Without structural Coupling, no governance restriction is paired with the specific human interest it protects. Each restriction can be weakened independently. Q1 (Coupling) failure = automatic failure of the full Coherence Test (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** For each restriction, name the specific interest it protects and bind the two together so that neither can be weakened without the other, with the protection as enforceable as the restriction. The document's own vocabulary is sufficient for the structure; the canonical form ('Coupling between [restriction] and [interest], with equivalent normative force' — Toolkit §2 B.1) is required only on the LAIF-native certification path, where an equivalence mapping is the alternative (Regulatory Integration Guide Part One).
2. **Problem:** Structural governance architecture score critically low (35/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 5 missed signals for this dimension. Critical gaps: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy. Full signal breakdown in the Scores section.
3. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
4. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.
5. **Problem:** Constitutional hierarchy not declared (structural score 35/100). Missing: full lifecycle scope declared, threshold gate conditions (all must pass simultaneously), non-amendable constitutional hierarchy.
   - **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   - **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-structural-transpar
  - **finding_type:** construct_gap
  - **severity:** medium
  - **diagnostic_gap:** Missing LAIF construct: Structural Transparency
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency
  - **operational_control:** Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.
  - **evidence_artifact:** Signed control procedure, exception log, and implementation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Institutional AI governance owner
  - **Evidence trace IDs:** LAIF-TRACE-03-sector-profile-signal, LAIF-TRACE-13-governance-force-signal
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 9: NHS England — AI in Clinical Decision Support (Policy Framework)

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------- |
| Document name      | NHS England — AI in Clinical Decision Support (Policy Framework)                          |
| Source type        | sector_policy                                                                             |
| Jurisdiction       | United Kingdom                                                                            |
| Sector             | Clinical AI Deployment                                                                    |
| Assessment mode    | external_framework                                                                        |
| Citation           | NHS England AI in Clinical Decision Support — Governance Framework (illustrative excerpt) |
| Source URL         | not provided                                                                              |
| Provenance         | REPRESENTATIVE_EXCERPT                                                                    |
| Document type      | procurement_assessment_form                                                               |
| Original file name | not provided                                                                              |
| Source SHA-256     | not provided                                                                              |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a sector instrument — operational requirements for a specific deployment context. It clearly names the things it exists to protect: openness about how decisions are made, explanations people can understand, human oversight of the system, safety.

It expresses a clear intention to protect people, but the promises are not fastened to the people they serve: a specific rule could be weakened or dropped without visibly breaking a commitment to any identifiable person.

It provides no route for an affected person to challenge or appeal an outcome — if the system gets it wrong for someone, this text gives them nothing to invoke.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: it gestures at correction and rollback, but not as a guaranteed capacity, and everything it creates can be undone by its author's successor.

To its credit, the administrative machinery is real: evidence and documentation duties, review and monitoring machinery, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                               |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| document_type                 | procurement_assessment_form                                                                                                         |
| recommended_use               | Procurement due diligence, supplier evidence requests, and contract-control design.                                                 |
| not_sufficient_for            | Not sufficient without contract terms, audit rights, verification evidence, and remedies.                                           |
| governance_force_profile      | Procurement assessment form; force arises through procurement conditions, contract clauses, supplier obligations, and audit rights. |
| systemic_repair_value         | Limited                                                                                                                             |
| operational_closure_rating    | Limited                                                                                                                             |
| evidence_sufficiency_rating   | Moderate                                                                                                                            |
| accountability_closure_rating | Moderate                                                                                                                            |
| lifecycle_control_rating      | Limited                                                                                                                             |
| residual_risk_control_rating  | Limited                                                                                                                             |
| implementation_gap_rating     | Limited                                                                                                                             |
| failure_pathway_risk          | Medium                                                                                                                              |
| priority_repair_actions       | add rollback/fallback control; document residual-risk acceptance and review                                                         |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Limited
- **Accountability closure:** Moderate
- **Lifecycle control:** Limited
- **Residual-risk closure:** Limited


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 20


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** add rollback/fallback control; document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** Medium
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Illustrative sector scenario: structured in the style of NHS England governance documentation but is not an official NHS England publication. Citation text confirms '(illustrative excerpt)'. For sector assessment demonstration only.
- **Intended use:** sector scenario — clinical AI governance
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 35/100 — limited structural signal
- **Calibrated position:** 43% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 31/100
- **Sector risk alignment:** 80/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present; conceptual — LAIF-like concepts insufficiently expressed
- **Structural strengths:** Expresses: transparency; Expresses: explainability / interpretability; Expresses: human oversight; +9 more
- **Governance signal strength:** 35
- **Structural dimension score:** 35/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected                                         |
| ---------------- | ------- | ---------------------------------------------------------------- |
| Coupling         | ABSENT  | none detected                                                    |
| Integrity Layer  | PARTIAL | meaningful account of outputs; bounded operation with escalation |
| Consistency      | ABSENT  | none detected                                                    |
| Reversibility    | PARTIAL | reversal capacity preserved                                      |
| Self-Application | ABSENT  | none detected                                                    |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                           | Missed signal labels                                                                                                 |
| -------------------- | ------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Structural           | 35/100 | mandatory obligation language (shall); full lifecycle scope declared; review / monitoring mechanisms; +1 more | numbered sub-requirements; risk stratification / proportionality; operational mechanisms defined; +3 more            |
| Terminology          | 0/100  | none detected                                                                                                 | Coupling; Coherence Test; Integrity Layer; +4 more                                                                   |
| Conceptual proximity | 31/100 | transparency; explainability / interpretability; human oversight; +1 more                                     | human rights / fundamental interests; accountability; proportionality; +5 more                                       |
| Auditability         | 40/100 | evidence / documentation requirements; review / monitoring mechanisms                                         | multiple mandatory obligations (shall/must pairs); numbered traceable requirements; specific, measurable obligations |
| Enforceability       | 60/100 | mandatory language (shall/must); named responsible parties; non-discretionary operational mandates            | risk-proportionate thresholds; enforcement consequences / penalties                                                  |
| Overall readiness    | 35/100 | limited structural signal                                                                                     | —                                                                                                                    |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** limited structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 5 — Sector risk alignment materially exceeds overall readiness.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Low LAIF-model signal may indicate missing LAIF-model signals, not legal invalidity under the source framework's own authority.; +2 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status                | Reviewer note                                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| protected interest | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected              | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit      | Partial substance detected in the source text (one signal family).                                               |
| escalation         | partial/implicit      | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| consequence        | gap / requires review | Source-text gaps or missed signals indicate this component requires reviewer confirmation or remediation.        |
| auditability       | detected              | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** Clinical AI Deployment
- **Sector profile key:** clinical_ai
- **Profile-specific remediation themes:** Assign a clinical governance owner with clinician reviewer and safety incident pathway.; Require clinical fallback, override record, patient safety review, and incident log.; Keep clinical source-evidence claims tied to exact text.
- **Profile-specific evidence cautions:** Clinical vocabulary does not determine medical, regulatory, or legal validity.; Do not invent clinical validation, fallback, override, patient safety review, or incident evidence.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: clinical decision output; Risk signal present: patient safety signal; Risk signal present: diagnostic / treatment language; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 20
- **Exact/deterministic count:** 20
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Implicit protective signals present but not declared as structural Coupling.
   - **Why it matters:** The document already expresses protective intent — detected: «2 Patients have the right to request a human clinician review of any AI-assisted clinical recomm». However, implicit intent does not constitute structural Coupling: the protection can be removed without affecting the obligation it was meant to serve. The upgrade required is structural, not conceptual (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** Convert each detected implicit signal into an explicit Coupling declaration: 'Coupling between [the restriction already present] and [the specific human interest the detected protective language names], with equivalent normative force on both sides — neither may be weakened in isolation.' The governance intent is present; only the structural binding is missing (Toolkit §2 B.1).
2. **Problem:** Conceptual governance coverage score critically low (31/100) — most deficient dimension after Coupling.
   - **Why it matters:** Low conceptual proximity indicates the document's governance intent is not substantially aligned with LAIF values. The adoption gap is more fundamental than terminology — substantive governance redesign is required, not just terminological substitution.
   - **Concrete fix:** Address the 8 missed signals for this dimension. Critical gaps: human rights / fundamental interests, accountability, proportionality. Full signal breakdown in the Scores section.
3. **Problem:** Structural governance architecture score critically low (35/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 6 missed signals for this dimension. Critical gaps: numbered sub-requirements, risk stratification / proportionality, operational mechanisms defined. Full signal breakdown in the Scores section.
4. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
5. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-conceptual-laif-like-concepts-insufficient
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** conceptual — LAIF-like concepts insufficiently expressed
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: conceptual — LAIF-like concepts insufficiently expressed
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.
  - **evidence_artifact:** Clinical fallback, override record, patient safety review, incident log, or clinical governance record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** Clinical governance owner with clinician reviewer and safety incident pathway
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


### Document 10: TUC/CIPD — Framework for Fair AI in Employment Decisions

#### Document Overview

##### Assessment Scope
| Field              | Value                                                                           |
| ------------------ | ------------------------------------------------------------------------------- |
| Document name      | TUC/CIPD — Framework for Fair AI in Employment Decisions                        |
| Source type        | sector_policy                                                                   |
| Jurisdiction       | United Kingdom                                                                  |
| Sector             | Employment and HR AI                                                            |
| Assessment mode    | external_framework                                                              |
| Citation           | Illustrative AI in Employment Governance Framework (sector assessment document) |
| Source URL         | not provided                                                                    |
| Provenance         | REPRESENTATIVE_EXCERPT                                                          |
| Document type      | public_sector_policy                                                            |
| Original file name | not provided                                                                    |
| Source SHA-256     | not provided                                                                    |


#### Plain-Language Reading (framework-free)
*What the measurements found, stated without any of this framework's vocabulary. Each statement is generated from a specific fired or missed signal — none of it is editorial.*

In plain terms, this document is a sector instrument — operational requirements for a specific deployment context. It clearly names the things it exists to protect: openness about how decisions are made, explanations people can understand, answerability for outcomes, the ability to challenge decisions, fairness and non-discrimination.

It expresses a clear intention to protect people, but the promises are not fastened to the people they serve: a specific rule could be weakened or dropped without visibly breaking a commitment to any identifiable person.

It does give people a route to challenge decisions — a genuine person-facing protection, and the main exception to the pattern above.

Nothing in it binds the author — it sets requirements for others but none that the issuing authority itself must pass — and nothing anchors it in time: it gestures at correction and rollback, but not as a guaranteed capacity, and everything it creates can be undone by its author's successor.

To its credit, the administrative machinery is real: numbered, traceable requirements, evidence and documentation duties, review and monitoring machinery, genuinely mandatory language with named owners. Whether its tasks were done is checkable — a property many governance documents lack.

**Fair summary:** real machinery, real intent, and some of the deeper protective architecture — but not all of it. That is not a judgement that the document fails at its own job. It means that if you relied on this text alone to guarantee a specific person protection from a specific harm, parts of that load path are missing.


#### Governance Repair Profile
| Field                         | Value                                                                                                                                                                                            |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| document_type                 | public_sector_policy                                                                                                                                                                             |
| recommended_use               | Public-sector operating policy review, government AI use register design, disclosure/control mapping, and accountability-gap review.                                                             |
| not_sufficient_for            | Not sufficient without accountable owners, human-review evidence, disclosure records, exception handling, incident tracking, and monitoring consequences.                                        |
| governance_force_profile      | Public-sector AI policy; force depends on government authority, accountable public-sector owners, disclosure records, human review evidence, exceptions, incidents, and monitoring consequences. |
| systemic_repair_value         | Limited                                                                                                                                                                                          |
| operational_closure_rating    | Weak                                                                                                                                                                                             |
| evidence_sufficiency_rating   | Moderate                                                                                                                                                                                         |
| accountability_closure_rating | Moderate                                                                                                                                                                                         |
| lifecycle_control_rating      | Limited                                                                                                                                                                                          |
| residual_risk_control_rating  | Moderate                                                                                                                                                                                         |
| implementation_gap_rating     | Limited                                                                                                                                                                                          |
| failure_pathway_risk          | Medium                                                                                                                                                                                           |
| priority_repair_actions       | document residual-risk acceptance and review                                                                                                                                                     |
This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.


#### Operational Closure Findings
- **Operational closure:** Weak
- **Accountability closure:** Moderate
- **Lifecycle control:** Limited
- **Residual-risk closure:** Moderate


#### Evidence Sufficiency Findings
- **Evidence sufficiency:** Moderate
- **Evidence trace count:** 19


#### Implementation Gap Findings
- **Implementation gap rating:** Limited
- **Priority repair actions:** document residual-risk acceptance and review


#### Failure-Pathway Risk Findings
- **Failure-pathway risk:** Medium
- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.


##### Provenance / Source Basis
- **Source note:** Illustrative sector scenario: written in the style of TUC/CIPD employment AI guidance but is not an official publication of either body. Citation text confirms 'Illustrative...sector assessment document'. For sector assessment demonstration only.
- **Intended use:** sector scenario — employment AI governance
- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.


#### Mode / Boundary Notice
Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.
Assessment mode: external_framework. This public report is diagnostic, not certification for external-framework sources; it does not determine legal validity and cannot override formal LAIF-native failure. Evidence traces identify source-text support for LAIF-model signals only; reviewer confirmation required for source authority, implementation, and institutional or regulator effect. Score bands are interpretive readiness bands, not determinations of compliance.
Public status label: **Governance repair assessment — external-framework diagnostic.**


#### Executive Diagnostic Summary
This source does not pass the formal LAIF-native certification gate under LAIF criteria; external framework assessment remains diagnostic and does not determine legal validity.
- **Overall readiness:** 39/100 — limited structural signal
- **Calibrated position:** 48% of the 81.5-point ceiling achievable without LAIF-native branding. Raw scores compress on this instrument: 18.5 points are reserved for LAIF-branded documents, and lexical detection is conservative — read the calibrated figure, the functional alignment verdict, and the score band together, never the raw number as a percentage grade.
- **Conceptual proximity:** 41/100
- **Sector risk alignment:** 60/100
- **Remediation effort:** HIGH
- **Primary structural gaps:** structural — constitutional hierarchy not declared; terminological — no canonical LAIF terms present
- **Structural strengths:** Expresses: transparency; Expresses: explainability / interpretability; Expresses: accountability; +12 more
- **Governance signal strength:** 39
- **Structural dimension score:** 28/100
- **Position assessment:** diagnostic under the assessment model, not certification.
- **Functional alignment:** PARTIALLY ALIGNED — some LAIF constructs present in substance or in form


#### Functional Alignment (Substance Independent of Vocabulary)
DECLARED = LAIF-native form; FUNCTIONAL = substance present in the document's own vocabulary (≥2 independent signal families); PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; Regulatory Integration Guide Part One.
| Construct        | Verdict | Signal families detected      |
| ---------------- | ------- | ----------------------------- |
| Coupling         | ABSENT  | none detected                 |
| Integrity Layer  | PARTIAL | meaningful account of outputs |
| Consistency      | ABSENT  | none detected                 |
| Reversibility    | PARTIAL | reversal capacity preserved   |
| Self-Application | ABSENT  | none detected                 |


#### Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage
Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.
LAIF-native certification: Not claimed / not applicable to this external-framework assessment.


#### Scorecard
Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.
| Dimension            | Score  | Fired signal labels                                                                                       | Missed signal labels                                                                                                                    |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Structural           | 28/100 | numbered sub-requirements; mandatory obligation language (shall); operational mechanisms defined; +1 more | full lifecycle scope declared; risk stratification / proportionality; threshold gate conditions (all must pass simultaneously); +3 more |
| Terminology          | 0/100  | none detected                                                                                             | Coupling; Coherence Test; Integrity Layer; +4 more                                                                                      |
| Conceptual proximity | 41/100 | transparency; explainability / interpretability; accountability; +2 more                                  | human rights / fundamental interests; human oversight; proportionality; +4 more                                                         |
| Auditability         | 60/100 | numbered traceable requirements; evidence / documentation requirements; review / monitoring mechanisms    | multiple mandatory obligations (shall/must pairs); specific, measurable obligations                                                     |
| Enforceability       | 60/100 | mandatory language (shall/must); named responsible parties; non-discretionary operational mandates        | risk-proportionate thresholds; enforcement consequences / penalties                                                                     |
| Overall readiness    | 39/100 | limited structural signal                                                                                 | —                                                                                                                                       |


#### Score Calibration and Justification
Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.
- **Overall band:** limited structural signal
- **Formal LAIF-native status:** FAIL
- **Interpretation boundary:** Formal LAIF-native failure cannot be overridden by high proximity scores.
- **Calibration / anti-gaming cautions:** 4 — Sector risk alignment materially exceeds overall readiness.; Multiple evidence traces are present while formal LAIF-native compliance remains failed.; Low LAIF-model signal may indicate missing LAIF-model signals, not legal invalidity under the source framework's own authority.; +1 more
- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.


#### Governance-Force Profile
| Component          | Status           | Reviewer note                                                                                                    |
| ------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| mandate            | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| actor              | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| trigger            | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| protected interest | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| control            | partial/implicit | Partial substance detected in the source text (one signal family).                                               |
| evidence           | detected         | Source-text signals indicate this component is present or directly supported.                                    |
| reversibility      | partial/implicit | Partial substance detected in the source text (one signal family).                                               |
| escalation         | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| consequence        | partial/implicit | Source-text signals suggest the component may be present, but the report does not treat it as fully established. |
| auditability       | detected         | Source-text signals indicate this component is present or directly supported.                                    |


#### Sector / Institutional Context
- **Sector profile:** Employment and HR AI
- **Sector profile key:** employment_hr_ai
- **Profile-specific remediation themes:** Assign an HR policy owner with legal/compliance and bias-review support.; Require adverse-action review, bias evidence, human review, and appeal records.; Distinguish worker-protection governance from AI surveillance vocabulary.
- **Profile-specific evidence cautions:** Do not infer employment-law compliance or legal validity from HR terminology.; Do not generate bias or adverse-action evidence unless exact source text exists.
- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.
- **Sector diagnostic findings:** Risk signal present: employment lifecycle decision; Risk signal present: worker population; Risk signal present: performance assessment; +7 more


#### Evidence Trace Summary
Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.
- **Total traces:** 19
- **Exact/deterministic count:** 19
- **Fallback count:** 0
- **Evidence trace IDs:** LAIF-TRACE-01-sector-profile-signal (sector_profile_signal); LAIF-TRACE-02-sector-profile-signal (sector_profile_signal); LAIF-TRACE-03-sector-profile-signal (sector_profile_signal)
- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.


#### Construct Crosswalk
No LAIF-native constructs detected — expected for an external instrument; see the Functional Alignment table for substance detected in the document's own vocabulary.
Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.


#### Diagnostic Gaps
- LAIF-native vocabulary not used — expected for an external instrument; certification-channel distance, not a deficiency: Coupling, Coherence Test, Integrity Layer, Structural Transparency, Structural Honesty, Structural Containment, Materially Affects Interests
- Structural mechanism not detected in any vocabulary: threshold gate conditions (all must pass simultaneously)
- Structural mechanism not detected in any vocabulary: non-amendable constitutional hierarchy
- Structural mechanism not detected in any vocabulary: self-application clause (Part Seven)
- LAIF-native marker not present (branding, not substance): named decision instrument (Coherence Test / PDCA)


#### Remediation Priorities
LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.

##### Structured remediation details
1. **Problem:** Implicit protective signals present but not declared as structural Coupling.
   - **Why it matters:** The document already expresses protective intent — detected: «gnate an individual responsible for compliance with this framework. This individual shall have». However, implicit intent does not constitute structural Coupling: the protection can be removed without affecting the obligation it was meant to serve. The upgrade required is structural, not conceptual (LAIF v1.2 Principle 2; Toolkit §2 B.1).
   - **Concrete fix:** Convert each detected implicit signal into an explicit Coupling declaration: 'Coupling between [the restriction already present] and [the specific human interest the detected protective language names], with equivalent normative force on both sides — neither may be weakened in isolation.' The governance intent is present; only the structural binding is missing (Toolkit §2 B.1).
2. **Problem:** Structural governance architecture score critically low (28/100) — most deficient dimension after Coupling.
   - **Why it matters:** Without a constitutional hierarchy, operational revisions can alter the governance standard without triggering a constitutional amendment — foundational protections are not locked against erosion over time.
   - **Concrete fix:** Address the 6 missed signals for this dimension. Critical gaps: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously). Full signal breakdown in the Scores section.
3. **Problem:** Coherence Test not applied — no Q1/Q2/Q3 documentation present.
   - **Why it matters:** The Coherence Test is the primary LAIF decision instrument: Q1 Coupling (specific human interest identified and protected?), Q2 Consistency (governance logic scale-invariant?), Q3 Reversibility (future actors can modify?). Without it, there is no evidence provisions were tested for structural soundness before deployment (LAIF v1.2 Part One).
   - **Concrete fix:** Add PDCA Section B: apply all three Coherence Test questions to each major governance provision. Each must be answered affirmatively. Q1 failure = full failure — do not proceed to Q2/Q3 without satisfying Q1 (LAIF v1.2 Part One; Toolkit §2).
4. **Problem:** No all-conditions-must-pass deployment gate — deployment is not conditioned on transparency, honesty, and containment being simultaneously satisfied.
   - **Why it matters:** Without a threshold gate, a system can be deployed while any of the three core preconditions is unmet: the ability to account for its outputs, the correspondence of stated to implemented objectives, and operation within documented boundaries. Partial satisfaction functioning as approval is the single most common structural failure this model detects (LAIF v1.2 Part Two).
   - **Concrete fix:** Establish a deployment gate with three conditions that must all hold simultaneously — (i) the system can produce a meaningful account of any output that materially affects a person; (ii) stated objectives correspond to implemented objectives, verified by independent review; (iii) the system operates within documented boundaries in all tested conditions, escalating out-of-scope cases. The document's own vocabulary is sufficient; the canonical form is the Integrity Layer (Toolkit §1.3–§1.5), required only on the LAIF-native certification path.
5. **Problem:** Constitutional hierarchy not declared (structural score 28/100). Missing: full lifecycle scope declared, risk stratification / proportionality, threshold gate conditions (all must pass simultaneously).
   - **Why it matters:** Without a non-amendable three-tier hierarchy, operational revisions can erode Foundational Principles. LAIF's structure — Foundational Principles (non-amendable) → Provisions → Operational Standards — prevents governance degradation over time (LAIF v1.2 Principle 3).
   - **Concrete fix:** Declare the three-tier hierarchy explicitly: (i) PART ONE: Foundational Principles — non-amendable; (ii) Provisions derived from Principles; (iii) Operational Standards — subordinate and revisable. Add a non-amendable clause, self-application clause (Part Seven), and threshold gate conditions for the Integrity Layer precondition (LAIF v1.2 Parts One, Two, Seven).

#### Structured Remediation Patch Set
These patches are diagnostic LAIF remediation guidance. They do not determine legal validity or certify LAIF-native compliance unless separately adopted and verified.
Showing the 6 highest-priority patches of 12; the full set is available in the JSON assessment output.
- **patch_id:** LAIF-PATCH-01-structural-constitutional-hierarchy-not-de
  - **finding_type:** governance_force_gap
  - **severity:** medium
  - **diagnostic_gap:** structural — constitutional hierarchy not declared
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: structural — constitutional hierarchy not declared
  - **operational_control:** Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls.
  - **evidence_artifact:** Adverse-action review, bias evidence, human review/appeal record, or accommodation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** HR policy owner with legal/compliance and bias-review support
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-02-terminological-no-canonical-laif-terms-pre
  - **finding_type:** terminology_gap
  - **severity:** medium
  - **diagnostic_gap:** terminological — no canonical LAIF terms present
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: terminological — no canonical LAIF terms present
  - **operational_control:** Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls.
  - **evidence_artifact:** Adverse-action review, bias evidence, human review/appeal record, or accommodation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** HR policy owner with legal/compliance and bias-review support
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-03-missing-laif-construct-coupling
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coupling
  - **recommended_patch:** Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.
  - **operational_control:** Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls.
  - **evidence_artifact:** Adverse-action review, bias evidence, human review/appeal record, or accommodation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** HR policy owner with legal/compliance and bias-review support
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-04-missing-laif-construct-coherence-test
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Coherence Test
  - **recommended_patch:** Define a documented Coherence Test workflow that applies Coupling, Consistency, and Reversibility checks before the relevant decision or deployment trigger.
  - **operational_control:** Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls.
  - **evidence_artifact:** Adverse-action review, bias evidence, human review/appeal record, or accommodation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** HR policy owner with legal/compliance and bias-review support
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-05-missing-laif-construct-integrity-layer
  - **finding_type:** construct_gap
  - **severity:** high
  - **diagnostic_gap:** Missing LAIF construct: Integrity Layer
  - **recommended_patch:** Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.
  - **operational_control:** Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls.
  - **evidence_artifact:** Adverse-action review, bias evidence, human review/appeal record, or accommodation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** HR policy owner with legal/compliance and bias-review support
  - **Evidence trace IDs:** reviewer confirmation required / none linked
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.
- **patch_id:** LAIF-PATCH-06-missing-laif-construct-structural-transpar
  - **finding_type:** construct_gap
  - **severity:** medium
  - **diagnostic_gap:** Missing LAIF construct: Structural Transparency
  - **recommended_patch:** Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency
  - **operational_control:** Map HR AI decisions to adverse-action review, bias testing evidence, human review, appeal, and escalation controls.
  - **evidence_artifact:** Adverse-action review, bias evidence, human review/appeal record, or accommodation record.
  - **verification_test:** Create a verification test that samples this control control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status.
  - **responsible_actor:** HR policy owner with legal/compliance and bias-review support
  - **Evidence trace IDs:** LAIF-TRACE-09-governance-force-signal
  - **legal_authority_boundary:** diagnostic_only
  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.


#### Limits and Reviewer Actions
- confirm source authority and provenance before relying on any institutional interpretation
- verify evidence artifacts and implementation records outside this text-only diagnostic output
- assign accountable owners for accepted remediation patches
- confirm escalation, reversibility, and appeal controls where the source affects people or protected interests
- determine whether institution, regulator, contract, or governing body has authority to adopt any change
- treat this report as diagnostic, not certification, and not a legal validity determination
- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure


## Closing Interpretation Notes
- Public reports are diagnostics only and require evidence/authority review before institutional use.
- Reviewer confirmation required for source authority, implementation evidence, accountable ownership, and legal or contractual effect.
- Formal LAIF-native failure remains formal failure; high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.
- This report does not determine legal validity and does not provide legal advice.
- Raw regex patterns are not disclosed; only report-safe signal labels and summaries are rendered.

---
*LAIF v1.2 · Compliance Toolkit v1.1 · July 2026 · Public Report Template*  
*Generated by `test_real_world.py`; scoring logic, rubric weights, formal compliance calculation, certification gates, and validate.py enforcement unchanged.*