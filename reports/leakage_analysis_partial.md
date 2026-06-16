# Analiza wycieku danych (Data Leakage)

Porównanie wariantów dla modelu bazowego (Random Forest):

| Wariant | R2 | MAE | Różnica MAE do wariantu A |
|---------|---|---|---|
| A (z mmp_20min) | 1.0000 | 0.00 | 0.00 |
| B (bez mmp_20min) | 0.9619 | 6.62 | +6.62 |
| C (bez mmp_*) | 0.9134 | 10.36 | +10.36 |

## Wnioski z leakage
1. **Wpływ `mmp_20min`:** Wyniki wariantu A są nienaturalnie wysokie, co sugeruje silny wyciek danych (tzw. label leakage) z cechy `mmp_20min`, na podstawie której u części zawodników estymowane jest FTP (jako 95% 20min power). Z usunięciem tej cechy błąd rośnie, a R2 maleje.
2. **Zachowanie predykcji po usunięciu wycieku:** Po wykluczeniu mmp_20min (Wariant B), model osiąga MAE na poziomie 6.62, co stanowi realną miarę jego skuteczności na podstawie pozostałych wskaźników historycznych i krótko-dystansowych.
3. **Usunięcie wszystkich mmp (Wariant C):** Gdy wyeliminujemy wszelkie moce maksymalne, wskaźniki błędów ulegają zauważalnemu pogorszeniu, wskazując na znaczenie maksymalnych generowanych mocy w szerszych oknach do ogólnej oceny FTP.
