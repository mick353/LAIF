#!/usr/bin/env python3
"""Run LAIF's complete repository verification gate without GitHub Actions.

This uses the same governance, validation, adversarial, provenance, processing,
and deterministic-report checks as the existing GitHub workflow. Only Python,
Git, the checked-out repository, and locally installed test dependencies are
needed. Run from a clean, committed checkout to make the diff gate meaningful.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

CHECKS = (
    ("Compile governance scripts", (
        PYTHON, "-m", "py_compile",
        *(str(path.relative_to(ROOT)) for path in sorted((ROOT / "scripts" / "governance").glob("*.py"))),
    )),
    ("Validate governance config", (PYTHON, "-B", "scripts/governance/check_governance_config.py")),
    ("Check protected artifacts", (PYTHON, "-B", "scripts/governance/check_protected_artifacts.py")),
    ("Check semantic boundaries", (PYTHON, "-B", "scripts/governance/check_semantic_boundaries.py")),
    ("Governance tests", (PYTHON, "-B", "tests/test_governance.py")),
    ("Baseline validation", (PYTHON, "-B", "validate.py")),
    ("Verified corpus validation", (PYTHON, "-B", "validate.py", "--verified-corpus")),
    ("Evidence trace validation", (PYTHON, "-B", "validate.py", "--check-evidence-traces")),
    ("Published format parity", (PYTHON, "-B", "validate.py", "--check-corpus-formats")),
    ("Adversarial tests", (PYTHON, "-B", "test_adversarial.py")),
    ("Corpus provenance", (PYTHON, "-B", "test_provenance.py")),
    ("Semantic fidelity", (PYTHON, "-B", "test_semantic_fidelity.py")),
    ("Assessment fragility", (PYTHON, "-B", "tests/test_assessment_fragility.py")),
    ("Document processing runner", (PYTHON, "-B", "tests/test_document_processing_runner.py")),
    ("GitHub batch workflow logic (local tests)", (PYTHON, "-B", "tests/test_github_actions_document_processing.py")),
    ("Regenerate real-world assessment", (PYTHON, "-B", "test_real_world.py")),
)


def git(*args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=ROOT, check=False, capture_output=True, text=True
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def resolve_base(explicit: str | None, head: str) -> str:
    if explicit:
        base = explicit
    elif os.environ.get("GOVERNANCE_BASE_REF"):
        base = os.environ["GOVERNANCE_BASE_REF"]
    else:
        base = ""
        for candidate in ("origin/main", "main"):
            found = subprocess.run(
                ("git", "rev-parse", "--verify", "--quiet", candidate),
                cwd=ROOT, capture_output=True, check=False,
            )
            if found.returncode == 0 and git("merge-base", candidate, "HEAD") != head:
                base = candidate
                break
        if not base:
            base = "HEAD^"  # A main-branch run compares the most recent commit.

    git("rev-parse", "--verify", base)
    git("merge-base", base, "HEAD")
    return base


def reports_snapshot() -> dict[str, str]:
    directory = ROOT / "reports"
    if not directory.is_dir():
        raise RuntimeError("reports/ directory missing")
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*")) if path.is_file()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", help="Git comparison base, normally origin/main or main")
    parser.add_argument("--receipt", type=Path, help="Optional JSON verification receipt path")
    args = parser.parse_args()
    receipt: dict[str, object] = {
        "schema": "laif.local-verification.v1",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "checks": [],
        "state": "FAIL",
    }
    failure = ""

    try:
        head = git("rev-parse", "HEAD")
        receipt["commit"] = head
        dirty = git("status", "--porcelain", "--untracked-files=normal")
        if dirty:
            raise RuntimeError(
                "working tree is not clean; commit intended changes before the full gate "
                "(targeted checks can run on uncommitted changes)"
            )

        base_ref = resolve_base(args.base_ref, head)
        receipt["base_ref"] = base_ref
        receipt["base_sha"] = git("rev-parse", base_ref)
        env = dict(os.environ, GOVERNANCE_BASE_REF=base_ref)
        print(f"LAIF local gate | commit {head} | base {base_ref}", flush=True)
        print("No GitHub Actions, API credentials, or hosted runner required.\n", flush=True)

        for name, command in CHECKS:
            print(f"\n>>> {name}", flush=True)
            start = time.monotonic()
            result = subprocess.run(command, cwd=ROOT, env=env, check=False)
            elapsed = round(time.monotonic() - start, 3)
            receipt["checks"].append({
                "name": name, "command": list(command),
                "return_code": result.returncode, "seconds": elapsed,
            })
            if result.returncode:
                raise RuntimeError(f"{name} failed (exit {result.returncode})")

        if git("diff", "--name-only", "HEAD", "--", "reports/"):
            raise RuntimeError("regenerated reports/ differ from the committed versions")
        if git("ls-files", "--others", "--exclude-standard", "--", "reports/"):
            raise RuntimeError("regeneration produced untracked reports/")
        first = reports_snapshot()

        print("\n>>> Repeat regeneration to verify deterministic output", flush=True)
        start = time.monotonic()
        result = subprocess.run((PYTHON, "-B", "test_real_world.py"), cwd=ROOT, env=env, check=False)
        receipt["checks"].append({
            "name": "Deterministic second regeneration",
            "command": [PYTHON, "-B", "test_real_world.py"],
            "return_code": result.returncode,
            "seconds": round(time.monotonic() - start, 3),
        })
        if result.returncode or reports_snapshot() != first:
            raise RuntimeError("second report generation failed or produced different bytes")
        receipt["report_sha256"] = first
        receipt["state"] = "PASS"
        print("\nLAIF LOCAL GATE PASS: all suites, committed report parity and determinism", flush=True)
    except (RuntimeError, OSError) as exc:
        failure = str(exc)
        receipt["failure"] = failure
        print(f"\nLAIF LOCAL GATE FAIL: {failure}", file=sys.stderr, flush=True)
    finally:
        receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"Verification receipt: {args.receipt}", flush=True)
    return 0 if not failure else 1


if __name__ == "__main__":
    raise SystemExit(main())
