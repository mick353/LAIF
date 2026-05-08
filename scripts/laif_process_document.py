#!/usr/bin/env python3
"""User-facing document ingestion runner for LAIF assessment.

This wrapper extracts local document text, preserves extraction provenance, and
passes only the extracted text into the existing LAIF assessment engine. It does
not alter scoring, certification, evidence trace, remediation, calibration, or
validation behavior.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from assessment_engine import assess, generate_markdown_report

MIN_EXTRACTED_NONSPACE_CHARS = 50
TEXT_EXTENSIONS = {".txt", ".md", ".markdown"}
DOCLING_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm", ".png", ".jpg",
    ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".tex", ".csv", ".json",
    ".xml", ".epub", ".zip",
}
DOCX_EXTENSIONS = {".docx"}
PDF_EXTENSIONS = {".pdf"}
SOURCE_TYPE_BY_EXTENSION = {
    ".txt": "policy",
    ".md": "policy",
    ".markdown": "policy",
    ".docx": "policy",
    ".pdf": "policy",
}
SECTOR_CHOICES = [
    "auto",
    "general_ai_governance",
    "government_service_delivery",
    "departmental_ai_development",
    "procurement_vendor_governance",
    "clinical_ai",
    "employment_hr_ai",
    "education_ai",
]
EXTRACTOR_CHOICES = ["auto", "builtin", "docling", "markitdown", "python-docx", "pypdf"]
MODE_CHOICES = ["external_framework", "laif_native"]


class ExtractionError(RuntimeError):
    """Clear user-facing extraction failure."""


@dataclass
class ExtractionResult:
    text: str = ""
    input_path: str = ""
    file_name: str = ""
    file_extension: str = ""
    extractor_requested: str = "auto"
    extractor_used: str = ""
    extraction_warnings: list[str] = field(default_factory=list)
    extraction_errors: list[str] = field(default_factory=list)
    extraction_confidence: str = "failed"

    @property
    def extracted_characters(self) -> int:
        return len(self.text or "")

    def metadata(self) -> dict[str, Any]:
        return {
            "input_path": self.input_path,
            "file_name": self.file_name,
            "file_extension": self.file_extension,
            "extractor_requested": self.extractor_requested,
            "extractor_used": self.extractor_used,
            "extracted_characters": self.extracted_characters,
            "extraction_warnings": list(self.extraction_warnings),
            "extraction_errors": list(self.extraction_errors),
            "extraction_confidence": self.extraction_confidence,
        }


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _extract_with_docling(path: Path) -> str:
    if not _module_available("docling"):
        raise ExtractionError("Docling is not installed. Optional install: pip install docling")
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(str(path))
    return result.document.export_to_markdown()


def _extract_with_markitdown(path: Path) -> str:
    if not _module_available("markitdown"):
        raise ExtractionError(
            "MarkItDown is not installed. Optional install: pip install 'markitdown[pdf,docx]'"
        )
    from markitdown import MarkItDown

    result = MarkItDown(enable_plugins=False).convert(str(path))
    return result.text_content


def _extract_with_python_docx(path: Path) -> str:
    if not _module_available("docx"):
        raise ExtractionError("python-docx is not installed. Optional install: pip install python-docx")
    from docx import Document

    document = Document(str(path))
    parts: list[str] = []
    parts.extend(p.text for p in document.paragraphs if p.text)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text:
                    parts.append(cell.text)
    return "\n".join(parts)


def _extract_with_pypdf(path: Path) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    reader_class = None
    backend = ""
    if _module_available("pypdf"):
        from pypdf import PdfReader

        reader_class = PdfReader
        backend = "pypdf"
    elif _module_available("PyPDF2"):
        from PyPDF2 import PdfReader

        reader_class = PdfReader
        backend = "PyPDF2"
        warnings.append("Using PyPDF2 fallback because pypdf is not installed.")
    else:
        raise ExtractionError("pypdf/PyPDF2 is not installed. Optional install: pip install pypdf")

    reader = reader_class(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    text = "\n".join(pages)
    if not text.strip():
        warnings.append(
            "PDF text extraction returned no text. The document may be scanned or non-text; OCR is required and was not silently performed."
        )
    return text, backend, warnings


def _try_extractor(path: Path, extractor: str, requested: str, warnings: list[str]) -> ExtractionResult:
    used = extractor
    extra_warnings: list[str] = []
    if extractor == "builtin":
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            raise ExtractionError("Built-in extraction supports only .txt, .md, and .markdown files.")
        text = _read_text_file(path)
        confidence = "high"
    elif extractor == "docling":
        text = _extract_with_docling(path)
        confidence = "high"
    elif extractor == "markitdown":
        text = _extract_with_markitdown(path)
        confidence = "medium"
    elif extractor == "python-docx":
        if path.suffix.lower() not in DOCX_EXTENSIONS:
            raise ExtractionError("python-docx extraction supports only .docx files.")
        text = _extract_with_python_docx(path)
        confidence = "medium"
    elif extractor == "pypdf":
        if path.suffix.lower() not in PDF_EXTENSIONS:
            raise ExtractionError("pypdf extraction supports only .pdf files.")
        text, used, extra_warnings = _extract_with_pypdf(path)
        confidence = "medium"
    else:
        raise ExtractionError(f"Unknown extractor: {extractor}")

    return ExtractionResult(
        text=text or "",
        input_path=str(path),
        file_name=path.name,
        file_extension=path.suffix.lower(),
        extractor_requested=requested,
        extractor_used=used,
        extraction_warnings=[*warnings, *extra_warnings],
        extraction_confidence=confidence,
    )


def _validate_extracted_text(result: ExtractionResult) -> ExtractionResult:
    nonspace = len(re.sub(r"\s+", "", result.text or ""))
    if nonspace < MIN_EXTRACTED_NONSPACE_CHARS:
        result.extraction_confidence = "failed"
        message = (
            f"Extracted text is empty or below the safe minimum threshold "
            f"({nonspace} non-whitespace characters; minimum {MIN_EXTRACTED_NONSPACE_CHARS})."
        )
        if result.file_extension == ".pdf":
            message += " The document may be scanned or non-text; OCR is required and was not silently performed."
        result.extraction_errors.append(message)
        raise ExtractionError(message)
    return result


def _extract_document_text(path: Path, extractor: str = "auto") -> ExtractionResult:
    path = path.expanduser().resolve()
    if not path.exists():
        raise ExtractionError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise ExtractionError(f"Input path is not a file: {path}")

    suffix = path.suffix.lower()
    warnings: list[str] = []

    if extractor != "auto":
        result = _try_extractor(path, extractor, extractor, warnings)
        return _validate_extracted_text(result)

    if suffix in TEXT_EXTENSIONS:
        result = _try_extractor(path, "builtin", "auto", warnings)
        return _validate_extracted_text(result)

    attempts: list[str] = []
    if suffix in DOCLING_EXTENSIONS:
        attempts.append("docling")
    attempts.append("markitdown")
    if suffix in DOCX_EXTENSIONS:
        attempts.append("python-docx")
    if suffix in PDF_EXTENSIONS:
        attempts.append("pypdf")

    if not attempts:
        raise ExtractionError(
            f"Unsupported extension '{suffix or '<none>'}'. Use .txt/.md directly or install/request an optional extractor."
        )

    errors: list[str] = []
    for candidate in attempts:
        try:
            result = _try_extractor(path, candidate, "auto", warnings)
            return _validate_extracted_text(result)
        except ExtractionError as exc:
            message = str(exc)
            errors.append(f"{candidate}: {message}")
            if "not installed" in message:
                warnings.append(f"{candidate} unavailable: {message}")
            continue
        except Exception as exc:  # convert raw backend exceptions into clear failures
            message = f"{candidate}: {type(exc).__name__}: {exc}"
            errors.append(message)
            warnings.append(message)
            continue

    failure = ExtractionResult(
        input_path=str(path),
        file_name=path.name,
        file_extension=suffix,
        extractor_requested="auto",
        extractor_used="",
        extraction_warnings=warnings,
        extraction_errors=errors,
        extraction_confidence="failed",
    )
    raise ExtractionError(
        "No available extractor produced usable text. "
        + " | ".join(failure.extraction_errors)
    )


def _safe_output_stem(path: Path | str) -> str:
    stem = Path(path).stem if not isinstance(path, Path) else path.stem
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip(".-_")
    return safe[:80] or "document"


def _auto_sector(text: str, source_type: str, file_name: str) -> str:
    haystack = f"{file_name} {source_type} {text}".lower()
    checks = [
        ("clinical_ai", ("clinical", "patient", "diagnosis", "treatment", "safety risk")),
        ("procurement_vendor_governance", ("procurement", "vendor", "contract", "supplier", "third-party acquisition")),
        ("employment_hr_ai", ("hr", "hiring", "employment", "workforce", "personnel")),
        ("education_ai", ("student", "education", "school", "university", "learning")),
        ("government_service_delivery", ("public service", "benefits", "caseworker", "administrative appeal", "government service")),
        ("departmental_ai_development", ("department", "software development", "development team", "sdlc", "delivery pipeline")),
    ]
    for sector, terms in checks:
        if any(term in haystack for term in terms):
            return sector
    return "general_ai_governance"


def _infer_source_type(path: Path) -> str:
    return SOURCE_TYPE_BY_EXTENSION.get(path.suffix.lower(), "policy")


def _markdown_with_extraction_metadata(markdown: str, metadata: dict[str, Any], mode: str, sector: str) -> str:
    warnings = metadata.get("extraction_warnings") or []
    warning_text = "; ".join(warnings) if warnings else "none"
    block = "\n".join([
        "# LAIF Document Processing Extraction Metadata",
        "",
        f"- **Input file:** `{metadata.get('input_path', '')}`",
        f"- **Extractor used:** {metadata.get('extractor_used', '')}",
        f"- **Extracted characters:** {metadata.get('extracted_characters', 0)}",
        f"- **Warnings:** {warning_text}",
        f"- **Mode:** {mode}",
        f"- **Sector profile:** {sector}",
        "",
        "---",
        "",
    ])
    return block + markdown


def _write_outputs(
    *,
    output_dir: Path,
    input_path: Path,
    markdown_enabled: bool,
    json_enabled: bool,
    markdown_report: str,
    extraction_metadata: dict[str, Any],
    assessment_result: dict[str, Any],
) -> tuple[Path | None, Path | None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = _safe_output_stem(input_path)
    markdown_path = output_dir / f"{stem}.laif.md"
    json_path = output_dir / f"{stem}.laif.json"
    if markdown_enabled:
        markdown_path.write_text(markdown_report, encoding="utf-8")
    else:
        markdown_path = None
    if json_enabled:
        json_path.write_text(
            json.dumps(
                {
                    "extraction_metadata": extraction_metadata,
                    "assessment_result": assessment_result,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    else:
        json_path = None
    return markdown_path, json_path


def _summary_lines(result: dict[str, Any], metadata: dict[str, Any], md_path: Path | None, json_path: Path | None) -> list[str]:
    return [
        f"Document: {result.get('document_name', metadata.get('file_name', ''))}",
        f"File type: {metadata.get('file_extension') or '<none>'}",
        f"Extractor: {metadata.get('extractor_used', '')}",
        f"Extracted characters: {metadata.get('extracted_characters', 0)}",
        f"Assessment mode: {result.get('assessment_mode', '')}",
        f"Sector profile: {result.get('sector_profile', result.get('sector_used', ''))}",
        f"LAIF-native certification: {result.get('laif_native_certification_status') or result.get('external_framework_assessment', {}).get('laif_native_certification_status') or result.get('formal_laif_native_compliance', '')}",
        f"Overall score/band: {result.get('overall_readiness_score', '')} / {result.get('score_interpretation', '')}",
        f"Evidence traces: {len(result.get('evidence_traces', []))}",
        f"Remediation patches: {len(result.get('remediation_patches', []))}",
        f"Calibration cautions: {len(result.get('calibration_cautions', []))}",
        f"Gaming risk notes: {len(result.get('gaming_risk_notes', []))}",
        f"Markdown report: {md_path if md_path else 'not written'}",
        f"JSON report: {json_path if json_path else 'not written'}",
    ]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract a local document and process it with LAIF.")
    parser.add_argument("input_file", type=Path, help="Local document to process (.txt/.md always; .docx/.pdf with optional extractors).")
    parser.add_argument("--mode", choices=MODE_CHOICES, default="external_framework")
    parser.add_argument("--sector", choices=SECTOR_CHOICES, default="auto")
    parser.add_argument("--source-type", default=None)
    parser.add_argument("--document-name", default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("laif_outputs"))
    parser.add_argument("--markdown", dest="markdown", action="store_true", default=True)
    parser.add_argument("--no-markdown", dest="markdown", action="store_false")
    parser.add_argument("--json", dest="json", action="store_true", default=True)
    parser.add_argument("--no-json", dest="json", action="store_false")
    parser.add_argument("--extractor", choices=EXTRACTOR_CHOICES, default="auto")
    parser.add_argument("--fail-on-warnings", action="store_true", default=False)
    parser.add_argument("--print-report", action="store_true", default=False)
    parser.add_argument("--no-write", action="store_true", default=False)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    input_path = args.input_file
    try:
        extraction = _extract_document_text(input_path, args.extractor)
        metadata = extraction.metadata()
        if args.fail_on_warnings and extraction.extraction_warnings:
            raise ExtractionError("Extraction warnings present and --fail-on-warnings was set: " + "; ".join(extraction.extraction_warnings))

        source_type = args.source_type or _infer_source_type(input_path)
        document_name = args.document_name or input_path.stem
        sector = _auto_sector(extraction.text, source_type, input_path.name) if args.sector == "auto" else args.sector
        assessment_mode = "laif_native_certification" if args.mode == "laif_native" else "external_framework"
        source_note = (
            f"LOCAL_FILE_EXTRACTION using {metadata['extractor_used']}; "
            f"warnings: {metadata['extraction_warnings'] or 'none'}"
        )
        result = assess(
            document_name,
            source_type,
            extraction.text,
            sector=sector,
            assessment_mode=assessment_mode,
            provenance="LOCAL_FILE_EXTRACTION",
            source_note=source_note,
            extraction_metadata=metadata,
        )
        base_markdown = generate_markdown_report([result])
        markdown_report = _markdown_with_extraction_metadata(base_markdown, metadata, result.get("assessment_mode", assessment_mode), result.get("sector_profile", sector))

        md_path = json_path = None
        if not args.no_write:
            md_path, json_path = _write_outputs(
                output_dir=args.output_dir,
                input_path=input_path,
                markdown_enabled=args.markdown,
                json_enabled=args.json,
                markdown_report=markdown_report,
                extraction_metadata=metadata,
                assessment_result=result,
            )

        print("\n".join(_summary_lines(result, metadata, md_path, json_path)))
        if args.print_report:
            print("\n" + markdown_report)
        return 0
    except ExtractionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: document processing failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
