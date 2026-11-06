#!/usr/bin/env python3
"""Synthetic, offline negative-control tests for optional frontier evidence review."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from laif_assurance import digest_json
from laif_frontier_assurance import CONTROL_CATEGORIES, RISK_CATEGORIES, review_frontier

AS_OF = datetime(2026, 11, 6, 12, tzinfo=timezone.utc)
DEPLOYMENT = "fixture-deployment"
REVISION = "fixture-model-revision-7"


class FrontierFixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.policy = "".join(f"{category} shall allow authorised acts and block unsafe acts.\n" for category in CONTROL_CATEGORIES)
        policy_sha = self.write("policy.md", self.policy)
        appendix_sha = self.write("appendix.txt", "All controls have pre-deployment limits and human review.\n")
        inventory = [{"id": "appendix", "required": True, "disposition": "inspected", "file": "appendix.txt",
                      "sha256": appendix_sha, "quote": "pre-deployment limits"}]
        controls = []
        operations = []
        mapping = []
        for category in CONTROL_CATEGORIES:
            cases = []
            for kind, observed in (("positive", "ALLOW"), ("negative", "BLOCK")):
                tid = f"{category}-{kind}"
                filename = f"receipt-{tid}.json"
                sha = self.write(filename, {"control_id": category, "test_id": tid, "decision": observed,
                     "run_id": tid, "environment": "staging", "toolchain_version": "fixture-v1",
                     "deployment_id": DEPLOYMENT, "model_revision": REVISION,
                     "executed_at_utc": "2026-11-04T09:00:00Z"})
                cases.append({"kind": kind, "test_id": tid, "expected_action": observed,
                              "receipt_file": filename, "receipt_sha256": sha})
            controls.append({"id": category, "claim_quote": f"{category} shall allow authorised acts and block unsafe acts.",
                             "required_source_ids": ["appendix"], "execution_tests": cases})
            auth_sha = self.write(f"auth-{category}.txt", f"Approved {DEPLOYMENT} for test {category}")
            execution_sha = self.write(f"log-{category}.txt", f"Evidence for run-{category} and subsequent review")
            review_sha = self.write(f"review-{category}.txt", f"Independent review of run-{category}")
            operations.append({"control_id": category, "deployment_id": DEPLOYMENT, "model_revision": REVISION,
                "run_id": f"run-{category}", "executor": "test-executor", "reviewer": "safety-reviewer",
                "toolchain_version": "fixture-v1", "environment": "staging", "outcome": "PASS",
                "authorisation_issued_at_utc": "2026-11-04T08:00:00Z",
                "executed_at_utc": "2026-11-04T09:00:00Z", "reviewed_at_utc": "2026-11-04T10:00:00Z",
                "authorisation_file": f"auth-{category}.txt", "authorisation_sha256": auth_sha,
                "authorisation_quote": "Approved", "execution_log_file": f"log-{category}.txt",
                "execution_log_sha256": execution_sha, "execution_log_quote": "Evidence for",
                "review_file": f"review-{category}.txt", "review_sha256": review_sha,
                "review_quote": "Independent review"})
            mapping.append({"category": category, "control_id": category,
                            "enforcement_boundary": "infrastructure"})
        self.core = {"policy_file": "policy.md", "policy_sha256": policy_sha,
                     "deployment_id": DEPLOYMENT, "model_revision": REVISION,
                     "source_inventory": inventory,
                     "scope_attestation": {"reviewer": "human-attestor", "recorded_at_utc": "2026-11-04T08:00:00Z",
                                           "complete": True, "inventory_sha256": digest_json(inventory)},
                     "controls": controls}
        self.operations = {"schema": "laif.operational-annex.v1", "controls": operations}
        self.threats = {"deployment_id": DEPLOYMENT, "model_revision": REVISION,
                        "owner": "technical-lead", "reviewer": "risk-reviewer",
                        "reviewed_at_utc": "2026-11-04T11:00:00Z", "risks": [
            {"category": risk, "protected_interest": "public safety and effective human control",
             "failure_pathway": f"unauthorised {risk} actions", "control_owner": "safety-officer",
             "trigger": "increased AI autonomy", "stop_condition": "unapproved action observed",
             "test_method": "adversarial bounded test"} for risk in RISK_CATEGORIES]}
        self.evals = []
        for category in RISK_CATEGORIES:
            filename = f"eval-{category}.json"
            report_name = f"eval-report-{category}.json"
            report_sha = self.write(report_name, {"run_id": f"eval-{category}", "model_revision": REVISION,
                                                  "decision": "CLEAR", "observations": ["synthetic negative control"]})
            sha = self.write(filename, {"deployment_id": DEPLOYMENT, "model_revision": REVISION,
                 "category": category, "run_id": f"eval-{category}", "method_id": "synthetic-protocol-v1",
                 "toolchain_version": "fixture-v1", "decision": "CLEAR", "environment": "staging",
                 "evaluator": "evaluator-A", "reviewer": "reviewer-B",
                 "test_report": {"file": report_name, "sha256": report_sha},
                 "executed_at_utc": "2026-11-05T09:00:00Z", "reviewed_at_utc": "2026-11-05T10:00:00Z"})
            self.evals.append({"category": category, "receipt_file": filename, "receipt_sha256": sha})
        self.approval = {"deployment_id": DEPLOYMENT, "model_revision": REVISION,
                         "decision": "RELEASE", "approver": "responsible-officer",
                         "approved_at_utc": "2026-11-06T09:00:00Z"}
        self.manifest = {"schema": "laif.frontier-assurance.v1", "deployment_id": DEPLOYMENT,
                         "model_revision": REVISION, "last_material_change_at_utc": "2026-11-03T08:00:00Z",
                         "review_due_at_utc": "2026-12-06T12:00:00Z",
                         "capability_evaluations": self.evals, "control_map": mapping}
        self.sync()

    def write(self, filename, payload):
        if isinstance(payload, dict):
            payload = json.dumps(payload, sort_keys=True) + "\n"
        encoded = payload.encode("utf-8")
        (self.root / filename).write_bytes(encoded)
        return hashlib.sha256(encoded).hexdigest()

    def sync(self):
        self.manifest["core_manifest"] = {"file": "core.json", "sha256": self.write("core.json", self.core)}
        self.manifest["operational_annex"] = {"file": "operations.json", "sha256": self.write("operations.json", self.operations)}
        self.manifest["threat_register"] = {"file": "threats.json", "sha256": self.write("threats.json", self.threats)}
        for category in self.evals:
            category["receipt_sha256"] = hashlib.sha256((self.root / category["receipt_file"]).read_bytes()).hexdigest()
        self.manifest["decision_receipt"] = {"file": "decision.json", "sha256": self.write("decision.json", self.approval)}
        self.write("frontier.json", self.manifest)

    def result(self):
        self.sync()
        return review_frontier(self.manifest, self.root, as_of=AS_OF)

    def status(self):
        return self.result()["status"]

    def edit_eval(self, category, **changes):
        path = self.root / f"eval-{category}.json"
        document = json.loads(path.read_text())
        document.update(changes)
        if "decision" in changes:
            report_name = f"eval-report-{category}.json"
            report = json.loads((self.root / report_name).read_text())
            report["decision"] = changes["decision"]
            document["test_report"]["sha256"] = self.write(report_name, report)
        self.write(path.name, document)


class FrontierReviewTests(FrontierFixture):
    def test_valid_synthetic_bundle_is_only_review_ready(self):
        result = self.result()
        self.assertEqual(result["status"], "REVIEW_READY")
        self.assertEqual(len(result["controls"]), len(CONTROL_CATEGORIES))
        self.assertEqual(len(result["capabilities"]), len(RISK_CATEGORIES))
        self.assertIn("no authenticated execution", result["boundary"])

    def test_missing_required_capability_does_not_pass(self):
        self.evals.pop()
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_missing_threat_category_does_not_pass(self):
        self.threats["risks"].pop()
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_threat_register_without_stop_condition_does_not_pass(self):
        del self.threats["risks"][0]["stop_condition"]
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_threat_register_owner_cannot_review_own_work(self):
        self.threats["reviewer"] = self.threats["owner"]
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_duplicate_capability_does_not_pass(self):
        self.evals.append(copy.deepcopy(self.evals[0]))
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_unknown_capability_does_not_pass(self):
        self.evals[0]["category"] = "new_unreviewed_risk"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_absent_critical_control_does_not_pass(self):
        self.manifest["control_map"] = self.manifest["control_map"][:-1]
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_reused_control_cannot_cover_two_different_safeguards(self):
        self.manifest["control_map"][1]["control_id"] = "tool_authorisation"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_ai_self_report_is_not_independent_enforcement(self):
        self.manifest["control_map"][0]["enforcement_boundary"] = "model_self_report"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_interrupt_requires_infrastructure_not_supervised_host(self):
        for row in self.manifest["control_map"]:
            if row["category"] == "independent_interrupt":
                row["enforcement_boundary"] = "supervised_host"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_constant_allow_fails_negative_receipts(self):
        control = self.core["controls"][0]
        negative = control["execution_tests"][1]
        path = self.root / negative["receipt_file"]
        receipt = json.loads(path.read_text())
        receipt["decision"] = "ALLOW"
        negative["receipt_sha256"] = self.write(path.name, receipt)
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_malformed_core_action_cases_fail_without_crashing(self):
        self.core["controls"][0]["execution_tests"] = None
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_missing_operational_review_fails(self):
        self.operations["controls"].pop()
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_unhashable_operational_actor_fails_closed(self):
        self.operations["controls"][0]["executor"] = ["invalid-identity"]
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_simulation_only_does_not_pass(self):
        self.operations["controls"][0]["environment"] = "simulated"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_old_operational_evidence_cannot_authorise_new_revision(self):
        self.operations["controls"][0]["executed_at_utc"] = "2026-11-02T09:00:00Z"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_future_action_receipt_cannot_pass(self):
        case = self.core["controls"][0]["execution_tests"][0]
        receipt = json.loads((self.root / case["receipt_file"]).read_text())
        receipt["executed_at_utc"] = "2026-11-07T09:00:00Z"
        case["receipt_sha256"] = self.write(case["receipt_file"], receipt)
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_reused_evidence_from_other_model_is_rejected(self):
        self.edit_eval(RISK_CATEGORIES[0], model_revision="different-model")
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_adverse_capability_cannot_be_overridden_by_release(self):
        self.edit_eval("autonomous_replication", decision="BLOCKING")
        self.assertEqual(self.status(), "BLOCKING_FINDING")

    def test_inconclusive_capability_cannot_be_overridden(self):
        self.edit_eval("oversight_deception", decision="INCONCLUSIVE")
        self.assertEqual(self.status(), "BLOCKING_FINDING")

    def test_declared_pass_cannot_override_recorded_adverse_result(self):
        self.evals[0]["declared_decision"] = "CLEAR"
        self.edit_eval(RISK_CATEGORIES[0], decision="BLOCKING")
        self.assertEqual(self.status(), "BLOCKING_FINDING")

    def test_review_deadline_expired_fails(self):
        self.manifest["review_due_at_utc"] = "2026-11-06T11:59:00Z"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_material_model_change_invalidates_prior_evaluations(self):
        self.manifest["last_material_change_at_utc"] = "2026-11-05T11:00:00Z"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_approval_before_evaluations_is_invalid(self):
        self.approval["approved_at_utc"] = "2026-11-04T09:00:00Z"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_approval_by_evaluator_is_not_independent(self):
        self.approval["approver"] = "evaluator-A"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_unhashable_evaluator_identity_fails_closed(self):
        self.edit_eval(RISK_CATEGORIES[0], evaluator=["invalid-identity"])
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_shutdown_receipt_from_previous_revision_is_rejected(self):
        ctrl = self.core["controls"][3]
        case = ctrl["execution_tests"][0]
        receipt = json.loads((self.root / case["receipt_file"]).read_text())
        receipt["model_revision"] = "old-model"
        case["receipt_sha256"] = self.write(case["receipt_file"], receipt)
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_tampered_evaluation_digest_fails(self):
        self.evals[0]["receipt_sha256"] = "0" * 64
        # Do not call sync(), which computes the current digest for fixture convenience.
        result = review_frontier(self.manifest, self.root, as_of=AS_OF)
        self.assertEqual(result["status"], "EVIDENCE_INCOMPLETE")

    def test_evaluation_receipt_cannot_contradict_its_pinned_report(self):
        category = RISK_CATEGORIES[0]
        path = self.root / f"eval-{category}.json"
        receipt = json.loads(path.read_text())
        receipt["decision"] = "BLOCKING"
        self.write(path.name, receipt)
        result = self.result()
        self.assertEqual(result["status"], "BLOCKING_FINDING")
        self.assertTrue(any("corroborate" in issue for issue in result["capabilities"][0]["issues"]))

    def test_missing_evaluation_report_does_not_pass(self):
        category = RISK_CATEGORIES[0]
        path = self.root / f"eval-{category}.json"
        receipt = json.loads(path.read_text())
        receipt.pop("test_report")
        self.write(path.name, receipt)
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_human_hold_does_not_become_release_ready(self):
        self.approval["decision"] = "HOLD"
        self.assertEqual(self.status(), "RELEASE_HELD")

    def test_approver_must_not_be_technical_operator(self):
        self.approval["approver"] = "test-executor"
        self.assertEqual(self.status(), "EVIDENCE_INCOMPLETE")

    def test_cli_strict_exit_status(self):
        self.sync()
        command = [sys.executable, str(ROOT / "scripts/laif_frontier_assurance.py"),
                   str(self.root / "frontier.json"), "--as-of", "2026-11-06T12:00:00Z", "--require-review-ready"]
        allowed = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(json.loads(allowed.stdout)["status"], "REVIEW_READY")
        self.approval["decision"] = "HOLD"
        self.sync()
        refused = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(refused.returncode, 1, refused.stderr)


if __name__ == "__main__":
    unittest.main()
