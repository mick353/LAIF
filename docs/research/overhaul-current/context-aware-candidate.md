# Context-aware automatic documentary checks

This candidate makes the eight automatic checks more selective about what an excerpt establishes. It retains exact character ranges and quotation hashes. It distinguishes a direct obligation, a denial, a weak mention and a passage that needs context. Authored review remains a separate judgment.

## Controlled regression results

The previous detector matched the expected witness classifications in **9 of the original 22** controlled examples. This candidate matched **22 of 22**. A second set of 12 cases was added after reading the retained-source comparison. Across all 34 cases, the previous detector matched 14 and this candidate matched 34. The later cases are regression checks for known failures. Both sets are synthetic. They do not measure accuracy on unseen documents.

The cases cover everyday language for giving reasons, requirements that wrap across lines, exceptions, mixed or negated obligations, fences, separate table cells, and the difference between an approval and escalation. For each matched witness, tests verify the quotation against its original characters, line and SHA-256. The earlier 24 single-clause deletion checks still remove the intended component while preserving the other criteria.

## Retained document comparison

Both methods read the same five retained texts from the [locked protocol](predictions.json), with SHA-256 verified before reading and CRLF normalized to LF. The comparison includes their original scope classifications. NIST and OECD remain hash-verified local conversions. LAIF and the clinical PDCA are internal comparators. Seven of 40 criterion labels changed. Two more kept their label and changed their count of explicitly supported components.

| Retained text | Check | Previous → candidate | Why the change merits review |
|---|---|---|---|
| NIST | G.1 | Partial → not established | Assigning or documenting governance review does not show that the governing actors themselves are reviewed. |
| OECD | A.3 | Partial → not established | Broad scope and authorisation wording no longer stands in for operating boundaries or escalation. |
| DTA | A.1 | Not established → partial, zero explicit components | Related reasons or explanation wording becomes visible for review. |
| DTA | A.3 | Partial → not established | Policy applicability and ordinary approval do not establish the containment safeguards. |
| LAIF | A.3 | Provisionally supported → partial, three → two explicit components | The earlier third component used routine sign-off wording as evidence of escalation. |
| LAIF | Q1 | Remains partial, two → one explicit component | The stricter passage boundaries no longer combine adjacent text into the same witness. |
| LAIF | G.1 | Partial → not established | An independent deployment investigation or a board approving a plan does not establish review of the board itself. |
| Clinical PDCA | A.3 | Remains partial, two → one explicit component | Authorisation and human escalation are assessed separately. |
| Clinical PDCA | G.1 | Partial → not established | The prior related words did not establish a governing actor as the review target. |

The NIST comparison isolates MANAGE 2.4 (interruption/deactivation) and GOVERN 1.7 (decommissioning) as their own quotations while their criterion labels stay partial. The earlier baseline packet remains reproducible from the historical method. A lower or higher label can affect what a reviewer checks first. The comparisons here establish changes in the software’s reading, with no independent labels of document adequacy.

## Remaining interpretation work

Rules can miss equivalent wording, roles established elsewhere, obligations inherited from table headings, provisions spread over several paragraphs, and carefully drafted exceptions. Some legitimate passages will move to manual review. The software still cannot judge whether obligations are enforceable, apply in a particular situation, or are carried out. Evidence targets and qualifications are recurring challenges in contract inference research. [ContractNLI](https://aclanthology.org/2021.findings-emnlp.164/)

To repeat the controlled checks, run `python -m unittest discover -s tests -p test_auto_criteria.py`. To verify the historical packet and exercise the retained-text deletions, run `python scripts/laif_criterion_comparison.py --verify`. The candidate uses the existing automatic result schema and adds a reason beside each witness classification.
