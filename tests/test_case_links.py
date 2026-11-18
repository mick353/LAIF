"""End-to-end identity, missingness and non-overwrite checks for case links."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import laif_case_links as case_links


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "laif_case_links.py"
EXAMPLE = ROOT / "docs" / "examples" / "synthetic-case-links.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CaseLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policy = self.root / "policy.txt"
        self.contract = self.root / "contract.txt"
        self.policy.write_text("The owner must request a test before release.\n", encoding="utf-8")
        self.contract.write_text("The provider shall supply a signed test record.\n", encoding="utf-8")
        self.manifest_path = self.root / "case.json"
        self.manifest = {
            "schema": "laif.case-links.v1", "case_id": "case-1",
            "question": "Does the policy request reach the agreement?", "analyst_id": "reader-1",
            "sources": [
                {"id": "p1", "role": "policy", "status": "SUPPLIED", "file": "policy.txt",
                 "sha256": digest(self.policy), "version": "v1", "origin": "operator-supplied copy"},
                {"id": "c1", "role": "contract", "status": "SUPPLIED", "file": "contract.txt",
                 "sha256": digest(self.contract), "version": "draft-2", "origin": "operator-supplied copy"},
                {"id": "t1", "role": "test", "status": "NOT_SUPPLIED",
                 "reason": "No test record was supplied."},
            ],
            "links": [
                {"id": "L1", "from": "p1", "to": "c1", "relationship": "declared requirement flow",
                 "from_quote": "The owner must request a test before release.",
                 "to_quote": "The provider shall supply a signed test record.",
                 "note": "Human to check whether these versions apply together."},
                {"id": "L2", "from": "c1", "to": "t1", "relationship": "requested test record",
                 "from_quote": "The provider shall supply a signed test record.",
                 "note": "Record unavailable in supplied case."},
            ],
        }
        self.write_manifest()

    def write_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2) + "\n", encoding="utf-8")

    def call(self, *args, manifest=None):
        return subprocess.run(
            [sys.executable, "-S", str(SCRIPT), str(manifest or self.manifest_path), *map(str, args)],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_supplied_quotes_and_missing_records_remain_distinct(self):
        before = {path.name: path.read_bytes() for path in (self.policy, self.contract, self.manifest_path)}
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("**policy:** SUPPLIED", result.stdout)
        self.assertIn("**test:** NOT_SUPPLIED", result.stdout)
        self.assertIn("**remedy:** NOT_DECLARED", result.stdout)
        self.assertIn("EXACT_TEXT_AT_BOTH_ENDPOINTS", result.stdout)
        self.assertIn("ENDPOINT_NOT_SUPPLIED", result.stdout)
        self.assertIn("Links are analyst declarations", self.call("--json").stdout)
        structured = json.loads(self.call("--json").stdout)
        self.assertEqual([row["status"] for row in structured["links"]],
                         ["EXACT_TEXT_AT_BOTH_ENDPOINTS", "ENDPOINT_NOT_SUPPLIED"])
        self.assertEqual(structured["sources"][0]["sha256"], digest(self.policy))
        self.assertEqual({path.name: path.read_bytes() for path in (self.policy, self.contract, self.manifest_path)}, before)

    def test_stale_or_escaped_source_fails_before_report_write(self):
        report = self.root / "output.md"
        self.contract.write_text("Changed agreement.\n", encoding="utf-8")
        stale = self.call("--report", report)
        self.assertEqual(stale.returncode, 2)
        self.assertIn("SHA-256 mismatch", stale.stderr)
        self.assertFalse(report.exists())
        self.contract.write_text("The provider shall supply a signed test record.\n", encoding="utf-8")
        self.manifest["sources"][1]["file"] = "../other.txt"
        self.write_manifest()
        escaped = self.call("--report", report)
        self.assertEqual(escaped.returncode, 2)
        self.assertIn("outside evidence root", escaped.stderr)
        self.assertFalse(report.exists())

    def test_wrong_quote_and_ambiguous_json_fail_closed(self):
        self.manifest["links"][0]["to_quote"] = "A nonexistent clause"
        self.write_manifest()
        wrong = self.call()
        self.assertEqual(wrong.returncode, 2)
        self.assertIn("exact source quotation not present", wrong.stderr)
        self.manifest_path.write_text('{"schema":"laif.case-links.v1","schema":"other"}', encoding="utf-8")
        duplicate = self.call()
        self.assertEqual(duplicate.returncode, 2)
        self.assertIn("duplicate key", duplicate.stderr)

    def test_declared_version_change_gets_new_manifest_identity(self):
        original = json.loads(self.call("--json").stdout)
        self.manifest["sources"][1]["version"] = "draft-3"
        self.write_manifest()
        revised = json.loads(self.call("--json").stdout)
        self.assertNotEqual(original["manifest_sha256"], revised["manifest_sha256"])
        self.assertEqual(original["sources"][1]["sha256"], revised["sources"][1]["sha256"])
        self.assertEqual(revised["sources"][1]["version"], "draft-3")

    def test_pure_byte_core_matches_cli_and_rejects_mismatched_inputs(self):
        raw = self.manifest_path.read_bytes()
        byte_map = {"p1": self.policy.read_bytes(), "c1": self.contract.read_bytes()}
        pure = case_links.assess_bytes(self.manifest, raw, byte_map)
        self.assertEqual(pure, json.loads(self.call("--json").stdout))
        self.assertIn("EXACT_TEXT_AT_BOTH_ENDPOINTS", case_links.render(pure))
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            case_links.assess_bytes(self.manifest, raw, {**byte_map, "c1": b"changed"})
        with self.assertRaisesRegex(ValueError, "exactly the declared SUPPLIED"):
            case_links.assess_bytes(self.manifest, raw, {**byte_map, "extra": b"bytes"})
        with self.assertRaisesRegex(ValueError, "manifest object does not match"):
            case_links.assess_bytes({**self.manifest, "case_id": "other"}, raw, byte_map)

    def test_report_refuses_overwrite_and_escapes_user_markup(self):
        self.manifest["links"][0]["note"] = "<script>bad</script> ![pixel](https://example.test/x)\x1b[2J"
        self.write_manifest()
        report = self.root / "output.md"
        first = self.call("--report", report)
        self.assertEqual(first.returncode, 0, first.stderr)
        output = report.read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;bad&lt;/script&gt;", output)
        self.assertNotIn("![pixel]", output)
        self.assertNotIn("\x1b", output)
        second = self.call("--report", report)
        self.assertEqual(second.returncode, 2)
        self.assertIn("report already exists; choose a new path", second.stderr)
        self.assertEqual(report.read_text(encoding="utf-8"), output)
        same_as_source = self.call("--report", self.policy)
        self.assertEqual(same_as_source.returncode, 2)
        self.assertEqual(digest(self.policy), self.manifest["sources"][0]["sha256"])

    def test_declared_missing_source_cannot_be_quoted_or_mixed_with_supplied(self):
        self.manifest["links"][1]["to_quote"] = "No record"
        self.write_manifest()
        bad_quote = self.call()
        self.assertEqual(bad_quote.returncode, 2)
        self.assertIn("cannot quote a NOT_SUPPLIED source", bad_quote.stderr)
        self.manifest["links"][1].pop("to_quote")
        self.manifest["sources"].append({"id": "t2", "role": "test", "status": "SUPPLIED",
                                         "file": "contract.txt", "sha256": digest(self.contract),
                                         "version": "v2", "origin": "operator-supplied copy"})
        self.write_manifest()
        mixed = self.call()
        self.assertEqual(mixed.returncode, 2)
        self.assertIn("supplied and NOT_SUPPLIED records conflict", mixed.stderr)

    def test_malformed_role_status_and_link_endpoints_have_clear_errors(self):
        for key, value in (("role", []), ("status", [])):
            with self.subTest(key=key):
                self.manifest["sources"][0][key] = value
                self.write_manifest()
                result = self.call()
                self.assertEqual(result.returncode, 2)
                self.assertIn("p1: invalid role or status", result.stderr)
                self.assertNotIn("unhashable", result.stderr)
                self.manifest["sources"][0][key] = "policy" if key == "role" else "SUPPLIED"
        for side in ("from", "to"):
            with self.subTest(side=side):
                original = self.manifest["links"][0][side]
                self.manifest["links"][0][side] = []
                self.write_manifest()
                result = self.call()
                self.assertEqual(result.returncode, 2)
                self.assertIn("L1: link must name two distinct declared sources", result.stderr)
                self.assertNotIn("unhashable", result.stderr)
                self.manifest["links"][0][side] = original

    def test_six_roles_keep_distinct_and_opposing_supplied_records(self):
        additions = (
            ("pr1", "procedure", "Procedure says proceed after review."),
            ("t2", "test", "A second test failed under different conditions."),
            ("i1", "incident", "An incident was recorded after release."),
            ("r1", "remedy", "A remedy was proposed but not completed."),
        )
        for sid, role, sentence in additions:
            path = self.root / f"{sid}.txt"
            path.write_text(sentence + "\n", encoding="utf-8")
            self.manifest["sources"].append({
                "id": sid, "role": role, "status": "SUPPLIED", "file": path.name,
                "sha256": digest(path), "version": "v1", "origin": "synthetic test",
            })
        test_path = self.root / "t1.txt"
        test_path.write_text("The first test passed under its stated conditions.\n", encoding="utf-8")
        self.manifest["sources"][2] = {
            "id": "t1", "role": "test", "status": "SUPPLIED", "file": test_path.name,
            "sha256": digest(test_path), "version": "v1", "origin": "synthetic test",
        }
        self.manifest["links"][1] = {
            "id": "L2", "from": "t1", "to": "t2", "relationship": "author asks reviewer to compare tests",
            "from_quote": "The first test passed under its stated conditions.",
            "to_quote": "A second test failed under different conditions.",
            "note": "Different conditions may explain the result; inspect both records.",
        }
        self.write_manifest()
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        structured = json.loads(self.call("--json").stdout)
        self.assertEqual(set(structured["roles"].values()), {"SUPPLIED"})
        self.assertEqual(len(structured["sources"]), 7)
        self.assertEqual(structured["links"][1]["status"], "EXACT_TEXT_AT_BOTH_ENDPOINTS")
        self.assertIn("The first test passed", result.stdout)
        self.assertIn("A second test failed", result.stdout)
        self.assertIn("Different conditions may explain", result.stdout)

    def test_bundled_synthetic_example_is_runnable_and_not_a_real_case(self):
        result = self.call(manifest=EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("synthetic-supplier-policy", result.stdout)
        self.assertIn("test:** NOT_SUPPLIED", result.stdout)
        self.assertIn("no LAIF assessment", result.stdout)


if __name__ == "__main__":
    unittest.main()
