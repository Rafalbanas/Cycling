# Podsumowanie wdrożenia batchowego pobierania i budowy cech

Data wykonania: 2026-05-30

## Status bieżącego etapu

Zrealizowano etapy 1--4: sprawdzenie SSD, wdrożenie batch processora,
rozbudowę downloadera oraz test na małej próbce. Zgodnie z poleceniem prace
zatrzymano przed pobieraniem brakujących ponad 100 GiB archiwów.

| Element | Wartość |
|---|---|
| Batch processing wdrożony | tak |
| Test batch processingu | zakończony sukcesem |
| Nowe ZIP-y pobrane w tym etapie | 0 |
| ZIP-y dostępne lokalnie na SSD | 136 |
| ZIP-y przetworzone batchowo | 5 |
| ZIP-y z błędami batch processingu | 0 |
| Rekordy testowej partii przed filtrem FTP | 4910 |
| Rekordy testowej partii po filtrze FTP | 4807 |
| Zawodnicy w testowej partii | 5 |
| Cechy wariantu B bez `mmp_20min` | 46 |
| Cechy wariantu C bez cech `mmp_*` | 41 |
| Wolne miejsce na SSD po teście i kontroli końcowej | około 223 GiB |
| Próg bezpiecznego zatrzymania | 35 GiB |

Wartości dotyczą partii testowej, a nie finalnego datasetu do eksperymentów.

## Wdrożone skrypty

Dodano:

```text
scripts/build_features_dataset_batch.py
```

Skrypt:

- czyta ZIP-y z katalogu SSD `goldencheetah/raw_zips`,
- wyodrębnia wyłącznie CSV aktualnej partii,
- zapisuje cechy w `goldencheetah/processed/batches`,
- zapisuje manifest partii i stan wznawiania,
- rejestruje błędy ZIP-ów,
- usuwa wyłącznie tymczasowy cache po udanym zapisie cech,
- nie usuwa ZIP-ów,
- kontroluje wolne miejsce przed ekstrakcją, po ekstrakcji, po zapisie oraz po
  usunięciu cache,
- zatrzymuje się bezpiecznie poniżej 35 GiB wolnego miejsca.

Rozbudowano:

```text
scripts/download_goldencheetah_raw.py
```

Downloader:

- pomija istniejące ZIP-y,
- zapisuje nowe archiwa przez tymczasowe pliki `.part`,
- pobiera kontrolowane partie, domyślnie po 100 ZIP-ów,
- domyślnie wykonuje jedną partię na uruchomienie,
- kontroluje próg 35 GiB przed pobraniem kolejnego archiwum,
- zapisuje log SSD i raport Markdown.

Downloader został zweryfikowany składniowo i przez interfejs CLI. Nie
uruchamiano transferu sieciowego w tym etapie.

## Najważniejsze ścieżki

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/raw_zips
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/cache
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/batches
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/logs/batch_features.log
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/logs/batch_storage_monitor.csv
```

## Gotowość do treningu

Nie należy jeszcze trenować modeli. Najpierw trzeba osobno zatwierdzić
kontrolowane pobieranie brakujących ZIP-ów, przetworzyć dostępne partie i
scalić pliki `features_batch_*.csv` do pełniejszego datasetu.

## Komendy następnego etapu

Po zatwierdzeniu pobierania zalecany jest cykl po jednej partii:

```sh
venv/bin/python scripts/download_goldencheetah_raw.py \
  --batch-size 100 \
  --max-batches 1

venv/bin/python scripts/build_features_dataset_batch.py \
  --batch-size 20 \
  --workers 4
```

Po kilku cyklach należy sprawdzić:

```sh
df -h /Volumes/MasterThesisSSD
```

Następnie trzeba wdrożyć scalanie partii, filtr FTP i raporty pełnego zbioru
przed treningiem modeli.
