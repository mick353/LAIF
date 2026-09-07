# LAIF Score Interpretation

LAIF scores are **deterministic LAIF rubric outputs**. They are generated from configured rubric signals and should be read as structured interpretation-layer data, not as legal authority.

Scores are not:

- legal determinations;
- statistical confidence values;
- external regulatory compliance ratings;
- proof that an external framework is valid, invalid, safe, unsafe, enforceable, or unenforceable under its own authority.

Scores support triage, comparison, review, and remediation prioritisation. They help reviewers identify which governance dimensions appear stronger or weaker under the LAIF model.

## Score Definitions

### `structural_score`

**Measures:** The extent to which the document expresses LAIF-relevant structural governance elements such as duties, controls, review mechanisms, accountability structures, and decision constraints.

**Does not measure:** Legal validity, full institutional effectiveness, or every possible governance safeguard outside the LAIF rubric.

**LAIF-native mode:** A useful signal for where the candidate document is structurally strong or weak, but it does not override strict LAIF-native PASS/FAIL requirements.

**External framework assessment mode:** A diagnostic indicator of structural proximity to LAIF governance expectations, without requiring LAIF vocabulary and without certifying the external framework.

### `terminology_score`

**Measures:** Presence of canonical LAIF terminology and explicitly recognized LAIF constructs.

**Does not measure:** Whether an external framework uses different language to create legally meaningful or operationally useful controls.

**LAIF-native mode:** Highly load-bearing. Missing canonical terminology can support LAIF-native certification failure because LAIF-native adoption requires canonical terms and structures.

**External framework assessment mode:** Diagnostic only. A low score means LAIF vocabulary is absent or limited; it does not mean the external framework is legally invalid, unsafe, valueless, or governance-worthless.

### `conceptual_proximity_score`

**Measures:** Whether the document addresses concepts similar to LAIF concerns, such as oversight, accountability, transparency, monitoring, risk management, redress, documentation, human interests, and lifecycle controls.

**Does not measure:** Formal LAIF compliance or certification readiness by itself.

**LAIF-native mode:** Helpful for remediation context, but conceptual proximity cannot convert a formal LAIF-native `FAIL` into a `PASS`.

**External framework assessment mode:** A diagnostic bridge showing substantive overlap with LAIF concerns even where canonical LAIF vocabulary is absent.

### `auditability_score`

**Measures:** Whether the document creates reviewable records, evidence artifacts, monitoring duties, logging, reporting, or independent verification hooks.

**Does not measure:** Whether an actual audit has been performed, whether evidence is truthful in practice, or whether an external auditor would reach a legal compliance conclusion.

**LAIF-native mode:** Indicates whether the document supports LAIF-native verification expectations, subject to strict certification requirements.

**External framework assessment mode:** Identifies how readily an independent reviewer could verify obligations under the LAIF model.

### `enforceability_score`

**Measures:** Whether obligations are framed with operational force: mandatory language, responsible actors, triggers, consequences, escalation, and remedies.

**Does not measure:** Court enforceability, regulator enforcement likelihood, contractual enforceability, or jurisdiction-specific legal authority.

**LAIF-native mode:** Supports review of whether LAIF-native obligations are stated with enough force to satisfy the framework.

**External framework assessment mode:** Diagnoses whether commitments appear aspirational or institutionally enforceable under the LAIF lens.

### `overall_readiness_score`

**Measures:** A deterministic aggregate readiness signal derived from current model weights across scoring dimensions.

**Does not measure:** Legal readiness, deployment approval, statistical confidence, or external regulatory compliance.

**LAIF-native mode:** Triage metadata only. A high readiness score cannot override a strict LAIF-native certification failure.

**External framework assessment mode:** Comparative diagnostic metadata for prioritising review and remediation across documents.

### `sector_risk_alignment`

**Measures:** Whether a document addresses sector-specific risk signals and evidence expectations for its assessed context, such as clinical, employment, procurement, government, or operational AI settings.

**Does not measure:** Complete sector compliance, real-world safety performance, or regulator acceptance.

**LAIF-native mode:** Helps reviewers see whether a LAIF-native candidate addresses the risk profile relevant to its deployment context.

**External framework assessment mode:** Shows whether the external document addresses sector risks that LAIF expects to see, without turning the result into certification.

## Score Weights and Calibration

Current score weights are deterministic model weights. They are reviewable and calibration-sensitive. A weight expresses how the current LAIF rubric values a signal for diagnostic and remediation purposes; it should not be presented as empirically validated or statistically validated unless future validation work supports that claim.

When score weights change, reviewers should treat the change as interpretation-layer or assessment-sensitive work depending on whether it affects outputs, thresholds, or public meaning. Score-weight changes should be documented so historical comparisons remain understandable.

## Phase 3N Structured Remediation Patch Schema

Structured remediation records are defined in [REMEDIATION_PATCH_SCHEMA.md](REMEDIATION_PATCH_SCHEMA.md). They convert existing diagnostic findings into machine-readable patches, controls, evidence artifacts, verification tests, and responsible-actor guidance. These records are diagnostic unless separately adopted by a regulator, institution, contract, procurement process, or other authority, and they do not determine legal validity or certify LAIF-native compliance.

## Phase 3P Evidence Trace Reference

Phase 3P evidence traces are deterministic source-support metadata only. Exact or deterministic traces require direct source-text presence; otherwise the reviewer-confirmation fallback is used. See [Evidence Trace Model](EVIDENCE_TRACE_MODEL.md).

## Phase 3Q Calibration and Score Justification Reference

See [CALIBRATION_SCORE_JUSTIFICATION.md](CALIBRATION_SCORE_JUSTIFICATION.md) for the shared boundary governing score bands, score justification metadata, dimension justifications, calibration cautions, gaming-risk notes, evidence/sector/remediation relationships, and the rule that LAIF-model signal strength does not determine legal validity or certify LAIF-native compliance.

## Public report template reference

Public-facing rendering requirements are defined in [Public Report Template](PUBLIC_REPORT_TEMPLATE.md). That template is presentation-only and does not change scoring, validation, certification, evidence, remediation, sector-profile, calibration, or governance invariants.

## Phase 3S System QA Release Audit Reference

See [SYSTEM_QA_RELEASE_AUDIT.md](SYSTEM_QA_RELEASE_AUDIT.md) for the release-readiness audit boundary covering validation/certification separation, diagnostic modes, evidence, remediation, sector profiles, calibration, public reporting, protected artifacts, and verified corpus limits. That audit is documentation/test-only and does not change runtime behavior.


## Phase 3V external-framework interpretation

External-framework scores are interpreted as governance repair signals. They do not require the source document to be LAIF-native and they do not convert an external legal, policy, assurance, or technical instrument into LAIF-native certification. The front-facing interpretation emphasizes systemic repair value, operational closure, evidence sufficiency, accountability closure, lifecycle control, residual-risk closure, implementation readiness, and failure-pathway risk. Formal LAIF-native construct coverage remains available in the technical appendix / internal diagnostic boundary. See `GOVERNANCE_REPAIR_REPORTING.md` and the Phase 3S System QA Release Audit Reference in `SYSTEM_QA_RELEASE_AUDIT.md`.

## Score Calibration — Achievable Ceiling and Compression

Raw overall scores compress by construction and must never be read as
percentage grades. Two mechanisms cause the compression:

1. **Reserved scale.** The terminology dimension (15% of the overall weight)
   and the named-decision-instrument structural signal can only be earned by a
   document written with LAIF branding. The effective ceiling for any external
   instrument is therefore below 100. The ceiling is *derived from the live
   rubrics* by `_achievable_ceiling_external()` in `assessment_engine.py` — it
   is never asserted as a constant — and every external assessment result
   carries it in the `score_calibration` field together with the document's
   calibrated position (raw overall ÷ ceiling).

2. **Conservative lexical detection.** Dimension rubrics detect structural
   language; they undercount substance expressed in unanticipated phrasings.
   The compression is quantified by a permanent control: the semantic-fidelity
   suite's substance-perfect external fixture (S1) scores in the mid-50s raw,
   and test `SF7.2` pins that band so the calibration statements in the public
   report cannot drift from measured reality.

Interpretation rule: on this instrument, a raw overall in the mid-50s is what
excellence looks like for an external document; 90+ is unreachable by design.
Read the calibrated position, the functional alignment verdict, and the score
band together. The calibrated position is a comparative figure within the LAIF
model; like all scores here, it is not a legal finding or a compliance rating.

## Evidence Locator and Placement Guidance

Every per-document assessment carries a source-location layer, all of it
deterministic text analysis of the assessed excerpt:

- **Document structure map** — the document's own headings, detected from
  common conventions (markdown, Article/Section/Part, GOVERN n.n, numbered
  heads).
- **Evidence Locator** — for every fired rubric signal, a verbatim quote and
  its location in the document's own structure. Locator and scorer use
  identical pattern flags; test `SF9.2` enforces exact parity (every fired
  signal has a location; nothing located was scored as missed).
- **Not Found — and Where It Would Belong** — for missed signals and ABSENT
  core structures: confirmation of absence from the excerpt plus the most
  related existing section (keyword overlap with the document's own headings),
  falling back to the obligation-bearing section, or an honest "new provision
  required".
- **Attachment Points** — the document's own obligation sentences (diversified
  across sections), quoted with locations, as the exact places a
  restriction-protection pairing would attach.

Quotes are whitespace-normalised verbatim substrings of the assessed text
(`SF9.1`); span-window patterns use DOTALL in both scorer and locator so
hard-wrapped prose earns proximity signals (`SF9.2` guards the parity).

## Output Artifacts

A single assessment run emits three deterministic artifacts from one set of
results — they never diverge, and none contains an independent claim:

| Artifact | Audience | Contents |
|---|---|---|
| `reports/laif_real_world_assessment.md` | Reviewers, document owners | Full assessment: plain-language reading, evidence locator, not-found placement guidance, attachment points, peer exemplars, scorecards, remediation |
| `reports/laif_executive_summary.md` | Executives, boards, ministers | One page: the finding, corpus at a glance, highest-value actions, what good looks like, how to read it |
| `reports/laif_assessment_data.json` | GRC tooling, dashboards, independent re-analysis | Schema `laif.assessment.v1`: verdicts, scores, calibration, functional alignment with locations, outlines, anchors, gaps, remediation; findings and locations only, never bulk source text |

Every artifact carries the corpus fingerprint, so any citation can state exactly
which texts produced it. The JSON export marks each record `citable` strictly
according to its provenance classification, and carries the same boundary
notice as the reports: diagnostic model output, not a legal-validity
determination, not certification, not a compliance rating.

Executive-summary discipline (enforced by `test_semantic_fidelity.py` group
SF11): the summary must stay a one-pager, must never list adoption of the
assessing framework's vocabulary as a priority action, and must carry the
diagnostic-boundary, citability, and reproducibility statements.

## Drafting Register Neutrality

Governance substance is expressed in different registers by different
institutions, and the register is not the substance. Legal drafting says
"shall"; corporate standards and clinical procedures say "must"; first-person
public commitments say "we will". Regulators name a "provider" or "deployer";
a bank names a "Chief Risk Officer", a "Model Risk Committee", and "model
owners"; a hospital names a "Clinical Safety Officer". A framework declares a
"lifecycle"; a corporate standard writes a "change control" clause. A
supervisory instrument writes "proportionate to risk"; an operating standard
writes "a drift breach above 5% must be escalated within 5 working days".

Every rubric signal is therefore keyed to the **function** the language
performs, not to one institution's word for it:

| Signal | Function it detects | Registers accepted |
|---|---|---|
| mandatory obligation language | a non-discretionary duty | `shall`, `must`, `we will not` |
| named responsible parties | a role that can be held to the duty | regulatory actors, named officers, committees, boards, owners, internal audit, suppliers |
| risk-proportionate thresholds | a stated point at which something counts as a problem | proportionality language, named thresholds, tolerances, quantified breach triggers |
| full lifecycle scope | governance of the system after approval | `lifecycle`, change control, re-approval, retraining, decommissioning |
| human oversight | a person in the decision path | oversight, human-in-the-loop, human review, human decision-maker, manual review, referral to a human |
| explainability | an account of a specific decision | explainability, interpretability, "explanation of any individual decision", reasons for the decision |
| enforcement consequences | what happens on breach | penalties and sanctions, material breach, termination, suspension, rejection of non-compliant evidence |

The same rule governs the functional-alignment layer: a document that writes
"no model enters production unless all of the following hold simultaneously …
partial satisfaction is not approval" has stated an all-must-pass threshold
gate, and is scored as having one.

Two consequences follow, and both are enforced by tests:

1. **Register must never suppress substance.** A structure the document
   demonstrably contains must not be reported as absent because it is worded
   institutionally rather than legally. `InstitutionalRegisterDetectionTests`
   in `tests/test_document_processing_runner.py` pins this against a document
   that expresses every construct in corporate vocabulary.
2. **Breadth must never manufacture substance.** Ordinary business prose must
   still score near zero, and sector vocabulary without governance architecture
   must still be flagged. `NonGovernanceTextTests` and the adversarial suite's
   sector-gaming group pin this from the other side.

## Gap Detection Discipline

A gap is reported only where the document creates an expectation and leaves it
unclosed. Two rules keep the register honest:

- **A gap rule may name several closing controls, and fires only if all of them
  are missing.** A single proxy signal was too coarse: a document could carry a
  complete escalation chain — a named threshold, a notification deadline, a
  material-breach consequence — and still be told it lacked "thresholds",
  because the one proxy chosen for the rule used different vocabulary.
- **An empty register is a finding, and which finding depends on the document.**
  A text too thin to create expectations is reported as such, with its operative
  signal density stated. A substantive document that leaves nothing unclosed is
  reported as exactly that — and is told, in the same breath, that this is a
  reading of the text and not a certificate that the controls exist or operate.
  Thinness is measured by operative-signal density and structural position, never
  by the alignment verdict: a document can express every construct in its own
  vocabulary and still be two paragraphs of intent.

Control recommendations are named for the gap they close. Instrument-specific
naming (`_CONTROL_NAME_BY_PROFILE_AND_GAP`) applies only where the instrument is
identified by anchors in the document itself *and* that instrument's own
vocabulary names the control differently; otherwise the name is derived from the
gap type. A control name that does not correspond to its own gap is a reporting
defect, and is tested for.

## Self-Contradiction

A gap is something a document omits. A contradiction is something it revokes: a
protection asserted in one clause and negated in another — "committed to full
transparency" beside "cannot be disclosed under any circumstances", "human
oversight is maintained at all times" beside "executes automatically without
human review". Until it is resolved, no reading of the document is safe, so a
contradiction is reported ahead of the gap register in the executive finding and
quoted in its own section of the institutional report.

Two rules bound the detector:

- **Triggers accept the registers institutions actually use.** "We are committed
  to transparency" and "human oversight is maintained" are claims of the same
  properties as the canonical terms, and are treated as such.
- **Regulating a hazard is never committing it.** A clause that forbids the thing
  its own words name — "the restriction on automated decisioning *without human
  review* exists to protect the applicant" — is a protection, not a
  contradiction. The governing-context guard suppresses adversary matches inside
  prohibitions, and `test_semantic_fidelity.py` invariant 2 pins it.

## Instrument Form

Instrument form and subject matter are separate axes, and conflating them
misstates who a document binds:

| Form | What it is | What a reviewer must do with it |
|---|---|---|
| `procurement_assessment_form` | the buyer's instrument — a tender, questionnaire, or contract schedule | convert requirements into contract conditions and acceptance evidence |
| `vendor_compliance_submission` | the supplier's answer to it — a response or attestation | treat every assertion as a claim requiring independent verification |
| `internal_policy` | an institutional policy, standard, or procedure | test it against implementation records, ownership, and escalation evidence |
| `values_charter` | a statement of values and intent | ask for the policy that implements it; it carries no assurance force alone |

A tender that buys a clinical system is a procurement instrument whose *sector*
is clinical — the sector profile carries that dimension, and issuing-side anchors
therefore outrank sector vocabulary in classification. A values charter is
distinguished from a policy by the absence of sustained mandatory language: a
charter that says "shall" repeatedly is a policy that happens to be called a
charter.

The displayed sector basis always explains the profile the assessment actually
used. The runner's keyword detector and the engine's document-type-led routing
can legitimately reach different answers; showing one profile's name beside the
other's evidence is incoherent, and where a profile came from document type
rather than vocabulary the report says exactly that.

## Vocabulary Enumeration

Keying every signal to the function its language performs, rather than to one
institution's word for it, removes register bias — and makes the vocabulary
itself the attack surface. A document assembled from governance nouns
("Controls, procedures, protocols, safeguards, and mechanisms are in place.
Thresholds, tolerances, and materiality apply.") fires many signals and creates
no duty.

The two are separable at the sentence level. An operative sentence binds an
actor to an action; an enumeration is a dense run of governance terms with
nothing bound to anyone. `_vocabulary_enumeration()` counts a sentence as an
enumeration when it carries at least four distinct governance terms at more than
28% of its words, and either runs them as a comma-separated list or binds none of
them with a modal verb. The reported ratio is enumerated sentences over
substantive sentences.

Measured over the whole assessment corpus and every institutional fixture — EU
AI Act, NIST AI RMF, EO 14110, OECD, NHS DTAC, TUC/CIPD, plus bank, university,
procurement, charter, and attestation documents — genuine instruments score
0.00–0.06. A document built from the vocabulary scores 0.24. The threshold of
0.15, with a minimum of three enumerated sentences, sits well clear of both, and
`VocabularyEnumerationTests` re-checks every one of those documents on each run.

Consequences of a HIGH verdict, all of them stated rather than silent:

- Structural depth is HOLLOW, and the alignment verdict cannot reach
  FUNCTIONALLY ALIGNED. Functional verdicts are evidence-based, but where the
  evidence is a list of governance nouns the constructs have not been shown to
  be present.
- The finding leads with it, the coupling reading is qualified rather than
  asserted ("whether its obligations are bound to the interests they protect
  cannot be read from the text"), and the enumerated sentences are quoted in
  their own report section.
- It enters the gap register as a first-class gap, so the register is never
  silently empty for such a document, and the control it requires is a rewrite
  into operative form: for each named control, who must do it, when, evidenced
  how, and what happens if they do not.

The JSON export carries `vocabulary_enumeration` and `self_contradictions` per
document, so a consumer can see both integrity qualifiers without re-deriving
them.

## Analysing a Failure Is Not Committing It

Three layers apply the same rule, because three different detectors can
otherwise mistake a document's subject for its position:

| Layer | The mistake | The guard |
|---|---|---|
| Contradiction | "the restriction on automated decisioning **without human review**" read as a no-oversight admission | governing-context guard: adversary vocabulary inside a prohibition is a protection |
| Coupling quality | "Q1 — Coupling: Not satisfied" in a worked example read as the document disclaiming Coupling | analytical-frame guard: a document that declares Coupling structurally *and* works through a case where it fails is applying the test |
| Paraphrase | detections on documents that neither use nor claim LAIF vocabulary | reported as divergence notes, not violations (semantic-fidelity invariant 3) |

The coupling guard requires both conditions. A document that only disclaims
Coupling, with no structural declaration anywhere, is still NEGATED however many
analytical words surround the disclaimer.

## LAIF-Native Mode

LAIF-native mode asks a different question from external assessment: not whether
a document expresses the substance in its own vocabulary, but whether it
satisfies the deterministic certification gate. Its executive finding therefore
names the verdict, the specific checks that decided it, the coupling-quality
reading, and the boundary — because failing the gate says nothing about whether
a document governs well. A framework text and a source instrument are *expected*
to fail checks that only an assessment record can satisfy: LAIF v1.2 itself
fails on the two FINDING-block checks, and its own PDCA fails on the
constitutional-hierarchy checks that belong to the principal text.

## Scale Limits of Document-Level Detection

Gap rules test whether a signal is present anywhere in the document. In a short
instrument that is a fair proxy for whether an expectation is closed. In a long
one it is not: a control in section 40 does not close an obligation in section 3,
but both fire the same document-level signal. An empty register on a long
document therefore means the method has stopped discriminating, and the report
says so rather than presenting silence as a clean finding — for an instrument
past roughly 20,000 characters it directs the reviewer to assess section by
section. Stating a method's limits where they bite is part of the same
Structural Honesty obligation the reporting layer applies to provenance.

## Obligations in Table Form

Control registers, RACI tables, DPIA matrices and assurance schedules express
obligations as table rows rather than sentences. A row that pairs a control with
an owner — and usually a trigger, a threshold, and a consequence — binds an actor
to an action exactly as an operative sentence does, and is often a more precise
specification than prose. Such a document contains no "shall" anywhere, and
without recognising the form it reads as having no obligations at all.

`CONTROL_REGISTER_PAT` matches a table header pairing a control-type column with
an owner-type column, in either order; `CONTROL_REGISTER_POPULATED_PAT` requires
that header plus data rows beneath it. A populated register satisfies the
mandatory-obligation, named-parties and accountability signals, and is decisive
for the `internal_policy` document type: it is an institutional operating
instrument written in table form. Ordinary prose — including the vocabulary-soup
adversary — does not match, which the tests check directly.

## Presence Tests Read the Source, Never the Detector

A rubric signal can fire on a word used in another sense. "Review" in "review by
a person with authority to reverse the decision" is redress, not monitoring, so
a document containing only that clause was told its monitoring lacked
thresholds. A gap rule may therefore carry a `present_text` condition: the
source itself must contain the language the expectation rests on.

The sample tested against is built strictly from verbatim source fragments —
located signal quotes, functional-alignment evidence, and the quote bank. It
deliberately excludes rubric labels and any other detector-authored string:
"Auditability: review / monitoring mechanisms" is the detector's vocabulary, and
letting it satisfy a presence test would make the condition self-confirming.

## Artifact Coherence

Three artifacts describe one run, and a reader who opens two of them must not
find them contradicting each other. Four rules are enforced by tests:

- **One fingerprint, one date.** `_corpus_fingerprint()` and `REPORT_DATE` are
  each defined once. The markdown report previously recomputed the fingerprint
  inline and `test_real_world.py` held its own copy of the date, so a change to
  either definition would have made two artifacts describing the same run
  disagree about which corpus and which date produced them. The report date is a
  committed constant rather than the current date, because the artifacts must
  regenerate byte-identical; it is updated when the corpus or the engine changes
  materially enough to make the results new.
- **Construct coverage is shown on both axes.** The technical appendix's
  coverage table gives LAIF-native form *and* functional alignment side by side.
  Showing the vocabulary reading alone — `Coupling: false` beside a report
  finding that the document's obligations are bound to the interests they
  protect — reproduced inside the appendix exactly the confusion the two-axis
  model exists to prevent.
- **A functionally present construct is never called missing.** Remediation
  patches are conditioned on the functional verdict: where the substance is
  present, the only thing absent is LAIF's wording, and the patch says so.
  Where a construct is PARTIAL it is reported as partially expressed, not as
  missing. The Coherence Test is LAIF's own named decision instrument, so its
  absence from an external document is adoption distance by construction.
- **Certification-channel items never outrank real gaps.** Distance from LAIF's
  vocabulary is scored `low` severity and `optional_laif_adoption` priority. A
  terminology gap names the LAIF terms it did not find, so it is classified
  before the construct-name check — otherwise listing "Coupling, Coherence Test,
  Integrity Layer" as *missed vocabulary* was rated as severe as missing the
  constructs themselves.

## Precedence Between a Document's Own Provisions

The structural rubric's heaviest single signal asks whether a document orders
its own rules. LAIF states this as a three-tier hierarchy with a non-amendable
apex; a regulation writes "without prejudice to"; a corporate standard writes
"issued under the Group Risk Framework"; a policy writes "in the event of
conflict, X prevails"; any of them may bar waiver. All state which rule wins,
and the signal accepts all of them.

The finding is phrased for a reader who has never seen LAIF — "no precedence
rule between the document's own provisions" — and its remediation names the
three questions the text has to answer (which provision prevails on conflict,
what cannot be waived, what this document is subordinate to) before offering
LAIF's three-tier form as one way of answering them.

## Remediation Must Be Actionable

Two rules govern what the remediation layer is allowed to say:

- **Certification-channel items recommend no action.** Where a construct's
  substance is already present, or the construct is LAIF's own instrument, the
  patch says so in one sentence and asks for nothing. The public report lists
  them only as a count with a line explaining what they are — telling a reader
  to "define an institution-specific control" for not having used LAIF's words
  is both wrong and the grandstanding the reporting layer exists to avoid.
- **A recommendation names what to write, not what is missing.** The generic
  template restates the gap; specific findings carry specific remediation. The
  precedence finding, for instance, names the three questions the text must
  answer — which provision prevails on conflict, what cannot be waived, what the
  document is subordinate to — and lists the drafting forms that answer them.

Mode resolution happens before findings are worded. Several findings differ
between external-framework and LAIF-native assessment, and the raw `mode`
parameter is `None` whenever a caller relies on auto-detection — which silently
gave external documents the LAIF-native wording until the resolution was moved
ahead of the failure-mode block.
