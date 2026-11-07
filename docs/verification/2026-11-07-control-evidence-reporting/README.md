# Control-evidence reporting — 7 November 2026

**Released base:** PR #103 merged with approval at
`eb3300e15790702805403ccf39887f6c20eeb3ef`, preserving its tested tree
`13e3fc206d60c569f0e02131ae4117b828fd5187`. This follow-up began on a clean
branch from that main. It remains a separate candidate until merged.

## Practical improvement

The optional assurance checker already connects a policy claim to supporting
sources, test records, action receipts and an operational-review annex. Its JSON
output was difficult for a non-developer to inspect. The new readable report
makes those relationships visible without adding a separate assessment engine.

It shows the policy quotation/hash, source inventory and checks, recorded test
decisions and environments, operational-review attribution, remediation/retest
status and remaining issues. It keeps policy claims, declared test labels,
checked receipt structure and unauthenticated reviewer records distinct. An
adverse source/test result cannot be hidden by a later passing annex.

This is a useful incremental step towards following a promise into operational
evidence. It is not a complete policy/contract/procedure obligation graph or an
automatic test of protection equivalence.

## Parsing defect fixed

The evidence/assurance/calibration readers used ordinary JSON parsing. A record
containing two different values for the same key could silently retain the last
value, including a duplicate decision or outcome field. These paths now use a
shared strict JSON object reader in the existing evidence checker. Frontier
assurance reuses it too. Nested duplicates, non-finite constants, overflow such
as `1e999` and non-object roots are rejected. This applies to CLI manifests,
action receipts, calibration datasets and pinned calibration case manifests.

Valid input semantics and existing diagnostic/readiness rules are preserved.
The assurance JSON gains trace fields and receipt metadata. No source, score,
formal verdict rule, generated baseline or canonical framework text is changed.

## Real-source executions

| Case | Actual input | Observed result | Meaning |
|---|---|---|---|
| [DTA policy-only report](actual-dta-policy-only.md) | Exact pre-deployment assessment requirement from the retained DTA v2.1 raw source | `SCOPE_UNDECLARED`, `POLICY_CLAIM_ONLY`, no operational annex; gate exit **1** | The requirement is present, but source completeness and deployment evidence were not supplied. |
| [Release evidence report](actual-release-records.md) | Real CONTRIBUTING requirement, verifier, #103's passing full log and negative-regression log/test source | `EXECUTION_UNTESTED`, `DECLARED_TEST_RECORDS`, no operational annex; gate exit **1** | These are real software test records, not the action receipts or operational review required for that stronger assurance claim. |

Both exit codes are the **expected abstention**, not a failed software execution.
No deployment, action event, receipt, independent reviewer or production result
was fabricated. The source completeness attestation for the release case is a
developer's bounded declaration, not independent proof of exhaustiveness.

[Commands and expected results](case-execution.json) ·
[Policy-only manifest](actual-dta-policy-only.manifest.json) ·
[Release-evidence manifest](actual-release-records.manifest.json).
The JSON counterparts retain the complete diagnostic output.

From the repository root:

```bash
python3 -S scripts/laif_assurance.py docs/verification/2026-11-07-control-evidence-reporting/actual-dta-policy-only.manifest.json --evidence-root . --require-operational-review --print-report
python3 -S scripts/laif_assurance.py docs/verification/2026-11-07-control-evidence-reporting/actual-release-records.manifest.json --evidence-root . --require-operational-review --print-report
```

`--print-report` writes no report. `--markdown-report PATH` saves Markdown while
keeping JSON stdout. Report paths that alias input or evidence files, including
hard links, are rejected. Relative source paths stay confined to the explicit
`--evidence-root`; by default the root is the manifest directory. Pin this
revision to reproduce dated source hashes after later repository edits.

## Verification

**Final full local gate: PASS**, exit 0, **555 discovered tests** and all additional governance, corpus, provenance, format, adversarial, semantic and deterministic-report gates. No tests or checks were skipped. [Full execution log](full-local-verification.log).

- **20 new focused reporting/parsing tests PASS**, targeted and again in the full gate. [Targeted log](targeted-report-tests.log).
- Existing targeted suites also passed: assurance/calibration **57**, frontier assurance **44**, evidence checks **17**. All were included again in the full gate.
- Both actual-source CLI cases completed and returned the expected readiness-gate exit **1**. [Execution manifest](case-execution.json) and [captured log](real-cases.log).
- All three generated baseline outputs, the protected historical report and the four engine/fingerprint sources are byte-identical to merged main. [Preservation record](preservation.json).
- Active Markdown local destinations resolve; the complete inventory and scope are in [the documentation audit](documentation-audit.json). Notion release status and the practical-use guide were reconciled with merged #103 and this separate follow-up.

[Implementation hashes](implementation-sha256.json) pin the checker/reporting files used here. The reports bind source and manifest identity; preserve this verification record and repository revision for code-level reproduction.

```bash
python3 -m unittest discover -s tests -p test_assurance_reporting.py
python3 scripts/laif_verify.py --full --base-ref origin/main
```

The focused suite covers readable claims/receipts/limits, absence of operational
evidence, adverse-record precedence, remediation/attribution, missing sources,
inert markup, default JSON compatibility, deterministic no-write printing,
honest failure reports, input-overwrite prevention, duplicate/non-finite receipts,
all four CLI readers, malformed-input no-write behaviour, pinned calibration
cases, explicit-root confinement and both real-source cases.

Early development assertions were corrected for escaped Markdown and the
existing distinction between an omitted receipt list and an empty list. The
production readiness rules were not weakened to make those assertions pass.

## Limits and next evidence step

All tests were executed in Work cloud Linux/Python 3.12.14. Text/JSON/Markdown
paths are standard-library-only, including `python -S`; no paid API, user's PC or
GitHub Actions is used. Windows/Python 3.10 execution was not performed here.

A readable evidence chain does not prove that the cited event occurred, that a
reviewer is independent, that a remedy works or that the evidence is exhaustive.
Independent holdout review, measured user comprehension and real operational
records remain needed. The [plain-English use cases](../../product/USE_CASES.md)
identify current support and further expansion without claiming unique or
superior field performance.
