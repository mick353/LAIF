#!/usr/bin/env python3
"""Deterministic tests for LAIF governance check plumbing."""

from __future__ import annotations

import contextlib
import importlib
import io
import json
import os
import subprocess
import sys
import tempfile
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_DIR = REPO_ROOT / "scripts" / "governance"
FIXTURES_DIR = REPO_ROOT / "tests" / "governance_fixtures"

EXPANDED_SEMANTIC_SENSITIVE_TERMS = [
    "Coupling",
    "Integrity Layer",
    "Coherence Test",
    "Structural Transparency",
    "Structural Honesty",
    "Structural Containment",
    "Consistency",
    "Reversibility",
    "Foundational Principles",
    "non-amendable",
    "assessment_status",
    "citation_status",
    "transformation_status",
    "provenance_classification",
    "acquisition_channel",
    "verification_status",
    "network_status",
    "authoritative_origin_url",
    "transformation_chain",
]

sys.path.insert(0, str(GOVERNANCE_DIR))

governance_lib = importlib.import_module("governance_lib")
check_governance_config = importlib.import_module("check_governance_config")
check_protected_artifacts = importlib.import_module("check_protected_artifacts")
check_semantic_boundaries = importlib.import_module("check_semantic_boundaries")


@contextlib.contextmanager
def patched_env(**updates: str | None):
    old_values = {key: os.environ.get(key) for key in updates}
    try:
        for key, value in updates.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        yield
    finally:
        for key, value in old_values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


@contextlib.contextmanager
def pushd(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


@contextlib.contextmanager
def module_attr(module, name: str, value):
    old_value = getattr(module, name)
    setattr(module, name, value)
    try:
        yield
    finally:
        setattr(module, name, old_value)


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def init_repo(path: Path) -> None:
    run(["git", "init", "-q"], path)
    run(["git", "config", "user.email", "governance-tests@example.invalid"], path)
    run(["git", "config", "user.name", "Governance Tests"], path)


def commit_all(path: Path, message: str) -> str:
    run(["git", "add", "."], path)
    run(["git", "commit", "-q", "-m", message], path)
    return run(["git", "rev-parse", "HEAD"], path)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def minimal_config(
    *,
    protected: list[str] | None = None,
    sensitive_files: list[str] | None = None,
    terms: list[str] | None = None,
) -> dict:
    return {
        "protected_artifacts": protected if protected is not None else ["reports/laif_full_assessment.md"],
        "semantic_sensitive_files": sensitive_files if sensitive_files is not None else ["sensitive.txt"],
        "semantic_sensitive_terms": terms if terms is not None else ["Coupling"],
    }


def config_check_repo(tmp: Path, payload: dict | str) -> Path:
    config_path = tmp / "scripts" / "governance" / "protected_paths.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, str):
        config_path.write_text(payload, encoding="utf-8")
    else:
        write_json(config_path, payload)

    for path in payload.get("protected_artifacts", []) if isinstance(payload, dict) else []:
        target = tmp / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture\n", encoding="utf-8")
    for path in payload.get("semantic_sensitive_files", []) if isinstance(payload, dict) else []:
        target = tmp / path
        if target == config_path:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture\n", encoding="utf-8")
    return config_path


def clean_base_env() -> dict[str, None]:
    return {
        "GOVERNANCE_BASE_REF": None,
        "GITHUB_EVENT_PATH": None,
        "GITHUB_BASE_REF": None,
        "GITHUB_EVENT_NAME": None,
    }


class GovernanceLibTests(unittest.TestCase):
    def test_load_json_config_loads_valid_config(self) -> None:
        config = governance_lib.load_json_config(
            "TEST CONFIG ERROR", FIXTURES_DIR / "valid_config.json"
        )
        self.assertIn("protected_artifacts", config)
        self.assertIn("scripts/governance/governance_lib.py", config["semantic_sensitive_files"])

    def test_production_config_contains_expanded_semantic_sensitive_terms(self) -> None:
        config = governance_lib.load_json_config(
            "TEST CONFIG ERROR", governance_lib.CONFIG_PATH
        )
        self.assertEqual(
            config["semantic_sensitive_terms"],
            EXPANDED_SEMANTIC_SENSITIVE_TERMS,
        )

    def test_valid_fixture_config_matches_expanded_production_terms(self) -> None:
        # The valid governance fixture intentionally mirrors production semantic-sensitive
        # term coverage so tests exercise canonical LAIF/provenance boundary terms.
        fixture = governance_lib.load_json_config(
            "TEST CONFIG ERROR", FIXTURES_DIR / "valid_config.json"
        )
        production = governance_lib.load_json_config(
            "TEST CONFIG ERROR", governance_lib.CONFIG_PATH
        )
        self.assertEqual(
            fixture["semantic_sensitive_terms"],
            EXPANDED_SEMANTIC_SENSITIVE_TERMS,
        )
        self.assertEqual(
            fixture["semantic_sensitive_terms"],
            production["semantic_sensitive_terms"],
        )

    def test_fail_emits_deterministic_namespaced_error_and_exits_nonzero(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
            governance_lib.fail("TEST PREFIX", "deterministic failure")
        self.assertEqual(caught.exception.code, 1)
        self.assertEqual(stderr.getvalue(), "TEST PREFIX: deterministic failure\n")

    def test_run_git_successful_call(self) -> None:
        with pushd(REPO_ROOT):
            output = governance_lib.run_git(["rev-parse", "--is-inside-work-tree"], "GIT ERROR")
        self.assertEqual(output.strip(), "true")

    def test_run_git_failure_path_is_deterministic(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
            governance_lib.run_git(["definitely-not-a-git-command"], "GIT ERROR")
        self.assertEqual(caught.exception.code, 1)
        self.assertIn("GIT ERROR: git definitely-not-a-git-command failed:", stderr.getvalue())

    def test_resolve_base_ref_respects_governance_base_ref(self) -> None:
        env = clean_base_env()
        env["GOVERNANCE_BASE_REF"] = "explicit-base"
        with patched_env(**env):
            self.assertEqual(governance_lib.resolve_base_ref(), "explicit-base")

    def test_resolve_base_ref_prefers_explicit_ref_over_stale_pr_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            event_path = Path(tmp_name) / "event.json"
            event_path.write_text(
                json.dumps({"pull_request": {"base": {"sha": "event-base"}}}),
                encoding="utf-8",
            )
            env = clean_base_env()
            env["GOVERNANCE_BASE_REF"] = "explicit-base"
            env["GITHUB_EVENT_PATH"] = str(event_path)
            env["GITHUB_BASE_REF"] = "stale-local-branch"
            env["GITHUB_EVENT_NAME"] = "pull_request"
            with patched_env(**env):
                self.assertEqual(governance_lib.resolve_base_ref(), "explicit-base")

    def test_pull_request_no_base_failure_path_is_deterministic(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        env = clean_base_env()
        env["GITHUB_EVENT_NAME"] = "pull_request"
        with patched_env(**env):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as caught:
                    governance_lib.require_base_ref_or_skip("test governance check")
        self.assertEqual(caught.exception.code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            stderr.getvalue(),
            "test governance check ERROR: pull_request CI context did not provide a base ref; set GOVERNANCE_BASE_REF, GITHUB_EVENT_PATH, or GITHUB_BASE_REF\n",
        )

    def test_changed_files_from_merge_base_returns_expected_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            repo = Path(tmp_name)
            init_repo(repo)
            (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
            (repo / "new.txt").write_text("new\n", encoding="utf-8")
            commit_all(repo, "change")
            with pushd(repo):
                changed = governance_lib.changed_files_from_merge_base(base, "GIT ERROR")
        self.assertEqual(changed, {"tracked.txt", "new.txt"})


class GovernanceStatusTests(unittest.TestCase):
    def run_status(self) -> tuple[int, str, str]:
        completed = subprocess.run(
            [sys.executable, "scripts/governance/governance_status.py"],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.returncode, completed.stdout, completed.stderr

    def test_status_command_reports_deterministic_governance_summary(self) -> None:
        config = governance_lib.load_json_config(
            "TEST CONFIG ERROR", governance_lib.CONFIG_PATH
        )
        code, stdout, stderr = self.run_status()

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("LAIF Governance Status", stdout)
        self.assertIn(
            f"Protected artifact count: {len(config['protected_artifacts'])}", stdout
        )
        self.assertIn("reports/laif_full_assessment.md", stdout)
        self.assertIn(
            f"Semantic-sensitive file count: {len(config['semantic_sensitive_files'])}",
            stdout,
        )
        self.assertIn("scripts/governance/check_semantic_boundaries.py", stdout)
        self.assertIn(
            f"Semantic-sensitive term count: {len(config['semantic_sensitive_terms'])}",
            stdout,
        )
        self.assertIn("authoritative_origin_url", stdout)
        self.assertIn(
            "Semantic-boundary checks are advisory-only and do not block merges.",
            stdout,
        )
        self.assertIn(
            "Protected-artifact checks are blocking and fail on protected artifact drift.",
            stdout,
        )
        self.assertIn(
            "This status tool is read-only and does not alter LAIF scoring, assessment semantics",
            stdout,
        )
        self.assertIn("Test coverage file present: tests/test_governance.py: yes", stdout)
        self.assertIn("CI workflow present: .github/workflows/ci.yml: yes", stdout)
        self.assertNotIn("phase-3g-governance-status-report", stdout)


class GovernanceConfigCheckTests(unittest.TestCase):
    def run_config_main(self, config_path: Path) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with module_attr(check_governance_config, "CONFIG_PATH", config_path):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:
                    code = check_governance_config.main()
                except SystemExit as exc:
                    code = int(exc.code or 0)
        return code, stdout.getvalue(), stderr.getvalue()

    def valid_payload(self) -> dict:
        sensitive_files = sorted(check_governance_config.REQUIRED_GOVERNANCE_SENSITIVE_PATHS)
        return minimal_config(
            protected=["reports/laif_full_assessment.md"],
            sensitive_files=sensitive_files,
            terms=EXPANDED_SEMANTIC_SENSITIVE_TERMS,
        )

    def test_valid_config_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            config_path = config_check_repo(Path(tmp_name), self.valid_payload())
            code, stdout, stderr = self.run_config_main(config_path)
        self.assertEqual(code, 0)
        self.assertIn("Governance config valid:", stdout)
        self.assertEqual(stderr, "")

    def test_malformed_json_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            config_path = config_check_repo(Path(tmp_name), "{ malformed json")
            code, stdout, stderr = self.run_config_main(config_path)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("GOVERNANCE CONFIG ERROR: malformed governance config:", stderr)

    def test_missing_required_top_level_keys_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            config_path = config_check_repo(Path(tmp_name), {"protected_artifacts": []})
            code, stdout, stderr = self.run_config_main(config_path)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("GOVERNANCE CONFIG ERROR: missing required key: 'semantic_sensitive_files'", stderr)

    def test_configured_paths_that_do_not_exist_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            payload = self.valid_payload()
            config_path = tmp / "scripts" / "governance" / "protected_paths.json"
            write_json(config_path, payload)
            code, stdout, stderr = self.run_config_main(config_path)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("does not exist: reports/laif_full_assessment.md", stderr)

    def test_required_governance_sensitive_paths_must_be_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            payload = self.valid_payload()
            payload["semantic_sensitive_files"].remove("scripts/governance/check_semantic_boundaries.py")
            config_path = config_check_repo(Path(tmp_name), payload)
            code, stdout, stderr = self.run_config_main(config_path)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("must include governance check paths", stderr)
        self.assertIn("scripts/governance/check_semantic_boundaries.py", stderr)

    def test_governance_lib_must_remain_semantic_sensitive(self) -> None:
        self.assertIn(
            "scripts/governance/governance_lib.py",
            check_governance_config.REQUIRED_GOVERNANCE_SENSITIVE_PATHS,
        )
        config = governance_lib.load_json_config(
            "TEST CONFIG ERROR", governance_lib.CONFIG_PATH
        )
        self.assertIn("scripts/governance/governance_lib.py", config["semantic_sensitive_files"])


class ProtectedArtifactsCheckTests(unittest.TestCase):
    def run_main(self, repo: Path, config_path: Path, **env: str | None) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        merged_env = clean_base_env()
        merged_env.update(env)
        with module_attr(check_protected_artifacts, "CONFIG_PATH", config_path):
            with patched_env(**merged_env), pushd(repo):
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    try:
                        code = check_protected_artifacts.main()
                    except SystemExit as exc:
                        code = int(exc.code or 0)
        return code, stdout.getvalue(), stderr.getvalue()

    def repo_with_config(
        self,
        protected: list[str] | None = None,
        terms: list[str] | None = None,
    ) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        tmp_dir = tempfile.TemporaryDirectory()
        repo = Path(tmp_dir.name)
        init_repo(repo)
        config_path = repo / "scripts" / "governance" / "protected_paths.json"
        write_json(config_path, minimal_config(protected=protected, terms=terms))
        return tmp_dir, repo, config_path

    def test_local_non_pr_mode_with_no_base_ref_skips_cleanly(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            code, stdout, stderr = self.run_main(repo, config_path)
        self.assertEqual(code, 0)
        self.assertEqual(
            stdout,
            "No PR base ref detected; protected artifact drift check skipped.\n"
            "Set GITHUB_BASE_REF or GOVERNANCE_BASE_REF to enable deterministic diff detection.\n",
        )
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_detects_protected_artifact_changes(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            protected = repo / "reports" / "laif_full_assessment.md"
            protected.parent.mkdir(parents=True, exist_ok=True)
            protected.write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            protected.write_text("changed\n", encoding="utf-8")
            commit_all(repo, "protected change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Protected LAIF assessment artifact drift detected.", stderr)
        self.assertIn("reports/laif_full_assessment.md", stderr)

    def test_expanded_semantic_terms_do_not_affect_protected_artifact_blocking(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config(
            terms=EXPANDED_SEMANTIC_SENSITIVE_TERMS
        )
        with tmp_dir:
            protected = repo / "reports" / "laif_full_assessment.md"
            protected.parent.mkdir(parents=True, exist_ok=True)
            protected.write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            protected.write_text("changed despite Structural Transparency terms\n", encoding="utf-8")
            commit_all(repo, "protected change with expanded terms")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Protected LAIF assessment artifact drift detected.", stderr)
        self.assertIn("reports/laif_full_assessment.md", stderr)

    def test_pull_request_mode_with_explicit_base_ref_detects_protected_artifact_changes(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            protected = repo / "reports" / "laif_full_assessment.md"
            protected.parent.mkdir(parents=True, exist_ok=True)
            protected.write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            protected.write_text("changed in pr\n", encoding="utf-8")
            commit_all(repo, "protected pr change")
            code, stdout, stderr = self.run_main(
                repo,
                config_path,
                GOVERNANCE_BASE_REF=base,
                GITHUB_EVENT_NAME="pull_request",
            )
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Protected LAIF assessment artifact drift detected.", stderr)
        self.assertIn("reports/laif_full_assessment.md", stderr)

    def test_explicit_base_ref_allows_non_protected_changes(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "reports").mkdir(parents=True, exist_ok=True)
            (repo / "reports" / "laif_full_assessment.md").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "ordinary.txt").write_text("changed\n", encoding="utf-8")
            commit_all(repo, "ordinary change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn("No protected artifact paths changed relative to PR base.", stdout)
        self.assertEqual(stderr, "")

    def test_semantic_sensitive_terms_outside_protected_paths_do_not_block(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "reports").mkdir(parents=True, exist_ok=True)
            (repo / "reports" / "laif_full_assessment.md").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "ordinary.txt").write_text("Coupling changed outside protected paths\n", encoding="utf-8")
            commit_all(repo, "ordinary semantic term change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn("No protected artifact paths changed relative to PR base.", stdout)
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_is_used_when_pr_branch_ref_is_stale(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            protected = repo / "reports" / "laif_full_assessment.md"
            protected.parent.mkdir(parents=True, exist_ok=True)
            protected.write_text("base\n", encoding="utf-8")
            true_base = commit_all(repo, "base")
            run(["git", "branch", "stale-base-ref", true_base], repo)
            protected.write_text("feature protected change\n", encoding="utf-8")
            commit_all(repo, "feature protected change")
            code, stdout, stderr = self.run_main(
                repo,
                config_path,
                GOVERNANCE_BASE_REF=true_base,
                GITHUB_BASE_REF="stale-base-ref",
                GITHUB_EVENT_NAME="pull_request",
            )
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Protected LAIF assessment artifact drift detected.", stderr)
        self.assertIn("reports/laif_full_assessment.md", stderr)

    def test_pr_mode_with_unresolvable_base_ref_fails_deterministically(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "reports").mkdir(parents=True, exist_ok=True)
            (repo / "reports" / "laif_full_assessment.md").write_text("base\n", encoding="utf-8")
            commit_all(repo, "base")
            code, stdout, stderr = self.run_main(
                repo,
                config_path,
                GOVERNANCE_BASE_REF="refs/heads/does-not-exist",
                GITHUB_EVENT_NAME="pull_request",
            )
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn(
            "PROTECTED ARTIFACT CHECK FAILED: git merge-base refs/heads/does-not-exist HEAD failed:",
            stderr,
        )

    def test_pr_mode_without_resolvable_base_ref_fails_deterministically(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            code, stdout, stderr = self.run_main(repo, config_path, GITHUB_EVENT_NAME="pull_request")
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertEqual(
            stderr,
            "protected artifact drift check ERROR: pull_request CI context did not provide a base ref; set GOVERNANCE_BASE_REF, GITHUB_EVENT_PATH, or GITHUB_BASE_REF\n",
        )


class SemanticBoundariesCheckTests(unittest.TestCase):
    def run_main(self, repo: Path, config_path: Path, **env: str | None) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        merged_env = clean_base_env()
        merged_env.update(env)
        with module_attr(check_semantic_boundaries, "CONFIG_PATH", config_path):
            with patched_env(**merged_env), pushd(repo):
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    try:
                        code = check_semantic_boundaries.main()
                    except SystemExit as exc:
                        code = int(exc.code or 0)
        return code, stdout.getvalue(), stderr.getvalue()

    def repo_with_config(
        self,
        sensitive_files: list[str] | None = None,
        terms: list[str] | None = None,
    ) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        tmp_dir = tempfile.TemporaryDirectory()
        repo = Path(tmp_dir.name)
        init_repo(repo)
        config_path = repo / "scripts" / "governance" / "protected_paths.json"
        write_json(config_path, minimal_config(sensitive_files=sensitive_files, terms=terms))
        return tmp_dir, repo, config_path

    def test_local_non_pr_mode_with_no_base_ref_skips_cleanly(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            code, stdout, stderr = self.run_main(repo, config_path)
        self.assertEqual(code, 0)
        self.assertEqual(
            stdout,
            "No PR base ref detected; semantic-boundary check skipped.\n"
            "Set GITHUB_BASE_REF or GOVERNANCE_BASE_REF to enable deterministic diff detection.\n",
        )
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_detects_advisory_changes_without_failing(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "sensitive.txt").write_text("Coupling changed\n", encoding="utf-8")
            commit_all(repo, "semantic-sensitive change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn("Semantic-boundary governance notice.", stdout)
        self.assertIn("Mode: advisory/warn only; this check does not block merges.", stdout)
        self.assertIn("term: Coupling", stdout)
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_detects_new_structural_term_advisory_only(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config(
            terms=EXPANDED_SEMANTIC_SENSITIVE_TERMS
        )
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "sensitive.txt").write_text(
                "Structural Transparency changed\n", encoding="utf-8"
            )
            commit_all(repo, "semantic-sensitive structural term change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn("Semantic-boundary governance notice.", stdout)
        self.assertIn("Mode: advisory/warn only; this check does not block merges.", stdout)
        self.assertIn("term: Structural Transparency", stdout)
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_detects_new_provenance_term_advisory_only(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config(
            terms=EXPANDED_SEMANTIC_SENSITIVE_TERMS
        )
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "sensitive.txt").write_text(
                "authoritative_origin_url changed\n", encoding="utf-8"
            )
            commit_all(repo, "semantic-sensitive provenance term change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn("Semantic-boundary governance notice.", stdout)
        self.assertIn("Mode: advisory/warn only; this check does not block merges.", stdout)
        self.assertIn("term: authoritative_origin_url", stdout)
        self.assertEqual(stderr, "")

    def test_pull_request_mode_with_explicit_base_ref_keeps_semantic_boundary_advisory(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "sensitive.txt").write_text("Coupling changed in PR\n", encoding="utf-8")
            commit_all(repo, "semantic-sensitive pr change")
            code, stdout, stderr = self.run_main(
                repo,
                config_path,
                GOVERNANCE_BASE_REF=base,
                GITHUB_EVENT_NAME="pull_request",
            )
        self.assertEqual(code, 0)
        self.assertIn("Semantic-boundary governance notice.", stdout)
        self.assertIn("Mode: advisory/warn only; this check does not block merges.", stdout)
        self.assertIn("term: Coupling", stdout)
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_with_no_semantic_sensitive_changes_exits_cleanly(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "ordinary.txt").write_text("Coupling changed outside configured files\n", encoding="utf-8")
            commit_all(repo, "ordinary change")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn("No configured semantic-sensitive files changed relative to PR base.", stdout)
        self.assertNotIn("term: Coupling", stdout)
        self.assertEqual(stderr, "")

    def test_semantic_sensitive_file_change_without_configured_terms_is_advisory_only(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            base = commit_all(repo, "base")
            (repo / "sensitive.txt").write_text("non-sensitive wording changed\n", encoding="utf-8")
            commit_all(repo, "semantic-sensitive path without configured term")
            code, stdout, stderr = self.run_main(repo, config_path, GOVERNANCE_BASE_REF=base)
        self.assertEqual(code, 0)
        self.assertIn(
            "Configured semantic-sensitive files changed, but no configured terms were touched in changed hunk lines.",
            stdout,
        )
        self.assertIn("This advisory check performed no semantic interpretation.", stdout)
        self.assertEqual(stderr, "")

    def test_explicit_base_ref_keeps_semantic_boundary_deterministic_with_stale_pr_ref(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            true_base = commit_all(repo, "base")
            run(["git", "branch", "stale-base-ref", true_base], repo)
            (repo / "sensitive.txt").write_text("Coupling changed on feature\n", encoding="utf-8")
            commit_all(repo, "semantic-sensitive feature change")
            code, stdout, stderr = self.run_main(
                repo,
                config_path,
                GOVERNANCE_BASE_REF=true_base,
                GITHUB_BASE_REF="stale-base-ref",
                GITHUB_EVENT_NAME="pull_request",
            )
        self.assertEqual(code, 0)
        self.assertIn("Semantic-boundary governance notice.", stdout)
        self.assertIn("term: Coupling", stdout)
        self.assertEqual(stderr, "")

    def test_pr_mode_with_unresolvable_base_ref_fails_deterministically(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            (repo / "sensitive.txt").write_text("base\n", encoding="utf-8")
            commit_all(repo, "base")
            code, stdout, stderr = self.run_main(
                repo,
                config_path,
                GOVERNANCE_BASE_REF="refs/heads/does-not-exist",
                GITHUB_EVENT_NAME="pull_request",
            )
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn(
            "SEMANTIC BOUNDARY CHECK ERROR: git merge-base refs/heads/does-not-exist HEAD failed:",
            stderr,
        )

    def test_pr_mode_without_resolvable_base_ref_fails_deterministically(self) -> None:
        tmp_dir, repo, config_path = self.repo_with_config()
        with tmp_dir:
            code, stdout, stderr = self.run_main(repo, config_path, GITHUB_EVENT_NAME="pull_request")
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertEqual(
            stderr,
            "semantic-boundary check ERROR: pull_request CI context did not provide a base ref; set GOVERNANCE_BASE_REF, GITHUB_EVENT_PATH, or GITHUB_BASE_REF\n",
        )


class ReportsDirectoryAccountabilityTests(unittest.TestCase):
    """Every artifact in reports/ must be accounted for.

    An audit found two artifacts in reports/ that no code produced: not
    regenerated, not fingerprinted, and invisible to the CI check that compares
    committed reports against regenerated output — which only diffs the files
    the pipeline writes. One of them was labelled "Authoritative" across the
    README, CLAUDE.md, REPRODUCIBILITY.md, the publication status, and the
    verified corpus manifest, while carrying the least verification of anything
    in the repository.
    """

    REPO = Path(__file__).resolve().parents[1]

    def _generated(self) -> set:
        """Artifacts the deterministic pipeline writes, read from its source."""
        source = (self.REPO / "test_real_world.py").read_text(encoding="utf-8")
        return set(re.findall(r'"reports"\s*/\s*"([^"]+)"', source))

    def _declared_narrative(self) -> set:
        """Artifacts declared historical in the reports manifest."""
        manifest = (self.REPO / "reports" / "README.md").read_text(encoding="utf-8")
        section = manifest.split("Narrative analyses", 1)[-1]
        # Table rows only. Prose in the same section legitimately mentions the
        # generated artifacts, and picking those up would make the manifest
        # describe them as historical.
        rows = [line for line in section.splitlines() if line.startswith("|")]
        return set(re.findall(r"`([A-Za-z0-9_.-]+\.(?:md|json))`", "\n".join(rows)))

    def test_reports_manifest_exists(self) -> None:
        self.assertTrue((self.REPO / "reports" / "README.md").is_file(),
                        "reports/README.md must state what each artifact is")

    def test_every_artifact_is_generated_or_declared_historical(self) -> None:
        present = {p.name for p in (self.REPO / "reports").glob("*")
                   if p.is_file() and p.name != "README.md"}
        accounted = self._generated() | self._declared_narrative()
        orphans = sorted(present - accounted)
        self.assertEqual(
            orphans, [],
            f"artifacts in reports/ that are neither regenerated by "
            f"test_real_world.py nor declared as historical narrative analyses "
            f"in reports/README.md: {orphans}. Add them to the pipeline so CI "
            f"checks them, or record them in the manifest with their production "
            f"date and model version.")

    def test_generated_artifacts_are_named_in_the_manifest(self) -> None:
        manifest = (self.REPO / "reports" / "README.md").read_text(encoding="utf-8")
        for name in self._generated():
            self.assertIn(name, manifest,
                          f"{name} is generated but not described in reports/README.md")

    def test_narrative_artifacts_carry_a_production_date(self) -> None:
        manifest = (self.REPO / "reports" / "README.md").read_text(encoding="utf-8")
        section = manifest.split("Narrative analyses", 1)[-1]
        for name in self._declared_narrative():
            row = next((line for line in section.splitlines()
                        if line.startswith("|") and f"`{name}`" in line), "")
            self.assertRegex(
                row, r"\d{1,2}\s+\w+\s+20\d\d",
                f"the manifest row for {name} must give the date it was produced")

    def test_no_document_calls_an_unverified_artifact_authoritative(self) -> None:
        """The authority claim must sit on the artifact that carries the
        verification, not the one that does not."""
        narrative = self._declared_narrative()
        for doc in ("README.md", "CLAUDE.md", "REPRODUCIBILITY.md",
                    "PUBLICATION_STATUS.md"):
            text = (self.REPO / doc).read_text(encoding="utf-8")
            for line in text.splitlines():
                if not any(name in line for name in narrative):
                    continue
                if re.search(r"\bauthoritative\b", line, re.IGNORECASE):
                    self.assertRegex(
                        line, r"historical|not regenerated|narrative",
                        f"{doc} calls a non-regenerated artifact authoritative "
                        f"without qualifying it: {line.strip()[:120]}")


class DeadCodeTests(unittest.TestCase):
    """Unreferenced functions accumulate, and one of them was dangerous.

    An audit of the toolchain found seven functions no code called. One,
    `_native_certification_label`, returned "FAIL / not LAIF-native / canonical
    remediation required" for external documents — precisely the deficiency
    framing that was removed from every live path. Dead code that encodes a
    superseded judgement is a defect waiting to be wired back in.
    """

    REPO = Path(__file__).resolve().parents[1]
    MODULES = (
        "assessment_engine.py",
        "validate.py",
        "laif_spec.py",
        "official_documents.py",
        "sample_documents.py",
        "scripts/laif_process_document.py",
        "scripts/laif_batch_process_pending.py",
    )

    def test_no_unreferenced_functions_in_the_toolchain(self) -> None:
        sources = {}
        for path in self.REPO.rglob("*.py"):
            rel = path.relative_to(self.REPO).as_posix()
            if rel.startswith("laif_inputs/"):
                continue
            sources[rel] = path.read_text(encoding="utf-8")
        corpus = "\n".join(sources.values())

        dead = []
        for module in self.MODULES:
            text = sources.get(module, "")
            for name in re.findall(r"^def (\w+)\(", text, re.M):
                if name.startswith("__"):
                    continue
                references = len(re.findall(rf"\b{name}\b", corpus))
                definitions = len(re.findall(rf"^def {name}\(", corpus, re.M))
                if references - definitions == 0:
                    dead.append(f"{module}:{name}")

        self.assertEqual(
            dead, [],
            f"functions defined but never referenced anywhere in the toolchain "
            f"or its tests: {dead}. Remove them, or reference them from the code "
            f"path they were written for. A function nothing calls is a "
            f"judgement nobody reviewed.")


class GovernanceConfigCoverageTests(unittest.TestCase):
    """The governance config must cover what it claims to govern.

    An audit found protection on one of the two identically-situated narrative
    artifacts, and the semantic-boundary advisory covering `test_adversarial.py`
    but not `assessment_engine.py` — so a change to detection logic produced no
    signal while a change to one of its tests did.
    """

    REPO = Path(__file__).resolve().parents[1]

    def _config(self):
        return json.loads(
            (self.REPO / "scripts" / "governance" / "protected_paths.json")
            .read_text(encoding="utf-8"))

    def _narrative_artifacts(self):
        manifest = (self.REPO / "reports" / "README.md").read_text(encoding="utf-8")
        section = manifest.split("Narrative analyses", 1)[-1]
        rows = [line for line in section.splitlines() if line.startswith("|")]
        return {f"reports/{name}" for name in
                re.findall(r"`([A-Za-z0-9_.-]+\.(?:md|json))`", "\n".join(rows))}

    def test_every_narrative_artifact_is_protected(self) -> None:
        """A record that must not drift needs the immutability control."""
        protected = set(self._config()["protected_artifacts"])
        unprotected = sorted(self._narrative_artifacts() - protected)
        self.assertEqual(
            unprotected, [],
            f"narrative artifacts declared in reports/README.md but not listed in "
            f"protected_artifacts: {unprotected}")

    def test_generated_artifacts_are_not_protected(self) -> None:
        """They must change with the engine; CI checks them by regeneration.

        A path-level hard fail here would block every legitimate engine change
        while adding no safety.
        """
        protected = set(self._config()["protected_artifacts"])
        generated = {f"reports/{name}" for name in re.findall(
            r'"reports"\s*/\s*"([^"]+)"',
            (self.REPO / "test_real_world.py").read_text(encoding="utf-8"))}
        overlap = sorted(protected & generated)
        self.assertEqual(
            overlap, [],
            f"generated artifacts must not be path-protected: {overlap}")

    def test_files_that_decide_semantics_are_boundary_sensitive(self) -> None:
        sensitive = set(self._config()["semantic_sensitive_files"])
        decides_semantics = {
            "assessment_engine.py",
            "laif_spec.py",
            "validate.py",
            "official_documents.py",
            "sample_documents.py",
            "scripts/laif_process_document.py",
            "scripts/laif_batch_process_pending.py",
            "test_provenance.py",
            "test_semantic_fidelity.py",
            "test_adversarial.py",
        }
        missing = sorted(decides_semantics - sensitive)
        self.assertEqual(
            missing, [],
            f"files where a change can move a LAIF boundary, absent from "
            f"semantic_sensitive_files: {missing}")

    def test_every_configured_path_exists(self) -> None:
        config = self._config()
        for key in ("protected_artifacts", "semantic_sensitive_files"):
            for path in config[key]:
                self.assertTrue((self.REPO / path).exists(),
                                f"{key} names a path that does not exist: {path}")


class TestQualityTests(unittest.TestCase):
    """A test that cannot fail is worse than no test: it reports coverage that
    does not exist.

    An audit found two — `assertTrue(True)` standing in for an untested branch,
    and an equality assertion comparing an lru_cached function with itself.
    """

    REPO = Path(__file__).resolve().parents[1]

    def _test_sources(self):
        for path in sorted(self.REPO.rglob("test_*.py")):
            rel = path.relative_to(self.REPO).as_posix()
            if rel.startswith("laif_inputs/"):
                continue
            yield rel, path.read_text(encoding="utf-8")

    def test_every_test_function_asserts_something(self) -> None:
        import ast
        empty = []
        for rel, source in self._test_sources():
            for node in ast.walk(ast.parse(source)):
                if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
                    continue
                asserts = any(
                    isinstance(inner, ast.Assert)
                    or (isinstance(inner, ast.Call)
                        and isinstance(inner.func, ast.Attribute)
                        and inner.func.attr.startswith(("assert", "fail")))
                    for inner in ast.walk(node)
                )
                if not asserts:
                    empty.append(f"{rel}:{node.name}")
        self.assertEqual(empty, [], f"test functions with no assertion: {empty}")

    def test_no_assertion_is_trivially_true(self) -> None:
        import ast
        trivial = []
        for rel, source in self._test_sources():
            for node in ast.walk(ast.parse(source)):
                if not (isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Attribute)):
                    continue
                name = node.func.attr
                if (name in ("assertTrue", "assertFalse")
                        and node.args and isinstance(node.args[0], ast.Constant)):
                    trivial.append(f"{rel}:{node.lineno} {name}(literal)")
                if name in ("assertEqual", "assertIn", "assertIs") and len(node.args) >= 2:
                    if ast.dump(node.args[0]) == ast.dump(node.args[1]):
                        trivial.append(f"{rel}:{node.lineno} {name}(x, x)")
        self.assertEqual(
            trivial, [],
            f"assertions that cannot fail: {trivial}. An assertion comparing a "
            f"value with itself, or asserting a literal, reports coverage that "
            f"does not exist. Assert the property the branch was written for, or "
            f"delete the branch.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
