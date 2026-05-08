#!/usr/bin/env python3
"""Batch orchestration for pending LAIF document inputs.

This script intentionally shells out to scripts/laif_process_document.py for each
supported input file. It provides GitHub-friendly folder orchestration only and
must not change LAIF assessment, scoring, certification, sector, evidence trace,
or remediation behavior.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts" / "laif_process_document.py"
SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".docx", ".pdf"}
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
COMMIT_MODES = ("copy", "move", "archive")


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def utc_now_iso() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%S%fZ")


def safe_stem(stem: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", stem.strip())
    safe = re.sub(r"-+", "-", safe).strip(".-_")
    return safe[:120] or "document"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected a boolean value, got {value!r}")


def path_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def discover_pending_files(pending_dir: Path, processed_dir: Path, failed_dir: Path) -> list[Path]:
    if not pending_dir.exists():
        return []
    files: list[Path] = []
    for path in sorted(pending_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name == ".gitkeep":
            continue
        if path_is_relative_to(path, processed_dir) or path_is_relative_to(path, failed_dir):
            continue
        files.append(path)
    return files


def known_source_hashes(*roots: Path) -> set[str]:
    hashes: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for metadata_path in root.rglob("metadata/run_metadata.json"):
            try:
                payload = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            source_hash = payload.get("source_sha256")
            if isinstance(source_hash, str) and source_hash:
                hashes.add(source_hash)
    return hashes


def build_run_metadata(
    *,
    run_id: str,
    processed_at_utc: str,
    source_path: Path,
    source_sha256: str,
    report_dir: Path,
    status: str,
    command: list[str],
    return_code: int | None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "processed_at_utc": processed_at_utc,
        "original_file_name": source_path.name,
        "source_sha256": source_sha256,
        "source_path": str(source_path),
        "report_dir": str(report_dir),
        "status": status,
        "command": command,
        "return_code": return_code,
    }


def copy_or_move_source(source: Path, destination_dir: Path, commit_mode: str) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    if commit_mode == "move":
        shutil.move(str(source), str(destination))
    else:
        shutil.copy2(source, destination)
    return destination


def write_archive_manifest(metadata_dir: Path, metadata: dict[str, Any], archived_source: Path) -> None:
    manifest = {
        "archive_manifest_version": 1,
        "created_at_utc": utc_now_iso(),
        "run_id": metadata["run_id"],
        "status": metadata["status"],
        "source_sha256": metadata["source_sha256"],
        "archived_source_path": str(archived_source),
        "report_dir": metadata["report_dir"],
    }
    json_write(metadata_dir / "archive_manifest.json", manifest)


def run_one_file(
    *,
    source: Path,
    processed_dir: Path,
    failed_dir: Path,
    mode: str,
    sector: str,
    extractor: str,
    commit_mode: str,
) -> tuple[str, dict[str, Any]]:
    run_id = f"{compact_timestamp()}__{safe_stem(source.stem)}"
    processed_at_utc = utc_now_iso()
    source_hash = sha256_file(source)
    success_root = processed_dir / run_id
    success_source_dir = success_root / "source"
    success_report_dir = success_root / "reports"
    success_metadata_dir = success_root / "metadata"
    command = [
        sys.executable,
        str(RUNNER_PATH),
        str(source),
        "--output-dir",
        str(success_report_dir),
        "--mode",
        mode,
        "--sector",
        sector,
        "--extractor",
        extractor,
    ]

    success_report_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode == 0:
        archived_source = copy_or_move_source(source, success_source_dir, commit_mode)
        metadata = build_run_metadata(
            run_id=run_id,
            processed_at_utc=processed_at_utc,
            source_path=source,
            source_sha256=source_hash,
            report_dir=success_report_dir,
            status="success",
            command=command,
            return_code=completed.returncode,
        )
        json_write(success_metadata_dir / "run_metadata.json", metadata)
        if commit_mode == "archive":
            write_archive_manifest(success_metadata_dir, metadata, archived_source)
        return "success", {
            "run_id": run_id,
            "original_file_name": source.name,
            "source_sha256": source_hash,
            "source_path": str(source),
            "output_dir": str(success_root),
            "report_dir": str(success_report_dir),
            "metadata_path": str(success_metadata_dir / "run_metadata.json"),
        }

    if success_root.exists():
        shutil.rmtree(success_root)
    failed_root = failed_dir / run_id
    failed_source_dir = failed_root / "source"
    failed_metadata_dir = failed_root / "metadata"
    archived_source = copy_or_move_source(source, failed_source_dir, commit_mode)
    error_text = "\n".join(
        part
        for part in (
            f"Command: {' '.join(command)}",
            f"Return code: {completed.returncode}",
            "",
            "STDOUT:",
            completed.stdout,
            "",
            "STDERR:",
            completed.stderr,
        )
        if part is not None
    )
    (failed_root / "error.txt").write_text(error_text, encoding="utf-8")
    metadata = build_run_metadata(
        run_id=run_id,
        processed_at_utc=processed_at_utc,
        source_path=source,
        source_sha256=source_hash,
        report_dir=success_report_dir,
        status="failed",
        command=command,
        return_code=completed.returncode,
    )
    json_write(failed_metadata_dir / "run_metadata.json", metadata)
    if commit_mode == "archive":
        write_archive_manifest(failed_metadata_dir, metadata, archived_source)
    return "failed", {
        "run_id": run_id,
        "original_file_name": source.name,
        "source_sha256": source_hash,
        "source_path": str(source),
        "output_dir": str(failed_root),
        "error_path": str(failed_root / "error.txt"),
        "metadata_path": str(failed_metadata_dir / "run_metadata.json"),
        "return_code": completed.returncode,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process supported documents from a LAIF pending input folder.")
    parser.add_argument("--pending-dir", type=Path, default=Path("laif_inputs/pending"))
    parser.add_argument("--processed-dir", type=Path, default=Path("laif_inputs/processed"))
    parser.add_argument("--failed-dir", type=Path, default=Path("laif_inputs/failed"))
    parser.add_argument("--mode", choices=ASSESSMENT_MODES, default="external_framework")
    parser.add_argument("--sector", choices=SECTOR_CHOICES, default="auto")
    parser.add_argument("--extractor", choices=EXTRACTOR_CHOICES, default="auto")
    parser.add_argument("--commit-mode", choices=COMMIT_MODES, default="copy")
    parser.add_argument("--reprocess", type=parse_bool, default=False)
    parser.add_argument("--max-files", type=int, default=20)
    parser.add_argument("--output-summary", type=Path, default=Path("laif_batch_summary.json"))
    parser.add_argument("--fail-fast", type=parse_bool, default=False)
    return parser


def process_pending(args: argparse.Namespace) -> dict[str, Any]:
    pending_dir = args.pending_dir
    processed_dir = args.processed_dir
    failed_dir = args.failed_dir
    pending_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    failed_dir.mkdir(parents=True, exist_ok=True)

    successes: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    processed_attempts = 0
    existing_hashes = known_source_hashes(processed_dir, failed_dir)

    for source in discover_pending_files(pending_dir, processed_dir, failed_dir):
        suffix = source.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            skipped.append({"path": str(source), "reason": "skipped_unsupported", "extension": suffix})
            continue
        source_hash = sha256_file(source)
        if not args.reprocess and source_hash in existing_hashes:
            skipped.append({"path": str(source), "reason": "skipped_duplicate", "source_sha256": source_hash})
            continue
        if processed_attempts >= args.max_files:
            skipped.append({"path": str(source), "reason": "skipped_max_files", "max_files": args.max_files})
            continue
        processed_attempts += 1
        status, record = run_one_file(
            source=source,
            processed_dir=processed_dir,
            failed_dir=failed_dir,
            mode=args.mode,
            sector=args.sector,
            extractor=args.extractor,
            commit_mode=args.commit_mode,
        )
        if status == "success":
            successes.append(record)
            existing_hashes.add(record["source_sha256"])
        else:
            failures.append(record)
            existing_hashes.add(record["source_sha256"])
            if args.fail_fast:
                break

    summary = {
        "processed_at_utc": utc_now_iso(),
        "pending_dir": str(pending_dir),
        "processed_dir": str(processed_dir),
        "failed_dir": str(failed_dir),
        "mode": args.mode,
        "sector": args.sector,
        "extractor": args.extractor,
        "commit_mode": args.commit_mode,
        "reprocess": bool(args.reprocess),
        "max_files": args.max_files,
        "success_count": len(successes),
        "failed_count": len(failures),
        "skipped_count": len(skipped),
        "success": successes,
        "failed": failures,
        "skipped": skipped,
        "success_list": successes,
        "failed_list": failures,
        "skipped_list": skipped,
    }
    json_write(args.output_summary, summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_files < 0:
        parser.error("--max-files must be zero or greater")
    summary = process_pending(args)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
