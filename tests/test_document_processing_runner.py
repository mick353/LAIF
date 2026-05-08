#!/usr/bin/env python3
"""Tests for the Phase 3T user-facing LAIF document processing runner."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "laif_process_document.py"

spec = importlib.util.spec_from_file_location("laif_process_document", SCRIPT)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


GOVERNANCE_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, audit, "
    "monitoring, appeal, evidence documentation, public service delivery, administrative "
    "review, procurement controls, vendor accountability, contract remedies, risk management, "
    "redress, traceability, safety, non-discrimination, and documented escalation."
)

CANONICAL_ABSENT_STRONG_TEXT = (
    "External framework for AI risk management requires transparency, accountability, "
    "human oversight, audit logging, monitoring, appeal rights, evidence documentation, "
    "risk controls, redress, traceability, safety, non-discrimination, vendor controls, "
    "procurement review, contract remedies, and administrative review for affected people."
)

UNSAFE_PUBLIC_PHRASES = (
    "Final verdict",
    "Primary Failure Modes",
    "legal or governance invalidity",
    "legally invalid",
    "governance-invalid",
    "governance-worthless",
    "structurally incoherent",
    "compliance rating",
    "certified compliant",
    "invalid under law",
    "unlawful",
    "must amend law",
)
RAW_REGEX_TOKENS = (r"\b", "(?:", "(?=", "(?!")


class DocumentProcessingRunnerTests(unittest.TestCase):
    def _write(self, directory: Path, name: str, text: str) -> Path:
        path = directory / name
        path.write_text(text, encoding="utf-8")
        return path

    def _run_cli(self, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_cli_help_import_smoke(self):
        completed = self._run_cli(["--help"])
        self.assertIn("Extract a local document and process it with LAIF", completed.stdout)
        self.assertTrue(hasattr(runner, "main"))

    def test_txt_extraction_uses_builtin_reader(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.txt", GOVERNANCE_TEXT)
            result = runner._extract_document_text(path, "auto")
        self.assertEqual(result.extractor_used, "builtin")
        self.assertIn("public service delivery", result.text)
        self.assertEqual(result.extraction_confidence, "high")

    def test_md_extraction_uses_builtin_reader(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.md", "# Policy\n\n" + GOVERNANCE_TEXT)
            result = runner._extract_document_text(path, "auto")
        self.assertEqual(result.extractor_used, "builtin")
        self.assertIn("# Policy", result.text)

    def test_empty_file_fails_clearly(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "empty.txt", "")
            with self.assertRaisesRegex(runner.ExtractionError, "safe minimum threshold"):
                runner._extract_document_text(path, "auto")

    def test_unsupported_file_fails_clearly_when_builtin_requested(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.xyz", GOVERNANCE_TEXT)
            completed = self._run_cli([str(path), "--extractor", "builtin", "--no-write"], check=False)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Built-in extraction supports only", completed.stderr)

    def test_auto_sector_selects_clinical(self):
        text = "Clinical patient diagnosis treatment safety risk governance " + GOVERNANCE_TEXT
        self.assertEqual(runner._auto_sector(text, "policy", "clinical.txt"), "clinical_ai")

    def test_auto_sector_selects_procurement_vendor_governance(self):
        text = "Procurement vendor contract supplier third-party acquisition governance " + GOVERNANCE_TEXT
        self.assertEqual(runner._auto_sector(text, "policy", "procurement.txt"), "procurement_vendor_governance")

    def test_auto_sector_defaults_to_general_ai_governance(self):
        text = "Responsible AI governance transparency accountability audit monitoring and redress."
        self.assertEqual(runner._auto_sector(text, "policy", "general.txt"), "general_ai_governance")

    def test_no_write_processes_without_writing_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "policy.txt", GOVERNANCE_TEXT)
            out = root / "out"
            completed = self._run_cli([str(path), "--output-dir", str(out), "--no-write"])
            self.assertIn("Assessment mode: external_framework", completed.stdout)
            self.assertFalse(out.exists())

    def test_written_outputs_contain_extraction_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "policy.txt", GOVERNANCE_TEXT)
            out = root / "out"
            completed = self._run_cli([str(path), "--output-dir", str(out)])
            self.assertIn("Markdown report:", completed.stdout)
            markdown_files = list(out.glob("*.laif.md"))
            json_files = list(out.glob("*.laif.json"))
            self.assertEqual(len(markdown_files), 1)
            self.assertEqual(len(json_files), 1)
            markdown = markdown_files[0].read_text(encoding="utf-8")
            payload = json.loads(json_files[0].read_text(encoding="utf-8"))
        self.assertIn("LAIF Document Processing Extraction Metadata", markdown)
        self.assertIn("Extractor used", markdown)
        self.assertIn("extraction_metadata", payload)
        self.assertIn("assessment_result", payload)

    def test_json_output_includes_extraction_metadata_and_assessment_result(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "policy.txt", GOVERNANCE_TEXT)
            out = root / "out"
            self._run_cli([str(path), "--output-dir", str(out), "--no-markdown"])
            payload = json.loads(next(out.glob("*.laif.json")).read_text(encoding="utf-8"))
        self.assertEqual(payload["extraction_metadata"]["extractor_used"], "builtin")
        self.assertEqual(payload["assessment_result"]["assessment_mode"], "external_framework")

    def test_runner_invokes_external_framework_by_default(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.txt", GOVERNANCE_TEXT)
            completed = self._run_cli([str(path), "--no-write"])
        self.assertIn("Assessment mode: external_framework", completed.stdout)

    def test_formal_laif_native_failure_remains_fail_for_external_document(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "external_policy.txt", CANONICAL_ABSENT_STRONG_TEXT)
            extraction = runner._extract_document_text(path, "auto")
            result = runner.assess(
                "external_policy",
                "policy",
                extraction.text,
                sector="general_ai_governance",
                assessment_mode="external_framework",
                provenance="LOCAL_FILE_EXTRACTION",
            )
        self.assertEqual(result["assessment_mode"], "external_framework")
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")
        self.assertIn("FAIL", result["external_framework_assessment"]["laif_native_certification_status"])

    def test_evidence_traces_use_extracted_text_exact_spans(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.txt", GOVERNANCE_TEXT)
            extraction = runner._extract_document_text(path, "auto")
            result = runner.assess(
                "policy",
                "policy",
                extraction.text,
                sector="government_service_delivery",
                assessment_mode="external_framework",
            )
        for trace in result.get("evidence_traces", []):
            if trace["start_char"] is not None:
                self.assertEqual(trace["matched_text"], extraction.text[trace["start_char"]:trace["end_char"]])

    def test_generated_report_avoids_unsafe_public_phrases(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.txt", GOVERNANCE_TEXT)
            extraction = runner._extract_document_text(path, "auto")
            result = runner.assess("policy", "policy", extraction.text, assessment_mode="external_framework")
            markdown = runner._markdown_with_extraction_metadata(
                runner.generate_markdown_report([result]), extraction.metadata(), "external_framework", "general_ai_governance"
            )
        for phrase in UNSAFE_PUBLIC_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, markdown)

    def test_generated_report_does_not_expose_raw_regex_output(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.txt", GOVERNANCE_TEXT)
            extraction = runner._extract_document_text(path, "auto")
            result = runner.assess("policy", "policy", extraction.text, assessment_mode="external_framework")
            markdown = runner._markdown_with_extraction_metadata(
                runner.generate_markdown_report([result]), extraction.metadata(), "external_framework", "general_ai_governance"
            )
        for token in RAW_REGEX_TOKENS:
            with self.subTest(token=token):
                self.assertNotIn(token, markdown)

    def test_optional_docling_and_markitdown_unavailable_degrade_gracefully(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "policy.docx", "not a real docx")
            completed = self._run_cli([str(path), "--extractor", "docling", "--no-write"], check=False)
            if runner._module_available("docling"):
                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("ModuleNotFoundError", completed.stderr)
            else:
                self.assertIn("Docling is not installed", completed.stderr)
            completed = self._run_cli([str(path), "--extractor", "markitdown", "--no-write"], check=False)
            if not runner._module_available("markitdown"):
                self.assertIn("MarkItDown is not installed", completed.stderr)
            else:
                self.assertNotIn("ModuleNotFoundError", completed.stderr)

    @unittest.skipUnless(runner._module_available("docx"), "python-docx is not installed")
    def test_python_docx_extraction_when_available(self):
        from docx import Document

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "policy.docx"
            doc = Document()
            doc.add_paragraph(GOVERNANCE_TEXT)
            doc.save(str(path))
            result = runner._extract_document_text(path, "python-docx")
        self.assertEqual(result.extractor_used, "python-docx")
        self.assertIn("AI governance policy", result.text)

    @unittest.skipUnless(runner._module_available("pypdf") or runner._module_available("PyPDF2"), "pypdf/PyPDF2 is not installed")
    def test_pypdf_optional_fixture_generation_skipped(self):
        self.skipTest("No complex binary PDF fixture is generated in Phase 3T tests.")

    def test_no_generated_repo_report_path_is_touched(self):
        reports_dir = REPO_ROOT / "reports"
        before = {p: p.stat().st_mtime_ns for p in reports_dir.glob("*")} if reports_dir.exists() else {}
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "policy.txt", GOVERNANCE_TEXT)
            self._run_cli([str(path), "--output-dir", str(root / "out")])
        after = {p: p.stat().st_mtime_ns for p in reports_dir.glob("*")} if reports_dir.exists() else {}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
