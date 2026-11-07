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
    except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: {len(IDS)} PDFs and raw-text hashes, complete page maps and {total} exact page-bounded quotes")
    if args.reextract:
        print("PASS: Poppler extraction reproduces committed raw text byte-for-byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
