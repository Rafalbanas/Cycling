"""Resolve GoldenCheetah storage paths without moving the source repository."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_CONFIG_PATH = PROJECT_ROOT / "config" / "local_paths.json"


@dataclass(frozen=True)
class GoldenCheetahPaths:
    raw_zips: Path
    extracted: Path
    processed: Path
    cache: Path
    logs: Path


def configured_data_root() -> Path | None:
    env_value = os.environ.get("MASTER_THESIS_DATA_ROOT")
    if env_value:
        return Path(env_value).expanduser()

    if LOCAL_CONFIG_PATH.exists():
        config = json.loads(LOCAL_CONFIG_PATH.read_text(encoding="utf-8"))
        value = config.get("MASTER_THESIS_DATA_ROOT")
        if value:
            return Path(value).expanduser()
    return None


def goldencheetah_paths() -> GoldenCheetahPaths:
    data_root = configured_data_root()
    if data_root is None:
        local_data = PROJECT_ROOT / "data"
        return GoldenCheetahPaths(
            raw_zips=local_data / "raw" / "goldencheetah",
            extracted=local_data / "raw",
            processed=local_data / "processed",
            cache=local_data / "cache",
            logs=local_data / "raw" / "goldencheetah",
        )

    goldencheetah_root = data_root / "goldencheetah"
    return GoldenCheetahPaths(
        raw_zips=goldencheetah_root / "raw_zips",
        extracted=goldencheetah_root / "extracted",
        processed=goldencheetah_root / "processed",
        cache=goldencheetah_root / "cache",
        logs=goldencheetah_root / "logs",
    )


def main() -> None:
    paths = goldencheetah_paths()
    values = {
        "data_root": configured_data_root() or PROJECT_ROOT / "data",
        "raw_zips": paths.raw_zips,
        "extracted": paths.extracted,
        "processed": paths.processed,
        "cache": paths.cache,
        "logs": paths.logs,
    }
    if len(sys.argv) == 2:
        key = sys.argv[1]
        if key not in values:
            raise SystemExit(f"Nieznana ścieżka: {key}")
        print(values[key])
        return
    for key, value in values.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()

