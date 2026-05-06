#!/usr/bin/env python3
"""Validate the deterministic LAIF governance path configuration."""

from __future__ import annotations

from pathlib import Path

from governance_lib import CONFIG_PATH, fail as governance_fail, load_json_config

REQUIRED_KEYS = (
    "protected_artifacts",
    "semantic_sensitive_files",
    "semantic_sensitive_terms",
)
REQUIRED_GOVERNANCE_SENSITIVE_PATHS = {
    "scripts/governance/check_governance_config.py",
    "scripts/governance/check_protected_artifacts.py",
    "scripts/governance/check_semantic_boundaries.py",
    "scripts/governance/governance_lib.py",
    "scripts/governance/protected_paths.json",
}


def fail(message: str) -> None:
    governance_fail("GOVERNANCE CONFIG ERROR", message)


def validate_string_list(config: dict, key: str) -> list[str]:
    value = config.get(key)

    if not isinstance(value, list):
        fail(f"'{key}' must be a list")

    seen = set()

    for index, item in enumerate(value):
        if not isinstance(item, str):
            fail(f"'{key}' entry {index} must be a string")

        if not item:
            fail(f"'{key}' entry {index} must not be empty")

        if item != item.strip():
            fail(
                f"'{key}' entry {index} must not contain leading or trailing whitespace"
            )

        if item in seen:
            fail(f"'{key}' contains duplicate entry: {item}")

        seen.add(item)

    return value


def validate_path_list(config: dict, key: str) -> None:
    repo_root = CONFIG_PATH.parents[2]

    for index, item in enumerate(validate_string_list(config, key)):
        if item.startswith("/"):
            fail(f"'{key}' entry {index} must be repository-relative, not absolute")

        if "\\" in item:
            fail(f"'{key}' entry {index} must use forward slashes")

        if not (repo_root / item).exists():
            fail(f"'{key}' entry {index} does not exist: {item}")


def validate_term_list(config: dict, key: str) -> None:
    validate_string_list(config, key)


def load_config(path: Path) -> dict:
    return load_json_config("GOVERNANCE CONFIG ERROR", path)


def validate_config(config: dict) -> None:
    for key in REQUIRED_KEYS:
        if key not in config:
            fail(f"missing required key: '{key}'")

    validate_path_list(config, "protected_artifacts")
    validate_path_list(config, "semantic_sensitive_files")
    validate_term_list(config, "semantic_sensitive_terms")

    protected = config["protected_artifacts"]
    sensitive_files = set(config["semantic_sensitive_files"])

    if not protected:
        fail("'protected_artifacts' must contain at least one path")

    missing_governance_paths = sorted(
        REQUIRED_GOVERNANCE_SENSITIVE_PATHS - sensitive_files
    )
    if missing_governance_paths:
        fail(
            "'semantic_sensitive_files' must include governance check paths: "
            + ", ".join(missing_governance_paths)
        )


def main() -> int:
    config = load_config(CONFIG_PATH)

    validate_config(config)

    print(f"Governance config valid: {CONFIG_PATH}")
    print(f"Protected artifact paths: {len(config['protected_artifacts'])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
