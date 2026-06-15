# Raport końcowy po rundzie naprawczej

Data kontroli: 2026-06-05

## Ocena ogólna promotorska

Praca jest na tym etapie możliwa do wysłania promotorce jako wersja do oceny merytorycznej. Najważniejsze ryzyka, które wcześniej osłabiały wiarygodność tekstu, zostały ograniczone: poprawiono niespójność "5000 zawodników", doprecyzowano operacyjny charakter etykiety FTP, osłabiono nadinterpretację słowa "pasywne", dodano podstawową analizę błędów według zakresów FTP oraz usunięto widoczne problemy redakcyjno-składowe.

Najważniejsze zastrzeżenie nadal dotyczy walidacji: model estymuje etykietę `FTP = 0,95 x MMP20`, a nie laboratoryjnie zmierzony próg fizjologiczny. Ten punkt jest teraz w pracy komunikowany wyraźniej, ale promotorka może nadal oczekiwać dalszego doprecyzowania, jeżeli nacisk seminarium był bardziej fizjologiczny niż inżynierski.

## Wprowadzone poprawki

- Poprawiono sformułowania "5000 zawodników" na "5000 archiwów ZIP" tam, gdzie mowa o wejściowej próbie kontrolnej. Liczba zawodników po filtrze FTP pozostaje wskazana jako 4645.
- Wzmocniono opis etykiety FTP jako operacyjnej i heurystycznej, wyznaczanej ze wzoru `0,95 x MMP20`, bez utożsamiania jej z pomiarem laboratoryjnym.
- Złagodzono język dotyczący pasywnej estymacji, zwłaszcza w hipotezie, celu pracy, rozdziale eksperymentalnym i zakończeniu.
- Dodano akapit o anonimizacji, wtórnym charakterze danych i sposobie traktowania identyfikatorów zawodników.
- Dodano liczby zawodników w podziale Train/Test: 580 i 146.
- Dodano analizę błędów XGBoost wariantu B według zakresów FTP oraz zapisano ją w `results/error_by_ftp_bins.csv`.
- Poprawiono literówki i drobne problemy redakcyjne: `laboratóriów`, podwójna spacja, twarde odwołanie do tabeli, ręczne `\vspace*{-2.2cm}`.
- Zwężono odstępy w tabeli przykładowego rekordu telemetrycznego, co usunęło błąd `Overfull hbox`.
- Przygotowano propozycję streszczenia i słów kluczowych PL/EN w `reports/abstract_keywords_proposal.md`.
- Przygotowano czysty załącznik elektroniczny w `dist/zalacznik_elektroniczny/`.

## Ocena rozdziałów

| Część pracy | Ocena | Komentarz promotorski |
|---|---:|---|
| Wstęp | 4.0/5 | Cel i hipoteza są czytelniejsze po osłabieniu słowa "pasywne". Zakres pracy jest dobrze ustawiony, choć warto pilnować, aby "forma kolarska" nie brzmiała szerzej niż FTP. |
| Rozdział 1: teoria i literatura | 4.0/5 | Rozdział ma solidne tło pojęciowe. Poprawiono widoczne literówki. Nadal warto podczas ostatniego czytania sprawdzić, czy wszystkie twierdzenia fizjologiczne mają adekwatne cytowania. |
| Rozdział 2: metodologia | 4.5/5 | Najmocniejsza część pracy. Po dodaniu akapitu etyczno-anonimizacyjnego i wyraźniejszej definicji etykiety lepiej broni się metodologicznie. |
| Rozdział 3: eksperymenty i wyniki | 4.0/5 | Dodano potrzebną analizę błędów według zakresów FTP. Wyniki są dobrze pokazane, ale najwyższy zakres FTP ma bardzo małą liczebność, co trzeba interpretować ostrożnie. |
| Rozdział 4: dyskusja i zastosowanie | 4.0/5 | Dyskusja jest uczciwa i nie ukrywa ograniczeń. Po aktualizacji nie twierdzi już, że analiza błędów według FTP w ogóle nie istnieje. |
| Zakończenie | 4.0/5 | Wnioski są spójne z wynikami. Dobre jest warunkowe potwierdzenie hipotezy i wyraźne oddzielenie prototypu od gotowego systemu produkcyjnego. |
| Załącznik elektroniczny | 4.0/5 | Przygotowano czysty katalog techniczny bez raportów roboczych i lokalnej konfiguracji użytkownika. Warto przed formalnym złożeniem upewnić się, jakie dokładnie pliki uczelnia chce otrzymać. |

## Kontrola plagiatu i śladów AI

Nie wykonano pełnego sprawdzenia antyplagiatowego, ponieważ wymaga ono systemu typu JSA lub zewnętrznego narzędzia porównującego tekst z bazami publikacji. Lokalna kontrola nie wykazała oczywistych technicznych śladów do usunięcia, takich jak promptowe komentarze w treści pracy, placeholdery typu TODO w rozdziałach, sztuczne odwołania do "ChatGPT" ani niespójne fragmenty generatywne pozostawione w plikach LaTeX.

Ryzyko stylu AI oceniam jako umiarkowane, ale akceptowalne po obecnej rundzie: tekst bywa bardzo uporządkowany i ogólny, jednak zawiera konkretne liczby, ograniczenia, warianty eksperymentalne i odniesienia do danych. Najbardziej "AI-podobne" byłyby ogólne zdania o zastosowaniach praktycznych i zaletach uczenia maszynowego; warto je jeszcze raz przeczytać autorsko przed wysyłką, ale nie wymagają one pilnej przebudowy.

## Wynik kompilacji

- Komenda: `bash scripts/compile_thesis.sh`
- Wynik: sukces.
- PDF: `main.pdf`, 92 strony.
- Nierozwiązane cytowania: brak w końcowym logu.
- Nierozwiązane referencje: brak w końcowym logu.
- `Overfull hbox`: brak po poprawieniu tabeli `tables/fit_record_example.tex`.
- `Underfull hbox`: obecne, głównie typograficzne; nie blokują wysyłki.
- Kontrola wizualna renderowanych stron nie została wykonana, ponieważ w środowisku nie ma `pdftoppm`, `pdfinfo` ani biblioteki PyMuPDF.

## Plan naprawy przed finalnym złożeniem

1. Przejrzeć ręcznie finalny `main.pdf`, szczególnie strony z nową tabelą błędów, spisem tabel i rysunkami próby kontrolnej.
2. Zdecydować, czy promotorce wysłać sam PDF, czy PDF plus `reports/abstract_keywords_proposal.md` jako propozycję streszczenia.
3. Jeżeli uczelnia wymaga streszczenia w pracy, dodać sekcję PL/EN do `front.tex` zgodnie z uczelnianym wzorem.
4. Przed złożeniem uruchomić JSA lub uczelniany system antyplagiatowy; lokalna kontrola nie zastępuje takiego sprawdzenia.
5. Jeżeli promotorka zwróci uwagę na "formę kolarską" w tytule, rozważyć doprecyzowanie w rozmowie, że w pracy jest ona operacyjnie utożsamiona z FTP.
6. Przy wysyłce załącznika elektronicznego korzystać z `dist/zalacznik_elektroniczny/`, a nie z całego katalogu projektu.

## Decyzja końcowa

Po tej rundzie praca nadaje się do wysłania promotorce jako wersja po istotnych poprawkach. Nie oznacza to, że jest gotowa do natychmiastowego złożenia w dziekanacie: przed finalnym złożeniem potrzebna jest ręczna kontrola PDF, ewentualne dodanie streszczenia według wymogów uczelni oraz formalne sprawdzenie antyplagiatowe.
