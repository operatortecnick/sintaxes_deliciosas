#!/bin/bash
# Startup script for GitHub Search Application

echo "🚀 Starting GitHub Repository Search Application..."
echo "📦 Installing dependencies..."

# Install Python dependencies
pip install -r requirements.txt

# Install tkinter if not available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "📦 Installing tkinter..."
    sudo apt update && sudo apt install -y python3-tk
fi

echo "✅ Dependencies installed successfully!"
echo "🎯 Launching application..."

# Run the application
python3 github_search_app.py