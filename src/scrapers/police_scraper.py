import requests
from bs4 import BeautifulSoup
import pdfplumber
import pandas as pd
from pathlib import Path

BASE_URL = "https://www.npa.go.jp/publications/statistics/safetylife/jisatsu.html"
RAW_DIR = Path("data_raw")

def fetch_pdf_links():
    resp = requests.get(BASE_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    pdf_links = []
    for link in soup.find_all("a", href=True):
        if link["href"].endswith(".pdf"):
            pdf_links.append(link["href"])
    return pdf_links

def download_pdfs(pdf_links):
    RAW_DIR.mkdir(exist_ok=True)
    for url in pdf_links:
        filename = RAW_DIR / url.split("/")[-1]
        if not filename.exists():
            pdf_content = requests.get(url).content
            with open(filename, "wb") as f:
                f.write(pdf_content)

if __name__ == "__main__":
    links = fetch_pdf_links()
    download_pdfs(links)
