#!/usr/bin/env python3
"""Phase 3U tests for GitHub Actions batch document processing."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github/workflows/document-processing.yml"
BATCH_SCRIPT = REPO_ROOT / "scripts/laif_batch_process_pending.py"

STRONG_EXTERNAL_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, "
    "audit, monitoring, appeal, evidence documentation, public service delivery, "
    "and administrative review. Providers shall implement risk management, "
    "technical documentation, traceability, redress, review, escalation, and "
    "non-discrimination measures for high-risk AI systems."
)


class GithubActionsDocumentProcessingTests(unittest.TestCase):
    def run_batch(self, root: Path, *, max_files: int = 1) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(BATCH_SCRIPT),
                "--pending-dir",
                str(root / "pending"),
                "--processed-dir",
                str(root / "processed"),
                "--failed-dir",
                str(root / "failed"),
                "--batch-summaries-dir",
                str(root / "batch_summaries"),
                "--output-summary",
                str(root / "laif_batch_summary.json"),
                "--max-files",
                str(max_files),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_workflow_preserves_commit_outputs_false_default(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("commit_outputs", workflow)
        self.assertIn("default: 'false'", workflow)

    def test_workflow_artifact_includes_batch_summaries(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("laif_inputs/batch_summaries/**", workflow)
        self.assertIn("laif_batch_summary.json", workflow)

    def test_workflow_commit_step_includes_batch_summaries(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("git add laif_inputs/processed laif_inputs/failed laif_inputs/batch_summaries laif_batch_summary.json", workflow)

    def test_batch_run_writes_latest_and_timestamped_summary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / "sample.txt").write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")

            self.run_batch(root)
            latest = root / "laif_batch_summary.json"
            self.assertTrue(latest.exists())
            latest_payload = json.loads(latest.read_text(encoding="utf-8"))
            self.assertTrue(latest_payload["batch_run_id"].endswith("__batch"))
            self.assertIn("timestamped_summary_path", latest_payload)
            timestamped_path = Path(latest_payload["timestamped_summary_path"])
            self.assertTrue(timestamped_path.exists())

            timestamped_payload = json.loads(timestamped_path.read_text(encoding="utf-8"))
            self.assertEqual(latest_payload["batch_run_id"], timestamped_payload["batch_run_id"])
            self.assertEqual(str(timestamped_path), timestamped_payload["timestamped_summary_path"])

    def test_repeated_runs_preserve_summary_history_and_latest_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()

            for idx in (1, 2):
                (pending / f"NIST sample {idx}.txt").write_text(
                    f"{STRONG_EXTERNAL_TEXT} Batch history sample {idx}.",
                    encoding="utf-8",
                )
                self.run_batch(root, max_files=1)
                latest_payload = json.loads((root / "laif_batch_summary.json").read_text(encoding="utf-8"))
                self.assertTrue(Path(latest_payload["timestamped_summary_path"]).exists())

            timestamped = sorted((root / "batch_summaries").glob("*.json"))
            self.assertEqual(2, len(timestamped))
            latest_payload = json.loads((root / "laif_batch_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(timestamped[-1].name, Path(latest_payload["timestamped_summary_path"]).name)
            batch_run_ids = [json.loads(path.read_text(encoding="utf-8"))["batch_run_id"] for path in timestamped]
            self.assertEqual(2, len(set(batch_run_ids)))


if __name__ == "__main__":
    unittest.main()
