#!/usr/bin/env python3
"""
Tanner's Tech News - Daily Blog Generator v2
Scrapes multiple sources + Ollama generates blog post
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

# Multiple news sources
SOURCES = [
    ('https://news.ycombinator.com', 'Hacker News'),
    ('https://techcrunch.com', 'TechCrunch'),
    ('https://www.theverge.com', 'The Verge'),
    ('https://arstechnica.com', 'Ars Technica'),
    ('https://www.reddit.com/r/technology/top/.json?t=day', 'Reddit r/technology'),
]

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
    
    # Pattern: | 1. |  | [Title](url)
    for line in md.split('\n'):
        match = re.search(r'\|\s*\d+\.\s*\|\s*\|\s*\[(.+?)\]\(https?://[^)]+\)', line)
        if match:
            title = match.group(1)
            if len(title) > 10 and 'Hacker News' not in title:
                stories.append(title)
    
    return stories[:8]

def scrape_techcrunch():
    """Scrape TechCrunch"""
    try:
        response = requests.post(
            'https://api.firecrawl.dev/v1/scrape',
            headers=FIRE_HEADERS,
            json={'url': 'https://techcrunch.com', 'formats': ['markdown'], 'onlyMainContent': True},
            timeout=30
        )
        
        if not response.json().get('success'):
            return []
        
        md = response.json()['data']['markdown']
        stories = []
        
        # Look for article titles (headers)
        for line in md.split('\n'):
            if line.startswith('## ') or line.startswith('### '):
                title = line.lstrip('# ').strip()
                # Filter out navigation, ads, etc
                if len(title) > 20 and not any(x in title.lower() for x in ['cookie', 'privacy', 'subscribe', 'newsletter', 'sign up']):
                    stories.append(title)
        
        return stories[:6]
    except:
        return []

def scrape_verge():
    """Scrape The Verge"""
    try:
        response = requests.post(
            'https://api.firecrawl.dev/v1/scrape',
            headers=FIRE_HEADERS,
            json={'url': 'https://www.theverge.com', 'formats': ['markdown'], 'onlyMainContent': True},
            timeout=30
        )
        
        if not response.json().get('success'):
            return []
        
        md = response.json()['data']['markdown']
        stories = []
        
        for line in md.split('\n'):
            if line.startswith('## ') or line.startswith('### '):
                title = line.lstrip('# ').strip()
                if len(title) > 20 and not any(x in title.lower() for x in ['cookie', 'privacy', 'subscribe', 'sign up', 'newsletter']):
                    stories.append(title)
        
        return stories[:6]
    except:
        return []

def scrape_ars():
    """Scrape Ars Technica"""
    try:
        response = requests.post(
            'https://api.firecrawl.dev/v1/scrape',
            headers=FIRE_HEADERS,
            json={'url': 'https://arstechnica.com', 'formats': ['markdown'], 'onlyMainContent': True},
            timeout=30
        )
        
        if not response.json().get('success'):
            return []
        
        md = response.json()['data']['markdown']
        stories = []
        
        for line in md.split('\n'):
            if line.startswith('## ') or line.startswith('### '):
                title = line.lstrip('# ').strip()
                if len(title) > 20 and not any(x in title.lower() for x in ['cookie', 'privacy', 'subscribe']):
                    stories.append(title)
        
        return stories[:5]
    except:
        return []

def scrape_reddit_tech():
    """Scrape Reddit r/technology"""
    try:
        headers = {'User-Agent': 'TannerTechNews/1.0'}
        response = requests.get('https://www.reddit.com/r/technology/top/.json?t=day&limit=10', headers=headers, timeout=30)
        data = response.json()
        
        stories = []
        for post in data.get('data', {}).get('children', []):
            title = post['data'].get('title', '')
            if title and len(title) > 10:
                stories.append(title)
        
        return stories[:8]
    except:
        return []

def generate_post(all_headlines):
    """Generate blog post with Ollama"""
    
    headlines_text = ""
    for source, headlines in all_headlines.items():
        if headlines:
            headlines_text += f"\nFrom {source}:\n"
            for h in headlines[:5]:
                headlines_text += f"- {h}\n"
    
    prompt = f"""You are Tanner, an AI tech news writer. Write a daily tech roundup blog post.

Today's headlines from various tech sources:
{headlines_text}

Write a 500-700 word blog post with:
1. Catchy title (tech themed, 5-10 words)
2. Intro paragraph (what's trending today, big themes)
3. 5-7 story summaries with your take/analysis (pick the most interesting)
4. Brief closing thought

Style: Conversational, witty but informative. Use emojis. Avoid corporate speak.

Format as markdown with ## headers."""

    try:
        response = requests.post(OLLAMA_URL, json={
            'model': 'kimi-k2.5:cloud',
            'prompt': prompt,
            'stream': False
        }, timeout=180)
        return response.json().get('response', 'Error generating post')
    except Exception as e:
        return f"Error: {e}"

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🤖 TANNER'S TECH NEWS - {today}")
    print("="*50)
    
    # Scrape all sources
    print("\n📰 Scraping sources...")
    all_headlines = {}
    
    print("  Scraping Hacker News...")
    hn = scrape_hn()
    if hn:
        all_headlines['Hacker News'] = hn
        print(f"    ✅ {len(hn)} headlines")
    
    print("  Scraping TechCrunch...")
    tc = scrape_techcrunch()
    if tc:
        all_headlines['TechCrunch'] = tc
        print(f"    ✅ {len(tc)} headlines")
    
    print("  Scraping The Verge...")
    vg = scrape_verge()
    if vg:
        all_headlines['The Verge'] = vg
        print(f"    ✅ {len(vg)} headlines")
    
    print("  Scraping Ars Technica...")
    ars = scrape_ars()
    if ars:
        all_headlines['Ars Technica'] = ars
        print(f"    ✅ {len(ars)} headlines")
    
    print("  Scraping Reddit r/technology...")
    rd = scrape_reddit_tech()
    if rd:
        all_headlines['Reddit r/technology'] = rd
        print(f"    ✅ {len(rd)} headlines")
    
    total = sum(len(h) for h in all_headlines.values())
    print(f"\n📊 Total headlines: {total}")
    
    if not all_headlines:
        print("❌ No headlines collected. Exiting.")
        return
    
    # Generate
    print("\n✍️ Generating blog post with Ollama...")
    print("(This may take 60-90 seconds...)")
    content = generate_post(all_headlines)
    
    # Save
    import os
    os.makedirs('/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts', exist_ok=True)
    filename = f"/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts/{today}.md"
    
    header = f"""---
title: "Tanner's Tech News - {today}"
date: "{today}"
author: "Tanner (AI)"
tags: [tech, news, daily]
sources: {list(all_headlines.keys())}
---

"""
    
    with open(filename, 'w') as f:
        f.write(header + content)
    
    print(f"\n✅ SAVED: {filename}")
    print(f"\n📄 Sources used: {', '.join(all_headlines.keys())}")
    print(f"\n--- PREVIEW ---\n")
    print(content[:800] + "...")
    
    return filename

if __name__ == '__main__':
    main()
