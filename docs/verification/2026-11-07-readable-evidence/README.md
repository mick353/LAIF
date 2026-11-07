# Readable source quotations — 7 November 2026

Base main: merged PR #105, `368334a346138b28e9735e71a464dca6fe9ff393`.
This pass fixes a reader-facing defect: character offsets and trace IDs were
standing in for usable quotations in parts of the report. Some curated passages
were flattened into long list items; other attributed passages were only in JSON.

## Actual reports

| Source | Fresh report | What is preserved |
|---|---|---|
| Australian DTA Policy v2.1 | [Assessment](au_dta_policy_v2_1/assessment.md) | All eight authored criteria, 22 criterion-linked excerpts and previously attributed reasoning; human-attested origin |
| Retained NIST AI RMF 1.0 | [Assessment](5f667a6f-NIST.AI.1001/assessment.md) | All eight authored criteria and 16 criterion-linked excerpts; local-hash-only DOCX-derived source |
| EU Regulation 2026/1744 | [Assessment](eu_ai_act_amendment_2026_1744/assessment.md) | Existing attributed determinations, amendment traces and original-Act article passages; source/version qualifications |

These are fresh renderings of retained reasoning. They are not new legal
opinions or independent reviews. Historical reports and review files remain
unchanged. Completed reviews here carry the current presentation fingerprint;
source, evidence, framework, Toolkit and criterion-protocol identities were
checked against the previous records before reissue. Authored findings and
criteria were carried unchanged and their source spans revalidated.

## Reader-visible changes

- Full curated passages appear as block quotations under their criterion.
- Attributed determinations quote their trace passages beside the reasoning;
  the summary table links directly to those passages.
- Submitted findings quote both supporting and nominated counterevidence.
- Evidence IDs link to quotations in the same report. The gap register links
  to admitted primary quotes and retained source mechanisms. All retained
  mechanism witnesses and structured rows are displayed.
- Locations show a source name where available, recorded PDF pages, extracted
  page markers, Markdown sections or extracted-text lines. Missing pagination
  is not invented. An extracted marker is not new original-PDF verification.
- Character offsets remain in JSON audit data. Display normalisation is labelled;
  exact source text remains intact. Source markup is inert in the new quotations.
- The independent source-bound scholarly renderer and standalone quote bank use
  the same presentation. Public samples were regenerated.

## Executed validation

- **228 targeted tests PASS**, including nine new reader-level tests and the
  existing processing, substantive-review, scholarly, portable-review and
  real DTA/EU reporting tests. [Log](targeted-tests.log).
- Fresh DTA, EU and NIST reports were executed with standard-library Python
  (`-S`); every report's evidence links resolve to unique local anchors.
  [Execution manifest](execution.json).
- All ten baseline assessment records are identical to main except the top-level
  toolchain fingerprint. [Comparison](baseline-preservation.json).
- **Full local gate PASS**, exit 0: **587 discovered tests** in 145.308 seconds
  plus the additional governance, corpus, source, provenance, adversarial,
  semantic and deterministic-report gates; no skips. [Full log](full-local-verification.log).
- Pinned Poppler 24.02.0 re-extraction passed for both regulatory PDFs, 45
  page-bounded quotations, eight original-Act passages and 16 attributed finding
  records. [Log](regulatory-reextraction.log).
- The documentation audit checked 70 active guides/fresh reports and 205 local
  file links without unresolved destinations. [Scope and results](documentation-audit.json).

The full gate ran on implementation commit `26c62f9` (tree
`a52b2a4f9bee959a8047eb86109bb907d7033c03`) in Work cloud Linux/Python 3.12.14.
No production code changed after the successful targeted and full runs. The
subsequent commit records results and documentation. Source spans, quotations
and link targets were checked; no observed non-specialist usability study is claimed.

The shared evidence renderer is now included in the toolchain fingerprint, so
changes to citation presentation invalidate stale generated output identities.
The actual-source regression fixtures explicitly revalidate historical authored
content against the current presentation fingerprint; old records are preserved.

~~~bash
python3 scripts/laif_verify.py --full --base-ref origin/main
python3 -S scripts/laif_verify_regulatory_ingestion.py --reextract
~~~

No scoring, detection, certification rules or substantive determinations changed.
Canonical PDF/raw files and the protected historical report are unchanged. The
text workflow requires no paid model API, user's PC or GitHub Actions. Python
3.10 and Windows are not executed in this pass. This is a software presentation
fix; independent legal, field-accuracy and usability validation remain separate.
