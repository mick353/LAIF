#!/usr/bin/env python3
"""
LAIF Semantic Fidelity Suite
-----------------------------
Guards the assessment engine against the two symmetric failure modes of any
compliance instrument:

  FALSE NEGATIVE — a document that fully expresses LAIF's structural
      requirements in its own vocabulary must never be described as lacking
      them ("substance without vocabulary").
  FALSE POSITIVE — a document that uses LAIF's vocabulary without its
      substance must never be treated as substantively aligned
      ("vocabulary without substance").

Grounding: LAIF v1.2 Part Eight (equivalent structural diligence through
alternative documented means) and the Regulatory Integration Guide Part One
(SATISFIES/EXTENDS methodology). LAIF is the measuring instrument, not an
authority over other instruments' vocabulary — a measurement the source
document's own author would reject as a mischaracterisation is a defective
measurement.

Fixtures:
  S1 — semantic twin: full LAIF substance, zero LAIF vocabulary
  S2 — vocabulary shell: all 8 canonical constructs, zero substance
  S3 — plain-language public register: S1's core ideas for a lay audience
  S4 — S1 plus incidental 'linkage'/'connection' in protective sense
  S5 — S1 plus one canonical Coupling declaration

Usage:
    python3 test_semantic_fidelity.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assessment_engine import assess
from official_documents import OFFICIAL_DOCUMENTS

passed = 0
failed = 0


def _tty(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def check(ok, check_id, msg):
    global passed, failed
    if ok:
        passed += 1
        print(f"  [{_tty('32', 'PASS')}]  {check_id:<7} {msg}")
    else:
        failed += 1
        print(f"  [{_tty('31', 'FAIL')}]  {check_id:<7} {msg}")


def section(title):
    print(f"\n{'─' * 70}\n  {title}\n{'─' * 70}")


# ── Fixtures ──────────────────────────────────────────────────────────────────

S1_SEMANTIC_TWIN = """
Governance Charter for Automated Decision Systems

Part 1 — Founding Rules (these rules cannot be amended by any operational
revision and bind every provision below).

1.1 Every restriction imposed by this charter shall name, with specificity,
the person-level stake it exists to serve. The restriction on unsupervised
diagnostic output exists to protect the patient's stake in treatment decisions
based on accurate clinical assessment. The protection of that stake shall be
as enforceable, as accessible, and as precise as the restriction itself:
neither the restriction nor its paired protection may be weakened, suspended,
or repealed without the other. Every obligation in this charter is therefore
bound to a named beneficiary protection of the same legal strength.

1.2 The reasoning that justifies any rule at one scale shall be defensible
when applied to the smallest comparable operator and to the largest. Any
differential treatment between small and large operators shall be documented
with a principled justification, and the aggregate result of universal
application shall be acceptable.

1.3 Future decision-makers shall retain the capacity to reverse or modify the
consequences of any deployment. No system shall initiate an action with
substantially irreversible consequences for a person without prior documented
authorisation at a level of authority commensurate with the permanence of
those consequences.

Part 2 — Deployment Preconditions. All three of the following conditions must
be satisfied simultaneously before any deployment authorisation; partial
satisfaction of any condition is failure of the gate as a whole.

(a) The system shall produce, on request, a meaningful account of the basis
for any output that affects a person's legal, financial, health, or liberty
position, including its confidence characteristics and material limitations.
(b) The optimisation objectives stated in system documentation shall
correspond to the objectives actually implemented, verified by independent
review; the system shall perform consistently whether or not it is under
evaluation.
(c) The system shall operate within documented boundaries in all tested
conditions, including edge cases, and shall surface out-of-scope requests
through designated escalation channels rather than acting on them.

Part 3 — Application to This Authority. This charter applies to the
regulatory authority itself and to every governance actor administering it,
not only to system operators. The authority shall document its own compliance
with Parts 1 and 2 on the same evidentiary standard it demands of operators,
and any person affected by the authority's decisions shall have the right to
appeal to an independent reviewer with power to reverse the decision.

Part 4 — Enforcement. Providers and deployers shall maintain records
sufficient for audit. Non-compliance with any precondition shall result in
suspension of the deployment authorisation. Affected persons shall have
access to redress and remedies without fees or procedural barriers, through
mechanisms as effective as those available to enforce the restrictions.
"""

S2_VOCABULARY_SHELL = """
PART ONE — FOUNDATIONAL PRINCIPLES

This document adopts Coupling, the Coherence Test, and the Integrity Layer.
These principles cannot be amended. Self-application is adopted: the
framework applies to regulatory bodies.

Coupling is adopted as a principle. The Coherence Test is adopted as a
principle. The Integrity Layer is adopted as a principle. Structural
Transparency, Structural Honesty, and Structural Containment are adopted.
Consistency is adopted. Reversibility is adopted.

A.1 FINDING: Adopted.
B.1 FINDING: Adopted.
"""

S3_PLAIN_REGISTER = """
Our Commitments on AI Decision-Making

Every rule we impose exists to protect a specific person: when we restrict
what the system can decide alone, we say exactly who that protects and why,
and we promise the protection is just as strong as the rule. We will never
quietly drop the protection while keeping the rule, or drop the rule while
keeping the protection: the two stand or fall together.

Before any AI system goes live, three things must all be true at once: it can
explain any decision that affects you in words you can understand; it really
does what we say it does, checked by independent reviewers; and it stays
inside the limits we set for it, even in unusual situations, escalating to a
human when it is unsure.

If a decision could permanently affect someone's health, money, or rights, a
senior human being must approve it first, and you can always appeal to a
person with the power to reverse it. These commitments apply to us as an
organisation just as much as to our systems, whether we are a two-person team
or a global operator. We keep records so independent auditors can check all
of this, and if we fall short you are entitled to remedies at no cost to you.
"""

S4_TWIN_PLUS_PARAPHRASE = S1_SEMANTIC_TWIN + """
Part 5 — Interpretation. The linkage between each restriction and its named
beneficiary protection, and the connection between stated and implemented
objectives, shall be construed in favour of the affected person.
"""

S5_HYBRID = S1_SEMANTIC_TWIN.replace(
    "Every obligation in this charter is therefore\nbound to a named "
    "beneficiary protection of the same legal strength.",
    "This constitutes Coupling between each restriction and the specific "
    "human interest it protects, with equivalent normative force on both "
    "sides.\n"
)

s1 = assess(name="S1", source_type="fixture", text=S1_SEMANTIC_TWIN)
s2 = assess(name="S2", source_type="fixture", text=S2_VOCABULARY_SHELL)
s3 = assess(name="S3", source_type="fixture", text=S3_PLAIN_REGISTER)
s4 = assess(name="S4", source_type="fixture", text=S4_TWIN_PLUS_PARAPHRASE)
s5 = assess(name="S5", source_type="fixture", text=S5_HYBRID)


def n_functional(r):
    return sum(1 for v in r["functional_alignment"].values()
               if v["verdict"] in ("FUNCTIONAL", "DECLARED"))


# ── GROUP SF1 — Substance without vocabulary must be recognised ───────────────

section("GROUP SF1 — Substance without vocabulary (false-negative guard)")

check(s1["coupling_state"] == "FUNCTIONAL", "SF1.1",
      f"S1 coupling_state is FUNCTIONAL (got {s1['coupling_state']})")
check(s1["laif_alignment"] == "FUNCTIONALLY ALIGNED", "SF1.2",
      f"S1 overall verdict is FUNCTIONALLY ALIGNED (got {s1['laif_alignment']})")
check(all(v["verdict"] == "FUNCTIONAL" for v in s1["functional_alignment"].values()),
      "SF1.3", "S1 all five constructs FUNCTIONAL")
check(len(s1["contradictions"]) == 0, "SF1.4",
      "S1 not falsely accused of Structural Honesty contradictions")
check("does not structurally protect" not in
      (s1.get("executive_summary", {}).get("verdict", "") + " ".join(
          s1.get("executive_summary", {}).get("risks", []))),
      "SF1.5", "S1 narrative never asserts absence of protection")

check(s3["coupling_state"] == "FUNCTIONAL", "SF1.6",
      f"S3 plain register: coupling substance recognised (got {s3['coupling_state']})")
check(s3["laif_alignment"] in ("FUNCTIONALLY ALIGNED", "PARTIALLY ALIGNED"), "SF1.7",
      f"S3 plain register at least PARTIALLY ALIGNED (got {s3['laif_alignment']})")
check(s3["conceptual_proximity_score"] >= 30, "SF1.8",
      f"S3 register-aware conceptual proximity ≥30 (got {s3['conceptual_proximity_score']})")
check(s3["enforceability_score"] >= 40, "SF1.9",
      f"S3 plain-register mandatory language recognised, enforceability ≥40 "
      f"(got {s3['enforceability_score']})")


# ── GROUP SF2 — Vocabulary without substance must not be rewarded ─────────────

section("GROUP SF2 — Vocabulary without substance (false-positive guard)")

check(s2["structural_depth"] == "HOLLOW", "SF2.1",
      f"S2 shell depth is HOLLOW (got {s2['structural_depth']})")
check(s2["laif_alignment"] == "LAIF-NATIVE (HOLLOW)", "SF2.2",
      f"S2 alignment labelled LAIF-NATIVE (HOLLOW) (got {s2['laif_alignment']})")
check(s2["strong_laif_compliance"] != "STRONG PASS", "SF2.3",
      "S2 shell never earns STRONG PASS")
check(all(v["verdict"] != "FUNCTIONAL" for v in s2["functional_alignment"].values()),
      "SF2.4", "S2 shell earns no FUNCTIONAL construct credit")

# The head-to-head invariant: substance must outrank shell on every
# substance-sensitive axis.
check(s1["overall_readiness_score"] > s2["overall_readiness_score"], "SF2.5",
      f"S1 substance outscores S2 shell overall "
      f"({s1['overall_readiness_score']} > {s2['overall_readiness_score']})")
check(s1["conceptual_proximity_score"] > s2["conceptual_proximity_score"], "SF2.6",
      "S1 substance outscores S2 shell on conceptual proximity")
check(n_functional(s1) > sum(1 for v in s2["functional_alignment"].values()
                             if v["verdict"] == "FUNCTIONAL"), "SF2.7",
      "S1 functional construct count exceeds S2's")


# ── GROUP SF3 — Word choice must not be punished as a technicality ────────────

section("GROUP SF3 — Word-choice technicalities (register and paraphrase)")

check(s4["paraphrase_classification"] == "DIVERGENCE_NOTE", "SF3.1",
      f"S4 'linkage/connection' in own vocabulary → divergence note, not violation "
      f"(got {s4['paraphrase_classification']})")
check("terminological (paraphrase) — forbidden substitutions detected"
      not in s4["primary_failure_modes"], "SF3.2",
      "S4 paraphrase does not appear as a failure mode")
check(s4["laif_alignment"] == s1["laif_alignment"], "SF3.3",
      "S4 alignment verdict identical to S1 (word choice changed nothing)")
check(len(s4["contradictions"]) == 0, "SF3.4",
      "S4 not falsely accused of contradictions")

check(s5["coupling_state"] == "STRUCTURAL", "SF3.5",
      f"S5 canonical declaration recognised as STRUCTURAL (got {s5['coupling_state']})")
check(s5["laif_alignment"] == "FUNCTIONALLY ALIGNED", "SF3.6",
      f"S5 hybrid FUNCTIONALLY ALIGNED (got {s5['laif_alignment']})")
check(s5["paraphrase_classification"] == "VIOLATION" or not s5["paraphrase_violations"],
      "SF3.7", "S5 uses canonical vocabulary → guard operates in VIOLATION mode")


# ── GROUP SF4 — Governing language is not a contradiction ────────────────────

section("GROUP SF4 — Regulating a hazard is compliance, not contradiction")

_governing = (
    "All decisions can be appealed to an independent reviewer. "
    "No system shall initiate an action with substantially irreversible "
    "consequences without prior documented authorisation."
)
r_gov = assess(name="governing", source_type="fixture", text=_governing)
check(len(r_gov["contradictions"]) == 0, "SF4.1",
      "authorisation-gated irreversibility is not flagged as dishonesty")

_contradicting = (
    "All final decisions can be appealed within 30 days. However, once "
    "implemented, a decision is permanently recorded and cannot be reversed "
    "or appealed under any circumstances whatsoever."
)
r_con = assess(name="contradicting", source_type="fixture", text=_contradicting)
check(len(r_con["contradictions"]) >= 1, "SF4.2",
      "genuine reversibility contradiction still caught")


# ── GROUP SF5 — Official corpus regression ───────────────────────────────────

section("GROUP SF5 — Official corpus regression (audience acceptability)")

for name, doc in OFFICIAL_DOCUMENTS.items():
    r = assess(name=name, source_type=doc["source_type"], text=doc["text"],
               sector=doc.get("sector", "general_ai_governance"),
               provenance=doc["provenance"])
    short = name[:44]
    check(len(r["contradictions"]) == 0, "SF5.1",
          f"{short}… no false Structural Honesty accusation")
    check(not r["paraphrase_violations"]
          or r["paraphrase_classification"] == "DIVERGENCE_NOTE", "SF5.2",
          f"{short}… own-vocabulary wording never labelled a violation")
    check(r["laif_alignment"] in
          ("PARTIALLY ALIGNED", "STRUCTURALLY UNALIGNED",
           "FUNCTIONALLY ALIGNED"), "SF5.3",
          f"{short}… alignment verdict in expected range ({r['laif_alignment']})")


# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'═' * 70}")
if failed == 0:
    print(f"  {_tty('32', 'ALL SEMANTIC FIDELITY CHECKS PASS')}  (pass={passed}, fail=0)")
    print("  Substance is never outranked by vocabulary; no false accusations.")
else:
    print(f"  {_tty('31', 'SEMANTIC FIDELITY FAILURES')}  (pass={passed}, fail={failed})")
print(f"{'═' * 70}\n")

sys.exit(0 if failed == 0 else 1)
