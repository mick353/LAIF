# Document Processing Runner

## Purpose

Phase 3T adds a user-facing local document ingestion runner so a user can provide a document and ask LAIF to process it without writing custom Python snippets. The runner extracts text from a local file, records extraction metadata, sends the extracted text to the existing LAIF assessment engine, and emits markdown and JSON reports.

The runner is a convenience wrapper over existing LAIF assessment behavior. It does not change scoring, certification, validation, evidence trace logic, remediation logic, sector logic, calibration logic, governance checks, or public report rendering.

## User Workflow

Run the local CLI with an input file:

```bash
python3 scripts/laif_process_document.py path/to/document.docx
```

By default, outputs are written to `laif_outputs/`:

- `<safe_stem>.laif.md`
- `<safe_stem>.laif.json`

Use `--no-write` for a console-only summary, `--print-report` to print the markdown report, and `--output-dir DIR` to place generated outputs somewhere else.

## Supported File Types

The base repository supports deterministic built-in extraction for:

- `.txt`
- `.md`
- `.markdown`

The same command can process `.docx`, `.pdf`, and other document-like formats when optional local extraction packages are installed. Unsupported formats fail clearly rather than fabricating text.

## Extractor Strategy

The runner uses a pluggable extractor strategy:

1. `.txt`, `.md`, and `.markdown` use the built-in direct reader and require no optional dependency.
2. If a user explicitly requests an extractor with `--extractor`, only that extractor is attempted and unavailable backends fail clearly.
3. In `--extractor auto` mode, PDF, DOCX, office, HTML, image-like, and related document formats prefer Docling when installed.
4. MarkItDown is attempted as a lightweight optional fallback when installed.
5. `python-docx` is attempted for `.docx` files when installed.
6. `pypdf` or an already available `PyPDF2` fallback is attempted for `.pdf` files when installed.

The runner never makes network calls during document processing and never requires cloud OCR or external APIs.

## Optional Public Extractors

Optional local installs are documented, not required by the base repo:

```bash
pip install docling
pip install 'markitdown[pdf,docx]'
pip install python-docx pypdf
```

Docling is preferred when installed because it has broad format support, advanced PDF understanding, OCR support, local execution, Markdown/HTML/JSON export, and a simple CLI/Python API.

MarkItDown is a lightweight fallback for converting many file types to Markdown for text-analysis pipelines.

`python-docx` and `pypdf` provide targeted lightweight fallbacks for DOCX and PDF extraction.

Unstructured remains a possible future/heavy backend, not mandatory in Phase 3T, because it can require heavier system dependencies for PDF/image preprocessing.

## Extraction Metadata

Every run records extraction metadata in the JSON output and at the top of the markdown output:

- `input_path`
- `file_name`
- `file_extension`
- `extractor_requested`
- `extractor_used`
- `extracted_characters`
- `extraction_warnings`
- `extraction_errors`
- `extraction_confidence`

This metadata is also passed as local provenance into the assessment result. The extracted text is the assessed source; poor extraction can affect results.

## Failure and Warning Rules

The runner fails clearly when:

- the input path does not exist;
- the input path is not a file;
- no available extractor can handle the extension;
- extraction raises an exception;
- extracted text is empty or below the safe minimum threshold;
- `--fail-on-warnings` is set and extraction warnings were produced.

The runner never hallucinates or fabricates missing source text. It never silently OCRs scanned PDFs. If a PDF extraction returns little or no text, the runner reports that the document may be scanned or non-text and that OCR is required.

## LAIF Assessment Defaults

Default mode is `external_framework`. Users may request LAIF-native assessment mode with:

```bash
python3 scripts/laif_process_document.py path/to/document.txt --mode laif_native
```

Default sector is `auto`. The deterministic auto-sector heuristic is a processing convenience only and does not alter certification semantics, scoring weights, validation, or formal compliance. A user may specify one of the supported sector profiles explicitly with `--sector`.

## Output Files

By default, outputs go to `laif_outputs/`, which is a local generated-output folder and not a protected artifact location. JSON output contains both `extraction_metadata` and `assessment_result`. Markdown output contains an extraction metadata block followed by the standard public report rendering.

Do not commit private or sensitive processed documents or generated reports unless intentionally governed by a separate review process.

## Security and Privacy Boundary

Processing is local. The runner does not call cloud OCR, does not call external APIs, and does not make network requests during document processing. Users remain responsible for source-document sensitivity, local filesystem access, optional extractor behavior, and output handling.

## Protected Artifact Boundary

The runner does not write to `reports/`, verified corpus paths, manifests, protected governance artifacts, or validation artifacts by default. Generated runner outputs are user artifacts, not protected artifacts, unless a future governance process explicitly designates them as such.

## Evidence Trace Relationship

Evidence traces are based on the extracted text when using document ingestion. Exact traces must still satisfy the existing invariant that `matched_text` equals the assessed source slice at `source[start_char:end_char]`. If source fidelity matters, reviewers must inspect extraction metadata and, where necessary, compare traces against the original document.

## Limitations

- Extracted text quality depends on the selected extractor.
- Formatting, tables, headers, footers, footnotes, and reading order may vary by extractor.
- Scanned PDFs may require OCR; missing text must not be hallucinated.
- Optional extractor availability depends on the user's local environment.
- The runner is not a legal advice tool, safety certification, external regulatory compliance decision, or LAIF-native certification shortcut.

## Future GitHub Actions Workflow

A future Phase 3U may add a GitHub Actions workflow around this runner. Phase 3T intentionally adds the local/Codex/Claude Code CLI runner first and does not add CI workflow automation.
