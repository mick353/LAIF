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
        self.assertEqual(sum(ingestion.verify_source(ROOT, key) for key in ingestion.IDS), 45)

    def test_authored_findings_bind_current_reports_framework_and_evidence(self):
        for key in ingestion.IDS:
            self.assertEqual(ingestion.verify_decisions(ROOT, key), 8)

    def decision_fixture(self, root):
        key = "eu_ai_act_amendment_2026_1744"
        directory = Path("docs/verification/2026-11-07/regulatory")
        paths = [directory / (key + ".decisions.json"), directory / (key + ".assessment.md"),
                 directory / "original_act_substantive_evidence.json",
                 Path(f"docs/verified/manifests/{key}.json"),
                 Path(f"docs/verified/extracted/{key}.evidence.json"),
                 Path("LAIF_v1.2.txt"), Path("LAIF_Compliance_Toolkit.txt")]
        for path in paths:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, root / path)
        return key, root / directory / (key + ".decisions.json")

    def test_stale_report_or_framework_identity_rejected(self):
        for field in ("assessment_sha256", "framework_sha256", "toolkit_sha256", "source_pdf_sha256"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                key, path = self.decision_fixture(root)
                data = json.loads(path.read_text())
                data[field] = "0" * 64
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, "hash mismatch"):
                    ingestion.verify_decisions(root, key)

    def test_missing_or_duplicated_calibration_review_rejected(self):
        for mode in ("missing", "duplicate", "malformed"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                key, path = self.decision_fixture(root)
                data = json.loads(path.read_text())
                rows = data["criteria_findings"]
                if mode == "missing":
                    rows.pop(3)
                else:
                    rows[3]["criterion_id"] = "A.3" if mode == "duplicate" else []
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, "eight distinct"):
                    ingestion.verify_decisions(root, key)

    def test_unsupported_or_cross_document_reference_rejected(self):
        for reference in ("EUO-INVENTED", "au_dta_policy_v2_1-Q001"):
            with self.subTest(reference=reference), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                key, path = self.decision_fixture(root)
                data = json.loads(path.read_text())
                data["applicability_cases"][0]["trace_ids"] = [reference]
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, "evidence reference"):
                    ingestion.verify_decisions(root, key)

    def test_distinct_transition_dates_have_distinct_provision_evidence(self):
        key = "eu_ai_act_amendment_2026_1744"
        directory = ROOT / "docs/verification/2026-11-07/regulatory"
        data = json.loads((directory / (key + ".decisions.json")).read_text())
        cases = {row["case_id"]: row for row in data["applicability_cases"]}
        # The new Article 5 date cannot be supported by the unrelated Article 50 deadline.
        self.assertIn(key + "-Q028", cases["C05"]["trace_ids"])
        self.assertNotIn(key + "-Q021", cases["C05"]["trace_ids"])
        self.assertEqual(cases["C04"]["trace_ids"], ["EUO-111-1"])
        context = json.loads((directory / "original_act_substantive_evidence.json").read_text())
        paragraph = next(row["matched_text"] for row in context["traces"] if row["trace_id"] == "EUO-111-1")
        self.assertIn("31 December 2030", paragraph)
        self.assertNotIn("2 August 2030", paragraph)

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
