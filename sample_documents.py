#!/usr/bin/env python3
"""
LAIF Assessment — Document Corpus
----------------------------------
Representative excerpts from public AI governance frameworks.
Self-contained — no live fetching required.

Each entry carries:
  - Document metadata (source_type, jurisdiction, year, citation)
  - sector  — LAIF sector profile key for sector-aware assessment
  - text    — excerpt used for analysis

Documents 1–4: general AI governance frameworks (cross-sector).
Document 5:    clinical AI deployment policy (sector: clinical_ai).
Document 6:    employment AI governance framework (sector: employment_ai).
"""

DOCUMENTS = {

    "EU AI Act — Art. 9, 13 & 14": {
        "source_type":  "binding_regulation",
        "jurisdiction": "European Union",
        "year":         2024,
        "citation":     "Regulation (EU) 2024/1689 of the European Parliament and of the Council",
        "sector":       "general_ai_governance",
        "text": """\
EU AI Act (Regulation 2024/1689) — Risk Management, Transparency, and Human Oversight

Article 9 — Risk Management System

1. A risk management system shall be established, implemented, documented and
maintained in relation to high-risk AI systems throughout the entire lifecycle
of the system. The risk management system shall consist of a continuous iterative
process comprising: (a) identification and analysis of known and reasonably
foreseeable risks to health, safety or fundamental rights when the system is used
in accordance with its intended purpose; (b) estimation and evaluation of risks
arising from reasonably foreseeable misuse; (c) adoption of appropriate and
targeted risk management measures designed to address identified risks in
proportion to the degree of risk posed to health, safety or fundamental rights.

2. Risk management measures shall give due consideration to the effects and
possible interactions resulting from the combined application of requirements.
They shall take into account the state of the art, including as reflected in
relevant harmonised standards or common specifications.

3. Providers shall establish technical documentation demonstrating that the
high-risk AI system conforms to the requirements of this Chapter before placing
the system on the market or putting it into service. Technical documentation
shall be kept up to date and made available for inspection.

Article 13 — Transparency and Provision of Information to Deployers

1. High-risk AI systems shall be designed and developed so as to ensure that
their operation is sufficiently transparent to enable deployers to interpret the
system's output and use it appropriately. An appropriate type and degree of
transparency shall be ensured, in view of the intended purpose of the AI system.

2. Deployers shall have sufficient information about the system to ensure its use
remains within the scope of its intended purpose and does not put at risk the
health, safety or fundamental rights of natural persons. Providers shall supply
meaningful information about the system's capabilities, limitations, and the
degree of accuracy and reliability of outputs.

Article 14 — Human Oversight

1. High-risk AI systems shall be designed and developed in such a way, including
with appropriate human-machine interface tools, that they can be effectively
overseen by natural persons during the period in which the AI system is in use.

2. Human oversight shall aim to prevent or minimise the risks to health, safety
or fundamental rights that may emerge when a high-risk AI system is used in
accordance with its intended purpose or under conditions of reasonably foreseeable
misuse, in particular where such risks persist notwithstanding the application of
other requirements set out in this Chapter.

3. Natural persons to whom human oversight is assigned shall be able to understand
the capacities and limitations of the high-risk AI system and be able to duly
monitor its operation. Post-market monitoring shall be carried out by providers
to collect and review relevant data on the performance of high-risk AI systems
throughout their lifetime.
""",
    },

    "NIST AI RMF — Govern & Map Functions": {
        "source_type":  "voluntary_framework",
        "jurisdiction": "United States",
        "year":         2023,
        "citation":     "NIST AI Risk Management Framework 1.0 (NIST AI 100-1)",
        "sector":       "general_ai_governance",
        "text": """\
NIST AI Risk Management Framework 1.0 — Govern and Map Functions

GOVERN Function

The GOVERN function cultivates and implements organisational practices where
accountability for AI risk outcomes is distributed across appropriate roles.
Policies, processes, and cultural practices are in place to achieve responsible
AI risk management throughout the AI lifecycle.

GOVERN 1.1: Policies, processes, procedures, and practices across the organisation
related to the mapping, measuring, and managing of AI risks are in place,
transparent, and implemented effectively.

GOVERN 1.2: Accountability, criteria, and processes exist so that appropriate teams
and individuals are empowered, responsible, and trained for mapping, measuring,
and managing AI risks.

GOVERN 2.1: Organisational teams that develop, deploy, evaluate, and assess AI
systems document the context in which the AI system will be used as a basis for
identifying risks. This includes intended uses, known limitations, technical
specifications, and deployment environment.

GOVERN 4.1: Policies and practices are in place to foster a critical thinking and
safety-first mindset in the design, development, deployment, and uses of AI
systems to minimise potential negative impacts.

GOVERN 6.1: Policies and procedures are in place to address AI risks and benefits
arising from third-party entities, including AI-generated content used in training
or fine-tuning, and data and models from third parties.

MAP Function

MAP 2.2: Scientific findings, expert opinions, public concerns, and other
perspectives that may inform the AI risk assessment are gathered and considered.
Mechanisms for independent oversight of AI systems are in place to review
performance and ensure accountability.

MAP 5.1: Likelihood and magnitude of each identified impact (both potentially
beneficial and harmful) is examined and documented. Stakeholder consultations are
considered and documented for affected groups. Records of risk assessment
decisions are maintained for audit and review purposes.

MAP 5.2: Practices and personnel for supporting the ongoing identification of
impacts are in place and documented. Residual risk after controls are applied is
evaluated and recorded before deployment is authorised.
""",
    },

    "OECD AI Principles (2019, rev. 2024)": {
        "source_type":  "international_principles",
        "jurisdiction": "International (OECD member states)",
        "year":         2024,
        "citation":     "OECD Principles on AI, adopted May 2019, revised 2024",
        "sector":       "general_ai_governance",
        "text": """\
OECD Principles on AI — Value-Based Principles for Responsible AI

Adopted by the OECD Council, May 2019. Revised 2024.

1. Inclusive growth, sustainable development and well-being
Stakeholders should proactively engage in responsible stewardship of trustworthy
AI in pursuit of beneficial outcomes for people and the planet, while decreasing
inequalities and protecting natural environments, including by augmenting human
capabilities and enhancing creativity.

2. Human-centred values and fairness
AI actors should respect the rule of law, human rights and democratic values
throughout the AI system lifecycle. These include freedom, dignity and autonomy,
privacy and data protection, non-discrimination and equality, diversity, fairness,
social justice, and internationally recognised labour rights. AI actors should
implement mechanisms and safeguards, including capacity for human determination,
appropriate to the context and consistent with the state of the art.

3. Transparency and explainability
AI actors should commit to transparency and responsible disclosure regarding AI
systems. This includes providing meaningful information to enable those adversely
affected by an AI system to understand and challenge its outcome based on plain
and intelligible information about the factors and logic that served as a basis
for a decision.

4. Robustness, security and safety
AI systems should be technically robust and developed and run in ways that
minimise and where possible prevent unsafe outcomes, including unintended or
unexpected applications. AI actors should ensure traceability in relation to
datasets, processes and decisions made during the AI system lifecycle to enable
analysis of outputs and accountability for decisions.

5. Accountability
AI actors should be accountable for the proper functioning of AI systems and for
the respect of the above principles, based on their roles and consistent with
the state of the art. Mechanisms should ensure responsibility and redress for
AI systems and their outcomes. Those adversely affected should have access to
effective remedies and the ability to contest decisions made by or with AI.
""",
    },

    "US Executive Order 14110 — §4 Safety & §7 Workers": {
        "source_type":  "executive_directive",
        "jurisdiction": "United States (Federal)",
        "year":         2023,
        "citation":     "Executive Order 14110 on Safe, Secure, and Trustworthy AI (Oct 30, 2023)",
        "sector":       "general_ai_governance",
        "text": """\
Executive Order 14110 on Safe, Secure, and Trustworthy Artificial Intelligence
(October 30, 2023)

Section 4.1 — Ensuring the Safety and Security of AI

The Secretary of Commerce shall engage with industry, civil society, and other
stakeholders to develop guidelines, standards, methodologies, and related tools
for AI safety and security, including for the evaluation of AI systems' alignment
with democratic values and human rights. Safety standards shall be proportionate
to the level of risk posed, with higher-risk applications subject to more
stringent requirements.

Section 4.2 — Advancing Transparency and Accountability

Federal agencies using AI in high-stakes decisions affecting members of the public
shall design systems to provide meaningful explanations of their outputs and to
support oversight by affected individuals and government officials. Accountability
for all Federal agencies for their AI use is paramount. Agencies shall ensure that
AI deployment maintains appropriate human oversight and does not abrogate the
rights or welfare of the public.

Section 4.3 — Evidence and Reporting

Agencies shall document AI deployment decisions affecting fundamental rights and
maintain records sufficient for audit. Where AI systems produce consequential
decisions, agencies shall establish mechanisms for review, correction, and redress
for affected individuals.

Section 7 — Supporting Workers

Agencies shall ensure that AI deployment in workplaces preserves fundamental
protections for workers, maintaining the connection between obligations imposed on
workers and the protections those obligations are intended to serve. No deployment
shall sever the linkage between a worker's legal obligations and their
corresponding rights.
""",
    },

    "NHS England — AI in Clinical Decision Support (Policy Framework)": {
        "source_type":  "sector_policy",
        "jurisdiction": "United Kingdom",
        "year":         2024,
        "citation":     "NHS England AI in Clinical Decision Support — Governance Framework (illustrative excerpt)",
        "sector":       "clinical_ai",
        "text": """\
NHS England — Governance Framework for AI-Enabled Clinical Decision Support

1. Purpose and Scope

This framework governs the deployment of AI-enabled clinical decision support
systems (CDSS) across NHS trusts. It applies to all AI systems that generate
clinical recommendations, diagnostic outputs, or treatment suggestions that
materially affect patient care decisions. The framework covers the full deployment
lifecycle from procurement through post-market surveillance.

2. Clinical Validation Requirements

2.1 All AI-enabled CDSS must undergo prospective clinical validation in the target
patient population before deployment. Validation studies shall demonstrate
clinical accuracy, sensitivity, and specificity appropriate to the intended
clinical use case.

2.2 Providers shall maintain technical documentation of validation methodology,
datasets used, and performance metrics. Technical documentation shall be updated
following any material change to the system or its deployment context.

2.3 Adverse event reporting: Any AI-generated recommendation that contributes to
a patient safety incident must be reported through the National Reporting and
Learning System (NRLS) and reviewed by the Clinical AI Safety Committee.

3. Human Oversight and Clinician Responsibility

3.1 AI-generated clinical recommendations are advisory only. Clinical decision
authority rests with the responsible clinician. No CDSS shall be configured to
require clinicians to justify overriding an AI recommendation as a precondition
of recording their clinical decision.

3.2 Trusts shall ensure that clinical staff using AI systems have received
appropriate training on the system's capabilities, limitations, and documented
error characteristics before patient-facing deployment.

3.3 Post-market surveillance: Trusts shall conduct quarterly performance monitoring
of deployed AI systems, including review of override rates, adverse events, and
equity metrics across patient demographics.

4. Transparency and Patient Rights

4.1 Patients shall be informed when AI systems have materially contributed to a
clinical recommendation affecting their care. This information shall be provided
in plain language accessible to patients without clinical training.

4.2 Patients have the right to request a human clinician review of any
AI-assisted clinical recommendation. This right shall not be subject to conditions
or prerequisites.

4.3 Providers shall disclose the AI system's material limitations to deploying
clinicians, including known performance gaps in specific patient subgroups.

5. Safety and Containment

5.1 AI systems shall not autonomously initiate clinical actions — including
ordering tests, prescribing medications, or changing treatment plans — without
explicit clinician authorisation at the point of care.

5.2 Systems shall surface out-of-scope queries through designated clinical
escalation channels rather than generating recommendations outside their validated
indication.

5.3 Incident response: trusts shall maintain documented procedures for
suspending or rolling back an AI system within 24 hours of identification of
a patient safety concern.
""",
    },

    "TUC/CIPD — Framework for Fair AI in Employment Decisions": {
        "source_type":  "sector_policy",
        "jurisdiction": "United Kingdom",
        "year":         2024,
        "citation":     "Illustrative AI in Employment Governance Framework (sector assessment document)",
        "sector":       "employment_ai",
        "text": """\
Framework for the Governance of AI Systems in Employment Decisions

Produced for HR and employment law practitioners deploying AI in workforce management.

Section 1 — Scope

This framework applies to AI systems used to inform or automate decisions affecting
workers' employment status, including: applicant screening and recruitment scoring;
performance assessment and management; pay and bonus determination; promotion and
progression decisions; and dismissal or redundancy selection. Any system whose
outputs materially affect a worker's employment status or income falls within scope.

Section 2 — Employer Obligations

2.1 Transparency: Employers shall notify workers when AI systems are used in
employment decisions affecting them and shall provide a meaningful explanation
of the factors and weighting used in any AI-assisted decision.

2.2 Human review: Every AI-assisted employment decision that adversely affects a
worker's employment status — including decisions on hiring, performance rating,
pay, promotion, and dismissal — shall be subject to human review before it takes
effect. Workers have the right to request human review of any adverse AI decision.

2.3 Fairness audit: Employers shall commission an algorithmic fairness audit
before deploying any AI system for employment decisions. The audit shall assess
the system for discriminatory outputs across protected characteristics. Results
shall be documented and made available to worker representatives on request.

2.4 Worker consultation: Before deploying AI systems that will monitor worker
performance or determine employment outcomes, employers shall consult with trade
unions or worker representatives on the system's purpose, decision logic,
safeguards, and appeal processes.

Section 3 — Worker Rights

3.1 Right to explanation: Any worker adversely affected by an AI-assisted
employment decision has the right to a written explanation of the decision
in plain language, including the factors that contributed to the outcome.

3.2 Right of appeal: Every adverse employment decision informed by AI is
subject to an internal appeal process before a human decision-maker with
authority to reverse the AI recommendation. The appeal process shall be
completed within 20 working days.

3.3 Protection from automated dismissal: No dismissal decision may be taken
solely on the basis of AI output without human review and sign-off by a senior
manager. Workers facing dismissal where AI has been used must be informed of
this fact and given the opportunity to make representations before the decision
is finalised.

3.4 Collective rights: Trade unions and worker representatives have the right
to request disclosure of algorithmic audit results, model documentation, and
performance monitoring data for AI systems used in employment decisions.

Section 4 — Accountability

4.1 Designated AI Accountability Officer: Employers deploying AI in employment
decisions shall designate an individual responsible for compliance with this
framework. This individual shall have authority to suspend or recall AI systems
where fairness or legal compliance concerns arise.

4.2 Record-keeping: Employers shall maintain records of AI-assisted employment
decisions, including the factors considered and the human review outcome, for
a period of five years. Records shall be available for inspection on request.

4.3 Redress: Workers who believe an AI-assisted employment decision has caused
them harm through discrimination or procedural unfairness may raise a
discrimination policy complaint through internal grievance procedures or
employment tribunal proceedings.
""",
    },

}
