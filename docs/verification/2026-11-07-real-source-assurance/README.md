# Whole-source reporting assurance — 7 November 2026

PR #102 was merged with approval to main at
`cce91f2558475276e35a953eecc108567aa37e74`, preserving its tested tree
`bb1f8d4ecf318dcc6147332153fb7c3101fb27bc`. This is a separate reporting
follow-up from that clean main. It remains a candidate until merged.

## Why the small sample was insufficient

The synthetic vendor policy tests import mechanics, source locking and output
plumbing. It cannot establish reporting quality on long laws, tables,
questionnaires, voluntary guidance or historical instruments. This pass uses
**every one of the seven retained raw corpus documents**, with no source removed
because it is awkward. The corpus is known and curated; it is not independent,
random or representative of every field.

The baseline sweep processed six documents. The original EU Act failed because
its manifest recorded the PDF hash but omitted the typed `source_file` path.
The transformation narrative already identified the preserved file. Adding the
path fixes the failure without changing the PDF, extract, authority or pending
substantive-assessment status.

## Changes

- Scan the full candidate stream and retain up to three spatially distributed
  witnesses per mechanism, with accepted/retained counts and explicit limits.
  The report shows one per type; the evidence JSON keeps all retained witnesses.
- Separate recommendation wording from other control wording. Neither label
  determines legal force. Reject “responsible” used only as an adjective as a
  supposed responsibility assignment.
- Keep Markdown questionnaire/framework rows separate from clean prose. Retain
  whole bounded rows and available column headings; do not interpret unselected
  “Provided / Not provided” or “Yes / No” options as observed answers.
- Withhold partial roman-list continuations and concatenated table fragments
  from the primary prose quote bank. Keep exact source text and offsets intact.
- Expose existing version, instrument status and source qualifications. EO 14110
  is explicitly historical/revoked; the original EU Act is not a consolidated
  edition. The EO status points to the official revocation record; local-hash
  provenance is not promoted by that separate status check.
- Check quote/control/row spans, evidence IDs, reference resolution, available
  column context and retained coverage counts before output writes.
- Correct active documentation: all four Integrity Layer properties where
  applicable; current release versus historical verification; source admissions;
  review import; evidence limits; cross-field uses and expansion priorities.

The nine source-control categories are retrieval aids, not the LAIF assessment
criteria. The eight criterion rows remain A.1–A.4, Q1, Q2, Q3 and Self-Application.
No numeric weights, formal verdict rules, canonical texts or protected historical
assessment conclusions are changed.

## Actual whole-source outputs

Each linked directory contains an actual generated report, technical appendix,
completed source-bound acceptance review and `report-evidence.json`. The JSON
retains every selected prose quote, control witness, structured row and submitted
finding. All 14 submitted findings are authored development annotations, with
alternatives and limitations. They are deliberately narrow; they are not seven
complete substantive LAIF assessments or independent expert determinations.

| Source | Report | Provenance limitation retained |
|---|---|---|
| OECD Recommendation | [Generated review](51a29205-OECD_Legal_Instruments/51a29205-OECD_Legal_Instruments.laif.md) | Local extracted-file hash; upstream equivalence not proven |
| NHS DTAC 2.0 | [Generated review](55eccce3-DTAC_Form_2.0_February_2026/55eccce3-DTAC_Form_2.0_February_2026.laif.md) | Questionnaire template; supplier answers not inferred |
| NIST AI RMF 1.0 | [Generated review](5f667a6f-NIST.AI.1001/5f667a6f-NIST.AI.1001.laif.md) | User-supplied DOCX transform; original-PDF equivalence not proven |
| Australian DTA policy v2.1 | [Generated review](au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md) | Human-attested authoritative origin, distinct from byte-matched upstream retrieval |
| Historical EO 14110 | [Generated review](b0ef43db-202324283/b0ef43db-202324283.laif.md) | Revoked instrument; dated wording is not current authority |
| Original EU Act 2024/1689 | [Generated review](eu-ai-act-2024-1689/eu_ai_act_2024_1689.laif.md) | Original OJ edition; complete substantive assessment still pending |
| EU amendment 2026/1744 | [Generated review](eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md) | Version-specific amendment; not a current consolidated-law certificate |

[Execution manifest and hashes](corpus-execution.json).
The pre-existing complete, attributed DTA/EU assessments and curated evidence
remain in the [regulatory record](../2026-11-07/regulatory/README.md).

## Verification

**Final full local gate: PASS**, exit 0, with **535 discovered tests** and all additional governance, corpus, format, provenance, semantic, adversarial and deterministic-report gates. There were no skipped checks or tests in this run. See [full log](full-local-verification.log).

- **Seven whole-source workflow tests PASS within the full gate**, with 28 standard-library CLI executions across default processing, source-bound review import, preview and invalid-evidence rejection.
- **Thirteen new integrity/retrieval tests PASS**, targeted and again in the full gate. [Targeted log](integrity-tests.log).
- **Seven additional captured reviewed-source runs PASS** with 14 source-specific authored findings. [Capture log](corpus-capture.log) and [execution manifest](corpus-execution.json).
- **Regulatory re-extraction PASS:** both PDF/raw identities, complete page maps, 45 page-bounded quotations, eight original-Act passages and 16 authored regulatory records; Poppler reproduces raw extracts byte for byte. [Source log](regulatory-source-verification.log).
- **Ten baseline records preserved:** complete generated JSON identical except the top-level toolchain fingerprint. [Comparison](baseline-preservation.json).
- **169 Markdown files inventoried:** active guidance checked for local file links, with no unresolved active local destinations. Stale release/source claims and three-property summaries corrected; dated records and source text retained. [Inventory and scope](documentation-audit.json).
- **Notion reconciled:** project state, independent-study work item and a practical-use guide updated. [Record and links](notion-sync.md). Current Windows-host parity and scheduled sync remain unverified.

Reproduce the whole-source workflow regression:

```bash
python3 -m unittest discover -s tests -p test_real_source_reporting.py
python3 -m unittest discover -s tests -p test_source_scan_integrity.py
python3 -S scripts/laif_verify_regulatory_ingestion.py --reextract
python3 scripts/laif_verify.py --full --base-ref origin/main
```

The whole-source suite runs default and reviewed processing, no-write preview
and invalid-evidence rejection for each source (28 CLI executions). Source-
specific acceptance expectations are in
[`tests/fixtures/real_source_reporting.json`](../../../tests/fixtures/real_source_reporting.json).
Tests also check exact offsets, report/JSON/bundle agreement, all eight criterion
rows, unassessed criteria, source-status limits, retained table context and
unchanged scores/attributed regulatory reasoning.

The first targeted whole-source run failed four assertions because the test
expected raw punctuation where the report correctly escaped Markdown. Those
assertions were corrected to inspect the displayed text. Its 28 CLI executions
completed; that initial run is not recorded as a passing suite. The first full
run then found one test-quality failure: a positive-path integrity test lacked
an explicit assertion. That test now explicitly asserts successful return. The
final full gate reran all 535 discovered tests and passed. No production check
was bypassed or disabled.

[Baseline preservation](baseline-preservation.json) compares the complete
10-document generated JSON against merged main, excluding only the top-level
toolchain fingerprint. All other fields are identical. Source PDF/raw bytes,
framework texts and protected reports are preserved.

## Reporting quality and remaining work

The reporting path is more useful for professional assisted review: evidence is
traceable, source caveats survive into the report, control candidates are
credited, table choices are not treated as facts and analyst claims retain their
basis and limits. It still cannot decide from matching text alone whether a
protection is equivalent, a legal exception applies or a real control works.

Independent accuracy, reliability against human experts, completeness of legal
interpretation and usefulness to non-specialists remain unmeasured. No live AI
system, agent containment or institutional operational outcome was tested.
An unfamiliar holdout corpus, blind independent readers, matched checklist/search
baselines and observed review tasks are the next evidence step. See the
[use-case and expansion guide](../../product/USE_CASES.md).

Work cloud Linux/Python 3.12.14 was used. Text processing and every matrix CLI run
use standard-library Python (`-S`); no paid model API, GitHub Actions or user's PC
is needed. The separately executed PDF re-extraction gate uses local Poppler.
Windows and Python 3.10 runtime execution were not performed in this pass.
