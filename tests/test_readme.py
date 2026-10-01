"""Regression checks for deterministic, linked, taxonomy-preserving README output."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_catalog import Document
from generate_readme import anchor, newest_first, paper_list, render, replace_region, task_index


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

    def test_all_contributions_have_unique_anchors_and_resolvable_links(self):
        doc = Document()
        doc.feed(paper_list(self.entries, self.metadata))
        self.assertCountEqual(doc.ids, [anchor(e) for e in self.entries])
        self.assertEqual(len(doc.rows), len(self.entries))
        targets = [href[1:] for href in doc.links if href.startswith('#')]
        self.assertEqual(len(targets), 34)
        self.assertTrue(set(targets) <= set(doc.ids))
        self.assertTrue(all(len(row) in (3, 4) for row in doc.rows))

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


if __name__ == '__main__':
    unittest.main()
