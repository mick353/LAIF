#!/usr/bin/env python3
"""Compare separately labelled governance attributes; no automatic validity claim.

This offline analysis of a caller-supplied study file does not run LAIF, inspect
source documents, authenticate reviewers or establish independent ground truth.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from pathlib import Path

SYSTEMS = ("laif", "checklist", "keyword")
SPLITS = ("development", "holdout")
PROVENANCE = ("SYNTHETIC", "HUMAN_ADJUDICATED")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SHA1 = re.compile(r"^[0-9a-f]{40}$")


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON property: {key}")
        result[key] = value
    return result


def fraction(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def wilson95(successes: int, total: int) -> list[float] | None:
    """Descriptive binomial interval; does not correct cluster/selection bias."""
    if not total:
        return None
    z = 1.959963984540054
    p = successes / total
    centre = (p + z*z / (2*total)) / (1 + z*z / total)
    radius = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total)) / (1 + z*z/total)
    return [round(max(0.0, centre-radius), 6), round(min(1.0, centre+radius), 6)]


def required_text(obj: dict, key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a nonempty string")
    return value


def is_sha256(value: object) -> bool:
    return isinstance(value, str) and bool(SHA256.fullmatch(value))


def validate(study: object, *, require_human: bool = False) -> list[dict]:
    if not isinstance(study, dict) or study.get("schema") != "laif.comparative-study.v1":
        raise ValueError("schema must equal laif.comparative-study.v1")
    required_text(study, "study_id")
    provenance = study.get("label_provenance")
    if provenance not in PROVENANCE:
        raise ValueError("label_provenance must be SYNTHETIC or HUMAN_ADJUDICATED")
    if require_human and provenance != "HUMAN_ADJUDICATED":
        raise ValueError("human-adjudicated labels required; synthetic inputs rejected")
    if not is_sha256(study.get("protocol_sha256")):
        raise ValueError("protocol_sha256 must be an explicit lowercase SHA-256 digest")
    revision = study.get("evaluated_revision")
    if not isinstance(revision, str) or not SHA1.fullmatch(revision):
        raise ValueError("evaluated_revision must be a declared 40-character Git SHA")
    cases = study.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    ids, families, source_splits = set(), {}, {}
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("each case must be an object")
        case_id = required_text(case, "id")
        family = required_text(case, "family")
        required_text(case, "attribute")
        if case_id in ids:
            raise ValueError(f"duplicate case id: {case_id}")
        ids.add(case_id)
        split = case.get("split")
        if split not in SPLITS:
            raise ValueError(f"{case_id}: split must be development or holdout")
        if family in families and families[family] != split:
            raise ValueError(f"{case_id}: same family appears in both splits")
        families[family] = split
        source = case.get("source_sha256")
        if not is_sha256(source):
            raise ValueError(f"{case_id}: source_sha256 must be lowercase SHA-256")
        if source in source_splits and source_splits[source] != split:
            raise ValueError(f"{case_id}: same source appears in both splits")
        source_splits[source] = split
        if type(case.get("reference")) is not bool:
            raise ValueError(f"{case_id}: adjudicated reference must be boolean")
        predictions = case.get("predictions")
        if not isinstance(predictions, dict) or set(predictions) != set(SYSTEMS):
            raise ValueError(f"{case_id}: all three comparator predictions required")
        for system in SYSTEMS:
            if predictions[system] is not None and type(predictions[system]) is not bool:
                raise ValueError(f"{case_id}: {system} must be true, false or null (abstain)")
        votes = case.get("reviewer_votes")
        if not isinstance(votes, list):
            raise ValueError(f"{case_id}: reviewer_votes must be a list")
        seen_reviewers = set()
        for vote in votes:
            if not isinstance(vote, dict) or type(vote.get("value")) is not bool:
                raise ValueError(f"{case_id}: reviewer votes must have boolean values")
            reviewer = required_text(vote, "reviewer")
            if reviewer in seen_reviewers:
                raise ValueError(f"{case_id}: repeated reviewer {reviewer}")
            seen_reviewers.add(reviewer)
        if provenance == "HUMAN_ADJUDICATED":
            if len(seen_reviewers) < 2:
                raise ValueError(f"{case_id}: two distinct blinded reviewer votes required")
            if not is_sha256(case.get("adjudication_sha256")):
                raise ValueError(f"{case_id}: adjudication_sha256 required for human label")
    if not any(case["split"] == "holdout" for case in cases):
        raise ValueError("at least one holdout case required")
    return cases


def metrics(cases: list[dict], system: str) -> dict:
    tp = tn = fp = fn = abstentions = 0
    for case in cases:
        predicted = case["predictions"][system]
        gold = case["reference"]
        if predicted is None:
            abstentions += 1
        elif predicted and gold:
            tp += 1
        elif predicted and not gold:
            fp += 1
        elif not predicted and gold:
            fn += 1
        else:
            tn += 1
    answered = tp + tn + fp + fn
    p, r = fraction(tp, tp+fp), fraction(tp, tp+fn)
    f1 = fraction(2*tp, 2*tp+fp+fn)
    return {
        "n": len(cases), "answered": answered, "abstained": abstentions,
        "coverage": fraction(answered, len(cases)),
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        "precision": p, "precision_wilson95": wilson95(tp, tp+fp),
        "recall": r, "recall_wilson95": wilson95(tp, tp+fn),
        "f1": f1, "f1_interval": None,
        "false_positive_rate": fraction(fp, fp+tn),
        "false_negative_rate": fraction(fn, fn+tp),
        "accuracy_on_answered": fraction(tp+tn, answered),
    }


def reviewer_agreement(cases: list[dict]) -> list[dict]:
    voters = sorted({v["reviewer"] for c in cases for v in c["reviewer_votes"]})
    result = []
    for a, b in itertools.combinations(voters, 2):
        observations = []
        for case in cases:
            votes = {v["reviewer"]: v["value"] for v in case["reviewer_votes"]}
            if a in votes and b in votes:
                observations.append((votes[a], votes[b]))
        if not observations:
            continue
        n = len(observations)
        agreed = sum(x == y for x, y in observations)
        pa = sum(x for x, _ in observations) / n
        pb = sum(y for _, y in observations) / n
        expected = pa*pb + (1-pa)*(1-pb)
        kappa = ((agreed/n - expected)/(1-expected)) if n >= 2 and expected < 1 else None
        result.append({"reviewer_a": a, "reviewer_b": b, "n": n,
                       "observed_agreement": fraction(agreed, n),
                       "cohen_kappa": round(kappa, 6) if kappa is not None else None})
    return result


def paired_outcomes(cases: list[dict], baseline: str) -> dict:
    count = {"both_correct": 0, "laif_only_correct": 0,
             "baseline_only_correct": 0, "both_wrong": 0}
    for case in cases:
        # Keep pairwise comparisons only where both systems emitted a label.
        laif, other = case["predictions"]["laif"], case["predictions"][baseline]
        gold = case["reference"]
        if laif is None or other is None:
            continue
        if laif == gold and other == gold:
            count["both_correct"] += 1
        elif laif == gold:
            count["laif_only_correct"] += 1
        elif other == gold:
            count["baseline_only_correct"] += 1
        else:
            count["both_wrong"] += 1
    return {"common_answered_n": sum(count.values()), **count,
            "warning": "Paired descriptive counts only; abstentions excluded, not statistical significance."}


def analyse(study: dict, *, require_human: bool = False) -> dict:
    cases = validate(study, require_human=require_human)
    splits = {}
    for split in SPLITS:
        selected = [case for case in cases if case["split"] == split]
        labels = sorted({case["attribute"] for case in selected})
        splits[split] = {
            "n": len(selected),
            "systems": {name: metrics(selected, name) for name in SYSTEMS},
            "by_attribute": {
                label: {name: metrics([c for c in selected if c["attribute"] == label], name)
                        for name in SYSTEMS} for label in labels
            },
            "human_pairwise_agreement_before_adjudication": reviewer_agreement(selected),
            "paired_comparisons": {name: paired_outcomes(selected, name)
                                   for name in ("checklist", "keyword")},
            "errors_or_abstentions": {
                name: [case["id"] for case in selected
                       if case["predictions"][name] is None
                       or case["predictions"][name] != case["reference"]]
                for name in SYSTEMS
            },
        }
    canonical = json.dumps(study, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    holdout = [{key: case[key] for key in ("id", "family", "source_sha256", "attribute", "reference")}
               for case in sorted(cases, key=lambda x: x["id"]) if case["split"] == "holdout"]
    return {
        "schema": "laif.comparative-study-report.v1",
        "study_id": study["study_id"],
        "declared_label_provenance": study["label_provenance"],
        "declared_evaluated_revision": study["evaluated_revision"],
        "declared_protocol_sha256": study["protocol_sha256"],
        "input_canonical_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "holdout_snapshot_sha256": hashlib.sha256(
            json.dumps(holdout, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
        "comparator_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "splits": splits,
        "status": "DESCRIPTIVE_COMPARISON_ONLY",
        "boundary": (
            "Input provenance and reviewer independence are declared, not verified by this tool. "
            "A snapshot hash is not proof the holdout was registered before inspection. "
            "Undefined ratios are null; abstentions are not negative predictions. "
            "Wilson intervals assume independent Bernoulli observations and do not account "
            "for document clusters, multiplicity or selection bias. No F1 interval is provided. "
            "The report does not validate LAIF theory, field accuracy, legal compliance or model safety."
        ),
    }


def format_summary(report: dict) -> str:
    """Compact human reading view; the JSON report retains full evidence fields."""
    def show(value: float | None) -> str:
        return "undefined" if value is None else f"{value:.3f}"

    lines = [
        "INDEPENDENT-STUDY COMPARISON — descriptive, source labels self-declared",
        f"Study: {report['study_id']}",
        f"Label provenance (unverified): {report['declared_label_provenance']}",
        f"Evaluated revision (declared): {report['declared_evaluated_revision']}",
        "",
    ]
    for split in SPLITS:
        data = report["splits"][split]
        lines.append(f"{split.upper()} — {data['n']} labelled attributes")
        if not data["n"]:
            lines.append("  No cases in this split.")
            lines.append("")
            continue
        lines.append("  System       Covered     Precision   Recall      F1       FP  FN")
        for name in SYSTEMS:
            m = data["systems"][name]
            lines.append(
                f"  {name:<12} {m['answered']:>2}/{m['n']:<6}"
                f" {show(m['precision']):<11} {show(m['recall']):<11}"
                f" {show(m['f1']):<9} {m['FP']:>2}  {m['FN']:>2}"
            )
        for name, paired in data["paired_comparisons"].items():
            lines.append(
                f"  Paired LAIF vs {name}: common={paired['common_answered_n']},"
                f" LAIF-only correct={paired['laif_only_correct']},"
                f" baseline-only correct={paired['baseline_only_correct']}"
            )
        reviewers = data["human_pairwise_agreement_before_adjudication"]
        if reviewers:
            for item in reviewers:
                lines.append(
                    f"  Human pair {item['reviewer_a']} / {item['reviewer_b']}: "
                    f"n={item['n']}, agreement={show(item['observed_agreement'])}, "
                    f"kappa={show(item['cohen_kappa'])}"
                )
        else:
            lines.append("  Human inter-rater agreement: unavailable")
        lines.append("")
    lines.extend([
        "BOUNDARY: This tool does not verify the sources, humans, labels, protocols",
        "or execution of LAIF/baselines. Synthetic values are not field results.",
        "Passing the comparator does NOT validate legal compliance, AI safety,",
        "LAIF theory or empirical accuracy. Use --format json for full counts,",
        "case-level errors, conditional intervals and reproducibility hashes.",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path, help="caller-prepared JSON study file")
    parser.add_argument("--require-human", action="store_true",
                        help="reject datasets labelled SYNTHETIC (does not authenticate reviewers)")
    parser.add_argument("--format", choices=("summary", "json"), default="summary",
                        help="human-readable summary (default) or complete JSON statistics")
    args = parser.parse_args()
    try:
        data = json.loads(args.study.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        report = analyse(data, require_human=args.require_human)
    except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(format_summary(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
