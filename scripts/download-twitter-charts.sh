#!/usr/bin/env bash
# Downloads chart images from trading educators on Twitter/X using gallery-dl
# Requires: gallery-dl (pip install gallery-dl), valid Twitter cookies

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG="$SCRIPT_DIR/gallery-dl-config.json"

ACCOUNTS=(
  "qullamaggie"
  "DanZangerLive"
  "thechartist"
)

for account in "${ACCOUNTS[@]}"; do
  echo "=== Downloading media from @${account} ==="
  gallery-dl \
    --config "$CONFIG" \
    --dest "$ROOT_DIR/charts/" \
    "https://twitter.com/${account}/media"
done

echo "Done. Charts saved to $ROOT_DIR/charts/"
