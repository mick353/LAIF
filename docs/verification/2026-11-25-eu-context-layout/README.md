# Original EU AI Act context passage check

On 25 November 2026 in Canberra, Codex checked the eight [original-edition
context spans](../2026-11-07/regulatory/original_act_substantive_evidence.json)
used by the 2026 amendment assessment. The source was the English Official
Journal edition of 12 July 2024. The check used the PDF, extraction and
historical traces from LAIF main at `f76d2f1`. [Official Journal edition](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)

Poppler rendered nine pages from the pinned PDF. The visual pass checked the
headings, paragraph starts and ends, page breaks, and the context immediately
before and after each span. The accompanying script independently checks the
three input hashes, eight individual trace hashes and a unique text match
per recorded page window. It compares the stored trace with the admitted
page extraction, removing whitespace and the dated Official Journal
running headers and ELI footers listed in the script. It preserves wording
and punctuation. The [earlier whole-PDF check](../2026-11-18-eu-original-structure/README.md)
establishes the extraction comparison for all 144 pages.

| Trace | PDF pages | Visually checked boundary |
|---|---:|---|
| EUO-9 | 56–57 | Article 9 paragraphs 1–10, ending before Article 10 |
| EUO-13 | 59–60 | Article 13 paragraphs 1–3, with point (f) ending before Article 14 |
| EUO-14 | 60–61 | Article 14 paragraphs 1–5, including the final exception to separate verification |
| EUO-15 | 61–62 | Article 15 paragraphs 1–5 end on page 61. The stored span continues through the next section heading on page 62 and stops before Article 16 |
| EUO-85 | 110 | Both unnumbered paragraphs of Article 85 |
| EUO-86 | 110 | Article 86 paragraphs 1–3, ending before Article 87 |
| EUO-111-1 | 121 | Article 111 heading and both blocks of paragraph 1, ending before paragraph 2 |
| EUO-113 | 123 | Article 113 heading, application text and points (a)–(c), ending before the final binding clause |

The four page-spanning traces retain running matter at page breaks.
When citing Article 15 itself, use page 61 and end the passage before the
page 62 section heading. Use the historical JSON to reproduce the original
assessment input. Its operative-scope notes for Articles 111 and 113 apply
to that assessment. Current applicability and the full substantive assessment
require their own evidence and review.

From the repository root:

```powershell
py -3 -X utf8 docs/verification/2026-11-25-eu-context-layout/verify.py
```

All eight stored hashes and unique text matches passed. The visual inspection
covered page layout and passage boundaries. The text comparison checks the
full stored spans under the stated normalization.
