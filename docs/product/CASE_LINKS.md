# Map a supplied multi-document governance case

In the private [Research Workspace](https://laif-research-workspace.mick353.chatgpt.site),
open **Source index** and select **Map supplied documents and links**. Choose
retained documents, assign roles, record any unsupplied records and describe
the links you want to review. Select **Check case map**. Review **Links to follow up** and read or
select the text of the checked report, JSON or CLI manifest before downloading.
After editing a case, check it again. Saved case maps reopen with their declared
sources and links. Private Site records are saved in cloud storage.

### Download and replay a checked case

Select **Download case bundle** for the readable map, checked JSON, CLI
manifest and file inventory. Extract the ZIP and open `START-HERE.txt`.
If you need to replay the case, choose **Include original source files for
local replay** before downloading. The Workspace compares each original to
its pinned SHA-256 before including it. The choice clears after download,
when you switch cases, or when you recheck an edited case. Review quotations,
notes and any included originals before sharing.

The original files in a replay bundle sit beside the CLI manifest. When you
use the standard bundle, get the supplied sources under **Download individual
files** and place them beside the manifest without renaming them. Run the
existing `laif_case_links.py` command on the extracted CLI manifest. The Site
and local command use the same Python checks and report format.

### Recover edits from two tabs

If the Workspace reports a newer save, keep the tab with your draft open and
choose **Recover changes**. The Workspace can combine edits to different
records. When competing edits affect only a case's question or analyst name,
the comparison shows the saved value and your draft. Choose what to keep for
each field and select **Save chosen values**. If another save arrives during
the comparison, run **Recover changes** again and review the new values.

If a conflict also involves sources, links or assessment records, keep the
draft open. Use **Open saved workspace** to compare manually or **Export
backup** to keep a copy before you proceed.

To compare two records that appear to disagree, include each version and quote
both passages in a declared link. In the note, explain what differs and which
dates or conditions you still need to check. The report keeps both passages
with their original source identities for your review.

See the [current verification record](../verification/CURRENT.md) for the
hosted download and local replay results.

Use the optional local `laif_case_links.py` command when you have several
records for one governance question. It connects **only the files and links
you declare**. It does not search for missing records, infer contradictions,
decide which instrument controls another, or assess legal or operational
effectiveness.

## Try the synthetic case

From the repository root:

```bash
python3 -S scripts/laif_case_links.py docs/examples/synthetic-case-links.json
python3 -S scripts/laif_case_links.py docs/examples/synthetic-case-links.json --report laif_outputs/case-links/synthetic-map.md
```

The example pins the included supplier policy and expressly marks the contract,
procedure, test, incident and remedy records **not supplied**. Its one link
checks an exact policy sentence; the report does not claim that a test or
contract exists. The `--report` destination must be new and is never replaced.
Use `--json` to print the checked structured map. On Windows, use
`py -3 -X utf8` in place of `python3`.

## Prepare your own private case

Copy the example manifest outside the public repository. Replace its sample
file and SHA-256 with the **exact bytes** of each authorised source. Record
an ID, one of the roles `policy`, `contract`, `procedure`, `test`, `incident`,
`remedy`, a declared version and origin, and `status: SUPPLIED`. Paths are
relative to the manifest directory by default; `--evidence-root` selects a
different root. The tool refuses missing, changed or escaping source paths.
You can calculate a file hash with `Get-FileHash -Algorithm SHA256` in
PowerShell or `sha256sum` on Unix.

For a role without a supplied record, use `status: NOT_SUPPLIED` and a reason,
with no file or hash. A role omitted entirely appears as `NOT_DECLARED`.
Neither state proves the record does not exist elsewhere. Do not mix a
`SUPPLIED` and `NOT_SUPPLIED` entry for the same role.

Each optional link names two declared source IDs, a relationship **you**
assert, and a note. Add `from_quote` and `to_quote` where you can quote exact
UTF-8 text from both supplied files. The command verifies those strings in
the pinned bytes. A PDF or other binary file may be hash-pinned, but for
quote matching you must supply a separately identified and verified UTF-8
text derivative. `EXACT_TEXT_AT_BOTH_ENDPOINTS` means only that both cited
strings occur; it does **not** validate the relationship. An endpoint marked
`NOT_SUPPLIED` remains unresolved.

Keep private contracts, incidents and review notes outside public GitHub.
The report identifies local bytes and self-reported versions, origins and
analyst. It does not authenticate people, source authority, legal effect,
actual tests or remedies. Use the separate [assurance evidence workflow](../governance/ASSURANCE_CALIBRATION.md)
for control and receipt checks, and the [substantive review](../governance/SUBSTANTIVE_REVIEW.md)
for attributed LAIF criterion reasoning.

The validator and renderer are also available as pure Python functions:
`assess_bytes(manifest, manifest_bytes, sources_by_id)` and `render(outcome)`.
`sources_by_id` maps each declared `SUPPLIED` source ID to its **original bytes**;
the manifest object must parse exactly from `manifest_bytes`. These functions
allow another runtime to use the same checks without reading local paths.
The CLI's `--evidence-root` confinement and exclusive report creation remain
local-only concerns. Running this command does not synchronise local files
with the Site. Transfer requires explicit authorised intake and matching the
source identities; do not assume that a local path identifies a hosted file.
