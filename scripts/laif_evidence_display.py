"""Readable, inert quotations and source locators; no assessment interpretation."""
from __future__ import annotations

import html
import re


def safe_text(value: str) -> str:
    return re.sub(r"([\\`*_{}\[\]()#!|>])", r"\\\1", html.escape(str(value), quote=False))


def blockquote(value: str) -> str:
    # Escape each line: embedded headings, HTML and image links stay source text.
    return "\n".join("> " + safe_text(line) for line in str(value).splitlines())


def anchor(namespace: str, identity: str) -> str:
    return namespace + "-" + re.sub(r"[^a-z0-9-]+", "-", identity.lower()).strip("-")


def evidence_links(ids: list[str], namespace: str) -> str:
    return ", ".join("[" + safe_text(i) + "](#" + anchor(namespace, i) + ")" for i in ids)


def locate(text: str, start: int, end: int) -> dict:
    """Derive display locations from the SAME normalised text as the exact span.

    Page markers and headings are source metadata, not verification of pagination
    against an original PDF. Never convert character counts into page numbers.
    """
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
        raise ValueError("Cannot locate an invalid source span")
    prefix = text[:start]
    sections = list(re.finditer(r"(?m)^#{1,6}[ \t]+(.+?)[ \t]*$", prefix))
    pages = list(re.finditer(r"<!-- PDF page (\d+) -->", text[:end]))
    before = [m for m in pages if m.start() <= start]
    page_numbers = ([int(before[-1].group(1))] if before else []) + [int(m.group(1)) for m in pages if m.start() > start]
    return {"extracted_line": text.count("\n", 0, start) + 1,
            "section": sections[-1].group(1).strip() if sections else None,
            "pdf_page_markers": list(dict.fromkeys(page_numbers))}


def location_label(row: dict) -> str:
    location = row.get("source_location") or {}
    parts = []
    pages = location.get("pdf_page_markers") or []
    if pages:
        parts.append("PDF page marker" + ("s " if len(pages) > 1 else " ") + ", ".join(str(p) for p in pages))
    elif row.get("page"):
        parts.append("PDF page " + str(row["page"]))
    elif row.get("first_pdf_page"):
        parts.append("PDF pages " + str(row["first_pdf_page"]) + "–" + str(row["last_pdf_page"]))
    elif row.get("pdf_page"):
        parts.append("PDF page marker " + str(row["pdf_page"]))
    if row.get("article"):
        parts.append("Article " + str(row["article"]))
    if location.get("section"):
        parts.append("section “" + safe_text(location["section"]) + "”")
    line = location.get("extracted_line") or row.get("extracted_line")
    if line:
        parts.append("extracted-text line " + str(line))
    return "; ".join(parts) or "Location not recorded; quotation reproduced below"


def passage(row: dict, identity: str, namespace: str, *, source: str = "",
            with_anchor: bool = True, display: bool = False) -> list[str]:
    exact = row.get("exact_quote", row.get("matched_text", ""))
    quote = (row.get("display_quote") or exact) if display else exact
    lines = ([f'<a id="{anchor(namespace, identity)}"></a>', ""] if with_anchor else [])
    label = "**" + safe_text(identity) + "** — "
    if source:
        label += safe_text(source) + "; "
    lines += [label + location_label(row), "", blockquote(quote), ""]
    if quote != exact:
        lines += ["Display formatting normalised; the exact extracted text and offsets remain in the evidence JSON.", ""]
    return lines


def locate_review(review: dict | None, text: str) -> None:
    if review:
        for criterion in review["criteria"]:
            for row in criterion["source_excerpts"]:
                row["source_location"] = locate(text, row["start_char"], row["end_char"])
