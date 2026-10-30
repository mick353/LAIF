# LAIF assurance evidence, mutation controls and evaluation protocol

**Status:** optional diagnostic extension; local execution only. Introduced 30 October 2026. Does **not** amend LAIF's governance corpus, strict LAIF-native gate, PDCA, Coherence Test, assessment engine, scores, source manifests or previously generated reports. Does not call a model, network service or GitHub Actions.

## Commands (from the repository root)

```bash
python3 tests/test_assurance.py            # focused, standard library only
python3 scripts/laif_verify.py             # targeted local release checks
python3 scripts/laif_verify.py --full --base-ref origin/main  # full gate, when checkout is available
python3 scripts/laif_assurance.py /private/evidence/manifest.json --strict-scope --strict-actions --mutation-probes --require-review-ready
python3 scripts/laif_assurance.py /private/evidence/manifest.json --strict-scope --strict-actions --operational-annex /private/evidence/operations.json --require-operational-review
python3 scripts/laif_calibration.py --make-synthetic-corpus /tmp/laif-calibration-synthetic
python3 scripts/laif_calibration.py /tmp/laif-calibration-synthetic/dataset.json
```

The `--require-review-ready` and `--require-operational-review` gates implicitly enable strict scope and action checks even if the individual flags are omitted. The core `laif_evidence_checks.py` remains compatible with existing manifests. The new `laif_assurance.py` wraps the existing checker; the stricter switches apply to its diagnostic output **only**. Keep confidential evidence, operational logs, personal information, contracts and attack payloads **outside** this public repository. Output JSON contains identifiers; review it before distribution.

## P0: Source scope and missing attachments

Extend the current evidence manifest (`policy_file`, `policy_sha256`, `controls`) with a `source_inventory` and `scope_attestation`:

```json
{
  "policy_file": "policy.txt",
  "policy_sha256": "<SHA256-of-policy.txt>",
  "source_inventory": [
    {
      "id": "required-appendix", "required": true, "disposition": "inspected",
      "file": "appendix.txt", "sha256": "<SHA256-of-appendix>",
      "quote": "Exact span actually present in appendix"
    },
    {"id": "unrelated-advert", "required": false,
     "disposition": "excluded", "reason": "outside control scope"}
  ],
  "scope_attestation": {
    "reviewer": "human-reviewer-id", "recorded_at_utc": "2026-10-30T02:00:00Z",
    "complete": true,
    "inventory_sha256": "<SHA256-of-canonical-inventory-JSON>"
  },
  "controls": [
    {"id": "tool-authorisation", "claim_quote": "Exact verbatim policy claim",
     "required_source_ids": ["required-appendix"], "execution_tests": []}
  ]
}
```

`inventory_sha256` is `sha256(json.dumps(source_inventory, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))`. The provided helper `digest_json()` computes it. File paths must remain within the manifest directory; symlinks escaping that directory, invalid hashes, missing files and unsupported quotes are rejected. `required` sources marked `excluded` or `unreadable` block review readiness; **optional** excluded or unreadable sources need a recorded reason but need not block. A control referring to an undeclared required source also fails. `--strict-scope` requires an inventory, explicit required-source mapping and a hash-bound human scope attestation. It **cannot** discover unseen attachments or independently prove the inventory exhaustive; a reviewer must independently establish scope.

## P0: Action-receipt checks and mutation probes

A `control.execution_tests` entry declares a test identity, category, expected decision and **SHA-256-pinned JSON receipt**:

```json
{"test_id": "block-01", "kind": "negative", "expected_action": "BLOCK",
 "receipt_file": "block-01.json", "receipt_sha256": "<SHA256>"}
```

The receipt JSON contains `control_id`, `test_id`, `decision` (`ALLOW` or `BLOCK`), `run_id`, `executed_at_utc` (UTC offset required), `environment` (`simulated`, `staging`, `production`) and `toolchain_version`. A positive test must expect `ALLOW`; a negative test must expect `BLOCK`. A negative test that actually records `ALLOW` is an `OBSERVED_FAILURE` even if a separate manifest field falsely claims `"outcome": "PASS"`. The tool does **not** authenticate the producer of a receipt: operators must independently validate execution provenance.

`--strict-actions` requires **both** positive and negative receipt evidence; historical self-reported `evidence` entries alone do not satisfy the new operational gate. Existing adverse evidence cannot be overridden by adding receipts. `--mutation-probes` performs **hypothetical**, deterministic interventions on observed decisions: remove all checks, remove negative checks, force all decisions to ALLOW, and force all to BLOCK. A caught mutation means this checker would reject that altered **fixture**, not that an actual target system was attacked or defended. Tests cover tampered receipts, duplicate IDs, missing cases, always-allow, always-block and attempted false PASS labels. The final status describes evidence-readiness for a human, never control certification.

## P1: Frozen labelled calibration protocol

`laif_calibration.py` takes a versioned `laif.calibration.v1` dataset JSON: `dataset_version`, `cases`, and `holdout_seal`. Each case declares a unique `id`, `family` (near-duplicate/leakage grouping), `split` (`development` or `holdout`), `gold_label` (`READY` or `NOT_READY`), `label_provenance` (`SYNTHETIC` or `HUMAN_ADJUDICATED`), a relative `manifest_file`, and exact `manifest_sha256`. The holdout seal hashes sorted case identifiers, family, gold label and manifest hashes; it fails if these change without an explicit re-baseline. Keep the file and code revision fixed in an auditable Git commit or independent immutable record: a seal **inside** a mutable manifest is not itself a trusted external timestamp.

An `HUMAN_ADJUDICATED` case requires at least two distinct recorded `reviewer_votes`, and a pinned exact-source `adjudication_file`/`adjudication_sha256`/`adjudication_quote`. Reviewers may disagree; the adjudication record must justify the final label. The tool checks for family and byte-identical manifest/policy overlap **across splits**; it does not detect every semantic near-duplicate. Do not tune thresholds or fixtures after observing holdout errors without versioning a new holdout. `--require-adjudicated` rejects synthetic labels for final empirical reporting.

The evaluator runs with strict scope and strict action receipts, then publishes per-split TP/TN/FP/FN, false-positive and false-negative rates, accuracy, 95% Wilson intervals, disagreement count, dataset/holdout seals and hashes of the three evaluator files. Empty denominators display null. Wilson intervals account for simple binomial sampling error **only**: small samples, reviewer disagreement, clustered families, label contamination, domain shift and sample-selection bias remain limitations.

`--make-synthetic-corpus` creates a **deterministic eight-case toy dataset** (four development, four holdout) with absent controls, missing attachments, tampered receipts and constant-ALLOW failures. It tests software invariants and leakage checks but **does not validate performance on real institutional records**. A genuine performance claim requires human-labelled representative sources, adjudication, independent replicators and documented selection criteria. A numerical success on toy cases must never be advertised as an empirical accuracy or compliance certification.

## P2: Optional operational evidence annex

The CLI `--operational-annex /private/evidence/operations.json` accepts `laif.operational-annex.v1` and associates independent operator-review records with control IDs. Each record needs:

- `control_id`, `deployment_id`, `run_id`, `toolchain_version`, `executor`, `environment`, `executed_at_utc`, `authorisation_issued_at_utc`, `reviewed_at_utc` (UTC), `outcome` (`PASS`/`FAIL`);
- `authorisation_file`, `authorisation_sha256`, `authorisation_quote`;
- `execution_log_file`, `execution_log_sha256`, `execution_log_quote`;
- `reviewer` (different *recorded* actor than executor), `review_file`, `review_sha256`, `review_quote`;
- optional `remediation`: `change_ref`, `file`, `sha256`, `quote`;
- optional `retest`: `file`, `sha256`, `quote`, `outcome`, `executed_at_utc` **after** the first run.

An authorisation artefact must name the deployment, and execution/review artefacts must identify the same run; authorisation must precede execution, and review must follow. A recorded failure requires a documented remediation **and** a passing later retest; a remediation without retest remains `RETEST_REQUIRED`. Missing, altered or contradictory identities/artefacts produce `ANNEX_INVALID`; a complete record is only `REVIEW_RECORDED`, **not independently verified**. Reviewer identity is not cryptographically authenticated, and structured assessment does not prove an event occurred in production. The annex never changes the source/receipt diagnostic outcome. `--require-operational-review` only succeeds when **both** the core diagnostic and the annex are ready for review; it does not approve release. No private operational logs are committed by these utilities.

## Evaluation release acceptance and cost

- **Release checks:** run `python3 scripts/laif_verify.py`, the isolated `tests/test_assurance.py` suite, targeted existing evidence tests, and where a checkout exists the complete `--full --base-ref ...` gate. The PR must explicitly report what could not be executed.
- **P0 acceptance:** intentionally removed checks, omitted necessary attachments, forged PASS labels, tampering and constant action responses must be flagged; accepted valid positive/negative controls must remain accepted. Assess false positives on optional unrelated references.
- **P1 acceptance:** hashes and holdout seal stable across two identical runs, leakage injection detected, full confusion matrix and intervals produced; do not claim field accuracy until actual independent labels are available.
- **P2 acceptance:** record provenance, named authorisation, environment/version, failure/remediation/retest and reviewer records, with the gap between *recorded* and *verified* explicit.
- **Cost:** standard library and local compute only; obtaining independent gold labels and real operational evidence is a separate human/research cost.

**Boundaries:** none of these tools calls an AI API or initiates GitHub Actions. Nothing here proves lawful deployment, independent audit, actual monitoring coverage, production safety, or truth of a self-authored source. Respect applicable legal authority and the existing LAIF-native versus external-framework diagnostic separation.
