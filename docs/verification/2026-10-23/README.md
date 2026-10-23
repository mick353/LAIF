# Independent offline LAIF validation — 23 October 2026 AEDT

Result: the original current main failed full validation. The corrected local
branch passes the complete verifier with network access blocked, both with
optional parsers installed and in a fresh standard-library-only environment.
No GitHub Actions were invoked. Automatic approval review initially rejected
remote publication. Mike subsequently explicitly approved publishing the tested
branch and opening its review PR. Publication and merge state are recorded in
the associated PR; this report records the independently executed validation.

## Source identity and execution environment

- Repository: https://github.com/mick353/LAIF
- Inspected main / PR #73 merge: `dd3fd39c2ac09de37cb12c879388ae5761ac2e52`.
- PR #73 pre-merge base: `bf09fd355c9e108af2c2c3fc0c34befa71766782`.
- Fix commit: `ccfc8d4cf3658aa326fb92adea635ff729f8c148`.
- Local branch: `fix/offline-validation-20261023`, created from clean main
  after verifying 0 ahead / 0 behind; GitHub open-PR lookup returned none.
- Linux, CPython 3.12.14. Python 3.10 was unavailable and was not executed.
- Initial full run used the historical base above, not unchanged origin/main.
  That comparison contained all 12 PR #73 changed paths. Five configured
  semantic-sensitive paths changed; no configured terms occurred in their
  changed lines. Neither protected historical report changed.

## Executed results

| Check | Original main | Corrected branch |
|---|---|---|
| Evidence diagnostic tests | 14 passed | 17 passed |
| Governance config and historical-base diff checks | Passed | Passed |
| Four validate.py modes | Passed | Passed |
| unittest discovery | 308 tests, 1 failure and 2 errors | 312 passed |
| Standalone adversarial suite | Not reached after discovery failure | 82 passed |
| Standalone provenance suite | Not reached | 52 passed |
| Standalone semantic fidelity suite | Not reached | 68 passed |
| Real-world assessment generation, twice | Not reached | Passed; identical output |
| Committed-report drift / untracked reports | Not reached | Passed |
| Separate verbose governance suite | — | 48 passed |
| Deliberately broken evidence protections | — | All 7 detected |

The 17 evidence and 48 governance tests are included in the 312 discovered
tests. Repeated executions are not additional distinct tests. Validation
assertions and standalone suites use their own counting conventions.

The complete corrected gate passed twice in distinct runtime conditions:

1. Installed optional libraries, historical PR #73 base:
   `python3 ../offline_gate.py scripts/laif_verify.py --full --base-ref bf09fd355c9e108af2c2c3fc0c34befa71766782`.
2. Fresh virtual environment created with `python3 -m venv --without-pip`,
   then its Python ran the same offline harness and full verifier against
   `origin/main`. The branch was one committed change ahead of that base;
   this comparison was not empty. docx, pypdf, PyPDF2, docling and markitdown
   were all confirmed unavailable in that environment.

The audit harness installed a Linux seccomp filter denying `connect`, `sendto`,
`sendmsg` and `sendmmsg` with ENETUNREACH, verified a blocked connection probe,
then exec'd the verifier. The kernel filter persisted into subprocesses. This
was executed network denial, rather than an inference from source inspection.
The harness requires Linux libseccomp; LAIF itself does not depend on it.

## Confirmed defects and corrections

1. Evidence records with omitted/null quotes could become REVIEW_READY because
   the artifact loader uses None to mean no quote check for the policy file.
   Evidence records now separately require a nonempty string quote. Tests
   exercise omitted, null, blank and non-string quotes, plus strict CLI exits.
2. List/object type or outcome values caused uncaught TypeError during set
   membership. Metadata now undergoes string checks first; malformed records
   become EVIDENCE_INVALID and strict CLI calls exit 1 without a traceback.
3. Explicit optional parsers leaked library exceptions for corrupt documents.
   They now use the existing extraction attempt wrapper and raise the documented
   ExtractionError. The original corrupt-file tests pass with python-docx and
   pypdf installed; an added regression covers all four explicit adapters using
   deterministic injected parser failures.
4. A README assertion still required the retired CI wording. The assertion now
   requires the current local-verification wording, preserving every other
   product-mode and authority-boundary assertion.

No canonical assessment rule, scoring engine, spec, corpus or provenance
policy changed. Deterministic report regeneration changed only the JSON
toolchain fingerprint (`b3cd1b65f5da3dd0` to `b9759941d75b8fbe`) because the
document processor is fingerprinted. All remaining JSON content compared equal;
the generated Markdown reports stayed unchanged.

## Negative controls and change-sensitive governance

Executed evidence fixtures reject policy-only claims, missing coverage,
tampering, invented quotes, adverse outcomes, contradictory and duplicate IDs,
directory escapes and external symlinks. Positive records still pass.

Independent mutation probes disabled one protection at a time in memory:
artifact hash, exact quote, required quote, negative coverage, adverse outcome,
contradiction handling and duplicate handling. Every deliberately broken version
caused assertion failures in its corresponding regression test, with zero test
errors. Repository source was not modified by these probes.

The governance suite constructs temporary Git repositories and commits changed
protected files, then verifies exit 1 and the named offending path. Other
fixtures commit configured semantic term changes and verify advisory notices
with exit 0. They cover harmless changes and invalid/missing base references.
The semantic check is intentionally advisory, not a semantic approval gate.

Protected artifact SHA-256 values, equal to original main:

- `reports/laif_full_assessment.md`:
  `24e7b3cd8fad55dd2f711f6ad867bc1ea975f8cd89c7739ded7c6421940f8c97`.
- `reports/laif_assessment_aus_ai_policy_v2.md`:
  `4687297fe2f15bb92638ee78f08a08937b4d0b304254abb5ca00a6880c9db1c0`.

## Omissions and practical limits

- The EU AI Act manifest remains PENDING_INGESTION. Validation explicitly skips
  its source hash/file checks; four other manifests are ASSESSED. This existing
  omission was not repaired by inventing or acquiring replacement source text.
- Python 3.10 compatibility was not executed; neither was Windows execution.
- Docling and MarkItDown were unavailable: missing-library handling and injected
  parser failures were exercised, not real document extraction with those tools.
- Hashes, quotes and declared outcomes establish evidence integrity relative to
  supplied records; they do not independently prove operational effectiveness,
  legal status, production coverage or truth of self-reported outcomes.
- Unchanged-main success is not claimed. Original main failed; the fixed commit
  passed. Remote main remains unchanged until the patch is approved and merged.

## Evidence and reproduction

`baseline.log.gz`, `full-offline.log.gz`, `stdlib-offline.log.gz`,
`negative-controls.log.gz`, `governance-controls.log.gz` and `targeted.log.gz`
contain actual execution output. `sha256.json` records their compressed hashes.
The two `.py.txt` files preserve the execution harnesses; copy them beside a
checkout named LAIF and remove the `.txt` suffix to reproduce the commands.
For the second environment, use its Python executable to invoke the harness.

`fix.patch` is the exact six-file fix commit, including the fingerprint-only
generated-report update. Apply with `git am fix.patch` to the inspected main,
then run `python3 scripts/laif_verify.py --full --base-ref dd3fd39c2ac09de37cb12c879388ae5761ac2e52`.
Evidence additions in this directory are supplementary documentation; they do
not change the code exercised by the recorded gate.
