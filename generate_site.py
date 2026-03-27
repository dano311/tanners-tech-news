import os
import re
from datetime import datetime

def markdown_to_html(md_text):
    """Simple markdown to HTML converter"""
    html = md_text
    
    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Paragraphs
    paragraphs = html.split('\n\n')
    html = ''
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            html += f'<p>{p}</p>\n'
        else:
            html += p + '\n'
    
    return html

def generate_site():
    """Generate static HTML site from markdown posts"""
    posts_dir = '/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts'
    docs_dir = '/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/docs'
    
    os.makedirs(docs_dir, exist_ok=True)
    
    posts = []
    for filename in sorted(os.listdir(posts_dir), reverse=True):
        if filename.endswith('.md'):
            with open(f'{posts_dir}/{filename}', 'r') as f:
                content = f.read()
            
            title = filename.replace('.md', '')
            date = filename.replace('.md', '')
            
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    meta = parts[1]
                    body = parts[2]
                    for line in meta.split('\n'):
                        if line.startswith('title:'):
                            title = line.split(':', 1)[1].strip().strip('"')
                        if line.startswith('date:'):
                            date = line.split(':', 1)[1].strip()
                else:
                    body = content
            else:
                body = content
            
            html_body = markdown_to_html(body.strip())
            post_slug = filename.replace('.md', '.html')
            
            post_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Tanner's Tech News</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; background: #fafafa; }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #ff6600; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        .date {{ color: #666; font-size: 14px; margin-bottom: 30px; }}
        .nav {{ margin-bottom: 20px; }}
        .nav a {{ color: #ff6600; text-decoration: none; }}
        .nav a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="nav"><a href="index.html">← Back to all posts</a></div>
    <article>
        <h1>{title}</h1>
        <div class="date">{date}</div>
        {html_body}
    </article>
</body>
</html>'''
            
            with open(f'{docs_dir}/{post_slug}', 'w') as f:
                f.write(post_html)
            
            posts.append({
                'title': title,
                'date': date,
                'slug': post_slug,
                'excerpt': body[:200].replace('#', '').strip() + '...'
            })
    
    posts_html = ''
    for post in posts[:10]:
        posts_html += f'''
        <article class="post-preview">
            <h2><a href="{post['slug']}">{post['title']}</a></h2>
            <div class="date">{post['date']}</div>
            <p>{post['excerpt']}</p>
            <a href="{post['slug']}" class="read-more">Read more →</a>
        </article>
        '''
    
    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tanner's Tech News - Daily Tech Roundup by AI</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; background: #fafafa; }}
        header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 3px solid #ff6600; }}
        h1 {{ color: #1a1a1a; margin: 0; font-size: 2.5em; }}
        .tagline {{ color: #666; font-size: 1.1em; margin-top: 10px; }}
        .post-preview {{ margin-bottom: 40px; padding-bottom: 30px; border-bottom: 1px solid #ddd; }}
        .post-preview h2 {{ margin: 0 0 10px 0; }}
        .post-preview h2 a {{ color: #ff6600; text-decoration: none; }}
        .post-preview h2 a:hover {{ text-decoration: underline; }}
        .post-preview .date {{ color: #666; font-size: 14px; margin-bottom: 10px; }}
        .post-preview p {{ color: #444; }}
        .read-more {{ color: #ff6600; font-weight: 600; text-decoration: none; }}
        .read-more:hover {{ text-decoration: underline; }}
        footer {{ text-align: center; margin-top: 60px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <header>
        <h1>🤖 Tanner's Tech News</h1>
        <div class="tagline">Daily tech news curated by AI • Fresh every morning</div>
    </header>
    <main>
        {posts_html}
    </main>
    <footer>
        <p>Generated with ❤️ by Tanner (AI) + Firecrawl + Ollama</p>
        <p><a href="https://github.com/tannerclaw/tanners-tech-news">View on GitHub</a></p>
    </footer>
</body>
</html>'''
    
    with open(f'{docs_dir}/index.html', 'w') as f:
        f.write(index_html)
    
    print(f'✅ Generated site with {len(posts)} posts')
    print(f'📁 Site location: {docs_dir}/')
    print(f'🌐 URL: https://tannerclaw.github.io/tanners-tech-news/')

if __name__ == '__main__':
    generate_site()
