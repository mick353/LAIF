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

---

## 7. Resolution status (second review pass)

All six recommendations were implemented. A second pass then stress-tested the
system against four fresh documents chosen to be outside the corpus it was
tuned on: a bank AI governance standard, an NHS AI triage tender, a sales
report, and a two-word file. That pass found a further, more serious class of
defect and it has also been fixed.

### 7.1 Recommendations 1–6

| # | Recommendation | Status |
|---|---|---|
| 1 | Executive finding must be a function of the result | **Done** — derived from alignment verdict, coupling state, calibrated position, document-type framing, and the document's own leading gap |
| 2 | De-duplicate the institutional report | **Done** — pathways, controls, and owners are gap-specific; empty sections state their own meaning instead of emitting boilerplate |
| 3 | Fix document-type classification, fail honestly | **Done** — identity anchors, corporate-standard register added to `internal_policy`, procurement instrument form outranks sector vocabulary, and "not confidently classified" is stated where it applies |
| 4 | Widen sector auto-detection and show its basis | **Done** — whole-word counting, a `financial_services_ai` profile, and the detected sector reported with the terms that produced it |
| 5 | Institutional-report quote discipline | **Done** — sentence-anchored quotes through the same display-repair and damage gate as every other public quotation |
| 6 | State a reading order | **Done** — each artifact opens with who it is for and what to read first |

### 7.2 The register-bias defect

The stress test found that a deliberately excellent bank standard — named-interest
coupling with a mutual non-weakening lock, an all-conditions deployment gate,
an unconditional customer review right, quantified monitoring thresholds with
escalation and suspension, self-application, and change control — scored 35/100
and was reported as ABSENT on the Integrity Layer, Consistency, Reversibility,
and Self-Application. It was then told it lacked a named owner, lacked
monitoring thresholds, and lacked lifecycle scope, all of which it plainly
stated.

The cause was that rubric and construct patterns were keyed to the drafting
register of the corpus the system was built against — EU/NIST/OECD legal and
framework prose — rather than to the function the language performs. `shall`
counted and `must` did not; `provider` and `deployer` counted and `Chief Risk
Officer` did not; `lifecycle` counted and `change control` did not;
`proportionate to risk` counted and `a drift breach above 5%` did not.

This is the same failure the system is designed to expose in others: judging an
instrument by its vocabulary rather than by what it does. Every affected signal
is now keyed to function, with the accepted registers documented in
[SCORE_INTERPRETATION.md](../governance/SCORE_INTERPRETATION.md#drafting-register-neutrality).
The same document now scores 66/100 (81% of the achievable external ceiling),
is FUNCTIONAL on four of five constructs, and reports no false gaps.

Breadth was constrained from the other side at the same time: ordinary business
prose still scores near zero, sector vocabulary without governance architecture
is still flagged as gaming risk, and both directions are pinned by tests
(`InstitutionalRegisterDetectionTests`, `NonGovernanceTextTests`, and the
adversarial suite's sector-gaming group).

### 7.3 Second-pass fixes beyond register bias

- **Gap rules may name several closing controls** and fire only if all are
  missing — a document with a complete escalation chain is no longer told it
  lacks thresholds because it used different words for them.
- **Thinness is measured, not inferred from the alignment verdict.** A
  substantive document that leaves nothing unclosed now reports exactly that,
  with an explicit statement that it is a reading of the text and not a
  certificate that the controls exist or operate.
- **Control names correspond to their own gap.** Naming controls from a
  per-instrument list indexed by gap number produced names unrelated to the gap
  they closed; a redress gap was named as a clinical safety register.
- **`_term_hits` counts distinct terms**, so one generic phrase occurring twice
  can no longer satisfy a "two independent signals" classification gate. This
  had been routing corporate standards to public-sector policy on the phrase
  "human review" alone.
- **Recommended-use and limits statements are document-type specific** rather
  than a fixed paragraph, and both now carry the standing caveat that the
  assessment reads the document, not the organisation.

### 7.4 Use-case verdicts after the second pass

| Use case | Verdict |
|---|---|
| Document owner improving their own policy | **Works** |
| Executive needing a one-page brief | **Works** |
| Governance officer opening the institutional report | **Works** — finding, gaps, pathways, and controls are document-specific |
| Procurement officer screening a vendor | **Works** — tender is classified as a procurement instrument with the sector carried separately |
| Bank/insurer assessing an internal AI standard | **Works** — institutional register detected; `financial_services_ai` profile available |
| GRC engineer ingesting results | **Works** |
| Auditor verifying a published finding | **Works** |
| Non-governance document submitted by mistake | **Works** — scores near zero and says why |
| Unreadable or empty file | **Works** — fails with a specific extractor error, no assessment emitted |

---

## 8. Third pass — instrument classes outside the tuning set

A third stress set covered four further document classes: a corporate values
charter, a supplier attestation, a university academic policy, and a document
that asserts protections and then revokes them. It found five defects, all now
fixed and pinned by tests.

**Register bias was not sector-specific.** The academic policy expressed the
same substance as the bank standard in academic vocabulary — "may not be varied
independently", "all of the following are satisfied at the same time",
"the reviewer may substitute their own decision", "are themselves subject to
this policy", "falls below 90%, use must be paused" — and scored 44/100 with
Coupling, Consistency, Reversibility, and Self-Application reported ABSENT. It
now scores 64/100 and is FUNCTIONAL on four of five constructs.

**A percentage threshold could never match.** The enforceability threshold
pattern ended in a word boundary after `%`, which cannot match: `%` is not a
word character, so `below 90%,` failed the pattern that was written to catch it.
Every quantified breach trigger in every document had been invisible.

**Self-contradiction was detected but never reported.** A document claiming full
transparency and then refusing all disclosure, claiming human oversight and then
executing without review, was told its leading problem was a missing accountability
register. Contradictions now precede the gap register in the executive finding and
are quoted in their own section: a gap is something a document omits, a
contradiction is something it revokes.

**Contradiction triggers were keyed to a narrow phrasing** ("system
transparency", "operates within") and missed how institutions actually claim
these properties ("committed to full transparency", "human oversight is
maintained at all times"). Broadening them exposed the mirror risk immediately —
the bank standard's own clause "the restriction on automated credit decisioning
*without human review* exists to protect the applicant" was flagged as a
no-oversight contradiction. The governing-context guard now suppresses adversary
vocabulary appearing inside the prohibition that forbids it.

**Instrument form was conflated with subject matter, and with the other side of
the same transaction.** A supplier attestation was classified as a procurement
form — the two share the phrase "supplier response" but need opposite reviewer
treatment, since a tender needs contract conditions and an attestation needs
independent verification. A values charter had no class at all and was reported
as "not confidently classified" rather than as what it is: a document that
carries no assurance force until its values are written as duties.

Two consistency defects surfaced alongside these: the report displayed one
sector profile's name beside another's supporting evidence, because the runner's
keyword detector and the engine's document-type routing were both consulted; and
control recommendations were named from a per-instrument list indexed by gap
number, producing names unrelated to the gaps they closed.

| Document class | Before | After |
|---|---|---|
| Bank AI governance standard | 35, four constructs ABSENT, three false gaps | 66, FUNCTIONALLY ALIGNED, no false gaps |
| University academic policy | 44, four constructs ABSENT, three false gaps | 64, FUNCTIONALLY ALIGNED, no false gaps |
| Self-contradicting standard | leading finding: missing owner | leading finding: self-contradiction, quoted |
| Supplier attestation | procurement form | vendor submission, "a claim, not evidence" |
| Values charter | not classified | values charter, "no assurance force alone" |
| AI triage tender | clinical assurance checklist | procurement instrument, clinical sector |
| Sales report / empty file | correct | correct (unchanged) |

---

## 9. Fourth pass — the cost of breadth

Every earlier pass widened detection. The fourth pass attacked the result: a
document assembled entirely from governance vocabulary, with no duty anywhere in
it, scored **59/100 and FUNCTIONALLY ALIGNED** — within seven points of the
genuine bank standard. That is the price of register neutrality, and it had to
be paid back.

The discriminator is not vocabulary; it is sentence form. An operative sentence
binds an actor to an action. An enumeration is a dense run of governance nouns
with nothing bound to anyone. Measured across the entire assessment corpus and
every fixture built during these reviews, genuine instruments enumerate in 0-6%
of their sentences; the constructed document enumerates in 24%.

The detector now runs on every assessment. A HIGH verdict makes structural depth
HOLLOW, blocks the FUNCTIONALLY ALIGNED verdict, qualifies the coupling reading
instead of asserting it, quotes the offending sentences, and enters the gap
register as the leading gap with a rewrite into operative form as its control.
The soup now reports as PARTIALLY ALIGNED / HOLLOW with its own sentences
against it; the bank and university policies are untouched.

This closes the loop opened in §7.2. Detection is keyed to what language does,
in whatever register it is written — and a document that only says the words is
told so, in its own words.

---

## 10. Fifth pass — LAIF assessed by LAIF, and the limits of the method

The fifth pass ran LAIF's own corpus and full-length source instruments through
the runner, in both modes. It found the earlier invariant-finding defect still
living in a path the first review had not exercised, a false negation against
LAIF's own text, and a scale limit that had been going unstated.

**LAIF-native mode emitted one sentence for every document.** "This document is
assessed in LAIF-native mode. Formal LAIF-native certification remains governed
by the deterministic LAIF validation boundary shown in the technical appendix."
— true of every document ever assessed, and therefore useless. The native
finding now names the verdict, the specific failing checks, the coupling-quality
reading, the dimensional position, and the boundary. LAIF v1.2 fails on two
FINDING-block checks; its own PDCA fails on three constitutional-hierarchy
checks. Both are correct, both are now legible, and the finding says plainly
that a framework text is expected to fail checks only an assessment record can
satisfy.

**LAIF's own principal text was read as disclaiming Coupling.** Its worked
example contains "Q1 — Coupling: Not satisfied", which the negation detector
took as the document renouncing Coupling for itself — giving LAIF v1.2 a HOLLOW
structural depth. This is the third instance of one root error: mistaking a
document's subject for its position. A document that declares Coupling
structurally *and* works through a case where Q1 fails is applying the test. The
guard requires both conditions, so a bare disclaimer is still negation.

**An empty gap register was being presented as a clean finding on documents too
long for the method to discriminate.** Gap rules test signal presence across the
whole text; past roughly 20,000 characters every operative signal fires
somewhere, and no rule can fire. NIST AI 100-1 was accordingly told that "every
governance expectation this document creates has a corresponding control in the
same document" — a claim the method cannot support. Long documents now get the
truthful statement instead: detection has saturated, a control in one section
does not close an obligation in another, assess it section by section.

Stating where the method stops working is not a caveat added for safety. It is
the same obligation the reporting layer already carries on provenance, applied
to its own reach.

---

## 11. Sixth pass — the portfolio view and the operator's path

The sixth pass read a full institutional report end to end as its audience, then
ran the batch runner the way an operator would: from the folder holding the
documents.

**The batch runner failed every document when run from anywhere but the
repository root.** It located the single-document runner relative to the working
directory, so an operator batching a folder got a file-not-found error attributed
to each document rather than to the invocation. It now resolves the runner
beside itself.

**The portfolio governance-force matrix asserted four of its columns.** Lifecycle
control, accountability closure, and redress read "requires monitoring/change
gate", "requires named owner/sign-off", "requires redress/contestability
mapping" for every document ever batched — including documents that govern
change, name owners, and state a challenge route. Each cell is now derived from
that document's own gap register, and where a document creates too few
expectations to test, every cell says "not assessable" rather than letting the
absence of a gap read as the presence of a control.

**"Common gaps across portfolio" listed every gap seen once anywhere,** and
"most urgent common control gap" picked whichever sorted first alphabetically.
Recurring gaps are now those present in two or more documents, ordered by how
much of the portfolio shares them, and single-document gaps are listed
separately so they are actioned where they belong.

**A bank standard was reported as the portfolio's strongest public-sector
operating policy,** because three document types were collapsed into one role.
Public-sector, institutional, and procurement instruments are now separate
roles.

Two defects in the single-document report were fixed alongside. The same clause
could appear both as clean quoted evidence and as evidence requiring source
verification — a truncated candidate whose complete form had already been
admitted was still listed as outstanding. And the residual-risk paragraph
restated a generic failure mode; it now names the document's own unclosed gaps.
Failure-pathway steps now name the signal the quote evidences ("The document
raises **safety** at ..."), so the chain from quote to gap is visible rather
than implied.

---

## 12. Seventh pass — document forms

The seventh pass tested forms rather than registers: a control register written
entirely as a table, an all-caps agency directive, and a single complete clause.

**A fully specified control register scored 30/100 and was told it had
"insufficient operative content to assess control closure".** It was the most
operationally complete document in the entire test set — every row naming a
control, an owner, a trigger, a threshold, and a consequence — and it carried no
"shall" anywhere, because obligations were expressed as table rows. This is a
common institutional form: control registers, RACI tables, DPIA matrices,
assurance schedules. A row pairing a control with an owner binds an actor to an
action exactly as an operative sentence does. It is now recognised as such,
scores 45/100, classifies as an institutional operating instrument, and its gap
register correctly reports nothing unclosed.

**A single clause with no monitoring obligation was told its monitoring lacked
thresholds** — because "review by a person with authority to reverse the
decision" fired the review/monitoring signal. Gap rules can now require the
source text to carry the language the expectation rests on. The sample tested
against is built strictly from verbatim source fragments and deliberately
excludes rubric labels: letting the detector's own phrase "review / monitoring
mechanisms" satisfy the test would make the condition self-confirming, which is
how the first attempt at this fix failed.

**All-caps drafting was handled correctly** — every construct verdict is
identical under upper-case — but the agency directive did not classify, because
"directive" was missing from the institutional-form vocabulary. Government
service-delivery routing also missed "claimant", "council", and "local
authority".

---

## 13. Eighth pass — output isolation

The final pass re-ran every document class built across these reviews into one
output directory, the way a reviewer working through a folder of documents
would.

**The analyst directory was not namespaced by document.** Every markdown and
JSON report already carried the document stem, but `analyst/` did not — so
processing a second document into the same `--output-dir` silently replaced the
first one's gap register, control recommendations, failure pathways, and quote
bank. The files stayed on disk, beside a report they no longer described, with
nothing to indicate the mismatch. The batch runner was unaffected because it
gives each document its own directory; a reviewer using the single-document
runner repeatedly was not.

Analyst outputs are now written to `analyst/<document>/`. The tests locate the
directory rather than assuming its name, and one test processes two documents of
very different quality into a single output directory and checks that each
keeps its own register.

This was the last defect found. Across eight passes the pattern was consistent:
the engine's judgements were usually sound, and the failures were in what the
system *said* about them — an invariant sentence, an asserted column, a gap that
was declared rather than detected, a finding that outlived the document it was
computed from.

---

## 14. Ninth pass — the artifacts against each other

The ninth pass stopped reading artifacts individually and started reading them
against each other, and against the technical appendix, which no earlier pass
had opened.

**The appendix contradicted the report it accompanies.** Its construct-coverage
block showed `Coupling: false, Integrity Layer: false, Reversibility: false` for
a document the same run reports as FUNCTIONALLY ALIGNED on all three. The block
is a LAIF-*vocabulary* check, correctly labelled as internal diagnostic data —
but presented alone it reproduced, inside LAIF's own appendix, exactly the
vocabulary-for-substance confusion the two-axis model exists to prevent. Coverage
is now a two-column table: LAIF-native form beside functional alignment, with a
line saying that reading the first column alone will contradict the findings.

**Remediation patches called present constructs missing.** The bank standard
received `Missing LAIF construct: Coupling` at high severity and immediate
priority, alongside a report finding that its obligations are bound to the
interests they protect. Patches are now conditioned on the functional verdict:
present substance yields a certification-channel note, PARTIAL substance yields
"partially expressed", and the Coherence Test — LAIF's own named instrument — is
adoption distance by construction for any external document.

**A terminology gap was rated as severe as a construct gap,** because the
severity rule matched on the LAIF term names the gap listed as *not found*.
Certification-channel items are now `low` severity throughout; the bank standard
went from four high-severity patches to zero, with its one real structural gap
unchanged.

**Two constants were defined in four places.** The markdown report recomputed
the corpus fingerprint inline instead of calling the shared function, and
`test_real_world.py` held its own copy of the report date that silently
overrode the engine's — so the engine's three defaults were dead constants that
could disagree with the artifacts without any test noticing. Both are now
defined once. The report date, stale at July, is September.

**The corpus-wide top finding was a vocabulary check in disguise.** "Structural
— constitutional hierarchy not declared", present in 10 of 10 documents, was
detected almost entirely through LAIF's own headings, and named in LAIF's own
register. The underlying property is real and important — does a routine
revision change what the document requires? — so the signal now accepts the
forms real instruments use (conflicts clauses, "without prejudice to", waiver
bars, a stated parent framework), and the finding reads "no precedence rule
between the document's own provisions". No corpus score changed, because none of
these excerpts contains such a clause; the finding is now one a reader can act
on without adopting LAIF.

---

## 15. Tenth pass — the remediation layer, and the last vocabulary locks

The tenth pass read the remediation output as the person expected to act on it.

**The report told readers to build a control for not having used LAIF's
words.** The certification-channel item was rendered with the generic template:
"Define an institution-specific control for this diagnostic gap and assign
owner, trigger, evidence, escalation, and review obligations: certification
channel — LAIF-native vocabulary not used". These items now recommend no action
in one sentence, and the public report lists them as a count with an explanation
rather than as work.

**Auto-detected mode gave external documents LAIF-native wording.** Findings are
worded differently per mode, but mode resolution ran *after* the failure-mode
block, so the raw `None` parameter never matched `"external_framework"`. Every
caller that relied on auto-detection — which is the default — got the deficiency
wording. Resolution now precedes the findings.

**Two more signals were still vocabulary-locked.** Self-application was keyed to
"Part Seven" and "applies to regulatory", so "Group Risk is itself subject to
this Standard" and "Academic Board are themselves subject to this policy" scored
nothing on a 12-point signal while the functional layer read them as FUNCTIONAL.
The three institutional documents rose by three points each; no corpus score
moved.

**Small things that undermine trust.** `verification_test` read "samples this
control control". The generic recommendation restated the gap instead of saying
what to write.

Nothing in this pass changed a verdict. All of it changed whether a reader can
act on what they are told — which, after ten passes, is where the remaining
work has consistently been.

---

## 16. Eleventh pass — a report arguing with itself

The eleventh pass read the remediation list against the findings above it in the
same report, and found them disagreeing.

For the bank standard, the report said in sequence: **"Coupling substance
present in the document's own vocabulary (restriction paired with named stake,
mutual weakening lock)"** and then **"Restriction-protection pairing not
established — no governance restriction is bound to the specific interest it
protects, in any vocabulary."** Both were generated from the same run. The
findings layer had been moved onto functional alignment across earlier passes;
the remediation layer was still keyed to `construct_coverage`, which is a
vocabulary check. The same defect told a document with an explicit
all-conditions deployment gate that it had none, and prescribed the Coherence
Test — LAIF's own instrument — to instruments that had never claimed to contain
it.

The sector profile added a third voice: four LAIF adoption prescriptions, each
rendered as "<step> — not addressed in this document", asserted with no
detection behind them. For a document that pairs every restriction with a named
interest, "Introduce structural Coupling for each governance provision — not
addressed in this document" is simply false.

A renamed rubric label had also broken its construct mapping silently: the
self-application signal was renamed in the previous pass, and the map that
attaches the "substance functionally present" qualifier still held the old key.
A test now checks every key in that map against the live rubric.

After the fix the bank standard's remediation list is two steps: the substance
it already has, and the one real gap it does not — no precedence rule between
its own provisions, with the three statements that would close it. That is what
a reader can act on.
