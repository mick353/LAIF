#!/usr/bin/env python3
"""Tests for Phase 3U GitHub Actions batch document orchestration."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "laif_batch_process_pending.py"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "laif_process_pending_documents.yml"
DOC_PATH = REPO_ROOT / "docs" / "governance" / "GITHUB_ACTIONS_DOCUMENT_PROCESSING.md"

spec = importlib.util.spec_from_file_location("laif_batch_process_pending", SCRIPT_PATH)
batch = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(batch)

POLICY_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, "
    "audit, monitoring, appeal, evidence documentation, public service delivery, "
    "and administrative review."
)


def completed_process(returncode: int = 0, stdout: str = "ok", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["python"], returncode=returncode, stdout=stdout, stderr=stderr)


def fake_successful_runner(command: list[str], text: bool, capture_output: bool) -> subprocess.CompletedProcess[str]:
    output_dir = Path(command[command.index("--output-dir") + 1])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "sample.laif.md").write_text("# LAIF report\n", encoding="utf-8")
    (output_dir / "sample.laif.json").write_text('{"ok": true}\n', encoding="utf-8")
    (output_dir / "laif_processing_index.jsonl").write_text('{"ok": true}\n', encoding="utf-8")
    return completed_process(0)


def fake_failing_runner(command: list[str], text: bool, capture_output: bool) -> subprocess.CompletedProcess[str]:
    return completed_process(1, stdout="runner stdout", stderr="runner stderr")


class GitHubActionsDocumentProcessingTests(unittest.TestCase):
    def run_batch(self, root: Path, *extra: str, side_effect=fake_successful_runner) -> dict:
        pending = root / "pending"
        processed = root / "processed"
        failed = root / "failed"
        summary = root / "summary.json"
        args = [
            "--pending-dir",
            str(pending),
            "--processed-dir",
            str(processed),
            "--failed-dir",
            str(failed),
            "--output-summary",
            str(summary),
            *extra,
        ]
        with mock.patch.object(batch.subprocess, "run", side_effect=side_effect):
            exit_code = batch.main(args)
        self.assertEqual(exit_code, 0)
        return json.loads(summary.read_text(encoding="utf-8"))

    def test_batch_script_import_and_help_smoke(self) -> None:
        self.assertTrue(hasattr(batch, "process_pending"))
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--help"],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("--pending-dir", completed.stdout)
        self.assertIn("--commit-mode", completed.stdout)

    def test_pending_processed_failed_folder_logic_with_temp_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "pending").mkdir()
            summary = self.run_batch(root)
            self.assertTrue((root / "pending").is_dir())
            self.assertTrue((root / "processed").is_dir())
            self.assertTrue((root / "failed").is_dir())
            self.assertEqual(summary["success_count"], 0)

    def test_processes_one_txt_into_processed_source_reports_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            source = pending / "NIST sample.txt"
            source.write_text(POLICY_TEXT, encoding="utf-8")
            summary = self.run_batch(root)
            self.assertEqual(summary["success_count"], 1)
            run_root = next((root / "processed").iterdir())
            self.assertTrue((run_root / "source" / source.name).is_file())
            self.assertTrue(list((run_root / "reports").glob("*.laif.md")))
            self.assertTrue(list((run_root / "reports").glob("*.laif.json")))
            self.assertTrue((run_root / "reports" / "laif_processing_index.jsonl").is_file())
            metadata = json.loads((run_root / "metadata" / "run_metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["status"], "success")
            self.assertEqual(metadata["original_file_name"], source.name)

    def test_summary_success_count_and_copy_mode_leaves_pending(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            source = pending / "policy.txt"
            source.write_text(POLICY_TEXT, encoding="utf-8")
            summary = self.run_batch(root, "--commit-mode", "copy")
            self.assertEqual(summary["success_count"], 1)
            self.assertEqual(summary["failed_count"], 0)
            self.assertTrue(source.exists())

    def test_move_mode_removes_pending_source_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            source = pending / "policy.txt"
            source.write_text(POLICY_TEXT, encoding="utf-8")
            self.run_batch(root, "--commit-mode", "move")
            self.assertFalse(source.exists())
            self.assertTrue(list((root / "processed").glob("*/source/policy.txt")))

    def test_failure_path_writes_error_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            source = pending / "bad.txt"
            source.write_text("too short", encoding="utf-8")
            summary = self.run_batch(root, side_effect=fake_failing_runner)
            self.assertEqual(summary["failed_count"], 1)
            failed_root = next((root / "failed").iterdir())
            self.assertIn("runner stderr", (failed_root / "error.txt").read_text(encoding="utf-8"))
            metadata = json.loads((failed_root / "metadata" / "run_metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["status"], "failed")
            self.assertEqual(metadata["return_code"], 1)

    def test_duplicate_source_sha256_skipped_when_reprocess_false(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            source = pending / "policy.txt"
            source.write_text(POLICY_TEXT, encoding="utf-8")
            self.run_batch(root)
            summary = self.run_batch(root)
            self.assertEqual(summary["success_count"], 0)
            self.assertEqual(summary["skipped"][0]["reason"], "skipped_duplicate")

    def test_duplicate_processed_again_when_reprocess_true(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / "policy.txt").write_text(POLICY_TEXT, encoding="utf-8")
            self.run_batch(root)
            summary = self.run_batch(root, "--reprocess", "true")
            self.assertEqual(summary["success_count"], 1)
            self.assertEqual(len(list((root / "processed").iterdir())), 2)

    def test_max_files_limit_respected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            for index in range(3):
                (pending / f"policy-{index}.txt").write_text(POLICY_TEXT + str(index), encoding="utf-8")
            summary = self.run_batch(root, "--max-files", "2")
            self.assertEqual(summary["success_count"], 2)
            self.assertEqual(len([item for item in summary["skipped"] if item["reason"] == "skipped_max_files"]), 1)

    def test_gitkeep_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / ".gitkeep").write_text("", encoding="utf-8")
            summary = self.run_batch(root)
            self.assertEqual(summary["success_count"], 0)
            self.assertEqual(summary["skipped_count"], 0)

    def test_unsupported_extension_skipped_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / "image.png").write_text("not supported", encoding="utf-8")
            summary = self.run_batch(root)
            self.assertEqual(summary["success_count"], 0)
            self.assertEqual(summary["skipped"][0]["reason"], "skipped_unsupported")

    def test_workflow_yaml_exists_and_has_workflow_dispatch(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("LAIF Process Pending Documents", workflow)

    def test_workflow_has_commit_outputs_default_false(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("commit_outputs:", workflow)
        self.assertIn("default: false", workflow)
        self.assertIn("type: boolean", workflow)

    def test_workflow_uploads_artifact(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("actions/upload-artifact", workflow)
        self.assertIn("laif-batch-output", workflow)

    def test_workflow_does_not_write_under_reports(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertNotIn(" reports/", workflow)
        self.assertNotIn("reports/**", workflow)
        self.assertNotIn("git add reports", workflow)

    def test_docs_mention_public_repo_privacy_warning(self) -> None:
        docs = DOC_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("public repositories should not receive sensitive documents", docs)
        self.assertIn("commit_outputs=false", docs)

    def test_batch_script_shells_to_runner_and_does_not_import_assessment_engine(self) -> None:
        script = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn("laif_process_document.py", script)
        self.assertIn("subprocess.run", script)
        self.assertNotIn("import assessment_engine", script)
        self.assertNotIn("from assessment_engine", script)


if __name__ == "__main__":
    unittest.main(verbosity=2)
