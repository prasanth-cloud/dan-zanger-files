#!/usr/bin/env python3
"""
Scrapes the chartpattern.com Winners page for Dan Zanger's documented trades.
Extracts: ticker, entry date, exit date, % gain, chart image URL.
Saves results to data/winners.csv and downloads chart images.
"""

import csv
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_CSV = ROOT_DIR / "data" / "winners.csv"
CHART_DIR = ROOT_DIR / "charts" / "dan-zanger" / "winners"
BASE_URL = "https://www.chartpattern.com"
WINNERS_URL = f"{BASE_URL}/winners.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def fetch_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_winners(soup):
    rows = []
    tables = soup.find_all("table")
    for table in tables:
        for tr in table.find_all("tr")[1:]:
            cells = tr.find_all("td")
            if len(cells) >= 4:
                ticker = cells[0].get_text(strip=True)
                entry_date = cells[1].get_text(strip=True)
                exit_date = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                pct_gain = cells[3].get_text(strip=True) if len(cells) > 3 else ""
                img_tag = tr.find("img")
                img_url = urljoin(BASE_URL, img_tag["src"]) if img_tag else ""
                rows.append({
                    "ticker": ticker,
                    "entry_date": entry_date,
                    "exit_date": exit_date,
                    "pct_gain": pct_gain,
                    "chart_url": img_url,
                    "source": "chartpattern.com",
                    "pattern_type": "",
                    "sector": "",
                    "volume_confirmed": "",
                    "outcome": "winner",
                    "notes": "",
                })
    return rows


def download_chart(url, ticker, date):
    if not url:
        return ""
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    ext = url.split(".")[-1][:4]
    filename = f"{ticker}_{date}.{ext}".replace("/", "-")
    filepath = CHART_DIR / filename
    if filepath.exists():
        return str(filepath.relative_to(ROOT_DIR))
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        filepath.write_bytes(resp.content)
        time.sleep(0.5)
    except Exception as e:
        print(f"  Failed to download {url}: {e}")
        return ""
    return str(filepath.relative_to(ROOT_DIR))


def main():
    print(f"Fetching {WINNERS_URL}")
    soup = fetch_page(WINNERS_URL)
    winners = parse_winners(soup)
    print(f"Found {len(winners)} winner entries")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="") as f:
        fieldnames = [
            "ticker", "entry_date", "exit_date", "pct_gain", "chart_url",
            "local_path", "source", "pattern_type", "sector",
            "volume_confirmed", "outcome", "notes"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in winners:
            row["local_path"] = download_chart(
                row["chart_url"], row["ticker"], row["entry_date"]
            )
            writer.writerow(row)
            print(f"  {row['ticker']} ({row['entry_date']}) - {row['pct_gain']}")

    print(f"\nSaved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
