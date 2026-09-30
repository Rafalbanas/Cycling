# Cycling — estymacja FTP z telemetrii kolarskiej

Projekt magisterski obejmujący powtarzalny pipeline ETL i eksperymenty regresyjne służące do estymacji **operacyjnej etykiety FTP** na podstawie anonimowych danych treningowych GoldenCheetah OpenData. Repozytorium zawiera kod przygotowania danych, eksperymenty Ridge/Random Forest/XGBoost, analizę SHAP, rozdziały pracy oraz aplikację internetową prezentującą zweryfikowane wyniki.

> Etykieta `ftp_label = 0,95 × mmp_20min` jest heurystyką badawczą. Nie jest laboratoryjnym pomiarem progu fizjologicznego ani automatyczną rekomendacją treningową.

## Aplikacja internetowa

Publiczny adres: [https://cycling.banas.dev](https://cycling.banas.dev)

Funkcje:

- responsywna prezentacja zbioru i metodologii;
- pełny interfejs w języku polskim i angielskim z zapamiętywaniem wyboru;
- porównanie rzeczywistych wyników wariantów B i C oraz modeli regresyjnych;
- widok porównawczy B/C, wybór metryki oraz dostępne z klawiatury podpowiedzi wykresów;
- zanonimizowany wykres wartości testowych rzeczywistych i estymowanych;
- analiza MAE według zakresu FTP i znaczenia cech SHAP;
- kalkulator operacyjnej etykiety FTP z wyniku próby 20-minutowej;
- aktualizowany na żywo kalkulator połączony z suwakiem i polem liczbowym;
- osadzony podgląd aktualnej polskiej wersji pracy magisterskiej, tryb pełnoekranowy i pobieranie PDF;
- jawna informacja o ograniczeniach, wycieku danych w wariancie A i braku zapisanego artefaktu modelu do inferencji;
- endpointy diagnostyczne i API, które nie ujawniają identyfikatorów zawodników ani surowych danych.

## Najważniejsze wyniki

Główny zbiór obejmuje 151 399 sesji 726 zawodników przygotowanych z 781 archiwów. Zastosowano osobniczy podział 80/20 (`GroupShuffleSplit`, `random_state=42`).

| Wariant | Najlepszy model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| B — bez `mmp_20min` | XGBoost | 6,55 W | 9,68 W | 0,9630 |
| C — bez wszystkich cech `mmp_*` | XGBoost | 10,29 W | 14,49 W | 0,9170 |

Wariant A zawiera `mmp_20min`, z którego bezpośrednio obliczono etykietę, dlatego służy wyłącznie jako kontrola data leakage.

## Technologie

- Python 3.12 i biblioteka standardowa — lekki serwer aplikacji bez zależności produkcyjnych;
- HTML5, CSS i JavaScript bez zewnętrznych CDN;
- Nginx jako reverse proxy i terminacja HTTPS;
- systemd: autostart, restart po awarii i logi w journald;
- pipeline badawczy: pandas, NumPy, scikit-learn, XGBoost, Matplotlib, Seaborn i SHAP (zależności części analitycznej opisuje `dist/zalacznik_elektroniczny/requirements.txt`).

## Uruchamianie lokalne

Aplikacja nie wymaga instalowania pakietów:

```bash
python3 webapp/server.py
```

Domyślnie nasłuchuje na `http://127.0.0.1:20144`. Konfigurację można zmienić zmiennymi `CYCLING_HOST` i `CYCLING_PORT`.

Testy:

```bash
python3 -m unittest discover -s webapp/tests -v
```

Przygotowanie zbioru i eksperymenty opisuje [INSTRUKCJA_DANE.md](INSTRUKCJA_DANE.md). Duże dane źródłowe są ignorowane przez Git i nie są serwowane przez aplikację.

## API

| Metoda i ścieżka | Opis |
|---|---|
| `GET /healthz` | stan usługi |
| `GET /api/summary` | zagregowane metryki, dane SHAP i kontrola skali |
| `GET /api/predictions?variant=Variant_B&limit=120` | zanonimizowana próbka punktów testowych B lub C |
| `POST /api/estimate` | etykieta `0,95 × MMP20`; JSON: `{"mmp20": 286, "weight": 74}` |
| `GET /thesis/INF.MN-152863-6350.pdf` | najnowsza praca magisterska; parametr `download=1` wymusza pobranie |

API obsługuje polskie i angielskie komunikaty na podstawie `Accept-Language` lub pola `lang` w żądaniu kalkulatora. PDF jest dostępny wyłącznie w języku polskim; angielski interfejs nie sugeruje istnienia osobnego angielskiego dokumentu.

## Wdrożenie

Pliki referencyjne znajdują się w `deployment/`:

- `cycling-web.service` — usługa systemd na `127.0.0.1:20144`, `Restart=on-failure`;
- `nginx-cycling.conf` — osobny virtual host `cycling.banas.dev`, przekierowanie HTTP→HTTPS i nagłówki bezpieczeństwa.

Usługa działa jako dedykowany, nieuprzywilejowany użytkownik `cycling-web`. Skrypt kopiuje do `/opt/cycling-web` wyłącznie aplikację i wymagane zagregowane wyniki (bez danych surowych i reszty repozytorium), instaluje konfigurację i bezpiecznie przeładowuje Nginx:

```bash
sudo ./deployment/install.sh
```

Po kolejnej aktualizacji kodu:

```bash
git pull --ff-only origin cycling-web
python3 -m unittest discover -s webapp/tests -v
sudo ./deployment/install.sh
curl --fail http://127.0.0.1:20144/healthz
```

Logi:

```bash
journalctl -u cycling-web.service -f
tail -f /var/log/nginx/cycling.access.log /var/log/nginx/cycling.error.log
```

## Prywatność i bezpieczeństwo

Aplikacja korzysta z jawnej listy dozwolonych plików statycznych i dedykowanych endpointów. Nie udostępnia katalogu repozytorium, źródłowych archiwów treningowych, identyfikatorów zawodników, konfiguracji lokalnej ani sekretów. API predykcji usuwa `athlete_id` i zwraca wyłącznie pary wartości rzeczywista/estymowana.
