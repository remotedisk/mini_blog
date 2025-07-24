#!/usr/bin/env python3

"""
Typst Blog Build Script
Usage: python3 build.py [local|production]
"""

import os
import sys
import re
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Typst
    try:
        result = subprocess.run(['typst', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Typst: {result.stdout.strip()}")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("❌ Typst is not installed. Please install it first:")
        print("   📦 From releases: https://github.com/typst/typst/releases")
        print("   🦀 From source: cargo install --git https://github.com/typst/typst.git --rev 7278d887cf05fadc9a96478830e5876739b78f53 typst-cli")
        sys.exit(1)
    
    # Check Python (already running, but verify version)
    print(f"✅ Python: {sys.version.split()[0]}")

def extract_metadata(file_path, key):
    """Extract metadata from .typ file using typst query"""
    try:
        # Get the directory of the .typ file and change to it
        typ_dir = file_path.parent
        typ_filename = file_path.name
        
        result = subprocess.run([
            'typst', 'query', 
            typ_filename, 
            f"<meta:{key}>",
            '--field', 'value',
            '--one'
        ], capture_output=True, text=True, cwd=str(typ_dir))
        
        if result.returncode == 0:
            return result.stdout.strip().strip('"')  # Remove any surrounding quotes
        else:
            # Fallback to comment-based extraction if query fails
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith(f"// {key}:"):
                        return line.replace(f"// {key}:", "").strip()
            return ""
    except Exception as e:
        print(f"   ⚠️  Warning: Could not read metadata from {file_path}: {e}")
        return ""

def compile_typst_post(typ_file, output_file):
    """Compile a single Typst file to HTML"""
    try:
        env = os.environ.copy()
        env['TYPST_FEATURES'] = 'html'
        
        # Get the directory of the .typ file and change to it
        typ_dir = typ_file.parent
        original_cwd = Path.cwd()
        
        # Make paths relative to the typ file directory
        typ_filename = typ_file.name
        output_path = output_file.resolve()
        
        result = subprocess.run([
            'typst', 'compile',
            typ_filename, 
            str(output_path),
            '--format', 'html',
            '--features', 'html',
            '--root', '..'
        ], env=env, capture_output=True, text=True, cwd=str(typ_dir))
        
        if result.returncode != 0:
            print(f"   ❌ Typst compilation failed:")
            print(f"   {result.stderr}")
            return False
            
        if not output_file.exists():
            print(f"   ❌ Output file not created: {output_file}")
            return False
            
        return True
        
    except Exception as e:
        print(f"   ❌ Compilation error: {e}")
        return False

def extract_html_body(html_file):
    """Extract body content from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract body content
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_match:
            return body_match.group(1).strip()
        return content
        
    except Exception as e:
        print(f"   ❌ Could not extract HTML body: {e}")
        return ""

def extract_html_body_from_string(html_content):
    """Extract body content from HTML string"""
    try:
        # Extract body content
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
        if body_match:
            return body_match.group(1).strip()
        return html_content.strip()
        
    except Exception as e:
        print(f"   ❌ Could not extract HTML body from string: {e}")
        return ""

def process_template(template_file, output_file, variables):
    """Process a template file with variable substitution"""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Replace all variables
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
            
        return True
        
    except Exception as e:
        print(f"   ❌ Template processing failed: {e}")
        return False

def generate_blog_post(typ_file, site_config, environment):
    """Generate a single blog post"""
    filename = typ_file.stem
    print(f"📝 Processing blog post: {typ_file}")
    
    # Check if file exists and is readable
    if not typ_file.exists():
        print(f"   ❌ File not found: {typ_file}")
        return None
        
    if not os.access(typ_file, os.R_OK):
        print(f"   ❌ File not readable: {typ_file}")
        return None
    
    # Extract metadata
    title = extract_metadata(typ_file, "title") or "Untitled Post"
    date = extract_metadata(typ_file, "date") or "Unknown Date"
    author = extract_metadata(typ_file, "author") or "Anonymous"
    excerpt = extract_metadata(typ_file, "excerpt") or "No excerpt available."
    
    print(f"   Title: {title}")
    print(f"   Date: {date}")
    print(f"   Author: {author}")
    print(f"   Excerpt: {excerpt[:50]}...")
    
    # Create temp and final output paths
    dist_blog = Path("dist/blog")
    temp_file = dist_blog / f"{filename}.temp.html"
    final_file = dist_blog / f"{filename}.html"
    
    # Compile Typst to HTML
    print("   🔨 Compiling Typst...")
    if not compile_typst_post(typ_file, temp_file):
        return None
    
    # Extract body content
    body_content = extract_html_body(temp_file)
    if not body_content:
        print("   ❌ Could not extract body content")
        return None
    
    # Generate final HTML from template
    print("   📄 Generating HTML...")
    template_vars = {
        'SITE_TITLE': site_config['title'],
        'POST_TITLE': title,
        'POST_DATE': date,
        'POST_AUTHOR': author,
        'POST_CONTENT': body_content,
        'ENVIRONMENT': environment
    }
    
    if not process_template(Path("src/blog-post.html"), final_file, template_vars):
        return None
    
    # Clean up temp file
    if temp_file.exists():
        temp_file.unlink()
    
    print(f"   ✅ Blog post generated successfully: {final_file}")
    
    # Return metadata for blog index
    return {
        'filename': filename,
        'title': title,
        'date': date,
        'author': author,
        'excerpt': excerpt
    }

def generate_blog_index(posts_data, site_config, environment):
    """Generate the blog index page"""
    print("📋 Generating blog index...")
    
    # Sort posts by date (newest first)
    def parse_date(date_str):
        """Parse date string to allow sorting"""
        try:
            # Try to parse different date formats
            from datetime import datetime
            for fmt in ['%Y-%m-%d', '%Y.%m', '%Y-%m', '%m/%d/%Y', '%m-%d-%Y']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            # If no format works, return a default old date
            return datetime(1900, 1, 1)
        except:
            return datetime(1900, 1, 1)
    
    sorted_posts = sorted(posts_data, key=lambda x: parse_date(x['date']), reverse=True)
    
    # Generate blog posts HTML in news style
    posts_html = ""
    for post in sorted_posts:
        # Format date like news items
        date_formatted = f"<strong>{post['date']}</strong>"
        posts_html += f'''
                <li>{date_formatted}: <a href="{post['filename']}.html">{post['title']}</a></li>'''
    
    # Generate blog index page
    template_vars = {
        'SITE_TITLE': site_config['title'],
        'BLOG_POSTS': posts_html,
        'ENVIRONMENT': environment
    }
    
    return process_template(
        Path("src/blog-index.html"), 
        Path("dist/blog/index.html"), 
        template_vars
    )

def compile_typst_section(typ_file):
    """Compile a Typst file and return the HTML body content"""
    print(f"🔨 Compiling {typ_file}...")
    
    try:
        # Compile Typst to HTML
        result = subprocess.run([
            'typst', 'compile', str(typ_file), 
            '--format', 'html', 
            '--features', 'html',
            '--root', '..',
            '-'  # Output to stdout
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode != 0:
            print(f"   ❌ Typst compilation failed: {result.stderr}")
            return ""
        
        # Extract body content
        html_content = result.stdout
        body_content = extract_html_body_from_string(html_content)
        
        if body_content:
            print(f"   ✅ Successfully compiled {typ_file}")
            return body_content
        else:
            print(f"   ⚠️  No body content found in {typ_file}")
            return ""
            
    except Exception as e:
        print(f"   ❌ Error compiling {typ_file}: {e}")
        return ""

def generate_main_index(site_config, environment):
    """Generate the main index page"""
    print("📄 Generating main index page...")
    
    # Compile individual Typst sections
    about_content = compile_typst_section(Path("src/about.typ"))
    news_content = compile_typst_section(Path("src/news.typ"))
    cv_content = compile_typst_section(Path("src/cv.typ"))
    
    template_vars = {
        'SITE_TITLE': site_config['title'],
        'SITE_DESCRIPTION': site_config['description'],
        'ABOUT_TEXT': site_config['about'],
        'ABOUT_CONTENT': about_content,
        'NEWS_CONTENT': news_content,
        'CV_CONTENT': cv_content,
        'ENVIRONMENT': environment
    }
    
    return process_template(
        Path("src/main-index.html"), 
        Path("dist/index.html"), 
        template_vars
    )

def copy_static_assets():
    """Copy static assets and CSS to dist folder"""
    print("📦 Copying static assets and styles...")
    
    dist_dir = Path("dist")
    
    # Copy CSS file
    try:
        css_source = Path("src/style.css")
        css_dest = dist_dir / "style.css"
        if css_source.exists():
            shutil.copy2(css_source, css_dest)
            print("   ✅ Copied style.css")
        else:
            print("   ⚠️  Warning: style.css not found in src/")
    except Exception as e:
        print(f"   ❌ Failed to copy CSS: {e}")
        return False
    
    # Copy blog-specific CSS for blog pages
    try:
        css_source = Path("src/style.css")
        blog_css_dest = dist_dir / "blog" / "style.css"
        if css_source.exists():
            shutil.copy2(css_source, blog_css_dest)
            print("   ✅ Copied style.css to blog folder")
    except Exception as e:
        print(f"   ❌ Failed to copy CSS to blog folder: {e}")
        return False
    
    # Copy profile image p.jpg
    try:
        profile_image = Path("src/p.jpg")
        if profile_image.exists():
            shutil.copy2(profile_image, dist_dir / "p.jpg")
            print("   ✅ Copied p.jpg")
        else:
            print("   ⚠️  Warning: p.jpg not found in src/ directory")
    except Exception as e:
        print(f"   ❌ Failed to copy p.jpg: {e}")
        return False
    
    # Copy static assets
    static_dir = Path("static")
    if not static_dir.exists():
        print("   No static directory found")
        return True
    
    if not any(static_dir.iterdir()):
        print("   Static directory is empty")
        return True
    
    try:
        for item in static_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, dist_dir / item.name)
            elif item.is_dir():
                shutil.copytree(item, dist_dir / item.name, dirs_exist_ok=True)
        print("   ✅ Copied static assets")
        return True
    except Exception as e:
        print(f"   ❌ Failed to copy static assets: {e}")
        return False

def main():
    """Main build function"""
    # Parse command line arguments
    environment = sys.argv[1] if len(sys.argv) > 1 else "local"
    if environment not in ["local", "production"]:
        print("❌ Invalid environment. Use 'local' or 'production'")
        sys.exit(1)
    
    print(f"🔨 Building Typst blog for {environment} environment...")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Site configuration
    site_config = {
        'title': "Mini Blog",
        'description': "A beautiful blog powered by Typst",
        'about': "This blog showcases the power of Typst for creating beautiful documents and web content. Write in Typst, deploy to the web!"
    }
    
    # Create directories
    print("📁 Creating directories...")
    Path("dist/blog").mkdir(parents=True, exist_ok=True)
    
    # Find and process blog posts
    print("\n🔨 Processing blog posts...")
    
    blog_dir = Path("blog")
    typ_files = list(blog_dir.glob("*.typ"))
    
    print("📋 Found .typ files:")
    for typ_file in typ_files:
        print(f"   ✓ {typ_file}")
    print()
    
    if not typ_files:
        print("❌ No .typ files found in blog/ directory")
        sys.exit(1)
    
    # Process each blog post
    posts_data = []
    for typ_file in typ_files:
        print(f"🔄 Starting processing: {typ_file}")
        post_data = generate_blog_post(typ_file, site_config, environment)
        if post_data:
            posts_data.append(post_data)
            print(f"   ✅ Successfully processed: {typ_file}")
        else:
            print(f"   ❌ Failed to process: {typ_file}")
        print()
    
    if not posts_data:
        print("❌ No blog posts were successfully processed")
        sys.exit(1)
    
    print(f"📊 Successfully processed {len(posts_data)} blog post(s)")
    print()
    
    # Generate blog index
    if not generate_blog_index(posts_data, site_config, environment):
        print("❌ Failed to generate blog index")
        sys.exit(1)
    
    # Generate main index
    if not generate_main_index(site_config, environment):
        print("❌ Failed to generate main index")
        sys.exit(1)
    
    # Copy static assets
    if not copy_static_assets():
        print("❌ Failed to copy static assets")
        sys.exit(1)
    
    print("\n✅ Blog build complete!")
    print("📂 Output directory: ./dist/")
    print("📄 Files created:")
    print("   - dist/index.html (main page)")
    print("   - dist/style.css (stylesheet)")
    print("   - dist/blog/index.html (blog index)")
    print("   - dist/blog/style.css (stylesheet for blog pages)")
    
    # List generated blog posts
    for post in posts_data:
        print(f"   - dist/blog/{post['filename']}.html (blog post)")
    
    print("   - dist/* (static assets)")
    print()
    print("🌐 Main page: dist/index.html")
    print("📖 Blog index: dist/blog/index.html")

if __name__ == "__main__":
    main() 