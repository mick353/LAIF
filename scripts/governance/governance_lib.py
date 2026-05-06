"""Shared deterministic helpers for LAIF governance checks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).with_name("protected_paths.json")


def fail(prefix: str, message: str) -> None:
    """Print a namespaced governance error and stop the check."""

    print(f"{prefix}: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_git(args: list[str], error_prefix: str) -> str:
    """Run a git command and return stdout, failing with deterministic output."""

    completed = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(error_prefix, f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def load_json_config(error_prefix: str, path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load the governance JSON config as an object."""

    try:
        with path.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except FileNotFoundError:
        fail(error_prefix, f"missing governance config: {path}")
    except json.JSONDecodeError as exc:
        fail(error_prefix, f"malformed governance config: {exc}")

    if not isinstance(config, dict):
        fail(error_prefix, "top-level governance config must be a JSON object")

    return config


def resolve_base_ref() -> str | None:
    """Resolve the comparison base for PR-aware governance checks."""

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


def require_base_ref_or_skip(check_name: str) -> str | None:
    """Return a base ref, fail in PR CI if absent, or allow local skip."""

    base_ref = resolve_base_ref()
    if base_ref is not None:
        return base_ref

    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    if event_name == "pull_request":
        fail(
            f"{check_name} ERROR",
            "pull_request CI context did not provide a base ref; set GOVERNANCE_BASE_REF, GITHUB_EVENT_PATH, or GITHUB_BASE_REF",
        )

    print(f"No PR base ref detected; {check_name} skipped.")
    print("Set GITHUB_BASE_REF or GOVERNANCE_BASE_REF to enable deterministic diff detection.")
    return None


def merge_base_for(base_ref: str, error_prefix: str) -> str:
    """Return the merge base for base_ref and HEAD."""

    merge_base = run_git(["merge-base", base_ref, "HEAD"], error_prefix).strip()
    if not merge_base:
        fail(error_prefix, f"could not determine merge base for {base_ref}")
    return merge_base


def changed_files_from_merge_base(merge_base: str, error_prefix: str) -> set[str]:
    """Return repository-relative changed file paths since merge_base."""

    output = run_git(["diff", "--name-only", f"{merge_base}...HEAD"], error_prefix)
    return {line for line in output.splitlines() if line}
