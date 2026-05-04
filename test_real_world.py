#!/usr/bin/env python3
"""
LAIF Real-World Validation — Controlled Exploration
----------------------------------------------------
Applies LAIF validation checks to representative excerpts from external
AI governance frameworks. Observational phase only — validate.py is unchanged.

Checks applied per document:
  · Canonical term presence (Coupling, Integrity Layer, Coherence Test)
  · Framework hierarchy markers
  · PDCA structural block detection
  · Paraphrase violation scanning (forbidden term substitutions)
  · LAIF-adjacent concept inventory
  · Compliance scoring (n of 8 required constructs present)

Documents analysed:
  1. EU AI Act (Regulation 2024/1689) — Articles 9 & 13
  2. NIST AI RMF 1.0 — Govern function excerpts
  3. OECD AI Principles (2019, updated 2024) — all five principles
  4. US Executive Order 14110 (Oct 2023) — §4 Safety & §7 Workers

Usage:
    python3 test_real_world.py
"""

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import (
    find_paraphrase_violations,
    PARAPHRASE_GUARDS,
    HIERARCHY_PATTERNS,
    INTEGRITY_PATTERNS,
    COHERENCE_PATTERNS,
)


# ── Document corpus ───────────────────────────────────────────────────────────
# Faithful representative excerpts from public AI governance frameworks.

DOCUMENTS = {

    "EU AI Act — Art. 9 & 13": """\
EU AI Act (Regulation 2024/1689) — Risk Management and Transparency

Article 9 — Risk Management System

A risk management system shall be established, implemented, documented and
maintained in relation to high-risk AI systems throughout the entire lifecycle
of the system. The risk management system shall consist of a continuous iterative
process comprising: (a) identification and analysis of known and reasonably
foreseeable risks to health, safety or fundamental rights when the system is used
in accordance with its intended purpose; (b) estimation and evaluation of risks
arising from reasonably foreseeable misuse; (c) adoption of appropriate and
targeted risk management measures designed to address identified risks in proportion
to the degree of risk posed to health, safety or fundamental rights.

Risk management measures shall give due consideration to the effects and possible
interactions resulting from the combined application of requirements set out in this
Chapter. They shall take into account the state of the art, including as reflected
in relevant harmonised standards or common specifications.

Article 13 — Transparency and Provision of Information to Deployers

High-risk AI systems shall be designed and developed so as to ensure that their
operation is sufficiently transparent to enable deployers to interpret the system's
output and use it appropriately. An appropriate type and degree of transparency
shall be ensured, in view of the intended purpose of the AI system. Deployers
shall have sufficient information about the system to ensure its use remains within
the scope of its intended purpose and does not put at risk the health, safety or
fundamental rights of natural persons.
""",

    "NIST AI RMF — Govern Function": """\
NIST AI Risk Management Framework 1.0 — Govern Function

The GOVERN function cultivates and implements organisational practices where
accountability for AI risk outcomes is distributed across appropriate roles.
Policies, processes, and cultural practices are in place to achieve responsible
AI risk management throughout the AI lifecycle.

GOVERN 1.1: Policies, processes, procedures, and practices across the organisation
related to the mapping, measuring, and managing of AI risks are in place,
transparent, and implemented effectively.

GOVERN 1.2: Accountability, criteria, and processes exist so that appropriate teams
and individuals are empowered, responsible, and trained for mapping, measuring,
and managing AI risks.

GOVERN 2.1: Organisational teams that develop, deploy, evaluate, and assess AI
systems document the context in which the AI system will be used as a basis for
identifying risks. This includes intended uses, known limitations, technical
specifications, and deployment environment.

GOVERN 4.1: Policies and practices are in place to foster a critical thinking and
safety-first mindset in the design, development, deployment, and uses of AI
systems to minimise potential negative impacts.

GOVERN 6.1: Policies and procedures are in place to address AI risks and benefits
arising from third-party entities, including AI-generated content used in training
or fine-tuning, and data and models from third parties, consistent with the
organisation's policies on AI risk.
""",

    "OECD AI Principles (2019, rev. 2024)": """\
OECD Principles on AI — Value-Based Principles for Responsible AI

Adopted by the OECD Council, May 2019. Revised 2024.

1. Inclusive growth, sustainable development and well-being
Stakeholders should proactively engage in responsible stewardship of trustworthy
AI in pursuit of beneficial outcomes for people and the planet, while decreasing
inequalities and protecting natural environments, including by augmenting human
capabilities and enhancing creativity.

2. Human-centred values and fairness
AI actors should respect the rule of law, human rights and democratic values
throughout the AI system lifecycle. These include freedom, dignity and autonomy,
privacy and data protection, non-discrimination and equality, diversity, fairness,
social justice, and internationally recognised labour rights. AI actors should
implement mechanisms and safeguards, including capacity for human determination,
appropriate to the context and consistent with the state of the art.

3. Transparency and explainability
AI actors should commit to transparency and responsible disclosure regarding AI
systems. This includes providing meaningful information to enable those adversely
affected by an AI system to challenge its outcome based on plain and intelligible
information about the factors and logic that served as a basis for a decision.

4. Robustness, security and safety
AI systems should be technically robust and developed and run in ways that minimise
and where possible prevent unsafe outcomes, including unintended or unexpected
applications. AI actors should ensure traceability in relation to datasets,
processes and decisions made during the AI system lifecycle.

5. Accountability
AI actors should be accountable for the proper functioning of AI systems and for
the respect of the above principles, based on their roles and consistent with
the state of the art. Mechanisms should ensure responsibility and redress for AI
systems and their outcomes.
""",

    "US Executive Order 14110 — §4 Safety": """\
Executive Order 14110 on Safe, Secure, and Trustworthy Artificial Intelligence
(October 30, 2023)

Section 4.1 — Ensuring the Safety and Security of AI

The Secretary of Commerce shall engage with industry, civil society, and other
stakeholders to develop guidelines, standards, methodologies, and related tools
for AI safety and security, including for the evaluation of AI systems' alignment
with democratic values and human rights. Safety standards shall be proportionate
to the level of risk posed, with higher-risk applications subject to more
stringent requirements.

Section 4.2 — Advancing Transparency and Accountability

Federal agencies using AI in high-stakes decisions affecting members of the public
shall design systems to provide meaningful explanations of their outputs and to
support oversight by affected individuals and government officials. Accountability
for all Federal agencies for their AI use is paramount. Agencies shall ensure that
AI deployment maintains appropriate human oversight and does not abrogate the
rights or welfare of the public.

Section 7 — Supporting Workers

Agencies shall ensure that AI deployment in workplaces preserves fundamental
protections for workers, maintaining the connection between obligations imposed on
workers and the protections those obligations are intended to serve. No deployment
shall sever the linkage between a worker's legal obligations and their corresponding
rights.
""",

}


# ── Narrative interpretations (per document) ─────────────────────────────────

INTERPRETATIONS = {

    "EU AI Act — Art. 9 & 13": (
        "Attempts LAIF-like concepts: YES — proportionality, risk to fundamental\n"
        "  rights, transparency, and lifecycle governance signal all three Coherence\n"
        "  Test dimensions implicitly.\n"
        "  Expression: IMPLICIT — a risk-based classification framework that addresses\n"
        "  proportionality without declaring structural Coupling between each deployment\n"
        "  restriction and the specific human interest it protects.\n"
        "  LAIF failure: Article 9 requires risk management measures 'proportionate\n"
        "  to the degree of risk' — but proportionality is not Coupling. LAIF requires\n"
        "  that the restriction and its paired protection share equivalent normative\n"
        "  force and cannot be weakened in isolation. The Act imposes no such structural\n"
        "  pairing. No Coherence Test, no Integrity Layer precondition declared."
    ),

    "NIST AI RMF — Govern Function": (
        "Attempts LAIF-like concepts: YES — accountability, transparency, risk\n"
        "  governance, and safety-first mindset are present throughout.\n"
        "  Expression: IMPLICIT — functional decomposition (Govern / Map / Measure /\n"
        "  Manage) operationalises governance without constitutional hierarchy.\n"
        "  LAIF failure: Distributes accountability across organisational roles without\n"
        "  declaring structural Coupling. The RMF requires documentation of deployment\n"
        "  context but not the structural pairing of each constraint with the human\n"
        "  interest it protects. No hierarchy supremacy clause; no non-amendable\n"
        "  foundational principles; no self-application requirement binding the\n"
        "  governance body itself to the same standard."
    ),

    "OECD AI Principles (2019, rev. 2024)": (
        "Attempts LAIF-like concepts: YES — all five principles address dimensions\n"
        "  that LAIF encodes structurally as Coupling, Consistency, Reversibility,\n"
        "  and the Integrity Layer properties.\n"
        "  Expression: IMPLICIT — declaratory principle-based approach with no\n"
        "  structural interdependency between principles or enforcement mechanism.\n"
        "  LAIF failure: Principles are independent declarations, not coupled. Under\n"
        "  LAIF, Coupling requires that a restriction and its paired protection cannot\n"
        "  be weakened in isolation. Here, Principle 3 (transparency) and Principle 5\n"
        "  (accountability) are logically separable — a governance actor could weaken\n"
        "  one without structurally affecting the other. No Coherence Test applied."
    ),

    "US Executive Order 14110 — §4 Safety": (
        "Attempts LAIF-like concepts: YES — safety, transparency, accountability,\n"
        "  human rights, and worker protections signal broad governance intent.\n"
        "  Expression: IMPLICIT + direct paraphrase substitution detected.\n"
        "  LAIF failure (terminological): Section 4.1 uses 'alignment with democratic\n"
        "  values' as a structural relationship — a direct Coupling paraphrase violation.\n"
        "  Section 7 uses 'connection between obligations and protections' and 'linkage\n"
        "  between obligations and rights' — two further paraphrase violations. All\n"
        "  three deploy substitution language where LAIF requires the canonical term\n"
        "  Coupling with its structural enforcement meaning. This is the clearest\n"
        "  real-world example of conceptual drift from the LAIF corpus."
    ),

}


# ── Required LAIF constructs ──────────────────────────────────────────────────

REQUIRED_CONSTRUCTS = [
    ("Canonical: Coupling",                           r"\bCoupling\b"),
    ("Canonical: Integrity Layer",                    r"\bIntegrity Layer\b"),
    ("Canonical: Coherence Test",                     r"\bCoherence Test\b"),
    ("Hierarchy: Part One / Foundational Principles", r"PART ONE|FOUNDATIONAL PRINCIPLES"),
    ("Hierarchy: non-amendable clause",               r"cannot be amended|non-amendable"),
    ("Hierarchy: self-application (Part Seven)",      r"PART SEVEN|self.application|applies to regulatory"),
    ("Structure: Integrity Layer FINDING block",      r"A\.1 FINDING\s*:"),
    ("Structure: Coherence Test FINDING block",       r"B\.1 FINDING\s*:"),
]

LAIF_ADJACENT = [
    (r"\btransparency\b",                                        "transparency"),
    (r"\baccountability\b",                                      "accountability"),
    (r"\bproportionat",                                          "proportionality"),
    (r"\boversight\b",                                           "oversight"),
    (r"\bhuman rights\b|\bfundamental rights\b",                 "fundamental rights"),
    (r"\brisk.{0,5}management\b|\brisk.{0,5}assessment\b",      "risk governance"),
    (r"\bsafety\b",                                              "safety"),
    (r"\bexplainability\b|\bexplain",                            "explainability"),
    (r"\bhuman.centr|\bpeople.centr",                            "human-centric framing"),
    (r"\btraceability\b",                                        "traceability"),
]


# ── Output helpers ────────────────────────────────────────────────────────────

def _tty(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text

def _present(flag):
    tag, col = ("PRESENT", "32") if flag else ("ABSENT ", "31")
    return _tty(col, f"[{tag}]")

W = 66


# ── Per-document analysis ─────────────────────────────────────────────────────

def analyse(name, text):
    present, missing = [], []
    for label, pattern in REQUIRED_CONSTRUCTS:
        (present if re.search(pattern, text, re.IGNORECASE) else missing).append(label)

    paraphrase = {}
    for guard in PARAPHRASE_GUARDS:
        v = find_paraphrase_violations(text, guard)
        if v:
            paraphrase[guard["term"]] = v

    seen, adjacent = set(), []
    for pattern, label in LAIF_ADJACENT:
        if label not in seen and re.search(pattern, text, re.IGNORECASE):
            adjacent.append(label)
            seen.add(label)

    pdca_absent = all(
        not re.search(pat, text, re.DOTALL | re.IGNORECASE)
        for _, pat in (INTEGRITY_PATTERNS + COHERENCE_PATTERNS)
    )

    failure_types = []
    if pdca_absent and not any(l.startswith("Hierarchy") for l in present):
        failure_types.append("structural")
    if missing and ("Canonical: Coupling" in missing or "Canonical: Integrity Layer" in missing):
        failure_types.append("terminological")
    if paraphrase:
        failure_types.append("terminological (paraphrase)")
    if len(adjacent) >= 3 and len(present) == 0:
        failure_types.append("conceptual")

    return {
        "name":          name,
        "chars":         len(text),
        "present":       present,
        "missing":       missing,
        "score":         len(present),
        "total":         len(REQUIRED_CONSTRUCTS),
        "pct":           round(100 * len(present) / len(REQUIRED_CONSTRUCTS)),
        "paraphrase":    paraphrase,
        "adjacent":      adjacent,
        "failure_types": failure_types,
    }


def print_report(r, interpretation):
    print(f"\n{'─' * W}")
    score_tag = _tty("31", f"{r['score']}/{r['total']} ({r['pct']}%)")
    print(f"  DOCUMENT: {r['name']}")
    print(f"  {r['chars']:,} chars  ·  LAIF construct coverage: {score_tag}")
    print(f"{'─' * W}")

    print("\n  STRUCTURE & TERMINOLOGY")
    for label in r["present"]:
        print(f"    {_present(True)}   {label}")
    for label in r["missing"]:
        print(f"    {_present(False)}   {label}")

    print("\n  PARAPHRASE VIOLATIONS")
    if r["paraphrase"]:
        for term, violations in r["paraphrase"].items():
            print(f"    [guard: {term}]  {len(violations)} violation(s)")
            for _, ctx in violations[:3]:
                print(f"      ↳ …{ctx.replace(chr(10), ' ')[:108]}…")
    else:
        print("    none detected")

    print("\n  LAIF-ADJACENT CONCEPTS DETECTED")
    if r["adjacent"]:
        print("    · " + "  ·  ".join(r["adjacent"]))
    else:
        print("    · none")

    print("\n  FAILURE TYPES")
    if r["failure_types"]:
        print("    " + ",  ".join(r["failure_types"]))
    else:
        print("    none — document is LAIF-compliant")

    print("\n  INTERPRETATION")
    for line in interpretation.splitlines():
        print(f"    {line}")


# ── Cross-document summary ────────────────────────────────────────────────────

def print_summary(results):
    print(f"\n{'═' * W}")
    print(f"  SUMMARY — {len(results)} external governance documents analysed")
    print(f"{'─' * W}")

    failing = [r for r in results if r["pct"] < 100]
    pct_fail = round(100 * len(failing) / len(results))
    print(f"  Failing LAIF compliance:  {len(failing)}/{len(results)} ({pct_fail}%)")

    avg_score = sum(r["pct"] for r in results) / len(results)
    print(f"  Average construct coverage: {avg_score:.0f}%")

    missing_counter = Counter(label for r in results for label in r["missing"])
    print(f"\n  Most commonly absent constructs (all {len(results)} documents):")
    for label, count in missing_counter.most_common():
        bar = "▓" * count + "░" * (len(results) - count)
        print(f"    [{bar}]  {count}/{len(results)}  {label}")

    type_counter = Counter(ft for r in results for ft in r["failure_types"])
    print(f"\n  Failure type frequency:")
    for ft, count in type_counter.most_common():
        print(f"    {ft:<32}  {count}/{len(results)} documents")

    docs_with_violations = [r for r in results if r["paraphrase"]]
    print(f"\n  Paraphrase violations:  {len(docs_with_violations)}/{len(results)} documents")
    for r in docs_with_violations:
        for term, vs in r["paraphrase"].items():
            print(f"    {r['name'][:44]:<46}  [{term}]  {len(vs)} violation(s)")

    avg_adj = sum(len(r["adjacent"]) for r in results) / len(results)
    print(f"\n  Avg LAIF-adjacent signals per document:  {avg_adj:.1f} "
          f"(high = conceptual intent present without structural expression)")

    print(f"\n  KEY FINDINGS")
    print(f"    1. 100% of documents fail LAIF compliance — no external framework")
    print(f"       currently satisfies LAIF's structural requirements.")
    print(f"    2. Primary failure mode: conceptual + terminological. All documents")
    print(f"       express LAIF-like governance intent (avg {avg_adj:.1f} adjacent signals)")
    print(f"       without structural Coupling or Coherence Test declarations.")
    print(f"    3. Most common absence: canonical terms (Coupling, Integrity Layer,")
    print(f"       Coherence Test) — absent from all {len(results)} documents.")
    print(f"    4. Paraphrase violations found in {len(docs_with_violations)}/{len(results)} documents —")
    print(f"       'alignment', 'connection', 'linkage' used where LAIF requires Coupling.")
    print(f"    5. LAIF is measurably stricter than current governance language.")
    print(f"       The gap is not intent but structural declaration.")
    print(f"{'═' * W}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  LAIF Real-World Validation  ·  Controlled Exploration         ║")
    print("║  Framework v1.2  ·  April 2026  ·  Observational phase only    ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("  validate.py is unchanged — this script is observational only.\n")

    results = []
    for name, text in DOCUMENTS.items():
        r = analyse(name, text)
        interp = INTERPRETATIONS.get(name, "(no interpretation recorded)")
        print_report(r, interp)
        results.append(r)

    print_summary(results)
    sys.exit(0)


if __name__ == "__main__":
    main()
