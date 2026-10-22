#!/usr/bin/env python3
"""LAIF local verification entry point. Never invokes GitHub Actions."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*command: str, env: dict | None = None) -> None:
    print("CHECK:", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="run entire repository verification suite")
    parser.add_argument("--base-ref", help="git base ref for protected-artifact and semantic-diff checks")
    args = parser.parse_args()
    env = {**os.environ, "GOVERNANCE_BASE_REF": args.base_ref} if args.base_ref else os.environ.copy()
    try:
        run(PYTHON, "-m", "py_compile", "scripts/laif_evidence_checks.py", "scripts/laif_verify.py")
        run(PYTHON, "tests/test_evidence_checks.py")
        run(PYTHON, "scripts/governance/check_governance_config.py")
        if args.full:
            if args.base_ref:
                run(PYTHON, "scripts/governance/check_protected_artifacts.py", env=env)
                run(PYTHON, "scripts/governance/check_semantic_boundaries.py", env=env)
            else:
                print("NOT RUN: diff governance checks; pass --base-ref origin/main")
            for opts in ((), ("--verified-corpus",), ("--check-evidence-traces",), ("--check-corpus-formats",)):
                run(PYTHON, "validate.py", *opts)
            run(PYTHON, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py")
            for script in ("test_adversarial.py", "test_provenance.py", "test_semantic_fidelity.py"):
                run(PYTHON, script)
            run(PYTHON, "test_real_world.py")
            def snapshot_reports():
                return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted((ROOT / "reports").rglob("*")) if p.is_file()}
            first = snapshot_reports()
            run(PYTHON, "test_real_world.py")
            if first != snapshot_reports():
                print("FAIL: report regeneration is nondeterministic", file=sys.stderr)
                return 1
            # Committed reports must remain identical after regeneration.
            run("git", "diff", "--exit-code", "--", "reports/")
            extra = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "--", "reports/"], cwd=ROOT, text=True)
            if extra.strip():
                print("FAIL: untracked generated reports:", extra)
                return 1
    except subprocess.CalledProcessError as exc:
        print(f"FAIL: {exc.cmd} (exit {exc.returncode})", file=sys.stderr)
        return 1
    print("PASS: selected local checks (see NOT RUN notes for omissions).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
