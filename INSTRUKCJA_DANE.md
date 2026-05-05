# Instrukcja pozyskania i przetwarzania danych treningowych (GoldenCheetah OpenData / Kaggle)

Ponieważ w projekcie brakowało fizycznych plików treningowych z mierników mocy, niniejsza instrukcja krok po kroku opisuje, jak skorzystać z ogólnodostępnych baz danych w duchu Open Science, aby poprawnie zbudować zbiór cech (`features_ftp_dataset.csv`).

---

## 1. Skąd pobrać dane?

Dwa najlepsze, w pełni darmowe i anonimowe źródła surowych danych telemetrycznych z kolarstwa to:

### A. GoldenCheetah OpenData (Polecane)
Jest to gigantyczny, społecznościowy projekt zrzeszający tysiące kolarzy z całego świata udostępniających swoje surowe pliki.
*   **Adres:** Projekt opublikowany jest na GitHubie pod adresem [GoldenCheetah OpenData](https://github.com/GoldenCheetah/OpenData). Często zbiory hostowane są w chmurze AWS S3. Z poziomu repozytorium GitHub znajdziesz instrukcje pobrania zanonimizowanych paczek `.zip`.
*   Alternatywnie, najłatwiej wejść na główną stronę programu [GoldenCheetah](https://www.goldencheetah.org/) i poszukać zakładki OpenData.

### B. Repozytoria Kaggle
Kaggle to otwarta platforma dla analityków danych. 
*   **Adres:** Wejdź na [kaggle.com/datasets](https://www.kaggle.com/datasets)
*   **Wyszukiwanie:** Wpisz w lupkę frazy takie jak: `"cycling power dataset"`, `"GoldenCheetah open data"`, `"bike power heart rate"`.
*   Wybierz interesujący zbiór (upewniając się, że zawiera on próbki w postaci szeregów czasowych, a nie tylko gotowe podsumowania tabelaryczne). Platforma Kaggle zazwyczaj wymaga darmowej rejestracji w celu pobrania paczek `.zip`.

---

## 2. Gdzie i jak wypakować dane?

Pobrane dane zawsze będą w formie archiwów (`.zip` lub `.tar.gz`).
1. Rozpakuj pobrane paczki.
2. Zlokalizuj właściwe pliki sesji treningowych (najczęściej będą one pofragmentowane katalogami po różnych zawodnikach).
3. Skopiuj i wklej wszystkie pliki źródłowe do przygotowanego w tym projekcie folderu:
   👉 **`data/raw/`**
4. Struktura folderu po wklejeniu danych może (i powinna) wyglądać dowolnie, np:
   ```text
   data/raw/
   ├── kolarz_01/
   │   ├── aktywnosc_1.csv
   │   └── aktywnosc_2.csv
   ├── kolarz_02/
   │   └── aktywnosc_99.csv
   └── luzny_plik_treningu.fit
   ```
   *Nasz skrypt Pythona automatycznie przeszuka wszystkie podfoldery (rekursywnie).*

---

## 3. Obsługiwane formaty plików

Skrypt analityczny przygotowany w pliku `scripts/build_features_dataset.py` obsługuje formaty:
*   **`.csv`** (najbardziej pożądany i najszybszy w parsowaniu bez dodatkowych bibliotek)
*   **`.fit`** (wymaga wcześniejszej instalacji `pip install fitparse`)
*   **`.gpx`** (wymaga wcześniejszej instalacji `pip install gpxpy`)
*   **`.tcx`** (wymaga ewentualnie zewnętrznej implementacji readera)

Zaleca się na początek (do nauki modelu) wyszukać na Kaggle zbiór udostępniony od razu w formacie **CSV**, co pozwoli natychmiastowo skorzystać ze wsparcia biblioteki `pandas`.

---

## 4. Jak uruchomić pipeline przetwarzania?

Gdy upewnisz się, że pliki znajdują się w folderze `data/raw/`:

1. Otwórz wbudowany terminal (wiersz poleceń) w swoim edytorze kodu (np. VSCode).
2. Zainstaluj wymagane zależności (jeśli jeszcze ich nie masz):
   ```bash
   pip install pandas numpy
   ```
3. Uruchom dedykowany skrypt analityczny:
   ```bash
   python scripts/build_features_dataset.py
   ```
   *(Na systemach macOS może być wymagane użycie komendy `python3` zamiast `python`)*

---

## 5. Weryfikacja działania (Jak sprawdzić, czy wygenerował się zbiór)

Jeśli skrypt zadziała poprawnie:
1. Przejdź do folderu **`data/processed/`**.
2. Powinny znajdować się tam dwa nowo wygenerowane pliki:
   *   `dataset_report.txt` – czytelny plik tekstowy, w którym sprawdzisz ile plików udało się wczytać z `data/raw/`, ile miało błędy (np. brak czujnika mocy) oraz statystyki etykiety FTP.
   *   `features_ftp_dataset.csv` – to jest **GŁÓWNY WYNIKOWY ZBIÓR DANYCH**, ustrukturyzowana tabela zawierająca kolumny z cechami takimi jak `max_power`, `mean_heart_rate`, `mmp_20min`, `ftp_label` przygotowana prosto pod algorytmy ML.

Możesz kliknąć w plik `.csv` w swoim edytorze lub otworzyć go w programie Excel, aby wzrokowo zweryfikować ostateczną strukturę wejścia do algorytmu przed napisaniem kodu uczenia maszynowego.
