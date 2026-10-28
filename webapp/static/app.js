"use strict";

const translations = {
  pl: {
    pageTitle: "Cycling — FTP z danych treningowych", pageDescription: "Cycling — interaktywna prezentacja badań nad estymacją FTP z telemetrii kolarskiej.",
    skip: "Przejdź do treści", brandHome: "Cycling — strona główna", menu: "Menu", mainNav: "Główna nawigacja", languageLabel: "Wybierz język",
    navEstimator: "Estymator", navResults: "Wyniki", navMethod: "Metoda", navThesis: "Praca",
    heroEyebrow: "Telemetria × uczenie maszynowe", heroTitle: "Forma zapisana<br>w <em>danych.</em>", heroLead: "Zobacz, jak 151 tysięcy rzeczywistych treningów zamienia się w powtarzalny eksperyment estymacji operacyjnej etykiety FTP.", heroCalculate: "Oblicz FTP", heroResults: "Zobacz wyniki",
    activityVisual: "Abstrakcyjna wizualizacja profilu trasy i mocy", activityProfile: "Profil aktywności", activityChart: "Profil przykładowej aktywności", time: "czas", distance: "dystans", heartRate: "tętno",
    statSessions: "sesji treningowych", statAthletes: "anonimowych zawodników", statMae: "najlepsze MAE wariantu B", statR2: "najlepsze R² wariantu B",
    tool: "Narzędzie", estimatorTitle: "Estymator testu<br><em>20-minutowego.</em>", estimatorIntro: "Ta funkcja odtwarza definicję etykiety użytej w projekcie. Nie jest predykcją modelu ML — repozytorium zawiera wyniki ewaluacji, lecz nie zawiera zapisanego modelu gotowego do inferencji.",
    enterTest: "Podaj wynik próby", enterTestHelp: "Najlepsza średnia moc utrzymana przez pełne 20 minut.", mmpLabel: "Moc 20-minutowa", mmpRange: "Moc 20-minutowa w watach", weight: "Masa ciała", optional: "opcjonalnie", liveHint: "Wynik aktualizuje się automatycznie podczas zmiany wartości.", recalculate: "Przelicz ponownie",
    operationalResult: "Wynik operacyjny", projectFormula: "formuła projektu", relativeWeight: "Względem masy", methodLabel: "Metoda", important: "Ważne:", formulaWarning: "to heurystyczna etykieta użyta w badaniu, nie laboratoryjny pomiar progu fizjologicznego ani automatyczna rekomendacja zmiany stref.",
    validation: "Walidacja", resultsTitle: "Wyniki bez<br><em>skrótów.</em>", resultsIntro: "Podział testowy wykonano po zawodnikach, nie po pojedynczych sesjach. Dzięki temu osoby ze zbioru testowego nie występowały w treningu.", variantSelector: "Wybierz widok wariantu", variantB: "Wariant B", variantC: "Wariant C", comparison: "Porównanie", withoutMmp20: "bez MMP20", withoutAllMmp: "bez wszystkich MMP", metric: "Metryka",
    plainB: "Najprościej: w wariancie B najlepszy model mylił się średnio o około 6,55 W względem etykiety obliczonej z danych historycznych.", plainC: "Najprościej: po usunięciu wszystkich cech MMP najlepszy model mylił się średnio o około 10,29 W. To trudniejszy i bardziej konserwatywny wariant.", plainCompare: "Wariant B jest dokładniejszy, ale korzysta z krótszych statystyk MMP. Wariant C usuwa całą tę rodzinę cech i stanowi bardziej rygorystyczny punkt odniesienia.",
    modelComparison: "Porównanie modeli", modelChart: "Wykres porównania modeli", testSample: "Próba testowa", actualPredicted: "Rzeczywiste vs estymowane", scatterChart: "Wykres punktowy wartości rzeczywistych i estymowanych", ftpAxis: "wartość etykiety FTP [W]", variantBShort: "wariant B", variantCShort: "wariant C", idealLine: "linia idealna",
    topFeature: "Najważniejsza cecha", featureB: "W wariancie B dominuje sąsiednia statystyka MMP. Dlatego pokazujemy również konserwatywny wariant C.", featureC: "Po usunięciu całej rodziny MMP największe znaczenie przejmują kwantyle i rozkład mocy.", featureCompare: "Warianty korzystają z innych sygnałów: B opiera się głównie na MMP10, a C na kwantylach i rozkładzie mocy.",
    errorByFtp: "Błąd a poziom FTP", samples: "próbek", scaleCheck: "Kontrola skali", scaleCopy: "sesje w dodatkowej próbie na 4 645 zawodnikach. Wynik kontrolny potwierdził skalowalność pipeline'u, ale nie zastępuje bazowego eksperymentu.",
    metricsQuestion: "Co oznaczają MAE, RMSE i R²?", metricsAnswer: "MAE to przeciętny błąd w watach. RMSE mocniej karze duże pomyłki. R² opisuje, jaka część zróżnicowania etykiety została odtworzona przez model; im bliżej 1, tym lepiej.", variantQuestion: "Dlaczego są dwa warianty?", variantAnswer: "Wariant B usuwa MMP20, z którego wyliczono etykietę, lecz zachowuje krótsze cechy MMP. Wariant C usuwa wszystkie cechy MMP, dlatego jest bardziej konserwatywnym sprawdzianem.", splitQuestion: "Dlaczego podział po zawodnikach?", splitAnswer: "Sesje jednej osoby są do siebie podobne. Umieszczenie tej samej osoby w treningu i teście sztucznie ułatwiłoby zadanie. Podział osobniczy ogranicza ten rodzaj wycieku.",
    leakageTitle: "Wariant A nie jest sukcesem modelu.", leakageCopy: "Po pozostawieniu <code>mmp_20min</code> model praktycznie odtwarza równanie etykiety. To kontrola wycieku danych, dlatego aplikacja nie prezentuje go jako użytecznej predykcji.",
    researchPipeline: "Pipeline badawczy", methodTitle: "Od pliku treningu<br>do <em>wniosku.</em>", methodIntro: "Każdy etap pozostawia ślad w repozytorium: kod przetwarzania, raporty jakości, metryki i zanonimizowane wyniki testowe.", acquisition: "Pozyskanie", acquisitionCopy: "Anonimowe aktywności GoldenCheetah OpenData.", quality: "Kontrola jakości", qualityCopy: "Zakresy sensorów, braki, minimum 30 minut.", features: "Ekstrakcja cech", featuresCopy: "Moc, tętno, kadencja, MMP i rozkład intensywności.", evaluation: "Ewaluacja", evaluationCopy: "Ridge, Random Forest i XGBoost; podział osobniczy.",
    methodQuote: "Model estymuje operacyjną etykietę FTP, a nie laboratoryjnie zmierzony próg fizjologiczny.", keyCaveat: "Najważniejsze zastrzeżenie interpretacyjne pracy", featureImpact: "Wpływ cech", shapQuestion: "Czym jest SHAP?", shapAnswer: "SHAP przypisuje cechom udział w wyniku modelu. Pokazane wartości są średnią bezwzględną siłą wpływu w zbiorze testowym — mówią o znaczeniu cechy, ale nie dowodzą związku przyczynowego.", labelQuestion: "Co dokładnie przewiduje model?", labelAnswer: "Model odtwarza historyczną etykietę obliczoną jako 95% najlepszej średniej mocy z 20 minut. Nie przewiduje bezpośrednio progu mleczanowego, MLSS ani mocy krytycznej.",
    sourceDocument: "Dokument źródłowy", thesisTitle: "Praca<br><em>magisterska.</em>", thesisIntro: "Pełny dokument opisujący podstawy teoretyczne, metodologię, eksperymenty i ograniczenia rozwiązania.", thesisLanguage: "Dokument jest dostępny wyłącznie w języku polskim.", thesisName: "Model predykcji formy kolarskiej", fullscreen: "Pełny ekran", readerFormat: "Czytnik obrazów · 87 stron", readerControls: "Sterowanie czytnikiem", previousPage: "Poprzednia strona", nextPage: "Następna strona", page: "Strona", zoomOut: "Pomniejsz", zoomIn: "Powiększ", fitPage: "Dopasuj", thesisReader: "Czytnik pracy magisterskiej", readerLoading: "Ładowanie czytnika…", readerLoadError: "Nie udało się wczytać strony pracy.", thesisPageAlt: "Strona {page} pracy magisterskiej", readerNotice: "Czytnik ogranicza wygodne pobranie całego dokumentu, ale nie stanowi pełnego zabezpieczenia przed kopiowaniem treści.",
    honestInterpretation: "Uczciwa interpretacja", limitationsTitle: "Jedna liczba<br>nie opowiada <em>całej historii.</em>", heuristicTitle: "Etykieta jest heurystyką", heuristicCopy: "Współczynnik 0,95 nie uwzględnia indywidualnego profilu fizjologicznego.", historyTitle: "Walidacja jest historyczna", historyCopy: "Wyniki pochodzą z jednego repozytorium i nie zastępują walidacji prospektywnej.", sensorTitle: "Jakość sensorów ma znaczenie", sensorCopy: "Braki tętna, GPS i nietypowe sesje mogą obniżać wiarygodność estymacji.",
    footerCopy: "Interaktywna prezentacja projektu magisterskiego.<br>Dane: GoldenCheetah OpenData.", backTop: "Do góry ↑", loadError: "Nie udało się wczytać danych. Odśwież stronę.", actual: "Rzeczywista", predicted: "Estymowana", error: "Błąd", value: "Wartość",
    metricMae: "MAE — mniej znaczy lepiej", metricRmse: "RMSE — mniej znaczy lepiej", metricR2: "R² — więcej znaczy lepiej", metricMedian: "MedAE — mniej znaczy lepiej",
    analysisKicker: "Analiza XGBoost", analysisNote: "Statystyki liczone na całym pliku CSV wariantu (model XGBoost); wykres pokazuje co najwyżej 120 równomiernie pobranych punktów. Filtrowanie FTP działa tylko w tym panelu i nie zmienia pozostałych wyników na stronie.", ftpMinLabel: "FTP min [W]", filterHint: "filtruje tylko ten panel", ftpMaxLabel: "FTP max [W]", analysisApply: "Zastosuj", analysisReset: "Wyczyść", analysisLoading: "Ładowanie statystyk i wykresu…", analysisEmpty: "Brak próbek w wybranym zakresie FTP.", analysisError: "Nie udało się wczytać danych analitycznych.", analysisInvalidValue: "Podaj poprawną nieujemną wartość FTP.", analysisInvalidRange: "Zakres FTP jest niepoprawny — min jest większe niż max.", analysisCount: "próbki w zakresie", analysisTotal: "wszystkich próbek", analysisMedian: "MedAE", analysisBias: "Bias — przeciętny residual", residualChart: "Wykres residuali — estymacja minus rzeczywistość", residualY: "residual [W]"
  },
  en: {
    pageTitle: "Cycling — FTP from training data", pageDescription: "Cycling — an interactive presentation of research on FTP estimation from cycling telemetry.",
    skip: "Skip to content", brandHome: "Cycling — home", menu: "Menu", mainNav: "Main navigation", languageLabel: "Choose language",
    navEstimator: "Estimator", navResults: "Results", navMethod: "Method", navThesis: "Thesis",
    heroEyebrow: "Telemetry × machine learning", heroTitle: "Performance written<br>in <em>data.</em>", heroLead: "See how 151 thousand real training sessions become a reproducible experiment for estimating an operational FTP label.", heroCalculate: "Calculate FTP", heroResults: "Explore results",
    activityVisual: "Abstract activity profile and power visualisation", activityProfile: "Activity profile", activityChart: "Example activity profile", time: "time", distance: "distance", heartRate: "heart rate",
    statSessions: "training sessions", statAthletes: "anonymous athletes", statMae: "best MAE for variant B", statR2: "best R² for variant B",
    tool: "Tool", estimatorTitle: "20-minute test<br><em>estimator.</em>", estimatorIntro: "This tool reproduces the label definition used in the project. It is not an ML model prediction — the repository contains evaluation results, but no saved model artifact ready for inference.",
    enterTest: "Enter your test result", enterTestHelp: "The highest average power sustained for a full 20 minutes.", mmpLabel: "20-minute power", mmpRange: "20-minute power in watts", weight: "Body mass", optional: "optional", liveHint: "The result updates automatically as values change.", recalculate: "Recalculate",
    operationalResult: "Operational result", projectFormula: "project formula", relativeWeight: "Relative to body mass", methodLabel: "Method", important: "Important:", formulaWarning: "this is the heuristic label used in the study, not a laboratory measurement of a physiological threshold or an automatic recommendation to change training zones.",
    validation: "Validation", resultsTitle: "Results, without<br><em>shortcuts.</em>", resultsIntro: "The test split was performed by athlete, not by individual session. Athletes in the test set were therefore absent from model training.", variantSelector: "Choose variant view", variantB: "Variant B", variantC: "Variant C", comparison: "Comparison", withoutMmp20: "without MMP20", withoutAllMmp: "without all MMP features", metric: "Metric",
    plainB: "In plain language: the best model in variant B was wrong by about 6.55 W on average relative to the label calculated from historical data.", plainC: "In plain language: after removing all MMP features, the best model was wrong by about 10.29 W on average. This is the harder, more conservative variant.", plainCompare: "Variant B is more accurate, but uses shorter MMP statistics. Variant C removes the entire feature family and provides a stricter reference point.",
    modelComparison: "Model comparison", modelChart: "Model comparison chart", testSample: "Test sample", actualPredicted: "Actual vs estimated", scatterChart: "Scatter plot of actual and estimated values", ftpAxis: "FTP label value [W]", variantBShort: "variant B", variantCShort: "variant C", idealLine: "ideal line",
    topFeature: "Most important feature", featureB: "Variant B is dominated by a neighbouring MMP statistic. This is why the more conservative variant C is also shown.", featureC: "After removing the entire MMP family, power quantiles and distribution become the leading signals.", featureCompare: "The variants rely on different signals: B mainly on MMP10, while C relies on power quantiles and distribution.",
    errorByFtp: "Error by FTP level", samples: "samples", scaleCheck: "Scale check", scaleCopy: "sessions in an additional sample of 4,645 athletes. This control confirmed pipeline scalability, but does not replace the baseline experiment.",
    metricsQuestion: "What do MAE, RMSE and R² mean?", metricsAnswer: "MAE is the average error in watts. RMSE penalises large errors more strongly. R² describes how much of the label variation the model reproduces; values closer to 1 are better.", variantQuestion: "Why are there two variants?", variantAnswer: "Variant B removes MMP20, which defines the label, but retains shorter MMP features. Variant C removes every MMP feature and is therefore a more conservative test.", splitQuestion: "Why split by athlete?", splitAnswer: "Sessions from the same person are similar. Placing one athlete in both training and test sets would make the task artificially easy. A subject-wise split limits this type of leakage.",
    leakageTitle: "Variant A is not a modelling success.", leakageCopy: "With <code>mmp_20min</code> retained, the model essentially reconstructs the label equation. This is a data-leakage control, so the application does not present it as a useful prediction.",
    researchPipeline: "Research pipeline", methodTitle: "From a training file<br>to a <em>conclusion.</em>", methodIntro: "Every stage leaves an audit trail in the project: processing code, quality reports, metrics and anonymised test results.", acquisition: "Acquisition", acquisitionCopy: "Anonymous GoldenCheetah OpenData activities.", quality: "Quality control", qualityCopy: "Sensor ranges, missing values and a 30-minute minimum.", features: "Feature extraction", featuresCopy: "Power, heart rate, cadence, MMP and intensity distribution.", evaluation: "Evaluation", evaluationCopy: "Ridge, Random Forest and XGBoost; subject-wise split.",
    methodQuote: "The model estimates an operational FTP label, not a laboratory-measured physiological threshold.", keyCaveat: "The thesis's key interpretive caveat", featureImpact: "Feature impact", shapQuestion: "What is SHAP?", shapAnswer: "SHAP assigns features a contribution to model output. The values shown are mean absolute impact in the test set: they describe feature importance, but do not prove causality.", labelQuestion: "What exactly does the model predict?", labelAnswer: "The model reproduces a historical label calculated as 95% of the highest 20-minute mean power. It does not directly predict lactate threshold, MLSS or critical power.",
    sourceDocument: "Source document", thesisTitle: "Master's<br><em>thesis.</em>", thesisIntro: "The complete document covering the theoretical background, methodology, experiments and limitations of the solution.", thesisLanguage: "The document is available in Polish only.", thesisName: "Cycling performance prediction model", fullscreen: "Full screen", readerFormat: "Image reader · 87 pages", readerControls: "Reader controls", previousPage: "Previous page", nextPage: "Next page", page: "Page", zoomOut: "Zoom out", zoomIn: "Zoom in", fitPage: "Fit", thesisReader: "Master's thesis reader", readerLoading: "Loading reader…", readerLoadError: "The thesis page could not be loaded.", thesisPageAlt: "Page {page} of the master's thesis", readerNotice: "The reader discourages convenient whole-document downloads, but it is not complete protection against copying content.",
    honestInterpretation: "Honest interpretation", limitationsTitle: "One number does not<br>tell the <em>whole story.</em>", heuristicTitle: "The label is heuristic", heuristicCopy: "The 0.95 coefficient does not account for an individual's physiological profile.", historyTitle: "Validation is historical", historyCopy: "Results come from a single repository and do not replace prospective validation.", sensorTitle: "Sensor quality matters", sensorCopy: "Missing heart-rate or GPS data and unusual sessions can reduce estimate reliability.",
    footerCopy: "Interactive presentation of a master's thesis project.<br>Data: GoldenCheetah OpenData.", backTop: "Back to top ↑", loadError: "Data could not be loaded. Refresh the page.", actual: "Actual", predicted: "Estimated", error: "Error", value: "Value",
    metricMae: "MAE — lower is better", metricRmse: "RMSE — lower is better", metricR2: "R² — higher is better", metricMedian: "MedAE — lower is better",
    analysisKicker: "XGBoost analysis", analysisNote: "Statistics are computed on the variant's whole-CSV file (XGBoost model); the chart shows at most 120 evenly sampled points. FTP filtering applies only inside this panel and does not change the other results on the page.", ftpMinLabel: "FTP min [W]", filterHint: "filters only this panel", ftpMaxLabel: "FTP max [W]", analysisApply: "Apply", analysisReset: "Reset", analysisLoading: "Loading statistics and chart…", analysisEmpty: "No samples in the selected FTP range.", analysisError: "Could not load the analysis data.", analysisInvalidValue: "Enter a valid non-negative FTP value.", analysisInvalidRange: "Invalid FTP range — min is greater than max.", analysisCount: "samples in range", analysisTotal: "of all samples", analysisMedian: "MedAE", analysisBias: "Bias — mean residual", residualChart: "Residual chart — estimate minus actual", residualY: "residual [W]"
  }
};

const storedLanguage = localStorage.getItem("cycling-language");
const initialLanguage = storedLanguage || (navigator.language.toLowerCase().startsWith("en") ? "en" : "pl");
const state = {
  summary: null, view: "Variant_B", metric: "mae", language: initialLanguage,
  estimateTimer: null, estimateController: null,
  reader: { page: 1, pages: 0, zoom: 1, token: "", pageUrl: "", error: false },
  analysisRequestId: 0, analysisController: null
};
const $ = (selector, scope = document) => scope.querySelector(selector);
const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
const t = (key) => translations[state.language][key] || translations.pl[key] || key;
const number = (value, digits = 0) => Number(value).toLocaleString(state.language === "pl" ? "pl-PL" : "en-GB", { minimumFractionDigits: digits, maximumFractionDigits: digits });

function applyTranslations() {
  document.documentElement.lang = state.language;
  document.title = t("pageTitle");
  $("meta[name=description]").content = t("pageDescription");
  $$('[data-i18n]').forEach((node) => { node.textContent = t(node.dataset.i18n); });
  $$('[data-i18n-html]').forEach((node) => { node.innerHTML = t(node.dataset.i18nHtml); });
  $$('[data-i18n-aria]').forEach((node) => { node.setAttribute("aria-label", t(node.dataset.i18nAria)); });
  $$('[data-i18n-title]').forEach((node) => { node.setAttribute("title", t(node.dataset.i18nTitle)); });
  $$('[data-i18n-alt]').forEach((node) => { node.setAttribute("alt", t(node.dataset.i18nAlt).replace("{page}", state.reader.page)); });
  $$('[data-language]').forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.language === state.language)));
}

function setLanguage(language) {
  state.language = language === "en" ? "en" : "pl";
  localStorage.setItem("cycling-language", state.language);
  applyTranslations();
  if (state.summary) renderAll();
  scheduleEstimate(0);
}

function initNavigation() {
  const button = $(".menu-toggle"); const nav = $("#site-nav");
  button.addEventListener("click", () => { const open = button.getAttribute("aria-expanded") !== "true"; button.setAttribute("aria-expanded", String(open)); nav.classList.toggle("open", open); });
  $$("a", nav).forEach((link) => link.addEventListener("click", () => { nav.classList.remove("open"); button.setAttribute("aria-expanded", "false"); }));
  $$('[data-language]').forEach((button) => button.addEventListener("click", () => setLanguage(button.dataset.language)));
}

function initReveal() {
  if (!("IntersectionObserver" in window)) { $$(".reveal").forEach((node) => node.classList.add("visible")); return; }
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("visible"); observer.unobserve(entry.target); } }), { threshold: 0.1 });
  $$(".reveal").forEach((node) => observer.observe(node));
}

async function fetchJson(url, options = {}) {
  const headers = new Headers(options.headers || {}); headers.set("Accept-Language", state.language);
  const response = await fetch(url, { ...options, headers });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || t("loadError"));
  return body;
}

function scheduleEstimate(delay = 120) {
  clearTimeout(state.estimateTimer);
  state.estimateTimer = setTimeout(updateEstimate, delay);
}

async function updateEstimate() {
  const power = $("#mmp20"); const weight = $("#weight"); const error = $("#form-error");
  error.textContent = "";
  if (state.estimateController) state.estimateController.abort();
  state.estimateController = new AbortController();
  try {
    const result = await fetchJson("/api/estimate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mmp20: power.value, weight: weight.value, lang: state.language }), signal: state.estimateController.signal });
    $("#ftp-result").textContent = number(result.ftp, 1);
    $("#wkg-result").textContent = result.watts_per_kg ? `${number(result.watts_per_kg, 2)} W/kg` : "—";
    $(".formula").innerHTML = `<span>${number(result.mmp20, 0)} W</span><b>× 0.95</b><span>= ${number(result.ftp, 1)} W</span>`;
  } catch (exception) { if (exception.name !== "AbortError") error.textContent = exception.message; }
}

function initEstimator() {
  const form = $("#ftp-form"); const power = $("#mmp20"); const range = $("#mmp20-range"); const weight = $("#weight");
  power.addEventListener("input", () => { range.value = power.value; scheduleEstimate(); });
  range.addEventListener("input", () => { power.value = range.value; scheduleEstimate(); });
  weight.addEventListener("input", () => scheduleEstimate());
  form.addEventListener("submit", (event) => { event.preventDefault(); scheduleEstimate(0); });
}

function variantsForView() { return state.view === "compare" ? ["Variant_B", "Variant_C"] : [state.view]; }
function variantShort(variant) { return variant === "Variant_B" ? "B" : "C"; }
function metricMeta() {
  const map = {
    mae: { digits: 2, unit: " W", text: "metricMae", maxFloor: 15 },
    rmse: { digits: 2, unit: " W", text: "metricRmse", maxFloor: 20 },
    r2: { digits: 4, unit: "", text: "metricR2", maxFloor: 1 },
    median_ae: { digits: 2, unit: " W", text: "metricMedian", maxFloor: 12 }
  };
  return map[state.metric];
}

function renderStats() {
  $("[data-stat=sessions]").textContent = number(state.summary.dataset.sessions);
  $("[data-stat=athletes]").textContent = number(state.summary.dataset.athletes);
}

function renderModels() {
  const variants = variantsForView(); const meta = metricMeta();
  const rows = state.summary.models.filter((row) => variants.includes(row.variant));
  const rawMax = Math.max(...rows.map((row) => row[state.metric]));
  const max = state.metric === "r2" ? 1 : Math.max(meta.maxFloor, Math.ceil(rawMax / 5) * 5);
  $("#variant-title").textContent = state.view === "compare" ? t("comparison") : `${t(state.view === "Variant_B" ? "variantB" : "variantC")}`;
  $("#metric-explainer").textContent = t(meta.text);
  $("#axis-min").textContent = state.metric === "r2" ? "0" : "0 W";
  $("#axis-max").textContent = `${number(max, state.metric === "r2" ? 1 : 0)}${meta.unit}`;
  $("#model-bars").innerHTML = rows.map((row) => {
    const value = row[state.metric]; const label = state.view === "compare" ? `${row.model} · ${variantShort(row.variant)}` : row.model;
    const tooltip = `${label} — ${state.metric.toUpperCase()}: ${number(value, meta.digits)}${meta.unit}; R²: ${number(row.r2, 4)}; MAE: ${number(row.mae, 2)} W`;
    return `<div class="model-bar interactive-mark variant-${variantShort(row.variant).toLowerCase()}" tabindex="0" data-tooltip="${tooltip}"><div class="model-bar-head"><span>${label}</span><b>${number(value, meta.digits)}${meta.unit}</b></div><progress class="model-progress" max="${max}" value="${value}" aria-label="${tooltip}"></progress></div>`;
  }).join("");
  bindTooltips($("#model-bars"), $("#chart-tooltip"));
}

function renderFeatures() {
  const variants = variantsForView();
  let rows = variants.flatMap((variant) => state.summary.features[variant].slice(0, state.view === "compare" ? 5 : 8).map((row) => ({ ...row, variant })));
  const max = Math.max(...rows.map((row) => row.importance));
  $("#feature-title").textContent = state.view === "compare" ? `${t("comparison")} · SHAP` : `${t(state.view === "Variant_B" ? "variantB" : "variantC")} · SHAP`;
  $("#top-feature").textContent = state.view === "compare" ? "mmp_10min ↔ power_p75" : rows[0].feature;
  $("#top-feature-copy").textContent = t(state.view === "Variant_B" ? "featureB" : state.view === "Variant_C" ? "featureC" : "featureCompare");
  $("#feature-bars").innerHTML = rows.map((row) => { const prefix = state.view === "compare" ? `${variantShort(row.variant)} · ` : ""; const tooltip = `${prefix}${row.feature}: mean |SHAP| = ${number(row.importance, 2)}`; return `<div class="feature-row interactive-mark variant-${variantShort(row.variant).toLowerCase()}" tabindex="0" title="${tooltip}"><span>${prefix}${row.feature}</span><progress class="feature-progress" max="${max}" value="${row.importance}" aria-label="${tooltip}"></progress><b>${number(row.importance, 1)}</b></div>`; }).join("");
}

function renderErrorRanges() {
  $("#error-ranges").innerHTML = state.summary.error_ranges.map((row) => `<div class="error-range" tabindex="0" title="MAPE: ${number(row.mape, 2)}%; ${number(row.athletes)} ${state.language === "pl" ? "zawodników" : "athletes"}"><span>${row.range}</span><strong>${number(row.mae, 2)} W</strong><small>${number(row.samples)} ${t("samples")}</small></div>`).join("");
}

function scatterCircle(point, variant, x, y) {
  const error = point.predicted - point.actual; const text = `${t(variant === "Variant_B" ? "variantB" : "variantC")}: ${t("actual")} ${number(point.actual, 1)} W · ${t("predicted")} ${number(point.predicted, 1)} W · ${t("error")} ${error >= 0 ? "+" : ""}${number(error, 1)} W`;
  return `<circle class="point variant-${variantShort(variant).toLowerCase()}" tabindex="0" role="img" aria-label="${text}" data-tooltip="${text}" cx="${x(point.actual)}" cy="${y(point.predicted)}" r="3.5"><title>${text}</title></circle>`;
}

async function renderScatter() {
  const variants = variantsForView();
  const payloads = await Promise.all(variants.map((variant) => fetchJson(`/api/predictions?variant=${variant}&limit=${state.view === "compare" ? 80 : 120}`)));
  const datasets = payloads.map((payload, index) => ({ variant: variants[index], points: payload.points }));
  const values = datasets.flatMap((dataset) => dataset.points.flatMap((point) => [point.actual, point.predicted]));
  const low = Math.floor(Math.min(...values) / 50) * 50; const high = Math.ceil(Math.max(...values) / 50) * 50;
  const x = (value) => 42 + ((value - low) / (high - low)) * 490; const y = (value) => 305 - ((value - low) / (high - low)) * 270;
  const chart = $("#scatter-chart"); const grid = $(".scatter-grid", chart); grid.innerHTML = "";
  for (let index = 0; index <= 4; index += 1) { const gx = 42 + index * 122.5; const gy = 35 + index * 67.5; grid.insertAdjacentHTML("beforeend", `<line x1="${gx}" y1="35" x2="${gx}" y2="305"/><line x1="42" y1="${gy}" x2="532" y2="${gy}"/>`); }
  const ideal = $(".ideal-line", chart); ideal.setAttribute("x1", x(low)); ideal.setAttribute("y1", y(low)); ideal.setAttribute("x2", x(high)); ideal.setAttribute("y2", y(high));
  $(".scatter-points", chart).innerHTML = datasets.map((dataset) => dataset.points.map((point) => scatterCircle(point, dataset.variant, x, y)).join("")).join("");
  $(".legend-b").hidden = !variants.includes("Variant_B"); $(".legend-c").hidden = !variants.includes("Variant_C");
  bindTooltips($(".scatter-points", chart), $("#scatter-tooltip"));
}

function bindTooltips(container, output) {
  const show = (event) => { const target = event.target.closest("[data-tooltip]"); if (target && container.contains(target)) output.textContent = target.dataset.tooltip; };
  container.addEventListener("pointerover", show); container.addEventListener("focusin", show);
  container.addEventListener("pointerleave", () => { output.textContent = ""; });
}

function analysisBounds() {
  const minEl = $("#ftp-min"); const maxEl = $("#ftp-max");
  const minVal = minEl.value === "" ? null : Number(minEl.value);
  const maxVal = maxEl.value === "" ? null : Number(maxEl.value);
  if ((minVal !== null && (!Number.isFinite(minVal) || minVal < 0)) || (maxVal !== null && (!Number.isFinite(maxVal) || maxVal < 0))) return { error: "analysisInvalidValue" };
  if (minVal !== null && maxVal !== null && minVal > maxVal) return { error: "analysisInvalidRange" };
  return { min: minVal, max: maxVal };
}

function analysisCard(variant, stats) {
  const label = t(variant === "Variant_B" ? "variantB" : "variantC");
  const metrics = [
    ["MAE", stats.mae, " W", 2], ["RMSE", stats.rmse, " W", 2],
    [t("analysisMedian"), stats.median_ae, " W", 2],
    [t("analysisBias"), stats.bias, " W", 2],
    ["≤ 5 W", stats.within_5, " %", 1],
    ["≤ 10 W", stats.within_10, " %", 1],
    ["≤ 20 W", stats.within_20, " %", 1],
  ];
  const tooltip = `${label}: MAE ${number(stats.mae, 2)} W · RMSE ${number(stats.rmse, 2)} W · MedAE ${number(stats.median_ae, 2)} W · Bias ${number(stats.bias, 2)} W · ≤5 ${number(stats.within_5, 1)}% · ≤10 ${number(stats.within_10, 1)}% · ≤20 ${number(stats.within_20, 1)}%`;
  const rows = metrics.map(([name, value, unit, digits]) => `<div class="analysis-metric"><span>${name}</span><b>${number(value, digits)}${unit}</b></div>`).join("");
  return `<div class="analysis-card variant-${variantShort(variant).toLowerCase()}" tabindex="0" data-tooltip="${tooltip}"><div class="analysis-card-head"><span>${label}</span><b>${number(stats.count, 0)} ${t("analysisCount")} / ${number(stats.total_count, 0)} ${t("analysisTotal")}</b></div>${rows}</div>`;
}

function residualCircle(point, variant, x, y) {
  const error = point.predicted - point.actual; const fill = variant === "Variant_B" ? "#b8ff3d" : "#65cfe4";
  const text = `${t(variant === "Variant_B" ? "variantB" : "variantC")}: ${t("actual")} ${number(point.actual, 1)} W · ${t("predicted")} ${number(point.predicted, 1)} W · ${t("error")} ${error >= 0 ? "+" : ""}${number(error, 1)} W`;
  return `<circle class="point variant-${variantShort(variant).toLowerCase()}" tabindex="0" role="img" aria-label="${text}" data-tooltip="${text}" fill="${fill}" opacity="0.42" cx="${x(point.actual)}" cy="${y(error)}" r="3.5"><title>${text}</title></circle>`;
}

async function renderAnalysis() {
  const status = $("#analysis-status");
  if (state.analysisController) state.analysisController.abort();
  state.analysisController = new AbortController();
  state.analysisRequestId += 1;
  const request = state.analysisRequestId;
  const bounds = analysisBounds();
  if (bounds.error) { status.textContent = t(bounds.error); $("#analysis-cards").innerHTML = ""; $(".residual-points").innerHTML = ""; return; }
  const signal = state.analysisController.signal;
  status.textContent = t("analysisLoading");
  try {
    const params = {};
    if (bounds.min !== null) params.ftp_min = bounds.min;
    if (bounds.max !== null) params.ftp_max = bounds.max;
    const query = new URLSearchParams(params).toString();
    const variants = variantsForView();
    const payloads = await Promise.all(variants.map((variant) => fetchJson(`/api/analysis?variant=${variant}${query ? "&" + query : ""}`, { signal })));
    if (request !== state.analysisRequestId) return;
    const datasets = payloads.map((payload, index) => ({ variant: variants[index], stats: payload.stats, count: payload.count, points: payload.points }));
    const hasData = datasets.some((dataset) => dataset.count > 0);
    if (!hasData) { status.textContent = t("analysisEmpty"); $("#analysis-cards").innerHTML = ""; $(".residual-points").innerHTML = ""; return; }
    $("#analysis-cards").innerHTML = datasets.filter((dataset) => dataset.stats).map((dataset) => analysisCard(dataset.variant, dataset.stats)).join("");
    status.textContent = "";
    const points = datasets.flatMap((dataset) => dataset.points.map((point) => ({ ...point, variant: dataset.variant })));
    const axials = points.map((point) => point.actual);
    const residuais = points.map((point) => point.predicted - point.actual);
    const axLow = Math.floor(Math.min(...axials) / 50) * 50;
    const axHigh = Math.max(Math.ceil(Math.max(...axials) / 50) * 50, axLow + 50);
    const rMax = Math.max(10, Math.ceil(Math.max(...residuais.map((value) => Math.abs(value))) / 10) * 10);
    const rLow = -rMax; const rHigh = rMax;
    const x = (value) => 42 + ((value - axLow) / (axHigh - axLow)) * 490; const y = (value) => 305 - ((value - rLow) / (rHigh - rLow)) * 270;
    const chart = $("#residual-chart"); const grid = $(".residual-grid", chart); grid.innerHTML = "";
    for (let index = 0; index <= 4; index += 1) {
      const gx = 42 + index * 122.5; const gy = 35 + index * 67.5;
      const xVal = axLow + (axHigh - axLow) * index / 4; const yVal = rLow + (rHigh - rLow) * index / 4;
      grid.insertAdjacentHTML("beforeend", `<line x1="${gx}" y1="35" x2="${gx}" y2="305"/><line x1="42" y1="${gy}" x2="532" y2="${gy}"/><text class="axis-label" x="${gx}" y="320">${number(xVal, 0)}</text><text class="axis-label" x="30" y="${gy + 10}">${number(yVal, 0)}</text>`);
    }
    const zero = $(".residual-zero", chart); zero.setAttribute("x1", x(axLow)); zero.setAttribute("y1", y(0)); zero.setAttribute("x2", x(axHigh)); zero.setAttribute("y2", y(0));
    $(".residual-points", chart).innerHTML = points.map((point) => residualCircle(point, point.variant, x, y)).join("");
    bindTooltips($(".residual-points", chart), $("#residual-tooltip"));
    const existing = $(".scatter-legend", chart.parentElement);
    if (existing) existing.remove();
    const showB = variants.includes("Variant_B"); const showC = variants.includes("Variant_C");
    const legend = document.createElement("div");
    legend.className = "scatter-legend";
    legend.innerHTML = `${showB ? `<span class="legend-b"><i></i><b>${t("variantBShort")}</b></span>` : ""}${showC ? `<span class="legend-c"><i></i><b>${t("variantCShort")}</b></span>` : ""}`;
    chart.insertAdjacentElement("afterend", legend);
  } catch (exception) {
    if (request !== state.analysisRequestId) return;
    status.textContent = t("analysisError");
    $("#analysis-cards").innerHTML = ""; $(".residual-points").innerHTML = "";
  }
}

async function setView(view) {
  state.view = view;
  $$("[data-view]").forEach((button) => { const active = button.dataset.view === view; button.classList.toggle("active", active); button.setAttribute("aria-pressed", String(active)); });
  $("#plain-result-copy").textContent = t(view === "Variant_B" ? "plainB" : view === "Variant_C" ? "plainC" : "plainCompare");
  renderModels(); renderFeatures();
  renderAnalysis();
  try { await renderScatter(); } catch (_) { $(".scatter-points").innerHTML = ""; }
}

function renderAll() { renderStats(); renderErrorRanges(); setView(state.view); }

function initResultControls() {
  $$("[data-view]").forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));
  $("#metric-select").addEventListener("change", (event) => { state.metric = event.target.value; renderModels(); });
}

function initAnalysis() {
  $("#analysis-apply").addEventListener("click", () => { renderAnalysis(); });
  $("#analysis-reset").addEventListener("click", () => { $("#ftp-min").value = ""; $("#ftp-max").value = ""; $("#analysis-status").textContent = ""; renderAnalysis(); });
}

function initThesis() {
  const viewer = $("#thesis-viewer"); const viewport = $("#reader-viewport");
  const image = $("#reader-page-image"); const frame = $("#reader-page-frame"); const status = $("#reader-status");
  const fullscreen = $("#fullscreen-reader");

  const updateZoom = () => {
    frame.style.width = state.reader.zoom === 1 ? "min(100%, 1000px)" : `${state.reader.zoom * 100}%`;
    $("#reader-zoom-value").textContent = `${Math.round(state.reader.zoom * 100)}%`;
    $("#reader-zoom-out").disabled = state.reader.zoom <= 0.5;
    $("#reader-zoom-in").disabled = state.reader.zoom >= 2.5;
  };
  const setZoom = (zoom) => { state.reader.zoom = Math.min(2.5, Math.max(0.5, zoom)); updateZoom(); };
  const sourceFor = (page) => `${state.reader.pageUrl.replace("{page}", page)}?t=${encodeURIComponent(state.reader.token)}`;
  const updatePageControls = () => {
    $("#reader-page").value = state.reader.page;
    $("#reader-total").textContent = state.reader.pages || "—";
    $("#reader-prev").disabled = state.reader.page <= 1;
    $("#reader-next").disabled = state.reader.page >= state.reader.pages;
    image.alt = t("thesisPageAlt").replace("{page}", state.reader.page);
  };
  const loadPage = (requestedPage) => {
    if (!state.reader.pages) return;
    state.reader.page = Math.min(state.reader.pages, Math.max(1, Number(requestedPage) || 1));
    state.reader.error = false; status.textContent = t("readerLoading"); status.hidden = false;
    frame.hidden = true; updatePageControls();
    image.onload = () => {
      status.hidden = true; frame.hidden = false; viewport.scrollTo({ top: 0, left: 0 });
      [state.reader.page - 1, state.reader.page + 1].filter((page) => page >= 1 && page <= state.reader.pages).forEach((page) => { const preload = new Image(); preload.src = sourceFor(page); });
    };
    image.onerror = () => { state.reader.error = true; frame.hidden = true; status.textContent = t("readerLoadError"); status.hidden = false; };
    image.src = sourceFor(state.reader.page);
  };

  $("#reader-prev").addEventListener("click", () => loadPage(state.reader.page - 1));
  $("#reader-next").addEventListener("click", () => loadPage(state.reader.page + 1));
  $("#reader-page").addEventListener("change", (event) => loadPage(event.target.value));
  $("#reader-zoom-out").addEventListener("click", () => setZoom(state.reader.zoom - 0.25));
  $("#reader-zoom-in").addEventListener("click", () => setZoom(state.reader.zoom + 0.25));
  $("#reader-zoom-reset").addEventListener("click", () => setZoom(1));
  viewport.addEventListener("keydown", (event) => {
    if (event.target.matches("input")) return;
    if (event.key === "ArrowLeft") { event.preventDefault(); loadPage(state.reader.page - 1); }
    if (event.key === "ArrowRight") { event.preventDefault(); loadPage(state.reader.page + 1); }
    if (["+", "="].includes(event.key)) { event.preventDefault(); setZoom(state.reader.zoom + 0.25); }
    if (event.key === "-") { event.preventDefault(); setZoom(state.reader.zoom - 0.25); }
    if (event.key === "0") { event.preventDefault(); setZoom(1); }
  });
  fullscreen.addEventListener("click", async () => {
    if (document.fullscreenElement) { await document.exitFullscreen(); return; }
    if (viewer.requestFullscreen) await viewer.requestFullscreen();
  });
  if (!viewer.requestFullscreen) fullscreen.hidden = true;
  updateZoom();
  fetchJson("/api/thesis/manifest").then((manifest) => {
    state.reader.pages = manifest.pages; state.reader.pageUrl = manifest.page_url; state.reader.token = manifest.token;
    loadPage(1);
  }).catch(() => { state.reader.error = true; status.textContent = t("readerLoadError"); });
}

async function initData() {
  try { state.summary = await fetchJson("/api/summary"); renderAll(); }
  catch (exception) { console.error(exception); $("#model-bars").innerHTML = `<p>${t("loadError")}</p>`; }
}

applyTranslations();
initNavigation(); initReveal(); initEstimator(); initResultControls(); initAnalysis(); initThesis(); initData(); scheduleEstimate(0);
