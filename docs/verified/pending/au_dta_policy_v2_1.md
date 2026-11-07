# DTA AI-in-Government Policy v2.1 — Source Deposited; Verification Pending

**Completion update (7 November 2026):** The following deposit checklist is retained as history. PDF SHA-256, full extraction, provenance manifest, exact page-bounded evidence traces and separate source-scoped assessment are completed on PR #98. See the [execution record](../../verification/2026-11-07/regulatory/README.md). Human legal/policy review and merge remain outstanding. DTA is HUMAN_ATTESTED_AUTHORITATIVE; upstream retrieval returned HTTP 503 twice, so byte equivalence is not claimed.

**As at:** 7 November 2026 (AEDT)  
**Status:** `SOURCE_DEPOSITED_PENDING_VERIFICATION` — original PDF present in the PR #98 branch, not yet admitted as `PRIMARY_CITABLE` in LAIF's verified corpus.  
**Scope:** Current Australian Government policy, separate from protected historical v2.0 assessment.

- Publisher: Australian Government Digital Transformation Agency.
- Publication: *Policy for the responsible use of AI in government*, version 2.1, 26 pages.
- Policy text states v2.0 effective 15 December 2025; v2.1 minor updates published 21 October 2026 (page 6).
- Official source: https://www.digital.gov.au/sites/default/files/documents/2026-10/Policy%20for%20the%20responsible%20use%20of%20AI%20in%20government%202_1_1.pdf
- Acquisition channel: `HUMAN_GITHUB_DEPOSIT`, uploaded by repository owner to PR #98 on 7 November 2026.
- Repository PDF: [Policy for the responsible use of AI in government 2_1_1.pdf](../manual_ingest/Policy%20for%20the%20responsible%20use%20of%20AI%20in%20government%202_1_1.pdf)
- Git blob SHA-1: `6ef6a984c71e48d2ec3a39be9194c5f2ba85e1e4`. **Not** a PDF SHA-256 or upstream-byte equivalence assertion.
- Historical v2.0: `docs/verified/manual_ingest/Policy for the responsible use of AI in Government 2.0_0.pdf`; protected `reports/laif_assessment_aus_ai_policy_v2.md`.

## Substantive source checkpoints (pending formal evidence traces)

- Page 6: mandatory scope for non-corporate Commonwealth entities and national-security carveouts.
- Pages 10–11: public transparency statements, accountable officials and use-case owners, internal register.
- Pages 12–13: incident reporting and response, mandatory staff training.
- Pages 14–16: in-scope use-case assessment, pre-deployment impact assessment, high-risk oversight and annual review.
- Pages 21–22: in-scope criteria, exceptions for certain early experimentation.

These are **document observations**, not findings that any agency complies or fails.

## Required next steps

1. Retrieve the exact committed PDF bytes in a local LAIF checkout; record file SHA-256, size, extraction tool/version and exact source origin comparison. The repository blob SHA-1 above establishes Git object identity only.
2. Follow `MANUAL_INGESTION_WORKFLOW.md`: version-specific `docs/verified/manual_ingest/` custody, deterministic text extraction to `docs/verified/raw/`, extraction hash, page boundaries and direct quotation checks.
3. Create a separate provenance manifest and source-specific evidence trace; do not inherit v2.0 verification.
4. Run `python3 validate.py`, `python3 validate.py --verified-corpus`, `python3 validate.py --check-evidence-traces`, and the full local LAIF verification gate.
5. Produce a new dated v2.1 assessment and v2.0→v2.1 delta with reviewer sign-off; leave the protected historical report unchanged.

**Not yet completed:** SHA-256, full-text ingestion, provenance manifest, quote traces, full local verification, new assessment and human policy review.
