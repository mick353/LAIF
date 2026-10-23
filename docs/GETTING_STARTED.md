# Get from a policy document to an actionable review

LAIF is a local Python toolkit. Start with its included synthetic document, inspect the outputs, then use a document you are authorised to review.

## 1. Run the included example

Install Git and Python 3. The project targets Python 3.10; the published independent verification used Python 3.12 on Linux. No model API key or third-party package is needed for the built-in text extractor.

```bash
git clone https://github.com/mick353/LAIF.git
cd LAIF
python3 scripts/laif_process_document.py docs/examples/vendor-policy.md --extractor builtin
```

On Windows, replace `python3` with your installed Python launcher, such as `py -3`. Windows has not been independently verified in the published run.

## 2. Read the right output first

Start with `laif_outputs/vendor-policy.institutional_report.md`.

| Output | Use it for |
|---|---|
| `vendor-policy.institutional_report.md` | Executive finding, quoted evidence, strengths, gaps and practical next steps |
| `vendor-policy.technical_appendix.md` | Technical scoring and interpretation detail |
| `vendor-policy.laif.md` and `.laif.json` | Full assessment and machine-readable data |
| `analyst/vendor-policy/quote_bank.md` | Check quotations against the input |
| `analyst/vendor-policy/governance_gap_register.json` | Inspect the identified control gaps |
| `analyst/vendor-policy/control_recommendations.json` | Turn gaps into proposed controls for human review |
| `analyst/vendor-policy/AI_ANALYST_PROMPT.md` | Instructions for further analysis with an assistant of your choice |

The sample is deliberately incomplete. It is not a benchmark or a recommended policy template. [Inspect the committed example and actual output](examples/README.md).

## 3. Review your own document

```bash
python3 scripts/laif_process_document.py /path/to/your-policy.md --extractor builtin
```

Use `.txt`, `.md` or `.markdown` for the dependency-free path. Keep private inputs and generated outputs outside the public repository or in the ignored `laif_outputs/` directory. Never add confidential material to a public commit.

To select a sector and a separate output directory:

```bash
python3 scripts/laif_process_document.py /path/to/your-policy.md --extractor builtin --sector government_service_delivery --output-dir /path/to/private-results
```

Use `--no-write --print-report` to print without writing report or index files. Run `python3 scripts/laif_process_document.py --help` for all options.

## Word and PDF

For `.docx` and PDF files, choose an installed optional extractor. For example, in your own virtual environment:

```bash
python3 -m venv .venv
# Activate the environment using the command appropriate to your operating system.
python -m pip install python-docx pypdf
python scripts/laif_process_document.py /path/to/policy.docx --extractor python-docx
python scripts/laif_process_document.py /path/to/policy.pdf --extractor pypdf
```

These packages are optional and installation needs network access. Text extraction runs locally. The runner does not silently perform OCR: image-only PDFs need a separate authorised extraction process. Always inspect extracted text and warnings before relying on the assessment. Docling and MarkItDown are additional optional adapters; they were not available for real-document testing in the published verification.

## Batch processing

The local batch runner processes the pending folder and writes per-document outputs and portfolio summaries:

```bash
python3 scripts/laif_batch_process_pending.py --help
```

Read its [batch-processing reference](product/REFERENCE.md#batch-processing) before placing documents in the input queue. No GitHub Actions run is required.

## Make the human review count

1. Confirm the document type and sector; automatic classification is heuristic.
2. Check source quotations in context and distinguish an omitted control from one documented elsewhere.
3. Review the proposed controls with the responsible policy, legal, assurance or operational owner.
4. Ask for evidence that controls operate, including permitted-action tests and attempted-bypass tests.
5. Record which findings were accepted, rejected or resolved with additional evidence.

Software tests verify tool behaviour. They do not establish legal compliance or institutional control effectiveness. See [assessment method](product/METHOD.md) and [evidence diagnostic reference](product/REFERENCE.md#evidence-checks).

## Verify the toolkit

```bash
python3 scripts/laif_verify.py
python3 scripts/laif_verify.py --full --base-ref origin/main
```

Use the actual pre-change base SHA when inspecting an already merged change. The [quality guide](product/QUALITY.md) describes verified capabilities and runtime limits.
