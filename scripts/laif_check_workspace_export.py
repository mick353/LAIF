#!/usr/bin/env python3
"""Check a private LAIF Workspace export locally without changing its files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


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


def _check_artifacts(files, artifact_dir):
    if not files:
        raise ExportError("This export contains no embedded artifacts to compare.")
    root = artifact_dir.resolve(strict=True)
    if not root.is_dir():
        raise ExportError("The artifacts location must be a directory.")
    for name, contents in files.items():
        artifact = (root / name).resolve()
        if not artifact.is_relative_to(root):
            raise ExportError("An artifact path leaves the supplied directory.")
        if _companion(artifact, f"Artifact {name}") != contents.encode("utf-8"):
            raise ExportError(f"Artifact bytes differ: {name}.")


def _check_markdown(path, revision, source_hash, files):
    text = _companion(path, "Markdown report").decode("utf-8-sig")
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


def check_export(path, *, source=None, report=None, artifacts_dir=None):
    """Check package identity and any explicitly supplied file bytes."""
    package = _mapping(
        json.loads(
            _companion(path, "Workspace package").decode("utf-8-sig"),
            object_pairs_hook=_object, parse_constant=_non_json_constant,
        ),
        "Workspace package",
    )
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
    markdown_status = _check_markdown(report, revision, source_hash, files) if report else "NOT_REQUESTED"
    if artifacts_dir is not None:
        _check_artifacts(files, artifacts_dir)
    return {
        "assessment_id": run["id"],
        "assessment_kind": run["kind"],
        "method_revision": revision,
        "source_sha256": source_hash,
        "source_metadata": "MATCH" if metadata is not None else "NOT_INCLUDED",
        "source_file": source_status,
        "markdown_report": markdown_status,
        "embedded_artifacts": len(files),
        "artifact_files_verified": len(files) if artifacts_dir is not None else 0,
        "scope": "Package identity and supplied file checks only. Review conclusions and source authority require separate evidence.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="JSON package exported from Workspace")
    parser.add_argument("--source", type=Path, help="original source file to hash")
    parser.add_argument("--report", type=Path, help="downloaded Full report Markdown")
    parser.add_argument("--artifacts-dir", type=Path, help="directory of downloaded individual artifacts")
    args = parser.parse_args(argv)
    try:
        result = check_export(args.package, source=args.source, report=args.report, artifacts_dir=args.artifacts_dir)
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        print(f"CHECK FAILED: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
