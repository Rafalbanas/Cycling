"""Build an auditable, rich GoldenCheetah feature dataset.

The original pipeline only exported duration, mean power and MMP20. This
version keeps the same raw CSV inputs but writes a separate rich dataset,
preserves an unfiltered copy, and documents the explicit FTP quality filter.
"""

from __future__ import annotations

import argparse
import logging
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from data_paths import goldencheetah_paths

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

FTP_MIN_DEFAULT = 50.0
FTP_MAX_DEFAULT = 500.0
MIN_DURATION_SEC = 1800
SHORT_GAP_LIMIT = 5

RAW_COLUMN_MAP = {
    "secs": "timestamp_sec",
    "time": "timestamp_sec",
    "timestamp": "timestamp_sec",
    "km": "distance_km_cumulative",
    "distance": "distance_km_cumulative",
    "power": "power",
    "pwr": "power",
    "watts": "power",
    "hr": "heart_rate",
    "bpm": "heart_rate",
    "heartrate": "heart_rate",
    "heart_rate": "heart_rate",
    "cad": "cadence",
    "rpm": "cadence",
    "cadence": "cadence",
    "alt": "altitude_m",
    "altitude": "altitude_m",
}

NUMERIC_COLUMNS = [
    "timestamp_sec",
    "distance_km_cumulative",
    "power",
    "heart_rate",
    "cadence",
    "altitude_m",
]


def find_training_files(raw_dir: Path) -> list[Path]:
    """Return extracted athlete CSV files, excluding downloader metadata."""
    return sorted(
        path
        for path in raw_dir.glob("*/*.csv")
        if path.parent.name != "goldencheetah"
    )


def interpolate_short_gaps(series: pd.Series, limit: int = SHORT_GAP_LIMIT) -> pd.Series:
    """Linearly interpolate only complete internal gaps up to ``limit`` rows."""
    missing = series.isna()
    if not missing.any():
        return series
    groups = missing.ne(missing.shift()).cumsum()
    gap_sizes = missing.groupby(groups).transform("sum")
    fillable = missing & (gap_sizes <= limit)
    interpolated = series.interpolate(method="linear", limit_area="inside")
    return series.where(~fillable, interpolated)


def read_and_clean(filepath: Path) -> tuple[pd.DataFrame, dict[str, float]]:
    df = pd.read_csv(filepath)
    df.columns = [str(column).lower().strip() for column in df.columns]
    df = df.rename(columns=RAW_COLUMN_MAP)

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            df[column] = np.nan
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[NUMERIC_COLUMNS].copy()
    if df.empty:
        return df, {}

    df.loc[(df["power"] < 0) | (df["power"] > 2000), "power"] = np.nan
    df.loc[(df["heart_rate"] < 30) | (df["heart_rate"] > 220), "heart_rate"] = np.nan
    df.loc[(df["cadence"] < 0) | (df["cadence"] > 200), "cadence"] = np.nan

    quality = {
        "missing_power_fraction": float(df["power"].isna().mean()),
        "missing_hr_fraction": float(df["heart_rate"].isna().mean()),
        "missing_cadence_fraction": float(df["cadence"].isna().mean()),
    }
    quality["valid_samples_fraction"] = float(
        1.0 - np.mean(
            [
                quality["missing_power_fraction"],
                quality["missing_hr_fraction"],
                quality["missing_cadence_fraction"],
            ]
        )
    )

    for column in ["power", "heart_rate", "cadence", "distance_km_cumulative", "altitude_m"]:
        df[column] = interpolate_short_gaps(df[column])
    return df, quality


def safe_fraction(mask: pd.Series, valid: pd.Series) -> float:
    valid_count = int(valid.sum())
    if valid_count == 0:
        return np.nan
    return float((mask & valid).sum() / valid_count)


def calculate_mmp(series: pd.Series, window_seconds: int) -> float:
    if series.notna().sum() < window_seconds:
        return np.nan
    rolling = series.rolling(window=window_seconds, min_periods=window_seconds).mean()
    return float(rolling.max()) if rolling.notna().any() else np.nan


def coefficient_of_variation(series: pd.Series) -> float:
    mean = series.mean()
    if pd.isna(mean) or mean == 0:
        return np.nan
    return float(series.std() / mean)


def extract_features(df: pd.DataFrame, quality: dict[str, float]) -> dict[str, float | str]:
    if df.empty:
        return {"error": "Pusty plik CSV"}

    timestamp = df["timestamp_sec"]
    duration_sec = float(timestamp.max() - timestamp.min() + 1) if timestamp.notna().any() else float(len(df))
    if duration_sec < MIN_DURATION_SEC:
        return {"error": "Zbyt krótka sesja (< 30 min)"}

    power = df["power"]
    if power.notna().sum() == 0:
        return {"error": "Brak danych o mocy (power)"}

    mmp_20min = calculate_mmp(power, 1200)
    if pd.isna(mmp_20min):
        return {"error": "Nie można obliczyć FTP (brak pełnego okna MMP20)"}

    hr = df["heart_rate"]
    cadence = df["cadence"]
    distance = df["distance_km_cumulative"]
    altitude = df["altitude_m"]

    features: dict[str, float | str] = dict(quality)
    features["duration_sec"] = duration_sec

    dt = timestamp.diff().clip(lower=0, upper=10)
    distance_diff = distance.diff()
    if distance.notna().sum() >= 2:
        features["moving_time_sec"] = float(dt.where(distance_diff > 0, 0).sum())
        features["distance_km"] = float(max(distance.max() - distance.min(), 0))
    else:
        features["moving_time_sec"] = float((power.fillna(0) > 0).sum())
        features["distance_km"] = np.nan

    if altitude.notna().sum() >= 2:
        elevation_diff = altitude.diff()
        features["elevation_gain_m"] = float(elevation_diff.where((elevation_diff > 0) & (elevation_diff <= 20), 0).sum())
    else:
        features["elevation_gain_m"] = np.nan

    features.update(
        {
            "mean_power": float(power.mean()),
            "median_power": float(power.median()),
            "max_power": float(power.max()),
            "power_std": float(power.std()),
            "power_p25": float(power.quantile(0.25)),
            "power_p75": float(power.quantile(0.75)),
            "power_p90": float(power.quantile(0.90)),
            "power_p95": float(power.quantile(0.95)),
            "power_cv": coefficient_of_variation(power),
            "zero_power_fraction": safe_fraction(power == 0, power.notna()),
            "time_above_mean_power_fraction": safe_fraction(power > power.mean(), power.notna()),
            "mmp_30s": calculate_mmp(power, 30),
            "mmp_1min": calculate_mmp(power, 60),
            "mmp_3min": calculate_mmp(power, 180),
            "mmp_5min": calculate_mmp(power, 300),
            "mmp_10min": calculate_mmp(power, 600),
            "mmp_20min": mmp_20min,
            "ftp_label": float(0.95 * mmp_20min),
        }
    )

    valid_power = power.notna()
    power_bins = [
        ("power_zone_0_100_fraction", power < 100),
        ("power_zone_100_200_fraction", (power >= 100) & (power < 200)),
        ("power_zone_200_300_fraction", (power >= 200) & (power < 300)),
        ("power_zone_300_400_fraction", (power >= 300) & (power < 400)),
        ("power_zone_400_plus_fraction", power >= 400),
    ]
    for name, mask in power_bins:
        features[name] = safe_fraction(mask, valid_power)

    features["low_intensity_fraction"] = safe_fraction(power < 150, valid_power)
    features["moderate_intensity_fraction"] = safe_fraction((power >= 150) & (power < 250), valid_power)
    features["high_intensity_fraction"] = safe_fraction(power >= 250, valid_power)

    if hr.notna().any():
        features.update(
            {
                "mean_hr": float(hr.mean()),
                "median_hr": float(hr.median()),
                "max_hr": float(hr.max()),
                "hr_std": float(hr.std()),
                "hr_p25": float(hr.quantile(0.25)),
                "hr_p75": float(hr.quantile(0.75)),
                "hr_p90": float(hr.quantile(0.90)),
            }
        )
        if hr.mean() != 0:
            features["mean_power_to_mean_hr"] = float(power.mean() / hr.mean())
        else:
            features["mean_power_to_mean_hr"] = np.nan

        midpoint = len(df) // 2
        power_first, power_second = power.iloc[:midpoint], power.iloc[midpoint:]
        hr_first, hr_second = hr.iloc[:midpoint], hr.iloc[midpoint:]
        ratio_first = power_first.mean() / hr_first.mean() if hr_first.mean() else np.nan
        ratio_second = power_second.mean() / hr_second.mean() if hr_second.mean() else np.nan
        if pd.notna(ratio_first) and pd.notna(ratio_second) and ratio_first != 0:
            features["power_hr_decoupling_pct"] = float((ratio_first - ratio_second) / ratio_first * 100)
        else:
            features["power_hr_decoupling_pct"] = np.nan
        if pd.notna(hr_first.mean()) and hr_first.mean() != 0 and pd.notna(hr_second.mean()):
            features["hr_drift_simple"] = float((hr_second.mean() - hr_first.mean()) / hr_first.mean() * 100)
        else:
            features["hr_drift_simple"] = np.nan
    else:
        for name in [
            "mean_hr",
            "median_hr",
            "max_hr",
            "hr_std",
            "hr_p25",
            "hr_p75",
            "hr_p90",
            "mean_power_to_mean_hr",
            "power_hr_decoupling_pct",
            "hr_drift_simple",
        ]:
            features[name] = np.nan

    if cadence.notna().any():
        features.update(
            {
                "mean_cadence": float(cadence.mean()),
                "median_cadence": float(cadence.median()),
                "cadence_std": float(cadence.std()),
                "zero_cadence_fraction": safe_fraction(cadence == 0, cadence.notna()),
            }
        )
    else:
        for name in ["mean_cadence", "median_cadence", "cadence_std", "zero_cadence_fraction"]:
            features[name] = np.nan

    return features


def process_file(filepath: Path) -> dict[str, float | str]:
    try:
        df, quality = read_and_clean(filepath)
        features = extract_features(df, quality)
        if "error" not in features:
            features["file_name"] = filepath.name
            features["athlete_id"] = filepath.parent.name
            features["source_path"] = str(filepath)
        return features
    except Exception as exc:  # noqa: BLE001 - aggregate malformed session errors in report
        return {"error": f"Błąd wczytywania: {type(exc).__name__}"}


def describe_ftp(df: pd.DataFrame) -> dict[str, float | int]:
    ftp = df["ftp_label"]
    return {
        "records": int(len(df)),
        "athletes": int(df["athlete_id"].nunique()) if "athlete_id" in df else 0,
        "minimum": float(ftp.min()) if len(df) else np.nan,
        "maximum": float(ftp.max()) if len(df) else np.nan,
        "mean": float(ftp.mean()) if len(df) else np.nan,
        "median": float(ftp.median()) if len(df) else np.nan,
    }


def write_dataset_report(
    report_path: Path,
    source_files: int,
    errors: Counter,
    unfiltered: pd.DataFrame,
    filtered: pd.DataFrame,
    ftp_min: float,
    ftp_max: float,
) -> None:
    before = describe_ftp(unfiltered)
    after = describe_ftp(filtered)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    error_rows = "\n".join(f"| {reason} | {count} |" for reason, count in errors.most_common()) or "| Brak | 0 |"
    columns = "\n".join(f"- `{column}`" for column in filtered.columns)
    report_path.write_text(
        f"""# Raport budowy bogatego zbioru cech

Data wykonania: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Podsumowanie

| Element | Wartość |
|---|---:|
| Pliki sesji wejściowych | {source_files} |
| Rekordy przed filtrem FTP | {before["records"]} |
| Rekordy po filtrze FTP {ftp_min:.0f}--{ftp_max:.0f} W | {after["records"]} |
| Zawodnicy po filtrze | {after["athletes"]} |
| Odrzucone rekordy FTP | {before["records"] - after["records"]} |

## Przyczyny pominięcia sesji przed filtrem FTP

| Przyczyna | Liczba |
|---|---:|
{error_rows}

## Kolumny wynikowe

{columns}
""",
        encoding="utf-8",
    )


def write_outlier_report(
    report_path: Path,
    unfiltered: pd.DataFrame,
    filtered: pd.DataFrame,
    ftp_min: float,
    ftp_max: float,
) -> None:
    before = describe_ftp(unfiltered)
    after = describe_ftp(filtered)
    low = int((unfiltered["ftp_label"] < ftp_min).sum())
    high = int((unfiltered["ftp_label"] > ftp_max).sum())
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"""# Audyt wartości odstających FTP

Data wykonania: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Jawna reguła jakościowa: do zbioru eksperymentalnego przyjmowane są sesje, dla których
heurystyczna etykieta FTP spełnia warunek `{ftp_min:.0f} <= ftp_label <= {ftp_max:.0f}` W.

| Statystyka | Przed filtrowaniem | Po filtrowaniu |
|---|---:|---:|
| Liczba rekordów | {before["records"]} | {after["records"]} |
| Liczba zawodników | {before["athletes"]} | {after["athletes"]} |
| Minimalne FTP [W] | {before["minimum"]:.3f} | {after["minimum"]:.3f} |
| Maksymalne FTP [W] | {before["maximum"]:.3f} | {after["maximum"]:.3f} |
| Średnie FTP [W] | {before["mean"]:.3f} | {after["mean"]:.3f} |
| Mediana FTP [W] | {before["median"]:.3f} | {after["median"]:.3f} |

## Odrzucone rekordy

| Reguła | Liczba rekordów |
|---|---:|
| `ftp_label < {ftp_min:.0f}` W | {low} |
| `ftp_label > {ftp_max:.0f}` W | {high} |
| Razem | {low + high} |
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    paths = goldencheetah_paths()
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=paths.extracted)
    parser.add_argument("--output", type=Path, default=paths.processed / "features_ftp_dataset_rich.csv")
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--workers", type=int, default=max(1, min((os.cpu_count() or 2) - 1, 8)))
    parser.add_argument("--max-files", type=int)
    parser.add_argument("--ftp-min", type=float, default=FTP_MIN_DEFAULT)
    parser.add_argument("--ftp-max", type=float, default=FTP_MAX_DEFAULT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = find_training_files(args.raw_dir)
    if args.max_files:
        files = files[: args.max_files]
    if not files:
        raise SystemExit(f"Brak plików treningowych CSV w {args.raw_dir}")

    logging.info("Przetwarzanie %s sesji z użyciem %s wątków.", len(files), args.workers)
    rows: list[dict[str, float | str]] = []
    errors: Counter = Counter()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, result in enumerate(executor.map(process_file, files, chunksize=32), start=1):
            if "error" in result:
                errors[str(result["error"])] += 1
            else:
                rows.append(result)
            if index % 1000 == 0 or index == len(files):
                logging.info("Postęp: %s/%s sesji; zaakceptowane przed filtrem FTP: %s", index, len(files), len(rows))

    unfiltered = pd.DataFrame(rows)
    if unfiltered.empty:
        raise SystemExit("Nie wygenerowano żadnych rekordów cech.")

    filtered = unfiltered[
        unfiltered["ftp_label"].between(args.ftp_min, args.ftp_max, inclusive="both")
    ].copy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    unfiltered_path = args.output.with_name(f"{args.output.stem}_unfiltered{args.output.suffix}")
    unfiltered.to_csv(unfiltered_path, index=False)
    filtered.to_csv(args.output, index=False)

    write_dataset_report(
        args.report_dir / "rich_dataset_report.md",
        len(files),
        errors,
        unfiltered,
        filtered,
        args.ftp_min,
        args.ftp_max,
    )
    write_outlier_report(
        args.report_dir / "ftp_outlier_audit.md",
        unfiltered,
        filtered,
        args.ftp_min,
        args.ftp_max,
    )

    logging.info("Zapisano zbiór niefiltrowany: %s", unfiltered_path)
    logging.info("Zapisano zbiór eksperymentalny: %s", args.output)
    logging.info("Zapisano raporty w: %s", args.report_dir)


if __name__ == "__main__":
    main()
