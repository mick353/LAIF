# Map a supplied multi-document governance case

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
local-only concerns. This command does not itself add a Site case-map screen
or synchronise local files with the Site.
