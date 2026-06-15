# Raport testu batchowego przetwarzania GoldenCheetah

Data wykonania: 2026-05-30

## Cel testu

Przed rozpoczęciem pobierania brakujących archiwów sprawdzono działanie
batchowego wyodrębniania bogatych cech telemetrycznych na 5 istniejących
archiwach ZIP. Test nie jest finalnym eksperymentem uczenia maszynowego.

## Uruchomienie

```sh
venv/bin/python scripts/build_features_dataset_batch.py \
  --batch-size 5 \
  --max-zips 5 \
  --max-batches 1 \
  --workers 4
```

## Wynik

| Element | Wartość |
|---|---:|
| ZIP-y dostępne przed testem | 136 |
| ZIP-y przetworzone w teście | 5 |
| ZIP-y z błędami | 0 |
| Pliki CSV sesji odczytane z ZIP-ów | 7477 |
| Rekordy cech przed filtrem FTP | 4910 |
| Rekordy cech po filtrze `50 <= ftp_label <= 500` W | 4807 |
| Odrzucone etykiety FTP poza zakresem | 103 |
| Zawodnicy | 5 |
| Kolumny w pliku partii | 52 |
| Cechy wariantu B bez `mmp_20min` | 46 |
| Cechy wariantu C bez cech `mmp_*` | 41 |

Plik cech partii:

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/batches/features_batch_c3dcb8446cf3.csv
```

Manifest partii:

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/batches/features_batch_c3dcb8446cf3.json
```

## Kontrola miejsca

| Punkt pomiaru | Wolne miejsce |
|---|---:|
| Początek testu | 225,115 GiB |
| Przed ekstrakcją | 225,115 GiB |
| Po ekstrakcji CSV | 223,740 GiB |
| Po zapisie cech | 223,736 GiB |
| Po usunięciu cache | 224,616 GiB |

Próg bezpiecznego zatrzymania wynosi 35 GiB. Nie został osiągnięty.

## Kontrola cache i archiwów

| Element | Wynik |
|---|---|
| Tymczasowe katalogi ekstrakcji po sukcesie | brak |
| Pliki w `goldencheetah/cache` po sukcesie | 0 |
| ZIP-y po teście | 136, bez usuwania |
| Wartości nieskończone w danych numerycznych | 0 |
| Ścieżki tymczasowego cache zapisane w `source_path` | 0 |

Batch processor wyodrębnia wyłącznie potrzebne pliki CSV. Duże pliki JSON
zawarte w archiwach nie są rozpakowywane.

## Kontrola wznawiania

Wykonano dodatkowe uruchomienie bez nowych ZIP-ów:

```sh
venv/bin/python scripts/build_features_dataset_batch.py \
  --max-zips 0 \
  --max-batches 0 \
  --workers 4
```

Skrypt poprawnie odczytał zapisany stan: 5 ZIP-ów wcześniej przetworzonych,
0 ZIP-ów oczekujących w tym uruchomieniu. Nie uruchomiono ponownej ekstrakcji.

Stan wznawiania:

```text
/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/batches/batch_state.json
```

## Wniosek

Test batch processingu zakończył się sukcesem. Można przejść do osobno
zatwierdzonego, kontrolowanego pobierania archiwów i przetwarzania kolejnych
partii. Na tym etapie nie pobierano nowych ZIP-ów, nie trenowano modeli i nie
aktualizowano pracy LaTeX.

