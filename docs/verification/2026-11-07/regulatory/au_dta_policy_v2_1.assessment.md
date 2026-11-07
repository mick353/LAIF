# LAIF source-scoped assessment — Australian DTA Policy v2.1

**As at:** 7 November 2026, Australia/Sydney. **Status:** PR #98 review assessment, unmerged and noncanonical. **Method:** Codex-authored source analysis against LAIF v1.2 and Compliance Toolkit v1.1, accompanied by actual unchanged-engine external-framework processing. This is neither an independent scholarly validation nor a legal compliance certificate.

## Finding and decision

The policy establishes mandatory agency accountability, documented screening, pre-deployment impact assessment, incident handling and enhanced high-risk oversight. It supplies concrete governance controls relevant to LAIF; the engine's `ABSENT` functional-construct labels must not be read as evidence that the policy has no protections. Whether an agency implements the controls requires agency records that were not supplied.

Version 2.1 should be used for a policy reading as at this review date. Retain the deposited v2.0 PDF and the protected historical assessment unchanged. Version 2.1 adds the classification system in Appendix D; it does not restart the v2.0 implementation clock.

## Evidence and authority

- Source: `docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf`, 26 PDF pages.
- PDF SHA-256: `7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2`.
- Full raw extraction SHA-256: `3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b`.
- Manifest: `docs/verified/manifests/au_dta_policy_v2_1.json`; exact quotations: `docs/verified/extracted/au_dta_policy_v2_1.evidence.json` (Q001–Q017), with physical page boundaries and character offsets.
- Official [policy page](https://www.digital.gov.au/ai/ai-in-government-policy) and [versioned PDF URL](https://www.digital.gov.au/sites/default/files/documents/2026-10/Policy%20for%20the%20responsible%20use%20of%20AI%20in%20government%202_1_1.pdf). The official page corroborated version and dates. Direct PDF retrieval returned HTTP 503 twice; upstream-byte equivalence is **not established**. `HUMAN_ATTESTED_AUTHORITATIVE` records the owner's identified authoritative deposit; the local PDF and extracted text are SHA-256 verified.

PDF page indices coincide with printed Arabic numbers from page 4 onward; front matter uses Roman numerals. Source text, including copyright and attribution, is retained. Poppler layout extraction was selected because pypdf inserted spurious intra-word breaks in parts of these PDFs. No semantic text repair or OCR was performed. Tables remain layout text and require attention to their column headings.

## Applicability and timing

| Question | Source position | Practical consequence |
|---|---|---|
| Which organisations? | Non-corporate Commonwealth entities must apply the policy; corporate Commonwealth entities are encouraged (p6, Q001). | Determine entity status before treating these as mandatory agency controls. This is not an across-economy AI statute. |
| Carveouts | Defence portfolio AI use and the defined national intelligence community are excluded, with voluntary adoption possible (p6). | Apply the carveout to its stated functions and actors; do not infer a blanket exclusion for every activity of every partly listed organisation. |
| Effective date | v2.0 effective 15 December 2025; v2.1 minor updates published 21 October 2026 (p6, Q002). | Six- and twelve-month periods remain anchored to 15 December 2025: 15 June and 15 December 2026 respectively. |
| Agency deadlines | Strategic position within six months; use-case ownership/register, operational approach and mandatory staff training within twelve months (pp10–14, Q003–Q007). | At 7 November 2026 the six-month deadline has passed; the twelve-month deadline has not. No agency-specific breach is inferred. |
| New and existing use cases | Screen new cases during design. Begin assessments within twelve months; apply relevant actions to existing cases not yet assessed by 30 April 2027 (p14, Q007). | Distinguish organisational rollout dates from the requirement to finalise an in-scope assessment and agreed treatments before deployment (Q008). |
| Scope criteria | Harm, material administrative influence, unreviewed public interaction/impact, personal or sensitive/classified data, or DTA-directed elevated risk (p21, Q012). | Document screening; classification into a usage pattern alone is not a high-risk determination. |
| Early experimentation | Exception requires no commitment affecting later implementation, no risk of harm and no added privacy/security risks (p22, Q013). | A label such as “pilot” is insufficient. Record the conditions and reassess if moving towards adoption. |
| Ongoing use | Revalidate on material change; monitor vendor/regulatory changes; high-risk cases have reporting, executive/board governance and at least annual review (pp15–16, Q009–Q011). | Preserve owner, risk, incident and change records throughout operation. Medium-risk additional governance is expressed as a recommendation, not the high-risk mandatory rule. |

## Verified v2.0 to v2.1 delta

`dta_version_delta.json` records the historical PDF hash, all old-page extraction hashes and page comparisons. Both deposited PDFs were extracted with Poppler 24.02.0; comparison collapses whitespace only. Pages 7–22 match. Front matter and page 6 update version/date wording; pages 23–26 add Appendix D. Thus the principal mandatory-control pages 10–16 and scope pages 21–22 are textually unchanged by this comparison.

Appendix D requires classification in the use-case register, impact assessment tool and transparency statement (p23, Q014). The seven usage patterns are decision-making and administrative action, analytics, strategic support, workplace productivity, workflow automation, image processing and coding. The six domains are service delivery, compliance and fraud detection, law enforcement/intelligence/security, policy and legal, scientific, and corporate and enabling (pp23–26, Q014–Q017). Multiple meaningful patterns/domains may be selected.

Operational change: reconcile existing register and transparency fields to this taxonomy, retain old-to-new mappings and review multi-purpose cases. This is a newly included classification instruction in the PDF, not evidence of newly introduced underlying duties or a changed external standard. Historical linked taxonomy/standards were not acquired here; a claim that every external dependency is unchanged would exceed the comparison.

## LAIF interpretation — source analysis, separate from machine verdicts

| LAIF construct | Source-backed assessment | Evidence still required for an institution |
|---|---|---|
| Coupling (Q1) | Harm-based scope and proportionate treatment identify human interests; pre-deployment assessment connects risk identification to action. This supports functional protection, but the policy alone does not demonstrate LAIF's full inseparable pairing and equivalent protective force for every restriction. | Completed risk assessments, named beneficiaries/interests, approved treatments and challenge/redress routes. |
| Structural Transparency (A.1) | Public statements, documented assessments and staff explanation/accountability expectations support transparency (pp10–15). A public statement alone does not prove a comprehensible account of an individual system output. | Actual public statement, decision explanation, limitations and uncertainty disclosures. |
| Structural Honesty (A.2) | Monitoring intended operation and periodic high-risk review provide an implementation check (pp15–16). They do not demonstrate evaluation-independent behaviour. | Stated-versus-implemented objectives, test records and independent challenge. |
| Structural Containment (A.3) | Pre-deployment treatments and governed incident remediation provide control points (pp12,14). | Tested operational bounds, escalation/stop authority and authority for materially irreversible actions. |
| Consistency (Q2) | Common screening criteria, risk-proportionate oversight and internal assessment processes giving the same or higher risk outcomes support consistency (pp14–16,21). | Cross-case and cross-agency calibration with justified exceptions, rather than a scale-invariance claim based on policy text alone. |
| Reversibility (Q3) | Revalidation, monitoring and incident remediation support revision (pp12,15–16). | Tested rollback, correction of affected decisions and preservation of future options. |
| Self-Application | Accountable officials and executive oversight apply governance to the adopting agency itself (pp11–12,16). | Oversight independence, conflicts controls, escalations and evidence that the governing process is itself reviewed. |

None of the three Integrity Layer preconditions or the complete Coherence Test is certified as passed by this documentary analysis. The policy is an external instrument and need not adopt LAIF vocabulary.

## Actual engine execution and its limits

Both pypdf PDF processing and the reviewed-text route executed successfully; retained outputs are under `pypdf-diagnostic/au_dta_policy_v2_1/` and `reviewed-text/au_dta_policy_v2_1/`. The latter uses the committed full text, explicit public-sector context and the unchanged canonical engine. Its source hash identifies the extracted text; the run manifest and provenance record link that hash back to the original PDF.

The engine classifies `public_sector_policy`, returns formal LAIF-native `FAIL`, structural score **41**, and `ABSENT` for its five functional construct families. These are reproducible software outputs under its current rules, not established legal or empirical conclusions. In particular, Q003–Q011 show operative protective controls despite the family labels. Institutional report prose about missing machinery overstates what those labels establish; use this source-scoped analysis and exact evidence rather than repeating that prose as a finding about the policy. Scores are not percentages of compliance or safety.

The protected historical report is not recalculated or contradicted by silently applying a different engine. These are separate dated assessments with distinct methods. Human policy/semantic review remains outstanding; implementation assurance requires the actual agency evidence listed above.
