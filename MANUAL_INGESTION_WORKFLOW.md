# Manual Authoritative Ingestion Workflow

**Framework:** LAIF v1.2  
**Purpose:** Lawful authoritative-source acquisition when automated URL retrieval is blocked  
**Scope:** Provenance architecture only — no scoring, detector, interpretation, or assessment-semantic changes

---

## 1. Governing Rule

Manual acquisition is a lawful fallback when automated retrieval from an authoritative URL is blocked or unavailable. The acquisition channel does **not** itself prove authority. Authority is established only through the combined provenance record:

- documented `authoritative_origin_url`
- `acquisition_channel`
- `acquired_by`
- `acquired_at_utc`
- `acquisition_note`
- `source_file_sha256`
- `transformation_chain`
- local raw-file `sha256_hash`
- `citation_status`
- `provenance_classification`
- `verification_status`

No assessment logic changes when a source is manually acquired. The existing LAIF assessment engine and interpretation model are applied unchanged after ingestion and validation.

---

## 2. Manual Mode A — GitHub Direct Deposit

Use this mode when a human maintainer downloads the authoritative source outside the automated session and deposits it into the repository through GitHub or a Git commit.

1. Human downloads the authoritative file from the official source URL.
2. Human uploads or commits the exact downloaded file to:
   `docs/verified/manual_ingest/`
3. Pipeline computes SHA256 for the deposited source file:
   `sha256sum docs/verified/manual_ingest/<filename>`
4. Manifest is created or updated with:
   - `acquisition_channel: HUMAN_GITHUB_DEPOSIT`
   - `authoritative_origin_url`
   - `acquired_by`
   - `acquired_at_utc`
   - `acquisition_note`
   - `source_file_sha256`
   - `transformation_chain`
   - `verification_status`
5. Transformation/extraction is performed without paraphrasing, summarisation, semantic rewriting, or reconstructed text.
6. Extracted raw text is written to `docs/verified/raw/` and its SHA256 is recorded as `sha256_hash`.
7. Evidence trace is generated in `docs/verified/extracted/`.
8. Validation is executed:
   - `python3 validate.py`
   - `python3 validate.py --verified-corpus`
   - `python3 validate.py --check-evidence-traces`
9. Assessment is performed unchanged only after the source is accepted as citable under the manifest taxonomy.

---

## 3. Manual Mode B — Session Upload

Use this mode when a human supplies the authoritative source file through the active session/document-upload mechanism.

1. Human uploads the authoritative source file to the active session.
2. Agent writes the exact supplied file into:
   `docs/verified/manual_ingest/`
3. Pipeline computes SHA256 for the exact supplied file:
   `sha256sum docs/verified/manual_ingest/<filename>`
4. Manifest is created or updated with:
   - `acquisition_channel: HUMAN_SESSION_UPLOAD`
   - `authoritative_origin_url`
   - `acquired_by`
   - `acquired_at_utc`
   - `acquisition_note`
   - `source_file_sha256`
   - `transformation_chain`
   - `verification_status`
5. Transformation/extraction is performed without paraphrasing, summarisation, semantic rewriting, or reconstructed text.
6. Extracted raw text is written to `docs/verified/raw/` and its SHA256 is recorded as `sha256_hash`.
7. Evidence trace is generated in `docs/verified/extracted/`.
8. Validation is executed:
   - `python3 validate.py`
   - `python3 validate.py --verified-corpus`
   - `python3 validate.py --check-evidence-traces`
9. Assessment is performed unchanged only after the source is accepted as citable under the manifest taxonomy.

---

## 4. Explicit Prohibitions

The following are never permitted as authoritative-source substitutes:

- no LLM reconstruction of missing source text
- no paraphrased substitute source
- no “equivalent” regenerated document
- no assessment from memory
- no synthetic/sample/generated source substitution
- no treating screenshots as a full source unless explicitly marked `NON_CITABLE`
- no promotion of `NETWORK_BLOCKED_PENDING_HUMAN_SOURCE` to an assessed state without actual source acquisition

If a supplied source cannot be verified or human-attested, mark it `REJECTED_UNVERIFIED` and do not assess it as authoritative.

---

## 5. Verification Status Semantics

| Status | Operational meaning |
|---|---|
| `AUTOMATED_VERIFIED` | Automated retrieval from `authoritative_origin_url` succeeded and equivalence was verified. |
| `HUMAN_ATTESTED_AUTHORITATIVE` | Human operator supplied the file and asserted it came from the authoritative source. |
| `NETWORK_BLOCKED_PENDING_HUMAN_SOURCE` | Automated retrieval was blocked; this is not terminal and should route to manual acquisition. |
| `HASH_VERIFIED_LOCAL_ONLY` | Repository file integrity is verified, but upstream URL equivalence is not proven. |
| `REJECTED_UNVERIFIED` | Source is not accepted for authoritative assessment. |

---

## 6. Assessment Boundary

Manual ingestion is provenance and custody infrastructure only. It does not alter:

- scoring logic
- detector logic
- contradiction logic
- terminology enforcement
- coupling model
- interpretation-layer semantics
- existing assessment conclusions

*LAIF v1.2 · Manual Authoritative Ingestion Workflow · May 2026*
