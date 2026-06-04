"""Generate clean and publication-ready power-duration profiles for several athletes.

This script loads the processed partial dataset, filters for athletes with stable
and strictly decreasing median MMP profiles, selects 4 representative athletes,
and plots their power-duration curves on a log-scaled X-axis in a highly readable,
publication-quality format.
"""

from __future__ import annotations

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path("/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/features_ftp_dataset_rich_partial.csv")
OUTPUT_DIR = PROJECT_ROOT / "figures/theory"
OUTPUT_PATH = OUTPUT_DIR / "power_duration_profiles_examples.png"

def main() -> None:
    print(f"Loading dataset from: {DATA_PATH}")
    if not DATA_PATH.exists():
        print(f"Error: Dataset does not exist at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 6 available MMP features and corresponding durations in seconds
    mmp_cols = ["mmp_30s", "mmp_1min", "mmp_3min", "mmp_5min", "mmp_10min", "mmp_20min"]
    durations = [30, 60, 180, 300, 600, 1200]
    
    # Clean and filter
    df_clean = df.dropna(subset=mmp_cols + ["athlete_id"]).copy()
    
    # Count sessions per athlete
    athlete_counts = df_clean["athlete_id"].value_counts()
    eligible_athletes = athlete_counts[athlete_counts >= 30].index.tolist()
    
    if not eligible_athletes:
        print("Error: No athletes meet the session count criteria (>=30).")
        return
        
    print(f"Number of eligible athletes with >=30 sessions: {len(eligible_athletes)}")
    
    # Compute median profiles and apply logic checks (must be strictly decreasing)
    valid_profiles = {}
    for athlete in eligible_athletes:
        athlete_df = df_clean[df_clean["athlete_id"] == athlete]
        median_mmp = athlete_df[mmp_cols].median().to_numpy()
        
        # Check 1: Must be strictly decreasing
        is_decreasing = all(median_mmp[i] > median_mmp[i+1] for i in range(len(median_mmp) - 1))
        
        # Check 2: Difference between short-duration and long-duration power must be significant (no flat lines)
        has_drop = (median_mmp[0] - median_mmp[-1]) >= 150.0
        
        # Check 3: Check for reasonable physical limits (excluding extreme outliers)
        reasonable_range = (100.0 <= median_mmp[-1] <= 420.0) and (median_mmp[0] <= 1100.0)
        
        if is_decreasing and has_drop and reasonable_range:
            valid_profiles[athlete] = {
                "mmp": median_mmp,
                "mmp_20min": median_mmp[-1]
            }
            
    print(f"Number of valid, strictly decreasing profiles: {len(valid_profiles)}")
    
    if len(valid_profiles) < 4:
        print("Error: Not enough valid profiles found to select 4 athletes.")
        return
        
    # Sort selected athletes by their aerobic capacity (20 min power)
    sorted_athletes = sorted(valid_profiles.keys(), key=lambda x: valid_profiles[x]["mmp_20min"])
    
    # Select 4 representative athletes across the power spectrum (e.g. quartiles)
    indices = [
        int(len(sorted_athletes) * 0.15),
        int(len(sorted_athletes) * 0.45),
        int(len(sorted_athletes) * 0.70),
        int(len(sorted_athletes) * 0.92)
    ]
    selected_athletes = [sorted_athletes[idx] for idx in indices]
    
    # Plotting configuration for academic style
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
    })
    
    fig, ax = plt.subplots(figsize=(9, 6), constrained_layout=True)
    
    # Professional color palette (subdued, high contrast)
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]
    markers = ["o", "s", "^", "D"]
    
    for i, athlete_id in enumerate(selected_athletes):
        profile = valid_profiles[athlete_id]
        mmp_values = profile["mmp"]
        
        ax.plot(
            durations,
            mmp_values,
            label=f"Zawodnik {i+1}",
            color=colors[i],
            marker=markers[i],
            linewidth=2,
            markersize=7,
            alpha=0.85
        )
        
    # Vertical dashed line at 20 min (1200 s)
    ax.axvline(1200, color="#7F7F7F", linestyle="--", alpha=0.7, linewidth=1.2)
    
    # Align text carefully near the top of the axis
    ylim = ax.get_ylim()
    y_pos_text = ylim[0] + (ylim[1] - ylim[0]) * 0.85
    ax.text(
        1100,
        y_pos_text,
        "20 min",
        color="#555555",
        fontsize=11,
        va="center",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=2)
    )
    
    # Configure axes
    ax.set_xscale("log")
    ax.set_xticks(durations)
    ax.set_xticklabels(["30 s", "1 min", "3 min", "5 min", "10 min", "20 min"])
    
    ax.set_xlabel("Czas trwania wysiłku", fontsize=12, labelpad=8)
    ax.set_ylabel("Moc [W]", fontsize=12, labelpad=8)
    ax.set_title("Przykładowe profile najlepszej mocy średniej (MMP)", fontsize=13, pad=15, fontweight="bold")
    
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E2E2", loc="upper right")
    
    # Add minor padding to limits
    ax.set_xlim(25, 1500)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Successfully generated clean academic figure at: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
