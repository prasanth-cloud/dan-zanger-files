#!/usr/bin/env python3
"""
Interactive CLI tool to tag a chart image with metadata and append to the Chart Bible CSV.
Usage: python tag-chart.py <image_path>
"""

import csv
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT_DIR / "data" / "chart-bible-schema.csv"

PATTERN_TYPES = [
    "cup-with-handle", "flat-base", "double-bottom", "ascending-base",
    "high-tight-flag", "bull-flag", "VCP", "IPO-base", "channel-breakout",
    "wedge", "triangle", "other"
]

SOURCES = [
    "qullamaggie", "dan-zanger", "thechartist", "minervini-vol1",
    "minervini-vol2", "personal", "other"
]

OUTCOMES = ["winner", "failed", "unknown"]


def prompt_choice(label, options):
    print(f"\n{label}:")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("  Select #: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("  Invalid choice, try again.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python tag-chart.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    print(f"\nTagging: {image_path}")

    ticker = input("\nTicker: ").strip().upper()
    entry_date = input("Date (YYYY-MM-DD): ").strip()
    exit_date = input("Exit date (or blank): ").strip()
    pattern_type = prompt_choice("Pattern type", PATTERN_TYPES)
    source = prompt_choice("Source", SOURCES)
    sector = input("Sector: ").strip()
    volume_confirmed = input("Volume confirmed (Y/N): ").strip().upper()
    outcome = prompt_choice("Outcome", OUTCOMES)
    pct_move = input("% move at pivot: ").strip()
    notes = input("Notes: ").strip()

    row = {
        "ticker": ticker,
        "entry_date": entry_date,
        "exit_date": exit_date,
        "pattern_type": pattern_type,
        "source": source,
        "sector": sector,
        "volume_confirmed": volume_confirmed,
        "outcome": outcome,
        "pct_move_at_pivot": pct_move,
        "chart_image_path": image_path,
        "notes": notes,
    }

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CSV_PATH.exists() and CSV_PATH.stat().st_size > 0
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"\nAdded {ticker} ({entry_date}) to {CSV_PATH}")


if __name__ == "__main__":
    main()
