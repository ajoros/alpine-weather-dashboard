#!/usr/bin/env python3
"""
Generate Index Script
Creates a JSON index of available screenshots for the web dashboard
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

def parse_filename_timestamp(filename):
    """Extract timestamp from screenshot filename"""
    # Format: STATIONID_YYYYMMDD_HHMMSS.png
    match = re.search(r'(\d{8}_\d{6})', filename)
    if match:
        timestamp_str = match.group(1)
        return datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
    return None

def generate_screenshot_index():
    """Generate an index of all available screenshots"""
    screenshots_dir = Path("screenshots")
    
    if not screenshots_dir.exists():
        return {}
    
    # Group screenshots by station ID
    screenshots_by_station = {}
    
    for png_file in screenshots_dir.glob("*.png"):
        # Parse filename to extract station ID and timestamp
        # Handle complex station IDs like NOAA_DESI_ALPINE_YYYYMMDD_HHMMSS
        parts = png_file.stem.split('_')
        if len(parts) >= 3:
            # Find the timestamp part (should be YYYYMMDD_HHMMSS at the end)
            timestamp_match = None
            for i in range(len(parts) - 1):
                if len(parts[i]) == 8 and parts[i].isdigit() and len(parts[i+1]) == 6 and parts[i+1].isdigit():
                    # Found timestamp, everything before this is station ID
                    station_id = '_'.join(parts[:i])
                    screenshot_type = 'full_page' if station_id.startswith('NOAA_DESI') else 'single'
                    timestamp_match = True
                    break
            
            if not timestamp_match:
                # Fallback to original logic
                station_id = parts[0]
                screenshot_type = 'single'
            
            timestamp = parse_filename_timestamp(png_file.name)
            
            if timestamp:
                if station_id not in screenshots_by_station:
                    screenshots_by_station[station_id] = []
                
                screenshots_by_station[station_id].append({
                    'filename': png_file.name,
                    'path': f'screenshots/{png_file.name}',
                    'timestamp': timestamp.isoformat(),
                    'size': png_file.stat().st_size,
                    'type': screenshot_type
                })
    
    # Sort screenshots by timestamp (newest first) for each station
    for station_id in screenshots_by_station:
        screenshots_by_station[station_id].sort(
            key=lambda x: x['timestamp'], 
            reverse=True
        )
    
    return screenshots_by_station

def create_web_index():
    """Create web-accessible index file"""
    screenshots_index = generate_screenshot_index()
    
    # Create a simplified index for web consumption
    web_index = {
        'last_updated': datetime.now().isoformat(),
        'stations': {}
    }
    
    for station_id, screenshots in screenshots_index.items():
        if screenshots:  # Only include stations with screenshots
            # All stations now use single screenshot approach
            latest = screenshots[0]  # First item is most recent
            web_index['stations'][station_id] = {
                'latest_screenshot': latest,
                'total_screenshots': len(screenshots),
                'all_screenshots': screenshots[:15],  # Keep more for comprehensive view
                'has_multiple_views': False,
                'is_full_page': station_id.startswith('NOAA_DESI')
            }
    
    # Write index file
    with open('screenshots_index.json', 'w') as f:
        json.dump(web_index, f, indent=2)
    
    print(f"Generated index with {len(web_index['stations'])} stations")
    return web_index

if __name__ == "__main__":
    create_web_index()