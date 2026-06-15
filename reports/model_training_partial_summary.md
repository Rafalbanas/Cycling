# Podsumowanie trenowania modeli na zbiorze częściowym

## Użyty dataset
- **Plik:** `features_ftp_dataset_rich_partial.csv`
- **Rekordy (filtr FTP):** 151399
- **Zawodnicy:** 726

## Warianty
- **Variant A:** Zawiera `mmp_20min` (cecha powiązana metodologicznie z klasycznym testem FTP). Skutkuje ryzykiem mocnego data leakage.
- **Variant B:** Podstawowy i najbardziej zalecany. Posiada wszystkie metryki poza głównym źródłem wycieku `mmp_20min`. Zawiera 46 cech.
- **Variant C:** Konserwatywny. Całkowicie wycina zmienne z prefixem `mmp_` w celu oceny czy to telemetryczne cechy serca czy tylko moc wpływa na predykcje. Zawiera 41 cech.

## Podział danych
Zastosowano podział osobniczy, dzięki czemu modele były walidowane na kompletnie nieznanych zawodnikach z test-setu. 
Podział wyniósł 117903 (trening) do 33496 (test) wierszy.

## Wyniki i najlepsze modele
Z użytych algorytmów na czysto, najlepiej w Wariancie B poradził sobie **XGBoost** z wynikiem R2 na poziomie 0.9630.
Dla wariantu C zwyciężył **XGBoost** osiągając R2: 0.9170.

## Wniosek o leakage wariantu A
Widoczny jest drastyczny i spodziewany spadek metryk po przejściu z wariantu A na B i C. Zjawisko to wprost waliduje potrzebę zablokowania `mmp_20min` na etapie modelowania produkcyjnego, zgodnie z metodologią badawczą.

## Konkluzje do pracy
Uzyskane wyniki i wielkość próby danych (>150 000 wierszy dla >700 zawodników) są wystarczające do zbudowania solidnej podbudowy analitycznej w pracy magisterskiej, chociaż dalsza analiza błędów np. podział per-sezon czy profil kolarza, może być interesującą drogą rozszerzenia. Na tym etapie tabele wygenerowane przez te skrypty stanowią gotowy materiał do włączenia do pliku LaTeX.

**Do weryfikacji ręcznej (TODO dla autora):**
- Ocena czy R2 wariantu B odpowiada wymaganiom dziedziny na przewidywania kolarskie.
- Sprawdzenie ważności cech `feature_importance_variant_B_partial.csv` by zaobserwować jakie fizjologiczne parametry determinowały decyzje Random Forest / XGBoost (w szczególności bicie serca vs kadencja itp.).

