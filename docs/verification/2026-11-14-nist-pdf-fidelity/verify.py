"""Reproduce the bounded NIST AI RMF PDF-to-assessed-Markdown text comparison.

This is a source-fidelity check, not a LAIF assessment or legal conclusion.
It requires the optional pypdf package and the exact pinned repository files.
"""

import hashlib
import json
import re
from pathlib import Path

import pypdf


ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "docs/verified/manual_ingest/NIST.AI.100-1.pdf"
RAW = ROOT / "docs/verified/raw/5f667a6f-NIST.AI.1001.md"
SUPPORTING = ROOT / "docs/supporting/5f667a6f-NIST.AI.1001.md"
EXPECTED_PDF_SHA256 = "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1"
EXPECTED_RAW_SHA256 = "44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509"
CODE = re.compile(r"\b(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+\.\d+\s*:", re.I)
CATEGORY = re.compile(r"\b(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+\s*:", re.I)
TABLE_END = re.compile(
    r"\|\s*(?:\n|$)|Categories Subcategories|Continued on next page|"
    r"# AI RMF Profiles|6\. AI RMF Profiles"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text):
    # Deliberately ignores typography, punctuation, whitespace and Unicode
    # symbols. This establishes alphanumeric text alignment only.
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def marker_name(match):
    return re.sub(r"\s+", " ", match.group()).rstrip(":").upper()


def subcategories(text):
    matches = list(CODE.finditer(text))
    result = {}
    for index, match in enumerate(matches):
        name = marker_name(match)
        if name in result:
            raise ValueError("Duplicate subcategory: " + name)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        category = CATEGORY.search(body)
        if category:
            body = body[:category.start()]
        body = TABLE_END.split(body, maxsplit=1)[0]
        result[name] = normalize(body)
    return result


def categories(text):
    result = {}
    for match in CATEGORY.finditer(text):
        name = marker_name(match)
        if name in result:
            raise ValueError("Duplicate category: " + name)
        next_subcategory = CODE.search(text, match.end())
        if next_subcategory is None or next_subcategory.start() - match.end() >= 1000:
            continue
        result[name] = normalize(text[match.end():next_subcategory.start()])
    return result


def compare_markers(raw, pdf, extractor):
    left, right = extractor(raw), extractor(pdf)
    missing_from_pdf = sorted(left.keys() - right.keys())
    missing_from_raw = sorted(right.keys() - left.keys())
    unequal = sorted(key for key in left.keys() & right.keys() if left[key] != right[key])
    return {
        "raw_count": len(left),
        "pdf_count": len(right),
        "matched_count": len(left.keys() & right.keys()) - len(unequal),
        "missing_from_pdf": missing_from_pdf,
        "missing_from_raw": missing_from_raw,
        "unequal": unequal,
    }


def prose_windows(raw, pdf):
    # The PDF extractor inserts page headers in the middle of prose lines.
    # Remove only that known layout artifact before dehyphenating line wraps.
    pdf = re.sub(
        r"(?m)^Page\s+\d+\s*\nNIST AI 100-1 AI RMF 1\.0\s*\n", "", pdf
    )
    pdf_normalized = normalize(pdf)
    total = 0
    unmatched = []
    for line_number, line in enumerate(raw.splitlines(), 1):
        value = normalize(line)
        if len(value) < 80 or line.lstrip().startswith(("|", "#")):
            continue
        for start in range(0, len(value) - 99, 100):
            total += 1
            if value[start:start + 100] not in pdf_normalized:
                unmatched.append({"raw_line": line_number, "alphanumeric_offset": start})
    return {"window_size": 100, "total": total, "matched": total - len(unmatched),
            "unmatched": unmatched}


def main():
    pdf_sha = digest(PDF)
    raw_sha = digest(RAW)
    supporting_sha = digest(SUPPORTING)
    if (pdf_sha != EXPECTED_PDF_SHA256 or raw_sha != EXPECTED_RAW_SHA256 or
            supporting_sha != EXPECTED_RAW_SHA256):
        raise SystemExit("Pinned source bytes changed; this comparison is not valid")
    raw = RAW.read_text(encoding="utf-8")
    reader = pypdf.PdfReader(str(PDF))
    pdf = "\n".join(page.extract_text() or "" for page in reader.pages)
    result = {
        "schema": "laif.nist-pdf-fidelity.v1",
        "base_commit": "4f58bdb631d2c76836c8fdf48878104c3f49a685",
        "pdf_sha256": pdf_sha,
        "raw_markdown_sha256": raw_sha,
        "assessed_supporting_sha256": supporting_sha,
        "pdf_pages": len(reader.pages),
        "extractor": "pypdf",
        "extractor_version": pypdf.__version__,
        "categories": compare_markers(raw, pdf, categories),
        "subcategories": compare_markers(raw, pdf, subcategories),
        "prose_windows": prose_windows(raw, pdf),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if (result["categories"]["matched_count"] != 19 or
            result["subcategories"]["matched_count"] != 72 or
            result["prose_windows"]["total"] != 585 or
            result["prose_windows"]["unmatched"] != [
                {"raw_line": 113, "alphanumeric_offset": 300},
                {"raw_line": 388, "alphanumeric_offset": 0},
            ]):
        raise SystemExit("Expected source alignment was not reproduced")


if __name__ == "__main__":
    main()
