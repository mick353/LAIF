#!/usr/bin/env python3
"""Source-identity, negative-control and anti-gaming tests for LAIF evidence diagnostics."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from laif_evidence_checks import check_manifest

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "laif_evidence_checks.py"


class EvidenceChecksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.policy = "The operator shall monitor every tool call and block unauthorised execution."
        self.claim = self.policy
        self.policy_sha = self.write("policy.txt", self.policy)
        good = "test A: legitimate tool call allowed; test outcome PASS"
        blocked = "test B: unauthorised tool call blocked; test outcome PASS"
        self.good_sha = self.write("allowed.txt", good)
        self.blocked_sha = self.write("blocked.txt", blocked)
        self.control = {"id": "tool-authorisation", "claim_quote": self.claim,
                        "evidence": [self._test_record("positive", "legitimate", "allowed.txt", self.good_sha, good),
                                     self._test_record("negative", "bypass", "blocked.txt", self.blocked_sha, blocked)]}
        self.manifest = {"policy_file": "policy.txt", "policy_sha256": self.policy_sha,
                         "controls": [self.control]}

    def write(self, name, data):
        (self.root / name).write_text(data, encoding="utf-8")
        return hashlib.sha256(data.encode()).hexdigest()

    def _test_record(self, kind, test_id, filename, sha, quote, outcome="PASS"):
        return {"type": kind, "test_id": test_id, "file": filename, "sha256": sha,
                "quote": quote, "outcome": outcome}

    def status(self):
        return check_manifest(self.manifest, self.root)["controls"][0]["status"]

    def test_matched_positive_and_negative_controls_are_review_ready_only(self):
        outcome = check_manifest(self.manifest, self.root)
        self.assertEqual(self.status(), "REVIEW_READY")
        self.assertIn("human verification required", outcome["boundary"])
        self.assertEqual(outcome["controls"][0]["negative_tests"], 1)

    def test_policy_assertion_alone_is_not_verified(self):
        self.control["evidence"] = []
        self.assertEqual(self.status(), "POLICY_ONLY")

    def test_missing_negative_or_positive_controls_is_not_review_ready(self):
        for omit_type in ("negative", "positive"):
            with self.subTest(omit_type=omit_type):
                self.control["evidence"] = [t for t in self._example_evidence() if t["type"] != omit_type]
                self.assertEqual(self.status(), "INCOMPLETE_CONTROLS")

    def _example_evidence(self):
        return [self._test_record("positive", "legitimate", "allowed.txt", self.good_sha,
                          "test A: legitimate tool call allowed; test outcome PASS"),
                self._test_record("negative", "bypass", "blocked.txt", self.blocked_sha,
                          "test B: unauthorised tool call blocked; test outcome PASS")]

    def test_claim_must_appear_verbatim_in_source(self):
        self.control["claim_quote"] = "We guarantee 100 percent coverage."
        self.assertEqual(self.status(), "UNSUPPORTED_CLAIM")

    def test_modified_policy_fails_closed(self):
        (self.root / "policy.txt").write_text(self.policy + " changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            check_manifest(self.manifest, self.root)

    def test_tampered_artifact_and_invented_quote_do_not_count(self):
        self.control["evidence"][0]["sha256"] = "0" * 64
        self.assertEqual(self.status(), "EVIDENCE_INVALID")
        self.control["evidence"][0]["sha256"] = self.good_sha
        self.control["evidence"][0]["quote"] = "invented successful result"
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_outside_path_and_symlink_not_accepted(self):
        self.control["evidence"][0]["file"] = "../out-of-scope.txt"
        self.assertEqual(self.status(), "EVIDENCE_INVALID")
        self.control["evidence"][0]["file"] = "/tmp/somewhere.txt"
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_adverse_test_outcome_overrides_good_evidence(self):
        self.control["evidence"][1]["outcome"] = "FAIL"
        self.assertEqual(self.status(), "OBSERVED_FAILURE")

    def test_conflicting_same_test_identity_detected(self):
        t = dict(self.control["evidence"][1])
        t["outcome"] = "FAIL"
        self.control["evidence"].append(t)
        self.assertEqual(self.status(), "CONTRADICTORY_RECORDS")

    def test_duplicate_positive_outcome_cannot_inflate_coverage(self):
        self.control["evidence"].append(dict(self.control["evidence"][0]))
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_label_and_order_changes_do_not_change_evidence_verdict(self):
        original = self.status()
        self.manifest["policy_title"] = "Prestigious regulator"
        self.manifest["controls"][0]["evidence"].reverse()
        self.assertEqual(self.status(), original)
        self.manifest["policy_title"] = "Unknown startup"
        self.assertEqual(self.status(), original)

    def test_unrelated_file_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as other:
            target = Path(other) / "sensitive.txt"
            target.write_text("external test record", encoding="utf-8")
            link = self.root / "linked.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            self.control["evidence"][0]["file"] = "linked.txt"
            self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_empty_control_list_does_not_pass_strict_gate(self):
        self.manifest["controls"] = []
        path = self.root / "manifest.json"
        path.write_text(json.dumps(self.manifest), encoding="utf-8")
        result = subprocess.run([sys.executable, str(CHECKER), str(path), "--require-review-ready"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)

    def test_cli_strict_gate_fails_on_policy_only(self):
        self.control["evidence"] = []
        path = self.root / "manifest.json"
        path.write_text(json.dumps(self.manifest), encoding="utf-8")
        result = subprocess.run([sys.executable, str(CHECKER), str(path), "--require-review-ready"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('"status": "POLICY_ONLY"', result.stdout)


if __name__ == "__main__":
    unittest.main()
