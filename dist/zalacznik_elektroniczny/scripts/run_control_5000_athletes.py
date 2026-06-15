"""Run the isolated GoldenCheetah control experiment for up to 5000 athletes."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    median_absolute_error,
    r2_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

from data_paths import PROJECT_ROOT, configured_data_root

FTP_MIN = 50.0
FTP_MAX = 500.0
MIN_FREE_GIB = 35.0
DEFAULT_MAX_ATHLETES = 5000
RANDOM_SEED = 42


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=configured_data_root())
    parser.add_argument("--max-athletes", type=int, default=DEFAULT_MAX_ATHLETES)
    parser.add_argument(
        "--stage",
        choices=["download", "process", "analyze", "all"],
        default="all",
    )
    parser.add_argument("--download-batch-size", type=int, default=100)
    parser.add_argument("--process-batch-size", type=int, default=20)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--min-free-gib", type=float, default=MIN_FREE_GIB)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")],
        force=True,
    )


def free_gib(path: Path) -> float:
    return shutil.disk_usage(path).free / 1024**3


def bytes_in_files(paths: list[Path]) -> int:
    return sum(path.stat().st_size for path in paths if path.exists())


def ensure_ssd(data_root: Path | None, min_free_gib: float) -> Path:
    if data_root is None:
        raise SystemExit(
            "Brak ścieżki SSD. Podaj --data-root /Volumes/NAZWA_DYSKU/... "
            "albo ustaw MASTER_THESIS_DATA_ROOT."
        )
    resolved = data_root.expanduser().resolve()
    if not str(resolved).startswith("/Volumes/"):
        raise SystemExit(f"Ścieżka danych nie wskazuje SSD montowanego w /Volumes: {resolved}")
    if not resolved.exists():
        raise SystemExit(f"SSD lub ścieżka danych nie istnieje: {resolved}")
    available = free_gib(resolved)
    if available < min_free_gib:
        raise SystemExit(
            f"Za mało miejsca na SSD: {available:.3f} GiB; wymagane minimum: {min_free_gib:.3f} GiB."
        )
    return resolved


def paths_for(data_root: Path) -> dict[str, Path]:
    gc_root = data_root / "goldencheetah"
    repo_root = PROJECT_ROOT / "experiments" / "control_5000"
    return {
        "gc_root": gc_root,
        "raw_zips": gc_root / "raw_zips",
        "cache": gc_root / "cache",
        "logs": gc_root / "logs",
        "batches": gc_root / "processed" / "batches",
        "ssd_control": gc_root / "control_5000",
        "ssd_outputs": gc_root / "control_5000" / "outputs",
        "repo_root": repo_root,
        "results": repo_root / "results",
        "figures": repo_root / "figures",
        "report": PROJECT_ROOT / "reports" / "control_5000_experiment_report.md",
    }


def prepare_directories(paths: dict[str, Path]) -> None:
    for key in ["raw_zips", "cache", "logs", "batches", "ssd_outputs", "results", "figures"]:
        paths[key].mkdir(parents=True, exist_ok=True)


def run_command(command: list[str]) -> None:
    logging.info("Uruchamiam: %s", " ".join(command))
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def download_until_target(args: argparse.Namespace, paths: dict[str, Path]) -> None:
    while True:
        local_count = len(list(paths["raw_zips"].glob("*.zip")))
        missing = max(0, args.max_athletes - local_count)
        if missing == 0:
            logging.info("Osiągnięto limit lokalnych archiwów ZIP: %s", local_count)
            return
        limit = min(args.download_batch_size, missing)
        command = [
            sys.executable,
            "scripts/download_goldencheetah_raw.py",
            "--limit",
            str(limit),
            "--batch-size",
            str(limit),
            "--max-batches",
            "1",
            "--min-free-gib",
            str(args.min_free_gib),
        ]
        if args.dry_run:
            command.append("--dry-run")
        before = local_count
        run_command(command)
        after = len(list(paths["raw_zips"].glob("*.zip")))
        logging.info("Lokalne ZIP-y: %s -> %s", before, after)
        if args.dry_run or after <= before:
            return


def process_local_archives(args: argparse.Namespace) -> None:
    if args.dry_run:
        logging.info("Tryb dry-run: pomijam ekstrakcję cech.")
        return
    run_command(
        [
            sys.executable,
            "scripts/build_features_dataset_batch.py",
            "--batch-size",
            str(args.process_batch_size),
            "--workers",
            str(args.workers),
            "--min-free-gib",
            str(args.min_free_gib),
        ]
    )


def load_manifest_stats(manifests: list[Path], selected_zips: set[str]) -> tuple[dict, Counter]:
    archive_stats: dict[str, dict] = {}
    session_errors: Counter = Counter()
    for path in manifests:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for archive, stats in manifest.get("archive_results", {}).items():
            if archive not in selected_zips:
                continue
            archive_stats[archive] = stats
            session_errors.update(stats.get("session_errors", {}))
    return archive_stats, session_errors


def load_selected_rows(batch_files: list[Path], selected_zips: set[str]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in batch_files:
        frame = pd.read_csv(path)
        if "source_zip" not in frame.columns:
            raise SystemExit(f"Brak kolumny source_zip w batchu: {path}")
        selected = frame[frame["source_zip"].isin(selected_zips)]
        if not selected.empty:
            frames.append(selected)
    if not frames:
        raise SystemExit("Nie znaleziono rekordów cech dla wybranych archiwów.")
    return pd.concat(frames, ignore_index=True)


def numeric_feature_variants(df: pd.DataFrame) -> dict[str, list[str]]:
    excluded = {
        "athlete_id",
        "ftp_label",
        "date",
        "file_name",
        "uuid",
        "activity_id",
        "source_path",
        "source_zip",
    }
    base = [
        column
        for column in df.select_dtypes(include=[np.number]).columns
        if column not in excluded and not column.startswith("ftp_")
    ]
    return {
        "Variant_A": base,
        "Variant_B": [column for column in base if column != "mmp_20min"],
        "Variant_C": [column for column in base if not column.startswith("mmp_")],
    }


def build_models() -> dict[str, object]:
    return {
        "Ridge": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", Ridge(random_state=RANDOM_SEED)),
            ]
        ),
        "RandomForest": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=100,
                        random_state=RANDOM_SEED,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "XGBoost": XGBRegressor(
            n_estimators=100,
            random_state=RANDOM_SEED,
            objective="reg:squarederror",
            n_jobs=-1,
        ),
    }


def train_models(df: pd.DataFrame, variants: dict[str, list[str]]) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=RANDOM_SEED)
    train_idx, test_idx = next(splitter.split(df, groups=df["athlete_id"]))
    train = df.iloc[train_idx]
    test = df.iloc[test_idx]
    rows: list[dict] = []
    predictions_by_variant: dict[str, pd.DataFrame] = {}
    best_mae_by_variant: dict[str, float] = {}
    for variant, features in variants.items():
        for model_name, model in build_models().items():
            logging.info("Trenowanie: %s / %s", variant, model_name)
            model.fit(train[features], train["ftp_label"])
            predicted = model.predict(test[features])
            mae = float(mean_absolute_error(test["ftp_label"], predicted))
            rows.append(
                {
                    "Variant": variant,
                    "Model": model_name,
                    "MAE": mae,
                    "RMSE": float(np.sqrt(mean_squared_error(test["ftp_label"], predicted))),
                    "R2": float(r2_score(test["ftp_label"], predicted)),
                    "MedAE": float(median_absolute_error(test["ftp_label"], predicted)),
                    "Train_Athletes": int(train["athlete_id"].nunique()),
                    "Test_Athletes": int(test["athlete_id"].nunique()),
                    "Train_Sessions": int(len(train)),
                    "Test_Sessions": int(len(test)),
                }
            )

            if variant in {"Variant_B", "Variant_C"} and (
                variant not in best_mae_by_variant or mae < best_mae_by_variant[variant]
            ):
                prediction_frame = pd.DataFrame(
                    {
                        "experiment": "control_5000",
                        "variant": variant,
                        "model": model_name,
                        "athlete_id": test["athlete_id"].to_numpy(),
                        "y_true": test["ftp_label"].to_numpy(),
                        "y_pred": predicted,
                    }
                )
                prediction_frame["residual"] = prediction_frame["y_pred"] - prediction_frame["y_true"]
                predictions_by_variant[variant] = prediction_frame
                best_mae_by_variant[variant] = mae
    return pd.DataFrame(rows), predictions_by_variant


def describe_sessions(filtered: pd.DataFrame) -> dict:
    per_athlete = filtered.groupby("athlete_id").size()
    return {
        "minimum": int(per_athlete.min()),
        "mean": float(per_athlete.mean()),
        "median": float(per_athlete.median()),
        "maximum": int(per_athlete.max()),
    }


def missing_counts(filtered: pd.DataFrame) -> dict[str, int]:
    keys = [
        "mean_power",
        "mean_hr",
        "mean_cadence",
        "mmp_30s",
        "mmp_5min",
        "mmp_10min",
        "mmp_20min",
        "ftp_label",
    ]
    return {key: int(filtered[key].isna().sum()) for key in keys if key in filtered}


def compare_with_baseline(metrics: pd.DataFrame) -> pd.DataFrame:
    baseline_path = PROJECT_ROOT / "results" / "model_comparison_partial.csv"
    baseline = pd.read_csv(baseline_path)
    joined = baseline.merge(metrics, on=["Variant", "Model"], suffixes=("_Baseline", "_Control"))
    for metric in ["MAE", "RMSE", "R2", "MedAE"]:
        joined[f"{metric}_Difference"] = joined[f"{metric}_Control"] - joined[f"{metric}_Baseline"]
    return joined


def markdown_table(frame: pd.DataFrame, floatfmt: str = ".4f") -> str:
    columns = list(frame.columns)

    def format_value(value: object) -> str:
        if isinstance(value, (float, np.floating)):
            return format(float(value), floatfmt)
        return str(value)

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(format_value(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def archive_rejection_reasons(
    selected_zips: set[str],
    archive_stats: dict[str, dict],
    filtered: pd.DataFrame,
) -> dict[str, str]:
    retained = set(filtered["source_zip"].unique())
    reasons: dict[str, str] = {}
    for archive in sorted(selected_zips - retained):
        stats = archive_stats.get(archive)
        if not stats:
            reasons[archive] = "Brak manifestu po przetwarzaniu"
        elif stats.get("accepted_records", 0) == 0:
            errors = stats.get("session_errors", {})
            reasons[archive] = "; ".join(f"{key}: {value}" for key, value in sorted(errors.items()))
        else:
            reasons[archive] = "Wszystkie zaakceptowane sesje poza zakresem FTP 50--500 W"
    return reasons


def render_report(
    paths: dict[str, Path],
    data_root: Path,
    free_before: float,
    raw_zip_bytes: int,
    archive_stats: dict[str, dict],
    session_errors: Counter,
    selected_zips: set[str],
    filtered: pd.DataFrame,
    unfiltered: pd.DataFrame,
    metrics: pd.DataFrame,
    comparison: pd.DataFrame,
    rejections: dict[str, str],
) -> None:
    ftp = filtered["ftp_label"].describe()
    session_summary = describe_sessions(filtered)
    best_b = metrics[metrics["Variant"] == "Variant_B"].sort_values("MAE").iloc[0]
    best_c = metrics[metrics["Variant"] == "Variant_C"].sort_values("MAE").iloc[0]
    leakage = metrics[metrics["Variant"] == "Variant_A"]["R2"].min() > 0.99
    b_better_than_c = best_b["MAE"] < best_c["MAE"]
    error_rows = "\n".join(f"| {reason} | {count} |" for reason, count in session_errors.most_common())
    metric_rows = markdown_table(metrics, floatfmt=".4f")
    comparison_rows = markdown_table(
        comparison[
        [
            "Variant",
            "Model",
            "MAE_Baseline",
            "MAE_Control",
            "MAE_Difference",
            "RMSE_Baseline",
            "RMSE_Control",
            "R2_Baseline",
            "R2_Control",
            "MedAE_Baseline",
            "MedAE_Control",
        ]
        ],
        floatfmt=".4f",
    )
    paths["report"].write_text(
        f"""# Próba kontrolna na rozszerzonym zbiorze GoldenCheetah OpenData

Data wykonania: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. Cel

Eksperyment jest dodatkową próbą skalowalności. Nie zastępuje eksperymentu bazowego
i nie podmienia tabel, wykresów ani plików wynikowych używanych w głównym PDF.

## 2. Konfiguracja i SSD

| Element | Wartość |
|---|---|
| Ścieżka danych SSD | `{data_root}` |
| Wolne miejsce przed przebiegiem analitycznym | {free_before:.3f} GiB |
| Lokalne archiwa ZIP wybrane do kontroli | {len(selected_zips)} |
| Rozmiar lokalnych ZIP | {raw_zip_bytes / 1024**3:.3f} GiB |
| Cache | `{paths["cache"]}` |
| Logi | `{paths["logs"]}` |
| Duże wyniki pośrednie | `{paths["ssd_outputs"]}` |
| Małe wyniki końcowe | `{paths["results"]}` |

Metodologia pozostała zgodna z baseline: `ftp_label = 0.95 * mmp_20min`,
filtr FTP `50--500 W`, warianty A/B/C, `GroupShuffleSplit(test_size=0.2,
random_state=42)`, Ridge, Random Forest i XGBoost oraz te same ustawienia modeli.

## 3. Statystyki danych

| Element | Wartość |
|---|---:|
| Archiwa przed przetwarzaniem | {len(selected_zips)} |
| Archiwa z manifestem przetwarzania | {len(archive_stats)} |
| Zawodnicy odrzuceni po filtracji | {len(rejections)} |
| Sesje wejściowe CSV | {sum(int(item.get("csv_files", 0)) for item in archive_stats.values())} |
| Sesje zaakceptowane przed filtrem FTP | {len(unfiltered)} |
| Sesje po filtrze FTP | {len(filtered)} |
| Zawodnicy po filtrze FTP | {filtered["athlete_id"].nunique()} |
| Sesje z mocą | {int(filtered["mean_power"].notna().sum())} |
| Sesje z tętnem | {int(filtered["mean_hr"].notna().sum())} |
| Sesje z cechami MMP | {int(filtered["mmp_20min"].notna().sum())} |
| Sesje/zawodnik: minimum | {session_summary["minimum"]} |
| Sesje/zawodnik: średnia | {session_summary["mean"]:.3f} |
| Sesje/zawodnik: mediana | {session_summary["median"]:.3f} |
| Sesje/zawodnik: maksimum | {session_summary["maximum"]} |
| FTP minimum | {ftp["min"]:.3f} W |
| FTP średnia | {ftp["mean"]:.3f} W |
| FTP mediana | {ftp["50%"]:.3f} W |
| FTP maksimum | {ftp["max"]:.3f} W |

### Przyczyny pominięcia sesji

| Przyczyna | Liczba |
|---|---:|
{error_rows or "| Brak | 0 |"}

Szczegółowe statystyki, braki danych i odrzucenia zapisano w katalogu
`experiments/control_5000/results/`.

## 4. Wyniki modeli

{metric_rows}

## 5. Porównanie z baseline

{comparison_rows}

## 6. Interpretacja

- Wariant A {"nadal pokazuje oczekiwany leakage" if leakage else "wymaga ręcznej kontroli leakage"}.
- Najlepszy wariant B: `{best_b["Model"]}`, MAE `{best_b["MAE"]:.3f} W`, R² `{best_b["R2"]:.4f}`.
- Najlepszy wariant C: `{best_c["Model"]}`, MAE `{best_c["MAE"]:.3f} W`, R² `{best_c["R2"]:.4f}`.
- Wariant B {"zachowuje przewagę nad wariantem C" if b_better_than_c else "nie zachowuje przewagi nad wariantem C"} według MAE.

## 7. Ryzyka

- Etykieta nadal jest heurystyczna i zależy od `mmp_20min`.
- Wynik kontrolny nie powinien zastępować bazowego eksperymentu na przefiltrowanym zbiorze.
- Archiwa bez użytecznych sesji i błędne pliki są rejestrowane, a nie ukrywane.

## 8. Rekomendacja

Traktować przebieg jako dodatkową kontrolę skalowalności. Nie aktualizować automatycznie
głównych rozdziałów ani finalnego PDF. Ewentualne dodanie krótkiego podrozdziału
powinno nastąpić dopiero po ręcznej akceptacji wyników.

## 9. Propozycja krótkiego podrozdziału

### Dodatkowa ocena skalowalności pipeline'u

W celu uzupełniającej oceny skalowalności przeprowadzono próbę kontrolną na
rozszerzonym zbiorze GoldenCheetah OpenData. Zachowano definicję etykiety,
filtrację, warianty cech, podział osobniczy oraz konfigurację modeli z eksperymentu
bazowego. Próba ma charakter technicznej kontroli stabilności pipeline'u i nie
zastępuje wyników głównego eksperymentu.
""",
        encoding="utf-8",
    )


def analyze(args: argparse.Namespace, data_root: Path, paths: dict[str, Path], free_before: float) -> None:
    all_zips = sorted(paths["raw_zips"].glob("*.zip"))[: args.max_athletes]
    selected_zips = {path.name for path in all_zips}
    manifests = sorted(paths["batches"].glob("features_batch_*.json"))
    batch_files = sorted(paths["batches"].glob("features_batch_*.csv"))
    archive_stats, session_errors = load_manifest_stats(manifests, selected_zips)
    unfiltered = load_selected_rows(batch_files, selected_zips)
    filtered = unfiltered[unfiltered["ftp_label"].between(FTP_MIN, FTP_MAX, inclusive="both")].copy()
    if filtered["athlete_id"].nunique() < 2:
        raise SystemExit("Za mało zawodników po filtracji do uruchomienia GroupShuffleSplit.")

    variants = numeric_feature_variants(filtered)
    metrics, predictions_by_variant = train_models(filtered, variants)
    comparison = compare_with_baseline(metrics)
    rejections = archive_rejection_reasons(selected_zips, archive_stats, filtered)

    filtered.to_csv(paths["ssd_outputs"] / "features_ftp_control_5000.csv", index=False)
    unfiltered.to_csv(paths["ssd_outputs"] / "features_ftp_control_5000_unfiltered.csv", index=False)
    metrics.to_csv(paths["results"] / "control_5000_metrics.csv", index=False)
    comparison.to_csv(paths["results"] / "baseline_vs_control_5000.csv", index=False)
    for variant, prediction_frame in predictions_by_variant.items():
        suffix = variant.lower()
        prediction_frame.to_csv(paths["results"] / f"control_5000_predictions_{suffix}.csv", index=False)
    pd.Series(missing_counts(filtered), name="missing_count").rename_axis("feature").to_csv(
        paths["results"] / "missing_key_features.csv"
    )
    pd.Series(rejections, name="reason").rename_axis("source_zip").to_csv(
        paths["results"] / "rejected_athletes.csv"
    )
    data_stats = {
        "available_archives": len(all_zips),
        "processed_archives": len(archive_stats),
        "rejected_athletes": len(rejections),
        "sessions_input_csv": sum(int(item.get("csv_files", 0)) for item in archive_stats.values()),
        "sessions_before_ftp_filter": len(unfiltered),
        "sessions_after_ftp_filter": len(filtered),
        "athletes_after_ftp_filter": int(filtered["athlete_id"].nunique()),
        "sessions_with_power": int(filtered["mean_power"].notna().sum()),
        "sessions_with_hr": int(filtered["mean_hr"].notna().sum()),
        "sessions_with_mmp": int(filtered["mmp_20min"].notna().sum()),
        "sessions_per_athlete": describe_sessions(filtered),
        "ftp_label": filtered["ftp_label"].describe().to_dict(),
        "missing_key_features": missing_counts(filtered),
        "session_errors": dict(session_errors),
    }
    (paths["results"] / "control_5000_data_stats.json").write_text(
        json.dumps(data_stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    render_report(
        paths,
        data_root,
        free_before,
        bytes_in_files(all_zips),
        archive_stats,
        session_errors,
        selected_zips,
        filtered,
        unfiltered,
        metrics,
        comparison,
        rejections,
    )


def main() -> None:
    args = parse_args()
    data_root = ensure_ssd(args.data_root, args.min_free_gib)
    paths = paths_for(data_root)
    prepare_directories(paths)
    configure_logging(paths["logs"] / "control_5000.log")
    free_before = free_gib(data_root)
    logging.info("SSD: %s; wolne miejsce: %.3f GiB", data_root, free_before)

    if args.stage in {"download", "all"}:
        download_until_target(args, paths)
    if args.stage in {"process", "all"}:
        process_local_archives(args)
    if args.stage in {"analyze", "all"} and not args.dry_run:
        analyze(args, data_root, paths, free_before)


if __name__ == "__main__":
    main()
