#!/usr/bin/env python3
"""Batch processor for pending LAIF document inputs.

Processes local files from a pending directory with the existing document runner,
writes a latest batch summary, and preserves a timestamped per-run summary
history. This wrapper does not alter scoring, certification, validation, or
report-generation behavior.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
DEFAULT_PENDING_DIR = Path("laif_inputs/pending")
DEFAULT_PROCESSED_DIR = Path("laif_inputs/processed")
DEFAULT_FAILED_DIR = Path("laif_inputs/failed")
DEFAULT_BATCH_SUMMARIES_DIR = Path("laif_inputs/batch_summaries")
DEFAULT_OUTPUT_SUMMARY = Path("laif_batch_summary.json")


def utc_now() -> _dt.datetime:
    return _dt.datetime.now(_dt.UTC)


def utc_iso(value: _dt.datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_utc(value: _dt.datetime) -> str:
    return value.strftime("%Y%m%dT%H%M%S%fZ")


def safe_stem(stem: str) -> str:
    from scripts.laif_process_document import safe_stem as runner_safe_stem

    return runner_safe_stem(stem)


def pending_files(pending_dir: Path) -> list[Path]:
    if not pending_dir.exists():
        return []
    return sorted(path for path in pending_dir.iterdir() if path.is_file() and not path.name.startswith("."))


def unique_child(parent: Path, name: str) -> Path:
    candidate = parent / name
    if not candidate.exists():
        return candidate
    stem = Path(name).stem
    suffix = Path(name).suffix
    counter = 2
    while True:
        candidate = parent / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def move_input(source: Path, destination_dir: Path) -> str:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = unique_child(destination_dir, source.name)
    shutil.move(str(source), str(destination))
    return str(destination)


def process_one(path: Path, args: argparse.Namespace) -> dict[str, Any]:
    started = utc_now()
    document_run_id = f"{compact_utc(started)}__{safe_stem(path.stem)}"
    document_output_dir = args.processed_dir / document_run_id
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/laif_process_document.py"),
        str(path),
        "--output-dir",
        str(document_output_dir),
        "--mode",
        args.mode,
        "--sector",
        args.sector,
        "--source-type",
        args.source_type,
        "--extractor",
        args.extractor,
    ]
    completed = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True)
    finished = utc_now()

    record: dict[str, Any] = {
        "document_run_id": document_run_id,
        "input_path": str(path),
        "input_file_name": path.name,
        "started_at_utc": utc_iso(started),
        "finished_at_utc": utc_iso(finished),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    if completed.returncode == 0:
        record["status"] = "processed"
        record["output_dir"] = str(document_output_dir)
        record["archived_input_path"] = move_input(path, document_output_dir)
    else:
        failed_dir = args.failed_dir / document_run_id
        record["status"] = "failed"
        record["output_dir"] = str(failed_dir)
        record["archived_input_path"] = move_input(path, failed_dir)
        failure_payload = {
            "document_run_id": document_run_id,
            "input_file_name": path.name,
            "failed_at_utc": utc_iso(finished),
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        (failed_dir / "failure.json").write_text(json.dumps(failure_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def write_summary(summary: dict[str, Any], output_summary: Path, timestamped_summary_path: Path) -> None:
    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    timestamped_summary_path.parent.mkdir(parents=True, exist_ok=True)
    output_summary.parent.mkdir(parents=True, exist_ok=True)
    timestamped_summary_path.write_text(payload, encoding="utf-8")
    output_summary.write_text(payload, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process pending LAIF documents and write batch summaries.")
    parser.add_argument("--pending-dir", type=Path, default=DEFAULT_PENDING_DIR)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--failed-dir", type=Path, default=DEFAULT_FAILED_DIR)
    parser.add_argument("--batch-summaries-dir", type=Path, default=DEFAULT_BATCH_SUMMARIES_DIR)
    parser.add_argument("--output-summary", type=Path, default=DEFAULT_OUTPUT_SUMMARY)
    parser.add_argument("--max-files", type=int, default=25)
    parser.add_argument("--mode", choices=("external_framework", "laif_native"), default="external_framework")
    parser.add_argument("--sector", default="auto")
    parser.add_argument("--source-type", default="uploaded_document")
    parser.add_argument("--extractor", default="auto")
    return parser


def run(args: argparse.Namespace) -> int:
    batch_started = utc_now()
    batch_run_id = f"{compact_utc(batch_started)}__batch"
    timestamped_summary_path = args.batch_summaries_dir / f"{batch_run_id}.json"

    args.processed_dir.mkdir(parents=True, exist_ok=True)
    args.failed_dir.mkdir(parents=True, exist_ok=True)
    args.batch_summaries_dir.mkdir(parents=True, exist_ok=True)

    candidates = pending_files(args.pending_dir)
    selected = candidates[: max(args.max_files, 0)]
    records = [process_one(path, args) for path in selected]
    processed_count = sum(1 for record in records if record["status"] == "processed")
    failed_count = sum(1 for record in records if record["status"] == "failed")

    batch_finished = utc_now()
    summary: dict[str, Any] = {
        "batch_run_id": batch_run_id,
        "timestamped_summary_path": str(timestamped_summary_path),
        "latest_summary_path": str(args.output_summary),
        "started_at_utc": utc_iso(batch_started),
        "finished_at_utc": utc_iso(batch_finished),
        "pending_dir": str(args.pending_dir),
        "processed_dir": str(args.processed_dir),
        "failed_dir": str(args.failed_dir),
        "batch_summaries_dir": str(args.batch_summaries_dir),
        "selected_count": len(selected),
        "remaining_pending_count": max(len(candidates) - len(selected), 0),
        "processed_count": processed_count,
        "failed_count": failed_count,
        "records": records,
    }
    write_summary(summary, args.output_summary, timestamped_summary_path)

    print(f"Batch run ID: {batch_run_id}")
    print(f"Latest summary: {args.output_summary}")
    print(f"Timestamped summary: {timestamped_summary_path}")
    print(f"Processed: {processed_count}; Failed: {failed_count}; Remaining pending: {summary['remaining_pending_count']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
