#!/usr/bin/env python3
"""
Cleanup script that removes screenshots older than 2 days
based on the timestamp in the filename, not file modification time.
This works reliably across git checkouts.
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

def cleanup_old_screenshots(days_to_keep=2):
    """Remove screenshots older than specified days based on filename timestamp"""
    screenshots_dir = Path("screenshots")
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    # Pattern to extract date from filename: STATION_20251023_123456.png
    pattern = re.compile(r'_(\d{8})_\d{6}\.(png|json)$')
    
    deleted_count = 0
    kept_count = 0
    
    for file in screenshots_dir.glob("*"):
        if not file.is_file():
            continue
            
        match = pattern.search(file.name)
        if match:
            date_str = match.group(1)  # e.g., "20251023"
            try:
                file_date = datetime.strptime(date_str, "%Y%m%d")
                
                if file_date < cutoff_date:
                    print(f"Deleting old file: {file.name} (from {file_date.strftime('%Y-%m-%d')})")
                    file.unlink()
                    deleted_count += 1
                else:
                    kept_count += 1
            except ValueError:
                print(f"Warning: Could not parse date from {file.name}")
    
    print(f"\n✅ Cleanup complete!")
    print(f"   Deleted: {deleted_count} files")
    print(f"   Kept: {kept_count} files (last {days_to_keep} days)")
    
    return deleted_count

if __name__ == "__main__":
    cleanup_old_screenshots(days_to_keep=2)
