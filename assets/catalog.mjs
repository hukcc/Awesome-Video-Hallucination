export const TYPE_LABELS = { benchmark: 'Benchmark', mitigation: 'Mitigation', analysis: 'Analysis' };
export const RESOURCE_LABELS = { code: 'Code', dataset: 'Dataset', project: 'Project', leaderboard: 'Leaderboard' };
export const ROUTES = ['Decoding', 'Training', 'Grounding', 'Verification'];
export const SCOPE_LABELS = { direct: 'Direct focus', broader: 'Broader evaluation', related: 'Related work (review)', unreviewed: 'Not reviewed' };
export const DEFAULTS = Object.freeze({
  search: '', type: '', task: '', route: '', scope: '', mechanism: '', category: '', subtype: '',
  training: '', venue: '', year: '', resource: '', sort: 'newest', view: 'auto', tab: 'papers',
});

export function paperKey(entry) {
  return entry.arxiv_id || entry.paper_url;
}

export function normalizeSearch(value) {
  return String(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
    .replace(/\b(?:video|vid)[\s-]*(?:large\s+language\s+models?|llms?)\b/g, 'videollm')
    .replace(/[^a-z0-9.]+/g, ' ').trim();
}

export function groupPapers(entries, details) {
  const groups = new Map();
  for (const entry of entries) {
    const key = paperKey(entry);
    if (!groups.has(key)) {
      groups.set(key, { key, title: entry.title, paper_url: entry.paper_url,
        arxiv_id: entry.arxiv_id, date: entry.date, year: entry.year,
        detail: details[key] || {}, entries: [] });
    }
    groups.get(key).entries.push(entry);
  }
  return [...groups.values()];
}

export function trainingValue(entry) {
  if (entry.training_free === null) return 'na';
  return entry.training_free.includes('\u2714') ? 'yes' : 'no';
}

function matchesResource(entry, resource) {
  if (!resource) return true;
  if (resource === 'missing-code') return !entry.resources.code;
  if (resource === 'missing-project') return !entry.resources.project;
  return Boolean(entry.resources[resource]);
}

export function filterPapers(papers, filters = {}) {
  const f = { ...DEFAULTS, ...filters };
  const words = normalizeSearch(f.search).split(/\s+/).filter(Boolean);
  if (f.search.trim() && !words.length) return [];
  return papers.flatMap(paper => {
    if (f.task && !(paper.detail.tasks || []).includes(f.task)) return [];
    if (f.scope && (paper.detail.scope_review?.scope || 'unreviewed') !== f.scope) return [];
    if (f.year && String(paper.year) !== f.year) return [];
    // Contribution filters must agree on one entry, not borrow a role from another.
    const matches = paper.entries.filter(entry =>
      ['type', 'mechanism', 'category', 'subtype', 'venue'].every(key => !f[key] || entry[key] === f[key]) &&
      (!f.route || (entry.routes || []).includes(f.route)) &&
      (!f.training || trainingValue(entry) === f.training) && matchesResource(entry, f.resource));
    if (!matches.length) return [];
    const haystack = normalizeSearch([
      paper.title, paper.arxiv_id, paper.date, paper.detail.summary,
      ...(paper.detail.tasks || []), ...(paper.detail.aliases || []), ...(paper.detail.authors || []),
      ...matches.flatMap(e => [e.name, e.description, e.type, e.venue, e.category, e.mechanism, e.subtype, ...(e.routes || [])]),
    ].join(' '));
    if (!words.every(word => haystack.includes(word))) return [];
    return [{ ...paper, matches }];
  });
}

function publication(paper) {
  return paper.detail.published_on || paper.date.split('/').reverse().join('-');
}

export function sortPapers(papers, order = 'newest') {
  const title = (a, b) => a.title.localeCompare(b.title, 'en', { sensitivity: 'base' });
  return [...papers].sort((a, b) => {
    if (order === 'title') return title(a, b);
    if (order === 'added') {
      const added = (b.detail.added?.date || '').localeCompare(a.detail.added?.date || '');
      if (added) return added;
    }
    const chronological = publication(a).localeCompare(publication(b));
    return (order === 'oldest' ? chronological : -chronological) || title(a, b);
  });
}

export function readState(search) {
  const params = new URLSearchParams(search);
  const state = { ...DEFAULTS };
  for (const key of Object.keys(DEFAULTS)) if (params.has(key)) state[key] = params.get(key);
  if (!['newest', 'oldest', 'added', 'title'].includes(state.sort)) state.sort = DEFAULTS.sort;
  if (!['auto', 'table', 'cards'].includes(state.view)) state.view = DEFAULTS.view;
  if (!['papers', 'guide'].includes(state.tab)) state.tab = DEFAULTS.tab;
  return state;
}

export function stateQuery(state) {
  const params = new URLSearchParams();
  for (const key of Object.keys(DEFAULTS)) {
    if (state[key] && state[key] !== DEFAULTS[key]) params.set(key, state[key]);
  }
  const query = params.toString();
  return query ? `?${query}` : '';
}

export function resourcesFor(paper) {
  const links = new Map();
  for (const entry of paper.matches || paper.entries) {
    for (const [kind, url] of Object.entries(entry.resources)) {
      if (url) links.set(`${kind}:${url}`, { kind, url });
    }
  }
  return [...links.values()].sort((a, b) => Object.keys(RESOURCE_LABELS).indexOf(a.kind) - Object.keys(RESOURCE_LABELS).indexOf(b.kind));
}

export function markdownFor(paper) {
  const venues = [...new Set(paper.entries.map(e => e.venue))].join('; ');
  return `- [**${paper.title}**](${paper.paper_url}) (${venues}, ${paper.date})`;
}

const tex = value => String(value).replace(/[\\{}%&#_$]/g, char => char === '\\' ? '\\textbackslash{}' : `\\${char}`);

export function bibtexFor(paper) {
  const key = `${paper.title.split(/\s/)[0].replace(/[^a-z0-9]/gi, '')}${paper.year}${paper.arxiv_id?.replace('.', '') || ''}`;
  const fields = [`title = {{${tex(paper.title)}}}`];
  if (paper.detail.authors?.length) fields.push(`author = {${paper.detail.authors.map(tex).join(' and ')}}`);
  fields.push(`year = {${paper.year}}`, `url = {${paper.paper_url}}`);
  // Cite the verified arXiv record; do not invent proceedings metadata from a venue badge.
  if (paper.arxiv_id) fields.push(`eprint = {${paper.arxiv_id}}`, 'archivePrefix = {arXiv}');
  return `@misc{${key},\n  ${fields.join(',\n  ')}\n}`;
}
