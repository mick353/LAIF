# Quality and verification

LAIF's current document-processing core runs locally in Python. The text/Markdown path uses the standard library and does not require a model API key. Word and PDF support uses optional extraction packages.

For external research and regulator-facing communication, use the
[scholarly neutral report and review protocol](../research/SCHOLARLY_REPORTING.md).
It reports source evidence and uncertainty rather than promoting native
framework scores to legal or safety findings. This optional pathway is
source-hashed, has a committed synthetic sample and is included in full
local unit-test discovery. Independent construct validation and real-world
classification error rates remain unmeasured; reviewer identities and
independence declarations cannot be authenticated by the tool.

## Current release and whole-source candidate

PR #104 merged at ededd1b58afc56dbd06ad0b20f8793b3d1e79e3b with its 555-test verified tree. The [substantive-review record](../verification/2026-11-07-substantive-review/README.md) records the next authored-assessment enhancement: 578 tests and all additional gates passed in a fresh cloud Python 3.13.18 clone, with 23 focused tests and pinned PDF reproduction. Earlier counts below are dated evidence.

The small synthetic sample tests workflow mechanics. It is insufficient to demonstrate interpretation quality across institutions. The wider curated corpus tests source formats and known reporting failures, but still does not measure independent accuracy or deployment outcomes.

## Historical execution records

The **23 October baseline** complete local verifier passed on Python 3.12 on Linux with network connection and send operations blocked by an inherited kernel filter. That historical full gate also passed in a fresh environment without optional Python packages. These results predate the 30 October optional assurance and calibration extension.

The executed gate covered 312 discovered tests, plus standalone adversarial, provenance and semantic-fidelity suites. Evidence-diagnostic tests are included in the discovered total. The gate also ran corpus validation, change-sensitive governance checks, repeated corpus-report generation and report-drift checks.

Seven deliberate in-memory mutations disabled individual evidence protections. Their corresponding regression tests detected every mutation through assertion failures, demonstrating that these tests can reject the broken behaviour they are intended to guard against.

The consumer example has been processed with the built-in extractor. Its committed institutional assessment and quote bank match actual generated output, and the assessment records the matching input SHA-256.

**Independent validity remains an open research question.** The tests reported
here assess execution and specified invariants, not measured agreement with
independent legal or AI-safety experts, real-world AI behaviour or regulatory
enforcement findings. Any study claiming accuracy must identify its independent
corpus and blind reviewers, pre-register the target decisions and statistics,
report disagreements and confidence intervals, and publish negative cases.
See the [research register and validation protocol](../review/2026-11-07-external-scholarly-critique-triage.md).

## What those results mean

They provide evidence that the checked implementation operates locally and that the exercised protections detect their test cases. They do not measure universal detection accuracy or establish control effectiveness in a production organisation.

The toolkit targets Python 3.10. The 23 October independent execution described above used Python 3.12 on Linux; it did not verify Python 3.10 or Windows. A [focused Windows record](../verification/2026-10-23/windows-example.md) covers the Python 3.11 text example, and the later [full Windows local gate](../verification/2026-10-30/WINDOWS_RELEASE_VERIFICATION.md) covers Python 3.13.16. Python 3.10 has not been verified by those runs. Optional Docling and MarkItDown adapters were not available for real-document extraction testing. Automatic classification and findings require human source review.

## Run the checks yourself

```bash
python3 scripts/laif_verify.py
python3 scripts/laif_verify.py --full --base-ref origin/main
```

See the [verification reference](REFERENCE.md#verification) for base-reference handling. No GitHub Actions run is required.

[Product home](../../README.md) · [Getting started](../GETTING_STARTED.md) · [Worked example](../examples/README.md)

## 30 October 2026 assurance extension: historical verification boundary

The optional source-scope, action-receipt, mutation, synthetic calibration and operational-review code was compiled and **56 focused local tests passed** in an isolated offline test directory. Two repeated synthetic-calibration reports matched byte for byte. The new blob contents were matched to local Git object hashes. These tests use a compatibility copy of the unchanged existing evidence checker rather than a complete repository checkout.

The implementation session did not run the whole-repository gate. A later [Windows local verification](../verification/2026-10-30/WINDOWS_RELEASE_VERIFICATION.md) on the existing `Z:\laif` checkout passed the full gate on Python 3.13.16: 369 discovered tests (2 skipped), provenance and semantic checks, deterministic regeneration, and committed-report comparison. This is repository verification, not independent legal or operational acceptance. Real-world classifier error rates, independent replications, verified external reviewer identities and live enforcement outcomes remain unmeasured. The eight-case generated calibration corpus is synthetic and must not be advertised as field accuracy. No GitHub Actions was invoked.
