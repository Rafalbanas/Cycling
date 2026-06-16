"""Generate thesis figures from existing experiment result CSV files.

The script intentionally uses only repository-local result files. It does not
read raw data, does not access the SSD data root, and does not rerun
experiments.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTROL_COMPARISON = PROJECT_ROOT / "experiments/control_5000/results/baseline_vs_control_5000.csv"
OUTPUT_DIR = PROJECT_ROOT / "figures/control_5000"
MPL_CACHE = Path(tempfile.gettempdir()) / "master_thesis_matplotlib"
PREDICTION_CANDIDATES = [
    PROJECT_ROOT / "results/baseline_predictions_variant_b.csv",
    PROJECT_ROOT / "results/baseline_predictions_variant_c.csv",
    PROJECT_ROOT / "results/predictions_variant_B.csv",
    PROJECT_ROOT / "results/model_predictions_variant_B.csv",
    PROJECT_ROOT / "results/best_model_predictions.csv",
    PROJECT_ROOT / "experiments/control_5000/results/control_5000_predictions_variant_b.csv",
    PROJECT_ROOT / "experiments/control_5000/results/control_5000_predictions_variant_c.csv",
    PROJECT_ROOT / "experiments/control_5000/results/predictions_variant_B.csv",
    PROJECT_ROOT / "experiments/control_5000/results/model_predictions_variant_B.csv",
    PROJECT_ROOT / "experiments/control_5000/results/best_model_predictions.csv",
]

MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def repo_path(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def format_variant(value: str) -> str:
    return value.replace("Variant_", "")


def format_model(value: str) -> str:
    if value == "RandomForest":
        return "Random Forest"
    return value


def normalize_predictions(path: Path, default_experiment: str | None = None) -> pd.DataFrame | None:
    frame = pd.read_csv(path)
    aliases = {
        "y_true": ["y_true", "actual", "ftp_true", "ftp_label", "actual_ftp"],
        "y_pred": ["y_pred", "predicted", "prediction", "ftp_pred", "predicted_ftp"],
    }

    columns_lower = {column.lower(): column for column in frame.columns}
    resolved: dict[str, str] = {}
    for target, candidates in aliases.items():
        for candidate in candidates:
            if candidate in columns_lower:
                resolved[target] = columns_lower[candidate]
                break
        if target not in resolved:
            return None

    normalized = pd.DataFrame(
        {
            "y_true": pd.to_numeric(frame[resolved["y_true"]], errors="coerce"),
            "y_pred": pd.to_numeric(frame[resolved["y_pred"]], errors="coerce"),
        }
    ).dropna()
    if normalized.empty:
        return None

    if "experiment" in columns_lower:
        normalized["experiment"] = frame.loc[normalized.index, columns_lower["experiment"]].astype(str)
    elif default_experiment:
        normalized["experiment"] = default_experiment
    else:
        name = path.name.lower()
        normalized["experiment"] = "control_5000" if "control" in name else "baseline"

    if "variant" in columns_lower:
        normalized["variant"] = frame.loc[normalized.index, columns_lower["variant"]].astype(str)
    else:
        normalized["variant"] = "Variant_B" if "variant_b" in path.name.lower() else ""

    if "model" in columns_lower:
        normalized["model"] = frame.loc[normalized.index, columns_lower["model"]].astype(str)
    else:
        normalized["model"] = ""

    normalized["residual"] = normalized["y_pred"] - normalized["y_true"]
    return normalized


def generate_baseline_control_plot() -> None:
    print(f"Reading metrics CSV: {repo_path(CONTROL_COMPARISON)}")
    comparison = pd.read_csv(CONTROL_COMPARISON)
    comparison = comparison[comparison["Variant"].isin(["Variant_B", "Variant_C"])].copy()
    comparison["Label"] = comparison["Variant"].map(format_variant) + "\n" + comparison["Model"].map(format_model)
    comparison = comparison.sort_values(["Variant", "Model"]).reset_index(drop=True)

    labels = comparison["Label"].tolist()
    x_positions = list(range(len(comparison)))
    width = 0.38

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 7.8), constrained_layout=True)
    baseline_color = "#4F81BD"
    control_color = "#70AD47"

    axes[0].bar(
        [x - width / 2 for x in x_positions],
        comparison["MAE_Baseline"],
        width,
        label="Eksperyment bazowy",
        color=baseline_color,
    )
    axes[0].bar(
        [x + width / 2 for x in x_positions],
        comparison["MAE_Control"],
        width,
        label="Próba kontrolna 5000",
        color=control_color,
    )
    axes[0].set_ylabel("MAE [W]")
    axes[0].set_title("Błąd bezwzględny MAE dla wariantów B i C", pad=12)
    axes[0].set_ylim(0, 15)
    axes[0].set_xticks(list(x_positions))
    axes[0].set_xticklabels(labels)
    axes[0].grid(axis="y", linestyle=":", alpha=0.45)
    axes[0].bar_label(axes[0].containers[0], fmt="%.2f", padding=3, fontsize=8)
    axes[0].bar_label(axes[0].containers[1], fmt="%.2f", padding=3, fontsize=8)
    axes[0].legend(loc="upper right", frameon=False, ncol=2)

    axes[1].bar(
        [x - width / 2 for x in x_positions],
        comparison["R2_Baseline"],
        width,
        label="Eksperyment bazowy",
        color=baseline_color,
    )
    axes[1].bar(
        [x + width / 2 for x in x_positions],
        comparison["R2_Control"],
        width,
        label="Próba kontrolna 5000",
        color=control_color,
    )
    axes[1].set_ylabel(r"$R^2$")
    axes[1].set_title(r"Współczynnik determinacji $R^2$ dla wariantów B i C", pad=12)
    axes[1].set_ylim(0.86, 0.99)
    axes[1].set_xticks(list(x_positions))
    axes[1].set_xticklabels(labels)
    axes[1].grid(axis="y", linestyle=":", alpha=0.45)
    axes[1].bar_label(axes[1].containers[0], fmt="%.4f", padding=3, fontsize=8)
    axes[1].bar_label(axes[1].containers[1], fmt="%.4f", padding=3, fontsize=8)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "baseline_vs_control_5000_metrics.png"
    fig.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated figure: {repo_path(output_path)}")


def find_prediction_files() -> list[Path]:
    existing = [path for path in PREDICTION_CANDIDATES if path.exists()]
    if existing:
        return existing

    candidates = []
    for directory in [PROJECT_ROOT / "results", PROJECT_ROOT / "experiments/control_5000/results"]:
        if not directory.exists():
            continue
        for path in directory.glob("*.csv"):
            name = path.name.lower()
            if any(token in name for token in ["pred", "actual", "y_pred", "residual"]):
                candidates.append(path)
    return sorted(candidates)


def report_prediction_availability() -> None:
    prediction_files = find_prediction_files()
    if not prediction_files:
        print(
            "Prediction-vs-actual figures were not generated: no repository-local CSV "
            "with actual/predicted FTP columns was found."
        )
        return

    print("Potential prediction CSV files found, but no overlay was generated automatically:")
    for path in prediction_files:
        print(f"- {repo_path(path)}")
    print(
        "Expected columns would need to identify actual FTP and predicted FTP for both "
        "the baseline experiment and the 5000-archive control sample."
    )


def sample_for_plot(frame: pd.DataFrame, max_points_per_experiment: int = 6000) -> pd.DataFrame:
    samples = []
    for _, group in frame.groupby("experiment"):
        if len(group) > max_points_per_experiment:
            samples.append(group.sample(max_points_per_experiment, random_state=42))
        else:
            samples.append(group)
    return pd.concat(samples, ignore_index=True)


def load_variant_b_predictions() -> pd.DataFrame | None:
    baseline_path = PROJECT_ROOT / "results/baseline_predictions_variant_b.csv"
    control_path = PROJECT_ROOT / "experiments/control_5000/results/control_5000_predictions_variant_b.csv"
    if not baseline_path.exists() or not control_path.exists():
        report_prediction_availability()
        return None

    frames = [
        normalize_predictions(baseline_path, default_experiment="baseline"),
        normalize_predictions(control_path, default_experiment="control_5000"),
    ]
    if any(frame is None for frame in frames):
        print("Prediction CSV files were found, but their columns could not be normalized.")
        return None
    return pd.concat(frames, ignore_index=True)


def generate_prediction_overlay_plots() -> None:
    predictions = load_variant_b_predictions()
    if predictions is None:
        return

    predictions = predictions[predictions["variant"].str.lower().isin(["variant_b", "b", ""])]
    if predictions.empty:
        print("Prediction CSV files were found, but no Variant_B rows were available.")
        return

    plot_data = sample_for_plot(predictions)
    colors = {
        "baseline": "#4F81BD",
        "control_5000": "#70AD47",
    }
    labels = {
        "baseline": "Eksperyment bazowy",
        "control_5000": "Próba kontrolna 5000",
    }

    min_value = float(np.nanmin([plot_data["y_true"].min(), plot_data["y_pred"].min()]))
    max_value = float(np.nanmax([plot_data["y_true"].max(), plot_data["y_pred"].max()]))
    padding = max((max_value - min_value) * 0.04, 5.0)
    lim_min = min_value - padding
    lim_max = max_value + padding

    fig, ax = plt.subplots(figsize=(8.8, 7.2), constrained_layout=True)
    for experiment, group in plot_data.groupby("experiment"):
        ax.scatter(
            group["y_true"],
            group["y_pred"],
            s=9,
            alpha=0.22,
            color=colors.get(experiment, "#808080"),
            edgecolors="none",
            label=labels.get(experiment, experiment),
        )
    ax.plot([lim_min, lim_max], [lim_min, lim_max], linestyle="--", color="#C00000", linewidth=1.4, label="Linia idealna y=x")
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_xlabel("Rzeczywiste FTP [W]")
    ax.set_ylabel("Przewidywane FTP [W]")
    ax.set_title("Predykcja względem wartości referencyjnej FTP w wariancie B")
    ax.grid(True, linestyle=":", alpha=0.45)
    ax.legend(frameon=False)
    output_path = OUTPUT_DIR / "predicted_vs_actual_baseline_control.png"
    fig.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated figure: {repo_path(output_path)}")

    fig, ax = plt.subplots(figsize=(8.8, 6.2), constrained_layout=True)
    for experiment, group in plot_data.groupby("experiment"):
        ax.scatter(
            group["y_true"],
            group["residual"],
            s=9,
            alpha=0.22,
            color=colors.get(experiment, "#808080"),
            edgecolors="none",
            label=labels.get(experiment, experiment),
        )
    ax.axhline(0, linestyle="--", color="#C00000", linewidth=1.2)
    ax.set_xlabel("Rzeczywiste FTP [W]")
    ax.set_ylabel("Błąd predykcji [W]")
    ax.set_title("Rozkład reszt względem wartości referencyjnej FTP w wariancie B")
    ax.grid(True, linestyle=":", alpha=0.45)
    ax.legend(frameon=False)
    output_path = OUTPUT_DIR / "residuals_baseline_control.png"
    fig.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated figure: {repo_path(output_path)}")


def main() -> None:
    generate_baseline_control_plot()
    generate_prediction_overlay_plots()


if __name__ == "__main__":
    main()
