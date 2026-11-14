# NIST AI RMF 1.0 assessed-text fidelity check — 14 November 2026

## Question and evidence tier

Does the NIST text used by LAIF's retained assessment agree with the preserved
official NIST AI 100-1 PDF at the numbered category/subcategory level?
This is a local source-text comparison on branch
`source/nist-pdf-fidelity-20261114`, based on `origin/main` at
`4f58bdb631d2c76836c8fdf48878104c3f49a685`. It is not a new LAIF
assessment, independent legal review, official endorsement or proof of a
deployed control.

The [30 October source receipt](../2026-10-30/OPERATIONAL_DOCUMENT_SMOKE.md)
records a direct download from the [NIST publication page](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
and [official PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf):
1,946,127 bytes, SHA-256
`7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`.
That hash equals the preserved 48-page
[`NIST.AI.100-1.pdf`](../../verified/manual_ingest/NIST.AI.100-1.pdf).
This check compares that PDF with both the retained
[`raw Markdown`](../../verified/raw/5f667a6f-NIST.AI.1001.md) and
[`assessed supporting Markdown`](../../supporting/5f667a6f-NIST.AI.1001.md).
The two Markdown files have identical SHA-256:
`44ac320e6da1d15fcfded2933da7f62bf0ed552b78a81358102c057991ba6509`.
The original user-supplied DOCX has a different file format and is retained
unchanged.

## Reproduce

In a Python environment with optional `pypdf` installed, run from the
repository root:

```sh
python3 docs/verification/2026-11-14-nist-pdf-fidelity/verify.py
```

The committed [machine result](result.json) was produced on Windows with
Python 3.11 and `pypdf` 6.18.0 using the exact pinned PDF and Markdown bytes.
The script prints JSON and exits nonzero if source hashes, the 19 category
comparisons, the 72 subcategory comparisons or the stated prose-window result
change. It does not fetch a URL, call an AI model or use GitHub Actions.

## Comparison method and result

The verifier extracts all PDF pages using `pypdf.PdfReader.extract_text()`.
It finds `GOVERN`, `MAP`, `MEASURE` and `MANAGE` category and numbered
subcategory identifiers in both texts. For each body, it removes adjacent
table headings and continuation labels, joins PDF line-break hyphenation,
lowercases and strips punctuation, symbols and whitespace. Duplicate IDs
cause failure. The comparison therefore tests **alphanumeric wording and
coverage of the numbered table entries**, not typography or page layout.

| Check | Result | Scope |
| --- | --- | --- |
| Category descriptions | 19/19 exact after stated normalisation | Tables 1–4, `GOVERN` 1–6, `MAP` 1–5, `MEASURE` 1–4, `MANAGE` 1–4 |
| Numbered subcategory clauses | 72/72 exact after stated normalisation | All numbered entries in Tables 1–4; no missing or duplicate IDs |
| Other long non-table Markdown lines | 583/585 100-character alphanumeric windows found in PDF extraction | Diagnostic coverage check, not a full-document equivalence proof |

The two unmatched prose windows are at raw line **113**, offset **300**
(a duplicated Figure 3 caption at the join between the repeated copies),
and raw line **388**, offset **0** (a duplicated publication footer). The
substantive text of both appears in the PDF; the repeated concatenations are
DOCX extraction artefacts. They are outside the numbered table clauses.
The comparison removes PDF page headers before joining line-break hyphenation;
without that step, page boundaries create four additional false mismatches.

## Meaning and remaining limits

The exact category and subcategory matches materially strengthen fidelity for
the NIST Core tables used by the assessment, beyond the earlier broad token
overlap. They do not prove that every prose paragraph, figure, table geometry,
punctuation mark, appendix or DOCX property matches the official PDF. The
100-character windows sample long non-table lines; they are not a line-by-line
proof. A final source-admission decision should additionally inspect the
assessment-cited prose and figures in PDF context and review any consequential
differences before changing the [NIST source manifest](../../verified/manifests/5f667a6f-NIST.AI.1001.json).
The manifest's `HASH_VERIFIED_LOCAL_ONLY` status remains unchanged here.

For DTAC, the [current NHS England page](https://digital.nhs.uk/services/digital-technology-assessment-criteria-dtac)
links the exact `dtac_form_2.0_february_2026.docx` download and advises users
to download at point of use. The official binary URL is
`https://digital.nhs.uk/binaries/content/assets/website-assets/services/dtac/dtac_form_2.0_february_2026.docx`.
A direct automated download on 14 November 2026 returned HTTP 403, so no
upstream byte comparison was possible. The retained DTAC document and its
`HASH_VERIFIED_LOCAL_ONLY` status remain unchanged. To close that gate, an
authorised browser download of the official DOCX must be hashed and compared
with the retained `DTAC_Form_2.0_February_2026.docx` (local SHA-256
`fc8b64305d5b536ad1f9cafd7fd602ce9703adffaeceb5d9bdff46d25224ad60`),
with retrieval time, version and any discrepancy recorded.

## Release checks

The focused script and normal LAIF quick/full local gates are run on this
branch. Their exact results are recorded in the pull request. No protected
source, assessment report, manifest, scoring or detection file is changed.
