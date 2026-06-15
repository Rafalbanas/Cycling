# Podsumowanie etapów 1--4

Data wykonania: 2026-05-30

## Zakres wykonanych prac

Przeprowadzono audyt istniejącego pipeline'u, zweryfikowano publiczne źródło
GoldenCheetah OpenData w OSF, rozbudowano generator cech i zbudowano bogatszy
zbiór danych na największym bezpiecznie dostępnym lokalnie fragmencie danych.
Nie uruchamiano nowych eksperymentów uczenia maszynowego i nie aktualizowano
pracy LaTeX nowymi wynikami.

## Stan danych wejściowych

| Element | Wartość |
|---|---:|
| Lokalne archiwa ZIP GoldenCheetah | 136 |
| Rozpakowane pliki CSV sesji treningowych | 45973 |
| Katalogi zawodników zawierające sesje CSV | 134 |
| Archiwa ZIP dostępne publicznie w OSF | 6581 |
| Łączny rozmiar archiwów ZIP dostępnych w OSF | około 106,9 GiB |
| Archiwa ZIP brakujące lokalnie | 6445 |
| Łączny rozmiar brakujących lokalnie archiwów ZIP | około 105,0 GiB |

Pełniejsze pobranie zostało wstrzymane z powodu niewystarczającego i
zmiennego zapasu wolnego miejsca na woluminie. Szczegóły zapisano w
`reports/download_full_dataset_log.md`.

## Bogaty zbiór cech

Generator `scripts/build_features_dataset.py` zapisuje nowe artefakty osobno,
bez nadpisywania wcześniejszego pliku `data/processed/features_ftp_dataset.csv`.

| Element | Wartość |
|---|---:|
| Rekordy przed filtrowaniem FTP | 26123 |
| Rekordy po filtrowaniu FTP | 25945 |
| Zawodnicy po filtrowaniu FTP | 126 |
| Kolumny wynikowe łącznie | 51 |
| Cechy wariantu A, wraz z `mmp_20min` | 47 |
| Cechy wariantu B, bez `mmp_20min` | 46 |
| Cechy opcjonalnego wariantu C, bez cech `mmp_*` | 41 |

Wariant B obejmuje cechy czasu i objętości, mocy, krótkich okien maksymalnej
mocy, tętna, kadencji, jakości danych, histogramów intensywności i
odsprzężenia tętna. Nie zawiera `mmp_20min`, ponieważ ta cecha bezpośrednio
wyznacza etykietę `ftp_label`.

## Dostępność wybranych grup cech

| Cecha | Rekordy niepuste | Udział |
|---|---:|---:|
| `distance_km` | 25945 | 100,00% |
| `elevation_gain_m` | 24258 | 93,50% |
| `mean_hr` | 22662 | 87,35% |
| `power_hr_decoupling_pct` | 22591 | 87,07% |
| `mean_cadence` | 25494 | 98,26% |

Walidacja nie wykryła zduplikowanych ścieżek źródłowych, nieskończonych
wartości numerycznych ani etykiet FTP poza zakresem przyjętym dla zbioru
eksperymentalnego.

## Filtr jakościowy FTP

Przyjęto jawną regułę jakościową: `50 <= ftp_label <= 500` W.

| Element | Wartość |
|---|---:|
| Odrzucone rekordy łącznie | 178 |
| Rekordy z `ftp_label < 50` W | 174 |
| Rekordy z `ftp_label > 500` W | 4 |

Pełne statystyki przed i po filtracji zapisano w
`reports/ftp_outlier_audit.md`.

## Decyzja o zatrzymaniu

Zgodnie z warunkiem zadania prace zatrzymano po etapach 1--4. Pełny zbiór OSF
nie został pobrany z powodu ograniczenia miejsca na dysku. Kolejne kroki
powinny rozpocząć się od decyzji autora: zwolnienia miejsca, wskazania
zewnętrznego woluminu albo świadomej akceptacji eksperymentu na obecnym
lokalnym fragmencie danych.
