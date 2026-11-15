# Automatic eight-criterion documentary judgments

The normal engine, document runner and guided research report now produce an
automatic judgment for each of A.1–A.4, Q1–Q3 and G.1. These are deterministic
English-language rules over supplied text, not model API calls. The module is
`scripts/laif_auto_criteria.py`; its bytes are included in the toolchain identity.
This is a new detector and interpretation layer. Existing numerical dimensions,
native certification and source-bound authored reasoning remain separate.

## Decision contract

Each criterion has three explicit components, recorded in the result. A witness
must match all patterns for its component in one contiguous source clause.
Word lists or matches assembled from disconnected passages cannot support it.
The result retains the exact clause, character offsets, extracted-text line,
quote hash and its classification. All matching clauses remain available;
deleting one cannot silently retain that clause as evidence.

| Automatic determination | Meaning |
|---|---|
| PROVISIONALLY_SUPPORTED | All three components have explicit documentary-requirement witnesses and no detected contrary wording |
| PARTIAL_SUPPORT | Some requirements or qualified mentions were found, but at least one explicit component is unresolved |
| NOT_ESTABLISHED | The rules did not establish the required support, or found only contrary wording |
| SOURCE_CONFLICT | Supporting requirements coexist with detected contrary wording; scope and exceptions need review |
| REVIEW_REQUIRED | Input is empty or the extraction-quality gate does not admit documentary conclusions |

Recommendations, hypothetical/historical examples and clauses longer than 1,600
characters are retained as qualified/context evidence rather than sufficient
requirements. Explicit denial phrases cannot count as positive support. These
are bounded lexical rules, not complete negation, exception or legal analysis.
The absence of a match does not demonstrate absence of a safeguard.

Every criterion supplies a separate plain reader summary, missing components,
framework basis, component counts and an unvalidated-inference confidence label.
No probability is fabricated. A.4 applicability remains for review; the engine
does not silently assign NOT_APPLICABLE. Operational status remains
NOT_ESTABLISHED even when documentary requirements are provisionally supported.

## Interpretation limits

Components can occur in different clauses; the software does not establish that
their actors, scope, dates and exceptions align. Inspect the quotations together.
Legal force, equivalent enforceability, universal application and proportionality
require substantive review. Empirical performance and adversarial robustness
require supplied, evaluated operational evidence. The module does not establish
those properties from policy promises. Source authority is not inferred from
the automatic label. No independent accuracy claim is made.

## Authored review and compatibility

The additive `automatic_criteria` field never overwrites `criteria_review`,
`submitted_review` or canonical reasoning. An authored review remains visibly
attributed. The research dossier's unannotated status becomes
AUTOMATIC_DOCUMENTARY_DRAFT; poor-source and author-annotated states remain.
Consumers of the old status should use the new state or inspect the additive
field. Retained reports keep their original method and wording. Old source-
locked review files must not be silently rebound to the new fingerprint.

## Verification and rollback

Focused tests cover all eight complete/partial/missing cases, 24 targeted clause
deletions and unaffected criteria, weak wording, explicit contrary requirements,
hypotheticals, exact spans, unsafe markup, extraction abstention, engine output
and a retained real NIST deactivation-clause mutation. These validate specified
mechanics and selected examples, not general accuracy. Broad historical scores
can stay constant while the new component evidence changes appropriately.

Run `python -m unittest tests.test_auto_criteria` and the full local verifier.
The committed corpus reports are regenerated; historical protected reports stay
untouched. Rollback is a revert of the release commit and restored Site engine
pin. Existing source documents and authored reviews need no content migration;
new automatic outputs retain their own method identity.
