#!/usr/bin/env python3
"""Optional LAIF assurance diagnostics: source scope, execution receipts, operational review.

No changes to LAIF scoring or LAIF-native certification. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from laif_evidence_checks import check_manifest

_HEX = re.compile(r"[0-9a-f]{64}\Z")
_DECISIONS = {"ALLOW", "BLOCK"}
_KIND_EXPECTED = {"positive": "ALLOW", "negative": "BLOCK"}


def digest_json(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _utc(value: Any) -> bool:
    if not _nonblank(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0


def artifact(root: Path, file: Any, sha256: Any, quote: Any = None) -> bytes:
    if not _nonblank(file) or Path(file).is_absolute() or not isinstance(sha256, str) or not _HEX.fullmatch(sha256):
        raise ValueError("invalid relative file path or SHA-256")
    root = root.resolve()
    resolved = (root / file).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("evidence file missing or outside evidence root")
    content = resolved.read_bytes()
    if hashlib.sha256(content).hexdigest() != sha256:
        raise ValueError("SHA-256 mismatch")
    if quote is not None:
        if not _nonblank(quote) or quote not in content.decode("utf-8"):
            raise ValueError("exact source quotation not present")
    return content


def _source_inventory(manifest: dict, root: Path) -> tuple[dict, list[str]]:
    inventory = manifest.get("source_inventory")
    if inventory is None:
        return {}, ["no source inventory declared"]
    if not isinstance(inventory, list):
        raise ValueError("source_inventory must be a list")
    problems = []
    items = {}
    for item in inventory:
        if not isinstance(item, dict) or not _nonblank(item.get("id")):
            raise ValueError("source inventory item requires an id")
        sid = item["id"]
        if sid in items:
            raise ValueError("duplicate inventory source id")
        items[sid] = item
        if type(item.get("required")) is not bool or not isinstance(item.get("disposition"), str) or item["disposition"] not in {"inspected", "excluded", "unreadable"}:
            problems.append(f"{sid}: invalid source classification")
            continue
        if item["disposition"] == "inspected":
            try:
                artifact(root, item.get("file"), item.get("sha256"), item.get("quote"))
            except (ValueError, OSError, UnicodeError) as exc:
                problems.append(f"{sid}: {exc}")
        else:
            if not _nonblank(item.get("reason")):
                problems.append(f"{sid}: excluded/unreadable source requires a reason")
            if item["required"]:
                problems.append(f"{sid}: required source is {item['disposition']}")
    return items, problems


def _scope_problems(manifest: dict, root: Path, inventory: dict, inventory_problems: list[str], control: dict, strict: bool) -> tuple[str | None, list[str]]:
    # Optional mode must preserve the previous source-only diagnostic on old manifests.
    if manifest.get("source_inventory") is None and not strict:
        return None, []
    issues = list(inventory_problems)
    required = control.get("required_source_ids")
    if strict and manifest.get("source_inventory") is None:
        return "SCOPE_UNDECLARED", ["strict scope requires a source inventory"]
    if required is not None and (not isinstance(required, list) or any(not _nonblank(x) for x in required) or len(set(required)) != len(required)):
        issues.append("required_source_ids must be a unique string list")
    elif isinstance(required, list):
        for rid in required:
            if rid not in inventory:
                issues.append(f"undeclared required source: {rid}")
            elif inventory[rid].get("disposition") != "inspected":
                issues.append(f"required source not inspected: {rid}")
    if any("SHA-256 mismatch" in x or "evidence file missing" in x or "source quotation" in x for x in issues):
        return "SOURCE_INVALID", issues
    if issues and any("required" in x or "source classification" in x or "source requires" in x for x in issues):
        return "SOURCE_INCOMPLETE", issues
    attestation = manifest.get("scope_attestation")
    if strict:
        if not inventory or required is None or not isinstance(attestation, dict):
            issues.append("strict scope requires a nonempty inventory, declared required sources and an attestation")
        elif not (_nonblank(attestation.get("reviewer")) and _utc(attestation.get("recorded_at_utc"))
                  and attestation.get("complete") is True and attestation.get("inventory_sha256") == digest_json(manifest["source_inventory"])):
            issues.append("scope attestation incomplete or does not bind source inventory")
        if issues:
            return "SCOPE_UNDECLARED", issues
    elif issues:
        return "SOURCE_INCOMPLETE", issues
    return None, []


def _execution_tests(control: dict, root: Path) -> dict:
    records = control.get("execution_tests")
    if records is None:
        return {"status": "EXECUTION_UNTESTED", "counts": {"positive": 0, "negative": 0}, "issues": [], "cases": []}
    if not isinstance(records, list):
        return {"status": "EVIDENCE_INVALID", "counts": {}, "issues": ["execution_tests must be a list"], "cases": []}
    issues, cases, seen = [], [], set()
    counts = {"positive": 0, "negative": 0}
    mismatch = False
    for idx, entry in enumerate(records):
        if not isinstance(entry, dict):
            issues.append(f"execution test {idx}: not an object")
            continue
        kind, tid = entry.get("kind"), entry.get("test_id")
        if kind not in _KIND_EXPECTED or not _nonblank(tid) or tid in seen:
            issues.append(f"execution test {idx}: invalid or duplicate test identity")
            continue
        seen.add(tid)
        if entry.get("expected_action") != _KIND_EXPECTED[kind]:
            issues.append(f"execution test {tid}: kind and expected action conflict")
            continue
        try:
            raw = artifact(root, entry.get("receipt_file"), entry.get("receipt_sha256"))
            receipt = json.loads(raw.decode("utf-8"))
            if not isinstance(receipt, dict) or receipt.get("control_id") != control.get("id") or receipt.get("test_id") != tid:
                raise ValueError("receipt identity does not match control/test")
            if (not isinstance(receipt.get("decision"), str) or receipt["decision"] not in _DECISIONS or not _nonblank(receipt.get("run_id"))
                    or not _utc(receipt.get("executed_at_utc")) or not _nonblank(receipt.get("toolchain_version"))
                    or not isinstance(receipt.get("environment"), str) or receipt["environment"] not in {"simulated", "staging", "production"}):
                raise ValueError("receipt missing valid decision, run, environment, time or version")
        except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
            issues.append(f"execution test {tid}: {exc}")
            continue
        counts[kind] += 1
        decision = receipt["decision"]
        mismatch |= decision != entry["expected_action"]
        cases.append({"test_id": tid, "kind": kind, "expected": entry["expected_action"], "observed": decision,
                      "receipt_sha256": entry["receipt_sha256"], "run_id": receipt["run_id"]})
    if issues:
        status = "EVIDENCE_INVALID"
    elif mismatch:
        status = "OBSERVED_FAILURE"
    elif not all(counts.values()):
        status = "INCOMPLETE_CONTROLS"
    else:
        status = "REVIEW_READY"
    return {"status": status, "counts": counts, "issues": issues, "cases": cases}


def mutation_probes(execution: dict) -> list[dict]:
    """Hypothetical interventions on recorded decisions; never executes target systems."""
    cases = execution["cases"]
    if execution["status"] != "REVIEW_READY":
        return [{"intervention": "baseline", "caught": None, "note": "baseline not review-ready"}]
    transforms = {
        "remove_all_checks": [],
        "remove_negative_checks": [x for x in cases if x["kind"] != "negative"],
        "force_allow": [{**x, "observed": "ALLOW"} for x in cases],
        "force_block": [{**x, "observed": "BLOCK"} for x in cases],
    }
    result = []
    for op, mutated in transforms.items():
        if not mutated or not {"positive", "negative"}.issubset({c["kind"] for c in mutated}):
            verdict = "INCOMPLETE_CONTROLS"
        elif any(c["expected"] != c["observed"] for c in mutated):
            verdict = "OBSERVED_FAILURE"
        else:
            verdict = "REVIEW_READY"
        result.append({"intervention": op, "hypothetical_status": verdict, "caught": verdict != "REVIEW_READY"})
    return result


def _operational_annex(annex: dict | None, control: dict, root: Path) -> dict:
    if annex is None:
        return {"status": "NOT_SUPPLIED", "issues": []}
    if not isinstance(annex, dict) or annex.get("schema") != "laif.operational-annex.v1":
        raise ValueError("unsupported operational annex schema")
    records = annex.get("controls", [])
    if not isinstance(records, list):
        raise ValueError("annex controls must be a list")
    matches = [x for x in records if isinstance(x, dict) and x.get("control_id") == control.get("id")]
    if not matches:
        return {"status": "NOT_SUPPLIED", "issues": []}
    if len(matches) != 1:
        return {"status": "ANNEX_INVALID", "issues": ["duplicate operational control id"]}
    rec = matches[0]
    problems = []
    if not all(_nonblank(rec.get(key)) for key in ("deployment_id", "executor", "run_id", "toolchain_version")):
        problems.append("missing deployment, executor, run, or toolchain identity")
    if not isinstance(rec.get("environment"), str) or rec["environment"] not in {"staging", "production", "simulated"} or not _utc(rec.get("executed_at_utc")):
        problems.append("environment or execution date invalid")
    for prefix, identity in (("authorisation", "deployment_id"), ("execution_log", "run_id")):
        try:
            text = artifact(root, rec.get(prefix + "_file"), rec.get(prefix + "_sha256"), rec.get(prefix + "_quote")).decode("utf-8")
            if _nonblank(rec.get(identity)) and rec[identity] not in text:
                problems.append(f"{prefix}: record does not identify {identity}")
        except (ValueError, OSError, UnicodeError) as exc:
            problems.append(f"{prefix}: {exc}")
    if not _utc(rec.get("authorisation_issued_at_utc")) or not _utc(rec.get("reviewed_at_utc")):
        problems.append("authorisation/review timestamps must be UTC")
    elif _utc(rec.get("executed_at_utc")):
        auth = datetime.fromisoformat(rec["authorisation_issued_at_utc"].replace("Z", "+00:00"))
        executed = datetime.fromisoformat(rec["executed_at_utc"].replace("Z", "+00:00"))
        reviewed = datetime.fromisoformat(rec["reviewed_at_utc"].replace("Z", "+00:00"))
        if not (auth < executed < reviewed):
            problems.append("authorisation must predate execution and review must follow it")
    reviewer = rec.get("reviewer")
    if not _nonblank(reviewer) or reviewer == rec.get("executor"):
        problems.append("reviewer must be named and different from executor")
    try:
        text = artifact(root, rec.get("review_file"), rec.get("review_sha256"), rec.get("review_quote")).decode("utf-8")
        if _nonblank(rec.get("run_id")) and rec["run_id"] not in text:
            problems.append("review record: does not identify run_id")
    except (ValueError, OSError, UnicodeError) as exc:
        problems.append(f"review record: {exc}")
    if not isinstance(rec.get("outcome"), str) or rec["outcome"] not in {"PASS", "FAIL"}:
        problems.append("outcome must be PASS or FAIL")
    remediation = rec.get("remediation")
    if remediation is not None:
        if not isinstance(remediation, dict) or not _nonblank(remediation.get("change_ref")):
            problems.append("invalid remediation record")
        else:
            try:
                artifact(root, remediation.get("file"), remediation.get("sha256"), remediation.get("quote"))
            except (ValueError, OSError, UnicodeError) as exc:
                problems.append(f"remediation: {exc}")
    retest = rec.get("retest")
    if retest is not None:
        if not isinstance(retest, dict) or not isinstance(retest.get("outcome"), str) or retest["outcome"] not in {"PASS", "FAIL"} or not _utc(retest.get("executed_at_utc")):
            problems.append("invalid retest metadata")
        else:
            try:
                artifact(root, retest.get("file"), retest.get("sha256"), retest.get("quote"))
            except (ValueError, OSError, UnicodeError) as exc:
                problems.append(f"retest: {exc}")
            if _utc(rec.get("executed_at_utc")) and datetime.fromisoformat(retest["executed_at_utc"].replace("Z", "+00:00")) <= datetime.fromisoformat(rec["executed_at_utc"].replace("Z", "+00:00")):
                problems.append("retest must follow original execution")
    if problems:
        status = "ANNEX_INVALID"
    elif rec.get("outcome") == "FAIL" and (not remediation or not retest or retest["outcome"] != "PASS"):
        status = "RETEST_REQUIRED"
    elif remediation and not retest:
        status = "RETEST_REQUIRED"
    elif retest and retest["outcome"] == "FAIL":
        status = "RETEST_REQUIRED"
    else:
        status = "REVIEW_RECORDED"
    return {"status": status, "issues": problems, "environment": rec.get("environment"),
            "deployment_id": rec.get("deployment_id"),
            "boundary": "Pinned records and different recorded reviewers, not authenticated independent operational verification."}


def assess_assurance(manifest: dict, root: Path, *, strict_scope: bool = False,
                     strict_actions: bool = False, annex: dict | None = None,
                     with_mutations: bool = False) -> dict:
    """Evidence extension; never overrides core LAIF scores or reports."""
    base = check_manifest(manifest, root)
    if annex is not None:
        if not isinstance(annex, dict) or annex.get("schema") != "laif.operational-annex.v1" or not isinstance(annex.get("controls"), list):
            raise ValueError("invalid operational annex")
        ids = {x["id"] for x in manifest["controls"]}
        for item in annex["controls"]:
            if not isinstance(item, dict) or not _nonblank(item.get("control_id")) or item["control_id"] not in ids:
                raise ValueError("annex references unknown or malformed control")
    inventory, source_issues = _source_inventory(manifest, root)
    results = []
    for control, base_row in zip(manifest["controls"], base["controls"]):
        scope_status, issues = _scope_problems(manifest, root, inventory, source_issues, control, strict_scope)
        execution = _execution_tests(control, root)
        original = base_row["status"]
        status = original
        # An original adverse, contradicted, unsupported or invalid finding cannot be erased.
        if original in {"UNSUPPORTED_CLAIM", "EVIDENCE_INVALID", "CONTRADICTORY_RECORDS", "OBSERVED_FAILURE"}:
            pass
        elif scope_status is not None:
            status = scope_status
        elif execution["status"] == "EVIDENCE_INVALID":
            status = "EVIDENCE_INVALID"
        elif execution["status"] == "OBSERVED_FAILURE":
            status = "OBSERVED_FAILURE"
        elif execution["status"] == "INCOMPLETE_CONTROLS":
            status = "INCOMPLETE_CONTROLS"
        elif strict_actions and execution["status"] == "EXECUTION_UNTESTED":
            status = "EXECUTION_UNTESTED"
        elif execution["status"] == "REVIEW_READY":
            status = "REVIEW_READY"
        # Legacy source-only evidence never becomes operational evidence automatically.
        grade = ("EXECUTION_RECEIPT_CHECKED" if execution["status"] == "REVIEW_READY"
                 else "DECLARED_TEST_RECORDS" if base_row["positive_tests"] + base_row["negative_tests"] else "POLICY_CLAIM_ONLY")
        op = _operational_annex(annex, control, root)
        row = {"id": control["id"], "status": status, "original_status": original,
               "scope_status": (scope_status or ("NOT_CHECKED" if manifest.get("source_inventory") is None else "SOURCE_CHECKED")),
               "execution_status": execution["status"], "evidence_grade": grade,
               "execution_counts": execution["counts"], "issues": issues + execution["issues"],
               "operational_annex": op}
        if with_mutations:
            row["mutation_probes"] = mutation_probes(execution)
        results.append(row)
    return {"schema": "laif.assurance.v1", "policy_sha256": base["policy_sha256"],
            "strict_scope": strict_scope, "strict_actions": strict_actions,
            "controls": results, "review_ready_count": sum(r["status"] == "REVIEW_READY" for r in results),
            "boundary": "Source completeness is attested, not proven exhaustive. Receipts and reviewer identity are not authenticated. No LAIF certification or operational validation."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--strict-scope", action="store_true")
    parser.add_argument("--strict-actions", action="store_true")
    parser.add_argument("--operational-annex", type=Path)
    parser.add_argument("--mutation-probes", action="store_true", help="simulate disabling controls against recorded decisions")
    parser.add_argument("--require-review-ready", action="store_true")
    parser.add_argument("--require-operational-review", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        annex = json.loads(args.operational_annex.read_text(encoding="utf-8")) if args.operational_annex else None
        # A requested pass gate always applies the strict scope and execution controls.
        enforced = args.require_review_ready or args.require_operational_review
        outcome = assess_assurance(manifest, args.manifest.parent, strict_scope=args.strict_scope or enforced,
                                    strict_actions=args.strict_actions or enforced, annex=annex, with_mutations=args.mutation_probes)
    except (ValueError, OSError, UnicodeError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(outcome, indent=2, sort_keys=True))
    fail = ((args.require_review_ready and (not outcome["controls"] or any(x["status"] != "REVIEW_READY" for x in outcome["controls"])))
            or (args.require_operational_review and (not outcome["controls"] or any(x["status"] != "REVIEW_READY" or x["operational_annex"]["status"] != "REVIEW_RECORDED" for x in outcome["controls"]))))
    return int(bool(fail))


if __name__ == "__main__":
    raise SystemExit(main())
