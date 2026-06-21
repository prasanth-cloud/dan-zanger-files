# Chart Bible — Momentum Breakout Pattern Database

A structured collection of annotated chart patterns from top momentum traders, built for pattern recognition training.

## Sources

| Phase | Source | Method |
|-------|--------|--------|
| 1 | @qullamaggie (Twitter, YouTube, blog) | gallery-dl + yt-dlp |
| 2 | @DanZangerLive, @thechartist, chartpattern.com | gallery-dl + scraper |
| 3 | Minervini Vol 1 & 2 | Manual scan/photograph |

## Quick Start

```bash
pip install -r requirements.txt

# Phase 1 & 2: Download Twitter chart images
# First, configure Twitter cookies in scripts/gallery-dl-config.json
bash scripts/download-twitter-charts.sh

# Phase 2: Scrape chartpattern.com winners
python scripts/scrape-chartpattern-winners.py

# Tag any chart image
python scripts/tag-chart.py charts/qullamaggie/some_image.jpg
```

## Tagging Schema

Every chart entry gets tagged with:

| Field | Values |
|-------|--------|
| Pattern type | cup-with-handle, flat-base, double-bottom, ascending-base, high-tight-flag, bull-flag, VCP, IPO-base, channel-breakout, wedge, triangle |
| Source | qullamaggie, dan-zanger, thechartist, minervini-vol1, minervini-vol2 |
| Ticker | Stock symbol |
| Date | Entry date |
| Sector | Industry sector |
| Volume confirmed | Y/N |
| Outcome | winner / failed / unknown |
| % move at pivot | Percentage gain from breakout |
| Notes | Free text |

## Directory Structure

```
charts/
  qullamaggie/       # Phase 1 downloads
  dan-zanger/        # Phase 2 downloads
    winners/         # chartpattern.com scraped charts
  thechartist/       # Phase 2 downloads
  minervini/         # Phase 3 scanned pages
data/
  chart-bible-schema.csv   # Master database
  winners.csv              # chartpattern.com winners
  minervini-sepa-checklist.md  # VCP qualification criteria
scripts/
  download-twitter-charts.sh
  scrape-chartpattern-winners.py
  tag-chart.py
  gallery-dl-config.json
```

## Phase 4: Database Options

The CSV serves as a portable starting point. For a richer UI, import into:
- **Notion** — Gallery view with tag filters (fastest to set up)
- **Airtable** — Grid + gallery + advanced filtering by outcome/pattern
- **AlphaVyuh** — Custom "Chart Bible" module alongside watchlist & journal
