#!/usr/bin/env python3
"""Verify the public website index or import an explicitly authorised source proposal.

The website index is a discovery layer. It never admits a verified corpus source,
changes LAIF scoring, or turns uploaded diagnostics into canonical assessments.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA = 'laif.site-source-index.v1'
SUBMISSION = 'laif.site-source-submission.v1'
MAX_SOURCE = 8_000_000
MAX_PACKAGE = 16_000_000
ROOT = Path(__file__).resolve().parents[1]
INDEX = Path('docs/site/source-index.json')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    if path.stat().st_size > MAX_PACKAGE:
        raise ValueError('JSON package exceeds 16 MB.')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Non-finite JSON.')))


def checked_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or '\\' in relative or '..' in relative.split('/'):
        raise ValueError('Invalid source path.')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError('Source path escapes repository.')
    return path


def verify(root: Path) -> dict:
    index = read_json(root / INDEX)
    if index.get('schema') != SCHEMA or not isinstance(index.get('sources'), list):
        raise ValueError('Unsupported site source index.')
    ids = set()
    count = 0
    for source in index['sources']:
        if source['id'] in ids:
            raise ValueError('Duplicate source ID.')
        ids.add(source['id'])
        data = checked_path(root, source['repoPath']).read_bytes()
        if len(data) > MAX_SOURCE or digest(data) != source.get('sha256'):
            raise ValueError(f"Source hash/size mismatch: {source['id']}")
        explanation = source.get('explainer')
        if explanation:
            if explanation.get('source_sha256') != source['sha256']:
                raise ValueError('Explanation names a different source hash.')
            text = data.decode('utf-8')
            for quote in explanation.get('quotes', []):
                start, end = quote.get('start_char'), quote.get('end_char')
                if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
                    raise ValueError('Invalid quote offsets.')
                if text[start:end] != quote.get('exact_quote'):
                    raise ValueError(f"Explanation quote mismatch: {source['id']}")
                count += 1
    return {'sources': len(ids), 'verified_explanation_quotes': count}


def import_submission(root: Path, package: Path, acknowledge: bool) -> dict:
    if not acknowledge:
        raise ValueError('Use --acknowledge-publication only after the owner authorises public source publication.')
    value = read_json(package)
    consent = value.get('publication_consent', {})
    if value.get('schema') != SUBMISSION or consent != {'repository': 'mick353/LAIF', 'visibility': 'public', 'acknowledged': True}:
        raise ValueError('A public LAIF source contribution acknowledgement is required.')
    source = value.get('source', {})
    filename = source.get('file_name', '')
    if not re.fullmatch(r'[A-Za-z0-9_. ()-]+\.(md|txt|markdown|pdf)', filename, re.I):
        raise ValueError('Use a safe PDF, Markdown or text filename without directories.')
    has_text, has_binary = 'text' in source, 'binary_base64' in source
    if has_text == has_binary:
        raise ValueError('Supply exactly one original source encoding.')
    if has_binary:
        data = base64.b64decode(source['binary_base64'], validate=True)
        if not filename.lower().endswith('.pdf') or not data.startswith(b'%PDF-'):
            raise ValueError('PDF source signature/filename mismatch.')
    else:
        if filename.lower().endswith('.pdf') or not isinstance(source['text'], str):
            raise ValueError('Text source encoding/filename mismatch.')
        data = source['text'].encode('utf-8')
    sha = digest(data)
    if not data or len(data) > MAX_SOURCE or sha != source.get('sha256'):
        raise ValueError('Original source hash or size mismatch.')
    index = read_json(root / INDEX)
    existing = next((s for s in index['sources'] if s['sha256'] == sha), None)
    if existing:
        return {'status': 'already_indexed', 'source_id': existing['id'], 'sha256': sha}
    title = source.get('name')
    if not isinstance(title, str) or not title.strip() or len(title) > 250:
        raise ValueError('A source title of 1–250 characters is required.')
    assessments = value.get('assessments', [])
    if not isinstance(assessments, list) or len(assessments) > 25:
        raise ValueError('At most 25 associated proposed assessment records are allowed.')
    for assessment in assessments:
        if assessment.get('sourceSha256') != sha:
            raise ValueError('Assessment names different source bytes.')
        if not re.fullmatch(r'[a-f0-9]{40}', assessment.get('revision', '')):
            raise ValueError('Assessment must name an immutable engine revision.')
    folder = Path('docs/site/submissions') / sha[:20]
    source_path = folder / ('source.pdf' if has_binary else 'source.md')
    destination = checked_path(root, str(source_path))
    # Validation is complete before any source, proposal, or index write.
    destination.parent.mkdir(parents=True, exist_ok=False)
    destination.write_bytes(data)
    (destination.parent / 'proposal.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    item = {'id': 'contributed-'+sha[:20], 'name': title.strip(), 'organisation': 'Source contributor',
            'fileName': source_path.name, 'version': source.get('version') or 'Unspecified',
            'scope': source.get('scope') or 'unknown', 'sourceUrl': source.get('declared_source_url') or '',
            'repoPath': str(source_path), 'sha256': sha, 'lifecycle': 'active',
            'status': 'Contributed source · origin unverified', 'origin': 'canonical',
            'reviewStatus': 'PROPOSED_SOURCE_NOT_VERIFIED_CORPUS',
            'manifest': {'verification_status': 'HASH_VERIFIED_LOCAL_ONLY', 'citation_status': 'NOT_ESTABLISHED',
                         'provenance_notes': 'Owner-authorised source proposal. Repository inclusion is not authoritative-origin admission, legal validation or a canonical assessment.'}}
    index['sources'].append(item)
    (root / INDEX).write_text(json.dumps(index, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return {'status': 'proposal_imported', 'source_id': item['id'], 'sha256': sha, 'source_path': str(source_path),
            'assessment_status': 'Proposed records retained in proposal.json; not promoted to canonical reports.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('verify')
    ingest = sub.add_parser('import')
    ingest.add_argument('package', type=Path)
    ingest.add_argument('--acknowledge-publication', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = verify(args.root) if args.command == 'verify' else import_submission(args.root, args.package, args.acknowledge_publication)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Site catalogue error: {error}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
