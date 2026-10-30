# Evidence control calibration (optional, local-only)

Purpose: identify the difference between a documented policy claim and source-grounded evidence of its execution. This is a separate diagnostic adjunct to the LAIF assessment engine, not a new certification or scoring layer. It addresses the 23 October 2026 research brief on monitoring coverage, prompt-framing bias, negative controls and tool authorisation.

## Local commands

    python3 scripts/laif_verify.py
    python3 scripts/laif_verify.py --full --base-ref origin/main
    python3 scripts/laif_evidence_checks.py /private/evidence/manifest.json --require-review-ready

The first two commands use local Python, never GitHub Actions. The optional evidence checker has no model or network dependency. It reads files adjacent to the manifest and prints JSON to stdout. Keep operational logs, personal details, vendor contracts and other sensitive evidence outside the public repository; do not commit them.

## Source-grounded evidence manifest

The JSON manifest requires policy_file, policy_sha256, and controls. Each control has a unique id, an exact claim_quote from the policy, and optional evidence records. Example:

    {
      "policy_file": "policy.txt",
      "policy_sha256": "64-lowercase-hex-digits-of-policy-file",
      "controls": [
        {
          "id": "execution-authorisation",
          "claim_quote": "Exact verbatim policy claim",
          "evidence": [
            {
              "type": "positive",
              "test_id": "allowed-request",
              "file": "allowed.txt",
              "sha256": "64-lowercase-hex-digits-of-allowed-file",
              "quote": "Exact excerpt from allowed.txt",
              "outcome": "PASS"
            },
            {
              "type": "negative",
              "test_id": "blocked-bypass",
              "file": "blocked.txt",
              "sha256": "64-lowercase-hex-digits-of-blocked-file",
              "quote": "Exact excerpt from blocked.txt",
              "outcome": "PASS"
            }
          ]
        }
      ]
    }

The SHA-256 strings above are placeholders, not valid digests. Paths must be relative to the manifest directory; absolute paths, directory escapes, missing files, altered bytes and ungrounded quotes are rejected. Positive tests concern legitimate permitted operations. Negative tests concern disallowed actions or attempted bypasses. Test type and test ID uniquely identify the test; duplicate or inconsistent records do not inflate coverage.

## Results and limitations

- POLICY_ONLY: source-grounded claim, no test records.
- UNSUPPORTED_CLAIM: claimed quote is not supported by the supplied policy file.
- EVIDENCE_INVALID: malformed, duplicated, missing or mismatched supporting evidence.
- CONTRADICTORY_RECORDS: the same test identity reports both PASS and FAIL.
- OBSERVED_FAILURE: a source-grounded test record reports FAIL.
- INCOMPLETE_CONTROLS: tests cover only one of positive or negative scenarios.
- REVIEW_READY: both types present, SHA-256 and quote checks succeed, no duplicates, contradictions or recorded failures.

REVIEW_READY means ready for human review, not operational effectiveness verified. The algorithm verifies artefact integrity relative to supplied digests and quoted text, *not* the truth, independence or production representativeness of recorded outcomes; an incorrect self-reported PASS remains possible. The optional --require-review-ready gate returns nonzero unless every declared control is REVIEW_READY (including an empty control list). Without the gate, diagnostic findings do not cause a failing exit code.

A reviewer must independently confirm test execution, applicable permissions, monitoring coverage, operational provenance, independent negative controls and whether legitimate actions continue to work. These checks cannot determine legal validity, LAIF-native compliance, the Coherence Test, the Integrity Layer or PDCA outcomes. They do not alter assessment_engine.py, validate.py, report generation, official sources, or canonical meaning.

Regression tests cover policy-only assertions, omitted controls, tampering, unsupported source quotes, adverse outcomes, contradictions, duplicate test IDs, path confinement, strict-gate exit behaviour and attribution/order invariance. They are synthetic test fixtures, not measured deployment false-positive rates.

## Strict evidence scope, action receipts, calibration and operational review

The optional [assurance and calibration extension](ASSURANCE_CALIBRATION.md) adds source inventories (including missing required attachments), receipt-derived ALLOW/BLOCK decisions, hypothetical check-removal and constant-output mutation probes, frozen labelled calibration with leak detection and confidence intervals, and a separately recorded operational-review/retest annex. Existing evidence manifests and scores remain unchanged.

```bash
python3 scripts/laif_assurance.py /private/evidence/manifest.json --strict-scope --strict-actions --require-review-ready
python3 scripts/laif_calibration.py --make-synthetic-corpus /tmp/laif-calibration-synthetic
python3 scripts/laif_calibration.py /tmp/laif-calibration-synthetic/dataset.json
```

A passed diagnostic is **not** independently verified operational evidence or LAIF-native certification. Synthetic calibration fixtures establish software behaviour, not institutional accuracy. No GitHub Actions or external model service is involved.
