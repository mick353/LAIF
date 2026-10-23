# Product presentation verification — 23 October 2026 AEDT

This is a documentation, graphics and synthetic-example change. It does not alter the assessment engine, framework spec, source corpus, scoring, canonical documents, protected historical assessments or generated corpus reports.

- Based on main after independently tested fixes merged in PR #74, commit `6e29d8804f65737d1d6e9640e282af1a4473df18`.
- Fresh branch began at 0 ahead / 0 behind origin/main. It was subsequently reconciled with the owner's README-only October 2026 release-date update, commit `0955aab432314b46d9a49d64648105d3354b9399`. The date is preserved.
- Full local verifier executed under the inherited seccomp network-denial harness: PASS. Command: `python3 ../offline_gate.py scripts/laif_verify.py --full --base-ref origin/main`.
- 312 discovered tests passed, including 17 evidence-diagnostic tests; standalone adversarial 82, provenance 52, semantic fidelity 68 passed. The 83 README/fragility tests also passed in the earlier targeted run.
- Four validation modes and change-sensitive governance checks passed. Two regenerated corpus-report runs were identical and had no committed-report drift.
- Included quick-start document was processed successfully with the built-in extractor. The committed institutional assessment and quote bank match the generated files byte for byte, and the assessment carries the matching source SHA-256.
- 38 local documentation/image links resolved. Self-contained SVGs parsed; no scripts, foreign objects or external resources were present.
- All three graphics were rendered and visually inspected for typography, clipping and accuracy. Social PNG is 1280×640 and below 1 MB.
- Git diff whitespace checks passed. Subsequent changes only clarify reference wording, record unavailable settings access and add this verification record. After reconciliation and historical-model labelling, the 83 README/fragility tests were rerun and passed. The front-page introduction is model-independent and contains no GPT-4 reference; original clinical case files remain historical. No implementation code changed, so the complete earlier gate was not duplicated.

Raw full-gate output: [verification.log.gz](verification.log.gz).

Remaining settings work: repository About text, discovery topics and installation of the prepared social preview require a GitHub settings-capable connection or signed-in browser. Those settings have not been applied. No distribution licence was chosen for the owner.

Compressed execution-log SHA-256: `1e361d4684d81dde2794f81b426f92650891254f95b34df321185c776e87362b`.
