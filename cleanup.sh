#!/bin/bash

# Cleanup script to remove screenshots older than 2 days (48 hours)
# Run this locally to keep your repository clean

echo "🧹 Cleaning up old screenshots (older than 2 days)..."

# Count files before cleanup
OLD_PNG_COUNT=$(find screenshots/ -name "*.png" -mtime +2 | wc -l | tr -d ' ')
OLD_JSON_COUNT=$(find screenshots/ -name "metadata_*.json" -mtime +2 | wc -l | tr -d ' ')

if [ "$OLD_PNG_COUNT" -eq 0 ] && [ "$OLD_JSON_COUNT" -eq 0 ]; then
    echo "✅ No old files to clean up. Repository is already clean!"
    exit 0
fi

echo "Found $OLD_PNG_COUNT old screenshot(s) and $OLD_JSON_COUNT old metadata file(s)"

# Delete old screenshots
find screenshots/ -name "*.png" -mtime +2 -delete
find screenshots/ -name "metadata_*.json" -mtime +2 -delete

# Count remaining files
REMAINING=$(find screenshots/ -name "*.png" | wc -l | tr -d ' ')

echo "✅ Cleanup complete! $REMAINING screenshot(s) remaining (last 2 days)"
echo ""
echo "💡 Tip: Run 'python generate_index.py' to update the screenshots index"
