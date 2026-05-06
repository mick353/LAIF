#!/usr/bin/env python3
"""Fail when protected LAIF assessment artifacts appear in a PR diff.

This check is intentionally path-level only. It does not inspect semantics,
content, ASTs, hashes, or generated report meaning.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("protected_paths.json")
CHECK_NAME = "protected_artifacts"


def emit(status: str, message: str, **fields: object) -> None:
    """Emit a stable human- and machine-readable governance result line."""
    parts = [f"GOVERNANCE_RESULT status={status}", f"check={CHECK_NAME}", f"message={json.dumps(message, sort_keys=True)}"]
    for key in sorted(fields):
        parts.append(f"{key}={json.dumps(fields[key], sort_keys=True)}")
    print(" ".join(parts))


def fail(message: str) -> None:
    emit("ERROR", message)
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_git(args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def load_protected_paths() -> set[str]:
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except FileNotFoundError:
        fail(f"missing governance config: {CONFIG_PATH}")
    except json.JSONDecodeError as exc:
        fail(f"malformed governance config: {exc}")

    artifacts = config.get("protected_artifacts")
    if not isinstance(artifacts, list) or not all(isinstance(item, str) for item in artifacts):
        fail("governance config must define protected_artifacts as a list of strings")
    return set(artifacts)


def resolve_base_ref() -> str | None:
    explicit = os.environ.get("GOVERNANCE_BASE_REF")
    if explicit:
        return explicit

    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path:
        try:
            with Path(event_path).open("r", encoding="utf-8") as handle:
                event = json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError):
            event = {}
        base_sha = event.get("pull_request", {}).get("base", {}).get("sha")
        if base_sha:
            return base_sha

    github_base = os.environ.get("GITHUB_BASE_REF")
    if github_base:
        return f"origin/{github_base}"

    return None


def changed_files_against_base(base_ref: str) -> set[str]:
    merge_base = run_git(["merge-base", base_ref, "HEAD"])
    if not merge_base:
        fail(f"could not determine merge base for {base_ref}")

    output = run_git(["diff", "--name-only", f"{merge_base}...HEAD"])
    return {line for line in output.splitlines() if line}


def main() -> int:
    protected_paths = load_protected_paths()
    base_ref = resolve_base_ref()

    if base_ref is None:
        emit("WARN", "protected artifact drift check skipped; no PR base ref detected", protected_artifacts=len(protected_paths))
        print("SUMMARY: no PR base ref detected; set GITHUB_BASE_REF or GOVERNANCE_BASE_REF to enable path-level drift detection.")
        return 0

    changed_files = changed_files_against_base(base_ref)
    protected_changes = sorted(changed_files & protected_paths)

    if protected_changes:
        emit("ERROR", "protected artifact path-level drift detected", changed_paths=protected_changes, protected_artifacts=len(protected_paths))
        print("Protected LAIF assessment artifact drift detected.", file=sys.stderr)
        print("The following protected artifact path(s) appear in this PR diff:", file=sys.stderr)
        for path in protected_changes:
            print(f"  - {path}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Governance guidance:", file=sys.stderr)
        print("  * Do not modify protected assessment artifacts in this PR.", file=sys.stderr)
        print("  * Revert the protected artifact path-level changes before merging.", file=sys.stderr)
        print("  * This check is deterministic and path-level only; it performs no semantic interpretation.", file=sys.stderr)
        return 1

    emit("PASS", "no protected artifact paths changed", checked_changed_files=len(changed_files), protected_artifacts=len(protected_paths))
    print("SUMMARY: no protected artifact paths changed relative to PR base.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
