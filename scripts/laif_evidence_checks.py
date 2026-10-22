#!/usr/bin/env python3
"""Optional source-grounded LAIF control-evidence diagnostic (stdlib only).

Checks evidence identity, test coverage and contradictory records. It never
certifies control effectiveness, legal compliance or LAIF-native status.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SHA256 = re.compile(r"[0-9a-f]{64}\Z")
OUTCOMES = {"PASS", "FAIL"}
TEST_TYPES = {"positive", "negative"}


def _load_artifact(root: Path, name: str, expected: str, quote: str | None) -> str:
    """Require a confined file, exact SHA-256 and exact cited text."""
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise ValueError("invalid relative file path")
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes evidence directory")
    if not isinstance(expected, str) or not SHA256.fullmatch(expected):
        raise ValueError("invalid SHA-256")
    if quote is not None and (not isinstance(quote, str) or not quote.strip()):
        raise ValueError("missing source quote")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("SHA-256 mismatch")
    text = data.decode("utf-8")
    if quote is not None and quote not in text:
        raise ValueError("quoted text not found in source")
    return text


def check_manifest(manifest: dict, evidence_dir: Path) -> dict:
    """Diagnose corroboration of claimed controls; no scoring side effects."""
    root = evidence_dir.resolve()
    if not isinstance(manifest, dict) or not isinstance(manifest.get("controls"), list):
        raise ValueError("manifest requires a controls list")
    source_name = manifest.get("policy_file")
    source_sha = manifest.get("policy_sha256")
    # Source hash is mandatory: the policy being evaluated must be identifiable.
    policy = _load_artifact(root, source_name, source_sha, None)
    results = []
    ids = set()
    for record in manifest["controls"]:
        if not isinstance(record, dict):
            raise ValueError("each control must be an object")
        cid = record.get("id")
        if not isinstance(cid, str) or not cid.strip() or cid in ids:
            raise ValueError("control id must be nonempty and unique")
        ids.add(cid)
        quote = record.get("claim_quote")
        issues = []
        if not isinstance(quote, str) or not quote.strip() or quote not in policy:
            issues.append("claim quote absent from policy")
        evidence = record.get("evidence", [])
        if not isinstance(evidence, list):
            raise ValueError("evidence must be a list")
        seen = {}
        positive = negative = 0
        failed = contradicted = False
        for index, test in enumerate(evidence):
            if not isinstance(test, dict):
                issues.append(f"record {index}: not an object")
                continue
            ttype, outcome, test_id = (test.get("type"), test.get("outcome"), test.get("test_id"))
            if ttype not in TEST_TYPES or outcome not in OUTCOMES or not isinstance(test_id, str) or not test_id.strip():
                issues.append(f"record {index}: invalid test metadata")
                continue
            try:
                _load_artifact(root, test.get("file"), test.get("sha256"), test.get("quote"))
            except (ValueError, OSError, UnicodeError) as exc:
                issues.append(f"record {index}: {exc}")
                continue
            key = (ttype, test_id)
            if key in seen:
                if seen[key] != outcome:
                    contradicted = True
                else:
                    issues.append(f"record {index}: duplicate test identity")
                continue
            seen[key] = outcome
            positive += ttype == "positive"
            negative += ttype == "negative"
            failed |= outcome == "FAIL"
        if issues:
            status = "EVIDENCE_INVALID"
        elif contradicted:
            status = "CONTRADICTORY_RECORDS"
        elif failed:
            status = "OBSERVED_FAILURE"
        elif not evidence:
            status = "POLICY_ONLY"
        elif not positive or not negative:
            status = "INCOMPLETE_CONTROLS"
        else:
            status = "REVIEW_READY"
        if "claim quote absent from policy" in issues:
            status = "UNSUPPORTED_CLAIM"
        results.append({"id": cid, "status": status, "positive_tests": positive,
                        "negative_tests": negative, "issues": issues})
    return {"schema": "laif.evidence-diagnostic.v1", "policy_sha256": source_sha,
            "controls": results, "review_ready_count": sum(x["status"] == "REVIEW_READY" for x in results),
            "boundary": "Artifact integrity and declared test outcomes only; human verification required."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON file, paths relative to manifest directory")
    parser.add_argument("--require-review-ready", action="store_true", help="exit nonzero unless all controls are ready")
    args = parser.parse_args()
    try:
        result = check_manifest(json.loads(args.manifest.read_text(encoding="utf-8")), args.manifest.parent)
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, sort_keys=True, indent=2))
    return int(args.require_review_ready and (not result["controls"] or any(x["status"] != "REVIEW_READY" for x in result["controls"])))


if __name__ == "__main__":
    raise SystemExit(main())
