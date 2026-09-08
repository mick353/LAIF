#!/usr/bin/env python3
"""Document ingestion wrapper for LAIF structural assessment.

This runner extracts local document text, assesses the extracted text with the
existing LAIF assessment engine, and writes markdown/JSON artifacts plus an
append-only processing index. It does not perform OCR, network fetches, scoring
changes, certification changes, or governance/protected-artifact mutations.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import functools
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from assessment_engine import assess, classify_document_type, generate_markdown_report

MIN_EXTRACTED_CHARACTERS = 20
DEFAULT_OUTPUT_DIR = "laif_outputs"
INDEX_FILE_NAME = "laif_processing_index.jsonl"

ASSESSMENT_MODES = ("external_framework", "laif_native")
SECTOR_CHOICES = (
    "auto",
    "general_ai_governance",
    "government_service_delivery",
    "departmental_ai_development",
    "procurement_vendor_governance",
    "clinical_ai",
    "employment_hr_ai",
    "education_ai",
    "financial_services_ai",
)
EXTRACTOR_CHOICES = ("auto", "builtin", "docling", "markitdown", "python-docx", "pypdf")
BUILTIN_EXTENSIONS = {".txt", ".md", ".markdown"}


@dataclass
class ExtractionResult:
    text: str
    extractor_used: str
    extraction_confidence: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class ExtractionError(RuntimeError):
    """Raised when local document text cannot be extracted safely."""


def utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_stem(stem: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", stem.strip())
    safe = re.sub(r"-+", "-", safe).strip(".-_")
    return safe[:120] or "document"


def normalize_text(text: str) -> str:
    return (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def ensure_minimum_text(result: ExtractionResult, path: Path) -> ExtractionResult:
    text = normalize_text(result.text)
    if len(text) < MIN_EXTRACTED_CHARACTERS:
        raise ExtractionError(
            f"Extracted text from {path} is empty or below the safe minimum "
            f"threshold of {MIN_EXTRACTED_CHARACTERS} characters."
        )
    result.text = text
    return result


def extract_builtin(path: Path) -> ExtractionResult:
    if path.suffix.lower() not in BUILTIN_EXTENSIONS:
        raise ExtractionError(f"Built-in extractor supports only .txt, .md, and .markdown files: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")
    return ExtractionResult(text=text, extractor_used="builtin", extraction_confidence="high")


def extract_text_fallback(path: Path) -> ExtractionResult:
    """Read UTF-8 text from a non-text extension for deterministic tests/smokes."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")
    return ExtractionResult(text=text, extractor_used="text-fallback", extraction_confidence="low", warnings=["non-text extension decoded as UTF-8 text"])


def extract_docling(path: Path) -> ExtractionResult:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise ExtractionError("Docling extractor requested but docling is not installed.") from exc

    converter = DocumentConverter()
    converted = converter.convert(str(path))
    document = getattr(converted, "document", converted)
    if hasattr(document, "export_to_markdown"):
        text = document.export_to_markdown()
    elif hasattr(document, "export_to_text"):
        text = document.export_to_text()
    else:
        text = str(document)
    return ExtractionResult(text=text, extractor_used="docling", extraction_confidence="medium")


def extract_markitdown(path: Path) -> ExtractionResult:
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise ExtractionError("MarkItDown extractor requested but markitdown is not installed.") from exc

    converted = MarkItDown().convert(str(path))
    text = getattr(converted, "text_content", None) or getattr(converted, "markdown", None) or str(converted)
    return ExtractionResult(text=text, extractor_used="markitdown", extraction_confidence="medium")


def extract_python_docx(path: Path) -> ExtractionResult:
    if path.suffix.lower() != ".docx":
        raise ExtractionError("python-docx extractor supports only .docx files.")
    try:
        import docx
    except ImportError as exc:
        raise ExtractionError("python-docx extractor requested but python-docx is not installed.") from exc

    document = docx.Document(str(path))
    parts: list[str] = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    for table in document.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if cells:
                parts.append(" | ".join(cells))
    return ExtractionResult(text="\n".join(parts), extractor_used="python-docx", extraction_confidence="medium")


def extract_pypdf(path: Path) -> ExtractionResult:
    if path.suffix.lower() != ".pdf":
        raise ExtractionError("pypdf extractor supports only .pdf files.")
    reader_class = None
    module_name = None
    try:
        from pypdf import PdfReader as reader_class  # type: ignore[assignment]
        module_name = "pypdf"
    except ImportError:
        try:
            from PyPDF2 import PdfReader as reader_class  # type: ignore[assignment]
            module_name = "PyPDF2"
        except ImportError as exc:
            raise ExtractionError("pypdf extractor requested but neither pypdf nor PyPDF2 is installed.") from exc

    reader = reader_class(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return ExtractionResult(text="\n".join(pages), extractor_used=module_name or "pypdf", extraction_confidence="medium")


def _attempt(name: str, func: Callable[[Path], ExtractionResult], path: Path) -> tuple[ExtractionResult | None, str | None]:
    try:
        return ensure_minimum_text(func(path), path), None
    except ExtractionError as exc:
        return None, str(exc)
    except Exception as exc:  # local parser failures should be clear, not silent
        return None, f"{name} extractor failed for {path}: {exc}"


def extract_document(path: Path, extractor: str = "auto") -> ExtractionResult:
    if not path.exists() or not path.is_file():
        raise ExtractionError(f"Input file does not exist or is not a regular file: {path}")

    suffix = path.suffix.lower()
    if extractor == "builtin":
        return ensure_minimum_text(extract_builtin(path), path)
    if extractor == "docling":
        return ensure_minimum_text(extract_docling(path), path)
    if extractor == "markitdown":
        return ensure_minimum_text(extract_markitdown(path), path)
    if extractor == "python-docx":
        return ensure_minimum_text(extract_python_docx(path), path)
    if extractor == "pypdf":
        return ensure_minimum_text(extract_pypdf(path), path)

    warnings: list[str] = []
    attempts: list[tuple[str, Callable[[Path], ExtractionResult]]] = []
    if suffix in BUILTIN_EXTENSIONS:
        attempts.append(("builtin", extract_builtin))
    attempts.extend((("docling", extract_docling), ("markitdown", extract_markitdown)))
    if suffix == ".docx":
        attempts.append(("python-docx", extract_python_docx))
        attempts.append(("text-fallback", extract_text_fallback))
    if suffix == ".pdf":
        attempts.append(("pypdf", extract_pypdf))
        attempts.append(("text-fallback", extract_text_fallback))

    for name, func in attempts:
        result, warning = _attempt(name, func, path)
        if result is not None:
            result.warnings.extend(warnings)
            return result
        if warning:
            warnings.append(warning)

    if not attempts:
        raise ExtractionError(
            f"Unsupported file type {suffix or '<none>'}; no extractor can handle it without optional packages."
        )
    attempted = "; ".join(warnings)
    if suffix not in BUILTIN_EXTENSIONS and suffix not in {".docx", ".pdf"}:
        raise ExtractionError(
            f"Unsupported file type {suffix or '<none>'}; no installed extractor could handle it. "
            f"Attempted extractors: {attempted}"
        )
    raise ExtractionError("Unable to extract document text. Attempted extractors: " + attempted)


def _term_hits(text: str, terms: Iterable[str]) -> int:
    """Count how many DISTINCT terms occur, not how many times any one occurs.

    Every caller uses the result as a count of independent signals (">= 2
    signals present"). Occurrence counting made a single generic phrase
    repeated twice indistinguishable from two independent markers, which
    misclassified documents on one incidental word.
    """
    lowered = (text or "").lower()
    return sum(1 for term in terms if term.lower() in lowered)


EU_AI_ACT_SIGNAL_TERMS = (
    "regulation laying down harmonised rules",
    "harmonised rules on artificial intelligence",
    "artificial intelligence act",
    "high-risk ai systems",
    "provider",
    "providers",
    "deployer",
    "deployers",
    "conformity assessment",
    "market surveillance",
    "official journal",
    "general-purpose ai model",
    "placing on the market",
    "post-market monitoring",
    "technical documentation",
    "serious incident reporting",
)

PUBLIC_SECTOR_POLICY_SIGNAL_TERMS = (
    "policy for the responsible use of ai in government",
    "responsible use of ai in government",
    "public servants must",
    "government agencies must",
    "agencies must disclose",
    "responsible ai use by agencies",
    "accountable official",
    "accountable officials",
    # "human review" deliberately excluded: it is a generic oversight term used
    # in clinical, employment, financial, and corporate instruments alike, and
    # is not evidence of a public-sector operating policy.
    "disclose ai use",
    "ai use register",
    "ai use registers",
    "public sector policy",
    "digital transformation agency",
    "dta",
)


def eu_ai_act_broad_legal_signal(text: str) -> bool:
    lowered = (text or "").lower()
    hits = _term_hits(lowered, EU_AI_ACT_SIGNAL_TERMS)
    employment_hits = _term_hits(lowered, ("employment", "worker", "workers", "labour", "recruitment", "workplace rights"))
    return hits >= 2 and ("harmonised rules" in lowered or "artificial intelligence act" in lowered or "regulation laying down" in lowered or hits >= employment_hits + 2)


def public_sector_policy_signal(text: str) -> bool:
    return _term_hits(text, PUBLIC_SECTOR_POLICY_SIGNAL_TERMS) >= 2


def executive_policy_directive_signal(text: str) -> bool:
    lowered = (text or "").lower()
    return "executive order" in lowered and any(term in lowered for term in ("federal agencies", "agency heads", "secretaries", "secretary"))


def voluntary_risk_framework_signal(text: str) -> bool:
    lowered = (text or "").lower()
    return "risk management framework" in lowered and any(term in lowered for term in ("voluntary", "govern, map, measure", "non-sector-specific", "use-case agnostic"))


def sector_assurance_checklist_signal(text: str) -> bool:
    lowered = (text or "").lower()
    clinical_hits = _term_hits(lowered, ("clinical", "patient", "nhs", "dcb0129", "hazard log", "clinical safety case"))
    return ("digital technology assessment criteria" in lowered or "dtac" in lowered or clinical_hits >= 2) and clinical_hits >= 1


def broad_governance_framework_signal(text: str) -> bool:
    lowered = (text or "").lower()
    if eu_ai_act_broad_legal_signal(text):
        return True
    broad_terms = (
        "risk management framework", "voluntary framework", "non-sector-specific", "use-case agnostic",
        "harmonised rules", "artificial intelligence act", "conformity assessment", "market surveillance",
        "regulation laying down", "executive order", "federal agencies", "providers", "deployers",
        "trustworthy ai", "govern map measure manage", "govern, map, measure, and manage",
        "responsible use of ai in government", "public servants", "federal agencies",
    )
    legal_terms = ("regulation", "article", "official journal", "conformity", "provider", "deployer", "market surveillance")
    framework_hits = sum(lowered.count(term) for term in broad_terms)
    legal_hits = sum(lowered.count(term) for term in legal_terms)
    employment_hits = sum(lowered.count(term) for term in ("employment", "worker", "workers", "hiring", "candidate", "hr"))
    clinical_hits = sum(lowered.count(term) for term in ("clinical", "patient", "clinician", "nhs", "dcb0129", "hazard log"))
    if clinical_hits >= 2:
        return False
    return framework_hits >= 1 or (legal_hits >= 3 and legal_hits >= employment_hits)


def auto_sector(text: str) -> str:
    lowered = text.lower()
    doc_type = classify_document_type(text)
    if doc_type in {"binding_legal_instrument", "voluntary_risk_framework"}:
        return "general_ai_governance"
    if doc_type == "executive_policy_directive" or executive_policy_directive_signal(text):
        return "government_service_delivery" if any(term in lowered for term in ("federal agencies", "agency heads", "secretaries", "secretary")) else "general_ai_governance"
    if doc_type == "sector_assurance_checklist" or sector_assurance_checklist_signal(text):
        return "clinical_ai"
    if doc_type == "public_sector_policy" or public_sector_policy_signal(text):
        return "government_service_delivery"
    if eu_ai_act_broad_legal_signal(text) or voluntary_risk_framework_signal(text):
        return "general_ai_governance"
    if broad_governance_framework_signal(text):
        return "general_ai_governance"
    patterns: list[tuple[str, Iterable[str]]] = [
        ("clinical_ai", ("clinical", "patient", "clinician", "diagnosis", "medical", "healthcare", "safety incident", "dcb0129", "hazard log", "nhs")),
        ("procurement_vendor_governance", ("procurement", "vendor", "contract", "supplier", "service level", "audit access")),
        ("employment_hr_ai", ("employment", "hiring", "hr", "human resources", "candidate", "adverse action")),
        ("education_ai", ("education", "student", "academic", "school", "accessibility", "learning")),
        ("financial_services_ai", ("credit", "lending", "loan", "mortgage", "underwriting", "borrower", "applicant", "policyholder", "premium", "affordability", "aml", "model risk", "model validation", "financial crime", "bank")),
        ("government_service_delivery", ("public service", "public sector", "government", "government agencies", "agencies must", "public servants", "accountable officials", "ai use register", "service delivery", "administrative review", "benefit", "caseworker", "claimant", "claimants", "council", "local authority", "entitlement")),
        ("departmental_ai_development", ("software development", "release", "pipeline", "model register", "rollback", "architecture")),
    ]
    # Whole-word counting. Substring counting silently matched "hr" inside
    # "through"/"thresholds" and "benefit" inside "benefits", routing documents
    # to unrelated sector profiles.
    def _count(term: str) -> int:
        if " " in term:
            return lowered.count(term)
        return len(re.findall(rf"\b{re.escape(term)}\b", lowered))

    scores = [(sum(_count(term) for term in terms), sector) for sector, terms in patterns]
    best_score, best_sector = max(
        scores,
        key=lambda item: (item[0], -[s for s, _ in patterns].index(item[1])),
    )
    # A single incidental mention is not a sector. Require either a clear signal
    # or a clear margin over the runner-up before leaving the general profile.
    ranked = sorted(scores, reverse=True)
    runner_up = ranked[1][0] if len(ranked) > 1 else 0
    if best_score >= 3 or (best_score >= 2 and best_score > runner_up):
        return best_sector
    return "general_ai_governance"


def auto_sector_basis(text: str, sector: str | None = None) -> dict:
    """Why a sector was chosen — reported so a user can see and correct it.

    `sector` names the profile actually used by the assessment. It must be
    passed wherever the basis is displayed next to that profile: the runner's
    own detector and the engine's document-type-led routing can legitimately
    reach different answers, and showing one profile's name beside the other's
    evidence is incoherent.
    """
    lowered = (text or "").lower()
    chosen = sector or auto_sector(text)
    terms_by_sector = {
        "clinical_ai": ("clinical", "patient", "clinician", "diagnosis", "medical", "healthcare", "dcb0129", "hazard log", "nhs"),
        "procurement_vendor_governance": ("procurement", "vendor", "contract", "supplier", "service level", "audit access"),
        "employment_hr_ai": ("employment", "hiring", "hr", "human resources", "candidate", "adverse action"),
        "education_ai": ("education", "student", "academic", "school", "learning"),
        "financial_services_ai": ("credit", "lending", "loan", "mortgage", "underwriting", "applicant", "premium", "aml", "model risk", "model validation", "bank"),
        "government_service_delivery": ("public service", "public sector", "government", "public servants", "service delivery", "caseworker", "claimant", "council", "local authority"),
        "departmental_ai_development": ("software development", "release", "pipeline", "model register", "rollback", "architecture"),
        "general_ai_governance": (),
    }
    hits = []
    for term in terms_by_sector.get(chosen, ()):
        n = (lowered.count(term) if " " in term
             else len(re.findall(rf"\b{re.escape(term)}\b", lowered)))
        if n:
            hits.append(f"{term} ×{n}")
    if hits:
        basis = ", ".join(hits[:6])
    elif chosen != "general_ai_governance":
        # The profile came from document type or an instrument anchor, not from
        # sector vocabulary. Saying "no vocabulary reached the threshold" beside
        # a named profile would read as a contradiction.
        basis = ("routed by document type rather than sector vocabulary; "
                 "override with --sector if the institutional context differs")
    else:
        basis = "no sector-specific vocabulary reached the detection threshold"
    return {"sector": chosen, "basis": basis, "auto_detected": True}

def resolve_assessment_mode(mode: str) -> str:
    return "laif_native_certification" if mode == "laif_native" else "external_framework"


def build_processing_metadata(
    *,
    input_path: Path,
    input_path_original: str,
    output_dir: Path,
    processed_at_utc: str,
    source_sha256: str,
    safe_output_stem: str,
    markdown_enabled: bool,
    json_enabled: bool,
    original_pending_path: str = "",
    stored_source_path: str = "",
) -> dict:
    return {
        "processed_at_utc": processed_at_utc,
        "input_path_original": input_path_original,
        "input_path": str(input_path),
        "runner_input_path": str(input_path),
        "original_pending_path": original_pending_path or input_path_original,
        "stored_source_path": stored_source_path or str(input_path),
        "input_file_name": input_path.name,
        "original_file_name": input_path.name,
        "original_file_stem": input_path.stem,
        "source_sha256": source_sha256,
        "safe_output_stem": safe_output_stem,
        "markdown_output_path": str(output_dir / f"{safe_output_stem}.laif.md") if markdown_enabled else "",
        "json_output_path": str(output_dir / f"{safe_output_stem}.laif.json") if json_enabled else "",
    }


def markdown_metadata_block(processing: dict, extraction: dict, assessment: dict) -> str:
    lines = [
        "## Document Processing Metadata",
        "",
        f"- **Processed at UTC / processed_at_utc:** {processing['processed_at_utc']}",
        f"- **Original input path:** {processing['input_path_original']}",
        f"- **Resolved input path / runner_input_path:** {processing['runner_input_path']}",
        f"- **Original pending path / original_pending_path:** {processing['original_pending_path']}",
        f"- **Stored source path / stored_source_path:** {processing['stored_source_path']}",
        f"- **Original file name:** {processing['original_file_name']}",
        f"- **Source SHA-256:** {processing['source_sha256']}",
        f"- **Extractor used:** {extraction['extractor_used']}",
        f"- **Extracted characters:** {extraction['extracted_characters']}",
        f"- **Assessment mode:** {assessment.get('assessment_mode', '')}",
        f"- **Sector profile:** {assessment.get('sector_profile', '')}",
        f"- **Safe output stem:** {processing['safe_output_stem']}",
        f"- **Markdown output path:** {processing['markdown_output_path']}",
        f"- **JSON output path:** {processing['json_output_path']}",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def json_dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def index_record(processing: dict, extraction: dict, assessment: dict, input_path: Path, document_name: str) -> dict:
    return {
        "processed_at_utc": processing["processed_at_utc"],
        "original_file_name": processing["original_file_name"],
        "input_path_original": processing["input_path_original"],
        "input_path": str(input_path),
        "runner_input_path": processing.get("runner_input_path", str(input_path)),
        "original_pending_path": processing.get("original_pending_path", processing.get("input_path_original")),
        "stored_source_path": processing.get("stored_source_path", str(input_path)),
        "source_sha256": processing["source_sha256"],
        "safe_output_stem": processing["safe_output_stem"],
        "markdown_output_path": processing["markdown_output_path"],
        "json_output_path": processing["json_output_path"],
        "document_name": document_name,
        "assessment_mode": assessment.get("assessment_mode"),
        "sector_profile": assessment.get("sector_profile"),
        "document_type": assessment.get("document_type"),
        "formal_laif_native_compliance": assessment.get("formal_laif_native_compliance", assessment.get("formal_laif_compliance")),
        "overall_readiness_score": assessment.get("overall_readiness_score", assessment.get("overall_score")),
        "evidence_trace_count": len(assessment.get("evidence_traces", [])),
        "remediation_patch_count": len(assessment.get("remediation_patches", [])),
        "calibration_caution_count": len(assessment.get("calibration_cautions", [])),
        "gaming_risk_note_count": len(assessment.get("gaming_risk_notes", [])),
        "extractor_used": extraction.get("extractor_used"),
        "extracted_characters": extraction.get("extracted_characters"),
        "extraction_confidence": extraction.get("extraction_confidence"),
        "warning_count": extraction.get("warning_count"),
        "error_count": extraction.get("error_count"),
    }


def append_index(output_dir: Path, record: dict) -> None:
    index_path = output_dir / INDEX_FILE_NAME
    with index_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")



SIGNAL_CATEGORIES: list[tuple[str, tuple[str, ...], str]] = [
    ("risk management", ("risk management", "risk assessment", "risk", "govern", "map", "measure", "manage"), "source_risk_management"),
    ("human oversight", ("human oversight", "human review", "override", "intervention", "clinician review"), "operational_control"),
    ("clinical safety", ("clinical safety", "patient", "hazard log", "safety case", "DCB0129"), "sector_safety"),
    ("technical security", ("secure", "security", "resilient", "cybersecurity"), "technical_control"),
    ("data protection", ("data protection", "data governance", "data quality"), "data_governance"),
    ("privacy", ("privacy", "privacy-enhanced", "confidentiality"), "privacy_control"),
    ("audit/documentation", ("audit", "documentation", "document", "evidence", "record", "traceability"), "evidence_artifact"),
    ("monitoring/review", ("monitor", "review", "evaluate", "assessment", "supervision"), "monitoring_review"),
    ("incident reporting", ("incident", "reporting", "safety incident"), "incident_response"),
    ("accountability/owner", ("accountability", "accountable", "owner", "responsible", "assign"), "ownership"),
    ("enforcement/consequence", ("enforcement", "consequence", "penalty", "shall", "must"), "enforcement"),
    ("lifecycle/change control", ("lifecycle", "change control", "change", "release"), "lifecycle_control"),
    ("rollback/fallback", ("rollback", "fallback", "fail-safe"), "fallback"),
    ("residual risk", ("residual risk", "accepted risk", "risk acceptance"), "residual_risk"),
    ("appeal/redress/contestability", ("appeal", "redress", "contestability", "contest", "administrative review"), "redress"),
    ("procurement/supplier assurance", ("procurement", "supplier", "vendor", "contract", "assurance"), "supplier_assurance"),
    ("interoperability", ("interoperability", "interoperate", "integration"), "interoperability"),
    ("bias/discrimination/fairness", ("bias", "discrimination", "fairness", "fair", "non-discrimination"), "fairness"),
]

# ── Evidence-conditioned gap rules ────────────────────────────────────────────
# A gap is DETECTED, never asserted. Each rule fires only when the document
# actually creates an expectation (a fired rubric signal) while the control that
# would close it is absent (a missed rubric signal). The firing signal supplies
# the gap's own evidence quote and location, so two different documents produce
# two different registers — and a document with no detected gap is reported as
# having none rather than receiving a default checklist.
#
#   present : (dimension, signal label) whose presence creates the expectation
#   absent  : (dimension, signal label) whose absence leaves it unclosed
#   sector  : restrict to a sector profile, or None for all documents
GAP_RULES = [
    {
        "gap_type": "obligation_without_owner",
        "title": "Obligations are stated without a named accountable owner",
        "severity": "high",
        "present": ("enforceability", "mandatory language (shall/must)"),
        "absent": ("enforceability", "named responsible parties"),
        "meaning": ("The document imposes duties in mandatory language but does not "
                    "name the role or body that must discharge them, so no one can be "
                    "held to the duty and no reviewer can test whether it was met."),
        "control_artifact": "Accountability register naming the role responsible for each mandatory duty, with deputy and escalation route.",
        "control_trigger": "Adoption of the document, change of post-holder, or any new deployment relying on the duty.",
        "control_threshold": "No reliance on a duty that has no currently named owner.",
    },
    {
        "gap_type": "evidence_presence_without_sufficiency",
        "title": "Evidence is requested without a sufficiency standard",
        "severity": "high",
        "present": ("auditability", "evidence / documentation requirements"),
        "absent": ("auditability", "specific, measurable obligations"),
        "meaning": ("The document asks for documentation but does not state what makes "
                    "that documentation adequate, so any artefact can satisfy the "
                    "request and the assurance value of the evidence is unknown."),
        "control_artifact": "Evidence acceptance criteria defining required content, currency, and reviewer competence for each requested artefact.",
        "control_trigger": "Each submission of evidence under the document.",
        "control_threshold": "Evidence that does not meet the stated criteria is rejected rather than filed.",
    },
    {
        "gap_type": "monitoring_without_threshold",
        "title": "Monitoring is required without thresholds or escalation",
        "severity": "medium",
        "present": ("auditability", "review / monitoring mechanisms"),
        # The "review / monitoring" signal also fires on "review" used as
        # redress. Require language that actually establishes recurring
        # observation before claiming monitoring is unthresholded.
        "present_text": r"\bmonitor\w*\b|\bsurveillance\b|\bpost.market\b|\bperiodic\w*\b|\bongoing\s+(?:review|assessment)\b|\b(?:annual|quarterly|monthly|weekly|semester|biannual)\w*\b|\baudit\w*\b",
        "absent": (("enforceability", "risk-proportionate thresholds"),
                   ("enforceability", "enforcement consequences / penalties")),
        "meaning": ("The document requires review or monitoring but does not say what "
                    "result would count as a problem, so monitoring can run "
                    "indefinitely without ever triggering an action."),
        "control_artifact": "Monitoring specification listing metrics, thresholds, escalation route, and the decision each breach forces.",
        "control_trigger": "Each monitoring cycle and any out-of-range result.",
        "control_threshold": "A breach must produce a recorded decision, not only a recorded observation.",
    },
    {
        "gap_type": "policy_without_enforcement_consequence",
        "title": "Requirements carry no stated consequence for non-compliance",
        "severity": "medium",
        "present": ("enforceability", "mandatory language (shall/must)"),
        "absent": ("enforceability", "enforcement consequences / penalties"),
        "meaning": ("The document states requirements but attaches no consequence to "
                    "breaching them, so compliance rests on goodwill and a breach "
                    "produces no defined institutional response."),
        "control_artifact": "Consequence schedule mapping each class of breach to a defined response, up to suspension of use.",
        "control_trigger": "Any identified breach or exception request.",
        "control_threshold": "No breach is closed without a recorded consequence or a documented, authorised exception.",
    },
    {
        "gap_type": "risk_without_closure_gate",
        "title": "Risk is discussed without a gate that can stop deployment",
        "severity": "high",
        "present": ("conceptual", "risk governance"),
        "absent": ("structural", "threshold gate conditions (all must pass simultaneously)"),
        "meaning": ("The document engages with risk but sets no precondition that must "
                    "hold before deployment proceeds, so risk can be documented and "
                    "deployment can continue regardless of what the assessment found."),
        "control_artifact": "Deployment gate listing the conditions that must all hold before go-live, and who signs each.",
        "control_trigger": "Every new deployment and every material change to an existing one.",
        "control_threshold": "Deployment does not proceed while any gate condition is unmet.",
    },
    {
        "gap_type": "incident_reporting_without_redress",
        "title": "Affected people have no route to challenge an outcome",
        "severity": "high",
        "present": ("conceptual", "safety"),
        "absent": ("conceptual", "contestability / redress"),
        "meaning": ("The document addresses safety but gives the people affected by a "
                    "decision nothing they can invoke — no appeal, review, or remedy — "
                    "so harm to an individual has no defined path to correction."),
        "control_artifact": "Published route by which an affected person can contest an outcome, with owner, timescale, and reversal authority.",
        "control_trigger": "Any decision materially affecting a person, and any complaint received.",
        "control_threshold": "No decision pathway operates without a stated contest route.",
    },
    {
        "gap_type": "lifecycle_without_change_control",
        "title": "No lifecycle scope, so change is not governed",
        "severity": "medium",
        "present": ("auditability", "review / monitoring mechanisms"),
        "present_text": r"\bmonitor\w*\b|\baudit\w*\b|\bperiodic\w*\b|\bongoing\b|\b(?:annual|quarterly|monthly)\w*\b|\bdeploy\w*\b|\brelease\w*\b",
        "absent": (("structural", "full lifecycle scope declared"),
                   ("structural", "operational mechanisms defined")),
        "meaning": ("The document governs a point in time rather than the life of the "
                    "system, so retraining, vendor updates, and scope creep after "
                    "approval fall outside its control."),
        "control_artifact": "Change-control procedure defining what counts as a material change and what re-approval it forces.",
        "control_trigger": "Model, data, supplier, or purpose change after initial approval.",
        "control_threshold": "A material change without re-approval suspends use.",
    },
    {
        "gap_type": "safety_case_without_live_review",
        "title": "Clinical safety claims lack a live review cadence",
        "severity": "high",
        "present": ("conceptual", "safety"),
        "absent": ("auditability", "review / monitoring mechanisms"),
        "sector": "clinical_ai",
        "meaning": ("Safety is asserted at a point in time without a recurring review "
                    "obligation, so a clinically safe system at approval can drift "
                    "without anyone being required to notice."),
        "control_artifact": "Clinical safety review schedule with named Clinical Safety Officer, hazard log currency, and incident linkage.",
        "control_trigger": "Scheduled review, incident, or material clinical change.",
        "control_threshold": "An out-of-date safety case suspends clinical use.",
    },
    {
        "gap_type": "supplier_duty_without_deployer_acceptance",
        "title": "Supplier duties lack deployer acceptance evidence",
        "severity": "medium",
        "present": ("enforceability", "named responsible parties"),
        "absent": ("auditability", "specific, measurable obligations"),
        "sector": "procurement_vendor_governance",
        "meaning": ("Duties are placed on a supplier without defining what the deploying "
                    "organisation must verify on receipt, so supplier assertions can "
                    "pass into operational reliance unchecked."),
        "control_artifact": "Acceptance checklist stating what the deployer verifies before accepting each supplier assurance.",
        "control_trigger": "Contract award, renewal, and each supplier release.",
        "control_threshold": "Unverified supplier assurances do not enter the assurance record.",
    },
]

GAP_BLUEPRINTS = [
    ("evidence_presence_without_sufficiency", "Evidence is requested but sufficiency is not closed", "high"),
    ("obligation_without_owner", "Obligation is present without a named operational owner", "high"),
    ("risk_without_closure_gate", "Risk language lacks a closure gate", "high"),
    ("monitoring_without_threshold", "Monitoring lacks thresholds and escalation", "medium"),
    ("policy_without_enforcement_consequence", "Policy language lacks enforcement consequence", "medium"),
    ("safety_case_without_live_review", "Safety case lacks live review cadence", "high"),
    ("supplier_duty_without_deployer_acceptance", "Supplier duty lacks deployer acceptance evidence", "medium"),
    ("incident_reporting_without_redress", "Incident reporting lacks affected-person redress", "high"),
    ("lifecycle_without_change_control", "Lifecycle language lacks change-control artifact", "medium"),
    ("residual_risk_without_acceptance", "Residual risk lacks acceptance authority", "medium"),
    ("framework_guidance_without_implementation_artifact", "Framework guidance lacks implementation artifact", "high"),
    ("legal_obligation_without_operational_mapping", "Legal obligation lacks operational mapping", "high"),
]

NOISE_RE = re.compile(r"(?:[A-Za-z]{1}\s){8,}|[\ufffd]{2,}|(?:\b\w\b\s*){12,}")

STRONG_QUOTE_TERMS = (
    "shall", "must", "requires", "require", "ensure", "establish", "implement",
    "monitor", "review", "risk", "oversight", "accountability", "accountable",
    "evidence", "documentation", "document", "incident", "safety", "privacy",
    "security", "conformity", "assessment", "control", "audit", "record",
)
ACTION_QUOTE_TERMS = STRONG_QUOTE_TERMS + ("manage", "assign", "maintain", "protect", "report", "disclose")
BOILERPLATE_QUOTE_RE = re.compile(r"(difficulties with accessing|accessibility|contact us|support@|@\w|email:|telephone|copyright|isbn|all rights reserved|certain commercial entities, equipment, or materials may be identified)", re.IGNORECASE)
GENERIC_FRAGMENT_RE = re.compile(r"(?:requirements agencies must follow|monitoring, will help ensure|this document in order to describe|to combat this risk, the federal government will ensure that the collection|the assessment must be documented and take|the notification shall contain the conclusions of the assessment|by la ying down those r ules|this regulation ensures the free moveme nt, cross-border , of)", re.IGNORECASE)
PDF_INTR_WORD_DAMAGE_RE = re.compile(r"\b(?:super vision|inv estig ation|enf or cement|monitor ing|obliga tion|ar ticle|ser ious|general-pur pose|g eneral-pur pose|provid er|provid ed|ensur ing|har monisation|uni on|f alsifi ed|accompanie d|r isk|la ying|r ules|a rtificial|i ntelligence|p rovider|d eployer|o bligation|a ssessment|syste ms?|g enerated|cont ent|ai-g enerated|f or|exper ience|regard ing|marke t|post-mark et|impro ving|cor rective|classif ied|inter preted|ite rative|r un|f ocused|mitiga tion|comp et ent author ity|author ity|comp et ent|super visory|notifi cation|docu mentation|imple mentation|imple ment|assess ment|require ments|deci sions?)\b", re.IGNORECASE)
INCOMPLETE_END_RE = re.compile(r"\b(?:are|is|and|or|to|of|the|that|with|for|take|taken|should|must|shall|will|through|within|including|regarding|by|from|under|related\s+to|in\s+relation\s+to|as\s+part\s+of|in\s+order\s+to|their\s+ai|the\s+agency\s+make|broader\s+enterprise|ai\s+systems\s+work|nist\s+will\s+review)\s*$", re.IGNORECASE)
TOC_QUOTE_RE = re.compile(r"^\s*(?:\d+(?:\.\d+)*\s+){0,2}[A-Z][A-Za-z&/ -]{2,70}\s+\d{1,4}\s*$")
TITLE_ONLY_RE = re.compile(r"^[A-Z][A-Za-z0-9&/:,() -]{8,80}$")
BROKEN_GLYPH_RE = re.compile(r"\b[A-Za-z]{1,3}(?:\s+[A-Za-z]{1,3}){4,}\b", re.IGNORECASE)


def _sentence_spans(text: str) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    for match in re.finditer(r"[^.!?\n]*(?:[.!?]|\n|$)", text):
        sent = match.group(0).strip()
        if len(sent) < 20:
            continue
        start = text.find(sent, match.start())
        if start >= 0:
            spans.append((start, start + len(sent), sent))
    if not spans and text.strip():
        snippet = text.strip()[:500]
        start = text.find(snippet)
        spans.append((start, start + len(snippet), snippet))
    return spans


DISPLAY_QUOTE_REPAIRS: tuple[tuple[str, str], ...] = (
    ("AI-g enerated", "AI-generated"),
    ("g eneral-pur pose", "general-purpose"),
    ("general-pur pose", "general-purpose"),
    ("T o", "To"),
    ("appropr iate", "appropriate"),
    ("identifie d", "identified"),
    ("pro vider", "provider"),
    ("bef ore", "before"),
    ("ser vice", "service"),
    ("repor t", "report"),
    ("managem ent", "management"),
    ("refer red", "referred"),
    ("suc h", "such"),
    ("Super vision", "Supervision"),
    ("inv estig ation", "investigation"),
    ("enf or cement", "enforcement"),
    ("monitor ing", "monitoring"),
    ("exper ience", "experience"),
    ("syste ms", "systems"),
    ("regard ing", "regarding"),
    ("marke t", "market"),
    ("comp et ent author ity", "competent authority"),
    ("author ity", "authority"),
    ("comp et ent", "competent"),
    ("super visory", "supervisory"),
    ("notifi cation", "notification"),
    ("docu mentation", "documentation"),
    ("imple mentation", "implementation"),
    ("imple ment", "implement"),
    ("assess ment", "assessment"),
    ("require ments", "requirements"),
    ("deci sions", "decisions"),
    ("deci sion", "decision"),
    ("obliga tion", "obligation"),
    ("Ar ticle", "Article"),
    ("provid er", "provider"),
    ("provid ed", "provided"),
    ("ensur ing", "ensuring"),
    ("ser ious", "serious"),
    ("syste m", "system"),
    ("har monisation", "harmonisation"),
    ("f alsifi ed", "falsified"),
    ("accompanie d", "accompanied"),
    ("cont ent", "content"),
    ("r isk", "risk"),
    ("la ying", "laying"),
    ("r ules", "rules"),
    ("a rtificial", "artificial"),
    ("i ntelligence", "intelligence"),
    ("p rovider", "provider"),
    ("d eployer", "deployer"),
    ("o bligation", "obligation"),
    ("a ssessment", "assessment"),
    ("f or", "for"),
)



SPLIT_WORD_DAMAGE_REASON = "display quote contains unresolved PDF split-word extraction damage"
SPLIT_WORD_ALLOWED_TOKENS = {
    "ai", "eu", "us", "uk", "iso", "nist", "act", "article", "risk",
    "to", "of", "in", "on", "by", "for", "and", "or", "the", "a", "an",
    "be", "its", "it", "as", "has", "have", "not", "shall", "must", "should",
    "will", "may", "can", "under", "within", "through",
}
SPLIT_WORD_COMMON_SUFFIXES = (
    "ed", "ing", "ion", "tion", "sion", "ment", "ity", "er", "or", "age",
    "ice", "ate", "ive", "al", "ent", "ant", "ure", "ary", "ence", "ance",
)
SPLIT_WORD_COMMON_PREFIXES = (
    "appropr", "identifie", "pro", "bef", "ser", "rep", "managem",
    "refer", "suc", "dam", "provid", "assess", "imple", "govern",
    "document", "monitor", "supervis", "author", "compet", "notifi",
)
GOVERNANCE_JOINED_TERMS = {
    "appropriate", "identified", "provider", "before", "service", "report",
    "management", "referred", "such", "damage", "assessment", "implementation",
    "documentation", "monitoring", "supervision", "authority", "competent",
    "notification", "requirements", "decisions", "obligation", "incident",
    "governance", "conformity", "oversight", "artificial", "intelligence",
}


def unresolved_split_word_damage(display_quote: str) -> tuple[bool, str]:
    """Detect likely unresolved PDF intra-word split damage in display text.

    The detector is intentionally heuristic and generic: it looks for unnatural
    adjacent alphabetic chunks that resemble one word after deterministic display
    repairs have already run, while allowing ordinary short governance words and
    acronyms such as AI, EU, US, UK, ISO, NIST, Act, and Article.
    """
    clean = " ".join((display_quote or "").split())
    if not clean:
        return False, ""

    suspicious: list[str] = []
    if re.search(r"(?:^|[.!?]\s+)[A-Za-z]\s+[a-z](?=\s)", clean):
        suspicious.append("sentence-start single-letter split")

    tokens = list(re.finditer(r"[A-Za-z]+", clean))
    for left, right in zip(tokens, tokens[1:]):
        if clean[left.end():right.start()] != " ":
            continue
        left_text = left.group(0)
        right_text = right.group(0)
        left_lower = left_text.lower()
        right_lower = right_text.lower()
        if left_lower in SPLIT_WORD_ALLOWED_TOKENS or right_lower in SPLIT_WORD_ALLOWED_TOKENS:
            continue
        if left_text.isupper() or right_text.isupper():
            continue
        joined = left_lower + right_lower
        if len(joined) < 6:
            continue
        suffix_like = len(right_lower) <= 5 and right_lower.endswith(SPLIT_WORD_COMMON_SUFFIXES)
        prefix_like = left_lower in SPLIT_WORD_COMMON_PREFIXES
        governance_join = joined in GOVERNANCE_JOINED_TERMS
        short_tail = len(right_lower) <= 2 and len(left_lower) >= 4
        single_letter_tail = len(right_lower) == 1 and len(left_lower) >= 5
        balanced_chunks = 2 <= len(left_lower) <= 8 and 2 <= len(right_lower) <= 5 and governance_join
        if governance_join or (prefix_like and (suffix_like or len(right_lower) <= 5)) or (short_tail and prefix_like) or single_letter_tail or balanced_chunks:
            suspicious.append(f"{left_text} {right_text}")

    if suspicious:
        return True, SPLIT_WORD_DAMAGE_REASON
    return False, ""

PRIMARY_QUOTE_QUALITY_THRESHOLD = 70
FINAL_PRIMARY_GATE_PREFIX = "final primary quote admission gate failed"
INCOMPLETE_EVIDENCE_PROPOSITION_REASON = f"{FINAL_PRIMARY_GATE_PREFIX}: incomplete evidence proposition"


def validate_primary_quote_record(record: dict) -> tuple[bool, str]:
    """Final hard admission gate for primary evidence quote records.

    This validator runs only after exact/display quote fields, display
    normalisation metadata, quote quality fields, and low-confidence metadata
    exist.  It is deliberately independent from quote-quality scoring so no
    damaged or incomplete record can leak into primary evidence rendering.
    """
    display_quote = " ".join(str(record.get("display_quote") or record.get("exact_quote") or "").split())
    exact_quote = " ".join(str(record.get("exact_quote") or "").split())
    if not display_quote:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: empty display quote"
    if not exact_quote:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: missing exact quote trace"
    if record.get("raw_exact_quote_retained") is not True:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: raw exact quote trace was not retained"

    score = record.get("quote_quality_score")
    try:
        score_value = int(score)
    except (TypeError, ValueError):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: missing quote quality score"
    if score_value < PRIMARY_QUOTE_QUALITY_THRESHOLD:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: quote quality score below primary threshold"

    low_confidence_reason = str(record.get("low_confidence_reason") or "").strip()
    if low_confidence_reason:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: low-confidence reason present: {low_confidence_reason}"

    unresolved_damage, unresolved_reason = unresolved_split_word_damage(display_quote)
    if unresolved_damage:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: {unresolved_reason}"

    has_complete_proposition, proposition_reason = quote_has_complete_evidence_proposition(display_quote)
    if not has_complete_proposition:
        return False, proposition_reason

    incomplete_reason = _incomplete_quote_reason(display_quote)
    if incomplete_reason:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: {incomplete_reason}"

    if NOISE_RE.search(display_quote) or (BROKEN_GLYPH_RE.search(display_quote) and "ai use or governance" not in display_quote.lower()):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: obvious PDF spacing artefact remains in display quote"
    if re.search(r"\b[A-Za-z]{1,2}\s+[A-Za-z]{1,2}\s+[A-Za-z]{1,2}\b", display_quote):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: display quote is unreadable as a normal institutional quote"

    display_letters = re.findall(r"[A-Za-z]", display_quote)
    if len(display_letters) < max(10, len(display_quote) // 4):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: display quote lacks readable institutional text"

    lower = display_quote.lower()
    if not any(term in lower for term in ACTION_QUOTE_TERMS):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: quote cannot support a complete source-says proposition"
    if not re.search(r"\b(shall|must|should|requires?|ensure|establish|implement|monitor|review|reviewed|update|updated|manage|document|assign|maintain|protect|report|disclose|notify|integrated|incorporated|consider)\b", lower):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: quote cannot support a complete source-says proposition"
    if len(_quote_signal_dimensions(display_quote)) < 2:
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: quote lacks enough actor/action/object/context structure for primary evidence"

    # Incident-report extraction damage has proven especially prone to clean-looking
    # but semantically brittle repairs. Keep the raw evidence visible in the
    # low-confidence trace unless the final source text was already clean.
    exact_lower = exact_quote.lower()
    if "repor t" in exact_lower and ("syste ms" in exact_lower or "marke t" in exact_lower):
        return False, f"{FINAL_PRIMARY_GATE_PREFIX}: raw incident-report evidence retains multiple PDF split-word artefacts requiring source review"

    return True, ""


def _append_final_gate_reason(record: dict, reason: str) -> dict:
    gated = dict(record)
    gated.setdefault("display_quote", gated.get("exact_quote", ""))
    gated.setdefault("quote_display_normalized", False)
    gated.setdefault("quote_display_normalization_reason", "")
    gated["raw_exact_quote_retained"] = True
    existing = str(gated.get("low_confidence_reason") or "").strip()
    if existing and reason not in existing:
        gated["low_confidence_reason"] = f"{existing}; {reason}"
    else:
        gated["low_confidence_reason"] = reason
    return gated


def _finalize_primary_quote_bank(records: list[dict], low_confidence_quote_candidates: list[dict] | None = None) -> list[dict]:
    primary: list[dict] = []
    seen_primary: set[str] = set()
    seen_low: set[str] = {q.get("exact_quote", "") for q in (low_confidence_quote_candidates or [])}
    for record in records:
        ok, reason = validate_primary_quote_record(record)
        if ok:
            admitted = dict(record)
            exact_key = " ".join(str(admitted.get("exact_quote") or "").split())
            if exact_key in seen_primary:
                continue
            seen_primary.add(exact_key)
            admitted["evidence_tier"] = "primary_quote_evidence"
            admitted["evidence_status"] = "clean_primary_quote"
            primary.append(admitted)
            continue
        gated = _append_final_gate_reason(record, reason)
        exact_quote = gated.get("exact_quote", "")
        if low_confidence_quote_candidates is not None and exact_quote not in seen_low:
            gated["quote_id"] = f"LQ{len(low_confidence_quote_candidates)+1:03d}"
            gated["evidence_tier"] = "low_confidence_extraction_trace"
            low_confidence_quote_candidates.append(gated)
            seen_low.add(exact_quote)
    for idx, record in enumerate(primary, start=1):
        record["quote_id"] = f"Q{idx:03d}"
        record["evidence_id"] = record["quote_id"]
    return primary



def _verification_issue_reason(record: dict) -> str:
    exact = " ".join(str(record.get("exact_quote") or "").split())
    display = " ".join(str(record.get("display_quote") or exact).split())
    reasons: list[str] = []
    unresolved_damage, unresolved_reason = unresolved_split_word_damage(display)
    if unresolved_damage:
        reasons.append(unresolved_reason)
    damage_reason = _unrepaired_extraction_damage_reason(exact, display)
    if damage_reason:
        reasons.append(damage_reason)
    has_complete, proposition_reason = quote_has_complete_evidence_proposition(display)
    if not has_complete:
        reasons.append(proposition_reason)
    incomplete_reason = _incomplete_quote_reason(display)
    if incomplete_reason:
        reasons.append(incomplete_reason)
    if NOISE_RE.search(display) or BROKEN_GLYPH_RE.search(display):
        reasons.append("obvious PDF spacing artefact or malformed extraction")
    gate_ok, gate_reason = validate_primary_quote_record(record)
    if not gate_ok:
        reasons.append(gate_reason)
    low_reason = str(record.get("low_confidence_reason") or "").strip()
    if low_reason:
        reasons.append(low_reason)
    deduped: list[str] = []
    for reason in reasons:
        reason = reason.strip()
        if reason and reason not in deduped:
            deduped.append(reason)
    return " / ".join(deduped) or "source-text verification required before primary quotation use"


def _likely_governance_signal(quote: str) -> str:
    lower = _normalized_for_quality(quote).lower()
    if "provider" in lower and ("natural person" in lower or "interact" in lower):
        return "provider obligation / human interaction transparency control"
    if "risk management" in lower or "residual risk" in lower:
        return "risk management obligation / residual risk control"
    if "technical documentation" in lower or "document" in lower:
        return "documentation / auditability control"
    if "incident" in lower or "report" in lower:
        return "incident reporting / post-market monitoring control"
    if "human oversight" in lower or "human review" in lower:
        return "human oversight / review control"
    if "conformity" in lower or "assessment" in lower:
        return "conformity assessment / assurance control"
    if any(term in lower for term in ("shall", "must", "should", "ensure", "establish", "implement", "monitor", "review", "manage")):
        return "governance obligation / institutional control signal"
    return "weak or noisy extraction trace"


VERIFICATION_RELEVANCE_MIN_SCORE = 3


def verification_relevance_assessment(record: dict) -> tuple[bool, int, str]:
    """Return whether an impaired candidate is useful enough for main-report verification.

    Verification-required evidence is intentionally narrower than the low-confidence
    audit trace: it must give a reviewer an actor/regulated party, an obligation or
    control action, and an object/domain signal that can support a concrete source
    review.
    """
    exact = str(record.get("exact_quote") or "")
    display = str(record.get("display_quote") or exact)
    combined = _normalized_for_quality(f"{exact} {display}").lower()
    reasons: list[str] = []
    if BOILERPLATE_QUOTE_RE.search(exact) or GENERIC_FRAGMENT_RE.search(exact):
        return False, 0, "weak verification relevance: boilerplate or generic fragment without reviewer-useful governance signal"
    if re.search(r"\b(free\s+moveme?\s*nt|cross-border|internal market)\b", combined) and not re.search(r"\b(provider|deployer|agency|shall|must|ensure|risk|documentation|incident|conformity|oversight)\b", combined):
        return False, 0, "weak verification relevance: incomplete movement/cross-border fragment without governance obligation"
    if len(re.findall(r"[A-Za-z]", combined)) < 25:
        return False, 0, "weak verification relevance: too little readable governance text"

    actor_terms = (
        "provider", "providers", "deployer", "deployers", "agency", "agencies", "public servant",
        "public servants", "organisation", "organization", "department", "supplier", "clinician",
        "nist", "humans", "responsible party", "accountable official", "all providers",
    )
    action_patterns = (
        r"\bshall\b", r"\bmust\b", r"\bshould\b", r"\brequires?\b", r"\brequired\b",
        r"\bensure\b", r"\bestablish\b", r"\bimplement\b", r"\bmaintain\b",
        r"\bmonitor\b", r"\breview\b", r"\bdocument\b", r"\breport\b",
        r"\bassess\b", r"\bdisclose\b", r"\bmanage\b", r"\bdesigned\b", r"\bdeveloped\b",
        r"\bintegrated\b", r"\bincorporated\b", r"\bnotify\b", r"\bupdated\b",
    )
    object_terms = (
        "ai system", "ai systems", "high-risk ai", "risk management", "risk", "residual risk",
        "evidence", "documentation", "technical documentation", "oversight", "human oversight",
        "human review", "natural persons", "incident", "reporting", "safety", "security",
        "privacy", "conformity", "assessment", "monitoring", "review", "escalation",
        "transparency statement", "ai use", "governance arrangements", "enterprise risk management",
        "control", "record", "register", "accountability",
    )

    has_actor = any(term in combined for term in actor_terms)
    has_action = any(re.search(pattern, combined) for pattern in action_patterns)
    has_object = any(term in combined for term in object_terms)
    score = int(has_actor) + int(has_action) + int(has_object)
    if has_actor:
        reasons.append("actor or regulated party present")
    if has_action:
        reasons.append("obligation/action/control signal present")
    if has_object:
        reasons.append("object/control/domain signal present")
    missing = []
    if not has_actor:
        missing.append("actor or regulated party")
    if not has_action:
        missing.append("obligation/action/control signal")
    if not has_object:
        missing.append("object/control/domain signal")
    if missing:
        return False, score, "weak verification relevance: missing " + ", ".join(missing)
    complete, _ = quote_has_complete_evidence_proposition(display or exact)
    unresolved_damage, _ = unresolved_split_word_damage(display or exact)
    extraction_damage = bool(PDF_INTR_WORD_DAMAGE_RE.search(exact) or NOISE_RE.search(display) or BROKEN_GLYPH_RE.search(display))
    if not complete and not (unresolved_damage or extraction_damage):
        return False, score, "weak verification relevance: incomplete fragment without extraction damage requiring source repair"
    return True, score, "; ".join(reasons)


def _is_governance_relevant_for_verification(record: dict) -> bool:
    return verification_relevance_assessment(record)[0]


def build_verification_required_evidence(candidates: list[dict], processing: dict, extraction: dict, limit: int = 12, admitted_quotes: list[dict] | None = None) -> list[dict]:
    """Passages that carry governance signal but cannot be quoted cleanly.

    A passage already admitted as a primary quote is excluded: the same clause
    must never appear in the report both as clean evidence and as evidence
    needing source verification. A truncated candidate whose complete form was
    admitted has been resolved, not left outstanding.
    """
    verification: list[dict] = []
    seen: set[str] = set()
    admitted = [" ".join(str(q.get("exact_quote") or "").split())
                for q in (admitted_quotes or [])]
    admitted = [q for q in admitted if q]
    for candidate in candidates:
        exact = " ".join(str(candidate.get("exact_quote") or "").split())
        if not exact or exact in seen:
            continue
        # Resolved elsewhere: a complete form of this passage was admitted.
        if any(exact in quote or quote in exact for quote in admitted):
            continue
        relevant, relevance_score, relevance_reason = verification_relevance_assessment(candidate)
        if not relevant:
            existing_reason = str(candidate.get("low_confidence_reason") or candidate.get("quote_quality_reason") or "").strip()
            candidate["low_confidence_reason"] = f"{existing_reason}; {relevance_reason}" if existing_reason and relevance_reason not in existing_reason else relevance_reason
            continue
        display = " ".join(str(candidate.get("display_quote") or exact).split())
        issue_reason = _verification_issue_reason(candidate)
        record = {
            "evidence_id": f"VQ{len(verification)+1:03d}",
            "evidence_tier": "verification_required_extracted_evidence",
            "evidence_status": "source_verification_required",
            "exact_quote": exact,
            "display_quote": display,
            "raw_exact_quote_retained": True,
            "source_file": candidate.get("source_file") or processing.get("stored_source_path") or processing.get("input_path"),
            "original_file_name": candidate.get("original_file_name") or processing.get("original_file_name"),
            "source_sha256": candidate.get("source_sha256") or processing.get("source_sha256"),
            "start_offset": candidate.get("start_offset"),
            "end_offset": candidate.get("end_offset"),
            "extraction_confidence": candidate.get("extraction_confidence") or extraction.get("extraction_confidence", "unknown"),
            "extraction_issue_reason": issue_reason,
            "likely_governance_signal": _likely_governance_signal(display or exact),
            "verification_relevance_score": relevance_score,
            "verification_relevance_reason": relevance_reason,
            "why_retained": "The passage appears evidence-bearing for governance analysis, but extraction quality or proposition completeness prevents clean primary quotation use.",
            "what_it_can_support": "A source-backed finding that the document appears to contain a relevant governance signal requiring source verification.",
            "what_it_cannot_support": "It cannot be presented as a clean, complete direct quotation or as proof of implementation, sufficiency, legal validity, certification, or operational adoption.",
            "reviewer_instruction": "Review the original source document or a cleaner text extraction before treating this passage as a clean quotation.",
        }
        verification.append(record)
        seen.add(exact)
        if len(verification) >= limit:
            break
    return verification


def build_extraction_quality_profile(extracted_text: str, extraction: dict, quote_bank: list[dict], verification_required_evidence: list[dict], low_confidence_quote_candidates: list[dict]) -> dict:
    text = extracted_text or ""
    token_count = max(1, len(re.findall(r"\S+", text)))
    damaged_hits = len(PDF_INTR_WORD_DAMAGE_RE.findall(text)) + len(NOISE_RE.findall(text)) + len(BROKEN_GLYPH_RE.findall(text))
    damaged_token_density = round(damaged_hits / token_count, 6)
    incomplete_count = 0
    final_gate_failure_count = 0
    for candidate in low_confidence_quote_candidates or []:
        display = candidate.get("display_quote") or candidate.get("exact_quote") or ""
        if not quote_has_complete_evidence_proposition(display)[0] or _incomplete_quote_reason(display):
            incomplete_count += 1
        reason = str(candidate.get("low_confidence_reason") or candidate.get("quote_quality_reason") or "")
        if FINAL_PRIMARY_GATE_PREFIX in reason:
            final_gate_failure_count += 1
    quote_candidate_count = max(1, len(quote_bank) + len(verification_required_evidence) + len(low_confidence_quote_candidates or []))
    incomplete_quote_density = round(incomplete_count / quote_candidate_count, 6)
    verification_count = len(verification_required_evidence or [])
    low_count = len(low_confidence_quote_candidates or [])
    primary_count = len(quote_bank or [])
    confidence = extraction.get("extraction_confidence", "unknown")
    low_confidence_extractor = confidence == "low" and extraction.get("extractor_used") != "text-fallback"
    poor_damage_threshold = 0.03
    limited_damage_threshold = 0.005
    damaged_or_incomplete_count = verification_count + incomplete_count + final_gate_failure_count
    damaged_or_incomplete_dominant = verification_count > primary_count or (primary_count == 0 and damaged_or_incomplete_count > 0)
    repeated_damaged_evidence = damaged_or_incomplete_count >= 3 or (low_count >= 4 and damaged_token_density >= limited_damage_threshold)
    final_gate_failures_high = final_gate_failure_count >= max(3, primary_count * 2) and damaged_token_density >= limited_damage_threshold
    verification_damage_high = verification_count >= 3 and damaged_token_density >= limited_damage_threshold
    if (
        low_confidence_extractor
        or (damaged_token_density >= poor_damage_threshold and repeated_damaged_evidence and damaged_or_incomplete_dominant)
        or (verification_count >= 4 and primary_count == 0)
        or (low_count >= 4 and damaged_token_density >= limited_damage_threshold and repeated_damaged_evidence)
        or final_gate_failures_high
        or verification_damage_high
        or (repeated_damaged_evidence and damaged_token_density >= limited_damage_threshold and damaged_or_incomplete_dominant)
    ):
        level = "poor"
    elif verification_count or damaged_token_density >= limited_damage_threshold or incomplete_quote_density >= 0.25 or final_gate_failure_count:
        level = "limited" if primary_count == 0 else "moderate"
    elif low_count > primary_count * 2 and low_count >= 4:
        level = "moderate"
    else:
        level = "high"

    clean_primary_count = len(_gate_passing_primary_quotes(quote_bank or []))
    if level == "poor":
        primary_quote_eligible = False
    elif level == "limited":
        primary_quote_eligible = clean_primary_count >= 2 and not damaged_or_incomplete_dominant
    else:
        primary_quote_eligible = clean_primary_count > 0
    warning = ""
    action = "Primary quotes may be used normally while retaining exact extracted source traces."
    if level in {"limited", "poor"}:
        warning = "Extraction quality limits clean primary quotation use but does not invalidate the source document or deterministic source-backed findings."
        action = "Review the original source document or produce a cleaner text extraction before treating verification-required passages as clean quotations."
    elif verification_count:
        warning = "Some evidence-bearing extracted passages require source verification before clean quotation use."
        action = "Use primary_quote_evidence for clean quotation and verify extraction-impaired passages against the source before quoting them as clean text."
    return {
        "extraction_quality_level": level,
        "primary_quote_eligible": primary_quote_eligible,
        "verification_required_evidence_present": verification_count > 0,
        "source_text_reliability_warning": warning,
        "damaged_token_density": damaged_token_density,
        "incomplete_quote_density": incomplete_quote_density,
        "final_gate_failure_count": final_gate_failure_count,
        "verification_required_count": verification_count,
        "low_confidence_quote_count": low_count,
        "primary_quote_count": primary_count,
        "extractor_used": extraction.get("extractor_used", "unknown"),
        "extraction_confidence": confidence,
        "recommended_user_action": action,
    }

def _gate_passing_primary_quotes(quote_bank: list[dict]) -> list[dict]:
    return [quote for quote in quote_bank if validate_primary_quote_record(quote)[0]]

def _preserve_initial_case(match: re.Match[str], replacement: str) -> str:
    text = match.group(0)
    if text.startswith("AI-"):
        return replacement
    if text[:1].isupper() and replacement[:1].islower():
        return replacement[:1].upper() + replacement[1:]
    return replacement


# Compiled once. These 54 patterns were rebuilt on every call, and the function
# runs tens of thousands of times over a large document's quote candidates —
# re.escape, re.compile and the IGNORECASE flag lookup accounted for most of the
# runtime of quote-bank construction. Behaviour and output are unchanged.
_DISPLAY_QUOTE_REPAIR_PATTERNS = tuple(
    (re.compile(rf"(?<![A-Za-z]){re.escape(_damaged)}(?![A-Za-z])", re.IGNORECASE),
     _damaged, _repaired)
    for _damaged, _repaired in DISPLAY_QUOTE_REPAIRS
)


def normalize_quote_for_display(quote: str) -> tuple[str, bool, str]:
    """Return deterministic presentation text while preserving the raw exact quote elsewhere."""
    display = quote or ""
    changed_repairs: list[str] = []
    for pattern, damaged, repaired in _DISPLAY_QUOTE_REPAIR_PATTERNS:
        if pattern.search(display):
            display = pattern.sub(lambda m, r=repaired: _preserve_initial_case(m, r), display)
            changed_repairs.append(f"{damaged}->{repaired}")
    normalized = display != (quote or "")
    if normalized:
        return display, True, "deterministic PDF intra-word spacing repair: " + ", ".join(changed_repairs)
    return display, False, ""


# Quote quality is recomputed for the same candidate text many times over
# (sorting, gating, display). The mapping is pure, so memoising it removes the
# repetition without changing any result.
@functools.lru_cache(maxsize=8192)
def _normalized_for_quality(quote: str) -> str:
    clean = " ".join((quote or "").split())
    return normalize_quote_for_display(clean)[0]


def _quote_display_fields(exact_quote: str) -> dict:
    display_quote, normalized, reason = normalize_quote_for_display(exact_quote)
    return {
        "display_quote": display_quote,
        "quote_display_normalized": normalized,
        "quote_display_normalization_reason": reason,
        "raw_exact_quote_retained": True,
    }


def _incomplete_quote_reason(quote: str) -> str:
    clean = " ".join((quote or "").split())
    lower = clean.lower()
    if not clean:
        return "empty quote"
    if re.match(r"^[a-z,;:]", clean) or clean.endswith(",") or INCOMPLETE_END_RE.search(clean):
        return "incomplete quote could not be expanded to complete evidence statement"
    if not quote_has_complete_evidence_proposition(clean)[0]:
        return "incomplete quote could not be expanded to complete evidence statement"
    incomplete_patterns = (
        r"^after completing the manage function, plans for prioritizing risk and regular monitoring$",
        r"^ai-generated content has undergone$",
        r"^when implementing the risk management system as provided$",
        r"shall be responsible for ensuring$",
        r"\b(has undergone|as provided|for ensuring)\s*$",
    )
    if any(re.search(pattern, lower) for pattern in incomplete_patterns):
        return "incomplete quote could not be expanded to complete evidence statement"
    return ""



def quote_has_complete_evidence_proposition(display_quote: str) -> tuple[bool, str]:
    """Return whether display text can stand alone as primary evidence.

    The primary evidence surface must let a reviewer understand the full
    source-says proposition without supplying missing continuation text from
    the source. This catches readable but semantically dangling fragments after
    display normalisation and before any report/analyst primary rendering.
    """
    clean = " ".join((display_quote or "").split())
    if not clean:
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON
    lower = clean.lower().strip(" \\\"“”'")

    if re.match(r"^to above should\b", lower):
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON
    if re.search(r"\bdra\s+w\b", lower):
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON

    incomplete_endings = (
        "on the use of high-risk",
        "before that system is placed on the market or put into",
        "shall be such that the relevant residual risk",
        "should ensure that the provider",
        "ensure that the provider",
        "take into account",
        "placed on",
        "put into",
        "the provider",
        "provider",
        "residual risk",
        "high-risk",
        "their ai",
        "the agency make",
        "broader enterprise",
        "ai systems work",
        "as appropriate; a review",
        "nist will review",
        "when they publish and make any changes to their ai",
        "updated annually or sooner, should the agency make",
    )
    if any(lower.endswith(ending) for ending in incomplete_endings):
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON

    dangling_patterns = (
        r"\b(can|may|must|shall|should|will|would|could)\s*$",
        r"\b(in order to|so as to|with a view to|for the purpose of)\s+[^.!?;:]*$",
        r"\b(ensure|ensures|ensuring|requires?|required|referred to|such that)\s+(?:the\s+)?$",
        r"\b(?:take|taken|taking)\s+into\s+account(?:\s+[^.!?;:]*)?$",
        r"\b(?:placed|placing)\s+on(?:\s+[^.!?;:]*)?$",
        r"\bput(?:ting)?\s+into(?:\s+[^.!?;:]*)?$",
        r"\b(?:associated|connected|related)\s+with\s*$",
        r"\b(?:relevant|residual|high-risk)\s*$",
        r";\s*(?:a|an|the)?\s*(?:review|assessment|process|procedure)?\s*$",
        r"\bintegrated\s+(?:and\s+incorporated\s+)?into\s+broader\s+enterprise\s*$",
        r"\bassume\s+that\s+ai\s+systems\s+work\s*$",
        r"\bchanges\s+to\s+their\s+ai\s*$",
        r"\bshould\s+the\s+agency\s+make\s*$",
    )
    if any(re.search(pattern, lower) for pattern in dangling_patterns):
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON

    subordinate_markers = ("when", "where", "while", "if", "unless", "because", "after", "before", "should")
    if re.match(r"^(in order to|when|where|while|if|unless|because|after|before)\b", lower) and not re.search(r"[.!?]$", clean):
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON
    if re.search(r"[,;]\s*(?:" + "|".join(subordinate_markers) + r")\b[^.!?]*$", lower) and not re.search(r"[.!?]$", clean):
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON

    has_sentence_punctuation = bool(re.search(r"[.!?]$", clean))
    has_legal_control_proposition = (
        bool(re.search(r"\b(shall|must|should|requires?|ensure|establish|implement|monitor|review|reviewed|update|updated|manage|document|assign|maintain|protect|report|disclose|notify|integrated|incorporated|consider)\b", lower))
        and len(_quote_signal_dimensions(clean)) >= 2
        and not re.search(r"\b(?:of|to|for|with|that|the|and|or|by|on|into|through|within|including|regarding|from|under)\s*$", lower)
    )
    if not has_sentence_punctuation and not has_legal_control_proposition:
        return False, INCOMPLETE_EVIDENCE_PROPOSITION_REASON

    return True, ""

def _unrepaired_extraction_damage_reason(exact_quote: str, display_quote: str) -> str:
    exact_has_damage = bool(PDF_INTR_WORD_DAMAGE_RE.search(exact_quote or "") or NOISE_RE.search(exact_quote or ""))
    display_has_damage = bool(PDF_INTR_WORD_DAMAGE_RE.search(display_quote or "") or NOISE_RE.search(display_quote or "") or BROKEN_GLYPH_RE.search(display_quote or ""))
    if exact_has_damage and display_has_damage:
        return "extraction-damaged spacing could not be safely normalised"
    return ""


def _quote_signal_dimensions(quote: str) -> set[str]:
    lower = _normalized_for_quality(quote).lower()
    dimensions: set[str] = set()
    if re.search(r"\b(provider|providers|deployer|deployers|agency|agencies|organisation|organization|department|supplier|clinician|public servants?|responsible party|accountable officials?|nist|humans?)\b", lower):
        dimensions.add("actor")
    if re.search(r"\b(shall|must|should|required|requires?|ensure|establish|implement|maintain|monitor|review|reviewed|update|updated|document|report|assess|disclose|manage|notify|integrated|incorporated|consider)\b", lower):
        dimensions.add("action")
    if re.search(r"\b(risk|ai rmf|ai systems?|transparency statement|statement|governance arrangements|enterprise risk management|evidence|documentation|oversight|accountability|incident|safety|privacy|security|conformity|assessment|register|record|review|redress|technical documentation|human review)\b", lower):
        dimensions.add("object")
    if re.search(r"\b(before deployment|post-market|incident|harm|audit|assurance|approval|monitoring|escalation|exception|deployment|review)\b", lower):
        dimensions.add("context")
    return dimensions


def _profile_quote_terms(assessment: dict) -> tuple[str, ...]:
    profile = document_profile_key(assessment) if isinstance(assessment, dict) else ""
    by_profile = {
        "nist": ("risk management framework", "govern", "map", "measure", "manage", "trustworthy ai", "valid", "reliable", "safe", "secure", "accountable", "transparent", "fair", "document risks", "monitor", "review"),
        "eu_ai_act": ("providers", "deployers", "high-risk ai systems", "risk management system", "technical documentation", "conformity assessment", "post-market monitoring", "serious incident reporting", "human oversight", "general-purpose ai model"),
        "eo_14110": ("agencies shall", "secretary", "agency", "safety", "security standards", "report", "implementation", "privacy", "civil rights", "labour", "competition", "accountability"),
        "dtac": ("clinical safety case", "hazard log", "dcb0129", "clinical safety officer", "data protection", "technical security", "interoperability", "evidence submission"),
        "australian_policy": ("agencies must", "public servants", "responsible ai use", "human review", "disclose ai use", "ai use register", "accountability record", "exception", "incident reporting"),
    }
    return by_profile.get(profile, ())


def _profile_quote_score(sentence: str, assessment: dict) -> int:
    lower = sentence.lower()
    return sum(1 for term in _profile_quote_terms(assessment) if term in lower)


def _expanded_sentence_window(text: str, start: int, end: int) -> tuple[int, int, str]:
    para_start = text.rfind("\n\n", 0, start)
    para_start = 0 if para_start < 0 else para_start + 2
    para_end = text.find("\n\n", end)
    para_end = len(text) if para_end < 0 else para_end
    sent_start = max(para_start, text.rfind(".", para_start, start) + 1, text.rfind("!", para_start, start) + 1, text.rfind("?", para_start, start) + 1)
    sent_ends = [idx for idx in (text.find(".", end), text.find("!", end), text.find("?", end)) if idx >= 0]
    sent_end = min(sent_ends) + 1 if sent_ends else para_end
    expanded = text[sent_start:sent_end].strip()
    expanded_start = text.find(expanded, sent_start) if expanded else start
    if expanded and expanded_start >= 0:
        return expanded_start, expanded_start + len(expanded), expanded
    return start, end, text[start:end].strip()


def _expand_incomplete_candidate(text: str, start: int, end: int, quote: str) -> tuple[int, int, str]:
    """Expand bridge-ending evidence only to source sentence/paragraph boundaries."""
    display_quote = _normalized_for_quality(quote)
    if not _incomplete_quote_reason(display_quote):
        return start, end, quote
    expanded_start, expanded_end, expanded_quote = _expanded_sentence_window(text, start, end)
    expanded_display = _normalized_for_quality(expanded_quote)
    if (expanded_start, expanded_end, expanded_quote) != (start, end, quote) and not _incomplete_quote_reason(expanded_display):
        return expanded_start, expanded_end, expanded_quote
    return start, end, quote

def quote_quality(quote: str, extraction: dict) -> tuple[int, str]:
    """Score candidate evidence before it can enter the primary quote bank."""
    raw_clean = " ".join((quote or "").split())
    display_clean = _normalized_for_quality(raw_clean)
    lower = display_clean.lower()
    norm_lower = lower
    if extraction.get("extraction_confidence") == "low" and extraction.get("extractor_used") != "text-fallback":
        return 20, "extractor reported low confidence"
    if not raw_clean:
        return 0, "empty quote"
    if BOILERPLATE_QUOTE_RE.search(raw_clean):
        return 10, "generic disclaimer or identification boilerplate"
    if GENERIC_FRAGMENT_RE.search(raw_clean):
        return 15, "generic incomplete fragment without governance context"
    damage_reason = _unrepaired_extraction_damage_reason(raw_clean, display_clean)
    if damage_reason:
        return 15, damage_reason
    unresolved_damage, unresolved_reason = unresolved_split_word_damage(display_clean)
    if unresolved_damage:
        return 15, unresolved_reason
    if TOC_QUOTE_RE.match(display_clean):
        return 10, "table of contents or page-number fragment"
    if NOISE_RE.search(display_clean) or (BROKEN_GLYPH_RE.search(display_clean) and "ai use or governance" not in norm_lower):
        return 15, "possible PDF extraction noise, glyph spacing, or malformed fragment"
    if len(re.findall(r"[A-Za-z]", display_clean)) < max(10, len(display_clean) // 4):
        return 20, "insufficient alphabetic governance content"
    if TITLE_ONLY_RE.match(display_clean) and len(display_clean.split()) <= 8 and not any(t in lower for t in ACTION_QUOTE_TERMS):
        return 20, "title or isolated heading without governance action"
    incomplete_reason = _incomplete_quote_reason(display_clean)
    if incomplete_reason:
        return 25, incomplete_reason
    dimensions = _quote_signal_dimensions(display_clean)
    if len(display_clean) < 80 and not any(t in norm_lower for t in ("shall", "must", "should", "requires", "required", "ensure", "implement", "review", "update", "notify")):
        return 35, "short fragment without strong obligation or control phrase"
    if not any(t in norm_lower for t in ACTION_QUOTE_TERMS):
        return 35, "no governance action, obligation, risk, evidence, or control term"
    if not re.search(r"\b(shall|must|should|requires?|ensure|establish|implement|monitor|review|reviewed|update|updated|manage|document|assign|maintain|protect|report|disclose|notify|integrated|incorporated|consider)\b", norm_lower):
        return 35, "no institutional action or obligation verb explaining a governance signal"
    if len(dimensions) < 2:
        return 45, "quote lacks enough actor/action/object/context structure for primary evidence"
    score = 70 + len(dimensions) * 5
    if len(display_clean) >= 120:
        score += 5
    if any(t in norm_lower for t in ("shall", "must", "requires", "ensure", "implement", "conformity", "incident", "evidence")):
        score += 5
    return min(score, 95), "primary evidence: complete governance action with actor/control context"


def _is_low_confidence_quote(quote: str, extraction: dict) -> tuple[bool, str]:
    score, reason = quote_quality(quote, extraction)
    return score < 70, reason


def _candidate_quote_record(quote_id: str, start: int, end: int, quote: str, processing: dict, extraction: dict, assessment: dict, category: str, repair_field: str) -> dict:
    score, reason = quote_quality(quote, extraction)
    return {
        "quote_id": quote_id,
        "source_file": processing.get("stored_source_path") or processing.get("input_path"),
        "original_file_name": processing.get("original_file_name"),
        "source_sha256": processing.get("source_sha256"),
        "document_type": assessment.get("document_type", "unknown_governance_document"),
        "sector_profile": assessment.get("sector_profile", "general_ai_governance"),
        "signal_category": category,
        "exact_quote": quote,
        **_quote_display_fields(quote),
        "surrounding_context": quote,
        "start_offset": start,
        "end_offset": end,
        "extraction_confidence": extraction.get("extraction_confidence", "unknown"),
        "why_it_matters": f"Candidate source evidence for {category} analysis.",
        "what_it_proves": f"The document contains language potentially relevant to {category}.",
        "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
        "linked_governance_repair_field": repair_field,
        "linked_gap_ids": [],
        "low_confidence_reason": reason if score < 70 else "",
        "quote_quality_score": score,
        "quote_quality_reason": reason,
    }


def build_quote_bank(text: str, processing: dict, extraction: dict, assessment: dict, low_confidence_quote_candidates: list[dict] | None = None) -> list[dict]:
    records: list[dict] = []
    seen: set[tuple[int, int, str]] = set()
    lowered_text = text.lower()
    spans = _sentence_spans(text)
    for category, terms, repair_field in SIGNAL_CATEGORIES:
        best: tuple[int, int, str] | None = None
        matching_spans: list[tuple[int, int, str]] = []
        for start, end, sentence in spans:
            lo = _normalized_for_quality(sentence).lower()
            if any(term.lower() in lo for term in terms):
                matching_spans.append((start, end, sentence))
        if matching_spans:
            best = max(matching_spans, key=lambda item: (_profile_quote_score(item[2], assessment), quote_quality(item[2], extraction)[0], len(item[2])))
        if best is None:
            for term in terms:
                idx = lowered_text.find(term.lower())
                if idx >= 0:
                    start = max(0, idx - 160)
                    end = min(len(text), idx + 320)
                    start, end, sentence = _expanded_sentence_window(text, start, end)
                    best = (start, end, sentence)
                    break
        if best is None:
            continue
        start, end, quote = best
        start, end, quote = _expand_incomplete_candidate(text, start, end, quote)
        if (start, end, category) in seen or quote not in text:
            continue
        score, reason = quote_quality(quote, extraction)
        if score < PRIMARY_QUOTE_QUALITY_THRESHOLD:
            # Exclude low-confidence/noisy fragments from the primary quote bank.
            continue
        seen.add((start, end, category))
        context_start = max(0, start - 160)
        context_end = min(len(text), end + 160)
        records.append({
            "quote_id": f"Q{len(records)+1:03d}",
            "source_file": processing.get("stored_source_path") or processing.get("input_path"),
            "original_file_name": processing.get("original_file_name"),
            "source_sha256": processing.get("source_sha256"),
            "document_type": assessment.get("document_type", "unknown_governance_document"),
            "sector_profile": assessment.get("sector_profile", "general_ai_governance"),
            "signal_category": category,
            "exact_quote": quote,
            **_quote_display_fields(quote),
            "surrounding_context": text[context_start:context_end].strip(),
            "start_offset": start,
            "end_offset": end,
            "extraction_confidence": extraction.get("extraction_confidence", "unknown"),
            "why_it_matters": f"This is deterministic source evidence for {category} analysis.",
            "what_it_proves": f"The document contains language relevant to {category}.",
            "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
            "linked_governance_repair_field": repair_field,
            "linked_gap_ids": [],
            "low_confidence_reason": "",
            "quote_quality_score": score,
            "quote_quality_reason": reason,
        })
        if len(records) >= 12:
            break
    if len(records) < 12:
        for start, end, quote in spans:
            if any(existing["exact_quote"] == quote for existing in records):
                continue
            score, reason = quote_quality(quote, extraction)
            display_fields = _quote_display_fields(quote)
            if score < PRIMARY_QUOTE_QUALITY_THRESHOLD or _incomplete_quote_reason(display_fields["display_quote"]):
                continue
            context_start = max(0, start - 160)
            context_end = min(len(text), end + 160)
            records.append({
                "quote_id": f"Q{len(records)+1:03d}",
                "source_file": processing.get("stored_source_path") or processing.get("input_path"),
                "original_file_name": processing.get("original_file_name"),
                "source_sha256": processing.get("source_sha256"),
                "document_type": assessment.get("document_type", "unknown_governance_document"),
                "sector_profile": assessment.get("sector_profile", "general_ai_governance"),
                "signal_category": "display-normalised source evidence",
                "exact_quote": quote,
                **display_fields,
                "surrounding_context": text[context_start:context_end].strip(),
                "start_offset": start,
                "end_offset": end,
                "extraction_confidence": extraction.get("extraction_confidence", "unknown"),
                "why_it_matters": "This source evidence required deterministic display normalisation while retaining exact extracted text.",
                "what_it_proves": "The document contains a complete governance signal affected by repairable PDF intra-word spacing.",
                "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
                "linked_governance_repair_field": "source_excerpt",
                "linked_gap_ids": [],
                "low_confidence_reason": "",
                "quote_quality_score": score,
                "quote_quality_reason": reason,
            })
            if len(records) >= 12:
                break
    if records:
        records = sorted(records, key=lambda record: 0 if record.get("quote_display_normalized") else 1)
        for idx, record in enumerate(records, start=1):
            record["quote_id"] = f"Q{idx:03d}"
    if not records:
        for start, end, quote in spans[:1]:
            start, end, quote = _expand_incomplete_candidate(text, start, end, quote)
            score, reason = quote_quality(quote, extraction)
            if score < PRIMARY_QUOTE_QUALITY_THRESHOLD or quote not in text:
                continue
            records.append({
                "quote_id": "Q001", "source_file": processing.get("stored_source_path") or processing.get("input_path"),
                "original_file_name": processing.get("original_file_name"), "source_sha256": processing.get("source_sha256"),
                "document_type": assessment.get("document_type", "unknown_governance_document"), "sector_profile": assessment.get("sector_profile", "general_ai_governance"),
                "signal_category": "audit/documentation", "exact_quote": quote, **_quote_display_fields(quote), "surrounding_context": quote,
                "start_offset": start, "end_offset": end, "extraction_confidence": extraction.get("extraction_confidence", "unknown"),
                "why_it_matters": "Fallback exact source excerpt for reviewer orientation.",
                "what_it_proves": "The quoted text exists in the extracted source.",
                "what_it_does_not_prove": "It does not prove implementation, sufficiency, legal validity, certification, or operational adoption.",
                "linked_governance_repair_field": "source_excerpt", "linked_gap_ids": [], "low_confidence_reason": "",
                "quote_quality_score": score, "quote_quality_reason": reason,
            })
    return _finalize_primary_quote_bank(records, low_confidence_quote_candidates)


def build_low_confidence_quote_candidates(text: str, processing: dict, extraction: dict, assessment: dict, limit: int = 12) -> list[dict]:
    candidates: list[dict] = []
    seen_quotes: set[str] = set()
    for start, end, quote in _sentence_spans(text):
        score, reason = quote_quality(quote, extraction)
        compact = " ".join(quote.split())
        display_compact_for_gate = normalize_quote_for_display(compact)[0]
        has_complete_proposition, proposition_reason = quote_has_complete_evidence_proposition(display_compact_for_gate)
        if not has_complete_proposition:
            if reason and proposition_reason not in reason:
                reason = f"{reason}; {proposition_reason}"
            else:
                reason = proposition_reason
            score = min(score, PRIMARY_QUOTE_QUALITY_THRESHOLD - 1)
        if score >= PRIMARY_QUOTE_QUALITY_THRESHOLD or compact in seen_quotes:
            continue
        display_compact = _normalized_for_quality(compact).lower()
        if not any(term in display_compact for term in ACTION_QUOTE_TERMS + ("artificial intelligence", "ai-generated", "secure", "resilient")) and score > 15:
            continue
        seen_quotes.add(compact)
        candidate = _candidate_quote_record(f"LQ{len(candidates)+1:03d}", start, end, quote, processing, extraction, assessment, "low-confidence candidate", "source_excerpt")
        if not has_complete_proposition:
            existing_reason = str(candidate.get("low_confidence_reason") or reason).strip()
            if existing_reason and proposition_reason not in existing_reason:
                candidate_reason = f"{existing_reason}; {proposition_reason}"
            else:
                candidate_reason = proposition_reason
            candidate["low_confidence_reason"] = candidate_reason
            candidate["quote_quality_score"] = min(int(candidate.get("quote_quality_score") or score), PRIMARY_QUOTE_QUALITY_THRESHOLD - 1)
            candidate["quote_quality_reason"] = candidate_reason
        candidates.append(candidate)
        if len(candidates) >= limit:
            break
    return candidates



def document_profile_key(assessment: dict) -> str:
    if assessment.get("document_profile_key"):
        return assessment["document_profile_key"]
    doc_type = assessment.get("document_type", "unknown_governance_document")
    sector = assessment.get("sector_profile", "general_ai_governance")
    # Corpus-specific naming belongs only to the instrument it names. Identity
    # is established by anchors in the document itself; a shared sector or
    # document class is not identity.
    identified = assessment.get("known_instrument_profile") or ""
    if identified:
        return identified
    return doc_type


def document_specific_gap_title(gap_type: str, fallback: str, assessment: dict) -> str:
    profile = document_profile_key(assessment)
    titles = {
        "nist": {
            "framework_guidance_without_implementation_artifact": "NIST guidance requires implementation artifact before assurance reliance",
            "risk_without_closure_gate": "NIST risk guidance requires a risk closure gate before operational reliance",
            "evidence_presence_without_sufficiency": "NIST trustworthiness evidence requires sufficiency criteria before assurance reliance",
        },
        "eu_ai_act": {
            "legal_obligation_without_operational_mapping": "EU AI Act legal obligation requires local provider/deployer evidence mapping",
            "evidence_presence_without_sufficiency": "EU AI Act technical documentation requires evidence sufficiency gate",
            "monitoring_without_threshold": "EU AI Act monitoring obligation requires local threshold and escalation workflow",
        },
        "eo_14110": {
            "obligation_without_owner": "EO 14110 agency direction requires accountable implementation owner",
            "monitoring_without_threshold": "EO 14110 reporting expectation requires implementation tracking threshold",
            "policy_without_enforcement_consequence": "EO 14110 agency policy force requires escalation consequence",
        },
        "dtac": {
            "evidence_presence_without_sufficiency": "DTAC evidence submission requires sufficiency and live review gate",
            "safety_case_without_live_review": "DTAC clinical safety case requires live review and hazard-log ownership",
            "risk_without_closure_gate": "DTAC transferred clinical risk requires acceptance gate",
        },
        "australian_policy": {
            "obligation_without_owner": "Public sector AI policy requires accountable owner for responsible use",
            "evidence_presence_without_sufficiency": "Public sector AI use records require evidence sufficiency and disclosure control",
            "policy_without_enforcement_consequence": "Government AI policy requires exception and incident escalation consequence",
        },
    }
    return titles.get(profile, {}).get(gap_type, fallback)


# A control's name must say what the control does about THIS gap. Naming
# controls from a per-instrument list indexed by gap number produced names
# unrelated to the gap they closed (a redress gap named as a safety register).
_CONTROL_NAME_BY_GAP = {
    "obligation_without_owner": "Accountability Register for Mandatory Duties",
    "evidence_presence_without_sufficiency": "Evidence Acceptance Criteria and Rejection Log",
    "monitoring_without_threshold": "Monitoring Threshold and Escalation Specification",
    "policy_without_enforcement_consequence": "Breach Consequence Schedule",
    "risk_without_closure_gate": "Deployment Gate with Stop Authority",
    "incident_reporting_without_redress": "Affected-Person Challenge and Reversal Route",
    "lifecycle_without_change_control": "Change-Control and Re-Approval Procedure",
    "safety_case_without_live_review": "Clinical Safety Live Assurance Register",
    "supplier_duty_without_deployer_acceptance": "Supplier Assurance Acceptance Checklist",
    "declaratory_without_operative_commitment": "Statement of Operative Commitments",
    "insufficient_operative_content": "Assessment of the Operative Instrument This Document Refers To",
    "vocabulary_without_operative_effect": "Rewrite of Named Controls into Operative Form",
}

# Instrument-specific naming applies only where the instrument is identified by
# anchors in the document itself AND the gap is one that instrument's own
# vocabulary names differently.
_CONTROL_NAME_BY_PROFILE_AND_GAP = {
    ("nist", "risk_without_closure_gate"): "AI Risk Closure Gate (GOVERN/MAP alignment)",
    ("nist", "evidence_presence_without_sufficiency"): "Trustworthiness Evidence Acceptance Matrix",
    ("eu_ai_act", "obligation_without_owner"): "Provider/Deployer Obligation Mapping Register",
    ("eu_ai_act", "evidence_presence_without_sufficiency"): "High-Risk AI Technical Documentation Sufficiency Gate",
    ("eu_ai_act", "monitoring_without_threshold"): "Post-Market Monitoring and Serious-Incident Escalation Control",
    ("eo_14110", "obligation_without_owner"): "Agency AI Directive Implementation Tracker",
    ("eo_14110", "evidence_presence_without_sufficiency"): "Federal AI Safety and Security Evidence Register",
    ("dtac", "safety_case_without_live_review"): "Clinical Safety Live Assurance Register",
    ("dtac", "evidence_presence_without_sufficiency"): "DTAC Evidence Sufficiency Matrix",
    ("australian_policy", "obligation_without_owner"): "Public Sector AI Use Register",
    ("australian_policy", "incident_reporting_without_redress"): "Human Review and Accountability Evidence Log",
}


def control_name_for_gap(gap: dict) -> str:
    profile = document_profile_key(gap)
    gap_type = gap.get("gap_type", "")
    named = _CONTROL_NAME_BY_PROFILE_AND_GAP.get((profile, gap_type))
    if named:
        return named
    return _CONTROL_NAME_BY_GAP.get(
        gap_type,
        f"Operational closure control for {gap_type.replace('_', ' ')}" if gap_type
        else "Operational closure control")


def executive_thesis(assessment: dict, gaps: list[dict], controls: list[dict]) -> str:
    """The one sentence a decision-maker reads.

    It must be a function of the assessment result: two documents of different
    structural quality can never receive the same finding. Leads with the
    engine's own verdict (structural alignment, calibrated position, whether
    obligations are bound to the people they protect), then the document-type
    framing, then this document's leading gap and next action.
    """
    doc_type = assessment.get("document_type", "unknown_governance_document")
    alignment = assessment.get("laif_alignment", "")
    coupling = assessment.get("coupling_state", "ABSENT")
    cal = assessment.get("score_calibration", {}) or {}
    pct = cal.get("overall_pct_of_ceiling")
    overall = assessment.get("overall_readiness_score", 0)

    # 1. Verdict — derived, never templated.
    verdict = {
        "FUNCTIONALLY ALIGNED": (
            "This document already expresses the structural protections a governance "
            "instrument needs, in its own vocabulary."),
        "PARTIALLY ALIGNED": (
            "This document carries part of the structural machinery a governance "
            "instrument needs; the rest is absent rather than differently worded."),
        "STRUCTURALLY UNALIGNED": (
            "This document does not express the load-bearing governance structures in "
            "any vocabulary — the gaps below are missing machinery, not missing "
            "terminology."),
    }.get(alignment, "This document's structural position requires reviewer confirmation.")
    if not assessment.get("english_language_readable", True):
        verdict = (
            "This assessment could not read the document. Every detection pattern in "
            "this engine is written against English governance drafting, and this "
            "text is not in English, so the scores and findings below describe the "
            "limits of the instrument rather than the quality of the document.")

    # 2. What that means for the people it governs.
    binding = {
        "STRUCTURAL": "Its obligations are explicitly bound to the interests they protect.",
        "FUNCTIONAL": "Its obligations are bound to the interests they protect, in the document's own words.",
        "IMPLICIT": "It signals protective intent, but its obligations are not bound to any identifiable beneficiary.",
        "ABSENT": "Its obligations are not tied to the people they are meant to protect.",
    }.get(coupling, "")
    if assessment.get("vocabulary_enumeration_risk") == "HIGH":
        binding = ("Whether its obligations are bound to the interests they protect "
                   "cannot be read from the text: the sentences carrying that language "
                   "list governance terms rather than create duties.")

    # 3. Position, stated with its calibration so it cannot read as a grade.
    position = (f"Structural position: {overall}/100"
                + (f" ({pct}% of what is achievable without adopting the assessing "
                   f"framework's own vocabulary)" if pct is not None else "")
                + ".")

    # 4. Document-type framing (what this kind of document can and cannot do).
    framing = {
        "voluntary_risk_framework": "It is valuable as a governance design framework, but creates design guidance rather than binding implementation gates.",
        "binding_legal_instrument": "It is a high-force legal source, but local obligation mapping and evidence registers still decide whether it operates.",
        "executive_policy_directive": "As executive direction its force depends on agency implementation tracking and escalation.",
        "sector_assurance_checklist": "As a sector assurance screen its value depends on live review and evidence sufficiency.",
        "public_sector_policy": "As a public-sector operating policy its value depends on registers, disclosure evidence, and human review logs.",
        "implementation_guide": "As implementation guidance it must be converted into owners, artefacts, thresholds, and stop/go consequences.",
        "internal_policy": "As institutional operating policy its assurance depends on implementation records, ownership, and escalation evidence.",
        "procurement_assessment_form": "As a procurement instrument its force arises through contract conditions and acceptance evidence.",
        "vendor_compliance_submission": "As a supplier attestation it is a claim, not evidence: every assertion in it needs independent verification before it enters an assurance record.",
        "values_charter": "As a statement of values it creates no duty, owner, or evidence obligation, so it cannot carry assurance weight until its values are written as operative commitments.",
    }.get(doc_type, "")

    # 4b. Self-contradiction. A document that claims a protection and negates it
    # in its own text cannot be relied on for that protection, whatever else it
    # scores. This outranks the gap register: a gap is something the document
    # omits, a contradiction is something it revokes.
    contradictions = assessment.get("contradictions") or []
    if contradictions:
        subjects = []
        for entry in contradictions:
            subject = (entry[0] if isinstance(entry, (list, tuple)) and entry
                       else str(entry)).replace(" (non-canonical)", "")
            if subject not in subjects:
                subjects.append(subject)
        contradiction_txt = (
            f"Self-contradiction — the document asserts and then negates the same "
            f"protection ({', '.join(subjects[:3])}"
            + (f", and {len(subjects) - 3} more" if len(subjects) > 3 else "")
            + "); resolve this before relying on any part of it, because the "
              "stated protection and the operative text disagree.")
    else:
        contradiction_txt = ""

    # 4c. Vocabulary enumerated rather than made operative. Like a
    # contradiction, this changes what every other finding means: the signals
    # below were fired by a word list, not by duties.
    if assessment.get("vocabulary_enumeration_risk") == "HIGH":
        enumeration_txt = (
            f"Governance vocabulary is listed rather than made operative — "
            f"{int((assessment.get('vocabulary_enumeration_ratio') or 0) * 100)}% of "
            f"substantive sentences name governance machinery without binding any of "
            f"it to an actor or an action, so the signals detected below reflect the "
            f"document's word choice rather than any duty it creates.")
    else:
        enumeration_txt = ""

    # 5. This document's own leading gap and next action.
    if gaps:
        lead = gaps[0]
        where = lead.get("source_evidence_location")
        gap_txt = (f"Leading gap: {lead['gap_title'].lower()}"
                   + (f" (at “{where}”)" if where else "") + ".")
        action = (f"Next action: {controls[0]['control_name'].lower()}."
                  if controls else "")
    else:
        gap_txt = empty_register_meaning(assessment)
        action = ""

    classification = (
        f"Classified as `{doc_type}`."
        if doc_type and doc_type != "unknown_governance_document"
        else ("Document type not confidently classified — the governance-force "
              "reading below is generic; confirm the document's institutional "
              "status before relying on it.")
    )

    # Contradiction precedes the gap and the next action: it changes what the
    # rest of the finding means.
    if not assessment.get("english_language_readable", True):
        return " ".join([
            verdict,
            f"Detected English function-word ratio "
            f"{assessment.get('english_function_word_ratio')}, against 0.15-0.37 for "
            f"English governance drafting.",
            "Assess this document with an instrument built for its language, or with "
            "a certified translation; do not rely on the numbers below.",
        ])

    parts = [verdict, binding, position, framing, classification,
             enumeration_txt, contradiction_txt, gap_txt, action]
    return " ".join(x for x in parts if x)


def native_executive_thesis(assessment: dict, gaps: list[dict], controls: list[dict]) -> str:
    """The finding for a document assessed against LAIF's own formal gate.

    LAIF-native mode asks a different question from external assessment: not
    "does this express the substance in its own vocabulary" but "does this
    satisfy the deterministic certification gate". The finding must therefore
    name the verdict, the checks that decided it, and what that verdict does and
    does not mean — never a fixed sentence that is true of every document.
    """
    formal = assessment.get("formal_laif_compliance", "")
    strong = assessment.get("strong_laif_compliance", "")
    depth = assessment.get("structural_depth", "")
    coupling_quality = assessment.get("coupling_quality", "")
    overall = assessment.get("overall_readiness_score", 0)
    checks = assessment.get("formal_checks_detail", []) or []
    failed = [name for name, ok in checks if not ok]
    passed = [name for name, ok in checks if ok]

    if formal == "PASS" and strong == "STRONG PASS":
        verdict = ("This document satisfies the LAIF-native certification gate, and its "
                   "Coupling is structurally declared rather than referenced.")
    elif formal == "PASS":
        verdict = (f"This document satisfies the formal LAIF-native certification gate, but "
                   f"its structural depth is {depth}: the required elements are present in "
                   f"form, and the substance behind them needs review before the pass is "
                   f"relied on.")
    else:
        verdict = ("This document does not satisfy the LAIF-native certification gate.")

    if failed:
        detail = (f"Failing check{'s' if len(failed) > 1 else ''}: {', '.join(failed)}"
                  + (f" ({len(passed)} of {len(checks)} checks satisfied)." if checks else "."))
    elif checks:
        detail = f"All {len(checks)} certification checks are satisfied."
    else:
        detail = ""

    # Certification is a form test, so say plainly what a failure here is not.
    boundary = ("Certification is a test of LAIF-native form, applied deterministically "
                "by the validation boundary in the technical appendix. Failing it says "
                "nothing about whether the document governs well — a framework text or "
                "a source instrument is expected to fail checks that only an assessment "
                "record can satisfy.")

    coupling_note = {
        "STRUCTURAL": "Coupling is declared structurally, with a named interest and paired force.",
        "SHALLOW": "Coupling is referenced but not structurally declared, so the term is carrying no load.",
        "NEGATED": "Coupling is disclaimed in the document's own terms, which is a Q1 failure.",
        "ABSENT": "Coupling does not appear, so Q1 cannot be evidenced from this text.",
    }.get(coupling_quality, "")

    position = f"Dimensional position: {overall}/100 against the LAIF-native rubrics."

    if gaps:
        lead = gaps[0]
        where = lead.get("source_evidence_location")
        gap_txt = (f"Leading gap: {lead['gap_title'].lower()}"
                   + (f" (at \u201c{where}\u201d)" if where else "") + ".")
        action = f"Next action: {controls[0]['control_name'].lower()}." if controls else ""
    else:
        gap_txt = empty_register_meaning(assessment)
        action = ""

    parts = [verdict, detail, coupling_note, position, boundary, gap_txt, action]
    return " ".join(x for x in parts if x)


def _signal_sets(assessment: dict) -> tuple[dict, dict]:
    """Fired/missed rubric signal labels per dimension, as sets."""
    bd = assessment.get("score_breakdown", {}) or {}
    fired, missed = {}, {}
    for dim, data in bd.items():
        fired[dim] = {lbl for lbl, _ in (data.get("fired") or [])}
        missed[dim] = {lbl for lbl, _ in (data.get("missed") or [])}
    return fired, missed


def _evidence_for_signal(assessment: dict, dimension: str, label: str) -> dict:
    """The document's own quote and location for a fired signal.

    The quote is passed through the same extraction-damage gate as any other
    public quotation: text carrying unresolved split-word damage (a common PDF
    artefact) is withheld and only the location is returned. Evidence is never
    fabricated and never displayed in a damaged form.
    """
    for row in (assessment.get("signal_locations", {}) or {}).get(dimension, []):
        if row.get("label") != label:
            continue
        raw = row.get("quote", "") or ""
        # Same pipeline the runner applies to any public quotation: run the
        # deterministic display repairs first, then withhold anything still
        # carrying unresolved extraction damage.
        repaired, _was_repaired, _repair_reason = normalize_quote_for_display(raw)
        damaged, _damage_reason = unresolved_split_word_damage(repaired)
        return {
            "quote": "" if damaged else repaired,
            "location": row.get("location", ""),
            "quote_withheld": bool(damaged),
        }
    return {}


def _assessment_source_text(assessment: dict, quote_bank: list[dict]) -> str:
    """Reconstruct enough of the source for text-level gap-rule conditions.

    The register is built from the assessment result, which carries located
    signal quotes and the quote bank rather than the whole document. Both are
    verbatim substrings of the source, so their concatenation is a faithful (if
    partial) sample for presence tests — and never introduces text the document
    does not contain.
    """
    parts = []
    for rows in (assessment.get("signal_locations", {}) or {}).values():
        for row in rows:
            parts.append(str(row.get("quote", "")))
    for construct in (assessment.get("functional_alignment", {}) or {}).values():
        parts.extend(str(x) for x in (construct.get("evidence") or []))
    parts.extend(str(q.get("exact_quote", "")) for q in (quote_bank or []))
    # Deliberately excludes strengths and any other rubric label: those carry
    # the detector's own vocabulary ("review / monitoring mechanisms") and would
    # satisfy a presence test the source document does not.
    return "\n".join(parts)


def build_governance_gap_register(assessment: dict, quote_bank: list[dict]) -> list[dict]:
    """Detect gaps the document actually has.

    A gap is emitted only where the document creates an expectation (a fired
    rubric signal) that the corresponding control does not close (a missed
    signal). Each gap carries the quote and location of the signal that created
    the expectation, so the register differs between documents and every entry
    is traceable to the source text.
    """
    scores = {k: assessment.get(k) for k in ("structural_score", "terminology_score", "conceptual_proximity_score", "auditability_score", "enforceability_score", "overall_readiness_score")}
    doc_type = assessment.get("document_type", "unknown_governance_document")
    sector = assessment.get("sector_profile") or assessment.get("sector_used")
    fired, missed = _signal_sets(assessment)
    source_text = _assessment_source_text(assessment, quote_bank)
    fallback_quote_ids = [q["quote_id"] for q in quote_bank[:3]]

    # Operative commitment density — value language is cheap to write; machinery
    # is not. A document that fires value signals but almost no operative ones
    # cannot generate many gaps (a rule needs an expectation to leave unclosed),
    # so a short register would otherwise imply near-completeness. Detect and
    # report that condition explicitly instead.
    _OPERATIVE_DIMS = ("structural", "auditability", "enforceability")
    op_fired = sum(len(fired.get(d, ())) for d in _OPERATIVE_DIMS)
    op_total = op_fired + sum(len(missed.get(d, ())) for d in _OPERATIVE_DIMS)
    op_density = (op_fired / op_total) if op_total else 0.0
    value_fired = len(fired.get("conceptual", ()))

    gaps: list[dict] = []
    if not assessment.get("english_language_readable", True):
        gaps.append({
            "gap_id": "GAP-001",
            "gap_title": "Document is not in a language this assessment can read",
            "severity": "high",
            "gap_type": "language_not_covered",
            "document_type": doc_type,
            "sector_profile": sector,
            "document_profile_key": document_profile_key(assessment),
            "detected_from": {
                "expectation_signal": "governance document submitted for assessment",
                "missing_control_signal": (
                    f"English function-word ratio "
                    f"{assessment.get('english_function_word_ratio')} — the engine's "
                    f"detection patterns are English-only"),
            },
            "source_evidence_quote": "",
            "source_evidence_location": "",
            "source_evidence_quote_ids": fallback_quote_ids,
            "related_scores": scores,
            "related_governance_repair_fields": ["governance_force"],
            "operational_meaning": (assessment.get("language_coverage_note") or ""),
            "failure_mode": ("A near-zero score produced by a language limit is read as "
                             "a finding about the document's governance."),
            "affected_stakeholders": ["assurance reviewers", "the document's owner"],
            "required_control_ids": ["CTRL-001"],
            "control_artifact": ("A certified translation assessed in its place, or an "
                                 "assessment instrument built for this language."),
            "control_trigger": "Before any reliance is placed on this assessment.",
            "control_threshold": ("No score, gap, or verdict from this run is cited for "
                                  "this document."),
            "reviewer_note": ("Discard the scores below. They measure what this engine "
                              "could read, which is nothing."),
        })
        for quote in quote_bank:
            quote["linked_gap_ids"] = [gaps[0]["gap_id"]]
        return gaps
    if assessment.get("vocabulary_enumeration_risk") == "HIGH":
        gaps.append({
            "gap_id": "GAP-001",
            "gap_title": "Governance vocabulary is listed rather than made operative",
            "severity": "high",
            "gap_type": "vocabulary_without_operative_effect",
            "document_type": doc_type,
            "sector_profile": sector,
            "document_profile_key": document_profile_key(assessment),
            "detected_from": {
                "expectation_signal": (
                    f"governance vocabulary present across "
                    f"{sum(len(v) for v in fired.values())} signals"),
                "missing_control_signal": (
                    f"{int((assessment.get('vocabulary_enumeration_ratio') or 0) * 100)}% "
                    f"of substantive sentences bind none of it to an actor or action"),
            },
            "source_evidence_quote": (assessment.get("vocabulary_enumeration_examples") or [""])[0],
            "source_evidence_location": "",
            "source_evidence_quote_ids": fallback_quote_ids,
            "related_scores": scores,
            "related_governance_repair_fields": ["governance_force", "operational_closure"],
            "operational_meaning": (assessment.get("vocabulary_enumeration_reason") or ""),
            "failure_mode": ("Signals fired by governance vocabulary are mistaken for "
                             "governance that operates."),
            "affected_stakeholders": assessment.get("sector_relevant_interests", [])[:3]
                                     or ["affected people", "assurance reviewers"],
            "required_control_ids": ["CTRL-001"],
            "control_artifact": ("A rewrite in operative form: for each named control, "
                                 "who must do it, when, evidenced how, and what happens "
                                 "if they do not."),
            "control_trigger": "Before this document is accepted as assurance for any decision.",
            "control_threshold": ("No signal in this document is treated as assurance until "
                                  "the sentence carrying it binds a named actor to an action."),
            "reviewer_note": ("Ask the author which sentence creates the duty. If none does, "
                              "assess the procedure or standard that is meant to."),
        })
    if op_total and op_density <= 0.15 and value_fired >= 2:
        gaps.append({
            "gap_id": "GAP-001",
            "gap_title": "Declaratory document — states values without operative commitments",
            "severity": "high",
            "gap_type": "declaratory_without_operative_commitment",
            "document_type": doc_type,
            "sector_profile": sector,
            "document_profile_key": document_profile_key(assessment),
            "detected_from": {
                "expectation_signal": f"conceptual: {value_fired} value signal(s) present",
                "missing_control_signal": (f"operative machinery: {op_fired} of {op_total} "
                                           f"structural/auditability/enforceability signals present"),
            },
            "source_evidence_quote": "",
            "source_evidence_location": "",
            "source_evidence_quote_ids": fallback_quote_ids,
            "related_scores": scores,
            "related_governance_repair_fields": ["governance_force", "operational_closure"],
            "operational_meaning": (
                f"The document uses the vocabulary of responsible governance "
                f"({value_fired} value themes detected) but carries almost none of the "
                f"machinery that would make those values operate: only {op_fired} of "
                f"{op_total} structural, auditability, and enforceability signals are "
                f"present. Because it creates few obligations, few specific gaps can be "
                f"detected — the shortness of the register below reflects the document's "
                f"thinness, not its completeness. Relying on it as assurance would mean "
                f"relying on stated intent alone."),
            "failure_mode": "Assurance is inferred from value language that commits the author to nothing testable.",
            "affected_stakeholders": assessment.get("sector_relevant_interests", [])[:3] or ["affected people", "assurance reviewers"],
            "required_control_ids": ["CTRL-001"],
            "control_artifact": "A statement of operative commitments: who must do what, by when, evidenced how, with what consequence for failure.",
            "control_trigger": "Before this document is accepted as assurance for any decision.",
            "control_threshold": "Do not treat this document as assurance evidence until operative commitments exist.",
            "reviewer_note": "Ask the author for the operating procedure, contract schedule, or control record this document refers to; assess that instead.",
        })

    for rule in GAP_RULES:
        if rule.get("sector") and rule["sector"] != sector:
            continue
        p_dim, p_label = rule["present"]
        absent_pairs = rule["absent"]
        # A rule may name one missing control or several. Several means ALL of
        # them must be missing: if the document closes the expectation through
        # any one of the named routes, there is no gap to report.
        if isinstance(absent_pairs[0], str):
            absent_pairs = (absent_pairs,)
        if p_label not in fired.get(p_dim, set()):
            continue
        # A rule may require the source text itself to carry the language its
        # expectation rests on, where the rubric signal is broad enough to fire
        # on the same word used in another sense.
        required_text = rule.get("present_text")
        if required_text and not re.search(required_text, source_text or "", re.IGNORECASE):
            continue
        if any(lbl not in missed.get(dim, set()) for dim, lbl in absent_pairs):
            continue
        a_dim, a_label = absent_pairs[0]

        idx = len(gaps) + 1
        gap_id = f"GAP-{idx:03d}"
        evidence = _evidence_for_signal(assessment, p_dim, p_label)
        # Prefer the quote bank entry matching this gap's evidence, else the
        # engine-located quote, else fall back to the shared bank.
        matched_ids = [q["quote_id"] for q in quote_bank
                       if evidence.get("quote") and
                       q.get("exact_quote", "")[:40] in evidence["quote"]]
        gaps.append({
            "gap_id": gap_id,
            "gap_title": document_specific_gap_title(rule["gap_type"], rule["title"], assessment),
            "severity": rule["severity"],
            "gap_type": rule["gap_type"],
            "document_type": doc_type,
            "sector_profile": sector,
            "document_profile_key": document_profile_key(assessment),
            "detected_from": {
                "expectation_signal": f"{p_dim}: {p_label}",
                "missing_control_signal": "; ".join(f"{dim}: {lbl}" for dim, lbl in absent_pairs),
            },
            "source_evidence_quote": evidence.get("quote", ""),
            "source_evidence_location": evidence.get("location", ""),
            "source_evidence_quote_ids": matched_ids or fallback_quote_ids,
            "related_scores": scores,
            "related_governance_repair_fields": ["operational_closure", "evidence_sufficiency", "governance_force"],
            "operational_meaning": rule["meaning"],
            "failure_mode": rule["title"],
            "affected_stakeholders": assessment.get("sector_relevant_interests", [])[:3] or ["affected people", "operators", "assurance reviewers"],
            "required_control_ids": [f"CTRL-{idx:03d}"],
            "control_artifact": rule["control_artifact"],
            "control_trigger": rule["control_trigger"],
            "control_threshold": rule["control_threshold"],
            "reviewer_note": "Confirm whether implementation artifacts outside this source document already close this gap.",
        })

    # No rule fired. Two very different situations share that outcome, and the
    # reader must be able to tell them apart:
    #   • the document carries the machinery and leaves nothing unclosed, or
    #   • the document is too thin to create expectations in the first place,
    #     so there is nothing for a rule to find unclosed.
    # Silence would read as the former. Detect and state the latter.
    if not gaps:
        overall = assessment.get("overall_readiness_score", 0) or 0
        # Thinness is a property of how much the document commits to, not of
        # its alignment verdict: a document can express every construct in its
        # own vocabulary (PARTIALLY/FUNCTIONALLY ALIGNED) and still be a
        # two-paragraph statement of intent, and a document can be dense with
        # operative machinery yet decline LAIF's vocabulary entirely. Only
        # operative-signal density and structural position can tell them apart.
        thin = (op_total == 0) or op_density < 0.5 or overall < 40
        if thin:
            gaps.append({
                "gap_id": "GAP-001",
                "gap_title": "Insufficient operative content to assess control closure",
                "severity": "high",
                "gap_type": "insufficient_operative_content",
                "document_type": doc_type,
                "sector_profile": sector,
                "document_profile_key": document_profile_key(assessment),
                "detected_from": {
                    "expectation_signal": f"operative machinery: {op_fired} of {op_total} signals present",
                    "missing_control_signal": "no rule could fire because no closable expectation was detected",
                },
                "source_evidence_quote": "",
                "source_evidence_location": "",
                "source_evidence_quote_ids": fallback_quote_ids,
                "related_scores": scores,
                "related_governance_repair_fields": ["governance_force", "operational_closure"],
                "operational_meaning": (
                    f"The assessed text creates too few operative expectations for gap "
                    f"detection to be meaningful: only {op_fired} of {op_total} "
                    f"structural, auditability, and enforceability signals are present, "
                    f"and structural position is {overall}/100. An empty gap register "
                    f"here means the document does not commit to enough to be tested — "
                    f"not that its controls are complete. If this is an extract, assess "
                    f"the full instrument; if it is the whole document, it cannot carry "
                    f"assurance weight on its own."),
                "failure_mode": "An absent finding is mistaken for a clean finding.",
                "affected_stakeholders": assessment.get("sector_relevant_interests", [])[:3] or ["affected people", "assurance reviewers"],
                "required_control_ids": ["CTRL-001"],
                "control_artifact": "The operative instrument this document refers to — procedure, contract schedule, standard, or register — assessed in its place.",
                "control_trigger": "Before this document is relied on as assurance for any decision.",
                "control_threshold": "Do not record this document as assurance evidence until an operative instrument is assessed.",
                "reviewer_note": "Confirm whether a fuller version or a downstream operating procedure exists; assess that instead.",
            })

    for quote in quote_bank:
        quote["linked_gap_ids"] = [gap["gap_id"] for gap in gaps if quote["quote_id"] in gap["source_evidence_quote_ids"]]
    return gaps


def build_failure_pathways(gaps: list[dict], quote_bank: list[dict]) -> list[dict]:
    """One pathway per detected gap, written from that gap's own evidence.

    Steps name the expectation the document actually creates, the control it
    actually lacks, and the consequence specific to that combination — so two
    pathways are never interchangeable.
    """
    pathways: list[dict] = []
    for idx, gap in enumerate(gaps[:5], 1):
        ctrl = gap.get("required_control_ids", [f"CTRL-{idx:03d}"])[0]
        quote = (gap.get("source_evidence_quote") or "").strip()
        where = gap.get("source_evidence_location") or "the document"
        signal = (gap.get("detected_from", {}) or {}).get("expectation_signal", "")
        signal_name = signal.split(":", 1)[-1].strip() if ":" in signal else signal.strip()
        expectation = (
            f"The document raises **{signal_name}** at “{where}”" if signal_name
            else f"The document creates an expectation at “{where}”")
        expectation += f": “{quote}”" if quote else "."
        pathways.append({
            "pathway_id": f"PATH-{idx:03d}",
            "title": f"{gap['gap_title']} — failure pathway",
            "severity": gap.get("severity", "medium"),
            "steps": [
                expectation,
                gap.get("operational_meaning", ""),
                (f"The institution cites this expectation as assurance, but the "
                 f"closing control — {gap.get('control_artifact', 'a documented control')[0].lower()}"
                 f"{gap.get('control_artifact', 'a documented control')[1:].rstrip('.')} — "
                 f"does not exist or is not current."),
                "A decision or deployment proceeds on the strength of the document alone.",
                "If the outcome is wrong, there is no record that this expectation controlled the decision, and no defined route to correct it.",
            ],
            "source_evidence_quote": quote,
            "source_evidence_location": where,
            "source_evidence_quote_ids": gap.get("source_evidence_quote_ids", []),
            "triggering_gap_ids": [gap["gap_id"]],
            "likely_institutional_failure": gap.get("failure_mode", "Paper compliance without live operational control."),
            "consequence": f"Reliance on {gap.get('gap_title', 'this expectation').lower()} cannot be evidenced after the fact.",
            "required_controls": [ctrl],
            "detection_signal": f"Absence or staleness of: {gap.get('control_artifact', 'the closing control')}",
            "escalation_gate": gap.get("control_threshold", "Pause reliance until the required artifact and accountable owner are confirmed."),
        })
    return pathways


_CONTROL_OWNER_BY_GAP = {
    "obligation_without_owner": "The role named in the accountability register for this duty (create the register if none exists).",
    "evidence_presence_without_sufficiency": "The assurance reviewer who accepts or rejects evidence submitted under this document.",
    "monitoring_without_threshold": "The operational owner of the monitored system, with escalation to the accountable executive.",
    "policy_without_enforcement_consequence": "The policy owner, jointly with whoever can suspend use of the system.",
    "risk_without_closure_gate": "The authority empowered to withhold deployment approval.",
    "incident_reporting_without_redress": "The complaints or appeals owner, with authority to reverse a decision.",
    "lifecycle_without_change_control": "The change-control authority for the system, typically its technical design authority.",
    "safety_case_without_live_review": "The named Clinical Safety Officer.",
    "vocabulary_without_operative_effect": "The document's author, with the accountable owner who would have to discharge the duties it names.",
    "supplier_duty_without_deployer_acceptance": "The contract or procurement owner accepting the supplier assurance.",
}


def _control_owner_for_gap(gap: dict) -> str:
    return _CONTROL_OWNER_BY_GAP.get(
        gap.get("gap_type", ""),
        "Named accountable owner for the controlled decision pathway.")


def build_control_recommendations(gaps: list[dict], pathways: list[dict], quote_bank: list[dict]) -> list[dict]:
    controls: list[dict] = []
    path_by_gap = {gap_id: p["pathway_id"] for p in pathways for gap_id in p.get("triggering_gap_ids", [])}
    for idx, gap in enumerate(gaps, 1):
        control_id = gap.get("required_control_ids", [f"CTRL-{idx:03d}"])[0]
        controls.append({
            "control_id": control_id,
            "control_name": control_name_for_gap(gap),
            "priority": "immediate" if gap.get("severity") == "high" else "near_term",
            "risk_addressed": gap.get("failure_mode"),
            "source_evidence_quote_ids": gap.get("source_evidence_quote_ids", []),
            "linked_gap_ids": [gap["gap_id"]],
            "linked_failure_pathways": [path_by_gap.get(gap["gap_id"])] if path_by_gap.get(gap["gap_id"]) else [],
            "owner": _control_owner_for_gap(gap),
            "required_artifact": gap.get("control_artifact", "Signed control record linking source requirement, local procedure, evidence file, threshold, reviewer, and decision outcome."),
            "minimum_evidence": "Current owner sign-off, implementation artifact, threshold log, review cadence record, and exception/escalation register.",
            "implementation_steps": [
                (f"Locate the expectation this closes: {gap.get('source_evidence_location') or 'see linked evidence'}"
                 + (f" — “{gap.get('source_evidence_quote')}”" if gap.get("source_evidence_quote") else "")),
                f"Create the artefact: {gap.get('control_artifact', 'a signed control record')}",
                f"Set the trigger: {gap.get('control_trigger', 'deployment or material change')}",
                f"Set the stop condition: {gap.get('control_threshold', 'no reliance without current evidence')}",
                "Assign a named owner and an independent reviewer, and record outcomes in an auditable register.",
            ],
            "trigger": gap.get("control_trigger", "New deployment, material change, incident, or scheduled assurance review."),
            "threshold": gap.get("control_threshold", "No continued reliance when required evidence is absent, stale, or unapproved."),
            "cadence": "Before deployment, after material change, after incident, and at least quarterly while in operational use.",
            "decision_consequence": "Proceed only with complete evidence; otherwise pause, remediate, escalate, or reject supplier/system use.",
            "residual_risk_if_not_implemented": "The institution may rely on governance language that does not control real-world decisions or harms.",
            "suggested_template_row": f"{control_id} | owner | artifact | trigger | threshold | cadence | decision consequence | quote IDs {', '.join(gap.get('source_evidence_quote_ids', []))}",
        })
    return controls


# Document-level signal detection saturates: past a certain length every
# operative signal fires somewhere in the text, so no gap rule can fire. That
# is a limit of the method, and stating it is the difference between a clean
# finding and an unearned one.
SATURATION_LENGTH_CHARS = 20000


def empty_register_meaning(assessment: dict) -> str:
    """What an empty gap register means for THIS document."""
    # Gap rules test whether a signal is present ANYWHERE in the document. In a
    # short instrument that is a fair proxy for whether the expectation is
    # closed. In a long one it is not: a control in section 40 does not close an
    # obligation in section 3, but both fire the same document-level signals. An
    # empty register on a long document therefore means the method stopped
    # discriminating, not that the document is complete.
    length = assessment.get("assessed_character_count") or 0
    if length >= SATURATION_LENGTH_CHARS:
        return (
            "No unclosed expectation was detected — but this document is long enough "
            "that every operative signal is present somewhere in it, which is the "
            "point at which document-level gap detection stops discriminating. It "
            "cannot show whether the control that appears in one section governs the "
            "obligation stated in another. For an instrument of this size, assess it "
            "section by section rather than reading an empty register as a clean one.")
    return (
        "No unclosed expectation was detected: every governance expectation this "
        "document creates has a corresponding control in the same document. This "
        "is a finding about the text, not a certificate of implementation — the "
        "controls still have to exist and operate in practice.")


def _residual_risk_clause(gaps: list[dict]) -> str:
    """Name what is actually unclosed in THIS document."""
    unclosed = []
    for gap in gaps[:4]:
        title = (gap.get("gap_title") or "").strip().rstrip(".")
        if title:
            unclosed.append(title[0].lower() + title[1:])
    if not unclosed:
        return "expectations it creates remain unclosed."
    if len(unclosed) == 1:
        return f"{unclosed[0]}."
    return "; ".join(unclosed[:-1]) + f"; and {unclosed[-1]}."


def _md_list(items: list[str], empty: str = "Reviewer confirmation required.") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {empty}"


def build_institutional_report(processing: dict, extraction: dict, assessment: dict, quote_bank: list[dict], gaps: list[dict], pathways: list[dict], controls: list[dict], verification_required_evidence: list[dict] | None = None, extraction_quality_profile: dict | None = None) -> str:
    mode = assessment.get("assessment_mode")
    doc_type = assessment.get("document_type", "unknown_governance_document")
    force = assessment.get("governance_force_profile") or assessment.get("governance_force_summary") or "source governance force requires reviewer confirmation"
    lines = [
        f"# Institutional Governance Assessment — {processing.get('original_file_name')}", "",
        "*For: the governance, assurance, procurement, or clinical owner deciding "
        "whether this document can be relied on. Read this file first; the "
        "technical appendix carries scoring detail and evidence traces, and the "
        "full assessment report carries located evidence and placement guidance. "
        "This is a diagnostic of the document as written — not a legal "
        "determination, and not proof of what an organisation actually does.*", "",
        "## Executive finding", "",
    ]
    if mode == "external_framework":
        lines.append(executive_thesis(assessment, gaps, controls))
    else:
        lines.append(native_executive_thesis(assessment, gaps, controls))
    if not assessment.get("english_language_readable", True):
        lines += ["", "## Language coverage limit", "",
                  f"- {assessment.get('language_coverage_note')}",
                  "- Every score, verdict, and gap in this report is an artefact of that "
                  "limit. None of it is a finding about the document."]
    lines += ["", "## Document identity and document type", "", f"- **Original file:** {processing.get('original_file_name')}", f"- **Document type:** {doc_type}", f"- **Assessment mode:** {mode}", f"- **Sector profile:** {assessment.get('sector_profile_label', assessment.get('sector_profile'))}"
        + (f" (auto-detected from: {processing.get('sector_basis')}; override with --sector)"
           if processing.get("sector_basis") else ""), f"- **Source SHA-256:** {processing.get('source_sha256')}", "", "## Recommended use / not sufficient for", "", f"- **Recommended use:** {assessment.get('recommended_use') or 'source framework review, procurement/legal/clinical/public-sector assurance scoping, control mapping, and remediation planning.'}", f"- **Limits:** {assessment.get('not_sufficient_for') or 'standalone proof of implementation, legal validity, external certification, supplier acceptance, clinical safety approval, or LAIF-native certification unless separately evidenced.'}", "- **In every case:** this is a reading of the document, not of the organisation. It cannot show whether the controls it describes are in place, current, or working.", "", "## Governance force profile", "", f"- {force if isinstance(force, str) else json.dumps(force, sort_keys=True)}", "- The document creates a strong evidence request where it uses risk, oversight, evidence, review, incident, or accountability language, but the reviewer must test whether that request is operationally closed.", "", "## Key quoted evidence", ""]
    primary_quote_eligible = True if extraction_quality_profile is None else bool(extraction_quality_profile.get("primary_quote_eligible"))
    primary_quotes = _gate_passing_primary_quotes(quote_bank) if primary_quote_eligible else []
    if primary_quote_eligible:
        for q in primary_quotes[:6]:
            quote_text = q.get("display_quote") or q["exact_quote"]
            lines.append(f"- **{q['quote_id']} — {q['signal_category']}:** “{quote_text}”")
    verification_required_evidence = verification_required_evidence or []
    if not primary_quotes:
        if not primary_quote_eligible:
            lines.append("- No high-confidence complete primary quotes are presented because source text extraction quality is limited or poor. Evidence-bearing extracted passages are retained below as source-verification-required evidence and in the analyst bundle.")
        elif verification_required_evidence:
            lines.append("- No high-confidence complete primary quotes were extracted. Evidence-bearing extracted passages are retained below as source-verification-required evidence and in the analyst bundle.")
        else:
            lines.append("- No high-confidence complete primary quotes were extracted; use the technical appendix and source text review before relying on quote-grade evidence.")
    lines += ["", "## Extracted evidence requiring source verification", ""]
    if verification_required_evidence:
        for evidence in verification_required_evidence[:6]:
            text = evidence.get("display_quote") or evidence.get("exact_quote") or ""
            lines += [
                f"- **{evidence.get('evidence_id')} — Source verification required:**",
                f"  - Extracted text: “{text}”",
                f"  - Issue: {evidence.get('extraction_issue_reason')}",
                f"  - Likely governance signal: {evidence.get('likely_governance_signal')}",
                f"  - Reviewer instruction: {evidence.get('reviewer_instruction')}",
            ]
    else:
        lines.append("- No extraction-impaired governance evidence required source-verification tiering.")
    if extraction_quality_profile and extraction_quality_profile.get("source_text_reliability_warning"):
        lines += ["", f"**Extraction quality note:** {extraction_quality_profile.get('source_text_reliability_warning')}"]
    if assessment.get("vocabulary_enumeration_risk") == "HIGH":
        lines += ["", "## Governance vocabulary without operative effect", "",
                  (assessment.get("vocabulary_enumeration_reason") or ""),
                  "",
                  ("The sentences below name governance machinery without binding it "
                   "to anyone. Read every other finding in this report in that light: "
                   "signals fired by these sentences record what the document says "
                   "about governance, not what it requires of anyone."), ""]
        for example in assessment.get("vocabulary_enumeration_examples", []):
            repaired, _was, _why = normalize_quote_for_display(example)
            damaged, _reason = unresolved_split_word_damage(repaired)
            if not damaged:
                lines.append(f"- \u201c{repaired.strip()}\u201d")
        lines.append("")
    contradictions = assessment.get("contradictions") or []
    if contradictions:
        lines += ["", "## Self-contradictions in the document", "",
                  ("Each entry below is a protection the document states and then "
                   "negates elsewhere in its own text. Until these are resolved the "
                   "document cannot be relied on for the protection it names — this "
                   "is a defect in the drafting, not a missing control."), ""]
        for idx, entry in enumerate(contradictions, 1):
            subject = entry[0] if isinstance(entry, (list, tuple)) and entry else str(entry)
            description = entry[1] if isinstance(entry, (list, tuple)) and len(entry) > 1 else ""
            context = entry[2] if isinstance(entry, (list, tuple)) and len(entry) > 2 else ""
            repaired, _was, _why = normalize_quote_for_display(context)
            damaged, _reason = unresolved_split_word_damage(repaired)
            lines.append(f"- **CONTRA-{idx:03d} — {subject}:** {description}."
                         + (f" Text: \u201c{repaired.strip()}\u201d" if context and not damaged
                            else " Source text withheld: extraction damage; verify in the source."))
        lines.append("")
    lines += ["", "## What the document controls well", "", _md_list(assessment.get("strengths", [])[:8], "No deterministic strengths detected."), "", "## What the document does not control", ""]
    lines.append(_md_list(
        [g["gap_title"] + f" ({g['gap_id']})" for g in gaps[:8]],
        empty_register_meaning(assessment)))
    lines += ["", "## Hidden failure pathways", ""]
    lines += ([("Failure pathway summaries below show how paperwork compliance can "
                "proceed without live operational control.")] if pathways else
              [("No failure pathway was traced: no expectation in this document was "
                "left without a closing control, so there is no paperwork-compliance "
                "route to trace from the text itself. Operational failure remains "
                "possible through non-implementation, which this assessment cannot see.")])
    lines += [""]
    for pth in pathways:
        lines.append(f"### {pth['pathway_id']} — {pth['title']}")
        lines.append("")
        lines.append(_md_list(pth.get("steps", [])))
        lines.append(f"- **Escalation gate:** {pth.get('escalation_gate')}")
        lines.append("")
    lines += ["## Operational gap analysis", ""]
    if gaps:
        for gap in gaps:
            lines.append(f"- **{gap['gap_id']} ({gap['severity']}):** {gap['operational_meaning']} Evidence: {', '.join(gap.get('source_evidence_quote_ids', [])) or 'review required'}.")
    else:
        lines.append("- No operational gap was detected in the assessed text. Assurance "
                     "review should now move from the document to its implementation "
                     "record: the artefacts, owners, and decision logs the document names.")
    lines += ["", "## Priority remediation roadmap", ""]
    if controls:
        for ctrl in controls[:8]:
            lines.append(f"- **{ctrl['priority']} — {ctrl['control_id']}:** {ctrl['control_name']}; owner: {ctrl['owner']}; artifact: {ctrl['required_artifact']}")
    else:
        lines.append("- No remediation is required to the document. Verify that the "
                     "controls it already specifies are in place, current, and "
                     "evidenced.")
    lines += ["", "## Control implementation templates", ""]
    if controls:
        lines += ["| Control ID | Owner | Required artifact | Trigger | Threshold | Cadence | Decision consequence |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for ctrl in controls[:8]:
            lines.append(f"| {ctrl['control_id']} | {ctrl['owner']} | {ctrl['required_artifact']} | {ctrl['trigger']} | {ctrl['threshold']} | {ctrl['cadence']} | {ctrl['decision_consequence']} |")
    else:
        lines.append("- No control template is issued: the document specifies its own "
                     "controls, triggers, and thresholds. Use those as the implementation "
                     "baseline rather than substituting generic ones.")
    lines += ["", "## Residual risk if no action is taken", ""]
    lines += ([("The failure pathway is paperwork compliance without live operational "
                "control. Specifically, this document can be cited as assurance while "
                + _residual_risk_clause(gaps) + " Until those controls exist and are "
                "current, a decision made on the strength of this document is not "
                "governed by it.")] if gaps else
              [("The residual risk is no longer in the drafting. It is in the gap between "
                "what this document requires and what is actually done: unevidenced "
                "controls, lapsed reviews, and unrecorded exceptions. That gap is invisible "
                "to a document assessment and must be tested against implementation records.")])
    lines += ["", "## Technical appendix pointer", "", f"See `{processing.get('safe_output_stem')}.technical_appendix.md` for processing metadata, source identity, scoring table, evidence traces, remediation patches, construct coverage on both the LAIF-native-form and functional-substance axes, and the certification boundary.", ""]
    return "\n".join(lines)


def build_technical_appendix(processing: dict, extraction: dict, assessment: dict, quote_bank: list[dict], gaps: list[dict], pathways: list[dict], controls: list[dict], low_confidence_quote_candidates: list[dict] | None = None, verification_required_evidence: list[dict] | None = None, extraction_quality_profile: dict | None = None) -> str:
    scores = ["structural_score", "terminology_score", "conceptual_proximity_score", "auditability_score", "enforceability_score", "overall_readiness_score"]
    lines = [f"# Technical Appendix — {processing.get('original_file_name')}", "", "## Document metadata", ""]
    for key in ("original_file_name", "source_sha256", "safe_output_stem"):
        lines.append(f"- **{key}:** {processing.get(key)}")
    lines += ["", "## Processing metadata", ""]
    for key in ("processed_at_utc", "input_path_original", "original_pending_path", "stored_source_path", "runner_input_path", "markdown_output_path", "json_output_path"):
        lines.append(f"- **{key}:** {processing.get(key)}")
    lines += ["", "## Extraction metadata", ""]
    for key in ("extractor_requested", "extractor_used", "extraction_confidence", "extracted_characters", "warning_count", "warnings", "error_count", "errors", "network_access_used"):
        lines.append(f"- **{key}:** {extraction.get(key)}")
    lines += ["", "## Scoring table", "", "| Score | Value |", "| --- | --- |"]
    for key in scores:
        lines.append(f"| {key} | {assessment.get(key)} |")
    lines += ["", "## Governance repair fields", "", "```json", json.dumps({k: assessment.get(k) for k in assessment if k.startswith('governance_') or k in ('document_type','assessment_mode')}, indent=2, sort_keys=True), "```", "", "## Evidence traces", "", "```json", json.dumps(assessment.get("evidence_traces", []), indent=2, sort_keys=True), "```", "", "## Remediation patches", "", "```json", json.dumps(assessment.get("remediation_patches", []), indent=2, sort_keys=True), "```", "", "## Construct coverage — form and substance", "",
        ("Two independent readings of the same constructs. **LAIF-native form** asks "
         "whether the document uses LAIF's canonical term; every external instrument "
         "is expected to answer no, and that answer says nothing about its governance. "
         "**Functional alignment** asks whether the substance is expressed in the "
         "document's own vocabulary. Reading the first column alone will contradict "
         "this report's findings."), "",
        "| Construct | LAIF-native form | Functional alignment |",
        "| --- | --- | --- |"]
    _coverage = assessment.get("construct_coverage", {}) or {}
    _functional = assessment.get("functional_alignment", {}) or {}
    _substance_of = {"Structural Transparency": "Integrity Layer",
                     "Structural Honesty": "Integrity Layer",
                     "Structural Containment": "Integrity Layer"}
    for _construct in sorted(set(_coverage) | set(_functional)):
        _form = "present" if _coverage.get(_construct) else "absent"
        _key = _substance_of.get(_construct, _construct)
        _verdict = (_functional.get(_key) or {}).get("verdict")
        if _verdict is None:
            _sub = "— (not a functional construct; see Integrity Layer)" if _construct in _substance_of else "—"
        else:
            _sub = _verdict + (f" (via {_key})" if _key != _construct else "")
        lines.append(f"| {_construct} | {_form} | {_sub} |")
    lines += ["", "```json", json.dumps(_coverage, indent=2, sort_keys=True), "```", "", "## Formal LAIF-native certification boundary", ""]
    if assessment.get("assessment_mode") == "external_framework":
        lines.append("Formal LAIF-native certification: Not claimed / not applicable to this external-framework assessment. Construct coverage is internal diagnostic data only.")
    else:
        lines.append(f"Formal LAIF-native certification: {assessment.get('formal_laif_native_compliance', assessment.get('formal_laif_compliance'))}")
    normalized_quote_ids = [q.get("quote_id") for q in quote_bank if q.get("quote_display_normalized")]
    lines += ["", "## Quote display traceability", ""]
    if normalized_quote_ids:
        lines.append("Display quote deterministically normalised from exact extracted substring; raw exact quote retained in analyst bundle.")
        lines.append(f"- Display-normalised quote IDs: {', '.join(normalized_quote_ids)}")
    else:
        lines.append("No primary quote display normalization was required; display quotes match exact extracted substrings.")
    lines += ["", "## Extraction quality profile", "", "```json", json.dumps(extraction_quality_profile or {}, indent=2, sort_keys=True), "```", "", "## Verification-required extracted evidence", "", "```json", json.dumps(verification_required_evidence or [], indent=2, sort_keys=True), "```", "", "## Low-confidence extraction/noise findings", "", f"- Low-confidence extraction noise: {assessment.get('low_confidence_extraction_noise', {})}", f"- Runner warnings: {extraction.get('warnings', [])}", "", "## Low-confidence quote candidates", "", "```json", json.dumps(low_confidence_quote_candidates or [], indent=2, sort_keys=True), "```", "", "## Warnings/errors", "", f"- Warnings: {extraction.get('warnings', [])}", f"- Errors: {extraction.get('errors', [])}", ""]
    return "\n".join(lines)


def build_ai_prompt() -> str:
    return """# AI Analyst Prompt

Use only the provided deterministic analyst bundle, high-quality `quote_bank`, diagnostics, and source excerpts. Do not invent quotes, obligations, legal claims, scores, documents, actors, controls, certifications, or legal-validity conclusions.

## Required analyst approach

- Lead with a document-specific thesis that names the document type, governance force, strongest control area, principal operational gap, and next action.
- Treat primary quote evidence as clean quote-grade evidence: use only `primary_quote_evidence` records in the cleaned `quote_bank`, and only when `extraction_quality_profile.primary_quote_eligible` is true.
- If `extraction_quality_profile.primary_quote_eligible` is false, do not use `quote_bank` as clean primary evidence; rely on document diagnostics and discuss extraction-impaired passages only as verification-required evidence.
- Use `display_quote` for prose quotations from `quote_bank` in the executive narrative, and cite the quote ID. Preserve `exact_quote` as the audit trace to the extracted source substring.
- Treat `verification_required_extracted_evidence` as evidence-bearing but extraction-impaired and reviewer-useful; it has passed relevance filtering but still requires source verification.
- Do not present verification-required extracted text as a clean direct quotation.
- Do not invent or silently repair source text.
- When using verification-required evidence, state that source verification or cleaner extraction is required.
- Distinguish source-backed findings from quote-grade evidence; a finding may be supported by source document profile and extracted evidence patterns even when no clean primary quotation is available.
- Treat `low_confidence_quote_candidates` as low-confidence trace only; do not use it as evidence unless it is manually reviewed against the source.
- Do not cite incomplete fragments, heading-only quotes, boilerplate, or extraction-damaged fragments as clean quotation.
- If available primary quotes are weak, state that quote-grade evidence is insufficient and request source review or better extraction while retaining verification-required evidence.
- Use a document-specific thesis, not generic LAIF language.
- Do not invent missing source context to rescue weak quotes.
- Distinguish “source says X” from “institution has implemented X.”
- Convert generic controls into client-ready implementation actions with owner, artifact, threshold, cadence, and decision consequence.
- Explain failure pathways in plain institutional terms: what breaks, who owns it, what evidence is missing, and what decision should stop.
- Distinguish legal force from operational force. A legal or policy source may be authoritative while still lacking local implementation evidence.
- Distinguish evidence presence from evidence sufficiency. A requested document, record, or quote is not proof that evidence is current, complete, reviewed, or accepted.
- Include an executive version and a technical appendix.
- Do not treat LAIF-native failure as the headline for external-framework documents.
- Preserve all source references and quote IDs. For each major recommendation, link to quote IDs, gap IDs, and control IDs.
- If evidence is insufficient, say so. Do not claim legal validity/invalidity. Do not claim certification unless provided by deterministic LAIF data.
"""


def build_validation_rules() -> str:
    return """# AI Report Validation Rules\n\n- Every quote must exist in `quote_bank`.\n- Every recommendation must map to a gap/control ID.\n- No invented legal obligations.\n- No invented citation.\n- No unsupported certification or legal-validity claim.\n- Required sections must be present.\n- Technical appendix must be preserved.\n- Low-confidence evidence must not be used as primary support.\n"""


def write_institutional_outputs(output_dir: Path, processing: dict, extraction: dict, assessment: dict, extracted_text: str) -> dict:
    low_confidence_quote_candidates = build_low_confidence_quote_candidates(extracted_text, processing, extraction, assessment)
    quote_bank = build_quote_bank(extracted_text, processing, extraction, assessment, low_confidence_quote_candidates)
    quote_bank = _finalize_primary_quote_bank(quote_bank, low_confidence_quote_candidates)
    verification_required_evidence = build_verification_required_evidence(
        low_confidence_quote_candidates, processing, extraction,
        admitted_quotes=_gate_passing_primary_quotes(quote_bank))
    extraction_quality_profile = build_extraction_quality_profile(extracted_text, extraction, quote_bank, verification_required_evidence, low_confidence_quote_candidates)
    gaps = build_governance_gap_register(assessment, quote_bank)
    pathways = build_failure_pathways(gaps, quote_bank)
    controls = build_control_recommendations(gaps, pathways, quote_bank)
    primary_quote_eligible = bool(extraction_quality_profile.get("primary_quote_eligible"))
    bundle = {
        "document_metadata": {"original_file_name": processing.get("original_file_name"), "source_sha256": processing.get("source_sha256"), "document_type": assessment.get("document_type"), "sector_profile": assessment.get("sector_profile")},
        "processing_metadata": processing,
        "extraction_metadata": extraction,
        "governance_repair_fields": {k: assessment.get(k) for k in assessment if k.startswith("governance_")},
        "scores": {k: assessment.get(k) for k in ("structural_score", "terminology_score", "conceptual_proximity_score", "auditability_score", "enforceability_score", "overall_readiness_score")},
        "quote_bank": quote_bank,
        "verification_required_extracted_evidence": verification_required_evidence,
        "extraction_quality_profile": extraction_quality_profile,
        "primary_quote_eligible": primary_quote_eligible,
        "evidence_tiering_policy": {
            "tier_1": "primary_quote_evidence",
            "tier_2": "verification_required_extracted_evidence",
            "tier_3": "low_confidence_extraction_trace",
        },
        "gap_register": gaps,
        "failure_pathways": pathways,
        "control_recommendations": controls,
        "extraction_warnings": extraction.get("warnings", []),
        "low_confidence_evidence_flags": [q for q in quote_bank if q.get("low_confidence_reason")],
        "low_confidence_quote_candidates": low_confidence_quote_candidates,
        "technical_appendix_data": {"construct_coverage": assessment.get("construct_coverage", {}), "formal_laif_native_compliance": assessment.get("formal_laif_native_compliance", assessment.get("formal_laif_compliance")), "evidence_traces": assessment.get("evidence_traces", []), "remediation_patches": assessment.get("remediation_patches", [])},
    }
    stem = processing["safe_output_stem"]
    # Namespaced by document. Every markdown and JSON output already carries the
    # document stem; the analyst directory did not, so processing several
    # documents into one --output-dir silently replaced each earlier document's
    # gap register, control recommendations, failure pathways and quote bank
    # with the last one's, leaving JSON that did not correspond to the report
    # beside it. The batch runner was unaffected (it gives each document its own
    # directory); a reviewer running the single-document runner repeatedly was
    # not.
    analyst_dir = output_dir / "analyst" / stem
    analyst_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{stem}.institutional_report.md").write_text(build_institutional_report(processing, extraction, assessment, quote_bank, gaps, pathways, controls, verification_required_evidence, extraction_quality_profile), encoding="utf-8")
    (output_dir / f"{stem}.technical_appendix.md").write_text(build_technical_appendix(processing, extraction, assessment, quote_bank, gaps, pathways, controls, low_confidence_quote_candidates, verification_required_evidence, extraction_quality_profile), encoding="utf-8")
    json_dump(analyst_dir / "analyst_bundle.json", bundle)
    with (analyst_dir / "quote_bank.jsonl").open("w", encoding="utf-8") as handle:
        for quote in quote_bank:
            handle.write(json.dumps(quote, sort_keys=True) + "\n")
    quote_md = ["# Quote Bank", "", "Primary quote evidence only. Verification-required extracted evidence is listed separately and must not be treated as clean direct quotation.", ""]
    if not primary_quote_eligible:
        quote_md += [
            "Primary quote evidence is unavailable or limited because the extraction quality profile marks `primary_quote_eligible` as false.",
            "Use `verification_required_evidence.md` for evidence-bearing extracted passages that require source verification before clean quotation use.",
            "",
        ]
    for q in (_gate_passing_primary_quotes(quote_bank) if primary_quote_eligible else []):
        display_quote = q.get("display_quote") or q["exact_quote"]
        quote_md += [
            f"## {q['quote_id']} — {q['signal_category']}",
            "",
            f"- **Signal category:** {q['signal_category']}",
            f"- **Quality score:** {q.get('quote_quality_score')} — {q.get('quote_quality_reason')}",
            "",
            "- **Display quote:**",
            f"> {display_quote}",
            "",
        ]
        if display_quote != q["exact_quote"]:
            quote_md += [
                "- **Trace/audit note:** display quote deterministically normalised from exact extracted substring; raw exact quote retained below and in the analyst bundle.",
                f"  - Raw exact quote: {q['exact_quote']}",
                f"  - Normalization reason: {q.get('quote_display_normalization_reason')}",
                "",
            ]
        quote_md += [f"- **Why it matters:** {q['why_it_matters']}", f"- **What it does not prove:** {q['what_it_does_not_prove']}", ""]
    if verification_required_evidence:
        quote_md += ["", "# Extracted evidence requiring source verification", ""]
        for evidence in verification_required_evidence:
            quote_md += [
                f"## {evidence['evidence_id']} — Source verification required",
                "",
                f"- **Status:** {evidence['evidence_status']}",
                f"- **Issue:** {evidence['extraction_issue_reason']}",
                f"- **Likely governance signal:** {evidence['likely_governance_signal']}",
                "",
                f"- **Extracted text:** {evidence.get('display_quote') or evidence.get('exact_quote')}",
                "",
                f"- **Reviewer instruction:** {evidence['reviewer_instruction']}",
                "",
            ]
    (analyst_dir / "quote_bank.md").write_text("\n".join(quote_md), encoding="utf-8")
    verification_md = ["# Verification-Required Extracted Evidence", ""]
    if verification_required_evidence:
        for evidence in verification_required_evidence:
            verification_md += [
                f"## {evidence['evidence_id']} — Source verification required",
                "",
                f"- **Exact quote retained:** {evidence['exact_quote']}",
                f"- **Display quote:** {evidence.get('display_quote')}",
                f"- **Issue:** {evidence['extraction_issue_reason']}",
                f"- **Likely governance signal:** {evidence['likely_governance_signal']}",
                f"- **Reviewer instruction:** {evidence['reviewer_instruction']}",
                "",
            ]
    else:
        verification_md.append("No verification-required extracted evidence records were generated.")
    (analyst_dir / "verification_required_evidence.md").write_text("\n".join(verification_md), encoding="utf-8")
    json_dump(analyst_dir / "governance_gap_register.json", {"gaps": gaps})
    json_dump(analyst_dir / "failure_pathways.json", {"failure_pathways": pathways})
    json_dump(analyst_dir / "control_recommendations.json", {"control_recommendations": controls})
    ai_bundle = dict(bundle)
    if not primary_quote_eligible:
        ai_bundle["primary_quote_policy_note"] = "Primary quote evidence is ineligible for AI clean-primary use because extraction_quality_profile.primary_quote_eligible is false; use verification_required_extracted_evidence only with source-verification caveats."
    (analyst_dir / "AI_ANALYST_PROMPT.md").write_text(build_ai_prompt(), encoding="utf-8")
    json_dump(analyst_dir / "AI_ANALYST_INPUT_BUNDLE.json", ai_bundle)
    (analyst_dir / "AI_REPORT_VALIDATION_RULES.md").write_text(build_validation_rules(), encoding="utf-8")
    return {"quote_bank": quote_bank, "verification_required_extracted_evidence": verification_required_evidence, "extraction_quality_profile": extraction_quality_profile, "gap_register": gaps, "failure_pathways": pathways, "control_recommendations": controls, "analyst_bundle": bundle, "low_confidence_quote_candidates": low_confidence_quote_candidates}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract a local document and run the LAIF assessment report wrapper.")
    parser.add_argument("input_file", type=Path, help="Local input document path")
    parser.add_argument("--mode", choices=ASSESSMENT_MODES, default="external_framework")
    parser.add_argument("--sector", choices=SECTOR_CHOICES, default="auto")
    parser.add_argument("--source-type", default="uploaded_document")
    parser.add_argument("--document-name", default=None)
    parser.add_argument("--output-dir", type=Path, default=Path(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--markdown", dest="markdown", action="store_true", default=True)
    parser.add_argument("--no-markdown", dest="markdown", action="store_false")
    parser.add_argument("--json", dest="json_output", action="store_true", default=True)
    parser.add_argument("--no-json", dest="json_output", action="store_false")
    parser.add_argument("--extractor", choices=EXTRACTOR_CHOICES, default="auto")
    parser.add_argument("--fail-on-warnings", action="store_true")
    parser.add_argument("--print-report", action="store_true")
    parser.add_argument("--no-write", action="store_true", help="Do not write markdown, JSON, or processing index outputs")
    parser.add_argument("--original-pending-path", default="", help="Original pending/source path before archival copy, for batch identity metadata")
    parser.add_argument("--stored-source-path", default="", help="Archived source path retained by batch processing, for identity metadata")
    return parser


def run(args: argparse.Namespace) -> int:
    input_path_original = str(args.input_file)
    input_path = args.input_file.expanduser().resolve()
    extraction = extract_document(input_path, args.extractor)
    if args.fail_on_warnings and extraction.warnings:
        raise ExtractionError("Extraction produced warnings and --fail-on-warnings was set: " + "; ".join(extraction.warnings))

    selected_sector = args.sector
    # Record why an auto-detected sector was chosen, so the report can show it
    # and the reader can override it with --sector.
    # Placeholder: the displayed basis must explain the sector the assessment
    # actually used, so it is recomputed after the assessment below.
    sector_basis = ""
    document_name = args.document_name or input_path.stem
    processed_at = utc_now_iso()
    source_hash = sha256_file(input_path)
    output_stem = safe_stem(input_path.stem)

    processing = build_processing_metadata(
        input_path=input_path,
        input_path_original=input_path_original,
        output_dir=args.output_dir,
        processed_at_utc=processed_at,
        source_sha256=source_hash,
        safe_output_stem=output_stem,
        markdown_enabled=args.markdown,
        json_enabled=args.json_output,
        original_pending_path=args.original_pending_path,
        stored_source_path=args.stored_source_path,
    )
    if sector_basis:
        processing["sector_basis"] = sector_basis
    extraction_metadata = {
        "input_path_original": input_path_original,
        "input_path": str(input_path),
        "runner_input_path": str(input_path),
        "original_pending_path": args.original_pending_path or input_path_original,
        "stored_source_path": args.stored_source_path or str(input_path),
        "input_file_name": input_path.name,
        "original_file_name": input_path.name,
        "original_file_stem": input_path.stem,
        "source_sha256": source_hash,
        "safe_output_stem": output_stem,
        "extractor_requested": args.extractor,
        "extractor_used": extraction.extractor_used,
        "extraction_confidence": extraction.extraction_confidence,
        "extracted_characters": len(extraction.text),
        "minimum_extracted_characters": MIN_EXTRACTED_CHARACTERS,
        "warning_count": len(extraction.warnings),
        "warnings": extraction.warnings,
        "error_count": len(extraction.errors),
        "errors": extraction.errors,
        "ocr_performed": False,
        "network_access_used": False,
    }

    assessment = assess(
        document_name,
        args.source_type,
        extraction.text,
        sector=selected_sector,
        assessment_mode=resolve_assessment_mode(args.mode),
        source_sha256=source_hash,
        original_file_name=input_path.name,
        original_pending_path=args.original_pending_path or input_path_original,
        stored_source_path=args.stored_source_path or str(input_path),
        runner_input_path=str(input_path),
        processed_at_utc=processed_at,
    )
    # The basis must explain the profile the assessment used, not a separately
    # derived one — the report shows them side by side.
    if selected_sector == "auto":
        used = assessment.get("sector_profile") or assessment.get("sector_used")
        basis = auto_sector_basis(extraction.text, used).get("basis", "")
        if basis:
            processing["sector_basis"] = basis
    base_report = generate_markdown_report([assessment])
    markdown_report = markdown_metadata_block(processing, extraction_metadata, assessment) + base_report
    payload = {
        "processing_metadata": processing,
        "extraction_metadata": extraction_metadata,
        "assessment_result": assessment,
    }

    if not args.no_write:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        if args.markdown:
            Path(processing["markdown_output_path"]).write_text(markdown_report, encoding="utf-8")
        if args.json_output:
            json_dump(Path(processing["json_output_path"]), payload)
        analyst_outputs = write_institutional_outputs(args.output_dir, processing, extraction_metadata, assessment, extraction.text)
        payload["institutional_analyst_outputs"] = {
            "quote_bank_count": len(analyst_outputs["quote_bank"]),
            "gap_count": len(analyst_outputs["gap_register"]),
            "failure_pathway_count": len(analyst_outputs["failure_pathways"]),
            "control_recommendation_count": len(analyst_outputs["control_recommendations"]),
        }
        if args.json_output:
            json_dump(Path(processing["json_output_path"]), payload)
        append_index(args.output_dir, index_record(processing, extraction_metadata, assessment, input_path, document_name))

    print(f"Original input path: {input_path_original}")
    print(f"Resolved input path: {input_path}")
    print(f"Original file name: {input_path.name}")
    print(f"Processed at UTC: {processed_at}")
    print(f"Source SHA-256: {source_hash}")
    print(f"Extractor used: {extraction.extractor_used}")
    print(f"Extracted characters: {len(extraction.text)}")
    print(f"Assessment mode: {assessment.get('assessment_mode')}")
    print(f"Sector profile: {assessment.get('sector_profile')}")
    if args.no_write:
        print("Write mode: disabled (--no-write); no markdown, JSON, or index outputs written.")
    else:
        if args.markdown:
            print(f"Markdown report: {processing['markdown_output_path']}")
        if args.json_output:
            print(f"JSON report: {processing['json_output_path']}")
        print(f"Institutional report: {args.output_dir / (processing['safe_output_stem'] + '.institutional_report.md')}")
        print(f"Technical appendix: {args.output_dir / (processing['safe_output_stem'] + '.technical_appendix.md')}")
        print(f"Analyst bundle: {args.output_dir / 'analyst' / output_stem / 'analyst_bundle.json'}")
        print(f"Processing index: {args.output_dir / INDEX_FILE_NAME}")
    if args.print_report:
        print("\n" + markdown_report)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except ExtractionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
