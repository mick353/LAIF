#!/usr/bin/env python3
"""Regression tests for the LAIF document processing runner."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from scripts.laif_process_document import INDEX_FILE_NAME, process_document

SAMPLE_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, "
    "audit, monitoring, appeal, evidence documentation, public service delivery, "
    "and administrative review."
)


class DocumentProcessingRunnerTests(unittest.TestCase):
    def _write_input(self, root, name="Sample Policy.txt", text=SAMPLE_TEXT):
        input_path = Path(root) / name
        input_path.write_text(text, encoding="utf-8")
        return input_path

    def _run_write_enabled(self, root, name="Sample Policy.txt"):
        input_path = self._write_input(root, name=name)
        output_dir = Path(root) / "out"
        processed = process_document(input_path, output_dir=output_dir)
        return input_path, output_dir, processed

    def test_processing_metadata_includes_identity_fields(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, _, processed = self._run_write_enabled(td, name="NIST AI RMF 1.0 sample.txt")
            metadata = processed["extraction_metadata"]
            self.assertEqual(metadata["input_file_name"], input_path.name)
            self.assertEqual(metadata["original_file_name"], input_path.name)
            self.assertEqual(metadata["original_file_stem"], input_path.stem)
            self.assertEqual(metadata["file_extension"], input_path.suffix)
            self.assertEqual(metadata["safe_output_stem"], "NIST_AI_RMF_1.0_sample")
            self.assertTrue(metadata["processed_at_utc"].endswith("Z"))
            self.assertEqual(len(metadata["source_sha256"]), 64)
            self.assertEqual(metadata["extractor_requested"], "auto")
            self.assertEqual(metadata["extractor_used"], "text")
            self.assertGreater(metadata["extracted_characters"], 0)
            self.assertIn("extraction_confidence", metadata)
            self.assertIsInstance(metadata["extraction_warnings"], list)
            self.assertIsInstance(metadata["extraction_errors"], list)

    def test_markdown_metadata_includes_original_name_and_source_hash(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, output_dir, processed = self._run_write_enabled(td, name="Department Policy Sample.txt")
            md_files = list(output_dir.glob("*.laif.md"))
            self.assertEqual(len(md_files), 1)
            markdown = md_files[0].read_text(encoding="utf-8")
            self.assertIn(f"Original file name:** {input_path.name}", markdown)
            self.assertIn("Source SHA-256:**", markdown)
            self.assertIn(processed["extraction_metadata"]["source_sha256"], markdown)
            self.assertIn("Processed at UTC:**", markdown)
            self.assertIn("Extractor used:** text", markdown)
            self.assertIn("Extracted characters:**", markdown)
            self.assertIn("Assessment mode:** external_framework", markdown)
            self.assertIn("Sector profile:** general_ai_governance", markdown)

    def test_json_output_contains_top_level_processing_extraction_and_assessment(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, output_dir, _ = self._run_write_enabled(td)
            json_files = list(output_dir.glob("*.laif.json"))
            self.assertEqual(len(json_files), 1)
            payload = json.loads(json_files[0].read_text(encoding="utf-8"))
            self.assertIn("processing_metadata", payload)
            self.assertIn("extraction_metadata", payload)
            self.assertIn("assessment_result", payload)
            self.assertEqual(payload["processing_metadata"]["original_file_name"], input_path.name)
            self.assertEqual(payload["extraction_metadata"]["input_file_name"], input_path.name)
            self.assertEqual(payload["assessment_result"]["document_name"], input_path.name)

    def test_index_jsonl_created_and_includes_summary_fields(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, output_dir, processed = self._run_write_enabled(td)
            index_path = output_dir / INDEX_FILE_NAME
            self.assertTrue(index_path.exists())
            lines = [json.loads(line) for line in index_path.read_text(encoding="utf-8").splitlines() if line]
            self.assertEqual(len(lines), 1)
            record = lines[0]
            self.assertEqual(record["original_file_name"], input_path.name)
            self.assertTrue(record["processed_at_utc"].endswith("Z"))
            self.assertEqual(record["source_sha256"], processed["extraction_metadata"]["source_sha256"])
            self.assertTrue(record["markdown_output_path"].endswith(".laif.md"))
            self.assertTrue(record["json_output_path"].endswith(".laif.json"))
            self.assertIn("overall_readiness_score", record)
            self.assertIsInstance(record["evidence_trace_count"], int)
            self.assertIsInstance(record["remediation_patch_count"], int)
            self.assertEqual(record["extractor_used"], "text")

    def test_no_write_does_not_create_index_or_reports(self):
        with tempfile.TemporaryDirectory() as td:
            input_path = self._write_input(td)
            output_dir = Path(td) / "out"
            processed = process_document(input_path, output_dir=output_dir, no_write=True)
            self.assertFalse((output_dir / INDEX_FILE_NAME).exists())
            self.assertFalse(list(output_dir.glob("*.laif.md")))
            self.assertFalse(list(output_dir.glob("*.laif.json")))
            self.assertEqual(processed["processing_metadata"]["original_file_name"], input_path.name)

    def test_two_files_append_two_index_lines_and_preserve_names(self):
        with tempfile.TemporaryDirectory() as td:
            output_dir = Path(td) / "out"
            first = self._write_input(td, name="NIST AI RMF 1.0 sample.txt")
            second = self._write_input(td, name="Department Policy Sample.txt")
            process_document(first, output_dir=output_dir)
            process_document(second, output_dir=output_dir)
            md_files = list(output_dir.glob("*.laif.md"))
            json_files = list(output_dir.glob("*.laif.json"))
            self.assertEqual(len(md_files), 2)
            self.assertEqual(len(json_files), 2)
            lines = [json.loads(line) for line in (output_dir / INDEX_FILE_NAME).read_text(encoding="utf-8").splitlines() if line]
            self.assertEqual(len(lines), 2)
            self.assertEqual(
                {line["original_file_name"] for line in lines},
                {"NIST AI RMF 1.0 sample.txt", "Department Policy Sample.txt"},
            )

    def test_output_filenames_remain_safe_stem_based_and_metadata_preserves_original_name(self):
        with tempfile.TemporaryDirectory() as td:
            input_path, output_dir, processed = self._run_write_enabled(td, name="Policy: Unsafe & Characters?.txt")
            self.assertEqual(processed["extraction_metadata"]["safe_output_stem"], "Policy_Unsafe_Characters")
            self.assertEqual(processed["extraction_metadata"]["input_file_name"], input_path.name)
            self.assertTrue((output_dir / "Policy_Unsafe_Characters.laif.md").exists())
            self.assertTrue((output_dir / "Policy_Unsafe_Characters.laif.json").exists())
            payload = json.loads((output_dir / "Policy_Unsafe_Characters.laif.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["processing_metadata"]["safe_output_stem"], "Policy_Unsafe_Characters")
            self.assertEqual(payload["processing_metadata"]["original_file_name"], input_path.name)

    def test_corrected_wildcard_glob_patterns_are_used(self):
        with tempfile.TemporaryDirectory() as td:
            _, output_dir, _ = self._run_write_enabled(td)
            self.assertTrue(list(output_dir.glob("*.laif.md")))
            self.assertTrue(list(output_dir.glob("*.laif.json")))

    def test_cli_smoke_uses_wildcard_outputs_and_index(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            input_file = self._write_input(root, name="sample_policy.txt")
            output_dir = root / "out"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "laif_process_document.py"),
                    str(input_file),
                    "--output-dir",
                    str(output_dir),
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn("Assessment mode:", completed.stdout)
            self.assertIn("external_framework", completed.stdout)
            self.assertIn("Markdown report:", completed.stdout)
            self.assertIn("JSON report:", completed.stdout)
            self.assertTrue(list(output_dir.glob("*.laif.md")))
            self.assertTrue(list(output_dir.glob("*.laif.json")))
            self.assertTrue((output_dir / INDEX_FILE_NAME).exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
