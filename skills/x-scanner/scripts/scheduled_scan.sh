#!/usr/bin/env bash
# Scheduled X scan — runs via cron, saves digest to daily output file.
#
# Output goes to: <skill-directory>/digests/
# Filename format: YYYY-MM-DD_HHmm.txt

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIGEST_DIR="$SKILL_DIR/digests"
TIMESTAMP=$(TZ="America/New_York" date +"%Y-%m-%d_%H%M")
OUTFILE="$DIGEST_DIR/${TIMESTAMP}.txt"

mkdir -p "$DIGEST_DIR"

# Run the scan (last 12 hours by default)
python3 "$SKILL_DIR/scripts/scan_x.py" --summary-only > "$OUTFILE" 2>&1

# Also keep a "latest" symlink for easy access
ln -sf "$OUTFILE" "$DIGEST_DIR/latest.txt"

# Clean up digests older than 7 days
find "$DIGEST_DIR" -name "*.txt" -not -name "latest.txt" -mtime +7 -delete 2>/dev/null

# macOS notification
if command -v osascript &>/dev/null; then
  LINE_COUNT=$(wc -l < "$OUTFILE" | tr -d ' ')
  FLAGGED=$(grep -c '^\[FLAGGED\]' "$OUTFILE" 2>/dev/null || echo 0)
  osascript -e "display notification \"$FLAGGED flagged posts, $LINE_COUNT lines total\" with title \"X Scanner\" subtitle \"Digest ready\"" 2>/dev/null
fi
