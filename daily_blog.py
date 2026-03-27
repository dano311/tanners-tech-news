#!/usr/bin/env python3
"""
Tanner's Tech News - Daily Blog Generator
Scrapes Hacker News + Ollama generates blog post
"""

import json
import requests
import re
from datetime import datetime

# Config
with open('/home/dan/.openclaw/agents/main/agent/auth-profiles.json', 'r') as f:
    config = json.load(f)

FIRE_KEY = config['firecrawl']['key']
FIRE_HEADERS = {'Authorization': f'Bearer {FIRE_KEY}'}
OLLAMA_URL = 'http://localhost:11434/api/generate'

def scrape_hn():
    """Scrape Hacker News frontpage"""
    response = requests.post(
        'https://api.firecrawl.dev/v1/scrape',
        headers=FIRE_HEADERS,
        json={'url': 'https://news.ycombinator.com', 'formats': ['markdown']},
        timeout=30
    )
    
    if not response.json().get('success'):
        return []
    
    md = response.json()['data']['markdown']
    stories = []
    
    # Pattern: | 1. |  | [Title](url) ( [domain](url)) |
    for line in md.split('\n'):
        match = re.search(r'\|\s*\d+\.\s*\|\s*\|\s*\[(.+?)\]\(https?://[^)]+\)', line)
        if match:
            title = match.group(1)
            if len(title) > 10 and 'Hacker News' not in title:
                stories.append(title)
    
    return stories[:10]  # Top 10

def generate_post(stories):
    """Generate blog post with Ollama"""
    
    headlines_text = '\n'.join([f"- {s}" for s in stories[:8]])
    
    prompt = f"""You are Tanner, an AI tech news writer. Write a daily tech roundup blog post.

Today's Hacker News headlines:
{headlines_text}

Write a 400-600 word blog post with:
1. Catchy title (tech themed, 5-8 words)
2. Intro paragraph (what's trending today)
3. 4-6 story summaries with your take/analysis
4. Brief closing thought

Style: Conversational, slightly witty, informative. Use emojis. Avoid corporate speak.

Format as markdown with ## headers."""

    try:
        response = requests.post(OLLAMA_URL, json={
            'model': 'kimi-k2.5:cloud',
            'prompt': prompt,
            'stream': False
        }, timeout=180)
        return response.json().get('response', 'Error')
    except Exception as e:
        return f"Error: {e}"

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🤖 TANNER'S TECH NEWS - {today}")
    print("="*50)
    
    # Scrape
    print("\n📰 Scraping Hacker News...")
    stories = scrape_hn()
    
    if not stories:
        print("❌ No stories found")
        return
    
    print(f"✅ Found {len(stories)} stories")
    for i, s in enumerate(stories[:5], 1):
        print(f"  {i}. {s[:60]}...")
    
    # Generate
    print("\n✍️ Generating with Ollama...")
    print("(This may take 30-60 seconds...)")
    content = generate_post(stories)
    
    # Save
    import os
    os.makedirs('/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts', exist_ok=True)
    filename = f"/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts/{today}.md"
    
    header = f"""---
title: "Tanner's Tech News - {today}"
date: "{today}"
author: "Tanner (AI)"
tags: [tech, news, daily]
---

"""
    
    with open(filename, 'w') as f:
        f.write(header + content)
    
    print(f"\n✅ SAVED: {filename}")
    print(f"\n📄 FULL POST:\n")
    print("="*50)
    print(content)

if __name__ == '__main__':
    main()
