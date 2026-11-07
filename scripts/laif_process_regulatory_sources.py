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
SOURCE_HASHES = {
    "au_dta_policy_v2_1": "7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2",
    "eu_ai_act_amendment_2026_1744": "0bea4d808256b08275777949ba9cb3c70b7d02e4ebb3ac9b205671b1f552d386",
}
RAW_HASHES = {
    "au_dta_policy_v2_1": "3165de723fc222c8e8f86fbd0562a07f930841795f4e83f3de3685f37697f21b",
    "eu_ai_act_amendment_2026_1744": "dfcdbe4c3da4ce06f7b39bade40b4b08c132718352ef70b670ef8f163fb9a5b0",
}
CONTEXT = {
    "au_dta_policy_v2_1": ("Policy for the responsible use of AI in government v2.1", "government_service_delivery", "sector_policy"),
    "eu_ai_act_amendment_2026_1744": ("Regulation (EU) 2026/1744 amending the Artificial Intelligence Act", "general_ai_governance", "binding_regulation"),
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
    parser.add_argument("--verified-text", action="store_true",
                        help="Assess pinned reviewed text extraction with stdlib only, preserving PDF identity in run manifest")
    args = parser.parse_args(argv)
    if not args.verified_text:
        try:
            import pypdf  # noqa: F401
        except ImportError:
            print("ERROR: PDF extraction requires pypdf. Install in a virtual environment: python -m pip install pypdf", file=sys.stderr)
            return 2

    out = args.output_dir.expanduser().resolve()
    if out == ROOT or any(out == ROOT / name or ROOT / name in out.parents
                          for name in ("docs", "reports", ".git")):
        print("ERROR: select an output directory outside repository evidence, reports and Git metadata", file=sys.stderr)
        return 2
    names = SOURCES if args.source == "all" else {args.source: SOURCES[args.source]}
    # Preflight every selected input before producing any outputs. A changed
    # deposit must be explicitly reviewed and repinned, never silently assessed
    # under the old source identity.
    for key, filename in names.items():
        source = ROOT / "docs" / "verified" / "manual_ingest" / filename
        if not source.is_file():
            print(f"ERROR: missing committed source: {source}", file=sys.stderr)
            return 2
        with source.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                print(f"ERROR: source is not a PDF: {source}", file=sys.stderr)
                return 2
        if sha256(source) != SOURCE_HASHES[key]:
            print(f"ERROR: SHA-256 mismatch for pinned source: {source}", file=sys.stderr)
            return 2
        if args.verified_text:
            raw = ROOT / "docs" / "verified" / "raw" / f"{key}.md"
            if not raw.is_file() or sha256(raw) != RAW_HASHES[key]:
                print(f"ERROR: missing or changed reviewed extraction: {raw}", file=sys.stderr)
                return 2
    results = []
    for key, filename in names.items():
        source = ROOT / "docs" / "verified" / "manual_ingest" / filename
        target = out / key
        assessed_input = ROOT / "docs" / "verified" / "raw" / f"{key}.md" if args.verified_text else source
        extractor = "builtin" if args.verified_text else "pypdf"
        cmd = [sys.executable, str(ROOT / "scripts" / "laif_process_document.py"),
               str(assessed_input), "--extractor", extractor, "--mode", "external_framework",
               "--output-dir", str(target), "--source-type", "uploaded_document"]
        title, sector, source_type = CONTEXT[key]
        cmd[-1] = source_type
        cmd.extend(["--document-name", title, "--sector", sector])
        completed = subprocess.run(cmd, cwd=ROOT, check=False)
        record = {"id": key, "repository_path": source.relative_to(ROOT).as_posix(),
                  "source_sha256": sha256(source), "source_bytes": source.stat().st_size,
                  "source_hash_verified": True, "extractor": extractor,
                  "assessed_input_sha256": sha256(assessed_input),
                  "assessed_input": assessed_input.relative_to(ROOT).as_posix(),
                  "processor_exit_code": completed.returncode,
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
