# LAIF System — Independent Usability Review

**Date:** September 2026
**Reviewed commit:** `cd85edd` (verified against `origin/main`, clean clone)
**Method:** Live end-to-end use cases with documents not previously seen by the
system, run through the production entry point (`scripts/laif_process_document.py`).
No inspection-only findings — every observation below is reproduced from an
actual run.

---

## 1. Scope and method

Three documents were authored for this review to represent realistic user inputs
and were processed through the standard runner:

| Fixture | Represents | Character |
|---|---|---|
| `trust_ai_policy.md` | An NHS-style hospital Trust internal AI use policy, draft for board approval | Typical real-world institutional policy: sincere, procedural, structurally thin |
| `vendor_statement.md` | A supplier's "Responsible AI" statement supplied to a public-sector buyer | Marketing-register assurance text with minimal operative content |
| `strong_charter.md` | A governance charter expressing full structural substance in its own vocabulary | Deliberate high-quality control |

Each was run with default options. Outputs examined: institutional report,
full assessment report, JSON result, technical appendix, analyst bundle.

---

## 2. Headline result

**The assessment engine works. The institutional report does not carry its
findings.**

The engine discriminated the three documents correctly and by a wide margin:

| Document | Overall | Structural alignment | Coupling state |
|---|---|---|---|
| `strong_charter` | 58/100 | FUNCTIONALLY ALIGNED | FUNCTIONAL |
| `trust_ai_policy` | 20/100 | STRUCTURALLY UNALIGNED | IMPLICIT |
| `vendor_statement` | 10/100 | STRUCTURALLY UNALIGNED | ABSENT |

The full assessment report (`*.laif.md`) preserved that discrimination cleanly,
reporting calibrated positions of **71% / 25% / 12%** respectively.

The institutional report (`*.institutional_report.md`) — the artifact whose name
invites a governance officer to open it first — gave **all three documents the
identical executive finding sentence**, word for word.

---

## 3. Findings

### F1 — CRITICAL: the institutional report's executive finding is invariant

All three documents received:

> "This document is useful as a governance source, but institutional reliance
> depends on proof of operational closure, accountable ownership, evidence
> sufficiency, and decision consequences."

A substance-complete charter, a thin hospital policy, and a vendor marketing
page are not equivalently useful governance sources, and the engine knows it.
The finding is generated from templates rather than from the result, so the
single sentence a decision-maker reads carries no information.

**Impact:** a reader who opens only this artifact cannot distinguish a strong
document from a weak one. This is the most consequential defect in the system.

### F2 — CRITICAL: approximately 70% of the institutional report is repeated text

Within a single 116-line report:

- All **failure pathways** (PATH-001…003) have identical bodies; only the title
  differs.
- All **operational gaps** (GAP-001…005) share one description, and every gap
  cites the same evidence set ("Q001, Q002, Q003").
- The **control implementation template** is a 7-column table with five rows in
  which every cell is identical.
- Remediation roadmap entries differ only in the trailing gap name.

Cross-document, two entirely unrelated documents produced institutional reports
differing in only **48 of 114 lines**, most of that difference being quoted
evidence.

**Impact:** the artifact reads as machine filler. A professional reader
discounts the whole report, including the parts that are sound.

### F3 — HIGH: document-type classification is wrong, and the error propagates

The hospital Trust's internal policy was classified `procurement_assessment_form`.
The report then advised that its governance force "arises through procurement
conditions, contract clauses, supplier obligations, and audit rights" — none of
which apply to a Trust's own internal policy. The vendor statement, by contrast,
classified as `unknown_governance_document`.

**Impact:** materially misleading guidance, confidently stated. The
classification is not merely cosmetic: it drives the governance-force narrative
and the recommended-use text.

### F4 — HIGH: sector auto-detection did not fire on an unmistakably clinical document

A document containing *patient*, *clinical staff*, *clinical judgement*,
*Clinical Digital Committee*, and *patient safety* was assessed under the
`general_ai_governance` profile rather than a clinical profile, forfeiting the
sector-specific risk indicators and evidence expectations that exist for it.

### F5 — MEDIUM: quoted evidence is truncated mid-sentence and carries numbering artefacts

Observed verbatim in the institutional reports:

- `"3 Suppliers should provide evidence of regulatory approval where the tool is a"`
  — leading fragment of "3.3", trailing truncation mid-clause.
- `"Affected persons shall have"` — cut before the substantive right.
- `"(b) The optimisation objectives stated in system documentation shall"` — cut
  before the obligation.

**Impact:** quotes are the report's evidentiary backbone. Fragments undermine
the claim that findings are anchored in the source, and cannot be pasted into a
board paper.

### F6 — LOW: artifact sprawl without a stated reading order

One document produces five outputs (institutional report, full report, technical
appendix, JSON, analyst bundle) plus an index entry, with no guidance on which
to open first or who each is for.

---

## 4. What works well

These are strengths confirmed under live conditions, not assumptions:

1. **Engine discrimination is accurate and well-separated** (58 / 20 / 10 with
   matching alignment and coupling verdicts).
2. **The full assessment report is genuinely usable.** It preserved calibration,
   carried the plain-language reading, evidence locator, not-found placement
   guidance, and peer exemplars.
3. **The plain-language reading is the system's best output.** On the Trust
   policy it correctly observed that the document names only some of the
   interests it serves, that its protective intent is not fastened to any
   identifiable person, that it gives an affected patient no route to challenge
   an outcome, that nothing binds its author or survives them — while crediting
   its real administrative machinery. Every one of those statements is
   independently verifiable against the source text.
4. **Performance is excellent** — 0.43 s per document end to end.
5. **Provenance, determinism, and reproducibility hold** — corpus fingerprint
   reproduced identically from a clean clone; all committed artifacts matched
   fresh regeneration byte for byte.

---

## 5. Use-case verdicts

| Use case | Verdict | Notes |
|---|---|---|
| Document owner improving their own policy | **Works** | Full report gives located evidence, placement guidance, and attachment points |
| Executive needing a one-page brief | **Works (corpus runs)** | `laif_executive_summary.md` is fit for purpose |
| Governance officer opening the "institutional" report | **Fails** | F1, F2, F3 — invariant finding, boilerplate, wrong document type |
| Procurement officer screening a vendor | **Partially works** | Engine scores correctly; institutional narrative misleads |
| GRC engineer ingesting results | **Works** | `laif.assessment.v1` JSON is well-formed and complete |
| Auditor verifying a published finding | **Works** | Fingerprint, hashes, provenance tiers, deterministic regeneration |

---

## 6. Recommendations, in priority order

1. **Make the institutional executive finding a function of the result** —
   alignment verdict, coupling state, calibrated position, and the document's
   own leading gap. It must be impossible for three documents of different
   quality to receive the same sentence.
2. **De-duplicate the institutional report.** Emit one control template with the
   gaps listed against it, or make each pathway/control genuinely specific.
   Repetition should be impossible by construction, not by review.
3. **Fix document-type classification, and fail honestly.** An internal
   institutional policy must not be read as a procurement form; where confidence
   is low, say "not classified" rather than asserting a type that drives wrong
   advice.
4. **Widen sector auto-detection**, and state the detected sector and its basis
   so a user can correct it.
5. **Apply the full report's quote discipline to the institutional report** —
   whole clauses, word boundaries, no numbering fragments.
6. **State a reading order** at the top of each artifact: who it is for and what
   to open first.

Items 1, 2 and 5 are report-layer changes that cannot affect scoring. Items 3
and 4 touch classification inputs and require regression coverage against the
existing corpus.

---

*Prepared by independent review of commit `cd85edd`. Fixtures and raw outputs
are reproducible with `scripts/laif_process_document.py` on the documents
described in §1.*
