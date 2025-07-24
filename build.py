#!/usr/bin/env python3

"""
Typst Blog Build Script with Jinja2 Templates
Usage: python3 build.py
"""

import os
import re
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def check_typst():
    """Check if Typst is installed"""
    try:
        typst_version = subprocess.run(['typst', '--version'], capture_output=True, check=True)
        print("✅ Typst found", typst_version.stdout.decode('utf-8').strip())
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Typst not found. Install from: https://github.com/typst/typst/releases")
        exit(1)

def query_typst(typ_file, selector):
    """Query Typst file for specific content using typst query"""
    try:
        result = subprocess.run([
            'typst', 'query', "--root", "..", str(typ_file), selector, '--field', 'value', '--one'
        ], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().strip('"')
    except:
        pass
    return ""

def extract_metadata(typ_file, key):
    """Extract metadata from .typ file"""
    # Try typst query first
    metadata = query_typst(typ_file, f"<meta:{key}>")
    if metadata:
        return metadata
    
    # Fallback to comment parsing
    try:
        with open(typ_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith(f"// {key}:"):
                    return line.replace(f"// {key}:", "").strip()
    except:
        pass
    return ""

def compile_typst(typ_file, output_file=None):
    """Compile Typst file to HTML"""
    print(f"Compiling {typ_file} to {output_file}")
    cmd = ['typst', 'compile', str(typ_file), '--format', 'html', '--features', 'html', '--root', '..']
    if output_file:
        cmd.append(str(output_file))
    else:
        cmd.append('-')  # stdout
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to compile {typ_file}: {result.stderr}")
        return ""
    
    if output_file:
        return True
    
    # Extract body content from stdout
    body_match = re.search(r'<body[^>]*>(.*?)</body>', result.stdout, re.DOTALL)
    return body_match.group(1).strip() if body_match else result.stdout.strip()

def process_blog_post(typ_file):
    """Process a single blog post"""
    print(f"📝 Processing: {typ_file.name}")
    
    # Extract metadata using typst query
    title = extract_metadata(typ_file, "title") or "Untitled"
    desc = extract_metadata(typ_file, "desc") or ""
    date = extract_metadata(typ_file, "date") or "Unknown"
    author = extract_metadata(typ_file, "author") or "Anonymous"
    published = extract_metadata(typ_file, "published") or "True"
    tags = query_typst(typ_file, "<meta:tags>").split(', ') if query_typst(typ_file, "<meta:tags>") else []
    
    # Skip unpublished posts
    if published.lower() == "false":
        print(f"   ⏭️  Skipping unpublished post")
        return None
    
    # Try to extract HTML content using query first
    html_content = query_typst(typ_file, "<html>")
    
    if not html_content:
        # Fallback to compilation method
        temp_file = Path("dist/blog") / f"{typ_file.stem}.temp.html"
        if not compile_typst(typ_file, temp_file):
            return None
        
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
            html_content = body_match.group(1).strip() if body_match else content
            temp_file.unlink()  # cleanup
        except Exception as e:
            print(f"❌ Error extracting body: {e}")
            return None
    
    return {
        'filename': typ_file.stem,
        'title': title,
        'desc': desc,
        'date': date,
        'author': author,
        'published': published,
        'tags': tags,
        'content': html_content
    }

def parse_date(date_str):
    """Parse date string for sorting"""
    for fmt in ['%Y-%m-%d', '%Y.%m', '%Y-%m', '%m/%d/%Y', '%m-%d-%Y']:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime(1900, 1, 1)

def main():
    print("🔨 Building Typst blog...")
    
    # Check dependencies
    check_typst()
    
    # Setup
    env = Environment(loader=FileSystemLoader('templates'), autoescape=True, trim_blocks=True, lstrip_blocks=True)
    site_config = {'title': "Xiaotian Han", 'description': "A beautiful blog powered by Typst"}
    Path("dist/blog").mkdir(parents=True, exist_ok=True)
    
    # Process blog posts
    blog_posts = []
    for typ_file in Path("content/blog").glob("*.typ"):
        post = process_blog_post(typ_file)
        if post:
            blog_posts.append(post)
            # Render individual post
            env.get_template("blog-post.html").stream(
                site_title=site_config['title'],
                post_title=post['title'],
                post_date=post['date'],
                post_author=post['author'],
                post_content=post['content']
            ).dump(str(Path("dist/blog") / f"{post['filename']}.html"))
    
    if not blog_posts:
        print("❌ No blog posts found")
        exit(1)
    
    # Sort posts by date
    blog_posts.sort(key=lambda x: parse_date(x['date']), reverse=True)
    
    # Render blog index
    env.get_template("blog-index.html").stream(
        site_title=site_config['title'],
        blog_posts=blog_posts
    ).dump("dist/blog/index.html")
    
    # Extract content for main index using queries
    print("Extracting main index content")
    about_content = query_typst(Path("content/about.typ"), "<html>") or compile_typst(Path("content/about.typ"))
    news_content = query_typst(Path("content/news.typ"), "<html>") or compile_typst(Path("content/news.typ"))
    cv_content = query_typst(Path("content/cv.typ"), "<html>") or compile_typst(Path("content/cv.typ"))
    
    env.get_template("main-index.html").stream(
        site_title=site_config['title'],
        about_content=about_content,
        news_content=news_content,
        cv_content=cv_content
    ).dump("dist/index.html")
    
    # Copy static files from public folder
    public_dir = Path("public")
    if public_dir.exists():
        for static_file in public_dir.glob("*"):
            if static_file.is_file():
                shutil.copy2(static_file, f"dist/{static_file.name}")
                shutil.copy2(static_file, f"dist/blog/{static_file.name}")
    
    print(f"✅ Generated {len(blog_posts)} posts")
    print("🌐 Main: dist/index.html")
    print("📖 Blog: dist/blog/index.html")


if __name__ == "__main__":
    main() 