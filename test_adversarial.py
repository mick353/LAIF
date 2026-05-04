#!/usr/bin/env python3
"""
LAIF Adversarial Test Suite
---------------------------
Injects known violations into synthetic document snippets and verifies the
harness catches them consistently. If every test passes, the harness enforces
its own rules — the framework applies to itself.

Groups:
  A  Paraphrase guard — Coupling vs alignment / connection / linkage
     (allow/deny boundary: context-aware distinction)
  B  Paraphrase guard — Coherence Test vs 'coherence check'
  C  Paraphrase guard — Integrity Layer vs 'integrity requirements'
  D  Header format — 'April 2026' required in opening 400 chars
  E  Framework hierarchy markers — PART ONE, non-amendable, self-application
  F  PDCA structure — Integrity Layer FINDING sections (A.1–A.3)
  G  PDCA structure — Coherence Test FINDING sections (B.1–B.3)
  H  Cross-layer — full Coupling→alignment substitution throughout PDCA

Exit 0 if all tests pass, Exit 1 if any are missed or produce false positives.

Usage:
    python3 test_adversarial.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import (
    find_paraphrase_violations,
    PARAPHRASE_GUARDS,
    INTEGRITY_PATTERNS,
    COHERENCE_PATTERNS,
    HIERARCHY_PATTERNS,
    CONTEXT_WINDOW,
    check_block_anchoring,
    detect_semantic_substitution,
    PDCA_ANCHORING_CHECKS,
    V12_ANCHORING_CHECKS,
)

# ── Test runner ───────────────────────────────────────────────────────────────

_counts = {"caught": 0, "missed": 0, "pass": 0, "false_positive": 0}

def _tty(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text

def _label(tag, colour, label, detail=""):
    detail_str = f"  {_tty('90', detail)}" if detail else ""
    print(f"  {_tty(colour, f'[{tag}]'):<28} {label}{detail_str}")

def expect_violation(label, text, guard):
    """Guard must catch at least one violation."""
    v = find_paraphrase_violations(text, guard)
    if v:
        _counts["caught"] += 1
        _label("CAUGHT", "32", label)
    else:
        _counts["missed"] += 1
        _label("MISSED", "31", label, "— expected violation, none detected")

def expect_clean(label, text, guard):
    """Guard must produce no violations (legitimate use)."""
    v = find_paraphrase_violations(text, guard)
    if not v:
        _counts["pass"] += 1
        _label("PASS", "32", label)
    else:
        _counts["false_positive"] += 1
        _label("FALSE+", "33", label, f"— {len(v)} unexpected violation(s): {v[0][1][:70]}")

def expect_pattern_present(label, text, pattern):
    """Regex must match — harness can parse this section."""
    if re.search(pattern, text, re.DOTALL | re.IGNORECASE):
        _counts["pass"] += 1
        _label("FOUND", "32", label)
    else:
        _counts["missed"] += 1
        _label("MISSING", "31", label, "— expected pattern match, none found")

def expect_pattern_absent(label, text, pattern):
    """Regex must not match — harness correctly detects removed/altered section."""
    if not re.search(pattern, text, re.DOTALL | re.IGNORECASE):
        _counts["caught"] += 1
        _label("CAUGHT", "32", label, "— absence correctly detected")
    else:
        _counts["missed"] += 1
        _label("MISSED", "31", label, "— expected no match, but pattern still matches")

def section(title):
    print(f"\n{'─' * 66}")
    print(f"  {title}")
    print(f"{'─' * 66}")


# ── Guards ────────────────────────────────────────────────────────────────────

G_COUPLING  = next(g for g in PARAPHRASE_GUARDS if g["term"] == "Coupling")
G_INTEGRITY = next(g for g in PARAPHRASE_GUARDS if g["term"] == "Integrity Layer")
G_COHERENCE = next(g for g in PARAPHRASE_GUARDS if g["term"] == "Coherence Test")


# ── GROUP A — Coupling guard: allow/deny boundary ────────────────────────────

def group_a():
    section("GROUP A — Coupling guard: allow/deny boundary")

    # --- Should be CAUGHT (standalone substitutions) ---

    expect_violation(
        "A1  'alignment' as standalone descriptor of system behaviour",
        "The deployment ensures structural alignment between restrictions and the "
        "protected interests they serve.",
        G_COUPLING,
    )
    expect_violation(
        "A2  'connection' replacing Coupling in formal governance sentence",
        "There must be a documented connection between the restriction and the "
        "specific human interest it is designed to serve.",
        G_COUPLING,
    )
    expect_violation(
        "A3  'linkage' replacing Coupling as regulatory requirement",
        "A regulatory linkage between the prohibition and the protected interest "
        "is assumed in this framework but is not expressly required.",
        G_COUPLING,
    )
    expect_violation(
        "A4  'alignment' in PDCA-style finding with no Coupling nearby",
        "B.1 FINDING: The alignment between the deployment authorisation and the "
        "patient's interest in accurate documentation is not established.",
        G_COUPLING,
    )

    # --- Should be ALLOWED (legitimate co-occurrence / contrast) ---

    expect_clean(
        "A5  'alignment' co-occurring with Coupling in same window — allowed",
        "The Coupling standard is deliberately distinct from simple alignment: it "
        "requires that neither the restriction nor its paired protection can be "
        "weakened in isolation, a demand alignment-based standards do not impose.",
        G_COUPLING,
    )
    expect_clean(
        "A6  'alignment' in 'unlike ... alignment' contrast phrasing — allowed",
        "Unlike approaches that rely on alignment between system objectives and "
        "outcomes, this framework demands structural coupling between each "
        "restriction and the specific human interest at stake.",
        G_COUPLING,
    )
    expect_clean(
        "A7  'alignment' in 'beyond alignment' contrast phrasing — allowed",
        "Going beyond alignment, LAIF requires that the restriction and its paired "
        "protection be of equivalent normative force — a standard alignment-based "
        "frameworks do not impose.",
        G_COUPLING,
    )
    expect_clean(
        "A8  'alignment' in 'rather than alignment' contrast phrasing — allowed",
        "The framework uses Coupling rather than alignment as its organising "
        "concept because Coupling carries an enforceable structural requirement "
        "that alignment language does not.",
        G_COUPLING,
    )


# ── GROUP B — Coherence Test guard ───────────────────────────────────────────

def group_b():
    section("GROUP B — Coherence Test guard")

    expect_violation(
        "B1  'coherence check' used as standalone substitute for Coherence Test",
        "A coherence check was performed on the deployment documentation prior "
        "to sign-off and no structural issues were identified.",
        G_COHERENCE,
    )
    expect_clean(
        "B2  'coherence check' co-occurring with Coherence Test — allowed",
        "The Coherence Test (earlier drafts referred to this as a coherence check) "
        "requires three affirmative answers; a partial coherence check that omits "
        "Q3 is not compliant.",
        G_COHERENCE,
    )


# ── GROUP C — Integrity Layer guard ──────────────────────────────────────────

def group_c():
    section("GROUP C — Integrity Layer guard")

    expect_violation(
        "C1  'integrity requirements' replacing Integrity Layer as threshold concept",
        "The system must satisfy all integrity requirements before deployment "
        "may proceed. Partial satisfaction is not sufficient.",
        G_INTEGRITY,
    )
    expect_clean(
        "C2  'integrity requirements' alongside Integrity Layer — allowed",
        "The Integrity Layer specifies the integrity requirements that constitute "
        "the precondition of lawful deployment under LAIF v1.2 Part Two.",
        G_INTEGRITY,
    )


# ── GROUP D — Header format ───────────────────────────────────────────────────

def group_d():
    section("GROUP D — Header format: 'April 2026' required in opening 400 chars")

    missing = (
        "LAW-ALIGNED INTELLIGENCE FRAMEWORK\n"
        "Version 1.2\n"
        "A Constitutional Scaffold for AI Governance\n"
        "Incorporates feedback from: EU AI Act · NIST AI RMF · OECD AI Principles\n"
    )
    present = (
        "LAW-ALIGNED INTELLIGENCE FRAMEWORK\n"
        "Version 1.2  |  April 2026\n"
        "A Constitutional Scaffold for AI Governance\n"
    )

    expect_pattern_absent("D1  header missing 'April 2026' — harness must catch", missing[:400], r"April 2026")
    expect_pattern_present("D2  header containing 'April 2026' — harness must pass", present[:400], r"April 2026")


# ── GROUP E — Framework hierarchy markers ────────────────────────────────────

def group_e():
    section("GROUP E — Framework hierarchy markers in LAIF v1.2")

    full = (
        "PART ONE — FOUNDATIONAL PRINCIPLES\n"
        "These principles cannot be amended by any body acting under the authority "
        "this framework confers.\n"
        "PROVISION LAYER\nProvisions are derived from the principles above.\n"
        "Compliance Toolkit v1.1 — Operational Standard — subordinate to Provisions.\n"
        "PART SEVEN — Self-Application: the framework applies to regulatory bodies "
        "and governance actors themselves.\n"
    )

    no_part_one     = full.replace("PART ONE — FOUNDATIONAL PRINCIPLES\n",
                                   "SECTION ONE — PRINCIPLES\n")
    no_non_amendable = full.replace("cannot be amended", "guide the interpretation of")
    no_self_apply   = full.replace(
        "PART SEVEN — Self-Application: the framework applies to regulatory bodies "
        "and governance actors themselves.\n", ""
    )

    _, p_part_one    = HIERARCHY_PATTERNS[0]
    _, p_non_amend   = HIERARCHY_PATTERNS[1]
    _, p_self_apply  = HIERARCHY_PATTERNS[4]

    expect_pattern_present("E1  PART ONE present — harness must pass",          full,            p_part_one)
    expect_pattern_absent( "E2  PART ONE removed — harness must catch",         no_part_one,     p_part_one)
    expect_pattern_present("E3  non-amendable clause present — harness must pass", full,         p_non_amend)
    expect_pattern_absent( "E4  non-amendable clause removed — harness must catch", no_non_amendable, p_non_amend)
    expect_pattern_present("E5  self-application clause present — harness must pass", full,      p_self_apply)
    expect_pattern_absent( "E6  self-application clause removed — harness must catch", no_self_apply, p_self_apply)


# ── GROUP F — PDCA Integrity Layer sections ──────────────────────────────────

def group_f():
    section("GROUP F — PDCA structure: Integrity Layer FINDING sections")

    intact = (
        "SECTION A — INTEGRITY LAYER VERIFICATION\n"
        "A.1  Structural Transparency\n"
        "A.1 FINDING: STRUCTURAL TRANSPARENCY NOT SATISFIED IN ASSESSED CONFIGURATIONS\n"
        "A.2  Structural Honesty\n"
        "A.2 FINDING: STRUCTURAL HONESTY NOT SATISFIED IN ASSESSED CONFIGURATIONS\n"
        "A.3  Structural Containment\n"
        "A.3 FINDING: STRUCTURAL CONTAINMENT NOT SATISFIED IN ASSESSED CONFIGURATIONS\n"
        "INTEGRITY LAYER FINDING: THRESHOLD NOT SATISFIED IN ASSESSED CONFIGURATIONS\n"
        "SECTION B — COHERENCE TEST DOCUMENTATION\n"
    )

    no_a1   = intact.replace("A.1 FINDING: STRUCTURAL TRANSPARENCY NOT SATISFIED IN ASSESSED CONFIGURATIONS\n", "")
    no_a3   = intact.replace("A.3 FINDING: STRUCTURAL CONTAINMENT NOT SATISFIED IN ASSESSED CONFIGURATIONS\n", "")
    no_il   = intact.replace("INTEGRITY LAYER FINDING: THRESHOLD NOT SATISFIED IN ASSESSED CONFIGURATIONS\n", "")

    _, p_a1 = INTEGRITY_PATTERNS[0]
    _, p_a3 = INTEGRITY_PATTERNS[2]
    p_il    = r"INTEGRITY LAYER FINDING\s*:(.*?)(?=SECTION B|\Z)"

    expect_pattern_present("F1  A.1 FINDING present — harness can parse",         intact,  p_a1)
    expect_pattern_absent( "F2  A.1 FINDING removed — harness detects absence",   no_a1,   p_a1)
    expect_pattern_present("F3  A.3 FINDING present — harness can parse",         intact,  p_a3)
    expect_pattern_absent( "F4  A.3 FINDING removed — harness detects absence",   no_a3,   p_a3)
    expect_pattern_present("F5  Integrity Layer overall FINDING present — passes", intact,  p_il)
    expect_pattern_absent( "F6  Integrity Layer overall FINDING removed — caught", no_il,   p_il)


# ── GROUP G — PDCA Coherence Test sections ───────────────────────────────────

def group_g():
    section("GROUP G — PDCA structure: Coherence Test FINDING sections")

    intact = (
        "SECTION B — COHERENCE TEST DOCUMENTATION\n"
        "B.1  Question One — The Coupling Question\n"
        "B.1 FINDING: COUPLING QUESTION NOT SATISFIED\n"
        "B.2  Question Two — The Consistency Question\n"
        "B.2 FINDING: CONSISTENCY QUESTION NOT SATISFIED\n"
        "B.3  Question Three — The Reversibility Question\n"
        "B.3 FINDING: REVERSIBILITY QUESTION NOT SATISFIED\n"
        "SECTION C — PROVISION LAYER COMPLIANCE\n"
    )

    no_b1 = intact.replace("B.1 FINDING: COUPLING QUESTION NOT SATISFIED\n", "")
    no_b2 = intact.replace("B.2 FINDING: CONSISTENCY QUESTION NOT SATISFIED\n", "")
    no_b3 = intact.replace("B.3 FINDING: REVERSIBILITY QUESTION NOT SATISFIED\n", "")

    _, p_b1 = COHERENCE_PATTERNS[0]
    _, p_b2 = COHERENCE_PATTERNS[1]
    _, p_b3 = COHERENCE_PATTERNS[2]

    expect_pattern_present("G1  B.1 FINDING present — harness can parse",         intact, p_b1)
    expect_pattern_absent( "G2  B.1 FINDING removed — harness detects absence",   no_b1,  p_b1)
    expect_pattern_present("G3  B.2 FINDING present — harness can parse",         intact, p_b2)
    expect_pattern_absent( "G4  B.2 FINDING removed — harness detects absence",   no_b2,  p_b2)
    expect_pattern_present("G5  B.3 FINDING present — harness can parse",         intact, p_b3)
    expect_pattern_absent( "G6  B.3 FINDING removed — harness detects absence",   no_b3,  p_b3)


# ── GROUP H — Cross-layer: full Coupling→alignment substitution ──────────────

def group_h():
    section("GROUP H — Cross-layer: 'Coupling' replaced throughout PDCA body")

    # Realistic PDCA fragment with Coupling used correctly
    original = (
        "B.1  Question One — The Coupling Question\n"
        "Coupling requires that the deployment authorisation identify and protect "
        "the specific human interest at risk with equivalent normative force.\n"
        "B.1 FINDING: COUPLING QUESTION NOT SATISFIED\n"
        "The deployment does not satisfy the Coupling requirement. No protection of "
        "equivalent force is paired with the deployment authorisation.\n"
        "B.2  Question Two — The Consistency Question\n"
    )

    # Attacker replaces every instance of Coupling with alignment
    substituted = original.replace("Coupling", "alignment").replace("COUPLING", "ALIGNMENT")

    expect_violation(
        "H1  Coupling replaced with 'alignment' throughout — paraphrase guard catches it",
        substituted,
        G_COUPLING,
    )
    expect_clean(
        "H2  Original text with Coupling intact — guard produces no violations",
        original,
        G_COUPLING,
    )
    # The structural section parser (B.1 FINDING) must still locate the section
    # even after the term substitution — the section label itself is intact
    _, p_b1 = COHERENCE_PATTERNS[0]
    expect_pattern_present(
        "H3  B.1 FINDING structurally present after substitution — parser still finds section",
        substituted,
        p_b1,
    )


# ── GROUP I — Concept anchoring ──────────────────────────────────────────────

def expect_anchor(label, text, canonical_pattern, display_term, expected):
    """check_block_anchoring must return the expected verdict."""
    verdict = check_block_anchoring(text, canonical_pattern, display_term)
    if verdict == expected:
        key = "caught" if expected != "PASS" else "pass"
        _counts[key] += 1
        _label(f"{verdict}", "32", label)
    else:
        key = "missed" if expected != "PASS" else "false_positive"
        _counts[key] += 1
        _label(f"WRONG ({verdict})", "31", label,
               f"— expected {expected}, got {verdict}")


def group_i():
    section("GROUP I — Concept anchoring: check_block_anchoring")

    Q1_CANONICAL = PDCA_ANCHORING_CHECKS[3]["canonical"]   # Coupling
    A1_CANONICAL = PDCA_ANCHORING_CHECKS[0]["canonical"]   # Structural Transparency
    Q2_CANONICAL = PDCA_ANCHORING_CHECKS[4]["canonical"]   # Consistency

    # I1 — canonical term present → PASS
    expect_anchor(
        "I1  'Coupling' explicit in block → PASS",
        "Coupling between constraints and outcomes is established.",
        Q1_CANONICAL, "Coupling", "PASS",
    )

    # I2 — relational phrase + domain noun, canonical absent → CONCEPT_SUBSTITUTED
    expect_anchor(
        "I2  'alignment between constraints and outcomes' → CONCEPT_SUBSTITUTED",
        "There is alignment between constraints and outcomes in this deployment.",
        Q1_CANONICAL, "Coupling", "CONCEPT_SUBSTITUTED",
    )

    # I3 — 'coherence between restrictions and interests' → CONCEPT_SUBSTITUTED
    expect_anchor(
        "I3  'coherence between restrictions and interests' → CONCEPT_SUBSTITUTED",
        "The assessment confirms coherence between restrictions and protected interests.",
        Q1_CANONICAL, "Coupling", "CONCEPT_SUBSTITUTED",
    )

    # I4 — 'consistent relationship between restrictions and results' → CONCEPT_SUBSTITUTED
    expect_anchor(
        "I4  'consistent relationship between restrictions and results' → CONCEPT_SUBSTITUTED",
        "A consistent relationship between restrictions and results was observed.",
        Q1_CANONICAL, "Coupling", "CONCEPT_SUBSTITUTED",
    )

    # I5 — contrast phrasing with canonical present → PASS (canonical appears → PASS)
    expect_anchor(
        "I5  'Unlike alignment, LAIF requires Coupling' → PASS",
        "Unlike alignment, LAIF requires Coupling between constraints and outcomes.",
        Q1_CANONICAL, "Coupling", "PASS",
    )

    # I6 — Structural Transparency named explicitly → PASS
    expect_anchor(
        "I6  'Structural Transparency is not satisfied' → PASS",
        "Structural Transparency is not satisfied in the assessed configuration.",
        A1_CANONICAL, "Structural Transparency", "PASS",
    )

    # I7 — Transparency concept via relational phrase, canonical absent → CONCEPT_SUBSTITUTED
    expect_anchor(
        "I7  Transparency as 'correlation between outputs and their basis' → CONCEPT_SUBSTITUTED",
        "There is an insufficient correlation between outputs and their objectives "
        "in the clinical deployment configuration.",
        A1_CANONICAL, "Structural Transparency", "CONCEPT_SUBSTITUTED",
    )

    # I8 — Consistency named explicitly → PASS
    expect_anchor(
        "I8  'The Consistency requirement is not satisfied' → PASS",
        "The Consistency requirement is not satisfied at this scale of deployment.",
        Q2_CANONICAL, "Consistency", "PASS",
    )

    # I9 — Consistency block, no term, no relational pattern → ANCHOR_MISSING
    expect_anchor(
        "I9  Vague block with no term and no relational pattern → ANCHOR_MISSING",
        "The deployment was assessed under the second question of the test. "
        "Results were inconclusive.",
        Q2_CANONICAL, "Consistency", "ANCHOR_MISSING",
    )

    # I10 — completely empty / irrelevant block → ANCHOR_MISSING
    expect_anchor(
        "I10 Empty block → ANCHOR_MISSING",
        "No information recorded.",
        Q1_CANONICAL, "Coupling", "ANCHOR_MISSING",
    )


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Adversarial Test Suite  ·  April 2026                    ║")
    print("║  Injects violations — verifies the harness catches them        ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    group_a()
    group_b()
    group_c()
    group_d()
    group_e()
    group_f()
    group_g()
    group_h()
    group_i()

    caught = _counts["caught"]
    passed = _counts["pass"]
    missed = _counts["missed"]
    false_pos = _counts["false_positive"]
    total = caught + passed + missed + false_pos
    bad = missed + false_pos

    print(f"\n{'═' * 66}")
    status = _tty("32", "ALL TESTS PASS") if bad == 0 else _tty("31", "FAILURES DETECTED")
    print(f"  {status}  ({total} tests)")
    print(f"  Violations caught : {caught}  |  Clean passes   : {passed}")
    if bad:
        print(f"  Missed violations : {missed}  |  False positives : {false_pos}")
    print(f"{'═' * 66}\n")

    sys.exit(1 if bad > 0 else 0)


if __name__ == "__main__":
    main()
