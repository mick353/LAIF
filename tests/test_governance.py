#!/usr/bin/env python3
"""Deterministic standard-library self-tests for LAIF governance checks."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests" / "governance_fixtures"
SCRIPTS = REPO_ROOT / "scripts" / "governance"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CONFIG_CHECK = load_module("check_governance_config", SCRIPTS / "check_governance_config.py")
PROTECTED_CHECK = SCRIPTS / "check_protected_artifacts.py"
SEMANTIC_CHECK = SCRIPTS / "check_semantic_boundaries.py"


class GovernanceConfigTests(unittest.TestCase):
    def test_valid_fixture_config_is_accepted(self) -> None:
        config = json.loads((FIXTURES / "valid_protected_paths.json").read_text(encoding="utf-8"))
        CONFIG_CHECK.validate_config(config)

    def test_duplicate_protected_path_is_rejected(self) -> None:
        config = json.loads((FIXTURES / "invalid_duplicate_paths.json").read_text(encoding="utf-8"))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                CONFIG_CHECK.validate_config(config)

    def test_repository_governance_config_is_valid(self) -> None:
        config = CONFIG_CHECK.load_config(SCRIPTS / "protected_paths.json")
        CONFIG_CHECK.validate_config(config)


class GovernanceScriptIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.worktree = Path(self.tmp.name)
        self._run(["git", "init", "-q"], cwd=self.worktree)
        self._run(["git", "config", "user.email", "governance-tests@example.invalid"], cwd=self.worktree)
        self._run(["git", "config", "user.name", "Governance Tests"], cwd=self.worktree)
        (self.worktree / "reports").mkdir()
        (self.worktree / "docs" / "governance").mkdir(parents=True)
        (self.worktree / "reports" / "laif_full_assessment.md").write_text("baseline\n", encoding="utf-8")
        (self.worktree / "docs" / "governance" / "SEMANTIC_BOUNDARIES.md").write_text("baseline\n", encoding="utf-8")
        self._run(["git", "add", "."], cwd=self.worktree)
        self._run(["git", "commit", "-q", "-m", "baseline"], cwd=self.worktree)
        self.base_ref = self._run(["git", "rev-parse", "HEAD"], cwd=self.worktree).stdout.strip()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _run(self, args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if completed.returncode != 0:
            raise AssertionError(f"command failed: {' '.join(args)}\nstdout={completed.stdout}\nstderr={completed.stderr}")
        return completed

    def _script_env(self) -> dict[str, str]:
        env = os.environ.copy()
        env["GOVERNANCE_BASE_REF"] = self.base_ref
        env["PYTHONHASHSEED"] = "0"
        return env

    def test_protected_artifact_check_passes_without_protected_change(self) -> None:
        (self.worktree / "unprotected.txt").write_text("change\n", encoding="utf-8")
        self._run(["git", "add", "."], cwd=self.worktree)
        self._run(["git", "commit", "-q", "-m", "unprotected change"], cwd=self.worktree)

        completed = subprocess.run(["python3", str(PROTECTED_CHECK)], cwd=self.worktree, env=self._script_env(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('GOVERNANCE_RESULT status=PASS check=protected_artifacts', completed.stdout)
        self.assertIn('SUMMARY: no protected artifact paths changed', completed.stdout)

    def test_protected_artifact_check_blocks_configured_path(self) -> None:
        (self.worktree / "reports" / "laif_full_assessment.md").write_text("changed\n", encoding="utf-8")
        self._run(["git", "add", "."], cwd=self.worktree)
        self._run(["git", "commit", "-q", "-m", "protected change"], cwd=self.worktree)

        completed = subprocess.run(["python3", str(PROTECTED_CHECK)], cwd=self.worktree, env=self._script_env(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        self.assertEqual(completed.returncode, 1)
        self.assertIn('GOVERNANCE_RESULT status=ERROR check=protected_artifacts', completed.stdout)
        self.assertIn('reports/laif_full_assessment.md', completed.stdout + completed.stderr)

    def test_semantic_boundary_check_warns_without_blocking(self) -> None:
        target = self.worktree / "docs" / "governance" / "SEMANTIC_BOUNDARIES.md"
        target.write_text("baseline\nassessment_status changed\n", encoding="utf-8")
        self._run(["git", "add", "."], cwd=self.worktree)
        self._run(["git", "commit", "-q", "-m", "semantic advisory change"], cwd=self.worktree)

        completed = subprocess.run(["python3", str(SEMANTIC_CHECK)], cwd=self.worktree, env=self._script_env(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('GOVERNANCE_RESULT status=WARN check=semantic_boundaries', completed.stdout)
        self.assertIn('Mode: advisory/warn only; this check does not block merges.', completed.stdout)
        self.assertIn('assessment_status', completed.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
