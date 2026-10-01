#!/usr/bin/env python3
"""Render the README task index and paper tables from the shared catalog."""

import argparse
import json
from collections import defaultdict
from html import escape
from pathlib import Path

from generate_taxonomy_tree import TAXONOMY

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = (
    ('benchmark', 'Evaluation Benchmarks', 'Benchmarks', 'Paper & Focus'),
    ('mitigation', 'Mitigation Strategies', 'Mitigation', 'Paper & Approach'),
    ('analysis', 'Evaluation Analyses', 'Analyses', 'Paper & Focus'),
)
COLORS = {
    'Spatiotemporal Dynamics': '\U0001f535',
    'Referential Inconsistency': '\U0001f7e2',
    'Context-Driven Fabrication': '\U0001f7e0',
    'Audio-Visual Conflict': '\U0001f7e3',
}
RESOURCE_LABELS = {'code': 'Code', 'dataset': 'Dataset', 'project': 'Project', 'leaderboard': 'Leaderboard'}


def paper_key(entry):
    return entry['arxiv_id'] or entry['paper_url']


def anchor(entry):
    return 'paper-' + entry['id']


def link(label, url):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def newest_first(entries, details):
    # Stable alphabetical ties; month-only dates are not assigned an invented day.
    ordered = sorted(entries, key=lambda e: (e['name'].casefold(), e['id']))
    return sorted(ordered, key=lambda e: details[paper_key(e)]['published_on'], reverse=True)


def task_index(entries, metadata):
    groups = defaultdict(list)
    for entry in entries:
        groups[paper_key(entry)].append(entry)
    details = metadata['papers']
    ordered = newest_first([group[0] for group in groups.values()], details)
    lines = [
        '#### Browse by Task', '',
        'Expand a task to jump directly to papers below. Tags describe paper-level scope; '
        'the linked benchmark and method entries explain each contribution. Papers are ordered newest first.', '',
    ]
    for task in metadata['task_vocabulary']:
        papers = [entry for entry in ordered if task in details[paper_key(entry)]['tasks']]
        lines += ['<details>', f'<summary><b>{escape(task)}</b> ({len(papers)} papers)</summary>', '', '<p>']
        labels = []
        for entry in papers:
            labels.append(' / '.join(link(e['name'], '#' + anchor(e)) for e in groups[paper_key(entry)]))
        lines += [' &middot;\n'.join(labels), '</p>', '', '</details>', '']
    return '\n'.join(lines).rstrip()


def row(entry, related):
    first = (
        f'<a id="{anchor(entry)}"></a><b>{escape(entry["name"])}</b><br>\n'
        f'        {link(entry["title"], entry["paper_url"])}<br>\n'
        f'        {escape(entry["description"])}'
    )
    siblings = [other for other in related if other['id'] != entry['id']]
    if siblings:
        labels = {'benchmark': 'Related benchmark', 'mitigation': 'Related method', 'analysis': 'Related analysis'}
        refs = [link(f'{labels[e["type"]]}: {e["name"]}', '#' + anchor(e)) for e in siblings]
        first += '<br>\n        <sub>' + ' &middot; '.join(refs) + '</sub>'
    cells = [first, escape(entry['venue']) + '<br>' + escape(entry['date'])]
    if entry['type'] == 'mitigation':
        cells.append('Yes' if entry['training_free'] == '\u2714\ufe0e' else 'No')
    resources = [link(label, entry['resources'][key]) for key, label in RESOURCE_LABELS.items() if entry['resources'].get(key)]
    cells.append(' &middot; '.join(resources) or '-')
    return ['    <tr>'] + [f'      <td align="left">{cell}</td>' for cell in cells] + ['    </tr>']


def paper_list(entries, metadata):
    details = metadata['papers']
    groups = defaultdict(list)
    for entry in entries:
        groups[paper_key(entry)].append(entry)
    lines = []
    emitted = []
    for kind, title, category_label, first_header in SECTIONS:
        lines += [f'## {title}', '']
        if kind == 'benchmark':
            lines += [
                'Each entry describes the listed contribution. Dates are **first publication** '
                '(first arXiv submission, or publisher issue when no arXiv record is used), '
                'not venue year. Entries are newest first within each subtype. '
                '[Sources and review notes](data/paper_details.json).', '',
            ]
        elif kind == 'mitigation':
            lines += [
                '**Training-free:** Yes = no additional parameter learning for the intervention; '
                'No = training is required, including auxiliary modules with a frozen backbone. '
                'Dates use first publication; entries are newest first within each subtype.', '',
            ]
        else:
            lines += [
                'Studies of evaluation validity and hallucination mechanisms without a standalone '
                'benchmark or mitigation method. Cross-category studies use their closest primary '
                'category. Dates use first publication.', '',
            ]
        for mechanism, _, categories in TAXONOMY:
            for category, _, _, subtypes in categories:
                category_entries = [e for e in entries if e['type'] == kind and e['category'] == category and e['mechanism'] == mechanism]
                if not category_entries:
                    continue
                prefix = COLORS[category] + ' ' if kind != 'analysis' else ''
                lines += [f'### {prefix}{category} {category_label} ({mechanism})', '']
                for subtype, _, _ in subtypes:
                    matching = newest_first([e for e in category_entries if e['subtype'] == subtype], details)
                    if not matching:
                        continue
                    emitted.extend(e['id'] for e in matching)
                    noun = 'entry' if len(matching) == 1 else 'entries'
                    headers = [first_header, 'Venue / First Published']
                    widths = [65, 17, 18]
                    if kind == 'mitigation':
                        headers.append('Training-Free')
                        widths = [57, 16, 10, 17]
                    headers.append('Resources')
                    lines += [
                        '<details open>', f'<summary><b>{escape(subtype)}</b> ({len(matching)} {noun})</summary>', '',
                        '<table width="100%">', '  <thead>', '    <tr>',
                    ]
                    lines += [f'      <th width="{width}%" align="left">{escape(label)}</th>' for label, width in zip(headers, widths)]
                    lines += ['    </tr>', '  </thead>', '  <tbody>']
                    for entry in matching:
                        lines += row(entry, groups[paper_key(entry)])
                    lines += ['  </tbody>', '</table>', '', '</details>', '']
        lines += ['[Back to task index](#browse-by-task)', '', '---', '']
    if sorted(emitted) != sorted(e['id'] for e in entries):
        raise ValueError('Every contribution must occur exactly once in the configured taxonomy.')
    return '\n'.join(lines).rstrip()


def replace_region(text, name, content):
    start, end = f'<!-- BEGIN {name} -->', f'<!-- END {name} -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f'Expected one pair of {name} markers in README.md')
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + '\n\n' + content + '\n\n' + end + after


def render(text, data, metadata):
    text = replace_region(text, 'TASK INDEX', task_index(data['entries'], metadata))
    return replace_region(text, 'PAPER LIST', paper_list(data['entries'], metadata))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated README sections are out of date.')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/papers.json').read_text())
    metadata = json.loads((ROOT / 'data/paper_details.json').read_text())
    path = ROOT / 'README.md'
    original = path.read_text()
    generated = render(original, data, metadata)
    if args.check:
        if generated != original:
            raise SystemExit('README sections are stale. Run python3 scripts/generate_readme.py')
        print(f'PASS: README task index and {len(data["entries"])} contribution entries are current.')
    elif generated != original:
        path.write_text(generated)
        print('Updated README task index and paper list.')


if __name__ == '__main__':
    main()
