#!/bin/bash

# Setup cron job for automated local screenshot cleanup
# Runs every 4 hours

SCRIPT_DIR="/Users/Andrew.Joros@dri.edu/weather-dashboard-automation/web-dashboard"
CRON_CMD="0 */4 * * * cd $SCRIPT_DIR && /usr/bin/python3 cleanup_by_date.py >> cleanup_cron.log 2>&1"

echo "🔧 Setting up automated local cleanup (every 4 hours)..."
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "cleanup_by_date.py"; then
    echo "⚠️  Cron job already exists!"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep "cleanup_by_date.py"
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled. Existing cron job unchanged."
        exit 0
    fi
    # Remove old cron job
    crontab -l | grep -v "cleanup_by_date.py" | crontab -
    echo "✅ Removed old cron job"
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job installed successfully!"
    echo ""
    echo "📋 Cleanup schedule:"
    echo "   • Runs every 4 hours: 00:00, 04:00, 08:00, 12:00, 16:00, 20:00"
    echo "   • Deletes screenshots older than 2 days"
    echo "   • Logs to: $SCRIPT_DIR/cleanup_cron.log"
    echo ""
    echo "📝 To view your cron jobs:"
    echo "   crontab -l"
    echo ""
    echo "📝 To remove this cron job:"
    echo "   crontab -l | grep -v cleanup_by_date.py | crontab -"
    echo ""
    echo "📝 To view cleanup logs:"
    echo "   tail -f $SCRIPT_DIR/cleanup_cron.log"
else
    echo "❌ Failed to install cron job"
    exit 1
fi
