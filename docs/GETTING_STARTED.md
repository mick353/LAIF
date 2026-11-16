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
document. The review path shows your location, not completion or certification.

## 4. Review and export

Choose **4. Export** or **Reports & export** and confirm the selected assessment.
Read the report, record only quality checks you have actually performed, and
add your reviewer name, role, notes and unresolved questions.

| Export | Contents |
|---|---|
| **Review brief** (new automated runs) | Concise provisional findings, candidate decisions and remaining review work |
| **Full report** | Full pipeline report with labelled Site review information where provided |
| **JSON package** | Structured assessment, source metadata and review records |

Open the downloaded file and check its title, source identity, method revision
and outstanding work before sharing. Exporting does not publish to GitHub.
A completed checklist records operator attestations, not independent approval.
Keep private exports out of public issues and commits.

## Save, resume and recover

Watch the save indicator. Signed-in changes are saved as user-scoped cloud
records, including source bytes and review outputs. **Saved workspace** or
**All changes saved** differs from **Session only** or **Save failed**.
Processing in the browser does not mean the document never leaves your computer.

On Home, **Continue review** opens the most recent automated assessment.
Use **Assessments** for older runs. New editions preserve earlier sources and
runs; check changed text before applying previous review decisions.

If saving is unavailable, keep the tab open and choose **Export backup**.
A report download is not a complete workspace backup. Backup import/export
controls are under **Status & verification**; check restored sources and runs
before continuing. Browser and local Python records do not automatically synchronise.

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
