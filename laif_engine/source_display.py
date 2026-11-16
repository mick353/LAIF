"""LAIF engine: source display. Moved without changing assessment rules."""

import re
from .detection import (
    AUDITABILITY_RUBRIC,
    CONCEPTUAL_RUBRIC,
    ENFORCEABILITY_RUBRIC,
    STRUCTURAL_RUBRIC,
    TERMINOLOGY_RUBRIC,
)
from .source_spans import (
    _locate_offset,
    _quote_at,
)


def _located_signals(text, outline):
    """First-match location and verbatim quote for every fired rubric signal,
    per dimension. Deterministic; quotes are exact substrings of the excerpt
    window around the match."""
    out = {}
    for dim, rubric in (("structural", STRUCTURAL_RUBRIC),
                        ("terminology", TERMINOLOGY_RUBRIC),
                        ("conceptual", CONCEPTUAL_RUBRIC),
                        ("auditability", AUDITABILITY_RUBRIC),
                        ("enforceability", ENFORCEABILITY_RUBRIC)):
        rows = []
        for _, pat, label in rubric:
            m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
            if m:
                rows.append({
                    "label":    label,
                    "quote":    _quote_at(text, m.start(), m.end()),
                    "location": _locate_offset(m.start(), outline),
                })
        out[dim] = rows
    return out


# Sentence charclass permits newlines: obligation sentences in hard-wrapped
# prose span lines; quotes are whitespace-normalised on capture.
_OBLIGATION_SENTENCE = re.compile(
    r"[A-Z][^.!?]{10,180}\b(?:shall|must)\b(?:\s+not)?[^.!?]{5,200}[.!?]"
)


def _obligation_anchors(text, outline, limit=3):
    """Up to `limit` obligation sentences with locations — the exact places a
    restriction-protection pairing would attach. Diversified: at most one
    anchor per document section, so guidance spans the document rather than
    clustering in its first section."""
    anchors, seen_sections = [], set()
    spare = None
    for m in _OBLIGATION_SENTENCE.finditer(text):
        loc = _locate_offset(m.start(), outline)
        entry = {"quote": " ".join(m.group(0).split())[:140], "location": loc}
        if loc in seen_sections:
            spare = spare or entry
            continue
        seen_sections.add(loc)
        anchors.append(entry)
        if len(anchors) >= limit:
            break
    if not anchors and spare:
        anchors.append(spare)
    return anchors


_ANCHOR_HINTS = {
    "Coupling":         "protect rights interest worker patient consumer safety",
    "Integrity Layer":  "safety security testing evaluation standards oversight",
    "Consistency":      "scope application definitions general provisions",
    "Reversibility":    "review monitoring appeal correction redress oversight",
    "Self-Application": "implementation administration governance authority council",
}


def _suggest_anchor(label, outline, obligation_anchors):
    """Deterministic suggestion for where a missing element would belong:
    the document's own section whose title shares vocabulary with the
    missing signal; else the first obligation sentence's section; else an
    honest 'new provision required'."""
    enriched = f"{label} {_ANCHOR_HINTS.get(label.split(' ')[0].strip(), '')} " \
               f"{_ANCHOR_HINTS.get(label, '')}"
    words = {w for w in re.split(r"[^a-z]+", enriched.lower()) if len(w) > 3}
    best, best_score = None, 0
    for _, sec in outline:
        sec_words = {w for w in re.split(r"[^a-z]+", sec.lower()) if len(w) > 3}
        score = len(words & sec_words)
        if score > best_score:
            best, best_score = sec, score
    if best:
        return f"most related existing section: '{best}'"
    if obligation_anchors:
        return f"attach under '{obligation_anchors[0]['location']}'"
    return "no existing section covers this — a new provision is required"


# ── Plain-language reading ────────────────────────────────────────────────────
# A framework-free narrative of what the measurements found, written for a
# reader who has never heard of LAIF — including the assessed document's own
# authors. Every sentence is conditioned on a measured signal; nothing here is
# free-floating editorial. Deliberately uses no LAIF vocabulary.

_PLAIN_VALUE_NAMES = {
    "human rights / fundamental interests":   "people's fundamental rights",
    "transparency":                            "openness about how decisions are made",
    "explainability / interpretability":       "explanations people can understand",
    "accountability":                          "answerability for outcomes",
    "human oversight":                         "human oversight of the system",
    "proportionality":                         "matching rules to the size of the risk",
    "safety":                                  "safety",
    "contestability / redress":                "the ability to challenge decisions",
    "reversibility / modifiability":           "the ability to correct or reverse outcomes",
    "risk governance":                         "structured risk management",
    "traceability / responsibility":           "traceability of decisions",
    "fairness / labour / non-discrimination":  "fairness and non-discrimination",
}

_PLAIN_SOURCE_TYPES = {
    "executive_directive":      "a statement of values followed by a tasking list — "
                                "named officials receive instructions and deadlines",
    "binding_regulation":       "binding law — it imposes obligations on identified "
                                "parties, enforceable through the legal system",
    "voluntary_framework":      "a voluntary playbook — structured practices an "
                                "organisation may adopt, with no binding force of its own",
    "international_principles": "an intergovernmental commitment — principles that "
                                "governments endorse and are expected, but not "
                                "compelled, to implement",
    "sector_policy":            "a sector instrument — operational requirements for a "
                                "specific deployment context",
}


def _plain_reading(result):
    """
    Return a list of plain-language paragraphs interpreting the measurements
    for a lay reader. Framework-free by design: no LAIF terminology.
    """
    paras   = []
    bd      = result["score_breakdown"]
    fired_c = [lbl for lbl, _ in bd["conceptual"]["fired"]]
    miss_c  = [lbl for lbl, _ in bd["conceptual"]["missed"]]
    fired_a = [lbl for lbl, _ in bd["auditability"]["fired"]]
    cstate  = result.get("coupling_state", "ABSENT")
    func    = result.get("functional_alignment", {})
    align   = result.get("laif_alignment", "")

    def fv(construct):
        return func.get(construct, {}).get("verdict", "ABSENT")

    # ── What this document is, and what it cares about ──────────────────────
    intro  = _PLAIN_SOURCE_TYPES.get(result["source_type"], "a governance document")
    values = [_PLAIN_VALUE_NAMES[l] for l in fired_c if l in _PLAIN_VALUE_NAMES]
    first  = f"In plain terms, this document is {intro}."
    if len(values) >= 3:
        first += (f" It clearly names the things it exists to protect: "
                  f"{', '.join(values[:5])}"
                  + (" and more." if len(values) > 5 else "."))
    elif values:
        first += (f" It names only some of the human concerns it exists to serve "
                  f"({', '.join(values)}).")
    else:
        first += (" Notably, it barely names the human concerns it exists to "
                  "serve — the reader must infer who is meant to benefit.")
    paras.append(first)

    # ── Do promises reach the person? ────────────────────────────────────────
    if cstate in ("STRUCTURAL", "FUNCTIONAL"):
        s = ("Its strongest structural feature: promises are fastened to the "
             "people they serve. When it restricts something, it says who that "
             "protects — and the protection is written to be as durable as the "
             "rule, so that one cannot quietly outlive the other.")
        if cstate == "FUNCTIONAL":
            s += (" It does this in its own words rather than any framework's "
                  "vocabulary, and the pairing is real.")
        paras.append(s)
    elif cstate == "IMPLICIT":
        paras.append(
            "It expresses a clear intention to protect people, but the promises "
            "are not fastened to the people they serve: a specific rule could be "
            "weakened or dropped without visibly breaking a commitment to any "
            "identifiable person."
        )
    else:
        s = ("Trace who receives something in each operative sentence and a "
             "pattern appears: institutions receive duties, deadlines, and "
             "reporting obligations — but the people the document is about "
             "receive nothing they can hold. Protection exists here as intended "
             "future outcomes, not as present commitments to identifiable "
             "people; because promises and beneficiaries are never fastened "
             "together, individual provisions can erode without anyone being "
             "able to say a promise to them was broken.")
        paras.append(s)
    if "contestability / redress" in miss_c:
        paras.append(
            "It provides no route for an affected person to challenge or appeal "
            "an outcome — if the system gets it wrong for someone, this text "
            "gives them nothing to invoke."
        )
    elif "contestability / redress" in fired_c and cstate not in ("STRUCTURAL", "FUNCTIONAL"):
        paras.append(
            "It does give people a route to challenge decisions — a genuine "
            "person-facing protection, and the main exception to the pattern above."
        )

    # ── Does anything bind the author, and does anything survive them? ──────
    author_bound = fv("Self-Application") in ("DECLARED", "FUNCTIONAL")
    durable      = fv("Reversibility") in ("DECLARED", "FUNCTIONAL")
    if author_bound and durable:
        paras.append(
            "Unusually, it binds its own author — the governing authority is "
            "subject to the same tests it imposes on others — and it protects "
            "the future: consequences can be corrected, and permanent effects "
            "require senior approval before they happen."
        )
    elif author_bound:
        paras.append(
            "Unusually, it binds its own author: the governing authority is "
            "subject to the same tests it imposes on others. It is weaker on "
            "time: little in it guarantees that outcomes can be corrected or "
            "that permanent effects need special approval."
        )
    elif durable:
        paras.append(
            "It takes the future seriously — consequences can be corrected or "
            "reversed, and permanent effects require approval first — but "
            "nothing in it binds the author: it sets tests for others and none "
            "that the issuing authority itself must pass."
        )
    else:
        s = ("Nothing in it binds the author — it sets requirements for others "
             "but none that the issuing authority itself must pass — and "
             "nothing anchors it in time: ")
        if fv("Reversibility") == "PARTIAL":
            s += ("it gestures at correction and rollback, but not as a "
                  "guaranteed capacity, and everything it creates can be "
                  "undone by its author's successor.")
        else:
            s += ("everything it creates can be modified or undone by its "
                  "author's successor without any special safeguard.")
        paras.append(s)

    # ── Credit where due ─────────────────────────────────────────────────────
    credit = []
    if "numbered traceable requirements" in fired_a:
        credit.append("numbered, traceable requirements")
    if "evidence / documentation requirements" in fired_a:
        credit.append("evidence and documentation duties")
    if "review / monitoring mechanisms" in fired_a:
        credit.append("review and monitoring machinery")
    if result["enforceability_score"] >= 60:
        credit.append("genuinely mandatory language with named owners")
    if credit:
        paras.append(
            f"To its credit, the administrative machinery is real: "
            f"{', '.join(credit)}. Whether its tasks were done is checkable — "
            f"a property many governance documents lack."
        )

    # ── Fair summary ─────────────────────────────────────────────────────────
    if align == "FUNCTIONALLY ALIGNED":
        paras.append(
            "**Fair summary:** the protective architecture is genuinely there, "
            "expressed in the document's own words. Any remaining distance from "
            "a stricter standard is wording and paperwork, not substance."
        )
    elif align == "PARTIALLY ALIGNED":
        paras.append(
            "**Fair summary:** real machinery, real intent, and some of the "
            "deeper protective architecture — but not all of it. That is not a "
            "judgement that the document fails at its own job. It means that if "
            "you relied on this text alone to guarantee a specific person "
            "protection from a specific harm, parts of that load path are missing."
        )
    elif align.startswith("LAIF-NATIVE (HOLLOW"):
        paras.append(
            "**Fair summary:** this document borrows the vocabulary of strong "
            "governance without the machinery behind it. The words are present; "
            "the load-bearing structure is not."
        )
    elif align.startswith("LAIF-NATIVE"):
        paras.append(
            "**Fair summary:** written in the assessing framework's own form; "
            "see the structural-depth verdict above for whether the substance "
            "matches the form."
        )
    else:
        paras.append(
            "**Fair summary:** whatever its other merits, none of the deeper "
            "protective architecture — promises fastened to people, rules that "
            "bind the rule-maker, guarantees that survive a change of author — "
            "is present in any form. That is not a judgement of the document "
            "against its own objectives; it is a statement of what a person "
            "could and could not rely on this text for."
        )
    return paras


# ── Signal grouping for display ───────────────────────────────────────────────
# Display-only classification — does NOT affect scoring.
# Human interest signals relate to specific human interests at risk.
# Governance signals relate to structural, procedural, and architectural controls.
