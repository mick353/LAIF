#!/usr/bin/env python3
"""Run the two deposited regulatory PDFs through the canonical LAIF processor.

Portable: works in any clone with Python and pypdf installed. This is a
documentary assessment, NOT verified-corpus admission or legal certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "au_dta_policy_v2_1": "Policy for the responsible use of AI in government 2_1_1.pdf",
    "eu_ai_act_amendment_2026_1744": "OJ_L_202601744_EN_TXT.pdf",
}

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="Directory for generated reports; prefer outside public repo")
    parser.add_argument("--source", choices=("all", *SOURCES), default="all")
    args = parser.parse_args(argv)
    try:
        import pypdf  # noqa: F401
    except ImportError:
        print("ERROR: PDF extraction requires pypdf. Install in a virtual environment: python -m pip install pypdf", file=sys.stderr)
        return 2

    out = args.output_dir.expanduser().resolve()
    if out == ROOT or out == ROOT / "docs" or out == ROOT / "reports":
        print("ERROR: select a separate output directory, not a protected repository location", file=sys.stderr)
        return 2
    names = SOURCES if args.source == "all" else {args.source: SOURCES[args.source]}
    results = []
    for key, filename in names.items():
        source = ROOT / "docs" / "verified" / "manual_ingest" / filename
        if not source.is_file():
            print(f"ERROR: missing committed source: {source}", file=sys.stderr)
            return 2
        with source.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                print(f"ERROR: source is not a PDF: {source}", file=sys.stderr)
                return 2
        target = out / key
        cmd = [sys.executable, str(ROOT / "scripts" / "laif_process_document.py"),
               str(source), "--extractor", "pypdf", "--mode", "external_framework",
               "--output-dir", str(target), "--source-type", "uploaded_document"]
        completed = subprocess.run(cmd, cwd=ROOT, check=False)
        record = {"id": key, "repository_path": source.relative_to(ROOT).as_posix(),
                  "source_sha256": sha256(source), "source_bytes": source.stat().st_size,
                  "extractor": "pypdf", "processor_exit_code": completed.returncode,
                  "output_dir": str(target)}
        results.append(record)
        if completed.returncode:
            break
    out.mkdir(parents=True, exist_ok=True)
    summary = {"schema": "laif-regulatory-pdf-run-v1",
               "scope": "documentary assessment only; not legal certification",
               "source_admission": "NOT_PERFORMED",
               "official_upstream_byte_equivalence": "NOT_VERIFIED",
               "human_quote_and_legal_review": "REQUIRED",
               "results": results}
    (out / "run_manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if any(item["processor_exit_code"] != 0 for item in results):
        print("FAIL: assessment processor returned nonzero; see run_manifest.json", file=sys.stderr)
        return 1
    print(f"PASS: documentary processing completed; inspect {out / 'run_manifest.json'} and the generated reports.")
    print("NOT VERIFIED: upstream equivalence, corpus admission, legal conclusions, operational AI safety.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
