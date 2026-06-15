# Załącznik elektroniczny do pracy magisterskiej

Ten katalog zawiera wybrane elementy potrzebne do odtworzenia najważniejszych etapów analizy opisanej w pracy:

- `scripts/` - skrypty pobierania danych, budowy cech, trenowania modeli, analizy SHAP, próby kontrolnej 5000 archiwów oraz analizy błędów według zakresów FTP,
- `results/` - zapisane metryki, predykcje testowe, listy cech i pomocnicze zestawienia interpretowalności,
- `figures/` - wykresy wykorzystane w pracy,
- `config/local_paths.example.json` - przykładowa konfiguracja ścieżek lokalnych,
- `requirements.txt` - podstawowe zależności środowiska Python.

## Odtworzenie analizy

1. Utworzyć środowisko Python i zainstalować zależności:

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

2. Skonfigurować lokalne ścieżki na podstawie `config/local_paths.example.json`.

3. Uruchamiać skrypty zgodnie z kolejnością opisaną w pracy: pobranie danych, budowa cech, trenowanie modeli, analiza interpretowalności i analiza błędów.

## Elementy celowo pominięte

W załączniku nie umieszczono:

- roboczych raportów z katalogu `reports/`,
- starych wersji PDF, DOCX i plików pomocniczych LaTeX,
- pliku `config/local_paths.json` z lokalnymi ścieżkami użytkownika,
- notatek, promptów, audytów roboczych i plików tymczasowych,
- skryptów zawierających robocze placeholdery TODO.

Załącznik ma charakter techniczny i zawiera wyłącznie materiały potrzebne do weryfikacji potoku analitycznego oraz wyników.
