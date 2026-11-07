#!/usr/bin/env python3
"""Adversarial tests of the non-promotional scholarly evidence workflow.

Synthetic fixtures verify software behaviour, not the correctness of LAIF's
substantive analysis or the validity of any legal/safety conclusion.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import laif_research_report as researcher
import laif_research_review as peer

SOURCE = ROOT / "docs/examples/vendor-policy.md"


class ScholarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dossier = researcher.build_dossier(
            SOURCE, source_scope="excerpt", date="2026-11-07")
        cls.doc_text = SOURCE.read_text(encoding="utf-8")

    def test_inventories_are_source_bounded_and_sha_locked(self) -> None:
        d = self.dossier
        self.assertEqual(d["schema"], researcher.SCHEMA)
        self.assertEqual(d["status"], "EVIDENCE_INVENTORY_ONLY")
        self.assertEqual(d["source"]["source_sha256"],
                         hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertEqual(d["source"]["source_scope"], "excerpt")
        self.assertEqual(d["evidence_manifest_sha256"],
                         researcher._evidence_manifest_sha256(d["evidence"]))
        self.assertEqual(d["independent_replication"], "NOT_PERFORMED")
        self.assertEqual(d["scholarly_validation"], "NOT_ESTABLISHED")
        self.assertGreater(len(d["evidence"]), 0)
        self.assertLessEqual(len(d["evidence"]), 8)
        for item in d["evidence"]:
            self.assertEqual(self.doc_text[item["start_char"]:item["end_char"]],
                             item["exact_quote"])
            self.assertEqual(item["evidence_status"], "EXTRACTED_TEXT_MATCH_ONLY")

    def test_neutral_report_avoids_automated_certification_and_absence_claims(self) -> None:
        report = researcher.render_markdown(self.dossier)
        self.assertIn("not independently authenticated", report)
        self.assertIn("non-exhaustive", report)
        self.assertIn("No analyst findings were supplied", report)
        self.assertIn("source scope", report.lower())
        self.assertNotIn("LAIF-native FAIL", report)
        self.assertNotIn("Total LAIF", report)
        self.assertNotIn("overall score", report.lower())
        self.assertNotIn("no rights of appeal exist", report.lower())
        self.assertNotIn("must adopt LAIF", report)
        self.assertIn("Source-bounded AI governance evidence review", report)

    def test_repeatable_given_same_source_code_and_date(self) -> None:
        second = researcher.build_dossier(SOURCE, source_scope="excerpt", date="2026-11-07")
        self.assertEqual(self.dossier, second)
        self.assertEqual(researcher.render_markdown(self.dossier),
                         researcher.render_markdown(second))

    def test_committed_neutral_example_matches_actual_renderer(self) -> None:
        committed = (ROOT / "docs/examples/sample-scholarly-report.md").read_text(encoding="utf-8")
        self.assertEqual(committed, researcher.render_markdown(self.dossier))

    def test_explicit_abstention_when_quote_quality_is_insufficient(self) -> None:
        with patch.object(researcher, "build_extraction_quality_profile",
                          return_value={"primary_quote_eligible": False}):
            dossier = researcher.build_dossier(SOURCE, date="2026-11-07")
        self.assertEqual(dossier["evidence"], [])
        self.assertEqual(dossier["status"], "EVIDENCE_REVIEW_REQUIRED")
        self.assertIn("Abstention:", researcher.render_markdown(dossier))
        self.assertIn("must abstain", " ".join(dossier["limitations"]))

    def test_unusable_quotation_does_not_enter_report(self) -> None:
        records = [{"exact_quote": "not in the source", "start_offset": 0, "end_offset": 17}]
        self.assertEqual(researcher._observations(self.doc_text, records, True, 8), [])
        self.assertEqual(researcher._observations(self.doc_text, records, False, 8), [])

    def test_unicode_markdown_injection_escaped_in_report(self) -> None:
        d = json.loads(json.dumps(self.dossier))
        d["research_question"] = "<script>alert('x')</script>\n# Fake finding"
        d["source"]["file_name"] = "<not-safe>.md"
        d["evidence"][0]["exact_quote"] = "![external pixel](https://example.org/pixel)\n# Injected heading"
        report = researcher.render_markdown(d)
        self.assertNotIn("<script>", report)
        self.assertNotIn("\n# Fake finding", report)
        self.assertIn("&lt;script&gt;", report)
        self.assertNotIn("![external pixel]", report)
        self.assertIn(r"\!\[external pixel\]", report)
        self.assertNotIn("> # Injected heading", report)

    def test_source_url_requires_explicit_safe_attribution(self) -> None:
        for url in ("http://example.com", "https://a:b@example.com", "https://[malformed"):
            with self.subTest(url=url), self.assertRaises(researcher.ResearchInputError):
                researcher.build_dossier(SOURCE, source_url=url)

    def test_wrong_extractor_rejected_before_misreading_bytes(self) -> None:
        with self.assertRaisesRegex(researcher.ResearchInputError, "incorrect local extractor"):
            researcher.build_dossier(SOURCE, extractor="pypdf")

    def test_analyst_findings_require_source_identity_and_alternatives(self) -> None:
        template = researcher.review_template(self.dossier)
        evidence_id = template["available_evidence_ids"][0]
        template["findings"] = [{
            "finding_id": "F001", "claim_type": "INFERENCE",
            "statement": "A written control is described; its operation remains untested.",
            "evidence_ids": [evidence_id], "counterevidence_ids": [],
            "alternative_explanations": ["A separate operating protocol may contain the tests."],
            "limitations": "Only an excerpt was supplied.", "analyst_id": "researcher-a",
        }]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.json"
            path.write_text(json.dumps(template), encoding="utf-8")
            dossier = researcher.build_dossier(SOURCE, date="2026-11-07", review_file=path)
            self.assertEqual(dossier["status"], "ANALYST_ANNOTATED_DRAFT")
            self.assertIn("independent corroboration not established", researcher.render_markdown(dossier))
            template["source_sha256"] = "0" * 64
            path.write_text(json.dumps(template), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "SHA-256"):
                researcher.build_dossier(SOURCE, review_file=path)
            template["source_sha256"] = self.dossier["source"]["source_sha256"]
            template["evidence_manifest_sha256"] = "0" * 64
            path.write_text(json.dumps(template), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "manifest SHA-256"):
                researcher.build_dossier(SOURCE, review_file=path)
            template["evidence_manifest_sha256"] = self.dossier["evidence_manifest_sha256"]
            template["findings"][0]["evidence_ids"] = ["UNKNOWN"]
            path.write_text(json.dumps(template), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "existing evidence IDs"):
                researcher.build_dossier(SOURCE, review_file=path)
            template["findings"][0]["evidence_ids"] = [evidence_id]
            template["findings"][0]["alternative_explanations"] = []
            path.write_text(json.dumps(template), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "alternative"):
                researcher.build_dossier(SOURCE, review_file=path)

    def test_annotation_ids_cannot_shift_after_quote_limit_changes(self) -> None:
        template = researcher.review_template(self.dossier)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "template.json"
            path.write_text(json.dumps(template), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "manifest SHA-256"):
                researcher.build_dossier(SOURCE, max_quotes=1, review_file=path)

    def test_ambiguous_duplicate_json_keys_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicated.json"
            path.write_text('{"schema":"a","schema":"b"}', encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "duplicate JSON key"):
                researcher._read_json(path)

    def test_preview_does_not_write_and_require_evidence_holds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "no-output"
            command = [sys.executable, str(ROOT / "scripts/laif_research_report.py"),
                       str(SOURCE), "--date", "2026-11-07", "--preview",
                       "--output-dir", str(dest)]
            proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse(dest.exists())
            self.assertIn("Source-bounded AI governance evidence review", proc.stdout)

    def test_distinct_scope_and_date_do_not_overwrite_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "results"
            base = [sys.executable, str(ROOT / "scripts/laif_research_report.py"),
                    str(SOURCE), "--output-dir", str(dest)]
            first = subprocess.run(base + ["--date", "2026-11-06", "--scope", "excerpt"],
                                   cwd=ROOT, capture_output=True, text=True)
            second = subprocess.run(base + ["--date", "2026-11-07", "--scope", "unknown"],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(len(list(dest.glob("*.research_data.json"))), 2)


class SecondReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dossier = researcher.build_dossier(SOURCE, source_scope="excerpt", date="2026-11-07")
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.path = Path(cls.tmp.name) / "dossier.research_data.json"
        cls.path.write_text(json.dumps(cls.dossier, sort_keys=True), encoding="utf-8")
        cls.loaded, cls.digest, cls.targets = peer.load_dossier(cls.path)

    def review(self, reviewer: str, *, verdict: str = "source_matched",
               inspected: bool = True, independent: bool = True) -> dict:
        t = peer.review_template(self.digest, self.targets)
        t["reviewer_id"] = reviewer
        t["original_source_inspected"] = inspected
        t["independence_declaration"] = ("self_declared_independent" if independent else "unknown")
        for row in t["ratings"]:
            row["verdict"] = verdict
            row["reason"] = "Reviewed source excerpt and context independently."
        p = Path(self.tmp.name) / f"{reviewer}.json"
        p.write_text(json.dumps(t), encoding="utf-8")
        return peer.validate_review(p, self.digest, self.targets)

    def test_template_does_not_claim_completed_review(self) -> None:
        t = peer.review_template(self.digest, self.targets)
        self.assertEqual(t["independence_declaration"], "unknown")
        self.assertFalse(t["original_source_inspected"])
        self.assertTrue(all(row["verdict"] == "unverified" for row in t["ratings"]))

    def test_single_reviewer_cannot_claim_independence(self) -> None:
        s = peer.summarise(self.digest, self.targets, [self.review("scholar-a")])
        self.assertEqual(s["status"], "INSUFFICIENT_SECOND_READERS")
        self.assertIsNone(s["pairwise_raw_agreement"])
        self.assertEqual(s["publication_clearance"], "NOT_GRANTED")

    def test_two_reviewers_are_not_a_certification(self) -> None:
        s = peer.summarise(self.digest, self.targets,
                           [self.review("scholar-a"), self.review("scholar-b")])
        self.assertEqual(s["status"], "CONCORDANT_SELF_ATTESTATIONS_NOT_CERTIFICATION")
        self.assertEqual(s["pairwise_raw_agreement"], 1.0)
        self.assertEqual(s["paired_rating_count"], len(self.targets))
        self.assertEqual(s["external_identity_verification"], "NOT_PERFORMED")
        self.assertIn("not a measure", peer.render_markdown(s).lower())

    def test_conflicting_review_requires_adjudication(self) -> None:
        s = peer.summarise(self.digest, self.targets,
                           [self.review("scholar-a"), self.review("scholar-b", verdict="source_disagrees")])
        self.assertEqual(s["status"], "DISAGREEMENT_REQUIRES_ADJUDICATION")
        self.assertEqual(s["paired_agreement_count"], 0)

    def test_source_context_not_attested_blocks_ready_label(self) -> None:
        s = peer.summarise(self.digest, self.targets,
                           [self.review("scholar-a"), self.review("scholar-b", inspected=False)])
        self.assertEqual(s["status"], "INDEPENDENCE_OR_SOURCE_CONTEXT_NOT_ATTESTED")

    def test_bad_review_hash_and_invalid_types_rejected(self) -> None:
        t = peer.review_template(self.digest, self.targets)
        t["reviewer_id"] = "scholar-a"
        t["dossier_sha256"] = "not the same file"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "invalid.json"
            p.write_text(json.dumps(t), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "hash mismatch"):
                peer.validate_review(p, self.digest, self.targets)
            t["dossier_sha256"] = self.digest
            t["independence_declaration"] = []
            p.write_text(json.dumps(t), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "declaration"):
                peer.validate_review(p, self.digest, self.targets)
            t["independence_declaration"] = "unknown"
            t["ratings"][0]["target_id"] = []
            p.write_text(json.dumps(t), encoding="utf-8")
            with self.assertRaisesRegex(researcher.ResearchInputError, "invalid"):
                peer.validate_review(p, self.digest, self.targets)

    def test_review_template_cli_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "results"
            p = subprocess.run([sys.executable, str(ROOT / "scripts/laif_research_review.py"),
                                str(self.path), "--template", "--output-dir", str(dest)],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)["dossier_sha256"], self.digest)
            self.assertFalse(dest.exists())

    def test_reviewer_collision_rejected(self) -> None:
        r = self.review("same-person")
        with self.assertRaisesRegex(researcher.ResearchInputError, "unique"):
            peer.summarise(self.digest, self.targets, [r, r])


if __name__ == "__main__":
    unittest.main()
