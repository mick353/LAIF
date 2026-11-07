# DTA AI-in-Government Policy v2.1 — Admission Pending

**Checked:** 7 November 2026 (AEDT)  
**Status:** `PENDING_SOURCE_ACQUISITION` — publication verified, original file **not** held or hash-verified in this repository  
**Use:** Current-policy Australian Government analysis, separate from historical v2.0 assessment

- Publisher: Australian Government Digital Transformation Agency (DTA).
- Document: *Policy for the responsible use of AI in government*, version 2.1 (official PDF filename suffix `2_1_1`).
- Official landing page: https://www.digital.gov.au/ai/ai-in-government-policy
- Exact source URL advertised by DTA: https://www.digital.gov.au/sites/default/files/documents/2026-10/Policy%20for%20the%20responsible%20use%20of%20AI%20in%20government%202_1_1.pdf
- Status evidence: official site states v2.0 took effect 15 December 2025; minor v2.1 updates published 21 October 2026; page last updated 22 October 2026.
- Existing legacy evidence: `docs/verified/manual_ingest/Policy for the responsible use of AI in Government 2.0_0.pdf`; `reports/laif_assessment_aus_ai_policy_v2.md` is a **protected historical report**.

## Admission steps

1. Retrieve the exact PDF from DTA, or supply it through `HUMAN_GITHUB_DEPOSIT` / `HUMAN_SESSION_UPLOAD`. Do not synthesize source text from a web extract.
2. Preserve the new PDF under a version-specific filename in `docs/verified/manual_ingest/`; record acquisition URL, time, channel, operator and source SHA-256. Do not alter the v2.0 PDF.
3. Extract without semantic rewriting to a new version-specific `docs/verified/raw/` file; record tool, pages/boundaries and SHA-256. Check quotations directly against the official PDF.
4. Create a separate provenance manifest and evidence trace. Keep citation and assessment states pending until verified, with no inherited v2.0 validation status.
5. Run `python3 validate.py`, `python3 validate.py --verified-corpus`, `python3 validate.py --check-evidence-traces` and the local verification gate. Only then produce a **new dated report** with a v2.0→v2.1 delta and human review. Do not regenerate or edit the protected v2.0 report.

**Unfilled fields:** file SHA-256, acquisition timestamp/method, extracted-text hash, evidence trace, assessment results. No current-law finding is asserted by this record.
