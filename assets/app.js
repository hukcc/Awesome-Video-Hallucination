import {
  DEFAULTS, TYPE_LABELS, RESOURCE_LABELS, ROUTES, SCOPE_LABELS, groupPapers, filterPapers, sortPapers,
  readState, stateQuery, trainingValue, resourcesFor, markdownFor, bibtexFor,
} from './catalog.mjs';

const $ = selector => document.querySelector(selector);
const state = { filters: readState(location.search), papers: [], loaded: false };
const mobile = matchMedia('(max-width: 899px)');
let searchEditing = false;
let notificationTimer;

function node(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function link(text, url, className = '') {
  const element = node('a', className, text);
  element.href = url;
  return element;
}

function iconButton(icon, label, action) {
  const button = node('button', 'icon-button');
  button.type = 'button';
  button.title = label;
  button.setAttribute('aria-label', label);
  const image = node('img');
  image.src = `assets/icons/${icon}.svg`;
  image.alt = '';
  button.append(image);
  button.addEventListener('click', action);
  return button;
}

function notify(message) {
  clearTimeout(notificationTimer);
  $('#notification').textContent = message;
  notificationTimer = setTimeout(() => { $('#notification').textContent = ''; }, 3000);
}

async function copy(text, label) {
  try {
    await navigator.clipboard.writeText(text);
    notify(`${label} copied`);
  } catch {
    window.prompt(`Copy ${label.toLowerCase()}`, text);
  }
}

function roles(paper) {
  const list = node('div', 'role-list');
  [...new Set(paper.matches.map(e => e.type))].forEach(type => {
    list.append(node('span', `type-tag ${type}`, TYPE_LABELS[type]));
  });
  return list;
}

function resourceLinks(paper) {
  const container = node('div', 'resource-links');
  const links = resourcesFor(paper);
  const totals = {};
  links.forEach(({ kind }) => { totals[kind] = (totals[kind] || 0) + 1; });
  const counts = {};
  links.forEach(({ kind, url }) => {
    counts[kind] = (counts[kind] || 0) + 1;
    const label = RESOURCE_LABELS[kind] + (totals[kind] > 1 ? ` ${counts[kind]}` : '');
    container.append(link(label, url));
  });
  if (!links.length) container.append(node('span', 'no-resources', 'No linked resources'));
  return container;
}

function copyActions(paper) {
  const actions = node('div', 'copy-actions');
  actions.append(
    iconButton('copy', 'Copy Markdown', () => copy(markdownFor(paper), 'Markdown')),
    iconButton('quote', 'Copy BibTeX', () => copy(bibtexFor(paper), 'BibTeX')),
  );
  return actions;
}

function details(paper) {
  const container = node('details', 'paper-details');
  const total = paper.entries.length;
  container.append(node('summary', '', `${total > 1 ? total + ' contributions' : 'Details'} & sources`));
  const list = node('ul', 'contribution-list');
  const matching = new Set(paper.matches.map(e => e.id));
  for (const entry of paper.entries) {
    const item = node('li', matching.has(entry.id) ? '' : 'not-matched');
    item.append(node('strong', '', `${entry.name} / ${TYPE_LABELS[entry.type]}`));
    if (!matching.has(entry.id)) item.append(node('span', '', ' (outside current filters)'));
    item.append(node('p', '', entry.description));
    item.append(node('p', '', `${entry.mechanism} > ${entry.category} > ${entry.subtype}`));
    if (entry.type === 'mitigation') item.append(node('p', '', `Training-free: ${trainingValue(entry) === 'yes' ? 'Yes' : 'No'}`));
    if (entry.routes?.length) item.append(node('p', '', `Technical route: ${entry.routes.join(' / ')}`));
    const resources = resourceLinks({ entries: [entry] });
    if (resourcesFor({ entries: [entry] }).length) item.append(resources);
    list.append(item);
  }
  container.append(list);
  if (paper.detail.authors?.length) container.append(node('p', 'source-note', paper.detail.authors.join(', ')));
  if (paper.detail.source_url) {
    const provenance = node('p', 'source-note');
    provenance.append(link('Descriptions and task-tag source', paper.detail.source_url),
      document.createTextNode(` / ${paper.detail.evidence}; reviewed ${paper.detail.reviewed_on}.`));
    container.append(provenance);
  }
  if (paper.detail.note) container.append(node('p', 'source-note', paper.detail.note));
  if (paper.detail.scope_review) {
    const review = paper.detail.scope_review;
    const note = node('p', 'source-note', `Scope: ${SCOPE_LABELS[review.scope]}. ${review.reason} `);
    note.append(link('Review evidence', review.source_url),
      document.createTextNode(` / ${review.evidence}; reviewed ${review.reviewed_on}.`));
    container.append(note);
  }
  if (paper.detail.added) {
    const added = node('p', 'source-note');
    added.append(link(`First listed ${paper.detail.added.date}`,
      `https://github.com/hukcc/Awesome-Video-Hallucination/commit/${paper.detail.added.commit}`));
    container.append(added);
  }
  return container;
}

function paperContent(paper, parent) {
  parent.append(node('p', 'paper-names', [...new Set(paper.entries.map(e => e.name))].join(' / ')));
  const heading = node('h2');
  heading.append(link(paper.title, paper.paper_url, 'paper-title'));
  parent.append(heading, node('p', 'paper-summary', paper.detail.summary || 'Summary pending source review.'));
  const tags = node('div', 'tags');
  (paper.detail.tasks || []).forEach(task => {
    const tag = link(task, stateQuery({ ...state.filters, task, tab: 'papers' }), 'task-tag');
    tag.addEventListener('click', event => {
      if (modifiedClick(event)) return;
      event.preventDefault();
      change({ task });
    });
    tags.append(tag);
  });
  parent.append(tags, details(paper));
}

function scope(paper) {
  const section = node('div');
  section.append(roles(paper), node('p', 'venue', [...new Set(paper.matches.map(e => e.venue))].join(' / ')));
  section.append(node('p', 'scope-text', [...new Set(paper.matches.map(e => e.category))].join('; ')));
  section.append(node('p', 'scope-text', SCOPE_LABELS[paper.detail.scope_review?.scope || 'unreviewed']));
  const requirements = [...new Set(paper.matches.filter(e => e.type === 'mitigation').map(trainingValue))];
  if (requirements.length) section.append(node('p', 'scope-text', `Training-free: ${requirements.map(v => v === 'yes' ? 'Yes' : 'No').join(' / ')}`));
  return section;
}

function dateInfo(paper) {
  const section = node('div');
  const time = node('time', 'date-value', paper.date);
  time.dateTime = paper.detail.published_on || paper.date.split('/').reverse().join('-');
  section.append(time);
  if (state.filters.sort === 'added' && paper.detail.added) {
    section.append(node('p', 'date-caption added-date', 'First listed'));
    section.append(node('p', 'date-value', paper.detail.added.date));
  }
  return section;
}

function renderTable(papers) {
  const table = node('table', 'paper-table');
  const caption = node('caption', 'sr-only', 'Papers matching the selected filters');
  const head = node('thead');
  const header = node('tr');
  ['Paper', 'Contribution & venue', 'First published', 'Resources'].forEach(label => {
    const th = node('th', '', label);
    th.scope = 'col';
    header.append(th);
  });
  head.append(header);
  const body = node('tbody');
  for (const paper of papers) {
    const row = node('tr');
    row.dataset.paper = paper.key;
    const content = node('td');
    paperContent(paper, content);
    const scopeCell = node('td');
    scopeCell.append(scope(paper));
    const date = node('td');
    date.append(dateInfo(paper));
    const resources = node('td');
    resources.append(resourceLinks(paper), copyActions(paper));
    row.append(content, scopeCell, date, resources);
    body.append(row);
  }
  table.append(caption, head, body);
  return table;
}

function renderCards(papers) {
  const grid = node('div', 'card-grid');
  for (const paper of papers) {
    const card = node('article', 'paper-card');
    card.dataset.paper = paper.key;
    const top = node('div', 'card-topline');
    top.append(roles(paper), dateInfo(paper));
    card.append(top);
    paperContent(paper, card);
    const venue = [...new Set(paper.matches.map(e => e.venue))].join(' / ');
    const categories = [...new Set(paper.matches.map(e => e.category))].join('; ');
    card.append(node('p', 'scope-text', `${venue} / ${categories}`), resourceLinks(paper));
    const bottom = node('div', 'card-bottom');
    const requirements = [...new Set(paper.matches.filter(e => e.type === 'mitigation').map(trainingValue))];
    bottom.append(node('span', 'date-caption', requirements.length ? `Training-free: ${requirements.map(v => v === 'yes' ? 'Yes' : 'No').join(' / ')}` : ''));
    bottom.append(copyActions(paper));
    card.append(bottom);
    grid.append(card);
  }
  return grid;
}

function render() {
  const f = state.filters;
  $('#catalog').hidden = f.tab !== 'papers';
  $('#reading-guide').hidden = f.tab !== 'guide';
  document.querySelectorAll('[data-tab]').forEach(tab => {
    tab.href = stateQuery({ ...f, tab: tab.dataset.tab }) || '?';
    if (tab.dataset.tab === f.tab) tab.setAttribute('aria-current', 'page');
    else tab.removeAttribute('aria-current');
  });
  $('#search-input').value = f.search;
  $('#search-input').placeholder = mobile.matches ? 'Search papers, methods, tasks...' : 'Search titles, methods, tasks, arXiv IDs...';
  $('#sort-select').value = f.sort;
  const active = $('#active-filters');
  active.replaceChildren();
  for (const key of Object.keys(DEFAULTS).filter(k => !['sort', 'view', 'tab'].includes(k))) {
    const select = document.querySelector(`[data-filter="${key}"]`);
    if (select) {
      select.querySelectorAll('[data-unknown]').forEach(option => option.remove());
      if (f[key] && ![...select.options].some(o => o.value === f[key])) {
        const unknown = new Option(`Unknown: ${f[key]}`, f[key]);
        unknown.dataset.unknown = 'true';
        select.append(unknown);
      }
      select.value = f[key];
    }
    if (f[key]) {
      const value = select ? select.selectedOptions[0].textContent : f[key];
      const label = select ? select.parentElement.firstChild.textContent.trim() : 'Search';
      const button = node('button', 'filter-token', `${label}: ${value}`);
      button.type = 'button';
      button.setAttribute('aria-label', `Remove ${label.toLowerCase()} filter: ${value}`);
      const close = node('span', '', '\u00d7');
      close.setAttribute('aria-hidden', 'true');
      button.append(close);
      button.addEventListener('click', () => change({ [key]: '' }));
      active.append(button);
    }
  }
  $('#filter-count').textContent = active.childElementCount ? `(${active.childElementCount})` : '';
  const cardView = mobile.matches || f.view === 'cards';
  $('#table-view').setAttribute('aria-pressed', String(!cardView));
  $('#cards-view').setAttribute('aria-pressed', String(cardView));
  if (!state.loaded) return;
  const results = sortPapers(filterPapers(state.papers, f), f.sort);
  const contributions = results.reduce((sum, paper) => sum + paper.matches.length, 0);
  const count = $('#visible-count');
  count.replaceChildren(node('strong', '', `${results.length} ${results.length === 1 ? 'paper' : 'papers'}`),
    document.createTextNode(` / ${contributions} ${contributions === 1 ? 'contribution' : 'contributions'}`));
  $('#paper-results').replaceChildren(results.length ? (cardView ? renderCards(results) : renderTable(results)) : document.createDocumentFragment());
  $('#empty-state').hidden = results.length > 0;
}

function change(patch, { replace = false } = {}) {
  state.filters = { ...state.filters, ...patch };
  const next = location.pathname + stateQuery(state.filters) + location.hash;
  if (next !== location.pathname + location.search + location.hash) history[replace ? 'replaceState' : 'pushState'](null, '', next);
  render();
}

function reset() {
  searchEditing = false;
  change({ ...DEFAULTS, view: state.filters.view, tab: 'papers', sort: state.filters.sort });
}

function modifiedClick(event) {
  return event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;
}

function options(select, values, labels = {}) {
  values.forEach(value => select.add(new Option(labels[value] || value, value)));
}

$('#filter-panel').open = !mobile.matches;
mobile.addEventListener('change', () => {
  $('#filter-panel').open = !mobile.matches;
  render();
});
$('#search-input').addEventListener('input', event => {
  change({ search: event.target.value }, { replace: searchEditing });
  searchEditing = true;
});
$('#search-input').addEventListener('blur', () => { searchEditing = false; });
document.querySelectorAll('[data-filter]').forEach(select => {
  select.addEventListener('change', () => change({ [select.dataset.filter]: select.value }));
});
$('#sort-select').addEventListener('change', event => change({ sort: event.target.value }));
$('#table-view').addEventListener('click', () => change({ view: 'table' }));
$('#cards-view').addEventListener('click', () => change({ view: 'cards' }));
$('#reset-button').addEventListener('click', reset);
$('#empty-reset').addEventListener('click', reset);
$('#share-button').addEventListener('click', () => copy(location.href, 'View link'));
document.querySelectorAll('[data-tab]').forEach(tab => {
  tab.addEventListener('click', event => {
    if (modifiedClick(event)) return;
    event.preventDefault();
    change({ tab: tab.dataset.tab });
  });
});
document.querySelectorAll('[data-preset]').forEach(preset => {
  preset.addEventListener('click', event => {
    if (modifiedClick(event)) return;
    event.preventDefault();
    change({ ...readState(new URL(preset.href).search), view: state.filters.view });
  });
});
window.addEventListener('popstate', () => {
  searchEditing = false;
  state.filters = readState(location.search);
  render();
});

async function init() {
  render();
  try {
    const responses = await Promise.all(['data/papers.json', 'data/paper_details.json'].map(url => fetch(url)));
    if (responses.some(response => !response.ok)) throw new Error('Collection request failed');
    const [data, metadata] = await Promise.all(responses.map(response => response.json()));
    state.papers = groupPapers(data.entries, metadata.papers);
    options($('#type-filter'), Object.keys(TYPE_LABELS), TYPE_LABELS);
    options($('#task-filter'), metadata.task_vocabulary);
    options($('#route-filter'), ROUTES);
    options($('#scope-filter'), Object.keys(SCOPE_LABELS), SCOPE_LABELS);
    for (const key of ['mechanism', 'category', 'subtype', 'venue', 'year']) {
      const values = [...new Set(data.entries.map(e => String(e[key])))].sort((a, b) => a.localeCompare(b));
      options($(`#${key}-filter`), key === 'year' ? values.reverse() : values);
    }
    const counts = $('#collection-counts');
    counts.replaceChildren();
    [[state.papers.length, 'papers'], [data.benchmark_count, 'benchmarks'], [data.mitigation_count, 'methods'], [data.analysis_count, 'analysis']].forEach(([number, label]) => {
      const item = node('span');
      item.append(node('strong', '', number), document.createTextNode(' ' + label));
      counts.append(item);
    });
    state.loaded = true;
    $('#paper-results').setAttribute('aria-busy', 'false');
    render();
  } catch (error) {
    $('#collection-counts').textContent = 'Collection unavailable';
    $('#visible-count').textContent = 'The paper collection could not be loaded.';
    const message = node('p');
    message.append(link('Open the full list on GitHub', 'https://github.com/hukcc/Awesome-Video-Hallucination#evaluation-benchmarks'));
    const retry = node('button', '', 'Retry');
    retry.type = 'button';
    retry.addEventListener('click', () => location.reload());
    $('#paper-results').replaceChildren(message, retry);
    $('#paper-results').setAttribute('aria-busy', 'false');
    console.error(error);
  }
}

init();
