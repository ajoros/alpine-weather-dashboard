#!/bin/bash

# Helper script to safely push changes when GitHub Actions is also committing
# This handles the common case where automated commits conflict with manual commits

echo "🔄 Pulling latest changes from remote..."
git pull --no-rebase

if [ $? -eq 0 ]; then
    echo "✅ Pull successful! Now pushing..."
    git push
    
    if [ $? -eq 0 ]; then
        echo "🎉 Push successful!"
    else
        echo "❌ Push failed. You may need to resolve conflicts manually."
        exit 1
    fi
else
    echo "❌ Pull failed. You may need to resolve conflicts manually."
    exit 1
fi