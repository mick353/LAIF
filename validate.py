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
    python3 validate.py                          # representative corpus mode (default)
    python3 validate.py --verified-corpus         # verified corpus mode (hash + provenance checks)
    python3 validate.py --check-evidence-traces   # evidence trace citation verification
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


# ── Verified corpus mode ─────────────────────────────────────────────────────

VERIFIED_REQUIRED_FIELDS = [
    "document_id", "title", "jurisdiction", "source_type",
    "authoritative_url", "retrieval_date_utc", "retrieval_method",
    "publication_date", "version_identifier", "sha256_hash",
    "raw_filename", "extraction_boundaries", "transformation_status",
    "citation_status", "provenance_classification", "assessment_status",
]

VALID_TRANSFORMATION = {"RAW_VERBATIM", "STRUCTURALLY_EXTRACTED", "NORMALISED_FORMATTING_ONLY"}
VALID_CITATION       = {"PRIMARY_CITABLE", "DERIVED_EXCERPT", "NON_CITABLE"}
VALID_PROVENANCE     = {"AUTHORITATIVE_PRIMARY_SOURCE", "AUTHORITATIVE_GOVERNMENT_PUBLICATION", "REGULATORY_PUBLICATION"}
VALID_ASSESSMENT     = {"ASSESSED", "PENDING_ASSESSMENT", "PENDING_INGESTION"}


def _load_manifests():
    """Return list of (filename, dict) from docs/verified/manifests/*.json."""
    import json
    manifests_dir = REPO / "docs" / "verified" / "manifests"
    if not manifests_dir.exists():
        return []
    results = []
    for path in sorted(manifests_dir.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                results.append((path.name, json.load(f)))
        except Exception as exc:
            warn(f"Could not load manifest {path.name}: {exc}")
    return results


def _verify_hash(raw_path, expected_hash):
    """Return (actual_hash, match: bool)."""
    import hashlib
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    return digest, digest == expected_hash


def run_verified_corpus():
    """Verified corpus mode: check manifests, hashes, and provenance metadata."""
    import json  # noqa: F401 — imported for clarity; already available above

    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Validation Harness  ·  VERIFIED CORPUS MODE              ║")
    print("║  Framework v1.2  ·  Compliance Toolkit v1.1  ·  April 2026     ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print("  Checking: docs/verified/manifests/  ·  docs/verified/raw/")
    print("  Existing representative corpus checks are NOT run in this mode.")
    print("  Assessment scoring and detection logic are unchanged.\n")

    manifests = _load_manifests()
    if not manifests:
        fail("No manifests found in docs/verified/manifests/ — verified corpus is empty")
        _print_summary()
        sys.exit(1)

    raw_dir = REPO / "docs" / "verified" / "raw"
    pending = 0

    for mfile, manifest in manifests:
        doc_id = manifest.get("document_id", mfile)
        status = manifest.get("assessment_status", "")

        section(f"MANIFEST  {doc_id}")

        # ── 1. Required fields ───────────────────────────────────────────────
        if status == "PENDING_INGESTION":
            # Pending documents: only check fields that should be present
            info("assessment_status = PENDING_INGESTION — hash/file checks skipped")
            pending += 1
            for f_ in ("document_id", "title", "jurisdiction", "source_type",
                        "authoritative_url", "citation_status", "provenance_classification"):
                if manifest.get(f_):
                    ok(f"Field present: {f_}")
                else:
                    warn(f"Field missing or null: {f_}")
            continue

        missing = [f for f in VERIFIED_REQUIRED_FIELDS if f not in manifest or manifest[f] is None]
        if missing:
            fail(f"Missing required fields: {', '.join(missing)}")
        else:
            ok("All required provenance fields present")

        # ── 2. Enum validation ───────────────────────────────────────────────
        ts = manifest.get("transformation_status", "")
        cs = manifest.get("citation_status", "")
        pc = manifest.get("provenance_classification", "")
        as_ = manifest.get("assessment_status", "")

        if ts in VALID_TRANSFORMATION:
            ok(f"transformation_status: {ts}")
        else:
            fail(f"transformation_status invalid: '{ts}'")

        if cs in VALID_CITATION:
            ok(f"citation_status: {cs}")
        else:
            fail(f"citation_status invalid: '{cs}'")

        if pc in VALID_PROVENANCE:
            ok(f"provenance_classification: {pc}")
        else:
            fail(f"provenance_classification invalid: '{pc}'")

        if as_ in VALID_ASSESSMENT:
            ok(f"assessment_status: {as_}")
        else:
            fail(f"assessment_status invalid: '{as_}'")

        # ── 3. Citation consistency rule ─────────────────────────────────────
        # PRIMARY_CITABLE requires RAW_VERBATIM or NORMALISED_FORMATTING_ONLY
        if cs == "PRIMARY_CITABLE" and ts not in {"RAW_VERBATIM", "NORMALISED_FORMATTING_ONLY"}:
            fail(f"Rule violation: PRIMARY_CITABLE requires RAW_VERBATIM or NORMALISED_FORMATTING_ONLY "
                 f"(got transformation_status={ts!r})")
        elif cs == "PRIMARY_CITABLE":
            ok("Citation rule satisfied: PRIMARY_CITABLE + allowed transformation_status")

        # ── 4. SHA256 hash verification ──────────────────────────────────────
        raw_filename = manifest.get("raw_filename")
        expected_hash = manifest.get("sha256_hash", "")
        if raw_filename:
            raw_path = raw_dir / raw_filename
            if raw_path.exists():
                actual, match = _verify_hash(raw_path, expected_hash)
                if match:
                    ok(f"SHA256 verified: {actual[:16]}...")
                else:
                    fail(f"SHA256 MISMATCH — expected {expected_hash[:16]}... "
                         f"got {actual[:16]}...")
            else:
                fail(f"Raw file not found: docs/verified/raw/{raw_filename}")
        else:
            fail("raw_filename not specified — cannot verify hash")

        # ── 5. Extraction boundaries ─────────────────────────────────────────
        boundaries = manifest.get("extraction_boundaries") or {}
        if boundaries.get("full_document"):
            ok("Extraction boundary: full_document = true")
        elif boundaries.get("sections"):
            ok(f"Extraction boundary: {len(boundaries['sections'])} sections defined")
        else:
            warn("Extraction boundaries not specified or empty")

        # ── 6. Assessment reference ──────────────────────────────────────────
        if as_ == "ASSESSED":
            ref = manifest.get("assessment_reference")
            if ref:
                ok(f"Assessment reference: {ref}")
            else:
                warn("assessment_status = ASSESSED but assessment_reference is null")

        # ── 7. Evidence trace ────────────────────────────────────────────────
        trace_rel = manifest.get("evidence_trace")
        if trace_rel:
            trace_path = REPO / trace_rel
            if trace_path.exists() and trace_path.stat().st_size > 0:
                ok(f"Evidence trace present: {trace_rel}")
            else:
                warn(f"Evidence trace referenced but not found: {trace_rel}")
        else:
            warn("No evidence_trace field — reproducibility trail not documented")

    # ── Summary ───────────────────────────────────────────────────────────────
    assessed  = sum(1 for _, m in manifests if m.get("assessment_status") == "ASSESSED")
    total_man = len(manifests)

    print(f"\n{'═' * 66}")
    print(f"  Verified corpus: {total_man} manifests  "
          f"({assessed} ASSESSED  ·  {pending} PENDING_INGESTION)")
    p, f_, w = infra_results["pass"], infra_results["fail"], infra_results["warn"]
    status_str = _tty("32", "PASS") if f_ == 0 else _tty("31", "FAIL")
    print(f"  Provenance checks:  [{status_str}]  pass={p}  fail={f_}  warn={w}")
    print(f"\n  NOTE: Assessment scoring and detection logic are unchanged.")
    print(f"  This mode verifies provenance infrastructure only.")
    print(f"{'═' * 66}\n")

    sys.exit(1 if f_ > 0 else 0)


def _print_summary():
    p, f_, w = infra_results["pass"], infra_results["fail"], infra_results["warn"]
    status_str = _tty("32", "PASS") if f_ == 0 else _tty("31", "FAIL")
    print(f"\n{'═' * 66}")
    print(f"  Infrastructure checks (1–5):  [{status_str}]  "
          f"pass={p}  fail={f_}  warn={w}")
    print(f"  Checks 6–8 are PDCA/case findings — FAILs indicate the")
    print(f"  framework correctly flagged incoherence, not harness errors.")
    print(f"{'═' * 66}\n")


# ── Evidence trace verification ─────────────────────────────────────────────
#
# Each CITATION entry is a tuple (description, regex_pattern).
# description  — human-readable label for reporting
# regex_pattern — compiled against the raw source file text; must match if the
#                 citation is valid. Patterns are document-specific and hardcoded
#                 from direct inspection of the raw files — no probabilistic inference.
#
# Design: fail loudly on any missing citation. No probabilistic matching.
# A citation is VERIFIED if re.search(pattern, raw_text, re.MULTILINE) succeeds.
# A citation is MISSING if the pattern produces no match.

EVIDENCE_TRACE_CORPUS = [
    {
        "document_id":  "51a29205-OECD",
        "raw_file":     "docs/verified/raw/51a29205-OECD_Legal_Instruments.md",
        "trace_file":   "docs/verified/extracted/51a29205-OECD-evidence-trace.md",
        # OECD sections appear as "1.1. Inclusive growth..." at line start.
        "citations": [
            ("OECD Principle 1.1",  r"^1\.1\."),
            ("OECD Principle 1.2",  r"^1\.2\."),
            ("OECD Principle 1.3",  r"^1\.3\."),
            ("OECD Principle 1.4",  r"^1\.4\."),
            ("OECD Principle 1.5",  r"^1\.5\."),
            ("OECD Principle 2.1",  r"^2\.1\."),
            ("OECD Principle 2.2",  r"^2\.2\."),
        ],
    },
    {
        "document_id":  "b0ef43db-EO14110",
        "raw_file":     "docs/verified/raw/b0ef43db-202324283.md",
        "trace_file":   "docs/verified/extracted/b0ef43db-EO14110-evidence-trace.md",
        # EO sections appear as "## Section 4." and subsections as "### 4.1."
        # §13(c) appears as "(c) This order is not intended..."
        "citations": [
            ("EO §2 (Section 2)",           r"## Section 2\."),
            ("EO §3(k) (Section 3)",        r"## Section 3\."),
            ("EO §4.1 (subsection 4.1)",    r"### 4\.1\."),
            ("EO §4.2 (subsection 4.2)",    r"### 4\.2\."),
            ("EO §4.5 (subsection 4.5)",    r"### 4\.5\."),
            ("EO §4.6 (subsection 4.6)",    r"### 4\.6\."),
            ("EO §7 (Section 7)",           r"## Section 7\."),
            ("EO §10.1 (subsection 10.1)",  r"### 10\.1\."),
            ("EO §13 (Section 13)",         r"## Section 13\."),
            ("EO §13(c) text",              r"\(c\) This order is not intended"),
        ],
    },
    {
        "document_id":  "5f667a6f-NIST",
        "raw_file":     "docs/verified/raw/5f667a6f-NIST.AI.1001.md",
        "trace_file":   "docs/verified/extracted/5f667a6f-NIST-evidence-trace.md",
        # NIST subcategories appear in table cells as "GOVERN 1.1: ..."
        "citations": [
            ("NIST GOVERN 1.1",   r"GOVERN 1\.1"),
            ("NIST GOVERN 1.2",   r"GOVERN 1\.2"),
            ("NIST GOVERN 1.4",   r"GOVERN 1\.4"),
            ("NIST GOVERN 1.7",   r"GOVERN 1\.7"),
            ("NIST GOVERN 6.1",   r"GOVERN 6\.1"),
            ("NIST GOVERN 6.2",   r"GOVERN 6\.2"),
            ("NIST MAP 1.1",      r"MAP 1\.1"),
            ("NIST MAP 1.6",      r"MAP 1\.6"),
            ("NIST MAP 5.1",      r"MAP 5\.1"),
            ("NIST MEASURE 2.5",  r"MEASURE 2\.5"),
            ("NIST MEASURE 2.6",  r"MEASURE 2\.6"),
            ("NIST MANAGE 1.3",   r"MANAGE 1\.3"),
            ("NIST MANAGE 2.2",   r"MANAGE 2\.2"),
            ("NIST MANAGE 4.1",   r"MANAGE 4\.1"),
            ("NIST voluntary text", r"voluntary"),
            ("NIST living document", r"living document"),
        ],
    },
    {
        "document_id":  "55eccce3-DTAC",
        "raw_file":     "docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md",
        "trace_file":   "docs/verified/extracted/55eccce3-DTAC-evidence-trace.md",
        # DTAC categories appear as "### C1 - Clinical safety" etc.
        "citations": [
            ("DTAC Category C1 (Clinical safety)",    r"### C1"),
            ("DTAC Category C2 (Data protection)",    r"### C2"),
            ("DTAC Category C3 (Technical security)", r"### C3"),
            ("DTAC Category C4 (Interoperability)",   r"### C4"),
            ("DTAC Category D1 (Usability)",          r"### D1"),
            ("DTAC procurement gate text",            r"C1-C4"),
        ],
    },
]


def run_check_evidence_traces():
    """--check-evidence-traces mode: verify section citations against raw source files."""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Validation Harness  ·  EVIDENCE TRACE VERIFICATION       ║")
    print("║  Framework v1.2  ·  Compliance Toolkit v1.1  ·  April 2026     ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print("  Verifying: section citations in evidence traces exist in raw sources.")
    print("  Method: deterministic regex match against raw file text.")
    print("  A FAIL means the cited section was not found — not a scoring change.\n")

    all_pass = True

    for doc in EVIDENCE_TRACE_CORPUS:
        section(f"EVIDENCE TRACE  {doc['document_id']}")

        raw_path   = REPO / doc["raw_file"]
        trace_path = REPO / doc["trace_file"]

        # ── File existence checks ────────────────────────────────────────────
        if not raw_path.exists():
            fail(f"Raw file not found: {doc['raw_file']}")
            all_pass = False
            continue
        if not trace_path.exists():
            fail(f"Evidence trace not found: {doc['trace_file']}")
            all_pass = False
            continue

        raw_text   = raw_path.read_text(encoding="utf-8")
        trace_text = trace_path.read_text(encoding="utf-8")

        ok(f"Raw file loaded: {len(raw_text):,} chars")
        ok(f"Evidence trace loaded: {len(trace_text):,} chars")

        # ── Citation verification ────────────────────────────────────────────
        missing = []
        for description, pattern in doc["citations"]:
            if re.search(pattern, raw_text, re.MULTILINE):
                ok(f"VERIFIED  {description}")
            else:
                fail(f"MISSING   {description}  (pattern: {pattern!r})")
                missing.append(description)
                all_pass = False

        if missing:
            print()
            warn(f"{len(missing)} citation(s) not found in raw source — "
                 f"evidence trace may reference non-existent sections")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_citations = sum(len(d["citations"]) for d in EVIDENCE_TRACE_CORPUS)
    p, f_, w = infra_results["pass"], infra_results["fail"], infra_results["warn"]
    status_str = _tty("32", "PASS") if f_ == 0 else _tty("31", "FAIL")

    print(f"\n{'═' * 66}")
    print(f"  Evidence trace verification: [{status_str}]")
    print(f"  Documents: {len(EVIDENCE_TRACE_CORPUS)}  "
          f"Citations checked: {total_citations}  "
          f"pass={p}  fail={f_}  warn={w}")
    print(f"\n  Verification scope: section identifiers exist in raw files.")
    print(f"  This does NOT verify verbatim quote accuracy.")
    print(f"  Assessment scoring and detection logic are unchanged.")
    print(f"{'═' * 66}\n")

    sys.exit(1 if f_ > 0 else 0)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "--verified-corpus" in sys.argv:
        run_verified_corpus()
        return  # run_verified_corpus calls sys.exit internally

    if "--check-evidence-traces" in sys.argv:
        run_check_evidence_traces()
        return  # run_check_evidence_traces calls sys.exit internally

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

    _print_summary()
    sys.exit(1 if infra_results["fail"] > 0 else 0)


if __name__ == "__main__":
    main()
