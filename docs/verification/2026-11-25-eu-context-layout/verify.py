#!/usr/bin/env python3
"""Reproduce the text checks for the eight original Act context spans."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "docs/verified/manual_ingest/OJ_L_202401689_EN_TXT.pdf"
RAW = ROOT / "docs/verified/raw/eu_ai_act_2024_1689.md"
TRACE = ROOT / "docs/verification/2026-11-07/regulatory/original_act_substantive_evidence.json"
EXPECTED = {
    "EUO-9": (56, 57),
    "EUO-13": (59, 60),
    "EUO-14": (60, 61),
    "EUO-15": (61, 62),
    "EUO-85": (110, 110),
    "EUO-86": (110, 110),
    "EUO-111-1": (121, 121),
    "EUO-113": (123, 123),
}
ELI = re.escape("ELI: http://data.europa.eu/eli/reg/2024/1689/oj")
FURNITURE = re.compile(
    rf"(?:EN\s+OJ L, 12\.7\.2024|OJ L, 12\.7\.2024\s+EN|"
    rf"\d+/144\s+{ELI}|{ELI}\s+\d+/144)"
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compact(text):
    return "".join(
        "".join(line.split())
        for line in text.splitlines()
        if not FURNITURE.fullmatch(line.strip())
    )


def main():
    pins = {
        PDF: "bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e",
        RAW: "7fb1ae279b6353a9da6bf7dd82218f3cfb2329cc1f9f1512aa269bc4985fe697",
        TRACE: "9ff7e941d64cacd6ab8c7c67736a138c77a1cdb8796c5713104e6d8410b401af",
    }
    inputs = {path: path.read_bytes() for path in pins}
    for path, pin in pins.items():
        if digest(inputs[path]) != pin:
            raise ValueError(f"Input hash changed: {path.relative_to(ROOT)}")

    chunks = re.split(r"<!-- PDF page (\d+) -->\n\n", inputs[RAW].decode("utf-8"))
    numbers = [int(number) for number in chunks[1::2]]
    if numbers != list(range(1, 145)):
        raise ValueError("Expected sequential page markers 1–144")
    pages = dict(zip(numbers, chunks[2::2]))
    traces = json.loads(inputs[TRACE])["traces"]
    if [trace["trace_id"] for trace in traces] != list(EXPECTED):
        raise ValueError("Unexpected trace IDs, duplicates or order")

    for trace in traces:
        key = trace["trace_id"]
        first, last = EXPECTED[key]
        text = trace["matched_text"]
        if (trace["first_pdf_page"], trace["last_pdf_page"]) != (first, last):
            raise ValueError(f"Unexpected page range: {key}")
        if digest(text.encode("utf-8")) != trace["sha256"]:
            raise ValueError(f"Trace hash mismatch: {key}")
        window = compact("\n".join(pages[page] for page in range(first, last + 1)))
        excerpt = compact(text)
        if not excerpt or window.count(excerpt) != 1:
            raise ValueError(f"Expected exactly one match in pages {first}–{last}: {key}")
        print(f"PASS {key}: stored hash and text match on pages {first}–{last}")


if __name__ == "__main__":
    main()
