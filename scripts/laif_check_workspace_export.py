#!/usr/bin/env python3
"""Check a private LAIF Workspace export locally without changing its files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import zipfile
import zlib

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.laif_process_document import ExtractionError, RUN_RECEIPT_SUFFIX, check_assessment_receipt


# The Workspace writer caps file contents at 32 MiB. Allow room for the inventory
# and ZIP metadata while keeping local reads bounded.
_BUNDLE_LIMIT = 33 * 1024 * 1024
_ARCHIVE_LIMIT = 34 * 1024 * 1024
_ENTRY_LIMIT = 2048


class ExportError(ValueError):
    """The package or one of its supplied companion files failed a check."""


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ExportError("JSON contains a duplicate object key.")
        result[key] = value
    return result


def _non_json_constant(value):
    raise ExportError(f"Invalid JSON numeric constant: {value}.")


def _mapping(value, label):
    if not isinstance(value, dict):
        raise ExportError(f"{label} must be a JSON object.")
    return value


def _records(value, label):
    if not isinstance(value, list):
        raise ExportError(f"{label} must be a JSON array.")
    return (_mapping(item, label) for item in value)


def _read_json(content, label):
    return _mapping(json.loads(content.decode("utf-8-sig"), object_pairs_hook=_object,
                               parse_constant=_non_json_constant), label)


def _digest(value, pattern, label):
    if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
        raise ExportError(f"{label} is missing or is not a valid hexadecimal identifier.")
    return value.lower()


def _files(run):
    files = _mapping(run.get("files"), "Run files")
    by_name = {}
    names = set()
    for path, contents in files.items():
        parts = path.split("/")
        if any(
            not part or part in (".", "..") or part[-1] in (" ", ".")
            or re.search(r'[<>:"\\|?*\x00-\x1f]', part)
            for part in parts
        ):
            raise ExportError("An embedded artifact has an unsafe path.")
        name = parts[-1]
        if name.casefold() in names:
            raise ExportError("Two embedded artifacts have the same download filename.")
        if not isinstance(contents, str):
            raise ExportError("Embedded artifact contents must be text.")
        names.add(name.casefold())
        by_name[name] = contents
    return by_name


def _companion(path, label):
    if not path.is_file():
        raise ExportError(f"{label} must be a readable regular file.")
    return path.read_bytes()


def _artifact_from_dir(root, name):
    if not root.is_dir():
        raise ExportError("The artifacts location must be a directory.")
    artifact = (root / name).resolve()
    if not artifact.is_relative_to(root):
        raise ExportError("An artifact path leaves the supplied directory.")
    return _companion(artifact, f"Artifact {name}")


def _check_markdown(content, revision, source_hash, files):
    text = content.decode("utf-8-sig")
    lines = text.replace("\r\n", "\n").split("\n")
    header = []
    for line in lines:
        if not line.startswith("> "):
            break
        header.append(line)
    for label, expected in (
        ("Canonical implementation", revision), ("Source SHA-256", source_hash)
    ):
        prefix = f"> {label}: "
        values = [line.removeprefix(prefix).lower() for line in header if line.startswith(prefix)]
        if values != [expected]:
            raise ExportError(f"Markdown header does not match the package {label}.")
    markdown = [contents for name, contents in files.items() if name.endswith(".laif.md")]
    if not markdown:
        return "HEADER_MATCH_ONLY"
    if len(markdown) != 1 or markdown[0].replace("\r\n", "\n") not in "\n".join(lines[len(header):]):
        raise ExportError("The full report Markdown does not contain the embedded assessment body.")
    return "HEADER_AND_EMBEDDED_BODY_MATCH"


def _check_shared_extraction(run, source_hash, files):
    checks = run.get("checks")
    if not isinstance(checks, dict) or "shared_extraction_match" not in checks:
        return "NOT_RECORDED", 0
    if run["kind"] != "browser_pipeline" or checks["shared_extraction_match"] is not True:
        raise ExportError("The shared extraction check is invalid for this assessment.")
    text = run.get("extractedText")
    if not isinstance(text, str):
        raise ExportError("The shared extraction must include the exact extracted text.")
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    artifacts = {}
    for key, suffix in (("payload", ".laif.json"), ("research", ".research_data.json"),
                        ("bundle", "analyst_bundle.json")):
        copies = [value for name, value in files.items() if name.endswith(suffix)]
        artifact = _mapping(run.get(key), f"Shared extraction {key}")
        if len(copies) != 1 or _read_json(copies[0].encode("utf-8"), key) != artifact:
            raise ExportError(f"The run's {key} differs from its individual artifact.")
        artifacts[key] = artifact
    payload, research, bundle = (artifacts[key] for key in ("payload", "research", "bundle"))
    processing = _mapping(payload.get("processing_metadata"), "Processing metadata")
    research_source = _mapping(research.get("source"), "Research source")
    if any(data.get("source_sha256") != source_hash for data in (processing, research_source)):
        raise ExportError("Report and research source identities differ from the run.")
    assessment = _mapping(payload.get("assessment_result"), "Assessment result")
    methods = [_mapping(data.get("automatic_criteria"), "Automatic documentary checks")
               for data in (assessment, research)]
    if any(data.get("extracted_text_sha256") != text_hash for data in (research_source, *methods)):
        raise ExportError("Report and research extraction identities differ from the retained text.")
    method_hash = _digest(methods[0].get("method_sha256"), r"[0-9a-f]{64}", "Automatic method SHA-256")
    if methods[1].get("method_sha256") != method_hash:
        raise ExportError("Report and research automatic methods differ.")

    def exact_quote(record, start_field, end_field):
        start, end = record.get(start_field), record.get(end_field)
        quote = record.get("exact_quote")
        if (type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text)
                or not isinstance(quote, str) or text[start:end] != quote):
            raise ExportError("An evidence quotation differs from the retained extracted text.")
        return start, end, quote

    quote_bank = list(_records(bundle.get("quote_bank"), "Analyst quote bank"))
    for record in quote_bank:
        exact_quote(record, "start_offset", "end_offset")
        if record.get("source_sha256") != source_hash:
            raise ExportError("An analyst quotation names a different source.")
    witnesses = set()
    for method in methods:
        for criterion in _records(method.get("criteria"), "Automatic criteria"):
            for component in _records(criterion.get("components"), "Criterion components"):
                for witness in _records(component.get("witnesses"), "Component witnesses"):
                    span = exact_quote(witness, "start_char", "end_char")
                    if hashlib.sha256(span[2].encode("utf-8")).hexdigest() != witness.get("quote_sha256"):
                        raise ExportError("An automatic quotation does not match its SHA-256.")
                    witnesses.add(span)
    count = len(quote_bank) + len(witnesses)
    if type(checks.get("quotes_checked")) is not int or checks["quotes_checked"] != count:
        raise ExportError("The recorded quote count differs from the verified spans.")
    return "MATCH", count


def _check_run_receipt(run, source_hash):
    files = run["files"]
    paths = [path for path in files if path.endswith(RUN_RECEIPT_SUFFIX)]
    checks = run.get("checks")
    recorded = isinstance(checks, dict) and "assessment_receipt_match" in checks
    if not paths and not recorded:
        return "NOT_RECORDED", 0
    if (run["kind"] != "browser_pipeline" or len(paths) != 1
            or not recorded or checks["assessment_receipt_match"] is not True):
        raise ExportError("A completed browser assessment must carry one verified assessment receipt.")
    path = paths[0]
    receipt = _read_json(files[path].encode("utf-8"), "Assessment receipt")
    if receipt.get("source_sha256") != source_hash:
        raise ExportError("Assessment receipt names a different source.")

    def contents(relative):
        if relative not in files:
            raise ExportError(f"Missing embedded assessment artifact: {relative}.")
        return files[relative].encode("utf-8")

    def identity(relative):
        data = contents(relative)
        return len(data), hashlib.sha256(data).hexdigest()

    try:
        check_assessment_receipt(path, receipt, identity, lambda relative: _read_json(contents(relative), "Analyst bundle"))
    except ExtractionError as exc:
        raise ExportError(str(exc)) from exc
    count = len(receipt["artifacts"])
    if type(checks.get("assessment_artifacts_checked")) is not int or checks["assessment_artifacts_checked"] != count:
        raise ExportError("The recorded assessment receipt file count differs from the verified inventory.")
    return "MATCH", count


def _check_package(package, *, source=None, report_bytes=None, read_artifact=None):
    if package.get("workspace_export_schema") != "laif.workspace-export.v1":
        raise ExportError("Choose a JSON package from Workspace Reports & export.")
    run = _mapping(package.get("run"), "Assessment run")
    if not isinstance(run.get("id"), str) or not run["id"].strip():
        raise ExportError("Assessment run ID is missing.")
    if run.get("kind") not in ("browser_pipeline", "imported_authored"):
        raise ExportError("Assessment run kind is unrecognised.")
    revision_pattern = r"[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?"
    revision = _digest(run.get("revision"), revision_pattern, "Run revision")
    if _digest(package.get("canonical_revision"), revision_pattern, "Package revision") != revision:
        raise ExportError("Package and assessment revisions differ.")
    source_hash = _digest(run.get("sourceSha256"), r"[0-9a-fA-F]{64}", "Run source SHA-256")
    metadata = package.get("source_metadata")
    if metadata is not None:
        metadata = _mapping(metadata, "Source metadata")
        if _digest(metadata.get("sha256"), r"[0-9a-fA-F]{64}", "Metadata source SHA-256") != source_hash:
            raise ExportError("Package and assessment source hashes differ.")
        if not metadata.get("id") or metadata["id"] != run.get("documentId"):
            raise ExportError("Package source ID differs from the assessment source ID.")
    if "report_quality_review" in package and package["report_quality_review"] != run.get("review"):
        raise ExportError("Package and assessment operator review records differ.")
    files = _files(run)
    if run["kind"] == "browser_pipeline" and sum(name.endswith(".laif.md") for name in files) != 1:
        raise ExportError("An automated assessment must contain one embedded full report.")
    extraction_status, quote_count = _check_shared_extraction(run, source_hash, files)
    receipt_status, receipt_count = _check_run_receipt(run, source_hash)
    source_status = "NOT_REQUESTED"
    if source is not None:
        if not source.is_file():
            raise ExportError("Source must be a readable regular file.")
        digest = hashlib.sha256()
        with source.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != source_hash:
            raise ExportError("Supplied source bytes differ from the assessment source hash.")
        source_status = "SOURCE_BYTES_MATCH"
    markdown_status = (_check_markdown(report_bytes, revision, source_hash, files)
                       if report_bytes is not None else "NOT_REQUESTED")
    if read_artifact is not None:
        if not files:
            raise ExportError("This export contains no embedded artifacts to compare.")
        for name, contents in files.items():
            if read_artifact(name) != contents.encode("utf-8"):
                raise ExportError(f"Artifact bytes differ: {name}.")
    return {
        "assessment_id": run["id"],
        "assessment_kind": run["kind"],
        "method_revision": revision,
        "source_sha256": source_hash,
        "source_metadata": "MATCH" if metadata is not None else "NOT_INCLUDED",
        "source_file": source_status,
        "markdown_report": markdown_status,
        "shared_extraction": extraction_status,
        "quotation_spans_verified": quote_count,
        "assessment_receipt": receipt_status,
        "assessment_receipt_files_verified": receipt_count,
        "embedded_artifacts": len(files),
        "artifact_files_verified": len(files) if read_artifact is not None else 0,
        "scope": "Package identity and supplied file checks only. Review conclusions and source authority require separate evidence.",
    }


def check_export(path, *, source=None, report=None, artifacts_dir=None):
    """Check a JSON export and any explicitly supplied companion files."""
    package = _read_json(_companion(path, "Workspace package"), "Workspace package")
    root = artifacts_dir.resolve() if artifacts_dir is not None else None
    return _check_package(package, source=source,
                          report_bytes=_companion(report, "Markdown report") if report else None,
                          read_artifact=(lambda name: _artifact_from_dir(root, name)) if root else None)


def check_review_bundle(path, *, source=None):
    """Verify a Workspace review ZIP in place without extracting it."""
    if not path.is_file():
        raise ExportError("Review ZIP must be a readable regular file.")
    if path.stat().st_size > _ARCHIVE_LIMIT:
        raise ExportError("Review ZIP exceeds the Workspace archive size limit.")
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        names = {entry.filename for entry in entries}
        if len(entries) > _ENTRY_LIMIT or sum(entry.file_size for entry in entries) > _BUNDLE_LIMIT:
            raise ExportError("Review ZIP exceeds the Workspace bundle limits.")
        if len({name.casefold() for name in names}) != len(entries) or any(
            entry.is_dir() or stat.S_ISLNK(entry.external_attr >> 16)
            or entry.flag_bits & 1 or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
            for entry in entries
        ):
            raise ExportError("Review ZIP contains duplicate or unsupported entries.")
        core = {"START-HERE.txt", "assessment.laif.json", "report.laif.md"}
        if not (core | {"manifest.json"}) <= names:
            raise ExportError("Choose a complete review ZIP from Workspace Reports & export.")
        manifest = _read_json(archive.read("manifest.json"), "Review ZIP manifest")
        if manifest.get("schema") != "laif.workspace-review-bundle.v1":
            raise ExportError("Choose a review ZIP from Workspace Reports & export.")
        package = _read_json(archive.read("assessment.laif.json"), "Workspace package")
        run = _mapping(package.get("run"), "Assessment run")
        files = _files(run)
        if run.get("kind") == "browser_pipeline":
            core.add("review-brief.md")
        expected = core | {f"files/{name}" for name in files}
        inventory = _mapping(manifest.get("files"), "Review ZIP inventory")
        if names != expected | {"manifest.json"} or set(inventory) != expected:
            raise ExportError("Review ZIP inventory differs from the files required for this assessment.")
        for name in sorted(expected):
            info = _mapping(inventory[name], f"Inventory record for {name}")
            data = archive.read(name)
            if (type(info.get("bytes")) is not int or len(data) != info["bytes"]
                    or hashlib.sha256(data).hexdigest() != info.get("sha256")):
                raise ExportError(f"Review ZIP file differs from its manifest: {name}.")
        for key, value in (("assessment_id", run.get("id")), ("canonical_revision", run.get("revision")),
                           ("source_sha256", run.get("sourceSha256")), ("exported_at", package.get("exportedAt"))):
            if not isinstance(value, str) or not value or manifest.get(key) != value:
                raise ExportError(f"Review ZIP identity differs from the assessment package: {key}.")
        result = _check_package(package, source=source, report_bytes=archive.read("report.laif.md"),
                                read_artifact=(lambda name: archive.read(f"files/{name}")) if files else None)
        return {**result, "bundle_files_verified": len(expected)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="review ZIP or JSON export from Workspace")
    parser.add_argument("--source", type=Path, help="original source file to hash")
    parser.add_argument("--report", type=Path, help="downloaded Full report Markdown")
    parser.add_argument("--artifacts-dir", type=Path, help="directory of downloaded individual artifacts")
    args = parser.parse_args(argv)
    try:
        if args.package.suffix.lower() == ".zip":
            if args.report or args.artifacts_dir:
                parser.error("A review ZIP already supplies the report and artifacts.")
            result = check_review_bundle(args.package, source=args.source)
        else:
            result = check_export(args.package, source=args.source, report=args.report, artifacts_dir=args.artifacts_dir)
    except (OSError, ValueError, RuntimeError, EOFError, zipfile.BadZipFile, zlib.error) as error:
        print(f"CHECK FAILED: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
