# Markdown documentation audit — 16 November 2026

Owner: Codex, documentation delivery. Repository baseline `ab13d95`.

## Scope and results

- Scanned all **189 tracked repository Markdown files** for link targets, audience/routing, Python references and dated/current-status language. Product entry points and their destinations received a content review. Generated reports and retained sources were inventoried and link-scanned, not independently reassessed.
- Also inventoried all **12 tracked Site Markdown files** at source `2e863ff7ef43ddfb384f5461016a928b612bef00`; vendor notices, source copies, fixtures and dated verification records retain their original roles.
- Initial scan: 652 inline Markdown/HTML link references; no missing local path targets. Reference syntax inside code/examples is not proof of a rendered navigation link.
- GitHub checks: all 14 distinct API entities resolved (repository, profile, one commit, nine pull requests, two issues). The clone URL and new-issue route belong to that verified repository. Checks verify destination identity, not the truth of historical claims.
- Separated browser getting-started instructions from local Python setup. Updated technical incoming links, product overview, quality guide, contributor bridge, README navigation and agent routing. Preserved the old guided-start anchor as a forwarding section.
- Current Site guide links must follow `main`; engine/source evidence stays revision-pinned. Site release follows the documentation merge.
- No legal currency, independent construct validity or third-party source availability review was performed. No historical evidence was deleted, moved or regenerated.

## Historical anchor findings

Site link checks also resolved PR #107, both pinned `08dd61a` documentation
paths, and the noble-hashes, pypdf and Pyodide licence/tag destinations. All
local links in the 12 Site Markdown files resolve. New `main` guide targets
are validated in the candidate tree and must be merged before Site publication.
The final repository path scan checked 597 local link references with none missing.

The initial scan flagged 14 fragment links in generated assessment records. Their targets normalise punctuation/spacing differently from the displayed heading slugs. These remain recorded defects in historical output, not current setup-guide links. Preserve the reports; a dedicated renderer/reproduction change should correct future output and explicitly decide whether to regenerate historical copies. Use heading search to navigate the affected records in the meantime.

| File | Fragment |
|---|---|
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.laif.md` | `#peer-exemplars-what-good-looks-like-in-this-corpus` |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/OJ_L_202601744_EN_TXT.laif.md` | `#peer-exemplars-what-good-looks-like-in-this-corpus` |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md` | `#peer-exemplars-what-good-looks-like-in-this-corpus` |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md` | `#peer-exemplars-what-good-looks-like-in-this-corpus` |
| `reports/laif_real_world_assessment.md` | `#peer-exemplars-what-good-looks-like-in-this-corpus` |
| `reports/laif_real_world_assessment.md` | `#document-1-us-executive-order-14110-2-principles-6-workers-7-civil-rights-official-text` |
| `reports/laif_real_world_assessment.md` | `#document-2-oecd-recommendation-on-ai-oecdlegal0449-sections-1-2-official-text` |
| `reports/laif_real_world_assessment.md` | `#document-3-nist-ai-rmf-10-nist-ai-100-1-govern-map-functions-official-text` |
| `reports/laif_real_world_assessment.md` | `#document-4-nhs-england-dtac-v20-february-2026-introduction-c1-clinical-safety-official-text` |
| `reports/laif_real_world_assessment.md` | `#document-5-eu-ai-act-art-9-13-14` |
| `reports/laif_real_world_assessment.md` | `#document-6-nist-ai-rmf-govern-map-functions` |
| `reports/laif_real_world_assessment.md` | `#document-8-us-executive-order-14110-4-safety-7-workers` |
| `reports/laif_real_world_assessment.md` | `#document-9-nhs-england-ai-in-clinical-decision-support-policy-framework` |
| `reports/laif_real_world_assessment.md` | `#document-10-tuccipd-framework-for-fair-ai-in-employment-decisions` |

## Baseline Markdown inventory

Every tracked Markdown file is listed below. Classification describes intended use, not factual validation.

| File | Lines | Review lane |
|---|---:|---|
| `AGENTS.md` | 62 | guide/reference |
| `CLAUDE.md` | 449 | guide/reference |
| `CONTRIBUTING.md` | 115 | guide/reference |
| `MANUAL_INGESTION_WORKFLOW.md` | 155 | guide/reference |
| `PUBLICATION_STATUS.md` | 179 | guide/reference |
| `README.md` | 210 | guide/reference |
| `REPRODUCIBILITY.md` | 241 | guide/reference |
| `THIRD_PARTY_NOTICES.md` | 30 | guide/reference |
| `corpus_manifest.md` | 143 | guide/reference |
| `docs/GETTING_STARTED.md` | 241 | guide/reference |
| `docs/examples/README.md` | 58 | guide/reference |
| `docs/examples/sample-assessment.md` | 335 | generated example/evidence |
| `docs/examples/sample-quote-bank.md` | 99 | generated example/evidence |
| `docs/examples/sample-scholarly-report.md` | 205 | generated example/evidence |
| `docs/examples/vendor-policy.md` | 11 | synthetic fixture |
| `docs/governance/AI_ANALYST_BUNDLE.md` | 28 | guide/reference |
| `docs/governance/ASSESSMENT_FRAGILITY.md` | 121 | guide/reference |
| `docs/governance/ASSURANCE_CALIBRATION.md` | 138 | guide/reference |
| `docs/governance/AUTOMATIC_CRITERIA.md` | 72 | guide/reference |
| `docs/governance/CALIBRATION_SCORE_JUSTIFICATION.md` | 95 | guide/reference |
| `docs/governance/DOCUMENT_PROCESSING_RUNNER.md` | 187 | guide/reference |
| `docs/governance/EVIDENCE_CHECKS.md` | 74 | guide/reference |
| `docs/governance/EVIDENCE_TRACE_MODEL.md` | 101 | guide/reference |
| `docs/governance/FRONTIER_SAFETY_ASSURANCE.md` | 230 | guide/reference |
| `docs/governance/GITHUB_ACTIONS_DOCUMENT_PROCESSING.md` | 132 | guide/reference |
| `docs/governance/GOVERNANCE_FORCE_MODEL.md` | 79 | guide/reference |
| `docs/governance/GOVERNANCE_REPAIR_REPORTING.md` | 46 | guide/reference |
| `docs/governance/INSTITUTIONAL_ANALYST_REPORTING.md` | 45 | guide/reference |
| `docs/governance/MERGE_POLICY.md` | 97 | guide/reference |
| `docs/governance/PROTECTED_ARTIFACTS.md` | 92 | guide/reference |
| `docs/governance/PUBLIC_REPORT_TEMPLATE.md` | 87 | guide/reference |
| `docs/governance/REMEDIATION_PATCH_SCHEMA.md` | 100 | guide/reference |
| `docs/governance/RESULT_TAXONOMY.md` | 93 | guide/reference |
| `docs/governance/ROLLBACK_RECOVERY.md` | 95 | guide/reference |
| `docs/governance/SCORE_INTERPRETATION.md` | 605 | guide/reference |
| `docs/governance/SECTOR_PROFILES.md` | 145 | guide/reference |
| `docs/governance/SEMANTIC_BOUNDARIES.md` | 160 | guide/reference |
| `docs/governance/SUBSTANTIVE_REVIEW.md` | 98 | guide/reference |
| `docs/governance/SYSTEM_QA_RELEASE_AUDIT.md` | 145 | guide/reference |
| `docs/product/METHOD.md` | 52 | guide/reference |
| `docs/product/OVERVIEW.md` | 90 | guide/reference |
| `docs/product/PRODUCT_READINESS_2026-11.md` | 116 | guide/reference |
| `docs/product/QUALITY.md` | 70 | guide/reference |
| `docs/product/REFERENCE.md` | 130 | guide/reference |
| `docs/product/USE_CASES.md` | 71 | guide/reference |
| `docs/regulatory/CURRENT_AUTHORITY_CROSSWALK_2026-11.md` | 158 | guide/reference |
| `docs/research/LEGACY_RESULT_BOUNDARIES.md` | 51 | guide/reference |
| `docs/research/SCHOLARLY_REPORTING.md` | 301 | guide/reference |
| `docs/research/SCHOLARLY_REPORT_TEMPLATE.md` | 112 | guide/reference |
| `docs/review/2026-11-07-external-scholarly-critique-triage.md` | 200 | guide/reference |
| `docs/review/INDEPENDENT_STUDY_OPERATIONS.md` | 123 | guide/reference |
| `docs/review/USABILITY_REVIEW_2026-09.md` | 815 | guide/reference |
| `docs/site/README.md` | 32 | guide/reference |
| `docs/site/VERIFICATION.md` | 12 | guide/reference |
| `docs/supporting/51a29205-OECD_Legal_Instruments.md` | 731 | historical/evidence |
| `docs/supporting/55eccce3-DTAC_Form_2.0_February_2026.md` | 197 | historical/evidence |
| `docs/supporting/5f667a6f-NIST.AI.1001.md` | 388 | historical/evidence |
| `docs/supporting/b0ef43db-202324283.md` | 406 | historical/evidence |
| `docs/verification/2026-05-11/README.md` | 5 | historical/evidence |
| `docs/verification/2026-05-11/runs/run-1/assessment.md` | 379 | historical/evidence |
| `docs/verification/2026-05-11/runs/run-2/assessment.md` | 81 | historical/evidence |
| `docs/verification/2026-05-11/runs/run-3/assessment.md` | 81 | historical/evidence |
| `docs/verification/2026-05-11/runs/run-4/assessment.md` | 81 | historical/evidence |
| `docs/verification/2026-05-11/runs/run-5/assessment.md` | 81 | historical/evidence |
| `docs/verification/2026-05-11/runs/run-6/assessment.md` | 82 | historical/evidence |
| `docs/verification/2026-10-23/README.md` | 137 | historical/evidence |
| `docs/verification/2026-10-23/current-product-package.md` | 14 | historical/evidence |
| `docs/verification/2026-10-23/product-presentation.md` | 19 | historical/evidence |
| `docs/verification/2026-10-23/windows-example.md` | 35 | historical/evidence |
| `docs/verification/2026-10-30/CROSS_REFERENCE_QA.md` | 14 | historical/evidence |
| `docs/verification/2026-10-30/OPERATIONAL_DOCUMENT_SMOKE.md` | 19 | historical/evidence |
| `docs/verification/2026-10-30/PARKED_BRANCH_TRIAGE.md` | 19 | historical/evidence |
| `docs/verification/2026-10-30/WINDOWS_RELEASE_VERIFICATION.md` | 28 | historical/evidence |
| `docs/verification/2026-10-30/WORK_HANDOVER.md` | 48 | historical/evidence |
| `docs/verification/2026-11-06/FRONTIER_SAFETY_RELEASE_CHECK.md` | 77 | historical/evidence |
| `docs/verification/2026-11-07-assessment-repairs/COMBINED_VALIDATION.md` | 9 | historical/evidence |
| `docs/verification/2026-11-07-assessment-repairs/CONTINUED_VALIDATION.md` | 16 | historical/evidence |
| `docs/verification/2026-11-07-assessment-repairs/README.md` | 43 | historical/evidence |
| `docs/verification/2026-11-07-consolidated-candidate/README.md` | 56 | historical/evidence |
| `docs/verification/2026-11-07-consolidated-candidate/REASONING_REVIEW.md` | 40 | historical/evidence |
| `docs/verification/2026-11-07-consolidated-candidate/review-dossiers/dta/research_report.md` | 121 | historical/evidence |
| `docs/verification/2026-11-07-consolidated-candidate/review-dossiers/eu/research_report.md` | 130 | historical/evidence |
| `docs/verification/2026-11-07-control-evidence-reporting/README.md` | 108 | historical/evidence |
| `docs/verification/2026-11-07-control-evidence-reporting/actual-dta-policy-only.md` | 54 | historical/evidence |
| `docs/verification/2026-11-07-control-evidence-reporting/actual-release-records.md` | 65 | historical/evidence |
| `docs/verification/2026-11-07-control-evidence-reporting/notion-sync.md` | 9 | historical/evidence |
| `docs/verification/2026-11-07-generated-report-quality/README.md` | 53 | historical/evidence |
| `docs/verification/2026-11-07-generated-report-quality/au_dta_policy_v2_1/au_dta_policy_v2_1.institutional_report.md` | 253 | historical/evidence |
| `docs/verification/2026-11-07-generated-report-quality/au_dta_policy_v2_1/au_dta_policy_v2_1.technical_appendix.md` | 1034 | historical/evidence |
| `docs/verification/2026-11-07-generated-report-quality/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.institutional_report.md` | 238 | historical/evidence |
| `docs/verification/2026-11-07-generated-report-quality/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.technical_appendix.md` | 1037 | historical/evidence |
| `docs/verification/2026-11-07-portable-review/README.md` | 55 | historical/evidence |
| `docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.laif.md` | 263 | historical/evidence |
| `docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.md` | 11 | historical/evidence |
| `docs/verification/2026-11-07-portable-review/demonstration/vendor-policy.technical_appendix.md` | 800 | historical/evidence |
| `docs/verification/2026-11-07-readable-evidence/5f667a6f-NIST.AI.1001/assessment.md` | 734 | historical/evidence |
| `docs/verification/2026-11-07-readable-evidence/README.md` | 79 | historical/evidence |
| `docs/verification/2026-11-07-readable-evidence/au_dta_policy_v2_1/assessment.md` | 1372 | historical/evidence |
| `docs/verification/2026-11-07-readable-evidence/eu_ai_act_amendment_2026_1744/assessment.md` | 1642 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/51a29205-OECD_Legal_Instruments/51a29205-OECD_Legal_Instruments.laif.md` | 289 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/51a29205-OECD_Legal_Instruments/51a29205-OECD_Legal_Instruments.technical_appendix.md` | 1036 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/55eccce3-DTAC_Form_2.0_February_2026/55eccce3-DTAC_Form_2.0_February_2026.laif.md` | 287 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/55eccce3-DTAC_Form_2.0_February_2026/55eccce3-DTAC_Form_2.0_February_2026.technical_appendix.md` | 1034 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/5f667a6f-NIST.AI.1001/5f667a6f-NIST.AI.1001.laif.md` | 270 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/5f667a6f-NIST.AI.1001/5f667a6f-NIST.AI.1001.technical_appendix.md` | 1085 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/README.md` | 135 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md` | 343 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/au_dta_policy_v2_1/au_dta_policy_v2_1.technical_appendix.md` | 1034 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/b0ef43db-202324283/b0ef43db-202324283.laif.md` | 263 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/b0ef43db-202324283/b0ef43db-202324283.technical_appendix.md` | 1035 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/eu-ai-act-2024-1689/eu_ai_act_2024_1689.laif.md` | 299 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/eu-ai-act-2024-1689/eu_ai_act_2024_1689.technical_appendix.md` | 1213 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md` | 319 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.technical_appendix.md` | 1037 | historical/evidence |
| `docs/verification/2026-11-07-real-source-assurance/notion-sync.md` | 11 | historical/evidence |
| `docs/verification/2026-11-07-reporting-challenge/README.md` | 50 | historical/evidence |
| `docs/verification/2026-11-07-reporting-challenge/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md` | 272 | historical/evidence |
| `docs/verification/2026-11-07-reporting-challenge/au_dta_policy_v2_1/au_dta_policy_v2_1.technical_appendix.md` | 1034 | historical/evidence |
| `docs/verification/2026-11-07-reporting-challenge/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md` | 256 | historical/evidence |
| `docs/verification/2026-11-07-reporting-challenge/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.technical_appendix.md` | 1037 | historical/evidence |
| `docs/verification/2026-11-07-substantive-review/5f667a6f-NIST.AI.1001/assessment.md` | 430 | historical/evidence |
| `docs/verification/2026-11-07-substantive-review/README.md` | 96 | historical/evidence |
| `docs/verification/2026-11-07-substantive-review/au_dta_policy_v2_1/assessment.md` | 535 | historical/evidence |
| `docs/verification/2026-11-07-substantive-review/notion-sync.md` | 9 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/README.md` | 75 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/REASONING_REVIEW.md` | 21 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/VALIDATION.md` | 38 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/au_dta_policy_v2_1.assessment.md` | 170 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/eu_ai_act_amendment_2026_1744.assessment.md` | 216 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.institutional_report.md` | 123 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.laif.md` | 464 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.technical_appendix.md` | 1095 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/analyst/Policy-for-the-responsible-use-of-AI-in-government-2_1_1/AI_ANALYST_PROMPT.md` | 29 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/analyst/Policy-for-the-responsible-use-of-AI-in-government-2_1_1/AI_REPORT_VALIDATION_RULES.md` | 10 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/analyst/Policy-for-the-responsible-use-of-AI-in-government-2_1_1/quote_bank.md` | 117 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/analyst/Policy-for-the-responsible-use-of-AI-in-government-2_1_1/verification_required_evidence.md` | 9 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/OJ_L_202601744_EN_TXT.institutional_report.md` | 86 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/OJ_L_202601744_EN_TXT.laif.md` | 466 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/OJ_L_202601744_EN_TXT.technical_appendix.md` | 1022 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/analyst/OJ_L_202601744_EN_TXT/AI_ANALYST_PROMPT.md` | 29 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/analyst/OJ_L_202601744_EN_TXT/AI_REPORT_VALIDATION_RULES.md` | 10 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/analyst/OJ_L_202601744_EN_TXT/quote_bank.md` | 6 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/analyst/OJ_L_202601744_EN_TXT/verification_required_evidence.md` | 3 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/analyst/au_dta_policy_v2_1/AI_ANALYST_PROMPT.md` | 29 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/analyst/au_dta_policy_v2_1/AI_REPORT_VALIDATION_RULES.md` | 10 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/analyst/au_dta_policy_v2_1/quote_bank.md` | 117 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/analyst/au_dta_policy_v2_1/verification_required_evidence.md` | 3 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/au_dta_policy_v2_1.institutional_report.md` | 132 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md` | 467 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/au_dta_policy_v2_1.technical_appendix.md` | 1045 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/analyst/eu_ai_act_amendment_2026_1744/AI_ANALYST_PROMPT.md` | 29 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/analyst/eu_ai_act_amendment_2026_1744/AI_REPORT_VALIDATION_RULES.md` | 10 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/analyst/eu_ai_act_amendment_2026_1744/quote_bank.md` | 154 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/analyst/eu_ai_act_amendment_2026_1744/verification_required_evidence.md` | 9 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.institutional_report.md` | 90 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md` | 457 | historical/evidence |
| `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.technical_appendix.md` | 1044 | historical/evidence |
| `docs/verification/2026-11-14-nist-pdf-fidelity/README.md` | 95 | historical/evidence |
| `docs/verification/CURRENT.md` | 60 | historical/evidence |
| `docs/verification/INDEX.md` | 30 | historical/evidence |
| `docs/verified/README.md` | 78 | historical/evidence |
| `docs/verified/SOURCE_CURRENCY.md` | 36 | historical/evidence |
| `docs/verified/extracted/51a29205-OECD-evidence-trace.md` | 102 | historical/evidence |
| `docs/verified/extracted/55eccce3-DTAC-evidence-trace.md` | 131 | historical/evidence |
| `docs/verified/extracted/5f667a6f-NIST-evidence-trace.md` | 123 | historical/evidence |
| `docs/verified/extracted/au_dta_policy_v2_1.md` | 191 | historical/evidence |
| `docs/verified/extracted/b0ef43db-EO14110-evidence-trace.md` | 101 | historical/evidence |
| `docs/verified/extracted/eu-ai-act-2024-1689-ingestion-trace.md` | 17 | historical/evidence |
| `docs/verified/extracted/eu_ai_act_amendment_2026_1744.md` | 369 | historical/evidence |
| `docs/verified/nist_reconciliation.md` | 151 | historical/evidence |
| `docs/verified/pending/2026-11-07_SOURCE_SCOPED_PRELIMINARY_REVIEW.md` | 57 | historical/evidence |
| `docs/verified/pending/au_dta_policy_v2_1.md` | 38 | historical/evidence |
| `docs/verified/pending/eu_ai_act_2026_amendment.md` | 39 | historical/evidence |
| `docs/verified/pending/eu_ai_act_ingestion_ready.md` | 133 | historical/evidence |
| `docs/verified/raw/51a29205-OECD_Legal_Instruments.md` | 731 | historical/evidence |
| `docs/verified/raw/55eccce3-DTAC_Form_2.0_February_2026.md` | 197 | historical/evidence |
| `docs/verified/raw/5f667a6f-NIST.AI.1001.md` | 388 | historical/evidence |
| `docs/verified/raw/au_dta_policy_v2_1.md` | 1118 | historical/evidence |
| `docs/verified/raw/b0ef43db-202324283.md` | 406 | historical/evidence |
| `docs/verified/raw/eu_ai_act_2024_1689.md` | 6822 | historical/evidence |
| `docs/verified/raw/eu_ai_act_amendment_2026_1744.md` | 2823 | historical/evidence |
| `docs/verified/url_verification/verification_report.md` | 200 | historical/evidence |
| `laif_inputs/processed/README.md` | 5 | guide/reference |
| `reports/README.md` | 55 | historical/evidence |
| `reports/laif_assessment_aus_ai_policy_v2.md` | 385 | historical/evidence |
| `reports/laif_executive_summary.md` | 52 | historical/evidence |
| `reports/laif_full_assessment.md` | 634 | historical/evidence |
| `reports/laif_real_world_assessment.md` | 3559 | historical/evidence |
| `verified_corpus_manifest.md` | 192 | guide/reference |

## Site Markdown inventory

| File | Role |
|---|---|
| `README.md` | maintainer guide |
| `THIRD_PARTY_NOTICES.md` | source/fixture/licence |
| `docs/AUTOMATIC_CRITERIA_RELEASE.md` | dated release evidence |
| `docs/MODERNISATION_REVIEW.md` | dated release evidence |
| `docs/UX_REVIEW_2026-11-07.md` | dated release evidence |
| `docs/verification/JOURNEY_EXPERIENCE_2026-11-16.md` | dated release evidence |
| `docs/verification/UX_UPGRADE_2026-11-07.md` | dated release evidence |
| `public/canonical/5f667a6f-NIST.AI.1001.md` | source/fixture/licence |
| `public/canonical/au_dta_policy_v2_1.md` | source/fixture/licence |
| `public/canonical/eu_ai_act_amendment_2026_1744.md` | source/fixture/licence |
| `tests/fixtures/vendor-policy.md` | source/fixture/licence |
| `vendor/shadcn-tailwind-4.13.0.LICENSE.md` | source/fixture/licence |
