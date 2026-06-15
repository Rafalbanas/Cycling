# Raport poprawek czytelności i struktury

Data wykonania: 2026-06-06

## Zmienione pliki

- `front.tex`
- `chapters/wstep.tex`
- `chapters/rozdzial1_teoria.tex`
- `chapters/rozdzial3_metodologia.tex`
- `chapters/rozdzial4_eksperymenty.tex`
- `chapters/rozdzial5_dyskusja.tex`
- `chapters/zakonczenie.tex`
- `reports/readability_and_structure_fix_report.md`

## Oświadczenia

W repozytorium nie znaleziono osobnego aktualnego wzoru oświadczeń uczelni. Porównano bieżącą treść z wcześniejszą historią pliku `front.tex` i zachowano stosowany dotychczas układ oraz brzmienie klauzul.

Tytuł pracy przeniesiono do jednej komendy `\thesistitlepl`, używanej na stronie tytułowej i w oświadczeniu autora. Zapobiega to rozbieżnościom tytułu w kolejnych wersjach. Zachowano dane autora: Rafał Banaś, kierunek Informatyka, numer albumu 152863. Poprawiono oczywistą interpunkcję w zdaniu dotyczącym repozytoriów. Pola daty i podpisów pozostały niewypełnione zgodnie z dotychczasowym wzorem projektu.

## Wstęp

Pierwsze akapity uporządkowano według kolejności problemowej:

1. znaczenie monitorowania formy w sporcie wytrzymałościowym;
2. obciążający charakter testów FTP;
3. dostępność telemetrii z urządzeń sportowych;
4. trudność interpretacji danych terenowych;
5. zastosowanie uczenia maszynowego i pomysł estymacji z rutynowych jazd;
6. operacyjne zawężenie pojęcia formy kolarskiej do FTP;
7. hipoteza, cele, pytania badawcze, metody i struktura pracy.

Zachowano zakres badania, liczby, hipotezę i pytania badawcze. Dodano zwięzłe wskazanie zastosowanych metod badawczych.

## Struktura podrozdziałów

Usunięto nieuzasadnione pojedyncze poziomy numeracji:

- `2.2.1 Uzasadnienie przetwarzania batchowego` włączono do sekcji `2.2 Charakterystyka źródeł danych`;
- `2.3.1 Filtracja wartości FTP` włączono do sekcji `2.3 Przygotowanie danych`;
- `3.7.1 Pomocnicza analiza interpretowalności SHAP dla wariantu C` włączono do sekcji `3.7 Znaczenie i ważność cech predykcyjnych`.

Nazwy zachowano jako nienumerowane, kursywne wprowadzenia do odpowiednich fragmentów. Spis treści nie zawiera samotnych podpunktów.

Początki rozdziałów 1--4 uzupełniono lub uproszczono tak, aby wskazywały cel rozdziału, jego zawartość i związek z celem pracy.

## Zakończenie

Usunięto pogrubione śródtytuły tworzone przez `\paragraph`. Zakończenie ma formę ciągłej syntezy obejmującej:

- wykonany potok analityczny i zakres danych;
- uzyskane wyniki wariantów A, B i C;
- warunkową weryfikację hipotezy i odpowiedzi na pytania badawcze;
- znaczenie praktyczne rozwiązania;
- ograniczenia i kierunki dalszych prac.

Nie zmieniono wartości metryk, wyników eksperymentów ani sensu wniosków.

## Kontrola spójności

- Tytuł pracy jest identyczny na stronie tytułowej i w oświadczeniu autora dzięki wspólnej komendzie LaTeX.
- We wstępie forma kolarska jest jawnie zdefiniowana operacyjnie jako poziom FTP.
- Opis struktury pracy odpowiada czterem numerowanym rozdziałom widocznym w spisie treści.
- Nie występują samotne podpunkty `2.2.1`, `2.3.1` ani `3.7.1`.
- Zakończenie nie zawiera `\textbf`, `\bfseries` ani pogrubionych nagłówków `\paragraph`.

## Kompilacja PDF

Uruchomiono:

```bash
latexmk -pdf main.tex
```

Wynik:

- kompilacja zakończona powodzeniem;
- wygenerowany plik: `main.pdf`;
- liczba stron: 91;
- kontrola `qpdf --check main.pdf`: bez błędów składni i kodowania strumieni;
- undefined citations: brak;
- undefined references: brak;
- `Overfull \hbox`: brak;
- `Overfull \vbox`: brak;
- `Underfull \hbox`: 84 ostrzeżenia nieblokujące, wynikające głównie z justowania, szerokości pola tekstowego i długich identyfikatorów technicznych.

Wizualnie sprawdzono stronę tytułową, oba oświadczenia, spis treści, pierwszą stronę wstępu, początki rozdziałów 1--4, zmienione fragmenty sekcji 2.2 i 2.3 oraz wszystkie strony zakończenia. Nie stwierdzono obciętego tekstu, nakładania elementów ani tekstu wychodzącego poza marginesy.
