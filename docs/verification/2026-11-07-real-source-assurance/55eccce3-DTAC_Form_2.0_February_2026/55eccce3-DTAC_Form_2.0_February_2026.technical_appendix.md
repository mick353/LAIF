# Technical Appendix — 55eccce3-DTAC_Form_2.0_February_2026.md

## Document metadata

- **original_file_name:** 55eccce3-DTAC_Form_2.0_February_2026.md
- **source_sha256:** d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811
- **safe_output_stem:** 55eccce3-DTAC_Form_2.0_February_2026

## Processing metadata

- **processed_at_utc:** 2026-11-07T07:43:04Z
- **input_path_original:** docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md
- **original_pending_path:** docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md
- **markdown_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/55eccce3-DTAC_Form_2.0_February_2026/55eccce3-DTAC_Form_2.0_February_2026.laif.md
- **json_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/55eccce3-DTAC_Form_2.0_February_2026/55eccce3-DTAC_Form_2.0_February_2026.laif.json

## Extraction metadata

- **extractor_requested:** builtin
- **extractor_used:** builtin
- **extraction_confidence:** high
- **extracted_characters:** 42558
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
| structural_score | 33 |
| terminology_score | 0 |
| conceptual_proximity_score | 50 |
| auditability_score | 80 |
| enforceability_score | 80 |
| overall_readiness_score | 50 |

## Governance repair fields

```json
{
  "assessment_mode": "external_framework",
  "document_type": "sector_assurance_checklist",
  "governance_force_profile": "Sector assurance checklist; useful for assurance triage where mapped to accountable reviewers, evidence artifacts, and pass/fail gates.",
  "governance_repair_signal_basis": {
    "auditability_score": 80,
    "conceptual_proximity_score": 50,
    "detected_control_gaps": [
      "define decision/release gate",
      "add rollback/fallback control"
    ],
    "enforceability_score": 80,
    "evidence_trace_count": 20,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 2,
    "remediation_patch_count": 12,
    "sector_profile": "clinical_ai",
    "sector_risk_alignment": 80,
    "structural_score": 33
  },
  "governance_signal": {
    "score": 68,
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
    "end_char": 9500,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bpatient\\s+(?:safety|harm|risk|consent)\\b",
    "matched_text": "patient safety",
    "normalized_match": "patient safety",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 9486,
    "supports": "sector profile signal: patient safety signal",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 2623,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bdiagnos\\w*\\b|\\btreatment\\b|\\bprescri\\w*\\b",
    "matched_text": "diagnostic",
    "normalized_match": "diagnostic",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 2613,
    "supports": "sector profile signal: diagnostic / treatment language",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 17373,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bclinician\\b|\\bphysician\\b|\\bnurse\\b|\\bhealthcare\\s+professional\\b",
    "matched_text": "clinician",
    "normalized_match": "clinician",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 17364,
    "supports": "sector profile signal: named clinical actor",
    "trace_id": "LAIF-TRACE-03-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1830,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bmedical device\\b|\\bSoftware as a Medical Device\\b|\\bSaMD\\b",
    "matched_text": "medical device",
    "normalized_match": "medical device",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 1816,
    "supports": "sector profile signal: medical device classification",
    "trace_id": "LAIF-TRACE-04-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 352,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 348,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-05-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 13879,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\blifecycle\\b|\\blife.cycle\\b|\\bchange\\s+control\\b|\\bre.approval\\b|\\bpost.deployment\\b|\\bpost.implementation\\b|\\bretrain\\w*\\b|\\b(?:decommission|retire|withdraw)\\w*\\b.{0,60}\\b(?:system|model|service|tool)\\b|\\bmaterial\\s+change\\b",
    "matched_text": "lifecycle",
    "normalized_match": "lifecycle",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 13870,
    "supports": "structural signal: full lifecycle scope declared",
    "trace_id": "LAIF-TRACE-06-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 21619,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\bhigh.risk\\b|\\brisk.{0,5}(?:level|categor|classif)",
    "matched_text": "high risk",
    "normalized_match": "high risk",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 21610,
    "supports": "structural signal: risk stratification / proportionality",
    "trace_id": "LAIF-TRACE-07-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 16111,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\\b|\\b(?:deployment|approval|assurance)\\s+gate\\b|\\bconditions?\\s+of\\s+use\\b|\\bconditions\\b.{0,60}\\bmust\\s+be\\s+(?:satisfied|met)\\b",
    "matched_text": "procedures",
    "normalized_match": "procedures",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 16101,
    "supports": "structural signal: operational mechanisms defined",
    "trace_id": "LAIF-TRACE-08-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 5647,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "review",
    "normalized_match": "review",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 5641,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 23671,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman rights\\b|\\bfundamental rights\\b|\\bhuman interests?\\b|\\bperson.level stakes?\\b|\\baffected persons?\\b|\\bbeneficiar|\\bcivil rights\\b|\\bdata subjects?\\b|\\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\\u2019)?s?\\s+(?:interest|right)s?\\b|\\brights?\\s+of\\s+(?:the\\s+)?(?:applicant|customer|patient|employee|individual|person)\\b",
    "matched_text": "data subject",
    "normalized_match": "data subject",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 23659,
    "supports": "conceptual signal: human rights / fundamental interests",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 23855,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "transparency",
    "normalized_match": "transparency",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 23843,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 22967,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\brisk.{0,5}(?:level|proportion)",
    "matched_text": "proportionat",
    "normalized_match": "proportionat",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 22955,
    "supports": "conceptual signal: proportionality",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 7350,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bsafety\\b",
    "matched_text": "safety",
    "normalized_match": "safety",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 7344,
    "supports": "conceptual signal: safety",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 12717,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bcontest\\w*\\b|\\bappeal\\b|\\bchallenge\\b|\\bredress\\b|\\bremedies\\b|\\brequest\\s+(?:\\w+\\s+){0,2}review\\s+of\\s+(?:any|the|a)\\s+decision\\b|\\bright\\s+(?:to|of)\\s+(?:human|academic|independent|manual)?\\s*review\\b|\\bcomplaints?\\s+(?:process|procedure|route|handling)\\b",
    "matched_text": "challenge",
    "normalized_match": "challenge",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 12708,
    "supports": "conceptual signal: contestability / redress",
    "trace_id": "LAIF-TRACE-14-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 8987,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\brisk\\s+(?:management|assessment|governance|control|framework|committee|appetite|register|tolerance|owner)\\w*\\b|\\b(?:model|operational|clinical|credit|conduct)\\s+risk\\b|\\brisk.based\\b",
    "matched_text": "clinical risk",
    "normalized_match": "clinical risk",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 8974,
    "supports": "conceptual signal: risk governance",
    "trace_id": "LAIF-TRACE-15-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3345,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b.{1,300}\\bshall\\b|\\bmust\\b.{1,300}\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)[^\\n]*\\n(?:\\|[^\\n]*\\n){3,}",
    "matched_text": "must be completed by the manufacturer of a DHT in the first instance. If the manufacturer is not the seller of the product, or placing it on the market, the seller must",
    "normalized_match": "must be completed by the manufacturer of a dht in the first instance. if the manufacturer is not the seller of the product, or placing it on the market, the seller must",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 3177,
    "supports": "auditability signal: multiple mandatory obligations (shall/must pairs)",
    "trace_id": "LAIF-TRACE-16-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3928,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:document|record|evidence|technical documentation|certif|report)\\b",
    "matched_text": "evidence",
    "normalized_match": "evidence",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 3920,
    "supports": "auditability signal: evidence / documentation requirements",
    "trace_id": "LAIF-TRACE-17-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 5647,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:review|audit|monitor|evaluat|inspect|post.market)\\b",
    "matched_text": "review",
    "normalized_match": "review",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 5641,
    "supports": "auditability signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-18-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 12618,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:specific|targeted|defined|identif|concrete|measur)\\b.{0,80}\\b(?:requirement|obligation|measure|standard|criterion)\\b|\\bwithin\\s+\\d+\\s+(?:working\\s+|business\\s+|calendar\\s+)?(?:day|hour|week|month|year)s?\\b|\\b(?:above|below|exceed\\w*|outside|greater\\s+than|less\\s+than)\\b.{0,40}\\d+\\s*%|\\b(?:monthly|quarterly|annual(?:ly)?|weekly|biannual\\w*)\\b.{0,80}\\b(?:review|monitor|report|assess|audit|attest)\\w*|\\b(?:review|monitor|report|assess|audit|attest)\\w*\\b.{0,60}\\b(?:monthly|quarterly|annual(?:ly)?|weekly)\\b",
    "matched_text": "defined in the DCB0129 standard",
    "normalized_match": "defined in the dcb0129 standard",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 12587,
    "supports": "auditability signal: specific, measurable obligations",
    "trace_id": "LAIF-TRACE-19-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 352,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|\\bwe\\s+will\\s+(?:never|not)\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_type": "procurement_standard",
    "start_char": 348,
    "supports": "enforceability signal: mandatory language (shall/must)",
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
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-01-structural-no-precedence-rule-between-the",
    "recommended_patch": "State the order of precedence among this document's own provisions: which prevails if two conflict, which cannot be waived or changed except by a named authority, and what this document is subordinate to. A conflicts clause, a 'without prejudice to' clause, a waiver bar, or a stated parent framework each satisfies this.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "certification channel \u2014 LAIF-native vocabulary not used (expected for an external instrument; not a governance deficiency)",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-02-certification-channel-laif-native-vocabula",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "low",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Missing LAIF construct: Coupling",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-03-missing-laif-construct-coupling",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "high",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: the Coherence Test shall document Q1 Coupling, Q2 Consistency, and Q3 Reversibility before authorization.",
    "diagnostic_gap": "Certification channel \u2014 the Coherence Test is LAIF's named decision instrument; an external document is not expected to contain it",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "planned",
    "laif_construct": "Coherence Test",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-04-certification-channel-the-coherence-test-i",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "low",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Partially expressed construct: Integrity Layer \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-05-partially-expressed-construct-integrity-la",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "high",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Transparency \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [
      "LAIF-TRACE-11-governance-force-signal"
    ],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Transparency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-06-partially-expressed-construct-structural-t",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "transparency",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Honesty \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Honesty",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-07-partially-expressed-construct-structural-h",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Containment \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Containment",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-08-partially-expressed-construct-structural-c",
    "recommended_patch": "Carry the substance already present through to every provision it should govern, so the property holds across the document rather than in the clauses where it happens to appear.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Reversibility",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "reversibility",
    "implementation_priority": "near_term",
    "laif_construct": "Reversibility",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-09-missing-laif-construct-reversibility",
    "recommended_patch": "Add an escalation path and reversibility procedure that identifies who can pause, roll back, review, or remedy the affected decision.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this reversibility control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Low structural score (33/100): missed signals include numbered sub-requirements, threshold gate conditions (all must pass simultaneously), provision hierarchy / precedence rule",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "trigger",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-10-low-structural-score-33-100-missed-signals",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Low structural score (33/100): missed signals include numbered sub-requirements, threshold gate conditions (all must pass simultaneously), provision hierarchy /",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this trigger control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Low terminology score (0/100): missed signals include Coupling, Coherence Test, Integrity Layer",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-11-low-terminology-score-0-100-missed-signals",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "low",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Structured remediation step: Restriction-protection pairing not detected; verify the complete instrument and incorporated protections before proposing changes.",
    "evidence_artifact": "Clinical fallback, override record, patient safety review, incident log, or clinical governance record.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Tie clinical AI use to clinician review, fallback criteria, override logging, patient safety review, and incident escalation.",
    "patch_id": "LAIF-PATCH-12-structured-remediation-step-restriction-pr",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Clinical governance owner with clinician reviewer and safety incident pathway",
    "severity": "medium",
    "source_document": "Digital Technology Assessment Criteria (DTAC) \u2014 Assessment Form v2.0",
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
| Integrity Layer | absent | PARTIAL |
| Reversibility | absent | ABSENT |
| Self-Application | absent | ABSENT |
| Structural Containment | absent | PARTIAL (via Integrity Layer) |
| Structural Honesty | absent | PARTIAL (via Integrity Layer) |
| Structural Transparency | absent | PARTIAL (via Integrity Layer) |

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
  "damaged_token_density": 0.001294,
  "extraction_confidence": "high",
  "extraction_quality_level": "moderate",
  "extractor_used": "builtin",
  "final_gate_failure_count": 2,
  "incomplete_quote_density": 0.173913,
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
    "display_quote": "# Digital Technology Assessment Criteria for Health and Social Care (DTAC)",
    "document_type": "sector_assurance_checklist",
    "end_offset": 74,
    "exact_quote": "# Digital Technology Assessment Criteria for Health and Social Care (DTAC)",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 0,
    "surrounding_context": "# Digital Technology Assessment Criteria for Health and Social Care (DTAC)",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The Digital Technology Assessment Criteria",
    "document_type": "sector_assurance_checklist",
    "end_offset": 213,
    "exact_quote": "The Digital Technology Assessment Criteria",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 171,
    "surrounding_context": "The Digital Technology Assessment Criteria",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Manufacturers must provide this form in lieu of the older v1.0 form from 6 April 2026 when requested by health and care organisations to facilitate assurance of Digital Health Technology products.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 530,
    "exact_quote": "Manufacturers must provide this form in lieu of the older v1.0 form from 6 April 2026 when requested by health and care organisations to facilitate assurance of Digital Health Technology products.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "display quote contains unresolved PDF split-word extraction damage; weak verification relevance: missing object/control/domain signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "display quote contains unresolved PDF split-word extraction damage",
    "quote_quality_score": 15,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 334,
    "surrounding_context": "Manufacturers must provide this form in lieu of the older v1.0 form from 6 April 2026 when requested by health and care organisations to facilitate assurance of Digital Health Technology products.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The Digital Technology Assessment Criteria (DTAC) the assessment framework for digital health technologies (DHTs) bringing together baseline standards and policies that apply to these products.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 838,
    "exact_quote": "The Digital Technology Assessment Criteria (DTAC) the assessment framework for digital health technologies (DHTs) bringing together baseline standards and policies that apply to these products.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 645,
    "surrounding_context": "The Digital Technology Assessment Criteria (DTAC) the assessment framework for digital health technologies (DHTs) bringing together baseline standards and policies that apply to these products.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "| In-scope of DTAC | Out of scope of DTAC |  |\n| --- | --- | --- |\n| DHTs to improve health outcomes | DHTs to improve how the health and care system functions | Hardware, onboard software, embedded software in hardware devices |\n| medical devices classed as software or AI as a medical device, or software designed to work alongside a medical devicesoftware, apps or wearable devices used to help people manage their own health or well-being, or designed to work alongside devices to do so | software or apps designed to help deliver, manage, or administrate the provision of care by the health and care system that might influence the care an individual receives: e.g.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 2254,
    "exact_quote": "| In-scope of DTAC | Out of scope of DTAC |  |\n| --- | --- | --- |\n| DHTs to improve health outcomes | DHTs to improve how the health and care system functions | Hardware, onboard software, embedded software in hardware devices |\n| medical devices classed as software or AI as a medical device, or software designed to work alongside a medical devicesoftware, apps or wearable devices used to help people manage their own health or well-being, or designed to work alongside devices to do so | software or apps designed to help deliver, manage, or administrate the provision of care by the health and care system that might influence the care an individual receives: e.g.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "table cell/row requires its source column and assessment context; weak verification relevance: missing object/control/domain signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "table cell/row requires its source column and assessment context",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 1584,
    "surrounding_context": "| In-scope of DTAC | Out of scope of DTAC |  |\n| --- | --- | --- |\n| DHTs to improve health outcomes | DHTs to improve how the health and care system functions | Hardware, onboard software, embedded software in hardware devices |\n| medical devices classed as software or AI as a medical device, or software designed to work alongside a medical devicesoftware, apps or wearable devices used to help people manage their own health or well-being, or designed to work alongside devices to do so | software or apps designed to help deliver, manage, or administrate the provision of care by the health and care system that might influence the care an individual receives: e.g.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "appointment scheduling or management of digital referrals.Software designed to release staff time, reduce costs or improve efficiency: e.g.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 2394,
    "exact_quote": "appointment scheduling or management of digital referrals.Software designed to release staff time, reduce costs or improve efficiency: e.g.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 2255,
    "surrounding_context": "appointment scheduling or management of digital referrals.Software designed to release staff time, reduce costs or improve efficiency: e.g.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "or example systems for managing utilisation of facilities such as bed management.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 2476,
    "exact_quote": "or example systems for managing utilisation of facilities such as bed management.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 2395,
    "surrounding_context": "or example systems for managing utilisation of facilities such as bed management.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "DSPT), but DTAC as a whole is not an appropriate assessment framework.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 3162,
    "exact_quote": "DSPT), but DTAC as a whole is not an appropriate assessment framework.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ008",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 3092,
    "surrounding_context": "DSPT), but DTAC as a whole is not an appropriate assessment framework.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "DTAC forms must be completed by the manufacturer of a DHT in the first instance.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 3246,
    "exact_quote": "DTAC forms must be completed by the manufacturer of a DHT in the first instance.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ009",
    "quote_quality_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment",
    "quote_quality_score": 15,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 3166,
    "surrounding_context": "DTAC forms must be completed by the manufacturer of a DHT in the first instance.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "If the manufacturer is not the seller of the product, or placing it on the market, the seller must work with the manufacturer to provide a completed DTAC form.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 3406,
    "exact_quote": "If the manufacturer is not the seller of the product, or placing it on the market, the seller must work with the manufacturer to provide a completed DTAC form.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "quote lacks enough actor/action/object/context structure for primary evidence; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ010",
    "quote_quality_reason": "quote lacks enough actor/action/object/context structure for primary evidence",
    "quote_quality_score": 45,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 3247,
    "surrounding_context": "If the manufacturer is not the seller of the product, or placing it on the market, the seller must work with the manufacturer to provide a completed DTAC form.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The assessment criteria are made up of five core components.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 3810,
    "exact_quote": "The assessment criteria are made up of five core components.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ011",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 3750,
    "surrounding_context": "The assessment criteria are made up of five core components.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Sections A and B will provide the assessors the context required to understand your product and support your evidence.",
    "document_type": "sector_assurance_checklist",
    "end_offset": 3929,
    "exact_quote": "Sections A and B will provide the assessors the context required to understand your product and support your evidence.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party",
    "original_file_name": "55eccce3-DTAC_Form_2.0_February_2026.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ012",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "clinical_ai",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
    "source_sha256": "d7272288ce5bb79c0554fcbbe9f6fc5a9c9bf95f9e7b34850edc9c7e698d2811",
    "start_offset": 3811,
    "surrounding_context": "Sections A and B will provide the assessors the context required to understand your product and support your evidence.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
