# Próba kontrolna na rozszerzonym zbiorze GoldenCheetah OpenData

Data wykonania: 2026-06-03 06:41:36

## 1. Cel

Eksperyment jest dodatkową próbą skalowalności. Nie zastępuje eksperymentu bazowego
i nie podmienia tabel, wykresów ani plików wynikowych używanych w głównym PDF.

## 2. Konfiguracja i SSD

| Element | Wartość |
|---|---|
| Ścieżka danych SSD | `/Volumes/MasterThesisSSD/MasterThesisData` |
| Wolne miejsce przed przebiegiem analitycznym | 124.657 GiB |
| Lokalne archiwa ZIP wybrane do kontroli | 5000 |
| Rozmiar lokalnych ZIP | 81.701 GiB |
| Cache | `/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/cache` |
| Logi | `/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/logs` |
| Duże wyniki pośrednie | `/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/control_5000/outputs` |
| Małe wyniki końcowe | `/Users/rafalbanas/Projects/Master_thesis/experiments/control_5000/results` |

Metodologia pozostała zgodna z baseline: `ftp_label = 0.95 * mmp_20min`,
filtr FTP `50--500 W`, warianty A/B/C, `GroupShuffleSplit(test_size=0.2,
random_state=42)`, Ridge, Random Forest i XGBoost oraz te same ustawienia modeli.

## 3. Statystyki danych

| Element | Wartość |
|---|---:|
| Archiwa przed przetwarzaniem | 5000 |
| Archiwa z manifestem przetwarzania | 5000 |
| Zawodnicy odrzuceni po filtracji | 355 |
| Sesje wejściowe CSV | 1906188 |
| Sesje zaakceptowane przed filtrem FTP | 985263 |
| Sesje po filtrze FTP | 979672 |
| Zawodnicy po filtrze FTP | 4645 |
| Sesje z mocą | 979672 |
| Sesje z tętnem | 840946 |
| Sesje z cechami MMP | 979672 |
| Sesje/zawodnik: minimum | 1 |
| Sesje/zawodnik: średnia | 210.909 |
| Sesje/zawodnik: mediana | 94.000 |
| Sesje/zawodnik: maksimum | 4722 |
| FTP minimum | 50.012 W |
| FTP średnia | 195.857 W |
| FTP mediana | 195.485 W |
| FTP maksimum | 499.132 W |

### Przyczyny pominięcia sesji

| Przyczyna | Liczba |
|---|---:|
| Brak danych o mocy (power) | 631214 |
| Zbyt krótka sesja (< 30 min) | 282697 |
| Nie można obliczyć FTP (brak pełnego okna MMP20) | 7014 |

Szczegółowe statystyki, braki danych i odrzucenia zapisano w katalogu
`experiments/control_5000/results/`.

## 4. Wyniki modeli

| Variant | Model | MAE | RMSE | R2 | MedAE | Train_Athletes | Test_Athletes | Train_Sessions | Test_Sessions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Variant_A | Ridge | 0.0002 | 0.0003 | 1.0000 | 0.0002 | 3716 | 929 | 762054 | 217618 |
| Variant_A | RandomForest | 0.0005 | 0.0088 | 1.0000 | 0.0001 | 3716 | 929 | 762054 | 217618 |
| Variant_A | XGBoost | 0.3175 | 1.0831 | 0.9995 | 0.1755 | 3716 | 929 | 762054 | 217618 |
| Variant_B | Ridge | 7.1818 | 10.3026 | 0.9579 | 4.8463 | 3716 | 929 | 762054 | 217618 |
| Variant_B | RandomForest | 6.0076 | 8.9972 | 0.9679 | 3.8538 | 3716 | 929 | 762054 | 217618 |
| Variant_B | XGBoost | 6.4017 | 9.2994 | 0.9657 | 4.3254 | 3716 | 929 | 762054 | 217618 |
| Variant_C | Ridge | 12.4636 | 17.5614 | 0.8778 | 9.0925 | 3716 | 929 | 762054 | 217618 |
| Variant_C | RandomForest | 9.1785 | 13.7538 | 0.9251 | 5.9514 | 3716 | 929 | 762054 | 217618 |
| Variant_C | XGBoost | 9.8635 | 14.1170 | 0.9210 | 6.8633 | 3716 | 929 | 762054 | 217618 |

## 5. Porównanie z baseline

| Variant | Model | MAE_Baseline | MAE_Control | MAE_Difference | RMSE_Baseline | RMSE_Control | R2_Baseline | R2_Control | MedAE_Baseline | MedAE_Control |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Variant_A | Ridge | 0.0016 | 0.0002 | -0.0014 | 0.0024 | 0.0003 | 1.0000 | 1.0000 | 0.0011 | 0.0002 |
| Variant_A | RandomForest | 0.0026 | 0.0005 | -0.0021 | 0.0238 | 0.0088 | 1.0000 | 1.0000 | 0.0011 | 0.0001 |
| Variant_A | XGBoost | 0.3058 | 0.3175 | 0.0117 | 0.8671 | 1.0831 | 0.9997 | 0.9995 | 0.1810 | 0.1755 |
| Variant_B | Ridge | 7.0560 | 7.1818 | 0.1259 | 10.3271 | 10.3026 | 0.9579 | 0.9579 | 4.6443 | 4.8463 |
| Variant_B | RandomForest | 6.6193 | 6.0076 | -0.6117 | 9.8129 | 8.9972 | 0.9619 | 0.9679 | 4.3761 | 3.8538 |
| Variant_B | XGBoost | 6.5457 | 6.4017 | -0.1439 | 9.6801 | 9.2994 | 0.9630 | 0.9657 | 4.3289 | 4.3254 |
| Variant_C | Ridge | 12.7912 | 12.4636 | -0.3277 | 17.5975 | 17.5614 | 0.8776 | 0.8778 | 9.7920 | 9.0925 |
| Variant_C | RandomForest | 10.3591 | 9.1785 | -1.1806 | 14.8032 | 13.7538 | 0.9134 | 0.9251 | 7.4221 | 5.9514 |
| Variant_C | XGBoost | 10.2891 | 9.8635 | -0.4255 | 14.4925 | 14.1170 | 0.9170 | 0.9210 | 7.3426 | 6.8633 |

## 6. Interpretacja

- Wariant A nadal pokazuje oczekiwany leakage.
- Najlepszy wariant B: `RandomForest`, MAE `6.008 W`, R² `0.9679`.
- Najlepszy wariant C: `RandomForest`, MAE `9.179 W`, R² `0.9251`.
- Wariant B zachowuje przewagę nad wariantem C według MAE.

## 7. Ryzyka

- Etykieta nadal jest heurystyczna i zależy od `mmp_20min`.
- Wynik kontrolny nie powinien zastępować bazowego eksperymentu na przefiltrowanym zbiorze.
- Archiwa bez użytecznych sesji i błędne pliki są rejestrowane, a nie ukrywane.

## 8. Rekomendacja

Traktować przebieg jako dodatkową kontrolę skalowalności. Nie aktualizować automatycznie
głównych rozdziałów ani finalnego PDF. Ewentualne dodanie krótkiego podrozdziału
powinno nastąpić dopiero po ręcznej akceptacji wyników.

## 9. Propozycja krótkiego podrozdziału

### Dodatkowa ocena skalowalności pipeline'u

W celu uzupełniającej oceny skalowalności przeprowadzono próbę kontrolną na
rozszerzonym zbiorze GoldenCheetah OpenData. Zachowano definicję etykiety,
filtrację, warianty cech, podział osobniczy oraz konfigurację modeli z eksperymentu
bazowego. Próba ma charakter technicznej kontroli stabilności pipeline'u i nie
zastępuje wyników głównego eksperymentu.
