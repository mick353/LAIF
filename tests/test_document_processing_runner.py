#!/usr/bin/env python3
"""Phase 3T tests for the LAIF document processing runner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from assessment_engine import assess, generate_markdown_report
from scripts import laif_process_document as runner

STRONG_EXTERNAL_TEXT = (
    "AI governance policy with transparency, accountability, human oversight, "
    "audit, monitoring, appeal, evidence documentation, public service delivery, "
    "and administrative review. Providers shall implement risk management, "
    "technical documentation, traceability, redress, review, escalation, and "
    "non-discrimination measures for high-risk AI systems."
)


class DocumentProcessingRunnerTests(unittest.TestCase):
    def run_cli(self, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "scripts/laif_process_document.py", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_cli_help_and_import_smoke(self) -> None:
        completed = self.run_cli(["--help"])
        self.assertIn("--extractor", completed.stdout)
        self.assertIn("--no-write", completed.stdout)
        self.assertTrue(hasattr(runner, "extract_document"))

    def test_txt_extraction_builtin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.txt"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            result = runner.extract_document(path, "builtin")
            self.assertEqual(result.extractor_used, "builtin")
            self.assertIn("transparency", result.text)

    def test_md_extraction_builtin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.md"
            path.write_text("# Policy\n\n" + STRONG_EXTERNAL_TEXT, encoding="utf-8")
            result = runner.extract_document(path, "builtin")
            self.assertEqual(result.extractor_used, "builtin")
            self.assertIn("# Policy", result.text)

    def test_empty_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "empty.txt"
            path.write_text("", encoding="utf-8")
            completed = self.run_cli([str(path), "--no-write"], check=False)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("safe minimum", completed.stderr)

    def test_unsupported_file_fails_when_no_extractor_can_handle_it(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "policy.unsupported"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            completed = self.run_cli([str(path), "--no-write"], check=False)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("Unsupported file type", completed.stderr)

    def test_optional_extractor_degradation_or_skip_if_not_installed(self) -> None:
        optional = {
            "docling": "docling",
            "markitdown": "markitdown",
            "python-docx": "docx",
            "pypdf": "pypdf",
        }
        for extractor, module_name in optional.items():
            with self.subTest(extractor=extractor):
                if importlib.util.find_spec(module_name) is None and extractor != "pypdf":
                    with self.assertRaises(runner.ExtractionError):
                        with tempfile.TemporaryDirectory() as td:
                            path = Path(td) / ("sample.docx" if extractor == "python-docx" else "sample.pdf")
                            path.write_bytes(b"not a real document")
                            runner.extract_document(path, extractor)
                elif extractor == "pypdf" and importlib.util.find_spec("pypdf") is None and importlib.util.find_spec("PyPDF2") is None:
                    with self.assertRaises(runner.ExtractionError):
                        with tempfile.TemporaryDirectory() as td:
                            path = Path(td) / "sample.pdf"
                            path.write_bytes(b"not a real pdf")
                            runner.extract_document(path, extractor)
                else:
                    self.assertTrue(True)

    def test_auto_sector_clinical_procurement_general(self) -> None:
        self.assertEqual(runner.auto_sector("clinical patient clinician safety incident"), "clinical_ai")
        self.assertEqual(runner.auto_sector("procurement vendor contract audit access"), "procurement_vendor_governance")
        self.assertEqual(runner.auto_sector("general transparency accountability governance"), "general_ai_governance")
        self.assertEqual(runner.auto_sector("AI Risk Management Framework voluntary non-sector-specific use-case agnostic govern map measure manage trustworthy AI."), "general_ai_governance")
        self.assertEqual(runner.auto_sector("Regulation laying down harmonised rules on artificial intelligence high-risk AI systems providers deployers conformity assessment market surveillance employment workers."), "general_ai_governance")
        self.assertEqual(runner.auto_sector("Digital health technology clinical safety DCB0129 clinical safety case hazard log patient care NHS data protection interoperability."), "clinical_ai")

    def test_no_write_writes_no_outputs_and_no_index(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            completed = self.run_cli([str(path), "--output-dir", str(out), "--no-write"])
            self.assertIn("Write mode: disabled", completed.stdout)
            self.assertFalse(out.exists())

    def test_write_enabled_creates_markdown_json_and_index(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            self.assertTrue(list(out.glob("*.laif.md")))
            self.assertTrue(list(out.glob("*.laif.json")))
            self.assertTrue((out / "laif_processing_index.jsonl").exists())

    def test_json_has_required_top_level_structure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            payload = json.loads(next(out.glob("*.laif.json")).read_text(encoding="utf-8"))
            self.assertEqual(set(payload), {"processing_metadata", "extraction_metadata", "assessment_result", "institutional_analyst_outputs"})
            self.assertIn("processed_at_utc", payload["processing_metadata"])
            self.assertIn("source_sha256", payload["extraction_metadata"])


    def test_institutional_analyst_outputs_generated_and_quote_exactness(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            source_text = STRONG_EXTERNAL_TEXT + " Organizations should document risks, assign accountability, monitor AI systems, review outcomes, manage incidents, and maintain evidence."
            path.write_text(source_text, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            institutional = next(out.glob("*.institutional_report.md"))
            appendix = next(out.glob("*.technical_appendix.md"))
            analyst = out / "analyst"
            self.assertTrue(institutional.exists())
            self.assertTrue(appendix.exists())
            for name in (
                "analyst_bundle.json",
                "quote_bank.jsonl",
                "quote_bank.md",
                "governance_gap_register.json",
                "failure_pathways.json",
                "control_recommendations.json",
                "AI_ANALYST_PROMPT.md",
                "AI_ANALYST_INPUT_BUNDLE.json",
                "AI_REPORT_VALIDATION_RULES.md",
            ):
                self.assertTrue((analyst / name).exists(), name)

            md = institutional.read_text(encoding="utf-8")
            for heading in ("Executive finding", "Key quoted evidence", "Operational gap", "Failure pathway", "Control implementation", "Residual risk"):
                self.assertIn(heading, md)
            self.assertNotIn("Formal LAIF-native compliance: FAIL", md[:1200])
            self.assertIn("LAIF-native construct coverage", appendix.read_text(encoding="utf-8"))

            bundle = json.loads((analyst / "analyst_bundle.json").read_text(encoding="utf-8"))
            self.assertTrue(bundle["quote_bank"])
            self.assertTrue(bundle["gap_register"])
            self.assertTrue(bundle["failure_pathways"][0]["steps"])
            for quote in bundle["quote_bank"]:
                self.assertIn(quote["exact_quote"], source_text)
            controls = bundle["control_recommendations"]
            for control in controls:
                for key in ("owner", "required_artifact", "minimum_evidence", "trigger", "threshold", "cadence", "decision_consequence"):
                    self.assertTrue(control[key])
            prompt = (analyst / "AI_ANALYST_PROMPT.md").read_text(encoding="utf-8")
            self.assertIn("Do not invent quotes", prompt)
            self.assertIn("Do not claim legal validity/invalidity", prompt)


    def test_phase_3x_quote_quality_rejects_non_primary_fragments(self) -> None:
        text = """
Artificial Intelligence Risk Management

3 Secure and Resilient 15

By la ying down those r ules providers shall maintain conformity assessment evidence and monitor incidents for high-risk AI systems.

Trustworthy AI systems should be valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed. Organizations should document risks, assign accountability, monitor AI systems, review outcomes, manage incidents, and maintain evidence of risk management activities.

If you are having difficulties with accessing this document, please email: support@example.com.
"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "nist_like.txt"
            out = root / "out"
            path.write_text(text, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            quotes = [q["exact_quote"] for q in bundle["quote_bank"]]
            joined = "\n".join(quotes)
            self.assertNotIn("Artificial Intelligence Risk Management", quotes)
            self.assertNotIn("3 Secure and Resilient 15", joined)
            self.assertNotIn("support@example.com", joined)
            self.assertNotIn("By la ying down those r ules", joined)
            self.assertTrue(any("Trustworthy AI systems should be valid and reliable" in q for q in quotes))
            self.assertTrue(all(q["quote_quality_score"] >= 70 for q in bundle["quote_bank"]))
            self.assertIn("low_confidence_quote_candidates", bundle)

    def test_phase_3y_real_bad_quotes_are_not_primary_evidence(self) -> None:
        bad_fragments = [
            "Certain commercial entities, equipment, or materials may be identified in this document in order to describe",
            "monitoring, will help ensure that AI systems function as intended, are",
            "the development or use of the model causes a ser ious incident, the general-pur pose AI model provid er should",
            "requirements agencies must follow.",
        ]
        good_quote = (
            "Agencies must maintain records of AI use, ensure human review for decisions that materially affect people, "
            "monitor implementation outcomes, and retain evidence of accountability, disclosure, and exception handling."
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "policy_like.txt"
            out = root / "out"
            path.write_text("\n\n".join(bad_fragments + [good_quote]), encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_text = "\n".join(q["exact_quote"] for q in low)
            for bad in bad_fragments:
                self.assertNotIn(bad, primary)
                self.assertIn(bad, low_text)
            self.assertTrue(all(q.get("low_confidence_reason") or q.get("quote_quality_reason") for q in low))
            self.assertIn("Agencies must maintain records of AI use", primary)


    def test_phase_3x_document_classification_and_sector_routing(self) -> None:
        eo_like = "Executive Order on Safe, Secure, and Trustworthy Artificial Intelligence. Federal agencies shall develop guidance, manage risks, protect privacy, and report implementation."
        eu_like = "Regulation laying down harmonised rules on artificial intelligence, high-risk AI systems, providers, deployers, conformity assessment, market surveillance."
        policy_like = "Policy for the responsible use of AI in government. Public servants must use AI responsibly, disclose AI use, ensure human review, manage risks, and maintain accountability records."
        dtac_like = "Digital Technology Assessment Criteria clinical safety DCB0129 clinical safety case hazard log patient care NHS data protection interoperability."

        self.assertNotEqual(runner.auto_sector(eo_like), "employment_hr_ai")
        eu_with_workers = eu_like + " The source also mentions employment, workers, labour, recruitment, and workplace rights."
        self.assertEqual(runner.auto_sector(eu_with_workers), "general_ai_governance")
        self.assertNotEqual(runner.auto_sector(eu_with_workers), "employment_hr_ai")
        self.assertIn(runner.auto_sector(policy_like), {"government_service_delivery", "general_ai_governance"})
        self.assertNotEqual(runner.auto_sector(policy_like), "employment_hr_ai")
        self.assertNotEqual(runner.auto_sector(policy_like), "procurement_vendor_governance")
        self.assertEqual(runner.auto_sector(dtac_like), "clinical_ai")

        self.assertEqual(assess("eo", "policy", eo_like, assessment_mode="external_framework", sector="auto")["document_type"], "executive_policy_directive")
        self.assertEqual(assess("eu", "policy", eu_with_workers, assessment_mode="external_framework", sector="auto")["document_type"], "binding_legal_instrument")
        self.assertEqual(assess("policy", "policy", policy_like, assessment_mode="external_framework", sector="auto")["document_type"], "public_sector_policy")
        self.assertEqual(assess("dtac", "policy", dtac_like, assessment_mode="external_framework", sector="auto")["document_type"], "sector_assurance_checklist")

        policy_result = assess("Australian Government AI Policy", "policy", policy_like, assessment_mode="external_framework", sector=runner.auto_sector(policy_like))
        policy_assessment = dict(policy_result)
        policy_assessment["sector_profile"] = runner.auto_sector(policy_like)
        policy_quotes = [{"quote_id": "Q001"}]
        policy_gaps = runner.build_governance_gap_register(policy_assessment, policy_quotes)
        policy_controls = runner.build_control_recommendations(policy_gaps, [], policy_quotes)
        self.assertTrue(any(c["control_name"] in {"Public Sector AI Use Register", "Human Review and Accountability Evidence Log"} for c in policy_controls))
        self.assertIn("public-sector operating policy", runner.executive_thesis(policy_assessment, policy_gaps, policy_controls))

        eu_result = assess("EU AI Act", "policy", eu_with_workers, assessment_mode="external_framework", sector=runner.auto_sector(eu_with_workers))
        eu_gaps = runner.build_governance_gap_register(eu_result, [{"quote_id": "Q001"}])
        eu_controls = runner.build_control_recommendations(eu_gaps, [], [{"quote_id": "Q001"}])
        self.assertTrue(any(c["control_name"] in {"Provider/Deployer Obligation Mapping Register", "High-Risk AI Evidence and Technical Documentation Gate"} for c in eu_controls))
        self.assertIn("high-force legal source", runner.executive_thesis(eu_result, eu_gaps, eu_controls))

    def test_phase_3x_executive_finding_and_document_specific_controls(self) -> None:
        nist_text = "AI Risk Management Framework voluntary non-sector-specific use-case agnostic govern map measure manage trustworthy AI. Organizations should document risks, assign accountability, monitor AI systems, review outcomes, manage incidents, and maintain evidence of risk management activities."
        dtac_text = "Digital Technology Assessment Criteria clinical safety DCB0129 clinical safety case hazard log patient care NHS data protection interoperability. Clinical teams must document safety cases, maintain hazard logs, review incidents, and ensure evidence supports deployment decisions."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            nist = root / "nist.txt"
            dtac = root / "dtac.txt"
            nist_out = root / "nist_out"
            dtac_out = root / "dtac_out"
            nist.write_text(nist_text, encoding="utf-8")
            dtac.write_text(dtac_text, encoding="utf-8")
            self.run_cli([str(nist), "--output-dir", str(nist_out), "--mode", "external_framework", "--sector", "auto"])
            self.run_cli([str(dtac), "--output-dir", str(dtac_out), "--mode", "external_framework", "--sector", "auto"])
            nist_report = next(nist_out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn("valuable as a governance design framework", nist_report)
            self.assertIn("Classified as `voluntary_risk_framework`", nist_report)
            self.assertNotIn("This document is assessed as an external governance source", nist_report)
            nist_controls = json.loads((nist_out / "analyst" / "control_recommendations.json").read_text(encoding="utf-8"))["control_recommendations"]
            dtac_controls = json.loads((dtac_out / "analyst" / "control_recommendations.json").read_text(encoding="utf-8"))["control_recommendations"]
            self.assertTrue(any("AI Risk Management Implementation Register" == c["control_name"] for c in nist_controls))
            self.assertTrue(any("Clinical Safety" in c["control_name"] or "DTAC" in c["control_name"] for c in dtac_controls))

    def test_relative_input_from_different_cwd_preserves_original_and_resolves_identity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            work = root / "work"
            docs = work / "docs"
            out = work / "out"
            docs.mkdir(parents=True)
            input_file = docs / "Relative Path Policy.txt"
            input_file.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts/laif_process_document.py"),
                    "docs/Relative Path Policy.txt",
                    "--output-dir",
                    "out",
                ],
                cwd=work,
                text=True,
                capture_output=True,
                check=True,
            )

            json_path = next(out.glob("*.laif.json"))
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            processing = payload["processing_metadata"]
            extraction = payload["extraction_metadata"]
            expected_hash = hashlib.sha256(input_file.read_bytes()).hexdigest()

            self.assertEqual(processing["input_path_original"], "docs/Relative Path Policy.txt")
            self.assertEqual(extraction["input_path_original"], "docs/Relative Path Policy.txt")
            self.assertTrue(Path(processing["input_path"]).is_absolute())
            self.assertTrue(Path(extraction["input_path"]).is_absolute())
            self.assertEqual(Path(processing["input_path"]).resolve(), input_file.resolve())
            self.assertEqual(Path(extraction["input_path"]).resolve(), input_file.resolve())
            self.assertEqual(processing["source_sha256"], expected_hash)
            self.assertEqual(extraction["source_sha256"], expected_hash)

            markdown = next(out.glob("*.laif.md")).read_text(encoding="utf-8")
            self.assertIn("Original input path", markdown)
            self.assertIn("docs/Relative Path Policy.txt", markdown)
            self.assertIn("Resolved input path", markdown)
            self.assertIn(str(input_file.resolve()), markdown)
            self.assertIn("Original file name", markdown)
            self.assertIn("Relative Path Policy.txt", markdown)
            self.assertIn("Source SHA-256", markdown)
            self.assertIn(expected_hash, markdown)

            index_path = out / "laif_processing_index.jsonl"
            lines = [json.loads(line) for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0]["input_path_original"], "docs/Relative Path Policy.txt")
            self.assertTrue(Path(lines[0]["input_path"]).is_absolute())
            self.assertEqual(Path(lines[0]["input_path"]).resolve(), input_file.resolve())
            self.assertEqual(lines[0]["source_sha256"], expected_hash)

    def test_markdown_metadata_has_original_name_hash_and_processed_at(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "Policy Sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            markdown = next(out.glob("*.laif.md")).read_text(encoding="utf-8")
            self.assertIn("Original file name", markdown)
            self.assertIn("Policy Sample.txt", markdown)
            self.assertIn("Source SHA-256", markdown)
            self.assertIn("processed_at_utc", markdown)

    def test_index_appends_and_preserves_original_names_for_two_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "out"
            first = root / "NIST AI RMF 1.0 sample.txt"
            second = root / "Department Policy Sample.txt"
            first.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            second.write_text(STRONG_EXTERNAL_TEXT + " departmental software development release pipeline", encoding="utf-8")
            self.run_cli([str(first), "--output-dir", str(out)])
            self.run_cli([str(second), "--output-dir", str(out)])
            lines = [json.loads(line) for line in (out / "laif_processing_index.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(lines), 2)
            self.assertEqual({line["original_file_name"] for line in lines}, {first.name, second.name})
            for line in lines:
                self.assertTrue(line["markdown_output_path"].endswith(".laif.md"))
                self.assertTrue(line["json_output_path"].endswith(".laif.json"))
                self.assertIsInstance(line["evidence_trace_count"], int)
                self.assertIsInstance(line["remediation_patch_count"], int)

    def test_output_names_are_safe_stem_based_metadata_preserves_original_names(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "NIST AI RMF 1.0 sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
            json_path = next(out.glob("*.laif.json"))
            self.assertEqual(json_path.name, "NIST-AI-RMF-1.0-sample.laif.json")
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["processing_metadata"]["original_file_name"], path.name)
            self.assertEqual(payload["processing_metadata"]["safe_output_stem"], "NIST-AI-RMF-1.0-sample")

    def test_default_mode_external_framework(self) -> None:
        parser = runner.build_parser()
        args = parser.parse_args(["input.txt"])
        self.assertEqual(args.mode, "external_framework")

    def test_formal_laif_native_failure_remains_fail_for_external_strong_signal_doc(self) -> None:
        result = assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")
        self.assertEqual(result["assessment_mode"], "external_framework")
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")

    def test_external_framework_report_reframed_as_governance_repair(self) -> None:
        result = assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")
        report = generate_markdown_report([result])
        front = report.split("Technical Appendix", 1)[0]
        self.assertIn("LAIF Governance Repair Assessment", report)
        self.assertIn("Governance Repair Profile", report)
        self.assertIn("Operational Closure Findings", report)
        self.assertIn("Evidence Sufficiency Findings", report)
        self.assertIn("Failure-Pathway Risk Findings", report)
        self.assertIn("document_type", report)
        self.assertIn("recommended_use", report)
        self.assertIn("not_sufficient_for", report)
        self.assertIn("systemic_repair_value", result)
        self.assertIn("failure_pathway_risk", result)
        self.assertNotIn("Formal LAIF-native compliance: FAIL", front)
        self.assertNotIn("LAIF-native certification: Not claimed / not applicable", front)
        self.assertIn("Technical Appendix", report)
        self.assertIn("Internal Diagnostic Boundary", report)
        self.assertIn("LAIF-native certification: Not claimed / not applicable to this external-framework assessment.", report)

    def test_laif_native_mode_preserves_formal_certification_behavior(self) -> None:
        result = assess("laif native fixture", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="laif_native_certification")
        report = generate_markdown_report([result])
        self.assertEqual(result["assessment_mode"], "laif_native_certification")
        self.assertEqual(result["formal_laif_native_compliance"], "FAIL")
        self.assertIn("LAIF-native certification: FAIL / canonical remediation required", report)

    def test_document_type_classification_examples(self) -> None:
        cases = [
            ("Regulation laying down harmonised rules on artificial intelligence high-risk AI systems providers deployers conformity assessment market surveillance.", "binding_legal_instrument"),
            ("Executive Order 14110 directs federal agencies and the Secretary of Commerce to manage safe secure trustworthy artificial intelligence.", "executive_policy_directive"),
            ("Artificial Intelligence Risk Management Framework voluntary framework govern, map, measure, and manage AI risks non-sector-specific use-case agnostic.", "voluntary_risk_framework"),
            ("DTAC Digital Technology Assessment Criteria clinical safety case DCB0129 hazard log patient care NHS.", "sector_assurance_checklist"),
        ]
        for text, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(assess(expected, "policy", text, assessment_mode="external_framework")["document_type"], expected)

    def test_malformed_pdf_fragments_are_not_primary_paraphrase_findings(self) -> None:
        text = "his Regulation, without there being scope... al law that may give effect..."
        result = assess("malformed", "pdf", text, assessment_mode="external_framework")
        self.assertEqual(result["paraphrase_violations"], {})
        report = generate_markdown_report([result])
        self.assertNotIn("Paraphrase violation", report)
        self.assertNotIn("Forbidden paraphrase", report)

    def test_exact_evidence_traces_satisfy_matched_text_slice(self) -> None:
        result = assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")
        exact_traces = [t for t in result["evidence_traces"] if t.get("matched_text")]
        self.assertTrue(exact_traces)
        for trace in exact_traces:
            self.assertEqual(trace["matched_text"], STRONG_EXTERNAL_TEXT[trace["start_char"]:trace["end_char"]])

    def test_generated_report_unsafe_phrase_absence(self) -> None:
        report = generate_markdown_report([assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")])
        for phrase in ("Final verdict", "Primary Failure Modes", "This document fails formal LAIF v1.2 compliance"):
            self.assertNotIn(phrase, report)

    def test_raw_regex_absence(self) -> None:
        report = generate_markdown_report([assess("external", "policy", STRONG_EXTERNAL_TEXT, assessment_mode="external_framework")])
        for token in (r"\b", "(?:", "(?=", "(?!"):
            self.assertNotIn(token, report)

    def test_no_writes_under_reports(self) -> None:
        before = {p.name: p.stat().st_mtime_ns for p in (REPO_ROOT / "reports").glob("*")}
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "sample.txt"
            out = root / "out"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out)])
        after = {p.name: p.stat().st_mtime_ns for p in (REPO_ROOT / "reports").glob("*")}
        self.assertEqual(before, after)

    def test_source_sha256_matches_input_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.txt"
            path.write_text(STRONG_EXTERNAL_TEXT, encoding="utf-8")
            self.assertEqual(runner.sha256_file(path), hashlib.sha256(path.read_bytes()).hexdigest())


    def test_phase_3z_document_type_precedence_expected_classifications(self) -> None:
        samples = {
            "nist": (
                "Artificial Intelligence Risk Management Framework. This voluntary framework helps organizations govern, map, measure, and manage AI risks. It is non-sector-specific and use-case agnostic.",
                "voluntary_risk_framework",
                {"general_ai_governance"},
            ),
            "eu": (
                "Regulation laying down harmonised rules on artificial intelligence. The Artificial Intelligence Act sets obligations for providers and deployers of high-risk AI systems, conformity assessment, technical documentation, post-market monitoring, market surveillance, general-purpose AI model duties, and serious incident reporting. It also mentions employment and workers.",
                "binding_legal_instrument",
                {"general_ai_governance"},
            ),
            "eo": (
                "Executive Order on Safe, Secure, and Trustworthy Artificial Intelligence. Federal agencies shall develop guidance, manage risks, protect privacy, report implementation, and assign responsibilities to Secretaries and agency heads.",
                "executive_policy_directive",
                {"government_service_delivery", "general_ai_governance"},
            ),
            "dtac": (
                "Digital Technology Assessment Criteria. Clinical safety DCB0129, clinical safety case, hazard log, Clinical Safety Officer, patient care, NHS data protection, technical security, and interoperability.",
                "sector_assurance_checklist",
                {"clinical_ai"},
            ),
            "policy": (
                "Policy for the responsible use of AI in government. Government agencies and public servants must disclose AI use, ensure human review, maintain AI use registers, monitor implementation, retain accountability records, and manage exceptions and incidents.",
                "public_sector_policy",
                {"government_service_delivery", "general_ai_governance"},
            ),
        }
        for name, (text, expected_type, expected_sectors) in samples.items():
            with self.subTest(name=name):
                result = assess(name, "policy", text, assessment_mode="external_framework", sector="auto")
                self.assertEqual(result["document_type"], expected_type)
                self.assertIn(runner.auto_sector(text), expected_sectors)
                self.assertIn(result["sector_profile"], expected_sectors)
        self.assertNotEqual(assess("eu", "policy", samples["eu"][0], assessment_mode="external_framework", sector="auto")["document_type"], "public_sector_policy")
        self.assertNotEqual(runner.auto_sector(samples["eu"][0]), "employment_hr_ai")
        self.assertNotEqual(runner.auto_sector(samples["eo"][0]), "employment_hr_ai")
        self.assertNotEqual(runner.auto_sector(samples["policy"][0]), "procurement_vendor_governance")
        self.assertNotEqual(runner.auto_sector(samples["policy"][0]), "employment_hr_ai")

    def test_phase_3z_public_sector_policy_does_not_override_stronger_identities(self) -> None:
        public_terms = " Government agencies must disclose AI use, ensure human review, and maintain an AI use register."
        stronger = {
            "eu": ("Regulation laying down harmonised rules on artificial intelligence. The Artificial Intelligence Act sets obligations for providers and deployers, conformity assessment, market surveillance." + public_terms, "binding_legal_instrument"),
            "eo": ("Executive Order on Safe, Secure, and Trustworthy Artificial Intelligence. Federal agencies shall report implementation to Secretaries and agency heads." + public_terms, "executive_policy_directive"),
            "nist": ("Artificial Intelligence Risk Management Framework. This voluntary framework helps organizations govern, map, measure, and manage AI risks. It is non-sector-specific and use-case agnostic." + public_terms, "voluntary_risk_framework"),
            "dtac": ("Digital Technology Assessment Criteria. Clinical safety DCB0129, clinical safety case, hazard log, Clinical Safety Officer, patient care." + public_terms, "sector_assurance_checklist"),
        }
        for name, (text, expected) in stronger.items():
            with self.subTest(name=name):
                self.assertEqual(assess(name, "policy", text, assessment_mode="external_framework", sector="auto")["document_type"], expected)

    def test_phase_3z_bad_quote_fragments_are_only_low_confidence_candidates(self) -> None:
        bad_fragments = [
            "To combat this risk, the Federal Government will ensure that the collection,",
            "The assessment must be documented and take",
            "The notification shall contain the conclusions of the assessment of the quality management syste m and the reasoned",
            "AI-g enerated cont ent has undergone",
            "Certain commercial entities, equipment, or materials may be identified in this document in order to describe",
            "monitoring, will help ensure that AI systems function as intended, are",
            "the development or use of the model causes a ser ious incident, the general-pur pose AI model provid er should",
            "requirements agencies must follow.",
        ]
        good_quote = (
            "Government agencies must maintain records of AI use, ensure human review for decisions that materially affect people, "
            "monitor implementation outcomes, and retain evidence of accountability, disclosure, exception handling, and incident response."
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "quality.txt"
            out = root / "out"
            path.write_text("\n\n".join(bad_fragments + [good_quote]), encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_text = "\n".join(q["exact_quote"] for q in low)
            for bad in bad_fragments:
                self.assertNotIn(bad, primary)
                self.assertIn(bad, low_text)
            self.assertTrue(all(q.get("low_confidence_reason") or q.get("quote_quality_reason") for q in low))
            self.assertIn("Government agencies must maintain records of AI use", primary)


    def test_phase_3z1_real_filename_identity_classifications(self) -> None:
        cases = {
            "2023-24283.pdf": (
                "Executive Order on Safe, Secure, and Trustworthy Artificial Intelligence. Federal agencies shall develop guidance, manage risks, protect privacy, report implementation, and assign responsibilities to Secretaries and agency heads.",
                "executive_policy_directive",
                {"government_service_delivery", "general_ai_governance"},
            ),
            "DTAC_Form_2.0_February_2026.docx": (
                "Digital Technology Assessment Criteria. Clinical safety DCB0129, clinical safety case, hazard log, Clinical Safety Officer, patient care, NHS data protection, technical security, and interoperability.",
                "sector_assurance_checklist",
                {"clinical_ai"},
            ),
            "NIST.AI.100-1.docx": (
                "Artificial Intelligence Risk Management Framework. This voluntary framework helps organizations govern, map, measure, and manage AI risks. It is non-sector-specific and use-case agnostic.",
                "voluntary_risk_framework",
                {"general_ai_governance"},
            ),
            "OJ_L_202401689_EN_TXT.pdf": (
                "Regulation laying down harmonised rules on artificial intelligence. The Artificial Intelligence Act sets obligations for providers and deployers of high-risk AI systems, conformity assessment, technical documentation, post-market monitoring, market surveillance, general-purpose AI model duties, and serious incident reporting. It also mentions employment and workers.",
                "binding_legal_instrument",
                {"general_ai_governance"},
            ),
            "Policy for the responsible use of AI in Government 2.0_0.pdf": (
                "Policy for the responsible use of AI in government. Government agencies and public servants must disclose AI use, ensure human review, maintain AI use registers, monitor implementation, retain accountability records, and manage exceptions and incidents.",
                "public_sector_policy",
                {"government_service_delivery", "general_ai_governance"},
            ),
        }
        for filename, (text, expected_type, expected_sectors) in cases.items():
            with self.subTest(filename=filename):
                result = assess(filename, "uploaded_document", text, assessment_mode="external_framework", sector="auto", original_file_name=filename)
                self.assertEqual(result["document_type"], expected_type)
                self.assertIn(result["sector_profile"], expected_sectors)
                if filename.startswith("OJ_L"):
                    self.assertNotEqual(result["sector_profile"], "employment_hr_ai")
                    self.assertNotEqual(result["sector_profile"], "clinical_ai")
                if expected_type != "public_sector_policy":
                    self.assertNotEqual(result["document_type"], "public_sector_policy")

    def test_phase_3z1_public_sector_policy_generic_terms_do_not_overreach(self) -> None:
        generic_fragments = [
            "federal agencies shall report implementation",
            "government assessment requirements",
            "human review required",
            "requirements agencies must follow",
            "public sector guidance",
        ]
        for fragment in generic_fragments:
            with self.subTest(fragment=fragment):
                result = assess("generic", "policy", fragment, assessment_mode="external_framework", sector="auto")
                self.assertNotEqual(result["document_type"], "public_sector_policy")

    def test_phase_3z1_real_artifact_quote_fragments_and_good_quotes(self) -> None:
        bad_fragments = [
            "To combat this risk, the Federal Government will ensure that the collection,",
            "The assessment must be documented and take",
            "The notification shall contain the conclusions of the assessment of the quality management syste m and the reasoned",
            "AI-g enerated cont ent has undergone",
            "When implementing the r isk management system as provid ed",
            "Regulation, or is f alsifi ed, or accompanie d by f alsifi ed documentation",
            "Uni on har monisation legislation listed in Section A of Annex I apply , provid ers shall be responsible f or ensur ing",
            "Certain commercial entities, equipment, or materials may be identified in this document in order to describe",
            "monitoring, will help ensure that AI systems function as intended, are",
            "the development or use of the model causes a ser ious incident, the general-pur pose AI model provid er should",
            "requirements agencies must follow.",
        ]
        good_quotes = [
            "Government agencies must maintain records of AI use, ensure human review for decisions that materially affect people, monitor implementation outcomes, and retain evidence of accountability, disclosure, exception handling, and incident response.",
            "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system.",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "quote_quality.txt"
            out = root / "out"
            path.write_text("\n\n".join(bad_fragments + good_quotes), encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_text = "\n".join(q["exact_quote"] for q in low)
            for bad in bad_fragments:
                self.assertNotIn(bad, primary)
                self.assertIn(bad, low_text)
            for good in good_quotes:
                self.assertIn(good, primary)
            self.assertTrue(all(q.get("low_confidence_reason") or q.get("quote_quality_reason") for q in low))


    def test_phase_3z2_display_quote_trace_and_repair(self) -> None:
        damaged = "Super vision, inv estig ation, enf or cement and monitor ing in respect of providers of general-purpose AI models shall be carried out by the competent authority."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text(damaged, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            quote = bundle["quote_bank"][0]
            self.assertIn("Super vision, inv estig ation", quote["exact_quote"])
            self.assertIn(quote["exact_quote"], path.read_text(encoding="utf-8"))
            self.assertIn("Supervision, investigation, enforcement and monitoring", quote["display_quote"])
            self.assertTrue(quote["quote_display_normalized"])
            self.assertTrue(quote["raw_exact_quote_retained"])
            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn("Supervision, investigation, enforcement and monitoring", report)
            self.assertNotIn("Super vision, inv estig ation", report)
            prompt = (out / "analyst" / "AI_ANALYST_PROMPT.md").read_text(encoding="utf-8")
            self.assertIn("Use `display_quote` for prose", prompt)
            self.assertIn("Preserve `exact_quote`", prompt)

    def test_phase_3z2_eu_damaged_legal_quote_display_accepted(self) -> None:
        damaged = "The obliga tion set out in this Ar ticle shall not apply to providers of general-purpose AI models that are released under a free and open-source licence."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text(damaged, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_exact = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            primary_display = "\n".join(q["display_quote"] for q in bundle["quote_bank"])
            self.assertIn("The obliga tion set out in this Ar ticle", primary_exact)
            self.assertIn("The obligation set out in this Article shall not apply", primary_display)

    def test_phase_3z2_incomplete_nist_quote_downgraded_and_complete_quote_accepted(self) -> None:
        bad = "After completing the MANAGE function, plans for prioritizing risk and regular monitoring"
        good = "After completing the MANAGE function, plans for prioritizing risk and regular monitoring are documented, reviewed periodically, and assigned to organizational roles."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "NIST.AI.100-1.docx"
            out = root / "out"
            path.write_text("\n\n".join([bad, good]), encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_exact = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            primary_display = "\n".join(q["display_quote"] for q in bundle["quote_bank"])
            low_text = "\n".join(q["exact_quote"] for q in bundle.get("low_confidence_quote_candidates", []))
            self.assertNotIn(bad + "\n\n", primary_exact)
            self.assertIn(bad, low_text)
            self.assertIn("incomplete quote could not be expanded", "\n".join(q.get("low_confidence_reason", "") for q in bundle.get("low_confidence_quote_candidates", [])))
            self.assertIn("plans for prioritizing risk and regular monitoring are documented", primary_display)
            complete = next(q for q in bundle["quote_bank"] if "are documented" in q["exact_quote"])
            self.assertEqual(complete["display_quote"], complete["exact_quote"])
            self.assertFalse(complete["quote_display_normalized"])

    def test_phase_3z2_damaged_fragments_remain_low_confidence(self) -> None:
        fragments = [
            "AI-g enerated cont ent has undergone",
            "When implementing the r isk management system as provid ed",
            "Uni on har monisation legislation listed in Section A of Annex I apply , provid ers shall be responsible f or ensur ing",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join(fragments), encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_text = "\n".join(q["exact_quote"] for q in low)
            for fragment in fragments:
                self.assertNotIn(fragment, primary)
                self.assertIn(fragment, low_text)
            reasons = "\n".join(q.get("low_confidence_reason", "") for q in low)
            self.assertTrue("extraction-damaged spacing could not be safely normalised" in reasons or "incomplete quote could not be expanded" in reasons)

    def test_phase_3z2_ai_input_bundle_and_quote_bank_markdown_include_display_trace(self) -> None:
        damaged = "Super vision, inv estig ation, enf or cement and monitor ing in respect of providers of general-purpose AI models shall be carried out by the competent authority."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text(damaged, encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            ai_bundle = json.loads((out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            self.assertIn("exact_quote", ai_bundle["quote_bank"][0])
            self.assertIn("display_quote", ai_bundle["quote_bank"][0])
            quote_bank_md = (out / "analyst" / "quote_bank.md").read_text(encoding="utf-8")
            self.assertIn("Display quote", quote_bank_md)
            self.assertIn("Raw exact quote", quote_bank_md)

    def test_phase_3z3_display_quote_repairs_and_incomplete_quote_handling(self) -> None:
        damaged = "Providers must ensure that users have appropriate exper ience with AI syste ms regard ing placing on the marke t and supervision by the comp et ent author ity."
        bad_incident = "This policy requires agencies to provide a way to manage AI incidents through"
        bad_training = "Agencies must implement mandatory training for all staff on responsible AI use within"
        good_incident = "This policy requires agencies to provide a way to manage AI incidents through documented escalation pathways, accountable owners, review thresholds, and evidence records."
        good_training = "Agencies must implement mandatory training for all staff on responsible AI use within defined onboarding, annual refresher, and role-specific assurance processes."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "Policy for the responsible use of AI in Government 2.0_0.pdf"
            out = root / "out"
            path.write_text("\n\n".join([damaged, bad_incident, bad_training, good_incident, good_training]), encoding="utf-8")
            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_exact = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            primary_display = "\n".join(q.get("display_quote", q["exact_quote"]) for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_exact = "\n".join(q["exact_quote"] for q in low)
            low_reasons = "\n".join(q.get("low_confidence_reason", "") for q in low)

            self.assertIn("exper ience", primary_exact)
            self.assertIn("AI syste ms", primary_exact)
            self.assertIn("comp et ent author ity", primary_exact)
            self.assertIn(
                "Providers must ensure that users have appropriate experience with AI systems regarding placing on the market and supervision by the competent authority.",
                primary_display,
            )
            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn("experience with AI systems", report)
            self.assertIn("competent authority", report)
            for damaged_fragment in ("exper ience", "syste ms", "regard ing", "marke t", "comp et ent author ity"):
                self.assertNotIn(damaged_fragment, report)

            self.assertNotIn(bad_incident + "\n\n", primary_exact)
            self.assertNotIn(bad_training + "\n\n", primary_exact)
            self.assertIn(bad_incident, low_exact)
            self.assertIn(bad_training, low_exact)
            self.assertIn("incomplete quote could not be expanded", low_reasons)
            self.assertIn(good_incident, primary_exact)
            self.assertIn(good_training, primary_exact)
            good_incident_quote = next(q for q in bundle["quote_bank"] if q["exact_quote"] == good_incident)
            good_training_quote = next(q for q in bundle["quote_bank"] if q["exact_quote"] == good_training)
            self.assertEqual(good_incident_quote["display_quote"], good_incident)
            self.assertEqual(good_training_quote["display_quote"], good_training)

    def test_phase_3z4_generic_quote_readability_gate(self) -> None:
        repairable = "T o that end, appropr iate human oversight measures should be identifie d by the pro vider of the system bef ore its placing on the market or putting into ser vice."
        unresolved = "The risk managem ent measures refer red to shall be suc h that unresolvedsplit dam age remains."
        clean = "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system."
        bad_through = "This policy requires agencies to provide a way to manage AI incidents through"
        bad_within = "Agencies must implement mandatory training for all staff on responsible AI use within"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join([repairable, unresolved, clean, bad_through, bad_within]), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_display = "\n".join(q.get("display_quote", q["exact_quote"]) for q in bundle["quote_bank"])
            primary_exact = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_exact = "\n".join(q.get("exact_quote", "") for q in low)
            low_reasons = "\n".join(q.get("low_confidence_reason", "") for q in low)
            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")

            self.assertIn("To that end, appropriate human oversight measures should be identified by the provider", primary_display)
            self.assertIn("T o that end", primary_exact)
            self.assertIn(clean, primary_display)
            self.assertNotIn("unresolvedsplit dam age", primary_display)
            self.assertIn(unresolved, low_exact)
            self.assertIn("display quote contains unresolved PDF split-word extraction damage", low_reasons)
            self.assertIn(bad_through, low_exact)
            self.assertIn(bad_within, low_exact)
            self.assertIn("incomplete quote could not be expanded", low_reasons)

            unresolved_candidate = next(q for q in low if q.get("exact_quote") == unresolved)
            self.assertIn("display_quote", unresolved_candidate)
            self.assertTrue(unresolved_candidate["raw_exact_quote_retained"])
            self.assertIn("quote_quality_reason", unresolved_candidate)

            self.assertIn("appropriate human oversight measures", report)
            self.assertIn("Providers of high-risk AI systems shall establish", primary_display)
            for damaged_fragment in (
                "T o",
                "appropr iate",
                "identifie d",
                "pro vider",
                "bef ore",
                "ser vice",
                "repor t",
                "managem ent",
                "refer red",
                "suc h",
            ):
                self.assertNotIn(damaged_fragment, primary_display)
                self.assertNotIn(damaged_fragment, report)

    def test_phase_3z5_final_primary_evidence_admission_gate(self) -> None:
        damaged_incident = "Providers of high-risk AI syste ms placed on the Union marke t shall repor t any serious incident to the competent authority."
        repairable_risk = "The risk managem ent measures refer red to shall be suc h that risks are mitigated."
        incomplete = "This policy requires agencies to provide a way to manage AI incidents through"
        clean = "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system."
        safely_repaired = "T o that end, appropr iate human oversight measures should be identifie d by the pro vider of the system bef ore its placing on the market or putting into ser vice."
        bad_fragments = (
            "syste ms",
            "marke t",
            "repor t",
            "managem ent",
            "refer red",
            "suc h",
            "T o",
            "appropr iate",
            "identifie d",
            "pro vider",
            "bef ore",
            "ser vice",
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join([damaged_incident, repairable_risk, incomplete, clean, safely_repaired]), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_display = "\n".join(q.get("display_quote", q["exact_quote"]) for q in bundle["quote_bank"])
            primary_exact = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_exact = "\n".join(q.get("exact_quote", "") for q in low)
            low_reasons = "\n".join(q.get("low_confidence_reason", "") for q in low)

            for fragment in bad_fragments:
                self.assertNotIn(fragment, primary_display)
            self.assertNotIn(damaged_incident, primary_exact)
            self.assertIn(damaged_incident, low_exact)
            self.assertIn(incomplete, low_exact)
            self.assertIn("final primary quote admission gate failed", low_reasons)
            self.assertIn("incomplete quote could not be expanded", low_reasons)

            self.assertIn(clean, primary_display)
            clean_quote = next(q for q in bundle["quote_bank"] if q.get("display_quote") == clean)
            self.assertEqual(clean_quote["display_quote"], clean_quote["exact_quote"])
            self.assertTrue(clean_quote["raw_exact_quote_retained"])

            repaired_quote = next(q for q in bundle["quote_bank"] if "appropriate human oversight measures should be identified by the provider" in q.get("display_quote", ""))
            self.assertIn("T o that end", repaired_quote["exact_quote"])
            self.assertNotIn("T o", repaired_quote["display_quote"])
            self.assertTrue(repaired_quote["raw_exact_quote_retained"])

            damaged_candidate = next(q for q in low if q.get("exact_quote") == damaged_incident)
            self.assertIn("exact_quote", damaged_candidate)
            self.assertIn("display_quote", damaged_candidate)
            self.assertTrue(damaged_candidate["raw_exact_quote_retained"])

            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            for fragment in bad_fragments:
                self.assertNotIn(fragment, report)
            self.assertIn("Providers of high-risk AI systems shall establish", report)
            self.assertIn("appropriate human oversight measures should be identified by the provider", report)

            quote_bank_md = (out / "analyst" / "quote_bank.md").read_text(encoding="utf-8")
            primary_display_lines = "\n".join(line for line in quote_bank_md.splitlines() if line.startswith("> "))
            for fragment in bad_fragments:
                self.assertNotIn(fragment, primary_display_lines)

            ai_bundle = json.loads((out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            ai_display = "\n".join(q.get("display_quote", q["exact_quote"]) for q in ai_bundle["quote_bank"])
            for fragment in bad_fragments:
                self.assertNotIn(fragment, ai_display)

    def test_phase_3z6_complete_evidence_proposition_gate(self) -> None:
        bad_fragments = [
            "In order to ensure that providers of high-risk AI systems can take into account the experience on the use of high-risk",
            "The risk management measures referred to in paragraph 2, point (d), shall be such that the relevant residual risk",
            "To above should dra w up documentation of the assessment before that system is placed on the market or put into",
            "This process should ensure that the provider",
        ]
        good_quotes = [
            "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system.",
            "The risk management measures referred to in paragraph 2, point (d), shall be such that the relevant residual risk associated with each hazard is judged acceptable.",
            "This process should ensure that the provider documents the assessment before the system is placed on the market or put into service.",
            "T o that end, appropr iate human oversight measures should be identifie d by the pro vider of the system bef ore its placing on the market or putting into ser vice.",
        ]
        expected_reason = "final primary quote admission gate failed: incomplete evidence proposition"

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join(bad_fragments + good_quotes), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_display_values = [q.get("display_quote", q["exact_quote"]) for q in bundle["quote_bank"]]
            primary_display = "\n".join(primary_display_values)
            primary_exact = "\n".join(q["exact_quote"] for q in bundle["quote_bank"])
            low = bundle.get("low_confidence_quote_candidates", [])
            low_exact = "\n".join(q.get("exact_quote", "") for q in low)
            low_reasons = "\n".join(q.get("low_confidence_reason", "") for q in low)

            for bad in bad_fragments:
                self.assertNotIn(bad, primary_display_values)
                self.assertIn(bad, low_exact)
            self.assertIn(expected_reason, low_reasons)

            self.assertIn("Providers of high-risk AI systems shall establish", primary_display)
            self.assertIn("residual risk associated with each hazard is judged acceptable", primary_display)
            self.assertIn("provider documents the assessment before the system is placed on the market or put into service", primary_display)
            self.assertIn("appropriate human oversight measures should be identified by the provider", primary_display)
            self.assertIn("T o that end", primary_exact)

            repaired_quote = next(q for q in bundle["quote_bank"] if "appropriate human oversight measures should be identified by the provider" in q.get("display_quote", ""))
            self.assertNotIn("T o", repaired_quote["display_quote"])
            self.assertNotIn("appropr iate", repaired_quote["display_quote"])
            self.assertTrue(repaired_quote["raw_exact_quote_retained"])

            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            report_quote_lines = [line for line in report.splitlines() if line.startswith("- **Q")]
            for bad in bad_fragments:
                self.assertFalse(any(line.endswith(f"“{bad}”") for line in report_quote_lines))
            self.assertIn("Providers of high-risk AI systems shall establish", report)
            self.assertIn("appropriate human oversight measures should be identified by the provider", report)

            quote_bank_md = (out / "analyst" / "quote_bank.md").read_text(encoding="utf-8")
            primary_display_lines = [line[2:] for line in quote_bank_md.splitlines() if line.startswith("> ")]
            for bad in bad_fragments:
                self.assertNotIn(bad, primary_display_lines)

            ai_bundle = json.loads((out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            ai_display_values = [q.get("display_quote", q["exact_quote"]) for q in ai_bundle["quote_bank"]]
            for bad in bad_fragments:
                self.assertNotIn(bad, ai_display_values)

    def test_phase_3z6_institutional_report_warns_when_no_complete_primary_quotes_remain(self) -> None:
        bad_fragments = [
            "This process should ensure that the provider",
            "To above should dra w up documentation of the assessment before that system is placed on the market or put into",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join(bad_fragments), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            self.assertEqual(bundle["quote_bank"], [])
            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn(
                "No high-confidence complete primary quotes are presented because source text extraction quality is limited or poor. Evidence-bearing extracted passages are retained below as source-verification-required evidence and in the analyst bundle.",
                report,
            )
            self.assertIn("## Extracted evidence requiring source verification", report)
            self.assertIn("No extraction-impaired governance evidence required source-verification tiering", report)
            low_reasons = "\n".join(q.get("low_confidence_reason", "") for q in bundle.get("low_confidence_quote_candidates", []))
            self.assertIn("final primary quote admission gate failed: incomplete evidence proposition", low_reasons)

    def test_phase_3z5_validator_blocks_high_scoring_damaged_display_quote(self) -> None:
        record = {
            "exact_quote": "Providers of high-risk AI syste ms placed on the Union marke t shall repor t any serious incident to the competent authority.",
            "display_quote": "Providers of high-risk AI syste ms placed on the Union marke t shall repor t any serious incident to the competent authority.",
            "quote_display_normalized": False,
            "quote_display_normalization_reason": "",
            "raw_exact_quote_retained": True,
            "quote_quality_score": 95,
            "quote_quality_reason": "primary evidence: complete governance action with actor/control context",
            "low_confidence_reason": "",
        }
        ok, reason = runner.validate_primary_quote_record(record)
        self.assertFalse(ok)
        self.assertIn("final primary quote admission gate failed", reason)
        self.assertIn("display quote contains unresolved PDF split-word extraction damage", reason)

    def test_phase_3z4_unresolved_split_word_detector_allows_clean_governance_terms(self) -> None:
        clean = "AI, EU, US, UK, ISO and NIST guidance under the Act and Article provisions refers to risk management for providers."
        damaged = "Providers shall repor t incidents and maintain dam age records for oversight."
        self.assertEqual(runner.unresolved_split_word_damage(clean), (False, ""))
        self.assertEqual(
            runner.unresolved_split_word_damage(damaged),
            (True, "display quote contains unresolved PDF split-word extraction damage"),
        )

    def test_phase_3z1_real_artifact_profile_smoke(self) -> None:
        cases = {
            "2023-24283.pdf": ("Executive Order on Safe, Secure, and Trustworthy Artificial Intelligence. Federal agencies shall develop guidance, manage risks, protect privacy, report implementation, and assign responsibilities to Secretaries and agency heads.", "executive_policy_directive", {"government_service_delivery", "general_ai_governance"}),
            "DTAC_Form_2.0_February_2026.docx": ("Digital Technology Assessment Criteria. Clinical safety DCB0129, clinical safety case, hazard log, Clinical Safety Officer, patient care, NHS data protection, technical security, and interoperability.", "sector_assurance_checklist", {"clinical_ai"}),
            "NIST.AI.100-1.docx": ("Artificial Intelligence Risk Management Framework. This voluntary framework helps organizations govern, map, measure, and manage AI risks. It is non-sector-specific and use-case agnostic.", "voluntary_risk_framework", {"general_ai_governance"}),
            "OJ_L_202401689_EN_TXT.pdf": ("Regulation laying down harmonised rules on artificial intelligence. The Artificial Intelligence Act sets obligations for providers and deployers of high-risk AI systems, conformity assessment, technical documentation, post-market monitoring, market surveillance, general-purpose AI model duties, and serious incident reporting. It also mentions employment and workers.", "binding_legal_instrument", {"general_ai_governance"}),
            "Policy for the responsible use of AI in Government 2.0_0.pdf": ("Policy for the responsible use of AI in government. Government agencies and public servants must disclose AI use, ensure human review, maintain AI use registers, monitor implementation, retain accountability records, and manage exceptions and incidents.", "public_sector_policy", {"government_service_delivery", "general_ai_governance"}),
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for filename, (text, expected_type, expected_sectors) in cases.items():
                with self.subTest(filename=filename):
                    src = root / filename
                    src.write_text(text, encoding="utf-8")
                    out = root / ("out_" + filename.replace(" ", "_"))
                    self.run_cli([str(src), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])
                    bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
                    meta = bundle["document_metadata"]
                    self.assertEqual(meta["document_type"], expected_type)
                    self.assertIn(meta["sector_profile"], expected_sectors)

    def test_phase_3aa_evidence_tiering_mixed_source_behavior(self) -> None:
        clean_quote = "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system."
        damaged_relevant = "Providers shall ensure that AI systems intended to interac t directly with natural persons are designed and developed in"
        incomplete_relevant = "The risk management measures referred to in paragraph 2, point (d), shall be such that the relevant residual risk"
        boilerplate = "Certain commercial entities, equipment, or materials may be identified in this document in order to describe"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join([clean_quote, damaged_relevant, incomplete_relevant, boilerplate]), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_display = "\n".join(q.get("display_quote", q["exact_quote"]) for q in bundle["quote_bank"])
            verification = bundle.get("verification_required_extracted_evidence", [])
            verification_exact = "\n".join(q.get("exact_quote", "") for q in verification)
            low_exact = "\n".join(q.get("exact_quote", "") for q in bundle.get("low_confidence_quote_candidates", []))

            self.assertIn(clean_quote, primary_display)
            self.assertNotIn(damaged_relevant, primary_display)
            self.assertNotIn(incomplete_relevant, primary_display)
            self.assertIn(damaged_relevant, verification_exact)
            self.assertNotIn(incomplete_relevant, verification_exact)
            self.assertIn(incomplete_relevant, low_exact)
            self.assertNotIn(boilerplate, verification_exact)
            self.assertTrue(boilerplate in low_exact or boilerplate not in verification_exact)
            self.assertTrue(all(q.get("evidence_status") == "source_verification_required" for q in verification))
            self.assertTrue(all(q.get("raw_exact_quote_retained") is True for q in verification))
            self.assertTrue(all(q.get("likely_governance_signal") for q in verification))
            self.assertTrue(all(q.get("reviewer_instruction") for q in verification))

            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn("## Key quoted evidence", report)
            self.assertIn(clean_quote, report)
            self.assertIn("## Extracted evidence requiring source verification", report)
            self.assertIn("Source verification required", report)
            self.assertIn(damaged_relevant, report)
            self.assertNotIn(incomplete_relevant, report)
            self.assertNotIn("Certain commercial entities", report)

            issue_reasons = "\n".join(q.get("extraction_issue_reason", "") for q in verification)
            self.assertIn("split-word extraction damage", issue_reasons)

    def test_phase_3aa_extraction_quality_profile_and_ai_bundle_policy(self) -> None:
        noisy = "Providers shall ensure that AI systems intended to interac t directly with natural persons are designed and developed in"
        clean = "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            noisy_path = root / "OJ_L_202401689_EN_TXT.pdf"
            clean_path = root / "clean_OJ_L_202401689_EN_TXT.pdf"
            noisy_out = root / "noisy_out"
            clean_out = root / "clean_out"
            noisy_path.write_text(noisy, encoding="utf-8")
            clean_path.write_text(clean, encoding="utf-8")

            self.run_cli([str(noisy_path), "--output-dir", str(noisy_out), "--mode", "external_framework", "--sector", "auto"])
            self.run_cli([str(clean_path), "--output-dir", str(clean_out), "--mode", "external_framework", "--sector", "auto"])

            noisy_bundle = json.loads((noisy_out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            noisy_profile = noisy_bundle.get("extraction_quality_profile") or {}
            self.assertIn(noisy_profile.get("extraction_quality_level"), {"limited", "poor"})
            self.assertTrue(noisy_profile.get("verification_required_evidence_present"))
            self.assertFalse(noisy_profile.get("primary_quote_eligible"))
            self.assertIn("cleaner text extraction", noisy_profile.get("recommended_user_action", ""))
            self.assertIn("verification_required_extracted_evidence", noisy_bundle)
            self.assertIn("quote_bank", noisy_bundle)
            self.assertIn("low_confidence_quote_candidates", noisy_bundle)

            clean_bundle = json.loads((clean_out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            clean_profile = clean_bundle.get("extraction_quality_profile") or {}
            self.assertIn(clean_profile.get("extraction_quality_level"), {"high", "moderate"})
            self.assertTrue(clean_profile.get("primary_quote_eligible"))
            self.assertEqual(clean_bundle.get("verification_required_extracted_evidence"), [])

            prompt = (noisy_out / "analyst" / "AI_ANALYST_PROMPT.md").read_text(encoding="utf-8")
            self.assertIn("primary_quote_evidence", prompt)
            self.assertIn("verification_required_extracted_evidence", prompt)
            self.assertIn("Do not present verification-required extracted text as a clean direct quotation", prompt)
            self.assertIn("Do not invent or silently repair source text", prompt)


    def test_phase_3aa1_poor_extraction_policy_overrides_primary_quote_count(self) -> None:
        bad_fragments = [
            "(155) In order to ensure that providers of high-risk AI systems can take into account the experience on the use of high-risk AI systems for impro ving their systems and the design and development process or can take any possible cor rective action in a timely manner, all providers should have a post-mark et monitoring system in place.",
            "(63) The fact that an AI system is classif ied as a high-risk AI system under this Regulation should not be inter preted as",
            "(65) The risk-management system should consist of a continuous, ite rative process that is planned and r un throughout",
            "Codes of practice should also be f ocused on specific risk assessment and mitiga tion measures.",
        ]
        superficially_valid_primary = "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system."
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join([*bad_fragments, superficially_valid_primary]), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            profile = bundle["extraction_quality_profile"]
            self.assertEqual(profile["extraction_quality_level"], "poor")
            self.assertGreater(profile["primary_quote_count"], 0)
            self.assertFalse(profile["primary_quote_eligible"])
            self.assertTrue(bundle.get("verification_required_extracted_evidence"))

            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn("## Key quoted evidence", report)
            self.assertIn("No high-confidence complete primary quotes are presented because source text extraction quality is limited or poor", report)
            self.assertIn("## Extracted evidence requiring source verification", report)
            key_section = report.split("## Key quoted evidence", 1)[1].split("## Extracted evidence requiring source verification", 1)[0]
            self.assertNotIn("- **Q", key_section)
            self.assertNotIn(superficially_valid_primary, key_section)

    def test_phase_3aa1_eu_damaged_fragments_not_rendered_as_key_quoted_evidence_when_poor(self) -> None:
        bad_fragments = [
            "(155) In order to ensure that providers of high-risk AI systems can take into account the experience on the use of high-risk AI systems for impro ving their systems and the design and development process or can take any possible cor rective action in a timely manner, all providers should have a post-mark et monitoring system in place.",
            "(63) The fact that an AI system is classif ied as a high-risk AI system under this Regulation should not be inter preted as",
            "(65) The risk-management system should consist of a continuous, ite rative process that is planned and r un throughout",
            "Codes of practice should also be f ocused on specific risk assessment and mitiga tion measures.",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text("\n\n".join(bad_fragments), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            key_section = report.split("## Key quoted evidence", 1)[1].split("## Extracted evidence requiring source verification", 1)[0]
            for damaged in ["impro ving", "cor rective", "post-mark et", "classif ied", "inter preted", "ite rative", "r un", "f ocused", "mitiga tion"]:
                self.assertNotIn(damaged, key_section)
            verification_section = report.split("## Extracted evidence requiring source verification", 1)[1]
            self.assertIn("impro ving", verification_section)
            self.assertNotIn("mitiga tion", key_section)

    def test_phase_3aa1_clean_source_still_renders_primary_quotes(self) -> None:
        clean_quotes = [
            "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system.",
            "Providers shall keep the technical documentation up to date and retain evidence necessary to demonstrate conformity with applicable requirements.",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "clean_governance.txt"
            out = root / "out"
            path.write_text("\n\n".join(clean_quotes), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            profile = bundle["extraction_quality_profile"]
            self.assertIn(profile["extraction_quality_level"], {"high", "moderate"})
            self.assertTrue(profile["primary_quote_eligible"])
            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            self.assertIn(clean_quotes[0], report)
            self.assertIn("technical documentation up to date", report)

    def test_phase_3aa1_mixed_moderate_renders_clean_primary_and_verification_required(self) -> None:
        clean_quotes = [
            "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system.",
            "Providers shall keep the technical documentation up to date and retain evidence necessary to demonstrate conformity with applicable requirements.",
        ]
        damaged_quote = "Providers shall ensure that AI systems intended to interac t directly with natural persons are designed and developed in"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "mixed_governance.txt"
            out = root / "out"
            path.write_text("\n\n".join([*clean_quotes, damaged_quote]), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            profile = bundle["extraction_quality_profile"]
            self.assertEqual(profile["extraction_quality_level"], "moderate")
            self.assertTrue(profile["primary_quote_eligible"])
            self.assertTrue(bundle.get("verification_required_extracted_evidence"))
            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            key_section = report.split("## Key quoted evidence", 1)[1].split("## Extracted evidence requiring source verification", 1)[0]
            verification_section = report.split("## Extracted evidence requiring source verification", 1)[1]
            self.assertIn(clean_quotes[0], key_section)
            self.assertIn("technical documentation up to date", key_section)
            self.assertIn(damaged_quote, verification_section)

    def test_phase_3aa1_ai_bundle_policy_when_primary_quote_ineligible(self) -> None:
        noisy = "Providers shall ensure that AI systems intended to interac t directly with natural persons are designed and developed in"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "OJ_L_202401689_EN_TXT.pdf"
            out = root / "out"
            path.write_text(noisy, encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            ai_bundle = json.loads((out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            profile = ai_bundle["extraction_quality_profile"]
            self.assertFalse(profile["primary_quote_eligible"])
            self.assertFalse(ai_bundle["primary_quote_eligible"])
            self.assertIn("quote_bank", ai_bundle)
            self.assertTrue(ai_bundle.get("verification_required_extracted_evidence"))
            self.assertIn("primary_quote_policy_note", ai_bundle)

            prompt = (out / "analyst" / "AI_ANALYST_PROMPT.md").read_text(encoding="utf-8")
            self.assertIn("extraction_quality_profile.primary_quote_eligible", prompt)
            self.assertIn("do not use `quote_bank` as clean primary evidence", prompt)
            self.assertIn("Do not present verification-required extracted text as a clean direct quotation", prompt)


    def test_phase_3aa2_evidence_relevance_and_quote_boundaries(self) -> None:
        weak_scrap = "This Regulation ensures the free moveme nt, cross-border , of"
        useful_damaged = "Providers shall ensure that AI systems intended to interac t directly with natural persons are designed and developed in"
        clean_primary = "Providers of high-risk AI systems shall establish, implement, document and maintain a risk management system throughout the lifecycle of the AI system."
        bad_primary = [
            "NIST will review the AI RMF and update it as appropriate; a review",
            "AI risk management efforts should consider that humans may assume that AI systems work",
            "AI risk management should be integrated and incorporated into broader enterprise",
            "Agencies must notify the DTA when they publish and make any changes to their AI",
            "The statement must be reviewed and updated annually or sooner, should the agency make",
        ]
        good_primary = [
            "NIST will review the AI RMF periodically and update it as appropriate.",
            "AI risk management efforts should consider that humans may assume that AI systems work as intended, even when system limitations require active monitoring and review.",
            "AI risk management should be integrated and incorporated into broader enterprise risk management processes.",
            "Agencies must notify the DTA when they publish and make any changes to their AI transparency statement.",
            "The statement must be reviewed and updated annually or sooner, should the agency make material changes to its AI use or governance arrangements.",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "mixed_quality.txt"
            out = root / "out"
            path.write_text("\n\n".join([weak_scrap, useful_damaged, clean_primary] + bad_primary + good_primary), encoding="utf-8")

            self.run_cli([str(path), "--output-dir", str(out), "--mode", "external_framework", "--sector", "auto"])

            bundle = json.loads((out / "analyst" / "analyst_bundle.json").read_text(encoding="utf-8"))
            primary_exact = [q.get("exact_quote", "") for q in bundle.get("quote_bank", [])]
            verification = bundle.get("verification_required_extracted_evidence", [])
            verification_exact = [q.get("exact_quote", "") for q in verification]
            low_exact = [q.get("exact_quote", "") for q in bundle.get("low_confidence_quote_candidates", [])]

            self.assertIn(clean_primary, primary_exact)
            self.assertNotIn(weak_scrap, primary_exact)
            self.assertNotIn(weak_scrap, verification_exact)
            self.assertIn(weak_scrap, low_exact)

            self.assertNotIn(useful_damaged, primary_exact)
            self.assertIn(useful_damaged, verification_exact)
            useful_record = next(q for q in verification if q.get("exact_quote") == useful_damaged)
            self.assertTrue(useful_record.get("likely_governance_signal"))
            self.assertTrue(useful_record.get("reviewer_instruction"))
            self.assertGreaterEqual(useful_record.get("verification_relevance_score", 0), 3)
            self.assertIn("actor or regulated party", useful_record.get("verification_relevance_reason", ""))

            for bad in bad_primary:
                self.assertNotIn(bad, primary_exact)
                self.assertNotIn(bad, verification_exact)
                self.assertIn(bad, low_exact)
            for good in good_primary:
                self.assertIn(good, primary_exact)

            report = next(out.glob("*.institutional_report.md")).read_text(encoding="utf-8")
            key_section = report.split("## Key quoted evidence", 1)[1].split("## Extracted evidence requiring source verification", 1)[0]
            verification_section = report.split("## Extracted evidence requiring source verification", 1)[1].split("## What the document controls well", 1)[0]
            self.assertIn(clean_primary, key_section)
            self.assertIn(useful_damaged, verification_section)
            self.assertNotIn(weak_scrap, report)
            for bad in bad_primary:
                self.assertNotIn(f"“{bad}”", key_section)
            for good in good_primary:
                self.assertIn(good, key_section)

            ai_bundle = json.loads((out / "analyst" / "AI_ANALYST_INPUT_BUNDLE.json").read_text(encoding="utf-8"))
            self.assertEqual([q.get("exact_quote", "") for q in ai_bundle.get("quote_bank", [])], primary_exact)
            self.assertEqual([q.get("exact_quote", "") for q in ai_bundle.get("verification_required_extracted_evidence", [])], verification_exact)
            self.assertIn("low_confidence_quote_candidates", ai_bundle)

            prompt = (out / "analyst" / "AI_ANALYST_PROMPT.md").read_text(encoding="utf-8")
            self.assertIn("clean quote-grade evidence", prompt)
            self.assertIn("reviewer-useful", prompt)
            self.assertIn("low-confidence trace only", prompt)

    def test_phase_3z_no_external_ai_api_network_patterns_added(self) -> None:
        haystack = "\n".join(
            path.read_text(encoding="utf-8")
            for root in (REPO_ROOT / "scripts", REPO_ROOT / "tests")
            for path in root.rglob("*.py")
        ) + (REPO_ROOT / "assessment_engine.py").read_text(encoding="utf-8")
        forbidden = ("op" + "enai", "anth" + "ropic", "gem" + "ini", "google" + ".generativeai", "requests" + ".post", "ht" + "tpx", "urllib" + ".request")
        self.assertFalse(any(token in haystack for token in forbidden))


if __name__ == "__main__":
    unittest.main()
