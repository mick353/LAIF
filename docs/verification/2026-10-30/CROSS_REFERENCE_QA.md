# Corpus cross-reference QA — 30 October 2026

The Public Article, principal text, Case Analysis, Policy Paper, and Regulatory Integration Guide lacked the standard related-document block required by `CLAUDE.md`. This change inserts the same informational line after each title block in both the published DOCX and validated TXT. It does not revise the body, scoring, assessment conclusions, or source status.

## Local checks

- `python validate.py`: checks 1–5 passed, 53 passes, zero warnings and failures; the five cross-reference warnings are resolved.
- `python validate.py --check-corpus-formats`: all eight DOCX/TXT pairs correspond, including matching load-bearing vocabulary and provision counts.
- `python scripts/laif_verify.py --full --base-ref origin/main`: passed on this branch; 373 discovered unit tests passed with two symlink-dependent skips. Verified-source, semantic-fidelity, adversarial, and deterministic-report checks passed; committed reports did not drift.
- Word rendered all five edited DOCX files to temporary PDFs. First pages were visually inspected for title-block placement and legibility. Page counts remained unchanged: Public Article 6, principal text 42, Case Analysis 14, Policy Paper 13, Regulatory Guide 20.
- A package comparison against `origin/main` found that only `word/document.xml` changed in each DOCX. All existing paragraph text remained identical; each document gained one related-document paragraph.
- No GitHub Actions run was used.

The related-document line is a navigation aid. It does not certify the documents or assert that the referenced external sources are admitted to the verified corpus.
