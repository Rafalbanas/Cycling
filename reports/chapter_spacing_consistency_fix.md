# Raport: ujednolicenie odstępów tytułów rozdziałów

## Zakres zmiany

Zmieniono globalny styl dokumentu w pliku `style.tex`. Nie modyfikowano treści
rozdziałów, wyników eksperymentów, tabel, rysunków, podpisów ani bibliografii.

## Mechanizm formatowania

Dokument korzystał wcześniej z domyślnego formatowania `\chapter` klasy `book`.
Dodano pakiet `titlesec` i ustawiono jeden wspólny format dla rozdziałów:

```tex
\titleformat{\chapter}[display]
  {\normalfont\bfseries\fontsize{16}{19}\selectfont}
  {Rozdział \thechapter}
  {0.4em}
  {}

\titlespacing*{\chapter}
  {0pt}
  {-18pt}
  {16pt}
```

Ustawione wartości:

- rozmiar tytułu: `16pt`, interlinia `19pt`,
- odstęp między etykietą `Rozdział X` a tytułem: `0.4em`,
- odstęp przed nagłówkiem rozdziału: `-18pt`,
- odstęp po nagłówku rozdziału: `16pt`.

## Weryfikacja

Kompilacja poleceniem:

```sh
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

zakończyła się powodzeniem. Wygenerowany plik `main.pdf` ma **57 stron**.
Spis treści działa i wskazuje aktualne strony rozdziałów. Numeracja stron jest
widoczna i poprawna. Kontrola wizualna wykazała spójny, bardziej zwarty układ
tytułów bez przyklejenia nagłówków do górnej krawędzi strony.

## Strony do ręcznej kontroli

- `6` - Wstęp,
- `11` - Rozdział 1,
- `25` - Rozdział 2,
- `29` - Rozdział 3,
- `34` - Rozdział 4,
- `45` - Rozdział 5,
- `49` - Zakończenie,
- `52` - Spis rysunków,
- `53` - Spis tabel,
- `54` - Bibliografia,
- `56` - Netografia,
- `57` - Załącznik elektroniczny.
