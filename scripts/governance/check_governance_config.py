#!/usr/bin/env python3
"""Validate the deterministic LAIF governance path configuration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("protected_paths.json")
CHECK_NAME = "governance_config"
REQUIRED_KEYS = (
    "protected_artifacts",
    "semantic_sensitive_files",
    "semantic_sensitive_terms",
)


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
            fail(f"'{key}' entry {index} must not contain leading or trailing whitespace")
        if item in seen:
            fail(f"'{key}' contains duplicate entry: {item}")
        seen.add(item)
    return value


def validate_path_list(config: dict, key: str) -> None:
    for index, item in enumerate(validate_string_list(config, key)):
        if item.startswith("/"):
            fail(f"'{key}' entry {index} must be repository-relative, not absolute")
        if "\\" in item:
            fail(f"'{key}' entry {index} must use forward slashes")


def validate_term_list(config: dict, key: str) -> None:
    validate_string_list(config, key)


def load_config(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except FileNotFoundError:
        fail(f"missing config file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"malformed JSON in {path}: {exc}")

    if not isinstance(config, dict):
        fail("top-level config must be a JSON object")
    return config


def validate_config(config: dict) -> None:
    for key in REQUIRED_KEYS:
        if key not in config:
            fail(f"missing required key: '{key}'")

    validate_path_list(config, "protected_artifacts")
    validate_path_list(config, "semantic_sensitive_files")
    validate_term_list(config, "semantic_sensitive_terms")

    protected = config["protected_artifacts"]
    if not protected:
        fail("'protected_artifacts' must contain at least one path")


def main() -> int:
    config = load_config(CONFIG_PATH)
    validate_config(config)
    emit(
        "PASS",
        "governance config valid",
        config_path=str(CONFIG_PATH),
        protected_artifacts=len(config["protected_artifacts"]),
        semantic_sensitive_files=len(config["semantic_sensitive_files"]),
        semantic_sensitive_terms=len(config["semantic_sensitive_terms"]),
    )
    print("SUMMARY: governance config valid; deterministic path and term lists are well formed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
