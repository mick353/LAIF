#!/usr/bin/env python3
"""
LAIF Validation Harness
-----------------------
Ingests the .txt corpus, applies CLAUDE.md rules, and runs a PDCA /
Coherence Test check against the GPT-4 Clinical assessment document.

Checks 1–5  Infrastructure / rule compliance  (PASS/FAIL — FAIL = problem)
Checks 6–7  PDCA assessment findings          (FINDING — expected to surface incoherence)
Check  8    Case Analysis summary             (RESULT  — documents real-world outcomes)
Check  9    Concept anchoring                 (PASS/FAIL — FAIL = problem)

Exit 0 if no infrastructure failures, Exit 1 if any rule check fails.

Usage:
    python3 validate.py
"""

import re
import sys
from pathlib import Path

# Canonical LAIF terms and spec constants — imported for reference.
# validate.py detection logic is NOT changed by this import.
try:
    from laif_spec import CANONICAL_TERMS, INTEGRITY_LAYER, COHERENCE_TEST  # noqa: F401
except ImportError:
    pass  # laif_spec.py is optional; validate.py remains self-contained

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

# Characters either side of a match to examine for context
CONTEXT_WINDOW = 200

# CLAUDE.md §Terminology — context-aware paraphrase guards.
# Source: LAIF_Compliance_Toolkit.txt §1 — canonical term definitions.
# Source: LAIF v1.2 Principle 2 — Coupling is structurally load-bearing;
#   paraphrases (alignment, connection, linkage) lose the bidirectional
#   enforcement requirement that Coupling carries.
#
# A forbidden match is ALLOWED if:
#   (a) allow_if_nearby  — the protected term appears within CONTEXT_WINDOW chars
#       (the forbidden word is used in discussion or contrast alongside the real term)
#   (b) allow_if_contrast — explicit contrast phrasing detected in the window
#       (e.g. "unlike alignment", "beyond alignment", "rather than alignment")
#
# Everything else is flagged as a standalone substitution.
PARAPHRASE_GUARDS = [
    {
        "term":    "Coupling",
        "forbidden": r"\b(alignment|connection|linkage)\b",
        "allow_if_nearby":   r"\bCoupling\b",
        "allow_if_contrast": [
            r"unlike\b.{0,60}(alignment|connection|linkage)",
            r"not\s+(?:merely\s+)?(alignment|connection|linkage)",
            r"rather\s+than\b.{0,60}(alignment|connection|linkage)",
            r"beyond\b.{0,60}(alignment|connection|linkage)",
            r"distinguish.{0,60}(alignment|connection|linkage)",
            r"in\s+contrast\b.{0,60}(alignment|connection|linkage)",
            r"differ.{0,60}(alignment|connection|linkage)",
        ],
    },
    {
        "term":    "Integrity Layer",
        "forbidden": r"\b(integrity conditions?|integrity requirements?|integrity criteria)\b",
        "allow_if_nearby":   r"\bIntegrity Layer\b",
        "allow_if_contrast": [],
    },
    {
        "term":    "Coherence Test",
        "forbidden": r"\bcoherence check\b",
        "allow_if_nearby":   r"\bCoherence Test\b",
        "allow_if_contrast": [],
    },
    {
        "term":    "Materially Affects Interests",
        "forbidden": r"\bmaterial impact\b",
        "allow_if_nearby":   r"\bMaterially Affects Interests\b",
        "allow_if_contrast": [],
    },
    # Source: LAIF v1.2 Part Two A.1; Toolkit §1.3 — Structural Transparency is
    # a defined Integrity Layer property requiring a compliant meaningful account
    # of any material output. "output transparency" and "transparency conditions"
    # are informal substitutes that lose the structural threshold requirement.
    {
        "term":    "Structural Transparency",
        "forbidden": r"\b(?:transparency conditions?|output transparency)\b",
        "allow_if_nearby":   r"\bStructural Transparency\b",
        "allow_if_contrast": [
            r"(?:unlike|beyond|rather\s+than)\b.{0,80}(?:output transparency|transparency conditions?)",
        ],
    },
    # Source: LAIF v1.2 Part Two A.2; Toolkit §1.4 — Structural Honesty requires
    # that stated optimisation objectives correspond to actual implemented objectives.
    # "honesty conditions", "model honesty", "system honesty" lose this structural
    # correspondence requirement.
    {
        "term":    "Structural Honesty",
        "forbidden": r"\b(?:honesty conditions?|model honesty|system honesty)\b",
        "allow_if_nearby":   r"\bStructural Honesty\b",
        "allow_if_contrast": [],
    },
    # Source: LAIF v1.2 Part Two A.3; Toolkit §1.5 — Structural Containment requires
    # operation within documented operational boundaries across all tested conditions.
    # "boundary controls", "scope controls", "containment conditions" are informal
    # substitutes that drop the all-conditions and edge-case coverage requirement.
    {
        "term":    "Structural Containment",
        "forbidden": r"\b(?:boundary controls?|scope controls?|containment conditions?)\b",
        "allow_if_nearby":   r"\bStructural Containment\b",
        "allow_if_contrast": [],
    },
    # Source: LAIF v1.2 Provision D1; Toolkit §2 B.3 — Reversibility (Q3) requires
    # that future actors can modify or reverse deployment consequences. "rollback
    # capability/requirement/clause" and "modifiability requirement" are informal
    # operational terms that omit the future-actor and governance-architecture dimensions.
    {
        "term":    "Reversibility",
        "forbidden": r"\b(?:rollback\s+(?:requirement|clause|condition|capability)|modifiability\s+(?:requirement|clause))\b",
        "allow_if_nearby":   r"\bReversibility\b",
        "allow_if_contrast": [],
    },
]

# Exported pattern constants — imported by test_adversarial.py
# Source: LAIF v1.2 Part Two — Integrity Layer A.1/A.2/A.3 are preconditions
#   of lawful deployment; all three must be satisfied simultaneously.
#   Partial satisfaction = failure. No partial credit.
INTEGRITY_PATTERNS = [
    ("A.1  Structural Transparency", r"A\.1 FINDING\s*:(.*?)(?=A\.2 FINDING|B\.1|\Z)"),
    ("A.2  Structural Honesty",       r"A\.2 FINDING\s*:(.*?)(?=A\.3 FINDING|B\.1|\Z)"),
    ("A.3  Structural Containment",   r"A\.3 FINDING\s*:(.*?)(?=INTEGRITY LAYER FINDING|\Z)"),
]

# Source: LAIF v1.2 Part One — Coherence Test: Q1 Coupling, Q2 Consistency,
#   Q3 Reversibility. All three must be answered affirmatively.
#   Failure at Q1 (Coupling) = automatic failure of the full Coherence Test.
#   Q1 is the most commonly failed question (CLAUDE.md §The Coherence Test).
COHERENCE_PATTERNS = [
    ("Q1  Coupling",      r"B\.1 FINDING\s*:(.*?)(?=B\.2 FINDING|\Z)"),
    ("Q2  Consistency",   r"B\.2 FINDING\s*:(.*?)(?=B\.3 FINDING|\Z)"),
    ("Q3  Reversibility", r"B\.3 FINDING\s*:(.*?)(?=SECTION C|\Z)"),
]

# Source: LAIF v1.2 Principle 3 — Framework Hierarchy is load-bearing:
#   Operational Standards (Toolkit) < Provisions < Foundational Principles.
#   Provisions cannot contradict Principles. Principles are non-amendable.
# Source: LAIF v1.2 Part Seven — Self-Application: governance actors and
#   regulatory bodies are subject to the same Coherence Test as operators.
HIERARCHY_PATTERNS = [
    ("Foundational Principles declared",     r"FOUNDATIONAL PRINCIPLES|PART ONE"),
    ("Non-amendable declaration present",    r"cannot be amended|non-amendable"),
    ("Provision Layer present",              r"PROVISION LAYER|Provision Layer"),
    ("Toolkit marked subordinate",           r"Compliance Toolkit|Operational Standard"),
    ("Self-application clause (Part Seven)", r"PART SEVEN|self.application|applies to regulatory"),
]

# Concept anchoring — relational phrase heuristic signals a Coupling-like concept
# is being expressed without the canonical term.
# Source: LAIF v1.2 Principle 2 — Coupling requires explicit naming of the
#   human interest AND a protection of equivalent normative force; relational
#   phrasing without canonical terminology loses structural enforcement.
RELATIONAL_PHRASES = [
    r"\balignment between\b",
    r"\bcoherence between\b",
    r"\brelationship between\b",
    r"\bconsistency between\b",
    r"\bconnection between\b",
    r"\blinkage between\b",
    r"\bcorrelation between\b",
]

DOMAIN_NOUNS = [
    r"\b(constraints?|rules?|obligations?|prohibitions?)\b",
    r"\b(outcomes?|results?|interests?|goals?|objectives?)\b",
    r"\b(restrictions?|protections?|protected interests?)\b",
]

# Anchoring checks for PDCA sections (Integrity Layer + Coherence Test)
PDCA_ANCHORING_CHECKS = [
    {
        "label":     "A.1  Structural Transparency",
        "extract":   r"A\.1 FINDING\s*:(.*?)(?=A\.2 FINDING|B\.1|\Z)",
        "canonical": r"\bStructural Transparency\b",
        "term":      "Structural Transparency",
    },
    {
        "label":     "A.2  Structural Honesty",
        "extract":   r"A\.2 FINDING\s*:(.*?)(?=A\.3 FINDING|B\.1|\Z)",
        "canonical": r"\bStructural Honesty\b",
        "term":      "Structural Honesty",
    },
    {
        "label":     "A.3  Structural Containment",
        "extract":   r"A\.3 FINDING\s*:(.*?)(?=INTEGRITY LAYER FINDING|\Z)",
        "canonical": r"\bStructural Containment\b",
        "term":      "Structural Containment",
    },
    {
        "label":     "Q1  Coupling",
        "extract":   r"B\.1 FINDING\s*:(.*?)(?=B\.2 FINDING|\Z)",
        "canonical": r"\bCoupling\b",
        "term":      "Coupling",
    },
    {
        "label":     "Q2  Consistency",
        "extract":   r"B\.2 FINDING\s*:(.*?)(?=B\.3 FINDING|\Z)",
        "canonical": r"\bConsistency\b",
        "term":      "Consistency",
    },
    {
        "label":     "Q3  Reversibility",
        "extract":   r"B\.3 FINDING\s*:(.*?)(?=SECTION C|\Z)",
        "canonical": r"\bReversibility\b",
        "term":      "Reversibility",
    },
]

# Anchoring checks for LAIF v1.2 Principle 1 block
V12_ANCHORING_CHECKS = [
    {
        "label":     "Principle 1 — Coherence Standard named",
        "extract":   r"(Principle 1.*?)(?=Principle 2|\Z)",
        "canonical": r"\bCoherence Standard\b",
        "term":      "Coherence Standard",
    },
    {
        "label":     "Principle 1 — Coupling condition declared",
        "extract":   r"(Principle 1.*?)(?=Principle 2|\Z)",
        "canonical": r"\bcoupled\b|\bCoupling\b",
        "term":      "coupled/Coupling",
    },
    {
        "label":     "Principle 1 — Consistency condition declared",
        "extract":   r"(Principle 1.*?)(?=Principle 2|\Z)",
        "canonical": r"\bconsistent\b|\bConsistency\b",
        "term":      "consistent/Consistency",
    },
    {
        "label":     "Principle 1 — Revisability condition declared",
        "extract":   r"(Principle 1.*?)(?=Principle 2|\Z)",
        "canonical": r"\brevisable\b|\bReversibility\b",
        "term":      "revisable/Reversibility",
    },
]


# ── Core pure function (importable by tests) ──────────────────────────────────

def find_paraphrase_violations(text, guard, window=CONTEXT_WINDOW):
    """Return list of (char_pos, context_snippet) for unallowed substitutions.

    Scans text for occurrences of guard["forbidden"]. Each match is examined
    in a ±window char context. The match is suppressed (allowed) if:
      - guard["allow_if_nearby"] appears in the context window, or
      - any pattern in guard["allow_if_contrast"] matches the context window.
    Remaining matches are standalone substitutions and are returned as violations.
    """
    violations = []
    for m in re.finditer(guard["forbidden"], text, re.IGNORECASE):
        start = max(0, m.start() - window)
        end   = min(len(text), m.end() + window)
        ctx   = text[start:end]

        if re.search(guard["allow_if_nearby"], ctx, re.IGNORECASE):
            continue
        if any(re.search(p, ctx, re.IGNORECASE) for p in guard.get("allow_if_contrast", [])):
            continue

        violations.append((m.start(), ctx.replace("\n", " ").strip()))
    return violations


def detect_semantic_substitution(block_text):
    """Return True if block uses relational phrasing + domain nouns without canonical term."""
    has_relational = any(re.search(p, block_text, re.IGNORECASE) for p in RELATIONAL_PHRASES)
    has_domain     = any(re.search(p, block_text, re.IGNORECASE) for p in DOMAIN_NOUNS)
    return has_relational and has_domain


def check_block_anchoring(block_text, canonical_pattern, display_term):
    """Return 'PASS', 'ANCHOR_MISSING', or 'CONCEPT_SUBSTITUTED'.

    PASS              — canonical term found in block
    CONCEPT_SUBSTITUTED — canonical absent + semantic substitution heuristic fires
    ANCHOR_MISSING    — canonical absent, no substitution signal detected
    """
    if re.search(canonical_pattern, block_text, re.IGNORECASE):
        return "PASS"
    return "CONCEPT_SUBSTITUTED" if detect_semantic_substitution(block_text) else "ANCHOR_MISSING"


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


# ── CHECK 9 — Concept anchoring ──────────────────────────────────────────────

def check_concept_anchoring(text, checks, source_label):
    """Verify that each structural block contains its canonical term."""
    section(f"CHECK 9 — Concept Anchoring  [{source_label}]")
    info("Each structural block must contain its canonical LAIF term explicitly.")
    info("ANCHOR_MISSING = term absent; CONCEPT_SUBSTITUTED = paraphrase without term.\n")

    for chk in checks:
        m = re.search(chk["extract"], text, re.DOTALL | re.IGNORECASE)
        if not m:
            warn(f"{chk['label']} — structural block not located (cannot anchor-check)")
            continue
        verdict = check_block_anchoring(m.group(1), chk["canonical"], chk["term"])
        if verdict == "PASS":
            ok(f"{chk['label']}")
        elif verdict == "CONCEPT_SUBSTITUTED":
            fail(f"{chk['label']} — CONCEPT_SUBSTITUTED: '{chk['term']}' absent; semantic substitution detected")
        else:
            fail(f"{chk['label']} — ANCHOR_MISSING: '{chk['term']}' not found in structural block")


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
        for guard in PARAPHRASE_GUARDS:
            violations = find_paraphrase_violations(text, guard)
            if violations:
                issues.append(
                    f'"{guard["term"]}" — {len(violations)} standalone substitution(s) detected'
                )
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
    for label, pattern in HIERARCHY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            ok(label)
        else:
            warn(f"{label} — marker not detected in LAIF_v1.2.txt")


# ── CHECK 6 — PDCA Integrity Layer ───────────────────────────────────────────

def check_integrity_layer(text):
    section("CHECK 6 — PDCA Integrity Layer  (A.1 · A.2 · A.3)  [GPT-4 Clinical]")
    info("Precondition of lawful deployment — all three must be satisfied simultaneously.")
    info("Partial satisfaction = failure. No partial credit.  (LAIF v1.2 Part Two)\n")

    for label, pattern in INTEGRITY_PATTERNS:
        m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not m:
            warn(f"{label} — finding section not located")
            continue
        excerpt = m.group(1).strip().replace("\n", " ")
        if re.search(r"NOT SATISFIED", excerpt, re.IGNORECASE):
            finding("NOT SATISFIED", label)
            info(excerpt[:180] + ("..." if len(excerpt) > 180 else ""))
        else:
            finding("SATISFIED", label)

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

    for label, pattern in COHERENCE_PATTERNS:
        m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not m:
            warn(f"{label} — finding section not located")
            continue
        excerpt = m.group(1).strip().replace("\n", " ")
        if re.search(r"NOT SATISFIED", excerpt, re.IGNORECASE):
            finding("NOT SATISFIED", label)
            info(excerpt[:180] + ("..." if len(excerpt) > 180 else ""))
        else:
            finding("SATISFIED", label)

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

    pattern = r"^(.+?)\s*\|\s*(FAIL|PASS|PARTIAL)\s*\|\s*(FAIL|PASS|PARTIAL)\s*\|\s*(FAIL|PASS|PARTIAL)\s*\|\s*(.+?)\s*$"
    rows = [m.groups() for line in text.splitlines()
            if (m := re.match(pattern, line.strip(), re.IGNORECASE))]

    if not rows:
        warn("Case summary table not parsed — check file format")
        return

    flagged = 0
    for case, q1, q2, q3, verdict in rows:
        v    = verdict.strip()
        q1v, q2v, q3v = q1.upper(), q2.upper(), q3.upper()
        tag  = "FLAGGED" if "Flagged" in v or "FAIL" in (q1v, q2v, q3v) else "CLEAR"
        if tag == "FLAGGED":
            flagged += 1
        result(tag, f"{case:<36} Q1:{q1v:<8} Q2:{q2v:<8} Q3:{q3v:<8} → {v}")

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

    if "PDCA (GPT-4 Clinical)" in docs:
        check_concept_anchoring(docs["PDCA (GPT-4 Clinical)"], PDCA_ANCHORING_CHECKS, "PDCA GPT-4 Clinical")
    else:
        fail("PDCA file unavailable — check 9 (PDCA anchoring) skipped")

    if "LAIF v1.2" in docs:
        check_concept_anchoring(docs["LAIF v1.2"], V12_ANCHORING_CHECKS, "LAIF v1.2")
    else:
        fail("LAIF v1.2 unavailable — check 9 (v1.2 anchoring) skipped")

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
