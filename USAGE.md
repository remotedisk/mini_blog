# Typst Academic Homepage Usage Guide

## 📝 Content Editing

### About Section (`src/about.typ`)
Contains your bio, contact information, and social links:

```typst
Hi there!

I am an Assistant Professor of Computer Science at Case Western Reserve University from Fall 2024. I completed my Ph.D. at Texas A&M University. My research focuses on machine learning, large language models (LLMs). You can contact me via #link("mailto:your-email@university.edu")[your-email (at) university.edu].

#link("https://scholar.google.com/")[google scholar] / #link("https://twitter.com/yourhandle")[𝕏] / #link("https://github.com/yourusername")[github] / #link("/cv.pdf")[cv]
```

### News Section (`src/news.typ`)
Recent announcements and updates:

```typst
=== 🔥 News
- *2024.07*: New paper accepted at #link("https://conference.com")[Conference 2024]!
- *2024.06*: Started new position at University!
- *2024.05*: Paper wins best paper award at #link("https://venue.com")[Venue 2024]!

#html.elem("details")[
  #html.elem("summary", attrs: (style: "color: rgba(74, 99, 199, 1)"))[
    More...
  ]
  - *2024.04*: Older news item
  - *2024.03*: Even older news
]
```

### CV Section (`src/cv.typ`)
Publications, education, experience, and awards:

```typst
=== Selected Publications(#link("https://scholar.google.com/")[Google Scholar])

#table(
  columns: (0.8in, 1fr),
  stroke: none,
  column-gutter: 0.2in,
  inset: (x: 0pt, y: 3pt),
  align: (x, y) => (left, left).at(x),

  [*[ICML2024]*], [#link("https://arxiv.org/abs/paper")[Paper Title: Solving Important Problems]],
  [], [Your Name, Co-Author Name, Another Author],
  [], [_International Conference on Machine Learning (ICML)_, 2024],
  [],[#text(red)[*ICML2024 Spotlight*]],
  [],[],
)

=== Education
- _Ph.D. in Computer Science_, Your University #h(1fr) 2019 -- 2024
- _M.S. in Computer Science_, Previous University #h(1fr) 2017 -- 2019
```

### Blog Posts (`blog/*.typ`)
Individual blog posts with metadata:

```typst
// Blog Post Metadata
// title: Your Amazing Blog Post
// date: 2024-07-23
// author: Your Name
// excerpt: A brief description of what this post is about...

= Your Amazing Blog Post

This is the content of your blog post. You can use all Typst features:

== Math Support
$ E = m c^2 $

== Code Blocks
```python
def hello_world():
    print("Hello from Typst!")
```

== Links and References
Check out #link("https://typst.app")[Typst] for more information.
```

## 🔨 Build Process

The build system automatically:

1. **Compiles Typst Sections**: `src/about.typ`, `src/news.typ`, `src/cv.typ`
2. **Extracts HTML Content**: Removes `<html>` and `<body>` wrappers
3. **Integrates into Homepage**: Injects content into main template
4. **Processes Blog Posts**: Compiles and generates individual pages
5. **Generates Indexes**: Creates blog listing and main homepage
6. **Copies Assets**: Styles and static files

## 🎨 Customization

### Templates (`src/`)
- `main-index.html` - Homepage template
- `blog-index.html` - Blog listing template  
- `blog-post.html` - Individual post template
- `style.css` - Bear Blog-inspired styles

### Site Configuration (`build.py`)
```python
site_config = {
    'title': 'Your Name',
    'description': 'Your tagline or description',
    'about': 'Brief about text for metadata'
}
```

## 🚀 Development Workflow

1. **Edit Content**: Modify `.typ` files for your content
2. **Test Locally**: Run `./dev.sh` to build and serve
3. **Review Changes**: Check `http://localhost:8000`
4. **Deploy**: Push to GitHub for automatic deployment

## 📁 File Structure
```
mini_blog/
├── src/
│   ├── about.typ          # About section content
│   ├── news.typ           # News and announcements
│   ├── cv.typ             # CV and publications
│   ├── main-index.html    # Homepage template
│   ├── blog-index.html    # Blog listing template
│   ├── blog-post.html     # Blog post template
│   └── style.css          # Bear Blog CSS styles
├── blog/
│   ├── post1.typ          # Blog post files
│   └── post2.typ
├── static/
│   └── image.jpg          # Static assets
├── dist/                  # Generated site (auto-created)
├── build.py               # Python build script
├── dev.sh                 # Development script
└── README.md
```

## 💡 Tips

- **Math**: Use `$ ... $` for inline math, display math on separate lines
- **Links**: Use `#link("url")[text]` for external links
- **Emphasis**: Use `*bold*` and `_italic_` for text formatting
- **Code**: Use backticks for inline code, ```` for code blocks
- **Tables**: Use Typst's table syntax for structured data
- **Images**: Place in `static/` and reference with relative paths

This system gives you the power of Typst for beautiful document creation with the convenience of a modern web deployment workflow! 