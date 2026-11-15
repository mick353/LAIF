"""Actual source-bound save, resume and export checks for candidate review."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "examples" / "vendor-policy.md"
RESEARCH = ROOT / "scripts" / "laif_research_report.py"
REVIEW = ROOT / "scripts" / "laif_review_session.py"


class ReviewSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / SOURCE.name
        self.source.write_bytes(SOURCE.read_bytes())
        generated = subprocess.run(
            [sys.executable, "-S", str(RESEARCH), str(self.source), "--scope", "excerpt",
             "--output-dir", str(self.root / "dossier")],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        self.dossier = next((self.root / "dossier").glob("*.research_data.json"))
        self.session = self.dossier.with_name(
            self.dossier.name.removesuffix(".research_data.json") + ".candidate_review.json"
        )

    def call(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, "-S", str(REVIEW), str(self.dossier), str(self.source), *map(str, args)],
            cwd=ROOT, input=input_text, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_save_resume_and_summary_keep_unanswered_passages_unresolved(self):
        first = self.call("--analyst", "reviewer-1", input_text="a\nRelevant wording only\nq\n")
        self.assertEqual(first.returncode, 0, first.stderr)
        saved = json.loads(self.session.read_text(encoding="utf-8"))
        self.assertEqual(saved["decisions"]["E001"]["decision"], "ACCEPT_FOR_REVIEW")
        self.assertEqual(len(saved["decisions"]), 1)
        second = self.call("--analyst", "reviewer-1", input_text="n\nNeed an implementation log\nq\n")
        self.assertEqual(second.returncode, 0, second.stderr)
        resumed = json.loads(self.session.read_text(encoding="utf-8"))
        self.assertEqual(resumed["decisions"]["E001"], saved["decisions"]["E001"])
        self.assertEqual(resumed["decisions"]["E002"]["decision"], "NEEDS_EVIDENCE")
        summary = self.call("--summary")
        self.assertEqual(summary.returncode, 0, summary.stderr)
        self.assertIn("AUTHOR TRIAGE ONLY", summary.stdout)
        self.assertIn("UNREVIEWED", summary.stdout)
        self.assertIn("2/", summary.stdout)
        self.assertNotIn("SUPPORTED_IN_SCOPE", summary.stdout)

    def test_changed_source_and_method_block_resume_without_touching_session(self):
        first = self.call("--analyst", "reviewer-1", input_text="a\nCheck context\nq\n")
        self.assertEqual(first.returncode, 0, first.stderr)
        original_session = self.session.read_bytes()
        self.source.write_bytes(self.source.read_bytes() + b"\nChanged")
        stale = self.call("--summary")
        self.assertEqual(stale.returncode, 2)
        self.assertIn("Original source bytes changed", stale.stderr)
        self.assertEqual(self.session.read_bytes(), original_session)
        self.source.write_bytes(SOURCE.read_bytes())
        payload = json.loads(self.dossier.read_text(encoding="utf-8"))
        payload["method"]["renderer_sha256"] = "0" * 64
        self.dossier.write_text(json.dumps(payload), encoding="utf-8")
        stale_method = self.call("--summary")
        self.assertEqual(stale_method.returncode, 2)
        self.assertIn("method identity is stale", stale_method.stderr)
        self.assertEqual(self.session.read_bytes(), original_session)

    def test_rejects_tampered_decision_and_conflicting_analyst(self):
        first = self.call("--analyst", "reviewer-1", input_text="r\nNot relevant\nq\n")
        self.assertEqual(first.returncode, 0, first.stderr)
        other = self.call("--analyst", "reviewer-2", "--summary")
        self.assertEqual(other.returncode, 2)
        self.assertIn("Analyst ID differs", other.stderr)
        saved = json.loads(self.session.read_text(encoding="utf-8"))
        saved["decisions"]["E001"]["quote_sha256"] = "0" * 64
        self.session.write_text(json.dumps(saved), encoding="utf-8")
        tampered = self.call("--summary")
        self.assertEqual(tampered.returncode, 2)
        self.assertIn("invalid or stale", tampered.stderr)

    def test_export_escapes_authored_markup_and_refuses_overwrite(self):
        first = self.call("--analyst", "reviewer-1",
                          input_text="o\n<script>bad</script> ![pixel](https://example.test/x)\nq\n")
        self.assertEqual(first.returncode, 0, first.stderr)
        export = self.root / "review.md"
        done = self.call("--summary", "--export", export)
        self.assertEqual(done.returncode, 0, done.stderr)
        report = export.read_text(encoding="utf-8")
        self.assertIn("OUTSIDE\\_SCOPE", report)
        self.assertNotIn("<script>", report)
        self.assertNotIn("![pixel]", report)
        again = self.call("--summary", "--export", export)
        self.assertEqual(again.returncode, 2)
        self.assertEqual(export.read_text(encoding="utf-8"), report)

    def test_partial_session_and_unknown_choice_never_become_decisions(self):
        unknown = self.call("--analyst", "reviewer-1", input_text="x\nq\n")
        self.assertEqual(unknown.returncode, 0, unknown.stderr)
        self.assertFalse(self.session.exists())
        self.session.write_text('{"schema": "laif.candidate-review.v1",', encoding="utf-8")
        partial = self.session.read_bytes()
        resumed = self.call("--analyst", "reviewer-1", input_text="a\nAnything\n")
        self.assertEqual(resumed.returncode, 2)
        self.assertEqual(self.session.read_bytes(), partial)

    def test_orphaned_temporary_save_does_not_replace_last_complete_session(self):
        first = self.call("--analyst", "reviewer-1", input_text="a\nCheck context\nq\n")
        self.assertEqual(first.returncode, 0, first.stderr)
        complete = self.session.read_bytes()
        orphan = self.session.with_name(self.session.name + ".interrupted.tmp")
        orphan.write_bytes(b'{"schema": "laif.candidate-review.v1",')
        summary = self.call("--summary")
        self.assertEqual(summary.returncode, 0, summary.stderr)
        self.assertIn("1/", summary.stdout)
        self.assertEqual(self.session.read_bytes(), complete)
        self.assertTrue(orphan.exists())

    def test_non_object_dossier_and_session_fail_with_controlled_error(self):
        original_dossier = self.dossier.read_bytes()
        for malformed in ("[]", '"scalar"', "null"):
            self.dossier.write_text(malformed, encoding="utf-8")
            result = self.call("--summary")
            self.assertEqual(result.returncode, 2)
            self.assertIn("JSON object", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        self.dossier.write_bytes(original_dossier)
        for malformed in ("[]", '"scalar"', "null"):
            self.session.write_text(malformed, encoding="utf-8")
            result = self.call("--summary")
            self.assertEqual(result.returncode, 2)
            self.assertIn("JSON object", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
