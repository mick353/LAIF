#!/usr/bin/env python3
"""Optional, offline frontier/agentic AI evidence review; never a safety certificate.

This is a strict extension of LAIF's existing source, action-receipt and
operational-annex diagnostics. It checks supplied records, not running models.
It does not change LAIF-native certification, assessment scores or reports.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from laif_assurance import _nonblank, _utc, artifact, assess_assurance
from laif_evidence_checks import read_json_object


# Explicit versioned coverage requirements, not an assertion that these are
# all possible frontier hazards. Changes to these lists need reviewer approval.
RISK_CATEGORIES = (
    "cyber_misuse", "chemical_biological_misuse", "autonomous_replication",
    "oversight_deception", "model_exfiltration", "persuasion_at_scale",
)
CONTROL_CATEGORIES = (
    "tool_authorisation", "credential_isolation", "network_egress",
    "independent_interrupt", "oversight_integrity", "harmful_use_gating",
    "incident_response",
)


def _datetime(value: Any) -> datetime:
    if not _utc(value):
        raise ValueError("expected UTC ISO-8601 timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _json_artifact(root: Path, record: Any, *, prefix: str = "") -> dict:
    if not isinstance(record, dict):
        raise ValueError("missing evidence reference")
    raw = artifact(root, record.get(prefix + "file"), record.get(prefix + "sha256"))
    parsed = read_json_object(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("evidence JSON must be an object")
    return parsed


def _indexed(items: Any, key: str, label: str, problems: list[str]) -> dict:
    if not isinstance(items, list):
        problems.append(f"{label} must be a list")
        return {}
    indexed = {}
    for item in items:
        if not isinstance(item, dict) or not _nonblank(item.get(key)):
            problems.append(f"{label}: malformed entry")
            continue
        value = item[key]
        if value in indexed:
            problems.append(f"{label}: duplicate {value}")
        else:
            indexed[value] = item
    return indexed


def review_frontier(manifest: dict, root: Path, *, as_of: datetime) -> dict:
    """Return deterministic evidence-readiness diagnostics at an explicit instant.

    A REVIEW_READY result is only permission for a human to review records;
    this code never authorises a deployment or asserts an effective safeguard.
    """
    if not isinstance(manifest, dict) or manifest.get("schema") != "laif.frontier-assurance.v1":
        raise ValueError("expected laif.frontier-assurance.v1")
    if as_of.tzinfo is None or as_of.utcoffset().total_seconds() != 0:
        raise ValueError("as_of must be UTC")
    root = root.resolve()
    problems: list[str] = []
    identity = (manifest.get("deployment_id"), manifest.get("model_revision"))
    if not all(_nonblank(x) for x in identity):
        raise ValueError("deployment_id and model_revision are required")
    try:
        changed = _datetime(manifest.get("last_material_change_at_utc"))
        review_due = _datetime(manifest.get("review_due_at_utc"))
        if changed > as_of:
            problems.append("material change is later than review instant")
        if review_due <= as_of:
            problems.append("review deadline elapsed: new assessment required")
        if review_due <= changed:
            problems.append("review deadline is not after material change")
    except ValueError as exc:
        problems.append(f"lifecycle timestamps: {exc}")
        changed = as_of

    # The existing assurance engine remains authoritative for documentary
    # scope, positive/negative action receipts and operational review records.
    core, operations, core_rows, core_controls, operational_controls = None, None, {}, {}, {}
    latest_control_evidence = changed
    operating_actors = set()
    try:
        core = _json_artifact(root, manifest.get("core_manifest"))
        operations = _json_artifact(root, manifest.get("operational_annex"))
        if core.get("deployment_id") != identity[0] or core.get("model_revision") != identity[1]:
            problems.append("core evidence is not bound to this deployment and model revision")
        core_result = assess_assurance(core, root, strict_scope=True, strict_actions=True, annex=operations)
        core_rows = {x["id"]: x for x in core_result["controls"]}
        core_controls = {x["id"]: x for x in core["controls"]}
        operational_controls = _indexed(operations.get("controls"), "control_id", "operational records", problems)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        problems.append(f"core assurance: {exc}")

    mappings = _indexed(manifest.get("control_map"), "category", "control mapping", problems)
    unknown = set(mappings) - set(CONTROL_CATEGORIES)
    if unknown:
        problems.append("unknown control categories: " + ", ".join(sorted(unknown)))
    seen_ids = set()
    control_results = []
    for category in CONTROL_CATEGORIES:
        entry = mappings.get(category)
        issues = []
        if entry is None:
            issues.append("required category missing")
        else:
            cid = entry.get("control_id")
            if not _nonblank(cid) or cid in seen_ids:
                issues.append("control ID missing or reused across different safeguards")
            else:
                seen_ids.add(cid)
                if entry.get("enforcement_boundary") not in ("infrastructure", "supervised_host"):
                    issues.append("model-level assurances alone cannot enforce a boundary")
                if category == "independent_interrupt" and entry.get("enforcement_boundary") != "infrastructure":
                    issues.append("interruption must be independently enforced by infrastructure")
                row = core_rows.get(cid)
                if not row or row.get("status") != "REVIEW_READY" or row.get("operational_annex", {}).get("status") != "REVIEW_RECORDED":
                    issues.append("strict LAIF assurance and independent operational review not ready")
                op = operational_controls.get(cid)
                if not op or op.get("deployment_id") != identity[0] or op.get("model_revision") != identity[1]:
                    issues.append("operational review is not bound to the model revision")
                elif op.get("environment") not in ("staging", "production"):
                    issues.append("simulation-only operational record")
                if op:
                    if _nonblank(op.get("executor")):
                        operating_actors.add(op["executor"])
                    else:
                        issues.append("operational executor identity is missing or invalid")
                    try:
                        observed = _datetime(op.get("executed_at_utc"))
                        reviewed = _datetime(op.get("reviewed_at_utc"))
                        if not (changed <= observed < reviewed <= as_of):
                            issues.append("operational evidence stale, future-dated or not reviewed")
                        latest_control_evidence = max(latest_control_evidence, reviewed)
                    except ValueError as exc:
                        issues.append(f"operational evidence time invalid: {exc}")
                if cid in core_controls:
                    action_cases = core_controls[cid].get("execution_tests")
                    if not isinstance(action_cases, list):
                        issues.append("action receipt list missing or malformed")
                        action_cases = []
                    for case in action_cases:
                        try:
                            receipt = _json_artifact(root, case, prefix="receipt_")
                            if receipt.get("deployment_id") != identity[0] or receipt.get("model_revision") != identity[1]:
                                issues.append("action receipt not bound to deployment and revision")
                            observed = _datetime(receipt.get("executed_at_utc"))
                            if not (changed <= observed <= as_of):
                                issues.append("action receipt stale or future-dated")
                            latest_control_evidence = max(latest_control_evidence, observed)
                        except (ValueError, AttributeError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
                            issues.append(f"action receipt invalid: {exc}")
        control_results.append({"category": category, "status": "REVIEW_READY" if not issues else "EVIDENCE_GAP", "issues": issues})

    register_reviewed = changed
    try:
        register = _json_artifact(root, manifest.get("threat_register"))
        if register.get("deployment_id") != identity[0] or register.get("model_revision") != identity[1]:
            problems.append("threat register not bound to model revision and deployment")
        if (not _nonblank(register.get("owner")) or not _nonblank(register.get("reviewer"))
                or register.get("owner") == register.get("reviewer")):
            problems.append("threat assessment lacks distinct responsible owner and reviewer")
        register_reviewed = _datetime(register.get("reviewed_at_utc"))
        if not (changed <= register_reviewed <= as_of):
            problems.append("threat assessment stale or future-dated")
        risks = _indexed(register.get("risks"), "category", "threat register risks", problems)
        if set(risks) != set(RISK_CATEGORIES):
            problems.append("threat register must explicitly address every required risk category")
        for category, risk in risks.items():
            if not all(_nonblank(risk.get(field)) for field in
                       ("protected_interest", "failure_pathway", "control_owner", "trigger", "stop_condition", "test_method")):
                problems.append(f"{category}: threat lacks interest, failure pathway, owner, trigger, stop condition or method")
    except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        problems.append(f"threat register invalid: {exc}")

    evaluations = _indexed(manifest.get("capability_evaluations"), "category", "capability evaluations", problems)
    unknown = set(evaluations) - set(RISK_CATEGORIES)
    if unknown:
        problems.append("unknown capability categories: " + ", ".join(sorted(unknown)))
    evaluation_results = []
    blocking = False
    evaluator_names = set()
    latest_evaluation = changed
    for category in RISK_CATEGORIES:
        entry = evaluations.get(category)
        issues = []
        recorded = "MISSING"
        if entry is None:
            issues.append("required capability evaluation missing")
        else:
            try:
                receipt = _json_artifact(root, entry, prefix="receipt_")
                if receipt.get("category") != category or receipt.get("model_revision") != identity[1] or receipt.get("deployment_id") != identity[0]:
                    issues.append("evaluation identity does not match model and deployment")
                if not all(_nonblank(receipt.get(x)) for x in ("run_id", "method_id", "toolchain_version", "evaluator", "reviewer")):
                    issues.append("evaluation lacks run, method, toolchain or responsible actors")
                if receipt.get("evaluator") == receipt.get("reviewer"):
                    issues.append("independent reviewer must differ from evaluator")
                elif _nonblank(receipt.get("evaluator")):
                    evaluator_names.add(receipt["evaluator"])
                if receipt.get("environment") not in {"staging", "production"}:
                    issues.append("evaluation is simulation-only or environment unspecified")
                executed = _datetime(receipt.get("executed_at_utc"))
                reviewed = _datetime(receipt.get("reviewed_at_utc"))
                if not (register_reviewed <= executed < reviewed <= as_of):
                    issues.append("evaluation stale, future-dated or not reviewed after execution")
                latest_evaluation = max(latest_evaluation, reviewed)
                recorded = receipt.get("decision")
                if recorded not in {"CLEAR", "BLOCKING", "INCONCLUSIVE"}:
                    issues.append("evaluation receipt has no valid observed decision")
                if recorded in {"BLOCKING", "INCONCLUSIVE"}:
                    blocking = True
                if not isinstance(receipt.get("test_report"), dict):
                    issues.append("evaluation lacks a pinned result report")
                else:
                    report = _json_artifact(root, receipt["test_report"])
                    bound_fields = ("deployment_id", "model_revision", "category", "run_id",
                                    "method_id", "toolchain_version", "executed_at_utc", "decision")
                    if any(report.get(field) != receipt.get(field) for field in bound_fields):
                        issues.append("test report does not corroborate receipt decision, method, time and identity")
                    observations = report.get("observations")
                    if (not isinstance(observations, list) or not observations
                            or any(not _nonblank(value) for value in observations)
                            or not _nonblank(report.get("coverage_limitations"))):
                        issues.append("test report lacks recorded observations or coverage limitations")
            except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
                issues.append(f"evaluation evidence invalid: {exc}")
        evaluation_results.append({"category": category, "recorded_decision": recorded,
                                   "status": "REVIEW_READY" if not issues and recorded == "CLEAR" else "REVIEW_REQUIRED",
                                   "issues": issues})

    approval_status = "MISSING"
    try:
        approval = _json_artifact(root, manifest.get("decision_receipt"))
        approval_status = approval.get("decision", "MISSING")
        if approval.get("model_revision") != identity[1] or approval.get("deployment_id") != identity[0]:
            problems.append("decision identity does not match model and deployment")
        if approval_status not in {"RELEASE", "CONDITIONAL", "HOLD"}:
            problems.append("decision must be RELEASE, CONDITIONAL or HOLD")
        if not _nonblank(approval.get("approver")) or approval.get("approver") in evaluator_names | operating_actors:
            problems.append("decision approver missing or same as an evaluator or operator")
        decided = _datetime(approval.get("approved_at_utc"))
        if not (max(latest_evaluation, latest_control_evidence) < decided <= as_of):
            problems.append("decision must follow all capability and control evidence and precede review instant")
    except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        problems.append(f"decision receipt invalid: {exc}")

    complete = (not problems and all(x["status"] == "REVIEW_READY" for x in control_results)
                and all(x["status"] == "REVIEW_READY" for x in evaluation_results))
    if blocking:
        status = "BLOCKING_FINDING"
    elif not complete:
        status = "EVIDENCE_INCOMPLETE"
    elif approval_status != "RELEASE":
        status = "RELEASE_HELD"
    else:
        status = "REVIEW_READY"
    return {"schema": "laif.frontier-review.v1", "deployment_id": identity[0], "model_revision": identity[1],
            "as_of_utc": as_of.isoformat().replace("+00:00", "Z"), "status": status,
            "decision_recorded": approval_status, "issues": problems,
            "controls": control_results, "capabilities": evaluation_results,
            "boundary": "Hash-pinned, self-supplied records only; no authenticated execution, live monitoring, model evaluation, safety certification, legal approval or permission to deploy."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--as-of", help="UTC ISO-8601 review instant; defaults to current UTC")
    parser.add_argument("--require-review-ready", action="store_true", help="nonzero exit unless records are ready for human review")
    args = parser.parse_args()
    try:
        manifest = read_json_object(args.manifest.read_text(encoding="utf-8"))
        instant = _datetime(args.as_of) if args.as_of else datetime.now(timezone.utc)
        result = review_frontier(manifest, args.manifest.parent, as_of=instant)
    except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, sort_keys=True, indent=2))
    return int(bool(args.require_review_ready and result["status"] != "REVIEW_READY"))


if __name__ == "__main__":
    raise SystemExit(main())
