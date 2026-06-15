# Stan startowy etapu batchowego

Data wykonania: 2026-05-30

## Konfiguracja SSD

| Element | Wartość |
|---|---|
| Wolumin SSD | `/Volumes/MasterThesisSSD` |
| Status montowania | zamontowany |
| Katalog danych | `/Volumes/MasterThesisSSD/MasterThesisData` |
| Konfiguracja lokalna | `config/local_paths.json` |
| `MASTER_THESIS_DATA_ROOT` | `/Volumes/MasterThesisSSD/MasterThesisData` |
| Wolne miejsce na SSD | około 227 GiB |

Resolver `scripts/data_paths.py` poprawnie zwraca katalogi na SSD.

## Stan danych GoldenCheetah

| Element | Wartość |
|---|---:|
| Archiwa ZIP w aktywnym `raw_zips` | 136 |
| Łączny rozmiar logiczny archiwów ZIP | około 1,9 GiB |
| Pliki w `extracted` | 0 |
| Pliki w `processed` | 0 |
| Pliki w `cache` | 0 |

## Wnioski przed wdrożeniem

Archiwa ZIP zawierają pliki CSV sesji treningowych oraz duże pliki JSON.
Do budowy tabelarycznego zbioru cech potrzebne są pliki CSV. Batch processor
powinien wyodrębniać wyłącznie CSV, aby ograniczyć tymczasowe wykorzystanie
miejsca. Tymczasowa ekstrakcja musi być usuwana dopiero po poprawnym zapisie
pliku cech partii. Archiwa ZIP pozostają zachowane.

