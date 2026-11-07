# Technical Appendix — 51a29205-OECD_Legal_Instruments.md

## Document metadata

- **original_file_name:** 51a29205-OECD_Legal_Instruments.md
- **source_sha256:** f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6
- **safe_output_stem:** 51a29205-OECD_Legal_Instruments

## Processing metadata

- **processed_at_utc:** 2026-11-07T07:43:02Z
- **input_path_original:** docs/verified/raw/51a29205-OECD_Legal_Instruments.md
- **original_pending_path:** docs/verified/raw/51a29205-OECD_Legal_Instruments.md
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md
- **markdown_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/51a29205-OECD_Legal_Instruments/51a29205-OECD_Legal_Instruments.laif.md
- **json_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/51a29205-OECD_Legal_Instruments/51a29205-OECD_Legal_Instruments.laif.json

## Extraction metadata

- **extractor_requested:** builtin
- **extractor_used:** builtin
- **extraction_confidence:** high
- **extracted_characters:** 29787
- **warning_count:** 0
- **warnings:** []
- **error_count:** 0
- **errors:** []
- **network_access_used:** False

## Integrity Layer requirement signals

All four properties are listed. A matched phrase is not a substantive pass; a non-match is not proof of absence. Assess what the instrument requires separately from actual system behaviour. Calibration applies under LAIF section 2.5.

| Property | Source section | Detector observation |
| --- | --- | --- |
| Structural Transparency | 2.1 | DETECTED_REQUIRES_REVIEW |
| Structural Honesty | 2.2 | NOT_DETECTED_REQUIRES_REVIEW |
| Structural Containment | 2.3 | NOT_DETECTED_REQUIRES_REVIEW |
| Structural Calibration | 2.5 | NOT_DETECTED_REQUIRES_REVIEW |

Substantive Coherence Test determination: source-based review required. Scores, terminology and gap registers do not provide that determination.


## Scoring table

| Score | Value |
| --- | --- |
| structural_score | 49 |
| terminology_score | 0 |
| conceptual_proximity_score | 84 |
| auditability_score | 80 |
| enforceability_score | 40 |
| overall_readiness_score | 53 |

## Governance repair fields

```json
{
  "assessment_mode": "external_framework",
  "document_type": "unknown_governance_document",
  "governance_force_profile": "Governance document with unclear authority; reviewer must establish institutional force, accountable owner, and evidence basis before reliance.",
  "governance_repair_signal_basis": {
    "auditability_score": 80,
    "conceptual_proximity_score": 84,
    "detected_control_gaps": [
      "document residual-risk acceptance and review"
    ],
    "enforceability_score": 40,
    "evidence_trace_count": 20,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 2,
    "remediation_patch_count": 12,
    "sector_profile": "general_ai_governance",
    "sector_risk_alignment": 40,
    "structural_score": 49
  },
  "governance_signal": {
    "score": 69,
    "tier": "MODERATE"
  }
}
```

## Evidence traces

```json
[
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 8821,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b",
    "matched_text": "Accountability",
    "normalized_match": "accountability",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 8807,
    "supports": "sector profile signal: accountability assignment",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7317,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b",
    "matched_text": "Transparency",
    "normalized_match": "transparency",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 7305,
    "supports": "sector profile signal: transparency requirements",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 728,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+\\.?\\d*",
    "matched_text": "Article 5",
    "normalized_match": "article 5",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 719,
    "supports": "structural signal: numbered sub-requirements",
    "trace_id": "LAIF-TRACE-03-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 29586,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "shall",
    "normalized_match": "shall",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 29581,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-04-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 4129,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\blifecycle\\b|\\blife.cycle\\b|\\bchange\\s+control\\b|\\bre.approval\\b|\\bpost.deployment\\b|\\bpost.implementation\\b|\\bretrain\\w*\\b|\\b(?:decommission|retire|withdraw)\\w*\\b.{0,60}\\b(?:system|model|service|tool)\\b|\\bmaterial\\s+change\\b",
    "matched_text": "lifecycle",
    "normalized_match": "lifecycle",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 4120,
    "supports": "structural signal: full lifecycle scope declared",
    "trace_id": "LAIF-TRACE-05-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7034,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\\b|\\b(?:deployment|approval|assurance)\\s+gate\\b|\\bconditions?\\s+of\\s+use\\b|\\bconditions\\b.{0,60}\\bmust\\s+be\\s+(?:satisfied|met)\\b",
    "matched_text": "mechanisms",
    "normalized_match": "mechanisms",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 7024,
    "supports": "structural signal: operational mechanisms defined",
    "trace_id": "LAIF-TRACE-06-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 4401,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "monitor",
    "normalized_match": "monitor",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 4394,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-07-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1843,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bprecondition\\b|all\\s+(?:three|four|five)\\s+(?:must|shall)\\b|\\bsimultaneously\\b|\\bat\\s+the\\s+same\\s+time\\b|all\\s+of\\s+the\\s+following\\b.{0,80}\\b(?:are\\s+satisfied|hold|apply|must)|(?:some\\s+but\\s+not\\s+all|partial\\s+(?:satisfaction|compliance))\\b.{0,80}\\bis\\s+not\\s+approval\\b",
    "matched_text": "at the same time",
    "normalized_match": "at the same time",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 1827,
    "supports": "structural signal: threshold gate conditions (all must pass simultaneously)",
    "trace_id": "LAIF-TRACE-08-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1206,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman rights\\b|\\bfundamental rights\\b|\\bhuman interests?\\b|\\bperson.level stakes?\\b|\\baffected persons?\\b|\\bbeneficiar|\\bcivil rights\\b|\\bdata subjects?\\b|\\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\\u2019)?s?\\s+(?:interest|right)s?\\b|\\brights?\\s+of\\s+(?:the\\s+)?(?:applicant|customer|patient|employee|individual|person)\\b",
    "matched_text": "Human Rights",
    "normalized_match": "human rights",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 1194,
    "supports": "conceptual signal: human rights / fundamental interests",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7317,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "Transparency",
    "normalized_match": "transparency",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 7305,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7336,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bexplainability\\b|\\binterpret\\b|\\bmeaningful\\s+(?:explanation|information)\\b|explain (?:any|each|every) decision|\\bin plain language\\b|words you can understand|\\bexplanation\\s+of\\s+(?:any|each|every|an?|the)\\b.{0,50}\\bdecision\\b|\\bexplain\\w*\\b.{0,60}\\b(?:individual|specific|each)\\s+(?:decision|output|determination)\\b|\\breasons?\\s+for\\s+(?:the|any|each|its)\\s+(?:decision|outcome|determination)\\b|\\bunderstand\\s+and\\s+contest\\b|\\baccount\\s+of\\s+(?:why|how)\\b.{0,80}\\b(?:output|decision|result|determination)\\b",
    "matched_text": "explainability",
    "normalized_match": "explainability",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 7322,
    "supports": "conceptual signal: explainability / interpretability",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 8821,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b|\\baccountable\\b|records? sufficient for audit|\\bauditors?\\b|\\binternal\\s+audit\\b|\\bowner\\s*:|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bsenior\\s+responsible\\s+owner\\b|\\breportable\\s+(?:control\\s+)?breach\\b|\\bresponsible\\s+for\\b.{0,80}\\b(?:compliance|discharg\\w+|the\\s+decision)\\b|\\|\\s*(?:owner|accountable|responsible)\\s*\\|",
    "matched_text": "Accountability",
    "normalized_match": "accountability",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 8807,
    "supports": "conceptual signal: accountability",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7098,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\boversight\\b|\\bhuman determination\\b|\\bhuman.in.the.loop\\b|escalat\\w+ to a human|human (?:being )?must approve|independent review\\w*|\\bhuman\\s+review\\b|\\bhuman\\s+decision.?maker\\b|\\bhuman\\s+intervention\\b|\\bmanual\\s+review\\b|\\breview\\w*\\s+by\\s+a\\s+(?:human|person|clinician|officer|manager|reviewer)\\b|\\b(?:routed|referred)\\s+to\\s+a\\s+human\\b",
    "matched_text": "oversight",
    "normalized_match": "oversight",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 7089,
    "supports": "conceptual signal: human oversight",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 8175,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bsafety\\b",
    "matched_text": "safety",
    "normalized_match": "safety",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 8169,
    "supports": "conceptual signal: safety",
    "trace_id": "LAIF-TRACE-14-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1805,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bcontest\\w*\\b|\\bappeal\\b|\\bchallenge\\b|\\bredress\\b|\\bremedies\\b|\\brequest\\s+(?:\\w+\\s+){0,2}review\\s+of\\s+(?:any|the|a)\\s+decision\\b|\\bright\\s+(?:to|of)\\s+(?:human|academic|independent|manual)?\\s*review\\b|\\bcomplaints?\\s+(?:process|procedure|route|handling)\\b",
    "matched_text": "challenge",
    "normalized_match": "challenge",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 1796,
    "supports": "conceptual signal: contestability / redress",
    "trace_id": "LAIF-TRACE-15-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 9431,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\brisk\\s+(?:management|assessment|governance|control|framework|committee|appetite|register|tolerance|owner)\\w*\\b|\\b(?:model|operational|clinical|credit|conduct)\\s+risk\\b|\\brisk.based\\b",
    "matched_text": "risk management",
    "normalized_match": "risk management",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 9416,
    "supports": "conceptual signal: risk governance",
    "trace_id": "LAIF-TRACE-16-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 9074,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btraceability\\b|\\btraceable\\b|\\bresponsibility\\b.{0,30}\\b(?:outcome|system|decision)\\b|\\baudit\\s+trail\\b|\\bchain\\s+of\\s+custody\\b|\\b(?:record|log|register)\\w*\\b.{0,60}\\b(?:each|every|all|the)\\s+(?:decision|outcome|change|override)s?\\b|\\bversion\\s+control\\b",
    "matched_text": "traceability",
    "normalized_match": "traceability",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 9062,
    "supports": "conceptual signal: traceability / responsibility",
    "trace_id": "LAIF-TRACE-17-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 6440,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bworkers?\\b|\\blabour\\s+rights?\\b|\\bfairness\\b|\\bnon.discriminat\\b",
    "matched_text": "fairness",
    "normalized_match": "fairness",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 6432,
    "supports": "conceptual signal: fairness / labour / non-discrimination",
    "trace_id": "LAIF-TRACE-18-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 728,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+|Part\\s+\\d+\\b",
    "matched_text": "Article 5",
    "normalized_match": "article 5",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 719,
    "supports": "auditability signal: numbered traceable requirements",
    "trace_id": "LAIF-TRACE-19-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 443,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:document|record|evidence|technical documentation|certif|report)\\b",
    "matched_text": "document",
    "normalized_match": "document",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_type": "international_recommendation",
    "start_char": 435,
    "supports": "auditability signal: evidence / documentation requirements",
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
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-01-structural-no-precedence-rule-between-the",
    "recommended_patch": "State the order of precedence among this document's own provisions: which prevails if two conflict, which cannot be waived or changed except by a named authority, and what this document is subordinate to. A conflicts clause, a 'without prejudice to' clause, a waiver bar, or a stated parent framework each satisfies this.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "certification channel \u2014 LAIF-native vocabulary not used (expected for an external instrument; not a governance deficiency)",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-02-certification-channel-laif-native-vocabula",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "low",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Missing LAIF construct: Coupling",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-03-missing-laif-construct-coupling",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "high",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: the Coherence Test shall document Q1 Coupling, Q2 Consistency, and Q3 Reversibility before authorization.",
    "diagnostic_gap": "Certification channel \u2014 the Coherence Test is LAIF's named decision instrument; an external document is not expected to contain it",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "planned",
    "laif_construct": "Coherence Test",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-04-certification-channel-the-coherence-test-i",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "low",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Partially expressed construct: Integrity Layer \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-05-partially-expressed-construct-integrity-la",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "high",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Transparency \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [
      "LAIF-TRACE-02-sector-profile-signal",
      "LAIF-TRACE-10-governance-force-signal"
    ],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Transparency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-06-partially-expressed-construct-structural-t",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Transparency",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Honesty \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Honesty",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-07-partially-expressed-construct-structural-h",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Containment \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Containment",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-08-partially-expressed-construct-structural-c",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Consistency",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Consistency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-09-missing-laif-construct-consistency",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Consistency",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Reversibility \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Rollback, appeal, redress, or corrective-action log with closure evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "reversibility",
    "implementation_priority": "near_term",
    "laif_construct": "Reversibility",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Maintain a rollback, appeal, or corrective-action playbook with decision authority and response time expectations.",
    "patch_id": "LAIF-PATCH-10-partially-expressed-construct-reversibilit",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this reversibility control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Low structural score (49/100): missed signals include risk stratification / proportionality, provision hierarchy / precedence rule, governing body bound by its own rules (self-application)",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [
      "LAIF-TRACE-16-governance-force-signal"
    ],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-11-low-structural-score-49-100-missed-signals",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Low structural score (49/100): missed signals include risk stratification / proportionality, provision hierarchy / precedence rule, governing body bound by its ",
    "responsible_actor": "Departmental AI governance owner with sector subject-matter reviewer",
    "severity": "medium",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
    "source_evidence": "risk management",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Low terminology score (0/100): missed signals include Coupling, Coherence Test, Integrity Layer",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-12-low-terminology-score-0-100-missed-signals",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "low",
    "source_document": "Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449)",
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
| Consistency | absent | ABSENT |
| Coupling | absent | ABSENT |
| Integrity Layer | absent | PARTIAL |
| Reversibility | absent | PARTIAL |
| Self-Application | absent | ABSENT |
| Structural Containment | absent | PARTIAL (via Integrity Layer) |
| Structural Honesty | absent | PARTIAL (via Integrity Layer) |
| Structural Transparency | absent | PARTIAL (via Integrity Layer) |

```json
{
  "Coherence Test": false,
  "Consistency": false,
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
  "damaged_token_density": 0.0,
  "extraction_confidence": "high",
  "extraction_quality_level": "moderate",
  "extractor_used": "builtin",
  "final_gate_failure_count": 8,
  "incomplete_quote_density": 0.421053,
  "low_confidence_quote_count": 12,
  "primary_quote_count": 7,
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

- Low-confidence extraction noise: [{'term': 'Coupling', 'phrase': 22353, 'context': 'ich may be provided by humans or machines;  clarifying that the Recommendation applies to generative AI systems, which produce “content”;  substituting the word “real” with “physical” for clarity and alignment with other international processes;  reflecting the fact that some AI systems can continue to evolve after their design and deployment.  In line with the conclusions of the 2024 Report to Council , t', 'classification': 'low_confidence_extraction_noise', 'reason': 'no_meaningful_governance_context'}]
- Runner warnings: []

## Low-confidence quote candidates

```json
[
  {
    "display_quote": "# OECD Recommendation of the Council on Artificial Intelligence",
    "document_type": "unknown_governance_document",
    "end_offset": 63,
    "exact_quote": "# OECD Recommendation of the Council on Artificial Intelligence",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 0,
    "surrounding_context": "# OECD Recommendation of the Council on Artificial Intelligence",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Recommendation of the Council on Artificial Intelligence",
    "document_type": "unknown_governance_document",
    "end_offset": 650,
    "exact_quote": "Recommendation of the Council on Artificial Intelligence",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "title or isolated heading without governance action; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "title or isolated heading without governance action; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 20,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 594,
    "surrounding_context": "Recommendation of the Council on Artificial Intelligence",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "HAVING REGARD\nto standards developed by the OECD in\nthe areas of privacy, digital security, consumer protection and responsible\nbusiness conduct;",
    "document_type": "unknown_governance_document",
    "end_offset": 979,
    "exact_quote": "HAVING REGARD\nto standards developed by the OECD in\nthe areas of privacy, digital security, consumer protection and responsible\nbusiness conduct;",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 834,
    "surrounding_context": "HAVING REGARD\nto standards developed by the OECD in\nthe areas of privacy, digital security, consumer protection and responsible\nbusiness conduct;",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "HAVING REGARD\nto the important work being carried out\non artificial intelligence (hereafter, \u201cAI\u201d) in other international\ngovernmental and non-governmental fora;",
    "document_type": "unknown_governance_document",
    "end_offset": 1370,
    "exact_quote": "HAVING REGARD\nto the important work being carried out\non artificial intelligence (hereafter, \u201cAI\u201d) in other international\ngovernmental and non-governmental fora;",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 1209,
    "surrounding_context": "HAVING REGARD\nto the important work being carried out\non artificial intelligence (hereafter, \u201cAI\u201d) in other international\ngovernmental and non-governmental fora;",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "RECOGNISING\nthat, at the same time, these\ntransformations may have disparate effects within, and between societies and\neconomies, notably regarding economic shifts, competition, transitions in the\nlabour market, inequalities, and implications for democracy and human rights,\nprivacy and data protection, and digital security;",
    "document_type": "unknown_governance_document",
    "end_offset": 2134,
    "exact_quote": "RECOGNISING\nthat, at the same time, these\ntransformations may have disparate effects within, and between societies and\neconomies, notably regarding economic shifts, competition, transitions in the\nlabour market, inequalities, and implications for democracy and human rights,\nprivacy and data protection, and digital security;",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 1809,
    "surrounding_context": "RECOGNISING\nthat, at the same time, these\ntransformations may have disparate effects within, and between societies and\neconomies, notably regarding economic shifts, competition, transitions in the\nlabour market, inequalities, and implications for democracy and human rights,\nprivacy and data protection, and digital security;",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "RECOGNISING\nthat trust is a key enabler of digital\ntransformation; that, although the nature of future AI applications and their\nimplications may be hard to foresee, the trustworthiness of AI systems is a key\nfactor for the diffusion and adoption of AI; and that a well-informed\nwhole-of-society public debate is necessary for capturing the beneficial\npotential of the technology, while limiting the risks associated with it;",
    "document_type": "unknown_governance_document",
    "end_offset": 2561,
    "exact_quote": "RECOGNISING\nthat trust is a key enabler of digital\ntransformation; that, although the nature of future AI applications and their\nimplications may be hard to foresee, the trustworthiness of AI systems is a key\nfactor for the diffusion and adoption of AI; and that a well-informed\nwhole-of-society public debate is necessary for capturing the beneficial\npotential of the technology, while limiting the risks associated with it;",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 2136,
    "surrounding_context": "RECOGNISING\nthat trust is a key enabler of digital\ntransformation; that, although the nature of future AI applications and their\nimplications may be hard to foresee, the trustworthiness of AI systems is a key\nfactor for the diffusion and adoption of AI; and that a well-informed\nwhole-of-society public debate is necessary for capturing the beneficial\npotential of the technology, while limiting the risks associated with it;",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "UNDERLINING\nthat certain existing national and\ninternational legal, regulatory and policy frameworks already have relevance to\nAI, including those related to human rights, consumer and personal data\nprotection, intellectual property rights, responsible business conduct, and\ncompetition, while noting that the appropriateness of some frameworks may need\nto be assessed and new approaches developed;",
    "document_type": "unknown_governance_document",
    "end_offset": 2961,
    "exact_quote": "UNDERLINING\nthat certain existing national and\ninternational legal, regulatory and policy frameworks already have relevance to\nAI, including those related to human rights, consumer and personal data\nprotection, intellectual property rights, responsible business conduct, and\ncompetition, while noting that the appropriateness of some frameworks may need\nto be assessed and new approaches developed;",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 2563,
    "surrounding_context": "UNDERLINING\nthat certain existing national and\ninternational legal, regulatory and policy frameworks already have relevance to\nAI, including those related to human rights, consumer and personal data\nprotection, intellectual property rights, responsible business conduct, and\ncompetition, while noting that the appropriateness of some frameworks may need\nto be assessed and new approaches developed;",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "RECOGNISING\nthat given the rapid development and\nimplementation of AI, there is a need for a stable policy environment that\npromotes a human-centric approach to trustworthy AI, that fosters research,\npreserves economic incentives to innovate, and that applies to all stakeholders\naccording to their role and the context;",
    "document_type": "unknown_governance_document",
    "end_offset": 3283,
    "exact_quote": "RECOGNISING\nthat given the rapid development and\nimplementation of AI, there is a need for a stable policy environment that\npromotes a human-centric approach to trustworthy AI, that fosters research,\npreserves economic incentives to innovate, and that applies to all stakeholders\naccording to their role and the context;",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ008",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 2963,
    "surrounding_context": "RECOGNISING\nthat given the rapid development and\nimplementation of AI, there is a need for a stable policy environment that\npromotes a human-centric approach to trustworthy AI, that fosters research,\npreserves economic incentives to innovate, and that applies to all stakeholders\naccording to their role and the context;",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The\ndecision to retire an AI system from operation may occur at any point during\nthe operation and monitoring phase.",
    "document_type": "unknown_governance_document",
    "end_offset": 4633,
    "exact_quote": "The\ndecision to retire an AI system from operation may occur at any point during\nthe operation and monitoring phase.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ009",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 4517,
    "surrounding_context": "The\ndecision to retire an AI system from operation may occur at any point during\nthe operation and monitoring phase.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "\u2012\nAI\nknowledge\n:\nAI knowledge refers to the skills and resources, such as data, code,\nalgorithms, models, research, know-how, training programmes, governance,\nprocesses, and best practices required to understand and participate in the AI\nsystem lifecycle, including managing risks.",
    "document_type": "unknown_governance_document",
    "end_offset": 5070,
    "exact_quote": "\u2012\nAI\nknowledge\n:\nAI knowledge refers to the skills and resources, such as data, code,\nalgorithms, models, research, know-how, training programmes, governance,\nprocesses, and best practices required to understand and participate in the AI\nsystem lifecycle, including managing risks.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ010",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 4789,
    "surrounding_context": "\u2012\nAI\nknowledge\n:\nAI knowledge refers to the skills and resources, such as data, code,\nalgorithms, models, research, know-how, training programmes, governance,\nprocesses, and best practices required to understand and participate in the AI\nsystem lifecycle, including managing risks.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "RECOMMENDS\nthat Members and\nnon-Members adhering to this Recommendation (hereafter the \u201cAdherents\u201d) promote\nand implement the following principles for responsible stewardship of\ntrustworthy AI, which are relevant to all stakeholders.",
    "document_type": "unknown_governance_document",
    "end_offset": 5558,
    "exact_quote": "RECOMMENDS\nthat Members and\nnon-Members adhering to this Recommendation (hereafter the \u201cAdherents\u201d) promote\nand implement the following principles for responsible stewardship of\ntrustworthy AI, which are relevant to all stakeholders.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "quote lacks enough actor/action/object/context structure for primary evidence; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ011",
    "quote_quality_reason": "quote lacks enough actor/action/object/context structure for primary evidence",
    "quote_quality_score": 45,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 5325,
    "surrounding_context": "RECOMMENDS\nthat Members and\nnon-Members adhering to this Recommendation (hereafter the \u201cAdherents\u201d) promote\nand implement the following principles for responsible stewardship of\ntrustworthy AI, which are relevant to all stakeholders.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "CALLS ON\nall AI actors to promote\nand implement, according to their respective roles, the following principles\nfor responsible stewardship of trustworthy AI.",
    "document_type": "unknown_governance_document",
    "end_offset": 5722,
    "exact_quote": "CALLS ON\nall AI actors to promote\nand implement, according to their respective roles, the following principles\nfor responsible stewardship of trustworthy AI.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "quote lacks enough actor/action/object/context structure for primary evidence; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "51a29205-OECD_Legal_Instruments.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ012",
    "quote_quality_reason": "quote lacks enough actor/action/object/context structure for primary evidence",
    "quote_quality_score": 45,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
    "source_sha256": "f35d85747b59c41424858536b566c3c66d0782e4d0036a1c3f6244ed5f259fe6",
    "start_offset": 5565,
    "surrounding_context": "CALLS ON\nall AI actors to promote\nand implement, according to their respective roles, the following principles\nfor responsible stewardship of trustworthy AI.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
