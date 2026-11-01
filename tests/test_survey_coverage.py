"""Protect original-survey contributions without adding public review labels."""

import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class SurveyCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coverage = json.loads((ROOT / 'data/survey_coverage.json').read_text())
        cls.entries = {e['id']: e for e in json.loads((ROOT / 'data/papers.json').read_text())['entries']}
        cls.metadata = json.loads((ROOT / 'data/paper_details.json').read_text())['papers']
        cls.benchmarks = json.loads((ROOT / 'data/benchmark_review.json').read_text())
        cls.methods = json.loads((ROOT / 'data/method_review.json').read_text())

    def test_complete_original_table_coverage_and_stable_placements(self):
        records = self.coverage['entries']
        self.assertEqual(Counter(r['type'] for r in records), dict(benchmark=19, mitigation=22))
        self.assertEqual(len({r['entry_id'] for r in records}), 41)
        self.assertEqual(len({r['paper_key'] for r in records}), 32)
        self.assertRegex(self.coverage['source_sha256'], r'^[a-f0-9]{64}$')
        for record in records:
            with self.subTest(name=record['survey_name']):
                entry = self.entries[record['entry_id']]
                self.assertEqual(entry['arxiv_id'] or entry['paper_url'], record['paper_key'])
                for field in ('type', 'category', 'subtype'):
                    self.assertEqual(entry[field], record[field])
                self.assertIn(record['paper_key'], self.metadata)
                table = 'S3.T1' if record['type'] == 'benchmark' else 'S4.T2'
                self.assertTrue(record['source_url'].startswith(self.coverage['source_url'] + '#' + table + '.'))
                self.assertTrue(record['reference_url'].startswith(self.coverage['source_url'] + '#bib.bib'))

    def test_protected_entries_are_never_pending_scope_removals(self):
        protected = {r['entry_id'] for r in self.coverage['entries']}
        for record in self.benchmarks['records']:
            if record['entry_id'] in protected:
                self.assertNotIn(record['decision'], ('remove', 'reclassify'))
        for record in self.methods['records']:
            if record['entry_id'] in protected:
                self.assertNotEqual(record['recommendation'], 'move_to_related')
        protected_keys = {r['paper_key'] for r in self.coverage['entries']}
        for key in protected_keys:
            self.assertNotEqual(self.metadata[key]['scope_review']['decision'], 'pending-manual-review')

    def test_restorations_preserve_original_entries_resources_and_dates(self):
        restored = [r for r in self.benchmarks['records'] if r['decision'] == 'retain_survey']
        self.assertEqual({r['original_entry']['name'] for r in restored}, {'OVBench', 'VideoHallu', 'RoadSocial'})
        for record in restored:
            self.assertEqual(record['previous_decision'], 'remove')
            expected = dict(record['original_entry'])
            if expected['name'] == 'OVBench':
                expected['description'] = (
                    'Evaluates models on streaming-video question answering across online perception, '
                    'memory, and reasoning tasks.'
                )
            self.assertEqual(self.entries[record['entry_id']], expected)
            self.assertEqual(record['preservation_source'], self.coverage['source_url'] + '#S3.T1')
        self.assertEqual(self.metadata['2503.21459'], self.benchmarks['archived_papers']['2503.21459'])
        protected_methods = [r for r in self.methods['records'] if r['recommendation'] == 'retain_survey']
        self.assertEqual({r['listed_name'] for r in protected_methods}, {'VTG-LLM', 'Vriptor', 'VideoChat-Online'})
        for record in protected_methods:
            self.assertEqual(record['previous_recommendation'], 'move_to_related')
            self.assertEqual(record['preservation_source'], self.coverage['source_url'] + '#S4.T2')

    def test_no_reader_facing_preservation_annotations(self):
        for filename in ('README.md', 'index.html', 'assets/app.js', 'figs/taxonomy_tree.tex'):
            text = (ROOT / filename).read_text()
            for marker in ('survey_coverage.json', 'Original-survey preservation', 'Retained as original-survey',
                           'preservation_source', 'preservation_reason'):
                self.assertNotIn(marker, text, filename)


if __name__ == '__main__':
    unittest.main()
