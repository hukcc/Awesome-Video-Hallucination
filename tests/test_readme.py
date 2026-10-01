"""Regression checks for deterministic, linked, taxonomy-preserving README output."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_catalog import Document
from generate_readme import anchor, newest_first, paper_list, recently_added, render, replace_region, resource_badge, task_index


class ReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'data/papers.json').read_text())
        cls.metadata = json.loads((ROOT / 'data/paper_details.json').read_text())
        cls.entries = cls.data['entries']

    def test_generated_readme_is_current_and_idempotent(self):
        text = (ROOT / 'README.md').read_text()
        self.assertEqual(render(text, self.data, self.metadata), text)
        self.assertEqual(render(render(text, self.data, self.metadata), self.data, self.metadata), text)

    def test_manual_content_is_untouched(self):
        original = 'keep intro\n<!-- BEGIN TASK INDEX -->old<!-- END TASK INDEX -->\nkeep citation'
        self.assertEqual(replace_region(original, 'TASK INDEX', 'new'),
                         'keep intro\n<!-- BEGIN TASK INDEX -->\n\nnew\n\n<!-- END TASK INDEX -->\nkeep citation')
        with self.assertRaises(ValueError):
            replace_region('no markers', 'TASK INDEX', 'new')

    def test_sorting_does_not_mutate_catalog(self):
        before = copy.deepcopy(self.entries)
        ordered = newest_first(self.entries, self.metadata['papers'])
        self.assertEqual(ordered[0]['arxiv_id'], '2609.36628')
        self.assertEqual(ordered[-1]['arxiv_id'], '2303.02961')
        self.assertEqual(self.entries, before)

    def test_recent_additions_use_history_and_link_all_sibling_contributions(self):
        output = recently_added(self.entries, self.metadata)
        self.assertIn('2026-10-01 &middot; 7 papers', output)
        self.assertNotIn('<details open>', output)
        doc = Document()
        doc.feed(output)
        expected = [anchor(e) for e in self.entries
                    if self.metadata['papers'][e['arxiv_id'] or e['paper_url']]['added']['date'] == '2026-10-01']
        self.assertCountEqual([href[1:] for href in doc.links if href.startswith('#')], expected)

    def test_unknown_addition_dates_are_not_invented_and_large_batches_are_bounded(self):
        metadata = copy.deepcopy(self.metadata)
        for paper in metadata['papers'].values():
            paper['added'] = None
        self.assertEqual(recently_added(self.entries, metadata), '')
        for paper in metadata['papers'].values():
            paper['added'] = {'date': '2026-10-01', 'commit': 'a' * 40}
        doc = Document()
        doc.feed(recently_added(self.entries, metadata))
        ids = {href[1:] for href in doc.links if href.startswith('#')}
        displayed = {e['arxiv_id'] or e['paper_url'] for e in self.entries if anchor(e) in ids}
        self.assertEqual(len(displayed), 8)
        self.assertIn('https://hukcc.github.io/Awesome-Video-Hallucination/?sort=added', doc.links)

    def test_all_contributions_have_unique_anchors_and_resolvable_links(self):
        doc = Document()
        doc.feed(paper_list(self.entries, self.metadata))
        self.assertCountEqual(doc.ids, [anchor(e) for e in self.entries])
        self.assertEqual(len(doc.rows), len(self.entries))
        targets = [href[1:] for href in doc.links if href.startswith('#')]
        self.assertEqual(len(targets), 34)
        self.assertTrue(set(targets) <= set(doc.ids))
        self.assertTrue(all(len(row) in (4, 5) for row in doc.rows))

    def test_task_index_covers_every_contribution(self):
        doc = Document()
        doc.feed(task_index(self.entries, self.metadata))
        self.assertEqual({href[1:] for href in doc.links}, {anchor(e) for e in self.entries})
        self.assertTrue(all(href.startswith('#paper-') for href in doc.links))

    def test_unknown_taxonomy_fails_instead_of_dropping_papers(self):
        entries = copy.deepcopy(self.entries)
        entries[0]['subtype'] = 'Unknown'
        with self.assertRaises(ValueError):
            paper_list(entries, self.metadata)

    def test_html_metacharacters_are_escaped(self):
        entries = copy.deepcopy(self.entries[:1])
        entries[0]['description'] = 'Visual <evidence> & quoted "claims".'
        output = paper_list(entries, self.metadata)
        self.assertIn('Visual &lt;evidence&gt; &amp; quoted &quot;claims&quot;.', output)
        self.assertNotIn('<evidence>', output)

    def test_every_resource_remains_a_linked_badge(self):
        doc = Document()
        doc.feed(paper_list(self.entries, self.metadata))
        entries = {anchor(e): e for e in self.entries}
        for cells in doc.rows:
            entry = entries[cells[0]['ids'][0]]
            expected = [url for url in entry['resources'].values() if url]
            images = cells[-1]['images']
            self.assertCountEqual([image['href'] for image in images], expected)
            self.assertTrue(all(image['src'].startswith('https://img.shields.io/badge/') and image['alt'] for image in images))
            if not expected:
                self.assertEqual(cells[-1]['text'], '-')

    def test_original_badge_styles_and_dataset_platforms(self):
        cases = [
            ('project', 'https://example.org', 'Page%20%F0%9F%94%97-Link-228B22?logo=readthedocs&logoColor=white'),
            ('code', 'https://github.com/example/repo', 'Code-Link-blue?logo=github'),
            ('dataset', 'https://huggingface.co/datasets/example/test', 'Dataset-HuggingFace-yellow?logo=huggingface'),
            ('dataset', 'https://www.kaggle.com/datasets/example/test', 'Dataset-Kaggle-20BEFF?logo=kaggle&logoColor=white'),
            ('leaderboard', 'https://huggingface.co/spaces/example/test', 'Page%20%F0%9F%94%97-Leaderboard-228B22?logo=readthedocs&logoColor=white'),
            ('dataset', 'https://example.org/data', 'Dataset-Link-yellow'),
        ]
        for kind, url, expected in cases:
            doc = Document()
            doc.feed('<table><tr><td>' + resource_badge(kind, url) + '</td></tr></table>')
            image = doc.rows[0][0]['images'][0]
            self.assertEqual(image['src'], 'https://img.shields.io/badge/' + expected)
            self.assertEqual(image['href'], url)

    def test_training_free_symbols_preserve_current_verified_values(self):
        doc = Document()
        doc.feed(paper_list(self.entries, self.metadata))
        entries = {anchor(e): e for e in self.entries}
        for cells in doc.rows:
            entry = entries[cells[0]['ids'][0]]
            if entry['type'] == 'mitigation':
                self.assertEqual(cells[3]['text'], entry['training_free'])

    def test_paper_titles_and_contribution_names_have_distinct_columns(self):
        doc = Document()
        output = paper_list(self.entries, self.metadata)
        doc.feed(output)
        entries = {anchor(e): e for e in self.entries}
        for cells in doc.rows:
            entry = entries[cells[0]['ids'][0]]
            self.assertEqual(cells[1]['text'], entry['name'])
            self.assertTrue(cells[0]['text'].startswith(entry['title'] + ' '))
        self.assertEqual(output.count('</a></b><br>'), len(self.entries))

    def test_task_index_is_compact_without_hiding_the_paper_tables(self):
        output = task_index(self.entries, self.metadata)
        self.assertIn('<summary><b>Task index</b>', output)
        self.assertNotIn('<details open>', output)
        self.assertEqual(output.count('<details>'), len(self.metadata['task_vocabulary']) + 1)
        text = (ROOT / 'README.md').read_text()
        self.assertLess(text.index('![Framework overview]'), text.index('## Find Your Papers'))
        self.assertIn('<details open>\n<summary><b>Event Misordering', text)

    def test_repository_badges_and_supporting_content_are_retained(self):
        text = (ROOT / 'README.md').read_text()
        for label in ('Awesome', 'arXiv', 'ACL 2026 Findings', 'Entries', 'Auto arXiv Update', 'License: MIT', 'Last Commit'):
            self.assertIn(f'[![{label}](', text)
        for content in ('imgs/teaser.png', 'imgs/fig2_taxonomy.png', '## Latest Updates', '## Citation', '@article{huang2026distorted,'):
            self.assertIn(content, text)


if __name__ == '__main__':
    unittest.main()
