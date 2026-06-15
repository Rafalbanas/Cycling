# Raport formatowania i konfiguracji magazynu SSD

Data wykonania: 2026-05-30

## Sformatowany dysk

Bezpośrednio przed formatowaniem polecenia `diskutil list` oraz
`diskutil info /dev/disk4` potwierdziły następujące parametry:

| Element | Wartość |
|---|---|
| Formatowany dysk | `/dev/disk4` |
| Urządzenie | `RTL9210B` |
| Lokalizacja | zewnętrzny SSD podłączony przez USB |
| Pojemność fizyczna | 256,1 GB |
| Dotychczasowa główna partycja | `/dev/disk4s4`, `Linux Filesystem`, 249,7 GB |

Sformatowano wyłącznie zewnętrzny dysk `/dev/disk4`. Nie wykonywano operacji
na dysku systemowym `/dev/disk0`.

Wykonane polecenie:

```sh
diskutil eraseDisk APFS MasterThesisSSD GPT /dev/disk4
```

## Wynik formatowania

| Element | Wartość |
|---|---|
| Format | APFS |
| Schemat partycji | GUID Partition Map |
| Nazwa woluminu | `MasterThesisSSD` |
| Punkt montowania | `/Volumes/MasterThesisSSD` |
| Wolne miejsce bezpośrednio po formatowaniu | około 238 GiB |
| Wolne miejsce po kopiowaniu danych | około 229 GiB |

Formatowanie oraz automatyczne zamontowanie woluminu zakończyły się
powodzeniem.

## Struktura katalogów na SSD

Utworzono:

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/
  raw_zips/
  extracted/
  processed/
  cache/
  logs/
  current_local_copy/
    raw/
    processed/
```

Repozytorium źródłowe pozostało lokalnie:

```text
/Users/rafalbanas/Projects/Master_thesis
```

## Konfiguracja projektu

Konfigurację lokalnej ścieżki zapisano w ignorowanym przez Git pliku:

```text
config/local_paths.json
```

Wartość konfiguracji:

```text
MASTER_THESIS_DATA_ROOT=/Volumes/MasterThesisSSD/MasterThesisData
```

Dodano wspólny resolver `scripts/data_paths.py`. Skrypty
`scripts/download_goldencheetah_raw.py` oraz
`scripts/build_features_dataset.py` korzystają teraz kolejno z:

1. zmiennej środowiskowej `MASTER_THESIS_DATA_ROOT`,
2. pliku `config/local_paths.json`,
3. lokalnego fallbacku `data/`, jeżeli konfiguracja SSD nie jest dostępna.

Downloader zapisuje nowe archiwa w:

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/raw_zips
```

Generator cech domyślnie korzysta z:

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/extracted
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed
```

## Kopia istniejących danych

Wykonano kopie przez `rsync -avh --progress`. Nie usuwano lokalnych plików.

| Zbiór | Lokalizacja lokalna | Kopia na SSD | Rozmiar lokalny | Rozmiar kopii |
|---|---|---|---:|---:|
| Dane surowe | `data/raw` | `current_local_copy/raw` | 8,2 GiB | 8,2 GiB |
| Dane przetworzone | `data/processed` | `current_local_copy/processed` | 43 MiB | 43 MiB |

Porównanie liczby plików:

| Element | Lokalnie | Na SSD |
|---|---:|---:|
| Wszystkie pliki w `raw` | 46248 | 46248 |
| Pliki CSV w `raw` | 45974 | 45974 |
| Sesje treningowe CSV po wyłączeniu technicznego `manifest.csv` | 45973 | 45973 |
| Archiwa ZIP w `raw` | 136 | 136 |
| Wszystkie pliki w `processed` | 19 | 19 |

Kopiowanie zakończyło się sukcesem.

## Aktywny katalog ZIP

Istniejące 136 archiwów ZIP udostępniono także w aktywnym katalogu
`goldencheetah/raw_zips` jako dowiązania twarde do plików w kopii archiwalnej.
Dzięki temu downloader rozpoznaje je jako pobrane bez ponownego transferu i
bez zajmowania dodatkowych 1,9 GiB na SSD.

| Element | Wartość |
|---|---:|
| Archiwa ZIP w aktywnym `raw_zips` | 136 |
| Łączny rozmiar logiczny archiwów ZIP | 2068152170 B |

## Pobieranie danych OSF

Zgodnie z zakresem tego etapu nie rozpoczęto pobierania brakujących archiwów
GoldenCheetah. Nie rozpoczęto także pełnej ekstrakcji, treningu modeli ani
aktualizacji pracy LaTeX.

## Błędy

Nie wystąpiły błędy formatowania, montowania ani kopiowania danych.

## Rekomendowany następny krok

Przed rozpoczęciem transferu ponad 100 GiB archiwów należy wdrożyć i
zweryfikować przetwarzanie batchowe: pobieranie ZIP-ów do `raw_zips`,
tymczasową ekstrakcję partii do `extracted`, zapis cech pośrednich w
`processed` oraz usuwanie wyłącznie tymczasowych plików rozpakowanych po
udanym przetworzeniu. Archiwa ZIP powinny pozostać na SSD, dopóki autor nie
zatwierdzi ich usunięcia.
