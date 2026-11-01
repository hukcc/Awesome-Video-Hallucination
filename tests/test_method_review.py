"""Contribution coverage, conservative scope decisions, and method provenance."""

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_remote_sources import collect_urls
from generate_method_review import render


class MethodReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((ROOT / 'data/method_review.json').read_text())
        cls.data = json.loads((ROOT / 'data/papers.json').read_text())
        cls.metadata = json.loads((ROOT / 'data/paper_details.json').read_text())
        cls.entries = {e['id']: e for e in cls.data['entries']}
        cls.records = cls.audit['records']

    def test_report_is_current_and_contains_every_entry_anchor(self):
        output = render(self.audit)
        self.assertEqual(output, (ROOT / 'docs/METHOD_REVIEW.md').read_text())
        for record in self.records:
            self.assertIn(f'id="method-{record["entry_id"]}"', output)
        self.assertEqual(output.count('**Training-free: Yes.**') +
                         output.count('**Training-free: No.**'), len(self.records))

    def test_all_methods_are_reviewed_and_pending_moves_are_not_applied(self):
        methods = {e['id'] for e in self.entries.values() if e['type'] == 'mitigation'}
        self.assertEqual(methods, {r['entry_id'] for r in self.records})
        self.assertEqual(len(self.records), len(methods))
        self.assertEqual(Counter(r['recommendation'] for r in self.records),
                         dict(retain=38, correct=1, move_to_related=14))
        for record in self.records:
            expected = 'pending-manual-review' if record['recommendation'] == 'move_to_related' else 'reviewed'
            self.assertEqual(record['status'], expected)
            self.assertEqual(self.entries[record['entry_id']]['name'], record['listed_name'])

    def test_review_depth_sources_and_training_requirements(self):
        for record in self.records:
            self.assertIn('Abstract', record['inspected_sections'])
            self.assertIn('Introduction', record['inspected_sections'])
            self.assertRegex(record['source_sha256'], r'^[a-f0-9]{64}$')
            self.assertTrue(all(record[k] for k in ('intervention', 'evaluation', 'rationale')))
            entry = self.entries[record['entry_id']]
            self.assertEqual(record['training_free'], entry['training_free'] == '\u2714\ufe0e')
            if entry['arxiv_id']:
                self.assertRegex(record['source_url'], rf'/html/{entry["arxiv_id"]}v\d+$')
            else:
                self.assertEqual(record['source_url'], 'https://www.ijcai.org/proceedings/2025/1019.pdf')
            detail = self.metadata['papers'][record['paper_key']]
            self.assertEqual(detail['source_url'], record['source_url'])
            self.assertEqual(detail['evidence'], record['inspected_sections'])

    def test_only_documented_catalog_corrections_change_original_records(self):
        descriptions = {'Temporal Insight', 'TAAE', 'MMA', 'GroundedVQA', 'mrDPO', 'PEP-MEK'}
        for record in self.records:
            original = record['original_entry']
            current = self.entries[record['entry_id']]
            changed = {k for k in original.keys() | current.keys() if original.get(k) != current.get(k)}
            expected = {'name', 'aliases'} if original['name'] == 'MoPE' else (
                {'description'} if original['name'] in descriptions else set())
            self.assertEqual(changed, expected, original['name'])
            for key in ('id', 'type', 'paper_url', 'resources', 'training_free', 'routes', 'category', 'subtype'):
                self.assertEqual(current[key], original[key])
        mope = next(e for e in self.entries.values() if e['name'] == 'GRPO with MoPE')
        self.assertIn('MoPE', mope['aliases'])
        pep = next(e for e in self.entries.values() if e['name'] == 'PEP-MEK')
        self.assertIn('Predict-Explain-Predict with Modality and Emotion Knowledge', pep['description'])
        self.assertNotIn('memory-based', pep['description'])

    def test_sibling_benchmarks_survive_pending_method_recommendations(self):
        for key in ('2406.06040', '2609.13288'):
            entries = [e for e in self.entries.values() if e['arxiv_id'] == key]
            self.assertEqual(Counter(e['type'] for e in entries), dict(benchmark=1, mitigation=1))

    def test_remote_audit_includes_method_evidence_without_metadata_dependency(self):
        urls = collect_urls({'entries': []}, {'papers': {}}, '', method_review=self.audit)
        self.assertEqual(len(urls), 53)
        for record in self.records:
            self.assertIn(f'{record["listed_name"]}: method evidence', urls[record['source_url']])

    def test_review_records_are_not_exposed_in_reader_surfaces(self):
        for filename in ('README.md', 'index.html'):
            content = (ROOT / filename).read_text()
            for marker in ('docs/METHOD_REVIEW.md', 'docs/BENCHMARK_REVIEW.md',
                           'docs/RELEVANCE_REVIEW.md', 'docs/CURATION.md', 'new_papers.md',
                           'Review log', 'Review notes', 'Update log', 'pending approval'):
                self.assertNotIn(marker, content, filename)
        app = (ROOT / 'assets/app.js').read_text()
        for marker in ('data/method_review.json', 'methodReviews', 'Method audit',
                       'Review evidence', 'reviewed_on', 'scope_review.reason'):
            self.assertNotIn(marker, app)
        deployment = (ROOT / '.github/workflows/pages.yml').read_text()
        self.assertNotIn('new_papers.md', deployment)
        self.assertIn('cp data/papers.json data/paper_details.json _site/data/', deployment)


if __name__ == '__main__':
    unittest.main()
