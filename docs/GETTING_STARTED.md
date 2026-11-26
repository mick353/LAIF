# Getting started with the LAIF Site

[Open the LAIF Research Workspace](https://laif-research-workspace.mick353.chatgpt.site)

Just exploring? Start with the
[public reading room](https://laif-public-guide.mick353.chatgpt.site).
It needs no sign-in and offers an example, report links and the real-document
comparison. It has no upload or analysis endpoint. This guide below covers the
separate private workspace where authorised users review their documents.

Use this guide alongside the Site. **You do not need to install Python, clone
GitHub or obtain a model API key.** The Site runs analysis in your browser and
guides you from source to findings, review and export.

The workspace currently requires authorised private access. Opening its link
does not grant access. Public GitHub is separate: it holds code, framework
documents and retained research records.

## Choose a route

| Your task | Start here |
|---|---|
| Explore without signing in | [Public reading room](https://laif-public-guide.mick353.chatgpt.site) |
| Review a document in your browser | Follow this guide |
| Understand an included assessment | Choose **Explore a worked example** on Home |
| Review how several records relate | In **Source index**, select **Map supplied documents and links** |
| Run a local copy, batches or specialist commands | [Local repository setup](LOCAL_SETUP.md) |
| Change code or contribute a source | [Contributing](../CONTRIBUTING.md) and [source contribution workflow](site/README.md) |

## 1. Explore before adding a document

On **Home**, try **The words**, **The meaning** and **The question** in the
interactive policy example. It separates the exact passage from an
interpretation and a follow-up question.

Choose **Explore a worked example** for the retained Australian Government
policy assessment. This is an authored review of a real retained document,
not a newly generated assessment or independent validation. Check its edition
and qualifications. **Source index** lets you browse and read retained sources.

## 2. Bring your source

Choose **Review your document** on Home or **Add source** in the header.
Select a PDF, Markdown or UTF-8 text file, or paste exact text. Enter its title
and record the edition, origin, completeness and jurisdiction where known.
A source website is attribution only; entering it does not fetch the document.

- Maximum source size: **8 MB**.
- Export Word files to PDF or text first. The local toolkit has a separate optional Word extractor.
- Scanned PDFs need a separate authorised text-extraction process; the Site does not perform OCR.
- Use only material you are authorised to process and store.

After adding the source, choose **Assess this document** or **2. Assessment**.
Keep the recommended **Document review** and automatic context unless an
advanced setting fits your task better. Select **Start assessment**. The first
run loads the engine and may take longer. The processing banner shows progress
and offers **Stop processing**.

## 3. Read the findings and check the source

The run opens **Findings & gaps**. Read the eight provisional documentary
checks, supporting passages and evidence still needed. Compare the extraction
with the original source, especially headings, tables and page breaks, before
recording candidate decisions.

Inspect each candidate passage in context. Record whether to keep it as a
review lead, reject it, request more evidence or mark it outside scope. Add
notes explaining your choice. These decisions do not prove that a control
operates or a legal requirement has been met.

**Not established means the scan did not establish the required wording.**
It does not prove absence. Positive wording does not prove implementation.
Automatic judgments, retained authored reasoning and your passage decisions
remain distinct.

Use **Quoted evidence** to inspect passages and **1. Source** to return to the
document. The source view shows the document and edition. **2. Assessment**
returns to the selected run's findings; **3. Review evidence** opens its quoted
passages. If the source has no assessment yet, step 2 starts one.
The review path shows your location, not completion or certification.

## 4. Review and export

Choose **4. Export** or **Reports & export** and confirm the selected assessment.
Use **Next review step** to find the next outstanding check. For automated
runs it starts with the extracted text and any unresolved source-text
candidates. When these are addressed, open the report checklist and record
who reviewed it.
Read the report, record only quality checks you have actually performed, and
add your reviewer name, role, notes and unresolved questions.

Choose **Download review bundle** to save the selected review as one ZIP.
Extract it and open `START-HERE.txt`. The ZIP includes the full Markdown report,
the JSON package, and, for automated runs, the review brief and available
pipeline files. `manifest.json` lists the exact assessment, method revision,
source hash and SHA-256 for the included files. Check extracted text and
reviewer notes before sharing. Download the original source separately.
If a retained report cannot load, use **Retry full report** in the download
panel. Use **Download individual files** if you only want one of the exports.

| Export | Contents |
|---|---|
| **Review brief** (new automated runs) | Concise provisional findings, candidate decisions and remaining review work |
| **Full report** | Full pipeline report with labelled Site review information where provided |
| **JSON package** | Structured assessment, source metadata and review records |

Open the downloaded file and check its title, source identity, method revision
and outstanding work before sharing. Exporting does not publish to GitHub.
A completed checklist records operator attestations, not independent approval.
Keep private exports out of public issues and commits.

### Check downloaded report files locally

Run the package checker from the repository root. It can check a review ZIP
in place, including the manifest, the report and every bundled artifact:

```bash
python3 scripts/laif_check_workspace_export.py path/to/review.laif-review.zip
```

Use `--source path/to/original.pdf` with the ZIP to verify the original
document's SHA-256 separately. The same checker accepts a standalone JSON
package:

```bash
python3 scripts/laif_check_workspace_export.py path/to/export.laif.json
```

Supply `--source path/to/original.pdf` to hash the original source bytes,
`--report path/to/full.laif.md` to compare the downloaded report, and
`--artifacts-dir path/to/files` to check all downloaded **Files** artifacts
against their embedded copies. Keep the original filenames in the artifact
directory. These options can be combined. On Windows, `py -3 -X utf8` can
replace `python3`.

For an extracted ZIP, select `assessment.laif.json` and `report.laif.md`.
For automated bundles, point `--artifacts-dir` at the extracted `files`
folder. The checker compares the exported files with their embedded copies.

The checker reports which files it inspected and returns a failure status for
any supplied file that differs. For a retained report with no embedded Markdown,
it checks the report header identifiers and reports `HEADER_MATCH_ONLY`.
For an automated export it also looks for the exact embedded assessment
body after newline normalization. Package checks establish internal
consistency and file matches. Establish source authority and assess the
reasoning separately.

## Review a case with several records

In **Source index**, select **Map supplied documents and links** to open
**Case links**. Add the records you have, assign roles such as policy, contract
or test, and say which other records were unavailable. For instance, link the
policy’s testing requirement to the test record it calls for. If nobody
supplied that record, mark it as **Not supplied** so the map preserves the
open question.

Select **Check case map** to confirm the identity of supplied files and any
exact quotations you entered. Read **Links to follow up** and the checked
report before sharing it. **Download case bundle** collects the checked files
in one ZIP. Select **Include original source files for local replay** when
you need the source bytes in that ZIP. Editing a checked case asks for a new
check. The same checks are available when you work with local files.
See the [case map guide](product/CASE_LINKS.md).

## Save, resume and recover

Watch the save indicator. Signed-in changes are saved as user-scoped cloud
records, including source bytes and review outputs. **Saved workspace** or
**All changes saved** differs from **Session only** or **Save failed**.
Processing in the browser does not mean the document never leaves your computer.

On Home, **Continue review** opens the most recent automated assessment.
Use the **Review queue** in **Assessments** to see what each record needs next.
Search by title, method revision or run ID, and filter by review status to find
source issues, extracted text to check, candidate decisions or report checklists.
The main action in each row opens that review step for the selected assessment.
Returning to the queue in the same tab keeps your search and filter. Open
evidence requests remain visible after you record the report checklist.

Choose **Evidence requested** under **Review status** to find assessments
with active requests. **Open evidence requests** lists the reviewer notes
and links each request to its exact candidate. The same shortcut is under
**Next review step** in **Reports & export**. The review brief lists current
requests near the top so they can travel with the exported assessment.

New editions preserve earlier sources and assessments. Check changed text
before applying earlier review decisions. Canberra timestamps and short run IDs
help distinguish repeated reviews of the same document. The same assessment
stays selected as you move through its source, findings and evidence.

If another tab saves first, choose **Recover changes**. The Workspace can
combine edits to different records. If both copies changed the same record,
keep this tab open and use **Open saved workspace** to compare the two copies.
You can also export this tab's draft as a backup.

If a save fails and **Retry save** is available, try it before closing the
tab. Keep the tab open until the save is confirmed or you have checked your
backup download. Use **Status & verification** for workspace backups. An
import adds new records and reports any differing versions that need your
review. Browser and local Python records have separate storage.

## Help and next steps

**How it works** offers the guided example, work-area suggestions and method
explanation. **Search workspace** finds documents, assessments and pages.
The full navigation menu includes evidence, comparison and verification.

[Current release and acceptance limits](verification/CURRENT.md) ·
[Method](product/METHOD.md) · [Local setup](LOCAL_SETUP.md) ·
[Documentation map](README.md)

## Guided local start

The Python commands previously on this page now live in the
[separate local setup guide](LOCAL_SETUP.md#guided-local-start).
This section preserves older links; those commands are not needed for Site use.
