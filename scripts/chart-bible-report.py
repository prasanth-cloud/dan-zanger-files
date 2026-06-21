#!/usr/bin/env python3
"""
Generates a summary report of the Chart Bible database.
Shows counts by source, pattern type, outcome, and sector.
"""

import csv
from collections import Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT_DIR / "data" / "chart-bible-schema.csv"


def main():
    if not CSV_PATH.exists():
        print("No chart-bible-schema.csv found. Tag some charts first.")
        return

    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Database is empty. Use tag-chart.py to add entries.")
        return

    total = len(rows)
    print(f"\n{'='*50}")
    print(f"  CHART BIBLE SUMMARY — {total} entries")
    print(f"{'='*50}\n")

    for field, label in [
        ("source", "By Source"),
        ("pattern_type", "By Pattern"),
        ("outcome", "By Outcome"),
        ("sector", "By Sector"),
    ]:
        counts = Counter(r.get(field, "").strip() for r in rows if r.get(field, "").strip())
        if counts:
            print(f"  {label}:")
            for val, count in counts.most_common(10):
                bar = "█" * min(count, 30)
                print(f"    {val:<20} {count:>4}  {bar}")
            print()

    winners = sum(1 for r in rows if r.get("outcome") == "winner")
    failed = sum(1 for r in rows if r.get("outcome") == "failed")
    if winners + failed > 0:
        win_rate = winners / (winners + failed) * 100
        print(f"  Win Rate: {win_rate:.1f}% ({winners}W / {failed}L)")

    print()


if __name__ == "__main__":
    main()
