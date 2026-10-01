# Collection Curation

## Sources of Truth

- `data/papers.json` is the shared contribution catalog for the README, browser, and taxonomy. It retains one entry per benchmark, mitigation method, or evaluation analysis, including a contribution-specific `description`. Do not remove a contribution merely because another entry cites the same paper.
- `scripts/generate_readme.py` generates the README task index and paper tables between marked comments. Edit the shared data, not generated rows. Content outside these regions remains hand-maintained.
- `data/paper_details.json` contains one record per distinct paper, keyed by arXiv ID or publisher URL. It adds a curator-written summary, task tags, primary-source link, evidence section, review date, first-publication date, and first recorded README appearance.
- `figs/taxonomy_tree.tex` is generated from `data/papers.json`. The three taxonomy image aliases must remain identical.
- `new_papers.md` records discovery and inclusion decisions. Automated discovery is not automatic admission to the curated collection.

## Editorial Rules

Read the official abstract before writing a summary or assigning tasks. Read the introduction or relevant method/evaluation sections when the abstract is insufficient, especially for training requirements or version changes. Link the reviewed arXiv version where possible, or the official publisher record. Record the sections actually inspected; do not imply a full-text review from an abstract alone.

Write one concise English sentence describing the contribution, not unsupported claims of superiority. Aim for 15-25 words (12-40 when needed for precision). A benchmark description explains what is evaluated; a method description explains the intervention; an analysis description explains the question investigated. Different contributions from one paper need different descriptions. Their evidence is recorded in the paper-level source record. General video-understanding papers should not be described as dedicated hallucination benchmarks unless the source supports that description. Task tags are selective discovery aids, not an exhaustive scope assessment or a new relevance verdict.

Use these task labels consistently:

| Tag | Scope |
| --- | --- |
| Video QA | Questions answered from video evidence |
| Video Captioning | Generating, assessing, or verifying video descriptions |
| Temporal Grounding | Locating query-relevant events or evidence in time |
| Audio-Visual Understanding | Joint use or assessment of auditory and visual evidence |
| Long-Video Understanding | Explicit long-video evaluation or methods |
| Motion Understanding | Fine-grained actions, limb motion, or motion attribution |
| Video Reasoning | Event order, causal relations, or multi-step visual reasoning |
| Hallucination Detection | Factuality verification, hallucination diagnosis, or answer reliability estimation |
| Video Understanding | Broad video-model methods or tasks when a narrower label is not established by the reviewed source |

Keep the existing mechanism/category/subtype taxonomy. A primary placement is not exclusive coverage. A paper can have several task tags and multiple contributions.

Training-free means the listed method does not require learning additional parameters for its intervention. Freezing the base model while training an auxiliary module is not training-free. Benchmarks and analyses use `null` (not applicable), not `false`.

## Dates and Versions

- `date` / `year` in `papers.json` refer to first arXiv submission, or publisher issue date when no arXiv record is used. Venue years may differ.
- `published_on` uses the verified day when available; month-only publisher dates remain month-only. Never invent a day for sorting.
- `added.date` and `added.commit` point to the earliest recorded appearance in README Git history. This is a repository addition date, not a publication or last-revision date. Older papers present at the initial import share that import date.
- For a new uncommitted paper, use `added: null` until its first inclusion commit exists. Backfill from that commit before publishing the browser; never substitute the paper date. Unknown addition dates sort after known dates.
- When a revision changes a method name, update README, JSON, and the tree together. Preserve stable entry IDs, official repository URLs, and useful old names in `aliases`.
- Copied BibTeX cites the arXiv record as `@misc`, with source-retrieved authors when available. Publisher-only entries use a basic title/year/URL record. It is not a fabricated proceedings citation; the publisher page is the source for full publication metadata.

## Browser Semantics

The default unit is a paper. All original contributions remain visible under its details. Type, mechanism, category, subtype, venue, resource, and training filters must match the same contribution. The result count distinguishes matching papers from matching contributions. Resource links in the main row belong to matching contributions; details retain resources for all contributions.

Search uses all query words, independent of order, across titles, contribution names, summaries, tasks, authors, venues, and IDs. Common forms of VideoLLM, Video LLM, Vid-LLM, and Video Large Language Model are normalized. It is keyword search, not semantic retrieval.

Filter, sort, layout, and reading-guide state are encoded in the URL. Desktop defaults to a table; narrow screens use cards. Publication sorting and repository-addition sorting are separate. The reading guide is an editorial path across complementary topics, not a performance ranking.

## README Semantics

The task index links to stable contribution anchors in the same README. Task labels and paper counts are paper-level; benchmark and method links from one paper appear together. The index is collapsed below the original introduction, overview figure, contents, and news. Every indexed paper retains its full taxonomy placement below.

Tables remain expanded and use four columns for benchmarks/analyses or five for methods. Preserve the original visual hierarchy: bold linked paper titles, a separate centered contribution-name column, centered metadata, and resource badges. Contribution descriptions remain visible as secondary text below titles. Each subtype is sorted by verified first-publication date descending, with alphabetical ties. Venue and publication date are separate concepts in one cell. Short names, full titles, contribution descriptions, resource badges, and related-contribution anchors are generated from the shared data. Preserve the original Page, Code, Dataset, and Leaderboard badge styles and the training-free check/cross symbols. Dataset badges must match their hosting platform; do not label Kaggle or other hosts as Hugging Face. Keep the top-level repository badges, figures, news, and citation content when improving navigation. Missing resources mean no verified link is recorded, not that the resource does not exist. The large taxonomy figure and resource legend are collapsed by default.

## Update Checklist

1. Verify scope, paper identity, current version, venue, and official resources against primary sources.
2. Update paper entries and contribution descriptions, keeping stable IDs and prior contributors' valid links.
3. Add or revise the paper-level summary, tasks, source URL, evidence section, review date, authors, and dates. Pin reviewed arXiv versions.
4. Backfill the first README inclusion commit and date from Git history, not the current modification date.
5. Run `python3 scripts/generate_readme.py` to regenerate the task index and paper list. Update the hand-maintained overview/counts and concise news only when necessary.
6. Regenerate the LaTeX taxonomy if entry names or placements change; compile and inspect the output, then refresh all three PNG aliases.
7. Run the checks below and test README task/related links, desktop/mobile layouts, combined filters, empty states, shared URLs, browser history, copy actions, and the reading guide.

```sh
node --test tests/catalog.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/generate_readme.py --check
python3 scripts/check_catalog.py
python3 scripts/generate_taxonomy_tree.py --check
```

GitHub Pages runs these checks before deployment; pull requests run the same validation. Automated checks enforce consistency and coverage, not scientific correctness. Scientific judgments still require source review.

## Review Note: 2026-10-01

All 78 distinct papers received abstract-based summaries and task tags, with individually linked sources. Existing inclusion decisions and all 95 contribution records were retained. Two version discrepancies were corrected after reading the current abstracts and introductions:

- [ViSSRes, arXiv v2](https://arxiv.org/html/2601.22574v2): the current method trains a residual aligner (also confirmed in Section 4.3). Replace the old STSCD display name and change training-free to No. Keep STSCD searchable.
- [Video-DPL, arXiv v3](https://arxiv.org/html/2511.18463v3): update the old VideoPLR display name. Keep VideoPLR searchable and preserve the official repository URL.

This pass enriches discovery metadata; it does not claim a new full-text relevance audit of every paper.

The README description pass also checked the [HAVEN introduction](https://arxiv.org/html/2503.19622v1): TDPO means **thinking-based**, not temporal, direct preference optimization. The shared summary and method description use the source's terminology.

## Icon Attribution

The browser uses unmodified SVG assets from [Lucide 0.468.0](https://github.com/lucide-icons/lucide/tree/0.468.0/icons). Their license is retained in `assets/icons/LICENSE`. No runtime icon CDN is required.
