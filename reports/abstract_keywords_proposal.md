# Propozycja streszczenia i słów kluczowych

## Streszczenie

Praca dotyczy estymacji operacyjnej etykiety Functional Threshold Power (FTP) na podstawie danych telemetrycznych rejestrowanych podczas treningów kolarskich. Celem badania było zaprojektowanie, implementacja i ocena prototypowego potoku analitycznego, który przekształca surowe dane z aktywności sportowych w zagregowany zbiór cech oraz umożliwia porównanie modeli regresyjnych. Materiał empiryczny stanowiły zanonimizowane dane GoldenCheetah OpenData. Po filtracji jakościowej zbiór bazowy obejmował 151 399 sesji treningowych 726 zawodników.

W pracy przygotowano trzy warianty eksperymentalne różniące się zakresem wykorzystanych cech. Wariant A miał charakter kontrolny i zawierał cechę `mmp_20min`, bezpośrednio związaną ze sposobem wyznaczania etykiety FTP. Wariant B usuwał tę cechę, natomiast wariant C usuwał całą rodzinę cech `mmp_*`. Modele Ridge Regression, Random Forest i XGBoost oceniono z użyciem podziału osobniczego, w którym sesje jednego zawodnika nie mogły występować jednocześnie w zbiorze treningowym i testowym.

Najlepszy wynik w głównym wariancie B uzyskał model XGBoost, osiągając MAE = 6,55 W oraz R2 = 0,9630. Wariant C, bardziej konserwatywny metodologicznie, uzyskał wyższy błąd, ale nadal pozwalał odtworzyć znaczną część wariancji operacyjnej etykiety FTP. Wyniki wskazują, że zagregowana telemetria treningowa zawiera użyteczny sygnał predykcyjny, lecz nie stanowią potwierdzenia laboratoryjnej trafności fizjologicznej. Model estymuje etykietę zdefiniowaną jako 0,95 maksymalnej średniej mocy 20-minutowej, a nie bezpośrednio zmierzony próg fizjologiczny.

## Słowa kluczowe

FTP, telemetria sportowa, kolarstwo, uczenie maszynowe, regresja, data leakage, GoldenCheetah, XGBoost

## Abstract

This thesis investigates the estimation of an operational Functional Threshold Power (FTP) label from telemetry data recorded during cycling training sessions. The aim of the study was to design, implement and evaluate a prototype analytical pipeline that transforms raw activity data into aggregated features and enables the comparison of regression models. The empirical material was based on anonymized GoldenCheetah OpenData records. After quality filtering, the baseline dataset contained 151,399 training sessions from 726 athletes.

Three experimental feature variants were prepared. Variant A was a control setting and included `mmp_20min`, a feature directly related to the FTP label definition. Variant B removed this feature, while Variant C removed the entire `mmp_*` feature family. Ridge Regression, Random Forest and XGBoost models were evaluated using a subject-wise split, ensuring that sessions from the same athlete did not appear in both the training and test sets.

In the main Variant B setting, the best result was achieved by XGBoost, with MAE = 6.55 W and R2 = 0.9630. Variant C, which was methodologically more conservative, produced a higher error but still explained a substantial part of the variance of the operational FTP label. The results indicate that aggregated training telemetry contains a useful predictive signal. However, they do not validate the physiological accuracy of the label in laboratory terms. The model estimates an operational label defined as 0.95 of the maximal 20-minute mean power rather than a directly measured physiological threshold.

## Keywords

FTP, sports telemetry, cycling, machine learning, regression, data leakage, GoldenCheetah, XGBoost
