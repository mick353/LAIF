import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("regulatory_ingestion", ROOT / "scripts/laif_verify_regulatory_ingestion.py")
ingestion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingestion)


class RegulatoryIngestionTests(unittest.TestCase):
    def test_committed_pdf_raw_pages_and_quotes(self):
        self.assertEqual(sum(ingestion.verify_source(ROOT, key) for key in ingestion.IDS), 44)

    def fixture(self, root):
        key = ingestion.IDS[0]
        manifest_path = Path(f"docs/verified/manifests/{key}.json")
        manifest = json.loads((ROOT / manifest_path).read_text())
        paths = [manifest_path, Path(manifest["source_file"]),
                 Path("docs/verified/raw") / manifest["raw_filename"],
                 Path(manifest["page_index"]), Path(manifest["evidence_trace"]),
                 Path(manifest["assessment_reference"].split(" (", 1)[0])]
        for path in paths:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, root / path)
        return key, manifest

    def test_corrupt_raw_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            key, manifest = self.fixture(root)
            raw = root / "docs/verified/raw" / manifest["raw_filename"]
            raw.write_bytes(raw.read_bytes() + b" altered")
            with self.assertRaisesRegex(ValueError, "text hash mismatch"):
                ingestion.verify_source(root, key)

    def test_invented_quotation_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            key, manifest = self.fixture(root)
            path = root / manifest["evidence_trace"]
            evidence = json.loads(path.read_text())
            evidence["traces"][0]["matched_text"] = "invented evidence"
            path.write_text(json.dumps(evidence))
            with self.assertRaisesRegex(ValueError, "not an exact source slice"):
                ingestion.verify_source(root, key)

    def test_wrong_page_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            key, manifest = self.fixture(root)
            path = root / manifest["evidence_trace"]
            evidence = json.loads(path.read_text())
            evidence["traces"][0]["page"] = 1
            path.write_text(json.dumps(evidence))
            with self.assertRaisesRegex(ValueError, "escapes its source page"):
                ingestion.verify_source(root, key)

    def test_recorded_assessment_inputs_match_extraction(self):
        # The assessment hash refers to the canonical processor's normalised
        # text; source_sha256 refers to the original committed raw file bytes.
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from laif_process_document import extract_document
        for key in ingestion.IDS:
            with self.subTest(key=key):
                raw = ROOT / "docs/verified/raw" / f"{key}.md"
                path = ROOT / "docs/verification/2026-11-07/regulatory/reviewed-text" / key / f"{key}.laif.json"
                result = json.loads(path.read_text())["assessment_result"]
                text = extract_document(raw, "builtin").text
                self.assertEqual(result["source_sha256"], ingestion.digest(raw.read_bytes()))
                self.assertEqual(result["assessed_text_sha256"], ingestion.digest(text.encode()))
                for trace in result["evidence_traces"]:
                    if trace["start_char"] is not None:
                        self.assertEqual(text[trace["start_char"]:trace["end_char"]], trace["matched_text"])


if __name__ == "__main__":
    unittest.main()
