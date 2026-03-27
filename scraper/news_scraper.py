#!/usr/bin/env python3
"""
Tanner's Tech News - Web Scraper
Uses Firecrawl to scrape tech news sources
"""

import json
import requests
from datetime import datetime

# Load API key
with open('/home/dan/.openclaw/agents/main/agent/auth-profiles.json', 'r') as f:
    config = json.load(f)

API_KEY = config['firecrawl']['key']
HEADERS = {'Authorization': f'Bearer {API_KEY}'}

# Tech news sources
SOURCES = [
    {'name': 'Hacker News', 'url': 'https://news.ycombinator.com', 'type': 'frontpage'},
    {'name': 'TechCrunch', 'url': 'https://techcrunch.com', 'type': 'frontpage'},
    {'name': 'The Verge', 'url': 'https://www.theverge.com', 'type': 'frontpage'},
    {'name': 'Ars Technica', 'url': 'https://arstechnica.com', 'type': 'frontpage'},
]

def scrape_url(url):
    """Scrape a URL using Firecrawl"""
    try:
        response = requests.post(
            'https://api.firecrawl.dev/v1/scrape',
            headers=HEADERS,
            json={'url': url, 'formats': ['markdown']},
            timeout=30
        )
        return response.json()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def extract_headlines(markdown, source):
    """Extract headlines from markdown"""
    lines = markdown.split('\n')
    headlines = []
    
    for line in lines:
        line = line.strip()
        # Look for links and headlines
        if line.startswith('[') and '](http' in line and len(line) > 20:
            # Extract title from markdown link
            title = line.split('](')[0][1:]
            if title and len(title) > 10 and not title.startswith('http'):
                headlines.append({
                    'title': title,
                    'source': source,
                    'scraped_at': datetime.now().isoformat()
                })
    
    return headlines[:10]  # Top 10 headlines

def scrape_all_sources():
    """Scrape all tech news sources"""
    all_headlines = []
    
    print(f"[{datetime.now().strftime('%H:%M')}] Starting news scrape...")
    print("="*50)
    
    for source in SOURCES:
        print(f"\n📰 Scraping {source['name']}...")
        result = scrape_url(source['url'])
        
        if result and result.get('success'):
            markdown = result['data'].get('markdown', '')
            headlines = extract_headlines(markdown, source['name'])
            all_headlines.extend(headlines)
            print(f"✅ Found {len(headlines)} headlines")
        else:
            print(f"❌ Failed to scrape {source['name']}")
    
    print(f"\n{'='*50}")
    print(f"Total headlines: {len(all_headlines)}")
    
    return all_headlines

if __name__ == '__main__':
    headlines = scrape_all_sources()
    
    # Save to file
    output_file = '/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/scraper/headlines.json'
    with open(output_file, 'w') as f:
        json.dump(headlines, f, indent=2)
    
    print(f"\n💾 Saved to: {output_file}")
    
    # Print sample
    print("\n📝 Sample Headlines:")
    for i, h in enumerate(headlines[:5], 1):
        print(f"{i}. {h['title'][:80]}...")
        print(f"   Source: {h['source']}")
        print()
