# Website source catalogue and contribution bridge

`source-index.json` is the public discovery index for the LAIF Research Workspace. It includes sixteen retained source/framework documents and source-based explanations supported by 39 exact quotations. Source hashes and raw text offsets are checked locally. The descriptions explain what each document contains; they do not establish its current legal applicability, upstream origin or the effectiveness of its controls.

The Site reads this index from a specific commit on public GitHub `main`, retrieves each named source and verifies SHA-256 before displaying it. It keeps the bundled catalogue if GitHub cannot be reached. A new source edition is retained separately; existing private workspace records and historical assessments are not overwritten. Catalogue refresh does not upgrade the pinned assessment engine.

## A new source, from the website to the repository

1. Add a PDF, Markdown or UTF-8 text document to the private workspace. Its bytes and hash are retained. Text receives an automatically selected overview; PDF text is available after extraction through the existing assessment pipeline.
2. Inspect the document and any generated results. To propose public inclusion, use **Prepare GitHub contribution**, review the publication contents and acknowledge the public destination. The downloaded package includes the source, metadata and selected associated proposed assessment records. Do not include confidential data, restricted source material or private reviewer details.
3. A maintainer receives that explicitly authorised package through GitHub or an authorised coding session. The Site's direct visitor-to-GitHub write integration is unavailable in the current platform connection. Opening a request or exporting a package does not itself create a repository commit or pull request.
4. Import it on a new branch with:

   ```sh
   python3 scripts/laif_site_catalog.py import /path/to/contribution.json --acknowledge-publication
   python3 scripts/laif_site_catalog.py verify
   python3 scripts/laif_verify.py --full --base-ref origin/main
   ```

5. Review source rights, metadata, declared scope and provenance before merge. Import preserves exact bytes and stores proposed analyses in `proposal.json`. It adds a **source proposal**, with `HASH_VERIFIED_LOCAL_ONLY` and `NOT_ESTABLISHED` citation status, to this discovery index. It does not admit an official/verified corpus source or promote a proposed assessment into a canonical report.
6. After the reviewed change reaches `main`, the Site's **Refresh from GitHub** reads and verifies the new index. It can then display the contributed source with its actual proposed/unverified status. Official-source admission and substantive assessment publication continue to use the governed LAIF workflows.

The script rejects missing public-publication consent, changed source bytes, unsafe paths, ambiguous encodings, duplicate/non-finite JSON and assessments tied to other source bytes. Duplicate source imports are idempotent. Source size is limited to 8 MB; contribution packages to 16 MB.

## Verify the existing catalogue

```sh
python3 scripts/laif_site_catalog.py verify
python3 -m unittest discover -s tests -p test_site_catalog.py
```

No GitHub Actions, model API or new subscription is required. A passing catalogue check proves local byte/quote identity and package constraints; it does not prove source authority, legal compliance or independent empirical validity.
