# Technical Appendix — Policy for the responsible use of AI in government 2_1_1.pdf

## Document metadata

- **original_file_name:** Policy for the responsible use of AI in government 2_1_1.pdf
- **source_sha256:** 7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2
- **safe_output_stem:** Policy-for-the-responsible-use-of-AI-in-government-2_1_1

## Processing metadata

- **processed_at_utc:** 2026-11-07T04:18:13Z
- **input_path_original:** /workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf
- **original_pending_path:** /workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf
- **markdown_output_path:** /workspace/scratch/a966521d6ca7/final-pypdf-run/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.laif.md
- **json_output_path:** /workspace/scratch/a966521d6ca7/final-pypdf-run/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.laif.json

## Extraction metadata

- **extractor_requested:** pypdf
- **extractor_used:** pypdf
- **extraction_confidence:** medium
- **extracted_characters:** 38833
- **warning_count:** 0
- **warnings:** []
- **error_count:** 0
- **errors:** []
- **network_access_used:** False

## Scoring table

| Score | Value |
| --- | --- |
| structural_score | 41 |
| terminology_score | 0 |
| conceptual_proximity_score | 65 |
| auditability_score | 100 |
| enforceability_score | 100 |
| overall_readiness_score | 63 |

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
    "enforceability_score": 100,
    "evidence_trace_count": 20,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 3,
    "remediation_patch_count": 12,
    "sector_profile": "government_service_delivery",
    "sector_risk_alignment": 40,
    "structural_score": 41
  },
  "governance_signal": {
    "score": 86,
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
    "end_char": 345,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:benefit|eligibility|entitlement|licen[cs]e|permit)\\b",
    "matched_text": "Licence",
    "normalized_match": "licence",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 338,
    "supports": "sector profile signal: service eligibility / entitlement decision",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 5919,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:caseworker|service delivery|public service|agency decision)\\b",
    "matched_text": "service delivery",
    "normalized_match": "service delivery",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 5903,
    "supports": "sector profile signal: service-delivery operational actor",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 4526,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bservice-impact (?:record|assessment)\\b|\\bimpact assessment\\b",
    "matched_text": "impact assessment",
    "normalized_match": "impact assessment",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 4509,
    "supports": "sector profile signal: service-impact record",
    "trace_id": "LAIF-TRACE-03-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 9832,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+\\.?\\d*",
    "matched_text": "Section 4",
    "normalized_match": "section 4",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 9823,
    "supports": "structural signal: numbered sub-requirements",
    "trace_id": "LAIF-TRACE-04-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7579,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 7575,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-05-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 22564,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\blifecycle\\b|\\blife.cycle\\b|\\bchange\\s+control\\b|\\bre.approval\\b|\\bpost.deployment\\b|\\bpost.implementation\\b|\\bretrain\\w*\\b|\\b(?:decommission|retire|withdraw)\\w*\\b.{0,60}\\b(?:system|model|service|tool)\\b|\\bmaterial\\s+change\\b",
    "matched_text": "material change",
    "normalized_match": "material change",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 22549,
    "supports": "structural signal: full lifecycle scope declared",
    "trace_id": "LAIF-TRACE-06-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 12483,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\bhigh.risk\\b|\\brisk.{0,5}(?:level|categor|classif)",
    "matched_text": "high risk",
    "normalized_match": "high risk",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 12474,
    "supports": "structural signal: risk stratification / proportionality",
    "trace_id": "LAIF-TRACE-07-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6323,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\\b|\\b(?:deployment|approval|assurance)\\s+gate\\b|\\bconditions?\\s+of\\s+use\\b|\\bconditions\\b.{0,60}\\bmust\\s+be\\s+(?:satisfied|met)\\b",
    "matched_text": "measures",
    "normalized_match": "measures",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 6315,
    "supports": "structural signal: operational mechanisms defined",
    "trace_id": "LAIF-TRACE-08-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 20398,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "monitor",
    "normalized_match": "monitor",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 20391,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 28778,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman rights\\b|\\bfundamental rights\\b|\\bhuman interests?\\b|\\bperson.level stakes?\\b|\\baffected persons?\\b|\\bbeneficiar|\\bcivil rights\\b|\\bdata subjects?\\b|\\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\\u2019)?s?\\s+(?:interest|right)s?\\b|\\brights?\\s+of\\s+(?:the\\s+)?(?:applicant|customer|patient|employee|individual|person)\\b",
    "matched_text": "human rights",
    "normalized_match": "human rights",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 28766,
    "supports": "conceptual signal: human rights / fundamental interests",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 8756,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "transparency",
    "normalized_match": "transparency",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 8744,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6531,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b|\\baccountable\\b|records? sufficient for audit|\\bauditors?\\b|\\binternal\\s+audit\\b|\\bowner\\s*:|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bsenior\\s+responsible\\s+owner\\b|\\breportable\\s+(?:control\\s+)?breach\\b|\\bresponsible\\s+for\\b.{0,80}\\b(?:compliance|discharg\\w+|the\\s+decision)\\b|\\|\\s*(?:owner|accountable|responsible)\\s*\\|",
    "matched_text": "accountability",
    "normalized_match": "accountability",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 6517,
    "supports": "conceptual signal: accountability",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3183,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\boversight\\b|\\bhuman determination\\b|\\bhuman.in.the.loop\\b|escalat\\w+ to a human|human (?:being )?must approve|independent review\\w*|\\bhuman\\s+review\\b|\\bhuman\\s+decision.?maker\\b|\\bhuman\\s+intervention\\b|\\bmanual\\s+review\\b|\\breview\\w*\\s+by\\s+a\\s+(?:human|person|clinician|officer|manager|reviewer)\\b|\\b(?:routed|referred)\\s+to\\s+a\\s+human\\b",
    "matched_text": "oversight",
    "normalized_match": "oversight",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 3174,
    "supports": "conceptual signal: human oversight",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 20465,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\brisk.{0,5}(?:level|proportion)",
    "matched_text": "proportionat",
    "normalized_match": "proportionat",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 20453,
    "supports": "conceptual signal: proportionality",
    "trace_id": "LAIF-TRACE-14-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 17432,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bsafety\\b",
    "matched_text": "safety",
    "normalized_match": "safety",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 17426,
    "supports": "conceptual signal: safety",
    "trace_id": "LAIF-TRACE-15-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6575,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\brisk\\s+(?:management|assessment|governance|control|framework|committee|appetite|register|tolerance|owner)\\w*\\b|\\b(?:model|operational|clinical|credit|conduct)\\s+risk\\b|\\brisk.based\\b",
    "matched_text": "risk-based",
    "normalized_match": "risk-based",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 6565,
    "supports": "conceptual signal: risk governance",
    "trace_id": "LAIF-TRACE-16-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 19398,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bworkers?\\b|\\blabour\\s+rights?\\b|\\bfairness\\b|\\bnon.discriminat\\b",
    "matched_text": "fairness",
    "normalized_match": "fairness",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 19390,
    "supports": "conceptual signal: fairness / labour / non-discrimination",
    "trace_id": "LAIF-TRACE-17-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 9832,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+|Part\\s+\\d+\\b",
    "matched_text": "Section 4",
    "normalized_match": "section 4",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 9823,
    "supports": "auditability signal: numbered traceable requirements",
    "trace_id": "LAIF-TRACE-18-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 853,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:document|record|evidence|technical documentation|certif|report)\\b",
    "matched_text": "document",
    "normalized_match": "document",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 845,
    "supports": "auditability signal: evidence / documentation requirements",
    "trace_id": "LAIF-TRACE-19-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 20398,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:review|audit|monitor|evaluat|inspect|post.market)\\b",
    "matched_text": "monitor",
    "normalized_match": "monitor",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
    "source_type": "uploaded_document",
    "start_char": 20391,
    "supports": "auditability signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-20-governance-force-signal"
  }
]
```

## Remediation patches

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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "high",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, and containment evidence before operational use.",
    "responsible_actor": "Service-delivery policy owner with administrative review / records authority support",
    "severity": "low",
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
    "source_document": "Policy for the responsible use of AI in government 2_1_1",
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
  "damaged_token_density": 0.000968,
  "extraction_confidence": "medium",
  "extraction_quality_level": "moderate",
  "extractor_used": "pypdf",
  "final_gate_failure_count": 7,
  "incomplete_quote_density": 0.25,
  "low_confidence_quote_count": 14,
  "primary_quote_count": 9,
  "primary_quote_eligible": true,
  "recommended_user_action": "Use primary_quote_evidence for clean quotation and verify extraction-impaired passages against the source before quoting them as clean text.",
  "source_text_reliability_warning": "Some evidence-bearing extracted passages require source verification before clean quotation use.",
  "verification_required_count": 1,
  "verification_required_evidence_present": true
}
```

## Verification-required extracted evidence

```json
[
  {
    "display_quote": "Policy for the responsible use of AI in government Page 12 Staff training on AI Agencies must implement mandatory training for all staff on responsible AI use within 12 months of this policy taking effect.",
    "end_offset": 18507,
    "evidence_id": "VQ001",
    "evidence_status": "source_verification_required",
    "evidence_tier": "verification_required_extracted_evidence",
    "exact_quote": "Policy for the responsible use of AI in government Page 12 Staff training on AI Agencies must implement mandatory training for all staff on responsible AI use within 12 months of this policy taking effect.",
    "extraction_confidence": "medium",
    "extraction_issue_reason": "final primary quote admission gate failed: low-confidence reason present: final primary quote admission gate failed: display quote is unreadable as a normal institutional quote / final primary quote admission gate failed: display quote is unreadable as a normal institutional quote",
    "likely_governance_signal": "governance obligation / institutional control signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "raw_exact_quote_retained": true,
    "reviewer_instruction": "Review the original source document or a cleaner text extraction before treating this passage as a clean quotation.",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 18300,
    "verification_relevance_reason": "actor or regulated party present; obligation/action/control signal present; object/control/domain signal present",
    "verification_relevance_score": 3,
    "what_it_can_support": "A source-backed finding that the document appears to contain a relevant governance signal requiring source verification.",
    "what_it_cannot_support": "It cannot be presented as a clean, complete direct quotation or as proof of implementation, sufficiency, legal validity, certification, or operational adoption.",
    "why_retained": "The passage appears evidence-bearing for governance analysis, but extraction quality or proposition completeness prevents clean primary quotation use."
  }
]
```

## Low-confidence extraction/noise findings

- Low-confidence extraction noise: []
- Runner warnings: []

## Low-confidence quote candidates

```json
[
  {
    "display_quote": "If you are having difficulties with accessing this document, please email: ai@dta.",
    "document_type": "public_sector_policy",
    "end_offset": 876,
    "exact_quote": "If you are having difficulties with accessing this document, please email: ai@dta.",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "generic disclaimer or identification boilerplate; weak verification relevance: boilerplate or generic fragment without reviewer-useful governance signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "generic disclaimer or identification boilerplate",
    "quote_quality_score": 10,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 794,
    "surrounding_context": "If you are having difficulties with accessing this document, please email: ai@dta.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "National security carveouts .",
    "document_type": "public_sector_policy",
    "end_offset": 2172,
    "exact_quote": "National security carveouts .",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 2143,
    "surrounding_context": "National security carveouts .",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Principles and requirements .",
    "document_type": "public_sector_policy",
    "end_offset": 3041,
    "exact_quote": "Principles and requirements .",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 3012,
    "surrounding_context": "Principles and requirements .",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Strategy and oversight .",
    "document_type": "public_sector_policy",
    "end_offset": 3185,
    "exact_quote": "Strategy and oversight .",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 3161,
    "surrounding_context": "Strategy and oversight .",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Mandatory requirements .",
    "document_type": "public_sector_policy",
    "end_offset": 3529,
    "exact_quote": "Mandatory requirements .",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 3505,
    "surrounding_context": "Mandatory requirements .",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "AI use case impact assessment .",
    "document_type": "public_sector_policy",
    "end_offset": 4528,
    "exact_quote": "AI use case impact assessment .",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 4497,
    "surrounding_context": "AI use case impact assessment .",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The increasing adoption of artificial intelligence (AI) is reshaping the economy, society and",
    "document_type": "public_sector_policy",
    "end_offset": 5744,
    "exact_quote": "The increasing adoption of artificial intelligence (AI) is reshaping the economy, society and",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 5651,
    "surrounding_context": "The increasing adoption of artificial intelligence (AI) is reshaping the economy, society and",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "enable better data analysis and evidence-based decisions, and improve service delivery for",
    "document_type": "public_sector_policy",
    "end_offset": 5923,
    "exact_quote": "enable better data analysis and evidence-based decisions, and improve service delivery for",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ008",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 5833,
    "surrounding_context": "enable better data analysis and evidence-based decisions, and improve service delivery for",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The Australian Government is committed to capturing the opportunities of AI in a way that",
    "document_type": "public_sector_policy",
    "end_offset": 6036,
    "exact_quote": "The Australian Government is committed to capturing the opportunities of AI in a way that",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ009",
    "quote_quality_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 15,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 5947,
    "surrounding_context": "The Australian Government is committed to capturing the opportunities of AI in a way that",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "It introduces requirements",
    "document_type": "public_sector_policy",
    "end_offset": 6368,
    "exact_quote": "It introduces requirements",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ010",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 6342,
    "surrounding_context": "It introduces requirements",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "for agencies to develop a strategic approach to adopting AI, establish an approach to",
    "document_type": "public_sector_policy",
    "end_offset": 6455,
    "exact_quote": "for agencies to develop a strategic approach to adopting AI, establish an approach to",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ011",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 6370,
    "surrounding_context": "for agencies to develop a strategic approach to adopting AI, establish an approach to",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "operationalise the responsible use of AI, ensure designated accountability for AI use cases,",
    "document_type": "public_sector_policy",
    "end_offset": 6549,
    "exact_quote": "operationalise the responsible use of AI, ensure designated accountability for AI use cases,",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; weak verification relevance: missing actor or regulated party",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ012",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 6457,
    "surrounding_context": "operationalise the responsible use of AI, ensure designated accountability for AI use cases,",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Policy for the responsible use of AI in government\nPage  12\nStaff training on AI\nAgencies must implement mandatory training for all staff on responsible AI use within \n12 months of this policy taking effect.",
    "document_type": "public_sector_policy",
    "end_offset": 18507,
    "evidence_tier": "low_confidence_extraction_trace",
    "exact_quote": "Policy for the responsible use of AI in government\nPage  12\nStaff training on AI\nAgencies must implement mandatory training for all staff on responsible AI use within \n12 months of this policy taking effect.",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "ownership",
    "low_confidence_reason": "final primary quote admission gate failed: display quote is unreadable as a normal institutional quote",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ013",
    "quote_quality_reason": "primary evidence: complete governance action with actor/control context",
    "quote_quality_score": 90,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "accountability/owner",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 18300,
    "surrounding_context": "procedures \nand/or frameworks to support responsible adoption. Accountable officials are responsible \nfor deciding the appropriate approach for their agency. \nPolicy for the responsible use of AI in government\nPage  12\nStaff training on AI\nAgencies must implement mandatory training for all staff on responsible AI use within \n12 months of this policy taking effect. Agencies should consider the Guidance for staff \ntraining on AI and can use the AI fundamentals training module to meet the requirement. \nThey can use the modu",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language relevant to accountability/owner.",
    "why_it_matters": "This is deterministic source evidence for accountability/owner analysis."
  },
  {
    "display_quote": "Agencies must communicate their strategic position on AI to give staff clear direction",
    "document_type": "public_sector_policy",
    "end_offset": 14436,
    "evidence_tier": "low_confidence_extraction_trace",
    "exact_quote": "Agencies must communicate their strategic position on AI to give staff clear direction",
    "extraction_confidence": "medium",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "final primary quote admission gate failed: display quote is unreadable as a normal institutional quote; weak verification relevance: missing object/control/domain signal",
    "original_file_name": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ014",
    "quote_quality_reason": "primary evidence: complete governance action with actor/control context",
    "quote_quality_score": 85,
    "raw_exact_quote_retained": true,
    "sector_profile": "government_service_delivery",
    "signal_category": "display-normalised source evidence",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF/docs/verified/manual_ingest/Policy for the responsible use of AI in government 2_1_1.pdf",
    "source_sha256": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "start_offset": 14350,
    "surrounding_context": "on AI adoption within 6 months of this policy \ntaking effect. This position is to emphasise how AI opportunities can be identified and \nembraced by the agency.\nAgencies must communicate their strategic position on AI to give staff clear direction \non AI adoption. In line with their current and anticipated use of AI, agencies can develop \na standalone AI strategy, augment an existing strategy or create o",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains a complete governance signal affected by repairable PDF intra-word spacing.",
    "why_it_matters": "This source evidence required deterministic display normalisation while retaining exact extracted text."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
