import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.npa.go.jp/safetylife/seianki/jisatsu/"
DOWNLOAD_DIR = "data/raw_downloads"

session = requests.Session()

session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
})

def safe_get(url):
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=10)
            if resp.status_code == 403:
                print(f"[403 BLOCKED] Attempt {attempt+1}, retrying...")
                time.sleep(2 + attempt)
                continue
            resp.raise_for_status()
            return resp
        except Exception as e:
            print(f"[ERROR] {url}: {e}")
            time.sleep(1)
    return None

def list_year_folders():
    print("[INFO] Fetching year folders...")
    resp = safe_get(BASE_URL)
    if resp is None:
        print("[FAIL] Could not fetch base URL")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    folders = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue

        # Recognize both Reiwa (R) and Heisei (H)
        if ("R0" in href) or href.startswith("H"):
            full = urljoin(BASE_URL, href)
            folders.append(full)

    print(f"[INFO] Year folders found: {len(folders)}")
    return folders

def list_files_in_folder(folder_url):
    resp = safe_get(folder_url)
    if resp is None:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    files = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue

        if href.endswith(".pdf") or href.endswith(".csv"):
            files.append(urljoin(folder_url, href))

    return files

def download_file(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    filename = url.split("/")[-1]
    out_path = os.path.join(out_dir, filename)

    if os.path.exists(out_path):
        print(f"[SKIP] {filename} exists")
        return

    print(f"[DOWNLOAD] {filename}")
    resp = safe_get(url)
    if resp is None:
        print(f"[ERROR] Failed to download {filename}")
        return

    with open(out_path, "wb") as f:
        f.write(resp.content)

    # Random throttle to look human
    time.sleep(random.uniform(1.2, 2.2))

def main():
    print("[START] Japanese Police Suicide Stats Scraper")

    year_folders = list_year_folders()
    all_files = []

    for folder in year_folders:
        print(f"[INFO] Scanning: {folder}")
        all_files.extend(list_files_in_folder(folder))

    print(f"[INFO] Total files discovered: {len(all_files)}")

    for file_url in all_files:
        download_file(file_url, DOWNLOAD_DIR)

    print("[DONE] All downloads complete.")

if __name__ == "__main__":
    main()
