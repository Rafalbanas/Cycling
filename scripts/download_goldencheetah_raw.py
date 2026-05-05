import os
import json
import logging
import urllib.request
from pathlib import Path
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
OSF_API_URL = "https://api.osf.io/v2/nodes/6hfpz/files/osfstorage/"
DATA_DIR = Path("data/raw/goldencheetah")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    to_download = []
    current_url = OSF_API_URL
    while current_url and len(to_download) < args.limit:
        with urllib.request.urlopen(current_url) as response:
            data = json.loads(response.read().decode())
            for f in data['data']:
                if f['attributes']['name'].endswith('.zip'):
                    to_download.append({'name': f['attributes']['name'], 'url': f['links']['download']})
                    if len(to_download) >= args.limit: break
            current_url = data['links'].get('next')
    for item in to_download:
        local_path = DATA_DIR / item['name']
        if not local_path.exists():
            logging.info(f"Pobieranie: {local_path.name}...")
            urllib.request.urlretrieve(item['url'], local_path)
    logging.info(f"Pobrano {len(to_download)} plików.")

if __name__ == "__main__": main()
