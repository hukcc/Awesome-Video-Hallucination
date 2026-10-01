import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { DEFAULTS, ROUTES, SCOPE_LABELS, groupPapers, filterPapers, normalizeSearch, sortPapers, readState, stateQuery, resourcesFor, trainingValue, bibtexFor, markdownFor, paperKey } from '../assets/catalog.mjs';

const data = JSON.parse(readFileSync(new URL('../data/papers.json', import.meta.url)));
const metadata = JSON.parse(readFileSync(new URL('../data/paper_details.json', import.meta.url)));
const papers = groupPapers(data.entries, metadata.papers);
const select = filters => filterPapers(papers, filters);

test('all contributions survive paper-level grouping', () => {
  assert.equal(papers.length, 78);
  assert.equal(data.entries.length, 95);
  assert.equal(papers.reduce((n, p) => n + p.entries.length, 0), data.entry_count);
  assert.equal(new Set(data.entries.map(e => e.id)).size, data.entry_count);
});

test('every paper has a concise, sourced, reviewed summary and controlled task tags', () => {
  assert.deepEqual(Object.keys(metadata.papers).sort(), papers.map(p => p.key).sort());
  for (const paper of papers) {
    const d = paper.detail;
    assert.ok(d.summary.split(/\s+/).length >= 12 && d.summary.split(/\s+/).length <= 40, paper.key);
    assert.ok(d.tasks.length > 0 && d.tasks.every(t => metadata.task_vocabulary.includes(t)));
    assert.equal(new Set(d.tasks).size, d.tasks.length);
    assert.match(d.reviewed_on, /^\d{4}-\d{2}-\d{2}$/);
    assert.ok(d.evidence.includes('Abstract'));
    assert.match(d.source_url, /^https:\/\//);
    if (paper.arxiv_id) assert.ok(d.source_url.startsWith(paper.paper_url + 'v'));
    else assert.equal(d.source_url, paper.paper_url);
    assert.equal(d.published_on.slice(0, 7), paper.date.split('/').reverse().join('-'));
    assert.match(d.added.date, /^\d{4}-\d{2}-\d{2}$/);
    assert.match(d.added.commit, /^[a-f0-9]{40}$/);
  }
});

test('contribution descriptions are concise, distinct within each paper, and searchable', () => {
  for (const paper of papers) {
    for (const entry of paper.entries) {
      const words = entry.description.split(/\s+/).length;
      assert.ok(words >= 12 && words <= 40, entry.id);
    }
    assert.equal(new Set(paper.entries.map(e => e.description)).size, paper.entries.length, paper.key);
  }
  assert.equal(select({ search: 'Harmonic RoPE', type: 'mitigation' })[0].key, '2503.15871');
  const tdpo = data.entries.find(e => e.name === 'Video-thinking (TDPO)');
  assert.ok(tdpo.description.includes('thinking-based direct preference optimization'));
  assert.ok(metadata.papers['2503.19622'].summary.includes('thinking-based'));
});

test('contribution types retain their original totals', () => {
  for (const type of ['benchmark', 'mitigation', 'analysis']) {
    assert.equal(select({ type }).reduce((n, p) => n + p.matches.length, 0), data[type + '_count']);
  }
});

test('filters cannot borrow training status from a different contribution', () => {
  assert.equal(select({ type: 'benchmark', training: 'yes' }).length, 0);
  assert.equal(select({ type: 'benchmark', training: 'no' }).length, 0);
  assert.equal(select({ type: 'benchmark', training: 'na' }).length, 42);
  const result = select({ search: 'DINO-HEAL', type: 'mitigation', training: 'yes' });
  assert.equal(result.length, 1);
  assert.equal(result[0].matches.length, 1);
  assert.equal(result[0].entries.length, 2);
});

test('all metadata filters can be combined on a real contribution', () => {
  const target = data.entries.find(e => e.name === 'DINO-HEAL');
  const f = Object.fromEntries(['type', 'mechanism', 'category', 'subtype', 'venue'].map(k => [k, target[k]]));
  const result = select({ ...f, year: String(target.year), resource: 'code', training: 'yes', task: 'Motion Understanding' });
  assert.equal(result.length, 1);
  assert.equal(result[0].key, '2412.03735');
});

test('all query terms match independently and case-insensitively', () => {
  assert.ok(select({ search: 'temporal DINO' }).some(p => p.key === '2412.03735'));
  assert.deepEqual(select({ search: 'temporal DINO' }).map(p => p.key), select({ search: 'dino TEMPORAL' }).map(p => p.key));
  assert.equal(select({ search: 'DINO nonexistentzz' }).length, 0);
});

test('VideoLLM spelling variants have identical results', () => {
  const variants = ['VideoLLMs', 'video llm', 'Vid-LLM', 'Video-LLMs', 'video large language models'];
  for (const term of variants) {
    assert.equal(normalizeSearch(term), 'videollm');
    assert.deepEqual(select({ search: term }).map(p => p.key), select({ search: variants[0] }).map(p => p.key));
  }
});

test('old method names remain searchable but current training flags win', () => {
  const vissres = select({ search: 'STSCD' });
  assert.equal(vissres.length, 1);
  assert.equal(vissres[0].entries[0].name, 'ViSSRes');
  assert.equal(trainingValue(vissres[0].entries[0]), 'no');
  assert.equal(select({ search: 'STSCD', training: 'yes' }).length, 0);
  assert.equal(select({ search: 'VideoPLR' })[0].entries[0].name, 'Video-DPL');
});

test('missing resource filters and resource merging are consistent', () => {
  for (const p of select({ resource: 'code' })) assert.ok(resourcesFor(p).some(r => r.kind === 'code'));
  for (const p of select({ resource: 'missing-code' })) assert.ok(p.matches.every(e => !e.resources.code));
  const sample = select({ search: '2412.03735' })[0];
  const links = resourcesFor(sample);
  assert.equal(links.length, new Set(links.map(r => r.kind + r.url)).size);
});

test('resource links do not leak across nonmatching contributions', () => {
  const sample = structuredClone(data.entries[0]);
  const other = { ...sample, id: 'test-method', type: 'mitigation', training_free: '\u2714', resources: { ...sample.resources, code: 'https://example.com/method' } };
  sample.resources.code = null;
  const grouped = groupPapers([sample, other], metadata.papers);
  assert.equal(filterPapers(grouped, { type: 'benchmark', resource: 'code' }).length, 0);
  assert.ok(!resourcesFor(filterPapers(grouped, { type: 'benchmark' })[0]).some(r => r.kind === 'code'));
});

test('sorting is chronological, stable, and does not mutate the input', () => {
  const snapshot = papers.map(p => p.key);
  const old = sortPapers(papers, 'oldest');
  const recent = sortPapers(papers, 'newest');
  assert.equal(old[0].key, '2303.02961');
  assert.equal(recent[0].key, '2609.36628');
  assert.deepEqual(papers.map(p => p.key), snapshot);
  const titles = sortPapers(papers, 'title').map(p => p.title);
  assert.deepEqual(titles, [...titles].sort((a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' })));
});

test('recently added uses repository history, not publication date', () => {
  const results = sortPapers(papers, 'added');
  assert.ok(results.slice(0, 7).every(p => p.detail.added.date === '2026-10-01'));
  const a = { ...papers[0], key: 'old-recent', detail: { published_on: '2020-01', added: { date: '2026-10-01' } } };
  const b = { ...papers[0], key: 'new-earlier', detail: { published_on: '2026-09', added: { date: '2026-09-01' } } };
  const unknown = { ...a, key: 'unknown', detail: { published_on: '2026-10' } };
  assert.deepEqual(sortPapers([b, unknown, a], 'added').map(p => p.key), ['old-recent', 'new-earlier', 'unknown']);
});

test('shared URLs round-trip every filter, sort, view, and tab', () => {
  const f = { ...DEFAULTS, search: 'video llm A&B', task: 'Video QA', route: 'Decoding', scope: 'direct', type: 'mitigation', mechanism: 'Dynamic Distortion', category: 'Spatiotemporal Dynamics', subtype: 'Event Misordering', training: 'yes', venue: 'CVPR 2025', year: '2024', resource: 'code', sort: 'added', view: 'cards', tab: 'guide' };
  assert.deepEqual(readState(stateQuery(f)), f);
  assert.equal(stateQuery(DEFAULTS), '');
  assert.equal(readState('?sort=bad&view=bad&tab=bad').sort, 'newest');
  assert.equal(readState('?resource=missing-code').resource, 'missing-code');
});

test('technical routes are controlled, evidence-backed, and contribution-specific', () => {
  for (const entry of data.entries) {
    if (entry.type !== 'mitigation') {
      assert.equal(entry.routes, undefined);
      continue;
    }
    assert.ok(entry.routes.length && entry.routes.every(r => ROUTES.includes(r)), entry.name);
    assert.equal(new Set(entry.routes).size, entry.routes.length);
    assert.equal(entry.routes.includes('Training'), trainingValue(entry) === 'no', entry.name);
    assert.ok(metadata.papers[paperKey(entry)].source_url);
  }
  assert.equal(select({ type: 'benchmark', route: 'Training' }).length, 0);
  assert.equal(select({ training: 'yes', route: 'Training' }).length, 0);
  assert.equal(select({ search: 'DINO-HEAL', route: 'Grounding' })[0].matches.length, 1);
  assert.ok(select({ search: 'TriCD', route: 'Decoding', training: 'no' }).length);
  assert.equal(select({ route: 'Unknown' }).length, 0);
});

test('relevance judgments retain evidence and leave related-work decisions pending', () => {
  for (const paper of papers) {
    const review = paper.detail.scope_review;
    assert.ok(Object.hasOwn(SCOPE_LABELS, review.scope));
    assert.ok(review.reason && review.evidence.includes('Abstract'));
    assert.match(review.source_url, /^https:\/\//);
    assert.match(review.reviewed_on, /^\d{4}-\d{2}-\d{2}$/);
    assert.equal(review.decision, review.scope === 'related' ? 'pending-manual-review' : 'retain');
  }
  assert.equal(select({ scope: 'related' }).length, 8);
  assert.equal(select({ scope: 'direct' }).length + select({ scope: 'broader' }).length + select({ scope: 'related' }).length, papers.length);
  for (const key of ['2501.00584', '2503.21459', '2604.20937', '2601.07761', '2604.20473']) {
    assert.equal(metadata.papers[key].scope_review.scope, 'broader', key);
  }
  assert.equal(select({ scope: 'unknown' }).length, 0);
  const missing = structuredClone(papers[0]);
  delete missing.detail.scope_review;
  assert.equal(filterPapers([missing], { scope: 'direct' }).length, 0);
  assert.equal(filterPapers([missing], { scope: 'unreviewed' }).length, 1);
});

test('reading guide uses the verified thinking-based TDPO definition', () => {
  const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
  assert.ok(html.includes('thinking-based direct preference optimization'));
  assert.ok(!html.includes('temporal preference optimization'));
});

test('empty and unknown queries do not silently show all papers', () => {
  assert.equal(select({ venue: 'Unknown venue' }).length, 0);
  assert.equal(select({ subtype: 'Unknown subtype' }).length, 0);
  assert.equal(select({ task: 'Unknown task' }).length, 0);
  assert.equal(select({ search: '   ' }).length, papers.length);
  assert.equal(select({ search: '---' }).length, 0);
  assert.equal(select({ search: '\u4e2d\u6587' }).length, 0);
});

test('citations retain identity and do not invent venue metadata', () => {
  const p = papers.find(p => p.key === '2412.03735');
  const bib = bibtexFor(p);
  assert.ok(bib.includes('archivePrefix = {arXiv}'));
  assert.ok(bib.includes(p.detail.authors[0]));
  assert.ok(!bib.includes('journal =') && !bib.includes('booktitle ='));
  assert.ok(markdownFor(p).includes(p.paper_url));
  const special = { ...p, title: 'A & B: 50% {test}_$' };
  assert.ok(bibtexFor(special).includes('A \\& B: 50\\% \\{test\\}\\_\\$'));
});

test('previous contributor resources and exclusions are preserved', () => {
  const distraction = data.entries.find(e => e.name === 'DistractionBench');
  assert.equal(distraction.resources.code, 'https://github.com/lab-flair/video-llm-boe');
  assert.equal(distraction.resources.dataset, 'https://huggingface.co/datasets/lab-flair/VideoLLM-BoE');
  assert.ok(!data.entries.some(e => ['2605.08974', '2609.35368', '2609.34330', '2609.12818', '2609.03756'].includes(e.arxiv_id)));
  assert.ok(data.entries.every(e => metadata.papers[paperKey(e)]));
});
