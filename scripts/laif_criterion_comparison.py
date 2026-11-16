"""Reproduce the locked, unblinded Codex eight-criterion exploration."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.laif_auto_criteria import judge

PACKET = ROOT / "docs/research/overhaul-current"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def remove_spans(text, spans):
    """Delete a union of exact spans without joining formerly separate clauses."""
    spans = sorted(set(spans))
    merged = []
    for start, end in spans:
        if not 0 <= start < end <= len(text):
            raise ValueError("Invalid source span")
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    edited = text
    for start, end in reversed(merged):
        edited = edited[:start] + "\n" + edited[end:]
    return edited


def rows(result):
    return {row["criterion_id"]: row for row in result["criteria"]}


def witness_count(row, component=None):
    return sum(len(c["witnesses"]) for c in row["components"]
               if component is None or c["component"] == component)


def compare(packet=PACKET):
    raw = (packet / "predictions.json").read_bytes()
    if digest(raw) != (packet / "predictions.sha256").read_text().strip():
        raise ValueError("Locked predictions changed")
    protocol = json.loads(raw)
    output = {"schema": "laif.criterion-comparison.v1", "author": "Codex",
              "prediction_sha256": digest(raw), "independent_validation": False,
              "documents": {}, "mutations": [], "systematic_ablations": []}
    texts = {}
    for source in protocol["documents"]:
        data = (ROOT / source["path"]).read_bytes()
        if digest(data) != source["sha256"]:
            raise ValueError("Source changed: " + source["id"])
        text = data.decode("utf-8").replace("\r\n", "\n")
        texts[source["id"]] = text
        actual = judge(text, source_scope=source["scope"])
        output["documents"][source["id"]] = {
            "path": source["path"], "source_sha256": source["sha256"],
            "judgment": actual,
            "prediction_comparison": {r["criterion_id"]: {
                "expected": source["expected"][r["criterion_id"]],
                "actual": r["determination"],
                "expectation_met": source["expected"][r["criterion_id"]] == r["determination"]}
                for r in actual["criteria"]}}
    for case in protocol["mutations"]:
        text = texts[case["source"]]
        if text.count(case["start"]) != 1:
            raise ValueError("Non-unique mutation start")
        start = text.index(case["start"])
        end = text.index(case["end"], start + len(case["start"]))
        edited = remove_spans(text, [(start, end)])
        before = rows(output["documents"][case["source"]]["judgment"])
        after = rows(judge(edited, source_scope="exploratory exact-clause deletion"))
        delta = witness_count(after[case["criterion"]], case["component"]) - witness_count(before[case["criterion"]], case["component"])
        output["mutations"].append({**case, "start_char": start, "end_char": end,
            "removed_quote": text[start:end], "removed_sha256": digest(text[start:end].encode()),
            "derivative_sha256": digest(edited.encode()), "target_witness_delta": delta,
            "expectation_met": delta < 0 if case["id"] == "remove_deactivation" else delta == 0,
            "before": before, "after": after})
    for source_id, text in texts.items():
        baseline = rows(output["documents"][source_id]["judgment"])
        for cid, row in baseline.items():
            witnesses = [w for c in row["components"] for w in c["witnesses"]]
            spans = sorted({(w["start_char"], w["end_char"]) for w in witnesses})
            if not spans:
                output["systematic_ablations"].append({"source": source_id, "criterion": cid,
                    "status": "NOT_APPLICABLE", "reason": "No matching source clauses to remove."})
                continue
            edited = remove_spans(text, spans)
            after = rows(judge(edited, source_scope="rule-guided whole-witness deletion"))
            output["systematic_ablations"].append({"source": source_id, "criterion": cid,
                "status": "EXPECTATION_MET" if after[cid]["determination"] == "NOT_ESTABLISHED" else "EXPECTATION_FAILED",
                "removed": [{"start_char": a, "end_char": b, "quote": text[a:b], "sha256": digest(text[a:b].encode())} for a, b in spans],
                "derivative_sha256": digest(edited.encode()),
                "before": row["determination"], "after": after[cid]["determination"],
                "all_criterion_deltas": {k: {"before": baseline[k]["determination"], "after": after[k]["determination"],
                    "witness_delta": witness_count(after[k])-witness_count(baseline[k])} for k in baseline}})
    totals = {key: {"supported_components": sum(r["supported_component_count"] for r in value["judgment"]["criteria"]),
                    "criteria_with_any_witness": sum(witness_count(r) > 0 for r in value["judgment"]["criteria"])}
              for key, value in output["documents"].items()}
    output["descriptive_counts_not_scores"] = totals
    output["ranking_expectation_met"] = all(totals["nist"][key] > totals["oecd"][key] for key in totals["nist"])
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(compare(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    path = PACKET / "results.json"
    if args.verify:
        if path.read_text(encoding="utf-8") != rendered:
            raise ValueError("Exploration receipt does not reproduce")
        print("Receipt reproduced; this is not independent validation.")
    else:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
        print(path)


if __name__ == "__main__":
    main()
