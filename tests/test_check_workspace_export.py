import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.laif_check_workspace_export import check_export, ExportError


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
        self.assertEqual(self.artifact_path.read_bytes(), self.body.encode("utf-8"))

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


if __name__ == "__main__":
    unittest.main()
