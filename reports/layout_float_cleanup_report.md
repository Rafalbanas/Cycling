# Raport korekty składu i rozmieszczenia floatów

## Zmienione pliki

- `chapters/rozdzial1_teoria.tex`
- `chapters/rozdzial4_eksperymenty.tex`
- `reports/layout_float_cleanup_report.md`

## Wprowadzone korekty

### Rozdział teoretyczno-literaturowy

- Przeniesiono rysunek 1.1 dotyczący dryfu tętna za pełną listę punktów fizjologicznych. Wcześniej rysunek rozdzielał listę pomiędzy punktami `Dryf tętna` oraz `Zmęczenie i wyczerpanie`.
- Dodano `\FloatBarrier` za rysunkiem 1.1, aby wykres nie rozdzielał dalszego wywodu interpretacyjnego.
- Dodano `\FloatBarrier` na logicznych granicach podsekcji dotyczących testu 20-minutowego, testu 60-minutowego oraz krzywej mocy.
- Dodano barierę za rysunkiem 1.4, aby wykres krzywej mocy nie wpadał pomiędzy pierwsze linie sekcji `Charakterystyka danych treningowych`.

### Rozdział eksperymentalny

- Dodano `\FloatBarrier` po tabeli 3.1, aby tabela charakterystyki zbioru nie mieszała się z tekstem kolejnej sekcji.
- Dodano bariery przed sekcjami dotyczącymi modeli, wyników oraz interpretacji modeli. Dzięki temu tabele 3.2, 3.3 i 3.4 pozostają przy odpowiadających im fragmentach tekstu.
- Dodano barierę po parze rysunków 3.1 i 3.2, aby wykresy porównawcze nie przechodziły do sekcji analizy rozkładu błędów.
- Dodano bariery za rysunkami 3.3 i 3.4, aby akapity interpretacyjne następowały po właściwych wykresach.
- Dodano barierę za parą rysunków 3.5 i 3.6, aby interpretacja ważności cech nie wyprzedzała wykresów.

## Preambuła

- Nie zmieniano pakietów ani ustawień globalnych.
- Pakiety `microtype` oraz `placeins` były już obecne w `style.tex`.
- Nie zastosowano globalnego `\sloppy`, wymuszonego pozycjonowania `[H]` ani dodatkowych `\clearpage`.

## Walidacja techniczna

- Kompilacja: `bash scripts/compile_thesis.sh`
- Wynik: sukces, wygenerowano `main.pdf` (81 stron).
- Brak `undefined citations`.
- Brak `undefined references`.
- Brak błędów LaTeX.
- Brak ostrzeżeń `Overfull \hbox` i `Overfull \vbox`.
- Liczba ostrzeżeń `Underfull \hbox`: 72, bez zmiany względem stanu przed korektą.
- Brak ostrzeżeń `Underfull \vbox`.
- Spis treści, spis tabel i spis rysunków zostały zaktualizowane poprawnie.
- `qpdf --check main.pdf`: sukces, brak błędów składni i kodowania strumieni.

## Kontrola wizualna

- `pdftoppm` nie był dostępny w środowisku. Do renderowania stron użyto lokalnego Ghostscript (`gs`).
- Przejrzano strony zawierające rysunki teoretyczne, schemat architektury, tabele eksperymentalne i wykresy wynikowe.
- Po korekcie floaty nie rozbijają zdań ani akapitów i nie wyprzedzają tekstu, który je zapowiada.
- Dodatkowe strony wynikają z uporządkowania bloków wykresów i zachowania granic logicznych sekcji.

## Celowo nie zmieniono

- treści merytorycznej akapitów;
- wyników eksperymentów, metryk i wartości liczbowych;
- zawartości tabel wynikowych;
- wykresów, podpisów oraz plików graficznych;
- wniosków i metodologii;
- globalnych parametrów składu;
- istniejących ostrzeżeń `Underfull \hbox`, ponieważ ich liczba nie wzrosła i nie powodują utraty czytelności.
