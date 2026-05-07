#!/usr/bin/env python3
"""Deterministic read-only governance status reporter for LAIF."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from governance_lib import load_json_config

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_RELATIVE_PATH = "scripts/governance/protected_paths.json"
KEY_GOVERNANCE_SCRIPTS = [
    "scripts/governance/check_governance_config.py",
    "scripts/governance/check_protected_artifacts.py",
    "scripts/governance/check_semantic_boundaries.py",
    "scripts/governance/governance_lib.py",
    "scripts/governance/governance_status.py",
]
TEST_GOVERNANCE_PATH = "tests/test_governance.py"
CI_WORKFLOW_PATH = ".github/workflows/ci.yml"


def _as_list(config: dict, key: str) -> list[str]:
    values = config.get(key, [])
    if not isinstance(values, list):
        return []
    return [str(value) for value in values]


def _print_counted_section(title: str, values: Iterable[str]) -> None:
    items = list(values)
    print(f"{title}: {len(items)}")
    for item in items:
        print(f"  - {item}")


def _exists(relative_path: str) -> str:
    return "yes" if (REPO_ROOT / relative_path).is_file() else "no"


def main() -> int:
    config = load_json_config("GOVERNANCE STATUS ERROR")
    protected_artifacts = _as_list(config, "protected_artifacts")
    semantic_sensitive_files = _as_list(config, "semantic_sensitive_files")
    semantic_sensitive_terms = _as_list(config, "semantic_sensitive_terms")

    print("LAIF Governance Status")
    print("======================")
    print(f"Config: {CONFIG_RELATIVE_PATH}")
    print()

    _print_counted_section("Protected artifact count", protected_artifacts)
    print()
    _print_counted_section("Semantic-sensitive file count", semantic_sensitive_files)
    print()
    _print_counted_section("Semantic-sensitive term count", semantic_sensitive_terms)
    print()

    print("Governance script presence:")
    for script in KEY_GOVERNANCE_SCRIPTS:
        print(f"  - {script}: {_exists(script)}")
    print(f"Test coverage file present: {TEST_GOVERNANCE_PATH}: {_exists(TEST_GOVERNANCE_PATH)}")
    print(f"CI workflow present: {CI_WORKFLOW_PATH}: {_exists(CI_WORKFLOW_PATH)}")
    print()

    print("Governance assumptions:")
    print("  - Semantic-boundary checks are advisory-only and do not block merges.")
    print("  - Protected-artifact checks are blocking and fail on protected artifact drift.")
    print(
        "  - This status tool is read-only and does not alter LAIF scoring, "
        "assessment semantics, generated reports, or verified-corpus manifests."
    )
    print("  - The status report does not depend on branch names, network access, or GitHub UI state.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
