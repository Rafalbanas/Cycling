"use strict";

const state = { summary: null, variant: "Variant_B" };

const $ = (selector, scope = document) => scope.querySelector(selector);
const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
const plNumber = (value, digits = 0) => Number(value).toLocaleString("pl-PL", {
  minimumFractionDigits: digits,
  maximumFractionDigits: digits,
});

function initNavigation() {
  const button = $(".menu-toggle");
  const nav = $("#site-nav");
  button.addEventListener("click", () => {
    const open = button.getAttribute("aria-expanded") !== "true";
    button.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("open", open);
  });
  $$("a", nav).forEach((link) => link.addEventListener("click", () => {
    nav.classList.remove("open");
    button.setAttribute("aria-expanded", "false");
  }));
}

function initReveal() {
  if (!("IntersectionObserver" in window)) {
    $$(".reveal").forEach((node) => node.classList.add("visible"));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  $$(".reveal").forEach((node) => observer.observe(node));
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || "Nie udało się pobrać danych.");
  return body;
}

function initEstimator() {
  const form = $("#ftp-form");
  const power = $("#mmp20");
  const range = $("#mmp20-range");
  const error = $("#form-error");
  const sync = (source, target) => { target.value = source.value; };
  power.addEventListener("input", () => sync(power, range));
  range.addEventListener("input", () => {
    sync(range, power);
    updateEstimate({ preventDefault() {} });
  });

  async function updateEstimate(event) {
    event.preventDefault();
    error.textContent = "";
    const submit = $("button[type=submit]", form);
    submit.disabled = true;
    try {
      const result = await fetchJson("/api/estimate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mmp20: power.value, weight: $("#weight").value }),
      });
      $("#ftp-result").textContent = plNumber(result.ftp, 1);
      $("#wkg-result").textContent = result.watts_per_kg ? `${plNumber(result.watts_per_kg, 2)} W/kg` : "—";
      $(".formula").innerHTML = `<span>${plNumber(result.mmp20, 0)} W</span><b>× 0,95</b><span>= ${plNumber(result.ftp, 1)} W</span>`;
    } catch (exception) {
      error.textContent = exception.message;
    } finally {
      submit.disabled = false;
    }
  }
  form.addEventListener("submit", updateEstimate);
}

function renderStats() {
  const dataset = state.summary.dataset;
  $("[data-stat=sessions]").textContent = plNumber(dataset.sessions);
  $("[data-stat=athletes]").textContent = plNumber(dataset.athletes);
}

function renderModels() {
  const models = state.summary.models.filter((row) => row.variant === state.variant);
  const max = Math.max(15, ...models.map((row) => row.mae));
  $("#variant-title").textContent = state.variant === "Variant_B" ? "Wariant B" : "Wariant C";
  $("#model-bars").innerHTML = models.map((row) => `
    <div class="model-bar">
      <div class="model-bar-head"><span>${row.model}</span><b>${plNumber(row.mae, 2)} W</b></div>
      <progress class="model-progress" max="${max}" value="${row.mae}" aria-label="MAE ${row.model}: ${plNumber(row.mae, 2)} W"></progress>
    </div>`).join("");
}

function renderFeatures() {
  const features = state.summary.features[state.variant];
  const max = features[0].importance;
  const title = state.variant === "Variant_B" ? "Wariant B · SHAP" : "Wariant C · SHAP";
  $("#feature-title").textContent = title;
  $("#top-feature").textContent = features[0].feature;
  $("#top-feature-copy").textContent = state.variant === "Variant_B"
    ? "W wariancie B dominuje sąsiednia statystyka MMP. Dlatego pokazujemy również konserwatywny wariant C."
    : "Po usunięciu całej rodziny MMP największe znaczenie przejmują kwantyle i rozkład mocy.";
  $("#feature-bars").innerHTML = features.slice(0, 8).map((row) => `
    <div class="feature-row">
      <span title="${row.feature}">${row.feature}</span>
      <progress class="feature-progress" max="${max}" value="${row.importance}" aria-label="Znaczenie cechy ${row.feature}"></progress>
      <b>${plNumber(row.importance, 1)}</b>
    </div>`).join("");
}

function renderErrorRanges() {
  $("#error-ranges").innerHTML = state.summary.error_ranges.map((row) => `
    <div class="error-range"><span>${row.range}</span><strong>${plNumber(row.mae, 2)} W</strong><small>${plNumber(row.samples)} próbek</small></div>`).join("");
}

async function renderScatter() {
  const chart = $("#scatter-chart");
  const pointsGroup = $(".scatter-points", chart);
  pointsGroup.innerHTML = "";
  const payload = await fetchJson(`/api/predictions?variant=${state.variant}&limit=120`);
  const points = payload.points;
  const values = points.flatMap((point) => [point.actual, point.predicted]);
  const low = Math.floor(Math.min(...values) / 50) * 50;
  const high = Math.ceil(Math.max(...values) / 50) * 50;
  const x = (value) => 42 + ((value - low) / (high - low)) * 490;
  const y = (value) => 305 - ((value - low) / (high - low)) * 270;

  const grid = $(".scatter-grid", chart);
  grid.innerHTML = "";
  for (let index = 0; index <= 4; index += 1) {
    const gx = 42 + index * 122.5;
    const gy = 35 + index * 67.5;
    grid.insertAdjacentHTML("beforeend", `<line x1="${gx}" y1="35" x2="${gx}" y2="305"/><line x1="42" y1="${gy}" x2="532" y2="${gy}"/>`);
  }
  const ideal = $(".ideal-line", chart);
  ideal.setAttribute("x1", x(low)); ideal.setAttribute("y1", y(low));
  ideal.setAttribute("x2", x(high)); ideal.setAttribute("y2", y(high));
  points.forEach((point) => pointsGroup.insertAdjacentHTML("beforeend", `<circle cx="${x(point.actual)}" cy="${y(point.predicted)}" r="3.2"/>`));
}

async function setVariant(variant) {
  state.variant = variant;
  $$(".variant-switcher button").forEach((button) => button.classList.toggle("active", button.dataset.variant === variant));
  renderModels();
  renderFeatures();
  try { await renderScatter(); } catch (_) { $(".scatter-points").innerHTML = ""; }
}

function initVariantButtons() {
  $$(".variant-switcher button").forEach((button) => button.addEventListener("click", () => setVariant(button.dataset.variant)));
}

async function initData() {
  try {
    state.summary = await fetchJson("/api/summary");
    renderStats();
    renderErrorRanges();
    await setVariant(state.variant);
  } catch (exception) {
    console.error(exception);
    $("#model-bars").innerHTML = `<p>Nie udało się wczytać wyników. Odśwież stronę.</p>`;
  }
}

initNavigation();
initReveal();
initEstimator();
initVariantButtons();
initData();
