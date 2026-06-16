# Raport zgodności pracy ze wzorem Uniwersytetu Ekonomicznego w Katowicach

Data audytu: 6 czerwca 2026 r.

## Podstawa oceny

Pracę porównano z dokumentami umieszczonymi w katalogu `wzory/`, przede wszystkim z:

- `zał._5_Zarządzenie_Nr_117-22.pdf` – szablonem pracy dyplomowej dla studiów II stopnia;
- `Zarządzenie_Nr_117-22-_załącznik_Nr_2.pdf` – wymaganiami merytorycznymi i edytorskimi;
- `Zarządzenie_Nr_117-22_wymogi_dla_prac_dyplomowych.pdf`.

Ze względu na wykonanie prototypu systemu, potoku ETL i modeli uczenia maszynowego pracę oceniono jako pracę projektową. Załącznik nr 4, dotyczący pracy w formie artykułu naukowego, nie jest właściwym wzorem.

## Ocena ogólna

**Status: praca może zostać wysłana promotorce jako kompletna wersja robocza, ale przed złożeniem ostatecznym wymaga kilku korekt formalnych.**

Ocena zgodności formalnej: **8/10**.

Najważniejsze elementy są spełnione: struktura pracy projektowej, objętość, liczba źródeł, marginesy, podstawowe rozmiary pisma, interlinia, wcięcia akapitowe, spisy oraz załącznik elektroniczny. Strona tytułowa i oświadczenia zostały dostosowane do załącznika nr 5.

## Wprowadzone zmiany

1. Przebudowano stronę tytułową zgodnie z układem załącznika nr 5.
2. Wstawiono dane autora:
   - Rafał Banaś;
   - kierunek: Informatyka;
   - numer albumu: 152863.
3. Wstawiono polski i angielski tytuł pracy.
4. Wstawiono informację: „Praca magisterska napisana pod kierunkiem dr Barbary Probierz”.
5. Odtworzono oświadczenie promotora.
6. Odtworzono oświadczenie autora i uzupełniono je danymi oraz tytułem pracy.
7. Pozostawiono puste miejsca na daty i podpisy.
8. Zweryfikowano, że strona tytułowa nie ma numeru strony, a dalsze strony mają numer w prawym dolnym rogu.

Zmiany znajdują się w pliku `front.tex`.

## Macierz zgodności

| Wymaganie | Ocena | Uwagi |
|---|---|---|
| Format A4 | Spełnione | Klasa dokumentu używa formatu A4. |
| Marginesy: górny i dolny 2,5 cm, lewy 3,5 cm, prawy 1,5 cm | Spełnione | Wartości ustawione dokładnie w `style.tex`. |
| Tekst 12 pkt, interlinia 1,5 | Spełnione | Ustawienia globalne są zgodne. |
| Wcięcie akapitowe 1 cm | Spełnione | Ustawione globalnie. |
| Nagłówki rozdziałów 16 pkt i podrozdziałów 14 pkt | Spełnione | Ustawienia zgodne z wymaganiami. |
| Krój Arial | Spełnione | Główny skrypt kompiluje pracę przez XeLaTeX i wykorzystuje systemowy krój Arial. |
| Strona tytułowa według załącznika nr 5 | Spełnione | Układ i dane zostały dostosowane. |
| Oświadczenie promotora | Spełnione | Treść i układ zgodne ze wzorem. |
| Oświadczenie autora | Spełnione | Uzupełnione danymi autora; pola daty i podpisu pozostawione puste. |
| Spis treści | Spełnione | Obecny w pracy. |
| Wstęp z problemem, celami, zakresem, metodami i strukturą | Spełnione merytorycznie | Przed wysłaniem końcowym wskazana kontrola zgodności nazw celów i pytań z zakończeniem. |
| Część teoretyczna, metodyczna i projektowo-empiryczna | Spełnione | Podział na większą liczbę rozdziałów jest dopuszczalny. |
| Zakończenie, ograniczenia i rekomendacje | Spełnione | Elementy występują w zakończeniu i dyskusji. |
| Objętość 110–170 tys. znaków ze spacjami bez załączników | Spełnione granicznie | Ekstrakcja tekstu z PDF dała około 169 753 znaków bez ostatniej strony załącznika. Wynik jest blisko górnej granicy. |
| Minimum 40 pozycji bibliograficznych | Spełnione | W bazach jest 51 cytowanych pozycji. |
| Minimum 8 źródeł obcojęzycznych | Spełnione | Bibliografia zawiera znacznie więcej niż 8 źródeł anglojęzycznych. |
| Styl cytowań APA | Zasadniczo spełnione | Używany jest styl autor–rok. Potrzebna końcowa kontrola metadanych i dat dostępu. |
| Bibliografia alfabetyczna i numerowana | Spełnione częściowo | Pozycje są sortowane i numerowane, ale podział „Bibliografia”/„Netografia” nie odtwarza dokładnie struktury „Literatura” ze wzoru. |
| Ciągła numeracja tabel i rysunków | Niespełnione | Obecnie numeracja zaczyna się ponownie w każdym rozdziale, np. 1.1, 2.1, 3.1. |
| Podpisy i źródła tabel oraz rysunków | Częściowo spełnione | Rozmiar i odstęp są zbliżone do wzoru; trzeba sprawdzić kompletność źródeł i zakres rzeczowy, podmiotowy oraz czasowy tytułów tabel. |
| Spis rysunków, tabel i załączników | Spełnione | Wszystkie spisy są obecne. |
| Rozdziały rozpoczynane od nowej strony | Spełnione | Zapewnia to klasa dokumentu. |
| Styl bezosobowy i zdania do około 25–30 słów | Częściowo spełnione | Wymaga końcowej korekty językowej; w pracy nadal występują długie zdania. |
| Wersje PDF i DOC/DOCX | Częściowo spełnione | Aktualny PDF jest poprawny; istniejący `main_for_review.docx` może nie zawierać najnowszych zmian. |
| Załączniki z kodem i danymi | Spełnione opisowo | Praca opisuje załącznik elektroniczny; przed złożeniem trzeba przygotować rzeczywiste archiwum. |

## Plan dostosowania

### Priorytet 1 – przed wysłaniem wersji finalnej

1. Zmienić numerację tabel i rysunków na ciągłą w całej pracy.
2. Uzgodnić z promotorką, czy napis „Załącznik 5. Szablon pracy dyplomowej dla studiów II stopnia” ma pozostać widoczny na finalnej stronie tytułowej. Został zachowany, ponieważ występuje we wzorze, ale uczelnie często traktują go jako oznaczenie formularza, a nie element składanej pracy.
3. Uporządkować końcowy wykaz źródeł zgodnie z układem uczelnianym: nadrzędny dział „Literatura”, kategorie źródeł oraz „Netografia”.
4. Wygenerować aktualny plik DOCX dopiero po zamknięciu wszystkich zmian w LaTeX-u.

### Priorytet 2 – kontrola redakcyjna

6. Sprawdzić każdy tytuł tabeli pod kątem zakresu rzeczowego, podmiotowego, przestrzennego i czasowego, o ile dany zakres ma zastosowanie.
7. Sprawdzić, czy każda tabela i każdy rysunek mają źródło, także gdy są opracowaniem własnym.
8. Rozważyć zmianę etykiety „Rysunek” na skrót „Rys.”, zgodny z przykładami w szablonie.
9. Rozważyć zmianę formatu nagłówka z „Rozdział 1.” na „1.”, jeżeli promotorka wymaga literalnego odwzorowania szablonu.
10. Skrócić najdłuższe zdania i usunąć pozostałości stylu osobowego, potocznego lub nadmiernie kategorycznego.

### Priorytet 3 – pakiet do złożenia

11. Przygotować archiwum ZIP z kodem, konfiguracją, dokumentacją odtworzenia i wymaganymi wynikami, bez danych objętych ograniczeniami licencyjnymi lub prywatnością.
12. Sprawdzić, czy wszystkie adresy internetowe mają daty dostępu i czy metadane DOI są poprawne.
13. Wykonać końcową kompilację PDF, kontrolę wizualną wszystkich stron oraz kontrolę braku pustych lub źle przeniesionych tabel i rysunków.
14. Upewnić się, że PDF, DOCX i wersja przekazana do Jednolitego Systemu Antyplagiatowego są identyczne treściowo.

## Rekomendacja promotorska

Aktualną wersję można przesłać promotorce do oceny i akceptacji kierunku zmian. Nie należy jeszcze traktować jej jako wersji gotowej do złożenia w dziekanacie. Największe ryzyko formalne stanowi nieciągła numeracja tabel i rysunków. Pozostałe rozbieżności są łatwe do usunięcia po potwierdzeniu przez promotorkę interpretacji wzoru.
