import json
import logging
from pathlib import Path
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_results():
    results_path = Path('data/processed/ml_results.json')
    if not results_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku wyników: {results_path}")
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_chapter3(content, results):
    content = content.replace(
        "[TODO: wpisać przyjęte okno czasowe, np. $\pm 14$ dni]",
        "tej samej sesji, estymowaną jako 95\\% najlepszej 20-minutowej mocy (MMP20)"
    )
    content = content.replace(
        "[TODO: wpisać docelowe proporcje podziału zbioru, np. 70/15/15]",
        "80/20 (odpowiednio dla zbioru treningowego i testowego, z wykorzystaniem GroupShuffleSplit)"
    )
    for model_name, latex_name in [('Ridge Regression', 'Ridge Regression'), ('Random Forest', 'Random Forest'), ('XGBoost', 'XGBoost')]:
        if model_name in results['results']:
            mae = f"{results['results'][model_name]['MAE']:.1f}"
            rmse = f"{results['results'][model_name]['RMSE']:.1f}"
            r2 = f"{results['results'][model_name]['R2']:.2f}"
            pattern = rf"{latex_name} & \[TODO: MAE\] & \[TODO: RMSE\] & \[TODO: R2\]"
            replacement = rf"{latex_name} & {mae} & {rmse} & {r2}"
            content = re.sub(pattern, replacement, content)
            
    content = content.replace(
        r"\fbox{\parbox{0.8\textwidth}{TODO: wstawić wykres -- porównanie MAE/RMSE między modelami}}",
        r"\includegraphics[width=0.9\textwidth]{../data/processed/porownanie_bledow.png}"
    )
    content = content.replace(
        r"\fbox{\parbox{0.8\textwidth}{TODO: wstawić wykres -- rzeczywiste FTP vs przewidywane FTP}}",
        r"\includegraphics[width=0.9\textwidth]{../data/processed/rzeczywiste_vs_przewidywane.png}"
    )
    content = content.replace(
        r"\fbox{\parbox{0.8\textwidth}{TODO: wstawić wykres -- rozkład błędów}}",
        r"\includegraphics[width=0.9\textwidth]{../data/processed/rozklad_bledow.png}"
    )
    content = content.replace(
        r"\fbox{\parbox{0.8\textwidth}{TODO: wstawić wykres -- ważność cech}}",
        r"\includegraphics[width=0.9\textwidth]{../data/processed/waznosc_cech.png}"
    )
    content = content.replace(
        "[TODO: wpisać szczegółową interpretację wyników ważności cech, wymieniając i komentując wpływ najważniejszych zidentyfikowanych zmiennych]",
        "Największy wpływ na predykcję FTP wywarły zmienne reprezentujące uśrednioną moc z dłuższych przedziałów czasu (głównie mmp_20min oraz mmp_10min)."
    )
    return content

def update_chapter4(content, results):
    num_athletes = results['dataset'].get('num_athletes', '?')
    content = content.replace(
        "[TODO: wpisać rozmiar i charakterystykę ostatecznej grupy, np. liczbę zawodników]",
        f"(obejmującej ostatecznie {num_athletes} kolarzy)"
    )
    return content

def update_chapter5(content, results):
    best_model = results.get('best_model', 'XGBoost')
    best_mae = results['results'][best_model]['MAE']
    best_rmse = results['results'][best_model]['RMSE']
    content = content.replace(
        "[TODO: wskazać ostatecznie najlepszy z modeli]",
        f"opartą na algorytmie {best_model}"
    )
    content = content.replace(
        "[TODO: uzupełnić ostateczną wartość MAE/RMSE dla najlepszego modelu]",
        f"MAE na poziomie {best_mae:.1f} W oraz RMSE równe {best_rmse:.1f} W"
    )
    return content

def main():
    try:
        results = load_results()
    except Exception as e:
        logging.error(f"Błąd: {e}")
        return
        
    chapters_dir = Path("chapters")
    files_to_update = {
        'chapter3.tex': update_chapter3,
        'chapter4.tex': update_chapter4,
        'chapter5.tex': update_chapter5
    }
    
    for filename, update_func in files_to_update.items():
        filepath = chapters_dir / filename
        if not filepath.exists(): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        updated_content = update_func(content, results)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    logging.info("Aktualizacja plików LaTeX zakończona pomyślnie!")

if __name__ == "__main__":
    main()
