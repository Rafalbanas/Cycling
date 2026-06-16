# Raport konfiguracji magazynu SSD dla danych GoldenCheetah

Data wykonania: 2026-05-30

## Status

Konfiguracja została zatrzymana po etapie wykrywania dysku. Zewnętrzny SSD jest
widoczny sprzętowo, ale jego główna partycja nie jest montowana przez macOS.
Nie wykonywano formatowania, kopiowania, pobierania ani usuwania danych.

## Wykryty dysk SSD

| Element | Wartość |
|---|---|
| Urządzenie | `RTL9210B` |
| Identyfikator całego dysku | `/dev/disk4` |
| Typ urządzenia | zewnętrzny SSD podłączony przez USB |
| Całkowita pojemność fizyczna | 256,1 GB |
| Główna partycja danych | `/dev/disk4s4` |
| Pojemność głównej partycji | 249,7 GB |
| Typ partycji | `Linux Filesystem` |
| System plików rozpoznany przez macOS | brak |
| Punkt montowania | brak |
| Wolne miejsce | nie można ustalić bez zamontowania systemu plików |

Polecenia `ls /Volumes`, `df -h`, `diskutil list` oraz
`diskutil info /dev/disk4s4` potwierdziły, że SSD nie jest zamontowany.
W katalogu `/Volumes` znajduje się wyłącznie wolumin systemowy
`Macintosh HD`.

## Ocena zgodności

Partycja nie ma formatu exFAT, APFS ani Mac OS Extended. macOS nie udostępnia
jej jako zapisywalnego woluminu, dlatego nie można utworzyć wymaganej
struktury:

```text
/Volumes/<NAZWA_DYSKU>/MasterThesisData/goldencheetah/
  raw_zips/
  extracted/
  processed/
  cache/
  logs/
```

Nie można również potwierdzić wymaganego progu co najmniej 180 GB wolnego
miejsca.

## Lokalne dane oczekujące na bezpieczną kopię

| Katalog | Rozmiar |
|---|---:|
| `data/raw` | 8,2 GiB |
| `data/processed` | 43 MiB |
| `data/final` | brak |
| `data/cache` | brak |

Zgodnie z wymaganiami nie usuwano ani nie przenoszono lokalnych danych.

## Stan realizacji etapów

| Etap | Status |
|---|---|
| Wykrycie fizycznego SSD | wykonano |
| Kontrola wolnego miejsca | zablokowana: partycja nie jest montowana |
| Utworzenie katalogów na SSD | niewykonane |
| Konfiguracja `MASTER_THESIS_DATA_ROOT` | niewykonana |
| Modyfikacja pipeline'u do pracy batchowej na SSD | niewykonana |
| Kopiowanie obecnych danych | niewykonane |
| Pobieranie brakujących archiwów OSF | niewykonane |
| Budowa pełniejszego bogatego datasetu | niewykonana |
| Trening modeli i aktualizacja LaTeX | celowo niewykonane |

## Wymagana decyzja autora

Do ręcznej weryfikacji: należy sprawdzić, czy na partycji linuksowej znajdują
się dane, które trzeba zachować. Jeżeli SSD może zostać wyczyszczony, należy
jawnie zatwierdzić jego ponowne sformatowanie. Dla pracy wyłącznie w macOS
zalecany jest APFS. Jeżeli dysk ma być używany również w innych systemach,
można wybrać exFAT.

Po zamontowaniu zapisywalnego woluminu należy ponownie uruchomić etap 1,
potwierdzić co najmniej 180 GB wolnego miejsca i dopiero wtedy kontynuować
konfigurację magazynu danych.

