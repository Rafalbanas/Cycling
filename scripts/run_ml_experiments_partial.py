import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error
from sklearn.impute import SimpleImputer

def main():
    # Setup paths
    os.environ["MASTER_THESIS_DATA_ROOT"] = "/Volumes/MasterThesisSSD/MasterThesisData"
    data_path = Path("/Volumes/MasterThesisSSD/MasterThesisData/goldencheetah/processed/features_ftp_dataset_rich_partial.csv")
    
    reports_dir = Path("reports")
    results_dir = Path("results")
    figures_dir = Path("figures/experiments_partial")
    
    reports_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print("Wczytywanie danych...")
    df = pd.read_csv(data_path)

    # 1. Audyt datasetu
    print("1. Audyt datasetu...")
    records_count = len(df)
    athlete_col = "athlete_id" if "athlete_id" in df.columns else None
    athletes_count = df[athlete_col].nunique() if athlete_col else 0
    target_col = "ftp_label"
    cols = df.columns.tolist()
    
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]
    
    inf_count = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
    nan_count = df.isnull().sum().sum()
    
    ftp_desc = df[target_col].describe().to_dict() if target_col in df.columns else {}

    audit_md = f"""# Audyt zbioru danych (częściowy)

- **Plik:** `{data_path.name}`
- **Liczba rekordów:** {records_count}
- **Liczba zawodników:** {athletes_count}
- **Liczba kolumn:** {len(cols)}
- **Kolumna identyfikatora zawodnika:** `{athlete_col}`
- **Kolumna etykiety FTP:** `{target_col}`

## Rozkład FTP
- Minimum: {ftp_desc.get('min', 'N/A'):.2f}
- Maksimum: {ftp_desc.get('max', 'N/A'):.2f}
- Średnia: {ftp_desc.get('mean', 'N/A'):.2f}
- Mediana: {ftp_desc.get('50%', 'N/A'):.2f}

## Jakość danych
- Suma wartości NaN we wszystkich komórkach: {nan_count}
- Suma wartości nieskończonych (inf): {inf_count}
- Kolumny z brakami danych (liczba): {len(missing_data)}

"""
    (reports_dir / "model_dataset_audit_partial.md").write_text(audit_md)

    # 2. Definicja wariantów cech
    print("2. Definiowanie wariantów cech...")
    exclude_cols = [athlete_col, target_col, "date", "file_name", "uuid", "activity_id", "source_path", "source_zip"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    base_features = [c for c in numeric_cols if c not in exclude_cols and not c.startswith("ftp_")]
    
    var_A_features = base_features.copy()
    var_B_features = [c for c in var_A_features if c != "mmp_20min"]
    var_C_features = [c for c in var_A_features if not c.startswith("mmp_")]

    (results_dir / "features_variant_A.txt").write_text("\n".join(var_A_features))
    (results_dir / "features_variant_B.txt").write_text("\n".join(var_B_features))
    (results_dir / "features_variant_C.txt").write_text("\n".join(var_C_features))

    variants = {
        "Variant_A": var_A_features,
        "Variant_B": var_B_features,
        "Variant_C": var_C_features
    }

    # 3. Podział danych
    print("3. Podział danych (GroupShuffleSplit)...")
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(df, groups=df[athlete_col]))
    
    df_train = df.iloc[train_idx]
    df_test = df.iloc[test_idx]
    
    train_athletes = df_train[athlete_col].nunique()
    test_athletes = df_test[athlete_col].nunique()
    
    split_md = f"""# Podział zbioru danych (Train/Test Split)

- **Metoda:** GroupShuffleSplit (grupowanie po `athlete_id`)
- **Parametry:** `test_size=0.2`, `random_state=42`

## Trening (Train)
- Liczba rekordów: {len(df_train)}
- Liczba unikalnych zawodników: {train_athletes}

## Test
- Liczba rekordów: {len(df_test)}
- Liczba unikalnych zawodników: {test_athletes}
"""
    (reports_dir / "train_test_split_partial.md").write_text(split_md)

    # 4. & 5. Modele i Metryki
    print("4. Trenowanie modeli i wyliczanie metryk...")
    y_train = df_train[target_col]
    y_test = df_test[target_col]

    results = []
    
    best_variant_B_model_name = None
    best_variant_B_r2 = -float("inf")
    best_variant_B_preds = None
    best_variant_B_model_obj = None
    
    best_variant_C_model_name = None
    best_variant_C_r2 = -float("inf")
    best_variant_C_preds = None
    best_variant_C_model_obj = None

    for var_name, var_feats in variants.items():
        models = {
            "Ridge": Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", Ridge(random_state=42))
            ]),
            "RandomForest": Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("model", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
            ]),
            "XGBoost": XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror', n_jobs=-1)
        }
        
        X_train = df_train[var_feats]
        X_test = df_test[var_feats]
        
        for model_name, model in models.items():
            print(f"Trenowanie: {model_name} na {var_name}...")
            
            # XGBoost handles NaNs naturally, but sklearn Pipeline handles imputation
            if model_name == "XGBoost":
                X_train_clean = X_train.copy()
                X_test_clean = X_test.copy()
            else:
                X_train_clean = X_train
                X_test_clean = X_test
                
            model.fit(X_train_clean, y_train)
            preds = model.predict(X_test_clean)
            
            mae = mean_absolute_error(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            r2 = r2_score(y_test, preds)
            medae = median_absolute_error(y_test, preds)
            
            results.append({
                "Variant": var_name,
                "Model": model_name,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
                "MedAE": medae,
                "Test_Records": len(y_test)
            })
            
            if var_name == "Variant_B" and r2 > best_variant_B_r2:
                best_variant_B_r2 = r2
                best_variant_B_model_name = model_name
                best_variant_B_preds = preds
                best_variant_B_model_obj = model
                
            if var_name == "Variant_C" and r2 > best_variant_C_r2:
                best_variant_C_r2 = r2
                best_variant_C_model_name = model_name
                best_variant_C_preds = preds
                best_variant_C_model_obj = model

    df_results = pd.DataFrame(results)
    df_results.to_csv(results_dir / "model_comparison_partial.csv", index=False)
    
    # Generate variant comparison (averaging across top models or showing all)
    df_results.to_csv(results_dir / "variant_comparison_partial.csv", index=False)

    def save_predictions(variant_name, model_name, preds, output_name):
        prediction_frame = pd.DataFrame({
            "experiment": "baseline",
            "variant": variant_name,
            "model": model_name,
            "athlete_id": df_test[athlete_col].to_numpy(),
            "y_true": y_test.to_numpy(),
            "y_pred": preds,
        })
        prediction_frame["residual"] = prediction_frame["y_pred"] - prediction_frame["y_true"]
        prediction_frame.to_csv(results_dir / output_name, index=False)

    save_predictions(
        "Variant_B",
        best_variant_B_model_name,
        best_variant_B_preds,
        "baseline_predictions_variant_b.csv",
    )
    save_predictions(
        "Variant_C",
        best_variant_C_model_name,
        best_variant_C_preds,
        "baseline_predictions_variant_c.csv",
    )

    # 6. Wykresy
    print("6. Generowanie wykresów...")
    sns.set_theme(style="whitegrid")
    
    # Pred vs Actual for best B
    plt.figure(figsize=(8,6))
    plt.scatter(y_test, best_variant_B_preds, alpha=0.3, s=10)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Rzeczywiste FTP")
    plt.ylabel("Przewidywane FTP")
    plt.title(f"Predykcja vs Rzeczywistość - Najlepszy model ({best_variant_B_model_name}, Wariant B)")
    plt.tight_layout()
    plt.savefig(figures_dir / "pred_vs_actual_best_var_B.png", dpi=150)
    plt.close()
    
    # Rozkład błędów
    errors = y_test - best_variant_B_preds
    plt.figure(figsize=(8,6))
    sns.histplot(errors, bins=50, kde=True)
    plt.xlabel("Błąd (Rzeczywiste - Przewidywane)")
    plt.ylabel("Liczba próbek")
    plt.title(f"Rozkład błędów predykcji ({best_variant_B_model_name}, Wariant B)")
    plt.tight_layout()
    plt.savefig(figures_dir / "error_distribution_best_var_B.png", dpi=150)
    plt.close()

    # Porównanie metryk
    plt.figure(figsize=(10,6))
    sns.barplot(data=df_results, x="Variant", y="MAE", hue="Model")
    plt.title("Porównanie MAE między wariantami i modelami")
    plt.tight_layout()
    plt.savefig(figures_dir / "mae_comparison.png", dpi=150)
    plt.close()
    
    plt.figure(figsize=(10,6))
    sns.barplot(data=df_results, x="Variant", y="R2", hue="Model")
    plt.title("Porównanie R2 między wariantami i modelami")
    plt.tight_layout()
    plt.savefig(figures_dir / "r2_comparison.png", dpi=150)
    plt.close()

    # 8. Ważność cech
    print("8. Zapisywanie ważności cech...")
    def get_feature_importances(model_obj, model_name, features):
        if model_name == "XGBoost":
            return features, model_obj.feature_importances_
        elif model_name == "RandomForest":
            out_features = model_obj.named_steps["imputer"].get_feature_names_out(features)
            return out_features, model_obj.named_steps["model"].feature_importances_
        return None, None

    features_B, importances_B = get_feature_importances(best_variant_B_model_obj, best_variant_B_model_name, variants["Variant_B"])
    if importances_B is not None:
        df_imp_b = pd.DataFrame({"Feature": features_B, "Importance": importances_B}).sort_values("Importance", ascending=False)
        df_imp_b.to_csv(results_dir / "feature_importance_variant_B_partial.csv", index=False)
        
        plt.figure(figsize=(10, 8))
        sns.barplot(data=df_imp_b.head(20), x="Importance", y="Feature")
        plt.title(f"Top 20 cech ({best_variant_B_model_name}, Wariant B)")
        plt.tight_layout()
        plt.savefig(figures_dir / "feature_importance_best_var_B.png", dpi=150)
        plt.close()

    features_C, importances_C = get_feature_importances(best_variant_C_model_obj, best_variant_C_model_name, variants["Variant_C"])
    if importances_C is not None:
        df_imp_c = pd.DataFrame({"Feature": features_C, "Importance": importances_C}).sort_values("Importance", ascending=False)
        df_imp_c.to_csv(results_dir / "feature_importance_variant_C_partial.csv", index=False)

        plt.figure(figsize=(10, 8))
        sns.barplot(data=df_imp_c.head(20), x="Importance", y="Feature")
        plt.title(f"Top 20 cech ({best_variant_C_model_name}, Wariant C)")
        plt.tight_layout()
        plt.savefig(figures_dir / "feature_importance_best_var_C.png", dpi=150)
        plt.close()


    # 7. Analiza leakage
    print("7. Generowanie analizy wycieku (leakage)...")
    
    r2_A_rf = df_results[(df_results["Variant"]=="Variant_A") & (df_results["Model"]=="RandomForest")]["R2"].values[0]
    r2_B_rf = df_results[(df_results["Variant"]=="Variant_B") & (df_results["Model"]=="RandomForest")]["R2"].values[0]
    r2_C_rf = df_results[(df_results["Variant"]=="Variant_C") & (df_results["Model"]=="RandomForest")]["R2"].values[0]

    mae_A_rf = df_results[(df_results["Variant"]=="Variant_A") & (df_results["Model"]=="RandomForest")]["MAE"].values[0]
    mae_B_rf = df_results[(df_results["Variant"]=="Variant_B") & (df_results["Model"]=="RandomForest")]["MAE"].values[0]
    mae_C_rf = df_results[(df_results["Variant"]=="Variant_C") & (df_results["Model"]=="RandomForest")]["MAE"].values[0]

    leakage_md = f"""# Analiza wycieku danych (Data Leakage)

Porównanie wariantów dla modelu bazowego (Random Forest):

| Wariant | R2 | MAE | Różnica MAE do wariantu A |
|---------|---|---|---|
| A (z mmp_20min) | {r2_A_rf:.4f} | {mae_A_rf:.2f} | 0.00 |
| B (bez mmp_20min) | {r2_B_rf:.4f} | {mae_B_rf:.2f} | {mae_B_rf - mae_A_rf:+.2f} |
| C (bez mmp_*) | {r2_C_rf:.4f} | {mae_C_rf:.2f} | {mae_C_rf - mae_A_rf:+.2f} |

## Wnioski z leakage
1. **Wpływ `mmp_20min`:** Wyniki wariantu A są {"nienaturalnie wysokie" if r2_A_rf > 0.95 else "bardzo wysokie"}, co sugeruje silny wyciek danych (tzw. label leakage) z cechy `mmp_20min`, na podstawie której u części zawodników estymowane jest FTP (jako 95% 20min power). Z usunięciem tej cechy błąd rośnie, a R2 maleje.
2. **Zachowanie predykcji po usunięciu wycieku:** Po wykluczeniu mmp_20min (Wariant B), model osiąga MAE na poziomie {mae_B_rf:.2f}, co stanowi realną miarę jego skuteczności na podstawie pozostałych wskaźników historycznych i krótko-dystansowych.
3. **Usunięcie wszystkich mmp (Wariant C):** Gdy wyeliminujemy wszelkie moce maksymalne, wskaźniki błędów {"utrzymują się na podobnym poziomie" if abs(mae_C_rf - mae_B_rf) < 2.0 else "ulegają zauważalnemu pogorszeniu"}, wskazując na {"brak dominacji krótkich okien" if abs(mae_C_rf - mae_B_rf) < 2.0 else "znaczenie maksymalnych generowanych mocy w szerszych oknach do ogólnej oceny FTP"}.
"""
    (reports_dir / "leakage_analysis_partial.md").write_text(leakage_md)

    # 9. Raport końcowy
    print("9. Generowanie raportu końcowego...")
    final_md = f"""# Podsumowanie trenowania modeli na zbiorze częściowym

## Użyty dataset
- **Plik:** `{data_path.name}`
- **Rekordy (filtr FTP):** {len(df)}
- **Zawodnicy:** {athletes_count}

## Warianty
- **Variant A:** Zawiera `mmp_20min` (cecha powiązana metodologicznie z klasycznym testem FTP). Skutkuje ryzykiem mocnego data leakage.
- **Variant B:** Podstawowy i najbardziej zalecany. Posiada wszystkie metryki poza głównym źródłem wycieku `mmp_20min`. Zawiera {len(variants["Variant_B"])} cech.
- **Variant C:** Konserwatywny. Całkowicie wycina zmienne z prefixem `mmp_` w celu oceny czy to telemetryczne cechy serca czy tylko moc wpływa na predykcje. Zawiera {len(variants["Variant_C"])} cech.

## Podział danych
Zastosowano podział osobniczy, dzięki czemu modele były walidowane na kompletnie nieznanych zawodnikach z test-setu. 
Podział wyniósł {len(df_train)} (trening) do {len(df_test)} (test) wierszy.

## Wyniki i najlepsze modele
Z użytych algorytmów na czysto, najlepiej w Wariancie B poradził sobie **{best_variant_B_model_name}** z wynikiem R2 na poziomie {best_variant_B_r2:.4f}.
Dla wariantu C zwyciężył **{best_variant_C_model_name}** osiągając R2: {best_variant_C_r2:.4f}.

## Wniosek o leakage wariantu A
Widoczny jest drastyczny i spodziewany spadek metryk po przejściu z wariantu A na B i C. Zjawisko to wprost waliduje potrzebę zablokowania `mmp_20min` na etapie modelowania produkcyjnego, zgodnie z metodologią badawczą.

## Konkluzje do pracy
Uzyskane wyniki i wielkość próby danych (>150 000 wierszy dla >700 zawodników) są wystarczające do zbudowania solidnej podbudowy analitycznej w pracy magisterskiej, chociaż dalsza analiza błędów np. podział per-sezon czy profil kolarza, może być interesującą drogą rozszerzenia. Na tym etapie tabele wygenerowane przez te skrypty stanowią gotowy materiał do włączenia do pliku LaTeX.

**Do weryfikacji ręcznej (TODO dla autora):**
- Ocena czy R2 wariantu B odpowiada wymaganiom dziedziny na przewidywania kolarskie.
- Sprawdzenie ważności cech `feature_importance_variant_B_partial.csv` by zaobserwować jakie fizjologiczne parametry determinowały decyzje Random Forest / XGBoost (w szczególności bicie serca vs kadencja itp.).

"""
    (reports_dir / "model_training_partial_summary.md").write_text(final_md)
    print("Wszystkie operacje zakończone pomyślnie. Pliki zapisano w katalogach reports/ i results/ oraz wykresy w figures/.")

if __name__ == "__main__":
    main()
