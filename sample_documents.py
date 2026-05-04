#!/usr/bin/env python3
"""
LAIF Assessment — Document Corpus
----------------------------------
Representative excerpts from public AI governance frameworks.
Self-contained — no live fetching required.

Each entry carries document metadata and the text excerpt used for analysis.
Excerpts are expanded beyond the original test_real_world.py versions to
provide sufficient signal density for multi-dimensional scoring.
"""

DOCUMENTS = {

    "EU AI Act — Art. 9, 13 & 14": {
        "source_type":  "binding_regulation",
        "jurisdiction": "European Union",
        "year":         2024,
        "citation":     "Regulation (EU) 2024/1689 of the European Parliament and of the Council",
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

}
