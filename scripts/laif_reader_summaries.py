"""Plain reading aids kept separate from an author's exact reasoning."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = {
    "A.1": "This check asks whether people can get explanations of decisions, including uncertainty and limits.",
    "A.2": "This check asks whether stated goals match actual behaviour, including during testing and use.",
    "A.3": "This check asks whether the system has clear operating limits and people authorised to stop it or handle problems.",
    "A.4": "This check asks whether the system's stated confidence is compared with measured accuracy for the people and uses concerned.",
    "Q1": "This check asks whether each restriction protects a specific human interest, with protections that can be enforced and remedies when they fail.",
    "Q2": "This check asks whether the same reasoning works for comparable actors, including the smallest, and whether exceptions are justified.",
    "Q3": "This check asks whether decisions can be changed, systems safely retired, and actions that cannot be undone properly justified and authorised.",
    "G.1": "This check asks whether the people setting and overseeing the rules must explain their decisions and face review and challenge themselves.",
}
OUTCOMES = {
    "SUPPORTED_IN_SCOPE": "The author finds support within the stated scope; this does not by itself show that the required actions happen in practice.",
    "PARTIAL_SUPPORT": "The author finds some support but leaves part of this question unresolved; read the reasons and limits below.",
    "NOT_ESTABLISHED": "The author has not established this requirement from the available evidence; this is not proof that the safeguard is absent.",
    "NOT_ESTABLISHED_IN_FULL": "The author has not established the full requirement from the available evidence; this is not proof that the safeguard is absent.",
    "NOT_DEMONSTRATED": "The author has not demonstrated this requirement from the available evidence; this is not proof that the safeguard is absent.",
    "SOURCE_CONFLICT": "The author identifies conflicting evidence; read the reasons and exceptions before reaching a conclusion.",
    "NOT_APPLICABLE": "The author considers this check outside the stated scope; read the applicability reasons before relying on that conclusion.",
    "CONDITIONAL_REQUIREMENT_NOT_ESTABLISHED": "The author has not established the requirement where its conditions apply; those conditions still need careful review.",
    "STRONG_TEXTUAL_SUPPORT_WHERE_APPLICABLE": "The author finds strong written support where the requirement applies; this does not show that it works in practice.",
    "POSITIVE_CLAUSES_COMPLETE_PACKAGE_NOT_DEMONSTRATED": "The author finds helpful clauses but has not demonstrated that the complete set of protections is in place.",
    "SUBSTANTIAL_TEXTUAL_SUPPORT_OPERATION_UNASSESSED": "The author finds substantial written support, but has not assessed whether it works in practice.",
}
EXTRA_JARGON = (
    "three normative-force limbs", "three normative force limbs", "section 2.5 trigger",
    "inseparability", "output-specific meaningful account", "output specific meaningful account",
)


def prohibited_terms():
    config = json.loads((ROOT / "scripts/governance/protected_paths.json").read_text(encoding="utf-8"))
    return tuple(config["semantic_sensitive_terms"]) + EXTRA_JARGON


def validate_reader_summary(value):
    """Reject jargon only in a reading aid, never in an author's reasoning."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("reader_summary must be nonempty text")
    for term in prohibited_terms():
        if re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", value, re.I):
            raise ValueError("reader_summary contains unexplained jargon: " + term)
    return value


def validate_summary_fields(value):
    """Recursively check only reader_summary fields in an output object."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "reader_summary":
                validate_reader_summary(item)
            else:
                validate_summary_fields(item)
    elif isinstance(value, list):
        for item in value:
            validate_summary_fields(item)


def reader_summary(criterion_id, determination):
    if criterion_id not in QUESTIONS or determination not in OUTCOMES:
        raise ValueError("Unknown authored criterion or determination for reader summary")
    return validate_reader_summary(QUESTIONS[criterion_id] + " " + OUTCOMES[determination])


def method_sha256():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def add_reader_summaries(review):
    """Return an enriched normalized review without changing the supplied object."""
    if review is None:
        return None
    return {**review, "reader_summary_method_sha256": method_sha256(),
            "reader_summary_origin": "AUTOMATIC_READING_AID_FOR_RECORDED_AUTHOR_STATUS",
            "criteria": [{**row, "reader_summary": reader_summary(row["criterion_id"], row["determination"])}
                         for row in review["criteria"]]}
