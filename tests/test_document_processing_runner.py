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

from assessment_engine import assess, classify_document_type, generate_markdown_report
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
        # Every control must be named for the gap it closes — a control name
        # that does not correspond to its own gap type is a reporting defect,
        # regardless of which instrument the document is.
        for gap, control in zip(eu_gaps, eu_controls):
            expected = runner._CONTROL_NAME_BY_PROFILE_AND_GAP.get(
                (runner.document_profile_key(eu_result), gap["gap_type"]))
            self.assertEqual(
                control["control_name"],
                expected or runner._CONTROL_NAME_BY_GAP[gap["gap_type"]],
                f"control name does not correspond to gap {gap['gap_type']}")
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
            # An identified instrument earns instrument-specific control naming
            # where its own vocabulary differs, and gap-derived naming otherwise.
            # In both cases the name must match the gap it closes.
            self.assertTrue(any("GOVERN/MAP" in c["control_name"] for c in nist_controls),
                            f"NIST control names: {[c['control_name'] for c in nist_controls]}")
            self.assertTrue(any("Clinical Safety" in c["control_name"] or "DTAC" in c["control_name"] for c in dtac_controls),
                            f"DTAC control names: {[c['control_name'] for c in dtac_controls]}")
            nist_gaps = json.loads((nist_out / "analyst" / "governance_gap_register.json").read_text(encoding="utf-8"))["gaps"]
            self.assertEqual(len(nist_controls), len(nist_gaps))
            for gap, control in zip(nist_gaps, nist_controls):
                self.assertIn(gap["gap_id"], control["linked_gap_ids"])
                self.assertEqual(control["risk_addressed"], gap["failure_mode"])
                self.assertEqual(control["required_artifact"], gap["control_artifact"])

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
        self.assertIn("AI Governance Structural Integrity Assessment", report)
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


    # ── Usability review 2026-09 regressions ─────────────────────────────
    TRUST_POLICY = (
        "# Northwood Hospital Trust — Artificial Intelligence Use Policy\n\n"
        "Version 0.3 (draft for Board approval)\n\n"
        "## 2. Principles\n\nAI tools must support, not replace, clinical "
        "judgement. Patient safety is our highest priority. Clinical staff "
        "remain responsible for decisions made with AI assistance.\n\n"
        "## 3. Approval of new tools\n\n3.3 Suppliers should provide evidence "
        "of regulatory approval where the tool is a medical device.\n\n"
        "## 4. Operation\n\nThe Trust will monitor AI tools in use and review "
        "performance annually. This policy applies to all staff and contractors."
    )
    VENDOR_STATEMENT = (
        "# Acme Analytics — Responsible AI Statement\n\nWe build AI systems "
        "that are fair, transparent, and accountable. Our AI Ethics Board "
        "oversees product decisions. We test models for bias. Customers receive "
        "model documentation describing intended use and known limitations."
    )

    def test_usability_executive_finding_varies_with_assessment(self) -> None:
        """A strong and a weak document must never share an executive finding."""
        strong = assess("strong", "policy", self.TRUST_POLICY + (
            " Every restriction names the person-level stake it protects; neither "
            "the restriction nor its paired protection may be weakened without the "
            "other. All three conditions must be satisfied simultaneously before "
            "deployment authorisation."), assessment_mode="external_framework")
        weak = assess("weak", "policy", self.VENDOR_STATEMENT,
                      assessment_mode="external_framework")
        s_gaps = runner.build_governance_gap_register(strong, [{"quote_id": "Q001"}])
        w_gaps = runner.build_governance_gap_register(weak, [{"quote_id": "Q001"}])
        s_ctrl = runner.build_control_recommendations(s_gaps, [], [{"quote_id": "Q001"}])
        w_ctrl = runner.build_control_recommendations(w_gaps, [], [{"quote_id": "Q001"}])
        s_thesis = runner.executive_thesis(strong, s_gaps, s_ctrl)
        w_thesis = runner.executive_thesis(weak, w_gaps, w_ctrl)
        self.assertNotEqual(s_thesis, w_thesis)
        # The finding must state the engine's own verdict, not a template.
        self.assertIn("Structural position:", s_thesis)
        self.assertIn("Structural position:", w_thesis)

    def test_usability_gaps_are_detected_not_asserted(self) -> None:
        """Gap registers differ by document and cite that document's evidence."""
        a = assess("a", "policy", self.TRUST_POLICY, assessment_mode="external_framework")
        b = assess("b", "policy", self.VENDOR_STATEMENT, assessment_mode="external_framework")
        ga = runner.build_governance_gap_register(a, [{"quote_id": "Q001"}])
        gb = runner.build_governance_gap_register(b, [{"quote_id": "Q001"}])
        self.assertNotEqual({g["gap_type"] for g in ga}, {g["gap_type"] for g in gb})
        # Every detected gap records why it fired.
        for gap in ga + gb:
            self.assertIn("detected_from", gap)
            self.assertTrue(gap["detected_from"].get("expectation_signal"))

    def test_usability_controls_are_gap_specific(self) -> None:
        """Control rows must not be interchangeable boilerplate."""
        a = assess("a", "policy", self.TRUST_POLICY, assessment_mode="external_framework")
        gaps = runner.build_governance_gap_register(a, [{"quote_id": "Q001"}])
        controls = runner.build_control_recommendations(gaps, [], [{"quote_id": "Q001"}])
        self.assertGreaterEqual(len(controls), 2)
        self.assertEqual(len({c["required_artifact"] for c in controls}), len(controls))
        self.assertEqual(len({c["owner"] for c in controls}), len(controls))

    def test_usability_internal_policy_not_classified_as_procurement(self) -> None:
        """An incidental mention of 'supplier' must not make a policy a procurement form."""
        self.assertEqual(classify_document_type(self.TRUST_POLICY), "internal_policy")

    def test_usability_corpus_naming_requires_instrument_identity(self) -> None:
        """Named-instrument vocabulary may only attach to that instrument."""
        from assessment_engine import known_instrument_profile
        self.assertEqual(known_instrument_profile(self.TRUST_POLICY, "trust.md", "policy"), "")
        self.assertEqual(
            known_instrument_profile("Digital Technology Assessment Criteria DTAC DCB0129",
                                     "dtac.md", "policy"), "dtac")

    def test_usability_sector_terms_match_whole_words(self) -> None:
        """'hr' inside 'through'/'thresholds' must not route to employment."""
        text = ("The system runs through documented thresholds and review "
                "thresholds throughout the lifecycle of the service.")
        self.assertNotEqual(runner.auto_sector(text), "employment_hr_ai")


# A document that carries the substance of every construct in institutional
# rather than LAIF vocabulary: named-interest coupling with a mutual
# non-weakening lock, an all-conditions deployment gate, an unconditional
# review right, quantified monitoring thresholds with escalation and
# suspension, self-application, and change control. Detection failures on this
# text are register bias, not genuine absence.
INSTITUTIONAL_STANDARD = """# Meridian Bank — Group AI Governance Standard (GS-114)

Owner: Chief Risk Officer. Approved by: Group Risk Committee. Review: annual.

## 1. Scope and binding effect
This Standard binds all Group entities. Non-compliance is a reportable control
breach under the Group Risk Framework.

## 2. Purpose of restrictions
Each control in this Standard exists to protect a named interest. The restriction
on automated credit decisioning without human review exists to protect the
applicant's interest in a decision they can understand and contest. Neither the
restriction nor the applicant's right of review may be removed without the other;
both require Group Risk Committee approval to amend.

## 3. Deployment gate
No model enters production unless all of the following hold simultaneously:
(a) the model owner can produce an explanation of any individual decision;
(b) documented objectives match implemented objectives, verified by Model
Validation independently of the build team;
(c) the model operates within its approved use boundary, and out-of-boundary
cases are routed to a human decision-maker.
Partial satisfaction is not approval.

## 4. Customer rights
Any customer subject to an automated decision may request human review within 30
days. Reviewers may overturn the decision. This right is not conditional.

## 5. Monitoring and thresholds
Model owners must monitor performance monthly. A drift breach above 5% or any
fairness metric outside tolerance must be escalated to the Model Risk Committee
within 5 working days, and use suspended if unresolved after 20 days.

## 6. Application to this function
Group Risk is itself subject to this Standard. The Group Risk Committee must
evidence its own compliance to Internal Audit annually.

## 7. Change control
Material change to a model, its data, or its purpose requires re-approval through
the deployment gate in section 3.
"""


class InstitutionalRegisterDetectionTests(unittest.TestCase):
    """Substance expressed in institutional vocabulary must be detected.

    Every assertion here corresponds to a structure that is demonstrably
    present in INSTITUTIONAL_STANDARD. A failure means the detector is keyed to
    a drafting register rather than to governance substance.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = assess("Meridian GS-114", "policy", INSTITUTIONAL_STANDARD,
                            assessment_mode="external_framework",
                            sector=runner.auto_sector(INSTITUTIONAL_STANDARD))

    def _fired(self, dimension: str) -> set:
        return {label for label, _ in self.result["score_breakdown"][dimension]["fired"]}

    def test_functional_alignment_detects_substance_in_own_vocabulary(self) -> None:
        fa = self.result["functional_alignment"]
        for construct in ("Coupling", "Integrity Layer", "Reversibility", "Self-Application"):
            self.assertEqual(
                fa[construct]["verdict"], "FUNCTIONAL",
                f"{construct} is expressed in this document; verdict was "
                f"{fa[construct]['verdict']} with families {fa[construct]['families']}")

    def test_named_roles_count_as_named_responsible_parties(self) -> None:
        """Chief Risk Officer, committees, model owners, Internal Audit are named parties."""
        self.assertIn("named responsible parties", self._fired("enforceability"))

    def test_quantified_breach_triggers_count_as_thresholds(self) -> None:
        """'above 5%', 'outside tolerance' state what counts as a problem."""
        self.assertIn("risk-proportionate thresholds", self._fired("enforceability"))

    def test_change_control_counts_as_lifecycle_scope(self) -> None:
        """Governing change after approval is lifecycle scope without the word."""
        self.assertIn("full lifecycle scope declared", self._fired("structural"))

    def test_must_carries_the_same_force_as_shall(self) -> None:
        self.assertIn("mandatory obligation language (shall/must)", self._fired("structural"))

    def test_human_review_counts_as_human_oversight(self) -> None:
        self.assertIn("human oversight", self._fired("conceptual"))

    def test_no_false_gaps_against_controls_the_document_states(self) -> None:
        """A control the document specifies must not be reported as missing."""
        gaps = runner.build_governance_gap_register(self.result, [{"quote_id": "Q001"}])
        titles = {g["gap_type"] for g in gaps}
        for false_positive in ("obligation_without_owner", "monitoring_without_threshold",
                               "lifecycle_without_change_control",
                               "insufficient_operative_content"):
            self.assertNotIn(false_positive, titles,
                             f"{false_positive} reported despite the document stating it")

    def test_empty_register_reads_as_a_finding_not_as_silence(self) -> None:
        gaps = runner.build_governance_gap_register(self.result, [{"quote_id": "Q001"}])
        report = runner.build_institutional_report(
            {"safe_output_stem": "x"}, {}, self.result, [{"quote_id": "Q001"}],
            gaps, runner.build_failure_pathways(gaps, []),
            runner.build_control_recommendations(gaps, [], []))
        self.assertIn("No unclosed expectation was detected", report)
        self.assertNotIn("| Control ID |", report)
        self.assertIn("not a certificate of implementation", report)

    def test_document_type_and_sector_route_to_institutional_profiles(self) -> None:
        self.assertEqual(classify_document_type(INSTITUTIONAL_STANDARD), "internal_policy")
        self.assertEqual(runner.auto_sector(INSTITUTIONAL_STANDARD), "financial_services_ai")

    def test_repeated_generic_phrase_is_one_signal_not_two(self) -> None:
        """_term_hits counts distinct terms, so one phrase cannot pass a 2-signal gate."""
        self.assertEqual(runner._term_hits("human review human review", ("human review", "dta")), 1)

    def test_procurement_instrument_form_outranks_sector_vocabulary(self) -> None:
        """A tender that buys a clinical system is still a tender."""
        tender = ("Invitation to Tender — AI-Assisted Triage System. Section C: Supplier "
                  "Assurance Questionnaire. Suppliers must supply a Clinical Safety Case "
                  "Report compliant with DCB0129 signed by a named Clinical Safety Officer "
                  "for NHS patient care.")
        self.assertEqual(classify_document_type(tender), "procurement_assessment_form")

    def test_control_names_correspond_to_their_own_gaps(self) -> None:
        tender = ("Invitation to Tender. Suppliers must supply evidence and shall notify "
                  "the Authority within 24 hours of any incident affecting patient safety. "
                  "Failure to notify constitutes a material breach and may result in "
                  "termination. The Authority reserves the right to audit supplier records.")
        result = assess("ITT", "policy", tender, assessment_mode="external_framework",
                        sector=runner.auto_sector(tender))
        gaps = runner.build_governance_gap_register(result, [{"quote_id": "Q001"}])
        controls = runner.build_control_recommendations(gaps, [], [{"quote_id": "Q001"}])
        self.assertEqual(len(gaps), len(controls))
        for gap, control in zip(gaps, controls):
            expected = runner._CONTROL_NAME_BY_PROFILE_AND_GAP.get(
                (runner.document_profile_key(result), gap["gap_type"]))
            self.assertEqual(control["control_name"],
                             expected or runner._CONTROL_NAME_BY_GAP[gap["gap_type"]])


# A policy expressing the same substance in academic register, used to check
# that register neutrality is not specific to one sector's vocabulary.
ACADEMIC_POLICY = """# University of Carrow — Policy on Automated Assessment Support

Approved by Academic Board. Owner: Pro-Vice-Chancellor (Education). Version 2.1.
Review: annual.

## 1. Purpose and scope
This policy applies to all use of automated tools that contribute to student
assessment, admissions, or progression decisions across all faculties.

## 2. Why these restrictions exist
Each restriction below protects a specific student interest. The prohibition on
automated final grading exists to protect the student's interest in an academic
judgement made by a qualified academic. That prohibition and that interest may
not be varied independently; either change requires Academic Board approval.

## 3. Conditions of use
An automated tool may only contribute to an assessment decision where all of the
following are satisfied at the same time:
(a) the marker can obtain a plain-language account of why the tool produced its
output, including its confidence and known limitations;
(b) the tool's stated purpose matches its validated purpose, confirmed by the
Academic Standards Office independently of the tool's sponsor;
(c) the tool operates only on the assessment types for which it was validated;
any other case must be referred to a human marker.
Meeting some but not all of these conditions is not approval.

## 4. Student rights
A student may request academic review of any decision to which an automated tool
contributed, within 20 working days. The reviewer may substitute their own
decision. This right may not be made conditional on any other process.

## 5. Monitoring
Faculties must report tool usage each semester. Where agreement between tool
output and marker judgement falls below 90%, use must be paused and referred to
the Academic Standards Office within 10 working days.

## 6. Application to governing bodies
Academic Board and the Academic Standards Office are themselves subject to this
policy and must report their own compliance to Senate annually.

## 7. Change
Any change to a tool's model, training data, or scope of use requires
re-approval under section 3 before continued use.
"""

# Asserts a protection in one clause and revokes it in the next.
SELF_CONTRADICTING = """# Helix Systems — AI Transparency Standard

## 1. Commitment to transparency
Helix is committed to full transparency in its AI systems. Users shall be given
meaningful information about how decisions affecting them are made.

## 2. Model disclosure
The scoring model, its features, and its weights are proprietary trade secrets
and cannot be disclosed to customers, regulators, or affected individuals under
any circumstances.

## 3. Reversibility
Helix supports the ability to correct outcomes. Decisions recorded in the ledger
are permanently written and cannot be reversed or amended once committed.

## 4. Human oversight
Human oversight is maintained at all times. The system executes remediation
actions automatically without human review or approval to ensure response times
are met.
"""


class AcademicRegisterDetectionTests(unittest.TestCase):
    """Register neutrality must not be specific to one sector's vocabulary."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = assess("POL-AS-09", "policy", ACADEMIC_POLICY,
                            assessment_mode="external_framework",
                            sector=runner.auto_sector(ACADEMIC_POLICY))

    def test_all_expressed_constructs_are_functional(self) -> None:
        fa = self.result["functional_alignment"]
        for construct in ("Coupling", "Integrity Layer", "Reversibility", "Self-Application"):
            self.assertEqual(fa[construct]["verdict"], "FUNCTIONAL",
                             f"{construct}: {fa[construct]['families']}")

    def test_percentage_breach_trigger_counts_as_a_threshold(self) -> None:
        """'falls below 90%' states what counts as a problem."""
        fired = {lbl for lbl, _ in self.result["score_breakdown"]["enforceability"]["fired"]}
        self.assertIn("risk-proportionate thresholds", fired)

    def test_pausing_use_counts_as_an_enforcement_consequence(self) -> None:
        fired = {lbl for lbl, _ in self.result["score_breakdown"]["enforceability"]["fired"]}
        self.assertIn("enforcement consequences / penalties", fired)

    def test_no_false_gaps(self) -> None:
        gaps = runner.build_governance_gap_register(self.result, [{"quote_id": "Q001"}])
        types = {g["gap_type"] for g in gaps}
        for false_positive in ("monitoring_without_threshold",
                               "policy_without_enforcement_consequence",
                               "lifecycle_without_change_control"):
            self.assertNotIn(false_positive, types)


class SelfContradictionTests(unittest.TestCase):
    """A revoked protection outranks an omitted one and must be reported."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = assess("Helix", "policy", SELF_CONTRADICTING,
                            assessment_mode="external_framework",
                            sector="general_ai_governance")

    def test_all_three_contradictions_detected(self) -> None:
        subjects = {c[0].replace(" (non-canonical)", "") for c in self.result["contradictions"]}
        for expected in ("Reversibility", "Structural Transparency", "Structural Containment"):
            self.assertIn(expected, subjects)

    def test_depth_is_hollow(self) -> None:
        self.assertEqual(self.result["structural_depth"], "HOLLOW")

    def test_executive_finding_states_the_contradiction(self) -> None:
        gaps = runner.build_governance_gap_register(self.result, [{"quote_id": "Q001"}])
        controls = runner.build_control_recommendations(gaps, [], [{"quote_id": "Q001"}])
        finding = runner.executive_thesis(self.result, gaps, controls)
        self.assertIn("Self-contradiction", finding)

    def test_report_quotes_each_contradiction(self) -> None:
        gaps = runner.build_governance_gap_register(self.result, [{"quote_id": "Q001"}])
        report = runner.build_institutional_report(
            {"safe_output_stem": "x"}, {}, self.result, [{"quote_id": "Q001"}],
            gaps, runner.build_failure_pathways(gaps, []),
            runner.build_control_recommendations(gaps, [], []))
        self.assertIn("## Self-contradictions in the document", report)
        self.assertIn("CONTRA-001", report)

    def test_regulating_a_hazard_is_not_committing_it(self) -> None:
        """A restriction naming the hazard must not be read as the hazard."""
        regulating = ("The model operates within its approved use boundary. The "
                      "restriction on automated credit decisioning without human "
                      "review exists to protect the applicant's interest in a "
                      "decision they can understand and contest.")
        result = assess("clean", "policy", regulating,
                        assessment_mode="external_framework", sector="general_ai_governance")
        self.assertEqual(result["contradictions"], [])


class InstrumentFormClassificationTests(unittest.TestCase):
    """Buyer's instrument, supplier's answer, and a values charter are distinct."""

    def test_supplier_response_is_a_vendor_submission_not_a_tender(self) -> None:
        response = ("Supplier Response — AI Governance Attestation. Submitted by: "
                    "Kestrel Analytics Ltd. We attest that our platform has been "
                    "assessed against our internal Model Governance Standard.")
        self.assertEqual(classify_document_type(response), "vendor_compliance_submission")

    def test_issuing_instrument_is_a_procurement_form(self) -> None:
        issuing = ("Invitation to Tender. Section C: Supplier Assurance Questionnaire. "
                   "Suppliers must provide evidence of current certification.")
        self.assertEqual(classify_document_type(issuing), "procurement_assessment_form")

    def test_values_statement_is_a_charter(self) -> None:
        charter = ("Responsible AI Charter. We believe artificial intelligence should "
                   "serve people. Our values guide everything we build. We are "
                   "committed to fairness and strive to be open about how our systems "
                   "work.")
        self.assertEqual(classify_document_type(charter), "values_charter")

    def test_a_charter_that_imposes_duties_is_not_a_charter(self) -> None:
        """Values vocabulary must not outrank actual obligations."""
        policy = ("Group AI Charter. We believe in fairness and our values guide us. "
                  "All business units shall maintain a model register. Model owners "
                  "must report breaches to the Risk Committee. Non-compliance is a "
                  "reportable control breach. This standard binds all Group entities.")
        self.assertNotEqual(classify_document_type(policy), "values_charter")

    def test_sector_basis_explains_the_profile_actually_used(self) -> None:
        """Showing one profile's name beside another's evidence is incoherent."""
        tender = ("Invitation to Tender — AI-Assisted Triage System. Section C: "
                  "Supplier Assurance Questionnaire. Suppliers must supply a Clinical "
                  "Safety Case Report compliant with DCB0129 for NHS patient care. "
                  "The contract may be terminated for material breach.")
        result = assess("ITT", "policy", tender, assessment_mode="external_framework",
                        sector="auto")
        used = result.get("sector_profile") or result.get("sector_used")
        basis = runner.auto_sector_basis(tender, used)["basis"]
        self.assertNotIn("no sector-specific vocabulary", basis)
        if used == "procurement_vendor_governance":
            self.assertNotIn("clinical", basis)


# Every broadened pattern's mirror risk: a document assembled from the
# vocabulary itself. It fires many signals and creates no duty.
GOVERNANCE_SOUP = """# Acme AI Governance Standard

Owner: Chief Risk Officer. Approved by: Governance Committee. Review: annual.
Version 3.

Controls, procedures, protocols, safeguards, and mechanisms are in place.
Thresholds, tolerances, and materiality apply. Change control and re-approval
and lifecycle and post-deployment and retraining are addressed. Human review,
human oversight, human decision-maker, manual review, and escalation to a human
are supported. Explanation of any individual decision, meaningful information,
transparency, interpretability, and plain-language account of why the output was
produced are provided. Internal Audit, model owners, suppliers, vendors, and
contractors are named. Accountability, traceability, audit trail, and version
control are maintained. Model risk, risk framework, risk committee, risk
appetite, risk register, and risk-based approach are used. Termination, material
breach, suspension, sanction, penalty, and non-compliance are consequences.
Fairness, non-discrimination, workers, and contestability and appeal and redress
are covered. Reviewers may overturn the decision. Use suspended. Monthly review.
Above 5%. Within 5 working days.

All of the following hold simultaneously. Partial satisfaction is not approval.
This Standard binds all Group entities. Group Risk is itself subject to this
Standard and must evidence its own compliance to Internal Audit.
Each restriction exists to protect the customer's interest. Neither may be
weakened without the other. Material change requires re-approval.
"""


class VocabularyEnumerationTests(unittest.TestCase):
    """Breadth must not certify a word list.

    Detection is keyed to function rather than to one institution's vocabulary,
    which makes the vocabulary itself the attack surface. These tests hold both
    sides: the soup is caught, and every genuine document stays clear of the
    detector.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.soup = assess("Acme", "policy", GOVERNANCE_SOUP,
                          assessment_mode="external_framework",
                          sector="general_ai_governance")

    def test_enumeration_is_detected(self) -> None:
        self.assertEqual(self.soup["vocabulary_enumeration_risk"], "HIGH")
        self.assertGreaterEqual(self.soup["vocabulary_enumeration_ratio"], 0.15)
        self.assertTrue(self.soup["vocabulary_enumeration_examples"])

    def test_a_word_list_is_never_certified_as_aligned(self) -> None:
        self.assertNotEqual(self.soup["laif_alignment"], "FUNCTIONALLY ALIGNED")
        self.assertEqual(self.soup["structural_depth"], "HOLLOW")

    def test_it_becomes_the_leading_finding_with_its_own_evidence(self) -> None:
        gaps = runner.build_governance_gap_register(self.soup, [{"quote_id": "Q001"}])
        self.assertEqual(gaps[0]["gap_type"], "vocabulary_without_operative_effect")
        controls = runner.build_control_recommendations(gaps, [], [{"quote_id": "Q001"}])
        finding = runner.executive_thesis(self.soup, gaps, controls)
        self.assertIn("listed rather than made operative", finding)
        report = runner.build_institutional_report(
            {"safe_output_stem": "x"}, {}, self.soup, [{"quote_id": "Q001"}],
            gaps, runner.build_failure_pathways(gaps, []), controls)
        self.assertIn("## Governance vocabulary without operative effect", report)

    def test_coupling_claim_is_qualified_not_asserted(self) -> None:
        gaps = runner.build_governance_gap_register(self.soup, [{"quote_id": "Q001"}])
        finding = runner.executive_thesis(self.soup, gaps,
                                          runner.build_control_recommendations(gaps, [], []))
        self.assertIn("cannot be read from the text", finding)

    def test_genuine_documents_stay_clear_of_the_detector(self) -> None:
        """The whole assessment corpus plus every institutional fixture."""
        import official_documents, sample_documents
        corpus = []
        for collection in (official_documents.OFFICIAL_DOCUMENTS, sample_documents.DOCUMENTS):
            for key, entry in collection.items():
                corpus.append((entry.get("name", key),
                               entry.get("text") or entry.get("excerpt")))
        corpus += [("bank standard", INSTITUTIONAL_STANDARD),
                   ("academic policy", ACADEMIC_POLICY),
                   ("values charter", "We believe AI should serve people. Our values "
                                      "guide everything we build. We are committed to "
                                      "fairness and strive to be open."),
                   ("self-contradicting", SELF_CONTRADICTING)]
        for name, text in corpus:
            result = assess(name, "policy", text, assessment_mode="external_framework",
                            sector="general_ai_governance")
            self.assertEqual(result["vocabulary_enumeration_risk"], "LOW",
                             f"false positive on {name}: ratio "
                             f"{result['vocabulary_enumeration_ratio']}")


class NonGovernanceTextTests(unittest.TestCase):
    """Broadened detection must not turn ordinary prose into a governance finding."""

    SALES_REPORT = (
        "Q3 Regional Sales Report. Revenue grew 12% against plan, driven by the "
        "enterprise segment. The team reviewed pipeline coverage monthly and "
        "documented account handovers. Northern region reported a shortfall of "
        "4% which management expects to recover in Q4. Headcount is unchanged."
    )

    def test_ordinary_business_prose_scores_near_zero(self) -> None:
        result = assess("Q3 sales", "report", self.SALES_REPORT,
                        assessment_mode="external_framework", sector="general_ai_governance")
        self.assertLess(result["overall_readiness_score"], 20)
        self.assertEqual(result["structural_score"], 0)
        self.assertEqual(result["enforceability_score"], 0)

    def test_sector_vocabulary_without_architecture_is_flagged(self) -> None:
        soup = ("Credit scoring underwriting insurance AML fraud detection model risk "
                "model validation fair lending fairness testing explainability.")
        result = assess("soup", "test", soup, assessment_mode="external_framework",
                        sector="financial_services_ai")
        self.assertEqual(result["sector_gaming_risk"], "HIGH")


if __name__ == "__main__":
    unittest.main()
