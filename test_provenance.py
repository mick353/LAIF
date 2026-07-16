#!/usr/bin/env python3
"""
LAIF Corpus Provenance Verification
------------------------------------
Machine-enforces the provenance rules in corpus_manifest.md across BOTH
corpus modules. A document's citability claim is only as good as the
weakest check here — so every check failure is a hard failure (exit 1).

GROUP P1 — Official corpus integrity (official_documents.py)
  P1.1  Every entry is classified OFFICIAL_EXCERPT.
  P1.2  The named source_file exists under docs/supporting/.
  P1.3  Every excerpt block is an exact contiguous substring of its source.
  P1.4  Every block's SHA-256 matches the pinned hash (re-computed here,
        independently of the import-time check in official_documents.py).
  P1.5  Entry text equals the blocks joined with the explicit […] marker —
        no silent splicing, no text outside the verified blocks.
  P1.6  Required provenance fields are present and non-empty
        (source_url, source_file, source_note, intended_use, citation).
  P1.7  Excerpt is substantive (≥ 1,000 characters) — a trivial excerpt
        cannot support a citable assessment of the source document.

GROUP P2 — Representative corpus honesty (sample_documents.py)
  P2.1  No entry claims OFFICIAL_EXCERPT (that classification is reserved
        for the marker+hash-verified corpus in official_documents.py).
  P2.2  Every entry carries all four provenance fields, with a valid
        classification code.
  P2.3  Every entry without a source_url declares its illustrative or
        synthetic nature in source_note or citation.

GROUP P3 — Cross-corpus consistency
  P3.1  No document name appears in both corpora.
  P3.2  Combined corpus loads and every entry has assessable text.

Usage:
    python3 test_provenance.py
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from official_documents import OFFICIAL_DOCUMENTS, REPO
from sample_documents import DOCUMENTS
from laif_spec import PROVENANCE_CLASSES

VALID_PROVENANCE = set(PROVENANCE_CLASSES)
JOINER = "\n\n[…]\n\n"
MIN_EXCERPT_CHARS = 1000

passed = 0
failed = 0


def _tty(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def check(ok, check_id, msg):
    global passed, failed
    if ok:
        passed += 1
        print(f"  [{_tty('32', 'PASS')}]  {check_id:<6} {msg}")
    else:
        failed += 1
        print(f"  [{_tty('31', 'FAIL')}]  {check_id:<6} {msg}")


def section(title):
    print(f"\n{'─' * 66}\n  {title}\n{'─' * 66}")


# ── GROUP P1 — Official corpus integrity ──────────────────────────────────────

section("GROUP P1 — Official corpus integrity (official_documents.py)")

for name, doc in OFFICIAL_DOCUMENTS.items():
    short = name[:52]

    check(doc.get("provenance") == "OFFICIAL_EXCERPT",
          "P1.1", f"{short}… classified OFFICIAL_EXCERPT")

    src_path = REPO / doc.get("source_file", "")
    src_ok = doc.get("source_file", "").startswith("docs/supporting/") and src_path.exists()
    check(src_ok, "P1.2", f"{short}… source file exists in docs/supporting/")
    if not src_ok:
        continue

    source_text = src_path.read_text(encoding="utf-8")
    extracted_blocks = []
    for k, b in enumerate(doc["blocks"], 1):
        i = source_text.find(b["start"])
        j = source_text.find(b["end"], i) if i >= 0 else -1
        block = source_text[i:j + len(b["end"])] if (i >= 0 and j >= 0) else None
        substring_ok = block is not None and block in source_text
        check(substring_ok, "P1.3",
              f"{short}… block {k} is a contiguous substring of source")
        if not substring_ok:
            continue
        digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
        check(digest == b["sha256"], "P1.4",
              f"{short}… block {k} SHA-256 matches pinned hash")
        extracted_blocks.append(block)

    check(doc.get("text") == JOINER.join(extracted_blocks),
          "P1.5", f"{short}… text is exactly the verified blocks joined with […]")

    fields_ok = all(str(doc.get(f, "")).strip()
                    for f in ("source_url", "source_file", "source_note",
                              "intended_use", "citation"))
    check(fields_ok, "P1.6", f"{short}… all provenance fields present and non-empty")

    check(len(doc.get("text", "")) >= MIN_EXCERPT_CHARS,
          "P1.7", f"{short}… excerpt is substantive "
                  f"({len(doc.get('text', ''))} chars ≥ {MIN_EXCERPT_CHARS})")


# ── GROUP P2 — Representative corpus honesty ──────────────────────────────────

section("GROUP P2 — Representative corpus honesty (sample_documents.py)")

for name, doc in DOCUMENTS.items():
    short = name[:52]

    check(doc.get("provenance") != "OFFICIAL_EXCERPT",
          "P2.1", f"{short}… does not claim OFFICIAL_EXCERPT")

    has_fields = all(f in doc for f in ("provenance", "source_url",
                                        "source_note", "intended_use"))
    valid_class = doc.get("provenance") in VALID_PROVENANCE
    check(has_fields and valid_class,
          "P2.2", f"{short}… four provenance fields present, classification valid")

    if not doc.get("source_url"):
        declared = any(kw in (doc.get("source_note", "") + doc.get("citation", "")).lower()
                       for kw in ("illustrative", "synthetic", "not an official",
                                  "demonstration"))
        check(declared, "P2.3",
              f"{short}… no source URL → illustrative/synthetic nature declared")


# ── GROUP P3 — Cross-corpus consistency ───────────────────────────────────────

section("GROUP P3 — Cross-corpus consistency")

overlap = set(DOCUMENTS) & set(OFFICIAL_DOCUMENTS)
check(not overlap, "P3.1",
      f"no document name appears in both corpora "
      f"({'overlap: ' + ', '.join(overlap) if overlap else 'disjoint'})")

combined = {**DOCUMENTS, **OFFICIAL_DOCUMENTS}
check(all(isinstance(d.get("text"), str) and d["text"].strip() for d in combined.values()),
      "P3.2", f"combined corpus loads with assessable text ({len(combined)} documents)")


# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'═' * 66}")
if failed == 0:
    print(f"  {_tty('32', 'ALL PROVENANCE CHECKS PASS')}  (pass={passed}, fail=0)")
    print("  OFFICIAL_EXCERPT citability claims are machine-verified.")
else:
    print(f"  {_tty('31', 'PROVENANCE FAILURES')}  (pass={passed}, fail={failed})")
    print("  Citability claims are NOT safe until all checks pass.")
print(f"{'═' * 66}\n")

sys.exit(0 if failed == 0 else 1)
