#!/usr/bin/env python3
"""Render the source-backed method audit without applying pending scope moves."""

import argparse
import json
from collections import Counter
from pathlib import Path

from generate_readme import resource_badge

ROOT = Path(__file__).resolve().parent.parent


def render(audit):
    counts = Counter(r['recommendation'] for r in audit['records'])
    pending = counts['move_to_related']
    retained = counts['retain'] + counts['correct'] + counts['retain_survey']
    lines = ['# Method Scope Audit', '',
             f'Reviewed **{audit["reviewed_on"]}**. All **{len(audit["records"])} method contributions** received '
             'official abstract, introduction, and relevant method/evaluation review. Sources are pinned arXiv versions '
             'or the official IJCAI PDF. This is a relevance, intervention, and evaluation-evidence audit, '
             'not experimental replication or a claim that every appendix was read.', '',
             f'Outcome: **{retained} retained** (including a method-name correction and '
             f'{counts["retain_survey"]} original-survey preservation decisions) and '
             f'**{pending} proposed moves to related work, awaiting human approval**. '
             'No method has been removed. All existing training-free flags agree with the inspected sources. '
             'Paper URLs, resource badges, stable identifiers, and sibling benchmark decisions are preserved.', '',
             '## Scope Rule', '',
             '- All original-survey contributions remain in their existing categories. '
             'VTG-LLM, Vriptor, and VideoChat-Online are no longer proposed moves. Their broader-scope '
             'assessments remain evidence, not pending removal instructions. Accepted community contributions '
             'are independently protected.',
             '- A core method explicitly targets unsupported or contradicted claims about input video. '
             'Targeted post-hoc claim verification and audio-visual hallucination interventions qualify; '
             'general QA, grounding, efficiency, or reliability methods are not automatically dedicated mitigation methods.',
             '- Research objective and strength of evaluation are separate. Vista-LLaMA, MMA, and Temporal Insight '
             'explicitly target hallucinations but have indirect or narrow evaluation evidence. '
             'They are retained with limitations, not presented as validated by dedicated hallucination rates.',
             '- Dedicated hallucination tests in a broad method are real evidence, but do not by themselves make '
             'that method a core hallucination intervention. CoE, Video-ToC, and SToP are conservative boundary '
             'recommendations for manual review, not claims that their hallucination experiments are absent.',
             '- Frozen backbones do not imply training-free operation when an auxiliary classifier, aligner, '
             'controller, or patcher is learned. Input-only gradient optimization with fixed parameters is distinguished '
             'from parameter learning; off-the-shelf pretrained components do not imply new task-specific training.',
             '- Detection, answer selection, selective risk, grounding accuracy, omission rates, and generation '
             'hallucination rates are different outcomes. Multimodal aggregate gains are not video-only gains.', '',
             'These are curator judgments about collection scope, not scientific-quality rankings. '
             'A method and benchmark from the same paper are reviewed independently. '
             'Pending recommendations below do not remove Vript-HAL, VHD, or any other sibling benchmark.', '',
             '## Manual Decision Queue', '',
             '| Method | Reason to Consider Related Work |', '| --- | --- |']
    ordered = sorted(audit['records'], key=lambda r: r['listed_name'].casefold())
    for record in ordered:
        if record['recommendation'] == 'move_to_related':
            lines.append(f'| [{record["listed_name"]}](#method-{record["entry_id"]}) | {record["rationale"]} |')
    lines += ['', '## Corrections and Evidence Limits', '',
              '- **MoPE:** name the mitigation entry **GRPO with MoPE**, as in Section 4.3. '
              'MoPE is the parsing/evaluation component; the listed intervention uses it as a training reward. '
              'The old name remains an alias.',
              '- **PEP-MEK:** expand as **Predict-Explain-Predict with Modality and Emotion Knowledge**, '
              'not perception-enhanced prompting or a memory-based mechanism. Table 3 reports mixed-modality '
              'results, not isolated video gains.',
              '- **ProCap:** automatic Temporal Inconsistency measures missing salient objects. '
              'Its separate human inconsistency ratings address unsupported content; a rating change is not an incidence rate.',
              '- **GroundedVQA:** tags drafted claims without rewriting them. Its evidence is 40 claims from 12 '
              'questions on one animated video, not a broad benchmark.',
              '- **Video-DPL / TRACE-RC:** evaluator accuracy and selective-risk ranking must not be reported as '
              'a reduction in hallucinations in all generated answers. TRACE-RC never changes base answers.',
              '- **C-TCD:** assumes a scene-matched counterfactual counterpart at inference. '
              '**ELV-Halluc-DPO:** the best SAH-ratio result uses in-video pairs; the combined 8k setting is different.',
              '- **mrDPO:** total error combines missing and hallucinated events. '
              '**VideoHallu-GRPO:** the source labels its training GRPO, but Equation 2 has a pairwise DPO form; '
              'the implementation has not been independently resolved or reproduced.', '',
              '## Evidence Register', '',
              'Each entry records the inspected sections, intervention, actual evaluation, training requirement, '
              'and recommendation. Source-file SHA-256 hashes in the machine-readable register identify the '
              'downloaded evidence used for this pass; they are not a guarantee that an HTML rendering will remain byte-identical.', '']
    for recommendation, heading in [('move_to_related', 'Pending Scope Decisions'),
                                    ('retain_survey', 'Retained Original-Survey Methods'),
                                    ('correct', 'Retained With a Name Correction'),
                                    ('retain', 'Retained Methods')]:
        lines += [f'### {heading}', '']
        for record in ordered:
            if record['recommendation'] != recommendation:
                continue
            entry = record['original_entry']
            lines += [f'<a id="method-{record["entry_id"]}"></a>', '',
                      f'#### {record["listed_name"]}', '',
                      f'[{entry["title"]}]({entry["paper_url"]}) '
                      f'([catalog entry](../README.md#paper-{record["entry_id"]})). '
                      f'**Training-free: {"Yes" if record["training_free"] else "No"}.**', '',
                      f'- **Intervention:** {record["intervention"]}',
                      f'- **Evaluation:** {record["evaluation"]}',
                      f'- **Assessment:** {record["rationale"]}',
                      f'- **Inspected:** [{record["inspected_sections"]}]({record["source_url"]}).', '']
            if record.get('preservation_source'):
                lines += [f'- **Retention:** [{record["preservation_reason"]}]({record["preservation_source"]}).', '']
            if recommendation == 'move_to_related':
                badges = ' '.join(resource_badge(kind, url) for kind, url in entry['resources'].items() if url)
                if badges:
                    lines += [badges, '']
    lines += ['## Maintenance', '',
              'Evidence, recommendations, and original contribution snapshots are in '
              '[`data/method_review.json`](../data/method_review.json). '
              f'Baseline: [`{audit["baseline_commit"][:7]}`]'
              f'(https://github.com/hukcc/Awesome-Video-Hallucination/commit/{audit["baseline_commit"]}). '
              'Regenerate with `python3 scripts/generate_method_review.py`. '
              'Tests enforce complete method coverage, training flags, preserved identities/resources, and '
              'retention of pending candidates. Scope moves require explicit human approval and a synchronized '
              'README, browser, taxonomy, and audit update.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    audit = json.loads((ROOT / 'data/method_review.json').read_text())
    path = ROOT / 'docs/METHOD_REVIEW.md'
    output = render(audit)
    if args.check:
        if not path.exists() or path.read_text() != output:
            raise SystemExit('Method report is stale. Run python3 scripts/generate_method_review.py')
        print('PASS: Method report matches the contribution-level evidence register.')
    else:
        path.write_text(output)


if __name__ == '__main__':
    main()
