#!/usr/bin/env python3
"""Offline, research-neutral evidence dossier from a local governance document.

This is a presentation/reviewer workflow, not a new LAIF scoring or certification
mode. Automated extraction cannot prove an absent safeguard, legal status or
real-world control effectiveness. Unreviewed dossiers contain observations,
questions and limitations, never asserted institutional findings.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from scripts.laif_evidence_display import locate, locate_review, passage, evidence_links
from assessment_engine import assess, toolchain_fingerprint
from laif_spec import ASSESSMENT_CRITERIA
from laif_criteria_review import validate_criteria_review, criterion_template
from laif_process_document import (
    ExtractionError, build_extraction_quality_profile, build_low_confidence_quote_candidates,
    build_quote_bank, build_verification_required_evidence, extract_document,
    safe_stem, sha256_file,
)

SCHEMA = "laif.research-dossier.v1"
ANNOTATION_SCHEMA = "laif.research-annotations.v1"
SCOPES = ("unknown", "excerpt", "declared_full_document")
STATES = ("unknown", "historical", "asserted_current")
CLAIM_TYPES = ("OBSERVATION", "INFERENCE", "HYPOTHESIS")
MAX_OBSERVATIONS = 12
DEFAULT_QUESTION = "Which governance commitments and evidence requirements are explicit in the supplied material?"
REVIEW_QUESTIONS = (
    "Which human interests, actors, duties and conditions does the source explicitly connect?",
    "Are obligations binding here, or does their force arise from another instrument or contract?",
    "What external law, guidance or operational documentation could qualify an apparent gap?",
    "What independent evidence would distinguish a stated control from an implemented one?",
    "How can decisions be contested, changed, suspended or reversed in the full governance setting?",
    "What counterexample or alternative reading would overturn the provisional interpretation?",
)


class ResearchInputError(ValueError):
    """Invalid research input or attempted unsupported attribution."""


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ResearchInputError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ResearchInputError(f"non-standard JSON constant {value}")


def _read_json(path: Path) -> dict:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object,
                            parse_constant=_reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ResearchInputError(f"cannot read JSON {path.name}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ResearchInputError("research annotations must be a JSON object")
    return parsed


def _report_date(raw: str | None) -> str:
    if raw is None:
        return dt.datetime.now(dt.timezone.utc).date().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        raise ResearchInputError("report date must use YYYY-MM-DD")
    try:
        return dt.date.fromisoformat(raw).isoformat()
    except ValueError as exc:
        raise ResearchInputError("invalid report date") from exc


def _extract_local(path: Path, preferred: str) -> Any:
    expected = {
        ".txt": "builtin", ".md": "builtin", ".markdown": "builtin",
        ".docx": "python-docx", ".pdf": "pypdf",
    }
    suffix = path.suffix.lower()
    if suffix not in expected:
        raise ResearchInputError("supported local formats: .txt, .md, .markdown, .docx, .pdf")
    if preferred == "auto-local":
        preferred = expected[suffix]
    if preferred != expected[suffix]:
        raise ResearchInputError(f"incorrect local extractor for {suffix}: use {expected[suffix]}")
    try:
        return extract_document(path, preferred)
    except ExtractionError as exc:
        raise ResearchInputError(str(exc)) from exc


def _observations(text: str, records: list[dict], eligible: bool, limit: int) -> list[dict]:
    if not eligible:
        return []
    output = []
    seen = set()
    for record in records:
        quote = record.get("exact_quote")
        start, end = record.get("start_offset"), record.get("end_offset")
        if (not _nonblank(quote) or not isinstance(start, int) or not isinstance(end, int)
                or start < 0 or end > len(text) or end <= start or text[start:end] != quote):
            # An extraction inconsistency is not a usable scholarly quotation.
            continue
        identity = (start, end)
        if identity in seen:
            continue
        seen.add(identity)
        output.append({
            "evidence_id": f"E{len(output)+1:03d}",
            "category": str(record.get("signal_category") or "source passage"),
            "exact_quote": quote,
            "start_char": start,
            "end_char": end,
            "extracted_line": text.count("\n", 0, start) + 1,
            "source_location": locate(text, start, end),
            "evidence_status": "EXTRACTED_TEXT_MATCH_ONLY",
            "interpretation_limit": "Passage exists in extracted text; it does not prove implementation, scope completeness or legal effect.",
        })
        if len(output) >= limit:
            break
    return output


def _check_ids(raw: Any, allowed: set[str], label: str) -> list[str]:
    if not isinstance(raw, list) or any(not _nonblank(x) or x not in allowed for x in raw):
        raise ResearchInputError(f"{label} must list existing evidence IDs")
    if len(set(raw)) != len(raw):
        raise ResearchInputError(f"{label} must not contain duplicate evidence IDs")
    return raw


def _evidence_manifest_sha256(observations: list[dict]) -> str:
    """Identity of the exact admitted evidence IDs, offsets and quotations."""
    manifest = [
        {key: row[key] for key in ("evidence_id", "start_char", "end_char", "exact_quote")}
        for row in observations
    ]
    encoded = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validated_annotations(path: Path | None, source_sha: str, manifest_sha: str,
                           observations: list[dict], data: dict | None = None) -> list[dict]:
    if path is None:
        return []
    data = _read_json(path) if data is None else data
    if (data.get("schema") != ANNOTATION_SCHEMA or data.get("source_sha256") != source_sha
            or data.get("evidence_manifest_sha256") != manifest_sha):
        raise ResearchInputError("annotation schema, source SHA-256 or evidence manifest SHA-256 mismatch")
    findings = data.get("findings")
    if not isinstance(findings, list):
        raise ResearchInputError("annotations.findings must be a list")
    allowed = {x["evidence_id"] for x in observations}
    bound = any(key in data for key in (
        "framework_source_sha256", "toolkit_source_sha256", "toolchain_fingerprint"))
    if bound and (data.get("framework_source_sha256") != sha256_file(ROOT / "LAIF_v1.2.txt")
                  or data.get("toolkit_source_sha256") != sha256_file(ROOT / "LAIF_Compliance_Toolkit.txt")
                  or data.get("toolchain_fingerprint") != toolchain_fingerprint()):
        raise ResearchInputError("annotation framework or Toolkit basis SHA-256 mismatch")
    if data.get("criteria_review") is not None:
        if not bound:
            raise ResearchInputError("criterion review requires current framework, Toolkit and toolchain identities")
        if data.get("criteria_review_protocol_sha256") != sha256_file(ROOT / "scripts/laif_criteria_review.py"):
            raise ResearchInputError("criterion-review protocol SHA-256 mismatch; generate a fresh template")
    output, seen = [], set()
    for item in findings:
        if not isinstance(item, dict):
            raise ResearchInputError("finding must be an object")
        fid = item.get("finding_id")
        if not isinstance(fid, str) or not re.fullmatch(r"F\d{3,5}", fid) or fid in seen:
            raise ResearchInputError("finding requires unique F001-style finding_id")
        seen.add(fid)
        statement = item.get("statement")
        reviewer = item.get("analyst_id")
        limits = item.get("limitations")
        claim_type = item.get("claim_type")
        alternatives = item.get("alternative_explanations")
        if (not all(_nonblank(x) for x in (statement, reviewer, limits))
                or claim_type not in CLAIM_TYPES
                or not isinstance(alternatives, list) or not alternatives
                or any(not _nonblank(x) for x in alternatives)):
            raise ResearchInputError(f"{fid}: statement, type, analyst, limitations and alternative explanation required")
        supporting = _check_ids(item.get("evidence_ids"), allowed, f"{fid}.evidence_ids")
        counter = _check_ids(item.get("counterevidence_ids", []), allowed, f"{fid}.counterevidence_ids")
        if not supporting:
            raise ResearchInputError(f"{fid}: at least one exact-source evidence reference required")
        criteria = item.get("criterion_ids", [])
        if (not isinstance(criteria, list) or any(not isinstance(x, str) or x not in ASSESSMENT_CRITERIA for x in criteria)
                or len(set(criteria)) != len(criteria)):
            raise ResearchInputError(f"{fid}: criterion_ids must be unique supported LAIF criterion IDs")
        output.append({
            "finding_id": fid, "claim_type": claim_type, "statement": statement.strip(),
            "evidence_ids": supporting, "counterevidence_ids": counter,
            "alternative_explanations": alternatives, "limitations": limits.strip(),
            "analyst_id": reviewer.strip(), "review_status": "ANALYST_SUBMITTED_UNVERIFIED",
            "criterion_ids": criteria,
            "method_basis_status": "HASH_BOUND_ANALYST_CLAIM" if bound else "UNBOUND_LEGACY_ANNOTATION",
        })
    return output


def build_dossier(path: Path, *, extractor: str = "auto-local", source_scope: str = "unknown",
                  instrument_status: str = "unknown", jurisdiction: str = "", source_url: str = "",
                  question: str = DEFAULT_QUESTION, date: str | None = None,
                  review_file: Path | None = None, max_quotes: int = 8) -> dict:
    if source_scope not in SCOPES or instrument_status not in STATES:
        raise ResearchInputError("unknown source scope or instrument status")
    if not _nonblank(question) or not 1 <= max_quotes <= MAX_OBSERVATIONS:
        raise ResearchInputError("research question and max-quotes (1–12) are required")
    if source_url:
        try:
            parsed_url = urlsplit(source_url)
        except ValueError as exc:
            raise ResearchInputError("source URL is malformed") from exc
        if (parsed_url.scheme != "https" or not parsed_url.netloc
                or parsed_url.username or parsed_url.password):
            raise ResearchInputError("source URL must be an HTTPS attribution URL without credentials; it is not fetched")
    date = _report_date(date)
    path = path.expanduser().resolve()
    extraction = _extract_local(path, extractor)
    source_sha = sha256_file(path)
    text = extraction.text
    # The existing engine supplies candidate evidence/sector heuristics only.
    # Its scoring, certification and stronger inferred narratives are not used.
    assessed = assess(path.stem, "uploaded_document", text, sector="auto",
                      assessment_mode="external_framework")
    processing = {"original_file_name": path.name, "stored_source_path": path.name,
                  "source_sha256": source_sha}
    extraction_meta = {"extractor_used": extraction.extractor_used,
                       "extraction_confidence": extraction.extraction_confidence,
                       "warnings": extraction.warnings}
    low = build_low_confidence_quote_candidates(text, processing, extraction_meta, assessed)
    quotes = build_quote_bank(text, processing, extraction_meta, assessed, low)
    verification_required = build_verification_required_evidence(
        low, processing, extraction_meta, admitted_quotes=quotes)
    quality = build_extraction_quality_profile(text, extraction_meta, quotes,
                                               verification_required, low)
    eligible = bool(quality.get("primary_quote_eligible"))
    observations = _observations(text, quotes, eligible, max_quotes)
    manifest_sha = _evidence_manifest_sha256(observations)
    review_data = _read_json(review_file) if review_file else None
    findings = _validated_annotations(review_file, source_sha, manifest_sha, observations, review_data)
    try:
        criteria_review = validate_criteria_review(review_data.get("criteria_review") if review_data else None, text)
    except ValueError as exc:
        raise ResearchInputError(str(exc)) from exc
    locate_review(criteria_review, text)
    criterion_keys = {row["criterion_id"] for row in criteria_review["criteria"]} if criteria_review else set()
    limits = [
        "Passage selection is heuristic and non-exhaustive; relevant clauses can be missed.",
        "Source scope and instrument status are operator declarations, not verified by this software.",
        "Exact extracted passages require inspection against the original document before external citation.",
        "Extracted-text character and line offsets are not verified page or original-byte citations.",
        "A missing lexical signal does not establish that an obligation, right or safeguard is absent.",
        "Other legal instruments, procedures and operational evidence may change the interpretation.",
        "The method has no independently validated sensitivity, specificity or legal-validity measure.",
        "Analyst identities and annotations are recorded but not independently authenticated.",
    ]
    if source_scope != "declared_full_document":
        limits.insert(0, "Only an excerpt or scope-unknown text was supplied: no document-wide absence claims are warranted.")
    if extraction.warnings:
        limits.append("Extraction warnings require manual review: " + "; ".join(extraction.warnings))
    if not eligible or not observations:
        limits.append("No primary-quote-grade evidence was admitted: analysis must abstain pending better source material.")
    return {
        "schema": SCHEMA,
        "status": "ANALYST_ANNOTATED_DRAFT" if findings or criteria_review else (
            "EVIDENCE_REVIEW_REQUIRED" if not observations else "EVIDENCE_INVENTORY_ONLY"),
        "report_date": date,
        "research_question": question.strip(),
        "source": {
            "file_name": path.name, "source_sha256": source_sha,
            "extracted_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "source_scope": source_scope, "instrument_status": instrument_status,
            "jurisdiction_claim": jurisdiction.strip() or "not supplied",
            "source_url_claim": source_url or "not supplied",
            "provenance": "LOCAL_DOCUMENT_NOT_AUTHORITY_VERIFIED",
            "extracted_characters": len(text), "extractor": extraction.extractor_used,
            "extraction_confidence": extraction.extraction_confidence,
        },
        "method": {
            "analytical_lens": "Law-Aligned Intelligence Framework (LAIF) v1.2, openly disclosed, not endorsed or legally authoritative",
            "method_version": "research-neutral-presentation-v1",
            "renderer_sha256": sha256_file(Path(__file__).resolve()),
            "assessment_channel": "external_framework_candidate_signals_only",
            "sampling_design": "Heuristic candidate retrieval only; not random, comprehensive, or an estimator of safeguard prevalence.",
            "internal_engine_fingerprint": toolchain_fingerprint(),
            "criteria_review_protocol_sha256": sha256_file(ROOT / "scripts/laif_criteria_review.py"),
            "framework_source_sha256": sha256_file(ROOT / "LAIF_v1.2.txt"),
            "toolkit_source_sha256": sha256_file(ROOT / "LAIF_Compliance_Toolkit.txt"),
            "scores_and_certification_excluded": True,
            "inference_policy": "Only exact-source observations are machine-produced; absence, legal effect, implementation and validity require human evidence.",
        },
        "evidence": observations,
        "evidence_manifest_sha256": manifest_sha,
        "reviewer_findings": findings,
        "criteria_review": criteria_review,
        "criteria_coverage": [
            {"criterion_id": key, **criterion,
             "finding_ids": [row["finding_id"] for row in findings if key in row["criterion_ids"]],
             "status": "AUTHOR_DETERMINATION_SUPPLIED" if key in criterion_keys else ("ANALYST_CLAIMS_ATTACHED_REVIEW_REQUIRED" if any(key in row["criterion_ids"] for row in findings) else "NOT_ASSESSED")}
            for key, criterion in ASSESSMENT_CRITERIA.items()
        ],
        "review_questions": list(REVIEW_QUESTIONS),
        "limitations": limits,
        "low_confidence_candidate_count": len(low),
        "verification_required_evidence_count": len(verification_required),
        "primary_quote_grade": eligible,
        "independent_replication": "NOT_PERFORMED",
        "scholarly_validation": "NOT_ESTABLISHED",
    }


def _md_text(value: Any) -> str:
    # User documents and reviewer inputs are not trusted Markdown. Escaping
    # HTML alone leaves image links, embedded Markdown and fake headings active.
    escaped = html.escape(str(value), quote=False).replace("\r", " ").replace("\n", " ")
    return re.sub(r"([\\`*_{}\[\]()#+!|>~])", r"\\\1", escaped)


def _blockquote(value: str) -> str:
    return "\n".join("> " + _md_text(line) for line in value.splitlines())


def render_markdown(dossier: dict) -> str:
    source = dossier["source"]
    evidence = dossier["evidence"]
    lines = [
        f"# Source-bounded AI governance evidence review — {_md_text(source['file_name'])}",
        "",
        "**Status:** " + _md_text(dossier["status"]) + " — scholarly working draft, not a certified conclusion.",
        "**Research question:** " + _md_text(dossier["research_question"]),
        "**Date:** " + dossier["report_date"],
        "",
        "## Source identity and coverage",
        "",
        "- Source file: " + _md_text(source["file_name"]),
        "- SHA-256 (original bytes): " + source["source_sha256"],
        "- SHA-256 (extracted text): " + source["extracted_text_sha256"],
        "- SHA-256 (admitted evidence manifest): " + dossier["evidence_manifest_sha256"],
        "- Research renderer SHA-256: " + dossier["method"]["renderer_sha256"],
        "- LAIF principal text SHA-256: " + dossier["method"].get("framework_source_sha256", "not recorded in legacy dossier"),
        "- Toolkit source SHA-256: " + dossier["method"].get("toolkit_source_sha256", "not recorded in legacy dossier"),
        "- Declared scope: " + _md_text(source["source_scope"]),
        "- Declared instrument status: " + _md_text(source["instrument_status"]),
        "- Jurisdiction (supplied, unverified): " + _md_text(source["jurisdiction_claim"]),
        "- Origin URL (supplied, not fetched): " + _md_text(source["source_url_claim"]),
        "- Extraction: " + _md_text(source["extractor"]) + "; source status not independently authenticated.",
        "",
        "## Method and inference controls",
        "",
        "The source was locally extracted and candidate passages were located through a selective, heuristic "
        "retrieval method that can miss relevant material. Under the same input, code and dependencies the "
        "candidate extraction can be repeated; no independent replication or sampling validity is claimed. "
        "The analytical lens is LAIF v1.2, disclosed for methodological transparency; "
        "its adoption is neither a subject nor an aim of this assessment. Internal scores, rankings and "
        "LAIF-native certification results are excluded.",
        "",
        "Passage presence is an observation; a claim about implementation, absence of protection, legal effect or "
        "comparative superiority is an interpretation requiring additional evidence and expert review.",
        "",
        "## Observations: exact extracted passages",
        "",
    ]
    if not evidence:
        lines += [
            "**Abstention:** no quote-grade candidate passage was admitted. Obtain and inspect a better "
            "source before forming findings.",
            "",
        ]
    for row in evidence:
        lines += [f"### {row['evidence_id']} — retrieval hint: {_md_text(row['category'])}", ""]
        lines += passage(row, row["evidence_id"], "research", source=dossier["source"]["file_name"])
        lines += ["This establishes only that the passage appears in the extracted text.", ""]
    lines += ["## Analyst interpretations and counterevidence", ""]
    if not dossier["reviewer_findings"] and not dossier.get("criteria_review"):
        lines += [
            "No analyst findings were supplied. The software deliberately does not convert undetected patterns "
            "into claims of missing safeguards or turn candidate quotations into legal conclusions.",
            "",
        ]
    if dossier.get("criteria_review"):
        from laif_process_document import criteria_review_sections
        lines += criteria_review_sections(dossier["criteria_review"], dossier["source"]["file_name"])
    for finding in dossier["reviewer_findings"]:
        lines += [
            f"### {_md_text(finding['finding_id'])} — {_md_text(finding['claim_type'])}",
            "",
            _md_text(finding["statement"]),
            "",
            "- Supporting passages: " + evidence_links(finding["evidence_ids"], "research"),
            "- Potential counterevidence passages: " + (
                evidence_links(finding["counterevidence_ids"], "research") or "none nominated; not proof of absence"),
            "- Alternative explanations: " + "; ".join(_md_text(x) for x in finding["alternative_explanations"]),
            "- Limits: " + _md_text(finding["limitations"]),
            "- Analyst (identity not authenticated): " + _md_text(finding["analyst_id"]),
            "- Review status: analyst-submitted; independent corroboration not established.",
            "- Method-basis binding: " + _md_text(finding.get("method_basis_status", "not recorded in legacy dossier")),
            "",
        ]
        for identity in dict.fromkeys(finding["evidence_ids"] + finding["counterevidence_ids"]):
            item = next(row for row in evidence if row["evidence_id"] == identity)
            lines += passage(item, identity, "research", source=dossier["source"]["file_name"], with_anchor=False)
    lines += ["## LAIF criteria coverage", "",
              "This records which criteria have analyst claims attached, not which criteria pass. Unmapped criteria remain NOT_ASSESSED. Pattern matches and filled fields do not certify substantive coherence or a deployment.", ""]
    for row in dossier.get("criteria_coverage", []):
        lines += [f"- **{row['criterion_id']} — {_md_text(row['name'])}:** {row['status']}. Source: {_md_text(row['source'])}. Findings: {', '.join(row['finding_ids']) or 'none'}. {_md_text(row['question'])}"]
    lines += ["", "## Questions for source and expert review", ""]
    lines += [f"{idx}. {_md_text(question)}" for idx, question in enumerate(dossier["review_questions"], start=1)]
    lines += ["", "## Limitations and next evidence", ""]
    lines += ["- " + _md_text(note) for note in dossier["limitations"]]
    lines += [
        "",
        "**Research status:** computationally repeatable candidate extraction; independent replication, "
        "construct validity, inter-reviewer agreement and substantive legal review have not been established.",
        "",
        "**Required next step:** verify source/version, inspect full context, test alternative interpretations "
        "and seek independent review before any public analytical conclusion.",
        "",
    ]
    return "\n".join(lines)


def review_template(dossier: dict, *, include_criteria: bool = False) -> dict:
    return {
        "schema": ANNOTATION_SCHEMA,
        "source_sha256": dossier["source"]["source_sha256"],
        "evidence_manifest_sha256": dossier["evidence_manifest_sha256"],
        "framework_source_sha256": dossier["method"].get("framework_source_sha256"),
        "toolkit_source_sha256": dossier["method"].get("toolkit_source_sha256"),
        "toolchain_fingerprint": dossier["method"].get("internal_engine_fingerprint"),
        "criteria_review_protocol_sha256": dossier["method"].get("criteria_review_protocol_sha256"),
        "instructions": ("Add source-supported findings with unique finding_id, claim_type "
                         "(OBSERVATION/INFERENCE/HYPOTHESIS), statement, evidence_ids, "
                         "counterevidence_ids, at least one alternative explanation, limitations "
                         "and analyst_id. Optional criterion_ids map claims to the listed LAIF criteria. "
                         "Keep the source/evidence/framework/Toolkit hashes and toolchain fingerprint unchanged. "
                         "A populated file is still an unverified analyst claim."),
        "available_evidence_ids": [x["evidence_id"] for x in dossier["evidence"]],
        "available_criteria": [{"criterion_id": key, **row} for key, row in ASSESSMENT_CRITERIA.items()],
        "findings": [],
        "criteria_review": criterion_template() if include_criteria else None,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a non-promotional, source-bounded scholarly evidence dossier offline.")
    parser.add_argument("source", type=Path, help="Local .txt, .md, .docx or .pdf governance document")
    parser.add_argument("--scope", choices=SCOPES, default="unknown", help="Operator-declared source completeness")
    parser.add_argument("--instrument-status", choices=STATES, default="unknown")
    parser.add_argument("--jurisdiction", default="")
    parser.add_argument("--source-url", default="", help="Attribution only; no network retrieval")
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--date", help="YYYY-MM-DD; provide for deterministic report dates")
    parser.add_argument("--criteria-template", action="store_true", help="include unfilled records for all eight LAIF criteria")
    parser.add_argument("--review-file", type=Path, help="Optional human analyst findings from prior review template")
    parser.add_argument("--extractor", choices=("auto-local", "builtin", "python-docx", "pypdf"), default="auto-local")
    parser.add_argument("--max-quotes", type=int, default=8, help="1–12 exact extracted passages")
    parser.add_argument("--output-dir", type=Path, default=Path("laif_outputs/research"))
    parser.add_argument("--preview", action="store_true", help="Print report without writing any file")
    parser.add_argument("--require-evidence", action="store_true", help="Nonzero exit if no quote-grade evidence is available")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        dossier = build_dossier(args.source, extractor=args.extractor, source_scope=args.scope,
                                instrument_status=args.instrument_status, jurisdiction=args.jurisdiction,
                                source_url=args.source_url, question=args.question, date=args.date,
                                review_file=args.review_file, max_quotes=args.max_quotes)
        if args.require_evidence and not dossier["evidence"]:
            raise ResearchInputError("no quote-grade evidence admitted; review is held")
        report = render_markdown(dossier)
        if args.preview:
            print(report)
            return 0
        args.output_dir.mkdir(parents=True, exist_ok=True)
        # Include the complete dossier content in the output identity so that a
        # later date, question, scope or analyst annotation cannot silently
        # overwrite a different earlier dossier for the same source document.
        dossier_bytes = json.dumps(dossier, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        run_digest = hashlib.sha256(dossier_bytes.encode("utf-8")).hexdigest()[:12]
        stem = safe_stem(args.source.stem) + "-" + dossier["source"]["source_sha256"][:10] + "-" + run_digest
        report_path = args.output_dir / f"{stem}.research_report.md"
        data_path = args.output_dir / f"{stem}.research_data.json"
        template_path = args.output_dir / f"{stem}.review_template.json"
        report_path.write_text(report, encoding="utf-8")
        data_path.write_text(dossier_bytes, encoding="utf-8")
        template_path.write_text(json.dumps(review_template(dossier, include_criteria=args.criteria_template), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Research report: {report_path}")
        print(f"Evidence JSON: {data_path}")
        print(f"Human review template: {template_path}")
        print(f"Status: {dossier['status']} | Source SHA-256: {dossier['source']['source_sha256']}")
        return 0
    except (ResearchInputError, OSError, UnicodeError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
