# Typst Academic Homepage

A clean, academic-style homepage and blog system powered by [Typst](https://typst.app/) with modular content sections and automatic compilation. Perfect for researchers, academics, and professionals who want a beautiful, maintainable website.

## ✨ Features

- 🎓 **Academic Design** — Clean, professional layout inspired by academic websites
- ✍️ **Modular Content** — Separate Typst files for about, news, CV, and blog posts
- 🚀 **Auto Compilation** — GitHub Actions automatically builds and deploys
- 📱 **Responsive Design** — Mobile-friendly academic layout
- 🧮 **Math Support** — LaTeX-quality mathematical expressions
- 📊 **Bear Blog Styling** — Modern, clean typography with excellent readability

## 📁 Content Structure

Your content is organized in separate Typst files:

- **`src/about.typ`** — About section with bio and links
- **`src/news.typ`** — News and announcements 
- **`src/cv.typ`** — Publications, education, experience, awards
- **`blog/*.typ`** — Individual blog posts
- **`static/`** — Images and other assets

## 🚀 Local Development

### Prerequisites

1. **Install Python 3** (required for template processing):
   ```bash
   # Python 3 comes pre-installed on most systems
   python3 --version  # Check if installed
   
   # If not installed:
   # macOS: brew install python3
   # Ubuntu/Debian: apt install python3
   # Windows: Download from python.org
   ```

2. **Install Typst** (choose one option):

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

1. **Edit your content:**
   ```bash
   # Edit your bio and social links
   nano src/about.typ
   
   # Update your news and announcements
   nano src/news.typ
   
   # Add publications and CV information
   nano src/cv.typ
   
   # Create blog posts
   nano blog/my-new-post.typ
   ```

2. **Build and serve:**
   ```bash
   chmod +x dev.sh
   ./dev.sh
   ```
   This will:
   - ✅ Compile all Typst content (about, news, CV, blog posts)
   - 📁 Generate integrated homepage and blog
   - 📄 Create `dist/` folder with the complete site
   - 🌐 Start local server at `http://localhost:8000`

3. **Just build (without server):**
   ```bash
   python3 build.py local
   ```

4. **Build for production:**
   ```bash
   python3 build.py production
   ```

### Manual Commands

```bash
# Build the entire blog
python3 build.py local

# Serve locally
python3 -m http.server 8000 -d dist
```

## 📁 Project Structure

```
mini_blog/
├── .github/workflows/
│   └── build-typst.yml     # GitHub Actions workflow
├── blog/
│   ├── test.typ            # Example blog post
│   └── getting-started.typ # Another blog post
├── static/
│   └── glacier.jpg         # Static assets (images, etc.)
├── src/
│   ├── main-index.html     # Main page template
│   ├── blog-index.html     # Blog index template
│   ├── blog-post.html      # Individual blog post template
│   └── style.css           # Shared stylesheet
├── dist/                   # Build output (auto-generated)
│   ├── index.html          # Main page
│   ├── style.css           # Main stylesheet
│   ├── blog/
│   │   ├── index.html      # Blog index
│   │   ├── style.css       # Stylesheet (copy for blog pages)
│   │   ├── test.html       # Compiled blog posts
│   │   └── getting-started.html
│   └── glacier.jpg         # Copied static assets
├── build.py               # Blog build script (Python)
├── dev.sh                 # Development script with server
└── README.md              # This file
```

## 🔧 Development Workflow

1. **Write blog posts** in the `blog/` folder as `.typ` files
2. **Add metadata** to each post (see format below)
3. **Add assets** (images, etc.) to the `static/` folder
4. **Customize** templates in the `src/` folder
5. **Run** `./dev.sh` to build and serve
6. **Rebuild** with `python3 build.py local` as needed
7. **Commit** changes to trigger GitHub Actions deployment

## 📝 Writing Blog Posts

### Blog Post Format

Each blog post should be a `.typ` file in the `blog/` folder with metadata at the top:

```typst
// Blog Post Metadata
// title: Your Post Title
// date: YYYY-MM-DD
// author: Your Name
// excerpt: A brief description that appears in the blog index...

= Your Post Title

Your post content goes here in Typst format.

== Subheading

You can use all Typst features:
- Lists
- *Bold* and _italic_ text
- Math: $E = m c^2$
- Code blocks
- Tables
- Images
```

### Example Blog Post

```typst
// Blog Post Metadata
// title: Getting Started with Typst
// date: 2024-07-23
// author: Jane Doe
// excerpt: Learn the basics of writing beautiful documents with Typst markup language.

= Getting Started with Typst

Welcome to the world of beautiful typography!

== Math Support

Typst has excellent math support: $integral_0^infinity e^(-x^2) dif x = sqrt(pi)/2$

== Code Examples

```python
def hello_world():
    print("Hello from Typst!")
```
```

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

## 🎨 Customizing Templates and Styles

### Templates

The blog uses three main templates in the `src/` folder:

### 1. Main Index (`src/main-index.html`)
The homepage of your blog. Variables:
- `{{SITE_TITLE}}` - Site title
- `{{SITE_DESCRIPTION}}` - Site description
- `{{ABOUT_TEXT}}` - About section text
- `{{ENVIRONMENT}}` - Build environment

### 2. Blog Index (`src/blog-index.html`)
Lists all blog posts. Variables:
- `{{SITE_TITLE}}` - Site title
- `{{BLOG_POSTS}}` - Generated list of blog posts
- `{{ENVIRONMENT}}` - Build environment

### 3. Blog Post (`src/blog-post.html`)
Individual blog post layout. Variables:
- `{{SITE_TITLE}}` - Site title
- `{{POST_TITLE}}` - Post title
- `{{POST_DATE}}` - Post date
- `{{POST_AUTHOR}}` - Post author
- `{{POST_CONTENT}}` - Compiled Typst content
- `{{ENVIRONMENT}}` - Build environment

### Customizing Site Information

Edit the site configuration in `build.py`:
```python
site_config = {
    'title': "Your Blog Name",
    'description': "Your blog description", 
    'about': "About your blog..."
}
```

### Styles

The blog uses a clean, **academic-style design** inspired by professional academic homepages. The single shared stylesheet at `src/style.css` contains all the CSS for the entire site:

**Design Philosophy:**
- **Minimal & Clean**: White background, plenty of whitespace, subtle borders
- **Typography-focused**: Emphasis on readability and content hierarchy  
- **Academic Aesthetic**: Professional look suitable for research, writing, and academic content
- **No cards or shadows**: Flat design with simple borders and dividers

**Key sections:**
- **Base Styles**: Clean typography, generous line spacing, academic color palette
- **Layout Components**: Simple header, minimal navigation, content-focused layout
- **Blog Components**: Clean post listings without cards or heavy styling
- **Blog Post Page**: Academic paper-like styling with clear hierarchy
- **Typst Content**: Professional styling for academic content (headings, tables, code, math)

**Customizing styles:**
1. Edit `src/style.css` to modify the design
2. The build script automatically copies it to `dist/style.css` and `dist/blog/style.css`
3. All templates reference the external CSS file (no inline styles)

**Academic color palette:**
```css
/* Current academic color scheme */
body { background: #ffffff; color: #333; }
h1, h2, h3 { color: #000; }
.text-muted { color: #888; }
a { color: #007acc; }
borders: #e5e5e5
```

**Common customizations:**
```css
/* Adjust typography */
body {
    font-family: 'Georgia', 'Times New Roman', serif; /* More academic feel */
    font-size: 17px; /* Larger for better readability */
}

/* Customize link colors */
a { color: #2c5aa0; } /* Academic blue */

/* Modify content width */
body { max-width: 1000px; } /* Wider for more content */
```

## 🌐 Production Deployment

The workflow automatically deploys to GitHub Pages when you push to the main branch:

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Set Source to "GitHub Actions"
   - Save

2. **Push changes:**
   ```bash
   git add .
   git commit -m "Add new blog post"
   git push origin main
   ```

3. **View deployed site:**
   - `https://yourusername.github.io/yourrepository`

## 🛠️ Build Script

The `build.py` script handles the complete blog build process using Python for better reliability:

```bash
# Usage
python3 build.py [local|production]

# Examples
python3 build.py local      # Local development build
python3 build.py production # Production build for deployment
```

**What it does:**
- ✅ Scans `blog/` folder for `.typ` files
- 🔍 Extracts metadata from each post
- 🔨 Compiles each post to HTML using Typst
- 📝 Wraps compiled content in blog post template
- 📋 Generates blog index with all posts
- 🏠 Creates main index page
- 📦 Copies static assets
- 🎯 Environment-specific configuration
- 🐛 Better error handling and debugging output

## 🛠️ Troubleshooting

**Typst not found:**
- Make sure Typst is installed and in your PATH
- Try: `typst --version`

**Python not found:**
- Make sure Python 3 is installed and in your PATH
- Try: `python3 --version`

**Build script issues:**
- Make sure Python 3 is installed and accessible
- Check that blog posts have proper metadata format
- Ensure template files exist in `src/` folder
- Run `python3 build.py local` to see detailed error messages

**Blog post not appearing:**
- Check metadata format at the top of your `.typ` file
- Ensure the file is in the `blog/` folder
- Verify the date format is YYYY-MM-DD
- Rebuild with `python3 build.py local` for detailed debugging output

**Template issues:**
- Check template syntax in `src/` templates
- Ensure template variables use the correct `{{VARIABLE}}` format
- Check for typos in variable names

**Styling issues:**
- Ensure `src/style.css` exists and is valid CSS
- Check that CSS files are being copied to `dist/` and `dist/blog/`
- Verify CSS links in templates point to the correct relative paths
- Clear browser cache if styles aren't updating

**Local server issues:**
- Try different ports: `python3 -m http.server 3000 -d dist`
- Or use Node.js: `npx serve dist -p 3000`

## ⚡ Tips

- **Multiple posts**: Add as many `.typ` files as you want to the `blog/` folder
- **Chronological order**: Posts are sorted by filename, consider using date prefixes
- **Draft posts**: Remove or comment out metadata to exclude posts from the index
- **Rich content**: Use all Typst features - math, tables, figures, code blocks
- **Fast iteration**: Use `./dev.sh` for build + serve in one command
- **Version control**: The `dist/` folder is ignored by git (build artifacts)
- **Organized assets**: Keep images and other assets in the `static/` folder
- **Shared build logic**: Both local development and CI use the same `build.py` script
- **SEO friendly**: Each post gets its own HTML page with proper meta tags

## 🎯 Blog Features

- **📝 Academic writing**: Write in Typst markup language with LaTeX-quality output
- **🎨 Clean typography**: Professional, academic-style design focused on readability
- **📊 Math support**: Beautiful mathematical expressions with proper formatting
- **💻 Code highlighting**: Clean syntax highlighting for technical content
- **📱 Responsive design**: Mobile-friendly academic layout
- **🚀 Fast deployment**: Automatic GitHub Actions deployment to GitHub Pages
- **🔍 SEO friendly**: Proper HTML structure and semantic markup
- **📑 Blog index**: Clean, academic-style post listing
- **🏷️ Metadata support**: Title, date, author, excerpt for each post
- **🎓 Academic aesthetic**: Inspired by professional academic homepages like [Xiaotian Han's site](https://ahxt.github.io/)

Perfect for researchers, academics, and anyone who appreciates clean, professional design! 🎓 