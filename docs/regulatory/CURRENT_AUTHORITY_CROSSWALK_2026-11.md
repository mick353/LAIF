# LAIF regulatory authority crosswalk — current-law research note

**Checked:** 6 November 2026. **Status:** informative, external-source research
note for human/legal review; **not** a verified-corpus assessment, statutory
interpretation, certified compliance mapping or amendment to the published
April 2026 LAIF v1.2 corpus. Laws, implementing dates, guidance and proposals
can change. Confirm the operative text and jurisdiction before operational use.

## The critical separation

1. **Binding authority:** law, a competent regulator, an applicable contract or
   an organisation's adopted internal control. LAIF by itself creates none of
   these for an external institution.
2. **LAIF design standard:** the Coherence Test, Integrity Layer, PDCA,
   obligations and proposed safety provisions in LAIF's published framework.
3. **Diagnostic tool:** the local Python engine and optional evidence annexes.
   These inspect submitted records; they do not certify legal conformity,
   actual model behaviour, effective containment, or a judicial defence.

The [April 2026 Regulatory Integration Guide](../../LAIF_Regulatory_Integration_Guide.txt)
is a historical published instrument. Its claim that certain PDCA sections
"SATISFY" external obligations is **not established by this repository**.
Use "potential supporting evidence for a specified legal requirement, subject
to the full requirement and competent review" in current-facing materials.
No generic PDCA completion automatically satisfies the EU AI Act, NIST,
US federal procurement rules or another jurisdiction's law.

## European Union: AI Act

**Primary source:** [Regulation (EU) 2024/1689 on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
and the Commission's [current consolidated AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng).
Use the actual relevant consolidated text, amendments, transitional rules,
classification and guidance at the date of the legal assessment.

**Commencement is provision-specific.** As amended by
[Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng),
the AI Act generally applies from **2 August 2026**, but Chapter III,
Sections 1–3 requirements for Annex III high-risk systems apply from
**2 December 2027**, and those for Annex I product-linked high-risk systems
from **2 August 2028** (subject to the actual exceptions and transitional
rules in Article 113). Chapter V general-purpose AI model obligations began
applying on **2 August 2025**, with an additional transition for models placed
on the market before that date under Article 111(3). These distinct dates
must not be collapsed into one blanket AI Act compliance deadline.

| Legal requirement / question | Possible LAIF contribution | Important remaining obligation or boundary |
|---|---|---|
| Risk classification, high-risk AI and prohibited practices (Arts 5–6, Annex III) | Coherence Test and documented classification reasoning | Statutory scope and exemptions must be determined under the AI Act itself. |
| High-risk lifecycle risk management (Art 9) | PDCA failure pathways, reversibility and risk owner documentation | An actual risk management system, lifecycle controls and required technical evidence are still necessary. |
| Data governance (Art 10) | Coupling, bias questions and evidence requests | Actual dataset governance, suitability, representativeness and relevant technical records cannot be inferred from PDCA prose. |
| Transparency and human oversight (Arts 13–14) | Integrity Layer, actor mapping and intervention requirements | Instructions for use, designed oversight capability and tested deployment-specific controls remain separately required. |
| Accuracy, robustness, cybersecurity and quality management (Arts 15, 17) | Evidence requests, negative tests, incident and change control | Actual performance, cybersecurity and functioning quality management must be demonstrated. |
| Conformity assessment (Art 43) | Traceable due-diligence input | LAIF outputs do not establish conformity assessment completion, CE marking or regulator acceptance. |
| General-purpose model provider obligations (Art 53) | Source and lifecycle accountability prompts | Provider-specific documentation, copyright and training-summary duties require separate legal mapping. |
| **Systemic-risk GPAI** (Arts 51, 55) | Optional frontier safety threat register, capability evaluations, distinct reviewers, containment and incident control evidence | The provider must perform required model evaluations and systemic-risk mitigation, report serious incidents, and secure models/infrastructure; the diagnostic is not those operational acts. |

In particular, [Article 55](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-55)
requires providers of general-purpose AI models with systemic risk to conduct
and document adversarial evaluation, assess and mitigate systemic risks, report
relevant serious incidents without undue delay, and ensure adequate
cybersecurity protection of the model and its physical infrastructure. The
Commission's [AI Act FAQ on AI agents](https://ai-act-service-desk.ec.europa.eu/en/faq)
explains how agentic tool use can affect the systemic-risk analysis. Statutory
implementation and any proposed amendments must be checked in force; a
proposal is not an enacted rule.

**Source custody gap:** on `main` as checked 6 November 2026, the original EU
AI Act is still `PENDING_INGESTION` in the verified corpus. Draft
[PR #90](https://github.com/mick353/LAIF/pull/90) proposes official source
admission but has not been merged, and admission is not an assessment of the
consolidated text. Do not represent LAIF's historical representative excerpt
as a full original-language, current-law assessment.

## United States: federal civilian use and acquisition

**Primary sources:** [OMB M-25-21 and M-25-22](https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/)
(both 3 April 2025), and the [White House release](https://www.whitehouse.gov/releases/2025/04/white-house-releases-new-policies-on-federal-agency-ai-use-and-procurement/).
The US Government Accountability Office independently documents the
replacement timeline in [GAO-25-107653](https://www.gao.gov/products/gao-25-107653).

The older references in the April 2026 LAIF guide need a current-facing
correction:

| Legacy reference | Current replacement for the corresponding federal-civilian subject | Implication for LAIF |
|---|---|---|
| OMB **M-24-10** | OMB **M-25-21**, federal agency use, innovation, governance and public trust | Update impact-assessment and internal governance cross-references; do not claim an old memo is active. |
| OMB **M-24-18** | OMB **M-25-22**, federal AI acquisition | Update vendor-assurance and procurement cross-references; do not assert PDCA automatically satisfies contract requirements. |
| Executive Order 14110 | Rescinded in January 2025 | Retain as historical source only, not current executive authority. |

**Additional federal procurement policy:** [OMB M-26-04 (11 December 2025)](https://www.whitehouse.gov/wp-content/uploads/2025/12/M-26-04-Increasing-Public-Trust-in-Artificial-Intelligence-Through-Unbiased-AI-Principles.pdf)
implements the administration's separate procurement requirements concerning
the stated **Unbiased AI Principles** for covered large language models. It
requires relevant contractual terms and agency procedures, subject to its
defined scope and exceptions; it supplements, rather than replaces, the
M-25-21/M-25-22 references above. Record its requirements separately from
technical frontier-safety testing. LAIF does not endorse or independently
validate the memo's policy assumptions.

M-25-21 and M-25-22 are US federal guidance, not universal AI law. Scope,
waivers, acquisition rules, agency implementation and later policy changes
must be verified by responsible legal and acquisition officers. National
security arrangements, state laws and sector laws are outside this brief.

## Australia: current adoption and safety-science context

**Primary sources:** [National AI Plan](https://www.industry.gov.au/publications/national-ai-plan),
[AI Safety Institute](https://www.industry.gov.au/science-technology-and-innovation/technology/artificial-intelligence/ai-safety-institute),
and [mandatory-guardrails consultation outcome](https://consult.industry.gov.au/ai-mandatory-guardrails).

- The Australian Government says it is **not proceeding at this time** with
  its previous broad proposal to introduce mandatory high-risk AI guardrails.
  Do not describe that proposal as enacted law.
- The [Guidance for AI Adoption](https://www.industry.gov.au/publications/voluntary-ai-safety-standard)
  provides voluntary practices; existing general and sector-specific law
  remains relevant. Voluntary guidance creates no new standalone legal duty.
- Australia's AI Safety Institute evaluates emerging capabilities and supports
  regulators and agencies. It is not itself a new AI licensing regulator.

**Potential LAIF adoption route:** an Australian agency or supplier could use
PDCA questions, procurement clauses and independently verified safety-case
evidence as supplemental due diligence. Legal authority, procurement policy,
privacy/security requirements and actual effectiveness still need separate
assessment. This is an opportunity for a controlled pilot, not a claim of
government endorsement.

## Voluntary, international and research sources

- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) and
  the [Generative AI Profile (NIST AI 600-1)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
  are risk-management references, not law by themselves. LAIF can provide
  additional control and protected-interest analysis under Govern, Map,
  Measure and Manage; implementation still requires genuine evidence.
- The [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026)
  and [UK AI Security Institute](https://www.aisi.gov.uk/frontier-ai-trends-report)
  inform evaluation threats and limitations, not legal obligations.
- A regulator or government adopting LAIF would need to address procedural
  rights, confidentiality, independent review, proportionality, enforcement
  powers and contestation. LAIF cannot grant those itself.

## Maintenance and publication rule

1. Keep the April 2026 principal text and paired DOCX/TXT sources intact until
   an explicitly authorised semantic revision. Do not silently rewrite an
   immutable historical guide as if it had always contained current law.
2. Treat this note as **external research**, not verified-corpus ingestion. A
   hyperlink and retrieval date do not establish byte custody or complete
   statutory interpretation. Verify any quoted clause with a trusted source
   snapshot before using it in formal assessment.
3. Recheck this crosswalk at least before each external publication, regulated
   pilot or material legal change. Record sources, dates, exact provisions and
   whether each reference is law, guidance, proposal or historical material.
4. Keep proposed frontier controls and legally operative requirements as
   different columns in a legal/control matrix. An engineer's `REVIEW_READY`
   result cannot be turned into legal `COMPLIANT` or certified `SAFE`.

Related: [Frontier Safety Assurance](../governance/FRONTIER_SAFETY_ASSURANCE.md),
[Result Taxonomy](../governance/RESULT_TAXONOMY.md),
[Publication Status](../../PUBLICATION_STATUS.md).
