#!/usr/bin/env python3
"""Generate the relevance review from the same evidence records used by the browser."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPES = [('related', 'Pending Manual Review'), ('broader', 'Broader Evaluations'), ('direct', 'Direct Focus')]


def render(data, metadata):
    groups = defaultdict(list)
    for entry in data['entries']:
        groups[entry['arxiv_id'] or entry['paper_url']].append(entry)
    reviews = {key: metadata['papers'][key]['scope_review'] for key in groups}
    counts = Counter(r['scope'] for r in reviews.values())
    introductions = sum('Introduction' in r['evidence'] for r in reviews.values())
    lines = ['# Relevance Review', '',
             'Editorial scope assessment, not a quality ranking or a removal decision. '
             'All existing papers, contributions, links, and taxonomy placements remain unchanged.', '',
             f'Coverage: **{len(groups)} papers / {len(data["entries"])} contributions**. '
             f'All abstracts were reviewed; **{introductions} papers** additionally received '
             'introduction review, with evaluation sections inspected where indicated. '
             'This is not a full-text audit of every paper.', '',
             f'Latest review: **{max(r["reviewed_on"] for r in reviews.values())}**. '
             f'**{counts["direct"]} direct-focus**, **{counts["broader"]} broader-evaluation**, '
             f'and **{counts["related"]} related-work candidates**.', '',
             '## Criteria', '',
             '- **Direct focus:** hallucination or unsupported video-grounded factual claims are an explicit research objective, '
             'diagnostic target, or mitigation target. This includes caption factuality and audio-visual hallucinations.',
             '- **Broader evaluation:** a general video task includes a concrete hallucination diagnostic, '
             'dedicated subset, or evidence-verification evaluation. Only that supported scope should be claimed.',
             '- **Related work (review):** grounding, QA accuracy, or self-correction is relevant, but the '
             'reviewed evidence does not establish a dedicated hallucination evaluation, or uses a substantially '
             'different definition. These are proposals for manual review, not assertions that a paper is irrelevant.', '',
             'The labels apply at paper level. A benchmark and method in the same paper can have different '
             'degrees of relevance. The existing taxonomy and contribution counts are retained pending decisions.', '',
             '## Manual Decision Queue', '',
             f'Review the {counts["related"]} candidates below before moving any entry. Decide whether '
             'coordinate/timestamp errors and general QA/correction metrics meet the intended collection scope. '
             'A move to Related Work is '
             'preferable to deletion when the paper remains useful background.', '',
             'Do **not** exclude OVBench, RoadSocial, CoE, Video-ToC, or SToP solely from their broad titles: '
             'the inspected source text establishes a specific hallucination evaluation. '
             'EchoPrune remains excluded; it must not be conflated with SToP.', '',
             '## Contribution-Level Caveats', '',
             '- **OVBench / VideoChat-Online:** the Temporal Hallucination Verification subset justifies paper-level '
             'inclusion; the model is still a general streaming-video architecture, not a dedicated mitigation design.',
             '- **Vript / Vriptor:** Vript-HAL is a hallucination benchmark, while the corpus, other benchmark tasks, '
             'and captioning model have broader purposes. Do not transfer a subset-level claim to the whole suite.',
             '- **VHD / TRACE-RC:** the method changes reliability ordering and accepted coverage, not model answers. '
             'Its placement among mitigation strategies means selective risk reduction, not factual correction.',
             '- **FactVC and Temporal Insight:** retain their explicit factuality/temporal-hallucination framing, '
             'but note that caption factuality or timestamp localization is not interchangeable with generative '
             'VideoLLM hallucination metrics.', '',
             '## Evidence Register', '',
             'Each row links both the existing README contribution and the exact reviewed source. '
             'Reasons are curator interpretations of those sources; the evidence column states the actual review depth.', '']
    for scope, heading in SCOPES:
        lines += [f'### {heading}', '', '| Paper / Contributions | Reason | Inspected Evidence |', '| --- | --- | --- |']
        keys = sorted((k for k in groups if reviews[k]['scope'] == scope), key=lambda k: groups[k][0]['name'].casefold())
        for key in keys:
            review = reviews[key]
            names = ' / '.join(f'[{e["name"]}](../README.md#paper-{e["id"]})' for e in groups[key])
            reason = review['reason'].replace('|', '\\|')
            evidence = review['evidence'].replace('|', '\\|')
            lines.append(f'| {names} | {reason} | [{evidence}]({review["source_url"]}) |')
        lines.append('')
    lines += ['## Maintenance', '',
              'Edit `scope_review` in `data/paper_details.json`, then run '
              '`python3 scripts/generate_relevance_review.py`. A new paper without a scope review is shown as '
              'Not reviewed in the browser, never silently classified as direct-focus. '
              'Apply approved inclusion or relocation decisions to the shared catalog and regenerate '
              'README and taxonomy together; this report does not apply them.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/papers.json').read_text())
    metadata = json.loads((ROOT / 'data/paper_details.json').read_text())
    path = ROOT / 'docs/RELEVANCE_REVIEW.md'
    output = render(data, metadata)
    if args.check:
        if not path.exists() or path.read_text() != output:
            raise SystemExit('Relevance report is stale. Run python3 scripts/generate_relevance_review.py')
        print('PASS: Relevance report matches shared scope evidence.')
    else:
        path.write_text(output)


if __name__ == '__main__':
    main()
