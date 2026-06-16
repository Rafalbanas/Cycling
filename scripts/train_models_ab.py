"""
train_models_ab.py
==================
Wariant A: wszystkie cechy (w tym mmp_20min -> data leakage)
Wariant B: bez cech powodujacych bezposredni wyciek informacji
           (usuwamy mmp_20min, poniewaz ftp_label = 0.95 * mmp_20min)

Wyniki: results/model_metrics.csv, data/processed/ml_results_A.json, data/processed/ml_results_B.json
Wykresy: data/processed/{wariant}_{typ_wykresu}.png
"""

import json
import logging
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    logging.warning("XGBoost niedostepny – pomijany.")

RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# Kolumny powodujace bezposredni wyciek danych
# ---------------------------------------------------------------------------
LEAKAGE_COLS = [
    "mmp_20min",      # ftp_label = 0.95 * mmp_20min  <- bezposredni wyciek
]

ALWAYS_DROP = [
    "ftp_label",      # zmienna celu - nigdy nie moze byc cecha
    "file_name",      # identyfikator pliku, nie cecha predykcyjna
    "athlete_id",     # identyfikator zawodnika, uzywamy jako grup do podziau
]

# ---------------------------------------------------------------------------
def create_pipeline(model, requires_scaling=False):
    steps = [("imputer", SimpleImputer(strategy="median"))]
    if requires_scaling:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", model))
    return Pipeline(steps)


def build_models():
    models = {
        "Ridge Regression": create_pipeline(Ridge(alpha=1.0), requires_scaling=True),
        "Random Forest": create_pipeline(
            RandomForestRegressor(n_estimators=200, random_state=RANDOM_SEED, n_jobs=-1)
        ),
    }
    if HAS_XGB:
        models["XGBoost"] = create_pipeline(
            XGBRegressor(
                n_estimators=200,
                random_state=RANDOM_SEED,
                objective="reg:squarederror",
                verbosity=0,
            )
        )
    return models


def train_and_evaluate(X_train, y_train, X_test, y_test, feature_names):
    """Trenuje wszystkie modele i zwraca wyniki + predykcje."""
    models = build_models()
    results = {}
    predictions = {}

    for name, pipeline in models.items():
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        results[name] = {
            "MAE":  float(mean_absolute_error(y_test, y_pred)),
            "RMSE": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "R2":   float(r2_score(y_test, y_pred)),
        }
        predictions[name] = (pipeline, y_pred)
        logging.info(
            f"  {name}: MAE={results[name]['MAE']:.3f} W | "
            f"RMSE={results[name]['RMSE']:.3f} W | R2={results[name]['R2']:.4f}"
        )

    return results, predictions


# ---------------------------------------------------------------------------
# Wykresy
# ---------------------------------------------------------------------------
def plot_errors(results, variant_tag, out_dir):
    """Slupkowy wykres MAE i RMSE dla wszystkich modeli."""
    sns.set_style("whitegrid")
    model_names = list(results.keys())
    mae_vals  = [results[m]["MAE"]  for m in model_names]
    rmse_vals = [results[m]["RMSE"] for m in model_names]
    x = np.arange(len(model_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    r1 = ax.bar(x - width / 2, mae_vals,  width, label="MAE [W]",  color="steelblue")
    r2 = ax.bar(x + width / 2, rmse_vals, width, label="RMSE [W]", color="tomato")
    ax.set_ylabel("Blad predykcji [W]")
    ax.set_title(f"Porownanie MAE i RMSE – Wariant {variant_tag}")
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, rotation=10, ha="right")
    ax.legend()
    ax.bar_label(r1, fmt="%.2f", padding=3, fontsize=8)
    ax.bar_label(r2, fmt="%.2f", padding=3, fontsize=8)
    plt.tight_layout()
    path = out_dir / f"porownanie_bledow_{variant_tag}.png"
    plt.savefig(path, dpi=300)
    plt.close()
    logging.info(f"Wykres zapisany: {path}")


def plot_pred_vs_actual(y_test, y_pred, model_name, variant_tag, out_dir):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(y_test, y_pred, alpha=0.5, edgecolors="white", linewidths=0.3, s=40, color="steelblue")
    lim_min = min(float(y_test.min()), float(y_pred.min())) - 5
    lim_max = max(float(y_test.max()), float(y_pred.max())) + 5
    ax.plot([lim_min, lim_max], [lim_min, lim_max], "r--", lw=1.5, label="Idealna predykcja")
    ax.set_xlabel("Rzeczywiste FTP [W]")
    ax.set_ylabel("Przewidywane FTP [W]")
    ax.set_title(f"Rzeczywiste vs Przewidywane FTP\n{model_name} – Wariant {variant_tag}")
    ax.legend()
    plt.tight_layout()
    path = out_dir / f"rzeczywiste_vs_przewidywane_{variant_tag}.png"
    plt.savefig(path, dpi=300)
    plt.close()
    logging.info(f"Wykres zapisany: {path}")


def plot_residuals(y_test, y_pred, model_name, variant_tag, out_dir):
    errors = np.array(y_test) - np.array(y_pred)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(errors, kde=True, bins=40, color="mediumorchid", ax=ax)
    ax.axvline(0, color="red", linestyle="--", lw=1.5, label="Blad = 0")
    ax.set_xlabel("Blad predykcji (Rzeczywiste – Przewidywane) [W]")
    ax.set_ylabel("Czestotliwosc")
    ax.set_title(f"Rozklad bledow predykcji – {model_name} – Wariant {variant_tag}")
    ax.legend()
    plt.tight_layout()
    path = out_dir / f"rozklad_bledow_{variant_tag}.png"
    plt.savefig(path, dpi=300)
    plt.close()
    logging.info(f"Wykres zapisany: {path}")


def plot_feature_importance(pipeline, feature_names, model_name, variant_tag, out_dir):
    model = pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        logging.info(f"Model {model_name} nie posiada feature_importances_ – pomijam wykres.")
        return
    importances = model.feature_importances_
    idx = np.argsort(importances)
    fig, ax = plt.subplots(figsize=(10, max(4, len(feature_names) * 0.4 + 1)))
    ax.barh(range(len(idx)), importances[idx], color="teal", align="center")
    ax.set_yticks(range(len(idx)))
    ax.set_yticklabels([feature_names[i] for i in idx], fontsize=9)
    ax.set_xlabel("Wzgledna waznosc cechy")
    ax.set_title(f"Waznosc cech – {model_name} – Wariant {variant_tag}")
    plt.tight_layout()
    path = out_dir / f"waznosc_cech_{variant_tag}.png"
    plt.savefig(path, dpi=300)
    plt.close()
    logging.info(f"Wykres zapisany: {path}")


# ---------------------------------------------------------------------------
# Glowna logika
# ---------------------------------------------------------------------------
def run_variant(df, feature_cols, groups, variant_tag, out_dir):
    logging.info(f"\n{'='*60}")
    logging.info(f"WARIANT {variant_tag}  |  Cechy: {feature_cols}")
    logging.info(f"{'='*60}")

    X = df[feature_cols].copy()
    y = df["ftp_label"].copy()

    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=RANDOM_SEED)
    train_idx, test_idx = next(gss.split(X, y, groups))
    X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
    X_test,  y_test  = X.iloc[test_idx],  y.iloc[test_idx]

    logging.info(
        f"Zbior treningowy: {len(X_train)} obs. | "
        f"Zbior testowy: {len(X_test)} obs. | "
        f"Zawodnicy unikalni: {groups.nunique()}"
    )

    results, predictions = train_and_evaluate(X_train, y_train, X_test, y_test, feature_cols)

    best_name = min(results, key=lambda k: results[k]["MAE"])
    best_pipeline, best_preds = predictions[best_name]

    # Wykresy
    plot_errors(results, variant_tag, out_dir)
    plot_pred_vs_actual(y_test, best_preds, best_name, variant_tag, out_dir)
    plot_residuals(y_test, best_preds, best_name, variant_tag, out_dir)
    plot_feature_importance(best_pipeline, feature_cols, best_name, variant_tag, out_dir)

    # JSON z wynikami wariantu
    report = {
        "variant": variant_tag,
        "feature_cols": feature_cols,
        "leakage_removed": LEAKAGE_COLS if variant_tag == "B" else [],
        "best_model": best_name,
        "results": results,
        "dataset": {
            "num_athletes": int(groups.nunique()),
            "train_size": int(len(X_train)),
            "test_size": int(len(X_test)),
        },
    }
    json_path = out_dir / f"ml_results_{variant_tag}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    logging.info(f"Wyniki JSON: {json_path}")

    return results


def save_combined_csv(results_A, results_B, results_dir):
    rows = []
    for model_name in results_A:
        rows.append({
            "Wariant": "A (z mmp_20min – data leakage)",
            "Model": model_name,
            "MAE [W]": round(results_A[model_name]["MAE"], 4),
            "RMSE [W]": round(results_A[model_name]["RMSE"], 4),
            "R2": round(results_A[model_name]["R2"], 6),
        })
    for model_name in results_B:
        rows.append({
            "Wariant": "B (bez mmp_20min – rzetelny)",
            "Model": model_name,
            "MAE [W]": round(results_B[model_name]["MAE"], 4),
            "RMSE [W]": round(results_B[model_name]["RMSE"], 4),
            "R2": round(results_B[model_name]["R2"], 6),
        })
    df_out = pd.DataFrame(rows)
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / "model_metrics.csv"
    df_out.to_csv(path, index=False, encoding="utf-8")
    logging.info(f"\nPorownanie wariantow zapisane: {path}")
    print("\n" + df_out.to_string(index=False))
    return df_out


def main():
    processed_dir = Path("data/processed")
    results_dir   = Path("results")
    dataset_path  = processed_dir / "features_ftp_dataset.csv"

    if not dataset_path.exists():
        logging.error(f"Brak pliku {dataset_path}. Uruchom najpierw build_features_dataset.py.")
        return

    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=["ftp_label", "athlete_id"])

    logging.info(f"Wczytano dataset: {len(df)} obserwacji, {df['athlete_id'].nunique()} zawodnikow")
    logging.info(f"Kolumny w datasecie: {list(df.columns)}")

    groups = df["athlete_id"]

    # Wszystkie dostepne cechy numeryczne (bez kolumn systemowych i etykiety)
    all_numeric = [
        c for c in df.columns
        if c not in ALWAYS_DROP and df[c].dtype in [np.float64, np.int64, float, int]
    ]
    logging.info(f"\nWszystkie cechy numeryczne: {all_numeric}")

    # Sprawdzenie wycieku
    if "mmp_20min" in all_numeric:
        logging.warning(
            "DATA LEAKAGE WYKRYTY: 'mmp_20min' jest cecha wejsciowa, "
            "a ftp_label = 0.95 * mmp_20min. "
            "Wariant B usunie te kolumne."
        )

    # --- Wariant A: wszystkie cechy (w tym mmp_20min) ---
    features_A = all_numeric
    results_A = run_variant(df, features_A, groups, "A", processed_dir)

    # --- Wariant B: bez cech powodujacych wyciek ---
    features_B = [c for c in all_numeric if c not in LEAKAGE_COLS]
    if not features_B:
        logging.error("Wariant B nie ma zadnych cech po usunieciu kolumn wycieku!")
        return
    results_B = run_variant(df, features_B, groups, "B", processed_dir)

    # Zbiorczy CSV
    save_combined_csv(results_A, results_B, results_dir)

    logging.info("\nGotowe. Sprawdz data/processed/ i results/model_metrics.csv")


if __name__ == "__main__":
    main()
