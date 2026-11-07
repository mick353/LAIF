# Substantive LAIF criterion reviews

The optional criterion review carries an author's actual LAIF reasoning into the
normal report for any local source. It covers A.1–A.4, Q1–Q3 and G.1. It does not
change scores or certify a deployment.

## Prepare the source-locked template

~~~bash
python3 -S scripts/laif_research_report.py /path/to/policy.md --scope declared_full_document --criteria-template --output-dir /path/to/review
~~~

The operator's full-document declaration concerns the supplied source, not the
completeness of the wider governance setting. The template's criterion records
start unfilled and are rejected until completed.

Complete criteria_review with analyst_id, as_at_date (YYYY-MM-DD), jurisdiction,
assessed_role, document_scope, overall_reasoning and limitations. Each criterion
needs these fields:

| Field | Required content |
|---|---|
| criterion_id | A.1, A.2, A.3, A.4, Q1, Q2, Q3 or G.1 |
| determination | SUPPORTED_IN_SCOPE, PARTIAL_SUPPORT, NOT_ESTABLISHED, SOURCE_CONFLICT or NOT_APPLICABLE |
| reasoning | Explain how the cited source supports the determination |
| framework_basis | Identify the relevant LAIF rule |
| applicability_reason | Explain applicability, including section 2.5 for Calibration |
| scope_and_exceptions | Identify actor, conditions, other instruments and remaining limits |
| alternative_explanation | A plausible reading or evidence that could change the conclusion |
| closure_evidence | What evidence or control would resolve the question |
| source_excerpts | 1–12 exact source spans, unique C-style IDs and context |

Q1 separately requires coupling.q1a (NONE, IMPLICIT, EXPLICIT or UNKNOWN),
coupling.q1b (NONE, SOFT, HARD or UNKNOWN), protected_interest, restriction and
equivalent_normative_force reasoning. An affirmative Q1 source-support label
cannot coexist with absent/unknown pairing or force. The software does not
determine equivalent force from those classifications.

A curated excerpt comes from the entire normalised extracted source, beyond
the automatic E-style quote inventory:

~~~json
{
  "evidence_id": "C001",
  "start_char": 100,
  "end_char": 150,
  "exact_quote": "Replace this with the exact span at the real offsets.",
  "context": "Identify the section, actor, conditions and qualifications."
}
~~~

Exact matching does not grant primary-quote quality or verify interpretation.
For a table, retain its governing row/column context and inspect the original.
Do not treat an unselected questionnaire option as an observed response.
Offsets identify extracted characters, not original PDF bytes or verified pages.
The report quotes each curated excerpt below its criterion, with a source name
and available section, page-marker and line references. Offsets remain audit
metadata. Submitted supporting and counterevidence passages are also quoted at
their findings, with links to the full evidence inventory.

Keep the source, evidence, framework, Toolkit, toolchain and criterion-protocol
hashes from the template. A source or method change needs a fresh template and
rechecked findings. The legacy findings list can coexist with criteria_review;
it may be empty when the criterion records supply the analysis.

## Generate the assessment

~~~bash
python3 -S scripts/laif_process_document.py /path/to/policy.md --extractor builtin --review-file /path/to/completed-review.json --require-complete-review --output-dir /path/to/output
~~~

The completeness gate rejects missing criterion records before writes. Without
it, valid partial reviews remain permitted and omissions stay NOT_ASSESSED.
Addressing every criterion does not mean that the Integrity Layer or Coherence
Test passes. A complete assessment may identify unmet or unestablished conditions.
PASS/FAIL certification labels are not imported; native certification is protected.

The executive finding leads with the authored reasoning. The Markdown report,
assessment JSON and analyst bundle preserve the determinations, quotations,
applicability, alternatives and closing evidence. Ordinary unreviewed runs retain
their existing path.

## Second readers

Generate a reviewed research dossier, then its second-reader template:

~~~bash
python3 -S scripts/laif_research_report.py /path/to/policy.md --review-file /path/to/completed-review.json --output-dir /path/to/dossier
python3 -S scripts/laif_research_review.py /path/to/generated.research_data.json --template
~~~

Use the generated dossier's actual filename. The target inventory includes every
criterion (CR-A.1 through CR-G.1 as applicable) and all curated C-style excerpts.
Defaults remain uncertain/unverified. A changed criterion or quotation changes
the dossier hash and invalidates older reader submissions. No independent review
is manufactured; self-attestation and agreement are not certification.

[Actual DTA/NIST assessments and verification](../verification/2026-11-07-substantive-review/README.md)
