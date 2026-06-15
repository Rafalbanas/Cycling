"""Extract rich GoldenCheetah features from ZIP archives in resumable batches."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import shutil
import zipfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pandas as pd

from build_features_dataset import process_file
from data_paths import PROJECT_ROOT, goldencheetah_paths

MIN_FREE_GIB_DEFAULT = 35.0
BATCH_SIZE_DEFAULT = 20


def free_gib(path: Path) -> float:
    path.mkdir(parents=True, exist_ok=True)
    return shutil.disk_usage(path).free / 1024**3


def configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")],
        force=True,
    )


def append_storage_event(path: Path, event: str, available_gib: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", encoding="utf-8") as handle:
        if write_header:
            handle.write("timestamp,event,free_gib\n")
        handle.write(f"{datetime.now().isoformat(timespec='seconds')},{event},{available_gib:.3f}\n")


def ensure_free_space(path: Path, minimum_gib: float, event: str, storage_log: Path) -> float:
    available = free_gib(path)
    append_storage_event(storage_log, event, available)
    logging.info("Wolne miejsce [%s]: %.3f GiB", event, available)
    if available < minimum_gib:
        raise RuntimeError(
            f"Przerwano bezpiecznie: wolne miejsce {available:.3f} GiB "
            f"jest mniejsze niż wymagane {minimum_gib:.3f} GiB."
        )
    return available


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"processed_zips": {}, "error_zips": {}, "updated_at": None}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def batch_id(archives: list[Path]) -> str:
    names = "\n".join(archive.name for archive in archives)
    return hashlib.sha256(names.encode("utf-8")).hexdigest()[:12]


def safe_extract_csv(archive: Path, destination: Path) -> list[Path]:
    extracted: list[Path] = []
    destination.mkdir(parents=True, exist_ok=True)
    destination_resolved = destination.resolve()
    with zipfile.ZipFile(archive) as zipped:
        for member in zipped.infolist():
            member_path = Path(member.filename)
            if member.is_dir() or member_path.suffix.lower() != ".csv":
                continue
            output = destination / member_path
            output.parent.mkdir(parents=True, exist_ok=True)
            if destination_resolved not in output.resolve().parents:
                raise ValueError(f"Niebezpieczna ścieżka w ZIP: {member.filename}")
            with zipped.open(member) as source, output.open("wb") as target:
                shutil.copyfileobj(source, target)
            extracted.append(output)
    return extracted


def process_archive(archive: Path, extraction_root: Path, workers: int) -> tuple[list[dict], dict]:
    athlete_id = archive.stem
    archive_root = extraction_root / athlete_id
    csv_files = safe_extract_csv(archive, archive_root)
    rows: list[dict] = []
    errors: Counter = Counter()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for csv_file, result in zip(csv_files, executor.map(process_file, csv_files, chunksize=32)):
            if "error" in result:
                errors[str(result["error"])] += 1
                continue
            result["athlete_id"] = athlete_id
            result["source_path"] = f"{archive.name}::{csv_file.relative_to(archive_root)}"
            result["source_zip"] = archive.name
            rows.append(result)

    return rows, {
        "csv_files": len(csv_files),
        "accepted_records": len(rows),
        "session_errors": dict(errors),
    }


def write_processed_lists(output_dir: Path, state: dict) -> None:
    processed = sorted(state["processed_zips"])
    errors = state["error_zips"]
    (output_dir / "processed_zips.txt").write_text(
        "".join(f"{name}\n" for name in processed),
        encoding="utf-8",
    )
    (output_dir / "error_zips.json").write_text(
        json.dumps(errors, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_status_report(
    report_path: Path,
    archives_total: int,
    state: dict,
    batches_dir: Path,
    available_gib: float,
    minimum_gib: float,
    stopped_reason: str | None,
) -> None:
    processed = len(state["processed_zips"])
    errors = len(state["error_zips"])
    batches = len(list(batches_dir.glob("features_batch_*.csv")))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"""# Status batchowego przetwarzania GoldenCheetah

Data aktualizacji: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

| Element | Wartość |
|---|---:|
| Archiwa ZIP dostępne lokalnie | {archives_total} |
| Archiwa ZIP przetworzone | {processed} |
| Archiwa ZIP z błędami | {errors} |
| Pliki CSV partii cech | {batches} |
| Wolne miejsce na SSD | {available_gib:.3f} GiB |
| Próg bezpiecznego zatrzymania | {minimum_gib:.3f} GiB |

Status zatrzymania: {stopped_reason or "brak; wykonanie zakończone planowo"}.

Archiwa ZIP nie są usuwane. Tymczasowa ekstrakcja CSV jest usuwana wyłącznie
po poprawnym zapisie pliku cech partii.
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    paths = goldencheetah_paths()
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-dir", type=Path, default=paths.raw_zips)
    parser.add_argument("--cache-dir", type=Path, default=paths.cache)
    parser.add_argument("--output-dir", type=Path, default=paths.processed / "batches")
    parser.add_argument("--log-file", type=Path, default=paths.logs / "batch_features.log")
    parser.add_argument("--storage-log", type=Path, default=paths.logs / "batch_storage_monitor.csv")
    parser.add_argument("--report", type=Path, default=PROJECT_ROOT / "reports" / "batch_processing_status.md")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE_DEFAULT)
    parser.add_argument("--max-zips", type=int)
    parser.add_argument("--max-batches", type=int)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--min-free-gib", type=float, default=MIN_FREE_GIB_DEFAULT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging(args.log_file)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    state_path = args.output_dir / "batch_state.json"
    state = load_state(state_path)
    all_archives = sorted(args.zip_dir.glob("*.zip"))
    pending = [archive for archive in all_archives if archive.name not in state["processed_zips"]]
    if args.max_zips is not None:
        pending = pending[: args.max_zips]

    stopped_reason: str | None = None
    completed_batches = 0
    logging.info(
        "Dostępne ZIP-y: %s; przetworzone wcześniej: %s; oczekujące w tym uruchomieniu: %s",
        len(all_archives),
        len(state["processed_zips"]),
        len(pending),
    )

    try:
        ensure_free_space(args.cache_dir, args.min_free_gib, "start", args.storage_log)
        for offset in range(0, len(pending), args.batch_size):
            if args.max_batches is not None and completed_batches >= args.max_batches:
                break
            archives = pending[offset : offset + args.batch_size]
            identifier = batch_id(archives)
            output_path = args.output_dir / f"features_batch_{identifier}.csv"
            manifest_path = args.output_dir / f"features_batch_{identifier}.json"
            extraction_root = args.cache_dir / f"extract_batch_{identifier}"

            if output_path.exists() and manifest_path.exists():
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                for archive_name in manifest["archives"]:
                    state["processed_zips"].setdefault(
                        archive_name,
                        {"batch_id": identifier, "recovered_from_existing_batch": True},
                    )
                save_state(state_path, state)
                logging.info("Pominięto istniejący batch: %s", identifier)
                completed_batches += 1
                continue

            ensure_free_space(args.cache_dir, args.min_free_gib, f"before_extract_{identifier}", args.storage_log)
            rows: list[dict] = []
            archive_results: dict[str, dict] = {}
            successful_archives: list[str] = []
            extraction_root.mkdir(parents=True, exist_ok=True)

            for archive in archives:
                try:
                    archive_rows, archive_result = process_archive(archive, extraction_root, args.workers)
                    rows.extend(archive_rows)
                    archive_results[archive.name] = archive_result
                    successful_archives.append(archive.name)
                except Exception as exc:  # noqa: BLE001 - preserve archive-level failure for resuming
                    message = f"{type(exc).__name__}: {exc}"
                    state["error_zips"][archive.name] = {
                        "error": message,
                        "timestamp": datetime.now().isoformat(timespec="seconds"),
                    }
                    logging.exception("Błąd ZIP %s", archive.name)

            ensure_free_space(args.cache_dir, args.min_free_gib, f"after_extract_{identifier}", args.storage_log)
            pd.DataFrame(rows).to_csv(output_path, index=False)
            manifest = {
                "batch_id": identifier,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "archives": successful_archives,
                "archive_results": archive_results,
                "records": len(rows),
            }
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            ensure_free_space(args.cache_dir, args.min_free_gib, f"after_write_{identifier}", args.storage_log)

            for archive_name in successful_archives:
                state["processed_zips"][archive_name] = {
                    "batch_id": identifier,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
                state["error_zips"].pop(archive_name, None)
            save_state(state_path, state)
            write_processed_lists(args.output_dir, state)

            shutil.rmtree(extraction_root)
            ensure_free_space(args.cache_dir, args.min_free_gib, f"after_cleanup_{identifier}", args.storage_log)
            logging.info(
                "Zapisano batch %s: ZIP-y=%s, rekordy=%s, plik=%s",
                identifier,
                len(successful_archives),
                len(rows),
                output_path,
            )
            completed_batches += 1
    except RuntimeError as exc:
        stopped_reason = str(exc)
        logging.error(stopped_reason)
    finally:
        save_state(state_path, state)
        write_processed_lists(args.output_dir, state)
        available = free_gib(args.cache_dir)
        write_status_report(
            args.report,
            len(all_archives),
            state,
            args.output_dir,
            available,
            args.min_free_gib,
            stopped_reason,
        )

    if stopped_reason:
        raise SystemExit(stopped_reason)


if __name__ == "__main__":
    main()

