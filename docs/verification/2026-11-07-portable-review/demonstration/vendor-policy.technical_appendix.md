# Technical Appendix — vendor-policy.md

## Document metadata

- **original_file_name:** vendor-policy.md
- **source_sha256:** e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523
- **safe_output_stem:** vendor-policy

## Processing metadata

- **processed_at_utc:** 2026-11-07T07:16:59Z
- **input_path_original:** docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md
- **original_pending_path:** docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md
- **stored_source_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md
- **runner_input_path:** /workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md
- **markdown_output_path:** ../portable-demonstration-output/vendor-policy.laif.md
- **json_output_path:** ../portable-demonstration-output/vendor-policy.laif.json

## Extraction metadata

- **extractor_requested:** builtin
- **extractor_used:** builtin
- **extraction_confidence:** high
- **extracted_characters:** 1287
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
| structural_score | 14 |
| terminology_score | 0 |
| conceptual_proximity_score | 16 |
| auditability_score | 80 |
| enforceability_score | 60 |
| overall_readiness_score | 35 |

## Governance repair fields

```json
{
  "assessment_mode": "external_framework",
  "document_type": "procurement_assessment_form",
  "governance_force_profile": "Procurement assessment form; force arises through procurement conditions, contract clauses, supplier obligations, and audit rights.",
  "governance_repair_signal_basis": {
    "auditability_score": 80,
    "conceptual_proximity_score": 16,
    "detected_control_gaps": [
      "document residual-risk acceptance and review"
    ],
    "enforceability_score": 60,
    "evidence_trace_count": 13,
    "formal_laif_native_compliance": "FAIL",
    "high_severity_patch_count": 2,
    "remediation_patch_count": 12,
    "sector_profile": "procurement_vendor_governance",
    "sector_risk_alignment": 40,
    "structural_score": 14
  },
  "governance_signal": {
    "score": 48,
    "tier": "WEAK"
  }
}
```

## Evidence traces

```json
[
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 790,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bprocurement\\b|\\bRFP\\b|\\btender\\b",
    "matched_text": "procurement",
    "normalized_match": "procurement",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 779,
    "supports": "sector profile signal: procurement process",
    "trace_id": "LAIF-TRACE-01-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 18,
    "evidence_type": "sector_profile_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bvendor\\b|\\bsupplier\\b|\\bthird[- ]party\\b",
    "matched_text": "supplier",
    "normalized_match": "supplier",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 10,
    "supports": "sector profile signal: vendor / third-party actor",
    "trace_id": "LAIF-TRACE-02-sector-profile-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 374,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 370,
    "supports": "structural signal: mandatory obligation language (shall/must)",
    "trace_id": "LAIF-TRACE-03-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 625,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:monitor|audit|review|inspect|evaluat)\\b",
    "matched_text": "review",
    "normalized_match": "review",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 619,
    "supports": "structural signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-04-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 495,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\btransparency\\b|\\btransparent\\b|\\bmeaningful account\\b|\\bshows? its work\\b|\\bdisclos\\w+\\b.{0,80}\\b(?:limitation|basis|logic|criteria|use\\s+of\\s+ai)\\b|\\b(?:publish|state|record)\\w*\\b.{0,60}\\bbasis\\s+(?:for|of)\\s+(?:the\\s+)?(?:decision|output|determination)\\b|\\binformed\\s+that\\b.{0,80}\\bautomated\\b|\\bplain.(?:language|english)\\b.{0,60}\\b(?:account|explanation|statement|information)\\b",
    "matched_text": "transparency",
    "normalized_match": "transparency",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 483,
    "supports": "conceptual signal: transparency",
    "trace_id": "LAIF-TRACE-05-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 511,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\baccountability\\b|\\baccountable\\b|records? sufficient for audit|\\bauditors?\\b|\\binternal\\s+audit\\b|\\bowner\\s*:|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bsenior\\s+responsible\\s+owner\\b|\\breportable\\s+(?:control\\s+)?breach\\b|\\bresponsible\\s+for\\b.{0,80}\\b(?:compliance|discharg\\w+|the\\s+decision)\\b|\\|\\s*(?:owner|accountable|responsible)\\s*\\|",
    "matched_text": "accountability",
    "normalized_match": "accountability",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 497,
    "supports": "conceptual signal: accountability",
    "trace_id": "LAIF-TRACE-06-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 952,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b.{1,300}\\bshall\\b|\\bmust\\b.{1,300}\\bmust\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)[^\\n]*\\n(?:\\|[^\\n]*\\n){3,}",
    "matched_text": "must request evidence of testing before deployment. The supplier must describe the intended use, material limitations and known risks. A human reviewer must",
    "normalized_match": "must request evidence of testing before deployment. the supplier must describe the intended use, material limitations and known risks. a human reviewer must",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 796,
    "supports": "auditability signal: multiple mandatory obligations (shall/must pairs)",
    "trace_id": "LAIF-TRACE-07-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 73,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:document|record|evidence|technical documentation|certif|report)\\b",
    "matched_text": "document",
    "normalized_match": "document",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 65,
    "supports": "auditability signal: evidence / documentation requirements",
    "trace_id": "LAIF-TRACE-08-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 625,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:review|audit|monitor|evaluat|inspect|post.market)\\b",
    "matched_text": "review",
    "normalized_match": "review",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 619,
    "supports": "auditability signal: review / monitoring mechanisms",
    "trace_id": "LAIF-TRACE-09-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 625,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:specific|targeted|defined|identif|concrete|measur)\\b.{0,80}\\b(?:requirement|obligation|measure|standard|criterion)\\b|\\bwithin\\s+\\d+\\s+(?:working\\s+|business\\s+|calendar\\s+)?(?:day|hour|week|month|year)s?\\b|\\b(?:above|below|exceed\\w*|outside|greater\\s+than|less\\s+than)\\b.{0,40}\\d+\\s*%|\\b(?:monthly|quarterly|annual(?:ly)?|weekly|biannual\\w*)\\b.{0,80}\\b(?:review|monitor|report|assess|audit|attest)\\w*|\\b(?:review|monitor|report|assess|audit|attest)\\w*\\b.{0,60}\\b(?:monthly|quarterly|annual(?:ly)?|weekly)\\b",
    "matched_text": "annual review",
    "normalized_match": "annual review",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 612,
    "supports": "auditability signal: specific, measurable obligations",
    "trace_id": "LAIF-TRACE-10-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 374,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\bshall\\b|\\bmust\\b|\\bwe\\s+will\\s+(?:never|not)\\b|(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)",
    "matched_text": "must",
    "normalized_match": "must",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 370,
    "supports": "enforceability signal: mandatory language (shall/must)",
    "trace_id": "LAIF-TRACE-11-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 18,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:\\b(?:provider|deployer|operator|agenc(?:y|ies)|responsible\\s+part(?:y|ies)|actors?|authorit(?:y|ies)|organisations?)\\b|\\b(?:chief|group|senior|head)\\s+[\\w-]+\\s+(?:officer|executive)\\b|\\b[\\w-]+\\s+committee\\b|\\bboard\\s+of\\s+[\\w-]+\\b|\\binternal\\s+audit\\b|\\b(?:model|system|product|risk|service|process|data|business)\\s+owners?\\b|\\bowner\\s*:|\\bsenior\\s+responsible\\s+owner\\b|\\b(?:data\\s+)?controller\\b|\\bsuppliers?\\b|\\bvendors?\\b|\\bcontractors?\\b|\\bhead\\s+of\\s+[\\w-]+\\b",
    "matched_text": "supplier",
    "normalized_match": "supplier",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 10,
    "supports": "enforceability signal: named responsible parties",
    "trace_id": "LAIF-TRACE-12-governance-force-signal"
  },
  {
    "assessment_mode": "external_framework",
    "confidence": "deterministic_pattern",
    "end_char": 565,
    "evidence_type": "governance_force_signal",
    "legal_authority_boundary": "Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.",
    "match_rule": "regex:(?:\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b|\\|[^\\n|]{0,60}\\b(?:owner|accountable|responsible|role|lead)\\b[^\\n]{0,200}\\|[^\\n|]{0,60}\\b(?:control|requirement|obligation|duty|measure|action|safeguard)s?\\b)[^\\n]*\\n(?:\\|[^\\n]*\\n){3,}|\\b(?:shall|must)\\s+(?:not\\s+)?(?:ensure|establish|implement|maintain|provide|design|develop|assess|approve|produce|operate|name|document|monitor|report|escalate|evidence|record|review|verify|notify|suspend|obtain|submit|demonstrate|comply|retain|publish|test|validate|apply|complete|register)\\b|\\b(?:shall|must)\\s+be\\s+\\w+ed\\b|\\brequires?\\s+(?:re.)?(?:approval|authoris\\w+|authoriz\\w+|sign.off)\\b|\\bno\\s+\\w+(?:\\s+\\w+)?\\s+(?:enters?|proceeds?|may|shall|is\\s+\\w+ed)\\b.{0,80}\\bunless\\b",
    "matched_text": "must maintain",
    "normalized_match": "must maintain",
    "source_document": "vendor-policy",
    "source_type": "uploaded_document",
    "start_char": 552,
    "supports": "enforceability signal: non-discretionary operational mandates",
    "trace_id": "LAIF-TRACE-13-governance-force-signal"
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
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-01-structural-no-precedence-rule-between-the",
    "recommended_patch": "State the order of precedence among this document's own provisions: which prevails if two conflict, which cannot be waived or changed except by a named authority, and what this document is subordinate to. A conflicts clause, a 'without prejudice to' clause, a waiver bar, or a stated parent framework each satisfies this.",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "certification channel \u2014 LAIF-native vocabulary not used (expected for an external instrument; not a governance deficiency)",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "terminology_gap",
    "governance_force_component": "control",
    "implementation_priority": "optional_laif_adoption",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-02-certification-channel-laif-native-vocabula",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "low",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "conceptual \u2014 governance concepts insufficiently expressed",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-03-conceptual-governance-concepts-insufficien",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: conceptual \u2014 governance concepts insufficiently expressed",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: Coupling shall pair each restriction with the specific human interest protected, with neither side weakened in isolation.",
    "diagnostic_gap": "Missing LAIF construct: Coupling",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Coupling",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-04-missing-laif-construct-coupling",
    "recommended_patch": "Define each restriction with the specific protected human or public interest it serves, then assign equivalent institutional force to both sides of the pairing.",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "high",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: the Coherence Test shall document Q1 Coupling, Q2 Consistency, and Q3 Reversibility before authorization.",
    "diagnostic_gap": "Certification channel \u2014 the Coherence Test is LAIF's named decision instrument; an external document is not expected to contain it",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "planned",
    "laif_construct": "Coherence Test",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-05-certification-channel-the-coherence-test-i",
    "recommended_patch": "No governance action is required. This records distance from the assessing framework's own vocabulary, which matters only if the organisation chooses to seek LAIF-native certification; the substance it names is either already expressed in the document's own words or belongs to that framework alone.",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "low",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form: deployment authorization shall require Structural Transparency, Structural Honesty, and Structural Containment evidence.",
    "diagnostic_gap": "Missing LAIF construct: Integrity Layer",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "immediate",
    "laif_construct": "Integrity Layer",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-06-missing-laif-construct-integrity-layer",
    "recommended_patch": "Define Integrity Layer entry criteria and assign an accountable owner to confirm transparency, honesty, containment and applicable calibration evidence before operational use.",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "high",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Transparency",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [
      "LAIF-TRACE-05-governance-force-signal"
    ],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Transparency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-07-missing-laif-construct-structural-transpar",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Transparency",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "transparency",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Honesty",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Honesty",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-08-missing-laif-construct-structural-honesty",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Honesty",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Structural Containment",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Structural Containment",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-09-missing-laif-construct-structural-containm",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Structural Containment",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Consistency",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Consistency",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-10-missing-laif-construct-consistency",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Missing LAIF construct: Consistency",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Missing LAIF construct: Reversibility",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [],
    "finding_type": "construct_gap",
    "governance_force_component": "reversibility",
    "implementation_priority": "near_term",
    "laif_construct": "Reversibility",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-11-missing-laif-construct-reversibility",
    "recommended_patch": "Add an escalation path and reversibility procedure that identifies who can pause, roll back, review, or remedy the affected decision.",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "Not directly quoted by current deterministic extractor; reviewer confirmation required.",
    "verification_test": "Create a verification test that samples this reversibility control, confirms the named owner, trigger, evidence artifact, escalation route, and review outcome, and records pass/follow-up status."
  },
  {
    "assessment_mode": "external_framework",
    "canonical_clause_if_adopting_laif": "If adopting LAIF-native form, translate this diagnostic gap into a canonical LAIF clause only after institutional authority approves the adoption path.",
    "diagnostic_gap": "Low structural score (14/100): missed signals include numbered sub-requirements, full lifecycle scope declared, risk stratification / proportionality",
    "evidence_artifact": "Contract clause, vendor disclosure, audit-access record, assurance artefact, or service-level evidence.",
    "evidence_trace_ids": [
      "LAIF-TRACE-07-governance-force-signal"
    ],
    "finding_type": "governance_force_gap",
    "governance_force_component": "control",
    "implementation_priority": "near_term",
    "laif_construct": "Governance-force implementation",
    "legal_authority_boundary": "diagnostic_only",
    "operational_control": "Translate AI governance requirements into contract clauses, vendor disclosure duties, audit-access rights, assurance review, and escalation consequences.",
    "patch_id": "LAIF-PATCH-12-low-structural-score-14-100-missed-signals",
    "recommended_patch": "Define an institution-specific control for this diagnostic gap and assign owner, trigger, evidence, escalation, and review obligations: Low structural score (14/100): missed signals include numbered sub-requirements, full lifecycle scope declared, risk stratification / proportionality",
    "responsible_actor": "Procurement lead with legal/compliance and vendor-management support",
    "severity": "medium",
    "source_document": "vendor-policy",
    "source_evidence": "must request evidence of testing before deployment. The supplier must describe the intended use, material limitations and known risks. A human reviewer must",
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
| Integrity Layer | absent | ABSENT |
| Reversibility | absent | ABSENT |
| Self-Application | absent | ABSENT |
| Structural Containment | absent | ABSENT (via Integrity Layer) |
| Structural Honesty | absent | ABSENT (via Integrity Layer) |
| Structural Transparency | absent | ABSENT (via Integrity Layer) |

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
  "extraction_quality_level": "high",
  "extractor_used": "builtin",
  "final_gate_failure_count": 0,
  "incomplete_quote_density": 0.0,
  "low_confidence_quote_count": 7,
  "primary_quote_count": 6,
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
    "display_quote": "Synthetic demonstration document.",
    "document_type": "procurement_assessment_form",
    "end_offset": 74,
    "exact_quote": "Synthetic demonstration document.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, object/control/domain signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ001",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 41,
    "surrounding_context": "Synthetic demonstration document.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "This is an invented supplier policy for learning and testing; it is not evidence about a real organisation and is not a recommended policy template.",
    "document_type": "procurement_assessment_form",
    "end_offset": 223,
    "exact_quote": "This is an invented supplier policy for learning and testing; it is not evidence about a real organisation and is not a recommended policy template.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ002",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 75,
    "surrounding_context": "This is an invented supplier policy for learning and testing; it is not evidence about a real organisation and is not a recommended policy template.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The supplier is committed to transparency, accountability and responsible AI.",
    "document_type": "procurement_assessment_form",
    "end_offset": 531,
    "exact_quote": "The supplier is committed to transparency, accountability and responsible AI.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ003",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 454,
    "surrounding_context": "The supplier is committed to transparency, accountability and responsible AI.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "Staff may raise concerns with the service manager.",
    "document_type": "procurement_assessment_form",
    "end_offset": 692,
    "exact_quote": "Staff may raise concerns with the service manager.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal, object/control/domain signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ004",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 642,
    "surrounding_context": "Staff may raise concerns with the service manager.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The service manager may suspend the assistant following a serious incident.",
    "document_type": "procurement_assessment_form",
    "end_offset": 1087,
    "exact_quote": "The service manager may suspend the assistant following a serious incident.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing actor or regulated party, obligation/action/control signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ005",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 1012,
    "surrounding_context": "The service manager may suspend the assistant following a serious incident.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The organisation will retain appropriate records.",
    "document_type": "procurement_assessment_form",
    "end_offset": 1137,
    "exact_quote": "The organisation will retain appropriate records.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "short fragment without strong obligation or control phrase; weak verification relevance: missing obligation/action/control signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ006",
    "quote_quality_reason": "short fragment without strong obligation or control phrase",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 1088,
    "surrounding_context": "The organisation will retain appropriate records.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  },
  {
    "display_quote": "The supplier will determine implementation arrangements during service delivery.",
    "document_type": "procurement_assessment_form",
    "end_offset": 1287,
    "exact_quote": "The supplier will determine implementation arrangements during service delivery.",
    "extraction_confidence": "high",
    "linked_gap_ids": [],
    "linked_governance_repair_field": "source_excerpt",
    "low_confidence_reason": "no institutional action or obligation verb explaining a governance signal; weak verification relevance: missing obligation/action/control signal, object/control/domain signal",
    "original_file_name": "vendor-policy.md",
    "quote_display_normalization_reason": "",
    "quote_display_normalized": false,
    "quote_id": "LQ007",
    "quote_quality_reason": "no institutional action or obligation verb explaining a governance signal",
    "quote_quality_score": 35,
    "raw_exact_quote_retained": true,
    "sector_profile": "procurement_vendor_governance",
    "signal_category": "low-confidence candidate",
    "source_file": "/workspace/scratch/a966521d6ca7/LAIF-consolidated/docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md",
    "source_sha256": "e8e8475acaf9fa54846ceac6b0bc8f5728e26e6f5b52ce83613150a791079523",
    "start_offset": 1207,
    "surrounding_context": "The supplier will determine implementation arrangements during service delivery.",
    "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
    "what_it_proves": "The document contains language potentially relevant to low-confidence candidate.",
    "why_it_matters": "Candidate source evidence for low-confidence candidate analysis."
  }
]
```

## Warnings/errors

- Warnings: []
- Errors: []
