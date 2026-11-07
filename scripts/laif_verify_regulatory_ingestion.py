#!/usr/bin/env python3
"""Verify PR #98 source bytes, page maps and exact quotations, offline.

Default checks use only Python's standard library. --reextract additionally
requires Poppler pdftotext; it checks extraction reproducibility without writing
to the corpus. No network, hosted service or model API is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = ("au_dta_policy_v2_1", "eu_ai_act_amendment_2026_1744")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_decisions(root: Path, key: str) -> int:
    """Check authored finding identity/coverage, never its legal correctness."""
    directory = root / "docs/verification/2026-11-07/regulatory"
    record = json.loads((directory / f"{key}.decisions.json").read_text(encoding="utf-8"))
    assessment = f"docs/verification/2026-11-07/regulatory/{key}.assessment.md"
    manifest = json.loads((root / f"docs/verified/manifests/{key}.json").read_text(encoding="utf-8"))
    expected = {
        "schema": "laif.regulatory-reasoning.v1", "document_id": key,
        "review_status": "AUTHOR_ANALYSIS_NOT_INDEPENDENT", "assessment_path": assessment,
        "assessment_sha256": digest((root / assessment).read_bytes()),
        "framework_sha256": digest((root / "LAIF_v1.2.txt").read_bytes()),
        "toolkit_sha256": digest((root / "LAIF_Compliance_Toolkit.txt").read_bytes()),
        "source_pdf_sha256": manifest["source_file_sha256"],
        "source_text_sha256": manifest["sha256_hash"],
    }
    if any(record.get(field) != value for field, value in expected.items()):
        raise ValueError(f"{key}: reasoning record identity, method or assessment hash mismatch")
    evidence = json.loads((root / manifest["evidence_trace"]).read_text(encoding="utf-8"))
    allowed = {row["trace_id"] for row in evidence["traces"]}
    if key == "eu_ai_act_amendment_2026_1744":
        context = json.loads((directory / "original_act_substantive_evidence.json").read_text(encoding="utf-8"))
        allowed.update(row["trace_id"] for row in context["traces"])
    findings = record.get("criteria_findings")
    criteria = {"A.1", "A.2", "A.3", "A.4", "Q1", "Q2", "Q3", "G.1"}
    if (not isinstance(findings, list) or len(findings) != len(criteria)
            or any(not isinstance(row, dict) for row in findings)
            or any(not isinstance(row.get("criterion_id"), str) for row in findings)
            or {row.get("criterion_id") for row in findings} != criteria):
        raise ValueError(f"{key}: reasoning record requires all eight distinct review areas")
    cases = record.get("applicability_cases")
    if not isinstance(cases, list) or not cases or any(not isinstance(row, dict) for row in cases):
        raise ValueError(f"{key}: applicability cases missing")
    case_ids = [row.get("case_id") for row in cases]
    if any(not isinstance(value, str) or not value.strip() for value in case_ids) or len(set(case_ids)) != len(case_ids):
        raise ValueError(f"{key}: duplicate or invalid applicability case ID")
    for row in findings + cases:
        refs = row.get("trace_ids")
        if (not isinstance(refs, list) or not refs
                or any(not isinstance(value, str) or value not in allowed for value in refs)):
            raise ValueError(f"{key}: unsupported or missing reasoning evidence reference")
        required = ("determination", "reasoning", "closure_evidence", "alternative_explanation", "scope_limit") if "criterion_id" in row else ("assumptions", "determination", "boundary")
        if any(not isinstance(row.get(field), str) or not row[field].strip() for field in required):
            raise ValueError(f"{key}: reasoning, closure or scope fields missing")
    return len(findings)


def verify_source(root: Path, key: str, reextract: bool = False) -> int:
    base = root / "docs/verified"
    manifest = json.loads((base / "manifests" / f"{key}.json").read_text(encoding="utf-8"))
    source = root / manifest["source_file"]
    raw = base / "raw" / manifest["raw_filename"]
    if digest(source.read_bytes()) != manifest["source_file_sha256"]:
        raise ValueError(f"{key}: source PDF hash mismatch")
    if digest(raw.read_bytes()) != manifest["sha256_hash"]:
        raise ValueError(f"{key}: extracted text hash mismatch")
    if manifest["citation_status"] != "PRIMARY_CITABLE" or manifest["verification_status"] not in {
        "AUTOMATED_VERIFIED", "HUMAN_ATTESTED_AUTHORITATIVE"
    }:
        raise ValueError(f"{key}: source not admitted for primary citation")
    if not (root / manifest["assessment_reference"].split(" (", 1)[0]).is_file():
        raise ValueError(f"{key}: assessment missing")
    index = json.loads((root / manifest["page_index"]).read_text(encoding="utf-8"))
    text = raw.read_text(encoding="utf-8")
    if index["raw_sha256"] != manifest["sha256_hash"] or index["source_sha256"] != manifest["source_file_sha256"]:
        raise ValueError(f"{key}: page-map identities differ from manifest")
    if index["page_count"] != len(index["pages"]):
        raise ValueError(f"{key}: page count mismatch")
    end = 0
    for number, page in enumerate(index["pages"], 1):
        start = page["start_char"]
        marker = f"\n\n<!-- PDF page {number} -->\n"
        if page["page"] != number or text[end:start] != marker or not start < page["end_char"] <= len(text):
            raise ValueError(f"{key}: invalid page boundary {number}")
        if digest(text[start:page["end_char"]].encode("utf-8")) != page["text_sha256"]:
            raise ValueError(f"{key}: page {number} text hash mismatch")
        end = page["end_char"]
    if end != len(text):
        raise ValueError(f"{key}: unindexed trailing text")
    evidence = json.loads((root / manifest["evidence_trace"]).read_text(encoding="utf-8"))
    if evidence["raw_sha256"] != manifest["sha256_hash"] or not evidence["traces"]:
        raise ValueError(f"{key}: evidence identity mismatch or no quotations")
    seen = set()
    for quote in evidence["traces"]:
        page = index["pages"][quote["page"] - 1]
        start, end = quote["start_char"], quote["end_char"]
        if quote["trace_id"] in seen or quote["source_document"] != key:
            raise ValueError(f"{key}: duplicate or misattributed trace")
        seen.add(quote["trace_id"])
        if not page["start_char"] <= start < end <= page["end_char"]:
            raise ValueError(f"{key}: quote escapes its source page")
        if not quote["matched_text"] or text[start:end] != quote["matched_text"]:
            raise ValueError(f"{key}: quotation is not an exact source slice")
    if reextract:
        result = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(source), "-"],
                                capture_output=True, check=True)
        pages = result.stdout.decode("utf-8").split("\f")
        if pages[-1].strip():
            raise ValueError(f"{key}: unexpected terminal page content")
        reconstructed = "".join(f"\n\n<!-- PDF page {n} -->\n{p}"
                                for n, p in enumerate(pages[:-1], 1))
        if reconstructed != text:
            raise ValueError(f"{key}: extraction differs; review tool version, never silently repin")
    return len(seen)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reextract", action="store_true")
    args = parser.parse_args(argv)
    try:
        total = sum(verify_source(ROOT, key, args.reextract) for key in IDS)
        # Contextual original-Act evidence is distinct from PR #90's corpus
        # admission. Verify its actual PDF and recorded passages as well.
        context = json.loads((ROOT / "docs/verification/2026-11-07/regulatory/original_act_substantive_evidence.json").read_text(encoding="utf-8"))
        source = ROOT / context["source_pdf"]
        if digest(source.read_bytes()) != context["source_sha256"]:
            raise ValueError("Original Act contextual PDF hash mismatch")
        for trace in context["traces"]:
            if digest(trace["matched_text"].encode("utf-8")) != trace["sha256"]:
                raise ValueError("Original Act contextual passage hash mismatch")
        decisions = sum(verify_decisions(ROOT, key) for key in IDS)
        if args.reextract:
            result = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(source), "-"],
                                    capture_output=True, check=True)
            text = result.stdout.decode("utf-8")
            if digest(result.stdout) != context["full_extraction_sha256"]:
                raise ValueError("Original Act contextual extraction hash mismatch")
            for trace in context["traces"]:
                if text[trace["start_char"]:trace["end_char"]] != trace["matched_text"]:
                    raise ValueError("Original Act contextual quotation mismatch")
    except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: {len(IDS)} PDFs and raw-text hashes, complete page maps and {total} exact page-bounded quotes")
    print(f"PASS: original-Act contextual PDF and {len(context['traces'])} passage hashes")
    print(f"PASS: {decisions} authored finding records and their applicability references; reasoning validity not established by this check")
    if args.reextract:
        print("PASS: Poppler extraction reproduces committed raw text byte-for-byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
