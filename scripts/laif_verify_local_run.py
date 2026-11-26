#!/usr/bin/env python3
"""Verify a saved LAIF document run against its completion receipt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.laif_process_document import ExtractionError, verify_assessment_receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path, help="Saved .laif-run.json alongside the assessment reports")
    parser.add_argument("--source", type=Path, help="Original source document, for an additional byte check")
    args = parser.parse_args(argv)
    try:
        receipt = verify_assessment_receipt(args.receipt, args.source)
    except (OSError, ValueError, ExtractionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"MATCH: {len(receipt['artifacts'])} assessment artifacts")
    if args.source is not None:
        print("MATCH: original source bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
