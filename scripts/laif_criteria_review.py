"""Source-bound authored criterion reviews; no scoring or certification."""
from __future__ import annotations
import datetime as dt
import re
from laif_spec import ASSESSMENT_CRITERIA

DETERMINATIONS = ('SUPPORTED_IN_SCOPE', 'PARTIAL_SUPPORT', 'NOT_ESTABLISHED', 'SOURCE_CONFLICT', 'NOT_APPLICABLE')
FIELDS = ('reasoning', 'framework_basis', 'applicability_reason', 'scope_and_exceptions', 'alternative_explanation', 'closure_evidence')
CONTEXT = ('analyst_id', 'as_at_date', 'jurisdiction', 'assessed_role', 'document_scope', 'overall_reasoning', 'limitations')


def validate_criteria_review(value: object, text: str) -> dict | None:
    """Validate records and exact spans, not an author's interpretation."""
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError('criteria_review must be an object')
    if any(not isinstance(value.get(k), str) or not value[k].strip() for k in CONTEXT):
        raise ValueError('criteria_review requires author, date, jurisdiction, role, scope, overall reasoning and limits')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value['as_at_date']):
        raise ValueError('criteria_review date must be YYYY-MM-DD')
    dt.date.fromisoformat(value['as_at_date'])
    rows = value.get('criteria')
    if not isinstance(rows, list) or not 1 <= len(rows) <= len(ASSESSMENT_CRITERIA):
        raise ValueError('criteria_review requires 1-8 criterion records')
    seen, ids, output = set(), set(), []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('criterion record must be an object')
        cid = row.get('criterion_id')
        if not isinstance(cid, str) or cid not in ASSESSMENT_CRITERIA or cid in seen:
            raise ValueError('criterion IDs must be supported and unique')
        seen.add(cid)
        if row.get('determination') not in DETERMINATIONS:
            raise ValueError('unsupported documentary determination; PASS/FAIL certification is not imported')
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in FIELDS):
            raise ValueError(f'{cid}: reasoning, framework basis, applicability, scope, alternative and closure evidence required')
        excerpts = row.get('source_excerpts')
        if not isinstance(excerpts, list) or not 1 <= len(excerpts) <= 12:
            raise ValueError(f'{cid}: 1-12 source excerpts required')
        checked = []
        for e in excerpts:
            if not isinstance(e, dict):
                raise ValueError('source excerpt must be an object')
            eid = e.get('evidence_id')
            if not isinstance(eid, str) or not re.fullmatch(r'C\d{3,5}', eid) or eid in ids:
                raise ValueError('curated source evidence requires globally unique C001-style IDs')
            ids.add(eid)
            start, end, quote = e.get('start_char'), e.get('end_char'), e.get('exact_quote')
            if (type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text)
                    or not isinstance(quote, str) or not quote.strip() or text[start:end] != quote):
                raise ValueError(f'{eid}: curated quotation differs from its exact extracted-source span')
            if not isinstance(e.get('context'), str) or not e['context'].strip():
                raise ValueError(f'{eid}: source context required')
            checked.append({**{k:e[k] for k in ('evidence_id','exact_quote','start_char','end_char','context')},
                            'evidence_status':'EXACT_EXTRACTED_TEXT_ONLY_CONTEXT_REQUIRES_REVIEW'})
        item = {k:row[k].strip() for k in ('criterion_id','determination',*FIELDS)}
        item['source_excerpts'] = checked
        if cid == 'Q1':
            c = row.get('coupling')
            if (not isinstance(c, dict) or c.get('q1a') not in ('NONE','IMPLICIT','EXPLICIT','UNKNOWN')
                    or c.get('q1b') not in ('NONE','SOFT','HARD','UNKNOWN')):
                raise ValueError('Q1 requires explicit Q1a/Q1b classifications')
            for k in ('protected_interest','restriction','equivalent_normative_force'):
                if not isinstance(c.get(k),str) or not c[k].strip():
                    raise ValueError('Q1 requires the interest, restriction and equivalent-force reasoning')
            if row['determination']=='SUPPORTED_IN_SCOPE' and (c['q1a'] in ('NONE','UNKNOWN') or c['q1b'] in ('NONE','UNKNOWN')):
                raise ValueError('affirmative Q1 source support conflicts with absent or unknown pairing/force')
            item['coupling'] = {k:c[k] for k in ('q1a','q1b','protected_interest','restriction','equivalent_normative_force')}
        output.append(item)
    return {**{k:value[k].strip() for k in CONTEXT},'criteria':output,
            'coverage':[{'criterion_id':k,'status':'AUTHOR_DETERMINATION_SUPPLIED' if k in seen else 'NOT_ASSESSED'} for k in ASSESSMENT_CRITERIA],
            'all_criteria_addressed':len(seen)==len(ASSESSMENT_CRITERIA),
            'review_status':'SOURCE_BOUND_AUTHOR_ASSESSMENT_NOT_INDEPENDENTLY_VERIFIED',
            'boundary':'All-criteria coverage means records were supplied, not that the Integrity Layer or Coherence Test passes. Exact quotations do not validate applicability, reasoning, legal force or control operation.'}


def criterion_template() -> dict:
    """Empty records require author evidence and reasoning before import."""
    rows=[]
    for cid in ASSESSMENT_CRITERIA:
        row={'criterion_id':cid,'determination':'',**{k:'' for k in FIELDS},'source_excerpts':[]}
        if cid=='Q1':
            row['coupling']={'q1a':'UNKNOWN','q1b':'UNKNOWN','protected_interest':'','restriction':'','equivalent_normative_force':''}
        rows.append(row)
    return {**{k:'' for k in CONTEXT},'criteria':rows}
