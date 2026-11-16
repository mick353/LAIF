#!/usr/bin/env python3
"""
LAIF Assessment Engine
----------------------
Produces structured, scored assessments of governance documents against
LAIF v1.2 compliance criteria. Sits around validate.py without weakening
its enforcement — formal compliance remains binary and strict.

Five scoring dimensions (0–100 each):
  structural_score           Explicit governance architecture       (weight 25%)
  terminology_score          Canonical LAIF term presence           (weight 15%)
  conceptual_proximity_score LAIF-like concepts without LAIF terms  (weight 20%)
  auditability_score         Objective checkability of obligations  (weight 20%)
  enforceability_score       Operational enforcement capacity       (weight 20%)

Every score is accompanied by a signal breakdown — fired signals that earned
points and missed signals that did not. This answers "why this number?" for
every dimension without relying on opaque aggregation.

Spec alignment references:
  LAIF v1.2 — Part One (Foundational Principles, Coherence Standard)
  LAIF v1.2 — Part Two (Transparency, Honesty, Containment, Calibration where §2.5 applies)
  LAIF v1.2 — Part Three (Provision Layer: Provisions A–D)
  LAIF v1.2 — Part Seven (Self-Application: framework applies to governance actors)
  LAIF_Compliance_Toolkit.txt — §1 Operational Standards, §2 PDCA, §7 Tiering
"""

import hashlib
import functools
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import find_paraphrase_violations, PARAPHRASE_GUARDS
from laif_spec import INTEGRITY_LAYER


# Historical imports, including private helpers, remain available to consumers.
from laif_engine.detection import (
    AUDITABILITY_RUBRIC,
    CONCEPTUAL_RUBRIC,
    CONSTRUCT_COVERAGE_CHECKS,
    CONTRADICTION_CHECKS,
    CONTRADICTION_PROXIMITY,
    CONTROL_REGISTER_PAT,
    CONTROL_REGISTER_POPULATED_PAT,
    COUPLING_HOLLOW_INDICATORS,
    COUPLING_NEGATION_INDICATORS,
    COUPLING_STRUCTURAL_INDICATORS,
    ENFORCEABILITY_RUBRIC,
    ENGLISH_MIN_WORDS,
    ENGLISH_RATIO_THRESHOLD,
    ENUMERATION_MIN_SENTENCES,
    ENUMERATION_RATIO_THRESHOLD,
    FORMAL_REQUIREMENTS,
    FUNCTIONAL_CONSTRUCT_FAMILIES,
    SECTOR_PROFILES,
    STRUCTURAL_RUBRIC,
    TERMINOLOGY_RUBRIC,
    _ANALYTICAL_FRAME_PAT,
    _ANALYTICAL_INSTRUMENT_MIN_MARKERS,
    _CONTROL_REGISTER_HEADER,
    _CONTROL_REGISTER_HEADER_ALT,
    _ENGLISH_FUNCTION_WORDS,
    _ENUMERATION_GOVERNANCE_TERM,
    _ENUMERATION_MODAL,
    _FUNCTIONAL_DECLARED_CHECKS,
    _FUNCTIONAL_REQUIRED_FAMILY,
    _GOVERNING_CONTEXT_PAT,
    _IMPLICIT_COUPLING_PATTERNS,
    _NEGATION_PREFIX_PAT,
    _NEGATIVE_CONSTRUCTION_PAT,
    _SECTOR_PROFILE_ALIASES,
    _SECTOR_PROFILE_PATCH_CONTEXT,
    _achievable_ceiling_external,
    _contradiction_check,
    _coupling_quality,
    _coupling_state,
    _english_coverage,
    _functional_alignment,
    _implicit_coupling_signals,
    _laif_alignment_verdict,
    _sector_gaming_risk,
    _sector_profile_key,
    _sector_profile_metadata,
    _sector_profile_patch_adjustments,
    _sector_profile_remediation_context,
    _sector_profile_signals,
    _structural_depth,
    _vocabulary_enumeration,
    integrity_requirement_diagnostics,
)
from laif_engine.findings import (
    _DIM_CONSEQUENCE,
    _DIRECTIONALITY_RIGHTS,
    _DIRECTIONALITY_SURVEILLANCE,
    _SCORE_WEIGHT_RATIONALE,
    _build_score_trace,
    _compliance_summary,
    _deployment_risk_tier,
    _directionality_penalty,
    _executive_summary,
    _governance_signal_strength,
    _remediation,
    _score_reason,
    _score_signals,
    _structured_findings,
    _structured_remediation,
    _tty,
    _tty_bar,
    score_bar,
)
from laif_engine.classification import (
    DOCUMENT_TYPE_PRECEDENCE,
    _DOCUMENT_TYPE_FORCE,
    _DOCUMENT_TYPE_PATTERNS,
    _DOCUMENT_TYPE_PRECEDENCE_RANK,
    _DOC_TYPE_USE,
    _EVIDENCE_GAP_RE,
    _GATE_GAP_RE,
    _LIFECYCLE_GAP_RE,
    _OWNER_GAP_RE,
    _RESIDUAL_RISK_RE,
    _ROLLBACK_GAP_RE,
    _SECTOR_KEYWORDS,
    _assessment_mode_fields,
    _build_governance_repair_fields,
    _document_type_pattern_hits,
    _filter_paraphrase_violations,
    _fragment_quality,
    _gap_absent,
    _identity_document_type,
    _keyword_sector_fallback,
    _quality_label,
    _resolve_assessment_mode,
    _risk_label,
    _strong_public_sector_policy_hits,
    classify_document_type,
    dominant_sector_for_document,
    known_instrument_profile,
)
from laif_engine.assessment import (
    assess,
)
from laif_engine.source_spans import (
    _ORPHAN_OPENER,
    _OUTLINE_PATTERNS,
    _document_outline,
    _locate_offset,
    _quote_at,
)
from laif_engine.source_display import (
    _ANCHOR_HINTS,
    _OBLIGATION_SENTENCE,
    _PLAIN_SOURCE_TYPES,
    _PLAIN_VALUE_NAMES,
    _located_signals,
    _obligation_anchors,
    _plain_reading,
    _suggest_anchor,
)
from laif_engine.evidence import (
    _CONSTRUCT_ORDER,
    _EVIDENCE_TRACE_LEGAL_AUTHORITY_BOUNDARY,
    _EVIDENCE_TRACE_MAX_PER_DOCUMENT,
    _GOVERNANCE_FORCE_COMPONENTS,
    _GOVERNANCE_KW,
    _HUMAN_INTEREST_KW,
    _PATCH_MAX_PER_DOCUMENT,
    _PATCH_SOURCE_EVIDENCE_FALLBACK,
    _REMEDIATION_PATCH_KEYS,
    _build_evidence_traces,
    _build_remediation_patches,
    _canonical_clause_for_gap,
    _construct_for_gap,
    _evidence_artifact_for_gap,
    _evidence_trace,
    _evidence_trace_links_for_patch,
    _extract_governance_force_traces,
    _extract_profile_signal_traces,
    _extract_remediation_anchor_traces,
    _fallback_evidence_trace,
    _find_text_span,
    _first_regex_match,
    _gap_pool,
    _gap_text,
    _governance_component_for_gap,
    _governance_force_profile,
    _implementation_priority_for_gap,
    _legal_authority_boundary_for_gap,
    _normalize_trace_text,
    _operational_control_for_gap,
    _patch_candidate_gap_entries,
    _patch_type_for_gap,
    _recommended_patch_for_gap,
    _remediation_groups,
    _responsible_actor_for_gap,
    _severity_for_gap,
    _slugify_patch_id,
    _text_pool,
    _trace_id,
    _trace_support_matches_patch,
    _verification_test_for_gap,
)
from laif_engine.report_helpers import (
    FINGERPRINT_DISPLAY_CHARS,
    REPORT_DATE,
    _DIMENSION_DISPLAY_NAMES,
    _DIMENSION_SCORE_KEYS,
    _calibration_cautions,
    _compact_list,
    _dimension_calibration_note,
    _dimension_justification_records,
    _has_fallback_only_evidence,
    _markdown_table,
    _md_anchor,
    _public_report_status_label,
    _report_boundary_notice,
    _report_caution_summary,
    _report_document_row,
    _report_evidence_summary,
    _report_limits_and_reviewer_actions,
    _report_patch_summary,
    _report_score_band,
    _safe_executive_risk_text,
    _safe_executive_verdict_text,
    _safe_markdown_cell,
    _score_band,
    _score_gaming_risk_notes,
    _score_interpretation_label,
    _score_justification_summary,
    _signal_labels,
)
from laif_engine.identity import (
    _corpus_fingerprint,
    toolchain_fingerprint,
)
from laif_engine.reporting import (
    export_assessment_data,
    generate_executive_summary,
    generate_markdown_report,
)
