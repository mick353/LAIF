#!/usr/bin/env python3
"""Process a source document into LAIF markdown/JSON assessment outputs."""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assessment_engine import assess

INDEX_FILE_NAME = "laif_processing_index.jsonl"
DEFAULT_OUTPUT_DIR = "laif_outputs"
SUPPORTED_TEXT_EXTENSIONS = {".md", ".txt", ".text"}


def _processed_at_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_output_stem(path):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem).strip("._-")
    safe = re.sub(r"_+", "_", safe)
    return safe or "document"


def _extract_text(path, extractor_requested="auto"):
    extension = path.suffix.lower()
    warnings = []
    errors = []
    extractor_used = "text"

    if extractor_requested not in {"auto", "text"}:
        raise ValueError(f"Unsupported extractor requested: {extractor_requested}")

    if extension not in SUPPORTED_TEXT_EXTENSIONS:
        warnings.append(
            f"Unsupported extension {extension or '<none>'}; attempting UTF-8 text extraction."
        )

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
        warnings.append("Input contained undecodable UTF-8 bytes; replacement characters were used.")

    confidence = 1.0 if not errors else 0.0
    if warnings:
        confidence = min(confidence, 0.85)

    return {
        "text": text,
        "extractor_used": extractor_used,
        "extracted_characters": len(text),
        "extraction_confidence": confidence,
        "extraction_warnings": warnings,
        "extraction_errors": errors,
    }


def _build_extraction_metadata(input_path, safe_stem, extractor_requested, extraction):
    return {
        "processed_at_utc": _processed_at_utc(),
        "input_path": str(input_path),
        "input_file_name": input_path.name,
        "original_file_name": input_path.name,
        "original_file_stem": input_path.stem,
        "file_extension": input_path.suffix,
        "source_sha256": _source_sha256(input_path),
        "safe_output_stem": safe_stem,
        "extractor_requested": extractor_requested,
        "extractor_used": extraction["extractor_used"],
        "extracted_characters": extraction["extracted_characters"],
        "extraction_confidence": extraction["extraction_confidence"],
        "extraction_warnings": list(extraction["extraction_warnings"]),
        "extraction_errors": list(extraction["extraction_errors"]),
    }


def _processing_metadata(extraction_metadata, markdown_output_path, json_output_path):
    return {
        "processed_at_utc": extraction_metadata["processed_at_utc"],
        "original_file_name": extraction_metadata["input_file_name"],
        "source_sha256": extraction_metadata["source_sha256"],
        "safe_output_stem": extraction_metadata["safe_output_stem"],
        "markdown_output_path": str(markdown_output_path),
        "json_output_path": str(json_output_path),
    }


def _markdown_report(result, extraction_metadata, processing_metadata):
    lines = [
        "# LAIF Document Processing Report",
        "",
        "## Processing Metadata",
        f"- **Processed at UTC:** {extraction_metadata['processed_at_utc']}",
        f"- **Original file name:** {extraction_metadata['input_file_name']}",
        f"- **Source SHA-256:** {extraction_metadata['source_sha256']}",
        f"- **Extractor used:** {extraction_metadata['extractor_used']}",
        f"- **Extracted characters:** {extraction_metadata['extracted_characters']}",
        f"- **Assessment mode:** {result.get('assessment_mode', '')}",
        f"- **Sector profile:** {result.get('sector_profile', '')}",
        f"- **Safe output stem:** {extraction_metadata['safe_output_stem']}",
        f"- **Markdown output path:** {processing_metadata['markdown_output_path']}",
        f"- **JSON output path:** {processing_metadata['json_output_path']}",
        "",
        "## Assessment Summary",
        f"- **Document name:** {result.get('document_name', '')}",
        f"- **Formal LAIF-native compliance:** {result.get('formal_laif_native_compliance', '')}",
        f"- **Overall readiness score:** {result.get('overall_readiness_score', '')}",
        f"- **Evidence trace count:** {len(result.get('evidence_traces', []))}",
        f"- **Remediation patch count:** {len(result.get('remediation_patches', []))}",
        f"- **Calibration caution count:** {len(result.get('calibration_cautions', []))}",
        f"- **Gaming risk note count:** {len(result.get('gaming_risk_notes', []))}",
        "",
        "## Extraction Metadata",
        "```json",
        json.dumps(extraction_metadata, indent=2, sort_keys=True),
        "```",
    ]
    return "\n".join(lines) + "\n"


def _index_record(result, extraction_metadata, processing_metadata):
    return {
        "processed_at_utc": extraction_metadata["processed_at_utc"],
        "original_file_name": extraction_metadata["input_file_name"],
        "input_path": extraction_metadata["input_path"],
        "source_sha256": extraction_metadata["source_sha256"],
        "safe_output_stem": extraction_metadata["safe_output_stem"],
        "markdown_output_path": processing_metadata["markdown_output_path"],
        "json_output_path": processing_metadata["json_output_path"],
        "document_name": result.get("document_name"),
        "assessment_mode": result.get("assessment_mode"),
        "sector_profile": result.get("sector_profile"),
        "formal_laif_native_compliance": result.get("formal_laif_native_compliance"),
        "overall_readiness_score": result.get("overall_readiness_score"),
        "evidence_trace_count": len(result.get("evidence_traces", [])),
        "remediation_patch_count": len(result.get("remediation_patches", [])),
        "calibration_caution_count": len(result.get("calibration_cautions", [])),
        "gaming_risk_note_count": len(result.get("gaming_risk_notes", [])),
        "extractor_used": extraction_metadata["extractor_used"],
        "extracted_characters": extraction_metadata["extracted_characters"],
        "extraction_confidence": extraction_metadata["extraction_confidence"],
        "warning_count": len(extraction_metadata.get("extraction_warnings", [])),
        "error_count": len(extraction_metadata.get("extraction_errors", [])),
    }


def process_document(input_path, output_dir=DEFAULT_OUTPUT_DIR, no_write=False, extractor="auto", sector="general_ai_governance"):
    source_path = Path(input_path).expanduser().resolve()
    if not source_path.exists() or not source_path.is_file():
        raise FileNotFoundError(f"Input document not found: {source_path}")

    out_dir = Path(output_dir).expanduser()
    safe_stem = _safe_output_stem(source_path)
    markdown_output_path = out_dir / f"{safe_stem}.laif.md"
    json_output_path = out_dir / f"{safe_stem}.laif.json"

    extraction = _extract_text(source_path, extractor)
    extraction_metadata = _build_extraction_metadata(source_path, safe_stem, extractor, extraction)
    result = assess(
        source_path.name,
        "processed_document",
        extraction["text"],
        sector=sector,
        assessment_mode="external_framework",
        extraction_metadata=extraction_metadata,
    )
    processing_metadata = _processing_metadata(
        extraction_metadata, markdown_output_path, json_output_path
    )
    payload = {
        "processing_metadata": processing_metadata,
        "extraction_metadata": extraction_metadata,
        "assessment_result": result,
    }

    if not no_write:
        out_dir.mkdir(parents=True, exist_ok=True)
        markdown_output_path.write_text(
            _markdown_report(result, extraction_metadata, processing_metadata),
            encoding="utf-8",
        )
        json_output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        index_path = out_dir / INDEX_FILE_NAME
        with index_path.open("a", encoding="utf-8") as index_file:
            index_file.write(json.dumps(_index_record(result, extraction_metadata, processing_metadata), sort_keys=True) + "\n")
    else:
        index_path = out_dir / INDEX_FILE_NAME

    return {
        "processing_metadata": processing_metadata,
        "extraction_metadata": extraction_metadata,
        "assessment_result": result,
        "markdown_output_path": markdown_output_path,
        "json_output_path": json_output_path,
        "index_path": index_path,
        "no_write": no_write,
    }


def _build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="Document to process")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory (default: laif_outputs)")
    parser.add_argument("--no-write", action="store_true", help="Run assessment without writing reports or appending the JSONL index")
    parser.add_argument("--extractor", default="auto", choices=("auto", "text"), help="Extractor to request")
    parser.add_argument("--sector", default="general_ai_governance", help="LAIF sector profile key")
    return parser


def main(argv=None):
    args = _build_parser().parse_args(argv)
    processed = process_document(
        args.input_path,
        output_dir=args.output_dir,
        no_write=args.no_write,
        extractor=args.extractor,
        sector=args.sector,
    )
    result = processed["assessment_result"]
    print(f"Assessment mode: {result.get('assessment_mode')}")
    print(f"Sector profile: {result.get('sector_profile')}")
    print(f"Original file name: {processed['extraction_metadata'].get('input_file_name')}")
    print(f"Source SHA-256: {processed['extraction_metadata'].get('source_sha256')}")
    if args.no_write:
        print("No-write mode: reports and index were not written")
    else:
        print(f"Markdown report: {processed['markdown_output_path']}")
        print(f"JSON report: {processed['json_output_path']}")
        print(f"Processing index: {processed['index_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
