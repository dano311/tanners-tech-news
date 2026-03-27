#!/usr/bin/env python3
"""Generate AI thumbnail images for tech blog articles"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

# Load OpenAI API key from auth profiles
AUTH_PROFILES_PATH = '/home/dan/.openclaw/agents/main/agent/auth-profiles.json'

def load_api_key():
    """Load OpenAI API key from auth profiles"""
    try:
        with open(AUTH_PROFILES_PATH, 'r') as f:
            profiles = json.load(f)
            return profiles.get('openai', {}).get('key')
    except Exception as e:
        print(f"Error loading API key: {e}")
        return None

# Image generation prompts - DALL-E style for tech blog
# Blue/orange color scheme to match the blog branding
THUMBNAIL_PROMPTS = [
    {
        "filename": "ai-robot-future.png",
        "prompt": "A sleek humanoid robot with glowing blue circuits and orange accents, standing in a futuristic tech lab with holographic screens displaying code. Modern minimalist style, blue and orange color scheme, dramatic lighting, high-tech atmosphere, digital art, clean lines, professional tech illustration"
    },
    {
        "filename": "cyber-security-shield.png",
        "prompt": "A glowing digital shield protecting circuit board patterns, with blue energy waves and orange warning indicators. Abstract cybersecurity concept, blue and orange color scheme, futuristic holographic style, tech illustration, clean modern design"
    },
    {
        "filename": "tech-chips-cpu.png",
        "prompt": "Close-up of a powerful computer CPU chip with blue and orange glowing circuits, surrounded by floating digital particles and code streams. Semiconductor technology concept, blue and orange accents, macro photography style, high-tech aesthetic, clean background"
    },
    {
        "filename": "data-privacy-abstract.png",
        "prompt": "Abstract visualization of data privacy - locked digital vault with flowing encrypted data streams in blue and orange colors. Minimalist geometric design, glowing lines, secure technology concept, modern tech illustration style"
    },
    {
        "filename": "streaming-entertainment.png",
        "prompt": "A modern streaming entertainment concept with floating digital screens showing content, blue and orange glowing accents, abstract media waves, futuristic entertainment technology, clean minimalist design, professional tech illustration"
    },
    {
        "filename": "neural-network-brain.png",
        "prompt": "Artificial intelligence brain visualization with glowing blue neural connections and orange synapse points, floating in a dark digital space. Abstract AI concept, blue and orange color scheme, futuristic neural network art, clean tech illustration"
    },
    {
        "filename": "smartphone-tech.png",
        "prompt": "A sleek modern smartphone with holographic interface elements floating above it, blue and orange glowing accents, app icons and notifications suspended in air, futuristic mobile technology concept, clean professional illustration"
    },
    {
        "filename": "cloud-computing.png",
        "prompt": "Abstract cloud computing concept - stylized cloud with glowing blue and orange data streams flowing into it, connected nodes and servers, modern tech infrastructure visualization, clean geometric design, professional illustration"
    },
    {
        "filename": "code-programming.png",
        "prompt": "Abstract representation of programming code - glowing blue and orange syntax elements, floating brackets and functions, digital code streams, modern software development concept, clean tech aesthetic, professional illustration"
    },
    {
        "filename": "tech-news-abstract.png",
        "prompt": "Abstract tech news header image - digital newspaper or news feed with holographic elements, blue and orange accent colors, floating headlines and data visualizations, modern journalism technology concept, clean minimalist design"
    }
]

def generate_image(prompt, api_key, output_path):
    """Generate image using OpenAI DALL-E 3 API"""
    url = "https://api.openai.com/v1/images/generations"
    
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            image_data = base64.b64decode(result['data'][0]['b64_json'])
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
        
        return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error details: {error_body}")
        except:
            pass
        return False
    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def main():
    """Generate all thumbnail images"""
    api_key = load_api_key()
    if not api_key:
        print("ERROR: Could not load OpenAI API key")
        return
    
    output_dir = Path('/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/docs/images')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {len(THUMBNAIL_PROMPTS)} thumbnail images...")
    print(f"Output directory: {output_dir}")
    print()
    
    generated = []
    failed = []
    
    for i, item in enumerate(THUMBNAIL_PROMPTS, 1):
        print(f"[{i}/{len(THUMBNAIL_PROMPTS)}] Generating: {item['filename']}")
        print(f"  Prompt: {item['prompt'][:80]}...")
        
        output_path = output_dir / item['filename']
        
        if output_path.exists():
            print(f"  → Already exists, skipping")
            generated.append(item['filename'])
            continue
        
        success = generate_image(item['prompt'], api_key, output_path)
        
        if success:
            print(f"  ✓ Saved to: {output_path}")
            generated.append(item['filename'])
        else:
            print(f"  ✗ Failed to generate")
            failed.append(item['filename'])
        
        print()
    
    print("=" * 60)
    print(f"GENERATION COMPLETE")
    print(f"  Generated: {len(generated)}/{len(THUMBNAIL_PROMPTS)}")
    print(f"  Failed: {len(failed)}")
    print()
    print("Generated files:")
    for f in generated:
        print(f"  ✓ {f}")
    if failed:
        print()
        print("Failed files:")
        for f in failed:
            print(f"  ✗ {f}")

if __name__ == '__main__':
    main()
