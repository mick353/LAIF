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



def _load_document_bundle(success: dict) -> dict:
    reports_dir = Path(success.get("reports_dir", ""))
    bundle_path = reports_dir / "analyst" / "analyst_bundle.json"
    payload: dict = {"success": success, "bundle": {}, "institutional_reports": []}
    if bundle_path.exists():
        try:
            payload["bundle"] = json.loads(bundle_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload["bundle"] = {}
    payload["institutional_reports"] = [str(p) for p in sorted(reports_dir.glob("*.institutional_report.md"))]
    payload["technical_appendices"] = [str(p) for p in sorted(reports_dir.glob("*.technical_appendix.md"))]
    return payload


def write_batch_institutional_outputs(summary: dict, args: argparse.Namespace) -> dict:
    docs = [_load_document_bundle(success) for success in summary.get("successes", [])]
    output_root = args.output_summary.parent if args.output_summary.parent != Path("") else Path(".")
    output_root.mkdir(parents=True, exist_ok=True)
    batch_id = summary.get("batch_run_id")
    all_quotes = []
    all_gaps = []
    all_controls = []
    doc_rows = []
    type_counts: dict[str, int] = {}
    force_rows = []
    for doc in docs:
        bundle = doc.get("bundle", {})
        meta = bundle.get("document_metadata", {})
        doc_type = meta.get("document_type", "unknown_governance_document")
        type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        quotes = bundle.get("quote_bank", [])
        gaps = bundle.get("gap_register", [])
        controls = bundle.get("control_recommendations", [])
        all_quotes.extend(quotes)
        for gap in gaps:
            row = dict(gap)
            row["source_document"] = meta.get("original_file_name")
            all_gaps.append(row)
        for ctrl in controls:
            row = dict(ctrl)
            row["source_document"] = meta.get("original_file_name")
            all_controls.append(row)
        doc_rows.append({
            "file": meta.get("original_file_name") or doc.get("success", {}).get("original_file_name"),
            "document_type": doc_type,
            "sector_profile": meta.get("sector_profile"),
            "institutional_reports": doc.get("institutional_reports", []),
            "technical_appendices": doc.get("technical_appendices", []),
            "quote_count": len(quotes),
            "gap_count": len(gaps),
            "control_count": len(controls),
        })
        force_rows.append(f"- **{doc_rows[-1]['file']}:** {doc_type}; sector {doc_rows[-1]['sector_profile']}; quotes {len(quotes)}; gaps {len(gaps)}.")
    common_gap_types = sorted({gap.get("gap_type", "unknown") for gap in all_gaps})

    def _first_doc(*types: str) -> dict:
        return next((row for row in doc_rows if row.get("document_type") in types), {})

    strongest_legal = _first_doc("binding_legal_instrument")
    strongest_voluntary = _first_doc("voluntary_risk_framework")
    strongest_public_policy = _first_doc("public_sector_policy", "internal_policy", "implementation_guide")
    strongest_clinical_sector = _first_doc("sector_assurance_checklist")
    urgent_gap = common_gap_types[0] if common_gap_types else "portfolio evidence sufficiency and operational closure"
    matrix_rows = []
    for row in doc_rows:
        dt = row.get("document_type")
        matrix_rows.append(
            "| {file} | {legal} | {policy} | {assurance} | {operational} | {evidence} | {lifecycle} | {accountability} | {redress} | {readiness} |".format(
                file=row.get("file"),
                legal="high" if dt == "binding_legal_instrument" else "limited",
                policy="high" if dt in {"executive_policy_directive", "public_sector_policy", "internal_policy"} else "medium" if dt == "binding_legal_instrument" else "limited",
                assurance="high" if dt in {"sector_assurance_checklist", "procurement_assessment_form"} else "medium" if dt == "technical_standard" else "limited",
                operational="requires local closure" if row.get("gap_count", 0) else "review required",
                evidence="quote-backed, sufficiency not presumed" if row.get("quote_count", 0) else "source review required",
                lifecycle="requires monitoring/change gate",
                accountability="requires named owner/sign-off",
                redress="requires redress/contestability mapping",
                readiness="ready for control mapping, not standalone assurance",
            )
        )
    report_lines = [
        f"# Batch Institutional Governance Report — {batch_id}", "",
        "## Batch identity", "",
        f"- **Batch run ID:** {batch_id}", f"- **Processed at UTC:** {summary.get('processed_at_utc')}", f"- **Success count:** {summary.get('success_count')}", f"- **Failed count:** {summary.get('failed_count')}", "",
        "## Processed file list", "",
    ]
    for row in doc_rows:
        report_lines.append(f"- {row['file']} — {row['document_type']} — institutional reports: {', '.join(row['institutional_reports'])}")
    report_lines += ["", "## Document type summary", "", json.dumps(type_counts, indent=2, sort_keys=True), "", "## Governance-force matrix", "", "| Document | Legal force | Policy force | Assurance/procurement force | Operational closure | Evidence sufficiency | Lifecycle control | Accountability closure | Redress/contestability | Implementation readiness |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    report_lines.extend(matrix_rows or ["| n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"] )
    report_lines += [
        "", "## Governance force comparison", "",
    ]
    report_lines.extend(force_rows or ["- No successful documents were available for comparison."])
    report_lines += [
        "", "## Portfolio source roles", "",
        f"- **Strongest legal source:** {strongest_legal.get('file', 'none detected')}.",
        f"- **Strongest voluntary governance design source:** {strongest_voluntary.get('file', 'none detected')}.",
        f"- **Strongest public-sector operating policy:** {strongest_public_policy.get('file', 'none detected')}.",
        f"- **Strongest clinical/sector assurance source:** {strongest_clinical_sector.get('file', 'none detected')}.",
        f"- **Most urgent common control gap:** {urgent_gap}.",
        "", "## Common gaps across portfolio", "",
    ]
    report_lines.extend([f"- {gap_type}" for gap_type in common_gap_types] or ["- No common gaps detected."])
    report_lines += ["", "## Cross-document failure pathways", "", "- Portfolio-level failure can occur when multiple source documents are cited as assurance while no combined owner, evidence register, threshold, cadence, or escalation model is implemented.", "", "## Priority implementation roadmap", ""]
    for ctrl in all_controls[:10]:
        report_lines.append(f"- **{ctrl.get('control_id')} ({ctrl.get('priority')}):** {ctrl.get('control_name')} — source: {ctrl.get('source_document')}")
    report_lines += ["", "## Recommended combined operating model", "", "Create a combined operating model with a legal-obligation map, policy implementation tracker, sector assurance register, evidence sufficiency matrix, lifecycle review gate, named accountability sign-off, redress/contestability pathway, and implementation-readiness dashboard. Link each source document to accountable owners, implementation artifacts, quote IDs, gap IDs, control IDs, review cadence, thresholds, escalation gates, and decision consequences.", "", "## Links/paths to each document institutional report", ""]
    for row in doc_rows:
        for report in row.get("institutional_reports", []):
            report_lines.append(f"- {report}")
    paths = {
        "batch_institutional_report": output_root / "batch_institutional_report.md",
        "portfolio_gap_register": output_root / "portfolio_gap_register.json",
        "portfolio_control_roadmap": output_root / "portfolio_control_roadmap.md",
        "batch_quote_bank": output_root / "batch_quote_bank.md",
        "batch_ai_prompt": output_root / "batch_ai_prompt.md",
        "batch_ai_input_bundle": output_root / "batch_ai_input_bundle.json",
    }
    paths["batch_institutional_report"].write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    json_dump(paths["portfolio_gap_register"], {"batch_run_id": batch_id, "gaps": all_gaps})
    roadmap = ["# Portfolio Control Roadmap", ""] + [f"- **{c.get('control_id')} ({c.get('priority')}):** {c.get('control_name')} — owner: {c.get('owner')} — source: {c.get('source_document')}" for c in all_controls]
    paths["portfolio_control_roadmap"].write_text("\n".join(roadmap) + "\n", encoding="utf-8")
    quote_md = ["# Batch Quote Bank", ""]
    for q in all_quotes:
        quote_md += [f"## {q.get('quote_id')} — {q.get('original_file_name')} — {q.get('signal_category')}", "", f"> {q.get('exact_quote')}", ""]
    paths["batch_quote_bank"].write_text("\n".join(quote_md), encoding="utf-8")
    paths["batch_ai_prompt"].write_text("# Batch AI Analyst Prompt\n\nUse only the provided deterministic batch AI input bundle, quote IDs, gap IDs, control IDs, and source metadata. Do not invent quotes, legal claims, obligations, scores, documents, actors, controls, certifications, or legal-validity conclusions.\n", encoding="utf-8")
    json_dump(paths["batch_ai_input_bundle"], {"batch_metadata": summary, "documents": doc_rows, "quote_bank": all_quotes, "portfolio_gap_register": all_gaps, "portfolio_control_roadmap": all_controls})
    # Also copy batch-level outputs into a subdirectory under the timestamped summaries
    # area for workflow artifacts without polluting the historical summary JSON glob.
    artifact_dir = args.batch_summaries_dir / f"{batch_id}_institutional_artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    for name, path in paths.items():
        target = artifact_dir / path.name
        shutil.copyfile(path, target)
    return {name: str(path) for name, path in paths.items()}

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
    summary["batch_institutional_outputs"] = write_batch_institutional_outputs(summary, args)
    json_dump(timestamped_summary_path, summary)
    json_dump(args.output_summary, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures and args.fail_fast else 0


def main(argv: list[str] | None = None) -> int:
    return run(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
