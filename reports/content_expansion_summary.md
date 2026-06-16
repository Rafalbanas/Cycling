# Podsumowanie rozbudowy treści pracy

## 1. Zakres wykonanych prac

Rozbudowano aktywne rozdziały pracy bez zmiany danych, skryptów przetwarzania ani wyników eksperymentów ML.

Zmienione pliki treści:

- `chapters/wstep.tex`
- `chapters/rozdzial1_teoria.tex`
- `chapters/rozdzial2_literatura.tex`
- `chapters/rozdzial3_metodologia.tex`
- `chapters/rozdzial4_eksperymenty.tex`
- `chapters/rozdzial5_dyskusja.tex`
- `chapters/zakonczenie.tex`

Dodane raporty:

- `reports/content_length_before_expansion.md`
- `reports/content_length_after_expansion.md`
- `reports/content_expansion_summary.md`

Przed edycją utworzono kopię aktywnych plików:

`backups/expand_content_20260531_213930/`

## 2. Rozbudowane sekcje

Rozbudowa objęła:

- uzasadnienie aktualności tematu i praktycznego znaczenia estymacji pasywnej we wstępie;
- relacje pomiędzy FTP, CP, MLSS, progami mleczanowymi i wentylacyjnymi;
- heurystyczny charakter testu 20-minutowego i współczynnika `0,95`;
- ograniczenia diagnostyki laboratoryjnej oraz specyfikę danych terenowych;
- znaczenie filtracji, inżynierii cech i kontroli leakage;
- powiązanie literatury z problemem badawczym;
- architekturę pipeline'u od ZIP do ewaluacji oraz uzasadnienie batch processingu;
- definicję etykiety `ftp_label`, grupy cech, warianty A/B/C i podział po `athlete_id`;
- interpretację metryk, modeli, wykresów i spadku jakości między wariantami B i C;
- perspektywę zawodnika, trenera i platformy analitycznej;
- ograniczenia walidacji, etykiet, sensorów i danych historycznych;
- ryzyka wdrożenia oraz potrzebę komunikowania niepewności;
- etapowe wdrażanie prototypu w trybie informacyjnym;
- wnioski teoretyczne, empiryczne i kierunki dalszych badań w zakończeniu.

## 3. Długość treści

| Część pracy | Stan przed | Stan po | Dodano |
|---|---:|---:|---:|
| Wstęp | 6 583 | 8 906 | 2 323 |
| Rozdział 1 | 36 494 | 48 107 | 11 613 |
| Rozdział 2 | 6 208 | 14 912 | 8 704 |
| Rozdział 3 | 13 949 | 19 069 | 5 120 |
| Rozdział 4 | 5 624 | 12 824 | 7 200 |
| Zakończenie | 2 802 | 5 020 | 2 218 |
| **Suma** | **71 660** | **108 838** | **37 178** |

Osiągnięto docelowy zakres około 100 000--110 000 znaków ze spacjami.

## 4. Audyt spójności

Nie zmieniono tabel wynikowych. Nie trenowano modeli i nie pobierano danych.

W aktywnych rozdziałach nie znaleziono:

- starych liczb `126`, `25 738`, `25 945`, `25738`, `25945`;
- fraz roboczych `TODO`, `FIXME`, `do uzupełnienia`, `należy dodać`, `można rozważyć`;
- słowa `opener`;
- aktywnych cytowań numerycznych ani komend `\cite`.

Zachowano cytowania autor-rok przez `\parencite`.

## 5. Kompilacja i PDF

Uruchomiono:

```sh
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
latexmk -g -pdf -interaction=nonstopmode -file-line-error main.tex
```

Drugie polecenie wymusiło pełną przebudowę wraz z `biber`.

Kompilacja zakończyła się powodzeniem. Końcowy plik `main.pdf` ma 63 strony.

W logu nie ma:

- błędów LaTeX;
- niezdefiniowanych cytowań;
- niezdefiniowanych referencji;
- ostrzeżeń `Overfull \hbox`.

Pozostały drobne ostrzeżenia `Underfull \hbox`. Render RGB dokumentu przez Ghostscript nie wykazał ucięć, osieroconych podpisów ani nietypowych pustych stron. Strony zawierające samodzielne wykresy są poprawnie wyśrodkowane.

## 6. Ręczna kontrola autora

Autor powinien jeszcze:

- przeczytać cały PDF pod kątem stylu i preferencji promotorki;
- sprawdzić aktualność strony tytułowej oraz oświadczeń względem wzoru uczelni;
- ocenić czytelność osi i etykiet wykresów w docelowym wydruku;
- potwierdzić dane bibliograficzne i daty dostępu źródeł internetowych;
- zdecydować, czy strony rysunkowe z wykresami mają pozostać jako samodzielne strony w finalnym składzie.
