#!/usr/bin/env python3
"""Offline, self-attested second-reader agreement checks for scholarly dossiers.

No review is fabricated or equated with legal approval, actual independence,
scientific replication, source authentication or verified control operation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

from laif_research_report import ResearchInputError, _nonblank, _read_json, safe_stem

SCHEMA = "laif.independent-review.v1"
SOURCE_VERDICTS = {"source_matched", "source_disagrees", "unverified"}
CLAIM_VERDICTS = {"supported", "challenged", "uncertain"}
INDEPENDENCE_STATES = {"self_declared_independent", "not_independent", "unknown"}


def load_dossier(path: Path) -> tuple[dict, str, dict[str, str]]:
    raw = path.read_bytes()
    dossier = _read_json(path)
    if dossier.get("schema") != "laif.research-dossier.v1":
        raise ResearchInputError("not a supported research dossier")
    if not isinstance(dossier.get("source"), dict):
        raise ResearchInputError("dossier source identity is missing")
    targets: dict[str, str] = {}
    for key, kind in (("evidence", "evidence"), ("reviewer_findings", "finding")):
        if not isinstance(dossier.get(key), list):
            raise ResearchInputError(f"dossier {key} is not a list")
        for item in dossier[key]:
            if not isinstance(item, dict):
                raise ResearchInputError("malformed dossier target")
            target_id = item.get("evidence_id" if kind == "evidence" else "finding_id")
            pattern = r"E\d{3,5}" if kind == "evidence" else r"F\d{3,5}"
            if (not isinstance(target_id, str) or not re.fullmatch(pattern, target_id)
                    or target_id in targets):
                raise ResearchInputError("dossier has missing or duplicate review targets")
            targets[target_id] = kind
    criteria_review = dossier.get("criteria_review")
    if criteria_review is not None:
        if not isinstance(criteria_review, dict) or not isinstance(criteria_review.get("criteria"), list):
            raise ResearchInputError("malformed criterion review targets")
        from laif_spec import ASSESSMENT_CRITERIA
        for row in criteria_review["criteria"]:
            if not isinstance(row, dict) or row.get("criterion_id") not in ASSESSMENT_CRITERIA:
                raise ResearchInputError("unsupported criterion review target")
            cid = "CR-" + row["criterion_id"]
            if cid in targets:
                raise ResearchInputError("duplicate criterion review target")
            targets[cid] = "finding"
            for excerpt in row.get("source_excerpts", []):
                eid = excerpt.get("evidence_id") if isinstance(excerpt, dict) else None
                if not isinstance(eid, str) or not re.fullmatch(r"C\d{3,5}", eid) or eid in targets:
                    raise ResearchInputError("duplicate or malformed curated review target")
                targets[eid] = "evidence"
    return dossier, hashlib.sha256(raw).hexdigest(), targets


def review_template(dossier_hash: str, targets: dict[str, str]) -> dict:
    return {
        "schema": SCHEMA,
        "dossier_sha256": dossier_hash,
        "reviewer_id": "REPLACE_WITH_REVIEWER_ID",
        "independence_declaration": "unknown",
        "original_source_inspected": False,
        "instructions": (
            "Independently inspect the original source and full context. Mark your "
            "independence accurately. Replace each verdict and add a specific reason. "
            "A declaration is not proof of reviewer identity or independence."
        ),
        "ratings": [
            {
                "target_id": target_id, "verdict": "unverified" if kind == "evidence" else "uncertain",
                "reason": "Review pending: full source context not yet checked.",
            }
            for target_id, kind in targets.items()
        ],
    }


def validate_review(path: Path, dossier_hash: str, targets: dict[str, str]) -> dict:
    data = _read_json(path)
    if data.get("schema") != SCHEMA or data.get("dossier_sha256") != dossier_hash:
        raise ResearchInputError(f"{path.name}: schema or dossier hash mismatch")
    reviewer_id = data.get("reviewer_id")
    independence = data.get("independence_declaration")
    inspected = data.get("original_source_inspected")
    if (not _nonblank(reviewer_id) or reviewer_id == "REPLACE_WITH_REVIEWER_ID"
            or not isinstance(independence, str)
            or independence not in INDEPENDENCE_STATES or not isinstance(inspected, bool)):
        raise ResearchInputError(f"{path.name}: reviewer identity/declaration/source-inspection missing")
    ratings = data.get("ratings")
    if not isinstance(ratings, list):
        raise ResearchInputError(f"{path.name}: ratings must be a list")
    validated: dict[str, dict[str, str]] = {}
    for rating in ratings:
        if not isinstance(rating, dict):
            raise ResearchInputError(f"{path.name}: rating must be an object")
        target = rating.get("target_id")
        verdict = rating.get("verdict")
        reason = rating.get("reason")
        if not isinstance(target, str) or target not in targets or target in validated or not _nonblank(reason):
            raise ResearchInputError(f"{path.name}: invalid, duplicate or unexplained target")
        allowed = SOURCE_VERDICTS if targets[target] == "evidence" else CLAIM_VERDICTS
        if not isinstance(verdict, str) or verdict not in allowed:
            raise ResearchInputError(f"{path.name}: {target} verdict must be one of {sorted(allowed)}")
        validated[target] = {"verdict": verdict, "reason": reason.strip()}
    return {
        "reviewer_id": reviewer_id.strip(),
        "independence_declaration": independence,
        "original_source_inspected": inspected,
        "ratings": validated,
        "submitted_file": path.name,
        "self_attested_only": True,
    }


def summarise(dossier_hash: str, targets: dict[str, str], reviews: list[dict]) -> dict:
    reviewers = [x["reviewer_id"] for x in reviews]
    if len(reviewers) != len(set(reviewers)):
        raise ResearchInputError("reviewer_id must be unique across submitted reviews")
    target_summary = {}
    for target_id, kind in targets.items():
        entries = [{"reviewer_id": review["reviewer_id"],
                    **review["ratings"][target_id]}
                   for review in reviews if target_id in review["ratings"]]
        decisions = {x["verdict"] for x in entries}
        undecided = "unverified" if kind == "evidence" else "uncertain"
        target_summary[target_id] = {
            "kind": kind, "ratings": entries, "review_count": len(entries),
            "agreement": ("NOT_COMPARABLE" if len(entries) < 2 else
                          "DISAGREEMENT" if len(decisions) > 1 else
                          "INCONCLUSIVE" if undecided in decisions else "CONCORDANT_SELF_ATTESTED"),
        }
    pair_matches, pair_total = 0, 0
    for first, second in combinations(reviews, 2):
        for target_id in targets:
            if target_id in first["ratings"] and target_id in second["ratings"]:
                pair_total += 1
                pair_matches += int(first["ratings"][target_id]["verdict"] ==
                                    second["ratings"][target_id]["verdict"])
    incomplete = any(x["review_count"] != len(reviews) for x in target_summary.values())
    conflict = any(x["agreement"] == "DISAGREEMENT" for x in target_summary.values())
    uncertain = any(x["agreement"] in ("INCONCLUSIVE", "NOT_COMPARABLE") for x in target_summary.values())
    weak_declaration = any(x["independence_declaration"] != "self_declared_independent" or
                           not x["original_source_inspected"] for x in reviews)
    if len(reviews) < 2:
        status = "INSUFFICIENT_SECOND_READERS"
    elif incomplete:
        status = "PARTIAL_REVIEW"
    elif weak_declaration:
        status = "INDEPENDENCE_OR_SOURCE_CONTEXT_NOT_ATTESTED"
    elif conflict:
        status = "DISAGREEMENT_REQUIRES_ADJUDICATION"
    elif uncertain:
        status = "UNRESOLVED_UNCERTAINTY"
    else:
        status = "CONCORDANT_SELF_ATTESTATIONS_NOT_CERTIFICATION"
    if not targets:
        status = "NO_REVIEWABLE_EVIDENCE_OR_FINDINGS"
    return {
        "schema": "laif.research-review-summary.v1",
        "dossier_sha256": dossier_hash,
        "status": status,
        "reviewer_count": len(reviews),
        "target_count": len(targets),
        "paired_rating_count": pair_total,
        "paired_agreement_count": pair_matches,
        "pairwise_raw_agreement": round(pair_matches / pair_total, 6) if pair_total else None,
        "agreement_note": "Descriptive pairwise raw agreement on shared targets only; not validity, calibration, kappa, independent replication or legal compliance.",
        "reviewers": reviews,
        "targets": target_summary,
        "external_identity_verification": "NOT_PERFORMED",
        "source_authentication": "SELF_ATTESTED_ONLY",
        "publication_clearance": "NOT_GRANTED",
    }


def render_markdown(summary: dict) -> str:
    lines = [
        "# Second-reader evidence review — provisional",
        "",
        "**Review state:** " + summary["status"],
        "**Dossier SHA-256:** " + summary["dossier_sha256"],
        "**Reviewers (self-identified):** " + str(summary["reviewer_count"]),
        "**Reviewable targets:** " + str(summary["target_count"]),
        "",
        "## Per-target agreement",
        "",
    ]
    for target, item in summary["targets"].items():
        lines.append(f"- {target} ({item['kind']}): {item['agreement']}; "
                     f"{item['review_count']} review(s).")
    lines += [
        "", "## Descriptive reviewer agreement", "",
        f"- Shared target-pairs: {summary['paired_rating_count']}",
        f"- Matching target-pairs: {summary['paired_agreement_count']}",
        "- Raw proportion: " + (str(summary["pairwise_raw_agreement"])
                               if summary["pairwise_raw_agreement"] is not None else "not calculable"),
        "",
        "These counts describe submitted labels only. They are not a measure of "
        "scientific validity, legal accuracy or independent replication.",
        "",
        "## Publication boundary",
        "",
        "Reviewer identities, independence claims and original-source inspection are "
        "self-attested, not independently authenticated. Conflicts, uncertainty "
        "and missing source checks require human resolution. Even concordant "
        "reviews do not authorise publication or certify any AI system.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="research_data.json from laif_research_report.py")
    parser.add_argument("--review", action="append", type=Path, default=[], help="Independent self-attested reviewer JSON; repeat for each reviewer")
    parser.add_argument("--template", action="store_true", help="Print blank second-reader JSON; no files written")
    parser.add_argument("--preview", action="store_true", help="Print review summary; no files written")
    parser.add_argument("--output-dir", type=Path, default=Path("laif_outputs/research"))
    args = parser.parse_args(argv)
    try:
        _dossier, dossier_hash, targets = load_dossier(args.dossier)
        if args.template:
            if args.review:
                raise ResearchInputError("use --template separately from --review")
            print(json.dumps(review_template(dossier_hash, targets), ensure_ascii=False, indent=2))
            return 0
        reviews = [validate_review(path, dossier_hash, targets) for path in args.review]
        if not reviews:
            raise ResearchInputError("provide at least one --review, or request --template")
        summary = summarise(dossier_hash, targets, reviews)
        report = render_markdown(summary)
        if args.preview:
            print(report)
            return 0
        args.output_dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(summary, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
        prefix = f"{safe_stem(args.dossier.stem)}-{digest}"
        data_path = args.output_dir / f"{prefix}.second_reader.json"
        report_path = args.output_dir / f"{prefix}.second_reader.md"
        data_path.write_text(payload, encoding="utf-8")
        report_path.write_text(report, encoding="utf-8")
        print(f"Second-reader assessment: {report_path}")
        print(f"Review evidence JSON: {data_path}")
        print(f"State: {summary['status']}; no publication clearance granted.")
        return 0
    except (OSError, UnicodeError, ResearchInputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
