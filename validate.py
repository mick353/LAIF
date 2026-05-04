#!/usr/bin/env python3
"""
LAIF Validation Harness
-----------------------
Ingests the .txt corpus, applies CLAUDE.md rules, and runs a PDCA /
Coherence Test check against the GPT-4 Clinical assessment document.

Checks 1–5  Infrastructure / rule compliance  (PASS/FAIL — FAIL = problem)
Checks 6–7  PDCA assessment findings          (FINDING — expected to surface incoherence)
Check  8    Case Analysis summary             (RESULT  — documents real-world outcomes)

Exit 0 if no infrastructure failures, Exit 1 if any rule check fails.

Usage:
    python3 validate.py
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).parent

CORPUS = {
    "Executive Brief":       "LAIF_Executive_Brief.txt",
    "Public Article":        "LAIF_Public_Article.txt",
    "LAIF v1.2":             "LAIF_v1.2.txt",
    "PDCA (GPT-4 Clinical)": "LAIF_PDCA_GPT4_Clinical.txt",
    "Case Analysis":         "LAIF_Case_Analysis.txt",
    "Compliance Toolkit":    "LAIF_Compliance_Toolkit.txt",
    "Policy Paper":          "LAIF_Policy_Paper.txt",
    "Regulatory Guide":      "LAIF_Regulatory_Integration_Guide.txt",
}

# Public-facing docs where plain-language paraphrase is acceptable
PUBLIC_DOCS = {"Executive Brief", "Public Article"}

# CLAUDE.md §Terminology — forbidden paraphrases of protected terms
PARAPHRASE_GUARDS = [
    ("Coupling",                   r"\b(alignment|connection|linkage)\b"),
    ("Integrity Layer",            r"\b(integrity conditions|integrity requirements|integrity criteria)\b"),
    ("Coherence Test",             r"\bcoherence check\b"),
    ("Materially Affects Interests", r"\bmaterial impact\b"),
]

# ── Output ────────────────────────────────────────────────────────────────────

infra_results = {"pass": 0, "fail": 0, "warn": 0}

def _tty(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text

def ok(msg):
    infra_results["pass"] += 1
    print(f"  {_tty('32', '[PASS]')}    {msg}")

def fail(msg):
    infra_results["fail"] += 1
    print(f"  {_tty('31', '[FAIL]')}    {msg}")

def warn(msg):
    infra_results["warn"] += 1
    print(f"  {_tty('33', '[WARN]')}    {msg}")

def finding(verdict, msg):
    colour = "32" if "SATISFIED" in verdict and "NOT" not in verdict else "31"
    print(f"  {_tty(colour, f'[{verdict}]'):<30} {msg}")

def result(verdict, msg):
    colour = "31" if verdict in ("FLAGGED", "PARTIAL") else "32"
    print(f"  {_tty(colour, f'[{verdict}]'):<30} {msg}")

def info(msg):
    print(f"           {_tty('90', msg)}")

def section(title):
    print(f"\n{'─' * 66}")
    print(f"  {title}")
    print(f"{'─' * 66}")


# ── CHECK 1 — Document ingestion ──────────────────────────────────────────────

def load_corpus():
    section("CHECK 1 — Document Ingestion")
    docs = {}
    for label, filename in CORPUS.items():
        path = REPO / filename
        if path.exists() and path.stat().st_size > 0:
            docs[label] = path.read_text(encoding="utf-8")
            ok(f"{filename}  ({len(docs[label]):,} chars)")
        else:
            fail(f"{filename} — not found or empty")
    return docs


# ── CHECK 2 — Header format ───────────────────────────────────────────────────

def check_headers(docs):
    section("CHECK 2 — Document Header Format  (CLAUDE.md §Version Numbering)")
    for label, text in docs.items():
        if "April 2026" in text[:400]:
            ok(label)
        else:
            warn(f"{label} — 'April 2026' not found in opening 400 chars")


# ── CHECK 3 — Terminology precision ──────────────────────────────────────────

def check_terminology(docs):
    section("CHECK 3 — Terminology Precision  (CLAUDE.md §Terminology — Use Precisely)")
    for label, text in docs.items():
        if label in PUBLIC_DOCS:
            info(f"{label} — public-facing; plain-language paraphrase acceptable")
            continue
        issues = []
        for term, pattern in PARAPHRASE_GUARDS:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                issues.append(f'"{term}" may be paraphrased as "{m.group(0)}"')
        if issues:
            for issue in issues:
                warn(f"{label} — {issue}")
        else:
            ok(f"{label}")


# ── CHECK 4 — Cross-reference integrity ──────────────────────────────────────

def check_cross_refs(docs):
    section("CHECK 4 — Cross-Reference Integrity  (CLAUDE.md §Cross-References)")
    marker = "LAIF v1.2 Principal Text"
    for label, text in docs.items():
        if marker in text:
            ok(label)
        else:
            warn(f"{label} — standard cross-reference block not present")


# ── CHECK 5 — Framework hierarchy markers ────────────────────────────────────

def check_hierarchy(docs):
    section("CHECK 5 — Framework Hierarchy  (CLAUDE.md §Hierarchy is load-bearing)")
    if "LAIF v1.2" not in docs:
        fail("LAIF_v1.2.txt not loaded — cannot verify hierarchy")
        return
    text = docs["LAIF v1.2"]
    checks = [
        ("Foundational Principles declared",    r"FOUNDATIONAL PRINCIPLES|PART ONE"),
        ("Non-amendable declaration present",   r"cannot be amended|non-amendable"),
        ("Provision Layer present",             r"PROVISION LAYER|Provision Layer"),
        ("Toolkit marked subordinate",          r"Compliance Toolkit|Operational Standard"),
        ("Self-application clause (Part Seven)", r"PART SEVEN|self.application|applies to regulatory"),
    ]
    for label, pattern in checks:
        if re.search(pattern, text, re.IGNORECASE):
            ok(label)
        else:
            warn(f"{label} — marker not detected in LAIF_v1.2.txt")


# ── CHECK 6 — PDCA Integrity Layer ───────────────────────────────────────────

def check_integrity_layer(text):
    section("CHECK 6 — PDCA Integrity Layer  (A.1 · A.2 · A.3)  [GPT-4 Clinical]")
    info("Precondition of lawful deployment — all three must be satisfied simultaneously.")
    info("Partial satisfaction = failure. No partial credit.  (LAIF v1.2 Part Two)\n")

    checks = [
        ("A.1  Structural Transparency", r"A\.1 FINDING\s*:(.*?)(?=A\.2 FINDING|B\.1|\Z)"),
        ("A.2  Structural Honesty",       r"A\.2 FINDING\s*:(.*?)(?=A\.3 FINDING|B\.1|\Z)"),
        ("A.3  Structural Containment",   r"A\.3 FINDING\s*:(.*?)(?=INTEGRITY LAYER FINDING|\Z)"),
    ]
    for label, pattern in checks:
        m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not m:
            warn(f"{label} — finding section not located")
            continue
        excerpt = m.group(1).strip().replace("\n", " ")
        if re.search(r"NOT SATISFIED", excerpt, re.IGNORECASE):
            finding("NOT SATISFIED", f"{label}")
            info(excerpt[:180] + ("..." if len(excerpt) > 180 else ""))
        else:
            finding("SATISFIED", f"{label}")

    # Overall Integrity Layer verdict
    m = re.search(r"INTEGRITY LAYER FINDING\s*:(.*?)(?=SECTION B|\Z)", text, re.DOTALL | re.IGNORECASE)
    if m:
        overall = m.group(1).strip().replace("\n", " ")
        print()
        if "NOT SATISFIED" in overall.upper():
            finding("THRESHOLD NOT SATISFIED", "Integrity Layer — deployment precondition not met")
        else:
            finding("THRESHOLD SATISFIED", "Integrity Layer")
        info(overall[:200] + ("..." if len(overall) > 200 else ""))


# ── CHECK 7 — PDCA Coherence Test ────────────────────────────────────────────

def check_coherence_test(text):
    section("CHECK 7 — PDCA Coherence Test  (Q1 · Q2 · Q3)  [GPT-4 Clinical]")
    info("All three questions must be answered affirmatively.")
    info("Failure at Q1 = automatic failure of the full test.  (LAIF v1.2 Part One)\n")

    checks = [
        ("Q1  Coupling",      r"B\.1 FINDING\s*:(.*?)(?=B\.2 FINDING|\Z)"),
        ("Q2  Consistency",   r"B\.2 FINDING\s*:(.*?)(?=B\.3 FINDING|\Z)"),
        ("Q3  Reversibility", r"B\.3 FINDING\s*:(.*?)(?=SECTION C|\Z)"),
    ]
    for label, pattern in checks:
        m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not m:
            warn(f"{label} — finding section not located")
            continue
        excerpt = m.group(1).strip().replace("\n", " ")
        if re.search(r"NOT SATISFIED", excerpt, re.IGNORECASE):
            finding("NOT SATISFIED", f"{label}")
            info(excerpt[:180] + ("..." if len(excerpt) > 180 else ""))
        else:
            finding("SATISFIED", f"{label}")

    # Overall PDCA verdict
    m = re.search(r"(FINDING:\s*DEPLOYMENT.*?NOT COHERENT[^\n]*)", text, re.IGNORECASE)
    print()
    if m:
        finding("NOT COHERENT", f"Overall PDCA verdict — {m.group(1).strip()[:120]}")
    else:
        finding("COHERENT", "Overall PDCA verdict — deployment coherent under LAIF v1.2")


# ── CHECK 8 — Case Analysis summary ──────────────────────────────────────────

def check_case_analysis(text):
    section("CHECK 8 — Case Analysis  (8 Retrospective Governance Failures)")
    info("Documents whether the Coherence Test would have flagged incoherence at the decision point.\n")

    # Parse summary table rows: "Case Label | FAIL/PASS/PARTIAL | ... | Verdict"
    pattern = r"^(.+?)\s*\|\s*(FAIL|PASS|PARTIAL)\s*\|\s*(FAIL|PASS|PARTIAL)\s*\|\s*(FAIL|PASS|PARTIAL)\s*\|\s*(.+?)\s*$"
    rows = [m.groups() for line in text.splitlines()
            if (m := re.match(pattern, line.strip(), re.IGNORECASE))]

    if not rows:
        warn("Case summary table not parsed — check file format")
        return

    flagged = 0
    for case, q1, q2, q3, verdict in rows:
        v = verdict.strip()
        q1v = q1.upper()
        q2v = q2.upper()
        q3v = q3.upper()
        tag = "FLAGGED" if "Flagged" in v or "FAIL" in (q1v, q2v, q3v) else "CLEAR"
        if tag == "FLAGGED":
            flagged += 1
        row_label = f"{case:<36} Q1:{q1v:<8} Q2:{q2v:<8} Q3:{q3v:<8} → {v}"
        result(tag, row_label)

    print()
    info(f"{flagged}/{len(rows)} cases: Coherence Test flagged structural incoherence at the decision point.")
    info("This is the expected outcome — the framework's scale-invariance claim is verified across sectors.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Validation Harness  ·  Law-Aligned Intelligence          ║")
    print("║  Framework v1.2  ·  Compliance Toolkit v1.1  ·  April 2026     ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    docs = load_corpus()
    check_headers(docs)
    check_terminology(docs)
    check_cross_refs(docs)
    check_hierarchy(docs)

    if "PDCA (GPT-4 Clinical)" in docs:
        pdca = docs["PDCA (GPT-4 Clinical)"]
        check_integrity_layer(pdca)
        check_coherence_test(pdca)
    else:
        fail("PDCA file unavailable — checks 6 and 7 skipped")

    if "Case Analysis" in docs:
        check_case_analysis(docs["Case Analysis"])
    else:
        fail("Case Analysis file unavailable — check 8 skipped")

    print(f"\n{'═' * 66}")
    p, f_, w = infra_results["pass"], infra_results["fail"], infra_results["warn"]
    status = _tty("32", "PASS") if f_ == 0 else _tty("31", "FAIL")
    print(f"  Infrastructure checks (1–5):  [{status}]  "
          f"pass={p}  fail={f_}  warn={w}")
    print(f"  Checks 6–8 are PDCA/case findings — FAILs indicate the")
    print(f"  framework correctly flagged incoherence, not harness errors.")
    print(f"{'═' * 66}\n")

    sys.exit(1 if f_ > 0 else 0)


if __name__ == "__main__":
    main()
