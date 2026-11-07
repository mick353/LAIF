# Source-scoped preliminary review — DTA v2.1 and EU 2026/1744

**As-at:** 7 November 2026 (AEDT)  
**Branch:** `docs/authoritative-source-currency-20261107` (draft PR #98)  
**Method:** Direct reading of the two owner-deposited PDFs and page-specific source excerpts, plus GitHub repository/source-custody inspection. This is a **pre-ingestion research note**, not a LAIF engine output, independent legal opinion, full-document comparison or certified source admission.

## Source custody and verification state

| Source | Repository PDF | Git blob SHA-1 | Status |
|---|---|---|---|
| DTA *Policy for the responsible use of AI in government*, v2.1 (26 pp.) | [PDF](../manual_ingest/Policy%20for%20the%20responsible%20use%20of%20AI%20in%20government%202_1_1.pdf) | `6ef6a984c71e48d2ec3a39be9194c5f2ba85e1e4` | `SOURCE_DEPOSITED_PENDING_VERIFICATION` |
| Regulation (EU) 2026/1744 (41 pp.) | [PDF](../manual_ingest/OJ_L_202601744_EN_TXT.pdf) | `90143567e4272f0684cfeaca5af66836c6b0b11e` | `SOURCE_DEPOSITED_PENDING_VERIFICATION` |

Git blob SHA-1 identifies a repository object; it is **not** the required original-file SHA-256 or evidence of upstream byte equivalence. No verified raw-text extraction, source-specific manifest, trace or fresh assessment has yet been generated.

## A. Australian Government policy v2.1: directly observed requirements

- **Applicability:** page 6 says non-corporate Commonwealth entities must apply the policy, corporate Commonwealth entities are encouraged, and defence/NIC uses are carved out. The policy states v2.0 took effect 15 December 2025 and v2.1 minor updates were published 21 October 2026.
- **Agency accountability:** pages 10–11 require public AI transparency statements, a strategic position, accountable officials, accountable use-case owners and a register of in-scope use cases. Some requirements have staged implementation deadlines.
- **Incident management and capability:** pages 12–13 require channels for staff and public AI safety concerns, incident-response processes and mandatory staff training.
- **Use-case risk:** pages 14–16 require documented in-scope screening, impact assessments for in-scope cases, treatment before deployment, ongoing monitoring, and enhanced governance and annual review for inherent high-risk use cases.
- **Scope nuance:** pages 21–22 list risk/impact criteria and an early-stage experimentation exception with conditions. These must be applied before inferring obligations for a particular use case.

**Research questions, not findings of noncompliance:** How do accountable-owner registers connect to incident records and actual intervention authority? What evidence shows the prescribed impact assessment is applied before deployment? What is the precise v2.0-to-v2.1 delta? Those questions require agency-specific records and the complete historical v2.0 comparison.

## B. EU amending regulation: directly observed changes

- **Instrument identity:** page 1 identifies Regulation (EU) 2026/1744 of 8 July 2026, published 24 July 2026, amending Regulation (EU) 2024/1689 and two other EU regulations.
- **AI literacy:** page 16 replaces Article 4 with a duty for providers/deployers to take measures supporting AI literacy; it explicitly does not require guaranteeing an individual's specified literacy level.
- **Bias and sensitive data:** page 17 inserts Article 4a, allowing exceptional processing for bias detection/correction under specified necessity, safeguards and actor-specific conditions. The amendment does not itself create a universal duty to undertake such processing.
- **Prohibited practices:** page 18 adds Article 5 provisions on specified non-consensual intimate material and child sexual abuse material, with carefully framed provider/deployer conditions and exceptions. Do not describe these as an unqualified prohibition of all image-generation capabilities.
- **Technical and governance rules:** pages 19–20 modify Article 10 and related documentation, provider and fundamental-rights provisions. Pages 26–33 revise AI Office supervisory and enforcement powers.
- **Staggered commencement:** page 35 amends Article 113 to provide 2 December 2027 for specified Annex III high-risk provisions and 2 August 2028 for specified Annex I high-risk provisions; it also specifies other exceptions and dates. The general application schedule and transitional provisions must not be collapsed into one date.
- **Agentic AI:** page 38 includes `AIH 0401` in Annex XIV's technology-specific codes, including agentic AI. This is a notified-body designation code, **not** a general declaration that every agentic system is legally high-risk.

**Research questions, not findings of noncompliance:** Which amendments apply to a given provider, deployer or product category as of a specified date? Which sections of the original 2024 Act remain unchanged? How does the amended Act interact with sector legislation and implementing acts? Answer only from the original and amendment together, with legal review.

## C. Explicit scholarly limits

1. The observations above are page-scoped and **not generated by the LAIF scoring or scholarly-report engine**.
2. Neither the Australian policy nor the EU amendment proves that any institution has implemented its written controls.
3. A requirement absent from a quoted passage is not necessarily absent from the full instrument, associated standards or the governing legal system.
4. The 2026 EU amendment is not a full consolidated Act; the original 2024 instrument is a separate dependency (draft PR #90).
5. No detector accuracy, legal compliance score, real-world AI safety performance, or framework superiority is claimed.

## D. Required completion sequence

1. In a local checkout of PR #98, calculate SHA-256 for the two committed PDF files and verify exact source identity against official DTA/EUR-Lex originals.
2. Move or copy exact originals into versioned `docs/verified/manual_ingest/` custody without deleting the deposited files or historical versions; record acquisition channel and operator.
3. Use the repository-supported PDF extractor, record its version, extract each page without semantic rewriting, and record raw-text SHA-256 and extraction limits. Review tables, footnotes and page boundaries.
4. Generate source-specific manifests and evidence traces; validate exact quotations and mark any extraction uncertainty.
5. Run `python3 validate.py`, `python3 validate.py --verified-corpus`, `python3 validate.py --check-evidence-traces`, then `python3 scripts/laif_verify.py --full --base-ref origin/main`. Record actual results.
6. Prepare separate research-neutral assessments: DTA v2.1 with a protected-v2.0 delta, and the EU amendment with the original Act and an actor/date applicability matrix. Request human legal/semantic review before changing canonical conclusions.

**Stop condition:** Until steps 1–5 pass, these files remain deposited sources, not LAIF-verified, `PRIMARY_CITABLE` assessment inputs.
