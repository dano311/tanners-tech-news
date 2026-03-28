#!/usr/bin/env python3
"""Generate 10 witty tech articles using Ollama"""

import json
import os
import subprocess
from datetime import datetime

# Load topics
with open('scraper/selected_topics.json') as f:
    topics = json.load(f)

# Article generation prompt template
ARTICLE_PROMPT = """You're Tanner, a witty AI tech blogger for "Tanner's Tech News". Your tone is:
- Sarcastic but informed
- Dry humor with clever observations
- Pop culture references when appropriate
- Never boring or corporate

Write a 400-600 word tech news article about this topic: {title}
Source: {source}

Include:
1. A catchy headline with an emoji
2. A snarky intro hook
3. The actual tech news explained in an entertaining way
4. A witty take on the implications
5. A closing zinger

Format as markdown with ## headers. Be conversational, not formal."""

TANNER_PERSONA = """You are Tanner, a witty AI tech blogger. Your style:
- Make tech news actually entertaining
- Use sarcasm and dry humor
- Reference memes and pop culture
- Sound like a smart friend at a coffee shop, not a press release
- Include relevant emojis in headers"""

def generate_article(topic, index):
    """Generate a single article using ollama"""
    prompt = ARTICLE_PROMPT.format(title=topic['title'], source=topic['source'])
    
    # Call ollama
    result = subprocess.run(
        ['ollama', 'run', 'kimi-k2.5:cloud', '--format', 'json'],
        input=json.dumps({
            'system': TANNER_PERSONA,
            'prompt': prompt
        }),
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    if result.returncode != 0:
        print(f"Error generating article {index}: {result.stderr}")
        return None
    
    # Parse response
    try:
        response = json.loads(result.stdout)
        return response.get('response', result.stdout)
    except:
        return result.stdout

def main():
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*60}")
        print(f"Generating Article {i}/10: {topic['title'][:60]}...")
        print(f"{'='*60}")
        
        content = generate_article(topic, i)
        
        if content:
            # Create markdown file
            filename = f"posts/new_batch/2026-03-27-{i:02d}.md"
            
            # Add frontmatter
            frontmatter = f"""---
title: "{topic['title']}"
date: "{date_str}"
author: "Tanner (AI)"
tags: [tech, news]
sources: ['{topic['source']}']
---

"""
            
            with open(filename, 'w') as f:
                f.write(frontmatter + content)
            
            print(f"✅ Saved to {filename}")
            print(f"   Length: {len(content)} chars")
        else:
            print(f"❌ Failed to generate article {i}")

if __name__ == '__main__':
    main()
