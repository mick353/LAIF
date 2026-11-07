# Continued evidence-boundary and quotation repairs

The follow-up extends the prior repairs to JSON findings, score reasons and remediation text. A missing match no longer establishes an absent dimension, unenforceable instrument, automatic Q1/Q2 failure or impossibility of audit in the affected paths. A detected Coupling structure no longer stands in for complete LAIF compliance. Detector categories, scores and formal verdict rules remain unchanged.

The quotation gate now rejects dangling complements such as “shall demonstrate that the high-risk AI system” and trailing reference prepositions. Candidate text is expanded when the source paragraph continues beyond a PDF line boundary, retaining qualifiers rather than admitting an apparently complete prefix. If the continuation cannot pass the quality gate, the clean-looking prefix is not silently used as a substitute. This is a deterministic extraction/admission repair, not proof of perfect language understanding.

## Executed checks

- Nine focused evidence-boundary tests PASS, including three new JSON/complement/continuation regressions.
- Existing document-processing suite: 148 tests PASS.
- Full repair-branch local gate: **382 discovered tests PASS** in 26.564 seconds, plus additional governance, source/format/provenance, adversarial/semantic and deterministic-report gates. Full log retained as `continued-full-local-verification.log`.
- Actual DTA and EU source runs PASS: 10 and 12 primary quotations respectively; completeness gates and all 22 exact raw-text offset spans checked. Scores/categories preserved. See `followup-source-regression.json`.
- Comparison against main across ten baseline documents preserves component/aggregate scores, formal verdicts, detector categories, functional evidence and score-trace signal/weight data. Explanatory reason text changes intentionally.
- Combined PR #98 + updated #99 full gate: **391 discovered tests PASS**, plus the additional gates. No full-gate command skipped. Combined tested tree: `7dccd6a0098064a82067e81438a28629d3ad8e3d`; repair code tree before this validation record: `be9f91e8a68d6ce179bd92a12a6434f413fee7c1`.

Framework/DOCX files are unchanged in this follow-up; the previously reviewed rendering/parity record remains applicable. Protected historical reports and source bytes remain unchanged. Baseline generated artefacts were regenerated for the new fingerprint. No GitHub merge, main update, Actions run or paid model API was used.
