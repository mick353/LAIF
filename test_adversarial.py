#!/usr/bin/env python3
"""
LAIF Adversarial Test Suite
---------------------------
Injects known violations into synthetic document snippets and verifies the
harness catches them consistently. If every test passes, the harness enforces
its own rules — the framework applies to itself.

Groups:
  A  Paraphrase guard — Coupling vs alignment / connection / linkage
  B  Paraphrase guard — Coherence Test vs 'coherence check'
  C  Paraphrase guard — Integrity Layer vs 'integrity requirements'
  D  Header format — 'April 2026' required in opening 400 chars
  E  Framework hierarchy markers — PART ONE, non-amendable, self-application
  F  PDCA structure — Integrity Layer FINDING sections (A.1–A.3)
  G  PDCA structure — Coherence Test FINDING sections (B.1–B.3)
  H  Cross-layer — full Coupling→alignment substitution throughout PDCA
  I  Concept anchoring — PASS / ANCHOR_MISSING / CONCEPT_SUBSTITUTED
  II Implicit semantic drift — canonical term absent, concept expressed implicitly

  III Fake coupling — term present, structural declaration absent or negated
  IV  Contradiction detection — claimed Integrity Layer properties contradicted
  V   Sector gaming — high keyword density without substantive governance

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
from assessment_engine import assess

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

def expect_flagged(label, text, canonical_pattern, display_term):
    """Boundary test: any non-PASS verdict counts as CAUGHT. PASS = missed detection."""
    verdict = check_block_anchoring(text, canonical_pattern, display_term)
    if verdict != "PASS":
        _counts["caught"] += 1
        _label(f"CAUGHT ({verdict})", "32", label)
    else:
        _counts["missed"] += 1
        _label("MISSED", "31", label, "— implicit substitution not detected")


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


# ── GROUP II — Implicit semantic drift ───────────────────────────────────────

def group_ii():
    section("GROUP II — Implicit semantic drift (no explicit relational phrases)")

    Q1 = PDCA_ANCHORING_CHECKS[3]["canonical"]   # Coupling

    # II-A — Implicit coupling via co-action verbs (no "between")
    expect_flagged(
        "II1  'operate together' — constraints + outcomes, no relational keyword",
        "Outcomes emerge as constraints operate together within the system.",
        Q1, "Coupling",
    )
    expect_flagged(
        "II2  'interacting restrictions' — passive determination phrasing",
        "System behaviour is determined by interacting restrictions.",
        Q1, "Coupling",
    )
    expect_flagged(
        "II3  'jointly govern' — co-action verb without explicit link",
        "Constraints jointly govern resulting states.",
        Q1, "Coupling",
    )
    expect_flagged(
        "II4  'in combination' — combinatory production phrasing",
        "Rules act in combination to produce outcomes.",
        Q1, "Coupling",
    )

    # II-B — Distributed cross-sentence expression
    expect_flagged(
        "II5  split sentences — constraints then outcomes, no linking phrase",
        "Constraints are enforced. These constraints produce consistent outcomes.",
        Q1, "Coupling",
    )
    expect_flagged(
        "II6  obligations → results — two-sentence implicit structure",
        "Obligations are applied. Results follow predictably from those obligations.",
        Q1, "Coupling",
    )

    # II-C — Passive semantic framing
    expect_flagged(
        "II7  'shaped by' — passive causal framing without relational noun",
        "Outcomes are shaped by constraints applied across the system.",
        Q1, "Coupling",
    )
    expect_flagged(
        "II8  'function of' — mathematical framing of constraint→result",
        "System results are a function of enforced restrictions.",
        Q1, "Coupling",
    )

    # II-D — High-level abstraction
    expect_flagged(
        "II9  'coordinated operation' — abstract systemic framing",
        "System integrity arises from the coordinated operation of constraints.",
        Q1, "Coupling",
    )
    expect_flagged(
        "II10 'constraint-driven' — nominalized coupling concept",
        "Predictable behaviour reflects constraint-driven execution.",
        Q1, "Coupling",
    )


# ── GROUP III–V helpers ───────────────────────────────────────────────────────

def info(msg):
    print(f"           \033[90m{msg}\033[0m" if sys.stdout.isatty() else f"           {msg}")

def expect_coupling_quality(label, result, expected_quality):
    """Detect that coupling_quality equals expected_quality."""
    actual = result.get("coupling_quality", "ABSENT")
    if actual == expected_quality:
        _counts["caught"] += 1
        _label(f"CAUGHT ({actual})", "32", label)
    else:
        _counts["missed"] += 1
        _label(f"MISSED (got {actual})", "31", label,
               f"— {result.get('coupling_quality_reason', 'no reason')[:80]}")

def expect_structural_coupling(label, result):
    """Clean case — genuine structural Coupling should return STRUCTURAL."""
    actual = result.get("coupling_quality", "ABSENT")
    if actual == "STRUCTURAL":
        _counts["pass"] += 1
        _label("PASS (STRUCTURAL)", "32", label)
    else:
        _counts["false_positive"] += 1
        _label(f"FALSE+ (got {actual})", "33", label,
               f"— legitimate structural Coupling incorrectly rejected")

def expect_contradiction(label, result, property_name):
    """Contradiction for property_name must be detected."""
    contras = result.get("contradictions", [])
    if any(p == property_name for p, _, _ in contras):
        _counts["caught"] += 1
        _label(f"CAUGHT (contradiction: {property_name})", "32", label)
    else:
        _counts["missed"] += 1
        _label("MISSED", "31", label,
               f"— expected contradiction for {property_name}, none detected")

def expect_no_contradiction(label, result):
    """Clean case — no contradictions should be detected."""
    contras = result.get("contradictions", [])
    if not contras:
        _counts["pass"] += 1
        _label("PASS (no contradictions)", "32", label)
    else:
        _counts["false_positive"] += 1
        _label(f"FALSE+ ({len(contras)} contradiction(s))", "33", label,
               f"— [{contras[0][0]}] {contras[0][1][:60]}")

def expect_gaming_risk(label, result, expected_levels):
    """Gaming risk must be in expected_levels (e.g. ['HIGH', 'MEDIUM'])."""
    actual = result.get("sector_gaming_risk", "LOW")
    if actual in expected_levels:
        _counts["caught"] += 1
        _label(f"CAUGHT (gaming: {actual})", "32", label)
    else:
        _counts["missed"] += 1
        _label(f"MISSED (got {actual})", "31", label,
               f"— {result.get('sector_gaming_reason', '')[:70]}")

def expect_no_gaming(label, result):
    """Clean case — no gaming risk should be detected."""
    actual = result.get("sector_gaming_risk", "LOW")
    if actual == "LOW":
        _counts["pass"] += 1
        _label("PASS (no gaming risk)", "32", label)
    else:
        _counts["false_positive"] += 1
        _label(f"FALSE+ (got {actual})", "33", label,
               f"— {result.get('sector_gaming_reason', '')[:70]}")

def expect_weak_or_hollow(label, result):
    """Structural depth must be WEAK or HOLLOW (not STRONG)."""
    depth = result.get("structural_depth", "WEAK")
    if depth in ("WEAK", "HOLLOW"):
        _counts["caught"] += 1
        _label(f"CAUGHT (depth: {depth})", "32", label)
    else:
        _counts["missed"] += 1
        _label(f"MISSED (got {depth})", "31", label,
               "— hollow/shallow document incorrectly rated STRONG")


# ── GROUP III — Fake Coupling ─────────────────────────────────────────────────

def group_iii():
    """
    GROUP III — Fake Coupling
    Adversarial inputs that include 'Coupling' in non-structural contexts.
    These must be detected as SHALLOW or NEGATED, not STRUCTURAL.

    Protocol Step 3: Failure Design — Fake Coupling
    Source: LAIF v1.2 Principle 2; Toolkit §2 B.1.
    """
    section("GROUP III — Fake Coupling (Principle 2 adversarial)")
    info("Tests that 'Coupling' is used structurally, not rhetorically or negatively.")
    info("SHALLOW/NEGATED = correctly detected; STRUCTURAL = missed detection.\n")

    # III-1: Hollow vocabulary — all formal terms present, Coupling acknowledged only
    r = assess(
        name="III-1",
        source_type="test",
        text=(
            "FOUNDATIONAL PRINCIPLES apply. Cannot be amended. PART ONE: constitutional.\n"
            "PART SEVEN: self-application to regulatory bodies acknowledged.\n"
            "Integrity Layer: noted. Coherence Test: referenced. Coupling: acknowledged.\n"
            "A.1 FINDING: noted. B.1 FINDING: Coupling acknowledged.\n"
        ),
    )
    expect_coupling_quality(
        "III-1 'Coupling: acknowledged' — referential, no structural declaration",
        r, "SHALLOW"
    )
    expect_weak_or_hollow(
        "III-1 structural depth not STRONG despite formal-gate terms present",
        r
    )

    # III-2: Negated Coupling — explicitly declared inapplicable
    r = assess(
        name="III-2",
        source_type="test",
        text=(
            "Following review, Coupling is not applicable to this deployment context "
            "and has been excluded from operational scope. The Coupling requirement was "
            "assessed and deemed outside the scope of this framework."
        ),
    )
    expect_coupling_quality(
        "III-2 'Coupling is not applicable' — explicit negation must be detected",
        r, "NEGATED"
    )

    # III-3: Structural Coupling — genuine declaration (should be STRUCTURAL, clean case)
    r = assess(
        name="III-3",
        source_type="test",
        text=(
            "The Coupling between the data retention restriction (limiting storage to 90 days) "
            "and the patient's specific human interest in privacy and data minimisation is "
            "declared with equivalent normative force. Neither the restriction nor its paired "
            "protection may be weakened in isolation."
        ),
    )
    expect_structural_coupling(
        "III-3 genuine structural Coupling — 'between X and Y, equivalent normative force'",
        r
    )

    # III-4: Referential Coupling — "as defined in LAIF"
    r = assess(
        name="III-4",
        source_type="test",
        text=(
            "Coupling, as defined in LAIF v1.2 Principle 2, has been referenced in this "
            "document. For the definition of Coupling, refer to the LAIF framework. "
            "See also: Coupling in the framework documentation."
        ),
    )
    expect_coupling_quality(
        "III-4 'Coupling as defined in LAIF' — referential, not declared",
        r, "SHALLOW"
    )

    # III-5: Coupling between wrong entities ("between systems", not restriction+interest)
    r = assess(
        name="III-5",
        source_type="test",
        text=(
            "The Coupling between the AI system and the oversight mechanism ensures "
            "coordination. System Coupling is maintained through API integration. "
            "Module Coupling between components is documented in the technical specification."
        ),
    )
    expect_coupling_quality(
        "III-5 'Coupling between systems' — wrong object (should be restriction+human interest)",
        r, "SHALLOW"
    )

    # III-6: Maximum term stuffing — all 8 formal-gate terms present, all hollow.
    # CRITICAL test: formal_laif_compliance = PASS but structural_depth should be HOLLOW.
    r = assess(
        name="III-6",
        source_type="test",
        text=(
            "FOUNDATIONAL PRINCIPLES: noted. Cannot be amended. PART ONE. PART SEVEN: "
            "self-application to regulatory bodies.\n"
            "Coupling: confirmed. Integrity Layer: confirmed. Coherence Test: applied.\n"
            "Non-amendable provisions apply.\n"
            "A.1 FINDING: acknowledged.\n"
            "B.1 FINDING: Coupling noted.\n"
        ),
    )
    # Formal gate passes (all 8 terms present)
    formal = r.get("formal_laif_compliance")
    if formal == "PASS":
        _counts["caught"] += 1
        _label("CAUGHT (formal PASS confirmed)", "32",
               "III-6 formal gate passes — hollow document exploits term-based check")
    else:
        _counts["missed"] += 1
        _label("MISSED", "31",
               "III-6 expected formal PASS on hollow doc, got FAIL")
    # But structural depth must be HOLLOW/WEAK, not STRONG
    expect_weak_or_hollow(
        "III-6 structural depth is WEAK/HOLLOW despite formal PASS — WEAK PASS correctly flagged",
        r
    )
    # And strong compliance must not be STRONG PASS
    sc = r.get("strong_laif_compliance", "FAIL")
    if sc != "STRONG PASS":
        _counts["caught"] += 1
        _label(f"CAUGHT (strong_compliance={sc})", "32",
               "III-6 hollow document correctly denied STRONG PASS")
    else:
        _counts["missed"] += 1
        _label("MISSED", "31",
               "III-6 hollow document incorrectly granted STRONG PASS")


# ── GROUP IV — Contradiction Detection ────────────────────────────────────────

def group_iv():
    """
    GROUP IV — Contradiction Detection
    Documents claiming Integrity Layer properties while contradicting them.
    Source: LAIF v1.2 A.2 Structural Honesty; Toolkit §1.4.
    Protocol Step 3: Failure Design — Surface Transparency / Hidden Irreversibility.
    """
    section("GROUP IV — Contradiction Detection (A.2 Structural Honesty adversarial)")
    info("Claimed properties contradicted by co-present language = structural dishonesty.")
    info("CAUGHT = contradiction detected; MISSED = adversarial input slipped through.\n")

    # IV-1: Reversibility claimed + irreversibility authorised
    r = assess(
        name="IV-1",
        source_type="test",
        text=(
            "Q3 Reversibility is satisfied. The deployment preserves the capacity of "
            "future actors to modify its consequences. "
            "However, once accepted, the AI decision is permanently recorded and cannot "
            "be reversed, appealed, or changed under any circumstances."
        ),
    )
    expect_contradiction(
        "IV-1 Reversibility claimed + 'permanently recorded and cannot be reversed'",
        r, "Reversibility"
    )

    # IV-2: Structural Transparency claimed + non-disclosure
    r = assess(
        name="IV-2",
        source_type="test",
        text=(
            "Structural Transparency: satisfied. The system can produce meaningful "
            "accounts of its outputs on request. "
            "The model architecture and training data are proprietary and cannot be "
            "disclosed to users or regulators under any circumstances."
        ),
    )
    expect_contradiction(
        "IV-2 Structural Transparency + 'proprietary and cannot be disclosed'",
        r, "Structural Transparency"
    )

    # IV-3: Consistency claimed + scale-exclusive carve-out
    r = assess(
        name="IV-3",
        source_type="test",
        text=(
            "Consistency: This governance framework applies consistently. "
            "However, this framework applies only to large enterprise deployments. "
            "Smaller deployments are exempt from these requirements."
        ),
    )
    expect_contradiction(
        "IV-3 Consistency + 'applies only to large deployments; smaller exempt'",
        r, "Consistency"
    )

    # IV-4: Clean document — no contradictions (should produce no false positive)
    r = assess(
        name="IV-4",
        source_type="test",
        text=(
            "Reversibility is maintained: all decisions are subject to human review "
            "and may be reversed through appeal within 30 days. "
            "Structural Transparency: outputs are explainable in plain language on request, "
            "with confidence levels and limitations disclosed. "
            "Consistency: governance applies at all scales."
        ),
    )
    expect_no_contradiction(
        "IV-4 clean document — no contradictions should be detected",
        r
    )


# ── GROUP V — Sector Gaming ───────────────────────────────────────────────────

def group_v():
    """
    GROUP V — Sector Gaming
    Inputs with high sector keyword density but no substantive governance content.
    Source: LAIF v1.2 Q2 Consistency — reasoning must hold at all scales; keyword-
    optimised documents do not satisfy scale-invariant governance logic.
    Protocol Step 3: Failure Design — Sector Gaming.
    """
    section("GROUP V — Sector Gaming (Q2 Consistency adversarial)")
    info("High sector keyword density without governance substance = gaming signal.")
    info("HIGH/MEDIUM gaming risk = correctly detected; LOW = missed.\n")

    # V-1: Clinical keyword stuffing with no governance architecture
    clinical_soup = (
        "This document covers clinical decision support, patient safety, clinical "
        "recommendations, clinical validation, diagnostic outputs, treatment decisions, "
        "physician oversight, clinical audit, adverse events, post-market surveillance, "
        "medical device, SaMD, informed consent, clinical governance, clinical trial, "
        "validation study, performance monitoring, patient consent, patient harm risk. "
        "All clinical AI systems are referenced. Clinical recommendations are acknowledged."
    )
    r = assess(
        name="V-1",
        source_type="test",
        text=clinical_soup,
        sector="clinical_ai",
    )
    expect_gaming_risk(
        "V-1 clinical keyword soup — high sector alignment, near-zero governance content",
        r, ["HIGH", "MEDIUM"]
    )

    # V-2: Employment AI with genuine governance (should NOT be flagged as gaming)
    genuine_employment = (
        "Employers shall notify workers when AI systems are used in employment decisions "
        "affecting them and shall provide a meaningful explanation of the factors used. "
        "Every adverse AI-assisted employment decision shall be subject to mandatory human "
        "review before it takes effect. Workers have the right to request human review. "
        "Employers shall commission an algorithmic fairness audit before deploying any AI "
        "system for hiring or performance assessment decisions. Bias audit results shall "
        "be documented and made available to worker representatives on request. "
        "A designated AI Accountability Officer shall be responsible for compliance. "
        "Records of AI-assisted employment decisions shall be maintained for five years. "
        "Workers facing AI-assisted dismissal shall have the right of appeal before a "
        "human decision-maker with authority to reverse the AI recommendation."
    )
    r = assess(
        name="V-2",
        source_type="test",
        text=genuine_employment,
        sector="employment_ai",
    )
    expect_no_gaming(
        "V-2 genuine employment AI governance — sector alignment with real governance content",
        r
    )

    # V-3: High sector alignment + very low overall (financial keyword stuffing)
    financial_soup = (
        "Credit scoring decision underwriting insurance risk AML fraud detection "
        "algorithmic trading high-frequency regulatory compliance credit assessment "
        "model risk management model validation model governance fair lending fairness "
        "testing bias test explainability XAI systemic risk systemic impact SREP ICAAP "
        "regulatory capital credit decision insurance pricing fraud AML compliance "
        "reporting. Credit scoring models assess insurance underwriting risk."
    )
    r = assess(
        name="V-3",
        source_type="test",
        text=financial_soup,
        sector="financial_services_ai",
    )
    expect_gaming_risk(
        "V-3 financial keyword list — sector signals without governance architecture",
        r, ["HIGH", "MEDIUM"]
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
    group_ii()
    group_iii()
    group_iv()
    group_v()

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
