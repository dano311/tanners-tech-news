#!/usr/bin/env python3
"""
Tanner's Tech News - Daily Blog Post Generator
Scrapes news → Ollama generates article → Saves to blog
"""

import json
import requests
from datetime import datetime

# Firecrawl config
with open('/home/dan/.openclaw/agents/main/agent/auth-profiles.json', 'r') as f:
    config = json.load(f)

FIRECRAWL_KEY = config['firecrawl']['key']
FIRE_HEADERS = {'Authorization': f'Bearer {FIRECRAWL_KEY}'}

OLLAMA_URL = 'http://localhost:11434/api/generate'

def scrape_source(url, name):
    """Scrape a news source"""
    try:
        response = requests.post(
            'https://api.firecrawl.dev/v1/scrape',
            headers=FIRE_HEADERS,
            json={'url': url, 'formats': ['markdown'], 'onlyMainContent': True},
            timeout=30
        )
        data = response.json()
        if data.get('success'):
            return {
                'source': name,
                'url': url,
                'title': data['data'].get('metadata', {}).get('title', name),
                'content': data['data'].get('markdown', '')[:5000]  # First 5000 chars
            }
    except Exception as e:
        print(f"Error scraping {name}: {e}")
    return None

def extract_headlines(markdown, source):
    """Extract key headlines from markdown"""
    headlines = []
    lines = markdown.split('\n')
    
    for line in lines:
        line = line.strip()
        # Look for titles (headers or links)
        if line.startswith('# ') or line.startswith('## '):
            title = line.lstrip('# ').strip()
            if len(title) > 20 and 'http' not in title[:30]:
                headlines.append(title)
        elif line.startswith('[') and '](' in line and '|' in line:
            # Hacker News format
            parts = line.split('|')
            for part in parts:
                if '[' in part and '](' in part:
                    title = part.split('](')[0].split('[')[-1]
                    if len(title) > 15 and 'points' not in title.lower():
                        headlines.append(title)
    
    return list(set(headlines))[:5]  # Unique, top 5

def generate_blog_post(headlines_data):
    """Use Ollama to generate blog post"""
    
    # Build prompt
    prompt = f"""You are Tanner, an AI tech news curator. Write a daily tech news blog post.

Here are today's headlines from various tech sources:

"""
    for source in headlines_data:
        prompt += f"\nFrom {source['source']}:\n"
        for h in source['headlines'][:5]:
            prompt += f"- {h}\n"
    
    prompt += """

Write a blog post with:
1. Catchy title (5-8 words)
2. Brief intro paragraph (2-3 sentences)
3. 3-5 main stories with your own spin/analysis
4. Closing thought (1 sentence)

Keep it conversational, slightly witty, and informative. Avoid corporate speak. Use emojis where appropriate. Aim for 400-600 words.

Format as markdown with ## headers for sections."""

    # Call Ollama
    try:
        response = requests.post(OLLAMA_URL, json={
            'model': 'kimi-k2.5:cloud',
            'prompt': prompt,
            'stream': False
        }, timeout=120)
        
        result = response.json()
        return result.get('response', 'Error generating post')
    except Exception as e:
        print(f"Ollama error: {e}")
        return f"Error: {e}"

def save_blog_post(content, date_str):
    """Save blog post to file"""
    filename = f"/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts/{date_str}.md"
    
    # Add header
    header = f"""---
title: "Tech News Roundup - {date_str}"
date: "{datetime.now().isoformat()}"
author: "Tanner"
tags: ["tech", "news", "daily"]
---

"""
    
    full_content = header + content
    
    with open(filename, 'w') as f:
        f.write(full_content)
    
    return filename

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🤖 TANNER'S TECH NEWS - {today}")
    print("="*50)
    
    # Scrape sources
    sources = [
        ('https://news.ycombinator.com', 'Hacker News'),
        ('https://techcrunch.com', 'TechCrunch'),
    ]
    
    headlines_data = []
    
    print("\n📰 Scraping sources...")
    for url, name in sources:
        print(f"  Scraping {name}...")
        data = scrape_source(url, name)
        if data:
            headlines = extract_headlines(data['content'], name)
            if headlines:
                headlines_data.append({
                    'source': name,
                    'headlines': headlines
                })
                print(f"    ✅ {len(headlines)} headlines")
        else:
            print(f"    ❌ Failed")
    
    if not headlines_data:
        print("❌ No headlines collected. Exiting.")
        return
    
    # Generate blog post
    print("\n✍️ Generating blog post with Ollama...")
    blog_content = generate_blog_post(headlines_data)
    
    # Save
    filepath = save_blog_post(blog_content, today)
    
    print(f"\n✅ Blog post saved!")
    print(f"📄 {filepath}")
    print(f"\n📊 Stats:")
    print(f"  Sources: {len(headlines_data)}")
    print(f"  Word count: {len(blog_content.split())}")
    print(f"\n--- PREVIEW ---")
    print(blog_content[:800] + "...")

if __name__ == '__main__':
    main()
