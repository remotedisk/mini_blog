#!/bin/bash

# Shared Typst Build Script
# Usage: ./build.sh [local|production]

set -e

ENVIRONMENT=${1:-local}

echo "🔨 Building Typst project for $ENVIRONMENT environment..."
echo "================================================="

# Check if typst is installed
if ! command -v typst &> /dev/null; then
    echo "❌ Typst is not installed. Please install it first:"
    echo "   📦 From releases: https://github.com/typst/typst/releases"
    echo "   🦀 From source: cargo install --git https://github.com/typst/typst.git --rev 7278d887cf05fadc9a96478830e5876739b78f53 typst-cli"
    exit 1
fi

echo "📋 Using Typst version: $(typst --version)"

# Create dist directory
echo "📁 Creating dist directory..."
mkdir -p dist

echo ""
echo "🔨 Compiling blog/test.typ to HTML..."
TYPST_FEATURES=html typst compile blog/test.typ dist/test.html --format html --features html

echo "📄 Generating index.html from template..."
case $ENVIRONMENT in
    "local")
        ENVIRONMENT_TEXT="Local Development Version"
        BADGE_CLASS="local"
        BADGE_TEXT="LOCAL"
        DESCRIPTION="This document was compiled from Typst source code locally."
        ;;
    "production")
        ENVIRONMENT_TEXT="Production Version"
        BADGE_CLASS="experimental"
        BADGE_TEXT="EXPERIMENTAL"
        DESCRIPTION="This document was compiled from Typst source code using GitHub Actions and native Typst HTML export."
        ;;
    *)
        echo "❌ Invalid environment: $ENVIRONMENT"
        echo "Usage: $0 [local|production]"
        exit 1
        ;;
esac

# Generate HTML from template
sed \
    -e "s/{{ENVIRONMENT_TEXT}}/$ENVIRONMENT_TEXT/g" \
    -e "s/{{BADGE_CLASS}}/$BADGE_CLASS/g" \
    -e "s/{{BADGE_TEXT}}/$BADGE_TEXT/g" \
    -e "s/{{DESCRIPTION}}/$DESCRIPTION/g" \
    src/index-template.html > dist/index.html

echo "📦 Copying static assets..."

echo ""
echo "✅ Build complete!"
echo "📂 Output directory: ./dist/"
echo "📄 Files created:"
echo "   - dist/test.html (main document)"
echo "   - dist/index.html (redirect page - $ENVIRONMENT)"
echo "   - dist/* (static assets)" 