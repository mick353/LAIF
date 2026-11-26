#!/usr/bin/env python3
"""Synthetic-only integrity tests for descriptive independent-study comparisons."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from laif_study_compare import analyse, format_summary, metrics, reviewer_agreement, validate, wilson95


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_case(i, gold, laif, checklist, keyword, *, split="holdout", family=None):
    return {"id": f"synthetic-{i}", "family": family or f"synthetic-family-{i}",
            "source_sha256": digest(f"synthetic source {i}"),
            "split": split, "attribute": "named_owner",
            "reference": gold,
            "reviewer_votes": [{"reviewer": "A", "value": gold},
                               {"reviewer": "B", "value": not gold if i in (2, 4) else gold}],
            "predictions": {"laif": laif, "checklist": checklist, "keyword": keyword}}


def study():
    return {"schema": "laif.comparative-study.v1", "study_id": "SYNTHETIC-EXAMPLE-ONLY",
            "label_provenance": "SYNTHETIC", "protocol_sha256": "a"*64,
            "evaluated_revision": "b"*40,
            "cases": [
                make_case(1, True, True, False, True),
                make_case(2, True, False, True, None),
                make_case(3, False, True, False, False),
                make_case(4, False, False, True, None),
                make_case(5, True, None, True, False),
                make_case(6, False, None, None, True),
            ]}


class StudyComparisonTests(unittest.TestCase):
    def test_clearly_synthetic_and_not_scientific_validity(self):
        report = analyse(study())
        self.assertEqual(report["status"], "DESCRIPTIVE_COMPARISON_ONLY")
        self.assertEqual(report["declared_label_provenance"], "SYNTHETIC")
        self.assertIn("not verified", report["boundary"])
        self.assertIn("not validate LAIF theory", report["boundary"])
        self.assertEqual(report["splits"]["development"]["n"], 0)
        self.assertEqual(report["splits"]["holdout"]["n"], 6)

    def test_false_negatives_are_distinct_from_abstentions(self):
        result = analyse(study())["splits"]["holdout"]["systems"]["laif"]
        self.assertEqual({k: result[k] for k in ("TP", "TN", "FP", "FN", "abstained")},
                         {"TP": 1, "TN": 1, "FP": 1, "FN": 1, "abstained": 2})
        self.assertEqual(result["coverage"], round(4/6, 6))
        self.assertEqual(result["precision"], 0.5)
        self.assertEqual(result["recall"], 0.5)
        self.assertEqual(result["f1"], 0.5)
        self.assertEqual(result["abstained_reference_positive"], 1)
        self.assertEqual(result["abstained_reference_negative"], 1)
        self.assertEqual(result["recall_over_all_positives"], 0.333333)

    def test_common_answer_advantage_can_reverse_across_all_cases(self):
        dataset = study()
        dataset["cases"] = [make_case(i, True, True if i < 3 else None, i != 2, None)
                            for i in range(1, 7)]
        result = analyse(dataset)["splits"]["holdout"]
        self.assertEqual(result["systems"]["laif"]["recall"], 1.0)
        self.assertEqual(result["systems"]["laif"]["recall_over_all_positives"], 0.333333)
        pair = result["paired_comparisons"]["checklist"]
        self.assertEqual(pair["common_answered_n"], 2)
        self.assertEqual(pair["accuracy_difference_on_common"], 0.5)
        self.assertEqual(pair["correct_per_case_difference_on_all"], -0.5)
        self.assertEqual(pair["coverage_difference_on_all"], -0.666667)
        self.assertEqual(pair["all_case_outcomes"]["abstained"]["correct"], 4)
        self.assertEqual(sum(sum(row.values()) for row in pair["all_case_outcomes"].values()), 6)
        pair = result["paired_comparisons"]["keyword"]
        self.assertIsNone(pair["accuracy_difference_on_common"])
        self.assertEqual(pair["all_case_outcomes"]["abstained"]["abstained"], 4)

    def test_family_deletion_can_expose_one_family_driving_the_result(self):
        dataset = study()
        dataset["cases"] = [make_case(i, True, True, False, True, family="large-family")
                            for i in range(8)] + [make_case(i, True, False, True, True) for i in range(8, 10)]
        split = analyse(dataset)["splits"]["holdout"]
        pair = split["paired_comparisons"]["checklist"]
        self.assertEqual(pair["correct_per_case_difference_on_all"], 0.6)
        self.assertEqual(pair["correct_per_case_difference_leave_one_family_out"],
                         {"families": 3, "status": "DESCRIPTIVE_RANGE", "range": [-1.0, 0.777778]})
        self.assertEqual(split["declared_families"], 3)
        self.assertEqual(split["source_documents"], 10)
        laif = split["systems"]["laif"]
        self.assertIsNone(laif["recall_wilson95"])
        self.assertIsNone(laif["precision_wilson95"])
        self.assertEqual(laif["wilson95_status"], "WITHHELD_REPEATED_SOURCE_OR_FAMILY")

    def test_same_source_in_multiple_families_cannot_count_as_independent(self):
        dataset = study()
        dataset["cases"][1]["source_sha256"] = dataset["cases"][0]["source_sha256"]
        split = analyse(dataset)["splits"]["holdout"]
        pair = split["paired_comparisons"]["checklist"]
        self.assertEqual(split["source_documents"], 5)
        self.assertIsNone(split["systems"]["laif"]["precision_wilson95"])
        self.assertEqual(pair["correct_per_case_difference_leave_one_family_out"]["status"],
                         "SOURCE_ASSIGNED_TO_MULTIPLE_FAMILIES")
        self.assertIsNone(pair["correct_per_case_difference_leave_one_family_out"]["range"])

    def test_agreement_keeps_directional_disagreements_and_sparse_reviewer_counts(self):
        cases = study()["cases"]
        cases[0]["reviewer_votes"].append({"reviewer": "C", "value": False})
        cases[0]["reviewer_votes"].reverse()
        pairs = reviewer_agreement(cases)
        self.assertEqual(pairs[0], {"reviewer_a": "A", "reviewer_b": "B", "n": 6,
                                    "both_positive": 2, "both_negative": 2,
                                    "reviewer_a_only_positive": 1, "reviewer_b_only_positive": 1,
                                    "observed_agreement": 0.666667, "cohen_kappa": 0.333333})
        self.assertEqual([(r["reviewer_a"], r["reviewer_b"], r["n"], r["cohen_kappa"]) for r in pairs[1:]],
                         [("A", "C", 1, None), ("B", "C", 1, None)])

    def test_frozen_holdout_checks_labels_but_allows_new_predictions(self):
        dataset = study()
        snapshot = analyse(dataset)["holdout_snapshot_sha256"]
        dataset["cases"].reverse()
        dataset["cases"][0]["predictions"]["laif"] = False
        changed = analyse(dataset, expected_holdout_sha256=snapshot)
        self.assertEqual(changed["holdout_against_expected"], "MATCH")
        dataset["cases"][0]["reference"] = not dataset["cases"][0]["reference"]
        with self.assertRaisesRegex(ValueError, "holdout snapshot differs"):
            analyse(dataset, expected_holdout_sha256=snapshot)

    def test_cli_verifies_protocol_and_expected_holdout(self):
        dataset = study()
        protocol = b"Frozen research protocol\r\n"
        dataset["protocol_sha256"] = hashlib.sha256(protocol).hexdigest()
        holdout = analyse(dataset)["holdout_snapshot_sha256"]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "study.json"
            path.write_text(json.dumps(dataset), encoding="utf-8")
            protocol_path = Path(temp) / "protocol.txt"
            protocol_path.write_bytes(protocol)
            cmd = [sys.executable, str(ROOT / "scripts/laif_study_compare.py"), str(path), "--format", "json",
                   "--protocol", str(protocol_path), "--expect-holdout-sha256", holdout]
            run = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")
            report = json.loads(run.stdout)
            self.assertEqual(report["protocol_bytes"], "MATCH")
            self.assertEqual(report["holdout_against_expected"], "MATCH")
            protocol_path.write_bytes(protocol.replace(b"\r\n", b"\n"))
            run = subprocess.run(cmd, capture_output=True, text=True, check=False, encoding="utf-8")
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("protocol bytes differ", run.stderr)
            self.assertEqual(run.stdout, "")

    def test_aligned_baselines_and_pairwise_comparisons(self):
        result = analyse(study())["splits"]["holdout"]
        self.assertEqual(result["systems"]["checklist"]["answered"], 5)
        self.assertEqual(result["systems"]["keyword"]["answered"], 4)
        pair = result["paired_comparisons"]["checklist"]
        self.assertEqual(pair["common_answered_n"], 4)
        self.assertEqual(pair["laif_only_correct"], 2)
        self.assertEqual(pair["baseline_only_correct"], 2)
        self.assertEqual(pair["both_wrong"], 0)

    def test_human_disagreement_is_pre_adjudication_and_separate(self):
        result = analyse(study())["splits"]["holdout"]["human_pairwise_agreement_before_adjudication"]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["n"], 6)
        self.assertEqual(result[0]["observed_agreement"], round(4/6, 6))
        self.assertLess(result[0]["cohen_kappa"], 1)

    def test_pairwise_perfect_agreement_and_degenerate_kappa(self):
        cases = [make_case(i, i % 2 == 0, True, True, True) for i in (7, 8, 9, 10)]
        self.assertEqual(reviewer_agreement(cases)[0]["cohen_kappa"], 1)
        for case in cases:
            case["reviewer_votes"] = [{"reviewer": "A", "value": True},
                                      {"reviewer": "B", "value": True}]
        self.assertIsNone(reviewer_agreement(cases)[0]["cohen_kappa"])

    def test_metrics_with_only_abstentions_do_not_invent_negative_labels(self):
        sample = [make_case(12, True, None, None, None)]
        result = metrics(sample, "laif")
        self.assertEqual(result["abstained"], 1)
        self.assertEqual(result["FN"], 0)
        self.assertIsNone(result["precision"])
        self.assertIsNone(result["recall"])
        self.assertIsNone(result["f1"])

    def test_undefined_ratio_and_wilson_bounds(self):
        self.assertIsNone(wilson95(0, 0))
        self.assertEqual(wilson95(0, 1)[0], 0)
        self.assertEqual(wilson95(1, 1)[1], 1)

    def test_no_partial_comparator_set(self):
        obj = study()
        del obj["cases"][0]["predictions"]["keyword"]
        with self.assertRaisesRegex(ValueError, "all three comparator"):
            validate(obj)

    def test_boolean_strictness_and_missing_reference(self):
        obj = study()
        obj["cases"][0]["reference"] = 1  # bool is a subclass of int, but 1 must not pass.
        with self.assertRaisesRegex(ValueError, "reference must be boolean"):
            validate(obj)
        obj = study()
        obj["cases"][0]["predictions"]["laif"] = "FAIL"
        with self.assertRaisesRegex(ValueError, "true, false or null"):
            validate(obj)

    def test_deduplicated_cases_and_leakage_prevention(self):
        obj = study()
        obj["cases"].append(copy.deepcopy(obj["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate case id"):
            validate(obj)
        obj = study()
        obj["cases"][0]["split"] = "development"
        obj["cases"][1]["family"] = obj["cases"][0]["family"]
        with self.assertRaisesRegex(ValueError, "family appears in both splits"):
            validate(obj)
        obj = study()
        obj["cases"][0]["split"] = "development"
        obj["cases"][1]["source_sha256"] = obj["cases"][0]["source_sha256"]
        with self.assertRaisesRegex(ValueError, "source appears in both splits"):
            validate(obj)

    def test_human_provenance_requires_two_votes_and_adjudication_digest(self):
        obj = study()
        with self.assertRaisesRegex(ValueError, "human-adjudicated labels required"):
            analyse(obj, require_human=True)
        obj["label_provenance"] = "HUMAN_ADJUDICATED"
        with self.assertRaisesRegex(ValueError, "adjudication_sha256 required"):
            validate(obj)
        for case in obj["cases"]:
            case["adjudication_sha256"] = digest(case["id"] + " synthetic record")
        self.assertEqual(analyse(obj, require_human=True)["status"], "DESCRIPTIVE_COMPARISON_ONLY")
        obj["cases"][0]["reviewer_votes"] = [obj["cases"][0]["reviewer_votes"][0]]
        with self.assertRaisesRegex(ValueError, "two distinct blinded"):
            validate(obj)

    def test_invalid_source_hash_prohibits_untraceable_cases(self):
        obj = study()
        obj["cases"][0]["source_sha256"] = "not-a-source-hash"
        with self.assertRaisesRegex(ValueError, "source_sha256"):
            validate(obj)

    def test_cli_rejects_duplicate_json_keys_and_synthetic_human_claim(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "study.json"
            path.write_text('{"schema":"laif.comparative-study.v1","schema":"override"}',
                            encoding="utf-8")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/laif_study_compare.py"), str(path)],
                                 capture_output=True, text=True, check=False)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("duplicate JSON property", run.stderr)
            path.write_text(json.dumps(study()), encoding="utf-8")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/laif_study_compare.py"),
                                  str(path), "--require-human"], capture_output=True,
                                 text=True, check=False)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("human-adjudicated labels required", run.stderr)

    def test_deterministic_cli_and_no_output_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "study.json"
            path.write_text(json.dumps(study(), indent=2) + "\n", encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/laif_study_compare.py"), str(path)]
            run1 = subprocess.run(command, capture_output=True, text=True, check=True)
            run2 = subprocess.run(command, capture_output=True, text=True, check=True)
            self.assertEqual(run1.stdout, run2.stdout)
            self.assertIn("SYNTHETIC", run1.stdout)
            self.assertIn("does NOT validate", run1.stdout)
            self.assertIn("Paired LAIF vs checklist", run1.stdout)
            full = subprocess.run(command + ["--format", "json"],
                                  capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(full.stdout)["splits"]["holdout"]["n"], 6)
            self.assertEqual(sorted(p.name for p in Path(temp).iterdir()), ["study.json"])

    def test_committed_fixture_and_summary_readability(self):
        path = ROOT / "docs/examples/comparative-study-synthetic.json"
        dataset = json.loads(path.read_text(encoding="utf-8"))
        result = analyse(dataset)
        self.assertEqual(result["splits"]["holdout"]["n"], 4)
        readable = format_summary(result)
        self.assertIn("SYNTHETIC", readable)
        self.assertIn("kappa", readable)
        self.assertIn("NOT validate", readable)


if __name__ == "__main__":
    unittest.main()
