# Dodanie notebooka i rysunków teoretycznych

## Notebook

Notebook pomocniczy skopiowano z katalogu `Downloads` do:

`notebooks/wykresy_magisterka-2.ipynb`

Notebook pozostaje materiałem pomocniczym. Kompilacja LaTeX nie zależy od jego wykonania.

## Generator rysunków

Utworzono skrypt:

`scripts/generate_theory_figures.py`

Skrypt używa wyłącznie `numpy` i `matplotlib`, ustawia ziarno `np.random.seed(42)`, zapisuje pliki z `dpi=300` oraz `bbox_inches="tight"` i zamyka figury przez `plt.close(fig)`. Używa backendu `Agg`, więc nie wymaga interfejsu graficznego.

Systemowy `python3` nie ma zainstalowanego pakietu `matplotlib`. Skrypt wykrywa tę sytuację i automatycznie uruchamia się ponownie przez projektowe `venv/bin/python`. Dzięki temu wymagane polecenie działa:

```sh
python3 scripts/generate_theory_figures.py
```

## Wygenerowane rysunki

Wygenerowano:

- `figures/theory/cardiac_drift.png`;
- `figures/theory/ftp_20min_protocol.png`;
- `figures/theory/ftp_60min_protocol.png`;
- `figures/theory/power_duration_curve.png`.

Rysunek dryfu tętna pokazuje w przybliżeniu stałą moc, narastające z opóźnieniem tętno i adnotację wskazującą skalę dryfu. Rysunki protokołów zawierają polskie nazwy etapów. W skrypcie ani w aktywnym rozdziale nie występuje słowo `opener`.

## Zmiany LaTeX

Zmieniono:

`chapters/rozdzial1_teoria.tex`

Podmieniono ścieżki rysunków 1.1, 1.2, 1.3 i 1.4 na nowe pliki z katalogu `figures/theory/`. Dodano wymagane opisy przed rysunkami. Rysunek testu 60-minutowego znajduje się bezpośrednio w podsekcji dotyczącej tego testu, przed kolejną podsekcją.

Źródła:

- rysunek 1.1: `Źródło: Opracowanie własne na podstawie (...)`;
- rysunek 1.2: `Źródło: Opracowanie własne.`;
- rysunek 1.3: `Źródło: Opracowanie własne.`;
- rysunek 1.4: `Źródło: Opracowanie własne na podstawie koncepcji mocy krytycznej.`

## Kompilacja i weryfikacja

Uruchomiono:

```sh
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Kompilacja zakończyła się powodzeniem. Końcowy plik `main.pdf` ma 59 stron.

Zweryfikowano:

- czytelność i brak ucięcia trzech wygenerowanych plików PNG;
- osadzenie rysunków w PDF;
- numerację rysunków: 1.2, 1.3 i 1.4;
- aktualizację wpisów w `main.lof`;
- brak błędów LaTeX, nierozwiązanych odwołań i ostrzeżeń `Overfull \hbox`;
- poprawność składni skryptu Python oraz poprawność JSON notebooka.

## Kontrola ręczna autora

Autor powinien otworzyć `main.pdf` w docelowym czytniku PDF i ocenić, czy rozmiar tekstu wewnątrz wykresów jest komfortowy przy wydruku oraz czy rozmieszczenie stron 17--19 odpowiada oczekiwanej estetyce pracy. Lokalny render kontrolny Ghostscript wyświetlał tekst dokumentu jako czarne prostokąty z powodu problemu renderera z czcionkami, dlatego końcową ocenę typografii otaczającego tekstu należy wykonać w standardowym czytniku PDF.
