import os
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_model_pipeline(model, requires_scaling=False):
    steps = [('imputer', SimpleImputer(strategy='median'))]
    if requires_scaling:
        steps.append(('scaler', StandardScaler()))
    steps.append(('model', model))
    return Pipeline(steps)

def main():
    processed_dir = Path("data/processed")
    dataset_path = processed_dir / "features_ftp_dataset.csv"
    
    if not dataset_path.exists():
        logging.error(f"Plik {dataset_path} nie istnieje.")
        return
        
    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=['ftp_label', 'athlete_id'])
    
    features = [
        'duration_sec', 'mean_power', 'max_power', 'median_power', 'std_power',
        'mean_heart_rate', 'max_heart_rate', 'median_heart_rate', 'std_heart_rate',
        'mean_cadence', 'max_cadence', 'mmp_30s', 'mmp_1min', 'mmp_3min', 'mmp_5min',
        'mmp_10min', 'mmp_20min', 'power_hr_ratio', 'hr_drift_simple',
        'time_power_zero', 'percent_power_zero'
    ]
    features = [f for f in features if f in df.columns]
    
    X = df[features]
    y = df['ftp_label']
    groups = df['athlete_id']
    
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups))
    
    X_train, y_train, groups_train = X.iloc[train_idx], y.iloc[train_idx], groups.iloc[train_idx]
    X_test, y_test, groups_test = X.iloc[test_idx], y.iloc[test_idx], groups.iloc[test_idx]
    
    models = {
        'Ridge Regression': create_model_pipeline(Ridge(alpha=1.0), requires_scaling=True),
        'Random Forest': create_model_pipeline(RandomForestRegressor(n_estimators=100, random_state=42))
    }
    
    if XGBRegressor:
        models['XGBoost'] = create_model_pipeline(XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror'))
    
    results = {}
    predictions = {}
    
    for name, pipeline in models.items():
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        predictions[name] = y_pred
        
    best_model_name = min(results, key=lambda k: results[k]['MAE'])
    
    # 1. Wykres: Porównanie MAE/RMSE
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    model_names = list(results.keys())
    mae_values = [results[m]['MAE'] for m in model_names]
    rmse_values = [results[m]['RMSE'] for m in model_names]
    x = np.arange(len(model_names))
    width = 0.35
    rects1 = ax.bar(x - width/2, mae_values, width, label='MAE [W]', color='skyblue')
    rects2 = ax.bar(x + width/2, rmse_values, width, label='RMSE [W]', color='salmon')
    ax.set_ylabel('Błąd predykcji [Wat]')
    ax.set_title('Porównanie błędów (MAE i RMSE) dla testowanych modeli')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names)
    ax.legend()
    ax.bar_label(rects1, fmt='%.1f', padding=3)
    ax.bar_label(rects2, fmt='%.1f', padding=3)
    plt.tight_layout()
    plt.savefig(processed_dir / "porownanie_bledow.png", dpi=300)
    plt.close()
    
    # 2. Wykres: Rzeczywiste vs Przewidywane
    best_preds = predictions[best_model_name]
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_test, best_preds, alpha=0.6, edgecolors='w', s=60)
    min_val = min(y_test.min(), best_preds.min()) - 10
    max_val = max(y_test.max(), best_preds.max()) + 10
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Idealna predykcja')
    ax.set_xlabel('Rzeczywiste FTP [W]')
    ax.set_ylabel('Przewidywane FTP [W]')
    ax.set_title(f'Rzeczywiste vs Przewidywane FTP ({best_model_name})')
    ax.legend()
    plt.tight_layout()
    plt.savefig(processed_dir / "rzeczywiste_vs_przewidywane.png", dpi=300)
    plt.close()
    
    # 3. Wykres: Rozkład błędów
    errors = y_test - best_preds
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(errors, kde=True, color='purple', bins=30, ax=ax)
    ax.axvline(x=0, color='red', linestyle='--', label='Błąd zero')
    ax.set_xlabel('Błąd predykcji (Rzeczywiste - Przewidywane) [W]')
    ax.set_ylabel('Częstość')
    ax.set_title(f'Rozkład błędów predykcji ({best_model_name})')
    ax.legend()
    plt.tight_layout()
    plt.savefig(processed_dir / "rozklad_bledow.png", dpi=300)
    plt.close()
    
    # 4. Wykres: Ważność cech
    best_pipeline = models[best_model_name]
    actual_model = best_pipeline.named_steps['model']
    if hasattr(actual_model, 'feature_importances_'):
        importances = actual_model.feature_importances_
    else:
        importances = models['Random Forest'].named_steps['model'].feature_importances_
        
    indices = np.argsort(importances)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(range(len(indices)), importances[indices], color='teal', align='center')
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([features[i] for i in indices])
    ax.set_xlabel('Względna ważność cechy')
    ax.set_title(f'Ważność cech (Model: {best_model_name})')
    plt.tight_layout()
    plt.savefig(processed_dir / "waznosc_cech.png", dpi=300)
    plt.close()
        
    report_data = {
        'best_model': best_model_name,
        'results': results,
        'dataset': {
            'num_athletes': int(groups.nunique()),
            'train_size': int(len(X_train)),
            'test_size': int(len(X_test))
        }
    }
    with open(processed_dir / 'ml_results.json', 'w') as f:
        json.dump(report_data, f, indent=4)
        
if __name__ == "__main__":
    main()
