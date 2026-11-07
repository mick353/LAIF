# Technical Appendix — au_dta_policy_v2_1.md

## Document metadata

- **original_file_name:** au_dta_policy_v2_1.md
- **source_sha256:** 3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b
- **safe_output_stem:** au_dta_policy_v2_1

## Processing metadata

- **processed_at_utc:** 2026-11-07T07:03:36Z
- **input_path_original:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md
- **original_pending_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md
- **markdown_output_path:** /workspace/scratch/a966521d6ca7/challenge-delivery/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md
- **json_output_path:** /workspace/scratch/a966521d6ca7/challenge-delivery/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.json

## Extraction metadata

- **extractor_requested:** builtin
- **extractor_used:** builtin
- **extraction_confidence:** high
- **extracted_characters:** 44399
- **warning_count:** 0
- **warnings:** []
- **error_count:** 0
- **errors:** []
- **network_access_used:** False

## Integrity Layer requirement signals

All four properties are listed. A matched phrase is not a substantive pass; a non-match is not proof of absence. Assess what the instrument requires separately from actual system behaviour. Calibration applies under LAIF section 2.5.

| Property | Source section | Detector observation |
| --- | --- | --- |
| Structural Transparency | 2.1 | NOT_DETECTED_REQUIRES_REVIEW |
| Structural Honesty | 2.2 | NOT_DETECTED_REQUIRES_REVIEW |
| Structural Containment | 2.3 | NOT_DETECTED_REQUIRES_REVIEW |
| Structural Calibration | 2.5 | NOT_DETECTED_REQUIRES_REVIEW |

Substantive Coherence Test determination: source-based review required. Scores, terminology and gap registers do not provide that determination.


## Scoring table

| Score | Value |
| --- | --- |
| structural_score | 41 |
| terminology_score | 0 |
| conceptual_proximity_score | 65 |
| auditability_score | 100 |
| enforceability_score | 80 |
| overall_readiness_score | 59 |

## Governance repair fields

```json
{
  "assessment_mode": "external_framework",
  "document_type": "public_sector_policy",
  "governance_force_profile": "Public-sector AI policy; force depends on government authority, accountable public-sector owners, disclosure records, human review evidence, exceptions, incidents, and monitoring consequences.",
  "governance_repair_signal_basis": {
    "auditability_score": 100,
    "conceptual_proximity_score": 65,
    "detected_control_gaps": [
      "define decision/release gate",
      "add rollback/fallback control"
    ],
    "enforceability_score": 80,
    "evidence_trace_count": 20,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 3,
    "remediation_patch_count": 12,
    "sector_profile": "government_service_delivery",
    "sector_risk_alignment": 40,
    "structural_score": 41
  },
  "governance_signal": {
    "score": 80,
    "tier": "STRONG"
  }
}
```

## Evidence traces

```json
[
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 442,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:benefit|eligibility|entitlement|licen[cs]e|permit)\\b",
    "matched_text": "Licence",
    "normalized_match": "licence",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 435,
    "supports": "sector profile signal: service eligibility / entitlement decision",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6219,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:caseworker|service delivery|public service|agency decision)\\b",
    "matched_text": "service delivery",
    "normalized_match": "service delivery",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 6203,
    "supports": "sector profile signal: service-delivery operational actor",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 4781,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bservice-impact (?:record|assessment)\\b|\\bimpact assessment\\b",
    "matched_text": "impact assessment",
    "normalized_match": "impact assessment",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 4764,
    "supports": "sector profile signal: service-impact record",
    "trace_id": "LAIF-TRACE-03-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 10189,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+\\.?\\d*",
    "matched_text": "Section 4",
    "normalized_match": "section 4",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 10180,
    "supports": "structural signal: numbered sub-requirements",
    "trace_id": "LAIF-TRACE-04-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7870,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 7866,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-05-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 23345,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\blifecycle\\b|\\blife.cycle\\b|\\bchange\\s+control\\b|\\bre.approval\\b|\\bpost.deployment\\b|\\bpost.implementation\\b|\\bretrain\\w*\\b|\\b(?:decommission|retire|withdraw)\\w*\\b.{0,60}\\b(?:system|model|service|tool)\\b|\\bmaterial\\s+change\\b",
    "matched_text": "material change",
    "normalized_match": "material change",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 23330,
    "supports": "structural signal: full lifecycle scope declared",
    "trace_id": "LAIF-TRACE-06-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 12923,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\bhigh.risk\\b|\\brisk.{0,5}(?:level|categor|classif)",
    "matched_text": "high risk",
    "normalized_match": "high risk",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 12914,
    "supports": "structural signal: risk stratification / proportionality",
    "trace_id": "LAIF-TRACE-07-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6619,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\\b|\\b(?:deployment|approval|assurance)\\s+gate\\b|\\bconditions?\\s+of\\s+use\\b|\\bconditions\\b.{0,60}\\bmust\\s+be\\s+(?:satisfied|met)\\b",
    "matched_text": "measures",
    "normalized_match": "measures",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 6611,
    "supports": "structural signal: operational mechanisms defined",
    "trace_id": "LAIF-TRACE-08-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 21131,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "monitor",
    "normalized_match": "monitor",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 21124,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 29856,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman rights\\b|\\bfundamental rights\\b|\\bhuman interests?\\b|\\bperson.level stakes?\\b|\\baffected persons?\\b|\\bbeneficiar|\\bcivil rights\\b|\\bdata subjects?\\b|\\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\\u2019)?s?\\s+(?:interest|right)s?\\b|\\brights?\\s+of\\s+(?:the\\s+)?(?:applicant|customer|patient|employee|individual|person)\\b",
    "matched_text": "human rights",
    "normalized_match": "human rights",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 29844,
    "supports": "conceptual signal: human rights / fundamental interests",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 9078,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "transparency",
    "normalized_match": "transparency",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 9066,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6825,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b|\\baccountable\\b|records? sufficient for audit|\\bauditors?\\b|\\binternal\\s+audit\\b|\\bowner\\s*:|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bsenior\\s+responsible\\s+owner\\b|\\breportable\\s+(?:control\\s+)?breach\\b|\\bresponsible\\s+for\\b.{0,80}\\b(?:compliance|discharg\\w+|the\\s+decision)\\b|\\|\\s*(?:owner|accountable|responsible)\\s*\\|",
    "matched_text": "accountability",
    "normalized_match": "accountability",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 6811,
    "supports": "conceptual signal: accountability",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3387,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\boversight\\b|\\bhuman determination\\b|\\bhuman.in.the.loop\\b|escalat\\w+ to a human|human (?:being )?must approve|independent review\\w*|\\bhuman\\s+review\\b|\\bhuman\\s+decision.?maker\\b|\\bhuman\\s+intervention\\b|\\bmanual\\s+review\\b|\\breview\\w*\\s+by\\s+a\\s+(?:human|person|clinician|officer|manager|reviewer)\\b|\\b(?:routed|referred)\\s+to\\s+a\\s+human\\b",
    "matched_text": "oversight",
    "normalized_match": "oversight",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 3378,
    "supports": "conceptual signal: human oversight",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 21200,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\brisk.{0,5}(?:level|proportion)",
    "matched_text": "proportionat",
    "normalized_match": "proportionat",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 21188,
    "supports": "conceptual signal: proportionality",
    "trace_id": "LAIF-TRACE-14-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 18105,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bsafety\\b",
    "matched_text": "safety",
    "normalized_match": "safety",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 18099,
    "supports": "conceptual signal: safety",
    "trace_id": "LAIF-TRACE-15-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6868,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\brisk\\s+(?:management|assessment|governance|control|framework|committee|appetite|register|tolerance|owner)\\w*\\b|\\b(?:model|operational|clinical|credit|conduct)\\s+risk\\b|\\brisk.based\\b",
    "matched_text": "risk-based",
    "normalized_match": "risk-based",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 6858,
    "supports": "conceptual signal: risk governance",
    "trace_id": "LAIF-TRACE-16-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 20099,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bworkers?\\b|\\blabour\\s+rights?\\b|\\bfairness\\b|\\bnon.discriminat\\b",
    "matched_text": "fairness",
    "normalized_match": "fairness",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 20091,
    "supports": "conceptual signal: fairness / labour / non-discrimination",
    "trace_id": "LAIF-TRACE-17-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 10189,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+|Part\\s+\\d+\\b",
    "matched_text": "Section 4",
    "normalized_match": "section 4",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 10180,
    "supports": "auditability signal: numbered traceable requirements",
    "trace_id": "LAIF-TRACE-18-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 946,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:document|record|evidence|technical documentation|certif|report)\\b",
    "matched_text": "document",
    "normalized_match": "document",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 938,
    "supports": "auditability signal: evidence / documentation requirements",
    "trace_id": "LAIF-TRACE-19-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 21131,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:review|audit|monitor|evaluat|inspect|post.market)\\b",
    "matched_text": "monitor",
    "normalized_match": "monitor",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_type": "sector_policy",
    "start_char": 21124,
    "supports": "auditability signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-20-governance-force-signal"
  }
]
```

## Remediation patches

Legacy rubric suggestions, not confirmed deficiencies or source-imposed obligations. Reconcile them with the located controls, attributed analysis and applicable authority before proposing a change.

```json
[
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "structural \u2014 no precedence rule between the document's own provisions",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-01-structural-no-precedence-rule-between-the",
    "recommended_patch": "State the order of precedence among this document's own provisions: which prevails if two conflict, which cannot be waived or changed except by a named authority, and what this document is subordinate to. A conflicts clause, a 'without prejudice to' clause, a waiver bar, or a stated parent framework each satisfies this.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "medium",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "certification channel \u2014 LAIF-native vocabulary not used (expected for an external instrument; not a governance deficiency)",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-02-certification-channel-laif-native-vocabula",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "low",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Missing LAIF construct: Coupling",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-03-missing-laif-construct-coupling",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "high",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: the Coherence Test shall document Q1 Coupling, Q2 Consistency, and Q3 Reversibility before authorization.",
    "diagnostic_gap": "Certification channel \u2014 the Coherence Test is LAIF's named decision instrument; an external document is not expected to contain it",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "planned",
    "laif_construct": "Coherence Test",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-04-certification-channel-the-coherence-test-i",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "low",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Missing LAIF construct: Integrity Layer",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-05-missing-laif-construct-integrity-layer",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "high",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Transparency",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [
      "LAIF-TRACE-11-governance-force-signal"
    ],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Transparency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-06-missing-laif-construct-structural-transpar",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "medium",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "transparency",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Honesty",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Honesty",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-07-missing-laif-construct-structural-honesty",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Honesty",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "medium",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Containment",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Containment",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-08-missing-laif-construct-structural-containm",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Containment",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "medium",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Reversibility",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "reversibility",
    "implementation_priority": "near_term",
    "laif_construct": "Reversibility",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-09-missing-laif-construct-reversibility",
    "recommended_patch": "Add an escalation path and reversibility procedure that identifies who can pause, roll back, review, or remedy the affected decision.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "medium",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this reversibility control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Low structural score (41/100): missed signals include threshold gate conditions (all must pass simultaneously), provision hierarchy / precedence rule, governing body bound by its own rules (self-application)",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "trigger",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-10-low-structural-score-41-100-missed-signals",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Low structural score (41/100): missed signals include threshold gate conditions (all must pass simultaneously), provision hierarchy / precedence rule, governing",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "medium",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this trigger control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Low terminology score (0/100): missed signals include Coupling, Coherence Test, Integrity Layer",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-11-low-terminology-score-0-100-missed-signals",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "low",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Structured remediation step: Implicit protective signals present but not declared as structural Coupling.",
    "evidence_artifact": "Reasons-for-decision, review pathway, service-impact record, or case decision log.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Map each service-impacting AI decision to reasons, administrative review, records retention, exception handling, and human caseworker escalation.",
    "patch_id": "LAIF-PATCH-12-structured-remediation-step-implicit-prote",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "high",
    "source_document": "Policy for the responsible use of AI in government v2.1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  }
]
```

## Construct coverage — form and substance

Two independent readings of the same constructs. **LAIF-native form** asks whether the document uses LAIF's canonical term; every external instrument is expected to answer no, and that answer says nothing about its governance. **Functional alignment** asks whether the substance is expressed in the document's own vocabulary. Reading the first column alone will contradict this report's findings.

| Construct | LAIF-native form | Functional alignment |
| --- | --- | --- |
| Coherence Test | absent | — |
| Consistency | present | ABSENT |
| Coupling | absent | ABSENT |
| Integrity Layer | absent | ABSENT |
| Reversibility | absent | ABSENT |
| Self-Application | absent | ABSENT |
| Structural Containment | absent | ABSENT (via Integrity Layer) |
| Structural Honesty | absent | ABSENT (via Integrity Layer) |
| Structural Transparency | absent | ABSENT (via Integrity Layer) |

```json
{
  "Coherence Test": false,
  "Consistency": true,
  "Coupling": false,
  "Integrity Layer": false,
  "Reversibility": false,
  "Structural Containment": false,
  "Structural Honesty": false,
  "Structural Transparency": false
}
```

## Formal LAIF-native certification boundary

Formal LAIF-native certification: Not claimed / not applicable to this external-framework assessment. Construct coverage is internal diagnostic data only.

## Quote display traceability

No primary quote display normalization was required; display quotes match exact extracted substrings.

## Extraction quality profile

```json
{
  "damaged_token_density": 0.000948,
  "extraction_confidence": "high",
  "extraction_quality_level": "high",
  "extractor_used": "builtin",
  "final_gate_failure_count": 0,
  "incomplete_quote_density": 0.0,
  "low_confidence_quote_count": 12,
  "primary_quote_count": 11,
  "primary_quote_eligible": true,
  "recommended_user_action": "Primary quotes may be used normally while retaining exact extracted source traces.",
  "source_text_reliability_warning": "",
  "verification_required_count": 0,
  "verification_required_evidence_present": false
}
```

## Verification-required extracted evidence

```json
[]
```

## Low-confidence extraction/noise findings

- Low-confidence extraction noise: []
- Runner warnings: []

## Low-confidence quote candidates

```json
[
  {
    "display_quote": "If you are having difficulties with accessing this document, please email: ai@dta.gov.au.",
    "document_type": "public_sector_policy",
    "end_offset": 976,
    "exact_quote": "If you are having difficulties with accessing this document, please email: ai@dta.gov.au.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "generic disclaimer or identification boilerplate; weak verification relevance: boilerplate or generic fragment without reviewer-useful governance signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "generic disclaimer or identification boilerplate",
    "quote_quality_score": 10,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 887,
    "surrounding_context": "If you are having difficulties with accessing this document, please email: ai@dta.gov.au.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "5\nImplementation................................................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 2109,
    "exact_quote": "5\nImplementation................................................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 1949,
    "surrounding_context": "5\nImplementation................................................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "6\n        National security carveouts......................................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 2473,
    "exact_quote": "6\n        National security carveouts......................................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 2302,
    "surrounding_context": "6\n        National security carveouts......................................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "8\nPrinciples and requirements........................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 3362,
    "exact_quote": "8\nPrinciples and requirements........................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 3213,
    "surrounding_context": "8\nPrinciples and requirements........................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "9\nStrategy and oversight...................................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 3518,
    "exact_quote": "9\nStrategy and oversight...................................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 3363,
    "surrounding_context": "9\nStrategy and oversight...................................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "10\n        Mandatory requirements...........................................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 3886,
    "exact_quote": "10\n        Mandatory requirements...........................................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 3714,
    "surrounding_context": "10\n        Mandatory requirements...........................................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "12\n        Mandatory requirements...........................................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 4402,
    "exact_quote": "12\n        Mandatory requirements...........................................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 4230,
    "surrounding_context": "12\n        Mandatory requirements...........................................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "13\nAI use case impact assessment.................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 4894,
    "exact_quote": "13\nAI use case impact assessment.................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ008",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 4749,
    "surrounding_context": "13\nAI use case impact assessment.................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "14\n        Mandatory requirements...........................................................................................................................................",
    "document_type": "public_sector_policy",
    "end_offset": 5262,
    "exact_quote": "14\n        Mandatory requirements...........................................................................................................................................",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "insufficient alphabetic governance content; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ009",
    "quote_quality_reason": "insufficient alphabetic governance content",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 5090,
    "surrounding_context": "14\n        Mandatory requirements...........................................................................................................................................",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Policy introduction\nThe increasing adoption of artificial intelligence (AI) is reshaping the economy, society and\ngovernment.",
    "document_type": "public_sector_policy",
    "end_offset": 6058,
    "exact_quote": "Policy introduction\nThe increasing adoption of artificial intelligence (AI) is reshaping the economy, society and\ngovernment.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no governance action, obligation, risk, evidence, or control term; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ010",
    "quote_quality_reason": "no governance action, obligation, risk, evidence, or control term",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 5933,
    "surrounding_context": "Policy introduction\nThe increasing adoption of artificial intelligence (AI) is reshaping the economy, society and\ngovernment.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Government agencies are embracing the AI opportunity to boost efficiency,\nenable better data analysis and evidence-based decisions, and improve service delivery for\npeople and business.",
    "document_type": "public_sector_policy",
    "end_offset": 6244,
    "exact_quote": "Government agencies are embracing the AI opportunity to boost efficiency,\nenable better data analysis and evidence-based decisions, and improve service delivery for\npeople and business.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ011",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 6059,
    "surrounding_context": "Government agencies are embracing the AI opportunity to boost efficiency,\nenable better data analysis and evidence-based decisions, and improve service delivery for\npeople and business.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The Australian Government is committed to capturing the opportunities of AI in a way that\nfacilitates innovation while mitigating harms.",
    "document_type": "public_sector_policy",
    "end_offset": 6382,
    "exact_quote": "The Australian Government is committed to capturing the opportunities of AI in a way that\nfacilitates innovation while mitigating harms.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "au_dta_policy_v2_1.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ012",
    "quote_quality_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment",
    "quote_quality_score": 15,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/au_dta_policy_v2_1.md",
    "source_sha256": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "start_offset": 6246,
    "surrounding_context": "The Australian Government is committed to capturing the opportunities of AI in a way that\nfacilitates innovation while mitigating harms.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
