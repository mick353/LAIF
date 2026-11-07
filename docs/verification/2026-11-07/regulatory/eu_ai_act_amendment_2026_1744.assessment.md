# LAIF source-scoped assessment — Regulation (EU) 2026/1744

**As at:** 7 November 2026, Australia/Sydney. **Status:** PR #98 review assessment, unmerged and noncanonical. **Method:** Codex-authored source analysis against LAIF v1.2, plus actual unchanged-engine external-framework processing. This assesses the amending instrument, not a fully verified consolidated AI Act, institutional compliance or independent legal advice.

## Finding and authority

Regulation 2026/1744 changes AI Act scope, literacy, bias-data processing, prohibited practices, high-risk requirements, supervision and application dates. It also amends the aviation and machinery regulations. Its simplifications retain express protection floors and procedural safeguards. Those provisions supply identifiable protection and oversight mechanisms; a whole-document engine label cannot establish that they lack governance substance.

The 41-page deposited Official Journal PDF exactly matches a fresh HTTP 200 EUR-Lex download: SHA-256 `0bea4d808256b08275777949ba9cb3c70b7d02e4ebb3ac9b205671b1f552d386`, 1,121,625 bytes. Raw extraction SHA-256 is `dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0`. See `docs/verified/manifests/eu_ai_act_amendment_2026_1744.json`, the page map and `docs/verified/extracted/eu_ai_act_amendment_2026_1744.evidence.json` (Q001–Q027).

[Official publication](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32026R1744). Dated 8 July 2026, published 24 July 2026. Article 4 provides entry into force on the third day after publication: **27 July 2026** (p41, Q027). Entry into force must be distinguished from each amended provision's application date.

The separate original Act PDF is held at `docs/verified/manual_ingest/OJ_L_202401689_EN_TXT.pdf`, SHA-256 `bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e`. PR #90 controls its separate admission. Nothing here merges, overwrites or promotes that PR. A dated consolidated edition and implementing Regulation 2026/1755 were not ingested. This report identifies explicit changes and remaining dependencies; it does not claim a complete current-law assessment of the consolidated Act.

## Regulatory change register

References below are to **Article 1 change-point numbers in the amendment**, not identically numbered Articles of the original Act. These are operative changes (pp15–35); recitals supply context, not substitute duties. Annex XIV occupies pp36–38; Articles 2–4 follow on pp38–41. Read the complete cited provision and exceptions before an actor-specific decision.

| Amendment change points | Regulatory change | Applicability and practical consequence |
|---|---|---|
| (1)–(4), pp15–16 | Adds SMC/SME definitions and innovation emphasis; revises sector-product scope, data-law preservation, equivalence limitations and safety-component definition. | Identify Annex I Section A/B product routes and the particular operator. Equivalent sector requirements do not create a self-selected blanket exemption: the new Article 2(13) requires protection conditions and Commission delegated specification. Q001–Q002. |
| (5), p16 | Replaces Article 4 AI-literacy duty with measures supporting literacy, contextualised by personnel and affected groups; no guarantee of an individual's specified literacy level. | Providers and deployers remain subject to a measures obligation. Retain training rationale and evidence; “no guarantee” does not mean no duty. Q003. |
| (6), p17 | Adds Article 4a's exceptional special-category-data processing for bias detection/correction. | Strict necessity, unavailable effective alternatives, security/access controls, non-transfer and deletion conditions apply. Paragraph 2 extends to stated other actors/systems under conditions and expressly creates no general duty to conduct bias processing. This does not displace data-protection law generally. Q004–Q005. |
| (7), p18 | Inserts Article 5 rules concerning specified non-consensual intimate material and child sexual abuse material. | Provider placing-on-market/putting-into-service conditions differ from deployer-purpose conditions; technical safeguards and national-law exceptions must be read. New prohibitions apply 2 December 2026. No blanket claim about all image generation. Q006–Q007, Q021. |
| (8), p18 | Inserts safety-component qualifications under Article 6. | Convenience and non-safety uses are distinguished from failures that endanger health/safety; do not equate all automation with high-risk classification. Q008. |
| (9)–(11), p19 | Revises data governance, technical documentation and proportionate quality-management implementation for SMEs/SMCs. | Annex IV minimum documentation remains, including the specified simplified form route. Proportional implementation expressly retains required rigour/protection. Q009–Q010. |
| (12)–(13), pp19–20 | Clarifies initial/new-provider cooperation and downstream information/access agreements; allows specified DPIA cross-references in fundamental-rights impact assessments. | Trace the actor change and exceptions, including the stated open-source component boundary (not a universal GPAI exception). Referencing a DPIA is not an exemption from unmet FRIA requirements. Q011–Q012. |
| (14)–(18), pp20–22 | Revises notified-body applications, designation and monitoring; requests joint-compliance standards and adds a conditional cybersecurity presumption via Regulation 2024/2847. | Establish the designated-body and sector-standard routes and each presumption’s conditions. Streamlining does not itself evidence conformity or waive underlying requirements. |
| (19)–(20), p22 | Replaces Article 43(3) product-sector conformity procedures and Article 50(7) synthetic-content code-of-practice arrangements. | Read the sector assessment route, harmonised-standard conditions and 28 January 2028 notified-body designation deadline. Transparency codes concern detection, marking and labelling; they do not themselves prove content compliance. |
| (21)–(25), pp23–25 | Revises code-of-practice evaluation, sandboxes, implementation rules and real-world testing; inserts Article 60a for specified Annex I Section B systems. | Sandbox timetable and testing conditions are distinct from general market authorisation. Article 60a authorisations and safeguards do not create a general permission to test uncontrolled systems. Q013. |
| (26)–(34), pp26–33 | Revises support/governance/supervision and AI Office competences, information and investigation powers, commitments, findings, penalties and procedural protections; adjusts fundamental-rights-authority access. | Determine Article 75(1) competence and the national-authority interface before assigning an enforcer. Judicial authorisation where required, defence/access-to-file and review protections remain material constraints. Q014–Q019. |
| (35)–(38), pp34–35 | Revises codes, guidance, delegated powers and penalties, including SME/SMC treatment. | Track future delegated/implementing instruments separately; proportionality and economic viability do not make obligations voluntary. |
| (39)–(40), p35 | Replaces transitional and application rules in Articles 111/113. | Use the actor/date matrix below; this is not a single postponement of the entire AI Act. Q020–Q023. |
| Annex XIV, pp36–38 | Adds designation codes, including AIH 0401 covering emerging technologies including agentic AI. | A notified-body designation code is not a rule making every agentic AI system high risk. Q024. |
| Articles 2–3, pp38–40 | Amends aviation Regulation 2018/1139 and machinery Regulation 2023/1230, including integration of AI requirements in relevant sector acts. | Product/sector legislation and future acts remain necessary. Machinery delegated requirements are to apply by 2 August 2028 (p40). Q025–Q026. |

This register groups the amendment's changes; it is not a line-by-line legal redline of every unchanged provision in three consolidated regulations.

## Actor and date applicability matrix

| Actor / provision | Date stated in operative source | Reading as at 7 November 2026 |
|---|---|---|
| Amending regulation, Article 4 | Third day after OJ publication: 27 July 2026 | In force; does not erase provision-specific application rules. |
| Original Article 113 general rule and unchanged point (b), checked on deposited original p123 | General application 2 August 2026; specified notified-body/GPAI/governance/penalty chapters and Article 78 from 2 August 2025, except Article 101 | These clauses are not replaced by amendment point (40). They prevent treating the high-risk schedule as an across-the-board delay. See `original_act_dependency.json` and retained exact page extraction; this is a limited dependency check, not promotion of PR #90. |
| Chapters I/II under replaced Article 113(a) | 2 February 2025, except specified new Article 5 provisions | Existing rule is not globally postponed. The new exceptions below have their own date. |
| New Article 5(1)(ba)/(bb), (1a)/(1b) | 2 December 2026 | Future application at the review date. Provider/deployer conditions differ. |
| Providers of synthetic-content systems placed on market before 2 August 2026, Article 111(4) | Comply with Article 50(2) by 2 December 2026 | Transitional deadline, not a permission to ignore other applicable duties. |
| Annex III / Article 6(2) high-risk systems, Chapter III Sections 1–3 except Article 6(5) | 2 December 2027 | These specified provisions are future; assess other duties on their own schedule. |
| Annex I / Article 6(1) high-risk systems, same sections/exception | 2 August 2028 | Product-law route and sector integration must also be checked. |
| Legacy high-risk systems, replaced Article 111(2) | Relevant Chapter III application date, subject to significant design changes; public-authority high-risk providers/deployers by 2 August 2030 | Do not apply the 2030 provision universally. Read the full transitional conditions and prohibition reservation. |
| Member States' sandbox arrangements, amended Article 57 | Operational by 2 August 2027 | Government implementation milestone, not the same obligation as provider conformity. |
| Articles 102–110, amended Article 113(d) | 27 July 2026 | This specifically amended schedule is already operative. |

All p35 date findings are traceable to Q020–Q023 and were checked against the rendered OJ page. Unchanged Article 113 provisions and original Act scope/exclusions must still be joined to the amendment before resolving a real deployment. EEA-relevance wording is not itself proof of domestic incorporation outside EU Member States.

## LAIF interpretation — source analysis

| LAIF construct | Evidence-backed reading | Unresolved assurance question |
|---|---|---|
| Coupling (Q1) | Article 4a conditions connect bias correction and fundamental-rights protection to strict processing restrictions; Article 2(13) retains the overall protection floor. | Does the combined legal and implementation architecture provide inseparable protection and equivalent practical force for each affected interest? An amendment alone cannot establish this universally. |
| Transparency (A.1) | Documentation minimums, specified synthetic-content rules and procedural access supply transparency mechanisms. | Are the required explanations, limitations and records actually usable by affected persons and supervisors? |
| Honesty (A.2) | Documentation and regulator information/investigation powers permit scrutiny of claims. | No execution evidence was supplied for any provider; objective correspondence and evaluation-independent behaviour remain untested. |
| Containment (A.3) | Prohibitions, safeguards, conditioned testing and enforcement powers constrain operation. | Tested bounds, stop authority and irreversible-action controls must be verified at system level. |
| Consistency (Q2) | Protection floors alongside proportional treatment and sector-equivalence conditions constrain simplification. | Need provision-level comparison and real enforcement evidence; proportionality is not proof of universal scale consistency. |
| Reversibility (Q3) | Correction/deletion safeguards, commitments, supervision and legislative revision support change. | They do not demonstrate that every deployed system's effects can be reversed. |
| Self-Application | Judicial/procedural protections and delegated-act oversight constrain governance actors as well as operators. | Actual independence, access and enforcement remain empirical questions. |

No complete Coherence Test or simultaneous Integrity Layer pass is certified here. The original Act's unchanged obligations cannot be declared absent simply because the amending text omits them.

## Actual execution and software limitations

`pypdf-diagnostic/` retains the executed PDF run. Intra-word spacing damage led to `unknown_governance_document` and an inappropriate automatically selected government-service sector. `reviewed-text/` retains a second executed run using the full Poppler text and explicit general-AI sector/source context. The unchanged engine recognises `binding_legal_instrument`, yields formal LAIF-native `FAIL`, structural score **74**, and `ABSENT` on its five functional construct families.

These labels are software observations under a narrow rubric, not a legal finding that the regulation lacks substantive protections. The generated institutional report also identifies whole-document signal saturation, then emits stronger “no remediation” wording; an empty gap register is **not accepted here as completeness evidence**. Its quoted snippets include incomplete propositions. Use the curated exact-page evidence and this analysis, not those snippets as stand-alone legal quotations. No scoring/detector rules were changed to obtain a preferred answer.

Remaining review: join the separately controlled original Act admission, relevant consolidated/implementing/sector texts, and a concrete actor/product/date before final current-law reliance. Human legal/semantic review is outstanding; PR #98 is not merged.
