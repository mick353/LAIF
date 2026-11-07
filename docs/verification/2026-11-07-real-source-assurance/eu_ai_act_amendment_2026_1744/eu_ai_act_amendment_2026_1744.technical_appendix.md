# Technical Appendix — eu_ai_act_amendment_2026_1744.md

## Document metadata

- **original_file_name:** eu_ai_act_amendment_2026_1744.md
- **source_sha256:** dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0
- **safe_output_stem:** eu_ai_act_amendment_2026_1744

## Processing metadata

- **processed_at_utc:** 2026-11-07T07:43:33Z
- **input_path_original:** docs/verified/raw/eu_ai_act_amendment_2026_1744.md
- **original_pending_path:** docs/verified/raw/eu_ai_act_amendment_2026_1744.md
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md
- **markdown_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md
- **json_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.json

## Extraction metadata

- **extractor_requested:** builtin
- **extractor_used:** builtin
- **extraction_confidence:** high
- **extracted_characters:** 182973
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
| structural_score | 74 |
| terminology_score | 0 |
| conceptual_proximity_score | 66 |
| auditability_score | 100 |
| enforceability_score | 100 |
| overall_readiness_score | 72 |

## Governance repair fields

```json
{
  "assessment_mode": "external_framework",
  "document_type": "binding_legal_instrument",
  "governance_force_profile": "Binding legal instrument with public-law force where adopted; operational closure depends on delegated controls, evidence, and enforcement machinery.",
  "governance_repair_signal_basis": {
    "auditability_score": 100,
    "conceptual_proximity_score": 66,
    "detected_control_gaps": [
      "document residual-risk acceptance and review"
    ],
    "enforceability_score": 100,
    "evidence_trace_count": 20,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 4,
    "remediation_patch_count": 12,
    "sector_profile": "general_ai_governance",
    "sector_risk_alignment": 80,
    "structural_score": 74
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
    "end_char": 2621,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhigh.risk\\b|\\bhigher.risk\\b",
    "matched_text": "high-risk",
    "normalized_match": "high-risk",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 2612,
    "supports": "sector profile signal: high-risk classification language",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 42758,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b",
    "matched_text": "accountability",
    "normalized_match": "accountability",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 42744,
    "supports": "sector profile signal: accountability assignment",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 63452,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b",
    "matched_text": "transparency",
    "normalized_match": "transparency",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 63440,
    "supports": "sector profile signal: transparency requirements",
    "trace_id": "LAIF-TRACE-03-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 30148,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat",
    "matched_text": "proportionat",
    "normalized_match": "proportionat",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 30136,
    "supports": "sector profile signal: risk-proportionate obligations",
    "trace_id": "LAIF-TRACE-04-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 54232,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\brisk\\s+(?:register|log|assessment|documentation)\\b",
    "matched_text": "risk assessment",
    "normalized_match": "risk assessment",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 54217,
    "supports": "sector profile signal: risk register / documentation",
    "trace_id": "LAIF-TRACE-05-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 54279,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baudit\\b|\\baudit trail\\b",
    "matched_text": "audit",
    "normalized_match": "audit",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 54274,
    "supports": "sector profile signal: audit trail",
    "trace_id": "LAIF-TRACE-06-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 2791,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btechnical documentation\\b|\\bconformity assessment\\b",
    "matched_text": "conformity assessment",
    "normalized_match": "conformity assessment",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 2770,
    "supports": "sector profile signal: technical documentation",
    "trace_id": "LAIF-TRACE-07-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 101572,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bimpact assessment\\b|\\bFRIA\\b|\\bDPIA\\b",
    "matched_text": "impact assessment",
    "normalized_match": "impact assessment",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 101555,
    "supports": "sector profile signal: impact assessment",
    "trace_id": "LAIF-TRACE-08-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1181,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+\\.?\\d*",
    "matched_text": "Article 114",
    "normalized_match": "article 114",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 1170,
    "supports": "structural signal: numbered sub-requirements",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 38404,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 38400,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 60503,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\blifecycle\\b|\\blife.cycle\\b|\\bchange\\s+control\\b|\\bre.approval\\b|\\bpost.deployment\\b|\\bpost.implementation\\b|\\bretrain\\w*\\b|\\b(?:decommission|retire|withdraw)\\w*\\b.{0,60}\\b(?:system|model|service|tool)\\b|\\bmaterial\\s+change\\b",
    "matched_text": "withdraw or recall the AI system",
    "normalized_match": "withdraw or recall the ai system",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 60471,
    "supports": "structural signal: full lifecycle scope declared",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 2621,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\bhigh.risk\\b|\\brisk.{0,5}(?:level|categor|classif)",
    "matched_text": "high-risk",
    "normalized_match": "high-risk",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 2612,
    "supports": "structural signal: risk stratification / proportionality",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1645,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\\b|\\b(?:deployment|approval|assurance)\\s+gate\\b|\\bconditions?\\s+of\\s+use\\b|\\bconditions\\b.{0,60}\\bmust\\s+be\\s+(?:satisfied|met)\\b",
    "matched_text": "procedure",
    "normalized_match": "procedure",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 1636,
    "supports": "structural signal: operational mechanisms defined",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 16754,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "review",
    "normalized_match": "review",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 16748,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-14-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 40414,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bprecondition\\b|all\\s+(?:three|four|five)\\s+(?:must|shall)\\b|\\bsimultaneously\\b|\\bat\\s+the\\s+same\\s+time\\b|all\\s+of\\s+the\\s+following\\b.{0,80}\\b(?:are\\s+satisfied|hold|apply|must)|(?:some\\s+but\\s+not\\s+all|partial\\s+(?:satisfaction|compliance))\\b.{0,80}\\bis\\s+not\\s+approval\\b",
    "matched_text": "simultaneously",
    "normalized_match": "simultaneously",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 40400,
    "supports": "structural signal: threshold gate conditions (all must pass simultaneously)",
    "trace_id": "LAIF-TRACE-15-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 30936,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bPART ONE\\b|FOUNDATIONAL PRINCIPLES|cannot be amended|non.amendable|\\bin the event of (?:any\\s+)?(?:a\\s+)?conflict\\b.{0,140}\\b(?:prevail|take[s]?\\s+precedence|govern)|\\bnothing in this\\b.{0,140}\\b(?:derogat|limit|override|affect|prejudice)|\\b(?:is|are|shall be)\\s+subordinate to\\b|\\btakes?\\s+precedence over\\b|\\bprevails?\\s+over\\b|\\bshall not be (?:waived|derogated from|disapplied)\\b|\\bnot subject to waiver\\b|\\bmay only be amended by\\b|\\bwithout prejudice to\\b|\\bhierarchy of\\b.{0,60}\\b(?:documents|policies|standards|provisions|instruments)\\b|\\b(?:issued|made|established)\\s+under\\s+the\\b.{0,60}\\b(?:framework|policy|charter|constitution|act|regulation)\\b",
    "matched_text": "without prejudice to",
    "normalized_match": "without prejudice to",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 30916,
    "supports": "structural signal: provision hierarchy / precedence rule",
    "trace_id": "LAIF-TRACE-16-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 2048,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman rights\\b|\\bfundamental rights\\b|\\bhuman interests?\\b|\\bperson.level stakes?\\b|\\baffected persons?\\b|\\bbeneficiar|\\bcivil rights\\b|\\bdata subjects?\\b|\\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\\u2019)?s?\\s+(?:interest|right)s?\\b|\\brights?\\s+of\\s+(?:the\\s+)?(?:applicant|customer|patient|employee|individual|person)\\b",
    "matched_text": "fundamental rights",
    "normalized_match": "fundamental rights",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 2030,
    "supports": "conceptual signal: human rights / fundamental interests",
    "trace_id": "LAIF-TRACE-17-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 63452,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "transparency",
    "normalized_match": "transparency",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 63440,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-18-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 42758,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b|\\baccountable\\b|records? sufficient for audit|\\bauditors?\\b|\\binternal\\s+audit\\b|\\bowner\\s*:|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bsenior\\s+responsible\\s+owner\\b|\\breportable\\s+(?:control\\s+)?breach\\b|\\bresponsible\\s+for\\b.{0,80}\\b(?:compliance|discharg\\w+|the\\s+decision)\\b|\\|\\s*(?:owner|accountable|responsible)\\s*\\|",
    "matched_text": "accountability",
    "normalized_match": "accountability",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 42744,
    "supports": "conceptual signal: accountability",
    "trace_id": "LAIF-TRACE-19-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 30148,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\brisk.{0,5}(?:level|proportion)",
    "matched_text": "proportionat",
    "normalized_match": "proportionat",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_type": "binding_regulation",
    "start_char": 30136,
    "supports": "conceptual signal: proportionality",
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
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
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
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
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
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
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
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Missing LAIF construct: Integrity Layer",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-05-missing-laif-construct-integrity-layer",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "high",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Transparency",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [
      "LAIF-TRACE-03-sector-profile-signal",
      "LAIF-TRACE-18-governance-force-signal"
    ],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Transparency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-06-missing-laif-construct-structural-transpar",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "transparency",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Honesty",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Honesty",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-07-missing-laif-construct-structural-honesty",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Honesty",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Containment",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Containment",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-08-missing-laif-construct-structural-containm",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Containment",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Reversibility",
    "evidence_artifact": "Rollback, appeal, redress, or corrective-action log with closure evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "reversibility",
    "implementation_priority": "near_term",
    "laif_construct": "Reversibility",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Maintain a rollback, appeal, or corrective-action playbook with decision authority and response time expectations.",
    "patch_id": "LAIF-PATCH-09-missing-laif-construct-reversibility",
    "recommended_patch": "Add an escalation path and reversibility procedure that identifies who can pause, roll back, review, or remedy the affected decision.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "medium",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this reversibility control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
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
    "patch_id": "LAIF-PATCH-10-low-terminology-score-0-100-missed-signals",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "low",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Structured remediation step: Implicit protective signals present but not declared as structural Coupling.",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Implement a documented control procedure with owner, input, decision rule, output, exception route, and retention rule.",
    "patch_id": "LAIF-PATCH-11-structured-remediation-step-implicit-prote",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "high",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Structured remediation step: Complete Integrity Layer deployment gate not detected; review transparency, honesty, containment and calibration requirements where applicable.",
    "evidence_artifact": "Audit workpaper or trace sample showing repeatable verification steps and results.",
    "evidence_trace_ids": [
      "LAIF-TRACE-03-sector-profile-signal",
      "LAIF-TRACE-18-governance-force-signal"
    ],
    "finding_type": "construct_gap",
    "governance_force_component": "auditability",
    "implementation_priority": "immediate",
    "laif_construct": "Structural Transparency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Create repeatable audit sampling and trace review steps tied to the control evidence repository.",
    "patch_id": "LAIF-PATCH-12-structured-remediation-step-complete-integ",
    "recommended_patch": "Create a verification test and audit trail that a reviewer can repeat without relying on undocumented discretion.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "high",
    "source_document": "Regulation (EU) 2026/1744 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 (Digital Omnibus on AI)",
    "source_evidence": "transparency",
    "verification_test": "Create a verification test that samples this auditability control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
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
  "damaged_token_density": 0.00056,
  "extraction_confidence": "high",
  "extraction_quality_level": "moderate",
  "extractor_used": "builtin",
  "final_gate_failure_count": 1,
  "incomplete_quote_density": 0.045455,
  "low_confidence_quote_count": 12,
  "primary_quote_count": 10,
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
    "display_quote": "amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the\n              simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus\n                                                           on AI)",
    "document_type": "binding_legal_instrument",
    "end_offset": 915,
    "exact_quote": "amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the\n              simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus\n                                                           on AI)",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 649,
    "surrounding_context": "amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the\n              simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus\n                                                           on AI)",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "(1)     Regulation (EU) 2024/1689 of the European Parliament and of the Council (5) lays down harmonised rules on\n              artificial intelligence (AI) and aims to improve the functioning of the internal market, to promote the uptake of\n              human-centric and trustworthy AI, while ensuring a high level of protection of health, safety and fundamental rights\n              and supporting innovation.",
    "document_type": "binding_legal_instrument",
    "end_offset": 2089,
    "exact_quote": "(1)     Regulation (EU) 2024/1689 of the European Parliament and of the Council (5) lays down harmonised rules on\n              artificial intelligence (AI) and aims to improve the functioning of the internal market, to promote the uptake of\n              human-centric and trustworthy AI, while ensuring a high level of protection of health, safety and fundamental rights\n              and supporting innovation.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "tabular extract requires column/context verification; weak verification relevance: incomplete movement/cross-border fragment without governance obligation",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "tabular extract requires column/context verification",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 1676,
    "surrounding_context": "(1)     Regulation (EU) 2024/1689 of the European Parliament and of the Council (5) lays down harmonised rules on\n              artificial intelligence (AI) and aims to improve the functioning of the internal market, to promote the uptake of\n              human-centric and trustworthy AI, while ensuring a high level of protection of health, safety and fundamental rights\n              and supporting innovation.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "(2)     The experience gathered from the implementation of the parts of Regulation (EU) 2024/1689 that already apply can\n              inform the implementation of those parts that are yet to apply.",
    "document_type": "binding_legal_instrument",
    "end_offset": 2491,
    "exact_quote": "(2)     The experience gathered from the implementation of the parts of Regulation (EU) 2024/1689 that already apply can\n              inform the implementation of those parts that are yet to apply.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "tabular extract requires column/context verification; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "tabular extract requires column/context verification",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 2293,
    "surrounding_context": "(2)     The experience gathered from the implementation of the parts of Regulation (EU) 2024/1689 that already apply can\n              inform the implementation of those parts that are yet to apply.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "In addition, consultations of\n              stakeholders have revealed the need for additional measures to facilitate and provide clarification on implementation\n              and compliance, without reducing the level of protection for health, safety and fundamental rights from AI-related\n              risks that the provisions of Regulation (EU) 2024/1689 seek to achieve.",
    "document_type": "binding_legal_instrument",
    "end_offset": 3278,
    "exact_quote": "In addition, consultations of\n              stakeholders have revealed the need for additional measures to facilitate and provide clarification on implementation\n              and compliance, without reducing the level of protection for health, safety and fundamental rights from AI-related\n              risks that the provisions of Regulation (EU) 2024/1689 seek to achieve.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 2902,
    "surrounding_context": "In addition, consultations of\n              stakeholders have revealed the need for additional measures to facilitate and provide clarification on implementation\n              and compliance, without reducing the level of protection for health, safety and fundamental rights from AI-related\n              risks that the provisions of Regulation (EU) 2024/1689 seek to achieve.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "(5)    Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on\n             artificial intelligence and amending Regulations (EC) No 300/2008, (EU) No 167/2013, (EU) No 168/2013, (EU) 2018/858, (EU)\n             2018/1139 and (EU) 2019/2144 and Directives 2014/90/EU, (EU) 2016/797 and (EU) 2020/1828 (Artificial Intelligence Act) (OJ L,\n             2024/1689, 12.7.2024, ELI: http://data.europa.eu/eli/reg/2024/1689/oj).",
    "document_type": "binding_legal_instrument",
    "end_offset": 4192,
    "exact_quote": "(5)    Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on\n             artificial intelligence and amending Regulations (EC) No 300/2008, (EU) No 167/2013, (EU) No 168/2013, (EU) 2018/858, (EU)\n             2018/1139 and (EU) 2019/2144 and Directives 2014/90/EU, (EU) 2016/797 and (EU) 2020/1828 (Artificial Intelligence Act) (OJ L,\n             2024/1689, 12.7.2024, ELI: http://data.europa.eu/eli/reg/2024/1689/oj).",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "tabular extract requires column/context verification; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "tabular extract requires column/context verification",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 3706,
    "surrounding_context": "(5)    Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on\n             artificial intelligence and amending Regulations (EC) No 300/2008, (EU) No 167/2013, (EU) No 168/2013, (EU) 2018/858, (EU)\n             2018/1139 and (EU) 2019/2144 and Directives 2014/90/EU, (EU) 2016/797 and (EU) 2020/1828 (Artificial Intelligence Act) (OJ L,\n             2024/1689, 12.7.2024, ELI: http://data.europa.eu/eli/reg/2024/1689/oj).",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "(3)    Targeted amendments to Regulation (EU) 2024/1689 are necessary to address certain implementation challenges,\n              with a view to the effective, simple and uniform application of the relevant rules.",
    "document_type": "binding_legal_instrument",
    "end_offset": 4722,
    "exact_quote": "(3)    Targeted amendments to Regulation (EU) 2024/1689 are necessary to address certain implementation challenges,\n              with a view to the effective, simple and uniform application of the relevant rules.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "tabular extract requires column/context verification; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "tabular extract requires column/context verification",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 4509,
    "surrounding_context": "(3)    Targeted amendments to Regulation (EU) 2024/1689 are necessary to address certain implementation challenges,\n              with a view to the effective, simple and uniform application of the relevant rules.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "(4)    In order to enable AI innovation in the private and public sectors, it is important that the Commission and Member\n              States\u2019 competent authorities ensure that the supervision, enforcement and monitoring of sectoral and national laws\n              do not create overlaps, inconsistent interpretations or divergent enforcement.",
    "document_type": "binding_legal_instrument",
    "end_offset": 5078,
    "exact_quote": "(4)    In order to enable AI innovation in the private and public sectors, it is important that the Commission and Member\n              States\u2019 competent authorities ensure that the supervision, enforcement and monitoring of sectoral and national laws\n              do not create overlaps, inconsistent interpretations or divergent enforcement.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "tabular extract requires column/context verification; weak verification relevance: missing actor or regulated party",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "tabular extract requires column/context verification",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 4734,
    "surrounding_context": "(4)    In order to enable AI innovation in the private and public sectors, it is important that the Commission and Member\n              States\u2019 competent authorities ensure that the supervision, enforcement and monitoring of sectoral and national laws\n              do not create overlaps, inconsistent interpretations or divergent enforcement.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "(5)    Regulation (EU) 2024/1689 lays down horizontal rules for AI systems to ensure a consistent and high level of\n              protection of public interests as regards health safety and fundamental rights.",
    "document_type": "binding_legal_instrument",
    "end_offset": 5299,
    "exact_quote": "(5)    Regulation (EU) 2024/1689 lays down horizontal rules for AI systems to ensure a consistent and high level of\n              protection of public interests as regards health safety and fundamental rights.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "tabular extract requires column/context verification; weak verification relevance: missing actor or regulated party",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ008",
    "quote_quality_reason": "tabular extract requires column/context verification",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 5090,
    "surrounding_context": "(5)    Regulation (EU) 2024/1689 lays down horizontal rules for AI systems to ensure a consistent and high level of\n              protection of public interests as regards health safety and fundamental rights.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "For high-risk AI systems referred to in\n              Article 6(1), that Regulation applies in conjunction with the Union harmonisation legislation listed in Section A of\n              Annex I.",
    "document_type": "binding_legal_instrument",
    "end_offset": 5493,
    "exact_quote": "For high-risk AI systems referred to in\n              Article 6(1), that Regulation applies in conjunction with the Union harmonisation legislation listed in Section A of\n              Annex I.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ009",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 5300,
    "surrounding_context": "For high-risk AI systems referred to in\n              Article 6(1), that Regulation applies in conjunction with the Union harmonisation legislation listed in Section A of\n              Annex I.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "In certain cases, it is possible for such Union harmonisation legislation to lay down requirements that\n              achieve the same or a higher level of protection of relevant public interests as achieved by the specific requirements\n              or obligations laid down in Regulation (EU) 2024/1689.",
    "document_type": "binding_legal_instrument",
    "end_offset": 5799,
    "exact_quote": "In certain cases, it is possible for such Union harmonisation legislation to lay down requirements that\n              achieve the same or a higher level of protection of relevant public interests as achieved by the specific requirements\n              or obligations laid down in Regulation (EU) 2024/1689.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ010",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 5494,
    "surrounding_context": "In certain cases, it is possible for such Union harmonisation legislation to lay down requirements that\n              achieve the same or a higher level of protection of relevant public interests as achieved by the specific requirements\n              or obligations laid down in Regulation (EU) 2024/1689.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "In that case, it should be possible to limit the application of\n              specific requirements or obligations laid down in Regulation (EU) 2024/1689 in order to facilitate compliance,\n              minimise administrative burden and duplications, while preserving the level of protection ensured by that\n              Regulation.",
    "document_type": "binding_legal_instrument",
    "end_offset": 6134,
    "exact_quote": "In that case, it should be possible to limit the application of\n              specific requirements or obligations laid down in Regulation (EU) 2024/1689 in order to facilitate compliance,\n              minimise administrative burden and duplications, while preserving the level of protection ensured by that\n              Regulation.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "quote lacks enough actor/action/object/context structure for primary evidence; weak verification relevance: missing object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ011",
    "quote_quality_reason": "quote lacks enough actor/action/object/context structure for primary evidence",
    "quote_quality_score": 45,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 5800,
    "surrounding_context": "In that case, it should be possible to limit the application of\n              specific requirements or obligations laid down in Regulation (EU) 2024/1689 in order to facilitate compliance,\n              minimise administrative burden and duplications, while preserving the level of protection ensured by that\n              Regulation.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The Commission should be empowered to\n              adopt delegated acts to supplement that Regulation by identifying such cases and specifying the products concerned,\n              the requirements or obligations that may be limited, and the conditions and scope of any limitation, ensuring that\n              the level of protection provided by Regulation (EU) 2024/1689 is not reduced.",
    "document_type": "binding_legal_instrument",
    "end_offset": 6839,
    "exact_quote": "The Commission should be empowered to\n              adopt delegated acts to supplement that Regulation by identifying such cases and specifying the products concerned,\n              the requirements or obligations that may be limited, and the conditions and scope of any limitation, ensuring that\n              the level of protection provided by Regulation (EU) 2024/1689 is not reduced.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "quote lacks enough actor/action/object/context structure for primary evidence; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "eu_ai_act_amendment_2026_1744.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ012",
    "quote_quality_reason": "quote lacks enough actor/action/object/context structure for primary evidence",
    "quote_quality_score": 45,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/eu_ai_act_amendment_2026_1744.md",
    "source_sha256": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
    "start_offset": 6451,
    "surrounding_context": "The Commission should be empowered to\n              adopt delegated acts to supplement that Regulation by identifying such cases and specifying the products concerned,\n              the requirements or obligations that may be limited, and the conditions and scope of any limitation, ensuring that\n              the level of protection provided by Regulation (EU) 2024/1689 is not reduced.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
