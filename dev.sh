#!/bin/bash

# Typst Local Development Script

set -e

echo "🔧 Typst Local Development"
echo "=========================="

# Build the project using Python build script
python3 build.py local

echo ""
echo "🌐 Starting local server..."
echo "📍 Open: http://localhost:8000"
echo "⏹️  Press Ctrl+C to stop"

# Start local server
if command -v python3 &> /dev/null; then
    cd dist && python3 -m http.server 8000
elif command -v python &> /dev/null; then
    cd dist && python -m http.server 8000
elif command -v npx &> /dev/null; then
    cd dist && npx serve -p 8000
else
    echo "❌ No HTTP server available. Please install Python or Node.js"
    echo "📂 You can manually open: dist/index.html"
    exit 1
fi 