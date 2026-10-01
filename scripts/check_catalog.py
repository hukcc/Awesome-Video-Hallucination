#!/usr/bin/env python3
"""Check README/data agreement and local browser references without dependencies."""

import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = None
        self.cell = None
        self.links = []
        self.ids = []
        self.tables = []
        self.table = None
        self.current_href = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[key] for key in ('href', 'src') if key in attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'table':
            self.table = []
        if tag == 'tr':
            self.row = []
        if tag == 'td' and self.row is not None:
            self.cell = {'text': [], 'links': [], 'ids': [], 'images': []}
        if tag == 'a':
            self.current_href = attrs.get('href')
        if tag == 'a' and self.cell is not None:
            if 'href' in attrs:
                self.cell['links'].append(attrs['href'])
            if 'id' in attrs:
                self.cell['ids'].append(attrs['id'])
        if tag == 'br' and self.cell is not None:
            self.cell['text'].append(' ')
        if tag == 'img' and self.cell is not None:
            self.cell['images'].append({**attrs, 'href': self.current_href})

    def handle_data(self, text):
        if self.cell is not None:
            self.cell['text'].append(text)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.current_href = None
        if tag == 'td' and self.cell is not None:
            self.cell['text'] = ' '.join(''.join(self.cell['text']).split())
            self.row.append(self.cell)
            self.cell = None
        if tag == 'tr' and self.row is not None:
            if self.row:
                self.rows.append(self.row)
                if self.table is not None:
                    self.table.append(self.row)
            self.row = None
        if tag == 'table' and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def check():
    data = json.loads((ROOT / 'data/papers.json').read_text())
    entries = data['entries']
    details = json.loads((ROOT / 'data/paper_details.json').read_text())['papers']
    readme = Document()
    readme_text = (ROOT / 'README.md').read_text()
    readme.feed(readme_text)
    assert len(readme.rows) == len(entries) == data['entry_count']
    by_anchor = {'paper-' + e['id']: e for e in entries}
    seen = []
    for cells in readme.rows:
        assert len(cells[0]['ids']) == 1, cells[0]
        entry_anchor = cells[0]['ids'][0]
        entry = by_anchor[entry_anchor]
        seen.append(entry_anchor)
        assert 12 <= len(entry['description'].split()) <= 40, entry['name']
        expected = [entry['name'], entry['title'], entry['description']]
        related = [e for e in entries if e['paper_url'] == entry['paper_url'] and e['id'] != entry['id']]
        labels = {'benchmark': 'Related benchmark', 'mitigation': 'Related method', 'analysis': 'Related analysis'}
        if related:
            expected.append(' \u00b7 '.join(f'{labels[e["type"]]}: {e["name"]}' for e in related))
        assert cells[0]['text'] == ' '.join(expected), entry['name']
        assert cells[1]['text'] == entry['venue'] + ' ' + entry['date'], entry['name']
        assert len(cells) == (4 if entry['type'] == 'mitigation' else 3), entry['name']
        if entry['type'] == 'mitigation':
            assert cells[2]['text'] == entry['training_free'], entry['name']
        assert cells[0]['links'] == [entry['paper_url']] + ['#paper-' + e['id'] for e in related], entry['name']
        assert sorted(cells[-1]['links']) == sorted(url for url in entry['resources'].values() if url), entry['name']
        assert sorted(image['href'] for image in cells[-1]['images']) == sorted(cells[-1]['links']), entry['name']
        assert all(image['src'].startswith('https://img.shields.io/badge/') and image['alt'] for image in cells[-1]['images']), entry['name']
    assert Counter(seen) == Counter(by_anchor.keys()), 'Missing or duplicate README entries'
    for table in readme.tables:
        group = [by_anchor[cells[0]['ids'][0]] for cells in table]
        assert len({(e['type'], e['mechanism'], e['category'], e['subtype']) for e in group}) == 1
        dates = [details[e['arxiv_id'] or e['paper_url']]['published_on'] for e in group]
        assert dates == sorted(dates, reverse=True), 'Subtype is not newest first'
    index = Document()
    index.feed(readme_text.split('<!-- BEGIN TASK INDEX -->')[1].split('<!-- END TASK INDEX -->')[0])
    assert {href[1:] for href in index.links} == set(by_anchor), 'Task index coverage differs'
    for href in readme.links:
        if href.startswith('#'):
            assert href[1:] in readme.ids, 'Broken README entry anchor: ' + href
    for kind, count in Counter(e['type'] for e in entries).items():
        assert data[kind + '_count'] == count
    assert len({e['id'] for e in entries}) == len(entries)
    for entry in entries:
        assert entry['training_free'] in ('\u2714\ufe0e', '\u2718') if entry['type'] == 'mitigation' else entry['training_free'] is None
        for url in [entry['paper_url'], *entry['resources'].values()]:
            if url:
                assert urlsplit(url).scheme == 'https' and not re.search(r'\s', url), url
    for path in [ROOT / 'index.html', ROOT / 'README.md', ROOT / 'docs/CURATION.md']:
        text = path.read_text()
        doc = Document()
        doc.feed(text)
        assert len(doc.ids) == len(set(doc.ids)), path
        urls = doc.links + re.findall(r'\]\(([^)]+)\)', text)
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            assert (path.parent / unquote(parsed.path)).exists(), (path, url)
    assert not re.search(r'[\u4e00-\u9fff]', readme_text), 'README must remain English'
    for directory in ('assets', 'data', 'docs', 'tests'):
        for path in (ROOT / directory).rglob('*'):
            if path.suffix in ('.md', '.json', '.js', '.mjs', '.css'):
                assert not re.search(r'[\u4e00-\u9fff]', path.read_text()), path
    hashes = {hashlib.sha256((ROOT / 'imgs' / (name + '.png')).read_bytes()).hexdigest() for name in ('taxonomy_tree', 'taxonomy', 'fig2_taxonomy')}
    assert len(hashes) == 1, 'Taxonomy image aliases differ'
    print(f'PASS: {len(entries)} README/data entries, descriptions, task anchors, cross-links, date order, resource badges, English metadata, and taxonomy image aliases.')


if __name__ == '__main__':
    check()
