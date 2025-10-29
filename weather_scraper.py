#!/usr/bin/env python3
"""
Weather Underground Screenshot Automation Script
Captures weather forecast screenshots from multiple Weather Underground locations
"""

import os
import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class WeatherScraper:
    def __init__(self, config_file="locations.json"):
        self.config_file = config_file
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        self.locations = self.load_locations()
    
    def load_locations(self):
        """Load weather station locations from config file"""
        default_locations = [
            {
                "name": "Alpine Meadows",
                "url": "https://www.wunderground.com/forecast/us/ca/alpine-meadows/KCASQUAW15",
                "station_id": "KCASQUAW15"
            }
        ]
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config file: {e}")
                return default_locations
        else:
            # Create default config file
            with open(self.config_file, 'w') as f:
                json.dump(default_locations, f, indent=2)
            return default_locations
    
    async def capture_screenshot(self, location, browser):
        """Capture screenshot for a single location"""
        try:
            page = await browser.new_page()
            
            # Set user agent to look like a regular browser
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # Set viewport size for consistent screenshots
            if 'noaa.gov' in location['url'] or 'desi' in location['url']:
                await page.set_viewport_size({"width": 1600, "height": 1200})  # Wider for NOAA DESI
            else:
                await page.set_viewport_size({"width": 1200, "height": 800})
            
            print(f"Capturing screenshot for {location['name']}...")
            
            # Navigate to the weather page
            await page.goto(location['url'], wait_until='domcontentloaded', timeout=60000)
            
            # Simple wait for NOAA DESI or other sites
            if 'noaa.gov' in location['url'] or 'desi' in location['url']:
                print(f"  Waiting for NOAA DESI content to fully load: {location['name']}")
                await page.wait_for_timeout(16000)  # 16 second wait for plots to render
            else:
                await page.wait_for_timeout(3000)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{location['station_id']}_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            
            # Take screenshot based on site type
            try:
                if 'noaa.gov' in location['url'] or 'desi' in location['url']:
                    # For NOAA DESI, take a simple full page screenshot
                    print(f"  Taking full page screenshot for NOAA DESI...")
                    
                    # Take full page screenshot - this should capture everything
                    await page.screenshot(path=str(filepath), full_page=True)
                    print(f"  Captured NOAA DESI page: {filepath}")
                    
                    return str(filepath)
                else:
                    # For Weather Underground, try to find the forecast container
                    forecast_element = page.locator('[class*="forecast"]').first
                    if await forecast_element.count() > 0:
                        await forecast_element.screenshot(path=str(filepath))
                    else:
                        # If specific element not found, take full page screenshot
                        await page.screenshot(path=str(filepath), full_page=True)
            except Exception as e:
                print(f"  Screenshot error for {location['name']}: {e}")
                # Fallback to full page screenshot
                await page.screenshot(path=str(filepath), full_page=True)
            
            print(f"Screenshot saved: {filepath}")
            
            await page.close()
            return str(filepath)
            
        except Exception as e:
            print(f"Error capturing screenshot for {location['name']}: {e}")
            if 'page' in locals():
                await page.close()
            return None
    
    async def capture_all_locations(self):
        """Capture screenshots for all configured locations"""
        print(f"Starting screenshot capture at {datetime.now()}")
        
        async with async_playwright() as p:
            # Launch browser in headless mode with additional options
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            screenshot_paths = []
            
            for location in self.locations:
                result = await self.capture_screenshot(location, browser)
                if result:
                    # All locations now return single screenshots
                    screenshot_paths.append({
                        'location': location['name'],
                        'path': result,
                        'timestamp': datetime.now().isoformat(),
                        'screenshot_type': 'full_page' if 'noaa.gov' in location['url'] or 'desi' in location['url'] else 'single'
                    })
            
            await browser.close()
        
        # Save metadata about captured screenshots
        metadata = {
            'capture_time': datetime.now().isoformat(),
            'screenshots': screenshot_paths
        }
        
        metadata_file = self.screenshots_dir / f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Captured {len(screenshot_paths)} screenshots")
        return screenshot_paths
    
    def cleanup_old_screenshots(self, days_to_keep=7):
        """Remove screenshots older than specified days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for file in self.screenshots_dir.glob("*.png"):
            if file.stat().st_mtime < cutoff_date.timestamp():
                file.unlink()
                print(f"Removed old screenshot: {file}")

async def main():
    scraper = WeatherScraper()
    
    # Capture screenshots
    await scraper.capture_all_locations()
    
    # Clean up old screenshots (keep last 2 days = 48 hours)
    scraper.cleanup_old_screenshots(days_to_keep=2)
    
    # Generate web index
    try:
        from generate_index import create_web_index
        create_web_index()
        print("Generated web index")
    except Exception as e:
        print(f"Error generating web index: {e}")

if __name__ == "__main__":
    asyncio.run(main())