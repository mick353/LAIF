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
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from assessment_engine import assess, generate_markdown_report

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
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    if suffix == ".pdf":
        attempts.append(("pypdf", extract_pypdf))

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


def auto_sector(text: str) -> str:
    lowered = text.lower()
    patterns: list[tuple[str, Iterable[str]]] = [
        ("clinical_ai", ("clinical", "patient", "clinician", "diagnosis", "medical", "healthcare", "safety incident")),
        ("procurement_vendor_governance", ("procurement", "vendor", "contract", "supplier", "service level", "audit access")),
        ("employment_hr_ai", ("employment", "hiring", "hr", "human resources", "candidate", "adverse action")),
        ("education_ai", ("education", "student", "academic", "school", "accessibility", "learning")),
        ("government_service_delivery", ("public service", "service delivery", "administrative review", "benefit", "caseworker")),
        ("departmental_ai_development", ("software development", "release", "pipeline", "model register", "rollback", "architecture")),
    ]
    scores = [(sum(lowered.count(term) for term in terms), sector) for sector, terms in patterns]
    best_score, best_sector = max(scores, key=lambda item: (item[0], -patterns.index((item[1], next(t for s, t in patterns if s == item[1])))))
    return best_sector if best_score > 0 else "general_ai_governance"


def resolve_assessment_mode(mode: str) -> str:
    return "laif_native_certification" if mode == "laif_native" else "external_framework"


def build_processing_metadata(
    *,
    input_path: Path,
    output_dir: Path,
    processed_at_utc: str,
    source_sha256: str,
    safe_output_stem: str,
    markdown_enabled: bool,
    json_enabled: bool,
) -> dict:
    return {
        "processed_at_utc": processed_at_utc,
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
        "input_path": str(input_path),
        "source_sha256": processing["source_sha256"],
        "safe_output_stem": processing["safe_output_stem"],
        "markdown_output_path": processing["markdown_output_path"],
        "json_output_path": processing["json_output_path"],
        "document_name": document_name,
        "assessment_mode": assessment.get("assessment_mode"),
        "sector_profile": assessment.get("sector_profile"),
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
    return parser


def run(args: argparse.Namespace) -> int:
    input_path = args.input_file
    extraction = extract_document(input_path, args.extractor)
    if args.fail_on_warnings and extraction.warnings:
        raise ExtractionError("Extraction produced warnings and --fail-on-warnings was set: " + "; ".join(extraction.warnings))

    selected_sector = auto_sector(extraction.text) if args.sector == "auto" else args.sector
    document_name = args.document_name or input_path.stem
    processed_at = utc_now_iso()
    source_hash = sha256_file(input_path)
    output_stem = safe_stem(input_path.stem)

    processing = build_processing_metadata(
        input_path=input_path,
        output_dir=args.output_dir,
        processed_at_utc=processed_at,
        source_sha256=source_hash,
        safe_output_stem=output_stem,
        markdown_enabled=args.markdown,
        json_enabled=args.json_output,
    )
    extraction_metadata = {
        "input_path": str(input_path),
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
        processed_at_utc=processed_at,
    )
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
        append_index(args.output_dir, index_record(processing, extraction_metadata, assessment, input_path, document_name))

    print(f"Input file: {input_path}")
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
