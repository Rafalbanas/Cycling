#!/usr/bin/env python3
"""Generate reproducible theoretical figures used in chapter 1."""

import os
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "figures" / "theory"

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-config"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "fontconfig-cache"))

try:
    import matplotlib
except ModuleNotFoundError:
    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
    if venv_python.exists() and Path(sys.executable) != venv_python:
        os.execve(str(venv_python), [str(venv_python), *sys.argv], os.environ)
    raise

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


POWER_COLOR = "#1f77b4"
TEST_COLOR = "#c44e52"
GRID_COLOR = "#b0b0b0"
HEART_RATE_COLOR = "#d62728"


def configure_plot_style() -> None:
    """Apply a simple, readable style without external plotting libraries."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 11,
            "axes.grid": True,
            "grid.color": GRID_COLOR,
            "grid.linestyle": ":",
            "grid.linewidth": 0.7,
            "grid.alpha": 0.7,
        }
    )


def save_figure(fig: plt.Figure, filename: str) -> None:
    """Save a figure in publication-ready resolution and close it."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def add_phase_label(ax: plt.Axes, start: float, end: float, label: str, y: float) -> None:
    """Add a centered phase label with subtle alternating background."""
    ax.axvspan(start, end, color="#d9e6f2", alpha=0.18)
    ax.text((start + end) / 2, y, label, ha="center", va="center", fontsize=9)


def generate_cardiac_drift() -> None:
    """Generate an illustrative heart-rate drift chart at approximately constant power."""
    time = np.arange(0, 60, 0.1)
    power = np.full_like(time, 200.0) + np.random.normal(0, 3.5, size=time.size)
    heart_rate = (
        100
        + 48 * (1 - np.exp(-time / 2.0))
        + 0.38 * time
        + np.random.normal(0, 0.9, size=time.size)
    )

    fig, power_ax = plt.subplots(figsize=(11, 5.5))
    heart_rate_ax = power_ax.twinx()
    power_ax.plot(time, power, color=POWER_COLOR, linewidth=1.2, alpha=0.75)
    heart_rate_ax.plot(time, heart_rate, color=HEART_RATE_COLOR, linewidth=1.5)

    power_ax.set(
        title="Ilustracja zjawiska dryfu tętna przy stałej mocy",
        xlabel="Czas [min]",
        ylabel="Moc [W]",
        xlim=(0, 60),
        ylim=(100, 250),
    )
    heart_rate_ax.set_ylabel("Tętno [bpm]", color=HEART_RATE_COLOR)
    heart_rate_ax.set_ylim(100, 190)
    power_ax.tick_params(axis="y", colors=POWER_COLOR)
    power_ax.yaxis.label.set_color(POWER_COLOR)
    heart_rate_ax.tick_params(axis="y", colors=HEART_RATE_COLOR)
    heart_rate_ax.grid(False)

    drift_start = 10
    drift_end = 55
    start_heart_rate = heart_rate[np.searchsorted(time, drift_start)]
    end_heart_rate = heart_rate[np.searchsorted(time, drift_end)]
    drift = end_heart_rate - start_heart_rate
    heart_rate_ax.annotate(
        f"Dryf tętna\n(wzrost o około {drift:.0f} bpm)",
        xy=(drift_end, end_heart_rate),
        xytext=(36, 181),
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "->", "color": "#333333", "linewidth": 1.8},
    )
    fig.tight_layout()
    save_figure(fig, "cardiac_drift.png")


def generate_ftp_20min_protocol() -> None:
    """Generate a synthetic power profile for the 20-minute FTP protocol."""
    time = np.arange(0, 70, 0.1)
    power = np.zeros_like(time)

    warmup = time < 15
    activation = (time >= 15) & (time < 18)
    rest = (time >= 18) & (time < 25)
    test = (time >= 25) & (time < 45)
    cooldown = time >= 45

    power[warmup] = np.linspace(100, 165, warmup.sum())
    power[activation] = 300
    power[rest] = np.linspace(115, 100, rest.sum())
    power[test] = np.linspace(260, 245, test.sum())
    power[cooldown] = np.linspace(140, 95, cooldown.sum())
    power += np.random.normal(0, 4.5, size=time.size)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(time, power, color=POWER_COLOR, linewidth=1.3, label="Moc [W]")
    ax.axvspan(25, 45, color=TEST_COLOR, alpha=0.12, label="Odcinek testowy (20 min)")
    add_phase_label(ax, 0, 15, "Rozgrzewka", 185)
    add_phase_label(ax, 15, 18, "Wysiłek\npobudzający", 330)
    add_phase_label(ax, 18, 25, "Odpoczynek /\nspokojna jazda", 150)
    add_phase_label(ax, 25, 45, "Test 20-minutowy", 285)
    add_phase_label(ax, 45, 70, "Rozjazd", 165)
    ax.set(
        title="Profil mocy podczas protokołu testowego FTP (20 min)",
        xlabel="Czas [min]",
        ylabel="Moc [W]",
        xlim=(0, 70),
        ylim=(0, 360),
    )
    ax.legend(loc="upper right")
    fig.tight_layout()
    save_figure(fig, "ftp_20min_protocol.png")


def generate_ftp_60min_protocol() -> None:
    """Generate a synthetic power profile for the full 60-minute FTP protocol."""
    time = np.arange(0, 100, 0.1)
    power = np.zeros_like(time)

    warmup = time < 20
    preparation = (time >= 20) & (time < 30)
    test = (time >= 30) & (time < 90)
    cooldown = time >= 90

    power[warmup] = np.linspace(100, 165, warmup.sum())
    power[preparation] = np.linspace(125, 105, preparation.sum())
    power[test] = np.linspace(255, 245, test.sum())
    power[cooldown] = np.linspace(140, 100, cooldown.sum())
    power += np.random.normal(0, 4, size=time.size)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(time, power, color=POWER_COLOR, linewidth=1.3, label="Moc [W]")
    ax.axvspan(30, 90, color=TEST_COLOR, alpha=0.12, label="Odcinek testowy (60 min)")
    add_phase_label(ax, 0, 20, "Rozgrzewka", 185)
    add_phase_label(ax, 20, 30, "Przygotowanie /\nspokojna jazda", 155)
    add_phase_label(ax, 30, 90, "Test 60-minutowy", 280)
    add_phase_label(ax, 90, 100, "Rozjazd", 165)
    ax.set(
        title="Profil mocy podczas pełnego testu FTP (60 min)",
        xlabel="Czas [min]",
        ylabel="Moc [W]",
        xlim=(0, 100),
        ylim=(0, 330),
    )
    ax.legend(loc="upper right")
    fig.tight_layout()
    save_figure(fig, "ftp_60min_protocol.png")


def generate_power_duration_curve() -> None:
    """Generate an illustrative power-duration curve based on critical power."""
    duration = np.logspace(0, np.log10(7200), 300)
    max_power = 1200
    critical_power = 280
    decay_constant = 60
    power = critical_power + (max_power - critical_power) * np.exp(
        -duration / decay_constant
    )
    lower_bound = power * 0.90
    upper_bound = power * 1.05

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.fill_between(duration, 0, lower_bound, color="#9ecae1", alpha=0.45)
    ax.fill_between(
        duration,
        lower_bound,
        upper_bound,
        color="#4292c6",
        alpha=0.45,
        label="Przykładowy zakres obserwowanych wartości",
    )
    ax.plot(duration, power, color="#084594", linestyle="--", linewidth=2, label="Krzywa mocy")
    ax.axhline(
        critical_power,
        color=TEST_COLOR,
        linestyle=":",
        linewidth=1.5,
        label=f"Moc krytyczna: {critical_power} W",
    )
    ax.set_xscale("log")
    ax.set_xticks([1, 5, 15, 30, 60, 120, 300, 600, 1200, 3600, 7200])
    ax.set_xticklabels(["1 s", "5 s", "15 s", "30 s", "1 min", "2 min", "5 min", "10 min", "20 min", "1 h", "2 h"])
    ax.set(
        title="Przykładowa krzywa mocy na podstawie koncepcji mocy krytycznej",
        xlabel="Czas trwania wysiłku",
        ylabel="Moc [W]",
        xlim=(1, 7200),
        ylim=(0, max_power + 100),
    )
    ax.legend(loc="upper right")
    fig.tight_layout()
    save_figure(fig, "power_duration_curve.png")


def main() -> None:
    np.random.seed(42)
    configure_plot_style()
    generate_cardiac_drift()
    generate_ftp_20min_protocol()
    generate_ftp_60min_protocol()
    generate_power_duration_curve()
    print(f"Generated theory figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
