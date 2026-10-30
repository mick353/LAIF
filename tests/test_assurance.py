#!/usr/bin/env python3
"""Offline adversarial/negative controls for LAIF optional assurance and calibration."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from laif_assurance import assess_assurance, digest_json, mutation_probes
from laif_calibration import calibrate, make_synthetic_corpus, wilson


class AssuranceFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policy = "The organisation shall allow authorised AI actions and block unauthorised tools.\n"
        self.policy_sha = self.write("policy.md", self.policy)
        self.appendix_sha = self.write("appendix.txt", "Tool access is checked at execution.\n")
        self.inventory = [{"id": "appendix", "required": True, "disposition": "inspected", "file": "appendix.txt",
                           "sha256": self.appendix_sha, "quote": "Tool access is checked"}]
        self.control = {"id": "execution-control", "claim_quote": self.policy.strip(), "required_source_ids": ["appendix"],
                        "execution_tests": []}
        self.manifest = {"policy_file": "policy.md", "policy_sha256": self.policy_sha,
                         "source_inventory": self.inventory,
                         "scope_attestation": {"reviewer": "fixture-author", "recorded_at_utc": "2026-10-30T00:00:00Z",
                                               "complete": True, "inventory_sha256": digest_json(self.inventory)},
                         "controls": [self.control]}
        self.add_receipt("positive", "ALLOW")
        self.add_receipt("negative", "BLOCK")

    def write(self, file, contents):
        path = self.root / file
        path.parent.mkdir(exist_ok=True, parents=True)
        if isinstance(contents, dict):
            contents = json.dumps(contents, sort_keys=True) + "\n"
        # Write the exact bytes being hashed: Windows text mode otherwise
        # translates LF into CRLF and invalidates fixture SHA-256 records.
        payload = contents.encode("utf-8")
        path.write_bytes(payload)
        return hashlib.sha256(payload).hexdigest()

    def add_receipt(self, kind, decision):
        tid = f"test-{kind}"
        document = {"control_id": "execution-control", "test_id": tid, "decision": decision,
                    "environment": "simulated", "run_id": tid + "-run", "toolchain_version": "fixture-v1",
                    "executed_at_utc": "2026-10-30T00:00:00Z"}
        file = f"{tid}.json"
        sha = self.write(file, document)
        self.control["execution_tests"].append({"kind": kind, "test_id": tid,
            "expected_action": "ALLOW" if kind == "positive" else "BLOCK",
            "receipt_file": file, "receipt_sha256": sha})

    def run_assurance(self, **kw):
        result = assess_assurance(self.manifest, self.root, strict_scope=True, strict_actions=True, **kw)
        return result["controls"][0]

    def status(self, **kw):
        return self.run_assurance(**kw)["status"]

    def annex(self, *, outcome="PASS"):
        auth_sha = self.write("approval.txt", "approved deploy-0001 execution in staging")
        log_sha = self.write("execution.txt", "run-0001 execution outcome recorded")
        review_sha = self.write("review.txt", "different reviewer reviewed run-0001 observed results")
        return {"schema": "laif.operational-annex.v1", "controls": [{
            "control_id": "execution-control", "deployment_id": "deploy-0001", "run_id": "run-0001",
            "executor": "operator-A", "reviewer": "reviewer-B", "toolchain_version": "v1.0",
            "environment": "staging", "executed_at_utc": "2026-10-30T01:00:00Z",
            "authorisation_issued_at_utc": "2026-10-30T00:30:00Z", "reviewed_at_utc": "2026-10-30T01:30:00Z",
            "authorisation_file": "approval.txt", "authorisation_sha256": auth_sha,
            "authorisation_quote": "approved deploy-0001 execution", "execution_log_file": "execution.txt",
            "execution_log_sha256": log_sha, "execution_log_quote": "execution outcome",
            "review_file": "review.txt", "review_sha256": review_sha,
            "review_quote": "different reviewer", "outcome": outcome}]}


class SourceScopeTests(AssuranceFixture):
    def test_fixture_hashes_match_actual_file_bytes(self):
        self.assertEqual(
            hashlib.sha256((self.root / "policy.md").read_bytes()).hexdigest(),
            self.manifest["policy_sha256"],
        )
        for entry in self.control["execution_tests"]:
            self.assertEqual(
                hashlib.sha256((self.root / entry["receipt_file"]).read_bytes()).hexdigest(),
                entry["receipt_sha256"],
            )

    def test_complete_scope_and_receipts_is_review_ready_only(self):
        row = self.run_assurance()
        self.assertEqual(row["status"], "REVIEW_READY")
        self.assertEqual(row["evidence_grade"], "EXECUTION_RECEIPT_CHECKED")
        self.assertEqual(row["original_status"], "POLICY_ONLY")
        self.assertEqual(row["scope_status"], "SOURCE_CHECKED")
        self.assertEqual(row["operational_annex"]["status"], "NOT_SUPPLIED")

    def test_optional_extension_keeps_legacy_manifest_verdict(self):
        self.manifest.pop("source_inventory")
        self.manifest.pop("scope_attestation")
        self.control.pop("required_source_ids")
        self.control.pop("execution_tests")
        legacy = assess_assurance(self.manifest, self.root)
        self.assertEqual(legacy["controls"][0]["status"], "POLICY_ONLY")
        self.assertEqual(legacy["controls"][0]["scope_status"], "NOT_CHECKED")

    def test_missing_inventory_fails_strict(self):
        del self.manifest["source_inventory"]
        self.assertEqual(self.status(), "SCOPE_UNDECLARED")

    def test_absent_scope_attestation_fails_strict(self):
        del self.manifest["scope_attestation"]
        self.assertEqual(self.status(), "SCOPE_UNDECLARED")

    def test_scope_attestation_binds_inventory_digest(self):
        self.inventory.append({"id": "other", "required": False, "disposition": "excluded", "reason": "not relevant"})
        self.assertEqual(self.status(), "SCOPE_UNDECLARED")

    def test_unreadable_required_appendix_blocks(self):
        self.inventory[0] = {"id": "appendix", "required": True, "disposition": "unreadable", "reason": "source missing"}
        self.assertEqual(self.status(), "SOURCE_INCOMPLETE")

    def test_excluded_required_appendix_blocks(self):
        self.inventory[0] = {"id": "appendix", "required": True, "disposition": "excluded", "reason": "outside original review"}
        self.assertEqual(self.status(), "SOURCE_INCOMPLETE")

    def test_referenced_source_missing_from_inventory_blocks(self):
        self.control["required_source_ids"] = ["appendix", "secret-attachment"]
        self.assertEqual(self.status(), "SOURCE_INCOMPLETE")

    def test_absent_required_source_mapping_blocks_in_strict_mode(self):
        del self.control["required_source_ids"]
        self.assertEqual(self.status(), "SCOPE_UNDECLARED")

    def test_optional_excluded_source_can_be_reported_without_false_failure(self):
        self.inventory.append({"id": "irrelevant", "required": False, "disposition": "excluded", "reason": "irrelevant marketing leaflet"})
        self.manifest["scope_attestation"]["inventory_sha256"] = digest_json(self.inventory)
        self.assertEqual(self.status(), "REVIEW_READY")

    def test_tampered_source_sha_blocks(self):
        self.write("appendix.txt", "tampered")
        self.assertEqual(self.status(), "SOURCE_INVALID")

    def test_unverified_source_quote_blocks(self):
        self.inventory[0]["quote"] = "invented appendix content"
        self.assertEqual(self.status(), "SOURCE_INVALID")

    def test_escaping_symlink_source_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.root / "offsite.txt"
            try:
                path.symlink_to(Path(td) / "missing")
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unsupported")
            self.inventory[0]["file"] = "offsite.txt"
            self.assertEqual(self.status(), "SOURCE_INVALID")

    def test_attribution_invariance(self):
        before = self.status()
        self.manifest["publisher"] = "Prestigious regulator"
        self.assertEqual(self.status(), before)
        self.manifest["publisher"] = "Unknown supplier"
        self.assertEqual(self.status(), before)

    def test_reversing_receipt_order_is_invariant(self):
        before = self.status()
        self.control["execution_tests"].reverse()
        self.assertEqual(self.status(), before)

    def test_existing_source_test_failure_cannot_be_overridden(self):
        x = {"type": "positive", "test_id": "self-reported-failure", "outcome": "FAIL",
             "file": "appendix.txt", "sha256": self.appendix_sha, "quote": "Tool access"}
        self.control["evidence"] = [x]
        self.assertEqual(self.status(), "OBSERVED_FAILURE")


class ActionMutationTests(AssuranceFixture):
    def test_disabling_every_check_is_detected(self):
        self.control["execution_tests"] = []
        self.assertEqual(self.status(), "INCOMPLETE_CONTROLS")

    def test_deleting_negative_test_is_detected(self):
        self.control["execution_tests"] = self.control["execution_tests"][:1]
        self.assertEqual(self.status(), "INCOMPLETE_CONTROLS")

    def test_missing_execution_records_is_detected(self):
        del self.control["execution_tests"]
        self.assertEqual(self.status(), "EXECUTION_UNTESTED")

    def test_constant_allow_behavior_fails_negative_test(self):
        self.control["execution_tests"] = []
        self.add_receipt("positive", "ALLOW")
        self.add_receipt("negative", "ALLOW")
        self.assertEqual(self.status(), "OBSERVED_FAILURE")

    def test_constant_block_behavior_fails_positive_test(self):
        self.control["execution_tests"] = []
        self.add_receipt("positive", "BLOCK")
        self.add_receipt("negative", "BLOCK")
        self.assertEqual(self.status(), "OBSERVED_FAILURE")

    def test_self_reported_pass_cannot_override_measured_negative_failure(self):
        self.control["execution_tests"] = []
        self.add_receipt("positive", "ALLOW")
        self.add_receipt("negative", "ALLOW")
        for x in self.control["execution_tests"]:
            x["outcome"] = "PASS"
        self.assertEqual(self.status(), "OBSERVED_FAILURE")

    def test_tampered_receipt_invalidates_result(self):
        self.control["execution_tests"][1]["receipt_sha256"] = "0" * 64
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_invalid_source_receipt_identity_blocks(self):
        entry = self.control["execution_tests"][1]
        receipt = json.loads((self.root / entry["receipt_file"]).read_text())
        receipt["control_id"] = "wrong-control"
        entry["receipt_sha256"] = self.write(entry["receipt_file"], receipt)
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_invalid_utc_and_version_blocks(self):
        entry = self.control["execution_tests"][0]
        receipt = json.loads((self.root / entry["receipt_file"]).read_text())
        receipt["executed_at_utc"] = "2026-10-30T04:00:00"  # offset absent
        receipt["toolchain_version"] = ""
        entry["receipt_sha256"] = self.write(entry["receipt_file"], receipt)
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_duplicate_execution_test_id_blocks(self):
        self.control["execution_tests"].append(dict(self.control["execution_tests"][0]))
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_test_kind_must_match_expected_action(self):
        self.control["execution_tests"][1]["expected_action"] = "ALLOW"
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_malformed_decision_type_is_diagnosed(self):
        entry = self.control["execution_tests"][0]
        receipt = json.loads((self.root / entry["receipt_file"]).read_text())
        receipt["decision"] = ["ALLOW"]
        entry["receipt_sha256"] = self.write(entry["receipt_file"], receipt)
        self.assertEqual(self.status(), "EVIDENCE_INVALID")

    def test_require_ready_cli_implicitly_requires_scope(self):
        self.manifest.pop("scope_attestation")
        path = self.root / "manifest.json"
        path.write_text(json.dumps(self.manifest), encoding="utf-8")
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "laif_assurance.py"), str(path),
                                "--require-review-ready"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("SCOPE_UNDECLARED", result.stdout)

    def test_real_receipt_action_overrides_reported_claim(self):
        assert self.status() == "REVIEW_READY"
        entry = self.control["execution_tests"][1]
        receipt = json.loads((self.root / entry["receipt_file"]).read_text())
        receipt["decision"] = "ALLOW"
        entry["receipt_sha256"] = self.write(entry["receipt_file"], receipt)
        self.assertEqual(self.status(), "OBSERVED_FAILURE")

    def test_four_synthetic_mutations_not_review_ready(self):
        probes = self.run_assurance(with_mutations=True)["mutation_probes"]
        self.assertEqual({x["intervention"] for x in probes}, {"remove_all_checks", "remove_negative_checks", "force_allow", "force_block"})
        self.assertTrue(all(x["caught"] for x in probes), probes)
        self.assertEqual({x["hypothetical_status"] for x in probes}, {"INCOMPLETE_CONTROLS", "OBSERVED_FAILURE"})

    def test_mutations_do_not_claim_to_execute_target(self):
        self.control["execution_tests"] = []
        probes = self.run_assurance(with_mutations=True)["mutation_probes"]
        self.assertIsNone(probes[0]["caught"])
        self.assertIn("baseline not review-ready", probes[0]["note"])


class OperationalAnnexTests(AssuranceFixture):
    def test_independent_reviewer_record_is_recorded_not_certified(self):
        row = self.run_assurance(annex=self.annex())
        self.assertEqual(row["status"], "REVIEW_READY")
        self.assertEqual(row["operational_annex"]["status"], "REVIEW_RECORDED")
        self.assertIn("not authenticated", row["operational_annex"]["boundary"])

    def test_missing_authorisation_is_invalid(self):
        annex = self.annex()
        del annex["controls"][0]["authorisation_sha256"]
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "ANNEX_INVALID")

    def test_forged_or_mutated_review_record_is_invalid(self):
        annex = self.annex()
        annex["controls"][0]["review_sha256"] = "f" * 64
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "ANNEX_INVALID")

    def test_self_review_not_accepted(self):
        annex = self.annex()
        annex["controls"][0]["reviewer"] = annex["controls"][0]["executor"]
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "ANNEX_INVALID")

    def test_failure_requires_retest(self):
        self.assertEqual(self.run_assurance(annex=self.annex(outcome="FAIL"))["operational_annex"]["status"], "RETEST_REQUIRED")

    def test_remediation_without_retest_requires_retest(self):
        annex = self.annex()
        sha = self.write("fix.txt", "corrected authorisation bug")
        annex["controls"][0]["remediation"] = {"change_ref": "commit-123", "file": "fix.txt", "sha256": sha,
                                                 "quote": "corrected authorisation"}
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "RETEST_REQUIRED")

    def test_retest_failure_is_not_accepted(self):
        annex = self.annex(outcome="FAIL")
        sha = self.write("retest.txt", "retest remained unsafe")
        annex["controls"][0]["retest"] = {"outcome": "FAIL", "file": "retest.txt", "sha256": sha,
                                           "quote": "remained unsafe", "executed_at_utc": "2026-10-30T02:00:00Z"}
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "RETEST_REQUIRED")

    def test_recorded_successful_retest_after_remediation_is_reviewable(self):
        annex = self.annex(outcome="FAIL")
        sha = self.write("fix.txt", "fixed control boundary")
        sha2 = self.write("retest.txt", "retest successfully blocked unauthorised action")
        annex["controls"][0]["remediation"] = {"change_ref": "commit-123", "file": "fix.txt", "sha256": sha, "quote": "fixed control"}
        annex["controls"][0]["retest"] = {"outcome": "PASS", "file": "retest.txt", "sha256": sha2,
                                           "quote": "retest successfully", "executed_at_utc": "2026-10-30T02:00:00Z"}
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "REVIEW_RECORDED")

    def test_earlier_retest_is_invalid(self):
        annex = self.annex(outcome="FAIL")
        sha = self.write("retest.txt", "retest says it passed")
        annex["controls"][0]["retest"] = {"outcome": "PASS", "file": "retest.txt", "sha256": sha,
                                           "quote": "retest says", "executed_at_utc": "2026-10-30T00:00:00Z"}
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "ANNEX_INVALID")

    def test_operational_annex_cannot_override_failed_control(self):
        self.control["execution_tests"] = []
        self.add_receipt("positive", "BLOCK")
        self.add_receipt("negative", "BLOCK")
        row = self.run_assurance(annex=self.annex())
        self.assertEqual(row["status"], "OBSERVED_FAILURE")
        self.assertEqual(row["operational_annex"]["status"], "REVIEW_RECORDED")

    def test_optional_operational_gate_rejects_missing_annex(self):
        path = self.root / "manifest.json"
        path.write_text(json.dumps(self.manifest), encoding="utf-8")
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "laif_assurance.py"), str(path),
                                "--strict-scope", "--strict-actions", "--require-operational-review"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("NOT_SUPPLIED", result.stdout)


    def test_unrelated_approval_and_review_records_fail_identity_check(self):
        annex = self.annex()
        rec = annex["controls"][0]
        rec["run_id"] = "another-run"
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "ANNEX_INVALID")

    def test_authorisation_after_execution_fails_temporal_check(self):
        annex = self.annex()
        annex["controls"][0]["authorisation_issued_at_utc"] = "2026-10-30T02:30:00Z"
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "ANNEX_INVALID")

    def test_unknown_annex_control_is_rejected(self):
        annex = self.annex()
        annex["controls"].append({"control_id": "not-in-manifest"})
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.run_assurance(annex=annex)

    def test_failure_without_recorded_remediation_is_not_rehabilitated_by_retest(self):
        annex = self.annex(outcome="FAIL")
        sha = self.write("retest.txt", "retest succeeded")
        annex["controls"][0]["retest"] = {"outcome": "PASS", "file": "retest.txt", "sha256": sha,
                                           "quote": "retest succeeded", "executed_at_utc": "2026-10-30T02:00:00Z"}
        self.assertEqual(self.run_assurance(annex=annex)["operational_annex"]["status"], "RETEST_REQUIRED")


class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "calibration"
        self.dataset = make_synthetic_corpus(self.root)
        self.manifest = json.loads(self.dataset.read_text(encoding="utf-8"))

    def test_deterministic_holdout_and_positive_negative_coverage(self):
        r = calibrate(self.manifest, self.root)
        self.assertEqual(r["metrics"]["development"]["n"], 4)
        self.assertEqual(r["metrics"]["holdout"]["n"], 4)
        self.assertEqual(r["metrics"]["holdout"]["FP"], 0)
        self.assertEqual(r["metrics"]["holdout"]["FN"], 0)
        self.assertEqual(r["human_adjudicated_cases"], 0)
        self.assertIn("Synthetic cases", r["boundary"])

    def test_holdout_tampering_detected_even_when_label_only_changes(self):
        self.manifest["cases"][-1]["gold_label"] = "NOT_READY"
        with self.assertRaisesRegex(ValueError, "holdout seal"):
            calibrate(self.manifest, self.root)

    def test_family_leakage_detected(self):
        self.manifest["cases"][4]["family"] = self.manifest["cases"][0]["family"]
        self.manifest["holdout_seal"] = __import__("laif_calibration").holdout_seal(self.manifest["cases"])
        with self.assertRaisesRegex(ValueError, "family leakage"):
            calibrate(self.manifest, self.root)

    def test_manifest_content_tampering_detected(self):
        case = self.manifest["cases"][0]
        (self.root / case["manifest_file"]).write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            calibrate(self.manifest, self.root)

    def test_human_adjudication_gate_rejects_synthetic_cases(self):
        with self.assertRaisesRegex(ValueError, "human-adjudicated"):
            calibrate(self.manifest, self.root, require_adjudicated=True)

    def test_human_label_cannot_be_asserted_without_votes_and_record(self):
        self.manifest["cases"][0]["label_provenance"] = "HUMAN_ADJUDICATED"
        with self.assertRaisesRegex(ValueError, "two distinct"):
            calibrate(self.manifest, self.root)

    def test_synthetic_corpus_is_byte_for_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as td:
            other = Path(td) / "calibration"
            make_synthetic_corpus(other)
            for p in self.root.rglob("*"):
                if p.is_file():
                    self.assertEqual(p.read_bytes(), (other / p.relative_to(self.root)).read_bytes())

    def test_wilson_handles_zero_denominators_and_small_samples(self):
        self.assertIsNone(wilson(0, 0))
        self.assertEqual(wilson(0, 1)[0], 0)
        self.assertEqual(wilson(1, 1)[1], 1)
        self.assertGreater(wilson(0, 1)[1], 0.5)

    def test_no_false_accuracy_claim_in_frozen_fixture_run(self):
        result = calibrate(self.manifest, self.root)
        self.assertIn("not field accuracy", result["boundary"])
        self.assertTrue(all(x["label_provenance"] == "SYNTHETIC" for x in result["cases"]))


if __name__ == "__main__":
    unittest.main()
