#!/usr/bin/env python3
"""Summarize prediction errors by reference FTP range."""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "baseline_predictions_variant_b.csv"
OUTPUT = ROOT / "results" / "error_by_ftp_bins.csv"


def main() -> None:
    df = pd.read_csv(INPUT)
    required = {"athlete_id", "y_true", "y_pred"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df["abs_error_w"] = (df["y_true"] - df["y_pred"]).abs()
    df["ape_pct"] = np.where(
        df["y_true"] != 0,
        df["abs_error_w"] / df["y_true"] * 100,
        np.nan,
    )
    df["FTP range"] = pd.cut(
        df["y_true"],
        bins=[0, 150, 250, 350, np.inf],
        labels=["<150 W", "150-250 W", "250-350 W", ">=350 W"],
        right=False,
    )

    summary = (
        df.groupby("FTP range", observed=False)
        .agg(
            Samples=("y_true", "size"),
            Athletes=("athlete_id", "nunique"),
            **{"MAE [W]": ("abs_error_w", "mean"), "MAPE [%]": ("ape_pct", "mean")},
        )
        .reset_index()
    )
    summary["MAE [W]"] = summary["MAE [W]"].round(2)
    summary["MAPE [%]"] = summary["MAPE [%]"].round(2)
    summary.to_csv(OUTPUT, index=False)
    print(summary.to_string(index=False))
    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()
