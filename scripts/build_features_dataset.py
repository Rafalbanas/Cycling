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
    # FIT i GPX wymagają bibliotek, których teraz nie instalujemy w locie, 
    # ale skrypt jest przygotowany pod ich przyszłą obsługę.
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
    if duration < 1800: return None 
    power = df['power']
    hr = df['heart_rate']
    features['mean_power'] = power.mean()
    features['mmp_20min'] = calculate_mmp(power, 1200)
    features['ftp_label'] = 0.95 * features['mmp_20min'] if pd.notna(features['mmp_20min']) else np.nan
    return features

def main():
    raw_dir, processed_dir = setup_directories()
    files = find_training_files(raw_dir)
    if not files:
        logging.info("Brak plików w data/raw/.")
        return
    dataset_rows = []
    for filepath in files:
        try:
            df = unify_columns(read_file(filepath))
            df = clean_data(df)
            f = extract_features(df)
            if f and pd.notna(f['ftp_label']):
                f['file_name'] = filepath.name
                f['athlete_id'] = filepath.parent.name
                dataset_rows.append(f)
        except Exception as e:
            continue
    if dataset_rows:
        pd.DataFrame(dataset_rows).to_csv(processed_dir / "features_ftp_dataset.csv", index=False)
        logging.info("Dataset zapisany.")

if __name__ == "__main__": main()
