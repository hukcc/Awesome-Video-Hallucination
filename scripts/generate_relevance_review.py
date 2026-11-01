#!/usr/bin/env python3
"""Generate the relevance review from the same evidence records used by the browser."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPES = [('related', 'Related Work'), ('broader', 'Broader Evaluations'), ('direct', 'Direct Focus')]


def render(data, metadata):
    groups = defaultdict(list)
    for entry in data['entries']:
        groups[entry['arxiv_id'] or entry['paper_url']].append(entry)
    reviews = {key: metadata['papers'][key]['scope_review'] for key in groups}
    counts = Counter(r['scope'] for r in reviews.values())
    introductions = sum('Introduction' in r['evidence'] for r in reviews.values())
    pending = sum(r['decision'] == 'pending-manual-review' for r in reviews.values())
    lines = ['# Relevance Review', '',
             'Paper-level editorial scope assessment, not a quality ranking. '
             'The separate [benchmark audit](BENCHMARK_REVIEW.md) applies the stricter contribution-level '
             'inclusion rule and records removed, narrowed, and reclassified entries. '
             'The [53-method audit](METHOD_REVIEW.md) independently records interventions, evaluation limits, '
             'training requirements, and 11 proposed moves awaiting approval. '
             'Original-survey contributions and accepted community contributions are protected from scope-driven removal.', '',
             f'Coverage: **{len(groups)} papers / {len(data["entries"])} contributions**. '
             f'All abstracts were reviewed; **{introductions} papers** additionally received '
             'introduction review, with evaluation sections inspected where indicated. '
             'This is not a full-text audit of every paper.', '',
             f'Latest review: **{max(r["reviewed_on"] for r in reviews.values())}**. '
             f'**{counts["direct"]} direct-focus**, **{counts["broader"]} broader-evaluation**, '
             f'and **{counts["related"]} related-work assessments**; **{pending}** remain pending manual decisions.', '',
             '## Criteria', '',
             '- **Direct focus:** hallucination or unsupported video-grounded factual claims are an explicit research objective, '
             'diagnostic target, or mitigation target. This includes caption factuality and audio-visual hallucinations.',
             '- **Broader evaluation:** a general video task includes a concrete hallucination diagnostic, '
             'dedicated subset, or evidence-verification evaluation. Only that supported scope should be claimed.',
             '- **Related work (review):** grounding, QA accuracy, or self-correction is relevant, but the '
             'reviewed evidence does not establish a dedicated hallucination evaluation, or uses a substantially '
             'different definition. These are proposals for manual review, not assertions that a paper is irrelevant.', '',
             'The labels apply at paper level. A benchmark and method in the same paper can have different '
             'degrees of relevance. A paper-level label does not override benchmark eligibility. '
             'The benchmark audit does not newly approve or remove sibling mitigation contributions. '
             'The method audit is contribution-specific: a direct-focus paper can still contain a broader method. '
             'Its 11 pending method recommendations are distinct from the paper-level queue below. '
             'Scientific scope labels do not override original-survey or community preservation.', '',
             '## Manual Decision Queue', '',
             f'Review the {pending} unprotected related-work candidates below before moving any entry. '
             'VTG-LLM remains related in scientific scope but is retained as original-survey content, '
             'not a pending move. Decide whether '
             'coordinate/timestamp errors and general QA/correction metrics meet the intended collection scope. '
             'A move to Related Work is '
             'preferable to deletion when the paper remains useful background.', '',
             'CoE, Video-ToC, and SToP include specific hallucination evaluations despite broad titles. '
             'OVBench, VideoHallu, and RoadSocial are restored under original-survey preservation; '
             'their scope assessments remain unchanged. '
             'EchoPrune remains excluded; it must not be conflated with SToP.', '',
             '## Contribution-Level Caveats', '',
             '- **GameplayQA:** restored as an accepted community contribution from '
             '[PR #2](https://github.com/hukcc/Awesome-Video-Hallucination/pull/2), with its original category and resources. '
             'It remains a broader benchmark, not a dedicated hallucination benchmark; community preservation '
             'does not override the scientific scope assessment.',
             '- **VideoChat-Online / OVBench:** both original-survey contributions are retained. '
             'The model remains a general streaming-video architecture, and OVBench includes a hallucination task '
             'within a broader evaluation suite.',
             '- **Vript-HAL / Vriptor:** only Vript-HAL is listed as the benchmark, while the corpus, other benchmark tasks, '
             'and captioning model have broader purposes. Do not transfer a subset-level claim to the whole suite.',
             '- **VHD / TRACE-RC:** the method changes reliability ordering and accepted coverage, not model answers. '
             'Its current placement means selective risk reduction, not factual correction; '
             'the method audit proposes moving it to related work pending approval.',
             '- **FactVC / DualFact:** the benchmark entries now name their actual factuality datasets. '
             'The metric/framework names remain searchable aliases; caption factuality is not identical to general QA accuracy.',
             '- **VideoHEDGE:** retained as a hallucination-detection evaluation study on SoccerChat, not a new benchmark '
             'or a method that corrects answers.',
             '- **CMM / EmotionHallucer:** the listed benchmark scope is limited to video/audio-visual conditions; '
             'standalone audio, image, and text evaluation does not establish video relevance.', '',
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
            if review['decision'] == 'retain-original-survey':
                reason = 'Retained as original-survey content; not a pending move. ' + reason
            evidence = review['evidence'].replace('|', '\\|')
            lines.append(f'| {names} | {reason} | [{evidence}]({review["source_url"]}) |')
        lines.append('')
    lines += ['## Maintenance', '',
              'Edit `scope_review` in `data/paper_details.json`, then run '
              '`python3 scripts/generate_relevance_review.py`. A new paper without a scope review is shown as '
              'Unclassified in the browser, never silently classified as direct-focus. '
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
