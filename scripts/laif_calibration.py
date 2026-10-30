#!/usr/bin/env python3
"""Frozen, leakage-checked LAIF evidence diagnostic calibration (not certification)."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from laif_assurance import artifact, assess_assurance, digest_json

LABELS = {"READY", "NOT_READY"}
SPLITS = {"development", "holdout"}


def holdout_seal(cases: list[dict]) -> str:
    """Bind holdout identities, expected labels and pinned source bytes."""
    return digest_json([{k: c[k] for k in ("id", "family", "gold_label", "manifest_sha256")}
                        for c in sorted(cases, key=lambda x: x["id"]) if c["split"] == "holdout"])


def wilson(successes: int, total: int) -> list[float] | None:
    if not total:
        return None
    z = 1.959963984540054
    p = successes / total
    z2 = z*z
    centre = (p + z2/(2*total)) / (1 + z2/total)
    margin = z * math.sqrt(p*(1-p)/total + z2/(4*total*total)) / (1 + z2/total)
    return [round(max(0, centre-margin), 5), round(min(1, centre+margin), 5)]


def score(rows: list[dict]) -> dict:
    tp = sum(x["gold"] == "READY" and x["predicted"] == "READY" for x in rows)
    tn = sum(x["gold"] == "NOT_READY" and x["predicted"] == "NOT_READY" for x in rows)
    fp = sum(x["gold"] == "NOT_READY" and x["predicted"] == "READY" for x in rows)
    fn = sum(x["gold"] == "READY" and x["predicted"] == "NOT_READY" for x in rows)
    n = tp + tn + fp + fn
    return {"n": n, "TP": tp, "TN": tn, "FP": fp, "FN": fn,
            "false_positive_rate": round(fp/(fp+tn), 5) if fp+tn else None,
            "false_positive_wilson95": wilson(fp, fp+tn),
            "false_negative_rate": round(fn/(fn+tp), 5) if fn+tp else None,
            "false_negative_wilson95": wilson(fn, fn+tp),
            "accuracy": round((tp+tn)/n, 5) if n else None,
            "accuracy_wilson95": wilson(tp+tn, n)}


def calibrate(dataset: dict, root: Path, *, require_adjudicated: bool = False) -> dict:
    if not isinstance(dataset, dict) or dataset.get("schema") != "laif.calibration.v1":
        raise ValueError("unsupported calibration dataset schema")
    if not isinstance(dataset.get("dataset_version"), str) or not dataset["dataset_version"].strip():
        raise ValueError("dataset_version required")
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases or len({x.get("id") for x in cases if isinstance(x, dict)}) != len(cases):
        raise ValueError("nonempty cases and unique case IDs required")
    if not any(isinstance(x, dict) and x.get("split") == "holdout" for x in cases):
        raise ValueError("a frozen holdout split is required")
    if dataset.get("holdout_seal") != holdout_seal(cases):
        raise ValueError("holdout seal mismatch")
    seen_families, seen_manifests, seen_policies = {}, {}, {}
    rows = []
    for entry in cases:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry[k].strip() for k in
                                                  ("id", "family", "gold_label", "split", "manifest_file", "manifest_sha256", "label_provenance")):
            raise ValueError("case missing required metadata")
        if entry["split"] not in SPLITS or entry["gold_label"] not in LABELS:
            raise ValueError("invalid split or label")
        family = entry["family"]
        if family in seen_families and seen_families[family] != entry["split"]:
            raise ValueError("family leakage across development and holdout")
        seen_families[family] = entry["split"]
        if entry["manifest_sha256"] in seen_manifests and seen_manifests[entry["manifest_sha256"]] != entry["split"]:
            raise ValueError("identical evidence manifests leaked across splits")
        seen_manifests[entry["manifest_sha256"]] = entry["split"]
        if entry["label_provenance"] not in {"SYNTHETIC", "HUMAN_ADJUDICATED"}:
            raise ValueError("unknown label provenance")
        if require_adjudicated and entry["label_provenance"] != "HUMAN_ADJUDICATED":
            raise ValueError("human-adjudicated labels required for this run")
        votes = entry.get("reviewer_votes", [])
        if not isinstance(votes, list):
            raise ValueError("reviewer_votes must be a list")
        if entry["label_provenance"] == "HUMAN_ADJUDICATED":
            if (len(votes) < 2 or any(not isinstance(v, dict) or not isinstance(v.get("reviewer"), str)
                 or v.get("label") not in LABELS for v in votes) or len({v["reviewer"] for v in votes}) != len(votes)):
                raise ValueError("adjudicated case requires at least two distinct recorded reviewer votes")
            artifact(root, entry.get("adjudication_file"), entry.get("adjudication_sha256"), entry.get("adjudication_quote"))
        raw = artifact(root, entry["manifest_file"], entry["manifest_sha256"])
        case_manifest = json.loads(raw.decode("utf-8"))
        policy_hash = case_manifest.get("policy_sha256")
        if policy_hash in seen_policies and seen_policies[policy_hash] != entry["split"]:
            raise ValueError("policy content leakage across development and holdout")
        seen_policies[policy_hash] = entry["split"]
        result = assess_assurance(case_manifest, (root / entry["manifest_file"]).resolve().parent,
                                  strict_scope=True, strict_actions=True)
        # A case tests one control; don't conceal ambiguous multi-control decisions.
        if len(result["controls"]) != 1:
            raise ValueError("each calibration case requires exactly one control")
        actual = result["controls"][0]["status"]
        rows.append({"id": entry["id"], "family": family, "split": entry["split"],
                     "gold": entry["gold_label"], "predicted": "READY" if actual == "REVIEW_READY" else "NOT_READY",
                     "diagnostic_status": actual, "label_provenance": entry["label_provenance"],
                     "reviewer_disagreement": len({v["label"] for v in votes}) > 1})
    by_split = {split: score([x for x in rows if x["split"] == split]) for split in ("development", "holdout")}
    adjudicated = sum(x["label_provenance"] == "HUMAN_ADJUDICATED" for x in rows)
    code_files = ("laif_evidence_checks.py", "laif_assurance.py", "laif_calibration.py")
    code_versions = {name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                     for name in code_files}
    return {"schema": "laif.calibration-report.v1", "dataset_version": dataset["dataset_version"],
            "evaluator_sources_sha256": code_versions,
            "dataset_seal": digest_json(dataset), "holdout_seal": dataset["holdout_seal"],
            "evaluation_policy": "strict_scope=True;strict_actions=True;READY iff REVIEW_READY",
            "n_cases": len(rows), "human_adjudicated_cases": adjudicated,
            "reviewer_disagreement_cases": sum(x["reviewer_disagreement"] for x in rows),
            "metrics": by_split, "cases": rows,
            "boundary": "Synthetic cases measure software invariants, not field accuracy; Wilson intervals assume independent labelled cases and do not correct selection bias or clustered data. Pin dataset and code revisions externally."}


def _write(path: Path, contents: str | dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(contents, indent=2, sort_keys=True) + "\n") if isinstance(contents, dict) else contents
    path.write_text(data, encoding="utf-8")
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def make_synthetic_corpus(root: Path) -> Path:
    """Deterministically generate paired cases; illustrative synthetic data only."""
    if root.exists() and any(root.iterdir()):
        raise ValueError("synthetic corpus destination must be empty")
    root.mkdir(parents=True, exist_ok=True)
    cases = []
    scenarios = ("complete", "claim_only", "missing_negative", "tampered", "complete", "scope_missing", "always_allow", "complete")
    for i, scenario in enumerate(scenarios, start=1):
        folder = root / f"case-{i:02d}"
        policy = f"Case {i}: Operators shall allow authorised requests and block unauthorised actions.\n"
        policy_hash = _write(folder / "policy.txt", policy)
        appendix = f"Case {i} appendix: tool authorisation coverage and monitored actions.\n"
        appendix_sha = _write(folder / "appendix.txt", appendix)
        inventory = [{"id": "appendix", "required": True, "disposition": "inspected",
                      "file": "appendix.txt", "sha256": appendix_sha, "quote": appendix.strip()}]
        if scenario == "scope_missing":
            inventory = [{"id": "appendix", "required": True, "disposition": "unreadable", "reason": "simulated missing attachment"}]
        tests = []
        if scenario not in ("claim_only",):
            for kind, expected in (("positive", "ALLOW"), ("negative", "BLOCK")):
                if scenario == "missing_negative" and kind == "negative":
                    continue
                observed = "ALLOW" if scenario == "always_allow" else expected
                tid = f"case-{i}-{kind}"
                receipt = {"control_id": "authorization", "test_id": tid, "decision": observed,
                           "run_id": f"run-{i}-{kind}", "executed_at_utc": "2026-10-30T00:00:00Z",
                           "toolchain_version": "synthetic-fixture-1", "environment": "simulated"}
                path = f"{kind}.json"
                receipt_sha = _write(folder / path, receipt)
                if scenario == "tampered" and kind == "positive":
                    receipt_sha = "0" * 64
                tests.append({"test_id": tid, "kind": kind, "expected_action": expected,
                              "receipt_file": path, "receipt_sha256": receipt_sha})
        manifest = {"policy_file": "policy.txt", "policy_sha256": policy_hash, "source_inventory": inventory,
                    "scope_attestation": {"reviewer": "synthetic-fixture-generator", "recorded_at_utc": "2026-10-30T00:00:00Z",
                                          "complete": True, "inventory_sha256": digest_json(inventory)},
                    "controls": [{"id": "authorization", "claim_quote": policy.strip(), "required_source_ids": ["appendix"],
                                  "execution_tests": tests}]}
        sha = _write(folder / "manifest.json", manifest)
        cases.append({"id": f"case-{i:02d}", "family": f"synthetic-family-{i:02d}",
                      "split": "development" if i <= 4 else "holdout",
                      "gold_label": "READY" if scenario == "complete" else "NOT_READY",
                      "label_provenance": "SYNTHETIC", "manifest_file": f"case-{i:02d}/manifest.json",
                      "manifest_sha256": sha})
    dataset = {"schema": "laif.calibration.v1", "dataset_version": "synthetic-2026-10-30.1",
               "cases": cases, "holdout_seal": holdout_seal(cases)}
    _write(root / "dataset.json", dataset)
    return root / "dataset.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, nargs="?", help="calibration dataset JSON")
    parser.add_argument("--make-synthetic-corpus", type=Path)
    parser.add_argument("--require-adjudicated", action="store_true")
    args = parser.parse_args()
    try:
        if args.make_synthetic_corpus is not None:
            path = make_synthetic_corpus(args.make_synthetic_corpus)
        elif args.dataset is not None:
            path = args.dataset
        else:
            parser.error("provide dataset or --make-synthetic-corpus")
        report = calibrate(json.loads(path.read_text(encoding="utf-8")), path.parent,
                           require_adjudicated=args.require_adjudicated)
    except (ValueError, OSError, UnicodeError, TypeError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
