# Collection Curation

## Sources of Truth

- `data/papers.json` is the shared contribution catalog for the README, browser, and taxonomy. It retains one entry per benchmark, mitigation method, or evaluation analysis, including a contribution-specific `description`. Do not remove a contribution merely because another entry cites the same paper.
- `scripts/generate_readme.py` generates the README task index and paper tables between marked comments. Edit the shared data, not generated rows. Content outside these regions remains hand-maintained.
- The same generator renders a collapsed Recently Added section from the latest verified repository-addition date, capped at eight papers. It groups contributions from the same paper and never substitutes publication dates for missing addition records.
- `data/paper_details.json` contains one record per distinct paper, keyed by arXiv ID or publisher URL. It adds a curator-written summary, task tags, primary-source link, evidence section, review date, first-publication date, and first recorded README appearance.
- `figs/taxonomy_tree.tex` is generated from `data/papers.json`. The three taxonomy image aliases must remain identical.
- `new_papers.md` records discovery and inclusion decisions. Automated discovery is not automatic admission to the curated collection.
- `data/benchmark_review.json` records contribution-level benchmark eligibility, inspected task/metric evidence, original entries, and archived metadata. `scripts/generate_benchmark_review.py` renders the complete audit, including exclusions.
- `data/method_review.json` records each method's intervention, actual evaluation, training requirement, inspected sections, and scope recommendation. `scripts/generate_method_review.py` renders the audit. Pending moves remain in the catalog until approved.
- `community_contributions` in each paper's metadata records accepted issue/PR provenance, the contributor, the affected entry, and protected paper/resource links. These records do not establish scientific relevance.
- `data/survey_coverage.json` maps the original survey's 19 benchmark and 22 method entries to stable catalog IDs and exact source rows. Tests protect their continued inclusion and category placement.

## Original Survey Preservation

Retain papers appearing anywhere in the [original survey, arXiv v1](https://arxiv.org/html/2604.12944v1), including its text, tables, figures, and references. This owner-directed preservation rule takes precedence over scope-driven removal or relocation: a broader research objective is not a reason to remove an existing original-survey contribution. Check the original source and the coverage register before proposing any change to an existing entry. References cited only as background are not automatically added as new benchmarks or methods if they were never in the collection.

All 19 benchmarks and 22 methods in Tables 1 and 2 are preserved. OVBench, VideoHallu, and RoadSocial have been restored to their original benchmark categories. VTG-LLM, Vriptor, and VideoChat-Online are no longer pending moves. Preserve verified name/scope corrections such as Vript-HAL and Video-DPL, original resource badges, stable IDs, and first-addition dates. Retention does not change scientific evidence or turn broad work into dedicated hallucination research.

Display these contributions as ordinary table entries, without new survey-retention labels, audit explanations, or logs on the README or website. Keep the protection mapping and source evidence in maintenance data. The strict eligibility rules below continue to govern new candidates; accepted community contributions remain independently protected.

## Community Contributions

Preserve previously accepted content from issues, pull requests, and other contributors, including paper entries, valid resource links, badges, and contribution attribution. Check issue/PR discussions and Git history before any scope-driven removal. A general relevance-audit instruction does not authorize removing or relocating these contributions; obtain entry-specific human approval first. Corrections to factual descriptions remain source-backed and must not erase provenance.

GameplayQA was accepted in [PR #2 by @wangyz1999](https://github.com/hukcc/Awesome-Video-Hallucination/pull/2). It is restored to its original benchmark category with all three resource badges. Its broader scientific scope remains explicit, so it is not counted among the 32 strict-scope benchmarks. DistractionBench's code and dataset from [PR #3 by @s-honcharenko](https://github.com/hukcc/Awesome-Video-Hallucination/pull/3) remain intact. No standalone issue was returned by the all-state GitHub issue listing during this check; the accepted contributions identified there are these two merged PRs. Unaccepted suggestions are not automatically admitted.

Keep disputed community contributions visible and record the evidence or scope limitations in the audit records. This preservation exception does not turn a general video-understanding benchmark into a dedicated hallucination benchmark. Future updates must record newly accepted community contributions and maintain their regression checks.

Display accepted community contributions as ordinary paper entries, without special community/PR labels or exception notes in the README, browser entry, or taxonomy tree. Preserve provenance, contributor attribution, scope assessments, and the full rationale in the shared metadata and audit records. Standard relevance filtering remains available.

Keep review explanations, audit-report links, and discovery/review logs out of the reader-facing README and browser. Retain the source evidence and maintenance records in the repository; the website does not load or publish standalone audit registers or the discovery log. News covers substantive updates using concise counts or category-level summaries, without naming individual added papers. Keep the existing monthly bullet format; individual paper links belong in the separate Recently Added list and paper tables.

Keep routine listings free of per-paper relevance verdicts, Git commit provenance links, and repeated editorial notes. Retain relevance filtering, factual contribution descriptions, essential video-subset qualifiers, and the training-free legend. Show repository-addition dates in Recently Added and when sorting by addition date; retain full provenance and scope limitations in maintenance data.

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

## Relevance and Technical Routes

### Strict Benchmark Eligibility

For new candidates, the benchmark's core target must be video hallucination: unsupported or contradicted model claims about input video, including caption factuality, hallucination detection, targeted adversarial QA, and audio-visual conflicts. Read the official abstract, introduction, task construction, and relevant scoring protocol before admission. A title, keyword, general QA accuracy, or one hallucination-sensitive metric is not sufficient. Original-survey and accepted community entries remain protected by the preservation rules above.

Do not list a general captioning, reasoning, streaming-video, or object-consistency benchmark solely because it includes a hallucination task. A separately named dedicated hallucination dataset may be listed from a broad paper (for example, KPM-HA or Vript-HAL); do not invent a benchmark name for a general suite's subtask. Limit multimodal hallucination collections to actual video/audio-visual conditions. Use dataset names for datasets, not their associated metric or detection-framework names.

Record every benchmark decision and exact inspected source in `data/benchmark_review.json`, then regenerate the audit. Preserve removed entries and their resource links in that register. Removal of a benchmark does not automatically remove or newly validate a sibling method. Detection studies without a new benchmark may be retained as evaluation analyses, explicitly labeled as detection rather than answer correction.

### Paper-Level Scope and Method Routes

The [method audit](METHOD_REVIEW.md) is contribution-specific and independent of paper-level labels. Core methods explicitly target unsupported video-grounded claims, including dedicated claim verification and audio-visual hallucination interventions. General QA, grounding, efficiency, and reliability methods do not automatically qualify because they mention hallucinations or include a hallucination test. Distinguish the research objective from evaluation strength: direct-focus work with indirect or narrow evidence can be retained with explicit limitations. Never equate detector accuracy, selective risk, grounding IoU, omission, or pooled multimodal scores with hallucination rates in generated video descriptions or answers.

`scope_review` in `data/paper_details.json` records a paper-level editorial assessment, reason, source, inspected sections, review date, and decision status. The [relevance report](RELEVANCE_REVIEW.md) is generated from these records. Direct focus, broader evaluation, and related-work candidates are distinct from taxonomy placement and scientific quality. Related-work candidates remain in the catalog until a human approves a move or removal. Missing scope evidence belongs to the Unclassified filter, never to direct focus; individual listings do not display these verdicts.

Each mitigation contribution has one or more `routes` in `data/papers.json`. These are source-backed discovery labels, not mutually exclusive method classes:

| Route | Meaning |
| --- | --- |
| Decoding | Token selection, generation-time attention/activation intervention, or response selection/termination |
| Training | Parameter learning in the backbone or an auxiliary component, including supervised learning, preference optimization, and reinforcement learning |
| Grounding | Explicit visual evidence selection, localization, alignment, preservation, or reweighting |
| Verification | Explicit factuality, physical consistency, or answer-reliability checks, including checks used as training rewards |

Tags summarize the intervention described in the linked source, not every component used by a model. Benchmark and analysis entries do not borrow routes from a sibling method. Route filtering therefore applies to contributions; relevance filtering applies to papers. Tagging a related-work candidate does not approve its inclusion as a dedicated hallucination method.

## Remote Source Checks

`python3 scripts/check_remote_sources.py` performs read-only GET checks of paper URLs, resource links, README badge images, and pinned evidence links, including method-audit evidence, benchmark-audit evidence and archived resources. It also compares current arXiv submission histories with reviewed versions and flags explicit withdrawal notices for active papers. Results are saved as Markdown and JSON under `reports/remote-sources/`; this output is not committed by default.

The **Audit remote paper sources** workflow runs on relevant pull requests and main-branch updates, and can be started manually. It uploads the reports and displays a run summary; it does not block publication on a transient external failure or edit collection data. There is no recurring schedule. Existing monthly discovery is unchanged.

Treat successful HTTP responses as reachability only. Recheck 404/410 responses before removal; 401/403/429, challenge pages, transport failures, or an unrecognized arXiv record remain unverified. Read a changed paper version before updating evidence. Publisher-only retractions and version changes still require manual publisher review. Automated checks never establish relevance or authenticity on their own.

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

1. Verify scope, paper identity, current version, venue, and official resources against primary sources. Check the original survey and issue/PR provenance first; retain original-survey entries and protect accepted community contributions before proposing removals.
2. Update paper entries and contribution descriptions, keeping stable IDs and prior contributors' valid links.
3. Add or revise the paper-level summary, tasks, source URL, evidence section, review date, authors, and dates. Pin reviewed arXiv versions.
4. Backfill the first README inclusion commit and date from Git history, not the current modification date.
5. Run `python3 scripts/generate_readme.py` to regenerate the task index and paper list. Update the hand-maintained overview/counts and concise news only when necessary.
   Also regenerate `generate_relevance_review.py`, `generate_benchmark_review.py`, and `generate_method_review.py` reports after changing their evidence registers. Review remote-source audit flags before publishing.
6. Regenerate the LaTeX taxonomy if entry names or placements change; compile and inspect the output, then refresh all three PNG aliases.
7. Run the checks below and test README task/related links, desktop/mobile layouts, combined filters, empty states, shared URLs, browser history, copy actions, and the reading guide.

```sh
node --test tests/catalog.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/generate_readme.py --check
python3 scripts/generate_relevance_review.py --check
python3 scripts/generate_benchmark_review.py --check
python3 scripts/generate_method_review.py --check
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

## Review Note: 2026-11-01

All seven November discoveries received official abstract and introduction review. The initial pass admitted OmniCapBench and ARP-CD, excluded four video-generation/editing papers, and deferred Causal Chain Generation. The subsequent user-approved strict benchmark audit supersedes OmniCapBench's initial admission. See the [November decision log](../new_papers.md#reviewed---2026-11-01) for the historical decision and source provenance.

All 43 benchmark entries then received abstract, introduction, and relevant task/metric review: 26 were retained, six narrowed or corrected, ten initially removed from the benchmark list, and VideoHEDGE reclassified as an evaluation analysis. GameplayQA was subsequently restored under the community-preservation rule; OVBench, VideoHallu, and RoadSocial were restored under the original-survey rule. The current collection contains 76 papers and 91 contributions (36 benchmarks, 53 mitigation methods, two analyses). The benchmark-only pass preserved all 53 original methods and the original analysis. The [complete benchmark audit](BENCHMARK_REVIEW.md) retains the initial assessments and the superseding preservation decisions.

The subsequent [method audit](METHOD_REVIEW.md) reviewed all 53 method abstracts, introductions, and relevant method/evaluation sections. It initially recommended retaining 39 and moving 14 to related work; no methods were removed. Original-survey preservation supersedes the proposed moves for VTG-LLM, Vriptor, and VideoChat-Online, leaving 11 pending recommendations. The paper-level queue likewise excludes protected VTG-LLM. MoPE was renamed GRPO with MoPE, PEP-MEK's expansion was corrected, and six descriptions were clarified. Training flags, paper/resource URLs, and stable IDs are unchanged. Original records and scientific scope assessments remain in the audit register. This is source-based scope review, not experimental replication or full-paper endorsement.

The remote audit also identified v2 revisions of MotionHalluc and VidOmni-Bench. Their abstracts, introductions, and relevant evaluation/method sections were checked before updating evidence links. MotionHalluc's summary now uses Perceive-Parse-Verify, and its official code links were added to the benchmark and PPV entries. Existing classifications, dataset links, publication dates, and addition records were retained.

## Icon Attribution

The browser uses unmodified SVG assets from [Lucide 0.468.0](https://github.com/lucide-icons/lucide/tree/0.468.0/icons). Their license is retained in `assets/icons/LICENSE`. No runtime icon CDN is required.
