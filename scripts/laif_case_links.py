#!/usr/bin/env python3
"""Read a user-declared, byte-pinned chain of governance case records.

This checks supplied file identity and optional exact text quotations. It does
not infer relationships, missing controls, legal force or operational outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCHEMA = "laif.case-links.v1"
ROLES = ("policy", "contract", "procedure", "test", "incident", "remedy")
HEX = re.compile(r"[0-9a-f]{64}\Z")


def nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def safe(value: object) -> str:
    cleaned = "".join(ch if ch.isprintable() else " " for ch in str(value))
    escaped = html.escape(cleaned, quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+!|>~])", r"\\\1", escaped)


def blockquote(value: str) -> str:
    return "\n".join("> " + safe(line) for line in value.splitlines())


def read_manifest(raw: bytes) -> dict:
    """Parse exact JSON bytes without duplicate keys or non-finite numbers."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"ambiguous case manifest: duplicate key {key!r}")
            result[key] = value
        return result

    def finite(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError("non-finite case manifest number")
        return parsed

    def reject(value):
        raise ValueError(f"non-finite case manifest number: {value}")

    manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=unique,
                          parse_float=finite, parse_constant=reject)
    if not isinstance(manifest, dict):
        raise ValueError("case manifest must be a JSON object")
    return manifest


def local_source_bytes(manifest: dict, root: Path) -> dict[str, bytes]:
    """CLI-only path confinement. The semantic core receives bytes by source ID."""
    if not isinstance(manifest.get("sources"), list):
        raise ValueError("sources must be a list")
    root = root.resolve()
    result = {}
    for item in manifest["sources"]:
        if not isinstance(item, dict) or item.get("status") != "SUPPLIED":
            continue
        sid, file = item.get("id"), item.get("file")
        if not nonblank(sid) or not nonblank(file) or Path(file).is_absolute():
            raise ValueError(f"{sid}: invalid relative source path or ID")
        path = (root / file).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"{sid}: source missing or outside evidence root")
        result[sid] = path.read_bytes()
    return result


def assess_bytes(manifest: dict, manifest_bytes: bytes,
                 sources_by_id: dict[str, bytes]) -> dict:
    """Pure case-link checks for local CLI or a browser worker with retained bytes."""
    if read_manifest(manifest_bytes) != manifest:
        raise ValueError("manifest object does not match the supplied manifest bytes")
    if not isinstance(sources_by_id, dict):
        raise ValueError("sources_by_id must map source IDs to original bytes")
    if manifest.get("schema") != SCHEMA or not nonblank(manifest.get("case_id")):
        raise ValueError("expected laif.case-links.v1 with a nonempty case_id")
    if not nonblank(manifest.get("question")) or not nonblank(manifest.get("analyst_id")):
        raise ValueError("question and self-reported analyst_id are required")
    sources = manifest.get("sources")
    links = manifest.get("links")
    if not isinstance(sources, list) or not sources or not isinstance(links, list):
        raise ValueError("sources must be a nonempty list and links must be a list")

    checked = {}
    by_role = {role: [] for role in ROLES}
    for item in sources:
        if not isinstance(item, dict) or not nonblank(item.get("id")):
            raise ValueError("each source needs a unique nonempty id")
        sid = item["id"]
        if sid in checked:
            raise ValueError(f"duplicate source id: {sid}")
        role, status = item.get("role"), item.get("status")
        if role not in ROLES or status not in {"SUPPLIED", "NOT_SUPPLIED"}:
            raise ValueError(f"{sid}: invalid role or status")
        if status == "SUPPLIED":
            if not nonblank(item.get("version")) or not nonblank(item.get("origin")):
                raise ValueError(f"{sid}: supplied source needs version and declared origin")
            if not isinstance(item.get("sha256"), str) or not HEX.fullmatch(item["sha256"]):
                raise ValueError(f"{sid}: invalid SHA-256")
            if not nonblank(item.get("file")):
                raise ValueError(f"{sid}: supplied source needs a file name")
            content = sources_by_id.get(sid)
            if not isinstance(content, bytes):
                raise ValueError(f"{sid}: original source bytes are missing")
            if hashlib.sha256(content).hexdigest() != item["sha256"]:
                raise ValueError(f"{sid}: SHA-256 mismatch")
            record = {key: item[key] for key in ("id", "role", "status", "file", "sha256", "version", "origin")}
            record["identity_status"] = "LOCAL_BYTES_MATCHED"
        else:
            if not nonblank(item.get("reason")) or any(item.get(key) is not None for key in ("file", "sha256")):
                raise ValueError(f"{sid}: NOT_SUPPLIED needs a reason and no file or hash")
            record = {key: item[key] for key in ("id", "role", "status", "reason")}
            record["identity_status"] = "NO_SOURCE_SUPPLIED"
        checked[sid] = record
        by_role[role].append(record)

    supplied_ids = {sid for sid, record in checked.items() if record["status"] == "SUPPLIED"}
    if set(sources_by_id) != supplied_ids:
        raise ValueError("sources_by_id must contain exactly the declared SUPPLIED source IDs")

    role_status = {}
    for role, records in by_role.items():
        statuses = {record["status"] for record in records}
        if len(statuses) > 1:
            raise ValueError(f"{role}: supplied and NOT_SUPPLIED records conflict")
        role_status[role] = "NOT_DECLARED" if not records else next(iter(statuses))

    checked_links = []
    seen_links = set()
    for item in links:
        if not isinstance(item, dict) or not nonblank(item.get("id")):
            raise ValueError("each link needs a unique nonempty id")
        lid = item["id"]
        if lid in seen_links:
            raise ValueError(f"duplicate link id: {lid}")
        seen_links.add(lid)
        left, right = item.get("from"), item.get("to")
        if left not in checked or right not in checked or left == right:
            raise ValueError(f"{lid}: link must name two distinct declared sources")
        if not nonblank(item.get("relationship")) or not nonblank(item.get("note")):
            raise ValueError(f"{lid}: relationship and analyst note are required")
        quotes = {}
        for side, sid in (("from", left), ("to", right)):
            quote = item.get(side + "_quote")
            if quote is not None and not nonblank(quote):
                raise ValueError(f"{lid}: {side}_quote must be nonempty if supplied")
            if checked[sid]["status"] == "NOT_SUPPLIED":
                if quote is not None:
                    raise ValueError(f"{lid}: cannot quote a NOT_SUPPLIED source")
                continue
            if quote is not None:
                try:
                    source_text = sources_by_id[sid].decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise ValueError(f"{lid}: exact text quote requires a UTF-8 source or verified text derivative") from exc
                if quote not in source_text:
                    raise ValueError(f"{lid} {side}: exact source quotation not present")
                quotes[side] = quote
        if checked[left]["status"] == "NOT_SUPPLIED" or checked[right]["status"] == "NOT_SUPPLIED":
            link_status = "ENDPOINT_NOT_SUPPLIED"
        elif len(quotes) == 2:
            link_status = "EXACT_TEXT_AT_BOTH_ENDPOINTS"
        else:
            link_status = "EXACT_TEXT_LINK_INCOMPLETE"
        checked_links.append({"id": lid, "from": left, "to": right,
                              "relationship": item["relationship"], "note": item["note"],
                              "from_quote": quotes.get("from"), "to_quote": quotes.get("to"),
                              "status": link_status})

    return {"schema": SCHEMA, "case_id": manifest["case_id"], "question": manifest["question"],
            "analyst_id": manifest["analyst_id"], "analyst_identity": "SELF_REPORTED",
            "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "roles": role_status, "sources": list(checked.values()), "links": checked_links,
            "boundary": "File hashes and optional exact text matches are checked locally. Links are analyst declarations, not verified causal, legal or operational relationships."}


def render(outcome: dict) -> str:
    lines = ["# Supplied governance case links", "",
             "**Status:** AUTHOR-DECLARED CASE MAP; no LAIF assessment, legal finding or control-effectiveness verdict.",
             f"**Case:** {safe(outcome['case_id'])}",
             f"**Question:** {safe(outcome['question'])}",
             f"**Analyst (self-reported):** {safe(outcome['analyst_id'])}",
             f"**Manifest SHA-256:** {outcome['manifest_sha256']}", "",
             "## Supplied records by role", "",
             "A missing role means no record was declared in this manifest; it does not show the record does not exist elsewhere.", ""]
    for role in ROLES:
        lines.append(f"- **{role}:** {outcome['roles'][role]}")
    lines += ["", "## Source identities", ""]
    for source in outcome["sources"]:
        lines.append(f"### {safe(source['id'])} — {safe(source['role'])}")
        lines.append("")
        if source["status"] == "SUPPLIED":
            lines += [f"- File: {safe(source['file'])}", f"- Version (declared): {safe(source['version'])}",
                      f"- Origin (declared): {safe(source['origin'])}",
                      f"- SHA-256 (local bytes matched): {source['sha256']}"]
        else:
            lines += [f"- Not supplied: {safe(source['reason'])}"]
        lines.append("")
    lines += ["## Declared links", "",
              "Exact quotes below are checked against supplied UTF-8 source bytes. Their presence does not establish that one record implements, tests or remedies another.", ""]
    if not outcome["links"]:
        lines += ["No links declared. Record the missing relationship and source before drawing a conclusion.", ""]
    for link in outcome["links"]:
        lines += [f"### {safe(link['id'])}: {safe(link['from'])} → {safe(link['to'])}", "",
                  f"- Declared relationship: {safe(link['relationship'])}",
                  f"- Status: {link['status']}",
                  f"- Analyst note: {safe(link['note'])}"]
        for side in ("from", "to"):
            if link[side + "_quote"] is not None:
                lines += [f"- {side} exact text:", "", blockquote(link[side + "_quote"]), ""]
        lines.append("")
    lines += ["## What to check next", "",
              "Inspect each source in context, verify declared versions and authority, and obtain records marked NOT_SUPPLIED or NOT_DECLARED where relevant. Review the asserted relationships and any contradictory material with the responsible people. Use the separate LAIF assessment and assurance tools for their respective questions; this map does not import a finding.", ""]
    return "\n".join(lines)


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="laif.case-links.v1 JSON with user-declared sources and links")
    parser.add_argument("--evidence-root", type=Path, help="root for relative source files; defaults to manifest directory")
    parser.add_argument("--report", type=Path, help="write a new Markdown case map; refuses overwrite")
    parser.add_argument("--json", action="store_true", help="print checked structured case data instead of Markdown")
    args = parser.parse_args(argv)
    try:
        manifest_path = args.manifest.expanduser().resolve()
        manifest_bytes = manifest_path.read_bytes()
        manifest = read_manifest(manifest_bytes)
        evidence_root = (args.evidence_root or manifest_path.parent).expanduser().resolve()
        sources_by_id = local_source_bytes(manifest, evidence_root)
        outcome = assess_bytes(manifest, manifest_bytes, sources_by_id)
        text = json.dumps(outcome, indent=2, ensure_ascii=False, sort_keys=True) + "\n" if args.json else render(outcome)
        if manifest_path.read_bytes() != manifest_bytes:
            raise ValueError("case manifest changed during processing; no report written")
        if local_source_bytes(manifest, evidence_root) != sources_by_id:
            raise ValueError("source bytes changed during processing; no report written")
        if args.report is not None:
            target = args.report.expanduser().resolve()
            if target == manifest_path or any(target == (evidence_root / row["file"]).resolve()
                                              for row in outcome["sources"] if row["status"] == "SUPPLIED"):
                raise ValueError("report path overlaps a source or manifest")
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
            print(f"Case map saved: {target}")
        else:
            print(text, end="")
        return 0
    except (ValueError, OSError, UnicodeError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    raise SystemExit(run())
