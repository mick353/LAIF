"""End-to-end checks for the local first-run guide and its output boundaries."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "laif_start.py"
SAMPLE = ROOT / "docs" / "examples" / "vendor-policy.md"


class GuidedStartTests(unittest.TestCase):
    def call(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, "-S", str(SCRIPT), str(SAMPLE), *map(str, args)],
            cwd=ROOT, input=input_text, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
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
            self.assertEqual(list(target.glob("*.candidate_review.json")), [])
            payload = json.loads(data[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["source"]["source_scope"], "excerpt")
            self.assertEqual(payload["source"]["source_sha256"],
                             hashlib.sha256(SAMPLE.read_bytes()).hexdigest())
            self.assertEqual(payload["status"], "AUTOMATIC_DOCUMENTARY_DRAFT")
            self.assertIn("Open the Research report named above", run.stdout)
            self.assertIn("Human review template", run.stdout)
            self.assertIn("What the document wording supports", run.stdout)
            self.assertIn("provisional rule-based documentary judgments", run.stdout)
            self.assertIn("NOT_ESTABLISHED means this scan lacked enough wording", run.stdout)
            self.assertIn("passage triage", run.stdout)
            self.assertIn("does not complete it", run.stdout)
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
            self.assertIn("scores, strengths, gaps and controls are interpretive suggestions", first.stdout)
            self.assertIn("What remains unestablished", first.stdout)
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

    def test_joined_review_saves_and_resume_command_preserves_generated_files(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "research"
            first = self.call("--task", "evidence", "--scope", "excerpt", "--yes",
                              "--review-now", "--analyst", "first-reader", "--output-dir", target,
                              input_text="a\nRelevant candidate\nq\n")
            self.assertEqual(first.returncode, 0, first.stderr)
            dossier = next(target.glob("*.research_data.json"))
            session = next(target.glob("*.candidate_review.json"))
            saved = json.loads(session.read_text(encoding="utf-8"))
            self.assertEqual(saved["decisions"]["E001"]["decision"], "ACCEPT_FOR_REVIEW")
            self.assertIn("Resume candidate review:", first.stdout)
            self.assertIn(str(dossier.resolve()), first.stdout)
            self.assertIn(str(SAMPLE.resolve()), first.stdout)
            dossier_bytes = dossier.read_bytes()
            session_bytes = session.read_bytes()
            repeat = self.call("--task", "evidence", "--yes", "--review-now",
                               "--output-dir", target, input_text="q\n")
            self.assertEqual(repeat.returncode, 2)
            self.assertIn("Output folder is not empty", repeat.stderr)
            self.assertEqual(dossier.read_bytes(), dossier_bytes)
            self.assertEqual(session.read_bytes(), session_bytes)
            resumed = subprocess.run(
                [sys.executable, "-S", str(ROOT / "scripts" / "laif_review_session.py"),
                 str(dossier), str(SAMPLE), "--analyst", "first-reader"],
                cwd=ROOT, input="n\nNeed operating record\nq\n", capture_output=True,
                text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            decisions = json.loads(session.read_text(encoding="utf-8"))["decisions"]
            self.assertEqual(decisions["E001"], saved["decisions"]["E001"])
            self.assertEqual(decisions["E002"]["decision"], "NEEDS_EVIDENCE")

    def test_review_now_rejects_modes_without_evidence_before_write(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results"
            for args in (("--task", "internal", "--review-now"),
                         ("--inspect-only", "--review-now")):
                with self.subTest(args=args):
                    result = self.call(*args, "--yes", "--output-dir", target)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("requires a generated evidence report", result.stderr)
                    self.assertFalse(target.exists())

    def test_unused_analyst_attribution_is_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results"
            cases = (
                ("--task", "evidence", "--yes", "--analyst", "reader"),
                ("--task", "internal", "--yes", "--analyst", "reader"),
                ("--inspect-only", "--analyst", "reader"),
            )
            for args in cases:
                with self.subTest(args=args):
                    result = self.call(*args, "--output-dir", target)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("--analyst", result.stderr)
                    self.assertFalse(target.exists())
            chosen_internal = self.call("--analyst", "reader", "--output-dir", target,
                                        input_text="2\n")
            self.assertEqual(chosen_internal.returncode, 2)
            self.assertIn("internal diagnostic does not record passage decisions", chosen_internal.stderr)
            self.assertFalse(target.exists())

    def test_interactive_report_can_stop_before_candidate_review(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "research"
            result = self.call("--task", "evidence", "--output-dir", target,
                               input_text="y\nn\n")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Review candidate passages now?", result.stdout)
            self.assertEqual(len(list(target.glob("*.research_data.json"))), 1)
            self.assertEqual(list(target.glob("*.candidate_review.json")), [])

    def test_eof_at_review_offer_reports_saved_state_and_preserves_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "research"
            result = self.call("--task", "evidence", "--output-dir", target,
                               input_text="y\n")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Report saved. Candidate review not started", result.stdout)
            self.assertIn("Resume candidate review:", result.stdout)
            self.assertNotIn("Stopped before report generation", result.stderr)
            self.assertEqual(len(list(target.glob("*.research_report.md"))), 1)
            self.assertEqual(len(list(target.glob("*.research_data.json"))), 1)
            self.assertEqual(len(list(target.glob("*.review_template.json"))), 1)
            self.assertEqual(list(target.glob("*.candidate_review.json")), [])
            existing = {path.name: path.read_bytes() for path in target.iterdir()}
            repeat = self.call("--task", "evidence", "--yes", "--output-dir", target)
            self.assertEqual(repeat.returncode, 2)
            self.assertIn("Output folder is not empty", repeat.stderr)
            self.assertEqual({path.name: path.read_bytes() for path in target.iterdir()}, existing)

    def test_interrupted_joined_review_preserves_decision_and_can_resume(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "research"
            first = self.call("--task", "evidence", "--yes", "--review-now",
                              "--analyst", "first-reader", "--output-dir", target,
                              input_text="a\nInspect source context\n")
            self.assertEqual(first.returncode, 2)
            self.assertIn("Check the saved review before resuming", first.stderr)
            dossier = next(target.glob("*.research_data.json"))
            session = next(target.glob("*.candidate_review.json"))
            saved = json.loads(session.read_text(encoding="utf-8"))
            self.assertEqual(list(saved["decisions"]), ["E001"])
            resumed = subprocess.run(
                [sys.executable, "-S", str(ROOT / "scripts" / "laif_review_session.py"),
                 str(dossier), str(SAMPLE), "--analyst", "first-reader"],
                cwd=ROOT, input="n\nNeed the operating record\nq\n", capture_output=True,
                text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            decisions = json.loads(session.read_text(encoding="utf-8"))["decisions"]
            self.assertEqual(decisions["E001"], saved["decisions"]["E001"])
            self.assertEqual(decisions["E002"]["decision"], "NEEDS_EVIDENCE")

    def test_default_synthetic_source_enters_joined_review(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "default"
            run = subprocess.run(
                [sys.executable, "-S", str(SCRIPT), "--yes", "--review-now",
                 "--analyst", "default-reader", "--output-dir", str(target)],
                cwd=ROOT, input="a\nInspect context\nq\n", capture_output=True,
                text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("Using the included synthetic example", run.stdout)
            self.assertIn("Candidate passage review", run.stdout)
            dossier = next(target.glob("*.research_data.json"))
            session = next(target.glob("*.candidate_review.json"))
            self.assertEqual(json.loads(dossier.read_text(encoding="utf-8"))["source"]["source_sha256"],
                             hashlib.sha256(SAMPLE.read_bytes()).hexdigest())
            self.assertEqual(len(json.loads(session.read_text(encoding="utf-8"))["decisions"]), 1)

    def test_authorised_source_with_shell_characters_stays_bound_to_its_own_review(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "authorised $ policy.md"
            source.write_bytes(SAMPLE.read_bytes())
            target = Path(temp) / "case's results"
            run = subprocess.run(
                [sys.executable, "-S", str(SCRIPT), str(source), "--task", "evidence",
                 "--yes", "--review-now", "--analyst", "case-reader",
                 "--output-dir", str(target)],
                cwd=ROOT, input="n\nRequest an operating record\nq\n", capture_output=True,
                text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            dossier = next(target.glob("*.research_data.json"))
            session = next(target.glob("*.candidate_review.json"))
            self.assertEqual(json.loads(dossier.read_text(encoding="utf-8"))["source"]["file_name"],
                             source.name)
            self.assertEqual(json.loads(session.read_text(encoding="utf-8"))["source_sha256"],
                             hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertIn(str(source.resolve()), run.stdout)
            if os.name == "nt":
                self.assertIn("case''s results", run.stdout)
                self.assertIn("'" + str(source.resolve()) + "'", run.stdout)


if __name__ == "__main__":
    unittest.main()
