# Quality and verification

LAIF's current document-processing core runs locally in Python. The text/Markdown path uses the standard library and does not require a model API key. Word and PDF support uses optional extraction packages.

## What has been executed

The **23 October baseline** complete local verifier passed on Python 3.12 on Linux with network connection and send operations blocked by an inherited kernel filter. That historical full gate also passed in a fresh environment without optional Python packages. These results predate the 30 October optional assurance and calibration extension.

The executed gate covered 312 discovered tests, plus standalone adversarial, provenance and semantic-fidelity suites. Evidence-diagnostic tests are included in the discovered total. The gate also ran corpus validation, change-sensitive governance checks, repeated corpus-report generation and report-drift checks.

Seven deliberate in-memory mutations disabled individual evidence protections. Their corresponding regression tests detected every mutation through assertion failures, demonstrating that these tests can reject the broken behaviour they are intended to guard against.

The consumer example has been processed with the built-in extractor. Its committed institutional assessment and quote bank match actual generated output, and the assessment records the matching input SHA-256.

## What those results mean

They provide evidence that the checked implementation operates locally and that the exercised protections detect their test cases. They do not measure universal detection accuracy or establish control effectiveness in a production organisation.

The toolkit targets Python 3.10. The independent execution described here used Python 3.12; Python 3.10 and Windows execution have not been verified by that full run. A [separate focused Windows record](../verification/2026-10-23/windows-example.md) covers the Python 3.11 text example, evidence and local batch checks, governance checks and provenance mode. Optional Docling and MarkItDown adapters were not available for real-document extraction testing. Automatic classification and findings require human source review.

## Run the checks yourself

```bash
python3 scripts/laif_verify.py
python3 scripts/laif_verify.py --full --base-ref origin/main
```

See the [verification reference](REFERENCE.md#verification) for base-reference handling. No GitHub Actions run is required.

[Product home](../../README.md) · [Getting started](../GETTING_STARTED.md) · [Worked example](../examples/README.md)

## 30 October 2026 assurance extension: current verification boundary

The optional source-scope, action-receipt, mutation, synthetic calibration and operational-review code was compiled and **56 focused local tests passed** in an isolated offline test directory. Two repeated synthetic-calibration reports matched byte for byte. The new blob contents were matched to local Git object hashes. These tests use a compatibility copy of the unchanged existing evidence checker rather than a complete repository checkout.

**Not yet performed:** the current whole-repository `python3 scripts/laif_verify.py --full --base-ref <base>` suite; the complete checkout was unavailable in the implementation session. No result from the earlier 312-test baseline is represented as a fresh test of these new files. Real-world classifier error rates, independent replications, verified external reviewer identities and live enforcement outcomes remain unmeasured. The eight-case generated calibration corpus is synthetic and must not be advertised as field accuracy. No GitHub Actions was invoked.
