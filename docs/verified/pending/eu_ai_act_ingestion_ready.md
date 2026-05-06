# EU AI Act — Manual Authoritative Ingestion Readiness

**Document:** Regulation (EU) 2024/1689 — Artificial Intelligence Act
**Status:** READY_FOR_MANUAL_AUTHORITATIVE_INGESTION
**Preferred source:** EUR-Lex Regulation (EU) 2024/1689
**Preferred origin URL:** https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689
**Readiness date:** May 2026

---

## 1. Purpose

Automated retrieval from EUR-Lex returned HTTP 403 in the assessment environment. This is not a terminal failure state. The repository is prepared for lawful manual authoritative ingestion through either:

- `HUMAN_GITHUB_DEPOSIT`
- `HUMAN_SESSION_UPLOAD`

Do not reconstruct, paraphrase, summarise, or assess the EU AI Act from memory. No EU AI Act authoritative assessment may be performed until the full authoritative source is supplied and validated.

---

## 2. Expected File Destination

The human-supplied authoritative file must first be placed exactly as supplied in:

`docs/verified/manual_ingest/`

After extraction/normalisation, the verified raw text should be written to:

`docs/verified/raw/eu_ai_act_2024_1689.<ext>`

Recommended final extracted filename:

`docs/verified/raw/eu_ai_act_2024_1689.md`

---

## 3. Accepted Source Formats

Accepted authoritative-source formats:

- PDF
- HTML
- TXT
- MD

Screenshots are not accepted as a full citable source unless explicitly classified `NON_CITABLE` and excluded from authoritative assessment.

---

## 4. Required Manifest Fields

Update `docs/verified/manifests/eu-ai-act-2024-1689.json` before assessment. Required fields include:

- `document_id`
- `title`
- `jurisdiction`
- `source_type`
- `authoritative_url`
- `authoritative_origin_url`
- `acquisition_channel`
- `acquired_by`
- `acquired_at_utc`
- `acquisition_note`
- `source_file_sha256`
- `sha256_hash`
- `raw_filename`
- `publication_date`
- `version_identifier`
- `extraction_boundaries`
- `transformation_status`
- `transformation_chain`
- `citation_status`
- `provenance_classification`
- `verification_status`
- `assessment_status`
- `evidence_trace`

---

## 5. Required Hash Generation Step

After the authoritative file is deposited in `docs/verified/manual_ingest/`, compute:

```bash
sha256sum docs/verified/manual_ingest/<eu-ai-act-source-file>
```

Record this hash as `source_file_sha256`.

After extraction to `docs/verified/raw/`, compute:

```bash
sha256sum docs/verified/raw/eu_ai_act_2024_1689.md
```

Record this hash as `sha256_hash`.

---

## 6. Required Extraction Boundaries

Preferred extraction boundary:

```json
{
  "full_document": true,
  "sections": null,
  "notes": "Full Regulation (EU) 2024/1689 ingested from authoritative EUR-Lex source. No sections excluded."
}
```

If a future assessment intentionally assesses selected articles only, the manifest must explicitly list article numbers in `sections`, downgrade citeability where appropriate, and avoid any claim of full-document authoritative assessment.

---

## 7. Required Assessment Trigger

Only after source ingestion and validation pass may assessment begin:

```bash
python3 validate.py
python3 validate.py --verified-corpus
python3 validate.py --check-evidence-traces
```

Assessment must use the existing LAIF v1.2 refined model v1.1 unchanged. No scoring, detector, or interpretation semantics may change as part of EU AI Act ingestion.

---

*LAIF v1.2 · EU AI Act Manual Ingestion Readiness · May 2026*
