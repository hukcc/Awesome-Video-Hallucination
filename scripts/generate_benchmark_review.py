#!/usr/bin/env python3
"""Render the contribution-level benchmark audit, including excluded records."""

import argparse
import json
from collections import Counter
from pathlib import Path

from generate_readme import resource_badge

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = [('remove', 'Removed From the Benchmark List'),
             ('retain_community', 'Retained Community Contributions'),
             ('narrow', 'Narrowed or Corrected Scope'),
             ('reclassify', 'Reclassified'), ('retain', 'Retained Benchmarks')]


def render(audit):
    counts = Counter(r['decision'] for r in audit['records'])
    lines = ['# Benchmark Scope Audit', '',
             f'Reviewed **{audit["reviewed_on"]}**. All **{len(audit["records"])} pre-audit benchmark entries** '
             'received abstract, introduction, and task/metric review against the versioned arXiv text or official publisher PDF. '
             'This is a scope and contribution-type audit, not a replication of experiments or a full-paper methodological endorsement.', '',
             f'Outcome: **{counts["retain"]} retained**, **{counts["narrow"]} narrowed or corrected**, '
             f'**{counts["remove"]} removed from the benchmark list**, and **{counts["reclassify"]} reclassified as evaluation analysis**. '
             f'An additional **{counts["retain_community"]} community contribution is retained with a broader-scope label**. '
             f'The main list now has **{counts["retain"] + counts["narrow"] + counts["retain_community"]} benchmark contributions**, '
             f'of which **{counts["retain"] + counts["narrow"]} meet the strict scope**. '
             'The benchmark-only pass preserved all 53 mitigation contributions and the existing analysis. '
             'The subsequent [method audit](METHOD_REVIEW.md) records method-specific corrections and pending scope recommendations.', '',
             '## Inclusion Rule', '',
             '- Previously accepted community contributions are protected from automatic removal. '
             'GameplayQA was restored after the initial strict audit under the owner\'s preservation instruction. '
             'Its [accepted PR #2](https://github.com/hukcc/Awesome-Video-Hallucination/pull/2), '
             'original category and resources remain visible; retention does not change the broader-scope assessment. '
             'Disputed community entries require entry-specific human approval before removal or relocation.',
             '- The benchmark must centrally evaluate unsupported or contradicted language-model claims about input video, '
             'including video-caption factuality, targeted adversarial QA, hallucination detection, and audio-visual conflicts in videos.',
             '- General video QA, caption quality, object consistency, evidence grounding, or reasoning benchmarks do not qualify '
             'solely because they discuss hallucinations or contain one hallucination task/metric.',
             '- A separately named, dedicated hallucination dataset can be listed from a broader paper '
             '(KPM-HA and Vript-HAL). A generic subtask is not promoted into an invented standalone benchmark.',
             '- Dedicated multimodal hallucination benchmarks are restricted to their actual video/audio-visual conditions. '
             'Audio-only, image-only, and text-only tests do not count as video evidence.',
             '- Detection frameworks and scoring metrics are not dataset names. Named factuality datasets are listed as such; '
             'a detection study without a new benchmark belongs in evaluation analyses.', '',
             'These are curator judgments under the stricter user-approved collection scope. Exclusion does not mean '
             'a paper is false, scientifically weak, or unrelated. In particular, VideoHallu, STRAND, and FlexBench remain '
             'relevant background but fall outside this conservative benchmark boundary. Existing sibling methods were not '
             'removed or newly approved by this benchmark-only review.', '',
             '## Evidence Register', '',
             'The protocol column identifies the actual measured outcome. Accuracy, consistency, conditional answer-flip rates, '
             'and free-form hallucination rates are not interchangeable. Linked sections record what was inspected, '
             'not a claim that every appendix was read.', '']
    for decision, heading in DECISIONS:
        lines += [f'### {heading}', '', '| Entry | Decision and Scope | Task / Metric and Inspected Evidence |',
                  '| --- | --- | --- |']
        for row in sorted((r for r in audit['records'] if r['decision'] == decision),
                          key=lambda r: r['original_entry']['name'].casefold()):
            original = row['original_entry']
            label = f'[{original["name"]}]({original["paper_url"]})'
            if row['listed_name']:
                label += f'<br>Listed: [{row["listed_name"]}](../README.md#paper-{row["entry_id"]})'
            reason = row['rationale'].replace('|', '\\|')
            protocol = row['protocol'].replace('|', '\\|')
            evidence = f'[{row["inspected_sections"]}]({row["source_url"]})'
            lines.append(f'| {label} | {reason} | {protocol}<br>{evidence} |')
        lines.append('')
    lines += ['## Archived Resources', '',
              'Original paper identities and resource badges for removed benchmark contributions are retained below. '
              'They are provenance, not active benchmark recommendations. Resources may serve a whole paper, not only '
              'its hallucination component. The machine-readable register also preserves original contribution records '
              'and historical metadata snapshots, including GameplayQA before its subsequent restoration.', '']
    for row in audit['records']:
        if row['decision'] != 'remove':
            continue
        original = row['original_entry']
        badges = ' '.join(resource_badge(kind, url) for kind, url in original['resources'].items() if url)
        lines += [f'### {original["name"]}', '', f'[{original["title"]}]({original["paper_url"]})', '',
                  badges or 'No verified resource link was recorded.', '']
    lines += ['## Maintenance', '',
              'Evidence and original records: [`data/benchmark_review.json`](../data/benchmark_review.json). '
              f'Baseline: [`{audit["baseline_commit"][:7]}`]'
              f'(https://github.com/hukcc/Awesome-Video-Hallucination/commit/{audit["baseline_commit"]}). '
              'Update the register after primary-source review and regenerate this report with '
              '`python3 scripts/generate_benchmark_review.py`. Tests enforce active-benchmark review coverage, '
              'excluded-entry absence, preserved resources, and the original non-benchmark snapshots '
              'retained by the subsequent method audit.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    audit = json.loads((ROOT / 'data/benchmark_review.json').read_text())
    path = ROOT / 'docs/BENCHMARK_REVIEW.md'
    output = render(audit)
    if args.check:
        if not path.exists() or path.read_text() != output:
            raise SystemExit('Benchmark report is stale. Run python3 scripts/generate_benchmark_review.py')
        print('PASS: Benchmark report matches the contribution-level evidence register.')
    else:
        path.write_text(output)


if __name__ == '__main__':
    main()
