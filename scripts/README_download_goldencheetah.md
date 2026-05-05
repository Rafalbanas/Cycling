# Pobieranie Surowych Danych GoldenCheetah OpenData

Ten poradnik opisuje użycie skryptu `download_goldencheetah_raw.py`, który w bezpieczny sposób łączy się z chmurą AWS S3 i pobiera oryginalne, nieprzetworzone paczki z danymi od kolarzy (.zip). Dzięki temu zbudujesz zbiór danych bezpośrednio od źródłowego, 1-sekundowego próbkowania, zachowując zgodność z Twoją pracą dyplomową.

## 1. Instalacja zależności

Skrypt do komunikacji z publicznym wiadrem Amazon S3 wykorzystuje oficjalną bibliotekę `boto3`. Przed uruchomieniem zainstaluj ją w swoim środowisku Pythona:

```bash
pip install boto3
```

## 2. Pobieranie próbki danych (Bezpieczny test)

Ponieważ pełny zbiór GoldenCheetah OpenData zawiera pliki dla dziesiątek tysięcy zawodników i potrafi ważyć terabajty, **zawsze zaczynaj od pobrania małej próbki do testów**:

```bash
python scripts/download_goldencheetah_raw.py --limit 5
```
Powyższa komenda pobierze archiwa `.zip` tylko dla pierwszych 5 napotkanych w chmurze zawodników.

## 3. Pobieranie pełnego zbioru (Całość danych)

**UWAGA: Wymaga szybkiego internetu i dużej ilości miejsca na dysku!**
Jeśli przetestowałeś już kod i jesteś gotowy przetwarzać całą globalną bazę kolarzy na potrzeby finalnych eksperymentów do pracy:

```bash
python scripts/download_goldencheetah_raw.py --all
```

## 4. Wznowienie pobierania w przypadku przerwania

Skrypt jest w 100% odporny na przerwania połączenia internetowego lub wyłączenie komputera. Tworzy on manifest w tle (`manifest.csv`). 
Jeżeli przerwiesz skrypt w połowie (np. wciskając `Ctrl+C`), przy kolejnym uruchomieniu wystarczy odpalić go tą samą komendą. Skrypt:
1. Sprawdzi fizyczną obecność plików na dysku,
2. Przeczyta rejestr już pobranych plików,
3. Błyskawicznie **pominie istniejące pliki** i zacznie pobieranie od pierwszego brakującego zawodnika.

## 5. Gdzie znajdują się pobrane pliki?

Wszystkie paczki zostaną zapisane w lokalizacji:
👉 `data/raw/goldencheetah/`

Zarówno log konsoli z przebiegu (`download_log.txt`), jak i historia plików (`manifest.csv`) zapisywane są bezpośrednio w tym samym katalogu.

## 6. Integracja z potokiem danych (Kolejny krok)

Zauważ, że pobrane z AWS S3 pliki mają format skompresowanych archiwów `.zip`. Każdy ZIP to zwykle profil jednego kolarza zawierający jego pliki treningowe `.csv`.

Aby przejść do generowania tabeli cech (Machine Learning):
1. Ręcznie rozpakuj pobrane archiwa (np. narzędziem systemowym `unzip` lub 7-Zip). Najlepiej wypakować je do foldera `data/raw/`.
2. Uruchom przygotowany wcześniej mechanizm ETL:
   ```bash
   python scripts/build_features_dataset.py
   ```
Skrypt wygeneruje dla Ciebie `data/processed/features_ftp_dataset.csv`.
