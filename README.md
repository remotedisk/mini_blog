# Mini Blog - Typst to HTML

This repository contains a Typst document that is automatically compiled to HTML using GitHub Actions.

## 📋 What this does

The GitHub workflow automatically:
- Compiles `test.typ` to HTML using Typst's native HTML export (experimental)
- Creates a simple index page that redirects to the HTML document
- Deploys the HTML document to GitHub Pages for web viewing

## 🚀 Getting Started

### Prerequisites
- A GitHub repository with this code
- GitHub Pages enabled in repository settings

### Setup Instructions

1. **Enable GitHub Pages:**
   - Go to your repository settings
   - Navigate to "Pages" in the left sidebar
   - Under "Source", select "Deploy from a branch"
   - Choose "gh-pages" as the branch
   - Click "Save"

2. **Push your changes:**
   ```bash
   git add .
   git commit -m "Add Typst to HTML workflow"
   git push origin main
   ```

3. **The workflow will automatically run and:**
   - Build Typst from source (first run takes ~10-15 minutes)
   - Compile your document to HTML
   - Deploy to GitHub Pages
   - Make it available at: `https://yourusername.github.io/yourrepository`
   
   ⏱️ **Note**: The first build will take longer as it compiles Typst from source, but subsequent builds will be cached and much faster.

## 📁 Output Formats

The workflow generates:

- **HTML**: Native Typst HTML export with semantic markup (`test.html`) - *Experimental*
- **Index Page**: Simple redirect page to the HTML document (`index.html`)

## 🔧 Workflow Details

### Triggers
The workflow runs on:
- Push to `main` or `master` branch
- Pull requests to `main` or `master` branch
- Manual trigger via GitHub Actions tab

### Build Process
1. **Setup**: Installs Rust toolchain and builds Typst from source
2. **Compile**: Generates HTML using native Typst HTML export
3. **Package**: Creates artifacts and simple index page
4. **Deploy**: Publishes to GitHub Pages (on main branch only)

### Typst Reference Configuration
The workflow builds Typst from source using a specific git reference. To change the reference:

1. Edit `.github/workflows/build-typst.yml`
2. Modify the `TYPST_REF` environment variable at the top:
   ```yaml
   env:
     TYPST_REF: v0.11.0  # Change this to your desired reference
   ```

**Available reference options:**
- **Release tags**: `v0.11.0`, `v0.10.0`, `v0.9.0`, etc.
- **Latest development**: `main`
- **Specific commits**: Any commit hash from the Typst repository (e.g., `8ace67d9`, `a1b2c3d4e5f6`)
- **Branches**: Any branch name (e.g., `main`, `dev`, `experimental`)

**Benefits of building from source:**
- Access to the latest features and bug fixes
- Ability to use development versions
- Full control over the exact Typst version
- Access to experimental features like HTML export

### Examples

**Using a specific commit hash:**
```yaml
env:
  TYPST_REF: 8ace67d9  # Specific commit for reproducible builds
```

💡 **Finding commit hashes**: Visit the [Typst repository commits page](https://github.com/typst/typst/commits/main) to find specific commit hashes. You can use either the full hash or the short 8-character version.

**Using the latest development version:**
```yaml
env:
  TYPST_REF: main  # Latest development version
```

**Using a stable release:**
```yaml
env:
  TYPST_REF: v0.11.0  # Stable release tag
```

### Artifacts
After each workflow run, you can download:
- The generated HTML document and assets as a zip archive

## 📝 Customizing

### Adding More Files
To compile additional `.typ` files:
1. Add them to your repository
2. Modify the workflow file (`.github/workflows/build-typst.yml`)
3. Add compilation steps for each file

### Changing Typst Source
To use a different Typst reference (version, commit, or branch):
1. Edit the `TYPST_REF` environment variable in the workflow
2. Choose from release tags, commit hashes, or branch names

### Changing Output Location
The workflow currently processes `test.typ`. To change this:
1. Update the file paths in the workflow
2. Modify the `index.html` generation section

### Styling
The generated HTML includes basic styling. You can customize:
- The SVG wrapper styling in the workflow
- The index page appearance
- Add your own CSS files

## 🛠️ Troubleshooting

### Common Issues

**Workflow fails on first run:**
- Check that GitHub Pages is enabled in repository settings
- Ensure the repository is public (or GitHub Pages is available for private repos)

**Images not displaying:**
- Make sure image files (like `glacier.jpg`) are committed to the repository
- Check that image paths in the `.typ` file are correct

**HTML export issues:**
- **Experimental feature**: HTML export is still under development and may have limitations
- **Missing features**: Some Typst elements may not be fully supported in HTML export yet
- **Styling**: HTML output focuses on semantic markup; CSS styling needs to be added separately
- **Browser compatibility**: Modern browsers should display the HTML correctly

**Build from source issues:**
- **Build timeout**: The Rust compilation can take 10-15 minutes; this is normal
- **Reference not found**: Check that the reference exists in the [Typst repository](https://github.com/typst/typst)
  - For tags: Check [releases](https://github.com/typst/typst/tags)
  - For commits: Verify the commit hash exists in the repository
  - For branches: Ensure the branch name is correct
- **Build fails**: Try using a stable release tag instead of `main` branch or commit hashes
- **Cache issues**: If builds are inconsistent, the cache key includes the git reference to avoid conflicts

### Logs and Debugging
- Check the "Actions" tab in your GitHub repository
- Review workflow logs for specific error messages
- Build times: Expect 10-15 minutes for Typst compilation (first time), subsequent builds with cache are faster
- Artifacts are available for download even if deployment fails

## 📋 File Structure

```
mini_blog/
├── .github/
│   └── workflows/
│       └── build-typst.yml    # GitHub Actions workflow
├── test.typ                   # Your Typst document
├── glacier.jpg               # Image asset
└── README.md                 # This file
```

## 🌐 Live Demo

Once deployed, your document will be available at:
`https://yourusername.github.io/yourrepository`

The index page will automatically redirect to the HTML version of your document. 