# Cycling — interaktywna prezentacja wyników estymacji FTP

Lekka, dwujęzyczna aplikacja internetowa prezentująca zweryfikowane wyniki pracy magisterskiej dotyczącej estymacji **operacyjnej etykiety FTP** z anonimowej telemetrii kolarskiej GoldenCheetah OpenData.

Wersja demonstracyjna: [https://cycling.banas.dev](https://cycling.banas.dev)

> `ftp_label = 0,95 × MMP20` jest heurystyką badawczą. Nie stanowi laboratoryjnego pomiaru progu fizjologicznego, predykcji zapisanego modelu ML ani rekomendacji treningowej.

## Funkcje

- pełny interfejs PL/EN z zapamiętywaniem wyboru;
- responsywny i dostępny z klawiatury interfejs;
- porównanie rzeczywistych wyników wariantów B i C;
- wybór MAE, RMSE, R² i MedAE oraz interaktywne wykresy;
- wykres zanonimizowanych par wartości rzeczywistych i estymowanych;
- interpretacja SHAP i objaśnienia metodologii;
- kalkulator heurystyczny `0,95 × MMP20`, wyraźnie oddzielony od ML;
- czytnik pracy oparty na ładowanych na żądanie obrazach stron, z paginacją, zoomem, pełnym ekranem i widocznym znakiem wodnym.

Czytnik nie publikuje oryginalnego PDF. Ogranicza wygodne pobieranie całego dokumentu, ale nie jest zabezpieczeniem DRM i nie uniemożliwia kopiowania treści wyświetlanych w przeglądarce.

## Zweryfikowane wyniki

Główny zbiór obejmował 151 399 sesji 726 zawodników przygotowanych z 781 archiwów. Podział testowy wykonano po zawodnikach (`GroupShuffleSplit`, 80/20), a nie po sesjach.

| Wariant | Najlepszy model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| B — bez `mmp_20min` | XGBoost | 6,55 W | 9,68 W | 0,9630 |
| C — bez wszystkich cech `mmp_*` | XGBoost | 10,29 W | 14,49 W | 0,9170 |

Wariant A zawierał `mmp_20min`, z którego obliczono etykietę, dlatego jest traktowany wyłącznie jako kontrola wycieku danych.

## Zawartość publicznego projektu

Repozytorium aplikacji powinno zawierać wyłącznie:

- `webapp/` — serwer, interfejs i testy;
- `results/` — wymagane zagregowane metryki, SHAP oraz pary `y_true`/`y_pred` bez identyfikatorów;
- `experiments/control_5000/results/` — dwie zagregowane kontrole skali;
- `deployment/` — przykładowe konfiguracje systemd/Nginx i skrypty wdrożenia;
- `.gitignore`, `requirements.txt` i ten README.

Nie są publikowane: PDF/DOCX pracy, źródła LaTeX, dane surowe, identyfikatory zawodników, notebooki, materiały robocze, pliki kompilacji ani obrazy stron czytnika.

## Technologie i zależności

- Python 3.12, wyłącznie biblioteka standardowa w środowisku produkcyjnym;
- HTML5, CSS i JavaScript bez zewnętrznych CDN;
- Nginx oraz systemd;
- `poppler-utils` (`pdftoppm`) tylko do przygotowania prywatnych zasobów czytnika.

Plik `requirements.txt` dokumentuje brak zewnętrznych pakietów Python wymaganych przez aplikację.

## Uruchamianie lokalne

```bash
python3 webapp/server.py
```

Domyślny adres to `http://127.0.0.1:20144`. Dostępne zmienne:

- `CYCLING_HOST`;
- `CYCLING_PORT`;
- `CYCLING_THESIS_PAGES` — katalog z `page-*.jpg` poza repozytorium.

Testy:

```bash
python3 -m unittest discover -s webapp/tests -v
```

Testy tworzą tymczasowe obrazy stron, więc nie wymagają prywatnego dokumentu.

## Przygotowanie zasobów czytnika

Oryginalny PDF należy przechowywać poza repozytorium i katalogiem `/opt/cycling-web`, np. z prawami `0600` w `/var/lib/cycling-private/`. Obrazy stron również pozostają poza Git:

```bash
sudo ./deployment/prepare-thesis-pages.sh \
  /var/lib/cycling-private/master-thesis-pl.pdf \
  /var/lib/cycling-web/thesis-pages
```

Skrypt wymaga `pdftoppm`, generuje progresywne pliki JPEG o szerokości 1500 px i ustawia prawa odczytu dla użytkownika usługi. Znak wodny jest nakładany przez interfejs czytnika. Po zmianie dokumentu należy ponownie przygotować zasoby i zrestartować usługę.

## API

| Metoda i ścieżka | Opis |
|---|---|
| `GET /healthz` | stan usługi |
| `GET /api/summary` | zagregowane metryki, SHAP i kontrola skali |
| `GET /api/predictions?variant=Variant_B&limit=120` | zanonimizowane pary rzeczywista/estymowana |
| `POST /api/estimate` | kalkulator `0,95 × MMP20` |
| `GET /api/thesis/manifest` | krótkotrwała konfiguracja czytnika stron |

Bezpośrednie ścieżki zakończone `.pdf`, w tym wcześniejsze adresy pracy, zwracają `410 Gone`. Obrazy czytnika wymagają tokenu tworzonego na starcie procesu i otrzymują `Cache-Control: private, no-store`. Jest to ograniczenie wygodnego pobierania, nie mechanizm autoryzacji.

## Wdrożenie i aktualizacja

Przed pierwszym wdrożeniem przygotuj zasoby czytnika. Następnie:

```bash
python3 -m unittest discover -s webapp/tests -v
sudo ./deployment/install.sh
curl --fail http://127.0.0.1:20144/healthz
```

Skrypt kopiuje do `/opt/cycling-web` tylko pliki aplikacji i wymagane zanonimizowane wyniki. Nie kopiuje PDF ani całego repozytorium. Usługa działa jako `cycling-web`, uruchamia się po restarcie i ma `Restart=on-failure`.

Logi:

```bash
journalctl -u cycling-web.service -f
tail -f /var/log/nginx/cycling.access.log /var/log/nginx/cycling.error.log
```

## Automatyczne wdrożenie (CI/CD)

Workflow `.github/workflows/ci-cd.yml` uruchamia się przy `push`, `pull_request` i `workflow_dispatch`.

Job `test`: sprawdza składnię syntaktyczną (`python -m compileall`, `bash -n deployment/ssh-command.sh`), uruchamia testy `webapp/tests` i `deployment`, pakuje przetestowane źródło do `release.zip` i publikuje artefakt `release-<sha>`.

Job `deploy`: uruchamia się tylko przy push na `main` (nie przy PR), w środowisku `production`, na dedykowanym runnerze `[self-hosted, linux, x64, cycling-production]`. Testy i pakowanie działają na runnerze GitHuba; runner produkcyjny pobiera dokładnie ten artefakt. Wdrożenia są szeregowane przez `concurrency: cancel-in-progress: false`. Przed wdrożeniem job odrzuca przestarzały stan: jeśli `status` nie jest `uninitialized`, wymaga, aby uruchomiona rewizja była przodkiem `GITHUB_SHA` (`git merge-base --is-ancestor`). Po wdrożeniu weryfikuje, że `status` i publiczny `/healthz` zwracają dokładny `GITHUB_SHA`.

Jednorazowe przygotowanie serwera: `sudo bash deployment/setup-receiver.sh`. Skrypt tworzy konto `cycling-runner`, instaluje odbiorcę należącego do roota oraz regułę sudo ograniczoną do `/usr/local/sbin/cycling-deploy`. Drop-in systemd przełącza ścieżkę usługi na `/var/lib/cycling-deploy/current`; przed pierwszym wdrożeniem link wskazuje istniejącą instalację `/opt/cycling-web`. Skrypt nie restartuje aplikacji. Następnie zarejestruj oficjalnego GitHub Actions Runner dla tego repozytorium z etykietą `cycling-production` i zainstaluj jego usługę jako `cycling-runner`. Ten runner jest przeznaczony wyłącznie dla zaufanego joba wdrożeniowego z `main`; PR-y uruchamiają testy na `ubuntu-24.04`. Nie są potrzebne sekrety SSH ani otwarty publiczny port SSH.

Odbiorca (`deployment/receive.py`) działa jako root, odczytuje stałą konfigurację `/etc/cycling-web/deploy.json`:

```json
{
  "state_dir": "/var/lib/cycling-deploy",
  "health_url": "http://127.0.0.1:20144",
  "health_attempts": 10,
  "health_interval": 2
}
```

Akceptuje wyłącznie archiwum o maksymalnie 32 MiB (spakowane i rozpakowane), o poprawnym SHA-256 zgodnym z argumentem i dokładnie 14 wpisach ze stałej listy: 5 plików `webapp/`, 6 plików `results/*.csv`, 2 pliki `experiments/control_5000/results/` oraz `revision.txt`. Odrzuca symlinki, duplikaty, wpisy katalogowe, niezgodną rewizję w archiwum, błędną składnię `webapp/server.py`, nieprawidłowy JSON i brak nagłówków CSV. Zmiana jest atomowa: nowa release pod `/var/lib/cycling-deploy/releases` (katalogi 755, pliki 644) i zamiana symbolicznego linku `current`. Po wdrożeniu restartowany jest wyłącznie `cycling-web.service`; sprawność oznacza `/healthz` z dokładną rewizją i `/api/analysis` z `count > 0`. W razie porażki odbiorca wraca do poprzedniej release, a przy pierwszym wdrożeniu do legacy `/opt/cycling-web`.

`status` zwraca `uninitialized` przed pierwszym wdrożeniem (także gdy current wskazuje legacy bez `revision.txt`) oraz aktualną rewizję po wdrożeniu.

Opcjonalny transport SSH (nieużywany przez obecny workflow): `deployment/ssh-command.sh` dozwala wyłącznie `status` albo `deploy <40-hex-SHA> <64-hex-digest>` i wymusza `exec sudo -n /usr/local/sbin/cycling-deploy`.

Lokalna paczka (bez CI):

```bash
python3 deployment/package.py <SHA commita> release.zip
```

Testy odbiorcy (restart i health są zastąpione stubami, stan budowany w katalogu tymczasowym):

```bash
python3 -m unittest discover -s deployment -v
```

## Ograniczenia

- Repozytorium nie zawiera artefaktu wytrenowanego modelu gotowego do inferencji na nowych danych.
- Kalkulator jest implementacją wzoru, a nie modelem ML.
- Wyniki są historyczne i nie zastępują walidacji prospektywnej.
- Dokument pracy jest dostępny tylko po polsku.
- Wszystko, co przeglądarka może wyświetlić, może zostać skopiowane; czytnik jedynie utrudnia pobranie kompletnego dokumentu jednym kliknięciem.
