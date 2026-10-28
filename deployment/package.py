"""Package only the files the release is allowed to contain; nothing private ever enters a zip."""
import argparse
from pathlib import Path
import re
import zipfile

RELEASE_FILES = (
    "webapp/server.py",
    "webapp/index.html",
    "webapp/static/app.js",
    "webapp/static/styles.css",
    "webapp/static/favicon.svg",
    "results/model_comparison_partial.csv",
    "results/error_by_ftp_bins.csv",
    "results/shap_importance_variant_b.csv",
    "results/shap_importance_variant_c.csv",
    "results/baseline_predictions_variant_b.csv",
    "results/baseline_predictions_variant_c.csv",
    "experiments/control_5000/results/control_5000_data_stats.json",
    "experiments/control_5000/results/control_5000_metrics.csv",
)


def package(root, output, revision):
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Expected a full Git commit SHA")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in RELEASE_FILES:
            archive.write(root / name, name)
        archive.writestr("revision.txt", revision + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("revision")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    package(Path(__file__).resolve().parents[1], args.output, args.revision)
