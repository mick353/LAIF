#!/usr/bin/env python3
"""Phase 3T tests for the LAIF document processing runner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from assessment_engine import assess, generate_markdown_report
from scripts import laif_process_document as runner

STRONG_EXTERNAL_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, "
    "audit, monitoring, appeal, evidence documentation, public service delivery, "
    "and administrative review. Providers shall implement risk management, "
    "technical documentation, traceability, redress, review, escalation, and "
    "non-discrimination measures for high-risk AI systems."
)


class DocumentProcessingRunnerTests(unittest.TestCase):
    def run_cli(self, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "scripts/laif_process_document.py", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_cli_help_and_import_smoke(self) -> None:
        completed = self.run_cli(["--help"])
        self.assertIn("--extractor", completed.stdout)
        self.assertIn("--no-write", completed.stdout)
        self.assertTrue(hasattr(runner, "extract_document"))

    def test_txt_extraction_builtin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.txt"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            result = runner.extract_document(path, "builtin")
            self.assertEqual(result.extractor_used, "builtin")
            self.assertIn("transparency", result.text)

    def test_md_extraction_builtin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.md"
            path.write_text("# Policy\n\n" + STRONG_EXTERNAL_TEXT, encoding="utf-8")
            result = runner.extract_document(path, "builtin")
            self.assertEqual(result.extractor_used, "builtin")
            self.assertIn("# Policy", result.text)

    def test_empty_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "empty.txt"
            path.write_text("", encoding="utf-8")
            completed = self.run_cli([str(path), "--no-write"], check=False)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("safe minimum", completed.stderr)

    def test_unsupported_file_fails_when_no_extractor_can_handle_it(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "policy.unsupported"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            completed = self.run_cli([str(path), "--no-write"], check=False)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("Unsupported file type", completed.stderr)

    def test_optional_extractor_degradation_or_skip_if_not_installed(self) -> None:
        optional = {
            "docling": "docling",
            "markitdown": "markitdown",
            "python-docx": "docx",
            "pypdf": "pypdf",
        }
        for extractor, module_name in optional.items():
            with self.subTest(extractor=extractor):
                if importlib.util.find_spec(module_name) is None and extractor != "pypdf":
                    with self.assertRaises(runner.ExtractionError):
                        with tempfile.TemporaryDirectory() as td:
                            path = Path(td) / ("sample.docx" if extractor == "python-docx" else "sample.pdf")
                            path.write_bytes(b"not a real document")
                            runner.extract_document(path, extractor)
                elif extractor == "pypdf" and importlib.util.find_spec("pypdf") is None and importlib.util.find_spec("PyPDF2") is None:
                    with self.assertRaises(runner.ExtractionError):
                        with tempfile.TemporaryDirectory() as td:
                            path = Path(td) / "sample.pdf"
                            path.write_bytes(b"not a real pdf")
                            runner.extract_document(path, extractor)
                else:
                    self.assertTrue(True)

    def test_auto_sector_clinical_procurement_general(self) -> None:
        self.assertEqual(runner.auto_sector("clinical patient clinician safety incident"), "clinical_ai")
        self.assertEqual(runner.auto_sector("procurement vendor contract audit access"), "procurement_vendor_governance")
        self.assertEqual(runner.auto_sector("general transparency accountability governance"), "general_ai_governance")

    def test_no_write_writes_no_outputs_and_no_index(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            completed = self.run_cli([str(path), "--output-dir", str(out), "--no-write"])
            self.assertIn("Write mode: disabled", completed.stdout)
            self.assertFalse(out.exists())

    def test_write_enabled_creates_markdown_json_and_index(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            self.assertTrue(list(out.glob("*.laif.md")))
            self.assertTrue(list(out.glob("*.laif.json")))
            self.assertTrue((out / "laif_processing_index.jsonl").exists())

    def test_json_has_required_top_level_structure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            payload = json.loads(next(out.glob("*.laif.json")).read_text(encoding="utf-8"))
            self.assertEqual(set(payload), {"processing_metadata", "extraction_metadata", "assessment_result"})
            self.assertIn("processed_at_utc", payload["processing_metadata"])
            self.assertIn("source_sha256", payload["extraction_metadata"])

    def test_markdown_metadata_has_original_name_hash_and_processed_at(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "Policy Sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            markdown = next(out.glob("*.laif.md")).read_text(encoding="utf-8")
            self.assertIn("Original file name", markdown)
            self.assertIn("Policy Sample.txt", markdown)
            self.assertIn("Source SHA-256", markdown)
            self.assertIn("processed_at_utc", markdown)

    def test_index_appends_and_preserves_original_names_for_two_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "out"
            first = root / "NIST AI RMF 1.0 sample.txt"
            second = root / "Department Policy Sample.txt"
            first.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            second.write_text(STRONG_EXTERNAL_TEXT + " departmental software development release pipeline", encoding="utf-8")
            self.run_cli([str(first), "--output-dir", str(out)])
            self.run_cli([str(second), "--output-dir", str(out)])
            lines = [json.loads(line) for line in (out / "laif_processing_index.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(lines), 2)
            self.assertEqual({line["original_file_name"] for line in lines}, {first.name, second.name})
            for line in lines:
                self.assertTrue(line["markdown_output_path"].endswith(".laif.md"))
                self.assertTrue(line["json_output_path"].endswith(".laif.json"))
                self.assertIsInstance(line["evidence_trace_count"], int)
                self.assertIsInstance(line["remediation_patch_count"], int)

    def test_output_names_are_safe_stem_based_metadata_preserves_original_names(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "NIST AI RMF 1.0 sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            json_path = next(out.glob("*.laif.json"))
            self.assertEqual(json_path.name, "NIST-AI-RMF-1.0-sample.laif.json")
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["processing_metadata"]["original_file_name"], path.name)
            self.assertEqual(payload["processing_metadata"]["safe_output_stem"], "NIST-AI-RMF-1.0-sample")

    def test_default_mode_external_framework(self) -> None:
        parser = runner.build_parser()
        args = parser.parse_args(["input.txt"])
        self.assertEqual(args.mode, "external_framework")

    def test_formal_laif_native_failure_remains_fail_for_external_strong_signal_doc(self) -> None:
        result = assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")
        self.assertEqual(result["assessment_mode"], "external_framework")
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")

    def test_exact_evidence_traces_satisfy_matched_text_slice(self) -> None:
        result = assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")
        exact_traces = [t for t in result["evidence_traces"] if t.get("matched_text")]
        self.assertTrue(exact_traces)
        for trace in exact_traces:
            self.assertEqual(trace["matched_text"], STRONG_EXTERNAL_TEXT[trace["start_char"]:trace["end_char"]])

    def test_generated_report_unsafe_phrase_absence(self) -> None:
        report = generate_markdown_report([assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")])
        for phrase in ("Final verdict", "Primary Failure Modes", "This document fails formal LAIF v1.2 compliance"):
            self.assertNotIn(phrase, report)

    def test_raw_regex_absence(self) -> None:
        report = generate_markdown_report([assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")])
        for token in (r"\b", "(?:", "(?=", "(?!"):
            self.assertNotIn(token, report)

    def test_no_writes_under_reports(self) -> None:
        before = {p.name: p.stat().st_mtime_ns for p in (REPO_ROOT / "reports").glob("*")}
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
        after = {p.name: p.stat().st_mtime_ns for p in (REPO_ROOT / "reports").glob("*")}
        self.assertEqual(before, after)

    def test_source_sha256_matches_input_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.txt"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.assertEqual(runner.sha256_file(path), hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
