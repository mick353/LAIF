# Original EU AI Act: page text and structure receipt

**Scope:** The admitted **original** Official Journal edition of [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng/pdf), published 12 July 2024. This receipt does not assess the later amended or consolidated text. EUR-Lex separately lists [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1744) as an amending instrument and a [consolidation dated 27 July 2026](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng). Questions about legal effect require edition-specific legal review.

## Reproduce

From the repository root, using Python with `pypdf` installed:

```powershell
python docs/verification/2026-11-18-eu-original-structure/verify.py
```

The command reads the preserved PDF and admitted raw text, checks both SHA-256 identities against the [source manifest](../../verified/manifests/eu-ai-act-2024-1689.json), re-extracts all PDF pages with `pypdf`, and compares each page after removing whitespace only. It then inventories exact main-body `Article N` and `ANNEX Roman-numeral` heading lines. It prints a JSON result with the first PDF page for each heading; the observed run is saved in [result.json](result.json).

## Observed result

On 18 November 2026, Python 3.11.9 with `pypdf` 6.18.0 returned `PASS`: 144 of 144 nonblank PDF pages matched the corresponding stored raw page's non-whitespace character sequence; Article headings 1–113 appeared once, in order, before Annex I; Annex headings I–XIII appeared once, in order. The PDF SHA-256 was `bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e`; the raw text SHA-256 was `7fb1ae279b6353a9da6bf7dd82218f3cfb2329cc1f9f1512aa269bc4985fe697`. The [earlier ingestion trace](../../verified/extracted/eu-ai-act-2024-1689-ingestion-trace.md) used `pypdf` 6.21.4; this run checks the stored text against a second installed version of the extractor.

This is an automated extraction-consistency and heading-coverage check. Removing whitespace cannot prove visual layout, table structure, glyph correctness or quotation fidelity to the rendered page. Both versions use the same PDF extraction library family, so this is not an independent transcription. It does not validate legal interpretation, current-law applicability or LAIF assessment. The manifest's `PENDING_ASSESSMENT` status and the need to check quoted clauses against the official PDF remain unchanged.

## Existing assessment boundary

The [7 November whole-source generated report](../2026-11-07-real-source-assurance/eu-ai-act-2024-1689/eu_ai_act_2024_1689.laif.md) uses `external_framework` mode on the original-edition raw text (report artifact committed at `e9d137fd2e148f107274d6fb70b3038518afb26f`). It records 20 candidate control passages in eight retrieval categories and contains submitted development review annotations. Its executive finding explicitly requires full source-based assessment and deployment evidence. Neither that generated report nor this receipt is a complete attributed legal or LAIF assessment of the original Act; the source manifest still says `PENDING_ASSESSMENT`.

The distinct [8-passage contextual evidence record](../2026-11-07/regulatory/original_act_substantive_evidence.json), used in the separate 2026 amendment assessment, maps original-edition Article 9 (PDF pp. 56–57), 13 (59–60), 14 (60–61), 15 (61–62), 85 (110), 86 (110), 111(1) (121) and 113 (123). That record pins passage offsets and hashes in a Poppler extraction; it is not an eight-article full assessment. Its operative-scope notes restrict reliance on Article 111 to paragraph 1 and on Article 113 to the general application rule and point (b), with changed provisions to be read through the amendment. This receipt does not independently resolve those legal scope judgments.
