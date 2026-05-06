#!/usr/bin/env python3
"""Advisory semantic-boundary governance signal for configured paths and terms.

This check is intentionally conservative. It inspects only configured files,
changed hunk lines, and explicitly configured terms. It does not perform
semantic interpretation, AST analysis, fuzzy matching, synonym inference,
semantic scoring, or proof of semantic drift.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("protected_paths.json")
CHECK_NAME = "semantic_boundaries"


def emit(status: str, message: str, **fields: object) -> None:
    """Emit a stable human- and machine-readable governance result line."""
    parts = [f"GOVERNANCE_RESULT status={status}", f"check={CHECK_NAME}", f"message={json.dumps(message, sort_keys=True)}"]
    for key in sorted(fields):
        parts.append(f"{key}={json.dumps(fields[key], sort_keys=True)}")
    print(" ".join(parts))


@dataclass(frozen=True)
class Match:
    path: str
    hunk: str
    line_type: str
    term: str
    line: str


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
    return completed.stdout


def load_config() -> tuple[set[str], list[str]]:
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except FileNotFoundError:
        fail(f"missing governance config: {CONFIG_PATH}")
    except json.JSONDecodeError as exc:
        fail(f"malformed governance config: {exc}")

    files = config.get("semantic_sensitive_files")
    terms = config.get("semantic_sensitive_terms")
    if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
        fail("governance config must define semantic_sensitive_files as a list of strings")
    if not isinstance(terms, list) or not all(isinstance(item, str) for item in terms):
        fail("governance config must define semantic_sensitive_terms as a list of strings")
    return set(files), terms


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


def merge_base_for(base_ref: str) -> str:
    merge_base = run_git(["merge-base", base_ref, "HEAD"]).strip()
    if not merge_base:
        fail(f"could not determine merge base for {base_ref}")
    return merge_base


def changed_files(merge_base: str) -> set[str]:
    output = run_git(["diff", "--name-only", f"{merge_base}...HEAD"])
    return {line for line in output.splitlines() if line}


def changed_hunk_matches(merge_base: str, path: str, terms: list[str]) -> list[Match]:
    diff = run_git(["diff", "--unified=0", f"{merge_base}...HEAD", "--", path])
    matches: list[Match] = []
    current_hunk = "(no hunk header)"

    for raw_line in diff.splitlines():
        if raw_line.startswith("@@"):
            current_hunk = raw_line
            continue
        if raw_line.startswith(("+++", "---")):
            continue
        if raw_line.startswith("+"):
            line_type = "added"
            content = raw_line[1:]
        elif raw_line.startswith("-"):
            line_type = "removed"
            content = raw_line[1:]
        else:
            continue

        for term in terms:
            if term in content:
                matches.append(Match(path, current_hunk, line_type, term, content))
    return matches


def print_guidance(matches: list[Match]) -> None:
    print("Semantic-boundary governance notice.")
    print("This is a governance signal only.")
    print("This is not a semantic interpretation and is not proof of semantic drift.")
    print("Detection method: configured path + changed hunk line + exact configured term match.")
    print("Mode: advisory/warn only; this check does not block merges.")
    print("")
    print("Matched semantic-sensitive changed lines:")
    for match in matches:
        print(f"  - file: {match.path}")
        print(f"    hunk: {match.hunk}")
        print(f"    line_type: {match.line_type}")
        print(f"    term: {match.term}")
        print(f"    line: {match.line}")
    print("")
    print("Governance guidance:")
    print("  * Review the highlighted hunk(s) for intentional governance-sensitive edits.")
    print("  * Do not treat this notice as a semantic verdict.")
    print("  * No AST analysis, synonym inference, fuzzy matching, LLM analysis, or semantic scoring was performed.")


def main() -> int:
    sensitive_files, sensitive_terms = load_config()
    base_ref = resolve_base_ref()

    if base_ref is None:
        emit("WARN", "semantic-boundary check skipped; no PR base ref detected", semantic_sensitive_files=len(sensitive_files), semantic_sensitive_terms=len(sensitive_terms))
        print("SUMMARY: no PR base ref detected; set GITHUB_BASE_REF or GOVERNANCE_BASE_REF to enable advisory hunk-level detection.")
        return 0

    merge_base = merge_base_for(base_ref)
    changed_sensitive_files = sorted(changed_files(merge_base) & sensitive_files)

    if not changed_sensitive_files:
        emit("PASS", "no configured semantic-sensitive files changed", semantic_sensitive_files=len(sensitive_files), semantic_sensitive_terms=len(sensitive_terms))
        print("SUMMARY: no configured semantic-sensitive files changed relative to PR base.")
        return 0

    matches: list[Match] = []
    for path in changed_sensitive_files:
        matches.extend(changed_hunk_matches(merge_base, path, sensitive_terms))

    if matches:
        emit("WARN", "semantic-sensitive term touched in changed hunk lines", changed_sensitive_files=changed_sensitive_files, matches=len(matches))
        print_guidance(matches)
    else:
        emit("PASS", "configured semantic-sensitive files changed without configured term touches", changed_sensitive_files=len(changed_sensitive_files))
        print("SUMMARY: configured semantic-sensitive files changed, but no configured terms were touched in changed hunk lines.")
        print("This advisory check performed no semantic interpretation.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
