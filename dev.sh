#!/bin/bash
# Typst Academic Homepage Development Script
set -e

echo "🎓 Typst Academic Homepage Development"
echo "====================================="

# Check if Typst is installed
if ! command -v typst &> /dev/null; then
    echo "❌ Typst not found. Please install Typst first:"
    echo "   Visit: https://typst.app/"
    exit 1
fi

echo "🔍 Typst version: $(typst --version)"
echo ""

# Build the project using Python build script
echo "🔨 Building homepage with integrated Typst content..."
python3 build.py

echo ""
echo "🌐 Starting local development server..."
echo "📄 Homepage: http://localhost:8000"
echo "📖 Blog: http://localhost:8000/blog/"
echo "⏹️  Press Ctrl+C to stop"
echo ""
echo "💡 To edit content:"
echo "   - About section: src/about.typ"
echo "   - News section: src/news.typ"  
echo "   - CV section: src/cv.typ"
echo "   - Blog posts: blog/*.typ"
echo ""

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