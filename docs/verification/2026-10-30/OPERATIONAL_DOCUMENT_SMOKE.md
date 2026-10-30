# Local document-processing smoke — 30 October 2026

The current document processor was run against three real, already preserved source files on Windows. Optional `python-docx` 1.2.0 and `pypdf` 6.21.4 were installed in an isolated temporary virtual environment. Generated reports and analyst bundles stayed under the system temporary directory; no generated assessment was published or committed.

| Input | Mode and extractor | Source SHA-256 | Extracted characters | Result |
|---|---|---|---:|---|
| `docs/verified/manual_ingest/DTAC_Form_2.0_February_2026.docx` | `external_framework`, `python-docx` | `fc8b64305d5b536ad1f9cafd7fd602ce9703adffaeceb5d9bdff46d25224ad60` | 42,654 | Exit 0; zero extraction warnings/errors; JSON, Markdown, institutional report, technical appendix, analyst bundle and index written |
| `docs/verified/manual_ingest/NIST.AI.100-1.pdf` | `external_framework`, `pypdf` | `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1` | 106,492 | Exit 0; zero extraction warnings/errors; same output classes written |
| `docs/verified/manual_ingest/OJ_L_202401689_EN_TXT.pdf` | `external_framework`, `pypdf` | `bba630444b3278e881066774002a1d7824308934f49ccfa203e65be43692f55e` | 599,774 | Exit 0; zero extraction warnings/errors; same output classes written |

The EU command first used an unsupported `--assessment-mode` option and returned exit 2 without processing. It was corrected to the documented `--mode external_framework`; the recorded successful run is the corrected invocation. The provisional EU output is not the reviewed full-document assessment required by the verified-corpus manifest.

## Additional NIST source check

The official [NIST AI RMF publication page](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) links the [NIST PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf). A direct download on 30 October 2026 returned HTTP 200 and 1,946,127 bytes. Its SHA-256 `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1` exactly matches the preserved PDF. The assessed raw Markdown was historically extracted from a separate DOCX. A token comparison with the official PDF showed broad overlap, with ordering and figure/table differences; it is insufficient to certify that every DOCX clause and table matches the PDF. The existing manifest's `HASH_VERIFIED_LOCAL_ONLY` status for that assessed text therefore remains unchanged.

The official NHS DTAC DOCX endpoint returned HTTP 403 in this session, so no upstream byte comparison was made for DTAC.

These are local smoke and source-custody receipts. They show that the current program can process these file formats and produce its outputs. They do not establish extraction fidelity for every clause, LAIF assessment validity, legal certification, or operational performance across representative deployments. No GitHub Actions run was used.
