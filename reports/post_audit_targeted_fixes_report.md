# Raport punktowych poprawek po audycie formalno-merytorycznym

## Zmienione pliki

- `chapters/wstep.tex`
- `chapters/rozdzial1_teoria.tex`
- `chapters/rozdzial3_metodologia.tex`
- `chapters/rozdzial5_dyskusja.tex`
- `chapters/zakonczenie.tex`
- `reports/post_audit_targeted_fixes_report.md`

## Wprowadzone poprawki

| Punkt audytu | Plik | Opis |
| --- | --- | --- |
| 2.A | `chapters/rozdzial3_metodologia.tex` | Doprecyzowano, że wariant B usuwa bezpośredni składnik etykiety `mmp_20min`, ale inne cechy MMP, np. `mmp_10min` i `mmp_30min`, mogą pozostawać silnymi pośrednimi proxy. Wskazano rolę wariantu C jako bardziej konserwatywnej kontroli. |
| 2.B | `chapters/rozdzial5_dyskusja.tex` | Uzupełniono interpretację wariantu B: brak bezpośredniego leakage nie oznacza braku informacji z krzywej mocy. Wynik opisano jako predykcję operacyjnej, historycznej etykiety FTP, a wariant C jako scenariusz bardziej konserwatywny. |
| 2.C | `chapters/zakonczenie.tex` | Doprecyzowano zakres potwierdzenia hipotezy: prototyp, historyczna ewaluacja, dane GoldenCheetah OpenData i heurystyczna etykieta FTP. Dodano, że nie jest to potwierdzenie pełnej gotowości produkcyjnej bez walidacji prospektywnej. |
| 2.C | `chapters/zakonczenie.tex` | Dodano zdanie, że aktualizacja stref treningowych na podstawie modelu powinna być rekomendacją wymagającą weryfikacji, a nie automatyczną decyzją systemu. |
| 2.D | `chapters/rozdzial3_metodologia.tex` | Dodano ograniczenie populacyjne dotyczące niereprezentatywności użytkowników GoldenCheetah OpenData dla całej populacji kolarzy. |
| 2.E | `chapters/rozdzial3_metodologia.tex` | Dodano uwagę, że stabilność wyników można w przyszłości sprawdzić przez powtarzany `GroupShuffleSplit` lub `GroupKFold`, przy zachowaniu przewagi obecnego podziału grupowego nad losowym mieszaniem sesji. |
| 2.F | `chapters/rozdzial5_dyskusja.tex` | Doprecyzowano brak analizy błędów według zawodnika, zakresu FTP, liczby sesji, kompletności sensorów i profilu zawodnika oraz wynikające z tego ograniczenie interpretacyjne. |
| 3.D | `chapters/wstep.tex`, `chapters/rozdzial1_teoria.tex` | Usunięto nienaturalne określenie `teoriopoznawczy`; zastosowano określenie `teoretyczno-literaturowy` w nazwie rozdziału i skrócono nazwę celu do `Cel poznawczy`. |

## Kontrole bibliograficzne i formalne

- Sprawdzono `refs.bib` i `url_refs.bib`: nie znaleziono zduplikowanych kluczy ani powtórzonych DOI.
- Wpis `borszcz2018ftp` występuje jednokrotnie. Wpis `borszcz2019ftp_mlss` dotyczy innej publikacji i został pozostawiony.
- Źródła BikeRadar i Nomad Frontiers pozostawiono jako podstawę schematycznej ilustracji dryfu tętna. Nie podpierają samodzielnie kluczowych twierdzeń fizjologicznych.
- Źródło Phases Cycling pozostawiono w miejscach dotyczących praktyki treningowej; występuje obok mocniejszych źródeł naukowych lub podręcznikowych.
- Opis etykiety FTP już zawierał współczynnik `0,95`, charakter heurystyczny i operacyjny oraz rozróżnienie względem laboratoryjnego pomiaru MLSS/CP.
- Podpisy schematycznych rysunków testu 20-minutowego, testu 60-minutowego i dryfu tętna już zawierały informację `Źródło: Opracowanie własne`.

## Walidacja techniczna

- Kompilacja: `bash scripts/compile_thesis.sh`
- Wynik: sukces, wygenerowano `main.pdf` (78 stron).
- Bibliografia i netografia: wygenerowane poprawnie.
- Spis treści, spis rysunków i spis tabel: zaktualizowane poprawnie.
- Brak `undefined citations`.
- Brak `undefined references`.
- Brak błędów LaTeX i brak ostrzeżeń `Overfull \hbox` / `Overfull \vbox`.
- Pozostały ostrzeżenia `Underfull \hbox` (72 wystąpienia). Nie wskazują na obcięcie treści; nie były przedmiotem zmian.
- `qpdf --check main.pdf`: sukces, brak błędów składni i kodowania strumieni.
- `pdftoppm` nie był dostępny. Do renderowania kontrolnego użyto lokalnego Ghostscript (`gs`) i wizualnie sprawdzono strony dotknięte zmianami.

## Celowo nie zmieniono

- metodologii eksperymentów, sposobu trenowania modeli i definicji wariantów A/B/C;
- wartości metryk, tabel wynikowych, wykresów i wniosków liczbowych;
- plików bibliograficznych, ponieważ kontrola nie wykazała duplikatu wymagającego usunięcia;
- źródeł popularnych w netografii, ponieważ pełnią funkcję pomocniczą lub ilustracyjną;
- istniejących ostrzeżeń `Underfull \hbox`, ponieważ nie powodują błędów składu ani utraty czytelności;
- pozostałych, wcześniejszych zmian obecnych w nieczystym drzewie roboczym repozytorium.
