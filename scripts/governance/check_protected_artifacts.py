#!/usr/bin/env python3
"""Fail when protected LAIF assessment artifacts appear in a PR diff.

This check is intentionally path-level only. It does not inspect semantics,
content, ASTs, hashes, or generated report meaning.
"""

from __future__ import annotations

import sys

from governance_lib import (
    CONFIG_PATH,
    changed_files_from_merge_base,
    fail as governance_fail,
    load_json_config,
    merge_base_for,
    require_base_ref_or_skip,
)


def fail(message: str) -> None:
    governance_fail("PROTECTED ARTIFACT CHECK FAILED", message)


def load_protected_paths() -> set[str]:
    config = load_json_config("PROTECTED ARTIFACT CHECK FAILED", CONFIG_PATH)

    artifacts = config.get("protected_artifacts")
    if not isinstance(artifacts, list) or not all(isinstance(item, str) for item in artifacts):
        fail("governance config must define protected_artifacts as a list of strings")
    return set(artifacts)


def changed_files_against_base(base_ref: str) -> set[str]:
    merge_base = merge_base_for(base_ref, "PROTECTED ARTIFACT CHECK FAILED")
    return changed_files_from_merge_base(merge_base, "PROTECTED ARTIFACT CHECK FAILED")


def main() -> int:
    protected_paths = load_protected_paths()
    base_ref = require_base_ref_or_skip("protected artifact drift check")

    if base_ref is None:
        return 0

    changed_files = changed_files_against_base(base_ref)
    protected_changes = sorted(changed_files & protected_paths)

    if protected_changes:
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

    print("No protected artifact paths changed relative to PR base.")
    print(f"Checked protected artifact paths: {len(protected_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
