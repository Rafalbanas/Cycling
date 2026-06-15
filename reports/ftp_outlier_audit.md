# Audyt wartości odstających FTP

Data wykonania: 2026-05-30 20:56:08

Jawna reguła jakościowa: do zbioru eksperymentalnego przyjmowane są sesje, dla których
heurystyczna etykieta FTP spełnia warunek `50 <= ftp_label <= 500` W.

| Statystyka | Przed filtrowaniem | Po filtrowaniu |
|---|---:|---:|
| Liczba rekordów | 26123 | 25945 |
| Liczba zawodników | 126 | 126 |
| Minimalne FTP [W] | 0.100 | 50.058 |
| Maksymalne FTP [W] | 675.911 | 485.656 |
| Średnie FTP [W] | 184.703 | 185.703 |
| Mediana FTP [W] | 183.709 | 184.154 |

## Odrzucone rekordy

| Reguła | Liczba rekordów |
|---|---:|
| `ftp_label < 50` W | 174 |
| `ftp_label > 500` W | 4 |
| Razem | 178 |
