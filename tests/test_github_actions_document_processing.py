#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BATCH_SCRIPT = REPO_ROOT / "scripts" / "laif_batch_process_pending.py"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "laif_process_pending_documents.yml"
DOCS = REPO_ROOT / "docs" / "governance" / "GITHUB_ACTIONS_DOCUMENT_PROCESSING.md"

STRONG_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, audit, monitoring, appeal, "
    "evidence documentation, public service delivery, administrative review, risk management, and redress."
)


class GithubActionsDocumentProcessingTests(unittest.TestCase):
    def run_batch(self, root: Path, *extra: str) -> dict:
        pending = root / "pending"
        processed = root / "processed"
        failed = root / "failed"
        summaries = root / "batch_summaries"
        latest = root / "laif_batch_summary.json"
        pending.mkdir(exist_ok=True)
        completed = subprocess.run(
            [
                sys.executable,
                str(BATCH_SCRIPT),
                "--pending-dir",
                str(pending),
                "--processed-dir",
                str(processed),
                "--failed-dir",
                str(failed),
                "--batch-summaries-dir",
                str(summaries),
                "--output-summary",
                str(latest),
                *extra,
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("batch_run_id", completed.stdout)
        return json.loads(latest.read_text(encoding="utf-8"))

    def test_batch_script_import_help_smoke(self) -> None:
        completed = subprocess.run([sys.executable, str(BATCH_SCRIPT), "--help"], cwd=REPO_ROOT, text=True, capture_output=True, check=True)
        self.assertIn("--pending-dir", completed.stdout)
        self.assertIn("--batch-summaries-dir", completed.stdout)
        self.assertIn("--fail-fast", completed.stdout)

    def test_txt_processes_to_processed_layout_and_writes_latest_and_timestamped_summary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "pending" / "NIST sample.txt"
            source.parent.mkdir()
            source.write_text(STRONG_TEXT, encoding="utf-8")
            summary = self.run_batch(root, "--max-files", "5")
            self.assertEqual(summary["success_count"], 1)
            self.assertEqual(summary["failed_count"], 0)
            self.assertTrue(summary["batch_run_id"].endswith("__batch"))
            timestamped = Path(summary["timestamped_summary_path"])
            self.assertTrue(timestamped.exists())
            self.assertEqual(json.loads(timestamped.read_text(encoding="utf-8"))["batch_run_id"], summary["batch_run_id"])
            self.assertEqual(json.loads((root / "laif_batch_summary.json").read_text(encoding="utf-8"))["batch_run_id"], summary["batch_run_id"])
            self.assertTrue(list((root / "processed").glob("*/source/NIST sample.txt")))
            self.assertTrue(list((root / "processed").glob("*/reports/*.laif.md")))
            self.assertTrue(list((root / "processed").glob("*/reports/*.laif.json")))
            self.assertTrue(list((root / "processed").glob("*/reports/laif_processing_index.jsonl")))
            self.assertTrue(list((root / "processed").glob("*/metadata/metadata.json")))
            self.assertTrue(source.exists())
            self.assertEqual(summary["pending_dir"], str(root / "pending"))
            self.assertEqual(summary["batch_summaries_dir"], str(root / "batch_summaries"))

    def test_batch_summary_and_metadata_preserve_path_identity_and_duplicate_stems(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            first = pending / "NIST.AI.100-1.txt"
            second = pending / "NIST.AI.100-1.md"
            first.write_text(STRONG_TEXT + " pdf", encoding="utf-8")
            second.write_text(STRONG_TEXT + " docx", encoding="utf-8")
            summary = self.run_batch(root, "--max-files", "2")
            self.assertEqual(summary["success_count"], 2)
            names = {item["original_file_name"] for item in summary["successes"]}
            self.assertEqual(names, {"NIST.AI.100-1.txt", "NIST.AI.100-1.md"})
            for success in summary["successes"]:
                self.assertTrue(success.get("original_pending_path"))
                self.assertTrue(success.get("stored_source_path"))
                self.assertTrue(success.get("runner_input_path"))
                metadata = json.loads(Path(success["metadata_path"]).read_text(encoding="utf-8"))
                self.assertEqual(metadata["original_file_name"], success["original_file_name"])
                self.assertEqual(metadata["original_pending_path"], success["original_pending_path"])
                self.assertEqual(metadata["stored_source_path"], success["stored_source_path"])
                self.assertEqual(metadata["runner_input_path"], success["runner_input_path"])


    def test_batch_institutional_outputs_generated_and_compare_types(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / "NIST sample.txt").write_text(
                "AI Risk Management Framework voluntary non-sector-specific use-case agnostic govern map measure manage trustworthy AI. Organizations should document risks, assign accountability, monitor systems, and retain evidence.",
                encoding="utf-8",
            )
            (pending / "DTAC sample.txt").write_text(
                "Digital Technology Assessment Criteria clinical safety DCB0129 clinical safety case hazard log patient care NHS data protection interoperability. Suppliers must provide evidence and safety documentation.",
                encoding="utf-8",
            )
            summary = self.run_batch(root, "--max-files", "5")
            self.assertEqual(summary["success_count"], 2)
            self.assertEqual(len(list((root / "processed").glob("*/reports/*.institutional_report.md"))), 2)
            self.assertTrue(list((root / "processed").glob("*/reports/*.technical_appendix.md")))
            self.assertTrue(list((root / "processed").glob("*/reports/analyst/analyst_bundle.json")))
            batch_report = root / "batch_institutional_report.md"
            self.assertTrue(batch_report.exists())
            text = batch_report.read_text(encoding="utf-8")
            self.assertIn("Governance force comparison", text)
            self.assertIn("Document type summary", text)
            self.assertIn("NIST sample.txt", text)
            self.assertIn("DTAC sample.txt", text)
            for name in ("portfolio_gap_register.json", "portfolio_control_roadmap.md", "batch_quote_bank.md", "batch_ai_prompt.md", "batch_ai_input_bundle.json"):
                self.assertTrue((root / name).exists(), name)
            self.assertIn("batch_institutional_outputs", summary)


    def test_phase_3x_batch_report_uses_governance_force_matrix_language(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / "eu.txt").write_text(
                "Regulation laying down harmonised rules on artificial intelligence, high-risk AI systems, providers, deployers, conformity assessment, market surveillance. Providers shall maintain technical documentation, monitor incidents, and ensure evidence for post-market review.",
                encoding="utf-8",
            )
            (pending / "nist.txt").write_text(
                "AI Risk Management Framework voluntary non-sector-specific use-case agnostic govern map measure manage trustworthy AI. Organizations should document risks, assign accountability, monitor AI systems, review outcomes, manage incidents, and maintain evidence of risk management activities.",
                encoding="utf-8",
            )
            summary = self.run_batch(root, "--max-files", "5")
            report_path = Path(summary["batch_institutional_outputs"]["batch_institutional_report"])
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("Governance-force matrix", report)
            self.assertIn("Legal force", report)
            self.assertIn("Evidence sufficiency", report)
            self.assertIn("Strongest legal source", report)
            self.assertIn("Strongest voluntary governance design source", report)
            self.assertIn("Most urgent cross-document control gap", report)
            self.assertIn("Recommended combined operating model", report)
            self.assertNotIn("strongest deterministic evidence density", report)

    def test_move_mode_removes_pending_source_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "pending" / "move.txt"
            source.parent.mkdir()
            source.write_text(STRONG_TEXT, encoding="utf-8")
            summary = self.run_batch(root, "--commit-mode", "move")
            self.assertEqual(summary["success_count"], 1)
            self.assertFalse(source.exists())

    def test_failure_path_writes_failed_error_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "pending" / "bad.txt"
            source.parent.mkdir()
            source.write_text("too short", encoding="utf-8")
            summary = self.run_batch(root)
            self.assertEqual(summary["failed_count"], 1)
            self.assertTrue(list((root / "failed").glob("*/source/bad.txt")))
            self.assertTrue(list((root / "failed").glob("*/error.txt")))
            self.assertTrue(list((root / "failed").glob("*/metadata/metadata.json")))

    def test_duplicate_source_sha256_skipped_and_reprocess_runs_again(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "pending" / "dupe.txt"
            source.parent.mkdir()
            source.write_text(STRONG_TEXT, encoding="utf-8")
            first = self.run_batch(root)
            second = self.run_batch(root)
            self.assertEqual(first["success_count"], 1)
            self.assertEqual(second["success_count"], 0)
            self.assertEqual(second["skipped"][0]["reason"], "duplicate_source_sha256")
            third = self.run_batch(root, "--reprocess")
            self.assertEqual(third["success_count"], 1)
            self.assertEqual(len(list((root / "processed").glob("*/metadata/metadata.json"))), 2)

    def test_max_files_gitkeep_and_unsupported_extension(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            (pending / ".gitkeep").write_text("", encoding="utf-8")
            (pending / "a.txt").write_text(STRONG_TEXT + " a", encoding="utf-8")
            (pending / "b.txt").write_text(STRONG_TEXT + " b", encoding="utf-8")
            (pending / "z.exe").write_text("unsupported", encoding="utf-8")
            summary = self.run_batch(root, "--max-files", "1")
            self.assertEqual(summary["success_count"], 1)
            reasons = [item["reason"] for item in summary["skipped"]]
            self.assertIn("max_files_reached", reasons)
            self.assertIn("unsupported_extension", reasons)
            self.assertNotIn(".gitkeep", json.dumps(summary))

    def test_archive_mode_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "pending" / "archive.txt"
            source.parent.mkdir()
            source.write_text(STRONG_TEXT, encoding="utf-8")
            summary = self.run_batch(root, "--commit-mode", "archive")
            self.assertEqual(summary["success_count"], 1)
            self.assertTrue(source.exists())
            manifest = next((root / "processed").glob("*/archive_manifest.json"))
            self.assertEqual(json.loads(manifest.read_text(encoding="utf-8"))["commit_mode"], "archive")

    def test_workflow_shape_inputs_artifact_commit_paths_and_no_reports(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertTrue(WORKFLOW.exists())
        self.assertIn("workflow_dispatch:", text)
        for name in ("mode", "sector", "extractor", "commit_outputs", "commit_mode", "reprocess", "max_files"):
            self.assertIn(f"{name}:", text)
        self.assertIn("default: false", text)
        self.assertIn("laif_inputs/batch_summaries/**", text)
        self.assertIn("git add laif_inputs/processed laif_inputs/failed laif_inputs/batch_summaries laif_batch_summary.json", text)
        self.assertNotIn("reports/**", text)
        self.assertIn("python-docx pypdf", text)
        install_step = text.split("Install lightweight document extractors", 1)[1].split("Process pending documents", 1)[0].lower()
        self.assertNotIn("docling", install_step)

    def test_docs_privacy_warning_and_batch_summary_history(self) -> None:
        text = DOCS.read_text(encoding="utf-8").lower()
        self.assertIn("privacy", text)
        self.assertIn("public repository", text)
        self.assertIn("laif_batch_summary.json", text)
        self.assertIn("batch_summaries", text)

    def test_batch_script_shells_to_phase_3t_runner_and_does_not_import_engine(self) -> None:
        text = BATCH_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("scripts", text)
        self.assertIn("laif_process_document.py", text)
        self.assertNotIn("import assessment_engine", text)

    def test_repeated_two_batch_runs_produce_two_timestamped_summaries_latest_points_newest(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "pending"
            pending.mkdir()
            seen = []
            for idx in (1, 2):
                (pending / f"NIST sample {idx}.txt").write_text(STRONG_TEXT + f" {idx}", encoding="utf-8")
                summary = self.run_batch(root, "--max-files", "1")
                seen.append(summary["batch_run_id"])
                time.sleep(0.01)
            timestamped = sorted((root / "batch_summaries").glob("*.json"))
            self.assertEqual(len(timestamped), 2)
            latest = json.loads((root / "laif_batch_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(Path(latest["timestamped_summary_path"]).name, timestamped[-1].name)
            self.assertEqual(latest["batch_run_id"], seen[-1])


if __name__ == "__main__":
    unittest.main()
