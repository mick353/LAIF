#!/usr/bin/env python3
"""A small, local first-run guide over LAIF's existing document workflows.

This command does not assess a document itself. It previews extraction, then
calls the existing source evidence or internal diagnostic runner unchanged.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import laif_process_document as processor
from scripts import laif_research_report as research
from scripts import laif_review_session as reviewer

SAMPLE = ROOT / "docs" / "examples" / "vendor-policy.md"
EXTRACTORS = {
    ".txt": "builtin",
    ".md": "builtin",
    ".markdown": "builtin",
    ".docx": "python-docx",
    ".pdf": "pypdf",
}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Preview a local source and choose a clear first LAIF report."
    )
    p.add_argument("source", type=Path, nargs="?", default=SAMPLE,
                   help="authorised .txt, .md, .docx or .pdf file; defaults to the synthetic example")
    p.add_argument("--task", choices=("evidence", "internal"),
                   help="evidence inventory for source review, or interpretive internal diagnostic")
    p.add_argument("--scope", choices=research.SCOPES, default="unknown",
                   help="your declaration of source completeness for the evidence path")
    p.add_argument("--output-dir", type=Path, help="where the chosen runner saves its files")
    p.add_argument("--inspect-only", action="store_true",
                   help="show source and extraction quality without saving a report")
    p.add_argument("--hide-excerpt", action="store_true",
                   help="avoid printing a source passage to the terminal")
    p.add_argument("--yes", action="store_true",
                   help="run without the confirmation prompt after showing the preview")
    p.add_argument("--review-now", action="store_true",
                   help="after generating evidence, enter the source-bound candidate review")
    p.add_argument("--analyst", help="self-reported reviewer name or ID for --review-now")
    return p


def review_command(dossier: Path, source: Path) -> str:
    script = ROOT / "scripts" / "laif_review_session.py"
    if os.name == "nt":
        def quote(value: Path) -> str:
            return "'" + str(value).replace("'", "''") + "'"

        return f"py -3 -X utf8 {quote(script)} {quote(dossier)} {quote(source)}"
    return shlex.join(["python3", str(script), str(dossier), str(source)])


def choose_task(requested: str | None, automatic: bool) -> str:
    if requested:
        return requested
    if automatic:
        return "evidence"
    print("What do you want to do?")
    print("  1. Inspect source evidence and open questions (recommended)")
    print("  2. Generate an interpretive internal diagnostic")
    while True:
        answer = input("Choose 1 or 2 [1]: ").strip()
        if answer in ("", "1"):
            return "evidence"
        if answer == "2":
            return "internal"
        print("Enter 1 or 2.")


def source_preview(source: Path, hide_excerpt: bool) -> tuple[str, str]:
    suffix = source.suffix.lower()
    extractor = EXTRACTORS.get(suffix)
    if extractor is None:
        raise processor.ExtractionError(
            "Supported local formats: .txt, .md, .markdown, .docx and .pdf. "
            "Convert other files to an authorised text copy, then retry."
        )
    result = processor.extract_document(source, extractor)
    digest = processor.sha256_file(source)
    print("\nSource preview")
    print(f"  File: {source}")
    print(f"  SHA-256: {digest}")
    print(f"  Extractor: {result.extractor_used}")
    print(f"  Extracted characters: {len(result.text)}")
    print(f"  Extraction quality marker: {result.extraction_confidence} (format parsing only)")
    if result.warnings:
        for warning in result.warnings:
            print(f"  Warning: {warning}")
    else:
        print("  Extraction warnings: none reported")
    if suffix in (".docx", ".pdf"):
        print("  Check extracted passages against the original; OCR is not performed.")
    if not hide_excerpt:
        # Do not let source-controlled terminal characters alter the prompt.
        excerpt = " ".join(result.text[:360].split())
        excerpt = "".join(ch if ch.isprintable() else " " for ch in excerpt)
        print(f"  Opening text: {excerpt[:300]}{'...' if len(result.text) > 360 else ''}")
    return extractor, digest


def run(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.review_now and (args.task == "internal" or args.inspect_only):
        print("--review-now requires a generated evidence report, not internal or inspection-only mode.",
              file=sys.stderr)
        return 2
    source = args.source.expanduser().resolve()
    task = choose_task(args.task, args.yes or args.inspect_only or args.review_now)
    print("\nLAIF guided start")
    if source == SAMPLE:
        print("Using the included synthetic example; it is a demonstration, not a real case.")
    if task == "evidence":
        print("Task: locate source passages and questions for human review.")
        print("No compliance or safety conclusion is generated by this path.")
    else:
        print("Task: generate an interpretive internal diagnostic for expert review.")
        print("Its scores and proposed controls are not legal or operational findings.")
    try:
        extractor, digest = source_preview(source, args.hide_excerpt)
    except (processor.ExtractionError, OSError, UnicodeError) as exc:
        print(f"Cannot inspect source: {exc}", file=sys.stderr)
        if source.suffix.lower() == ".pdf":
            print("For a text PDF, install pypdf locally; image-only PDFs need separate OCR.",
                  file=sys.stderr)
        elif source.suffix.lower() == ".docx":
            print("For a Word file, install python-docx locally.", file=sys.stderr)
        return 2
    if args.inspect_only:
        print("\nInspection only: no report or processing index written.")
        return 0
    try:
        current_digest = processor.sha256_file(source)
    except OSError as exc:
        print(f"Cannot recheck source after preview: {exc}", file=sys.stderr)
        return 2
    if current_digest != digest:
        print("Source changed after preview; inspect it again before generating a report.",
              file=sys.stderr)
        return 2
    stem = processor.safe_stem(source.stem)
    output_dir = args.output_dir or Path("laif_outputs/guided") / f"{stem}-{digest[:12]}-{task}"
    print(f"\nOutput folder: {output_dir}")
    try:
        if output_dir.exists():
            if not output_dir.is_dir():
                print(f"Output path is not a directory: {output_dir}", file=sys.stderr)
                return 2
            if next(output_dir.iterdir(), None) is not None:
                print(f"Output folder is not empty: {output_dir}", file=sys.stderr)
                print("Choose a fresh --output-dir to preserve every existing file.",
                      file=sys.stderr)
                return 2
    except OSError as exc:
        print(f"Cannot inspect output folder: {exc}", file=sys.stderr)
        return 2
    if not args.yes and input("Save the selected report? [y/N]: ").strip().lower() not in ("y", "yes"):
        print("Stopped before report generation; no report or processing index written.")
        return 0
    call = ([str(source), "--scope", args.scope, "--extractor", extractor,
             "--output-dir", str(output_dir)] if task == "evidence" else
            [str(source), "--mode", "external_framework", "--extractor", extractor,
             "--output-dir", str(output_dir)])
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = research.main(call) if task == "evidence" else processor.main(call)
    print("\n" + output.getvalue().strip())
    if code:
        return code
    print("\nRead and act")
    if task == "evidence":
        print("  1. Open the Research report named above; check every quotation in the original.")
        print("  2. Use the Evidence JSON to inspect source identity, scope and extraction limits.")
        print("  What the document wording supports: candidate passages are exact extracted text;")
        print("    eight criterion labels are provisional rule-based documentary judgments.")
        print("  What remains unestablished: source authority, exceptions, legal effect and whether")
        print("    a stated control operates. NOT_ESTABLISHED means this scan lacked enough wording;")
        print("    it does not prove a safeguard is absent or a rule was breached.")
        print("  What to check next: inspect quoted context; keep, reject or request more")
        print("    evidence for each candidate passage. The saved choice is an operator disposition.")
        print("    An authored substantive criterion review is separate; passage triage")
        print("    does not complete it.")
    else:
        print(f"  1. Open {output_dir / (stem + '.institutional_report.md')} first.")
        print("  2. Follow its evidence links to the quote bank and source context.")
        print("  What the document wording supports: quoted passages and detected patterns;")
        print("    scores, strengths, gaps and controls are interpretive suggestions.")
        print("  What remains unestablished: document authority, legal effect and whether")
        print("    the described controls operate in practice.")
        print("  What to check next: verify source context, review the technical appendix")
        print("    and proposed controls with the responsible owner, and seek operating evidence.")
    print(f"  Source identity for this run: {digest}")
    if task == "evidence":
        dossiers = list(output_dir.glob("*.research_data.json"))
        if len(dossiers) != 1:
            print("Expected exactly one new evidence dossier; review was not started.", file=sys.stderr)
            return 2
        dossier = dossiers[0].resolve()
        print(f"  Resume candidate review: {review_command(dossier, source)}")
        enter_review = args.review_now
        if not args.yes and not enter_review:
            enter_review = input("Review candidate passages now? [y/N]: ").strip().lower() in ("y", "yes")
        if enter_review:
            print("\nCandidate passage review (human triage only)")
            review_args = [str(dossier), str(source)]
            if args.analyst:
                review_args.extend(["--analyst", args.analyst])
            try:
                return reviewer.run(review_args)
            except (KeyboardInterrupt, EOFError):
                print("\nReview stopped; completed passage decisions remain saved.", file=sys.stderr)
                return 2
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    try:
        raise SystemExit(run())
    except (EOFError, KeyboardInterrupt):
        print("\nStopped before report generation.", file=sys.stderr)
        raise SystemExit(2)
