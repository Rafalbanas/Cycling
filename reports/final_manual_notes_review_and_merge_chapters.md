# Końcowy audyt notatek ręcznych i scalenie rozdziałów

## 1. Kopia bezpieczeństwa

Przed edycją utworzono kopię aktywnych plików:

`backups/final_manual_review_20260531_210753/`

Kopia obejmuje `main.tex`, `style.tex`, `front.tex`, oba pliki bibliografii oraz aktywne pliki rozdziałów.

## 2. Zmienione pliki

W ramach bieżącego audytu zmieniono:

- `style.tex`
- `chapters/wstep.tex`
- `chapters/rozdzial1_teoria.tex`
- `chapters/rozdzial2_literatura.tex`
- `chapters/rozdzial3_metodologia.tex`
- `chapters/rozdzial4_eksperymenty.tex`
- `chapters/rozdzial5_dyskusja.tex`
- `chapters/zakonczenie.tex`
- `reports/final_manual_notes_review_and_merge_chapters.md`

Zweryfikowano również układ wejściowy w `main.tex`. Nie zmieniano skryptów przetwarzania danych, plików wynikowych ani danych eksperymentalnych.

## 3. Scalenie rozdziałów i nowy układ pracy

Dawne rozdziały 1 i 2 zostały połączone. Plik `chapters/rozdzial2_literatura.tex` pozostał fizycznie osobnym plikiem, ale nie tworzy już osobnego `\chapter`; stanowi sekcje 1.5 i 1.6 rozdziału pierwszego.

Nowy układ:

1. `Teoretyczne podstawy estymacji FTP i przegląd literatury`
2. `Metodologia badań i projekt rozwiązania`
3. `Eksperymenty i wyniki`
4. `Ocena rozwiązania, zastosowanie praktyczne i dyskusja`

Zaktualizowano opis struktury we wstępie. Spis treści po kompilacji odzwierciedla nową numerację.

## 4. Punkty poprawione wcześniej i zweryfikowane

Przed bieżącym audytem były już obecne:

- globalne, zwarte odstępy tytułów rozdziałów w `style.tex` z użyciem `titlesec`;
- finalne liczby: 781 archiwów ZIP, 726 zawodników i 151 399 rekordów po filtrze FTP;
- filtr `50 <= ftp_label <= 500 W`;
- warianty A/B/C oraz podział `GroupShuffleSplit` po `athlete_id`;
- rysunek 1.2 bez słowa `opener`, z wymaganym opisem protokołu;
- rysunek 1.3 bezpośrednio przy sekcji testu 60-minutowego;
- rysunek 1.4 ze źródłem: `Opracowanie własne na podstawie koncepcji mocy krytycznej`;
- źródła przy aktywnych rysunkach i tabelach;
- konfiguracja cytowań autor-rok przez `biblatex`.

## 5. Punkty poprawione w bieżącym audycie

Wprowadzono następujące korekty:

- scalono teorię i literaturę w jeden rozdział oraz usunięto powtórzenia;
- przepisano wstęp: zakres pracy ma formę akapitów, opis metod jest syntetyczny, a struktura wskazuje część teoretyczną i rozdziały empiryczne 2-4;
- ujednolicono terminologię: w opisie badania stosowana jest `metodologia`;
- rozwinięto ograniczenia testów opartych na VO2max, VT1, VT2, progach mleczanowych i laboratorium;
- rozszerzono opis Random Forest, Gradient Boosting i XGBoost;
- opisano równanie mocy krytycznej wraz z symbolami i wnioskiem wynikającym ze wzoru;
- uporządkowano rozdział metodologiczny, w tym etykietowanie, warianty A/B/C i podział osobniczy;
- usunięto sugestię, że finalny eksperyment korzystał z walidacji krzyżowej;
- rozszerzono opis przebiegu eksperymentu, parametrów modeli, metryk i oceny na nieznanych zawodnikach;
- poprawiono podpisy wykresów wynikowych oraz opis ważności cech;
- dodano `\FloatBarrier`, aby wykres ważności cech wariantu C nie przechodził za podsumowanie rozdziału;
- przepisano dyskusję i zakończenie w ostrożnym stylu akademickim;
- ujednolicono aktywne cytowania źródeł internetowych, aby Netografia nie zawierała zduplikowanych wpisów Phases Cycling, Kaggle i Figshare.

## 6. Korekta raportowania wyników

Nie trenowano modeli i nie zmieniano wyników eksperymentu. W tabeli wynikowej poprawiono wartości RMSE, ponieważ wcześniejsze wartości w LaTeX nie zgadzały się z plikiem źródłowym `results/model_comparison_partial.csv`.

Skorygowane wartości obejmują między innymi:

- wariant B, XGBoost: RMSE `9,68 W`;
- wariant C, XGBoost: RMSE `14,49 W`.

Pozostałe wartości MAE, MedAE i R2 zachowano zgodnie z raportem wynikowym.

## 7. Cytowania i przypisy

Aktywne rozdziały korzystają z cytowań autor-rok przez `\parencite`. Nie znaleziono aktywnych cytowań numerycznych ani przypisów dolnych zastępujących cytowania literaturowe.

W katalogu `chapters/` pozostają starsze, niewłączane przez `main.tex` pliki `chapter*.tex` oraz `introduction.tex`. Zawierają historyczne fragmenty i komendy `\cite`, ale nie są częścią kompilowanego PDF. Nie usuwano ich zgodnie z ograniczeniem zachowania istniejących plików.

## 8. Formatowanie i kontrola rysunków

Zweryfikowano globalny styl nagłówków rozdziałów oraz wyrenderowano strony startowe wstępu, rozdziałów 1-4, zakończenia, spisów, bibliografii i netografii.

Zweryfikowano wizualnie rysunki 1.2, 1.3, 1.4 oraz wykresy wynikowe 3.1-3.6. Każdy aktywny rysunek ma odwołanie w tekście, podpis i źródło. Nie stwierdzono ucięć grafik ani osieroconych podpisów.

## 9. Stare liczby i fragmenty robocze

W aktywnych źródłach nie znaleziono starych liczb `126`, `25 738`, `25 945`, `25738`, `25945`, roboczych fraz `TODO`, `FIXME`, `do uzupełnienia`, `należy dodać`, `można rozważyć`, ani słowa `opener`.

Starsze pliki niewłączane przez `main.tex` zachowano bez czyszczenia jako materiał historyczny.

## 10. Kompilacja i PDF

Uruchomiono:

```sh
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Kompilacja zakończyła się powodzeniem. Końcowy plik `main.pdf` ma 50 stron.

W końcowym logu nie ma:

- błędów LaTeX;
- niezdefiniowanych referencji;
- niezdefiniowanych cytowań;
- ostrzeżeń `Overfull \hbox`.

Pozostały drobne ostrzeżenia `Underfull \hbox`, głównie w oświadczeniu początkowym, kilku akapitach i jednym podpisie rysunku. Kontrola wizualna nie wykazała problemów wymagających dalszej korekty.

Do renderowania stron użyto Ghostscript z urządzeniem `png16m`, ponieważ `pdftoppm` nie jest dostępny lokalnie. Render `pngalpha` dawał artefakty przezroczystości, których nie ma w PDF ani w renderze RGB.

## 11. Punkty pozostawione bez zmian

Nie zmieniano:

- rzeczywistych wyników eksperymentów poza korektą błędnego przepisania RMSE do LaTeX;
- danych, archiwów ZIP ani plików wynikowych;
- skryptów pobierania, przetwarzania i trenowania modeli;
- wpisów w plikach bibliografii;
- starszych, niewłączanych plików rozdziałów.

## 12. Ręczna kontrola przed wysłaniem

Autor powinien jeszcze ręcznie:

- przeczytać cały PDF pod kątem preferencji stylistycznych promotorki;
- sprawdzić stronę tytułową i oświadczenia zgodnie z aktualnym wzorem uczelni;
- ocenić czytelność osi i legend wykresów w docelowym wydruku;
- potwierdzić poprawność danych bibliograficznych i dat dostępu źródeł internetowych;
- zdecydować, czy starsze, niewłączane pliki `chapters/chapter*.tex` i `chapters/introduction.tex` mają pozostać w repozytorium jako archiwum.
