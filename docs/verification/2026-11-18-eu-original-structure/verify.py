#!/usr/bin/env python3
"""Check the admitted original EU AI Act PDF against its stored page text.

This checks extraction consistency and heading inventory, not legal meaning.
It reads preserved inputs and writes nothing to the corpus.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pypdf


ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "docs/verified/manual_ingest/OJ_L_202401689_EN_TXT.pdf"
RAW = ROOT / "docs/verified/raw/eu_ai_act_2024_1689.md"
PDF_SHA256 = "bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e"
RAW_SHA256 = "7fb1ae279b6353a9da6bf7dd82218f3cfb2329cc1f9f1512aa269bc4985fe697"
PAGE_MARKER = re.compile(r"<!-- PDF page (\d+) -->\n\n")
ARTICLE = re.compile(r"(?m)^Article\s+(\d+)\s*$")
ANNEX = re.compile(r"(?m)^ANNEX\s+([IVX]+)\s*$")
ANNEXES = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(text: str) -> str:
    # Formatting varies between pypdf versions; preserve every non-whitespace
    # character in order. This deliberately does not validate visual layout.
    return re.sub(r"\s+", "", text)


def main() -> None:
    if sha256(PDF.read_bytes()) != PDF_SHA256:
        raise ValueError("Original Official Journal PDF hash changed")
    raw_bytes = RAW.read_bytes()
    if sha256(raw_bytes) != RAW_SHA256:
        raise ValueError("Admitted raw text hash changed")
    raw = raw_bytes.decode("utf-8")
    markers = list(PAGE_MARKER.finditer(raw))
    if not markers or markers[0].start() != 0:
        raise ValueError("Raw text does not begin at PDF page 1")
    page_numbers = [int(marker.group(1)) for marker in markers]
    if page_numbers != list(range(1, 145)):
        raise ValueError("Expected sequential PDF page markers 1–144")
    reader = pypdf.PdfReader(str(PDF))
    if len(reader.pages) != len(markers):
        raise ValueError("PDF page count differs from raw page markers")
    pages: list[str] = []
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(raw)
        raw_page = raw[marker.end():end]
        pdf_page = reader.pages[index].extract_text()
        if not raw_page.strip() or not pdf_page.strip():
            raise ValueError(f"Blank text on PDF page {index + 1}")
        if compact(raw_page) != compact(pdf_page):
            raise ValueError(f"Non-whitespace text mismatch on PDF page {index + 1}")
        pages.append(raw_page)

    # The Annex VIII forms mention Article 49; only the main body counts as
    # the Act's Article heading inventory.
    annex_start = next((i for i, page in enumerate(pages) if ANNEX.search(page)), None)
    if annex_start is None:
        raise ValueError("Annex I heading missing")
    first_annex = ANNEX.search(pages[annex_start])
    body_pages = pages[:annex_start] + [pages[annex_start][:first_annex.start()]]
    articles = [(int(match.group(1)), page_no) for page_no, page in enumerate(body_pages, 1)
                for match in ARTICLE.finditer(page)]
    annexes = [(match.group(1), page_no) for page_no, page in enumerate(pages, 1)
               for match in ANNEX.finditer(page)]
    if [number for number, _ in articles] != list(range(1, 114)):
        raise ValueError("Main-body Article heading inventory is not 1–113 in order")
    if [label for label, _ in annexes] != list(ANNEXES):
        raise ValueError("Annex heading inventory is not I–XIII in order")
    print(json.dumps({
        "status": "PASS",
        "edition": "original OJ L 2024/1689, 12 July 2024",
        "pdf_sha256": PDF_SHA256,
        "raw_sha256": RAW_SHA256,
        "extractor": f"pypdf {pypdf.__version__}",
        "matched_pdf_pages": len(pages),
        "article_headings": len(articles),
        "annex_headings": len(annexes),
        "article_pages": {str(number): page for number, page in articles},
        "annex_pages": {label: page for label, page in annexes},
    }, indent=2))


if __name__ == "__main__":
    main()
