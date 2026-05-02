const state = {
  entries: [],
  filters: {
    search: "",
    type: "",
    mechanism: "",
    category: "",
    year: "",
    resource: "",
  },
};

const elements = {
  total: document.querySelector("#total-count"),
  benchmarks: document.querySelector("#benchmark-count"),
  mitigations: document.querySelector("#mitigation-count"),
  resources: document.querySelector("#resource-count"),
  visible: document.querySelector("#visible-count"),
  grid: document.querySelector("#paper-grid"),
  template: document.querySelector("#paper-card-template"),
  search: document.querySelector("#search-input"),
  type: document.querySelector("#type-filter"),
  mechanism: document.querySelector("#mechanism-filter"),
  category: document.querySelector("#category-filter"),
  year: document.querySelector("#year-filter"),
  resource: document.querySelector("#resource-filter"),
  reset: document.querySelector("#reset-button"),
};

const resourceLabels = {
  project: "Project",
  code: "Code",
  dataset: "Dataset",
  leaderboard: "Leaderboard",
};

function hasAnyResource(entry) {
  return Object.values(entry.resources).some(Boolean);
}

function fillOptions(select, values) {
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.append(option);
  });
}

function searchableText(entry) {
  return [
    entry.title,
    entry.name,
    entry.venue,
    entry.date,
    entry.arxiv_id,
    entry.type,
    entry.category,
    entry.mechanism,
    entry.subtype,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function matchesResource(entry, resource) {
  if (!resource) return true;
  if (resource === "missing-code") return !entry.resources.code;
  if (resource === "missing-project") return !entry.resources.project;
  return Boolean(entry.resources[resource]);
}

function filteredEntries() {
  const query = state.filters.search.trim().toLowerCase();
  return state.entries.filter((entry) => {
    if (query && !searchableText(entry).includes(query)) return false;
    if (state.filters.type && entry.type !== state.filters.type) return false;
    if (state.filters.mechanism && entry.mechanism !== state.filters.mechanism) return false;
    if (state.filters.category && entry.category !== state.filters.category) return false;
    if (state.filters.year && String(entry.year) !== state.filters.year) return false;
    if (!matchesResource(entry, state.filters.resource)) return false;
    return true;
  });
}

function renderStats(data) {
  elements.total.textContent = data.entry_count;
  elements.benchmarks.textContent = data.benchmark_count;
  elements.mitigations.textContent = data.mitigation_count;
  elements.resources.textContent = data.entries.filter(hasAnyResource).length;
}

function renderCard(entry) {
  const fragment = elements.template.content.cloneNode(true);
  const card = fragment.querySelector(".paper-card");
  const typePill = fragment.querySelector(".type-pill");
  const title = fragment.querySelector(".paper-title");
  const trainingRow = fragment.querySelector(".training-row");
  const resources = fragment.querySelector(".resource-links");

  card.dataset.type = entry.type;
  typePill.textContent = entry.type === "benchmark" ? "Benchmark" : "Mitigation";
  typePill.classList.add(entry.type);
  fragment.querySelector(".date-pill").textContent = entry.date;
  title.href = entry.paper_url;
  title.textContent = entry.title;
  fragment.querySelector(".paper-name").textContent = entry.name;
  fragment.querySelector(".paper-venue").textContent = entry.venue;
  fragment.querySelector(".paper-category").textContent = `${entry.category} / ${entry.subtype}`;

  if (entry.type === "mitigation") {
    fragment.querySelector(".paper-training").textContent = entry.training_free || "-";
  } else {
    trainingRow.remove();
  }

  Object.entries(entry.resources).forEach(([kind, url]) => {
    if (!url) return;
    const link = document.createElement("a");
    link.href = url;
    link.textContent = resourceLabels[kind] || kind;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    resources.append(link);
  });

  if (!resources.children.length) {
    const missing = document.createElement("span");
    missing.textContent = "No resources yet";
    resources.append(missing);
  }

  return fragment;
}

function render() {
  const entries = filteredEntries();
  elements.visible.textContent = entries.length;
  elements.grid.replaceChildren();

  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No entries match the current filters.";
    elements.grid.append(empty);
    return;
  }

  entries.forEach((entry) => elements.grid.append(renderCard(entry)));
}

function setFilter(key, value) {
  state.filters[key] = value;
  render();
}

function initializeFilters(entries) {
  fillOptions(elements.type, [...new Set(entries.map((entry) => entry.type))].sort());
  fillOptions(elements.mechanism, [...new Set(entries.map((entry) => entry.mechanism))].sort());
  fillOptions(elements.category, [...new Set(entries.map((entry) => entry.category))].sort());
  fillOptions(
    elements.year,
    [...new Set(entries.map((entry) => entry.year).filter(Boolean))]
      .sort((a, b) => b - a)
      .map(String),
  );

  elements.search.addEventListener("input", (event) => setFilter("search", event.target.value));
  elements.type.addEventListener("change", (event) => setFilter("type", event.target.value));
  elements.mechanism.addEventListener("change", (event) => setFilter("mechanism", event.target.value));
  elements.category.addEventListener("change", (event) => setFilter("category", event.target.value));
  elements.year.addEventListener("change", (event) => setFilter("year", event.target.value));
  elements.resource.addEventListener("change", (event) => setFilter("resource", event.target.value));
  elements.reset.addEventListener("click", () => {
    Object.keys(state.filters).forEach((key) => {
      state.filters[key] = "";
    });
    elements.search.value = "";
    elements.type.value = "";
    elements.mechanism.value = "";
    elements.category.value = "";
    elements.year.value = "";
    elements.resource.value = "";
    render();
  });

  const params = new URLSearchParams(window.location.search);
  ["search", "type", "mechanism", "category", "year", "resource"].forEach((key) => {
    const value = params.get(key);
    if (!value) return;
    state.filters[key] = value;
    const input = key === "search" ? elements.search : elements[key];
    if (input) input.value = value;
  });
}

async function loadPapers() {
  const response = await fetch("data/papers.json");
  if (!response.ok) {
    throw new Error(`Unable to load papers.json: ${response.status}`);
  }
  const data = await response.json();
  state.entries = data.entries;
  renderStats(data);
  initializeFilters(data.entries);
  render();
}

loadPapers().catch((error) => {
  elements.grid.innerHTML = `<div class="empty-state">${error.message}</div>`;
});
