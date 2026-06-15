# Raport aktualizacji bibliografii

Data kontroli: 2026-06-02

## 1. Zakres kontroli

Przeprowadzono audyt aktywnych plików `refs.bib`, `url_refs.bib` oraz plików `.tex`
włączanych przez `main.tex`. Sprawdzono liczbę rekordów, wykorzystanie cytowań,
duplikaty po kluczu, DOI, tytule oraz zestawie autorów i roku, a także oddzielenie
publikacji naukowych od netografii. Wprowadzono wyłącznie krótkie uzupełnienia
literaturowe. Nie zmieniono metodologii eksperymentów, wariantów A/B/C,
hiperparametrów ani wyników liczbowych.

W repozytorium nie znaleziono plików o dokładnych nazwach
`Research Sources for Cycling Performance Prediction.md` oraz
`Audyt Pracy Magisterskiej_ Formalność i Jakość.md`. Audyt wykonano na podstawie
aktywnych źródeł projektu, istniejących raportów w katalogu `reports/` oraz listy
publikacji przekazanej w zadaniu.

## 2. Statystyki przed i po zmianach

| Kategoria | Przed zmianami | Po zmianach |
| --- | ---: | ---: |
| Bibliografia naukowa bez netografii | 40 | 45 |
| Netografia i datasety | 6 | 6 |
| Wszystkie aktywne rekordy `.bib` | 46 | 51 |
| Cytowane rekordy | 46 | 51 |
| Nieużywane rekordy | 0 | 0 |

Końcowa bibliografia naukowa obejmuje 3 książki, 36 artykułów i 6 materiałów
konferencyjnych.

## 3. Dodane źródła

1. Saeb et al. (2017), *The Need to Approximate the Use-Case in Clinical Machine
   Learning*, DOI `10.1093/gigascience/gix019`.
2. Chaibub Neto et al. (2019), *Detecting the Impact of Subject Characteristics
   on Machine Learning-Based Diagnostic Applications*, DOI
   `10.1038/s41746-019-0178-x`.
3. Dong (2022), *Leakage Prediction in Machine Learning Models When Using Data
   from Sports Wearable Sensors*, DOI `10.1155/2022/5314671`.
4. Karetnikov, Nuijten i Hassani (2021), *Data-Driven Support of Coaches in
   Professional Cycling Using Race Performance Prediction*, DOI
   `10.5220/0010656300003059`.
5. Stessens et al. (2024), *Physical Performance Estimation in Practice: A
   Systematic Review of Advancements in Performance Prediction and Modeling in
   Cycling*, DOI `10.1177/17479541241262385`.

Źródła Saeb et al. oraz Chaibub Neto et al. dodano jako bezpośrednią podbudowę
podziału osobniczego i ryzyka `identity confounding`. Praca Dong uzupełnia
kontekst leakage w danych z sensorów sportowych, ale nie stanowi jedynej podstawy
twierdzeń metodologicznych. Karetnikov et al. oraz Stessens et al. wzmacniają
przegląd zastosowań modelowania i ML w kolarstwie.

## 4. Źródła pominięte

Nie dodano następujących pozycji:

1. Amjad et al. (2026), Roth (2026) i Korkmaz (2026): bardzo nowe pozycje lub
   preprinty; nie są potrzebne do podbudowy tez, dla których istnieją publikacje
   recenzowane.
2. Gallet (2019): materiał konferencyjny o węższym zakresie; po dodaniu przeglądu
   Stessens et al. i pracy Karetnikov et al. nie wnosi koniecznego uzupełnienia.
3. Nimmerichter et al. (2017), Rodríguez-Rielves et al. (2021) i
   Montalvo-Pérez et al. (2021): poprawne publikacje metrologiczne, ale
   nadmiarowe wobec przeglądu Bouillod et al. (2022) oraz badania Valenzuela
   et al. (2022), które są już cytowane.
4. Patent Apple dotyczący predykcji FTP: nie jest potrzebny do argumentacji
   naukowej ani do krótkiego opisu rozwiązań rynkowych.
5. TrainerRoad, blogi, fora, Reddit, StackExchange i przypadkowe poradniki:
   nie dodawano ich do bibliografii naukowej.

## 5. Netografia i źródła komercyjne

Przeniesiono z `refs.bib` do `url_refs.bib`:

1. `nomadfrontiers_power_hr`,
2. `bikeradar_power_hr`.

Oba rekordy pozostają wyłącznie w netografii i są cytowane przy podpisie
ilustracji praktycznej dotyczącej relacji mocy i tętna. Nie podbudowują kluczowych
twierdzeń naukowych. Nie dodano TrainerRoad.

## 6. Duplikaty i książki

Końcowy skan nie wykazał:

1. zduplikowanych kluczy BibTeX,
2. zduplikowanych DOI,
3. zduplikowanych tytułów po normalizacji,
4. zduplikowanych rekordów według autorów i roku.

W aktywnych plikach występuje dokładnie jeden rekord książki Allena, Coggana
i McGregora:

```bibtex
@book{allen2019power,
  author    = {Allen, Hunter and Coggan, Andrew R. and McGregor, Stephen},
  title     = {Training and Racing with a Power Meter},
  edition   = {3},
  year      = {2019},
  publisher = {VeloPress},
  isbn      = {9781937715939}
}
```

Pozostawiono trzecie wydanie z 2019 roku. Starsza edycja nie występuje w
aktywnych plikach, więc nie było potrzeby zmiany klucza cytowania.

## 7. Zmodyfikowane pliki

1. `refs.bib`
2. `url_refs.bib`
3. `chapters/rozdzial2_literatura.tex`
4. `chapters/rozdzial3_metodologia.tex`
5. `reports/bibliography_update_report.md`
6. `main.pdf` - wygenerowany ponownie

W `chapters/rozdzial2_literatura.tex` uzupełniono przegląd ML w kolarstwie,
uzasadnienie kontroli leakage oraz opis `identity confounding`. W
`chapters/rozdzial3_metodologia.tex` wzmocniono uzasadnienie podziału
`GroupShuffleSplit` po `athlete_id`.

## 8. Kontrola techniczna

Projekt wykorzystuje XeLaTeX z powodu konfiguracji fontów w `style.tex`.
Wykonano:

```bash
biber main
latexmk -g -xelatex -interaction=nonstopmode -halt-on-error main.tex
qpdf --check main.pdf
```

Wynik:

- kompilacja PDF: sukces;
- plik wynikowy: `main.pdf`;
- liczba stron: 81;
- aktywne rekordy w `main.bbl`: 51;
- undefined citations: brak;
- undefined references: brak;
- duplicate entries: brak;
- unused bib entries: brak;
- ostrzeżenia `biber`: brak;
- kontrola składni PDF przez `qpdf`: sukces.

W logu pozostały ostrzeżenia `Underfull \hbox`, niezwiązane z bibliografią
i nieblokujące kompilacji.

Pierwsza próba kompilacji była zablokowana przez brak wolnego miejsca na dysku.
Usunięto wyłącznie odtwarzalne artefakty LaTeX, tymczasowe renderingi PDF oraz
cache `biber`, po czym wykonano pełną przebudowę.

## 9. Ocena końcowa

Bibliografia spełnia wymaganie minimum 40 pozycji naukowych bez netografii.
Końcowy wynik to 45 realnych pozycji naukowych, czyli poziom zgodny z docelowym
zakresem wskazanym w zadaniu. Dodane rekordy wzmacniają konkretne fragmenty
metodologii i przeglądu literatury, bez sztucznego zwiększania liczby źródeł.
