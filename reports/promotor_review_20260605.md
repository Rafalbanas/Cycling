# Raport promotorski - surowa ocena pracy magisterskiej

Data przegladu: 2026-06-05  
Oceniana wersja: `main.pdf` / `Rafal_Banas_praca_magisterska_final.pdf` z 2026-06-04, 92 strony, ok. 25 440 slow z ekstrakcji PDF.  
Temat: `Model predykcji formy kolarskiej oparty na danych telemetrycznych z urządzeń sportowych z wykorzystaniem uczenia maszynowego`

## Werdykt

Nie wysylalbym tej pracy promotorce bez poprawek minimalnych. Wyslalbym ja po jednej zwartej rundzie korekty techniczno-merytorycznej.

Rdzen pracy jest dobry: temat jest aktualny, czesc empiryczna ma realne dane, wariant kontrolny data leakage, wariant konserwatywny, podzial po zawodniku i uczciwie opisane ograniczenia. To jest material na obrone. Najwieksze ryzyka nie dotycza tego, czy praca "ma sens", tylko tego, czy promotorka nie zatrzyma jej na niespojnosciach, zbyt gladkim stylu i nieuporzadkowanych materialach dodatkowych.

Ocena surowa obecnej wersji: 4.0 / 5.0.  
Po poprawkach minimalnych: realistycznie 4.5 / 5.0.

## Najpilniejsze uwagi krytyczne

1. **Niespojnosc: "5000 zawodnikow" vs "5000 archiwow".**  
   W `chapters/rozdzial4_eksperymenty.tex` pojawia sie kilka okreslen "proba kontrolna 5000 zawodnikow" (linie 235, 272, 276, 295), podczas gdy poprawnie jest: 5000 archiwow ZIP i 4645 zawodnikow po filtrze FTP (linie 243-256). To jest blad, ktory promotor moze uznac za brak kontroli nad wynikami.

2. **Slowo "pasywne" jest metodologicznie wrazliwe.**  
   Praca dobrze pokazuje, ze wariant B po usunieciu `mmp_20min` nadal korzysta z sasiednich cech MMP, zwlaszcza `mmp_10min`. To jest uczciwie opisane, ale tytul, hipoteza i wnioski musza konsekwentnie podkreslac, ze wariant B nie jest "czysto pasywny" w rygorystycznym sensie. Najbezpieczniejszy wniosek powinien opierac sie na parze B/C, a nie tylko na wyniku B.

3. **Etykieta FTP jest rekonstruowana z tej samej sesji, nie z niezaleznego testu.**  
   To jest najpowazniejszy punkt merytoryczny. Model nie przewiduje laboratoryjnego FTP ani formalnego testu referencyjnego, tylko heurystyczna etykiete `0.95 * mmp_20min`. Praca to przyznaje, ale promotor moze zapytac: "czy model uczy sie formy, czy uczy sie odtwarzac profil mocy?". Odpowiedz musi byc przygotowana: jest to prototyp pasywnej estymacji etykiety operacyjnej, nie walidacja fizjologiczna.

4. **Brakuje mocnej analizy bledow wedlug grup.**  
   Metryki zagregowane sa dobre, ale dla pracy magisterskiej z ML warto dodac choc jedna prosta tabele: blad wedlug przedzialow FTP, ewentualnie MAPE lub MAE jako procent FTP. Sama dyskusja o tym ograniczeniu jest dobra, ale lepiej pokazac minimum danych.

5. **Zalacznik elektroniczny musi byc oczyszczony.**  
   Aktywny PDF nie zawiera TODO ani sladow ChatGPT/OpenAI. Natomiast w katalogach `reports/` i `scripts/` sa pliki robocze z TODO oraz metakomentarze o gotowosci pracy. Jesli do promotorki lub dziekanatu trafi ZIP calego repozytorium, to bedzie to wygladalo nieprofesjonalnie i moze zostac odczytane jako slad pracy automatycznej. Zalacznik powinien zawierac tylko niezbedne skrypty, dane wynikowe i instrukcje odtworzenia, bez historycznych raportow roboczych.

6. **Brak streszczenia i slow kluczowych moze byc problemem formalnym.**  
   W aktualnym `front.tex` widac strone tytulowa, oswiadczenia i spis tresci, ale nie widze streszczenia PL/EN ani slow kluczowych. Jesli szablon UE Katowice tego wymaga, trzeba to dodac przed wyslaniem.

7. **Drobne, ale widoczne uchybienia redakcyjne.**  
   Przyklady: `laboratóriów` w `chapters/rozdzial1_teoria.tex:60`, podwojna spacja w `chapters/rozdzial1_teoria.tex:32`, twarde odwolanie "tabeli 3.4" w `chapters/rozdzial4_eksperymenty.tex:155` zamiast `\ref{...}`, reczne `\vspace*{-2.2cm}` w `chapters/rozdzial4_eksperymenty.tex:315`. To nie sa wady naukowe, ale obnizaja wrazenie kontroli nad dokumentem.

## Ocena rozdzialow

| Czesc | Ocena | Surowa ocena promotorska | Najwazniejsze poprawki |
|---|---:|---|---|
| Wstep | 4.0/5 | Dobrze uzasadnia temat, cel, hipoteze i pytania. Mocne jest zawężenie "formy kolarskiej" do FTP. | Dodac krotkie, bardziej formalne wskazanie metod badawczych. Upewnic sie, ze "pasywne" jest zgodne z interpretacja wariantow B/C. |
| Rozdzial 1: teoria i literatura | 3.5/5 | Zakres jest szeroki i sensowny, ale miejscami ma styl podrecznikowy. Przeglad literatury jest bardziej opisowy niz krytyczno-porownawczy. | Skrocic najbardziej oczywiste fragmenty, poprawic literowki, ograniczyc zrodla blogowe do ilustracji, nie do twierdzen naukowych. |
| Rozdzial 2: metodologia | 4.0/5 | Najmocniejsza czesc koncepcyjna: pipeline, etykieta, warianty A/B/C i podzial po zawodniku sa dobrze opisane. | Dodac pelna liste cech albo tabele grup cech, liczbe zawodnikow train/test, wersje bibliotek i bardziej jawny opis tworzenia etykiety per sesja. |
| Rozdzial 3: eksperymenty i wyniki | 4.0/5 | Dobre porownanie modeli i wariantow. Wariant A jako kontrola leakage jest bardzo dobra decyzja. | Poprawic "5000 zawodnikow", dodac blad wzgledny/MAPE lub MAE w przedzialach FTP, usunac reczne poprawki layoutu typu `vspace`. |
| Rozdzial 4: dyskusja | 4.5/5 | Bardzo dobra ostroznosc interpretacyjna. Ograniczenia sa napisane dojrzale i bronia pracy przed nadinterpretacja. | Skondensowac powtorzenia. Dodac konkretniejszy akapit "co model moze, a czego nie moze twierdzic". |
| Zakonczenie | 4.5/5 | Warunkowa weryfikacja hipotezy jest uczciwa i bezpieczna. Dobre odpowiedzi na pytania badawcze. | Nieco wzmocnic konkluzje praktyczna, ale bez obiecywania gotowego systemu produkcyjnego. |
| Bibliografia i netografia | 3.5/5 | Liczba i profil zrodel sa wystarczajace. Sa dobre prace z fizjologii, ML, leakage i sport science. | Sprawdzic format online-first/przyszlych publikacji, dopilnowac dat dostepu, ograniczyc role netografii poradnikowej. |
| Formalia i sklad PDF | 3.5/5 | PDF buduje sie, ma 92 strony i brak nierozwiazanych cytowan/referencji w logu. | Naprawic jeden `Overfull \hbox` w tabeli `fit_record_example`, sprawdzic wymogi streszczenia, oczyscic zalacznik. |

## Audyt plagiatu

To nie jest pelny audyt JSA ani Turnitin. Przeprowadzilem praktyczny audyt ryzyka:

- sprawdzilem wybrane, charakterystyczne zdania w wyszukiwarce;
- sprawdzilem aktywne rozdzialy pod katem roboczych markerow i dokladnie zdublowanych akapitow;
- przejrzalem bibliografie oraz kilka DOI/zrodel;
- sprawdzilem repozytorium pod katem sladow roboczych w zalacznikach.

Wynik: nie znalazlem oczywistych dowodow kopiowania duzych fragmentow z internetu. Wyszukiwania dokladnych fraz z pracy nie zwrocily bezposrednich kopii. Czesciowe wyniki byly albo niepowiazane, albo dotyczyly ogolnych hasel ML. To nie gwarantuje wyniku antyplagiatu, ale nie widze czerwonej flagi typu "tekst skopiowany z jednego zrodla".

Zweryfikowane przykladowo zrodla:

- Stockwell i Corradini, "A Machine Learning Approach to Predict Cyclists' Functional Threshold Power" - widoczne w DBLP: https://dblp.org/rec/conf/ideal/StockwellC23.html
- Denham et al., "Cycling Power Outputs Predict Functional Threshold Power and Maximum Oxygen Uptake" - rekord repozytorium USQ: https://research.usq.edu.au/item/q6q61/cycling-power-outputs-predict-functional-threshold-power-and-maximum-oxygen-uptake
- Vos et al., "Predicting Cycling Performance Before and After Training..." - DOI/strona wydawcy: https://www.tandfonline.com/doi/abs/10.1080/08839514.2025.2565167
- Gough et al. 2025 - DOI widoczny w Journal of Science and Cycling: https://www.jsc-journal.com/index.php/JSC/article/download/964/845/5462

Ryzyka plagiatowe do ograniczenia:

1. Podpisy "opracowanie wlasne na podstawie..." musza byc prawdziwe. Jesli wykresy sa inspirowane materialami komercyjnymi lub blogami, nie moga sugerowac, ze sa wynikiem badania empirycznego.
2. Netografia poradnikowa powinna byc wykorzystywana tylko jako tlo praktyczne, nie jako fundament twierdzen fizjologicznych.
3. W zalaczniku nie powinno byc historycznych raportow z komentarzami typu "gotowe do promotora", bo to nie jest plagiat, ale wyglada zle i moze prowokowac pytania.

## Audyt sladow AI

Nie znalazlem jawnych markerow typu `ChatGPT`, `OpenAI`, `AI-generated` w aktywnych plikach pracy. Nie znalazlem tez dokladnie powtorzonych akapitow w aktywnych rozdzialach.

Sa jednak stylistyczne slady, ktore moga wygladac jak tekst generowany lub nadmiernie redagowany przez AI:

- bardzo czeste konstrukcje asekuracyjne: "nie oznacza", "nalezy interpretowac", "ma charakter", "z tego powodu";
- duza rownosc akapitow i malo indywidualnych przejsc autora;
- powtarzalne formuly wnioskowania: "model nie zastepuje", "wyniki nalezy interpretowac", "wariant pelni funkcje";
- miejscami zbyt gladki, bezosobowy styl w dyskusji i zakonczeniu.

To nie jest dowod uzycia AI. Detektory AI sa niewiarygodne i nie nalezy na nich opierac oceny. Ale promotor moze intuicyjnie wyczuc "zbyt gladki" styl. Najlepsza obrona to dodanie kilku bardziej autorskich, konkretnych zdan: dlaczego wybrano takie parametry, co bylo najtrudniejsze w danych, jak wygladal proces odrzucania outlierow, jakie decyzje byly kompromisem.

Najbardziej warto przeredagowac:

- `chapters/rozdzial2_literatura.tex:18-22` - bardzo gladka, ogolna interpretacja;
- `chapters/rozdzial4_eksperymenty.tex:224-237` - SHAP momentami brzmi jak nadinterpretacja fizjologiczna;
- `chapters/rozdzial5_dyskusja.tex:61-71` - opis modulu produkcyjnego jest dobry, ale brzmi jak specyfikacja wygenerowana z promptu;
- `chapters/zakonczenie.tex:18-23` - dobra tresc, ale mozna dodac bardziej autorski ton weryfikacji hipotezy.

## Plan naprawy

### Etap 0 - poprawki przed wyslaniem dzisiaj

1. Zamienic wszystkie "5000 zawodnikow" na "5000 archiwow ZIP" albo "4645 zawodnikow po filtrze FTP", zalezne od kontekstu.
2. Poprawic literowki: `laboratóriów`, podwojna spacje, ewentualnie inne drobiazgi z finalnego czytania.
3. Zastapic "tabeli 3.4" odwolaniem `tabeli~\ref{tab:wyniki_modele_wszystkie}`.
4. Usunac lub ograniczyc `\vspace*{-2.2cm}` w rozdziale eksperymentalnym, bo to wyglada jak reczne ratowanie skladu.
5. Sprawdzic, czy uczelnia wymaga streszczenia i slow kluczowych. Jesli tak, dodac streszczenie PL/EN.
6. Wyslac promotorce tylko PDF/DOCX i ewentualnie czysty zalacznik, nie cale repozytorium z raportami roboczymi.

### Etap 1 - poprawki na mocniejsza ocene

1. Dodac tabele z lista cech wariantu B i C albo przynajmniej grupy cech z liczebnoscia i przykladami.
2. Dodac liczbe zawodnikow w train/test, nie tylko liczbe sesji.
3. Dodac jedna analize bledow: MAE/MAPE w przedzialach FTP, np. `<150 W`, `150-250 W`, `250-350 W`, `>350 W`.
4. Dodac 1-2 zdania o licencji/etyce uzycia GoldenCheetah OpenData i anonimizacji.
5. Przeredagowac 4-6 najbardziej "AI-like" akapitow, szczegolnie w dyskusji i zakonczeniu.

### Etap 2 - jesli zostanie czas

1. Uruchomic powtarzany `GroupShuffleSplit` albo `GroupKFold` i pokazac stabilnosc MAE/R2.
2. Dodac prosty audyt outlierow: ile rekordow odrzucono, jakie byly skrajne wartosci przed filtrem, dlaczego filtr 50-500 W jest uzasadniony.
3. Dodac sanity check dla wariantu C jako glownego "konserwatywnego" wyniku w streszczeniu lub zakonczeniu.
4. Przygotowac czysta paczke zalacznika: `scripts/`, `results/`, `figures/`, `config/local_paths.example.json`, `README` z instrukcja, bez `reports/`, bez starych PDF i bez plikow roboczych.

## Kontrola techniczna wykonana podczas przegladu

- `bash scripts/compile_thesis.sh`: sukces, `latexmk` raportuje, ze `main.pdf` jest aktualny.
- `main.pdf` i `Rafal_Banas_praca_magisterska_final.pdf`: 92 strony, taki sam tekst wedlug ekstrakcji.
- Brak ostrzezen o nierozwiazanych cytowaniach i referencjach w `main.log`.
- W logu jest jeden istotny `Overfull \hbox` w `tables/fit_record_example.tex`, linie 7-21; reszta to glownie `Underfull \hbox`, typowe przy tabelach i polskim skladzie.
- Aktywne rozdzialy nie zawieraja jawnych markerow `TODO`, `ChatGPT`, `OpenAI`, `AI-generated`.

## Konkluzja

Praca jest zasadniczo gotowa merytorycznie, ale nie jest jeszcze czysta redakcyjnie. Najwieksza wartosc pracy to uczciwe pokazanie problemu data leakage i wariantu konserwatywnego. Najwieksze ryzyko to nadinterpretacja "pasywnej" estymacji oraz niespojnosc "5000 zawodnikow". Po poprawieniu tych punktow mozna ja wyslac promotorce z sensownym spokojem.
