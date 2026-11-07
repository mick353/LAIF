import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/laif_process_regulatory_sources.py"
spec = importlib.util.spec_from_file_location("regulatory_runner", SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class RegulatoryRunnerTests(unittest.TestCase):
    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(runner, "ROOT", root), patch.dict(sys.modules, {"pypdf": type(sys)("pypdf")}):
                result = runner.main(["--output-dir", str(root / "out"), "--source", "au_dta_policy_v2_1"])
                self.assertEqual(result, 2)

    def test_synthetic_pdf_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            directory = root / "docs/verified/manual_ingest"
            directory.mkdir(parents=True)
            (directory / runner.SOURCES["au_dta_policy_v2_1"]).write_bytes(b"%PDF-1.4\nfixture")
            fake = type("Result", (), {"returncode": 0})()
            hashes = {"au_dta_policy_v2_1": hashlib.sha256(b"%PDF-1.4\nfixture").hexdigest()}
            with patch.object(runner, "ROOT", root), patch.object(runner, "SOURCE_HASHES", hashes), patch.dict(sys.modules, {"pypdf": type(sys)("pypdf")}), patch.object(runner.subprocess, "run", return_value=fake):
                result = runner.main(["--output-dir", str(root / "out"), "--source", "au_dta_policy_v2_1"])
            self.assertEqual(result, 0)
            manifest = json.loads((root / "out/run_manifest.json").read_text())
            self.assertEqual(manifest["source_admission"], "NOT_PERFORMED")
            self.assertEqual(len(manifest["results"][0]["source_sha256"]), 64)

    def test_tampered_pdf_never_reaches_processor(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            directory = root / "docs/verified/manual_ingest"
            directory.mkdir(parents=True)
            (directory / runner.SOURCES["au_dta_policy_v2_1"]).write_bytes(b"%PDF-1.4\ntampered")
            with patch.object(runner, "ROOT", root), patch.dict(sys.modules, {"pypdf": type(sys)("pypdf")}), patch.object(runner.subprocess, "run") as run:
                result = runner.main(["--output-dir", str(root / "out"), "--source", "au_dta_policy_v2_1"])
            self.assertEqual(result, 2)
            run.assert_not_called()
            self.assertFalse((root / "out").exists())

    def test_evidence_and_git_descendants_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(runner, "ROOT", root), patch.dict(sys.modules, {"pypdf": type(sys)("pypdf")}):
                for path in ("docs/verified/raw", "reports/new", ".git/objects"):
                    with self.subTest(path=path):
                        self.assertEqual(runner.main(["--output-dir", str(root / path)]), 2)

if __name__ == "__main__":
    unittest.main()
