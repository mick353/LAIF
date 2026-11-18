# NIST historical evidence-trace citation erratum — review required

**Status:** additive correction proposal, 18 November 2026. The historical
[May evidence trace](../../verified/extracted/5f667a6f-NIST-evidence-trace.md)
is retained unchanged. This note identifies mismatches between its descriptions
of numbered NIST clauses and the preserved [official NIST AI RMF 1.0 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
(SHA-256 `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`).
The PDF table wording matches the retained raw Markdown for all 72 numbered
subcategories under the [14 November source-fidelity check](../2026-11-14-nist-pdf-fidelity/README.md).
That confirms the text being compared, not the trace's interpretations.

**Current-use caution:** do not use the historical trace's narrative labels or
finding bases as verified interpretations of NIST provisions. The local
validator checks that cited section identifiers occur in the raw file; it does
not check whether the surrounding description or inference is right. A source
custodian and substantive reviewer should redo affected mappings against the
PDF before relying on the historical trace for publication, source admission,
or current legal/governance conclusions. Neither a string-match PASS nor this
erratum regrades NIST, changes its manifest, or validates LAIF's assessment.

## Directly observed mismatches

PDF pages below are **one-based file pages**, not the publication's printed
page labels. The cited clause texts are also visible in the retained raw
Markdown [GOVERN table](../../verified/raw/5f667a6f-NIST.AI.1001.md) and
MEASURE/MANAGE tables. The right column paraphrases the actual clause; it is
not a replacement LAIF finding.

| Historical trace location and description | Numbered clause in the PDF | Consequence for the mapped finding |
| --- | --- | --- |
| A.1: GOVERN 1.7 described as role/documentation requirements | PDF p. 28: GOVERN 1.7 concerns safe decommissioning and phase-out | This cited clause does not support the stated transparency/role basis. |
| A.1: GOVERN 6.1 described as transparency/explainability policy | PDF p. 29: GOVERN 6.1 concerns third-party entity risks, including intellectual-property rights | The trace's claimed direct transparency mandate is unsupported by this clause. NIST addresses transparency elsewhere, including MEASURE 2.8–2.9 and explanatory prose; review those separately. |
| A.1: MEASURE 2.5 described as explainability/interpretability performance | PDF p. 34: MEASURE 2.5 concerns validity, reliability and generalisability limits | The cited clause does not by itself establish the described explainability requirement. |
| A.2: MEASURE 2.6 described as adversarial red teaming | PDF p. 35: MEASURE 2.6 concerns safety-risk evaluation, residual risk and safe failure | The trace's red-team claim is unsupported by this clause. Other security or testing text would require its own citation and scoped analysis. |
| A.2: MAP 1.6 described as documented stated-versus-implemented objectives | PDF p. 31: MAP 1.6 concerns eliciting system requirements and design decisions | Objective/implementation correspondence is not demonstrated by this citation alone. |
| A.3: MANAGE 1.3 described as deployment scope/operational boundaries | PDF p. 37: MANAGE 1.3 concerns planned responses to high-priority risks | The asserted boundary mechanism is not established by this clause. |
| A.3: MANAGE 2.2 described as ongoing monitoring | PDF p. 37: MANAGE 2.2 concerns mechanisms to sustain the value of deployed systems | The monitoring claim needs another source passage, such as the actual MANAGE 4.1 monitoring clause, and fresh interpretation. |
| Q2: GOVERN 6.2 described as deployment across organisational contexts | PDF p. 29: GOVERN 6.2 concerns contingency for failures or incidents in high-risk third-party data or AI systems | The claimed cross-scale consistency basis is unsupported by this clause. |

These are **citation-to-description errors**, not PDF/DOCX transcription
differences. This check did not audit every sentence in the trace or decide the
ultimate A.1, A.2, A.3 or Q2 outcomes. Several affected concepts do appear
elsewhere in NIST, so the appropriate next action is a fresh source-scoped
assessment with correct passages, alternatives and limits, followed by human
review. Do not mechanically replace one ID or verdict in the historical report.

## Exposure and preservation

The NIST manifest and public source-index JSON both name the old trace path.
`validate.py` checks its section identifiers, not semantic mapping. The
current generated document processor reads NIST source text and its own evidence
data; this audit found no code path that imports the old Markdown trace as a
scoring rule. The historical [full corpus assessment](../../../reports/laif_full_assessment.md)
and 7 November authored NIST review are separate records. The full assessment
contains some different, directly quoted NIST passages, but this note does not
certify its reasoning; the affected historical trace cannot be used to justify
its conclusions without re-review.

The private Site catalogue contains the manifest pointer and a retained NIST
authored run marked as needing independent review. As checked by the Site owner
on 18 November, the imported run contains none of the literal affected clause
labels; neither the private v19 UI nor public v2 reading room directly displays
the historical trace or those erroneous labels.
No Site source, corpus bytes, manifest status, historical trace, protected
assessment or generated report is changed by this proposal.

## Required substantive follow-up

1. Source custodian confirms the exact PDF pages and the eight mismatch rows.
2. Independent substantive reviewer inspects all NIST trace mappings, relevant
   counterevidence and full context, then issues a corrected, source-bound
   interpretation and decides whether any historical assessment finding needs
   revision. Preserve the original dated assessment and attach any amendment.
3. Product/Site owner checks whether current NIST authored-run wording inherits
   an affected claim; if it does, display a visible qualification or corrected
   reviewed record rather than silently changing an old run.

This note is a documented review gate, not completion of those decisions.
