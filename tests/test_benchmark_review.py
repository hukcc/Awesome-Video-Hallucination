"""Strict benchmark coverage, evidence, provenance, and regression checks."""

import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_benchmark_review import render
from generate_readme import resource_badge


class BenchmarkReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((ROOT / 'data/benchmark_review.json').read_text())
        cls.entries = json.loads((ROOT / 'data/papers.json').read_text())['entries']
        cls.by_id = {e['id']: e for e in cls.entries}
        cls.records = cls.audit['records']

    def test_report_is_current(self):
        self.assertEqual(render(self.audit), (ROOT / 'docs/BENCHMARK_REVIEW.md').read_text())

    def test_all_active_benchmarks_have_approved_contribution_level_review(self):
        approved = {r['entry_id'] for r in self.records if r['decision'] in ('retain', 'narrow')}
        self.assertEqual(approved, {e['id'] for e in self.entries if e['type'] == 'benchmark'})
        self.assertEqual(len(self.records), len({r['entry_id'] for r in self.records}))
        self.assertEqual(Counter(r['decision'] for r in self.records),
                         dict(retain=26, narrow=6, remove=10, reclassify=1))

    def test_decisions_match_catalog_and_inspected_evidence(self):
        for r in self.records:
            self.assertIn('Abstract', r['inspected_sections'])
            self.assertIn('Introduction', r['inspected_sections'])
            self.assertTrue(r['protocol'] and r['rationale'])
            self.assertTrue(r['source_url'].startswith('https://'))
            if r['original_entry']['arxiv_id']:
                self.assertRegex(r['source_url'], r'/html/\d{4}\.\d{4,5}v\d+$')
            if r['decision'] == 'remove':
                self.assertNotIn(r['entry_id'], self.by_id)
            else:
                current = self.by_id[r['entry_id']]
                self.assertEqual(current['name'], r['listed_name'])
                self.assertEqual(current['type'], r['listed_type'])
                self.assertEqual(current['resources'], r['original_entry']['resources'])
                self.assertEqual(current['paper_url'], r['original_entry']['paper_url'])
                if r['decision'] == 'narrow':
                    self.assertIn(r['original_entry']['name'], current['aliases'])

    def test_original_methods_and_analysis_remain_preserved(self):
        method_audit = json.loads((ROOT / 'data/method_review.json').read_text())
        originals = {r['entry_id']: r['original_entry'] for r in method_audit['records']}
        preserved = [originals[key] if key in originals else self.by_id[key]
                     for key in self.audit['unchanged_contribution_ids']]
        digest = hashlib.sha256(json.dumps(sorted(preserved, key=lambda e: e['id']), sort_keys=True).encode()).hexdigest()
        self.assertEqual(digest, self.audit['unchanged_contributions_sha256'])
        self.assertEqual(Counter(e['type'] for e in preserved), dict(mitigation=53, analysis=1))

    def test_removed_resources_and_orphaned_paper_metadata_are_archived(self):
        report = render(self.audit)
        active = {e['arxiv_id'] or e['paper_url'] for e in self.entries}
        archived = self.audit['archived_papers']
        removed_keys = {r['paper_key'] for r in self.records if r['decision'] == 'remove'} - active
        self.assertEqual(set(archived), removed_keys)
        for r in self.records:
            if r['decision'] != 'remove':
                continue
            self.assertIn(r['original_entry']['paper_url'], report)
            for kind, url in r['original_entry']['resources'].items():
                if url:
                    self.assertIn(resource_badge(kind, url), report)
        self.assertEqual(len([u for u in next(r for r in self.records if r['paper_key'] == '2610.12458')['original_entry']['resources'].values() if u]), 4)


if __name__ == '__main__':
    unittest.main()
