#!/usr/bin/env python3
"""Render the README task index and paper tables from the shared catalog."""

import argparse
import json
from collections import defaultdict
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

from generate_taxonomy_tree import TAXONOMY

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = (
    ('benchmark', 'Evaluation Benchmarks', 'Benchmarks', 'Benchmark'),
    ('mitigation', 'Mitigation Strategies', 'Mitigation', 'Method'),
    ('analysis', 'Evaluation Analyses', 'Analyses', 'Analysis'),
)
COLORS = {
    'Spatiotemporal Dynamics': '\U0001f535',
    'Referential Inconsistency': '\U0001f7e2',
    'Context-Driven Fabrication': '\U0001f7e0',
    'Audio-Visual Conflict': '\U0001f7e3',
}
RESOURCE_LABELS = {'project': 'Project Page', 'code': 'Code', 'dataset': 'Dataset', 'leaderboard': 'Leaderboard'}
RESOURCE_BADGES = {
    'project': ('Page%20%F0%9F%94%97-Link-228B22?logo=readthedocs&logoColor=white', 'page'),
    'code': ('Code-Link-blue?logo=github', 'code'),
    'dataset': ('Dataset-Link-yellow', 'dataset'),
    'huggingface': ('Dataset-HuggingFace-yellow?logo=huggingface', 'dataset'),
    'kaggle': ('Dataset-Kaggle-20BEFF?logo=kaggle&logoColor=white', 'dataset'),
    'leaderboard': ('Page%20%F0%9F%94%97-Leaderboard-228B22?logo=readthedocs&logoColor=white', 'leaderboard'),
}


def paper_key(entry):
    return entry['arxiv_id'] or entry['paper_url']


def anchor(entry):
    return 'paper-' + entry['id']


def link(label, url):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def badge_image(kind, url=''):
    variant = kind
    if kind == 'dataset':
        host = (urlsplit(url).hostname or '').removeprefix('www.')
        variant = {'huggingface.co': 'huggingface', 'kaggle.com': 'kaggle'}.get(host, kind)
    path, alt = RESOURCE_BADGES[variant]
    src = 'https://img.shields.io/badge/' + path
    return f'<img src="{escape(src, quote=True)}" alt="{alt}" title="{RESOURCE_LABELS[kind]}" />'


def resource_badge(kind, url):
    return f'<a href="{escape(url, quote=True)}">{badge_image(kind, url)}</a>'


def resource_legend():
    examples = [('project', '', 'Project Page'), ('code', '', 'GitHub Repository'),
                ('dataset', 'https://huggingface.co/', 'Hugging Face Dataset'),
                ('dataset', 'https://www.kaggle.com/', 'Kaggle Dataset'),
                ('leaderboard', '', 'Leaderboard')]
    items = [f'{badge_image(kind, url)} = {label}' for kind, url, label in examples]
    return '\n'.join([
        '<details>', '<summary><b>Resource badge legend</b></summary>', '',
        '<p>' + '<br>\n'.join(items) + '<br>\n<code>-</code> = No verified resource link</p>', '',
        '</details>',
    ])


def newest_first(entries, details):
    # Stable alphabetical ties; month-only dates are not assigned an invented day.
    ordered = sorted(entries, key=lambda e: (e['name'].casefold(), e['id']))
    return sorted(ordered, key=lambda e: details[paper_key(e)]['published_on'], reverse=True)


def recently_added(entries, metadata):
    groups = defaultdict(list)
    for entry in entries:
        groups[paper_key(entry)].append(entry)
    details = metadata['papers']
    dated = [group[0] for key, group in groups.items() if details[key].get('added')]
    if not dated:
        return ''
    latest = max(details[paper_key(e)]['added']['date'] for e in dated)
    batch = newest_first([e for e in dated if details[paper_key(e)]['added']['date'] == latest], details)
    lines = ['<details>', f'<summary><b>Recently added</b> &middot; {latest} &middot; {len(batch)} papers</summary>', '', '<p>']
    labels = [' / '.join(link(e['name'], '#' + anchor(e)) for e in groups[paper_key(p)]) for p in batch[:8]]
    lines += [' &middot;\n'.join(labels), '</p>', '',
              '<p><sub>Repository additions, not publication dates. '
              '<a href="https://hukcc.github.io/Awesome-Video-Hallucination/?sort=added">All recent additions</a>'
              '</sub></p>', '', '</details>']
    return '\n'.join(lines)


def task_index(entries, metadata):
    groups = defaultdict(list)
    for entry in entries:
        groups[paper_key(entry)].append(entry)
    details = metadata['papers']
    ordered = newest_first([group[0] for group in groups.values()], details)
    lines = [
        '#### Browse by Task', '',
        '<details>',
        f'<summary><b>Task index</b> &middot; {len(metadata["task_vocabulary"])} topics &middot; {len(groups)} papers</summary>', '',
        '<p><sub>Paper-level task tags. Newest first; links lead to individual contributions below.</sub></p>', '',
    ]
    for task in metadata['task_vocabulary']:
        papers = [entry for entry in ordered if task in details[paper_key(entry)]['tasks']]
        lines += ['<details>', f'<summary><b>{escape(task)}</b> ({len(papers)} papers)</summary>', '', '<p>']
        labels = []
        for entry in papers:
            labels.append(' / '.join(link(e['name'], '#' + anchor(e)) for e in groups[paper_key(entry)]))
        lines += [' &middot;\n'.join(labels), '</p>', '', '</details>', '']
    lines += ['</details>']
    return '\n'.join(lines).rstrip()


def row(entry, related):
    first = (
        f'<a id="{anchor(entry)}"></a><b>{link(entry["title"], entry["paper_url"])}</b><br>\n'
        f'        <sub>{escape(entry["description"])}</sub>'
    )
    siblings = [other for other in related if other['id'] != entry['id']]
    if siblings:
        labels = {'benchmark': 'Related benchmark', 'mitigation': 'Related method', 'analysis': 'Related analysis'}
        refs = [link(f'{labels[e["type"]]}: {e["name"]}', '#' + anchor(e)) for e in siblings]
        first += '<br>\n        <sub>' + ' &middot; '.join(refs) + '</sub>'
    cells = [first, f'<b>{escape(entry["name"])}</b>',
             escape(entry['venue']) + '<br><sub>' + escape(entry['date']) + '</sub>']
    if entry['type'] == 'mitigation':
        label = 'Yes' if entry['training_free'] == '\u2714\ufe0e' else 'No'
        cells.append(f'<span title="Training-free: {label}">{entry["training_free"]}</span>')
    resources = [resource_badge(key, entry['resources'][key]) for key in RESOURCE_LABELS if entry['resources'].get(key)]
    cells.append(' '.join(resources) or '-')
    aligns = ['left'] + ['center'] * (len(cells) - 1)
    return ['    <tr>'] + [f'      <td align="{align}">{cell}</td>' for align, cell in zip(aligns, cells)] + ['    </tr>']


def paper_list(entries, metadata):
    details = metadata['papers']
    groups = defaultdict(list)
    for entry in entries:
        groups[paper_key(entry)].append(entry)
    lines = []
    emitted = []
    for kind, title, category_label, name_header in SECTIONS:
        lines += [f'## {title}', '']
        if kind == 'benchmark':
            lines += [
                '> [!NOTE]\n'
                '> Newest first within each subtype. **Date** = first arXiv submission, '
                'or publisher issue date when no arXiv record is used; venue years may differ. '
                '[Sources and review notes](data/paper_details.json).', '',
                resource_legend(), '',
            ]
        elif kind == 'mitigation':
            lines += [
                '> [!NOTE]\n'
                '> **Training-free:** \u2714\ufe0e No additional parameter learning; '
                '\u2718 Training required, including auxiliary modules with a frozen backbone. '
                'Dates use first publication; newest first within each subtype.', '',
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
                    headers = ['Paper', name_header, 'Venue / Date']
                    widths = [53, 13, 16, 18]
                    if kind == 'mitigation':
                        headers.append('Training-Free')
                        widths = [46, 13, 14, 9, 18]
                    headers.append('Resources')
                    lines += [
                        '<details open>', f'<summary><b>{escape(subtype)}</b> ({len(matching)} {noun})</summary>', '',
                        '<table width="100%">', '  <thead>', '    <tr>',
                    ]
                    for label, width in zip(headers, widths):
                        align = 'left' if label == 'Paper' else 'center'
                        lines.append(f'      <th width="{width}%" align="{align}">{escape(label)}</th>')
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
    text = replace_region(text, 'RECENT PAPERS', recently_added(data['entries'], metadata))
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
