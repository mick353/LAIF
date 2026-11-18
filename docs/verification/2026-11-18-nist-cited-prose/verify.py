"""Check authored NIST review quotations against pinned raw text and official PDF.

This verifies alphanumeric source wording only, not the review's interpretation.
"""

import hashlib
import json
import re
from pathlib import Path

import pypdf


ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "docs/verified/manual_ingest/NIST.AI.100-1.pdf"
RAW = ROOT / "docs/verified/raw/5f667a6f-NIST.AI.1001.md"
REVIEW = ROOT / "docs/verification/2026-11-07-substantive-review/5f667a6f-NIST.AI.1001/completed-review.json"
RESULT = Path(__file__).with_name("result.json")
PINNED = {
    PDF: "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1",
    RAW: "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509",
    REVIEW: "5072a4a11adc0bb4560ed3572936145f4b212a35cd615d6afb75e150b600780c",
}


def normalize(value):
    # Same bounded alphanumeric comparison as the 14 November fidelity receipt.
    value = re.sub(r"-\s*\n\s*", "", value)
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def main():
    for path, expected in PINNED.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"Pinned input changed: {path.relative_to(ROOT)}")

    raw = RAW.read_text(encoding="utf-8")
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    if review["source_sha256"] != PINNED[RAW]:
        raise SystemExit("Review is not bound to pinned raw source")
    pdf = pypdf.PdfReader(str(PDF))
    pages = [normalize(page.extract_text() or "") for page in pdf.pages]
    rows = []
    seen = set()
    for criterion in review["criteria_review"]["criteria"]:
        for excerpt in criterion["source_excerpts"]:
            identity = (criterion["criterion_id"], excerpt["evidence_id"])
            if identity in seen:
                raise SystemExit(f"Duplicate cited excerpt: {identity}")
            seen.add(identity)
            start, end = excerpt["start_char"], excerpt["end_char"]
            quote = excerpt["exact_quote"]
            if raw[start:end] != quote:
                raise SystemExit(f"Raw span differs: {identity}")
            normalized = normalize(quote)
            if len(normalized) < 50:
                raise SystemExit(f"Cited excerpt too short for this check: {identity}")
            matches = [index + 1 for index, page in enumerate(pages) if normalized in page]
            if len(matches) != 1:
                raise SystemExit(f"Expected one PDF page for {identity}, found {matches}")
            rows.append({"criterion_id": identity[0], "evidence_id": identity[1],
                         "raw_start_char": start, "raw_end_char": end,
                         "quote_sha256": hashlib.sha256(quote.encode("utf-8")).hexdigest(),
                         "pdf_page_1_based": matches[0],
                         "normalized_length": len(normalized)})
    if len(rows) != 16 or len({row["criterion_id"] for row in rows}) != 8:
        raise SystemExit("Expected 16 authored excerpts across eight criteria")
    result = {
        "schema": "laif.nist-cited-prose-pdf-fidelity.v1",
        "baseline_commit": "e574fb28c6d4c56faaaa429df27d6581342032e9",
        "pdf_sha256": PINNED[PDF], "raw_sha256": PINNED[RAW],
        "authored_review_sha256": PINNED[REVIEW],
        "pdf_pages": len(pages), "extractor": "pypdf",
        "extractor_version": pypdf.__version__,
        "comparison": "exact raw span, then punctuation/whitespace-insensitive alphanumeric match within one PDF page",
        "matched_count": len(rows), "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if RESULT.exists() and json.loads(RESULT.read_text(encoding="utf-8")) != result:
        raise SystemExit("Committed result differs from reproduction")


if __name__ == "__main__":
    main()
