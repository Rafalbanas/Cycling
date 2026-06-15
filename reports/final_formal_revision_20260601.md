# Raport końcowy: ujednolicenie formalne pracy magisterskiej

Data weryfikacji: 2026-06-01

## 1. Zakres i lista zmodyfikowanych plików

Wprowadzono kontrolowane poprawki formalne i merytoryczne bez zmiany metodologii eksperymentów, wariantów A/B/C ani wartości MAE, RMSE i R².

Zmodyfikowane pliki:

1. `style.tex` - Arial, marginesy, wcięcie akapitowe, skala nagłówków, podpisy i obsługa TikZ.
2. `front.tex` - lokalna korekta szerokości pól formularzowych oświadczenia po zmianie marginesów.
3. `chapters/wstep.tex` - doprecyzowanie zakresu czasowego i przestrzennego.
4. `chapters/rozdzial1_teoria.tex` - formalny dopisek do tytułu i cytowania dotyczące CP.
5. `chapters/rozdzial2_literatura.tex` - uzupełnienie przeglądu metodologii ML w sporcie.
6. `chapters/rozdzial3_metodologia.tex` - formalny dopisek do tytułu, diagram pipeline'u i wzmocnienie uzasadnienia podziału grupowego.
7. `chapters/rozdzial4_eksperymenty.tex` - formalny dopisek do tytułu.
8. `chapters/rozdzial5_dyskusja.tex` - formalny dopisek do tytułu, walidacja czasowa oraz moduł backend/API i MLOps.
9. `refs.bib` - sześć nowych, cytowanych publikacji naukowych.
10. `main.pdf` - ponownie wygenerowany dokument wynikowy.

## 2. Bibliografia

| Kategoria | Przed zmianami | Po zmianach |
| --- | ---: | ---: |
| Wszystkie aktywne rekordy | 40 | 46 |
| Bibliografia naukowa bez netografii | 34 | 40 |
| Netografia i datasety | 6 | 6 |
| Aktywnie cytowane rekordy | 40 | 46 |
| Nieużywane rekordy | 0 | 0 |

Końcowa bibliografia naukowa obejmuje 3 książki, 32 artykuły oraz 5 materiałów konferencyjnych. Netografia i datasety są wydzielone osobno.

### Duplikaty

Ponowny audyt nie wykazał zduplikowanych kluczy, DOI ani tytułów. W bieżącej iteracji nie było potrzeby usuwania kolejnych rekordów. W pliku pozostawiono dokładnie jeden rekord książki Allena, Coggana i McGregora:

`allen2019power` - wydanie 3 z 2019 roku, ISBN `9781937715939`.

### Dodane źródła

1. Chorley i Lamb (2020), DOI `10.3390/sports8090123` - rozdział teoriopoznawczy; CP, W' i zastosowanie CP w treningu kolarskim.
2. Galán-Rioja i in. (2020), DOI `10.1007/s40279-020-01314-8` - rozdział teoriopoznawczy; relacja CP do progów metabolicznych i wentylacyjnych.
3. Richter, O'Reilly i Delahunt (2021), DOI `10.1080/14763141.2021.1910334` - przegląd literatury i metodologia; ryzyko zawyżenia wyników, gdy dane jednego zawodnika trafiają do treningu i testu.
4. Rossi, Pappalardo i Cintia (2022), DOI `10.3390/sports10010005` - przegląd literatury; prawidłowy trening, walidacja i testowanie modeli ML w sporcie.
5. Fuller, Ferber i Stanley (2022), DOI `10.1136/bmjsem-2021-001259` - przegląd literatury; ograniczenia i ostrożna interpretacja ML w badaniach aktywności fizycznej.
6. Bergmeir, Hyndman i Koo (2018), DOI `10.1016/j.csda.2017.11.003` - dyskusja; zależności czasowe, niestacjonarność i dobór procedury walidacyjnej dla szeregów czasowych.

## 3. Zmiany w rozdziałach

Tytuły głównych rozdziałów uzupełniono o formalne określenia wymagane dla pracy projektowej:

1. Rozdział 1: dopisek `(rozdział teoriopoznawczy)`.
2. Rozdział 2: dopisek `(rozdział metodyczny)`.
3. Rozdział 3: dopisek `(część badawcza)`.
4. Rozdział 4: dopisek `(rozdział utylitarny)`.

We wstępie doprecyzowano zakres przestrzenny jako międzynarodowy, określony przez repozytorium GoldenCheetah OpenData. Zakres czasowy opisano jako historyczne dane z wersji repozytorium pozyskanej na potrzeby badania, bez wymyślania nieudokumentowanej daty pobrania.

W rozdziale metodologicznym dodano diagram TikZ przedstawiający pełny pipeline: dane źródłowe, ekstrakcję, kontrolę jakości, inżynierię cech, etykietę FTP, warianty A/B/C, `GroupShuffleSplit` po `athlete_id`, modele i ewaluację.

Uzasadnienie `data leakage` i `GroupShuffleSplit` wzmocniono źródłem dotyczącym ML w sporcie. Zachowano zdanie wyjaśniające, dlaczego zwykły losowy podział rekordów zawyżałby ocenę jakości.

W dyskusji dodano rozróżnienie pomiędzy generalizacją na nowych zawodników a walidacją czasową. Wskazano `walk-forward validation` jako kierunek dalszych badań.

Moduł wdrożeniowy rozszerzono o backend aplikacji, API, cykliczne przetwarzanie nowych aktywności, wersjonowanie modelu, monitoring błędów, obserwację dryfu danych i okresową rekalibrację.

## 4. Formatowanie

Zastosowano parametry z Załącznika nr 5 do Zarządzenia Nr 117/22:

| Element | Ustawienie końcowe |
| --- | --- |
| Czcionka podstawowa | Arial |
| Powód wyboru | Oficjalny szablon uczelni jednoznacznie wymaga Ariala |
| Kompilator | XeLaTeX |
| Tekst podstawowy | 12 pkt |
| Interlinia | 1,5 |
| Margines górny | 2,5 cm |
| Margines dolny | 2,5 cm |
| Margines lewy | 3,5 cm |
| Margines prawy | 1,5 cm |
| Wcięcie akapitu | 1 cm |
| Wyrównanie tekstu | obustronne |
| Tytuły rozdziałów | 16 pkt, pogrubione |
| Tytuły podrozdziałów | 14 pkt, pogrubione |
| Tytuły podpunktów | 12 pkt, pogrubione |
| Podpisy tabel i rysunków | 11 pkt, interlinia pojedyncza, wyrównanie do lewego marginesu |

Formatowanie jest spójne w aktywnych plikach pracy. Nie zmieniono treści strony tytułowej ani oświadczeń.

## 5. Kontrola techniczna

Wykonano:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
qpdf --check main.pdf
```

Wynik:

- kompilacja PDF: sukces;
- liczba stron: 80;
- błędy LaTeX: brak;
- `undefined citations`: brak;
- `undefined references`: brak;
- brakujące pliki graficzne: brak;
- ostrzeżenia Biber: brak;
- `Overfull \hbox` i `Overfull \vbox`: brak;
- kontrola składni PDF przez `qpdf`: sukces;
- aktywne rekordy bibliograficzne w `main.bbl`: 46;
- orientacyjna długość tekstu głównego po `detex`: 117 690 znaków.

Wizualnie sprawdzono stronę oświadczenia oraz stronę z nowym diagramem pipeline'u. Diagram jest czytelny, podpisany i obecny w spisie rysunków.

### Pozostałe ostrzeżenia

W logu pozostaje 346 ostrzeżeń `Underfull \hbox`. Nie blokują kompilacji i nie wskazują na wychodzenie tekstu poza marginesy. Ich liczba wzrosła po zastosowaniu wymaganego Ariala i węższego pola tekstowego wynikającego z asymetrycznych marginesów. Przed oddaniem wersji drukowanej nadal zasadny jest pełny ręczny przegląd PDF.

### Pozostały punkt proceduralny

Załącznik nr 5 wskazuje przekazanie pracy elektronicznej w formacie `*.doc` lub `*.docx` oraz `*.pdf`. Repozytorium źródłowe jest projektem LaTeX i generuje poprawny PDF. Należy potwierdzić z promotorem lub dziekanatem, czy wymagany jest dodatkowy plik DOCX, czy akceptowany jest PDF wraz ze źródłami LaTeX.

## 6. Ocena końcowa

Praca spełnia teraz najważniejsze wymogi formalne dotyczące czcionki, marginesów, interlinii, akapitów, nagłówków, struktury pracy projektowej i minimalnej liczby 40 pozycji bibliografii naukowej bez netografii. Wzmocniono również elementy wskazane w audycie: architekturę rozwiązania, leakage, podział osobniczy, walidację czasową i scenariusz wdrożeniowy.

## 7. Checklista

- [x] Bibliografia naukowa około 40 pozycji
- [x] Usunięte duplikaty
- [x] Allen/Coggan/McGregor zostawione tylko w wydaniu 2019
- [x] Nazwy rozdziałów dopasowane do struktury formalnej
- [x] Zakres czasowy i przestrzenny doprecyzowany
- [x] Diagram pipeline'u dodany
- [x] Data leakage wzmocnione źródłami
- [x] GroupShuffleSplit lepiej uzasadniony
- [x] Ograniczenie dotyczące walidacji czasowej dodane
- [x] Fragment wdrożeniowy / MLOps dodany
- [x] Czcionka zgodna z wymogami
- [x] Tekst podstawowy 12 pkt
- [x] Interlinia 1,5
- [x] Margines lewy 3,5 cm
- [x] Margines prawy 1,5 cm
- [x] Margines górny 2,5 cm
- [x] Margines dolny 2,5 cm
- [x] Wcięcie akapitowe 1 cm
- [x] Tekst wyjustowany
- [x] Nagłówki spójne
- [x] Tabele i rysunki spójne
- [x] Bibliografia spójna
- [x] PDF kompiluje się bez błędów
- [x] Brak undefined citations
- [x] Brak undefined references
