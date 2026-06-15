# Raport budowy bogatego zbioru cech

Data wykonania: 2026-05-30 20:56:08

## Podsumowanie

| Element | Wartość |
|---|---:|
| Pliki sesji wejściowych | 45973 |
| Rekordy przed filtrem FTP | 26123 |
| Rekordy po filtrze FTP 50--500 W | 25945 |
| Zawodnicy po filtrze | 126 |
| Odrzucone rekordy FTP | 178 |

## Przyczyny pominięcia sesji przed filtrem FTP

| Przyczyna | Liczba |
|---|---:|
| Brak danych o mocy (power) | 12566 |
| Zbyt krótka sesja (< 30 min) | 6160 |
| Nie można obliczyć FTP (brak pełnego okna MMP20) | 1124 |

## Kolumny wynikowe

- `missing_power_fraction`
- `missing_hr_fraction`
- `missing_cadence_fraction`
- `valid_samples_fraction`
- `duration_sec`
- `moving_time_sec`
- `distance_km`
- `elevation_gain_m`
- `mean_power`
- `median_power`
- `max_power`
- `power_std`
- `power_p25`
- `power_p75`
- `power_p90`
- `power_p95`
- `power_cv`
- `zero_power_fraction`
- `time_above_mean_power_fraction`
- `mmp_30s`
- `mmp_1min`
- `mmp_3min`
- `mmp_5min`
- `mmp_10min`
- `mmp_20min`
- `ftp_label`
- `power_zone_0_100_fraction`
- `power_zone_100_200_fraction`
- `power_zone_200_300_fraction`
- `power_zone_300_400_fraction`
- `power_zone_400_plus_fraction`
- `low_intensity_fraction`
- `moderate_intensity_fraction`
- `high_intensity_fraction`
- `mean_hr`
- `median_hr`
- `max_hr`
- `hr_std`
- `hr_p25`
- `hr_p75`
- `hr_p90`
- `mean_power_to_mean_hr`
- `power_hr_decoupling_pct`
- `hr_drift_simple`
- `mean_cadence`
- `median_cadence`
- `cadence_std`
- `zero_cadence_fraction`
- `file_name`
- `athlete_id`
- `source_path`
