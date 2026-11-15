"""Reproduce a preregistered diagnostic probe; never infer author determinations."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from assessment_engine import assess, toolchain_fingerprint

PACKET = ROOT / "docs/research/overhaul-2026-11"
METRICS = ("structural_score", "terminology_score", "conceptual_proximity_score",
           "auditability_score", "enforceability_score", "overall_readiness_score")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare():
    raw = (PACKET / "predictions.json").read_bytes()
    if sha(raw) != (PACKET / "predictions.sha256").read_text().strip():
        raise ValueError("Prediction fingerprint mismatch")
    protocol = json.loads(raw)
    results, texts = {}, {}
    for document in protocol["documents"]:
        data = (ROOT / document["path"]).read_bytes()
        if sha(data) != document["sha256"]:
            raise ValueError("Source changed: " + document["id"])
        text = data.decode("utf-8").replace("\r\n", "\n")
        texts[document["id"]] = text
        result = assess(document["id"], "exploratory_retained_source", text,
                        assessment_mode=document["mode"])
        results[document["id"]] = {
            "source_sha256": document["sha256"], "mode": document["mode"],
            "scores": {k: result[k] for k in METRICS},
            "integrity_signals": result["integrity_requirement_diagnostics"],
            "substantive_determination": result["substantive_coherence_determination"],
            "actual_authored_criteria": None,
            "agreement_with_eight_criterion_predictions": None,
            "reason": "No authored review supplied. Diagnostic scores do not compute the eight authored determinations.",
        }
    checks = []
    for check in protocol["comparisons"]:
        left = results[check["left"]]["scores"][check["metric"]]
        right = results[check["right"]]["scores"][check["metric"]]
        checks.append({**check, "left_actual": left, "right_actual": right,
                       "expectation_met": left > right})
    mutations = []
    original = texts["nist"]
    baseline = results["nist"]["scores"]
    for mutation in protocol["mutations"]:
        if original.count(mutation["start"]) != 1:
            raise ValueError("Mutation start must be unique")
        start = original.index(mutation["start"])
        end = original.index(mutation["end"], start + len(mutation["start"]))
        modified = original[:start] + original[end:]
        result = assess("nist", "exploratory_retained_source", modified,
                        assessment_mode="external_framework")
        delta = {k: result[k] - baseline[k] for k in METRICS}
        # Overall is a derived weighted score, so specificity concerns the other dimensions.
        specific = all(v == 0 for k, v in delta.items()
                       if k not in (mutation["target"], "overall_readiness_score"))
        mutations.append({**mutation, "removed_quote": original[start:end],
                          "start_char": start, "end_char": end,
                          "mutated_text_sha256": sha(modified.encode("utf-8")),
                          "score_deltas": delta,
                          "expectation_met": delta[mutation["target"]] < 0 and specific,
                          "criterion_determination_delta": None})
    return {"schema": "laif.exploratory-comparison.v1", "author": "Codex",
            "prediction_sha256": sha(raw), "toolchain_fingerprint": toolchain_fingerprint(),
            "documents": results, "comparisons": checks, "mutations": mutations,
            "comparison_expectations_met": sum(c["expectation_met"] for c in checks),
            "mutation_expectations_met": sum(c["expectation_met"] for c in mutations),
            "eight_criterion_agreement": None,
            "ws1_acceptance": "NOT_ESTABLISHED",
            "limits": protocol["limitations"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="compare with retained receipt; no writes")
    args = parser.parse_args()
    rendered = json.dumps(compare(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    receipt = PACKET / "results.json"
    if args.verify:
        if receipt.read_text(encoding="utf-8") != rendered:
            raise ValueError("Exploratory receipt changed; investigate before accepting a new baseline")
        print("Exploratory receipt reproduced. This does not mean its hypotheses passed.")
    else:
        with receipt.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
        print(receipt)


if __name__ == "__main__":
    main()
