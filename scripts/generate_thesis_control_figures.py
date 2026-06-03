"""Generate thesis figures from existing experiment result CSV files."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTROL_COMPARISON = PROJECT_ROOT / "experiments/control_5000/results/baseline_vs_control_5000.csv"
OUTPUT_DIR = PROJECT_ROOT / "figures/control_5000"
MPL_CACHE = Path(tempfile.gettempdir()) / "master_thesis_matplotlib"

MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def format_variant(value: str) -> str:
    return value.replace("Variant_", "")


def format_model(value: str) -> str:
    if value == "RandomForest":
        return "RF"
    return value


def generate_baseline_control_plot() -> None:
    comparison = pd.read_csv(CONTROL_COMPARISON)
    comparison = comparison[comparison["Variant"].isin(["Variant_B", "Variant_C"])].copy()
    comparison["Label"] = comparison["Variant"].map(format_variant) + " / " + comparison["Model"].map(format_model)

    labels = comparison["Label"].tolist()
    x_positions = range(len(comparison))
    width = 0.36

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)

    axes[0].bar(
        [x - width / 2 for x in x_positions],
        comparison["MAE_Baseline"],
        width,
        label="Baseline 781 archiwów",
        color="#6C8EBF",
    )
    axes[0].bar(
        [x + width / 2 for x in x_positions],
        comparison["MAE_Control"],
        width,
        label="Kontrola 5000 archiwów",
        color="#82B366",
    )
    axes[0].set_ylabel("MAE [W]")
    axes[0].set_title("MAE")
    axes[0].set_xticks(list(x_positions))
    axes[0].set_xticklabels(labels, rotation=35, ha="right")
    axes[0].grid(axis="y", linestyle=":", alpha=0.45)

    axes[1].bar(
        [x - width / 2 for x in x_positions],
        comparison["R2_Baseline"],
        width,
        label="Baseline 781 archiwów",
        color="#6C8EBF",
    )
    axes[1].bar(
        [x + width / 2 for x in x_positions],
        comparison["R2_Control"],
        width,
        label="Kontrola 5000 archiwów",
        color="#82B366",
    )
    axes[1].set_ylabel(r"$R^2$")
    axes[1].set_title(r"$R^2$")
    axes[1].set_ylim(0.84, 0.99)
    axes[1].set_xticks(list(x_positions))
    axes[1].set_xticklabels(labels, rotation=35, ha="right")
    axes[1].grid(axis="y", linestyle=":", alpha=0.45)

    handles, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.03),
        ncol=2,
        frameon=False,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "baseline_vs_control_5000_metrics.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    generate_baseline_control_plot()


if __name__ == "__main__":
    main()
