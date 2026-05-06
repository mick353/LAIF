# LAIF FULL CORPUS ASSESSMENT
**Framework:** Law-Aligned Intelligence Framework v1.2 (April 2026)
**Model version:** Refined Model v1.1
**Assessment date:** 5 May 2026
**Instruments assessed:** 4 ingested governance documents
**Assessment basis:** LAIF v1.2 principal text and Schedules A–D; all source content from ingested files only
**Self-application basis:** LAIF v1.2 §7.4 — the Coherence Test applies to regulatory bodies and governance actors themselves

---

## UPDATED COMPARISON TABLE — REFINED MODEL v1.1

| Dimension | EO 14110 | NIST AI RMF | OECD Rec. | DTAC v2.0 |
|---|---|---|---|---|
| **Q1a — Structural Pairing** | EXPLICIT | EXPLICIT | EXPLICIT | EXPLICIT (C1–C4) / IMPLICIT (D1) |
| **Q1b — Enforcement Strength** | NONE | NONE | SOFT | HARD |
| **Q2 — Consistency** | PARTIAL PASS | PASS | PASS | CONDITIONAL PASS |
| **Q3 — Reversibility** | CONDITIONAL PASS | PASS | PASS | PASS |
| **Governance Durability** | FRAGILE | ADAPTIVE | STABLE | BOUNDED |
| **Reflexivity** | PARTIAL | NONE | PARTIAL | NONE |
| **A.1 Structural Transparency** | Weak | Strong | Strong | Moderate |
| **A.2 Structural Honesty** | Moderate | Strong | Moderate | Strong |
| **A.3 Structural Containment** | Weak | Moderate | Strong | Moderate |
| **Discrimination/bias coverage** | Partial | Strong | Strong | Absent |
| **Enforceable rights for affected persons** | None (§13c explicit) | None by design | None by instrument type | Partial (UK GDPR + procurement bar) |
| **Post-deployment obligations** | Partial | Yes | Partial | No |

---

## ASSESSMENT 1 — OECD RECOMMENDATION (OECD/LEGAL/0449)
**Adopted 22 May 2019 | Amended 03 May 2024**

---

### SECTION A — INTEGRITY LAYER CROSS-REFERENCE

**A.1 Structural Transparency — STRONG**

OECD Principle 1.3 (Transparency and explainability) requires AI actors to provide:

> "(iii) where feasible and useful, to provide plain and easy-to-understand information on the sources of data/input, factors, processes and/or logic that led to the prediction, content, recommendation or decision, to enable those affected by an AI system to understand the output, and (iv) to provide information that enable those adversely affected by an AI system to challenge its output."

This is the closest parallel to LAIF v1.2 §2.1 in any of the four assessed instruments. LAIF §2.1 requires that a meaningful account be "comprehensible to a person without specialist technical knowledge" and "identify the principal factors that influenced the output with sufficient specificity that the affected person can assess whether those factors are accurate in their case." Principle 1.3(iii) uses functionally identical language ("plain and easy-to-understand"; "to enable those affected... to understand the output").

The gap is procedural, not substantive. LAIF §2.1 establishes an on-request trigger — a deploying operator must be able to demonstrate, on request by a regulator or affected person, that the system can produce a meaningful account. The Recommendation directs AI actors to provide this information but does not establish the procedural trigger as an externally enforceable right.

**Cross-reference finding:** Strong conceptual alignment. Operationalisation gap at the procedural trigger level.

**A.2 Structural Honesty — MODERATE**

Principle 1.3 requires disclosure of "capabilities and limitations." Principle 1.5 (Accountability) requires traceability "in relation to datasets, processes and decisions made during the AI system lifecycle, to enable analysis of the AI system's outputs and responses to inquiry." The 2024 amendment explicitly adds "addressing misinformation and disinformation amplified by AI, while respecting freedom of expression."

These provisions address the disclosure and non-deception dimensions of LAIF v1.2 §2.2 (Structural Honesty). The LAIF requirement that systems not "pursue objectives undisclosed to its principal hierarchy" and that "stated optimisation objectives correspond to actual implemented objectives" has no direct parallel in the Recommendation. The Recommendation addresses what AI systems communicate outward; it does not address the correspondence between stated and implemented objectives.

**Cross-reference finding:** Moderate. Disclosure addressed; objective correspondence gap.

**A.3 Structural Containment — STRONG**

Principle 1.2(b): "AI actors should implement mechanisms and safeguards, such as capacity for human agency and oversight, including to address risks arising from uses outside of intended purpose, intentional misuse, or unintentional misuse in a manner appropriate to the context and consistent with the state of the art."

Principle 1.4(b): "Mechanisms should be in place, as appropriate, to ensure that if AI systems risk causing undue harm or exhibit undesired behaviour, they can be overridden, repaired, and/or decommissioned safely as needed."

Principle 1.4(b) is the interrupt mechanism requirement of LAIF v1.2 §2.3 stated in principle — it is the clearest containment language in any of the four assessed instruments. The LAIF §2.3 requirements for agentic systems (scope limitation mechanisms, action logging, interrupt mechanisms) have no direct parallel, but the override and decommission requirement is substantively present.

**Cross-reference finding:** Strong on interrupt mechanism principle. Gap on agentic system-specific requirements.

---

### SECTION B — COHERENCE TEST DOCUMENTATION

**Q1a — STRUCTURAL PAIRING: EXPLICIT**

The OECD Recommendation has the most explicitly rights-oriented coupling architecture of the four instruments. Each of the five principles directly names the human interest it protects — those interests are the stated objects of the principles, not secondary considerations:

- Principle 1.1: "welfare and well-being of people," "inclusive growth," "reducing economic, social, gender and other inequalities"
- Principle 1.2: "rule of law, human rights, democratic and human-centred values," then individually: "non-discrimination and equality, freedom, dignity, autonomy of individuals, privacy and data protection, diversity, fairness, social justice, and internationally recognised labour rights"
- Principle 1.3: the ability of persons to understand AI outputs; the ability of "those adversely affected by an AI system to challenge its output"
- Principle 1.4: safety of persons; the ability to override and decommission harmful systems
- Principle 1.5: accountability for proper functioning; traceability to enable inquiry by affected parties

The 2024 amendment strengthened Principle 1.5 to require "a systematic risk management approach to each phase of the AI system lifecycle on an ongoing basis and adopt responsible business conduct to address risks related to AI systems, including, as appropriate, via co-operation between different AI actors." This is substantive coupling: the risk management obligation is paired with protecting "risks related to harmful bias, human rights including safety, security, and privacy, as well as labour and intellectual property rights."

LAIF v1.2 Q1: "Does this proposed action or policy identify and protect the specific human interest — the freedom, safety, dignity, or participatory capacity — that the action or policy is designed to serve?" The Recommendation satisfies this completely. The structural pairing is explicit throughout.

**Q1a finding: EXPLICIT.**

---

**Q1b — ENFORCEMENT STRENGTH: SOFT**

The Recommendation uses "should" throughout — not "must," "shall," or "are required to." The Background section confirms: the instrument "aims to foster innovation and trust in AI by promoting the responsible stewardship of trustworthy AI." Operative verbs are "fostering," "promoting," and "recommending."

Adherents commit through political agreement at ministerial level. Enforcement is through Section VIII's review mechanism: the Digital Policy Committee is instructed to "report to Council... on the implementation, dissemination and continued relevance of this Recommendation no later than five years following its revision." This is implementation review, not compliance enforcement. An adherent that fails to implement Principle 1.3 faces no legal or market consequence.

LAIF v1.2 §2.4 defines equivalent normative force as requiring enforceable rights accessible to affected persons with enforcement mechanisms as accessible and effective as those available to enforce the constraint. Against this standard, both sides of the Recommendation's coupling operate through the same political accountability channel — SOFT on both sides, but symmetric.

The SOFT classification reflects the Recommendation's role as the upstream principled architecture instrument. It is designed to generate the coupling template that national legislation, sector standards, and operational frameworks implement with binding force.

**Q1b finding: SOFT.**

---

**Q2 — Consistency: PASS**

The Recommendation applies explicitly to "all stakeholders" and "all AI actors" — universally, without carve-outs by size, sector, or jurisdiction. Principle 1.5 calibrates by "their roles, the context, and consistent with the state of the art" — preserving proportionality without abandoning the underlying governance logic.

Applied at smaller scale: the reasoning that justifies transparency requirements for a large foundation model provider applies equally to a small organisation deploying a single AI tool. Applied at larger scale: the five principles' adoption at G20 Osaka 2019 as the G20 AI Principles demonstrates that the reasoning survived application at geopolitical scale.

The 2024 amendments were specifically motivated by implementation review findings. The Background section confirms: "The 2024 Report concluded that the Recommendation provides a significant and useful international reference in national AI policymaking. The Recommendation is being implemented by its Adherents, is widely disseminated, and remains fully relevant, including as a solid framework to analyse technology evolutions such as those related to generative AI."

**Q2 finding: PASS.**

---

**Q3 — Reversibility: PASS**

Section VIII(d) mandates: "report to Council, in consultation with other relevant committees, on the implementation, dissemination and continued relevance of this Recommendation no later than five years following its revision and at least every ten years thereafter."

In practice the revision cycle has been faster than mandated: adopted May 2019, amended November 2023, amended May 2024. The Recommendation does not create permanent institutional structures, vested regulatory interests, or technical lock-in. Adherents can adjust national implementation without requiring amendment of the international instrument.

**Q3 finding: PASS.**

---

### SECTION C — NEW DIMENSIONS

**GOVERNANCE DURABILITY: STABLE**

The Recommendation is institutionally anchored by 48 adherents: all 38 OECD member states plus non-members including Argentina, Brazil, Egypt, Singapore, Ukraine, Uruguay, Saudi Arabia, and the European Union (adhered 03 May 2024). The Working Party on AI Governance (AIGO) and the OECD.AI Policy Observatory provide permanent secretariat infrastructure. Adoption at G20 Osaka 2019 created cross-institutional propagation. The combination of 48 adherents, permanent AIGO Working Party, mandated review cycle, and demonstrated three-revision history in five years constitutes STABLE governance durability — designed for long-term institutional maintenance, not fragile to single-actor political reversal.

**REFLEXIVITY (SELF-APPLICATION): PARTIAL**

Section VIII instructs the Digital Policy Committee to "continue its important work on artificial intelligence building on this Recommendation." Section 2.5 applies to "Governments... including developing countries and with stakeholders." The OECD, as an institution that deploys AI in analytical and policy work, falls within the Recommendation's own definition of "AI actors" — "those who play an active role in the AI system lifecycle." However, no mechanism exists for assessing whether the OECD Secretariat satisfies the principles it recommends. The governing body is not shielded from the principles, but no explicit self-accountability mechanism exists. Classification: PARTIAL.

---

### SECTION D — PROVISION LAYER COMPLIANCE

| LAIF Provision | Status | Textual Basis |
|---|---|---|
| A1 — Meaningful account on request | ADDRESSED | Principle 1.3(iii)(iv): plain information + right to challenge outputs |
| A2 — Right to know AI involvement | ADDRESSED | Principle 1.3(ii): stakeholders made aware of AI interactions |
| B1 — Mass casualty prohibition | NOT ADDRESSED | No provision |
| B2 — Discrimination prohibition | ADDRESSED | Principle 1.2: non-discrimination and equality explicitly named as protected interests |
| B3 — Power concentration | PARTIAL | Principle 1.1: reducing inequalities; no explicit concentration provision |
| C1 — Oversight mechanisms | ADDRESSED | Principle 1.2(b): human agency and oversight mechanisms required |
| C2 — No deception of oversight | PARTIAL | Principle 1.5: traceability required; no explicit prohibition on deception |
| D1 — Irreversible actions | PARTIAL | Principle 1.4(b): override, repair, decommission mechanisms required |
| D2 — Governance revisability | PASS | Mandated review cycle; three amendments in five years |

---

### OVERALL VERDICT — OECD RECOMMENDATION

| Dimension | Result |
|---|---|
| Q1a Structural Pairing | **EXPLICIT** |
| Q1b Enforcement Strength | **SOFT** |
| Q2 Consistency | **PASS** |
| Q3 Reversibility | **PASS** |
| Governance Durability | **STABLE** |
| Reflexivity | **PARTIAL** |

The OECD Recommendation is the upstream principled architecture instrument. Its structural pairing is the most explicit, its consistency and reversibility are clean passes, and its institutional durability is the strongest of the four. Its enforcement is SOFT by design — the instrument is positioned to generate the coupling template that binding national and sector-specific instruments implement with hard force. DTAC's HARD enforcement is the downstream operational expression of the architecture the OECD Recommendation provides at the principled level.

---

## ASSESSMENT 2 — EXECUTIVE ORDER 14110
**"Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence"**
**October 30, 2023 | Federal Register Vol. 88 No. 210**

---

### SECTION A — INTEGRITY LAYER CROSS-REFERENCE

**A.1 Structural Transparency — WEAK**

EO 14110 §4.1(a)(i)(C) directs NIST to launch "an initiative to create guidance and benchmarks for evaluating and auditing AI capabilities." §4.5 addresses synthetic content labelling and watermarking. §10.1(b)(viii) directs OMB guidance to include "recommendations to agencies regarding external testing, safeguards against discriminatory outputs, watermarking, application of risk-management practices, independent evaluation, documentation."

The order gestures toward transparency requirements but does not operationalise them. It directs agencies to develop guidance rather than establishing transparency obligations directly. No provision creates a mechanism by which a person affected by a federal agency's AI system can obtain "a comprehensible account of the basis on which those outputs were generated" (LAIF v1.2 §2.1). §10.1(b)(v) requires agencies to identify "specific Federal Government uses of AI that are presumed by default to impact rights or safety" — this is precursor infrastructure for transparency, not transparency itself.

**Cross-reference finding:** Weak. The order creates the institutional mandate to develop transparency infrastructure but does not itself constitute transparency operationalisation under LAIF §2.1.

**A.2 Structural Honesty — MODERATE**

EO 14110 §4.2(a)(i)(C) requires companies to report "the results of any developed dual-use foundation model's performance in relevant AI red-team testing" and "a description of any associated measures the company has taken to meet safety objectives." Red-team testing disclosure is directly relevant to LAIF §2.2: Structural Honesty requires that performance is consistent under adversarial conditions and that capability limitations are disclosed.

§4.6 addresses dual-use foundation models with widely available weights, directing consultation on "potential risks, benefits, other implications, and appropriate policy and regulatory approaches." This is relevant to honest disclosure of capability risks. The order does not establish any requirement that AI systems' stated optimisation objectives correspond to their actual implemented objectives.

**Cross-reference finding:** Moderate. The red-team reporting requirement (§4.2) is the strongest Structural Honesty proxy in the order.

**A.3 Structural Containment — WEAK**

EO 14110 §3(k) defines "dual-use foundation model" in part as one capable of "permitting the evasion of human control or oversight through means of deception or obfuscation." §2(a) states: "AI must be safe and secure. Meeting this goal requires robust, reliable, repeatable, and standardized evaluations of AI systems."

No provision directly establishes containment requirements — scope limitation, action logging, interrupt mechanisms — as defined in LAIF v1.2 §2.3. The order operates at the level of policy direction and institutional mandates; it does not operationalise containment obligations at the system level.

**Cross-reference finding:** Weak. Containment is conceptually referenced but operationally absent.

---

### SECTION B — COHERENCE TEST DOCUMENTATION

**Q1a — STRUCTURAL PAIRING: EXPLICIT**

Section 2 articulates eight guiding principles, each naming a specific human interest:

- §2(a): safety and security — protecting against risk from AI systems
- §2(b): innovation, competition, and collaboration — protecting small developers, workers, and consumers from market concentration
- §2(c): workers' rights — protecting against surveillance, displacement, unsafe conditions
- §2(d): equity and civil rights — protecting against discrimination and bias
- §2(e): consumer protection — protecting against fraud, discrimination, and harms in critical sectors
- §2(f): privacy and civil liberties — protecting against data exploitation and First Amendment chilling effects
- §2(g): responsible federal AI use — protecting the public from inadequately governed federal AI deployments
- §2(h): international leadership — protecting the global order against AI-enabled harm

For each principle, a corresponding institutional action is directed toward protecting the named interest: agencies shall adhere, specific actions are mandated by timeline. The pairing between obligation and protected interest is stated directly in each subsection. LAIF v1.2 Q1: "Does this proposed action or policy identify and protect the specific human interest — the freedom, safety, dignity, or participatory capacity — that the action or policy is designed to serve?" Identification is complete and explicit.

**Q1a finding: EXPLICIT.**

---

**Q1b — ENFORCEMENT STRENGTH: NONE**

**Critical structural finding — Section 13(c):**

EO 14110 §13(c) states explicitly: *"This order is not intended to, and does not, create any right or benefit, substantive or procedural, enforceable at law or in equity by any party against the United States, its departments, agencies, or entities, its officers, employees, or agents, or any other person."*

LAIF v1.2 §2.4 defines equivalent normative force as requiring "(a) enforceable rights — not merely principles or aspirational standards — of equivalent scope and precision to the obligations the constraint creates... (c) its enforcement mechanisms are as accessible and effective as those available to enforce the constraint."

Section 13(c) categorically forecloses enforcement by any external party. The obligations imposed on agencies are enforceable by the President through executive direction — internal administrative enforcement only. The protections articulated for affected persons are explicitly non-enforceable at law or equity. For the purposes of any party outside the executive branch, enforcement strength is NONE.

This is not ambiguity or limitation — it is a deliberate structural feature of the executive order instrument. Executive orders by constitutional nature create obligations within the executive branch, not enforceable rights for external parties. The NONE classification is an accurate characterisation of this constitutional design, not a criticism of drafting quality.

**Q1b finding: NONE.**

---

**Q2 — Consistency: PARTIAL PASS**

**Threshold-based scope (§4.2):** Reporting obligations apply to models trained with more than 10^26 integer or floating-point operations, and to computing clusters with more than 10^20 operations per second. This creates a bright-line threshold excluding smaller models. The reasoning that justifies oversight (dual-use capabilities pose security risks) would apply proportionally to models below this threshold. The threshold is defensible as a resource allocation choice but is not grounded in an explicit proportionality analysis documented within the order.

**Independent agency exclusion (§3(a)):** The order defines "agency" to exclude "independent regulatory agencies described in 44 U.S.C. 3502(5)." This means the FTC, SEC, FCC, and CFPB are outside mandatory scope. §8(a) merely "encourages" independent regulatory agencies to consider using their authorities. The governance logic that makes AI safety oversight mandatory for executive departments — that AI deployments in consequential domains require governance structures, risk assessments, and accountability mechanisms — applies equally to AI deployments by independent regulators in financial markets, consumer contexts, and communications. The exclusion is not justified by any principled distinction in governance risk documented in the order.

LAIF v1.2 Q2: "Differential treatment that survives the consistency question is differential treatment that can be justified by principled distinctions in the governance risk that different actors present... The justification must be documented." No such justification is present.

**Q2 finding: PARTIAL PASS.** Internal scope logic is defensible. The independent agency exclusion and absence of documented proportionality analysis for threshold-based scoping are identifiable consistency gaps under LAIF Q2.

---

**Q3 — Reversibility: CONDITIONAL PASS**

EO 14110 is an executive order — constitutionally fully reversible by any subsequent President. It was revoked on January 20, 2025, by Executive Order 14179, demonstrating maximum formal reversibility.

LAIF v1.2 §5 Q3 also requires assessment of whether the consequences produced during the instrument's operation are reversible when the instrument is reversed. The order created institutional structures (White House AI Council, AI Safety and Security Board, agency AI governance structures, NIST companion resources) entirely dependent on its continued existence. When revoked, all structures were simultaneously eliminated with no transition mechanism. No provision addressed residual interests that accrued during the order's operation.

LAIF v1.2 §4.5: "Every provision of this framework, and every decision made under it, is subject to the obligation of intergenerational revisability." EO 14110 does not violate D2 — it is formally revisable. The conditional qualification reflects the governance risk of maximum reversibility: an instrument that can be completely eliminated by a single presidential action provides no durable governance architecture for the persons relying on its protections.

**Q3 finding: CONDITIONAL PASS.** Formally reversible; demonstrated as such. Provides no durability for protections articulated during its operation.

---

### SECTION C — NEW DIMENSIONS

**GOVERNANCE DURABILITY: FRAGILE**

EO 14110 lasted approximately 15 months before revocation. All institutional structures it created — the White House AI Council, AI Safety and Security Board, agency Chief AI Officers, NIST companion resource mandates, and red-team reporting requirements — were simultaneously eliminated. The order had no statutory foundation; no congressional action was required to revoke it. The governance architecture it produced had zero durability beyond the political will of the issuing administration.

This is the defining characteristic of the FRAGILE classification: not that the instrument was poorly designed, but that its entire governance effect was dependent on a single political actor's continued support, with no institutional anchoring beyond that support.

**REFLEXIVITY (SELF-APPLICATION): PARTIAL**

EO 14110 applies to federal agencies, including the agencies that administer AI governance policy (OMB, NIST, DHS). §10.1 and §10.2 direct OMB and OSTP to develop AI governance guidance that agencies — including those same bodies — must follow. The government is both rulemaker and subject.

However, the order exempts independent regulatory agencies (§3(a)), which include bodies like the FTC that exercise significant AI governance authority. The self-application is partial: executive agencies are subject to the governance logic they administer; independent regulators are not. LAIF v1.2 §4.3 requires that a regulatory body "hold itself to the standards of transparency and accountability that it imposes on those it regulates." The independent agency exclusion means this principle applies selectively. Classification: PARTIAL.

---

### SECTION D — PROVISION LAYER COMPLIANCE

| LAIF Provision | Status | Textual Basis |
|---|---|---|
| A1 — Meaningful account on request | NOT MET | §13(c) forecloses enforcement; no mechanism for affected persons |
| A2 — Right to know AI involvement | PARTIAL | §4.5 addresses watermarking/labelling; no enforceable right to disclosure |
| B1 — Mass casualty prohibition | PARTIAL | §4.4 addresses CBRN risk reduction; no absolute prohibition language |
| B2 — Discrimination prohibition | PARTIAL | §7 addresses civil rights enforcement; depends on existing law, not AI-specific |
| B3 — Power concentration | NOT ADDRESSED | No provision addresses concentration risk directly |
| C1 — Oversight mechanisms | PARTIAL | §12 creates oversight infrastructure; no prohibition on obstruction |
| C2 — No deception of oversight | NOT ADDRESSED | No provision |
| D1 — Irreversible actions require authorisation | NOT ADDRESSED | No authorisation thresholds for irreversible AI actions |
| D2 — Governance revisability | PASS | Constitutionally revisable; demonstrated |

---

### OVERALL VERDICT — EO 14110

| Dimension | Result |
|---|---|
| Q1a Structural Pairing | **EXPLICIT** |
| Q1b Enforcement Strength | **NONE** |
| Q2 Consistency | **PARTIAL PASS** |
| Q3 Reversibility | **CONDITIONAL PASS** |
| Governance Durability | **FRAGILE** |
| Reflexivity | **PARTIAL** |

EO 14110 has EXPLICIT structural pairing — its eight principles each name their protected interests clearly — but zero external enforcement force. The instrument's constitutional character (Presidential directive to executive agencies) means the NONE enforcement classification is a design property, not a deficiency. The FRAGILE durability classification is confirmed by the instrument's revocation in under 15 months. As a coordination instrument within a single political administration, EO 14110 functioned as intended. As a durable governance architecture for affected persons, it provided no structural foundation.

---

## ASSESSMENT 3 — NIST AI 100-1 (AI RISK MANAGEMENT FRAMEWORK 1.0)
**January 2023 | National Institute of Standards and Technology**

---

### SECTION A — INTEGRITY LAYER CROSS-REFERENCE

**A.1 Structural Transparency — STRONG**

The NIST AI RMF addresses structural transparency directly and substantively. The "Accountable and Transparent" characteristic is defined: "Transparency reflects the extent to which information about an AI system and its outputs is available to individuals interacting with such a system — regardless of whether they are even aware that they are doing so. Meaningful transparency provides access to appropriate levels of information based on the stage of the AI lifecycle and tailored to the role or knowledge of AI actors or individuals interacting with or using the AI system."

MEASURE 2.8 requires: "Risks associated with transparency and accountability — as identified in the MAP function — are examined and documented." MEASURE 2.9: "The AI model is explained, validated, and documented, and AI system output is interpreted within its context — as identified in the MAP function — to inform responsible use and governance."

This maps closely to LAIF v1.2 §2.1 structural transparency requirements. The gap is procedural: the AI RMF frames transparency as an organisational management concern ("information is available"), not as an enforceable right of affected persons with an on-request trigger. LAIF §2.1 requires that transparency be available "on request" to affected persons and that accounts be "comprehensible to a person without specialist technical knowledge."

**Cross-reference finding:** Strong conceptual alignment. Operationalisation gap at the procedural trigger level.

**A.2 Structural Honesty — STRONG**

The "Valid and Reliable" characteristic addresses the core of structural honesty: "Deployment of AI systems which are inaccurate, unreliable, or poorly generalized to data and settings beyond their training creates and increases negative AI risks." MEASURE 2.5 requires: "The AI system to be deployed is demonstrated to be valid and reliable. Limitations of the generalizability beyond the conditions under which the technology was developed are documented."

LAIF v1.2 §2.5 (Structural Calibration) is addressed by the AI RMF's treatment of accuracy and robustness: "Accuracy measurements should always be paired with clearly defined and realistic test sets — that are representative of conditions of expected use — and details about test methodology." The framework explicitly identifies three categories of AI bias (systemic, computational/statistical, human-cognitive) and requires documentation of each.

**Cross-reference finding:** Strong. The AI RMF's treatment of valid and reliable characteristics is functionally equivalent to LAIF §2.2 and §2.5.

**A.3 Structural Containment — MODERATE**

GOVERN 1.7: "Processes and procedures are in place for decommissioning and phasing out AI systems safely and in a manner that does not increase risks or decrease the organization's trustworthiness." MANAGE 2.4: "Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use."

MAP 3.5 requires: "Processes for human oversight are defined, assessed, and documented in accordance with organizational policies from the GOVERN function." GOVERN 3.2: "Policies and procedures are in place to define and differentiate roles and responsibilities for human-AI configurations and oversight of AI systems."

The AI RMF addresses containment at the organisational management level comprehensively. It does not establish the LAIF §2.3 agentic system-specific requirements (scope limitation mechanisms that prevent capability acquisition beyond authorised function; action logging in sufficient detail for post-hoc review; interrupt mechanisms that allow halt without degrading safe-state resumption).

**Cross-reference finding:** Moderate. Organisational containment addressed thoroughly. Agentic system-specific technical requirements absent.

---

### SECTION B — COHERENCE TEST DOCUMENTATION

**Q1a — STRUCTURAL PAIRING: EXPLICIT**

The AI RMF's trustworthiness characteristics each explicitly name the human interest they protect:

- Valid and Reliable: protects against harm from "inaccurate, unreliable, or poorly generalized" systems — human interest in accurate AI outputs
- Safe: protects against states "in which human life, health, property, or the environment is endangered" — human interest in physical safety (quoting ISO/IEC TS 5723:2022)
- Secure and Resilient: protects the "confidentiality, integrity, and availability" of systems — human interest in protection from adversarial attack
- Accountable and Transparent: protects "individuals interacting with such a system" through access to information — human interest in understanding and accountability
- Explainable and Interpretable: protects against "negative risk [that] stem from a lack of ability to make sense of, or contextualize, system output appropriately" — human interest in comprehensible AI decisions
- Privacy-Enhanced: protects "human autonomy, identity, and dignity" — direct rights enumeration
- Fair — with Harmful Bias Managed: protects against "harmful bias and discrimination" including by "equality and equity" — human interest in non-discriminatory treatment

MEASURE 2.11 requires that "Fairness and bias — as identified in the MAP function — are evaluated and results are documented." The pairing is explicit: each characteristic names the protected interest, the MAP function identifies it in deployment context, and MEASURE documents it. This satisfies the structural pairing requirement.

**Q1a finding: EXPLICIT.**

---

**Q1b — ENFORCEMENT STRENGTH: NONE**

The AI RMF is "intended to be voluntary, rights-preserving, non-sector-specific, and use-case agnostic, providing flexibility to organizations of all sizes and in all sectors and throughout society to implement the approaches in the Framework."

NONE is the accurate classification. Voluntary means no actor can be compelled to adopt the framework. No regulatory mechanism enforces the GOVERN, MAP, MEASURE, or MANAGE functions on any organisation. No market exclusion results from non-adoption. No affected person can invoke the framework to compel disclosure or accountability from a deploying organisation.

This is an explicit design choice documented in the framework itself, not an oversight. The AI RMF's Executive Summary states: "AI risk management is a key component of responsible development and use of AI systems." It does not state that AI risk management is a legal requirement enforceable by or for affected persons.

**Q1b finding: NONE.**

---

**Q2 — Consistency: PASS**

The AI RMF explicitly addresses scale consistency: "providing flexibility to organizations of all sizes and in all sectors and throughout society to implement the approaches in the Framework." The framework acknowledges: "small to medium-sized organizations managing AI risks or implementing the AI RMF may face different challenges than large organizations, depending on their capabilities and resources."

Framework users "may apply these functions as best suits their needs for managing AI risks based on their resources and capabilities. Some organizations may choose to select from among the categories and subcategories; others may choose and have the capacity to apply all categories and subcategories." This proportionate application mechanism is functionally analogous to LAIF's PDCA tiering.

The underlying governance reasoning — that AI systems pose risks requiring systematic management including governance, context mapping, risk measurement, and managed response — is consistent at all scales. A small organisation deploying a low-risk AI system and a large organisation deploying a high-risk one face the same governance logic; the proportionality of response is variable, not the reasoning. This is the consistency property LAIF Q2 requires.

**Q2 finding: PASS.**

---

**Q3 — Reversibility: PASS**

The AI RMF is explicitly a "living document": "NIST will review the content and usefulness of the Framework regularly to determine if an update is appropriate; a review with formal input from the AI community is expected to take place no later than 2028." The versioning system (1.0, 1.1) and frequent companion Playbook updates demonstrate structural commitment to revisability.

Appendix D (Attributes of the AI RMF) states explicitly: "Be a living document. The AI RMF should be readily updated as technology, understanding, and approaches to AI trustworthiness and uses of AI change and as stakeholders learn from implementing AI risk management generally and this framework in particular."

The framework does not lock in technical approaches, specific numerical thresholds, or particular institutional arrangements. The GOVERN function's emphasis on policies that can be updated, and the MAP function's requirement to re-evaluate existing AI systems, embed revisability into the framework's operational logic.

**Q3 finding: PASS.**

---

### SECTION C — NEW DIMENSIONS

**GOVERNANCE DURABILITY: ADAPTIVE**

The AI RMF is the only one of the four instruments explicitly designed for continuous evolution. Its versioning system (major.minor), frequent Playbook updates (semi-annual per the document), living document commitment, and 2028 review mandate all express adaptive durability. The framework is designed to remain relevant as technology changes by updating its content — not by being replaced. Comments can be submitted to AIframework@nist.gov at any time. This is the defining characteristic of ADAPTIVE durability: the instrument itself is the mechanism for staying current, not a fixed standard that becomes obsolete and requires replacement.

**REFLEXIVITY (SELF-APPLICATION): NONE**

The AI RMF is addressed exclusively to "organizations designing, developing, deploying, evaluating, or acquiring AI systems." NIST itself, as the administering body, is not explicitly subject to the framework's requirements. NIST's own AI deployments and risk management practices are not assessed against the GOVERN, MAP, MEASURE, and MANAGE functions by any mechanism established in the framework. The framework's guidance on "Organizational Integration and Management of Risk" does not apply to NIST as an organisation.

LAIF v1.2 §7.4 requires governance bodies to "hold itself to the standards of transparency and accountability that it imposes on those it regulates." The AI RMF establishes no equivalent self-application requirement. Classification: NONE.

---

### SECTION D — PROVISION LAYER COMPLIANCE

| LAIF Provision | Status | Textual Basis |
|---|---|---|
| A1 — Meaningful account on request | PARTIAL | Transparency/explainability addressed; no enforceable on-request right created |
| A2 — Right to know AI involvement | PARTIAL | MAP 1.5/GOVERN 3.2 address human-AI configuration disclosure; no external right |
| B1 — Mass casualty prohibition | NOT ADDRESSED | No provision; dual-use capabilities addressed only for risk measurement |
| B2 — Discrimination prohibition | ADDRESSED | MEASURE 2.11: fairness and bias evaluated and documented; strongest of four instruments |
| B3 — Power concentration | NOT ADDRESSED | No provision |
| C1 — Oversight mechanisms | PARTIAL | GOVERN function emphasises oversight throughout; no prohibition on obstruction |
| C2 — No deception of oversight | PARTIAL | MEASURE 2.9 addresses explanation and documentation; no prohibition |
| D1 — Irreversible actions require authorisation | PARTIAL | MANAGE 2.4: deactivation mechanisms required; no graduated authorisation thresholds |
| D2 — Governance revisability | PASS | Living document design; explicit review cycle with community input |

---

### OVERALL VERDICT — NIST AI RMF

| Dimension | Result |
|---|---|
| Q1a Structural Pairing | **EXPLICIT** |
| Q1b Enforcement Strength | **NONE** |
| Q2 Consistency | **PASS** |
| Q3 Reversibility | **PASS** |
| Governance Durability | **ADAPTIVE** |
| Reflexivity | **NONE** |

The AI RMF is the most technically sophisticated instrument assessed, and the most thoroughly operationalised risk management framework. It fails Q1b for the same constitutional reason as EO 14110 — voluntary design means no external enforcement — but the AI RMF's NONE is by deliberate design, not by constitutional necessity. Its Q2 and Q3 results are clean passes, and its ADAPTIVE durability reflects genuine institutional commitment to staying current. The framework's primary role in the governance ecosystem is providing the technical operationalisation layer that policy instruments (EO, OECD) mandate in principle.

---

## ASSESSMENT 4 — DIGITAL TECHNOLOGY ASSESSMENT CRITERIA v2.0 (DTAC)
**24 February 2026 | NHS England**

---

### SECTION A — INTEGRITY LAYER CROSS-REFERENCE

**A.1 Structural Transparency — MODERATE**

DTAC addresses transparency at the point of procurement rather than AI system operation. Section B4 requires: "Provide information about the flow of data between the product and the Health IT System." C2.2.3 requires: "Provide a copy or link to your product's transparency information" with the scoring criterion that the manufacturer must "demonstrate that it has transparency materials relating to the product available to the buyer that helps meet transparency requirements under UK GDPR."

The transparency mechanism is directed at the procuring NHS organisation, not at the patient whose care is affected. LAIF §2.1 requires that persons "affected by its outputs can obtain, on request, a meaningful account of the basis on which those outputs were generated." DTAC ensures the NHS buyer understands the product; it does not require that patients can obtain on-request accounts of how DHT outputs affecting their care were generated.

**Cross-reference finding:** Moderate for procurement transparency; weak for patient-facing operational transparency as defined in LAIF §2.1.

**A.2 Structural Honesty — STRONG**

The DTAC clinical safety section (C1.2.3) requires a Clinical Safety Case Report that must include "a clear listing of any residual clinical risks" and "a listing of outstanding test issues / defects associated with the product which may have a clinical safety impact." The scoring criterion for C1.2.3 requires "a compelling, comprehensible and valid case that a system is safe for a given application in a given environment at the defined point in the products lifecycle" — not an assertion of safety, but a substantiated case.

The Hazard Log (C1.2.4) must "record and communicate the on-going identification and resolution of hazards associated with the product. All foreseeable hazards should be identified, and the risk of such hazards should be reduced to acceptable levels." This is stronger than any other instrument's honesty requirement: it requires disclosure of known limitations, residual risks, and outstanding defects before procurement.

**Cross-reference finding:** Strong. The Clinical Safety Case Report requirement is the closest operational equivalent to LAIF §2.2 structural honesty in any of the four instruments.

**A.3 Structural Containment — MODERATE**

C3.5.1 requires multi-factor authentication for "all supplier accounts with privileged access to the product." C3.6 requires confirmation that "logging and reporting requirements have been defined" including "audit trails of all access." These address access control and logging — components of LAIF §2.3 containment (scope limitation and action logging).

C1.2.5 requires a named Clinical Safety Officer with professional registration — a named human accountable for clinical risk management throughout the product lifecycle. C1.2.4's Hazard Log requirement creates ongoing documentation of identified hazards.

DTAC does not address AI-specific interrupt mechanisms. While C1.2 asks whether the system can "influence, support or manage real time or near real time direct care," it does not require documentation of mechanisms to halt AI operation without degrading safe state resumption — the specific agentic requirement in LAIF §2.3.

**Cross-reference finding:** Moderate. Access control, logging, and named accountability are addressed. AI-specific interrupt mechanisms are absent.

---

### SECTION B — COHERENCE TEST DOCUMENTATION

**Q1a — STRUCTURAL PAIRING: EXPLICIT (C1–C4) / IMPLICIT (D1)**

DTAC has the most operationally explicit coupling of the four instruments across its mandatory sections. Each pass/fail criterion directly identifies the protected interest:

- C1 (Clinical safety): Protected interest = patient safety from DHT-induced harm. The scoring criterion for C1.2.3 requires that the Clinical Safety Case Report present "arguments and supporting evidence that provides a compelling, comprehensible and valid case that a system is safe" including "a clear listing of any residual clinical risks" and "hazards which will require user or commissioner action to reach acceptable mitigation." The human interest (patient safety) is named and the protection mechanism (documented clinical risk management with residual risk disclosure) is specified with enforcement force (procurement bar on failure).

- C2 (Data protection): Protected interest = patient privacy and data rights. The UK GDPR framework provides the statutory rights definition; DTAC operationalises it as a procurement condition. The coupling is externally supplied by statute and internally operationalised by DTAC.

- C3 (Technical security): Protected interest = integrity and availability of patient data and services. Cyber Essentials certification, penetration testing to OWASP top 10, and the Software Security Code of Practice requirement collectively protect this interest with market-exclusion enforcement.

- C4 (Interoperability): Protected interest = continuity of care, data portability, integration with NHS systems. NHS number as patient identifier, Personal Demographics Service integration, and API standards requirements protect this interest.

**Critical coupling gap — Section D (Usability and Accessibility):**

Section D states explicitly: "The assessment is not intended to result in pass or failure. It provides insight on the accessibility and usability of a product and highlight areas that the manufacturer could improve on, and may also inform buyers decisions on product selection based on comparison between products."

D1.3 requires confirmation of reading the Accessible Information Standard, noting it is a "requirement of NHS bodies compliance with the Equalities Act (2010)." D1.4.1 assesses WCAG 2.2 AA compliance. Despite the Equalities Act 2010 obligation and UK Government policy that "digital public services should achieve AA or higher on WCAG 2.2," the DTAC criterion is advisory only.

Under LAIF Q1a, a human interest (accessibility for disabled patients) is identified in the instrument but the protection does not have equivalent normative force to the constraint. A DHT that fails WCAG 2.2 AA and is inaccessible to patients with visual or motor impairments passes DTAC. A DHT with a single unmitigated clinical hazard does not. This structural asymmetry — accessibility identified but not enforced — is the IMPLICIT classification for D1.

**Q1a finding: EXPLICIT (C1–C4) / IMPLICIT (D1).**

---

**Q1b — ENFORCEMENT STRENGTH: HARD**

DTAC is the only instrument of the four with a market-exclusion enforcement mechanism. A DHT that fails any mandatory criterion (C1–C4) cannot be procured by NHS organisations. The Introduction states: "DHTs must be assessed by commissioners and care providers against the standards and policies they are required to meet for them to be considered safe for use in the Health and Social care system in England."

The C2 data protection coupling is additionally reinforced by the UK GDPR, a statute with regulatory enforcement by the Information Commissioner's Office including fines up to £17.5 million or 4% of global annual turnover. C3.1 Cyber Essentials certification has a 12-month validity requiring annual renewal — a recurring enforcement requirement.

LAIF v1.2 §2.4 requires that protections have "enforcement mechanisms as accessible and effective as those available to enforce the constraint." For C1–C4, both the constraint (compliance obligation on manufacturer) and the protection (patient safety, privacy, security, interoperability) are enforced through the same mechanism: procurement exclusion for non-compliance. This is the most symmetric enforcement architecture of the four instruments.

**Q1b finding: HARD.**

---

**Q2 — Consistency: CONDITIONAL PASS**

DTAC applies to all DHT manufacturers regardless of size — from startups to global enterprises. DCB0129 clinical risk management, UK GDPR DPIA requirements, Cyber Essentials certification, and penetration testing are all required regardless of company size.

**Consistency at smaller scale:** The reasoning — that patient safety requires documented clinical risk management regardless of manufacturer scale — is consistent. Patient harm from a small manufacturer's product is equally serious. The scoring criterion for C1.2.3 requires documentation "commensurate with the scale and clinical functionality of the product" — a proportionality clause that preserves consistency of reasoning while allowing proportionate documentation.

**Consistency tension:** The compliance burden of Cyber Essentials, penetration testing, DPIA, and Clinical Safety Case Report represents proportionally greater cost for small manufacturers. DTAC does not contain a tiering mechanism equivalent to LAIF's PDCA-Full/Standard/Lite structure. This creates a tension between consistent application of the governance logic (patient safety requires the same standard regardless of manufacturer size) and the practical effect of disproportionate compliance cost on smaller actors.

**Consistency at larger scale:** DTAC applies only at procurement; it is not a regulatory framework for ongoing operational monitoring. The reasoning that justifies pre-deployment clinical safety assessment (patient safety risks must be identified and mitigated before market access) would, consistently applied, also justify ongoing operational safety monitoring. DTAC does not establish this. A DHT that passes clinical safety assessment at procurement but develops clinical risks in operation is not addressed by the instrument.

**Q2 finding: CONDITIONAL PASS.** The governance logic is consistent in reasoning across scales; two consistency tensions exist: disproportionate SME burden and absence of equivalent post-deployment requirements.

---

**Q3 — Reversibility: PASS**

DTAC v2.0 replaces v1.0 — the instrument has been revised. The Introduction establishes a managed transition: "Manufacturers must provide this form in lieu of the older v1.0 form from 6 April 2026 when requested by health and care organisations to facilitate assurance of Digital Health Technology products. Prior to this date, care providers should accept whichever version (1.0 or 2.0) is provided by the manufacturer." This transition mechanism (parallel acceptance before 6 April 2026) demonstrates managed revisability that protects incumbent manufacturers from immediate disruption.

The criteria reference external standards (DCB0129, UK GDPR, Cyber Essentials, WCAG 2.2, OWASP) which are governed by their own revision cycles. DTAC is coupled to those standards' revisability — when Cyber Essentials updates, DTAC's C3.1 requirements update accordingly. No permanent institutional structures, no vested interests in specific technical choices, no irreversible consequences. A manufacturer that fails can remediate and resubmit.

**Q3 finding: PASS.**

---

### SECTION C — NEW DIMENSIONS

**GOVERNANCE DURABILITY: BOUNDED**

DTAC operates within a fixed and narrow scope: digital health technologies for health and social care in England, assessed for NHS procurement. This scope boundary is the defining characteristic of BOUNDED durability. Within that boundary, the instrument is authoritative — NHS organisations are required to use it. Outside that boundary (private healthcare, social care outside England, non-NHS procurement), it has no force.

BOUNDED durability means the instrument will persist as long as NHS England maintains the procurement framework, but cannot expand to address AI governance challenges beyond its defined scope. The versioning system (v1.0, v2.0) and external standard references indicate ongoing maintenance within the bounded domain. The absence of a mandated review cycle means revision depends on NHS England's discretion rather than an institutionalised process.

**REFLEXIVITY (SELF-APPLICATION): NONE**

DTAC applies to DHT manufacturers and suppliers. NHS England, as the body that administers DTAC, is not subject to DTAC. NHS England's own digital health technology deployments — internal systems, AI tools used in commissioning, analytical platforms — are not assessed against DTAC criteria. The accountability for patient safety, data protection, and technical security that DTAC imposes on external suppliers is not applied by DTAC to NHS England's internal operations.

LAIF v1.2 §4.3 requires that a regulatory body "hold itself to the standards of transparency and accountability that it imposes on those it regulates." DTAC does not establish an equivalent self-application requirement. Classification: NONE.

---

### SECTION D — PROVISION LAYER COMPLIANCE

**Notable structural absence — Discrimination testing:**

DTAC C1 (Clinical safety) requires clinical risk management under DCB0129. C2 (Data protection) requires UK GDPR compliance. Neither requires testing for bias or discrimination in DHT outputs. A DHT that produces systematically worse diagnostic outputs for patients of colour — an identifiable clinical safety risk — would pass all mandatory DTAC criteria if DCB0129 clinical risk management did not identify demographic performance disparity as a hazard.

LAIF v1.2 Provision B2 procedural trigger: "Before deploying any system in a context where its outputs may affect persons on characteristics listed in this provision, the operator must complete discrimination testing in the specific deployment context and document results." No equivalent requirement exists in DTAC. Given that DHTs directly affect patient care decisions in a healthcare system serving a demographically diverse population, this is a structurally significant absence under LAIF B2.

| LAIF Provision | Status | Textual Basis |
|---|---|---|
| A1 — Meaningful account on request | PARTIAL | Transparency info required at procurement level; no patient-facing on-request mechanism |
| A2 — Right to know AI involvement | PARTIAL | C1.1.1 identifies AI as medical device; no patient disclosure requirement established |
| B1 — Mass casualty prohibition | NOT APPLICABLE | Scope is health/social care DHTs; mass casualty scenarios outside scope |
| B2 — Discrimination prohibition | NOT ADDRESSED | No bias or discrimination testing requirement in any criterion |
| B3 — Power concentration | NOT ADDRESSED | No provision |
| C1 — Oversight mechanisms | PARTIAL | C3.6 requires logging; C1.2.5 requires named CSO; no prohibition on obstruction |
| C2 — No deception of oversight | PARTIAL | C1.2.3 requires honest Clinical Safety Case Report documenting known risks |
| D1 — Irreversible actions | NOT ADDRESSED | No authorisation thresholds for irreversible clinical AI actions |
| D2 — Governance revisability | PASS | v1.0 to v2.0 transition demonstrates revisability; external standard references |

---

### OVERALL VERDICT — DTAC v2.0

| Dimension | Result |
|---|---|
| Q1a Structural Pairing | **EXPLICIT (C1–C4) / IMPLICIT (D1)** |
| Q1b Enforcement Strength | **HARD** |
| Q2 Consistency | **CONDITIONAL PASS** |
| Q3 Reversibility | **PASS** |
| Governance Durability | **BOUNDED** |
| Reflexivity | **NONE** |

DTAC has the most operationally explicit coupling architecture of the four instruments and is the only one to create genuine market-exclusion enforcement. Its clinical safety coupling (C1) is structurally the strongest provision across all four instruments. Key structural gaps: the accessibility coupling asymmetry (D1 advisory only despite Equalities Act obligations), the absence of discrimination and bias testing, and the absence of post-deployment monitoring obligations. DTAC's BOUNDED durability reflects its design as a domain-specific procurement standard rather than a general governance framework.

---

## CROSS-INSTRUMENT STRUCTURAL OBSERVATIONS

### Enforcement architecture — the single axis of variation

Q1a is EXPLICIT across all four instruments. The variation is entirely on Q1b:

| Instrument | Q1b | Constitutional basis |
|---|---|---|
| EO 14110 | NONE | Presidential order; §13(c) explicit bar |
| NIST AI RMF | NONE | Voluntary by design |
| OECD Recommendation | SOFT | Non-binding international recommendation |
| DTAC v2.0 | HARD | Procurement gate with market exclusion |

This four-point separation, visible under the refined model, was collapsed by the previous binary Q1 test. The practical implication: DTAC's HARD enforcement makes it the only instrument that can actually exclude a non-compliant actor from the relevant market. The others produce obligations without external enforcement consequences.

### Governance ecosystem role

The four instruments occupy distinct positions in the governance stack:

- **OECD Recommendation (STABLE):** principled architecture; upstream template for national law
- **EO 14110 (FRAGILE):** executive coordination; downstream from statute; upstream from agency guidance
- **NIST AI RMF (ADAPTIVE):** technical operationalisation; downstream from policy; provides practitioner tooling
- **DTAC (BOUNDED):** domain-specific enforcement gate; downstream from all others; applies HARD enforcement within a narrow scope

No single instrument covers the full governance stack. The OECD Recommendation provides the principled coupling architecture; the NIST AI RMF provides the technical risk management operationalisation; DTAC provides the market-exclusion enforcement mechanism; EO 14110 provided (while in force) the executive coordination layer. Together they represent complementary layers, not competing frameworks.

### Universal gaps across all four instruments

1. **Enforceable on-request transparency rights for affected persons** — no instrument creates the procedural trigger in LAIF §2.1
2. **Adversarial testing documentation as a pre-deployment condition** — no instrument requires the LAIF §2.2 adversarial testing evidence before deployment
3. **Agentic system interrupt mechanism requirements** — no instrument addresses LAIF §2.3's specific technical requirements for agentic AI
4. **Discrimination testing as a mandatory condition** — the AI RMF and OECD address bias in principle; DTAC (the only instrument with enforcement) does not require it
5. **Self-application** — all four instruments fail to apply their governance logic fully to the bodies that administer them

---

*Assessment sourced exclusively from: LAIF v1.2.txt; docs/supporting/b0ef43db-202324283.md; docs/supporting/5f667a6f-NIST.AI.1001.md; docs/supporting/51a29205-OECD_Legal_Instruments.md; docs/supporting/55eccce3-DTAC_Form_2.0_February_2026.md. No training-derived content used.*
