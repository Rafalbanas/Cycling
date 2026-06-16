# Raport poprawek formalno-merytorycznych

Data weryfikacji: 2026-06-01

## Zakres zmian

Wprowadzono i zweryfikowano poprawki formalno-merytoryczne bez ingerencji w dane eksperymentalne, wartości metryk, tabele wynikowe ani liczbowe wnioski z eksperymentów.

### Zmienione pliki

- `chapters/wstep.tex` - doprecyzowanie operacyjnego znaczenia pojęcia „forma kolarska” jako poziomu FTP oraz ograniczeń tej interpretacji.
- `chapters/rozdzial1_teoria.tex` - ujednolicenie cytowań dotyczących FTP i wskazania źródła zbioru GoldenCheetah OpenData.
- `chapters/rozdzial2_literatura.tex` - uzupełnienie przeglądu narzędzi i aktualizacja opisu źródła GoldenCheetah OpenData.
- `chapters/rozdzial3_metodologia.tex` - opis technologii, narzędzi, skryptowego potoku ETL i powtarzalności eksperymentów; doprecyzowanie operacyjnego i heurystycznego charakteru zmiennej celu.
- `chapters/rozdzial5_dyskusja.tex` - rozbudowanie części dotyczącej praktycznego wdrożenia, jakości danych i komunikowania niepewności.
- `chapters/zakonczenie.tex` - dopisanie ograniczenia interpretacyjnego: model estymuje etykietę FTP, a nie laboratoryjnie zmierzony próg fizjologiczny.
- `main.tex` - dodanie spisu załączników po spisie tabel, uporządkowanie bibliografii i netografii oraz rozbudowanie opisu załącznika elektronicznego.
- `style.tex` - konfiguracja numerowanego środowiska wykazu źródeł.
- `refs.bib` - ujednolicenie metadanych wybranych pozycji bibliograficznych i netograficznych.
- `url_refs.bib` - ujednolicenie adresów URL i dat dostępu oraz korekta opisu GoldenCheetah OpenData na projekt Open Science Framework (OSF).
- `main.pdf` - ponownie wygenerowany dokument wynikowy.

## Rozbudowane sekcje

- We wstępie dodano akapit definiujący „formę kolarską” operacyjnie jako FTP. Zaznaczono, że FTP jest mierzalnym wskaźnikiem dyspozycji wytrzymałościowej, ale nie pełnym opisem formy sportowej.
- W rozdziale metodologicznym dodano sekcję `Wykorzystane technologie i narzędzia`: Python, `pandas`, `NumPy`, `scikit-learn`, `XGBoost`, `matplotlib`, skryptowy potok ETL i zasady odtwarzalności eksperymentów.
- W metodologii i zakończeniu dopisano, że `ftp_label` jest etykietą operacyjną i heurystyczną. Model nie estymuje laboratoryjnie zmierzonego progu fizjologicznego.
- W dyskusji dodano koncepcję modułu wspierającego platformę treningową: sugerowane FTP, informowanie o niepewności, ocena jakości danych i brak automatycznego zastępowania testów kontrolnych.
- Po spisie tabel dodano osobny `Spis załączników`.
- Opis załącznika elektronicznego obejmuje strukturę projektu, skrypty źródłowe ETL, skrypt uruchamiający, konfigurację eksperymentów, pliki wynikowe i dokumentację odtworzenia procesu badawczego.

## Bibliografia i netografia

- Wykaz źródeł jest numerowany i rozdzielony na bibliografię oraz netografię.
- Aktywnie cytowany wykaz zawiera 30 pozycji (25 z bibliografii, 5 z netografii).
- Z końcowej bibliografii w pliku `refs.bib` usunięto robocze komentarze `TODO_VERIFY_SOURCE`.
- Poprawiono formatowanie i łamanie linków (DOI/URL) przy pomocy pakietu `xurl` (`\urlstyle{same}`).
- Sprawdzono nagłówek i występowanie "Netografia", a także zidentyfikowano i zatwierdzono poprawnego autora `{scikit-learn developers}`.
- Ujednolicono format aktywnych pozycji internetowych: adresy zapisano w polu `url`, a daty dostępu w polu `urldate`.
- Zweryfikowano źródło GoldenCheetah OpenData i wskazano projekt OSF: `https://osf.io/6hfpz/`.
- Zachowano nieużywany historyczny klucz `figshare_cycling_analytics_datasets` dla zgodności z materiałami pomocniczymi, ale skorygowano jego metadane. Aktywna treść pracy korzysta z klucza `osf_goldencheetah_opendata`.
- Nie dodano fikcyjnych źródeł.
- Nie dodano komentarzy `TODO_SOURCE`, ponieważ w udostępnionych materiałach nie wskazano minimalnej liczby pozycji wymaganej przez uczelnię. Jeśli formalny limit okaże się wyższy niż 16, należy dodać takie znaczniki dopiero po ustaleniu wymaganej liczby i miejsc wymagających wsparcia literaturą.

## Dane i wyniki

Nie zmieniono danych wejściowych, wyników eksperymentów, wartości metryk, tabel ani liczbowych wniosków. Zmiany dotyczą treści opisowej, interpretacji ograniczeń, informacji wdrożeniowych oraz formatu źródeł.

## Liczba znaków ze spacjami

Po poprawkach praca ma **111 893 znaki ze spacjami** w warstwie tekstowej.

Pomiar wykonano po usunięciu znaczników LaTeX i normalizacji białych znaków. Obejmuje aktywne pliki rozdziałów, wstęp, zakończenie, spis załączników oraz opis załącznika elektronicznego. Nie obejmuje metadanych strony tytułowej ani generowanego automatycznie wykazu źródeł. Dla porównania surowe pliki aktywnych rozdziałów zawierają łącznie **119 498 znaków**, ale liczba ta obejmuje składnię LaTeX.

## Weryfikacja techniczna

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` - kompilacja zakończona powodzeniem.
- `qpdf --check main.pdf` - nie wykryto błędów składni ani kodowania strumieni PDF.
- Wygenerowany dokument ma 71 stron.
- Biber odnalazł 30 aktywnych kluczy cytowań.
- W końcowym logu nie występują błędy cytowań, niezdefiniowane odwołania ani ostrzeżenia o pustych kategoriach bibliografii.

## Pozostałe ryzyka formalne

- Nie udostępniono regulaminu ani wzoru uczelni. Należy potwierdzić wymaganą minimalną liczbę źródeł, kolejność wykazów końcowych oraz to, czy numeracja bibliografii i netografii powinna być wspólna, czy rozpoczynana osobno.
- W logu kompilacji pozostaje 15 ostrzeżeń `Underfull \hbox`. Nie blokują kompilacji, ale przed złożeniem pracy wskazany jest wizualny przegląd łamania tekstu.
- W repozytorium pozostają historyczne kopie rozdziałów i niewłączone pliki robocze ze starszymi odwołaniami. Nie wpływają one na wygenerowany dokument, ale przed przekazaniem załącznika elektronicznego warto jasno oddzielić materiały archiwalne od wersji finalnej.
- Przed złożeniem pracy warto ponownie sprawdzić dostępność adresów URL oraz zgodność dat dostępu z wymaganym przez uczelnię formatem prezentacji.
