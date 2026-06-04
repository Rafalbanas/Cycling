import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit
from xgboost import XGBRegressor
import shap

def translate_feature_names(df_cols):
    # Map feature names to Polish descriptions if needed, 
    # but keeping original column names is usually preferred in ML to match the dataset.
    # We will use the original feature names so they directly correspond to the methodology.
    pass

def main():
    data_path = Path("/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/features_ftp_dataset_rich_partial.csv")
    figures_dir = Path("figures/experiments_partial")
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    print("1. Wczytywanie danych...")
    df = pd.read_csv(data_path)
    df = df.dropna(subset=["ftp_label", "athlete_id"])
    
    athlete_col = "athlete_id"
    target_col = "ftp_label"
    
    print("2. Definiowanie cech dla Wariantu C...")
    exclude_cols = [athlete_col, target_col, "date", "file_name", "uuid", "activity_id", "source_path", "source_zip"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    base_features = [c for c in numeric_cols if c not in exclude_cols and not c.startswith("ftp_")]
    var_C_features = [c for c in base_features if not c.startswith("mmp_")]
    
    print(f"Liczba cech wariantu C: {len(var_C_features)}")
    
    print("3. Podział danych GroupShuffleSplit po athlete_id...")
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(df, groups=df[athlete_col]))
    
    df_train = df.iloc[train_idx]
    df_test = df.iloc[test_idx]
    
    X_train = df_train[var_C_features]
    y_train = df_train[target_col]
    X_test = df_test[var_C_features]
    y_test = df_test[target_col]
    
    print("4. Trenowanie modelu XGBoost (Wariant C)...")
    model = XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror', n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("5. Pobieranie próbki testowej do analizy SHAP...")
    # Sample 1500 records from the test set
    X_test_sample = X_test.sample(n=1500, random_state=42)
    
    print("6. Obliczanie wartości SHAP (TreeExplainer)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test_sample)
    
    print("7. Generowanie wykresów...")
    
    # 7.1. beeswarm plot (Summary Plot)
    plt.figure(figsize=(10, 8))
    shap.plots.beeswarm(shap_values, max_display=15, show=False)
    plt.title("Wykres beeswarm SHAP (Wariant C - XGBoost)", fontsize=12, pad=15)
    plt.xlabel("Wartość SHAP (wpływ na predykcję FTP [W])", fontsize=10)
    plt.ylabel("Cecha telemetryczna", fontsize=10)
    
    # Customize colorbar label if it exists
    fig = plt.gcf()
    for ax in fig.axes:
        if ax.get_label() == "colorbar":
            ax.set_ylabel("Wartość cechy (Niska -> Wysoka)", fontsize=9)
            
    plt.tight_layout()
    summary_path = figures_dir / "shap_summary_variant_c.png"
    plt.savefig(summary_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Zapisano beeswarm plot do: {summary_path}")
    
    # 7.2. bar plot (Mean Absolute SHAP)
    plt.figure(figsize=(10, 8))
    shap.plots.bar(shap_values, max_display=15, show=False)
    plt.title("Wpływ cech według średniej bezwzględnej wartości SHAP (Wariant C - XGBoost)", fontsize=12, pad=15)
    plt.xlabel("Średnia bezwzględna wartość SHAP (|SHAP value| [W])", fontsize=10)
    plt.ylabel("Cecha telemetryczna", fontsize=10)
    plt.tight_layout()
    bar_path = figures_dir / "shap_bar_variant_c.png"
    plt.savefig(bar_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Zapisano bar plot do: {bar_path}")
    
    # 8. Analiza i wyświetlenie najważniejszych cech
    # Calculate mean absolute SHAP values for each feature
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    df_importance = pd.DataFrame({
        "Feature": var_C_features,
        "Mean_Abs_SHAP": mean_abs_shap
    }).sort_values("Mean_Abs_SHAP", ascending=False)
    
    print("\n--- NAJWAŻNIEJSZE CECHY WEDŁUG SHAP (Wariant C) ---")
    print(df_importance.head(15).to_string(index=False))
    
    # Save importance as CSV in results directory
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    df_importance.to_csv(results_dir / "shap_importance_variant_c.csv", index=False)
    print(f"\nZapisano ważność cech SHAP do: {results_dir / 'shap_importance_variant_c.csv'}")

if __name__ == "__main__":
    main()
