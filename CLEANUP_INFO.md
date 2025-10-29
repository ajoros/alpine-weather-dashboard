# Screenshot Cleanup Documentation

## 🗓️ **Cleanup Schedule**

### Automated Cleanup (GitHub Actions)
- **Frequency**: Every 4 hours
- **Runs at**: 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC
- **Location**: `.github/workflows/update-weather.yml`
- **Code**: Line 48-50
  ```yaml
  - name: Clean up old screenshots (older than 48 hours)
    run: |
      python cleanup_by_date.py
  ```

### Manual Cleanup (Local)
- **When**: Run manually when needed
- **Command**: `./cleanup.sh`
- **Code**: Uses `cleanup_by_date.py` script

---

## 🧹 **Cleanup Scripts**

### 1. `cleanup_by_date.py` (Primary Cleanup Script)
**Location**: `web-dashboard/cleanup_by_date.py`

**How it works**:
- Parses date from filename (e.g., `KCASQUAW15_20251029_044838.png`)
- Extracts date: `20251029` → October 29, 2025
- Deletes files where date is older than 2 days from today
- Works reliably across git checkouts (doesn't use file modification time)

**Usage**:
```bash
python cleanup_by_date.py
```

**What it deletes**:
- `screenshots/*.png` older than 2 days (by filename date)
- `screenshots/metadata_*.json` older than 2 days (by filename date)

**Keeps**:
- Only files from the last 2 days (48 hours)
- Typically 80-100 screenshot files

---

### 2. `cleanup.sh` (Convenience Script)
**Location**: `web-dashboard/cleanup.sh`

**What it does**:
1. Runs `cleanup_by_date.py`
2. Shows summary of deleted/kept files
3. Provides helpful tips for next steps

**Usage**:
```bash
./cleanup.sh
```

**After cleanup**:
```bash
# Regenerate the index
python ../generate_index.py

# Commit and push changes
git add -A
git commit -m "Cleanup old screenshots"
./push.sh
```

---

## 📊 **Retention Policy**

| Item | Retention Period |
|------|-----------------|
| Screenshots (*.png) | 2 days |
| Metadata files | 2 days |
| screenshots_index.json | Always kept (regenerated) |

---

## 🔄 **Cleanup Flow**

### GitHub Actions (Automated):
```
Every 4 hours:
  1. Capture new weather screenshots (8 locations)
  2. Run cleanup_by_date.py (delete >2 day old files)
  3. Regenerate screenshots_index.json
  4. Commit & push to GitHub
  5. GitHub Pages updates automatically
```

### Local Cleanup (Manual):
```
When you run ./cleanup.sh:
  1. Runs cleanup_by_date.py
  2. Shows what was deleted
  3. Suggests regenerating index
  4. You manually commit & push
```

---

## 📁 **File Locations**

- **Cleanup scripts**: `web-dashboard/cleanup_by_date.py`, `web-dashboard/cleanup.sh`
- **GitHub Actions**: `web-dashboard/.github/workflows/update-weather.yml`
- **Screenshots**: `web-dashboard/screenshots/`
- **Index generator**: `weather-dashboard-automation/generate_index.py`

---

## 💡 **Why Filename-Based Cleanup?**

**Old method** (`find -mtime +2`):
- ❌ Uses file modification time
- ❌ Gets reset when files are checked out from git
- ❌ Unreliable across different machines

**New method** (filename parsing):
- ✅ Reads date directly from filename
- ✅ Always accurate regardless of git operations
- ✅ Works the same everywhere

---

## 🚨 **Troubleshooting**

### If cleanup isn't working:
1. Check if `cleanup_by_date.py` exists
2. Make sure Python 3 is installed
3. Verify filenames match pattern: `STATION_YYYYMMDD_HHMMSS.png`

### If repository size is growing:
1. Run `./cleanup.sh` locally
2. Check GitHub Actions logs: https://github.com/ajoros/alpine-weather-dashboard/actions
3. Verify cleanup step is running in workflow

### If you see old screenshots online:
1. Wait 5-10 minutes for GitHub Pages to update after push
2. Hard refresh the page (Cmd+Shift+R on Mac, Ctrl+F5 on Windows)
3. Check that cleanup committed and pushed successfully

---

## 📈 **Expected Repository Size**

- **With 2-day retention**: ~20-30 MB
- **Number of screenshots**: 80-100 files
- **Per location**: 10-12 screenshots (6 captures/day × 2 days)

---

## ⏰ **Next Cleanup Times** (Approximate)

GitHub Actions runs every 4 hours at:
- 00:00 UTC (5:00 PM PDT)
- 04:00 UTC (9:00 PM PDT)
- 08:00 UTC (1:00 AM PDT)
- 12:00 UTC (5:00 AM PDT)
- 16:00 UTC (9:00 AM PDT)
- 20:00 UTC (1:00 PM PDT)

*Times shown for Pacific Daylight Time (PDT/UTC-7)*
