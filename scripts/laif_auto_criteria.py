"""Deterministic, provisional eight-criterion documentary judgments.

This module evaluates explicit documentary requirements. It does not validate
implementation, legal applicability, or the truth of a document's assertions.
"""
from __future__ import annotations

from bisect import bisect_right
import hashlib
import re
from pathlib import Path

from laif_spec import ASSESSMENT_CRITERIA

SCHEMA = "laif.automatic-criteria.v1"
GOVERNING_ACTOR = r"\b(?:(?:governance|governing|oversight) (?:actors?|bod(?:y|ies)|committees?|boards?|authorit(?:y|ies))|regulators?|boards?|committees?)\b"
# Each component needs its own contextual witness, not a document-wide keyword.
# Patterns within a component are conjunctive within one clause.
RULES = {
    "A.1": (
        ("explanations of decisions or outputs", (r"explain\w*|explanation\w*|meaningful account|\b(?:give|provid\w*|supply|communicat\w*|disclos\w*)\b[^.;|]{0,50}\breasons?\b", r"decision\w*|output\w*|prediction\w*")),
        ("uncertainty and limitations", (r"uncertain\w*|confidence", r"limit\w*|error\w*|accuracy", r"disclos\w*|communicat\w*|\bprovid(?:e[sd]?|ing)\b|explain\w*|show|report\w*")),
        ("access for affected people", (r"affected|individual\w*|person\w*|user\w*", r"access|obtain|request|\bprovid(?:e[sd]?|ing)\b", r"explan\w*|account|\breasons?\b")),
    ),
    "A.2": (
        ("alignment of stated and implemented objectives", (r"stated|declared|intended", r"objectiv\w*|goal\w*", r"implement\w*|actual|behavio\w*", r"correspond\w*|align\w*|match\w*|consisten\w*")),
        ("consistent behaviour in testing and deployment", (r"evaluat\w*|test\w*", r"deploy\w*|operat\w*", r"same|consisten\w*|correspond\w*", r"behavio\w*")),
        ("checks for misleading behaviour", (r"decept\w*|mislead\w*|conceal\w*|gaming", r"detect\w*|test\w*|audit\w*|prevent\w*|monitor\w*")),
    ),
    "A.3": (
        ("defined operating boundaries", (
            r"\b(?:operating|operational|resource|access|action|capability) (?:boundar(?:y|ies)|limits?|limitations?|constraints?)\b|"
            r"\b(?:limits?|boundaries|constraints?) (?:on|for|of|to) (?:actions?|access|resources?|operations?|capabilities)\b|"
            r"\bscope (?:limits?|limitations?|constraints?) mechanisms?\b",
        )),
        ("interruption or deactivation", (r"interrupt\w*|deactivat\w*|disengag\w*|halt\w*|shut.?down|supersede|stop", r"system\w*|model\w*|operat\w*|AI")),
        ("escalation to an authorised person", (
            r"\bescalat\w*\b|\b(?:refer|referral|referred|referring)\b[^.;]{0,65}\b(?:incidents?|exceptions?|breach(?:es)?|anomal\w*)\b|"
            r"\b(?:incidents?|exceptions?|breach(?:es)?|anomal\w*)\b[^.;]{0,65}\b(?:refer|referred|notify|notified)\b",
            r"\b(?:officers?|committees?|boards?|authori[sz]ed (?:persons?|owners?)|human (?:operators?|reviewers?|supervisors?|decision.makers?)|to (?:a |the )?human)\b",
        )),
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
        ("revision or withdrawal of decisions", (r"\brevis(?:e[sd]?|ing|ions?|ab(?:le|ility))\b|\brevers(?:e[sd]?|ing|als?|ib(?:le|ility))\b|\b(?:rollback|roll back|withdraw\w*)\b", r"\b(?:decisions?|systems?|polic(?:y|ies)|deployments?)\b")),
        ("safe decommissioning", (r"decommission\w*|phas\w* out|retir\w*", r"safely|safe|risk\w*|harm\w*|transition")),
        ("justification and authority for irreversible action", (r"irreversib\w*|cannot be undone|permanent", r"justif\w*|proportion\w*", r"authoris\w*|authoriz\w*|approv\w*|authority")),
    ),
    "G.1": (
        ("review of the governance actors themselves", (
            rf"\b(?:independent|external) (?:audit|review|scrutiny) of (?:the |each )?{GOVERNING_ACTOR}|"
            rf"{GOVERNING_ACTOR} (?:(?:itself|themselves) )?(?:(?:must|shall|should|may)(?: also)? )?"
            r"(?:undergo(?:es)?|faces?|be subject to|submit to) (?:an? )?(?:independent|external) (?:audit|review|scrutiny)\b|"
            rf"{GOVERNING_ACTOR} (?:(?:must|shall|should|may)(?: also)? )?(?:be |is |are )?(?:independently|externally) "
            r"(?:audited|reviewed|scrutinised|scrutinized)\b",
        )),
        ("challenge to governance decisions", (r"governance|regulator\w*|governing|board|committee", r"appeal|challenge|contest\w*|redress", r"decision\w*|action\w*|rule\w*")),
        ("transparency of governance reasoning", (r"governance|regulator\w*|governing|board|committee", r"publish\w*|disclos\w*|transparen\w*", r"reason\w*|decision\w*|record\w*")),
    ),
}
OBLIGATION = re.compile(r"\b(?:must|shall|required|requires?|mandatory|responsib\w*|procedures? (?:are|is)|mechanisms? (?:are|is)|polic(?:y|ies) (?:are|is))\b", re.I)
WEAK = re.compile(r"\b(?:should|could|may|encourag\w*|recommend\w*|aim\w*)\b", re.I)
DENIAL = re.compile(
    r"\b(?:need not|not (?:be )?required|no (?:requirement|obligation)|not mandatory|may ignore|"
    r"(?:must|shall) (?:not|never) (?:be )?(?:explain\w*|disclos\w*|review\w*|record\w*|provid\w*|"
    r"allow\w*|deactivat\w*|interrupt\w*|escalat\w*|suspend\w*))\b", re.I,
)
NEGATED_MODAL = re.compile(r"\b(?:must|shall) (?:never|not (?!only\b))", re.I)
QUALIFIED_SCOPE = re.compile(
    r"\b(?:except (?:where|when|for|as|if)|subject to (?:any|the) exceptions?|"
    r"(?:where|when|if) (?:practicable|feasible|possible|appropriate)|unless exempt\w*)\b", re.I,
)
HYPOTHETICAL = re.compile(r"\b(?:for example|example\s*:|hypothetical|illustrat\w*|suppose|imagine|example of|previously|historically)\b", re.I)
BOUNDARY = re.compile(r"[ \t]*\|[ \t]*|(?<=;)\s+|(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])(?=(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d)")
WRAP_CONNECTOR = re.compile(r"\b(?:must|shall|and|or|of|to|for|the|by|with|a|an|that)$", re.I)
CONTEXT_BREAK = re.compile(r"^(?:#{1,6}(?:\s|$)|>\s|```|~~~|\f|\[?PAGE\b)", re.I)
TRAILING_SENTENCE = (".", "!", "?", ":", ";", "|", "\f")
FENCE = re.compile(r"^[ \t]{0,3}(\x60{3,}|~{3,})(.*)$")
COMPILED_RULES = {criterion: tuple((label, tuple(re.compile(pattern, re.I) for pattern in patterns))
                                    for label, patterns in components) for criterion, components in RULES.items()}


def _soft_wrap(previous: str, following: str) -> bool:
    previous, following = previous.strip(" \t\r\n"), following.strip(" \t\r\n")
    return bool(previous and following and re.match(r"[a-z]", following)
                and not previous.endswith(TRAILING_SENTENCE)
                and "|" not in previous and "|" not in following
                and not CONTEXT_BREAK.match(previous)
                and (len(previous) >= 60 or WRAP_CONNECTOR.search(previous)))


def _physical_blocks(text: str):
    """Allow narrow layout continuations while retaining actual source offsets."""
    start = offset = 0
    previous = ""
    for line in text.splitlines(keepends=True):
        if offset and not _soft_wrap(previous, line):
            yield start, offset
            start = offset
        offset += len(line)
        previous = line
    if start < offset:
        yield start, offset


def clauses(text):
    """Keep exact offsets; never join disjoint source passages into a witness."""
    for block_start, block_end in _physical_blocks(text):
        start = block_start
        for boundary in BOUNDARY.finditer(text, block_start, block_end):
            yield from _exact_clause(text, start, boundary.start())
            start = boundary.end()
        yield from _exact_clause(text, start, block_end)


def _exact_clause(text: str, start: int, stop: int):
    raw = text[start:stop]
    value = raw.strip()
    if value:
        offset = start + len(raw) - len(raw.lstrip())
        yield offset, offset + len(value), value


def _fenced_offsets(text: str) -> list[int]:
    """Locate Markdown fence boundaries without treating their contents as requirements."""
    offsets = []
    offset = 0
    opening = ""
    for line in text.splitlines(keepends=True):
        mark = FENCE.match(line)
        if mark:
            delimiter, suffix = mark.groups()
            if not opening:
                opening = delimiter
                offsets.append(offset)
            elif delimiter[0] == opening[0] and len(delimiter) >= len(opening) and not suffix.strip():
                opening = ""
                offsets.append(offset)
        offset += len(line)
    return offsets


def _polarity(text: str, quote_length: int, fenced: bool) -> tuple[str, str]:
    if fenced:
        return "CONTEXT_REVIEW_REQUIRED", "The passage is in a fenced block. Check how the document introduces it."
    if quote_length > 1600 or HYPOTHETICAL.search(text):
        return "CONTEXT_REVIEW_REQUIRED", "Illustrative, historical or unusually long passage."
    if QUALIFIED_SCOPE.search(text):
        return "CONTEXT_REVIEW_REQUIRED", "The passage contains an exception or qualifying condition."
    denial = DENIAL.search(text)
    if (denial or NEGATED_MODAL.search(text)) and len(OBLIGATION.findall(text)) > 1:
        return "CONTEXT_REVIEW_REQUIRED", "More than one obligation or denial appears in the passage."
    if denial:
        return "CONTRARY_REQUIREMENT", "The passage contains an explicit denial or prohibition."
    if NEGATED_MODAL.search(text):
        return "CONTEXT_REVIEW_REQUIRED", "The passage contains a prohibition whose scope needs review."
    if OBLIGATION.search(text) and not WEAK.search(text):
        return "EXPLICIT_REQUIREMENT", "The passage contains obligation wording."
    return "QUALIFIED_MENTION", "The passage mentions the component with weak or absent obligation wording."


def judge(text: str, *, evidence_eligible: bool = True, source_scope: str = "unknown") -> dict:
    fences = _fenced_offsets(text)
    parts = [(start, end, quote, re.sub(r"\s+", " ", quote), bisect_right(fences, start) % 2 == 1)
             for start, end, quote in clauses(text)]
    line_breaks = [match.start() for match in re.finditer("\n", text)]
    rows = []
    for cid, components in COMPILED_RULES.items():
        features = []
        for label, patterns in components:
            witnesses = []
            for start, end, quote, searchable, fenced in parts:
                if not all(pattern.search(searchable) for pattern in patterns):
                    continue
                polarity, reason = _polarity(searchable, len(quote), fenced)
                witnesses.append({"start_char": start, "end_char": end, "exact_quote": quote,
                                  "extracted_line": bisect_right(line_breaks, start) + 1,
                                  "polarity": polarity, "polarity_reason": reason,
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
                            "Continuation handling preserves quotations. Cross-references, exceptions, legal authority and actor identity require review.",
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
                reason = witness.get("polarity_reason", "")
                lines += [f"  - Extracted line {witness['extracted_line']}; {witness['polarity']}. {safe(reason)}".rstrip(), "",
                          *["> " + safe(line) for line in witness["exact_quote"].splitlines()], ""]
    lines += ["### Limits", "", *["- " + line for line in result["limitations"]], ""]
    return lines
