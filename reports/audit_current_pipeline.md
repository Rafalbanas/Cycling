# Audyt bieżącego pipeline'u

Data audytu: 2026-05-30

## Zakres repozytorium

Aktywny pipeline składa się z następujących elementów:

| Obszar | Plik | Rola |
|---|---|---|
| Pobieranie danych | `scripts/download_goldencheetah_raw.py` | Pobieranie archiwów ZIP z publicznego API Open Science Framework (`https://api.osf.io/v2/nodes/6hfpz/files/osfstorage/`) |
| Rozpakowywanie danych | `run_thesis_pipeline.sh` | Rozpakowywanie archiwów do katalogów zawodników w `data/raw/<athlete_id>/` |
| Budowa cech | `scripts/build_features_dataset.py` | Wczytanie sesji CSV, podstawowe czyszczenie, wyznaczenie etykiety FTP i zapis `data/processed/features_ftp_dataset.csv` |
| Trening bazowy | `scripts/train_models.py` | Starszy wariant treningu modeli |
| Porównanie A/B | `scripts/train_models_ab.py` | Porównanie wariantu kontrolnego z wyciekiem danych oraz wariantu bez `mmp_20min` |
| Aktualizacja starszych plików LaTeX | `scripts/update_latex_results.py` | Skrypt pomocniczy odnoszący się do wcześniejszych plików `chapter*.tex`; nie jest źródłem aktualnych rozdziałów pracy |

## Dane lokalne

| Element | Wartość |
|---|---:|
| Archiwa ZIP w `data/raw/goldencheetah/` | 136 |
| Rozmiar archiwów ZIP | 2 068 152 170 bajtów |
| Katalogi zawodników po rozpakowaniu | 136 |
| Pliki treningowe CSV | 45 973 |
| Katalogi zawodników zawierające pliki CSV | 134 |
| Schemat sesji treningowej | `secs, km, power, hr, cad, alt` |

W katalogu `data/raw/goldencheetah/` znajduje się również plik techniczny `manifest.csv`, który nie jest sesją treningową. Obecny generator cech przeszukuje rekurencyjnie cały katalog `data/raw`, przez co próbuje przetworzyć także manifest.

## Bieżący końcowy CSV

Plik `data/processed/features_ftp_dataset.csv` zawiera:

| Element | Wartość |
|---|---:|
| Liczba rekordów | 25 738 |
| Liczba zawodników | 126 |
| Kolumny | `duration_sec`, `mean_power`, `mmp_20min`, `ftp_label`, `file_name`, `athlete_id` |
| Zmienna celu | `ftp_label = 0.95 * mmp_20min` |
| Wariant A | `duration_sec`, `mean_power`, `mmp_20min` |
| Wariant B | `duration_sec`, `mean_power` |

## Audyt etykiety FTP przed przebudową pipeline'u

| Statystyka | Wartość |
|---|---:|
| Minimum FTP | 0.125 W |
| Maksimum FTP | 675.911 W |
| Średnia FTP | 185.726 W |
| Mediana FTP | 184.698 W |
| Rekordy z FTP < 50 W | 152 |
| Rekordy z FTP > 500 W | 4 |
| Rekordy poza zakresem 50--500 W | 156 |

Wartości skrajne wymagają jawnego filtrowania jakościowego przed ponownym treningiem modeli.

## Najważniejsze wnioski

1. Surowe dane zawierają sygnały mocy, tętna, kadencji, dystansu i wysokości, ale bieżący końcowy CSV wykorzystuje jedynie czas trwania, średnią moc i MMP20.
2. Wariant B jest zbyt ubogi względem możliwości danych źródłowych.
3. Rozbudowa cech jest możliwa bez wymiany formatu danych wejściowych.
4. Nowy pipeline powinien zachować wariant kontrolny A z `mmp_20min`, przygotować bogatszy wariant B bez tej cechy oraz wariant C bez cech MMP z krótszych okien.
5. Reguła jakościowa dla etykiety FTP powinna być jawna i raportowana.

