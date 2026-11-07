"""Authored, source-specific acceptance annotations; not an accuracy gold standard."""
import json
from pathlib import Path
from scripts import laif_research_report as research

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'tests/fixtures/real_source_reporting.json').read_text(encoding='utf-8'))


def case_review(key):
    manifest = json.loads((ROOT / 'docs/verified/manifests' / (key + '.json')).read_text(encoding='utf-8'))
    source = ROOT / 'docs/verified/raw' / manifest['raw_filename']
    dossier = research.build_dossier(source, max_quotes=12)
    review = research.review_template(dossier)
    findings = []
    for index, case in enumerate(CASES[key], 1):
        matches = [row for row in dossier['evidence'] if case['anchor'] in ' '.join(row['exact_quote'].split())]
        if len(matches) != 1:
            raise AssertionError(f'{key}: expected one exact-source witness for {case["anchor"]!r}, got {len(matches)}')
        findings.append({
            'finding_id': f'F{index:03d}', 'claim_type': 'INFERENCE',
            'statement': case['statement'], 'evidence_ids': [matches[0]['evidence_id']],
            'counterevidence_ids': [], 'criterion_ids': case['criterion_ids'],
            'alternative_explanations': ['Other provisions or operational evidence may establish stronger or qualified protection.'],
            'limitations': 'Authored development acceptance annotation. Not independent legal review, a complete LAIF assessment or proof of implementation.',
            'analyst_id': 'Work-Codex-source-reporting-acceptance-2026-11-07',
        })
    review['findings'] = findings
    return manifest, source, review
