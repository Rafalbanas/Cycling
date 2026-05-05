#!/bin/bash
set -e

LIMIT=$1
if [ -z "$LIMIT" ]; then
    LIMIT=50
fi

echo "================================================="
echo "=== ROZPOCZYNAMY PIPELINE PRACY MAGISTERSKIEJ ==="
echo "================================================="
echo "Cel: Przetworzenie $LIMIT kolarzy z GoldenCheetah OpenData"

source venv/bin/activate

echo ""
echo "[1/5] Pobieranie paczek z danymi kolarzy..."
python3 scripts/download_goldencheetah_raw.py --limit $LIMIT

echo ""
echo "[2/5] Rozpakowywanie i segregowanie paczek..."
for z in data/raw/goldencheetah/*.zip; do 
  athlete_id=$(basename "$z" .zip)
  mkdir -p "data/raw/$athlete_id"
  unzip -n -q "$z" -d "data/raw/$athlete_id/"
done

echo ""
echo "[3/5] Generowanie ustrukturyzowanego wektora cech (ETL)..."
echo "(Ten proces dla setek zawodników może zająć od 15 do nawet 60 minut!)"
python3 scripts/build_features_dataset.py

echo ""
echo "[4/5] Trenowanie modeli ML (Ridge, Random Forest, XGBoost)..."
python3 scripts/train_models.py

echo ""
echo "[5/5] Automatyczna aktualizacja pracy magisterskiej (LaTeX)..."
python3 scripts/update_latex_results.py

echo ""
echo "================================================="
echo "=== PIPELINE ZAKOŃCZONY SUKCESEM! ==="
echo "Wszystkie wyniki (liczby, błędy, wykresy i proporcje)"
echo "zostały z sukcesem osadzone w Twojej pracy magisterskiej."
echo "Skrypt wygenerował również finalny plik features_ftp_dataset.csv"
echo "================================================="
