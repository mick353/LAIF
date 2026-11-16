"""LAIF engine: reporting. Moved without changing assessment rules."""

from collections import Counter
from .evidence import (
    _governance_force_profile,
    _remediation_groups,
)
from .identity import (
    _corpus_fingerprint,
    toolchain_fingerprint,
)
from .report_helpers import (
    FINGERPRINT_DISPLAY_CHARS,
    REPORT_DATE,
    _compact_list,
    _markdown_table,
    _md_anchor,
    _public_report_status_label,
    _report_boundary_notice,
    _report_caution_summary,
    _report_document_row,
    _report_evidence_summary,
    _report_limits_and_reviewer_actions,
    _report_score_band,
    _safe_executive_verdict_text,
    _safe_markdown_cell,
)
from .source_display import (
    _suggest_anchor,
)


def generate_executive_summary(assessments, report_date=REPORT_DATE,
                               full_report_path="reports/laif_real_world_assessment.md"):
    """One-page executive summary for readers who will never open the full
    report: the finding, the corpus at a glance, what is missing everywhere,
    where to start, and how to read it. Fully derived from the same results —
    no independent claims."""
    lines = []
    a = lines.append
    count = len(assessments) or 1
    citable = [r for r in assessments if r.get("provenance") == "OFFICIAL_EXCERPT"]

    def avg(key, rows=None):
        rows = assessments if rows is None else rows
        return round(sum(r.get(key, 0) for r in rows) / len(rows)) if rows else 0

    cal = [(r, r.get("score_calibration", {}).get("overall_pct_of_ceiling", 0))
           for r in assessments
           if r.get("score_calibration", {}).get("achievable_ceiling", 100) < 100]
    # Certification-channel gaps (absence of the assessing framework's own
    # vocabulary) are never substantive actions for an external instrument —
    # excluded from the finding, the priorities, and the per-document column.
    def _is_channel_gap(g):
        """Distance from LAIF's own vocabulary, not a deficiency in the document.

        Covers both wordings: the certification-channel phrasing used for
        external instruments, and the terminology phrasing used where a
        document uses or claims LAIF vocabulary.
        """
        gl = str(g).lower()
        return ("canonical laif terms" in gl or "terminological" in gl
                or "paraphrase" in gl or "certification channel" in gl
                or "laif-native vocabulary not used" in gl)

    gap_counter = Counter(g for r in assessments
                          for g in r.get("primary_failure_modes", [])
                          if not _is_channel_gap(g))
    structure_absent = Counter()
    structure_present = Counter()
    for r in assessments:
        for c, v in r.get("functional_alignment", {}).items():
            if v.get("verdict") == "ABSENT":
                structure_absent[c] += 1
            else:
                structure_present[c] += 1

    a("# AI Governance Structural Integrity — Executive Summary")
    a("")
    a(f"**Date:** {report_date} · **Documents assessed:** {count} "
      f"({len(citable)} from verbatim official text) · "
      f"**Corpus fingerprint:** "
      f"`{_corpus_fingerprint(assessments)[:FINGERPRINT_DISPLAY_CHARS]}`  ")
    a(f"**Full assessment:** `{full_report_path}` — this page is a summary of it, "
      f"not a separate finding.")
    a("")
    a("---")
    a("")

    # ── The finding ──────────────────────────────────────────────────────
    a("## The finding")
    a("")
    universal = [(g, n) for g, n in gap_counter.most_common() if n == count]
    absent_everywhere = [c for c, n in structure_absent.items() if n == count]
    if universal:
        if len(universal) == 1:
            a(f"Every one of the {count} instruments assessed shares the same "
              f"structural gap: **{universal[0][0]}**.")
        else:
            a(f"Every one of the {count} instruments assessed shares the same "
              f"{len(universal)} structural gaps: "
              + "; ".join(f"**{g}**" for g, _ in universal) + ".")
    else:
        top = gap_counter.most_common(1)
        if top:
            a(f"The most widespread structural gap across the corpus is "
              f"**{top[0][0]}** ({top[0][1]} of {count} documents).")
    a("")
    if absent_everywhere:
        a(f"No document in this corpus expresses **{', '.join(absent_everywhere)}** "
          f"in any vocabulary — these are not terminology gaps but absent "
          f"governance machinery.")
        a("")
    a(f"Average conceptual proximity is {avg('conceptual_proximity_score')}/100 "
      f"while average overall readiness is {avg('overall_readiness_score')}/100: "
      f"these instruments consistently name the right human concerns and carry real "
      f"administrative machinery, but stop short of binding their obligations to "
      f"the people those obligations serve.")
    a("")

    # ── At a glance ──────────────────────────────────────────────────────
    a("## Corpus at a glance")
    a("")
    rows = []
    for r in sorted(assessments,
                    key=lambda x: -x.get("score_calibration", {})
                                    .get("overall_pct_of_ceiling", 0)):
        pct = r.get("score_calibration", {}).get("overall_pct_of_ceiling", 0)
        _doc_gaps = [g for g in r.get("primary_failure_modes", [])
                     if not _is_channel_gap(g)]
        _distinct = [g for g in _doc_gaps if gap_counter.get(g, 0) < count]
        top_gap = _distinct[0] if _distinct else "— (universal gaps only)"
        rows.append([
            _safe_markdown_cell(r.get("document_name", ""))[:52],
            "official" if r.get("provenance") == "OFFICIAL_EXCERPT" else "illustrative",
            r.get("laif_alignment", ""),
            f"{pct}%",
            _safe_markdown_cell(top_gap)[:46],
        ])
    lines.extend(_markdown_table(
        ["Document", "Text", "Structural alignment", "Calibrated position",
         "Gap specific to this document"], rows))
    a("")
    a("*Calibrated position is the score as a percentage of what is achievable "
      "without adopting the assessing framework's own vocabulary — raw scores "
      "compress by design and must not be read as percentage grades.*")
    a("")

    # ── Where to start ───────────────────────────────────────────────────
    a("## Where to start — highest-value actions across the corpus")
    a("")
    priority = []
    if absent_everywhere:
        for c in absent_everywhere[:2]:
            priority.append(
                f"**Establish {c.lower()} machinery.** No assessed instrument has "
                f"it in any form, so there is no peer text to adapt — an owner "
                f"adding it sets the benchmark.")
    for g, n in gap_counter.most_common(6):
        if len(priority) >= 4:
            break
        priority.append(f"**Close: {g}** — present in {n} of {count} documents.")
    if not priority:
        priority.append("**No structural gap is shared across this corpus** — "
                        "see each document's own section for its specific findings.")
    for i, item in enumerate(priority[:4], 1):
        a(f"{i}. {item}")
    a("")
    a("Every document's own section in the full report names the exact clause "
      "each fix attaches to, quoted from that document.")
    a("")

    # ── What good looks like ─────────────────────────────────────────────
    strongest = [(c, n) for c, n in structure_present.most_common() if n]
    if strongest:
        a("## What good already looks like here")
        a("")
        for c, n in strongest[:3]:
            a(f"- **{c}** — expressed in some form by {n} of {count} documents; "
              f"the full report quotes the strongest example and where it sits.")
        a("")

    # ── How to read ──────────────────────────────────────────────────────
    a("## How to read this")
    a("")
    a("- **This is a diagnostic, not a verdict.** It measures distance from a "
      "deliberately strict structural standard; it does not determine legal "
      "validity, and a gap is not a judgement of an instrument against its own "
      "objectives.")
    a("- **Findings from official text are citable** within each document's "
      "declared excerpt scope; findings from illustrative excerpts characterise "
      "framework style only.")
    a("- **Reproducible:** the fingerprint above identifies exactly which texts "
      "produced these results; regenerating from the same corpus yields "
      "byte-identical output.")
    a("")
    return "\n".join(lines)


def export_assessment_data(assessments, report_date=REPORT_DATE):
    """Machine-readable export for GRC tooling, dashboards, and independent
    re-analysis. Deterministic and self-describing; carries verdicts, scores,
    locations, and gaps — not full source text."""
    def doc_record(r):
        return {
            "document_name":       r.get("document_name", ""),
            "citation":            r.get("citation", ""),
            "jurisdiction":        r.get("jurisdiction", ""),
            "source_type":         r.get("source_type", ""),
            "sector":              r.get("sector_used", ""),
            "provenance":          r.get("provenance", ""),
            "citable":             r.get("provenance") == "OFFICIAL_EXCERPT",
            "source_url":          r.get("source_url", ""),
            "source_file":         r.get("source_file", ""),
            "assessed_text_sha256": r.get("assessed_text_sha256", ""),
            "assessment_mode":     r.get("assessment_mode", ""),
            "substantive_coherence_determination": r.get("substantive_coherence_determination", "REQUIRES_SOURCE_BASED_REVIEW"),
            "integrity_requirement_diagnostics": r.get("integrity_requirement_diagnostics", []),
            "automatic_criteria": r.get("automatic_criteria"),
            "scores": {
                "structural":           r.get("structural_score", 0),
                "terminology":          r.get("terminology_score", 0),
                "conceptual_proximity": r.get("conceptual_proximity_score", 0),
                "auditability":         r.get("auditability_score", 0),
                "enforceability":       r.get("enforceability_score", 0),
                "overall_readiness":    r.get("overall_readiness_score", 0),
                "sector_risk_alignment": r.get("sector_risk_alignment", 0),
            },
            "calibration":         r.get("score_calibration", {}),
            "structural_alignment": r.get("laif_alignment", ""),
            "coupling_state":      r.get("coupling_state", ""),
            "structural_depth":    r.get("structural_depth", ""),
            # Integrity qualifiers: a consumer must be able to see that a
            # document's signals came from a term list, or that it revokes a
            # protection it states, without re-deriving either.
            # Whether the engine's English-language patterns could read the
            # text at all. A consumer must be able to discard a near-zero score
            # that reflects the instrument rather than the document.
            "language_coverage": {
                "readable_by_engine":       r.get("english_language_readable", True),
                "english_function_word_ratio": r.get("english_function_word_ratio"),
                "note":                     r.get("language_coverage_note", ""),
            },
            "assessed_character_count": r.get("assessed_character_count", 0),
            "vocabulary_enumeration": {
                "risk":     r.get("vocabulary_enumeration_risk", "LOW"),
                "ratio":    r.get("vocabulary_enumeration_ratio", 0.0),
                "reason":   r.get("vocabulary_enumeration_reason", ""),
                "examples": r.get("vocabulary_enumeration_examples", []),
            },
            "self_contradictions": [
                {"property": c[0], "description": c[1], "context": c[2]}
                for c in r.get("contradictions", [])
                if isinstance(c, (list, tuple)) and len(c) >= 3
            ],
            "deployment_risk_tier": r.get("deployment_risk_tier", ""),
            "functional_alignment": {
                c: {
                    "verdict":   v.get("verdict", ""),
                    "families":  v.get("families", []),
                    "locations": v.get("evidence_locations", []),
                }
                for c, v in sorted(r.get("functional_alignment", {}).items())
            },
            "document_outline":    r.get("document_outline", []),
            "primary_structural_gaps": r.get("primary_failure_modes", []),
            "diagnostic_gaps":     r.get("gaps", []),
            "obligation_anchors":  r.get("obligation_anchors", []),
            "signal_locations":    r.get("signal_locations", {}),
            "contradictions": [
                {"property": p, "description": d, "evidence": c}
                for p, d, c in r.get("contradictions", [])
            ],
            "remediation": r.get("structured_remediation_steps", []),
        }

    return {
        "schema":        "laif.assessment.v1",
        "schema_revision": 4,
        # The code that produced this export, so a consumer can tell a stale
        # artifact from a current one without diffing its contents.
        "toolchain_fingerprint": toolchain_fingerprint(),
        "schema_revision_note": (
            "Revisions are additive only: fields are added, never removed or "
            "redefined. r2 added functional_alignment locations, obligation "
            "anchors, and score calibration; r3 added language_coverage, "
            "vocabulary_enumeration, self_contradictions, and "
            "assessed_character_count. A removal or a change of meaning would "
            "take a new schema id."),
        "report_date":   report_date,
        "framework":     "LAIF v1.2 · Compliance Toolkit v1.1",
        "generator":     "test_real_world.py / assessment_engine.py",
        "boundary_notice": (
            "Diagnostic model output. Not a legal-validity determination, not "
            "certification, and not a compliance rating. Findings from documents "
            "marked citable=true may be cited within each document's declared "
            "excerpt scope; findings from citable=false characterise framework "
            "style only."
        ),
        "corpus_fingerprint": _corpus_fingerprint(assessments),
        "document_count":     len(assessments),
        "citable_count":      sum(1 for r in assessments
                                  if r.get("provenance") == "OFFICIAL_EXCERPT"),
        "documents":          [doc_record(r) for r in assessments],
    }


def generate_markdown_report(assessments, report_date=REPORT_DATE,
                             generation_command="python3 test_real_world.py"):
    """Render a stable public markdown report without changing assessment data."""
    lines = []
    assessments = list(assessments or [])

    def h(level, text):
        lines.append("\n" + "#" * level + " " + text)

    def p(text=""):
        lines.append(text)

    def table(headers, rows):
        lines.extend(_markdown_table(headers, rows))

    count = len(assessments)
    avg = lambda key: round(sum(r.get(key, 0) for r in assessments) / count) if count else 0
    native_failures = [r for r in assessments if r.get("formal_laif_native_compliance", r.get("formal_laif_compliance")) == "FAIL"]
    external_count = sum(1 for r in assessments if r.get("assessment_mode") == "external_framework")
    evidence_total = sum(len(r.get("evidence_traces", [])) for r in assessments)
    evidence_exact = sum(_report_evidence_summary(r)["exact"] for r in assessments)
    evidence_fallback = sum(_report_evidence_summary(r)["fallback"] for r in assessments)
    patch_total = sum(len(r.get("remediation_patches", [])) for r in assessments)
    force_counter = Counter()
    for r in assessments:
        for component, status, _ in _governance_force_profile(r):
            if status in {"gap / requires review", "requires reviewer confirmation"}:
                force_counter[component] += 1

    lines.append("# AI Governance Structural Integrity Assessment")
    p("*How far do these instruments' protections actually reach the people "
      "they govern — and what would it take to close the distance?*  ")
    p(f"**Report date:** {report_date}  ")
    p("**Assessment model:** Law-Aligned Intelligence Framework (LAIF) v1.2 · "
      "Compliance Toolkit v1.1 — the model is the measuring lens, not the "
      "subject of the findings; see Method Summary.  ")
    p("**Report template:** Governance Repair Assessment, public template v2.0 "
      "(evidence locator, functional alignment, peer exemplars)  ")
    _fingerprint = _corpus_fingerprint(assessments)[:FINGERPRINT_DISPLAY_CHARS]
    p(f"**Reproducibility:** output of `{generation_command}`; "
      f"corpus fingerprint `{_fingerprint}` (SHA-256 over the assessed texts, in "
      f"corpus order). Each document's scope table carries the SHA-256 of exactly "
      f"the text assessed.")
    p("**Validator boundary:** validate.py enforcement remains unchanged; this report renders existing assessment results only.  ")
    p()

    h(2, "Contents")
    p("[Report Scope and Boundary](#report-scope-and-boundary) · "
      "[Executive Brief](#executive-brief) · "
      "[Cross-Document Dashboard](#cross-document-dashboard) · "
      "[Peer Exemplars](#peer-exemplars-what-good-looks-like-in-this-corpus) · "
      "[Closing Notes](#closing-interpretation-notes)")
    for _i, _r in enumerate(assessments, 1):
        _title = f"Document {_i}: {_r.get('document_name', '')}"
        p(f"{_i}. [{_r.get('document_name', '')[:76]}](#{_md_anchor(_title)})")
    p()

    h(2, "Report Scope and Boundary")
    h(3, "Result Boundary / How to Read This Report")
    p("This public report is a governance repair and systemic failure-pathway diagnostic for institutional review.")
    p("This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.")
    p("External-framework mode assesses governance repair adequacy, operational closure, evidence sufficiency, accountability closure, lifecycle control, residual-risk closure, implementation readiness, and failure-pathway risk.")
    p("This report does not determine legal validity, enforceability, safety status, procurement eligibility, clinical authority, HR authority, education authority, or regulatory acceptance.")
    p("Not LAIF-native is certification-channel wording only; it is not a legal-validity or governance-validity determination.")
    p("Evidence traces preserve exact-source and reviewer-confirmation boundaries; trace presence does not prove implementation.")
    p("A detector non-match is not proof of an absent protection. Instrument requirements, source-based Coherence Test judgements and actual deployment behaviour are separate assessment questions.")
    p("Score bands summarize LAIF-model readiness signals and are not determinations of compliance; high scores cannot override formal LAIF-native failure.")
    p("Formal fail boundary: high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.")
    p()

    _citable      = [r for r in assessments if r.get("provenance") == "OFFICIAL_EXCERPT"]
    _illustrative = [r for r in assessments if r.get("provenance") != "OFFICIAL_EXCERPT"]
    h(3, "Evidence Basis and Citability")
    p("Every document carries a machine-verified provenance classification; findings "
      "inherit the citability of the text they were computed from "
      "(enforced by `test_provenance.py`).")
    p()
    table(
        ["Document", "Provenance", "Citable", "Evidence basis"],
        [
            [
                r.get("document_name", "")[:52],
                r.get("provenance", "") or "not declared",
                "Yes" if r.get("provenance") == "OFFICIAL_EXCERPT" else "No",
                (r.get("source_file") or r.get("source_url") or "illustrative document")[:60],
            ]
            for r in assessments
        ]
    )
    p()
    p("**OFFICIAL_EXCERPT** — text extracted verbatim at run time from the committed "
      "source file via unique start/end markers and pinned by SHA-256 "
      "(`official_documents.py`); any drift fails the run. Findings may be cited as "
      "statements about the named instrument within the declared excerpt scope. "
      "**REPRESENTATIVE_EXCERPT** — condensed paraphrase; findings characterise the "
      "framework style only and must not be presented as assessments of the official "
      "source instrument.")
    p()

    h(3, "Functional Alignment Layer (Substance Independent of Vocabulary)")
    p("Beyond the layers above, each core construct (Coupling, Integrity Layer, "
      "Consistency, Reversibility, Self-Application) is assessed for its *substance* "
      "in the document's own vocabulary — DECLARED (LAIF-native form), FUNCTIONAL "
      "(≥2 independent signal families including the construct's defining family), "
      "PARTIAL, or ABSENT. Grounded in LAIF v1.2 Part Eight (equivalent structural "
      "diligence through alternative documented means) and the Regulatory Integration "
      "Guide's SATISFIES/EXTENDS methodology. A document is never penalised for "
      "expressing LAIF's requirements in its own words, and never credited for using "
      "LAIF's words without the substance. Overall alignment verdicts: LAIF-NATIVE "
      "(qualified by structural depth) / FUNCTIONALLY ALIGNED / PARTIALLY ALIGNED / "
      "STRUCTURALLY UNALIGNED.")
    p()

    h(3, "Fair-Reading Bounds")
    p("1. A LAIF-native FAIL measures distance from LAIF's deliberately stricter "
      "standard, not instrument quality; it must never be quoted as a judgement of "
      "the instrument against its own objectives.")
    p("2. Official-corpus findings hold within each document's declared excerpt "
      "scope only.")
    p("3. Signals are lexical, not interpretive; per-signal traceability is the "
      "compensating control.")
    p("4. Form/questionnaire-style instruments are undercounted by prose rubrics; "
      "affected scorecards carry an interpretation caveat.")
    p("5. Cross-document averages characterise this corpus, not all AI governance.")
    p("6. Raw overall scores compress: part of the 100-point scale is reserved for "
      "LAIF-branded documents and lexical detection is conservative — a "
      "substance-perfect external document scores in the mid-50s on this "
      "instrument, so mid-range raw scores denote strength, not failure; each "
      "scorecard carries a calibrated position against the achievable ceiling.")
    p()

    h(2, "Executive Brief")
    _cal_pairs = [(r, r.get("score_calibration", {}).get("overall_pct_of_ceiling", 0))
                  for r in assessments
                  if r.get("score_calibration", {}).get("achievable_ceiling", 100) < 100]
    if _cal_pairs:
        _best_r, _best_p = max(_cal_pairs, key=lambda x: x[1])
        _worst_r, _worst_p = min(_cal_pairs, key=lambda x: x[1])
        _gap_common = Counter(g for r in assessments
                              for g in r.get("primary_failure_modes", [])).most_common(1)
        _construct_presence = Counter()
        for r in assessments:
            for c, v in r.get("functional_alignment", {}).items():
                if v.get("verdict") != "ABSENT":
                    _construct_presence[c] += 1
        _most_present = _construct_presence.most_common(1)
        def _tagged(_rr):
            _nm = _rr.get("document_name", "")[:56]
            if _rr.get("provenance") != "OFFICIAL_EXCERPT":
                _nm += " [illustrative excerpt]"
            return _nm
        _narr = (f"Across this corpus the strongest calibrated position is "
                 f"{_best_p}% ({_tagged(_best_r)}) and the "
                 f"weakest is {_worst_p}% ({_tagged(_worst_r)}).")
        if _gap_common:
            _narr += (f" The most widespread structural gap is: "
                      f"{_gap_common[0][0]} ({_gap_common[0][1]}/{count} documents).")
        if _most_present:
            _narr += (f" The core structure most often present in some form is "
                      f"{_most_present[0][0]} ({_most_present[0][1]}/{count} documents); "
                      f"see Peer Exemplars for the passages other owners can adapt.")
        p(_narr)
        p()
    p(f"- **Total documents assessed:** {count} ({external_count} external instruments "
      f"assessed as governance repair diagnostics, not LAIF-native certification)")
    p(f"- **Average overall readiness:** {avg('overall_readiness_score')}/100")
    p(f"- **Average conceptual proximity:** {avg('conceptual_proximity_score')}/100")
    p(f"- **Average sector alignment:** {avg('sector_risk_alignment')}/100")
    if _citable:
        _cit_fail = sum(1 for r in _citable
                        if r.get("formal_laif_native_compliance",
                                 r.get("formal_laif_compliance")) == "FAIL")
        _cit_con  = round(sum(r.get("conceptual_proximity_score", 0)
                              for r in _citable) / len(_citable))
        p(f"- **Citable subset (OFFICIAL_EXCERPT, verbatim hash-pinned):** "
          f"{len(_citable)}/{count} documents; {_cit_fail}/{len(_citable)} not "
          f"LAIF-native; average conceptual proximity {_cit_con}/100. These findings "
          f"may be stated of the named source instruments within excerpt scope.")
    _align_counter = Counter(r.get("laif_alignment", "not assessed") for r in assessments)
    p(f"- **Functional alignment distribution:** "
      f"{_compact_list([f'{k} ({v})' for k, v in _align_counter.most_common()])}")
    _ext_cals = [r["score_calibration"] for r in assessments
                 if r.get("score_calibration", {}).get("achievable_ceiling", 100) < 100]
    if _ext_cals:
        _avg_pct = round(sum(c["overall_pct_of_ceiling"] for c in _ext_cals) / len(_ext_cals))
        p(f"- **Average calibrated position (external instruments):** {_avg_pct}% of the "
          f"{_ext_cals[0]['achievable_ceiling']}-point ceiling achievable without "
          f"LAIF-native branding — raw scores compress by design and must not be read "
          f"as percentage grades.")
    p(f"- **Evidence trace summary:** {evidence_total} traces; {evidence_exact} exact/deterministic; {evidence_fallback} reviewer-confirmation fallback.")
    p(f"- **Remediation patch summary:** {patch_total} structured patches across assessed documents.")
    p(f"- **Top governance-force patterns:** {_compact_list([f'{k} ({v})' for k, v in force_counter.most_common(3)])}")
    if external_count == count:
        p("- **Certification channel:** no document in this corpus claims or seeks "
          "LAIF-native certification, so the certification gate is not a finding "
          "about these documents; construct coverage remains available in each "
          "Technical Appendix.")
    else:
        p(f"- **LAIF-native certification summary:** {count - len(native_failures)}/{count} PASS; "
          f"{len(native_failures)}/{count} FAIL where LAIF-native certification is claimed/applicable.")
    p("- **Boundary note:** diagnostic findings require reviewer confirmation and cannot override formal LAIF-native failure.")
    p()

    h(2, "Method Summary")
    h(3, "Method and Scoring Model")
    p("Assessment layers preserved: Formal LAIF-native certification gate; Dimensional scoring model; Structural depth / adversarial hardening; Validation boundary.")
    p("The renderer presents deterministic rubric outputs that already exist in each assessment result; it does not change scoring weights, score calculations, formal compliance calculation, validation, certification gates, sector metadata, evidence traces, remediation patches, or calibration metadata.")
    p("The report uses controlled public wording, suppresses raw regex disclosure, avoids keyword-stuffing recipes, and preserves legal-authority boundaries.")
    p("No legal determination is made; no source is certified through this public template unless the separate LAIF-native certification gate passes.")
    p()

    h(2, "Cross-Document Dashboard")
    h(3, "Score distribution / deterministic rubric comparison")
    table(
        ["Document", "Mode", "Alignment", "Overall score / band", "Sector profile", "Evidence traces", "Patches", "Cautions"],
        [_report_document_row(r) for r in assessments],
    )
    p()
    h(3, "Common structural gaps (cross-document)")
    _gap_counter = Counter(gap for r in assessments
                           for gap in r.get("primary_failure_modes", []))
    p(_compact_list([f"{g} ({n}/{count} documents)"
                     for g, n in _gap_counter.most_common(6)],
                    limit=6, empty="none identified"))
    h(3, "Governance-force patterns")
    p(_compact_list([f"{k} ({v})" for k, v in force_counter.most_common(5)]))
    h(3, "Remediation themes")
    theme_counts = Counter()
    for r in assessments:
        for group_name in _remediation_groups(r.get("recommended_remediation_steps", [])).keys():
            theme_counts[group_name] += 1
    p(_compact_list([f"{k} ({v})" for k, v in theme_counts.most_common(5)]))
    p()

    # ── Peer Exemplars — turn the corpus into a library of working examples
    h(2, "Peer Exemplars — What Good Looks Like in This Corpus")
    p("For each core structure, the strongest expression found anywhere in this "
      "corpus, quoted with its location — a working example a document owner can "
      "adapt. Verdict order: DECLARED > FUNCTIONAL > PARTIAL. Structures no "
      "document expresses are named honestly.")
    p()
    _verdict_rank = {"DECLARED": 3, "FUNCTIONAL": 2, "PARTIAL": 1, "ABSENT": 0}
    _constructs = ["Coupling", "Integrity Layer", "Consistency",
                   "Reversibility", "Self-Application"]
    _ex_rows, _absent_everywhere = [], []
    for _c in _constructs:
        # Rank: verdict strength first, verified-official provenance breaks
        # ties — a paraphrased excerpt must never outrank real instrument
        # text as the passage owners are invited to adapt.
        _best, _best_key = None, (0, 0)
        for _r in assessments:
            _v = _r.get("functional_alignment", {}).get(_c, {})
            if not (_v.get("evidence") or []):
                continue
            _key = (_verdict_rank.get(_v.get("verdict", "ABSENT"), 0),
                    1 if _r.get("provenance") == "OFFICIAL_EXCERPT" else 0)
            if _key > _best_key and _key[0] > 0:
                _best, _best_key = (_r, _v), _key
        if _best is None:
            _absent_everywhere.append(_c)
            continue
        _r, _v = _best
        _ev  = (_v.get("evidence") or [""])[0]
        _loc = (_v.get("evidence_locations") or ["—"])[0]
        _official = _r.get("provenance") == "OFFICIAL_EXCERPT"
        _ex_rows.append([
            _c,
            _safe_markdown_cell(_r.get("document_name", ""))[:44],
            _v.get("verdict", ""),
            "verbatim official text" if _official
            else "illustrative excerpt — verify against the official instrument",
            _safe_markdown_cell(_loc)[:40],
            _safe_markdown_cell("«" + _ev + "»")[:130] if _ev else "—",
        ])
    if _ex_rows:
        table(["Structure", "Best example in corpus", "Strength", "Text status",
               "Where", "Verbatim passage"], _ex_rows)
    if _absent_everywhere:
        p(f"**Expressed by no document in this corpus:** "
          f"{', '.join(_absent_everywhere)} — there is no peer example to adapt; "
          f"an owner adding this would be setting the benchmark.")
    p()

    h(2, "Per-Document Assessment")
    for idx, r in enumerate(assessments, 1):
        h(3, f"Document {idx}: {r.get('document_name', '')}")

        h(4, "Document Overview")
        h(5, "Assessment Scope")
        overview = [
            ["Document name", r.get("document_name", "")],
            ["Source type", r.get("source_type", "")],
            ["Jurisdiction", r.get("jurisdiction", "")],
            ["Sector", r.get("sector_label", r.get("sector_used", ""))],
            ["Assessment mode", r.get("assessment_mode", "external_framework")],
            ["Citation", r.get("citation", "") or "not provided"],
            ["Source URL", r.get("source_url", "") or "not provided"],
            ["Provenance", r.get("provenance", "") or "not provided"],
        ]
        if r.get("assessment_mode") == "external_framework":
            overview.extend([
                ["Document type", r.get("document_type", "unknown_governance_document")],
                ["Assessed text SHA-256", r.get("assessed_text_sha256", "") or "unavailable"],
            ])
            if r.get("source_file"):
                overview.append(["Committed source file", r.get("source_file")])
            if r.get("original_file_name"):
                overview.append(["Original file name", r.get("original_file_name")])
            if r.get("source_sha256"):
                overview.append(["Original source SHA-256", r.get("source_sha256")])
        table(["Field", "Value"], overview)
        p()
        _doc_outline = r.get("document_outline", [])
        if _doc_outline:
            p(f"**Document structure detected ({len(_doc_outline)} sections):** "
              + " · ".join(_doc_outline[:10])
              + (" · …" if len(_doc_outline) > 10 else ""))
            p()

        # ── Plain-Language Reading — framework-free narrative, every sentence
        # keyed to a measured signal (see _plain_reading). No LAIF vocabulary.
        _plain = r.get("plain_reading", [])
        if _plain:
            h(4, "Plain-Language Reading (framework-free)")
            p("*What the measurements found, stated without any of this framework's "
              "vocabulary. Each statement is generated from a specific fired or "
              "missed signal — none of it is editorial.*")
            p()
            for _para in _plain:
                p(_para)
                p()


        if r.get("assessment_mode") == "external_framework":
            h(4, "Governance Repair Profile")
            table(
                ["Field", "Value"],
                [
                    ["document_type", r.get("document_type", "unknown_governance_document")],
                    ["recommended_use", r.get("recommended_use", "reviewer confirmation required")],
                    ["not_sufficient_for", r.get("not_sufficient_for", "reviewer confirmation required")],
                    ["governance_force_profile", r.get("governance_force_profile", "reviewer confirmation required")],
                    ["systemic_repair_value", r.get("systemic_repair_value", "reviewer confirmation required")],
                    ["operational_closure_rating", r.get("operational_closure_rating", "reviewer confirmation required")],
                    ["evidence_sufficiency_rating", r.get("evidence_sufficiency_rating", "reviewer confirmation required")],
                    ["accountability_closure_rating", r.get("accountability_closure_rating", "reviewer confirmation required")],
                    ["lifecycle_control_rating", r.get("lifecycle_control_rating", "reviewer confirmation required")],
                    ["residual_risk_control_rating", r.get("residual_risk_control_rating", "reviewer confirmation required")],
                    ["implementation_gap_rating", r.get("implementation_gap_rating", "reviewer confirmation required")],
                    ["failure_pathway_risk", r.get("failure_pathway_risk", "reviewer confirmation required")],
                    ["priority_repair_actions", _compact_list(r.get("priority_repair_actions", []), limit=5)],
                ],
            )
            p("This assessment measures governance repair adequacy and operational control closure. It does not require the source document to imitate LAIF-native form.")
            p()
            h(4, "Operational Closure Findings")
            p(f"- **Operational closure:** {r.get('operational_closure_rating', 'reviewer confirmation required')}")
            p(f"- **Accountability closure:** {r.get('accountability_closure_rating', 'reviewer confirmation required')}")
            p(f"- **Lifecycle control:** {r.get('lifecycle_control_rating', 'reviewer confirmation required')}")
            p(f"- **Residual-risk closure:** {r.get('residual_risk_control_rating', 'reviewer confirmation required')}")
            p()
            h(4, "Evidence Sufficiency Findings")
            p(f"- **Evidence sufficiency:** {r.get('evidence_sufficiency_rating', 'reviewer confirmation required')}")
            p(f"- **Evidence trace count:** {len(r.get('evidence_traces', []))}")
            p()
            h(4, "Implementation Gap Findings")
            p(f"- **Implementation gap rating:** {r.get('implementation_gap_rating', 'reviewer confirmation required')}")
            p(f"- **Priority repair actions:** {_compact_list(r.get('priority_repair_actions', []), limit=5)}")
            p()
            h(4, "Failure-Pathway Risk Findings")
            p(f"- **Failure-pathway risk:** {r.get('failure_pathway_risk', 'reviewer confirmation required')}")
            p("- **Reviewer next step:** confirm what the document actually controls, what it only appears to control, where systemic governance failure could still occur, and which operational controls must be assigned to a government, regulator, procurement team, or assurance reviewer.")
            p()
        if any(r.get(k) for k in ("provenance", "source_note", "source_url", "citation", "intended_use")):
            h(5, "Provenance / Source Basis")
            p(f"- **Source note:** {r.get('source_note', 'not provided') or 'not provided'}")
            p(f"- **Intended use:** {r.get('intended_use', 'not provided') or 'not provided'}")
            p("- **Reviewer confirmation required:** confirm source authority, version, excerpt completeness, and transformation chain.")
            p()

        h(4, "Mode / Boundary Notice")
        p("Legal / authority boundary: diagnostic LAIF-model assessment only; reviewer confirmation required.")
        p(_report_boundary_notice(r))
        if r.get("assessment_mode") == "external_framework":
            p("Public status label: **Governance repair assessment — external-framework diagnostic.**")
        else:
            p(f"Public status label: **{_public_report_status_label(r)}**.")
        p()

        h(4, "Executive Diagnostic Summary")
        p(_safe_executive_verdict_text(r))
        p(f"- **Overall readiness:** {r.get('overall_readiness_score', 0)}/100 — {_report_score_band(r)}")
        _cal = r.get("score_calibration", {})
        if _cal and _cal.get("achievable_ceiling", 100) < 100:
            p(f"- **Calibrated position:** {_cal.get('overall_pct_of_ceiling', 0)}% of the "
              f"{_cal.get('achievable_ceiling')}-point ceiling achievable without LAIF-native "
              f"branding. Raw scores compress on this instrument: "
              f"{round(100 - _cal.get('achievable_ceiling', 100), 1)} points are reserved for "
              f"LAIF-branded documents, and lexical detection is conservative — read the "
              f"calibrated figure, the functional alignment verdict, and the score band "
              f"together, never the raw number as a percentage grade.")
        p(f"- **Conceptual proximity:** {r.get('conceptual_proximity_score', 0)}/100")
        p(f"- **Sector risk alignment:** {r.get('sector_risk_alignment', 0)}/100")
        p(f"- **Remediation effort:** {r.get('remediation_effort', 'unknown')}")
        _structural_modes = [m for m in r.get("primary_failure_modes", [])
                             if "certification channel" not in str(m).lower()
                             and not str(m).startswith("terminological")]
        _channel_modes = len(r.get("primary_failure_modes", [])) - len(_structural_modes)
        p(f"- **Primary structural gaps:** "
          f"{_compact_list(_structural_modes, empty='none identified')}"
          + (f" (plus {_channel_modes} certification-channel note"
             f"{'s' if _channel_modes != 1 else ''}, not a governance gap)"
             if _channel_modes else ""))
        if r.get("strengths"):
            p(f"- **Structural strengths:** {_compact_list(r.get('strengths', []))}")
        p(f"- **Governance signal strength:** {r.get('governance_signal_strength', r.get('overall_readiness_score', 0))}")
        p(f"- **Structural dimension score:** {r.get('structural_depth_score', r.get('structural_score', 0))}/100")
        p("- **Position assessment:** diagnostic under the assessment model, not certification.")
        _alignment = r.get("laif_alignment", "")
        if _alignment:
            _align_gloss = {
                "FUNCTIONALLY ALIGNED": "LAIF's structural requirements are expressed "
                                        "in the document's own vocabulary; adoption "
                                        "distance is terminological",
                "PARTIALLY ALIGNED":    "some LAIF constructs present in substance or "
                                        "in form",
                "STRUCTURALLY UNALIGNED": "LAIF's distinctive structural mechanisms not "
                                          "detected in any form; conceptual overlap is "
                                          "measured separately",
            }.get(_alignment, "")
            p(f"- **Functional alignment:** {_alignment}"
              + (f" — {_align_gloss}" if _align_gloss else ""))
        p()

        # ── Functional Alignment table — substance independent of vocabulary
        _func = r.get("functional_alignment", {})
        if _func:
            h(4, "Functional Alignment (Substance Independent of Vocabulary)")
            p("DECLARED = LAIF-native form; FUNCTIONAL = substance present in the "
              "document's own vocabulary (≥2 independent signal families); "
              "PARTIAL = one family; ABSENT = none. Source: LAIF v1.2 Part Eight; "
              "Regulatory Integration Guide Part One.")
            table(
                ["Construct", "Verdict", "Signal families detected", "Location"],
                [
                    [c, v.get("verdict", ""),
                     _compact_list(v.get("families", [])),
                     _compact_list(v.get("evidence_locations", []), limit=2, empty="—")]
                    for c, v in _func.items()
                ]
            )
            if r.get("coupling_state") == "FUNCTIONAL":
                _fc_ev = _func.get("Coupling", {}).get("evidence", [])
                if _fc_ev:
                    p("Functional pairing evidence (verbatim from the document): "
                      + " · ".join(f"«{e[:120]}»" for e in _fc_ev[:2]))
                p("Two equally valid certification paths: (a) restate the existing "
                  "pairings as canonical Coupling declarations (Toolkit §2 B.1); or "
                  "(b) retain the document's own vocabulary and record a documented "
                  "equivalence mapping to PDCA Section B.1 per the Regulatory "
                  "Integration Guide's SATISFIES/EXTENDS methodology. The choice "
                  "belongs to the document's owner.")
            p()

        # ── Evidence Locator — every claim points into the document ─────
        _locs = r.get("signal_locations", {})
        if _locs:
            h(4, "Evidence Locator — Where the Signals Live")
            p("Verbatim quotes from the assessed text with their locations in the "
              "document's own structure. Top signals per dimension.")
            _loc_rows = []
            for _dim, _dim_label in (("structural", "Structural"),
                                      ("conceptual", "Conceptual"),
                                      ("auditability", "Auditability"),
                                      ("enforceability", "Enforceability")):
                for _row in _locs.get(_dim, [])[:3]:
                    _loc_rows.append([
                        _dim_label,
                        _safe_markdown_cell(_row["label"])[:44],
                        _safe_markdown_cell(_row["location"])[:44],
                        _safe_markdown_cell("«" + _row["quote"] + "»")[:120],
                    ])
            if _loc_rows:
                table(["Dimension", "Signal", "Location in document", "Verbatim quote"],
                      _loc_rows)
            p()

            # What was NOT found — and where it would belong
            h(4, "Not Found — and Where It Would Belong")
            p("For each material element the assessment did not detect: what was "
              "looked for, confirmation it was absent from the excerpt, and the "
              "most natural place in this document's own structure to add it.")
            _outline_pairs = [(0, lbl) for lbl in r.get("document_outline", [])]
            _oblig = r.get("obligation_anchors", [])
            _missing_rows = []
            _bd = r.get("score_breakdown", {})
            for _dim, _dim_label in (("structural", "Structural"),
                                      ("auditability", "Auditability"),
                                      ("enforceability", "Enforceability")):
                for _lbl, _w in _bd.get(_dim, {}).get("missed", [])[:2]:
                    _missing_rows.append([
                        _dim_label,
                        _safe_markdown_cell(_lbl)[:52],
                        _safe_markdown_cell(_suggest_anchor(_lbl, _outline_pairs, _oblig))[:110],
                    ])
            for _c, _v in r.get("functional_alignment", {}).items():
                if _v.get("verdict") == "ABSENT":
                    _missing_rows.append([
                        "Core structure",
                        _safe_markdown_cell(f"{_c} substance (any vocabulary)")[:52],
                        _safe_markdown_cell(_suggest_anchor(_c, _outline_pairs, _oblig))[:110],
                    ])
            if _missing_rows:
                table(["Layer", "Not detected in this excerpt", "Where it would belong"],
                      _missing_rows)
            else:
                p("All assessed elements were detected.")
            p()

            # Attachment points for the pairing fix — the exact sentences
            if _oblig and r.get("coupling_state") in ("ABSENT", "IMPLICIT"):
                h(4, "Attachment Points for Restriction-Protection Pairing")
                p("These obligation sentences are the exact places in this document "
                  "where a named-beneficiary protection would attach:")
                for _a in _oblig:
                    p(f"- Under **{_a['location']}**: «{_a['quote']}» — state here who "
                      f"this obligation protects, and bind the protection so neither "
                      f"can be weakened without the other.")
                p()

        if r.get("assessment_mode") == "external_framework":
            h(4, "Technical Appendix — Internal Diagnostic Boundary — LAIF-native construct coverage")
            p("Formal LAIF-native compliance details below are internal diagnostics for construct coverage only, not the headline finding for this external-framework assessment.")
            p(f"LAIF-native certification: Not claimed / not applicable to this external-framework assessment.")
            p()
        h(4, "Scorecard")
        p("Signals detected and Signals not detected are public labels only; raw detection patterns are not shown.")
        table(
            ["Dimension", "Score", "Fired signal labels", "Missed signal labels"],
            [
                ["Structural", f"{r.get('structural_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('structural', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('structural', {}).get('missed', [])])],
                ["Terminology", f"{r.get('terminology_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('terminology', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('terminology', {}).get('missed', [])])],
                ["Conceptual proximity", f"{r.get('conceptual_proximity_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('conceptual', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('conceptual', {}).get('missed', [])])],
                ["Auditability", f"{r.get('auditability_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('auditability', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('auditability', {}).get('missed', [])])],
                ["Enforceability", f"{r.get('enforceability_score', 0)}/100", _compact_list([x[0] for x in r.get('score_breakdown', {}).get('enforceability', {}).get('fired', [])]), _compact_list([x[0] for x in r.get('score_breakdown', {}).get('enforceability', {}).get('missed', [])])],
                ["Overall readiness", f"{r.get('overall_readiness_score', 0)}/100", _report_score_band(r), "—"],
            ],
        )
        p()

        h(4, "Score Calibration and Justification")
        p("Score justification explains LAIF-model signal strength only. It does not determine legal validity or certify LAIF-native compliance.")
        sj = r.get("score_justification", {})
        if sj:
            p(f"- **Overall band:** {sj.get('overall_band', _report_score_band(r))}")
            p(f"- **Formal LAIF-native status:** {sj.get('formal_laif_native_compliance', r.get('formal_laif_native_compliance', r.get('formal_laif_compliance', '')))}")
            p(f"- **Interpretation boundary:** {sj.get('interpretation_boundary', 'Formal LAIF-native failure cannot be overridden by high proximity scores.')}")
            for dim in sj.get("dimension_justifications", [])[:5]:
                p(f"- **{dim.get('dimension', 'dimension').title()}:** {dim.get('score', '')}/100 — {dim.get('band', '')}; {dim.get('calibration_note', '')}")
        cautions = _report_caution_summary(r)
        p(f"- **Calibration / anti-gaming cautions:** {cautions['total']} — {cautions['top']}")
        p("- **Anti-gaming boundary:** fired/missed labels are diagnostic summaries only; reviewers must require structural evidence and must not use this report as a keyword-stuffing recipe.")
        p()

        h(4, "Governance-Force Profile")
        table(["Component", "Status", "Reviewer note"], _governance_force_profile(r))
        p()

        h(4, "Sector / Institutional Context")
        p(f"- **Sector profile:** {r.get('sector_profile_label', r.get('sector_label', r.get('sector_used', 'general')))}")
        p(f"- **Sector profile key:** {r.get('sector_profile', r.get('sector_used', 'general_ai_governance'))}")
        p(f"- **Profile-specific remediation themes:** {_compact_list(r.get('sector_profile_remediation_themes', []))}")
        p(f"- **Profile-specific evidence cautions:** {_compact_list(r.get('sector_profile_evidence_cautions', []))}")
        p("- **Boundary:** profile diagnostics do not determine legal validity, LAIF-native certification, sector compliance, or sector obligations; reviewer confirmation required.")
        sector_findings = r.get("sector_specific_findings", [])
        if sector_findings:
            p(f"- **Sector diagnostic findings:** {_compact_list(sector_findings)}")
        p()

        h(4, "Evidence Trace Summary")
        p("Evidence traces are deterministic source-support metadata. They do not determine legal validity or certify LAIF-native compliance.")
        evidence = _report_evidence_summary(r)
        p(f"- **Total traces:** {evidence['total']}")
        p(f"- **Exact/deterministic count:** {evidence['exact']}")
        p(f"- **Fallback count:** {evidence['fallback']}")
        p(f"- **Evidence trace IDs:** {evidence['top']}")
        p("- **Reviewer-confirmation boundary:** trace support is source-text support for LAIF-model signals only and does not prove implementation, adoption, authority, or external effect.")
        p()

        h(4, "Construct Crosswalk")
        coverage = r.get("construct_coverage", {})
        if any(coverage.values()):
            table(["Construct", "Detected for LAIF-native gate"],
                  [[k, "yes" if v else "not detected"] for k, v in coverage.items()])
        else:
            p("No LAIF-native constructs detected — expected for an external "
              "instrument; see the Functional Alignment table for substance "
              "detected in the document's own vocabulary.")
        p("Each required LAIF-native construct remains necessary for certification; proximity evidence cannot substitute for a missing required construct.")
        p()

        h(4, "Diagnostic Gaps")
        gaps = r.get("gaps", []) or r.get("primary_failure_modes", [])
        if gaps:
            for gap in gaps:
                p(f"- {gap}")
        else:
            p("No diagnostic gaps generated by the current rubric.")
        p()

        h(4, "Remediation Priorities")
        p("LAIF structural remediation priorities are ordered diagnostic guidance, not authority determinations.")
        structured_steps = r.get("structured_remediation_steps", [])
        if structured_steps:
            h(5, "Structured remediation details")
            for i, step in enumerate(structured_steps[:5], 1):
                p(f"{i}. **Problem:** {step.get('problem', '')}")
                p(f"   - **Why it matters:** {step.get('why_it_matters', '')}")
                p(f"   - **Concrete fix:** {step.get('concrete_fix', '')}")
        else:
            p("Structured remediation details: reviewer confirmation required.")
            p("- **Problem:** diagnostic gap requires institutional review.")
            p("- **Why it matters:** governance-force evidence may be incomplete.")
            p("- **Concrete fix:** assign owner, evidence artifact, verification test, and authority review.")
        h(4, "Structured Remediation Patch Set")
        p("These patches are diagnostic guidance. They do not determine legal "
          "validity, and they do not certify compliance with the assessing "
          "framework unless that framework is separately adopted and verified.")
        _all_patches = r.get("remediation_patches", [])
        # Certification-channel items ask for no governance action: they record
        # distance from the assessing framework's own vocabulary. Listing them
        # beside real remediation invited a reader to build a control for not
        # having used LAIF's words. They stay in the JSON, counted here.
        patches = [x for x in _all_patches
                   if "certification channel" not in str(x.get("diagnostic_gap", "")).lower()]
        _channel = len(_all_patches) - len(patches)
        if patches:
            _shown = patches[:6]
            if len(patches) > 6:
                p(f"Showing the 6 highest-priority patches of {len(patches)}; the "
                  f"full set is available in the JSON assessment output.")
            if _channel:
                p(f"{_channel} further item{'s' if _channel != 1 else ''} in the JSON "
                  f"record distance from the assessing framework's own vocabulary. "
                  f"{'They require' if _channel != 1 else 'It requires'} no governance "
                  f"action and {'are' if _channel != 1 else 'is'} not listed here.")
            for patch in _shown:
                p(f"- **patch_id:** {patch.get('patch_id', '')}")
                p(f"  - **finding_type:** {patch.get('finding_type', '')}")
                p(f"  - **severity:** {patch.get('severity', '')}")
                p(f"  - **diagnostic_gap:** {patch.get('diagnostic_gap', '')}")
                p(f"  - **recommended_patch:** {patch.get('recommended_patch', '')}")
                p(f"  - **operational_control:** {patch.get('operational_control', '')}")
                p(f"  - **evidence_artifact:** {patch.get('evidence_artifact', '')}")
                p(f"  - **verification_test:** {patch.get('verification_test', '')}")
                p(f"  - **responsible_actor:** {patch.get('responsible_actor', '')}")
                ids = patch.get("evidence_trace_ids", [])
                p(f"  - **Evidence trace IDs:** {', '.join(ids) if ids else 'reviewer confirmation required / none linked'}")
                p(f"  - **legal_authority_boundary:** {patch.get('legal_authority_boundary', '')}")
                p("  - **Reviewer action:** confirm source authority; assign actor; verify evidence artifact; confirm escalation/reversibility; determine institution/regulator/contract authority.")
        elif _channel:
            p(f"No remediation patch is proposed. The {_channel} item"
              f"{'s' if _channel != 1 else ''} in the JSON record distance from the "
              f"assessing framework's own vocabulary and require no governance action.")
        else:
            p("No structured remediation patches generated by the current deterministic extractor.")
        p()

        h(4, "Limits and Reviewer Actions")
        for action in _report_limits_and_reviewer_actions(r):
            p(f"- {action}")
        p("- treat this report as diagnostic, not certification, and not a legal validity determination")
        p("- preserve the formal fail boundary: proximity evidence cannot override formal LAIF-native failure")
        p()

    h(2, "Integrity Layer requirement signals")
    p("These are text-pattern observations, not property verification or substantive Coherence Test verdicts. Non-detection is not absence. Calibration applicability follows section 2.5.")
    for item in assessments:
        h(3, item.get("document_name", "Document"))
        table(["Property", "Source section", "Observation"],
              [[r["property"], r["source_section"], r["signal_status"]]
               for r in item.get("integrity_requirement_diagnostics", [])])
    p()
    h(2, "Closing Interpretation Notes")
    p("- Public reports are diagnostics only and require evidence/authority review before institutional use.")
    p("- Reviewer confirmation required for source authority, implementation evidence, accountable ownership, and legal or contractual effect.")
    p("- Formal LAIF-native failure remains formal failure; high semantic, sector, evidence, or calibration proximity cannot override formal LAIF-native failure.")
    p("- This report does not determine legal validity and does not provide legal advice.")
    p("- Raw regex patterns are not disclosed; only report-safe signal labels and summaries are rendered.")
    p()
    p("---")
    p(f"*LAIF v1.2 · Compliance Toolkit v1.1 · {report_date} · Public Report Template*  ")
    p(f"*Generated by `{generation_command}`; scores and detector categories are diagnostics, not source-based Coherence Test or deployment certification determinations.*")
    return "\n".join(lines)
