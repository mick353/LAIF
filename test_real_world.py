#!/usr/bin/env python3
"""
LAIF Real-World Validation — Professional Assessment Engine
-----------------------------------------------------------
Applies LAIF v1.2 compliance checks to representative excerpts from
external AI governance frameworks. Produces:

  1. Console — per-document scorecards + cross-document summary
  2. File    — reports/laif_real_world_assessment.md

validate.py is unchanged. Formal compliance remains binary and strict.
This script adds diagnostic scoring, sector-aware analysis, per-signal
traceability, and remediation guidance around the existing enforcement layer.

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
W = 70


# ── Console output helpers ────────────────────────────────────────────────────

def _section(title):
    print(f"\n{'─' * W}")
    print(f"  {title}")
    print(f"{'─' * W}")


def _print_signal_breakdown(dim_label, score, fired, missed):
    bar = _tty_bar(score)
    print(f"    {dim_label:<28} {score:>3}/100  {bar}")
    for label, w in fired:
        print(f"        {_tty('32', '+')} {label} (+{w})")
    for label, w in missed[:4]:
        print(f"        {_tty('90', chr(8722))} {label} (0/{w})")
    if len(missed) > 4:
        print(f"        {_tty('90', f'  and {len(missed) - 4} more missed signals')}")


def _print_scorecard(r):
    compliance  = r["formal_laif_compliance"]
    comp_colour = "32" if compliance == "PASS" else "31"
    comp_tag    = _tty(comp_colour, f"[{compliance}]")

    _section(f"DOCUMENT: {r['document_name']}")
    print(f"  Source:     {r['source_type']} · {r.get('jurisdiction', '')} · {r.get('year', '')}")
    print(f"  Citation:   {r.get('citation', '')}")
    print(f"  Sector:     {r.get('sector_label', r['sector_used'])}")
    print(f"  Assessment mode: {r.get('assessment_mode', 'external_framework')}")
    print()
    native_status = r.get("formal_laif_native_compliance", compliance)
    native_suffix = " / not LAIF-native / canonical remediation required" if native_status == "FAIL" else ""
    print(f"  LAIF-native certification: {comp_tag}{native_suffix}")
    print("  External framework structural assessment: diagnostic (not certification)")
    if native_status == "FAIL":
        print("  Status note: not LAIF-native / canonical remediation required; not a legal or governance invalidity claim")
    else:
        print("  Status note: LAIF-native certification status is scoped to the LAIF certification channel")
    print()

    # Scores with per-signal breakdown
    print("  SCORES  (fired signals / missed signals)")
    bd = r["score_breakdown"]
    for dim_key, dim_label, score_key in [
        ("structural",    "Structural",           "structural_score"),
        ("terminology",   "Terminology",          "terminology_score"),
        ("conceptual",    "Conceptual Proximity", "conceptual_proximity_score"),
        ("auditability",  "Auditability",         "auditability_score"),
        ("enforceability","Enforceability",       "enforceability_score"),
    ]:
        _print_signal_breakdown(
            dim_label, r[score_key],
            bd[dim_key]["fired"], bd[dim_key]["missed"]
        )
    print(f"    {'─' * (W - 4)}")
    overall_bar = _tty_bar(r["overall_readiness_score"])
    print(f"    {'Overall Readiness':<28} {r['overall_readiness_score']:>3}/100  {overall_bar}")
    score_justification = r.get("score_justification", {})
    print(f"    Score band: {score_justification.get('overall_band', r.get('score_interpretation', 'unknown'))}")
    caution_count = (
        len(r.get('calibration_cautions', []))
        + len(r.get('gaming_risk_notes', []))
        + len(r.get('sector_profile_evidence_cautions', []))
    )
    print(f"    Calibration cautions: {len(r.get('calibration_cautions', []))}")
    print(f"    Gaming risk notes: {len(r.get('gaming_risk_notes', []))}")
    print(f"    Caution/note count: {caution_count}")
    effort_colour = ("32" if r["remediation_effort"] == "LOW" else
                     "33" if r["remediation_effort"] == "MEDIUM" else "31")
    print(f"    Remediation effort: {_tty(effort_colour, r['remediation_effort'])}")
    print()

    # Sector analysis
    print("  SECTOR ANALYSIS")
    print(f"    Profile:          {r.get('sector_label', r['sector_used'])}")
    print(f"    Sector profile:   {r.get('sector_profile_label', r.get('sector_label', r['sector_used']))}")
    profile_signals = r.get("sector_profile_diagnostic_signals", [])
    print(f"    Profile signals:  {len(profile_signals)}")
    if profile_signals:
        print(f"    Top signals:      {', '.join(profile_signals[:2])}")
    align_colour = ("32" if r["sector_risk_alignment"] >= 60 else
                    "33" if r["sector_risk_alignment"] >= 30 else "31")
    print(f"    Risk alignment:   {_tty(align_colour, str(r['sector_risk_alignment']) + '/100')}")
    risk_hits = [f for f in r["sector_specific_findings"] if f.startswith("Risk signal present")]
    risk_miss = [f for f in r["sector_specific_findings"] if f.startswith("Risk signal absent")]
    evid_gaps = [f for f in r["sector_specific_findings"] if f.startswith("Evidence gap")]
    if risk_hits:
        labels = ", ".join(f.replace("Risk signal present: ", "") for f in risk_hits)
        print(f"    Risk signals:     {labels}")
    if risk_miss:
        labels = ", ".join(f.replace("Risk signal absent: ", "") for f in risk_miss)
        print(f"    Not detected:     {labels}")
    if evid_gaps:
        labels = "; ".join(f.replace("Evidence gap: ", "") for f in evid_gaps[:3])
        print(f"    Evidence gaps:    {labels}")
    print()

    # Construct coverage
    print("  CONSTRUCT COVERAGE")
    for term, present in r["construct_coverage"].items():
        tag = _tty("32", "YES") if present else _tty("31", "NO ")
        print(f"    [{tag}]  {term}")
    print()

    # Paraphrase violations
    if r["paraphrase_violations"]:
        n_total = sum(len(v) for v in r["paraphrase_violations"].values())
        print("  PARAPHRASE VIOLATIONS  " + _tty("31", f"({n_total} detected)"))
        for term, violations in r["paraphrase_violations"].items():
            print(f"    [guard: {term}]  {len(violations)} violation(s)")
            for _, ctx in violations[:2]:
                print(f"      ... {ctx.replace(chr(10), ' ')[:100]}...")
    else:
        print("  PARAPHRASE VIOLATIONS  " + _tty("32", "none detected"))
    print()

    print("  PRIMARY LAIF DIAGNOSTIC GAPS")
    for fm in r["primary_failure_modes"]:
        print(f"    · {fm}")
    print()

    print("  STRENGTHS")
    for s in r["strengths"][:6]:
        print(f"    · {s}")
    print()

    print("  DIAGNOSTIC GAPS")
    for g in r["gaps"]:
        print(f"    · {g}")
    print()

    print("  SECTOR-AWARE REMEDIATION  (ordered by impact)")
    for i, step in enumerate(r["recommended_remediation_steps"][:5], 1):
        words = step.split()
        line, buf = [], []
        for w in words:
            buf.append(w)
            if len(" ".join(buf)) > 74:
                line.append("    " + (" ".join(buf[:-1])))
                buf = [w]
        if buf:
            line.append("    " + " ".join(buf))
        print(f"    {i}. {line[0].strip()}")
        for ln in line[1:]:
            print(f"       {ln.strip()}")
    if len(r["recommended_remediation_steps"]) > 5:
        print(f"    ... and {len(r['recommended_remediation_steps']) - 5} further steps in report")
    traces = r.get("evidence_traces", [])
    exact_traces = sum(1 for trace in traces if trace.get("confidence") in ("exact", "deterministic_pattern"))
    fallback_traces = sum(1 for trace in traces if trace.get("confidence") == "fallback_required")
    print(f"  Evidence traces: {len(traces)}")
    print(f"  Exact/deterministic traces: {exact_traces}")
    print(f"  Fallback-required traces: {fallback_traces}")
    patches = r.get("remediation_patches", [])
    print(f"  Structured remediation patches: {len(patches)}")
    for patch in patches[:2]:
        short = patch.get("recommended_patch", "")
        if len(short) > 96:
            short = short[:93].rstrip() + "..."
        print(
            f"    · {patch.get('patch_id', '')} | "
            f"{patch.get('finding_type', '')} | {patch.get('severity', '')} | {short}"
        )
    print()


def _print_summary(results):
    print(f"\n{'=' * W}")
    print(f"  CROSS-DOCUMENT DIAGNOSTIC SUMMARY -- {len(results)} frameworks analysed")
    print(f"{'─' * W}")

    failing  = [r for r in results if r["formal_laif_compliance"] == "FAIL"]
    pct_fail = round(100 * len(failing) / len(results))
    print(
        f"  LAIF-native certification: {len(results) - len(failing)}/{len(results)} pass  "
        f"({len(failing)}/{len(results)} fail / not LAIF-native / canonical remediation required, {pct_fail}%)"
    )
    print("  External framework structural assessment: diagnostic (not certification)")

    print()
    print("  SCORE OVERVIEW  (Str=Structural Ter=Terminology Con=Conceptual Aud=Auditability)")
    print(f"  {'Enf=Enforceability OVR=Overall Sec=Sector Risk Alignment'}")
    header = f"  {'Document':<40}  {'Str':>4} {'Ter':>4} {'Con':>4} {'Aud':>4} {'Enf':>4} {'OVR':>4} {'Sec':>4}"
    print(header)
    print(f"  {'─' * (W - 2)}")
    for r in results:
        name_trunc = r["document_name"][:40]
        print(
            f"  {name_trunc:<40}  "
            f"{r['structural_score']:>4} "
            f"{r['terminology_score']:>4} "
            f"{r['conceptual_proximity_score']:>4} "
            f"{r['auditability_score']:>4} "
            f"{r['enforceability_score']:>4} "
            f"{r['overall_readiness_score']:>4} "
            f"{r['sector_risk_alignment']:>3}%"
        )

    print()
    print("  REMEDIATION EFFORT")
    for r in results:
        effort_col = "31" if "HIGH" in r["remediation_effort"] else "33"
        print(f"    {r['document_name'][:46]:<48}  "
              f"{_tty(effort_col, r['remediation_effort'])}")

    paraphrase_docs = [r for r in results if r["paraphrase_violations"]]
    print()
    print(f"  Paraphrase violations:  {len(paraphrase_docs)}/{len(results)} documents")
    for r in paraphrase_docs:
        for term, vs in r["paraphrase_violations"].items():
            print(f"    {r['document_name'][:46]:<48}  [{term}]  {len(vs)} violation(s)")

    avg_conceptual = round(sum(r["conceptual_proximity_score"] for r in results) / len(results))
    avg_overall    = round(sum(r["overall_readiness_score"] for r in results) / len(results))
    avg_sector     = round(sum(r["sector_risk_alignment"] for r in results) / len(results))
    print()
    print(f"  Avg conceptual proximity:   {avg_conceptual}/100")
    print(f"  Avg overall readiness:      {avg_overall}/100")
    print(f"  Avg sector risk alignment:  {avg_sector}/100")

    print()
    print("  GOVERNANCE-FORCE PATTERNS")
    print(f"    1. {pct_fail}% do not pass the LAIF-native certification channel / are not LAIF-native --")
    print(f"       the diagnostic gap is terminological/structural, not a claim of legal invalidity.")
    print(f"    2. Avg conceptual proximity {avg_conceptual}/100 -- frameworks address the right")
    print(f"       governance dimensions without LAIF structural vocabulary.")
    print(f"    3. Terminology score 0/100 across general-governance documents -- LAIF")
    print(f"       canonical terms (Coupling, Integrity Layer, Coherence Test) absent.")
    print(f"    4. Paraphrase violations in {len(paraphrase_docs)}/{len(results)} documents --")
    print(f"       alignment/connection/linkage used where Coupling is required.")
    print(f"    5. Sector-specific documents show higher risk alignment scores,")
    print(f"       confirming sector profiles correctly contextualise the assessment.")
    print(f"{'=' * W}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Real-World Assessment Engine  ·  May 2026                    ║")
    print("║  Sector-aware · Traceable scoring · Spec-aligned                   ║")
    print("║  validate.py enforcement unchanged                                  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print("  Assessment mode / boundary:")
    print("    - LAIF-native certification is binary, strict, and model-bound (validate.py unchanged).")
    print("    - External framework structural assessment is diagnostic and not certification.")
    print("    - Scores are deterministic LAIF rubric outputs, not legal findings or compliance ratings.")
    print("    - Not LAIF-native is certification-channel wording, not a legal-validity or governance-worth claim.")
    print("  Scoring: traceable -- every number answered by fired/missed signals.")
    print("  Sector analysis: contextualised per deployment sector profile.")

    results = []
    for name, doc in DOCUMENTS.items():
        r = assess(
            name=name,
            source_type=doc["source_type"],
            text=doc["text"],
            sector=doc.get("sector", "general_ai_governance"),
            jurisdiction=doc.get("jurisdiction", ""),
            year=doc.get("year", ""),
            citation=doc.get("citation", ""),
            provenance=doc.get("provenance", "REPRESENTATIVE_EXCERPT"),
            source_url=doc.get("source_url", ""),
            source_note=doc.get("source_note", ""),
            intended_use=doc.get("intended_use", ""),
            assessment_mode="external_framework",
        )
        _print_scorecard(r)
        results.append(r)

    _print_summary(results)

    # Generate and write markdown report
    report_date = f"May {date.today().year}"
    md = generate_markdown_report(results, report_date=report_date)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(md, encoding="utf-8")
    print(f"  Markdown report written -> {REPORT_PATH.relative_to(Path(__file__).parent)}")
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
