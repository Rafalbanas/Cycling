# Długość treści przed rozbudową

Pomiar wykonano poleceniem `wc -m` przed rozbudową aktywnych rozdziałów.

Rozdział 1 jest przechowywany fizycznie w dwóch plikach: `chapters/rozdzial1_teoria.tex` oraz `chapters/rozdzial2_literatura.tex`. Ponieważ drugi plik zawiera sekcje 1.5 i 1.6, w raporcie jest liczony jako część rozdziału 1.

| Część pracy | Aktywne pliki | Liczba znaków ze spacjami |
|---|---|---:|
| Wstęp | `chapters/wstep.tex` | 6 583 |
| Rozdział 1. Teoretyczne podstawy estymacji FTP i przegląd literatury | `chapters/rozdzial1_teoria.tex`, `chapters/rozdzial2_literatura.tex` | 36 494 |
| Rozdział 2. Metodologia badań i projekt rozwiązania | `chapters/rozdzial3_metodologia.tex` | 6 208 |
| Rozdział 3. Eksperymenty i wyniki | `chapters/rozdzial4_eksperymenty.tex` | 13 949 |
| Rozdział 4. Ocena rozwiązania, zastosowanie praktyczne i dyskusja | `chapters/rozdzial5_dyskusja.tex` | 5 624 |
| Zakończenie | `chapters/zakonczenie.tex` | 2 802 |
| **Suma** |  | **71 660** |

Kopię aktywnych plików przed rozbudową zapisano w:

`backups/expand_content_20260531_213930/`
