#!/usr/bin/env bash
# Downloads Qullamaggie YouTube livestream recordings where he annotates trades
# Requires: yt-dlp (pip install yt-dlp)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$ROOT_DIR/charts/qullamaggie/youtube"
ARCHIVE_FILE="$OUTPUT_DIR/.downloaded.txt"

mkdir -p "$OUTPUT_DIR"

CHANNEL_URL="https://www.youtube.com/@Qullamaggie/videos"

echo "=== Downloading Qullamaggie YouTube videos ==="
yt-dlp \
  --download-archive "$ARCHIVE_FILE" \
  --output "$OUTPUT_DIR/%(upload_date)s_%(title)s.%(ext)s" \
  --write-thumbnail \
  --write-info-json \
  --format "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --merge-output-format mp4 \
  --sleep-interval 3 \
  --max-sleep-interval 8 \
  "$CHANNEL_URL"

echo "Done. Videos saved to $OUTPUT_DIR"
