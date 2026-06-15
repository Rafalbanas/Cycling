import subprocess
import os
import shutil
import logging
import sys
from pathlib import Path

# Setup
os.environ["MASTER_THESIS_DATA_ROOT"] = "/Volumes/MasterThesisSSD/MasterThesisData"
data_root = Path("/Volumes/MasterThesisSSD/MasterThesisData")
raw_zips = data_root / "goldencheetah" / "raw_zips"

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

MAX_ITERATIONS = 5
DOWNLOAD_BATCH_SIZE = 100
PROCESS_BATCH_SIZE = 20
MIN_FREE_GIB = 35.0

def get_free_gib():
    return shutil.disk_usage(data_root).free / 1024**3

for i in range(MAX_ITERATIONS):
    free = get_free_gib()
    logging.info(f"--- Iteration {i+1} --- Free space: {free:.2f} GiB")
    if free < MIN_FREE_GIB:
        logging.warning("Not enough free space, stopping.")
        break
    
    zips_before = len(list(raw_zips.glob("*.zip"))) if raw_zips.exists() else 0
    
    logging.info(f"Downloading batch of {DOWNLOAD_BATCH_SIZE} ZIPs...")
    dl_cmd = [
        sys.executable, "scripts/download_goldencheetah_raw.py", 
        "--limit", str(DOWNLOAD_BATCH_SIZE), 
        "--batch-size", str(DOWNLOAD_BATCH_SIZE),
        "--min-free-gib", str(MIN_FREE_GIB)
    ]
    res_dl = subprocess.run(dl_cmd)
    if res_dl.returncode != 0:
        logging.error("Download script failed or stopped. Will continue to process what we have, then stop.")
        
    zips_after = len(list(raw_zips.glob("*.zip"))) if raw_zips.exists() else 0
    downloaded = zips_after - zips_before
    logging.info(f"Downloaded {downloaded} new ZIPs.")
        
    free = get_free_gib()
    logging.info(f"After download, free space: {free:.2f} GiB")
    if free < MIN_FREE_GIB:
        logging.warning("Not enough free space after download, stopping.")
        break
        
    logging.info("Running batch processing...")
    proc_cmd = [
        sys.executable, "scripts/build_features_dataset_batch.py",
        "--batch-size", str(PROCESS_BATCH_SIZE),
        "--min-free-gib", str(MIN_FREE_GIB)
    ]
    res_proc = subprocess.run(proc_cmd)
    if res_proc.returncode != 0:
        logging.error("Processing script failed or stopped.")
        break
        
    if downloaded == 0 and res_dl.returncode == 0:
        logging.info("No more ZIPs to download. Stopping.")
        break

    if res_dl.returncode != 0:
        logging.info("Stopping iterations due to previous download errors.")
        break
