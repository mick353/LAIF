"""Deterministic, provisional eight-criterion documentary judgments.

This module evaluates explicit documentary requirements. It does not validate
implementation, legal applicability, or the truth of a document's assertions.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from laif_spec import ASSESSMENT_CRITERIA

SCHEMA = "laif.automatic-criteria.v1"
# Each component needs its own contextual witness, not a document-wide keyword.
# Patterns within a component are conjunctive within one clause.
RULES = {
    "A.1": (
        ("explanations of decisions or outputs", (r"explain\w*|explanation\w*|meaningful account", r"decision\w*|output\w*|prediction\w*")),
        ("uncertainty and limitations", (r"uncertain\w*|confidence", r"limit\w*|error\w*|accuracy", r"disclos\w*|communicat\w*|\bprovid(?:e[sd]?|ing)\b|explain\w*|show|report\w*")),
        ("access for affected people", (r"affected|individual\w*|person\w*|user\w*", r"access|obtain|request|\bprovid(?:e[sd]?|ing)\b", r"explan\w*|account|reason\w*")),
    ),
    "A.2": (
        ("alignment of stated and implemented objectives", (r"stated|declared|intended", r"objectiv\w*|goal\w*", r"implement\w*|actual|behavio\w*", r"correspond\w*|align\w*|match\w*|consisten\w*")),
        ("consistent behaviour in testing and deployment", (r"evaluat\w*|test\w*", r"deploy\w*|operat\w*", r"same|consisten\w*|correspond\w*", r"behavio\w*")),
        ("checks for misleading behaviour", (r"decept\w*|mislead\w*|conceal\w*|gaming", r"detect\w*|test\w*|audit\w*|prevent\w*|monitor\w*")),
    ),
    "A.3": (
        ("defined operating boundaries", (r"boundar\w*|limit\w*|scope", r"action\w*|access|resource\w*|operat\w*")),
        ("interruption or deactivation", (r"interrupt\w*|deactivat\w*|disengag\w*|halt\w*|shut.?down|supersede|stop", r"system\w*|model\w*|operat\w*|AI")),
        ("escalation to an authorised person", (r"escalat\w*|authoris\w*|authoriz\w*|approv\w*", r"human|officer|owner|responsib\w*|committee|board|person\w*")),
    ),
    "A.4": (
        ("comparison of confidence with measured accuracy", (r"confidence|probabilit\w*|uncertain\w*", r"calibrat\w*|observed accuracy|empirical accuracy", r"compar\w*|measur\w*|test\w*|evaluat\w*|validat\w*")),
        ("a defined evaluation population", (r"calibrat\w*|accuracy|confidence", r"population|sample|dataset|data set|subgroup|intended use")),
        ("review thresholds and corrective action", (r"calibrat\w*|accuracy|confidence", r"threshold|tolerance|error rate", r"review|correct\w*|recalibrat\w*|suspend\w*|retest")),
    ),
    "Q1": (
        ("a restriction linked to a protected interest", (r"restrict\w*|prohibit\w*|permission|permitted|allow\w*", r"right\w*|privacy|liberty|dignity|human interest|safety", r"protect\w*|safeguard\w*|unless|only if|condition")),
        ("equally enforceable protection", (r"protection|safeguard|right\w*", r"equally enforceable|same.{0,35}(?:force|enforceab)|equivalent.{0,35}(?:force|enforceab)", r"restrict\w*|permission|obligation")),
        ("remedy when the protection fails", (r"protection|safeguard|right\w*", r"remedy|redress|appeal|challenge", r"fail\w*|breach|violat\w*|denied")),
    ),
    "Q2": (
        ("consideration of the smallest affected actor", (r"smallest|small.{0,20}(?:actor|organi[sz]ation|provider)|individual actor", r"burden|proportion\w*|effect\w*|impact\w*|feasib\w*")),
        ("reasoning that applies across comparable actors", (r"all|every|universal\w*|comparab\w*", r"actor\w*|organi[sz]ation\w*|provider\w*|case\w*", r"same|consisten\w*|generali[sz]\w*|equal\w*")),
        ("justified exceptions", (r"exception\w*|exemption\w*", r"justif\w*|reason\w*|proportion\w*", r"document\w*|record\w*|review\w*")),
    ),
    "Q3": (
        ("revision or withdrawal of decisions", (r"revis\w*|revers\w*|rollback|roll back|withdraw\w*", r"decision\w*|system\w*|policy|policies|deployment")),
        ("safe decommissioning", (r"decommission\w*|phas\w* out|retir\w*", r"safely|safe|risk\w*|harm\w*|transition")),
        ("justification and authority for irreversible action", (r"irreversib\w*|cannot be undone|permanent", r"justif\w*|proportion\w*", r"authoris\w*|authoriz\w*|approv\w*|authority")),
    ),
    "G.1": (
        ("review of the governance actors themselves", (r"governance|oversight|regulator\w*|governing|board|committee", r"independent|external|themselves", r"audit\w*|review\w*|scrutin\w*")),
        ("challenge to governance decisions", (r"governance|regulator\w*|governing|board|committee", r"appeal|challenge|contest\w*|redress", r"decision\w*|action\w*|rule\w*")),
        ("transparency of governance reasoning", (r"governance|regulator\w*|governing|board|committee", r"publish\w*|disclos\w*|transparen\w*", r"reason\w*|decision\w*|record\w*")),
    ),
}
OBLIGATION = re.compile(r"\b(?:must|shall|required|requires?|mandatory|responsib\w*|procedures? (?:are|is)|mechanisms? (?:are|is)|polic(?:y|ies) (?:are|is))\b", re.I)
WEAK = re.compile(r"\b(?:should|could|may|encourag\w*|recommend\w*|aim\w*)\b", re.I)
DENIAL = re.compile(r"\b(?:need not|not (?:be )?required|no (?:requirement|obligation)|not mandatory|may ignore|must not (?:explain|disclose|review|record|provide|allow)|shall not (?:explain|disclose|review|record|provide|allow))\b", re.I)
HYPOTHETICAL = re.compile(r"\b(?:for example|hypothetical|illustrat\w*|suppose|imagine|example of|previously|historically)\b", re.I)
BOUNDARY = re.compile(r"\n+|(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])(?=(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d)")


def clauses(text):
    """Keep exact offsets; never join disjoint source passages into a witness."""
    start = 0
    for stop in [m.start() for m in BOUNDARY.finditer(text)] + [len(text)]:
        raw = text[start:stop]
        left = len(raw) - len(raw.lstrip())
        value = raw.strip()
        if value:
            yield start + left, start + left + len(value), value
        start = stop


def judge(text: str, *, evidence_eligible: bool = True, source_scope: str = "unknown") -> dict:
    parts = list(clauses(text))
    rows = []
    for cid, components in RULES.items():
        features = []
        for label, patterns in components:
            witnesses = []
            for start, end, quote in parts:
                if not all(re.search(pattern, quote, re.I) for pattern in patterns):
                    continue
                if len(quote) > 1600 or HYPOTHETICAL.search(quote):
                    polarity = "CONTEXT_REVIEW_REQUIRED"
                elif DENIAL.search(quote):
                    polarity = "CONTRARY_REQUIREMENT"
                elif OBLIGATION.search(quote) and not WEAK.search(quote):
                    polarity = "EXPLICIT_REQUIREMENT"
                else:
                    polarity = "QUALIFIED_MENTION"
                witnesses.append({"start_char": start, "end_char": end, "exact_quote": quote,
                                  "extracted_line": text.count("\n", 0, start) + 1,
                                  "polarity": polarity,
                                  "quote_sha256": hashlib.sha256(quote.encode("utf-8")).hexdigest()})
            features.append({"component": label, "witnesses": witnesses,
                             "supported": any(w["polarity"] == "EXPLICIT_REQUIREMENT" for w in witnesses),
                             "contrary": any(w["polarity"] == "CONTRARY_REQUIREMENT" for w in witnesses)})
        found = [f["component"] for f in features if f["supported"]]
        missing = [f["component"] for f in features if not f["supported"]]
        contrary = any(f["contrary"] for f in features)
        mentions = any(f["witnesses"] for f in features)
        if not evidence_eligible or not text.strip():
            determination = "REVIEW_REQUIRED"
            summary = "The extracted source is not suitable for an automatic conclusion. Inspect or replace the source before reviewing this check."
        elif contrary:
            determination = "SOURCE_CONFLICT" if found else "NOT_ESTABLISHED"
            summary = "The text contains wording that denies or weakens a relevant requirement. Review the quoted wording and its exceptions before relying on this check."
        elif not missing:
            determination = "PROVISIONALLY_SUPPORTED"
            summary = "The text states requirements for " + "; ".join(found) + ". Check that the clauses apply together and that the required actions actually occur."
        elif found or mentions:
            determination = "PARTIAL_SUPPORT"
            summary = "The text contains relevant wording, but this check remains incomplete. Evidence still needed: " + "; ".join(missing) + "."
        else:
            determination = "NOT_ESTABLISHED"
            summary = "The rules did not find enough explicit wording to establish this check. Inspect the source and related records before concluding that a safeguard is missing."
        rows.append({"criterion_id": cid, "name": ASSESSMENT_CRITERIA[cid]["name"],
                     "determination": determination, "reader_summary": summary,
                     "origin": "AUTOMATIC_RULE_BASED_DOCUMENTARY_JUDGMENT",
                     "components": features, "missing_components": missing,
                     "supported_component_count": len(found), "required_component_count": len(features),
                     "applicability": "REQUIRES_REVIEW" if cid == "A.4" else "DOCUMENTARY_SCOPE_ONLY",
                     "operational_status": "NOT_ESTABLISHED",
                     "confidence": "UNVALIDATED_RULE_BASED_INFERENCE",
                     "framework_basis": ASSESSMENT_CRITERIA[cid]["source"]})
    return {"schema": SCHEMA, "method_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "extracted_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "source_scope": source_scope, "evidence_eligible": evidence_eligible, "criteria": rows,
            "limitations": ["Rules cover explicit English wording and can miss equivalent formulations.",
                            "Clause matches do not resolve cross-references, exceptions, legal authority or actor identity.",
                            "No calibrated accuracy probability or independently validated effectiveness is available.",
                            "Documentary requirements do not establish operational behaviour."]}


def markdown(result):
    """Escape untrusted quotations; keep automatic reasoning separate from authors."""
    import html
    def safe(value):
        value = html.escape(str(value), quote=False)
        return re.sub(r"([\\`*_{}\[\]()#+!|>])", r"\\\1", value)
    lines = ["## Automatic eight-criterion documentary judgments", "",
             "Provisional rule-based assessment; inspect source context before relying on it. Authored conclusions remain separate.", ""]
    for row in result["criteria"]:
        lines += [f"### {row['criterion_id']} — {row['determination']}", "", row["reader_summary"], ""]
        for feature in row["components"]:
            lines.append(f"- {feature['component']}: {'explicit requirement found' if feature['supported'] else 'not established by explicit wording'}")
            for witness in feature["witnesses"]:
                lines += [f"  - Extracted line {witness['extracted_line']}; {witness['polarity']}", "",
                          *["> " + safe(line) for line in witness["exact_quote"].splitlines()], ""]
    lines += ["### Limits", "", *["- " + line for line in result["limitations"]], ""]
    return lines
