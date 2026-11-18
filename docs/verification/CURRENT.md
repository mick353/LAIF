# Current verified state

## 18 November 2026 follow-through

Repository main `d9bfdaa` includes released PRs #131–134. PR #131 fixes
interruption after report generation so saved outputs and resume instructions
are reported accurately. PR #132 adds the reproducible NIST cited-prose
check: 16/16 retained excerpts match raw spans and normalized official PDF
wording. PR #133 is the explicitly approved additive NIST trace erratum;
eight clause descriptions were incorrect. Historical sources, trace and
assessment remain unchanged; the erratum does not regrade NIST or promote
source status. See the [quotation receipt](2026-11-18-nist-cited-prose/README.md)
and [erratum](2026-11-18-nist-trace-erratum/README.md).

PR #134 adds [explicit case links](../product/CASE_LINKS.md): declared
policy/contract/procedure/test/incident/remedy records, byte identities,
optional exact UTF-8 quotations, declared relationships and explicit unsupplied
roles. Its pure Python validator and renderer support both local files and
browser-supplied bytes. It does not infer legal force, contradictions or
operating controls. The exact candidate passed 657 tests with two explicit
Windows symlink skips; focused case tests passed 8/8. The subsequent erratum
merge changes three documentation files only and passed focused readback.

Private Site **v20**, source `aad6e3d1ab91cdd9cb1bb518bb820ecf3e7cb437`,
deployment `appgdep_6afd0bb81bb881919e9ceae5a5bd59d9`, succeeded with owner-only
access. It adds saved case maps using the exact merged Python helper; the
assessment engine remains `e7594d3`. Browser-runtime and CLI case results were
byte-identical and stale source bytes were rejected. TypeScript, production
build, persistence/API and existing assessment-runtime checks passed.
The public guide remains v2.

Signed-in v20 acceptance created a synthetic case with a pinned policy source,
an explicitly unsupplied test record and a declared policy-to-test link/note.
After "All changes saved" and reload, the map ID, question, missingness reason,
relationship and note persisted. The shared Python worker checked the revision
and reported the unsupplied endpoint. At 320 CSS pixels the case page had
`scrollWidth = clientWidth = 305`; export buttons fit. Hosted case-export file
bytes were not captured because the browser download interface did not emit
a receipt. Local Site/CLI parity and export tests passed; neither proves that
last hosted download step. No export failure was observed.

Before this release, bounded keyboard checks reached all nine private v19
sections at 320 CSS pixels without body overflow; the public guide also had
no body overflow. Escape focus return and selected focus outlines were checked.
These observations do not establish true zoom, screen-reader or physical-phone
acceptance. Existing hosted export evidence below remains a dated v18 receipt.

Normal publisher-byte retrieval for the Ombudsman March 2025 PDF and DTAC
DOCX still returned HTTP 403 on 18 November. No source bytes were acquired or
verification status upgraded. Independent substantive review of NIST mappings,
EU applicability/assessment, intended-user and operational evidence remain open.
Automatic relationship discovery and contradiction adjudication are not part
of the declared case-map increment; they remain separate engineering/research
scope, not completed or merely awaiting a human click.

## Earlier integrated release and acceptance

Reconciled **16 November 2026, 23:12 Canberra (AEDT)**. Owner: LAIF delivery lead.
This is a dated checkpoint. See [delivery tasks](OVERHAUL_TASKS.md) and the
[historical evidence index](INDEX.md).

## Released repository work

Engine revision `e7594d3b98dcea75a06cb6b73d1a0e3d3a7177ce`, merged
[PR #128](https://github.com/mick353/LAIF/pull/128). Documentation-only
follow-ups can share this tested engine identity.

- [PR #125](https://github.com/mick353/LAIF/pull/125): removed four exact duplicate
  aliases (336,837 bytes), retaining all unique reports and current outputs.
  [Hashes and retained paths](2026-11-16-deduplication.json). CLAUDE is under
  8 KB; detailed guidance is linked. Browser/local guides remain separate.
- [PR #126](https://github.com/mick353/LAIF/pull/126): locked Codex exploratory
  predictions, five full retained sources, eight criteria, exact real-text
  deletions and all failures. [Results](../research/overhaul-current/README.md).
- [PR #127](https://github.com/mick353/LAIF/pull/127): ten engine modules and
  compatibility API. Corpus Markdown was byte-identical; JSON changed only its
  truthful source fingerprint. [Comparison](2026-11-16-engine-module-split.md).
- PR #128: separate plain reader summaries, a summary-only jargon gate and ten
  repaired current-report navigation links. Canonical authored reasoning is
  unchanged. Four historical link defects retain their original evidence bytes.
  [Navigation record](2026-11-16-report-navigation.md).

Final integrated full local gate: **645 tests, two explicit Windows symlink
capability skips**, plus corpus/provenance, adversarial, semantic-fidelity and
byte-identical double report regeneration. No GitHub Actions ran. The initial
readability gate found a missing assertion in a new test; it was fixed before
this successful final run. Software verification does not establish independent
accuracy, legal compliance or working operational controls.

## Live Sites and acceptance

[Public reading room](https://laif-public-guide.mick353.chatgpt.site): **v2**,
source `61b815b3c30c422a59888341067a991d7b849d37`, deployment
`appgdep_6afaf2bc69508191ac34ec7f810316b4`, succeeded 23:10 Canberra.
Live browser readback confirmed the public companion explanation and direct
main-workspace link. Anonymous HTTP 200 was established at v1.
The static site has no document upload or analysis endpoint. It includes an
interactive example, eight documentary ceilings, retained report links and
an honest NIST/OECD comparison. Keyboard walkthrough and 390-pixel reflow were
checked locally; no physical-phone or screen-reader result is implied.

[Private Research Workspace](https://laif-research-workspace.mick353.chatgpt.site):
**v19**, source `e79e534fbfb38a53d1258ee4dacc67cc8b3aab234`, deployment
`appgdep_6afaf2881d9c8191833c3b0a30d72eba`, succeeded 23:10 Canberra.
The 28-file browser runtime pins the merged engine revision above. Access
readback remains one owner and zero external visitors. Signed-in sources and
review records are saved in private cloud storage; browser computation does
not mean documents stay only on the device.

Site checks passed for storage/API isolation, source catalogue, decisions,
extraction, review brief, automatic criteria, plain summaries, report rendering,
TypeScript and production build. WebAssembly Python processed DTA, LAIF,
synthetic PDF and policy fixtures; source/quotation identity and negative
path/source checks passed. Local browser inspection confirmed separate summaries
and expandable original authored wording.

At v18, fresh hosted synthetic run `9561ab12-5fec-4357-a62c-e3b47ca1544e` used the
merged engine, verified all 28 runtime files and eight source quotations, produced
eight criterion judgments, saved and survived reload. Downloaded Markdown and
JSON were read and checked: [export receipt](2026-11-16-hosted-acceptance.md).
The run remains `DRAFT_REVIEW_REQUIRED`; no operator or legal attestation was
fabricated. Previous runs retain their original method and report.

The v19 interface pass preserves the engine and saved records. The source view
shows document/edition; assessment and evidence steps open their corresponding
views. Selecting an older run survives the source-to-assessment round trip.
Canberra timestamps and short IDs distinguish repeated runs. Duplicate intake
opens the existing source. Both Sites explain their roles and link to each other.
Live browser inspection preserved older run `9578d1db-efd3-48e7-bafe-6ccef52bcf4f`
through that round trip and opened quoted evidence. Focused navigation,
storage/API isolation, source catalogue, decisions, extraction, review brief,
guidance, summaries and rendering checks passed, with TypeScript and production
build. Public static checks and local mobile reflow passed. The unchanged
engine's full gate was not repeated for this interface-only pass.

## Remaining evidence-dependent acceptance

| Item / owner | State and next step |
|---|---|
| Intended-user acceptance / product owner | Fresh owner-document review, recovery, physical phone and screen reader remain unobserved. Synthetic browser checks do not replace these. |
| Preferred comparator intake / source custodian | Ombudsman March 2025 guide edition verified, but normal PC byte retrieval returned HTTP 403. Supply publisher PDF bytes or wait for working authoritative retrieval. Current comparison openly uses retained NIST/OECD. |
| Independent assessment validity / research owner | Unblinded Codex predictions are exploratory; independent adjudication and empirical control-effectiveness evidence remain absent. |
| Source/legal gates / source custodian | Original EU Act assessment, NIST fidelity qualifications and DTAC upstream identity remain separately tracked in issue #93. |

[Issue #110](https://github.com/mick353/LAIF/issues/110) remains open for user
acceptance; [issue #93](https://github.com/mick353/LAIF/issues/93) remains open
for source/legal evidence. These are not software fixes that a passing build
can establish. Untracked owner attachments are preserved.
