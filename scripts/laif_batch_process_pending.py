#!/usr/bin/env python3
"""Batch pending-document processor for the GitHub Actions LAIF workflow.

This orchestration layer scans pending inputs, shells out to the Phase 3T
``scripts/laif_process_document.py`` runner for each supported document, stores
per-document outputs under processed/failed run folders, and writes both a latest
batch summary and a timestamped batch-summary history entry.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = (".txt", ".md", ".markdown", ".docx", ".pdf")
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
PHASE_3T_RUNNER = Path("scripts") / "laif_process_document.py"


def utc_now() -> _dt.datetime:
    return _dt.datetime.now(_dt.UTC)


def utc_now_iso() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_utc_timestamp() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%S%fZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pending_candidates(pending_dir: Path) -> list[Path]:
    if not pending_dir.exists():
        return []
    return sorted((p for p in pending_dir.iterdir() if p.is_file() and p.name != ".gitkeep"), key=lambda p: p.name.lower())


def metadata_files(*roots: Path) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.glob("*/metadata/*.json")))
    return files


def prior_source_hashes(processed_dir: Path, failed_dir: Path) -> dict[str, dict]:
    hashes: dict[str, dict] = {}
    for path in metadata_files(processed_dir, failed_dir):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        source_hash = payload.get("source_sha256")
        if source_hash:
            hashes.setdefault(source_hash, {"metadata_path": str(path), "run_id": payload.get("run_id"), "status": payload.get("status")})
    return hashes


def make_run_id(source: Path) -> str:
    safe_stem = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in source.stem).strip(".-_") or "document"
    return f"{compact_utc_timestamp()}__{safe_stem[:80]}"


def copy_source(source: Path, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    shutil.copy2(source, destination)
    return destination


def move_source(source: Path, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    shutil.move(str(source), str(destination))
    return destination


def run_phase_3t(source_path: Path, reports_dir: Path, mode: str, sector: str, extractor: str, original_pending_path: Path | str = "", stored_source_path: Path | str = "") -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(PHASE_3T_RUNNER),
        str(source_path),
        "--output-dir",
        str(reports_dir),
        "--mode",
        mode,
        "--sector",
        sector,
        "--extractor",
        extractor,
        "--original-pending-path",
        str(original_pending_path or source_path),
        "--stored-source-path",
        str(stored_source_path or source_path),
    ]
    return subprocess.run(command, text=True, capture_output=True, check=False)


def write_archive_manifest(run_dir: Path, original_source: Path, archived_source: Path, source_sha256: str) -> None:
    json_dump(
        run_dir / "archive_manifest.json",
        {
            "archived_at_utc": utc_now_iso(),
            "commit_mode": "archive",
            "original_source_path": str(original_source),
            "archived_source_path": str(archived_source),
            "source_sha256": source_sha256,
        },
    )


def write_run_metadata(metadata_dir: Path, payload: dict) -> Path:
    metadata_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = metadata_dir / "metadata.json"
    json_dump(metadata_path, payload)
    return metadata_path


def process_one(source: Path, args: argparse.Namespace) -> dict:
    source_hash = sha256_file(source)
    run_id = make_run_id(source)
    run_dir = args.processed_dir / run_id
    source_dir = run_dir / "source"
    reports_dir = run_dir / "reports"
    metadata_dir = run_dir / "metadata"
    started = utc_now_iso()

    copied_source = copy_source(source, source_dir)
    completed = run_phase_3t(copied_source, reports_dir, args.mode, args.sector, args.extractor, source, copied_source)
    finished = utc_now_iso()
    metadata = {
        "status": "success" if completed.returncode == 0 else "failed",
        "run_id": run_id,
        "started_at_utc": started,
        "finished_at_utc": finished,
        "processed_at_utc": finished,
        "original_source_path": str(source),
        "original_pending_path": str(source),
        "stored_source_path": str(copied_source),
        "runner_input_path": str(copied_source),
        "reports_dir": str(reports_dir),
        "metadata_dir": str(metadata_dir),
        "source_sha256": source_hash,
        "source_file_name": source.name,
        "original_file_name": source.name,
        "mode": args.mode,
        "sector": args.sector,
        "extractor": args.extractor,
        "commit_mode": args.commit_mode,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }

    if completed.returncode == 0:
        if args.commit_mode == "move":
            # The processing copy is already stored. Remove the pending source only after successful processing.
            source.unlink()
        elif args.commit_mode == "archive":
            write_archive_manifest(run_dir, source, copied_source, source_hash)
        metadata_path = write_run_metadata(metadata_dir, metadata)
        return {"status": "success", "run_id": run_id, "source_path": str(source), "original_pending_path": str(source), "stored_source_path": str(copied_source), "runner_input_path": str(copied_source), "original_file_name": source.name, "source_sha256": source_hash, "metadata_path": str(metadata_path), "reports_dir": str(reports_dir)}

    failed_run_dir = args.failed_dir / run_id
    if failed_run_dir.exists():
        shutil.rmtree(failed_run_dir)
    failed_run_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(run_dir), str(failed_run_dir))
    failed_metadata_dir = failed_run_dir / "metadata"
    (failed_run_dir / "error.txt").write_text((completed.stderr or completed.stdout or "Document processing failed.").strip() + "\n", encoding="utf-8")
    metadata["stored_source_path"] = str(failed_run_dir / "source" / source.name)
    metadata["runner_input_path"] = str(failed_run_dir / "source" / source.name)
    metadata["reports_dir"] = str(failed_run_dir / "reports")
    metadata["metadata_dir"] = str(failed_metadata_dir)
    metadata_path = write_run_metadata(failed_metadata_dir, metadata)
    return {"status": "failed", "run_id": run_id, "source_path": str(source), "original_pending_path": str(source), "stored_source_path": metadata["stored_source_path"], "runner_input_path": metadata["runner_input_path"], "original_file_name": source.name, "source_sha256": source_hash, "metadata_path": str(metadata_path), "error_path": str(failed_run_dir / "error.txt")}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process pending LAIF input documents as a deterministic batch.")
    parser.add_argument("--pending-dir", type=Path, default=Path("laif_inputs/pending"))
    parser.add_argument("--processed-dir", type=Path, default=Path("laif_inputs/processed"))
    parser.add_argument("--failed-dir", type=Path, default=Path("laif_inputs/failed"))
    parser.add_argument("--batch-summaries-dir", type=Path, default=Path("laif_inputs/batch_summaries"))
    parser.add_argument("--mode", choices=ASSESSMENT_MODES, default="external_framework")
    parser.add_argument("--sector", choices=SECTOR_CHOICES, default="auto")
    parser.add_argument("--extractor", choices=EXTRACTOR_CHOICES, default="auto")
    parser.add_argument("--commit-mode", choices=COMMIT_MODES, default="copy")
    parser.add_argument("--reprocess", action="store_true", default=False)
    parser.add_argument("--max-files", type=int, default=20)
    parser.add_argument("--output-summary", type=Path, default=Path("laif_batch_summary.json"))
    parser.add_argument("--fail-fast", action="store_true", default=False)
    return parser


def run(args: argparse.Namespace) -> int:
    started = utc_now_iso()
    batch_run_id = f"{compact_utc_timestamp()}__batch"
    for directory in (args.pending_dir, args.processed_dir, args.failed_dir, args.batch_summaries_dir):
        directory.mkdir(parents=True, exist_ok=True)

    successes: list[dict] = []
    failures: list[dict] = []
    skipped: list[dict] = []
    attempted = 0
    seen_hashes = prior_source_hashes(args.processed_dir, args.failed_dir)

    for source in pending_candidates(args.pending_dir):
        suffix = source.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            skipped.append({"source_path": str(source), "file_name": source.name, "reason": "unsupported_extension", "extension": suffix})
            continue

        source_hash = sha256_file(source)
        if not args.reprocess and source_hash in seen_hashes:
            skipped.append({"source_path": str(source), "file_name": source.name, "reason": "duplicate_source_sha256", "source_sha256": source_hash, "prior": seen_hashes[source_hash]})
            continue

        if attempted >= args.max_files:
            skipped.append({"source_path": str(source), "file_name": source.name, "reason": "max_files_reached", "max_files": args.max_files})
            continue

        attempted += 1
        result = process_one(source, args)
        if result["status"] == "success":
            successes.append(result)
            seen_hashes.setdefault(result["source_sha256"], {"metadata_path": result["metadata_path"], "run_id": result["run_id"], "status": "success"})
        else:
            failures.append(result)
            seen_hashes.setdefault(result["source_sha256"], {"metadata_path": result["metadata_path"], "run_id": result["run_id"], "status": "failed"})
            if args.fail_fast:
                break

    finished = utc_now_iso()
    timestamped_summary_path = args.batch_summaries_dir / f"{batch_run_id}.json"
    summary = {
        "batch_run_id": batch_run_id,
        "started_at_utc": started,
        "finished_at_utc": finished,
        "processed_at_utc": finished,
        "timestamped_summary_path": str(timestamped_summary_path),
        "latest_summary_path": str(args.output_summary),
        "pending_dir": str(args.pending_dir),
        "processed_dir": str(args.processed_dir),
        "failed_dir": str(args.failed_dir),
        "batch_summaries_dir": str(args.batch_summaries_dir),
        "mode": args.mode,
        "sector": args.sector,
        "extractor": args.extractor,
        "commit_mode": args.commit_mode,
        "reprocess": args.reprocess,
        "max_files": args.max_files,
        "success_count": len(successes),
        "failed_count": len(failures),
        "skipped_count": len(skipped),
        "successes": successes,
        "failures": failures,
        "skipped": skipped,
    }
    json_dump(timestamped_summary_path, summary)
    json_dump(args.output_summary, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures and args.fail_fast else 0


def main(argv: list[str] | None = None) -> int:
    return run(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
