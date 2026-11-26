import hashlib
import json
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from scripts.laif_check_workspace_export import check_export, check_review_bundle, ExportError


class WorkspaceExportTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.package_path = self.root / "selected.laif.json"
        self.source_path = self.root / "source.md"
        self.source_path.write_bytes(b"Original source\r\n")
        self.digest = hashlib.sha256(self.source_path.read_bytes()).hexdigest()
        self.revision = "a" * 40
        self.body = "# Assessment\n\nExact Markdown.\n"
        self.report_path = self.root / "full.laif.md"
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()
        self.artifact_path = self.artifacts / "source.laif.md"
        self.artifact_path.write_bytes(self.body.encode("utf-8"))
        self.package = {
            "workspace_export_schema": "laif.workspace-export.v1",
            "canonical_revision": self.revision,
            "source_metadata": {"id": "d1", "sha256": self.digest},
            "report_quality_review": {"notes": "checked"},
            "run": {
                "id": "run-1", "kind": "browser_pipeline", "documentId": "d1",
                "revision": self.revision, "sourceSha256": self.digest,
                "review": {"notes": "checked"},
                "files": {"pipeline/source.laif.md": self.body},
            },
        }
        self.write_package()
        self.write_report(self.body)

    def write_package(self):
        self.package_path.write_text(json.dumps(self.package), encoding="utf-8")

    def write_report(self, body, revision=None):
        self.report_path.write_text(
            f"> Canonical implementation: {revision or self.revision}\n"
            f"> Source SHA-256: {self.digest}\n\n{body}", encoding="utf-8"
        )

    def test_checks_downloaded_package_and_source_without_writing(self):
        result = check_export(self.package_path, source=self.source_path, report=self.report_path,
                              artifacts_dir=self.artifacts)
        self.assertEqual(result["source_file"], "SOURCE_BYTES_MATCH")
        self.assertEqual(result["markdown_report"], "HEADER_AND_EMBEDDED_BODY_MATCH")
        self.assertEqual(result["artifact_files_verified"], 1)
        self.assertEqual(result["shared_extraction"], "NOT_RECORDED")
        self.assertEqual(self.artifact_path.read_bytes(), self.body.encode("utf-8"))

    def shared_assessment(self):
        text = "🔍 Explain the decision."
        quote = text[2:]
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        witness = {"start_char": 2, "end_char": len(text), "exact_quote": quote,
                   "quote_sha256": hashlib.sha256(quote.encode("utf-8")).hexdigest()}
        method = {"extracted_text_sha256": text_hash, "method_sha256": "d" * 64,
                  "criteria": [{"components": [{"witnesses": [witness]}]}]}
        run = self.package["run"]
        run.update(extractedText=text, checks={"shared_extraction_match": True, "quotes_checked": 2},
                   payload={"processing_metadata": {"source_sha256": self.digest},
                            "assessment_result": {"automatic_criteria": deepcopy(method)}},
                   research={"source": {"source_sha256": self.digest, "extracted_text_sha256": text_hash},
                             "automatic_criteria": deepcopy(method)},
                   bundle={"quote_bank": [{"start_offset": 2, "end_offset": len(text),
                                           "exact_quote": quote, "source_sha256": self.digest}]})
        return run

    def write_shared_artifacts(self, run):
        paths = {"payload": "source.laif.json", "research": "source.research_data.json",
                 "bundle": "analyst_bundle.json"}
        for key, name in paths.items():
            run["files"][name] = json.dumps(run[key])
        self.write_package()
        return {f"files/{name}": run["files"][name].encode("utf-8") for name in paths.values()}

    def test_checks_unicode_extraction_and_both_sources_of_quotes_in_bundle(self):
        run = self.shared_assessment()
        result = check_review_bundle(self.write_bundle(edits=self.write_shared_artifacts(run)),
                                     source=self.source_path)
        self.assertEqual(result["shared_extraction"], "MATCH")
        self.assertEqual(result["quotation_spans_verified"], 2)

    def test_rejects_inconsistent_extraction_even_with_a_rebuilt_zip_manifest(self):
        for change, message in (
            ("text", "extraction identities differ"),
            ("source", "source identities differ"),
            ("offset", "quotation differs"),
            ("quote_sha256", "quotation does not match"),
            ("counts", "quote count differs"),
            ("artifact", "differs from its individual artifact"),
        ):
            with self.subTest(change=change):
                run = self.shared_assessment()
                if change == "text":
                    run["extractedText"] += " Changed source."
                if change == "source":
                    run["research"]["source"]["source_sha256"] = "e" * 64
                if change == "offset":
                    run["bundle"]["quote_bank"][0]["start_offset"] = 1
                if change == "quote_sha256":
                    witness = run["research"]["automatic_criteria"]["criteria"][0]["components"][0]["witnesses"][0]
                    witness["quote_sha256"] = "0" * 64
                if change == "counts":
                    run["checks"]["quotes_checked"] += 1
                artifacts = self.write_shared_artifacts(run)
                if change == "artifact":
                    run["bundle"]["quote_bank"].clear()
                with self.assertRaisesRegex(ExportError, message):
                    check_review_bundle(self.write_bundle(edits=artifacts))

    def test_retained_package_checks_header_only_and_handles_absent_source_metadata(self):
        self.package["run"].update(kind="imported_authored", files={})
        self.package["source_metadata"] = None
        self.write_package()
        result = check_export(self.package_path, report=self.report_path)
        self.assertEqual(result["source_metadata"], "NOT_INCLUDED")
        self.assertEqual(result["markdown_report"], "HEADER_MATCH_ONLY")
        self.assertEqual(result["source_file"], "NOT_REQUESTED")
        with self.assertRaisesRegex(ExportError, "no embedded artifacts"):
            check_export(self.package_path, artifacts_dir=self.artifacts)

    def test_disagreed_review_revision_and_source_ids_fail(self):
        for container, key, value, message in (
            (self.package, "canonical_revision", "b" * 40, "revisions differ"),
            (self.package, "report_quality_review", {}, "review records differ"),
            (self.package["source_metadata"], "id", "other", "source ID differs"),
            (self.package["source_metadata"], "sha256", "0" * 64, "source hashes differ"),
        ):
            with self.subTest(key=key):
                original = container[key]
                container[key] = value
                self.write_package()
                with self.assertRaisesRegex(ExportError, message):
                    check_export(self.package_path)
                container[key] = original

    def test_duplicate_keys_and_nonstandard_numbers_fail(self):
        self.package_path.write_text('{"run": {}, "run": {}}', encoding="utf-8")
        with self.assertRaisesRegex(ExportError, "duplicate"):
            check_export(self.package_path)
        self.package_path.write_text('{"run": NaN}', encoding="utf-8")
        with self.assertRaisesRegex(ExportError, "numeric constant"):
            check_export(self.package_path)

    def test_rejects_unsafe_artifact_paths_and_duplicate_flat_names(self):
        files = self.package["run"]["files"]
        for path, message in (
            ("../misplaced.md", "unsafe path"),
            ("folder/C:misplaced.md", "unsafe path"),
            ("other/SOURCE.LAIF.MD", "same download filename"),
        ):
            with self.subTest(path=path):
                files[path] = "Other text."
                self.write_package()
                with self.assertRaisesRegex(ExportError, message):
                    check_export(self.package_path)
                del files[path]

    def test_rejects_source_artifact_and_body_mismatches(self):
        self.source_path.write_bytes(b"Other source")
        with self.assertRaisesRegex(ExportError, "Supplied source bytes differ"):
            check_export(self.package_path, source=self.source_path)
        self.artifact_path.write_bytes(b"Other artifact")
        with self.assertRaisesRegex(ExportError, "Artifact bytes differ"):
            check_export(self.package_path, artifacts_dir=self.artifacts)
        self.write_report("Incorrect report body.")
        with self.assertRaisesRegex(ExportError, "embedded assessment body"):
            check_export(self.package_path, report=self.report_path)
        self.write_report(self.body, revision="b" * 40)
        with self.assertRaisesRegex(ExportError, "Markdown header"):
            check_export(self.package_path, report=self.report_path)

    def write_bundle(self, *, edits=None, manifest_edits=None, after_manifest=None):
        exported_at = '2026-11-26T06:00:00.000Z'
        files = {
            'START-HERE.txt': b'Use the review brief or full report.',
            'assessment.laif.json': json.dumps({**self.package, 'exportedAt': exported_at}).encode(),
            'report.laif.md': self.report_path.read_bytes(),
        }
        if self.package['run']['kind'] == 'browser_pipeline':
            files['review-brief.md'] = b'Check the original source.'
            files['files/source.laif.md'] = self.artifact_path.read_bytes()
        files.update(edits or {})
        manifest = {
            'schema': 'laif.workspace-review-bundle.v1', 'assessment_id': 'run-1',
            'canonical_revision': self.revision, 'source_sha256': self.digest, 'exported_at': exported_at,
            'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                      for name, data in files.items()},
        }
        manifest.update(manifest_edits or {})
        files.update(after_manifest or {})
        path = self.root / 'review.zip'
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)
            archive.writestr('manifest.json', json.dumps(manifest))
        return path

    def test_checks_bundle_in_place(self):
        archive = self.write_bundle()
        result = check_review_bundle(archive, source=self.source_path)
        self.assertEqual(result['bundle_files_verified'], 5)
        self.assertEqual(result['artifact_files_verified'], 1)
        self.assertEqual(result['source_file'], 'SOURCE_BYTES_MATCH')
        self.assertFalse((self.root / 'manifest.json').exists())

    def test_retained_bundle_reports_header_scope(self):
        self.package['run'].update(kind='imported_authored', files={})
        result = check_review_bundle(self.write_bundle())
        self.assertEqual(result['bundle_files_verified'], 3)
        self.assertEqual(result['markdown_report'], 'HEADER_MATCH_ONLY')
        self.assertEqual(result['artifact_files_verified'], 0)

    def test_bundle_rejects_mismatches_and_unexpected_files(self):
        for options, message in (
            ({'manifest_edits': {'assessment_id': 'another'}}, 'identity differs'),
            ({'after_manifest': {'report.laif.md': b'Changed report text'}}, 'differs from its manifest'),
            ({'edits': {'files/source.laif.md': b'Different saved report'}}, 'Artifact bytes differ'),
            ({'edits': {'notes.txt': b'Unrelated file'}}, 'inventory differs'),
            ({'edits': {'Files/SOURCE.LAIF.MD': b'Duplicate name'}}, 'duplicate or unsupported'),
        ):
            with self.subTest(options=options):
                with self.assertRaisesRegex(ExportError, message):
                    check_review_bundle(self.write_bundle(**options))

    def test_bundle_limits_are_checked_before_reading_file_data(self):
        archive = self.write_bundle()
        with patch('scripts.laif_check_workspace_export._BUNDLE_LIMIT', 1):
            with self.assertRaisesRegex(ExportError, 'bundle limits'):
                check_review_bundle(archive)


if __name__ == "__main__":
    unittest.main()
