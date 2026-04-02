#!/usr/bin/env python3
"""Process WordPress posts into Astro Markdown files."""

import json, os, re
import html2text

# Author mapping based on byline in content
SANDRA_POSTS = {436, 833, 835}  # Posts with "Por Sandra Nakkoud"

def get_author(post_id):
    if post_id in SANDRA_POSTS:
        return "Sandra Nakkoud"
    return "Maurício Supleno"

def slug_to_title(slug):
    """Convert slug to readable title case."""
    return slug.replace('-', ' ').title()

def clean_html(html_content):
    """Convert HTML to clean Markdown."""
    h = html2text.HTML2Text()
    h.body_width = 0  # Don't wrap lines
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.unicode_snob = True
    h.escape_snob = True
    
    md = h.handle(html_content)
    # Clean up extra whitespace
    md = re.sub(r'\n{3,}', '\n\n', md)
    md = md.strip()
    return md

def create_frontmatter(post_id, slug, date, title, author, excerpt_html):
    """Create YAML frontmatter."""
    h = html2text.HTML2Text()
    h.body_width = 0
    h.unicode_snob = True
    h.escape_snob = True
    meta_desc = h.handle(excerpt_html).strip()[:160]
    meta_desc = re.sub(r'\s+', ' ', meta_desc)
    
    fm = f'''---
title: "{title}"
slug: "{slug}"
date: "{date}"
author: "{author}"
description: "{meta_desc}"
canonicalUrl: "https://supleno.com/blog/{slug}/"
---
'''
    return fm

def process_posts():
    posts_dir = '/tmp/supleno-blog'
    output_dir = '/tmp/supleno-blog/src/pages/blog'
    os.makedirs(output_dir, exist_ok=True)
    
    posts_data = []
    
    post_ids = [239, 436, 746, 826, 829, 831, 833, 835]
    
    for pid in post_ids:
        filepath = f'{posts_dir}/post_{pid}.json'
        if not os.path.exists(filepath):
            print(f"Skipping {pid} - no file")
            continue
            
        with open(filepath) as f:
            data = json.load(f)
        
        slug = data['slug']
        date = data['date'][:10]
        title = data['title']['rendered']
        author = get_author(pid)
        content_html = data['content']['rendered']
        excerpt_html = data['excerpt']['rendered']
        
        # Convert content to markdown
        content_md = clean_html(content_html)
        
        # Create frontmatter
        frontmatter = create_frontmatter(pid, slug, date, title, author, excerpt_html)
        
        # Combine and write
        full_md = frontmatter + '\n' + content_md
        
        # Write post file
        output_file = f'{output_dir}/{slug}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_md)
        
        posts_data.append({
            'slug': slug,
            'title': title,
            'date': date,
            'author': author
        })
        
        print(f"Created: {slug}.md ({date}) by {author}")
    
    # Create index data file
    with open(f'{posts_dir}/posts_index.json', 'w') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal posts: {len(posts_data)}")

if __name__ == '__main__':
    process_posts()
