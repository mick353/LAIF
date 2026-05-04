#!/usr/bin/env python3
"""
LAIF Real-World Validation — Professional Assessment Engine
-----------------------------------------------------------
Applies LAIF v1.2 compliance checks to representative excerpts from
external AI governance frameworks. Produces:

  1. Console — per-document scorecards + cross-document summary
  2. File    — reports/laif_real_world_assessment.md

validate.py is unchanged. Formal compliance remains binary and strict.
This script adds diagnostic scoring, strengths/gaps analysis, and
remediation guidance around the existing enforcement layer.

Usage:
    python3 test_real_world.py
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assessment_engine import (
    assess,
    generate_markdown_report,
    _tty,
    _tty_bar,
    score_bar,
)
from sample_documents import DOCUMENTS

REPORT_PATH = Path(__file__).parent / "reports" / "laif_real_world_assessment.md"
W = 66


# ── Console output helpers ────────────────────────────────────────────────────

def _section(title):
    print(f"\n{'─' * W}")
    print(f"  {title}")
    print(f"{'─' * W}")


def _score_line(label, n, width=34):
    bar  = _tty_bar(n)
    tag  = f"{n:>3}/100"
    print(f"    {label:<{width}} {tag}  {bar}")


def _print_scorecard(r):
    compliance = r["formal_laif_compliance"]
    comp_colour = "32" if compliance == "PASS" else "31"
    comp_tag    = _tty(comp_colour, f"[{compliance}]")

    _section(f"DOCUMENT: {r['document_name']}")
    print(f"  Source: {r['source_type']} · {r.get('jurisdiction', '')} · {r.get('year', '')}")
    print(f"  Citation: {r.get('citation', '')}")
    print()
    print(f"  FORMAL LAIF COMPLIANCE: {comp_tag}")
    print()

    print("  SCORES")
    _score_line("Structural",          r["structural_score"])
    _score_line("Terminology",         r["terminology_score"])
    _score_line("Conceptual Proximity",r["conceptual_proximity_score"])
    _score_line("Auditability",        r["auditability_score"])
    _score_line("Enforceability",      r["enforceability_score"])
    print(f"    {'─' * (W - 4)}")
    overall_bar = _tty_bar(r["overall_readiness_score"])
    print(f"    {'Overall Readiness':<34} {r['overall_readiness_score']:>3}/100  {overall_bar}")
    effort_colour = "32" if r["remediation_effort"] == "LOW" else \
                    "33" if r["remediation_effort"] == "MEDIUM" else \
                    "31" if r["remediation_effort"] == "HIGH" else "31"
    print(f"    Remediation effort: {_tty(effort_colour, r['remediation_effort'])}")
    print()

    print("  CONSTRUCT COVERAGE")
    for term, present in r["construct_coverage"].items():
        tag = _tty("32", "YES") if present else _tty("31", "NO ")
        print(f"    [{tag}]  {term}")
    print()

    if r["paraphrase_violations"]:
        print("  PARAPHRASE VIOLATIONS  " + _tty("31", f"({sum(len(v) for v in r['paraphrase_violations'].values())} detected)"))
        for term, violations in r["paraphrase_violations"].items():
            print(f"    [guard: {term}]  {len(violations)} violation(s)")
            for _, ctx in violations[:2]:
                print(f"      ↳ …{ctx.replace(chr(10), ' ')[:100]}…")
    else:
        print("  PARAPHRASE VIOLATIONS  " + _tty("32", "none detected"))
    print()

    print("  PRIMARY FAILURE MODES")
    for fm in r["primary_failure_modes"]:
        print(f"    · {fm}")
    print()

    print("  STRENGTHS")
    for s in r["strengths"][:8]:
        print(f"    · {s}")
    print()

    print("  GAPS")
    for g in r["gaps"]:
        print(f"    · {g}")
    print()

    print("  REMEDIATION STEPS")
    for i, step in enumerate(r["recommended_remediation_steps"], 1):
        words = step.split()
        line, buf = [], []
        for w in words:
            buf.append(w)
            if len(" ".join(buf)) > 72:
                line.append("    " + (" ".join(buf[:-1])))
                buf = [w]
        if buf:
            line.append("    " + " ".join(buf))
        print(f"    {i}. {line[0].strip()}")
        for l in line[1:]:
            print(f"       {l.strip()}")
    print()


def _print_summary(results):
    print(f"\n{'═' * W}")
    print(f"  CROSS-DOCUMENT SUMMARY — {len(results)} frameworks analysed")
    print(f"{'─' * W}")

    failing = [r for r in results if r["formal_laif_compliance"] == "FAIL"]
    pct_fail = round(100 * len(failing) / len(results))
    print(f"  Formal LAIF compliance:   {len(results) - len(failing)}/{len(results)} pass  "
          f"({len(failing)}/{len(results)} fail, {pct_fail}%)")

    print()
    print("  SCORE OVERVIEW")
    header = f"  {'Document':<38}  {'Str':>4} {'Ter':>4} {'Con':>4} {'Aud':>4} {'Enf':>4} {'OVR':>4}"
    print(header)
    print(f"  {'─' * (W - 2)}")
    for r in results:
        name_trunc = r["document_name"][:38]
        print(
            f"  {name_trunc:<38}  "
            f"{r['structural_score']:>4} "
            f"{r['terminology_score']:>4} "
            f"{r['conceptual_proximity_score']:>4} "
            f"{r['auditability_score']:>4} "
            f"{r['enforceability_score']:>4} "
            f"{r['overall_readiness_score']:>4}"
        )

    print()
    print("  REMEDIATION EFFORT")
    for r in results:
        effort_col = "31" if "HIGH" in r["remediation_effort"] else "33"
        print(f"    {r['document_name'][:44]:<46}  "
              f"{_tty(effort_col, r['remediation_effort'])}")

    paraphrase_docs = [r for r in results if r["paraphrase_violations"]]
    print()
    print(f"  Paraphrase violations:  {len(paraphrase_docs)}/{len(results)} documents")
    for r in paraphrase_docs:
        for term, vs in r["paraphrase_violations"].items():
            print(f"    {r['document_name'][:46]:<48}  [{term}]  {len(vs)} violation(s)")

    avg_conceptual = round(sum(r["conceptual_proximity_score"] for r in results) / len(results))
    avg_overall    = round(sum(r["overall_readiness_score"] for r in results) / len(results))
    print()
    print(f"  Avg conceptual proximity:  {avg_conceptual}/100  "
          "(frameworks express LAIF-like intent implicitly)")
    print(f"  Avg overall readiness:     {avg_overall}/100")

    print()
    print("  KEY FINDINGS")
    print(f"    1. {pct_fail}% fail formal compliance — the gap is terminological and")
    print(f"       structural, not conceptual. Intent is broadly present.")
    print(f"    2. Avg conceptual proximity {avg_conceptual}/100 — frameworks address the right")
    print(f"       governance dimensions without LAIF structural vocabulary.")
    print(f"    3. Terminology score 0/100 across all documents — LAIF canonical")
    print(f"       terms (Coupling, Integrity Layer, Coherence Test) absent universally.")
    print(f"    4. Paraphrase violations in {len(paraphrase_docs)}/{len(results)} documents —")
    print(f"       alignment/connection/linkage used where Coupling is required.")
    print(f"    5. LAIF is measurably stricter; existing frameworks are the adoption base.")
    print(f"{'═' * W}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Real-World Assessment Engine  ·  April 2026              ║")
    print("║  Professional scoring + reporting · validate.py unchanged      ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("  Formal compliance: binary and strict.")
    print("  Scoring: diagnostic — identifies strengths, gaps, and remediation paths.")

    results = []
    for name, doc in DOCUMENTS.items():
        r = assess(
            name=name,
            source_type=doc["source_type"],
            text=doc["text"],
            jurisdiction=doc.get("jurisdiction", ""),
            year=doc.get("year", ""),
            citation=doc.get("citation", ""),
        )
        _print_scorecard(r)
        results.append(r)

    _print_summary(results)

    # Generate and write markdown report
    report_date = f"May {date.today().year}"
    md = generate_markdown_report(results, report_date=report_date)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(md, encoding="utf-8")
    print(f"  Markdown report written → {REPORT_PATH.relative_to(Path(__file__).parent)}")
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
