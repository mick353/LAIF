"""Navigation targets follow GitHub heading IDs, independently of scores."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from assessment_engine import _md_anchor, assess, generate_markdown_report
from test_real_world import ALL_DOCUMENTS


class ReportNavigationTests(unittest.TestCase):
    def test_punctuation_does_not_collapse_adjacent_spaces(self):
        self.assertEqual(_md_anchor("Peer Exemplars — What Good Looks Like"),
                         "peer-exemplars--what-good-looks-like")
        self.assertEqual(_md_anchor("GOVERN & MAP"), "govern--map")
        self.assertEqual(_md_anchor("A\tB C_D-E"), "ab-c_d-e")

    def test_all_ten_current_document_targets_and_peer_section(self):
        # Explicit expected GitHub IDs: do not compute expectations with the helper.
        expected = [
            'document-1-us-executive-order-14110--2-principles-6-workers-7-civil-rights-official-text',
            'document-2-oecd-recommendation-on-ai-oecdlegal0449--sections-1--2-official-text',
            'document-3-nist-ai-rmf-10-nist-ai-100-1--govern--map-functions-official-text',
            'document-4-nhs-england-dtac-v20-february-2026--introduction--c1-clinical-safety-official-text',
            'document-5-eu-ai-act--art-9-13--14',
            'document-6-nist-ai-rmf--govern--map-functions',
            'document-7-oecd-ai-principles-2019-rev-2024',
            'document-8-us-executive-order-14110--4-safety--7-workers',
            'document-9-nhs-england--ai-in-clinical-decision-support-policy-framework',
            'document-10-tuccipd--framework-for-fair-ai-in-employment-decisions',
        ]
        assessments = [assess(name=name, assessment_mode='external_framework', **doc)
                       for name, doc in ALL_DOCUMENTS.items()]
        report = generate_markdown_report(assessments)
        headings = re.findall(r'^### (Document \d+: .+)$', report, re.MULTILINE)
        self.assertEqual(len(headings), 10)
        self.assertEqual([_md_anchor(heading) for heading in headings], expected)
        targets = re.findall(r'^\d+\. \[.*?\]\(#([^)]*)\)$', report, re.MULTILINE)
        self.assertEqual(targets, expected)
        self.assertIn('## Peer Exemplars — What Good Looks Like in This Corpus', report)
        self.assertIn('[Peer Exemplars](#peer-exemplars--what-good-looks-like-in-this-corpus)', report)


if __name__ == '__main__':
    unittest.main()
