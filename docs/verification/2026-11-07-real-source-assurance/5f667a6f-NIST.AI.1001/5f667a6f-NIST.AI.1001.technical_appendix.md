# Technical Appendix — 5f667a6f-NIST.AI.1001.md

## Document metadata

- **original_file_name:** 5f667a6f-NIST.AI.1001.md
- **source_sha256:** 44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509
- **safe_output_stem:** 5f667a6f-NIST.AI.1001

## Processing metadata

- **processed_at_utc:** 2026-11-07T07:43:06Z
- **input_path_original:** docs/verified/raw/5f667a6f-NIST.AI.1001.md
- **original_pending_path:** docs/verified/raw/5f667a6f-NIST.AI.1001.md
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md
- **markdown_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/5f667a6f-NIST.AI.1001/5f667a6f-NIST.AI.1001.laif.md
- **json_output_path:** /workspace/scratch/a966521d6ca7/wide-captured/5f667a6f-NIST.AI.1001/5f667a6f-NIST.AI.1001.laif.json

## Extraction metadata

- **extractor_requested:** builtin
- **extractor_used:** builtin
- **extraction_confidence:** high
- **extracted_characters:** 104630
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
| structural_score | 56 |
| terminology_score | 0 |
| conceptual_proximity_score | 92 |
| auditability_score | 80 |
| enforceability_score | 80 |
| overall_readiness_score | 64 |

## Governance repair fields

```json
{
  "assessment_mode": "external_framework",
  "document_type": "voluntary_risk_framework",
  "governance_force_profile": "Voluntary risk-management framework; high guidance value but limited force unless incorporated into contracts, regulation, assurance, or internal policy gates.",
  "governance_repair_signal_basis": {
    "auditability_score": 80,
    "conceptual_proximity_score": 92,
    "detected_control_gaps": [
      "add rollback/fallback control"
    ],
    "enforceability_score": 80,
    "evidence_trace_count": 20,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 3,
    "remediation_patch_count": 12,
    "sector_profile": "general_ai_governance",
    "sector_risk_alignment": 80,
    "structural_score": 56
  },
  "governance_signal": {
    "score": 84,
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
    "end_char": 61412,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhigh.risk\\b|\\bhigher.risk\\b",
    "matched_text": "high-risk",
    "normalized_match": "high-risk",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 61403,
    "supports": "sector profile signal: high-risk classification language",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 25660,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b",
    "matched_text": "accountability",
    "normalized_match": "accountability",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 25646,
    "supports": "sector profile signal: accountability assignment",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3973,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b",
    "matched_text": "Transparent",
    "normalized_match": "transparent",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 3962,
    "supports": "sector profile signal: transparency requirements",
    "trace_id": "LAIF-TRACE-03-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 68367,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman oversight\\b|\\bhuman determination\\b",
    "matched_text": "human oversight",
    "normalized_match": "human oversight",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 68352,
    "supports": "sector profile signal: human oversight mechanisms",
    "trace_id": "LAIF-TRACE-04-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 44997,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baudit\\b|\\baudit trail\\b",
    "matched_text": "audit",
    "normalized_match": "audit",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 44992,
    "supports": "sector profile signal: audit trail",
    "trace_id": "LAIF-TRACE-05-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 16870,
    "evidence_type": "provenance_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bimpact assessment\\b|\\bFRIA\\b|\\bDPIA\\b",
    "matched_text": "impact assessment",
    "normalized_match": "impact assessment",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 16853,
    "supports": "sector profile signal: impact assessment",
    "trace_id": "LAIF-TRACE-06-provenance-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 29773,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bArticle\\s+\\d+|GOVERN\\s+\\d+\\.\\d+|Section\\s+\\d+\\.?\\d*",
    "matched_text": "Section 5",
    "normalized_match": "section 5",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 29764,
    "supports": "structural signal: numbered sub-requirements",
    "trace_id": "LAIF-TRACE-07-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 66426,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "shall",
    "normalized_match": "shall",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 66421,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-08-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 2906,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\blifecycle\\b|\\blife.cycle\\b|\\bchange\\s+control\\b|\\bre.approval\\b|\\bpost.deployment\\b|\\bpost.implementation\\b|\\bretrain\\w*\\b|\\b(?:decommission|retire|withdraw)\\w*\\b.{0,60}\\b(?:system|model|service|tool)\\b|\\bmaterial\\s+change\\b",
    "matched_text": "Lifecycle",
    "normalized_match": "lifecycle",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 2897,
    "supports": "structural signal: full lifecycle scope declared",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 22311,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\bhigh.risk\\b|\\brisk.{0,5}(?:level|categor|classif)",
    "matched_text": "risk level",
    "normalized_match": "risk level",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 22301,
    "supports": "structural signal: risk stratification / proportionality",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 955,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:mechanisms?|safeguards?|measures?|controls?|procedures?|protocols?)\\b|\\b(?:deployment|approval|assurance)\\s+gate\\b|\\bconditions?\\s+of\\s+use\\b|\\bconditions\\b.{0,60}\\bmust\\s+be\\s+(?:satisfied|met)\\b",
    "matched_text": "procedure",
    "normalized_match": "procedure",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 946,
    "supports": "structural signal: operational mechanisms defined",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 1466,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "review",
    "normalized_match": "review",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 1460,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 96242,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bprecondition\\b|all\\s+(?:three|four|five)\\s+(?:must|shall)\\b|\\bsimultaneously\\b|\\bat\\s+the\\s+same\\s+time\\b|all\\s+of\\s+the\\s+following\\b.{0,80}\\b(?:are\\s+satisfied|hold|apply|must)|(?:some\\s+but\\s+not\\s+all|partial\\s+(?:satisfaction|compliance))\\b.{0,80}\\bis\\s+not\\s+approval\\b",
    "matched_text": "At the same time",
    "normalized_match": "at the same time",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 96226,
    "supports": "structural signal: threshold gate conditions (all must pass simultaneously)",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 28326,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bhuman rights\\b|\\bfundamental rights\\b|\\bhuman interests?\\b|\\bperson.level stakes?\\b|\\baffected persons?\\b|\\bbeneficiar|\\bcivil rights\\b|\\bdata subjects?\\b|\\b(?:applicant|customer|patient|employee|candidate|claimant|citizen|individual|person|resident|student)(?:'|\\u2019)?s?\\s+(?:interest|right)s?\\b|\\brights?\\s+of\\s+(?:the\\s+)?(?:applicant|customer|patient|employee|individual|person)\\b",
    "matched_text": "human rights",
    "normalized_match": "human rights",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 28314,
    "supports": "conceptual signal: human rights / fundamental interests",
    "trace_id": "LAIF-TRACE-14-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3973,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "Transparent",
    "normalized_match": "transparent",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 3962,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-15-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 19121,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bexplainability\\b|\\binterpret\\b|\\bmeaningful\\s+(?:explanation|information)\\b|explain (?:any|each|every) decision|\\bin plain language\\b|words you can understand|\\bexplanation\\s+of\\s+(?:any|each|every|an?|the)\\b.{0,50}\\bdecision\\b|\\bexplain\\w*\\b.{0,60}\\b(?:individual|specific|each)\\s+(?:decision|output|determination)\\b|\\breasons?\\s+for\\s+(?:the|any|each|its)\\s+(?:decision|outcome|determination)\\b|\\bunderstand\\s+and\\s+contest\\b|\\baccount\\s+of\\s+(?:why|how)\\b.{0,80}\\b(?:output|decision|result|determination)\\b",
    "matched_text": "explainability",
    "normalized_match": "explainability",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 19107,
    "supports": "conceptual signal: explainability / interpretability",
    "trace_id": "LAIF-TRACE-16-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 3959,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b|\\baccountable\\b|records? sufficient for audit|\\bauditors?\\b|\\binternal\\s+audit\\b|\\bowner\\s*:|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bsenior\\s+responsible\\s+owner\\b|\\breportable\\s+(?:control\\s+)?breach\\b|\\bresponsible\\s+for\\b.{0,80}\\b(?:compliance|discharg\\w+|the\\s+decision)\\b|\\|\\s*(?:owner|accountable|responsible)\\s*\\|",
    "matched_text": "Accountable",
    "normalized_match": "accountable",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 3948,
    "supports": "conceptual signal: accountability",
    "trace_id": "LAIF-TRACE-17-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 32346,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\boversight\\b|\\bhuman determination\\b|\\bhuman.in.the.loop\\b|escalat\\w+ to a human|human (?:being )?must approve|independent review\\w*|\\bhuman\\s+review\\b|\\bhuman\\s+decision.?maker\\b|\\bhuman\\s+intervention\\b|\\bmanual\\s+review\\b|\\breview\\w*\\s+by\\s+a\\s+(?:human|person|clinician|officer|manager|reviewer)\\b|\\b(?:routed|referred)\\s+to\\s+a\\s+human\\b",
    "matched_text": "oversight",
    "normalized_match": "oversight",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 32337,
    "supports": "conceptual signal: human oversight",
    "trace_id": "LAIF-TRACE-18-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 22311,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bproportionat|\\brisk.{0,5}(?:level|proportion)",
    "matched_text": "risk level",
    "normalized_match": "risk level",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 22301,
    "supports": "conceptual signal: proportionality",
    "trace_id": "LAIF-TRACE-19-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 23948,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bsafety\\b",
    "matched_text": "safety",
    "normalized_match": "safety",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_type": "voluntary_framework",
    "start_char": 23942,
    "supports": "conceptual signal: safety",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Partially expressed construct: Structural Transparency \u2014 some of its substance is present in the document's own vocabulary, but not enough to carry it",
    "evidence_artifact": "Signed control procedure, exception log, and implementation record.",
    "evidence_trace_ids": [
      "LAIF-TRACE-03-sector-profile-signal",
      "LAIF-TRACE-15-governance-force-signal"
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
    "source_evidence": "Transparent",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "patch_id": "LAIF-PATCH-11-low-terminology-score-0-100-missed-signals",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "low",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
    "patch_id": "LAIF-PATCH-12-structured-remediation-step-implicit-prote",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Institutional AI governance owner",
    "severity": "high",
    "source_document": "Artificial Intelligence Risk Management Framework (AI RMF 1.0) \u2014 NIST AI 100-1",
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
  "damaged_token_density": 0.000789,
  "extraction_confidence": "high",
  "extraction_quality_level": "moderate",
  "extractor_used": "builtin",
  "final_gate_failure_count": 4,
  "incomplete_quote_density": 0.12,
  "low_confidence_quote_count": 13,
  "primary_quote_count": 11,
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
    "display_quote": "This publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1 Update Schedule and Versions The Artificial Intelligence Risk Management Framework (AI RMF) is intended to be a living document.",
    "end_offset": 1449,
    "evidence_id": "VQ001",
    "evidence_status": "source_verification_required",
    "evidence_tier": "verification_required_extracted_evidence",
    "exact_quote": "This publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1 Update Schedule and Versions The Artificial Intelligence Risk Management Framework (AI RMF) is intended to be a living document.",
    "extraction_confidence": "high",
    "extraction_issue_reason": "final primary quote admission gate failed: low-confidence reason present: final primary quote admission gate failed: display quote is unreadable as a normal institutional quote / final primary quote admission gate failed: display quote is unreadable as a normal institutional quote",
    "likely_governance_signal": "risk management obligation / residual risk control",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "raw_exact_quote_retained": true,
    "reviewer_instruction": "Review the original source document or a cleaner text extraction before treating this passage as a clean quotation.",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 1232,
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
    "display_quote": "# NIST AI 100-1\n## Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
    "document_type": "voluntary_risk_framework",
    "end_offset": 81,
    "exact_quote": "# NIST AI 100-1\n## Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 0,
    "surrounding_context": "# NIST AI 100-1\n## Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)\nNIST AI 100-1\nArtificial Intelligence Risk Management\nFramework (AI RMF 1.0)\nThis publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1 January 2023",
    "document_type": "voluntary_risk_framework",
    "end_offset": 621,
    "exact_quote": "NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)\nNIST AI 100-1\nArtificial Intelligence Risk Management\nFramework (AI RMF 1.0)\nThis publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1 January 2023",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 294,
    "surrounding_context": "NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)NIST AI 100-1Artificial Intelligence Risk ManagementFramework (AI RMF 1.0)\nNIST AI 100-1\nArtificial Intelligence Risk Management\nFramework (AI RMF 1.0)\nThis publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1 January 2023",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Locascio, NIST Director and Under Secretary of Commerce for Standards and Technology\nCertain commercial entities, equipment, or materials may be identified in this document in order to describe an experimental procedure or concept adequately.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 978,
    "exact_quote": "Locascio, NIST Director and Under Secretary of Commerce for Standards and Technology\nCertain commercial entities, equipment, or materials may be identified in this document in order to describe an experimental procedure or concept adequately.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "generic disclaimer or identification boilerplate; weak verification relevance: boilerplate or generic fragment without reviewer-useful governance signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "generic disclaimer or identification boilerplate",
    "quote_quality_score": 10,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 736,
    "surrounding_context": "Locascio, NIST Director and Under Secretary of Commerce for Standards and Technology\nCertain commercial entities, equipment, or materials may be identified in this document in order to describe an experimental procedure or concept adequately.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The first number will represent the generation of the AI RMF and its companion documents (e.g., 1.0) and will change only with major revisions.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 1905,
    "exact_quote": "The first number will represent the generation of the AI RMF and its companion documents (e.g., 1.0) and will change only with major revisions.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "possible PDF extraction noise, glyph spacing, or malformed fragment",
    "quote_quality_score": 15,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 1762,
    "surrounding_context": "The first number will represent the generation of the AI RMF and its companion documents (e.g., 1.0) and will change only with major revisions.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "All changes will be tracked using a Version Control Table which identifies the history, including version number, date of change, and description of change.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 2146,
    "exact_quote": "All changes will be tracked using a Version Control Table which identifies the history, including version number, date of change, and description of change.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 1990,
    "surrounding_context": "All changes will be tracked using a Version Control Table which identifies the history, including version number, date of change, and description of change.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Comments on the AI RMF Playbook may be sent via email to AIframework@nist.gov at any time and will be reviewed and integrated on a semi-annual basis.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 2349,
    "exact_quote": "Comments on the AI RMF Playbook may be sent via email to AIframework@nist.gov at any time and will be reviewed and integrated on a semi-annual basis.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "generic disclaimer or identification boilerplate; weak verification relevance: boilerplate or generic fragment without reviewer-useful governance signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "generic disclaimer or identification boilerplate",
    "quote_quality_score": 10,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 2200,
    "surrounding_context": "Comments on the AI RMF Playbook may be sent via email to AIframework@nist.gov at any time and will be reviewed and integrated on a semi-annual basis.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "List of Tables\nTable 1 Categories and subcategories for the GOVERN function.22\nTable 2 Categories and subcategories for the MAP function.26\nTable 3 Categories and subcategories for the MEASURE function.29\nTable 4 Categories and subcategories for the MANAGE function.32\ni",
    "document_type": "voluntary_risk_framework",
    "end_offset": 2620,
    "exact_quote": "List of Tables\nTable 1 Categories and subcategories for the GOVERN function.22\nTable 2 Categories and subcategories for the MAP function.26\nTable 3 Categories and subcategories for the MEASURE function.29\nTable 4 Categories and subcategories for the MANAGE function.32\ni",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "incomplete quote could not be expanded to complete evidence statement; final primary quote admission gate failed: incomplete evidence proposition",
    "quote_quality_score": 25,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 2350,
    "surrounding_context": "List of Tables\nTable 1 Categories and subcategories for the GOVERN function.22\nTable 2 Categories and subcategories for the MAP function.26\nTable 3 Categories and subcategories for the MEASURE function.29\nTable 4 Categories and subcategories for the MANAGE function.32\ni",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Trustworthy AI systems and their responsible use can mitigate negative risks and contribute to bene- |  |\n| --- | --- | --- |\n|  | fits for people, organizations, and ecosystems.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 2879,
    "exact_quote": "Trustworthy AI systems and their responsible use can mitigate negative risks and contribute to bene- |  |\n| --- | --- | --- |\n|  | fits for people, organizations, and ecosystems.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "table cell/row requires its source column and assessment context; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ008",
    "quote_quality_reason": "table cell/row requires its source column and assessment context",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 2701,
    "surrounding_context": "Trustworthy AI systems and their responsible use can mitigate negative risks and contribute to bene- |  |\n| --- | --- | --- |\n|  | fits for people, organizations, and ecosystems.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Ideally, risk management efforts start with the Plan and Design function in the application context and are performed throughout the AI system lifecycle.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 3307,
    "exact_quote": "Ideally, risk management efforts start with the Plan and Design function in the application context and are performed throughout the AI system lifecycle.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ009",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 3154,
    "surrounding_context": "Ideally, risk management efforts start with the Plan and Design function in the application context and are performed throughout the AI system lifecycle.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Accountable & Transparent is shown as a vertical box |  |\n|  | because it relates to all other characteristics.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 4059,
    "exact_quote": "Accountable & Transparent is shown as a vertical box |  |\n|  | because it relates to all other characteristics.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "table cell/row requires its source column and assessment context; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ010",
    "quote_quality_reason": "table cell/row requires its source column and assessment context",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 3948,
    "surrounding_context": "Accountable & Transparent is shown as a vertical box |  |\n|  | because it relates to all other characteristics.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "5 | Functions organize AI risk management activities at their highest level to govern, map, measure, and manage AI risks.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 4195,
    "exact_quote": "5 | Functions organize AI risk management activities at their highest level to govern, map, measure, and manage AI risks.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "table cell/row requires its source column and assessment context; weak verification relevance: missing actor or regulated party",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ011",
    "quote_quality_reason": "table cell/row requires its source column and assessment context",
    "quote_quality_score": 30,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 4074,
    "surrounding_context": "5 | Functions organize AI risk management activities at their highest level to govern, map, measure, and manage AI risks.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Page ii\n# Executive Summary\nArtificial intelligence (AI) technologies have significant potential to transform society and people\u2019s lives \u2013 from commerce and health to transportation and cybersecurity to the environment and our planet.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 4565,
    "exact_quote": "Page ii\n# Executive Summary\nArtificial intelligence (AI) technologies have significant potential to transform society and people\u2019s lives \u2013 from commerce and health to transportation and cybersecurity to the environment and our planet.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ012",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 4331,
    "surrounding_context": "Page ii\n# Executive Summary\nArtificial intelligence (AI) technologies have significant potential to transform society and people\u2019s lives \u2013 from commerce and health to transportation and cybersecurity to the environment and our planet.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "This publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1\nUpdate Schedule and Versions\nThe Artificial Intelligence Risk Management Framework (AI RMF) is intended to be a living document.",
    "document_type": "voluntary_risk_framework",
    "end_offset": 1449,
    "evidence_tier": "low_confidence_extraction_trace",
    "exact_quote": "This publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1\nUpdate Schedule and Versions\nThe Artificial Intelligence Risk Management Framework (AI RMF) is intended to be a living document.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "final primary quote admission gate failed: display quote is unreadable as a normal institutional quote",
    "original_file_name": "5f667a6f-NIST.AI.1001.md",
    "passage_role": "document_text",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ013",
    "quote_quality_reason": "primary evidence: complete governance action with actor/control context",
    "quote_quality_score": 90,
    "raw_exact_quote_retained": true,
    "sector_profile": "general_ai_governance",
    "signal_category": "display-normalised source evidence",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verified/raw/5f667a6f-NIST.AI.1001.md",
    "source_sha256": "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    "start_offset": 1232,
    "surrounding_context": "stitute of Standards and Technology, nor is it intended to imply that the entities, materials, or equipment are necessarily the best available for the purpose.\nThis publication is available free of charge from: https://doi.org/10.6028/NIST.AI.100-1\nUpdate Schedule and Versions\nThe Artificial Intelligence Risk Management Framework (AI RMF) is intended to be a living document.\nNIST will review the content and usefulness of the Framework regularly to determine if an update is appropriate; a review with formal input from the AI communi",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains a complete governance signal affected by repairable PDF intra-word spacing.",
    "why_it_matters": "This source evidence required deterministic display normalisation while retaining exact extracted text."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
