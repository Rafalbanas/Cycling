import os
import sys
import glob
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, processed_dir

def find_training_files(raw_dir):
    supported_extensions = {'.csv', '.fit', '.gpx', '.tcx'}
    files = []
    for ext in supported_extensions:
        files.extend(raw_dir.rglob(f"*{ext}"))
        files.extend(raw_dir.rglob(f"*{ext.upper()}"))
    return list(set(files))

def read_file(filepath):
    ext = filepath.suffix.lower()
    if ext == '.csv':
        return pd.read_csv(filepath)
    raise ValueError(f"Obsługa {ext} wymaga dodatkowych bibliotek.")

def unify_columns(df):
    col_mapping = {
        'time': 'timestamp', 'date': 'timestamp', 'datetime': 'timestamp',
        'pwr': 'power', 'watts': 'power', 'power': 'power',
        'hr': 'heart_rate', 'bpm': 'heart_rate', 'heartrate': 'heart_rate', 'heart_rate': 'heart_rate',
        'cad': 'cadence', 'rpm': 'cadence', 'cadence': 'cadence'
    }
    df.columns = [str(col).lower().strip() for col in df.columns]
    df.rename(columns=col_mapping, inplace=True)
    expected_cols = ['timestamp', 'power', 'heart_rate', 'cadence']
    for col in expected_cols:
        if col not in df.columns:
            df[col] = np.nan
    return df

def clean_data(df):
    if 'power' in df.columns:
        df.loc[df['power'] < 0, 'power'] = np.nan
        df.loc[df['power'] > 2000, 'power'] = np.nan
    if 'heart_rate' in df.columns:
        df.loc[(df['heart_rate'] < 30) | (df['heart_rate'] > 220), 'heart_rate'] = np.nan
    df = df.interpolate(method='linear', limit=5)
    return df

def calculate_mmp(series, window_seconds):
    if series.isna().all() or len(series) < window_seconds:
        return np.nan
    return series.rolling(window=window_seconds, min_periods=int(window_seconds*0.8)).mean().max()

def extract_features(df):
    features = {}
    duration = len(df)
    features['duration_sec'] = duration
    
    if duration < 1800: 
        return {'error': 'Zbyt krótka sesja (< 30 min)'}
        
    if 'power' not in df.columns or df['power'].isna().all():
        return {'error': 'Brak danych o mocy (power)'}

    power = df['power']
    hr = df['heart_rate']
    features['mean_power'] = power.mean()
    features['mmp_20min'] = calculate_mmp(power, 1200)
    features['ftp_label'] = 0.95 * features['mmp_20min'] if pd.notna(features['mmp_20min']) else np.nan
    
    if pd.isna(features['ftp_label']):
        return {'error': 'Nie można obliczyć FTP (brak MMP20)'}
        
    return features

def generate_markdown_report(stats, df_features, processed_dir):
    report_path = processed_dir / "dataset_report.md"
    
    columns_list = "\n".join([f"- `{col}`" for col in df_features.columns]) if not df_features.empty else "Brak kolumn"
    
    report_content = f"""# Raport z Przetwarzania Zbioru Danych 🚴‍♂️

**Data wykonania:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

## 📊 Podsumowanie Przetwarzania

| Kategoria | Liczba sesji |
|-----------|--------------|
| 📂 **Znalezione pliki ogółem** | `{stats['total']}` |
| ✅ **Poprawnie przetworzone** | `{stats['success']}` |
| ❌ **Pominięte sesje** | `{stats['skipped']}` |

### ⚠️ Przyczyny Pominięcia
"""
    for reason, count in stats['errors'].items():
        report_content += f"- **{reason}:** {count} sesji\n"

    report_content += "\n## 📈 Statystyki wyekstrahowanego FTP\n\n"
    if not df_features.empty:
        report_content += f"- **Minimalne FTP:** `{df_features['ftp_label'].min():.1f} W`\n"
        report_content += f"- **Średnie FTP:** `{df_features['ftp_label'].mean():.1f} W`\n"
        report_content += f"- **Maksymalne FTP:** `{df_features['ftp_label'].max():.1f} W`\n"
    else:
        report_content += "Brak danych FTP do wyświetlenia.\n"

    report_content += f"\n## 📋 Wyekstrahowane Kolumny Cech\n\n{columns_list}\n"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    logging.info(f"Raport wygenerowany: {report_path}")

def main():
    raw_dir, processed_dir = setup_directories()
    files = find_training_files(raw_dir)
    if not files:
        logging.info("Brak plików w data/raw/.")
        return
        
    dataset_rows = []
    stats = {'total': len(files), 'success': 0, 'skipped': 0, 'errors': {}}
    
    for filepath in files:
        try:
            df = unify_columns(read_file(filepath))
            df = clean_data(df)
            f = extract_features(df)
            
            if 'error' in f:
                stats['skipped'] += 1
                stats['errors'][f['error']] = stats['errors'].get(f['error'], 0) + 1
            else:
                f['file_name'] = filepath.name
                f['athlete_id'] = filepath.parent.name
                dataset_rows.append(f)
                stats['success'] += 1
        except Exception as e:
            stats['skipped'] += 1
            error_msg = f"Błąd wczytywania: {type(e).__name__}"
            stats['errors'][error_msg] = stats['errors'].get(error_msg, 0) + 1
            continue
            
    df_features = pd.DataFrame(dataset_rows)
    if not df_features.empty:
        df_features.to_csv(processed_dir / "features_ftp_dataset.csv", index=False)
        logging.info("Dataset zapisany.")
        
    generate_markdown_report(stats, df_features, processed_dir)

if __name__ == "__main__": main()

