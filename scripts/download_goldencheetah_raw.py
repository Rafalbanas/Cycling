import argparse
import json
import logging
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

from data_paths import PROJECT_ROOT, goldencheetah_paths

OSF_API_URL = "https://api.osf.io/v2/nodes/6hfpz/files/osfstorage/?page%5Bsize%5D=100"
MIN_FREE_GIB_DEFAULT = 35.0
BATCH_SIZE_DEFAULT = 100


def free_gib(path: Path) -> float:
    path.mkdir(parents=True, exist_ok=True)
    return shutil.disk_usage(path).free / 1024**3


def ensure_free_space(path: Path, minimum_gib: float, expected_bytes: int = 0) -> float:
    available = free_gib(path)
    remaining_after_download = available - expected_bytes / 1024**3
    if remaining_after_download < minimum_gib:
        raise RuntimeError(
            f"Przerwano bezpiecznie: po kolejnym pobraniu pozostałoby "
            f"{remaining_after_download:.3f} GiB, poniżej progu {minimum_gib:.3f} GiB."
        )
    return available


def configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")],
    )


def fetch_remote_archives(cache_dir: Path) -> list[dict]:
    cache_file = cache_dir / "remote_archives_cache.json"
    if cache_file.exists():
        logging.info("Wczytano metadane archiwów z pamięci podręcznej.")
        return json.loads(cache_file.read_text(encoding="utf-8"))

    logging.info("Pobieranie metadanych archiwów z OSF API (to może zająć kilka minut)...")
    archives: list[dict] = []
    current_url: str | None = OSF_API_URL
    while current_url:
        with urllib.request.urlopen(current_url) as response:
            data = json.loads(response.read().decode())
        for file_data in data["data"]:
            attributes = file_data["attributes"]
            name = attributes["name"]
            if name.endswith(".zip"):
                archives.append(
                    {
                        "name": name,
                        "url": file_data["links"]["download"],
                        "size": int(attributes.get("size") or 0),
                    }
                )
        current_url = data["links"].get("next")
    
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(archives, ensure_ascii=False, indent=2), encoding="utf-8")
    return archives


def write_report(
    report_path: Path,
    started_at: datetime,
    finished_at: datetime,
    remote_archives: list[dict],
    data_dir: Path,
    downloaded: list[str],
    errors: list[str],
    free_before_gib: float,
    free_after_gib: float,
    stopped_reason: str | None,
) -> None:
    local_names = {path.name for path in data_dir.glob("*.zip")}
    remote_names = {item["name"] for item in remote_archives}
    missing = remote_names - local_names
    remote_bytes = sum(item["size"] for item in remote_archives)
    local_bytes = sum(path.stat().st_size for path in data_dir.glob("*.zip"))
    error_rows = "\n".join(f"- `{error}`" for error in errors) or "- brak"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"""# Log pobierania GoldenCheetah OpenData

## Podsumowanie

| Element | Wartość |
|---|---:|
| Rozpoczęcie | {started_at.isoformat(timespec="seconds")} |
| Zakończenie | {finished_at.isoformat(timespec="seconds")} |
| Archiwa ZIP dostępne publicznie | {len(remote_archives)} |
| Rozmiar publicznych archiwów ZIP | {remote_bytes / 1024**3:.3f} GiB |
| Archiwa ZIP dostępne lokalnie | {len(local_names)} |
| Rozmiar lokalnych archiwów ZIP | {local_bytes / 1024**3:.3f} GiB |
| Archiwa ZIP nadal brakujące | {len(missing)} |
| Archiwa pobrane w tym uruchomieniu | {len(downloaded)} |
| Wolne miejsce przed pobieraniem | {free_before_gib:.3f} GiB |
| Wolne miejsce po pobieraniu | {free_after_gib:.3f} GiB |

Status zatrzymania: {stopped_reason or "brak; wykonanie zakończone planowo"}.

## Błędy

{error_rows}
""",
        encoding="utf-8",
    )


def main() -> None:
    paths = goldencheetah_paths()
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE_DEFAULT)
    parser.add_argument("--max-batches", type=int, default=1)
    parser.add_argument("--limit", type=int, help="Opcjonalny łączny limit nowych archiwów ZIP.")
    parser.add_argument("--data-dir", type=Path, default=paths.raw_zips)
    parser.add_argument("--log-file", type=Path, default=paths.logs / "download_full_dataset_log.txt")
    parser.add_argument("--report", type=Path, default=PROJECT_ROOT / "reports" / "download_full_dataset_log.md")
    parser.add_argument("--min-free-gib", type=float, default=MIN_FREE_GIB_DEFAULT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    configure_logging(args.log_file)
    args.data_dir.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now()
    free_before = free_gib(args.data_dir)
    downloaded: list[str] = []
    errors: list[str] = []
    stopped_reason: str | None = None
    remote_archives: list[dict] = []

    try:
        ensure_free_space(args.data_dir, args.min_free_gib)
        remote_archives = fetch_remote_archives(paths.cache)
        missing = [item for item in remote_archives if not (args.data_dir / item["name"]).exists()]
        if args.limit is not None:
            missing = missing[: args.limit]
        logging.info(
            "Publiczne ZIP-y: %s; lokalne ZIP-y: %s; oczekujące ZIP-y: %s",
            len(remote_archives),
            len(list(args.data_dir.glob("*.zip"))),
            len(missing),
        )

        if args.dry_run:
            logging.info("Tryb dry-run: pominięto transfer archiwów.")
        else:
            for batch_number, offset in enumerate(range(0, len(missing), args.batch_size), start=1):
                if args.max_batches is not None and batch_number > args.max_batches:
                    break
                batch = missing[offset : offset + args.batch_size]
                logging.info("Rozpoczęcie partii pobierania %s: ZIP-y=%s", batch_number, len(batch))
                for item in batch:
                    local_path = args.data_dir / item["name"]
                    temporary_path = local_path.with_suffix(f"{local_path.suffix}.part")
                    try:
                        ensure_free_space(args.data_dir, args.min_free_gib, item["size"])
                        logging.info("Pobieranie: %s", local_path.name)
                        urllib.request.urlretrieve(item["url"], temporary_path)
                        temporary_path.replace(local_path)
                        downloaded.append(local_path.name)
                    except Exception as exc:  # noqa: BLE001 - preserve download failures in report
                        temporary_path.unlink(missing_ok=True)
                        message = f"{item['name']}: {type(exc).__name__}: {exc}"
                        errors.append(message)
                        logging.exception("Błąd pobierania %s", item["name"])
                logging.info(
                    "Zakończenie partii %s: pobrano=%s; wolne miejsce=%.3f GiB",
                    batch_number,
                    len(downloaded),
                    free_gib(args.data_dir),
                )
    except RuntimeError as exc:
        stopped_reason = str(exc)
        logging.error(stopped_reason)
    finally:
        finished_at = datetime.now()
        write_report(
            args.report,
            started_at,
            finished_at,
            remote_archives,
            args.data_dir,
            downloaded,
            errors,
            free_before,
            free_gib(args.data_dir),
            stopped_reason,
        )

    if stopped_reason:
        raise SystemExit(stopped_reason)


if __name__ == "__main__":
    main()
