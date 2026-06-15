import os
import glob
import pandas as pd
import json
import shutil
from pathlib import Path

# Config
os.environ["MASTER_THESIS_DATA_ROOT"] = "/Volumes/MasterThesisSSD/MasterThesisData"
data_root = Path("/Volumes/MasterThesisSSD/MasterThesisData")
goldencheetah_root = data_root / "goldencheetah"
raw_zips_dir = goldencheetah_root / "raw_zips"
processed_dir = goldencheetah_root / "processed" / "batches"
reports_dir = Path("/Users/rafalbanas/Projects/Master_thesis/reports")
reports_dir.mkdir(parents=True, exist_ok=True)

# Datasets
unfiltered_out = goldencheetah_root / "processed" / "features_ftp_dataset_rich_partial_unfiltered.csv"
filtered_out = goldencheetah_root / "processed" / "features_ftp_dataset_rich_partial.csv"

def get_free_gib():
    return shutil.disk_usage(data_root).free / 1024**3

def generate_reports():
    # 1. Merge all batches
    batch_files = glob.glob(str(processed_dir / "features_batch_*.csv"))
    if not batch_files:
        print("No batch files found.")
        return

    df_list = []
    for bf in batch_files:
        df_list.append(pd.read_csv(bf))
        
    df_unfiltered = pd.concat(df_list, ignore_index=True)
    df_unfiltered.to_csv(unfiltered_out, index=False)
    
    records_before = len(df_unfiltered)
    
    # 2. Filter out outliers
    if "ftp_label" in df_unfiltered.columns:
        df_filtered = df_unfiltered[(df_unfiltered["ftp_label"] >= 50) & (df_unfiltered["ftp_label"] <= 500)].copy()
        records_after = len(df_filtered)
        ftp_min_before = df_unfiltered["ftp_label"].min()
        ftp_max_before = df_unfiltered["ftp_label"].max()
        ftp_min_after = df_filtered["ftp_label"].min()
        ftp_max_after = df_filtered["ftp_label"].max()
        outliers_removed = records_before - records_after
    else:
        df_filtered = df_unfiltered.copy()
        records_after = len(df_filtered)
        ftp_min_before = ftp_max_before = ftp_min_after = ftp_max_after = "N/A"
        outliers_removed = 0

    df_filtered.to_csv(filtered_out, index=False)
    
    # Stats for report
    zips_final = len(list(raw_zips_dir.glob("*.zip"))) if raw_zips_dir.exists() else 0
    state_file = processed_dir / "batch_state.json"
    zips_processed = 0
    zips_error = 0
    if state_file.exists():
        state = json.loads(state_file.read_text())
        zips_processed = len(state.get("processed_zips", {}))
        zips_error = len(state.get("error_zips", {}))

    # Download summary logic: we know we started at 136 zips.
    zips_start = 136
    zips_downloaded = max(0, zips_final - zips_start)
    free_space = get_free_gib()

    # Column counts
    total_cols = len(df_filtered.columns)
    variant_b_cols = len([c for c in df_filtered.columns if c != "mmp_20min" and not c.startswith("ftp_")])
    variant_c_cols = len([c for c in df_filtered.columns if not c.startswith("mmp_") and not c.startswith("ftp_")])
    athletes_count = df_filtered["athlete_id"].nunique() if "athlete_id" in df_filtered.columns else 0

    # 3. Download Report
    download_report = reports_dir / "partial_500_download_report.md"
    download_report.write_text(f"""# Raport pobierania częściowego (max 500)

## Podsumowanie pobierania
- ZIP-y na starcie: {zips_start}
- ZIP-y pobrane: {zips_downloaded}
- ZIP-y finalnie: {zips_final}
- Wolne miejsce po pobieraniu: {free_space:.2f} GiB
- Zatrzymanie z powodu braku miejsca: {"Nie" if free_space > 35.0 else "Tak"}
- Czy można bezpiecznie kontynuować pobieranie kolejnej partii: {"Tak" if free_space > 35.0 else "Nie"}
""")

    # 4. Rich Dataset Report
    dataset_report = reports_dir / "partial_500_rich_dataset_report.md"
    dataset_report.write_text(f"""# Raport ze zbioru danych po częściowym przetwarzaniu

## Podsumowanie zbioru danych
- Liczba przetworzonych ZIP-ów: {zips_processed}
- Liczba ZIP-ów z błędami (ominiętych): {zips_error}
- Rekordy przed filtrem FTP: {records_before}
- Rekordy po filtrze FTP: {records_after}
- Liczba zawodników (unikalne athlete_id): {athletes_count}

## Cechy
- Wszystkie kolumny w zbiorze: {total_cols}
- Wariant B (bez mmp_20min): ~{variant_b_cols} cech
- Wariant C (bez mmp_*): ~{variant_c_cols} cech

## Jakość danych i braki
(Szczegóły można wygenerować w dedykowanym skrypcie audytu danych).
""")

    # 5. FTP Outlier Audit
    audit_report = reports_dir / "partial_500_ftp_outlier_audit.md"
    audit_report.write_text(f"""# Audyt wartości odstających dla zmiennej celu (FTP)

## Podsumowanie filtracji
- Zastosowany filtr: 50 <= ftp_label <= 500
- Rekordy przeanalizowane: {records_before}
- Liczba odrzuconych outlierów: {outliers_removed}
- Zakres FTP przed filtracją: [{ftp_min_before}, {ftp_max_before}]
- Zakres FTP po filtracji: [{ftp_min_after}, {ftp_max_after}]
""")

    print("Reports generated successfully.")

if __name__ == "__main__":
    generate_reports()
