# NIST authored-review quotations against the preserved official PDF

**Question:** Do the exact 16 source excerpts in the 7 November 2026 authored
NIST criterion review appear in the preserved NIST AI RMF 1.0 PDF? This is a
source-wording check on `origin/main` at `e574fb2`, not a review of the eight
interpretations, a new assessment, a source-status promotion or NIST endorsement.

The [earlier PDF receipt](../2026-11-14-nist-pdf-fidelity/README.md) records the
[NIST publication](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10),
[official PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), original
download and 19/19 category and 72/72 subcategory matches. This follow-up
checks the prose excerpts actually cited in the
[authored review](../2026-11-07-substantive-review/5f667a6f-NIST.AI.1001/completed-review.json).

## Method and result

Run `python docs/verification/2026-11-18-nist-cited-prose/verify.py` from the
repository root with optional `pypdf` installed. The script pins SHA-256 of
the 48-page PDF, retained raw Markdown and authored review; checks each
quotation against its exact raw-text character span; extracts every PDF page
with `pypdf` 6.18.0; then locates its alphanumeric wording on exactly one page
after removing typography, punctuation, whitespace and line-break hyphenation.
It compares the full committed [machine result](result.json) on later runs.

**Result: 16/16 curated excerpts match their raw spans and the PDF wording,
across all eight reviewed criteria.** The result records each evidence ID,
criterion, raw span, quote hash, normalized length and one-based PDF page. No
quotation text is copied into this receipt. This adds a bounded prose check to
the earlier 19/19 category, 72/72 subcategory and 583/585 diagnostic-window
results. The two earlier window mismatches remain documented extraction
artefacts; this receipt does not erase them.

The matching algorithm deliberately ignores punctuation, symbols, layout and
some hyphenation, and it examines only these 16 cited spans. It does not prove
whole-document, table-layout, figure, legal or semantic fidelity. A page match
does not show that the authored interpretation follows from the quotation.
The older [evidence trace](../../verified/extracted/5f667a6f-NIST-evidence-trace.md)
requires separate semantic review; it is not the authored-review input checked
here. The source manifest and its `HASH_VERIFIED_LOCAL_ONLY` status remain
unchanged pending a source-custodian decision.

## Other authoritative-source attempts on 18 November 2026

At approximately 01:52 UTC (12:52 Canberra AEDT), ordinary PowerShell GETs of
the [Commonwealth Ombudsman's March 2025 guide PDF](https://www.ombudsman.gov.au/__data/assets/pdf_file/0025/317437/Automated-Decision-Making-Better-Practice-Guide-March-2025.pdf)
and the [NHS England February 2026 DTAC DOCX](https://digital.nhs.uk/binaries/content/assets/website-assets/services/dtac/dtac_form_2.0_february_2026.docx)
both returned **HTTP 403**. No publisher bytes were obtained or substituted.
The publisher [Ombudsman PDF](https://www.ombudsman.gov.au/__data/assets/pdf_file/0025/317437/Automated-Decision-Making-Better-Practice-Guide-March-2025.pdf)
is still readable through web retrieval as a 61-page guide whose cover says
March 2025. The [NHS DTAC page](https://digital.nhs.uk/services/digital-technology-assessment-criteria-dtac)
still links a DOCX form and says to download at point of use, but its binary
could not be read through this route. Browser surfaces were unavailable for a
normal download attempt. No access control was bypassed. The Ombudsman
comparator intake and DTAC upstream byte identity remain open.
