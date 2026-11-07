# PR #98 — regulatory ingestion and assessment review

**Executed:** 7 November 2026 (Australia/Sydney), in Work's cloud Python environment. **Branch:** `docs/authoritative-source-currency-20261107`, starting at `4170f1825f5b05e4085c99c837658da097275687`; main at `09f8687b58d1c5547cfe58bcf4e38aa7da3619a2`. No merge authorised or performed.

## Read the two assessments

- [Australian DTA Policy v2.1](au_dta_policy_v2_1.assessment.md): applicability, staged deadlines, exact v2.0 comparison and LAIF interpretation.
- [EU Regulation 2026/1744](eu_ai_act_amendment_2026_1744.assessment.md): operative amendment register, actor/date matrix and LAIF interpretation.

These are **authored draft assessments for PR review**, accompanied by retained machine outputs. They are kept in this dated verification record rather than presented as published/canonical `reports/` artefacts before source and semantic review. They do not revise the protected historical narratives. Human review remains outstanding. Neither successful ingestion nor software tests certify legal compliance or LAIF's scientific validity.

## Source identity and evidence

| Source | PDF SHA-256 | Pages | Checked source quotations | Authority verification |
|---|---|---:|---:|---|
| DTA v2.1 | `7da206ff9bb77c5c4505577ea2fd11367700b38f4ff8c4e4592501e95221e5c2` | 26 | 17 | Owner-attested official deposit; two direct upstream HTTP 503 responses; no upstream-byte equivalence claim |
| EU 2026/1744 | `0bea4d808256b08275777949ba9cb3c70b7d02e4ebb3ac9b205671b1f552d386` | 41 | 27 | Fresh official EUR-Lex download matches exact PDF bytes |

Full text is in `docs/verified/raw/`, manifests in `docs/verified/manifests/`, and exact offset/page-bounded quote JSON plus readable traces in `docs/verified/extracted/`. `*.pages.json` indexes every extracted page. `upstream_retrieval.json` records actual URL attempts and results. DTA origin is accepted under the existing human-attestation workflow, with the upstream limitation retained.

Extraction used Poppler `pdftotext 24.02.0 -layout -enc UTF-8`. All page text is retained, with only explicit page separators added. No word repair, paraphrase, OCR or synthetic substitute was used. Poppler emitted two DTA “Invalid Font Weight” warnings, retained in the page map; these are not hidden or treated as text validation. Exact trace spans and reproduced text hashes passed separately. Key DTA classification (p23) and EU application/transition (p35) pages were rendered and visually checked. This is not an exhaustive glyph-by-glyph comparison of 67 pages. Tables retain layout columns; the original PDF governs ambiguity.

The original EU Act admission remains with PR #90. The amendment is not a consolidated Act. DTA v2.0 and original EU PDF bytes remain unchanged; the DTA comparison records the baseline PDF hash and all old-page extraction hashes in `dta_version_delta.json`. Pages 7–22 match v2.1 ignoring whitespace; Appendix D is new on pp23–26. Linked external standards were not version-compared.

## Actual processing and reproducibility

- `pypdf-diagnostic/`: execution snapshot from the portable PDF runner (only Markdown trailing whitespace trimmed; JSON is unchanged), including source hashes, institutional report, technical appendix, analyst bundle and run manifest. pypdf 6.10.0 was already available; no installation or paid service was needed.
- `reviewed-text/`: second executed canonical-engine assessment of the committed Poppler extraction, with explicit source title/type and sector. Raw text identity and original PDF identity remain separate. The processor applies its existing text normalisation before assessment; tests verify the recorded assessed-text hash against that exact normalisation.
- The canonical toolchain fingerprint is `e0e3292e34444f18`. The four fingerprinted engine files are unchanged. Runtime metadata includes the original execution paths/timestamps; those paths are not dependencies.
- A repeat using `python -S` (site packages disabled) reproduced both complete assessment-result dictionaries exactly after excluding only the execution timestamp. Core and reviewed-text processing need no PDF package, model API, PC path, network service or Actions run.

**Machine-output limitations:** The inherited full-report template prints “September 2026” and a corpus-regeneration command; these are template text, not the execution date or command. Actual execution metadata is 7 November 2026 and the portable runner commands are recorded above. pypdf spacing damage affected EU classification; the cleaner route correctly recognises a binding legal instrument. Both documents still receive `ABSENT` functional-family labels and formal LAIF-native `FAIL` from the unchanged engine. These are rubric outputs, not evidence of absent legal protection or institutional failure. Whole-document signal saturation, incomplete machine-selected quote propositions and overconfident institutional-report wording remain limitations; the authored assessments explicitly qualify them and provide curated source evidence. No scoring rules were altered to force different findings.

## Portable commands

Run in any complete Python 3.10+ clone of this branch (Windows users can replace `python3` with `py -3`). Choose a fresh output directory outside repository `docs/`, `reports/` and `.git/`:

```bash
python3 scripts/laif_verify_regulatory_ingestion.py
python3 scripts/laif_process_regulatory_sources.py --verified-text --output-dir /tmp/laif-regulatory-review
python3 scripts/laif_verify.py --full --base-ref origin/main
```

Optional source-PDF re-extraction requires local Poppler (`pdftotext` on PATH), not an online service:

```bash
python3 scripts/laif_verify_regulatory_ingestion.py --reextract
```

The default PDF-processing route remains available with optional pypdf installed in a virtual environment:

```bash
python3 scripts/laif_process_regulatory_sources.py --output-dir /tmp/laif-pdf-review
```

The runner now preflights selected PDF SHA-256 pins and rejects missing/changed reviewed text before processing it. Evidence/report/Git descendants are rejected as output locations. Processing does not grant source admission: that decision is separately documented in provenance manifests. Existing supplied files, protected narratives, baseline corpus/scoring semantics, unrelated PRs and GitHub Actions configuration are preserved.

## Verification and review status

See [VALIDATION.md](VALIDATION.md) and retained logs for actual command outcomes. The repository's legacy `--check-evidence-traces` gate checks its fixed historical trace corpus; the new source-specific verifier and discovered tests additionally check these two PDFs, full raw hashes, all page boundaries and 44 exact quotation spans. Passing the legacy gate alone would not establish the new evidence checks.

Open PRs inspected: #89, #90, #94, #95, #96, #97 and #98. No other PR was changed. Scope expands #98 from source-currency documentation to source admission and separate draft assessments, explicitly for source/policy/legal review. No merge, published-report replacement, institutional implementation claim, empirical detector validation or full consolidated-law certification is included.
