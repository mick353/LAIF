"""End-to-end checks for the local first-run guide and its output boundaries."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "laif_start.py"
SAMPLE = ROOT / "docs" / "examples" / "vendor-policy.md"


class GuidedStartTests(unittest.TestCase):
    def call(self, *args):
        return subprocess.run(
            [sys.executable, "-S", str(SCRIPT), str(SAMPLE), *map(str, args)],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )

    def test_inspection_is_read_only_and_identifies_source(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results"
            run = self.call("--inspect-only", "--output-dir", target)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn(hashlib.sha256(SAMPLE.read_bytes()).hexdigest(), run.stdout)
            self.assertIn("Extraction warnings: none reported", run.stdout)
            self.assertIn("no report or processing index written", run.stdout)
            self.assertFalse(target.exists())

    def test_interactive_decline_leaves_no_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results"
            run = subprocess.run(
                [sys.executable, "-S", str(SCRIPT), str(SAMPLE),
                 "--output-dir", str(target)],
                cwd=ROOT, input="1\nn\n", capture_output=True, text=True,
                encoding="utf-8",
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("Choose 1 or 2", run.stdout)
            self.assertIn("Output folder:", run.stdout)
            self.assertIn("Stopped before report generation", run.stdout)
            self.assertFalse(target.exists())

    def test_evidence_path_preserves_source_and_cautious_status(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "research"
            run = self.call("--task", "evidence", "--scope", "excerpt",
                            "--yes", "--output-dir", target)
            self.assertEqual(run.returncode, 0, run.stderr)
            reports = list(target.glob("*.research_report.md"))
            data = list(target.glob("*.research_data.json"))
            templates = list(target.glob("*.review_template.json"))
            self.assertEqual((len(reports), len(data), len(templates)), (1, 1, 1))
            payload = json.loads(data[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["source"]["source_scope"], "excerpt")
            self.assertEqual(payload["source"]["source_sha256"],
                             hashlib.sha256(SAMPLE.read_bytes()).hexdigest())
            self.assertEqual(payload["status"], "EVIDENCE_INVENTORY_ONLY")
            self.assertIn("Open the Research report named above", run.stdout)
            self.assertIn("Human review template", run.stdout)
            templates[0].write_text("edited review", encoding="utf-8")
            again = self.call("--task", "evidence", "--scope", "excerpt",
                              "--yes", "--output-dir", target)
            self.assertEqual(again.returncode, 2)
            self.assertIn("Output folder is not empty", again.stderr)
            self.assertEqual(templates[0].read_text(encoding="utf-8"), "edited review")

    def test_internal_path_points_to_readable_report_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "diagnostic"
            args = ("--task", "internal", "--yes", "--output-dir", target)
            first = self.call(*args)
            self.assertEqual(first.returncode, 0, first.stderr)
            report = target / "vendor-policy.institutional_report.md"
            self.assertTrue(report.exists())
            self.assertIn(str(report), first.stdout)
            self.assertIn("interpretive internal diagnostic", first.stdout)
            before = report.read_bytes()
            second = self.call(*args)
            self.assertEqual(second.returncode, 2)
            self.assertIn("Output folder is not empty", second.stderr)
            self.assertEqual(report.read_bytes(), before)

    def test_partial_outputs_or_subfolders_block_both_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            for task, existing_name in (("evidence", "partial.research_data.json"),
                                        ("internal", "analyst")):
                with self.subTest(task=task):
                    target = Path(temp) / task
                    target.mkdir()
                    existing = target / existing_name
                    if task == "evidence":
                        existing.write_text("partial run", encoding="utf-8")
                    else:
                        existing.mkdir()
                    run = self.call("--task", task, "--yes", "--output-dir", target)
                    self.assertEqual(run.returncode, 2)
                    self.assertIn("Output folder is not empty", run.stderr)
                    self.assertEqual(list(target.iterdir()), [existing])
                    if task == "evidence":
                        self.assertEqual(existing.read_text(encoding="utf-8"), "partial run")

    def test_missing_source_and_unsupported_format_fail_before_write(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results"
            missing = subprocess.run(
                [sys.executable, "-S", str(SCRIPT), str(Path(temp) / "absent.md"),
                 "--yes", "--output-dir", str(target)],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(missing.returncode, 2)
            self.assertIn("Cannot inspect source", missing.stderr)
            self.assertFalse(target.exists())
            unsupported = Path(temp) / "archive.bin"
            unsupported.write_bytes(b"test")
            bad = subprocess.run(
                [sys.executable, "-S", str(SCRIPT), str(unsupported),
                 "--yes", "--output-dir", str(target)],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(bad.returncode, 2)
            self.assertIn("Supported local formats", bad.stderr)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
