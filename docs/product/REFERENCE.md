# LAIF command and output reference

Use this guide for the implemented local workflow. Start with [Getting started](../GETTING_STARTED.md) if you are running LAIF for the first time.

## Document processing

```bash
python3 scripts/laif_process_document.py INPUT_FILE
```

The default mode is `external_framework`, the sector is automatically selected, and outputs are written under `laif_outputs/`. The built-in extractor supports `.txt`, `.md` and `.markdown`. Use `--extractor builtin` to select that path explicitly.

| Option | Purpose |
|---|---|
| `--mode external_framework` | Diagnose an external document in its own vocabulary; the default mode |
| `--mode laif_native` | Apply the strict internal LAIF-native channel |
| `--sector PROFILE` | Select a diagnostic sector instead of the automatic heuristic |
| `--document-name NAME` | Set the report's document name |
| `--source-type TYPE` | Supply source-type metadata |
| `--output-dir PATH` | Choose where reports and analyst outputs are written |
| `--extractor builtin` | Process text or Markdown without optional packages |
| `--extractor python-docx` | Process Word documents using an installed optional parser |
| `--extractor pypdf` | Process PDFs using an installed optional parser |
| `--fail-on-warnings` | Return a failure when extraction records warnings |
| `--no-write --print-report` | Print the assessment without creating reports or an index |

Run `python3 scripts/laif_process_document.py --help` for the complete flag set. The runner also exposes optional Docling and MarkItDown adapters; their use requires the corresponding packages. Extraction does not silently perform OCR. Inspect warnings and extracted text before relying on an assessment.

## Outputs

For an input named `vendor-policy.md`, a successful write-enabled run produces:

| Output | Purpose |
|---|---|
| `vendor-policy.institutional_report.md` | Executive finding, evidence, strengths, gaps and recommended next actions |
| `vendor-policy.technical_appendix.md` | Scoring and technical detail |
| `vendor-policy.laif.md` | Full assessment report |
| `vendor-policy.laif.json` | Structured assessment and processing metadata |
| `analyst/vendor-policy/quote_bank.md` and `.jsonl` | Source quotations for review |
| `analyst/vendor-policy/governance_gap_register.json` | Identified control gaps |
| `analyst/vendor-policy/failure_pathways.json` | Structured potential failure pathways |
| `analyst/vendor-policy/control_recommendations.json` | Proposed controls and review actions |
| `analyst/vendor-policy/analyst_bundle.json` | Structured material for follow-up analysis |
| `analyst/vendor-policy/AI_ANALYST_PROMPT.md` | Instructions for an assistant-assisted follow-up |
| `laif_processing_index.jsonl` | Append-only processing record |

Source identity includes the original filename and SHA-256. Processing metadata also records extraction details, output paths and a processing timestamp. Run-specific metadata is not a promise that every output byte will be identical across different machines and run times.

The institutional report and quote bank from the included demonstration are available as [actual generated sample outputs](../examples/README.md).

## Sector profiles

Available profiles include general AI governance, government service delivery, departmental AI development, procurement/vendor governance, clinical AI, employment/HR, education and financial services. Use the exact option values displayed by `--help`. Review automatic classification before relying on it.

## Batch processing

```bash
python3 scripts/laif_batch_process_pending.py --help
python3 scripts/laif_batch_process_pending.py --max-files 20
```

The batch runner reads supported documents from `laif_inputs/pending/`, maintains processed/failed queues, generates per-document outputs and produces batch and portfolio summaries. A fresh clone has empty queues; place only your intended inputs there. Local queue contents and outputs are ignored by Git. Original public-source custody files are retained in `docs/verified/manual_ingest/`, and prior batch records are preserved under `docs/verification/2026-05-11/`. Inspect the command's options and output paths before processing a private collection. Keep confidential inputs and outputs out of public commits.

## Evidence checks

```bash
python3 scripts/laif_evidence_checks.py /path/to/manifest.json
python3 scripts/laif_evidence_checks.py /path/to/manifest.json --require-review-ready
```

The manifest identifies a policy file and its SHA-256, an exact policy claim, and supporting test records. Each test record identifies a relative file, SHA-256, exact quote, positive/negative type, test ID and declared PASS/FAIL outcome.

The diagnostic checks file confinement and identity, quotations, declared test coverage, duplicate identities, contradictions and adverse outcomes. `--require-review-ready` returns nonzero unless every declared control meets the review-ready conditions; an empty control list does not pass.

`REVIEW_READY` means ready for human review of the supplied evidence. It does not establish truthful execution, independence, production coverage or operational effectiveness. Private test evidence should remain outside the public repository.

## Verification

```bash
python3 scripts/laif_verify.py
python3 scripts/laif_verify.py --full --base-ref origin/main
```

The targeted command checks the evidence diagnostic and governance configuration. Full mode adds change-sensitive governance checks when a base is supplied, corpus validation modes, test discovery, standalone suites, report regeneration and drift checks. It never invokes GitHub Actions.

For an already merged change, supply its actual pre-change base SHA. Comparing unchanged main with itself produces an empty diff, which does not demonstrate that change-sensitive protections reject invalid changes.

The semantic-boundary check is advisory. Protected-artifact drift is blocking. Neither constitutes automatic approval of a change's meaning.

[Product home](../../README.md) · [Assessment method](METHOD.md) · [Quality and verification](QUALITY.md)
