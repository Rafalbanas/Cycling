import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit
from xgboost import XGBRegressor
import shap

def run_shap_pipeline(data_path, variant, output_dir, csv_path, beeswarm_name, bar_name, sample_size=1500):
    data_path = Path(data_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n==================================================")
    print(f"Uruchamianie analizy SHAP dla Wariantu {variant}")
    print(f"Dane wejściowe: {data_path}")
    print(f"==================================================")
    
    if not data_path.exists():
        print(f"BŁĄD: Plik {data_path} nie istnieje!")
        return
        
    print("1. Wczytywanie danych...")
    df = pd.read_csv(data_path)
    df = df.dropna(subset=["ftp_label", "athlete_id"])
    
    athlete_col = "athlete_id"
    target_col = "ftp_label"
    
    print(f"2. Definiowanie cech dla Wariantu {variant}...")
    exclude_cols = [athlete_col, target_col, "date", "file_name", "uuid", "activity_id", "source_path", "source_zip"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    base_features = [c for c in numeric_cols if c not in exclude_cols and not c.startswith("ftp_")]
    
    if variant == "C":
        features = [c for c in base_features if not c.startswith("mmp_")]
    elif variant == "B":
        # Wariant B: usuwamy tylko mmp_20min
        features = [c for c in base_features if c != "mmp_20min"]
    else:
        raise ValueError(f"Nieznany wariant: {variant}")
        
    print(f"Liczba cech: {len(features)}")
    
    print("3. Podział danych GroupShuffleSplit po athlete_id...")
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(df, groups=df[athlete_col]))
    
    df_train = df.iloc[train_idx]
    df_test = df.iloc[test_idx]
    
    X_train = df_train[features]
    y_train = df_train[target_col]
    X_test = df_test[features]
    y_test = df_test[target_col]
    
    print(f"Rozmiar zbioru uczącego: {X_train.shape}, testowego: {X_test.shape}")
    
    print(f"4. Trenowanie modelu XGBoost (Wariant {variant})...")
    model = XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror', n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("5. Pobieranie próbki testowej do analizy SHAP...")
    actual_sample_size = min(len(X_test), sample_size)
    X_test_sample = X_test.sample(n=actual_sample_size, random_state=42)
    print(f"Użyta liczba obserwacji testowych do SHAP: {actual_sample_size}")
    
    print("6. Obliczanie wartości SHAP (TreeExplainer)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test_sample)
    
    print("7. Generowanie wykresów...")
    
    # 7.1. beeswarm plot (Summary Plot)
    plt.figure(figsize=(10, 8))
    shap.plots.beeswarm(shap_values, max_display=15, show=False)
    plt.title(f"Wykres beeswarm SHAP (Wariant {variant} - XGBoost)", fontsize=12, pad=15)
    plt.xlabel("Wartość SHAP (wpływ na predykcję FTP [W])", fontsize=10)
    plt.ylabel("Cecha telemetryczna", fontsize=10)
    
    # Dostosowanie etykiety paska kolorów
    fig = plt.gcf()
    for ax in fig.axes:
        if ax.get_label() == "colorbar":
            ax.set_ylabel("Wartość cechy (Niska -> Wysoka)", fontsize=9)
            
    plt.tight_layout()
    summary_path = output_dir / beeswarm_name
    plt.savefig(summary_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Zapisano beeswarm plot do: {summary_path}")
    
    # 7.2. bar plot (Mean Absolute SHAP)
    plt.figure(figsize=(10, 8))
    shap.plots.bar(shap_values, max_display=15, show=False)
    plt.title(f"Wpływ cech według średniej bezwzględnej wartości SHAP (Wariant {variant} - XGBoost)", fontsize=12, pad=15)
    plt.xlabel("Średnia bezwzględna wartość SHAP (|SHAP value| [W])", fontsize=10)
    plt.ylabel("Cecha telemetryczna", fontsize=10)
    plt.tight_layout()
    bar_path = output_dir / bar_name
    plt.savefig(bar_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Zapisano bar plot do: {bar_path}")
    
    # 8. Zapisywanie ważności cech
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    df_importance = pd.DataFrame({
        "Feature": features,
        "Mean_Abs_SHAP": mean_abs_shap
    }).sort_values("Mean_Abs_SHAP", ascending=False)
    
    print(f"\n--- NAJWAŻNIEJSZE CECHY WEDŁUG SHAP (Wariant {variant}) ---")
    print(df_importance.head(15).to_string(index=False))
    
    df_importance.to_csv(csv_path, index=False)
    print(f"\nZapisano ważność cech SHAP do: {csv_path}")

def main():
    # 1. Wariant B na zbiorze bazowym
    run_shap_pipeline(
        data_path="/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/features_ftp_dataset_rich_partial.csv",
        variant="B",
        output_dir="figures/experiments_partial",
        csv_path="results/shap_importance_variant_b.csv",
        beeswarm_name="shap_summary_variant_b.png",
        bar_name="shap_bar_variant_b.png",
        sample_size=1500
    )
    
    # 2. Wariant C na próbie kontrolnej 5000 archiwów ZIP
    run_shap_pipeline(
        data_path="/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/control_5000/outputs/features_ftp_control_5000.csv",
        variant="C",
        output_dir="figures/control_5000",
        csv_path="experiments/control_5000/results/shap_importance_variant_c_control_5000.csv",
        beeswarm_name="shap_summary_variant_c_control_5000.png",
        bar_name="shap_bar_variant_c_control_5000.png",
        sample_size=1500
    )

if __name__ == "__main__":
    main()
