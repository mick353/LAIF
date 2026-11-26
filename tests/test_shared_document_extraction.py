"""Shared processing input, stale file rejection and default-call compatibility."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from assessment_engine import assess
from scripts import laif_auto_criteria as automatic
from scripts import laif_process_document as processor
from scripts import laif_research_report as research


class SharedExtractionTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.source = self.root / "sample.md"
        self.source.write_bytes(b"# Review policy\r\nThe provider must explain each decision output to affected people.\r\n")

    def test_one_extraction_and_one_automatic_pass_per_delivered_report(self):
        with (patch.object(processor, "extract_document", wraps=processor.extract_document) as extract,
              patch.object(automatic, "judge", wraps=automatic.judge) as institution_judge,
              patch.object(research, "automatic_judge", wraps=research.automatic_judge) as dossier_judge,
              contextlib.redirect_stdout(io.StringIO())):
            prepared = processor.prepare_document(self.source, "builtin")
            institutional = self.root / "institutional"
            dossier_dir = self.root / "research"
            self.assertEqual(processor.main([str(self.source), "--extractor", "builtin", "--output-dir",
                                             str(institutional)], prepared=prepared), 0)
            self.assertEqual(research.main([str(self.source), "--date", "2026-11-26", "--output-dir",
                                            str(dossier_dir)], prepared=prepared), 0)
            self.assertEqual(extract.call_count, 1)
            self.assertEqual(institution_judge.call_count, 1)
            self.assertEqual(dossier_judge.call_count, 1)
        report = json.loads((institutional / "sample.laif.json").read_text(encoding="utf-8"))
        dossier = json.loads(next(dossier_dir.glob("*.research_data.json")).read_text(encoding="utf-8"))
        source_sha256 = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.assertEqual(report["processing_metadata"]["source_sha256"], source_sha256)
        self.assertEqual(dossier["source"]["source_sha256"], source_sha256)
        self.assertEqual(report["assessment_result"]["automatic_criteria"], dossier["automatic_criteria"])

    def test_prepared_document_rejects_changes_and_different_selectors(self):
        prepared = processor.prepare_document(self.source, "builtin")
        other = self.root / "other.md"
        other.write_bytes(self.source.read_bytes())
        for path, name in ((other, "builtin"), (self.source, "auto")):
            with self.subTest(path=path, extractor=name):
                with self.assertRaisesRegex(processor.ExtractionError, "path and extractor"):
                    processor.prepare_document(path, name, reuse=prepared)
        self.source.write_bytes(b"Replacement policy. The provider must maintain a testing record.\n")
        with self.assertRaisesRegex(processor.ExtractionError, "after document preparation"):
            processor.prepare_document(self.source, "builtin", reuse=prepared)

    def test_mutation_during_extraction_is_not_attributed_to_original(self):
        original_extract = processor.extract_document

        def edited(path, extractor):
            output = original_extract(path, extractor)
            path.write_bytes(b"Replacement source contents.\n")
            return output

        with patch.object(processor, "extract_document", side_effect=edited):
            with self.assertRaisesRegex(processor.ExtractionError, "during extraction"):
                processor.prepare_document(self.source, "builtin")

    def test_direct_engine_calls_keep_the_automatic_result_by_default(self):
        args = ("Example", "uploaded_document", self.source.read_text(encoding="utf-8"))
        baseline = assess(*args, assessment_mode="external_framework")
        deferred = assess(*args, assessment_mode="external_framework", include_automatic_criteria=False)
        self.assertEqual(len(baseline.pop("automatic_criteria")["criteria"]), 8)
        self.assertEqual(baseline, deferred)


if __name__ == "__main__":
    unittest.main()
