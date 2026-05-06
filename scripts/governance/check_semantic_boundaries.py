#!/usr/bin/env python3
"""Advisory semantic-boundary governance signal for configured paths and terms.

This check is intentionally conservative. It inspects only configured files,
changed hunk lines, and explicitly configured terms. It does not perform
semantic interpretation, AST analysis, fuzzy matching, synonym inference,
semantic scoring, or proof of semantic drift.
"""

from __future__ import annotations

from dataclasses import dataclass

from governance_lib import (
    CONFIG_PATH,
    changed_files_from_merge_base,
    fail as governance_fail,
    load_json_config,
    merge_base_for,
    require_base_ref_or_skip,
    run_git as governance_run_git,
)


@dataclass(frozen=True)
class Match:
    path: str
    hunk: str
    line_type: str
    term: str
    line: str


def fail(message: str) -> None:
    governance_fail("SEMANTIC BOUNDARY CHECK ERROR", message)


def run_git(args: list[str]) -> str:
    return governance_run_git(args, "SEMANTIC BOUNDARY CHECK ERROR")


def load_config() -> tuple[set[str], list[str]]:
    config = load_json_config("SEMANTIC BOUNDARY CHECK ERROR", CONFIG_PATH)

    files = config.get("semantic_sensitive_files")
    terms = config.get("semantic_sensitive_terms")
    if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
        fail("governance config must define semantic_sensitive_files as a list of strings")
    if not isinstance(terms, list) or not all(isinstance(item, str) for item in terms):
        fail("governance config must define semantic_sensitive_terms as a list of strings")
    return set(files), terms


def changed_files(merge_base: str) -> set[str]:
    return changed_files_from_merge_base(merge_base, "SEMANTIC BOUNDARY CHECK ERROR")


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
    base_ref = require_base_ref_or_skip("semantic-boundary check")

    if base_ref is None:
        return 0

    merge_base = merge_base_for(base_ref, "SEMANTIC BOUNDARY CHECK ERROR")
    changed_sensitive_files = sorted(changed_files(merge_base) & sensitive_files)

    if not changed_sensitive_files:
        print("No configured semantic-sensitive files changed relative to PR base.")
        print(f"Configured semantic-sensitive files: {len(sensitive_files)}")
        print(f"Configured semantic-sensitive terms: {len(sensitive_terms)}")
        return 0

    matches: list[Match] = []
    for path in changed_sensitive_files:
        matches.extend(changed_hunk_matches(merge_base, path, sensitive_terms))

    if matches:
        print_guidance(matches)
    else:
        print("Configured semantic-sensitive files changed, but no configured terms were touched in changed hunk lines.")
        print("This advisory check performed no semantic interpretation.")
        print(f"Changed configured semantic-sensitive files: {len(changed_sensitive_files)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
