"""Preserve community entries and provenance without special public annotations."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_readme import resource_badge, row
from generate_taxonomy_tree import wrap_entries
from check_remote_sources import collect_urls


class CommunityContributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'data/papers.json').read_text())
        cls.metadata = json.loads((ROOT / 'data/paper_details.json').read_text())['papers']
        cls.entries = {e['id']: e for e in cls.data['entries']}

    def test_accepted_prs_remain_in_active_metadata(self):
        protected = {key: detail['community_contributions'] for key, detail in self.metadata.items()
                     if detail.get('community_contributions')}
        self.assertTrue({'2603.24329', '2605.27101'} <= protected.keys())
        self.assertEqual(protected['2603.24329'][0]['author'], 'wangyz1999')
        self.assertEqual(protected['2603.24329'][0]['number'], 2)
        self.assertEqual(protected['2605.27101'][0]['author'], 's-honcharenko')
        self.assertEqual(protected['2605.27101'][0]['number'], 3)
        for key, contributions in protected.items():
            for contribution in contributions:
                entry = self.entries[contribution['entry_id']]
                self.assertEqual(entry['arxiv_id'], key)
                self.assertEqual(entry['paper_url'], contribution['paper_url'])
                for kind, url in contribution['resources'].items():
                    self.assertEqual(entry['resources'][kind], url)

    def test_original_community_resources_and_placement_survive(self):
        gameplay = next(e for e in self.entries.values() if e['arxiv_id'] == '2603.24329')
        self.assertEqual(gameplay['type'], 'benchmark')
        self.assertEqual(gameplay['category'], 'Context-Driven Fabrication')
        self.assertEqual(gameplay['subtype'], 'Object-Action Hallucination')
        self.assertEqual(gameplay['resources'], dict(
            project='https://hats-ict.github.io/gameplayqa/',
            code='https://github.com/HATS-ICT/GameplayQA',
            dataset='https://huggingface.co/datasets/wangyz1999/GameplayQA', leaderboard=None))
        distraction = next(e for e in self.entries.values() if e['arxiv_id'] == '2605.27101')
        self.assertEqual(distraction['resources']['code'], 'https://github.com/lab-flair/video-llm-boe')
        self.assertEqual(distraction['resources']['dataset'], 'https://huggingface.co/datasets/lab-flair/VideoLLM-BoE')
        self.assertEqual(self.metadata['2603.24329']['added']['commit'], 'fbdebdb81950d395bdb46cc2c843394ecb593bd5')

    def test_badges_remain_visible_and_attribution_stays_in_records(self):
        readme = (ROOT / 'README.md').read_text()
        curation = (ROOT / 'docs/CURATION.md').read_text()
        for detail in self.metadata.values():
            for contribution in detail.get('community_contributions', []):
                self.assertIn(contribution['url'], curation)
                self.assertIn('@' + contribution['author'], curation)
                self.assertNotIn(contribution['url'], readme)
                for kind, url in contribution['resources'].items():
                    self.assertIn(resource_badge(kind, url), readme)
        app = (ROOT / 'assets/app.js').read_text()
        self.assertNotIn('paper.detail.community_contributions', app)
        self.assertNotIn('Broader benchmark', app)

    def test_plain_presentation_does_not_upgrade_relevance(self):
        exceptional = [e for e in self.entries.values() if e.get('scope_exception')]
        self.assertEqual([e['arxiv_id'] for e in exceptional], ['2603.24329'])
        self.assertEqual(self.metadata['2603.24329']['scope_review']['scope'], 'broader')
        self.assertEqual(wrap_entries(exceptional), 'GameplayQA (2026)')
        readme = (ROOT / 'README.md').read_text()
        self.assertNotIn('Broader benchmark', readme)
        self.assertNotIn('Community PR #2', readme)
        self.assertNotIn('retained as a community contribution', readme)
        self.assertNotIn('Broader benchmark retained as a community contribution.', (ROOT / 'assets/app.js').read_text())

    def test_remote_checks_include_accepted_contribution_sources(self):
        urls = collect_urls({'entries': []}, {'papers': self.metadata}, '')
        for number in (2, 3):
            self.assertIn(f'https://github.com/hukcc/Awesome-Video-Hallucination/pull/{number}', urls)

    def test_issue_provenance_is_audited_without_public_annotations(self):
        detail = copy.deepcopy(self.metadata['2603.24329'])
        contribution = detail['community_contributions'][0]
        contribution.update(kind='issue', number=99,
                            url='https://github.com/hukcc/Awesome-Video-Hallucination/issues/99')
        entry = self.entries[contribution['entry_id']]
        rendered = '\n'.join(row(entry, [entry]))
        self.assertNotIn('Issue #99', rendered)
        self.assertNotIn('PR #99', rendered)
        urls = collect_urls({'entries': [entry]}, {'papers': {'2603.24329': detail}}, '')
        self.assertIn(contribution['url'], urls)
        self.assertNotIn('https://github.com/hukcc/Awesome-Video-Hallucination/pull/99', urls)


if __name__ == '__main__':
    unittest.main()
