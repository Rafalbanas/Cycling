# Final APA and numbers fix

## Stare liczby

W źródłach LaTeX znaleziono:

- `126` w aktywnym pliku `chapters/wstep.tex` oraz w starszych, niewłączanych przez `main.tex` plikach `chapters/chapter3.tex`, `chapters/chapter4.tex` i `chapters/chapter5.tex`;
- `25 738` w starszym pliku `chapters/chapter3.tex`;
- nie znaleziono wystąpień `25 945`, `25738` ani `25945`.

Po poprawkach jedyne pozostawione wystąpienie `126` znajduje się w `chapters/rozdzial5_dyskusja.tex` i jest jasno opisane jako liczebność wcześniejszych prób prototypowych.

## Poprawki danych eksperymentu

W sekcji „Zakres pracy”, w punkcie „Zakres podmiotowy”, wpisano finalne dane:

- 726 kolarzy o zróżnicowanym poziomie wytrenowania;
- 151 399 przefiltrowanych rekordów treningowych;
- 781 archiwów ZIP;
- repozytorium GoldenCheetah OpenData jako źródło danych.

Dla spójności poprawiono również starsze pliki `chapters/chapter3.tex`, `chapters/chapter4.tex` i `chapters/chapter5.tex`.

## Źródła rysunków i tabel

Sprawdzono podpisy aktywnych rysunków i tabel. Wykresy oraz tabele utworzone bezpośrednio na podstawie wyników własnych zachowują opis „Źródło: Opracowanie własne.” lub precyzyjniejszy opis wykorzystanych danych własnych.

Poprawiono źródła pod rysunkami:

- rysunek 1.1: opracowanie własne na podstawie materiałów Nomad Frontiers i BikeRadar;
- rysunek 1.2: opracowanie własne na podstawie materiału TrainerRoad;
- rysunek 1.4: opracowanie własne na podstawie „PerfectPace, The Critical Power Chart”.

Rysunek 1.3 pozostawiono jako opracowanie własne.

## Kompilacja

Uruchomiono:

```sh
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Ponieważ `latexmk` początkowo uznał PDF za aktualny na podstawie znaczników czasu, wykonano również wymuszoną pełną przebudowę:

```sh
latexmk -g -pdf -interaction=nonstopmode -file-line-error main.tex
```

Kompilacja zakończyła się powodzeniem. Końcowy plik `main.pdf` ma 60 stron. W logu końcowym nie ma błędów LaTeX, nierozwiązanych odwołań ani ostrzeżeń `Overfull \hbox`.
