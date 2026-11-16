# Current verified state

Reconciled **16 November 2026, 19:16 Canberra (AEDT)**. Owner: LAIF delivery lead.
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

[Public reading room](https://laif-public-guide.mick353.chatgpt.site): **v1**,
source `dde7238d759cce062d28e763a0dbb223e05dcfca`, deployment
`appgdep_6afab9b657dc81918a37ed1cbf57cdff`, succeeded 19:07 Canberra. Anonymous
HTTP 200 returned the guide without sign-in; live browser readback passed.
The static site has no document upload or analysis endpoint. It includes an
interactive example, eight documentary ceilings, retained report links and
an honest NIST/OECD comparison. Keyboard walkthrough and 390-pixel reflow were
checked locally; no physical-phone or screen-reader result is implied.

[Private Research Workspace](https://laif-research-workspace.mick353.chatgpt.site):
**v18**, source `2f762fb0a58f9dfa6a9eac68b4d7f55c380f6d3c`, deployment
`appgdep_6afabb1441b081918e0aba88e020f14d`, succeeded 19:13 Canberra.
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

Fresh hosted synthetic run `9561ab12-5fec-4357-a62c-e3b47ca1544e` used the
merged engine, verified all 28 runtime files and eight source quotations, produced
eight criterion judgments, saved and survived reload. Downloaded Markdown and
JSON were read and checked: [export receipt](2026-11-16-hosted-acceptance.md).
The run remains `DRAFT_REVIEW_REQUIRED`; no operator or legal attestation was
fabricated. Previous runs retain their original method and report.

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
