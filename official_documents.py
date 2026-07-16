#!/usr/bin/env python3
"""
LAIF Assessment — Official Document Corpus
-------------------------------------------
OFFICIAL_EXCERPT corpus entries built by verbatim extraction from the
committed source texts in docs/supporting/. Unlike sample_documents.py
(REPRESENTATIVE_EXCERPT paraphrases), every excerpt here is guaranteed
verbatim BY CONSTRUCTION: the text is sliced out of the source file at
import time using unique start/end markers, then pinned by SHA-256.

Guarantees enforced at import (a violation raises, it does not degrade):
  1. The source file exists in docs/supporting/.
  2. Each start marker occurs exactly once in the source (no ambiguity).
  3. Each excerpt block is an exact contiguous substring of the source.
  4. The SHA-256 of each extracted block matches the pinned hash.

Consequently, results produced from this corpus ARE citable as assessments
of the named source documents — subject to the excerpt scope stated in
each entry's source_note. test_provenance.py re-verifies all of the above
independently.

Where an entry uses multiple non-contiguous blocks, the blocks are joined
with the explicit elision marker "[…]" so the assessed text never silently
splices two passages together.

Provenance fields follow corpus_manifest.md:
  provenance   — always "OFFICIAL_EXCERPT" in this module
  source_url   — canonical URL of the authoritative publication
  source_file  — repo-relative path of the committed verbatim source text
  source_note  — exact excerpt scope and any accuracy caveats
  intended_use — role in the corpus
"""

import hashlib
from pathlib import Path

REPO = Path(__file__).parent


def _extract_block(source_text, start_marker, end_marker, sha256, label):
    """Extract a verbatim block [start_marker .. end_marker] from source_text.

    Raises ValueError on any integrity failure — a corpus that cannot prove
    verbatim provenance must not load as OFFICIAL_EXCERPT.
    """
    n_start = source_text.count(start_marker)
    if n_start == 0:
        raise ValueError(f"{label}: start marker not found in source")
    if n_start > 1:
        raise ValueError(f"{label}: start marker is ambiguous ({n_start} occurrences)")
    i = source_text.find(start_marker)
    j = source_text.find(end_marker, i)
    if j < 0:
        raise ValueError(f"{label}: end marker not found after start marker")
    block = source_text[i:j + len(end_marker)]
    digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
    if digest != sha256:
        raise ValueError(
            f"{label}: SHA-256 mismatch — source file or markers changed since the "
            f"excerpt was pinned (expected {sha256[:12]}…, got {digest[:12]}…). "
            f"Re-verify the excerpt against the authoritative source before re-pinning."
        )
    return block


def _load_official(source_file, blocks):
    """Load and join the verbatim blocks for one corpus entry."""
    path = REPO / source_file
    if not path.exists():
        raise ValueError(f"official corpus source file missing: {source_file}")
    source_text = path.read_text(encoding="utf-8")
    extracted = [
        _extract_block(source_text, b["start"], b["end"], b["sha256"],
                       f"{source_file} block {k + 1}")
        for k, b in enumerate(blocks)
    ]
    return "\n\n[…]\n\n".join(extracted)


# ── Excerpt block specifications ──────────────────────────────────────────────
# Markers are exact substrings of the committed source files. SHA-256 values
# pin the extracted text; any drift in the source file fails the import.

_EO14110_BLOCKS = [
    {   # Section 2 — Policy and Principles (a)–(h), complete
        "start":  "## Section 2. Policy and Principles",
        "end":    "exacerbating inequities, threatening human rights, and causing other harms.",
        "sha256": "15b1745c6c1a452871038a80c460e876b80414ca3eaf4f0bffbcc6c9205d77b3",
    },
    {   # Sections 6 (Supporting Workers) and 7 (Advancing Equity and Civil Rights), complete
        "start":  "## Section 6. Supporting Workers",
        "end":    "the Secretary of Housing and Urban Development shall issue additional guidance.",
        "sha256": "254cc05d146b62435079c57c5f9b747fe4ebcb9726fb17bf861cbef8aa8b25f6",
    },
]

_OECD_BLOCKS = [
    {   # Sections 1 (Principles 1.1–1.5) and 2 (Recommendations 2.1–2.5), complete
        "start":  "Section 1: Principles\nfor responsible stewardship of trustworthy AI",
        "end":    "the evidence base to assess progress in the implementation of these\nprinciples.",
        "sha256": "2767d797d5102afeb14b68f014676b5ffe843cc08109edccd196202001f4d9d4",
    },
]

_NIST_BLOCKS = [
    {   # Part 2 Core: GOVERN function narrative + Table 1, MAP function narrative + Table 2
        "start":  "## Govern\nThe GOVERN function:",
        "end":    "integrating feedback about positive, negative, and unanticipated impacts are in place and documented. |",
        "sha256": "623c77daab39fccc67e56f38035c516d5edbf7fb45134f53e4cd576c9c0963b3",
    },
]

_DTAC_BLOCKS = [
    {   # Introduction — scope, definitions, assessment structure
        "start":  "## Introduction",
        "end":    "provides a scored element to inform choices between products.",
        "sha256": "af9ec43ae77e13073692a313f0c235b46add1c09476934d3571163d23b1f88c9",
    },
    {   # Section C1 — Clinical safety (assessed criteria C1.1.1–C1.2.5, complete)
        "start":  "### C1 - Clinical safety",
        "end":    "hold a current registration with an appropriate professional body relevant to their training and experience. |",
        "sha256": "f0266b3ace5392bd1322c327db2499c1f1d10a22c86f0ef7731e9fa3827f1db9",
    },
]


# ── Official corpus ───────────────────────────────────────────────────────────

OFFICIAL_DOCUMENTS = {

    "US Executive Order 14110 — §2 Principles, §6 Workers, §7 Civil Rights (official text)": {
        "source_type":  "executive_directive",
        "jurisdiction": "United States (Federal)",
        "year":         2023,
        "citation":     "Executive Order 14110, 88 FR 75191 (Nov 1, 2023), FR Doc. 2023-24283",
        "sector":       "general_ai_governance",
        "provenance":   "OFFICIAL_EXCERPT",
        "source_url":   "https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence",
        "source_file":  "docs/supporting/b0ef43db-202324283.md",
        "source_note":  "Verbatim text of Section 2 (Policy and Principles, (a)-(h)), Section 6 "
                        "(Supporting Workers), and Section 7 (Advancing Equity and Civil Rights), "
                        "extracted from the committed Federal Register full text and pinned by "
                        "SHA-256. Non-contiguous sections joined with an explicit […] marker.",
        "intended_use": "citable real-world baseline",
        "blocks":       _EO14110_BLOCKS,
    },

    "OECD Recommendation on AI (OECD/LEGAL/0449) — Sections 1 & 2 (official text)": {
        "source_type":  "international_principles",
        "jurisdiction": "International (OECD member states)",
        "year":         2024,
        "citation":     "OECD Recommendation of the Council on Artificial Intelligence, "
                        "OECD/LEGAL/0449, adopted 22 May 2019, amended 3 May 2024",
        "sector":       "general_ai_governance",
        "provenance":   "OFFICIAL_EXCERPT",
        "source_url":   "https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449",
        "source_file":  "docs/supporting/51a29205-OECD_Legal_Instruments.md",
        "source_note":  "Verbatim text of Section 1 (Principles 1.1-1.5 for responsible "
                        "stewardship of trustworthy AI) and Section 2 (Recommendations 2.1-2.5 "
                        "for national policies), extracted from the committed OECD Legal "
                        "Instruments snapshot (6 May 2026) and pinned by SHA-256. Source "
                        "snapshot preserves the publisher's hard line-wrapping.",
        "intended_use": "citable real-world baseline",
        "blocks":       _OECD_BLOCKS,
    },

    "NIST AI RMF 1.0 (NIST AI 100-1) — GOVERN & MAP Functions (official text)": {
        "source_type":  "voluntary_framework",
        "jurisdiction": "United States",
        "year":         2023,
        "citation":     "NIST AI 100-1, Artificial Intelligence Risk Management Framework "
                        "(AI RMF 1.0), January 2023, https://doi.org/10.6028/NIST.AI.100-1",
        "sector":       "general_ai_governance",
        "provenance":   "OFFICIAL_EXCERPT",
        "source_url":   "https://doi.org/10.6028/NIST.AI.100-1",
        "source_file":  "docs/supporting/5f667a6f-NIST.AI.1001.md",
        "source_note":  "Verbatim text of the Part 2 Core GOVERN function (narrative + Table 1 "
                        "categories/subcategories) and MAP function (narrative + Table 2), "
                        "extracted from the committed NIST AI 100-1 full text and pinned by "
                        "SHA-256. Table text retains the source's markdown table formatting.",
        "intended_use": "citable real-world baseline",
        "blocks":       _NIST_BLOCKS,
    },

    "NHS England DTAC v2.0 (February 2026) — Introduction & C1 Clinical Safety (official text)": {
        "source_type":  "sector_policy",
        "jurisdiction": "United Kingdom",
        "year":         2026,
        "citation":     "Digital Technology Assessment Criteria for Health and Social Care "
                        "(DTAC) v2.0, NHS England, 24 February 2026",
        "sector":       "clinical_ai",
        "provenance":   "OFFICIAL_EXCERPT",
        "source_url":   "https://transform.england.nhs.uk/key-tools-and-info/digital-technology-assessment-criteria-dtac/",
        "source_file":  "docs/supporting/55eccce3-DTAC_Form_2.0_February_2026.md",
        "source_note":  "Verbatim text of the DTAC v2.0 Introduction (scope, definitions, "
                        "assessment structure) and assessed section C1 Clinical safety "
                        "(criteria C1.1.1-C1.2.5 incl. DCB0129 requirements), extracted from "
                        "the committed source text and pinned by SHA-256. Non-contiguous "
                        "sections joined with an explicit […] marker.",
        "intended_use": "citable sector scenario — clinical AI assurance",
        "blocks":       _DTAC_BLOCKS,
    },

}

# Materialise verbatim text for each entry (raises on any integrity failure).
for _name, _doc in OFFICIAL_DOCUMENTS.items():
    _doc["text"] = _load_official(_doc["source_file"], _doc["blocks"])


if __name__ == "__main__":
    import json
    for name, doc in OFFICIAL_DOCUMENTS.items():
        print(f"\n=== {name}")
        print(f"    source_file: {doc['source_file']}")
        for k, b in enumerate(doc["blocks"], 1):
            src = (REPO / doc["source_file"]).read_text(encoding="utf-8")
            i = src.find(b["start"])
            j = src.find(b["end"], i) + len(b["end"])
            block = src[i:j]
            print(f"    block {k}: {len(block)} chars, "
                  f"sha256={hashlib.sha256(block.encode('utf-8')).hexdigest()}")
        print(f"    total text: {len(doc['text'])} chars")
