# Mini Blog - Typst to HTML

A simple blog setup that compiles Typst documents to HTML with GitHub Actions deployment.

## 🚀 Local Development

### Prerequisites

1. **Install Typst** (choose one option):

   **Option A: From releases (easier)**
   ```bash
   # Download from: https://github.com/typst/typst/releases
   # Add to your PATH
   ```

   **Option B: Build from source (exact commit used in CI)**
   ```bash
   cargo install --git https://github.com/typst/typst.git --rev 7278d887cf05fadc9a96478830e5876739b78f53 typst-cli
   ```

   **Option C: Using package managers**
   ```bash
   # macOS
   brew install typst
   
   # Arch Linux
   pacman -S typst
   
   # Or check: https://typst.app/docs/getting-started/
   ```

### Quick Start

1. **Build and serve:**
   ```bash
   chmod +x build.sh dev.sh
   ./dev.sh
   ```
   This will:
   - ✅ Build the project using `build.sh`
   - 📁 Create `dist/` folder with output
   - 🌐 Start local server at `http://localhost:8000`

2. **Just build (without server):**
   ```bash
   ./build.sh local
   ```

3. **Build for production:**
   ```bash
   ./build.sh production
   ```

### Manual Commands

```bash
# Build the project
./build.sh local

# Or manually:
mkdir -p dist
TYPST_FEATURES=html typst compile blog/test.typ dist/test.html --format html --features html
# ... (see build.sh for full process)

# Serve locally
python3 -m http.server 8000 -d dist
```

## 📁 Project Structure

```
mini_blog/
├── .github/workflows/
│   └── build-typst.yml     # GitHub Actions workflow
├── blog/
│   └── test.typ            # Your Typst documents
├── static/
│   └── glacier.jpg         # Static assets (images, etc.)
├── src/
│   └── index-template.html # HTML template for index page
├── dist/                   # Build output (auto-generated)
│   ├── test.html          # Compiled HTML
│   ├── index.html         # Generated redirect page
│   └── glacier.jpg        # Copied static assets
├── build.sh               # Shared build script
├── dev.sh                 # Development script with server
└── README.md              # This file
```

## 🔧 Development Workflow

1. **Edit** Typst documents in the `blog/` folder
2. **Add assets** (images, etc.) to the `static/` folder
3. **Customize** HTML templates in the `src/` folder
4. **Run** `./dev.sh` to build and serve
5. **Rebuild** with `./build.sh local` as needed
6. **Commit** changes to trigger GitHub Actions deployment

## 🌐 Production Deployment

The workflow automatically deploys to GitHub Pages when you push to the main branch:

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Set Source to "GitHub Actions"
   - Save

2. **Push changes:**
   ```bash
   git add .
   git commit -m "Update content"
   git push origin main
   ```

3. **View deployed site:**
   - `https://yourusername.github.io/yourrepository`

## 📝 Adding Content

### Text and Formatting
```typst
= Heading Level 1
== Heading Level 2

This is *bold* and _italic_ text.

- List item 1
- List item 2

$ sum_(i=1)^n x_i = x_1 + x_2 + ... + x_n $
```

### Images
Place images in the `static/` folder, then reference them:
```typst
#figure(
  image("../static/your-image.jpg", width: 150pt),
  caption: [Your image caption],
) <your-label>
```

### Tables
```typst
#table(
  columns: (auto, auto, auto),
  [Header 1], [Header 2], [Header 3],
  [Row 1], [Data], [More data],
  [Row 2], [Data], [More data],
)
```

## 🎨 Customizing the Template

The HTML template is modular and easy to customize:

1. **Edit the template**: `src/index-template.html`
2. **Template variables**:
   - `{{ENVIRONMENT_TEXT}}` - Environment description
   - `{{BADGE_CLASS}}` - CSS class for the badge
   - `{{BADGE_TEXT}}` - Text shown in the badge
   - `{{DESCRIPTION}}` - Footer description

The `build.sh` script automatically replaces these variables based on the environment (local/production).

### Example: Custom Badge Colors
Edit `src/index-template.html`:
```css
.local {
    background: #ff9500;  /* Orange for local */
}
.experimental {
    background: #28a745;  /* Green for production */
}
```

## 🛠️ Build Script

The `build.sh` script is the core of the build process:

```bash
# Usage
./build.sh [local|production]

# Examples
./build.sh local      # Local development build
./build.sh production # Production build for deployment
```

**What it does:**
- ✅ Checks Typst installation
- 🔨 Compiles Typst documents to HTML
- 📄 Generates index.html from template
- 📦 Copies static assets
- 🎯 Environment-specific configuration

## 🛠️ Troubleshooting

**Typst not found:**
- Make sure Typst is installed and in your PATH
- Try: `typst --version`

**Build script issues:**
- Make sure scripts are executable: `chmod +x build.sh dev.sh`
- Check that all required files exist: `blog/test.typ`, `src/index-template.html`, `static/`

**Template issues:**
- Check template syntax in `src/index-template.html`
- Ensure template variables use the correct `{{VARIABLE}}` format

**Local server issues:**
- Try different ports: `python3 -m http.server 3000 -d dist`
- Or use Node.js: `npx serve dist -p 3000`

## ⚡ Tips

- **Fast iteration**: Use `./dev.sh` for build + serve in one command
- **Version control**: The `dist/` folder is ignored by git (build artifacts)
- **Organized assets**: Keep images and other assets in the `static/` folder
- **Multiple documents**: Add more `.typ` files to the `blog/` folder and extend `build.sh`
- **Shared build logic**: Both local development and CI use the same `build.sh` script
- **Environment awareness**: The build script automatically adjusts styling for local vs. production

Enjoy writing with Typst! 🎉 