#!/bin/bash

# Cleanup script to remove screenshots older than 2 days (48 hours)
# Run this locally to keep your repository clean
# Uses filename-based dates for reliable cleanup

echo "🧹 Cleaning up old screenshots (older than 2 days by filename date)..."
echo ""

# Run the Python cleanup script
python cleanup_by_date.py

if [ $? -eq 0 ]; then
    echo ""
    echo "💡 Tip: Run 'python ../generate_index.py' to update the screenshots index"
    echo "💡 Then commit and push: git add -A && git commit -m 'Cleanup old screenshots' && ./push.sh"
else
    echo "❌ Cleanup failed. Check if Python is installed and cleanup_by_date.py exists."
    exit 1
fi
