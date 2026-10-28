#!/usr/bin/env python3
"""Root-owned receiver for bounded cycling release archives over forced-command SSH."""
import ast
import csv
import fcntl
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen
import zipfile

CONFIG = Path("/etc/cycling-web/deploy.json")
LEGACY = Path("/opt/cycling-web")
MAX_BYTES = 32 * 1024 * 1024
HEALTH_BODY_LIMIT = 64 * 1024 + 1

# The release is exactly these files; nothing else, including directories
# and symlink-like entries, is accepted.
FILES = {
    "revision.txt",
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
}


def switch(current, destination):
    temporary = current.with_name("current.next")
    temporary.unlink(missing_ok=True)
    temporary.symlink_to(destination)
    temporary.replace(current)


def restart(config):
    # Fixed service command, never derived from the archive or SSH arguments.
    subprocess.run(["systemctl", "restart", "cycling-web.service"], check=True, timeout=45)


def status(state):
    current = state / "current"
    if not current.is_symlink():
        return "uninitialized"
    try:
        return (current.resolve(strict=True) / "revision.txt").read_text(encoding="utf-8").strip()
    except OSError:
        return "uninitialized"


def healthy(config, revision, revision_required=True):
    base = config["health_url"].rstrip("/")
    try:
        with urlopen(base + "/healthz", timeout=3) as response:
            body = response.read(HEALTH_BODY_LIMIT)
            if len(body) >= HEALTH_BODY_LIMIT:
                return False
            health = json.loads(body)
            if health.get("status") != "ok":
                return False
            if revision_required and health.get("revision") != revision:
                return False
        # The legacy deployment has no analysis endpoint; its status is still "ok".
        if not revision_required:
            return True
        with urlopen(base + "/api/analysis?variant=Variant_B", timeout=3) as response:
            body = response.read(HEALTH_BODY_LIMIT)
            if len(body) >= HEALTH_BODY_LIMIT:
                return False
            analysis = json.loads(body)
            return analysis.get("count", 0) > 0
    except (OSError, ValueError, AttributeError):
        return False


def deploy(config, revision, digest, stream):
    if not re.fullmatch(r"[a-f0-9]{40}", revision) or not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise ValueError("Invalid revision or archive digest")
    state = Path(config["state_dir"])
    state.mkdir(parents=True, exist_ok=True)
    with (state / "deploy.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        payload = stream.read(MAX_BYTES + 1)
        if len(payload) > MAX_BYTES or hashlib.sha256(payload).hexdigest() != digest:
            raise ValueError("Archive size or digest mismatch")
        releases = state / "releases"
        releases.mkdir(exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix="staging-", dir=releases))
        try:
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                entries = archive.infolist()
                if len(entries) != len(FILES) or {entry.filename for entry in entries} != FILES:
                    raise ValueError("Unexpected archive entries")
                if sum(entry.file_size for entry in entries) > MAX_BYTES:
                    raise ValueError("Expanded archive too large")
                for entry in entries:
                    if entry.is_dir():
                        raise ValueError("Directory entries are not allowed in releases")
                    target = staging / entry.filename
                    # The fresh staging path can never be a real symlink, so
                    # detect symlink entries from the Unix mode in the zip header.
                    if stat.S_ISLNK(entry.external_attr >> 16):
                        raise ValueError("Symlink entries are not allowed in releases")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    # Write regular files only, ignoring archive modes and symlink metadata.
                    target.write_bytes(archive.read(entry))
                    target.chmod(0o644)
            if (staging / "revision.txt").read_text(encoding="utf-8").strip() != revision:
                raise ValueError("Archive revision mismatch")
            ast.parse((staging / "webapp/server.py").read_text(encoding="utf-8"))
            json.loads(
                (staging / "experiments/control_5000/results/control_5000_data_stats.json").read_text(
                    encoding="utf-8"
                )
            )
            for name in (
                "results/model_comparison_partial.csv",
                "results/error_by_ftp_bins.csv",
                "results/shap_importance_variant_b.csv",
                "results/shap_importance_variant_c.csv",
                "results/baseline_predictions_variant_b.csv",
                "results/baseline_predictions_variant_c.csv",
                "experiments/control_5000/results/control_5000_metrics.csv",
            ):
                with (staging / name).open(encoding="utf-8", newline="") as handle:
                    if next(csv.reader(handle), None) is None:
                        raise ValueError("CSV release file must have a header")
            if not (staging / "webapp/index.html").read_text(encoding="utf-8").strip():
                raise ValueError("Empty index.html")
            staging.chmod(0o755)
            for directory in sorted(staging.rglob("*")):
                if directory.is_dir():
                    directory.chmod(0o755)
            release = releases / (revision + "-" + digest[:16])
            if release.exists():
                shutil.rmtree(staging)
            else:
                staging.rename(release)
            current = state / "current"
            previous = None
            if current.is_symlink():
                try:
                    previous = current.resolve(strict=True)
                except OSError:
                    previous = None
            if previous is None:
                # Before the first release, rollback falls back to the legacy deployment.
                previous = LEGACY
            switch(current, release)
            try:
                restart(config)
                for _ in range(config.get("health_attempts", 10)):
                    if healthy(config, revision):
                        break
                    time.sleep(config.get("health_interval", 2))
                else:
                    raise RuntimeError("Origin health check failed")
                # Persist rollback metadata before reporting success.
                if previous != release:
                    (state / "previous").write_text(str(previous) + "\n")
            except BaseException:
                if previous and previous != release:
                    switch(current, previous)
                    restart(config)
                    if previous == LEGACY:
                        # Legacy has no revision.txt and no analysis endpoint.
                        rollback_revision, revision_required = "", False
                    else:
                        try:
                            rollback_revision = (previous / "revision.txt").read_text(encoding="utf-8").strip()
                            revision_required = True
                        except OSError:
                            rollback_revision, revision_required = "", False
                    if healthy(config, rollback_revision, revision_required):
                        print(f"Rolled back to {previous}")
                    else:
                        print("ROLLBACK HEALTH CHECK FAILED", file=sys.stderr)
                else:
                    current.unlink(missing_ok=True)
                raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    print(f"Deployed {revision}")


def main():
    # Fixed root-owned config; neither SSH nor the archive can override paths.
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if sys.argv[1:] == ["status"]:
        print(status(Path(config["state_dir"])))
    elif len(sys.argv) == 3:
        deploy(config, sys.argv[1], sys.argv[2], sys.stdin.buffer)
    else:
        print("Expected status or REVISION ARCHIVE_SHA256", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
