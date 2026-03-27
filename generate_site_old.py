import os
import re
import subprocess
from datetime import datetime

# Category colors and icons for tags
CATEGORY_STYLES = {
    'AI': {'color': '#8b5cf6', 'icon': '🤖', 'bg': 'rgba(139, 92, 246, 0.1)'},
    'Hardware': {'color': '#f59e0b', 'icon': '💻', 'bg': 'rgba(245, 158, 11, 0.1)'},
    'Privacy': {'color': '#10b981', 'icon': '🔒', 'bg': 'rgba(16, 185, 129, 0.1)'},
    'Entertainment': {'color': '#ec4899', 'icon': '📺', 'bg': 'rgba(236, 72, 153, 0.1)'},
    'Security': {'color': '#ef4444', 'icon': '🛡️', 'bg': 'rgba(239, 68, 68, 0.1)'},
    'Policy': {'color': '#3b82f6', 'icon': '🏛️', 'bg': 'rgba(59, 130, 246, 0.1)'},
    'General': {'color': '#6b7280', 'icon': '📰', 'bg': 'rgba(107, 114, 128, 0.1)'},
}

def get_category_for_post(content, title):
    """Determine category based on content keywords"""
    content_lower = (content + ' ' + title).lower()
    
    if any(word in content_lower for word in ['openai', 'anthropic', 'chatbot', 'ai ', 'algorithm', 'machine learning', 'neural']):
        return 'AI'
    elif any(word in content_lower for word in ['iphone', 'android', 'amd', 'intel', 'chip', 'processor', 'gpu', 'hardware', 'laptop', 'computer']):
        return 'Hardware'
    elif any(word in content_lower for word in ['privacy', 'surveillance', 'data', 'tracking', 'encryption']):
        return 'Privacy'
    elif any(word in content_lower for word in ['netflix', 'streaming', 'movie', 'tv', 'entertainment', 'game', 'gaming']):
        return 'Entertainment'
    elif any(word in content_lower for word in ['security', 'hack', 'breach', 'vulnerability', 'malware']):
        return 'Security'
    elif any(word in content_lower for word in ['government', 'policy', 'law', 'regulation', 'trump', 'congress', 'court']):
        return 'Policy'
    return 'General'

def estimate_read_time(content):
    """Estimate reading time in minutes"""
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return f'{minutes} min read'

def markdown_to_html(md_text):
    """Enhanced markdown to HTML converter"""
    html = md_text
    
    # Headers with IDs for anchor links
    html = re.sub(r'^# (.+)$', r'<h1 class="article-title">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', lambda m: f'<h2 class="section-title" id="{m.group(1).lower().replace(" ", "-").replace(":", "").replace("—", "").replace("'", "").replace("🎭", "").replace("💋", "").replace("🚫", "").strip()[:30]}">{m.group(1).strip()}</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    
    # Lists
    lines = html.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item_text = stripped[2:]
            result.append(f'<li>{item_text}</li>')
        elif stripped.startswith('1. ') or stripped.startswith('2. ') or stripped.startswith('3. '):
            if not in_list:
                result.append('<ol>')
                in_list = True
            item_text = stripped[3:]
            result.append(f'<li>{item_text}</li>')
        else:
            if in_list and stripped:
                result.append('</ul>' if result[-2].startswith('<ul>') else '</ol>')
                in_list = False
            if stripped:
                result.append(f'<p>{stripped}</p>')
    
    if in_list:
        result.append('</ul>' if result[-2].startswith('<ul>') else '</ol>')
    
    html = '\n'.join(result)
    
    return html

def generate_css():
    """Generate comprehensive CSS for the site"""
    return '''
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #f1f5f9;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --accent-rgb: 59, 130, 246;
            --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
            --card-shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-sm: 6px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            --font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
            --transition-fast: 150ms ease;
            --transition-medium: 250ms ease;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #0f172a;
                --bg-secondary: #1e293b;
                --bg-tertiary: #334155;
                --text-primary: #f8fafc;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                --border-color: #334155;
                --accent-color: #60a5fa;
                --accent-hover: #3b82f6;
                --accent-rgb: 96, 165, 250;
                --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2);
                --card-shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: var(--font-sans);
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Header & Navigation */
        .site-header {
            position: sticky;
            top: 0;
            z-index: 100;
            background-color: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        
        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 64px;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: var(--text-primary);
            font-weight: 700;
            font-size: 1.25rem;
        }
        
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-color), #8b5cf6);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .logo-text {
            display: flex;
            flex-direction: column;
        }
        
        .logo-title {
            font-size: 1.125rem;
            font-weight: 700;
            line-height: 1.2;
        }
        
        .logo-tagline {
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 500;
        }
        
        .nav-links {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-link {
            padding: 8px 16px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            border-radius: var(--radius-sm);
            transition: all var(--transition-fast);
        }
        
        .nav-link:hover {
            color: var(--accent-color);
            background-color: var(--bg-secondary);
        }
        
        .nav-link.active {
            color: var(--accent-color);
            background-color: rgba(var(--accent-rgb), 0.1);
        }
        
        .github-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background-color: var(--bg-secondary);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all var(--transition-fast);
        }
        
        .github-link:hover {
            background-color: var(--bg-tertiary);
        }
        
        /* Search */
        .search-container {
            position: relative;
        }
        
        .search-toggle {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
            transition: all var(--transition-fast);
        }
        
        .search-toggle:hover {
            background-color: var(--bg-secondary);
            color: var(--accent-color);
        }
        
        .search-bar {
            position: absolute;
            top: 100%;
            right: 0;
            width: 320px;
            padding: 16px;
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            box-shadow: var(--card-shadow-hover);
            margin-top: 8px;
            z-index: 1000;
            display: none;
        }
        
        .search-bar.active {
            display: block;
        }
        
        .search-input-wrapper {
            display: flex;
            align-items: center;
            gap: 8px;
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            padding: 8px 12px;
        }
        
        .search-input {
            flex: 1;
            border: none;
            background: none;
            color: var(--text-primary);
            font-size: 0.875rem;
            outline: none;
        }
        
        .search-input::placeholder {
            color: var(--text-muted);
        }
        
        .search-close {
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
        }
        
        .search-close:hover {
            color: var(--text-primary);
            background-color: var(--bg-tertiary);
        }
        
        .search-results {
            margin-top: 16px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .search-result-item {
            padding: 12px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background-color var(--transition-fast);
        }
        
        .search-result-item:last-child {
            border-bottom: none;
        }
        
        .search-result-item:hover {
            background-color: var(--bg-secondary);
        }
        
        .search-result-title {
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 4px;
            font-size: 0.875rem;
        }
        
        .search-result-excerpt {
            color: var(--text-secondary);
            font-size: 0.8rem;
            line-height: 1.4;
        }
        
        /* Search Page */
        .search-page {
            max-width: 800px;
            margin: 0 auto;
            padding: 48px 24px;
        }
        
        .search-page-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 24px;
            text-align: center;
        }
        
        .search-page-input-wrapper {
            position: relative;
            margin-bottom: 32px;
        }
        
        .search-page-input {
            width: 100%;
            padding: 16px 20px 16px 48px;
            border: 2px solid var(--border-color);
            border-radius: var(--radius-lg);
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 1.125rem;
            outline: none;
            transition: border-color var(--transition-fast);
        }
        
        .search-page-input:focus {
            border-color: var(--accent-color);
        }
        
        .search-page-input-icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }
        
        .search-page-results {
            min-height: 200px;
        }
        
        .search-stats {
            color: var(--text-muted);
            font-size: 0.875rem;
            margin-bottom: 16px;
        }
        
        .search-result-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-bottom: 16px;
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .search-result-card:hover {
            border-color: var(--accent-color);
            transform: translateY(-2px);
            box-shadow: var(--card-shadow);
        }
        
        .search-result-card .category-badge {
            margin-bottom: 8px;
        }
        
        .search-result-card .article-meta {
            margin-top: 8px;
        }
        
        .search-result-card mark {
            background-color: rgba(var(--accent-rgb), 0.3);
            color: var(--text-primary);
            padding: 0 2px;
            border-radius: 2px;
        }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            padding: 80px 24px;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }
        
        .hero-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background-color: rgba(var(--accent-rgb), 0.1);
            color: var(--accent-color);
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: 50px;
            margin-bottom: 24px;
        }
        
        .hero-title {
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 16px;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-color) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 32px;
        }
        
        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 48px;
            flex-wrap: wrap;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            color: var(--accent-color);
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        /* Main Layout */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 48px 24px;
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 48px;
        }
        
        @media (max-width: 900px) {
            .main-container {
                grid-template-columns: 1fr;
            }
        }
        
        /* Article Cards */
        .articles-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        .view-all {
            color: var(--accent-color);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .view-all:hover {
            text-decoration: underline;
        }
        
        .articles-grid {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        
        .article-card {
            background-color: var(--bg-secondary);
            border-radius: var(--radius-lg);
            padding: 24px;
            border: 1px solid var(--border-color);
            transition: all var(--transition-medium);
            cursor: pointer;
        }
        
        .article-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--card-shadow-hover);
            border-color: rgba(var(--accent-rgb), 0.3);
        }
        
        .article-card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .category-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .article-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        .article-meta span {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .article-title {
            font-size: 1.375rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 12px;
        }
        
        .article-title a {
            color: var(--text-primary);
            text-decoration: none;
            transition: color var(--transition-fast);
        }
        
        .article-title a:hover {
            color: var(--accent-color);
        }
        
        .article-excerpt {
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .article-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 16px;
            border-top: 1px solid var(--border-color);
        }
        
        .read-more {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--accent-color);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 600;
            transition: all var(--transition-fast);
        }
        
        .read-more:hover {
            gap: 12px;
        }
        
        .read-more svg {
            width: 16px;
            height: 16px;
        }
        
        .share-buttons {
            display: flex;
            gap: 8px;
        }
        
        .share-btn {
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            background-color: var(--bg-tertiary);
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all var(--transition-fast);
        }
        
        .share-btn:hover {
            background-color: var(--accent-color);
            color: white;
            transform: scale(1.1);
        }
        
        /* Sidebar */
        .sidebar {
            position: sticky;
            top: 88px;
            height: fit-content;
        }
        
        .sidebar-section {
            background-color: var(--bg-secondary);
            border-radius: var(--radius-lg);
            padding: 24px;
            border: 1px solid var(--border-color);
            margin-bottom: 24px;
        }
        
        .sidebar-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .category-list {
            list-style: none;
        }
        
        .category-list li {
            margin-bottom: 8px;
        }
        
        .category-list a {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: var(--radius-sm);
            transition: all var(--transition-fast);
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .category-list a:hover {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
        }
        
        .category-count {
            margin-left: auto;
            padding: 2px 8px;
            background-color: var(--bg-tertiary);
            border-radius: 50px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        
        /* Newsletter */
        .newsletter-section {
            background: linear-gradient(135deg, var(--accent-color), #8b5cf6);
            border-radius: var(--radius-lg);
            padding: 24px;
            color: white;
        }
        
        .newsletter-title {
            font-size: 1.125rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .newsletter-text {
            font-size: 0.875rem;
            opacity: 0.9;
            margin-bottom: 16px;
        }
        
        .newsletter-form {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .newsletter-input {
            padding: 12px 16px;
            border-radius: var(--radius-sm);
            border: none;
            font-size: 0.875rem;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .newsletter-input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .newsletter-btn {
            padding: 12px 16px;
            background-color: white;
            color: var(--accent-color);
            border: none;
            border-radius: var(--radius-sm);
            font-weight: 600;
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .newsletter-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* Footer */
        .site-footer {
            background-color: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            padding: 64px 24px 32px;
        }
        
        .footer-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 48px;
            margin-bottom: 48px;
        }
        
        .footer-section h4 {
            font-size: 0.875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 16px;
            color: var(--text-primary);
        }
        
        .footer-links {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 12px;
        }
        
        .footer-links a {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            transition: color var(--transition-fast);
        }
        
        .footer-links a:hover {
            color: var(--accent-color);
        }
        
        .footer-bottom {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
            padding-top: 32px;
            border-top: 1px solid var(--border-color);
            text-align: center;
        }
        
        .footer-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
            font-size: 1.125rem;
        }
        
        .footer-credits {
            color: var(--text-muted);
            font-size: 0.875rem;
        }
        
        .footer-credits a {
            color: var(--accent-color);
            text-decoration: none;
        }

        .footer-contact-link {
            color: var(--accent-color);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
        }

        .footer-contact-link:hover {
            text-decoration: underline;
        }

        .advertise-btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: var(--accent-color);
            color: white;
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: var(--radius-sm);
            transition: all var(--transition-fast);
        }

        .advertise-btn:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }

        .footer-social {
            display: flex;
            gap: 12px;
        }

        /* Individual Article Page */
        .article-page {
            max-width: 800px;
            margin: 0 auto;
            padding: 48px 24px;
        }
        
        .article-back {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 32px;
            transition: color var(--transition-fast);
        }
        
        .article-back:hover {
            color: var(--accent-color);
        }
        
        .article-header {
            margin-bottom: 48px;
        }
        
        .article-header .category-badge {
            margin-bottom: 16px;
        }
        
        .article-header .article-title {
            font-size: clamp(1.75rem, 4vw, 2.5rem);
            margin-bottom: 16px;
        }
        
        .article-header .article-meta {
            font-size: 1rem;
        }
        
        .article-content {
            font-size: 1.125rem;
            line-height: 1.8;
        }
        
        .article-content h2 {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 48px 0 24px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--border-color);
        }
        
        .article-content h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin: 32px 0 16px;
        }
        
        .article-content p {
            margin-bottom: 24px;
            color: var(--text-secondary);
        }
        
        .article-content ul, .article-content ol {
            margin-bottom: 24px;
            padding-left: 24px;
        }
        
        .article-content li {
            margin-bottom: 8px;
            color: var(--text-secondary);
        }
        
        .article-content a {
            color: var(--accent-color);
            text-decoration: none;
        }
        
        .article-content a:hover {
            text-decoration: underline;
        }
        
        .article-content strong {
            color: var(--text-primary);
        }
        
        .article-content hr {
            border: none;
            height: 1px;
            background-color: var(--border-color);
            margin: 48px 0;
        }
        
        .article-share {
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid var(--border-color);
        }
        
        .article-share h4 {
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 16px;
            color: var(--text-muted);
        }
        
        .share-row {
            display: flex;
            gap: 12px;
        }
        
        .share-btn-large {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all var(--transition-fast);
        }
        
        .share-btn-large:hover {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
        }
        
        .share-btn-large.twitter:hover {
            background-color: #1da1f2;
            border-color: #1da1f2;
            color: white;
        }
        
        .share-btn-large.linkedin:hover {
            background-color: #0a66c2;
            border-color: #0a66c2;
            color: white;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header-container {
                padding: 0 16px;
            }
            
            .nav-links {
                display: none;
            }
            
            .hero {
                padding: 48px 16px;
            }
            
            .hero-stats {
                gap: 24px;
            }
            
            .main-container {
                padding: 32px 16px;
            }
            
            .article-card {
                padding: 20px;
            }
            
            .footer-grid {
                grid-template-columns: 1fr;
                gap: 32px;
            }
            
            .search-bar {
                width: calc(100vw - 32px);
                right: -16px;
            }
            
            .search-page {
                padding: 32px 16px;
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .article-card {
            animation: fadeIn 0.5s ease forwards;
        }
        
        .article-card:nth-child(1) { animation-delay: 0.1s; }
        .article-card:nth-child(2) { animation-delay: 0.2s; }
        .article-card:nth-child(3) { animation-delay: 0.3s; }
        .article-card:nth-child(4) { animation-delay: 0.4s; }
        .article-card:nth-child(5) { animation-delay: 0.5s; }
        
        /* Mobile menu */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text-primary);
            cursor: pointer;
            padding: 8px;
        }
        
        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: block;
            }
        }
    '''

def generate_share_icons():
    """SVG icons for social sharing"""
    return {
        'twitter': '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
        'linkedin': '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
        'copy': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>',
        'arrow': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>',
        'github': '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
        'search': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>',
        'close': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>',
    }

def generate_header_html(css, icons, active='home'):
    """Generate header HTML with search functionality"""
    home_active = 'active' if active == 'home' else ''
    articles_active = 'active' if active == 'articles' else ''
    search_active = 'active' if active == 'search' else ''
    
    return f'''
    <header class="site-header">
        <div class="header-container">
            <a href="index.html" class="logo">
                <div class="logo-icon">🤖</div>
                <div class="logo-text">
                    <span class="logo-title">Tanner's Tech News</span>
                    <span class="logo-tagline">AI-Curated Daily</span>
                </div>
            </a>
            <nav class="nav-links">
                <a href="index.html" class="nav-link {home_active}">Home</a>
                <a href="index.html#articles" class="nav-link {articles_active}">Articles</a>
                <a href="search.html" class="nav-link {search_active}">Search</a>
                <a href="https://github.com/dano311/tanners-tech-news" target="_blank" rel="noopener" class="github-link">
                    {icons['github']} GitHub
                </a>
            </nav>
            <div class="search-container">
                <button class="search-toggle" onclick="toggleSearch()" aria-label="Search">{icons['search']}</button>
                <div class="search-bar" id="searchBar">
                    <div class="search-input-wrapper">
                        <input type="text" class="search-input" id="searchInput" placeholder="Search articles..." autocomplete="off">
                        <button class="search-close" onclick="toggleSearch()" aria-label="Close search">{icons['close']}</button>
                    </div>
                    <div id="searchResults" class="search-results"></div>
                </div>
            </div>
            <button class="mobile-menu-btn" aria-label="Menu">☰</button>
        </div>
    </header>
    '''

def generate_search_script():
    """Generate the search JavaScript"""
    return '''
    <script>
        // Initialize Pagefind search
        let pagefind;
        document.addEventListener('DOMContentLoaded', async function() {
            try {
                pagefind = await import('/_pagefind/pagefind.js');
                await pagefind.init();
                console.log('Pagefind search initialized');
            } catch (e) {
                console.log('Pagefind not yet indexed, search will work after indexing');
            }
        });
        
        // Toggle search bar
        function toggleSearch() {
            const searchBar = document.getElementById('searchBar');
            const searchInput = document.getElementById('searchInput');
            searchBar.classList.toggle('active');
            if (searchBar.classList.contains('active')) {
                searchInput.focus();
            } else {
                searchInput.value = '';
                document.getElementById('searchResults').innerHTML = '';
            }
        }
        
        // Search input handler
        const searchInput = document.getElementById('searchInput');
        let searchTimeout;
        
        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                clearTimeout(searchTimeout);
                const query = e.target.value.trim();
                const resultsContainer = document.getElementById('searchResults');
                
                if (query.length < 2) {
                    resultsContainer.innerHTML = '';
                    return;
                }
                
                searchTimeout = setTimeout(async () => {
                    if (!pagefind) {
                        resultsContainer.innerHTML = '<div class="search-result-item"><div class="search-result-excerpt">Loading search...</div></div>';
                        return;
                    }
                    
                    try {
                        const search = await pagefind.search(query);
                        const results = await Promise.all(search.results.slice(0, 5).map(r => r.data()));
                        
                        if (results.length === 0) {
                            resultsContainer.innerHTML = '<div class="search-result-item"><div class="search-result-excerpt">No results found</div></div>';
                            return;
                        }
                        
                        resultsContainer.innerHTML = results.map(r => {
                            const title = r.meta?.title || r.url;
                            const excerpt = r.excerpt || '';
                            return `<div class="search-result-item" onclick="window.location.href='${r.url}'">
                                <div class="search-result-title">${title}</div>
                                <div class="search-result-excerpt">${excerpt.substring(0, 100)}...</div>
                            </div>`;
                        }).join('') + 
                        '<div class="search-result-item" style="text-align: center;"><a href="search.html?q=' + encodeURIComponent(query) + '" style="color: var(--accent-color); text-decoration: none; font-size: 0.875rem;">View all results →</a></div>';
                    } catch (err) {
                        console.error('Search error:', err);
                        resultsContainer.innerHTML = '<div class="search-result-item"><div class="search-result-excerpt">Search error. Try again.</div></div>';
                    }
                }, 300);
            });
        }
        
        // Close search on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const searchBar = document.getElementById('searchBar');
                if (searchBar && searchBar.classList.contains('active')) {
                    toggleSearch();
                }
            }
        });
        
        // Close search when clicking outside
        document.addEventListener('click', function(e) {
            const searchContainer = document.querySelector('.search-container');
            const searchBar = document.getElementById('searchBar');
            if (searchContainer && searchBar && !searchContainer.contains(e.target) && searchBar.classList.contains('active')) {
                toggleSearch();
            }
        });
    </script>
    '''

def generate_footer_html():
    """Generate footer HTML"""
    return '''
    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-grid">
                <div class="footer-section">
                    <h4>📰 About</h4>
                    <p style="color: var(--text-secondary); font-size: 0.875rem; line-height: 1.6; margin: 0;">
                        Tanner's Tech News is an AI-curated daily tech roundup. We scrape the best stories from across the web and summarize them with wit and insight. Fresh every morning at 8am.
                    </p>
                    <div style="margin-top: 16px;">
                        <a href="mailto:tanner@clawbox.us" class="footer-contact-link">📧 tanner@clawbox.us</a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h4>🔗 Quick Links</h4>
                    <ul class="footer-links">
                        <li><a href="index.html">Home</a></li>
                        <li><a href="search.html">Search</a></li>
                        <li><a href="mailto:tanner@clawbox.us">Contact</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>📂 Categories</h4>
                    <ul class="footer-links">
                        <li><a href="index.html">AI</a></li>
                        <li><a href="index.html">Hardware</a></li>
                        <li><a href="index.html">Privacy</a></li>
                        <li><a href="index.html">Security</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>💰 Advertise</h4>
                    <p style="color: var(--text-secondary); font-size: 0.875rem; line-height: 1.6; margin: 0 0 12px 0;">
                        Reach tech-savvy readers. Starting at $50/week.
                    </p>
                    <a href="mailto:ads@clawbox.us" class="advertise-btn">Inquire Now</a>
                </div>
            </div>
            
            <div class="footer-bottom">
                <div class="footer-logo">
                    <span>🤖</span>
                    Tanner's Tech News
                </div>
                <p class="footer-credits">
                    © 2026 Tanner's Tech News • Generated with ❤️ by AI • Powered by Firecrawl + Ollama<br>
                    <a href="https://github.com/dano311/tanners-tech-news">View on GitHub</a>
                </p>
            </div>
        </div>
    </footer>
    '''

def generate_site():
    """Generate static HTML site from markdown posts"""
    posts_dir = '/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/posts'
    docs_dir = '/home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/docs'
    
    os.makedirs(docs_dir, exist_ok=True)
    
    css = generate_css()
    icons = generate_share_icons()
    
    # Category counts
    category_counts = {}
    
    posts = []
    for filename in sorted(os.listdir(posts_dir), reverse=True):
        if filename.endswith('.md'):
            with open(f'{posts_dir}/{filename}', 'r') as f:
                content = f.read()
            
            title = filename.replace('.md', '')
            date = filename.replace('.md', '')
            author = "Tanner (AI)"
            tags = []
            sources = []
            
            body = content
            
            # Parse frontmatter
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    meta = parts[1]
                    body = parts[2]
                    for line in meta.split('\n'):
                        if line.startswith('title:'):
                            title = line.split(':', 1)[1].strip().strip('"').strip("'")
                        if line.startswith('date:'):
                            date = line.split(':', 1)[1].strip().strip('"').strip("'")
                        if line.startswith('author:'):
                            author = line.split(':', 1)[1].strip().strip('"').strip("'")
                        if line.startswith('tags:'):
                            tags_str = line.split(':', 1)[1].strip()
                            tags = [t.strip().strip('"').strip("'") for t in tags_str.strip('[]').split(',') if t.strip()]
                        if line.startswith('sources:'):
                            sources_str = line.split(':', 1)[1].strip()
                            sources = [s.strip().strip('"').strip("'") for s in sources_str.strip('[]').split(',') if s.strip()]
            
            category = get_category_for_post(body, title)
            category_counts[category] = category_counts.get(category, 0) + 1
            
            html_body = markdown_to_html(body.strip())
            post_slug = filename.replace('.md', '.html')
            read_time = estimate_read_time(body)
            
            # Format date nicely
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%B %d, %Y')
            except:
                formatted_date = date
            
            cat_style = CATEGORY_STYLES.get(category, CATEGORY_STYLES['General'])
            
            # Generate individual post page
            post_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Tanner's Tech News</title>
    <meta name="description" content="Daily tech news curated by AI">
    <style>{css}</style>
</head>
<body>
    {generate_header_html(css, icons, 'articles')}
    
    <main class="article-page">
        <a href="index.html" class="article-back">← Back to all articles</a>
        
        <article data-pagefind-body>
            <header class="article-header">
                <span class="category-badge" style="background-color: {cat_style['bg']}; color: {cat_style['color']};">
                    {cat_style['icon']} {category}
                </span>
                <h1 class="article-title" data-pagefind-meta="title">{title}</h1>
                <div class="article-meta">
                    <span>📅 {formatted_date}</span>
                    <span>•</span>
                    <span>⏱️ {read_time}</span>
                    <span>•</span>
                    <span>✍️ {author}</span>
                </div>
            </header>
            
            <div class="article-content">
                {html_body}
            </div>
            
            <div class="article-share">
                <h4>Share this article</h4>
                <div class="share-row">
                    <a href="https://twitter.com/intent/tweet?text={title.replace(' ', '%20')}&url=https://dano311.github.io/tanners-tech-news/{post_slug}" target="_blank" rel="noopener" class="share-btn-large twitter">
                        {icons['twitter']} Share on Twitter
                    </a>
                    <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://dano311.github.io/tanners-tech-news/{post_slug}" target="_blank" rel="noopener" class="share-btn-large linkedin">
                        {icons['linkedin']} Share on LinkedIn
                    </a>
                </div>
            </div>
        </article>
    </main>
    
    {generate_footer_html()}
    {generate_search_script()}
</body>
</html>'''
            
            with open(f'{docs_dir}/{post_slug}', 'w') as f:
                f.write(post_html)
            
            posts.append({
                'title': title,
                'date': date,
                'formatted_date': formatted_date,
                'slug': post_slug,
                'author': author,
                'excerpt': body[:250].replace('#', '').replace('*', '').strip() + '...',
                'category': category,
                'cat_style': cat_style,
                'read_time': read_time,
                'tags': tags,
                'sources': sources
            })
    
    # Sort categories by count
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Generate article cards for index
    posts_html = ''
    for post in posts[:10]:
        cat = post['cat_style']
        posts_html += f'''
        <article class="article-card" onclick="window.location.href='{post['slug']}'">
            <div class="article-card-header">
                <span class="category-badge" style="background-color: {cat['bg']}; color: {cat['color']};">
                    {cat['icon']} {post['category']}
                </span>
                <div class="article-meta">
                    <span>📅 {post['formatted_date']}</span>
                    <span>⏱️ {post['read_time']}</span>
                </div>
            </div>
            <h2 class="article-title"><a href="{post['slug']}">{post['title']}</a></h2>
            <p class="article-excerpt">{post['excerpt']}</p>
            <div class="article-footer">
                <a href="{post['slug']}" class="read-more">
                    Read more {icons['arrow']}
                </a>
                <div class="share-buttons">
                    <button class="share-btn" onclick="event.stopPropagation(); window.open('https://twitter.com/intent/tweet?text={post['title'].replace(' ', '%20')}&url=https://dano311.github.io/tanners-tech-news/{post['slug']}', '_blank')" aria-label="Share on Twitter">
                        {icons['twitter']}
                    </button>
                    <button class="share-btn" onclick="event.stopPropagation(); window.open('https://www.linkedin.com/sharing/share-offsite/?url=https://dano311.github.io/tanners-tech-news/{post['slug']}', '_blank')" aria-label="Share on LinkedIn">
                        {icons['linkedin']}
                    </button>
                </div>
            </div>
        </article>
        '''
    
    # Generate category list for sidebar
    categories_html = ''
    for cat_name, count in sorted_categories[:8]:
        cat = CATEGORY_STYLES.get(cat_name, CATEGORY_STYLES['General'])
        categories_html += f'''
        <li><a href="#" style="--category-color: {cat['color']}">
            <span>{cat['icon']}</span>
            {cat_name}
            <span class="category-count">{count}</span>
        </a></li>
        '''
    
    # Generate index page
    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tanner's Tech News - AI-Curated Daily Tech Roundup</title>
    <meta name="description" content="Daily tech news curated by AI. Fresh every morning with stories from Hacker News, TechCrunch, The Verge, and more.">
    <style>{css}</style>
</head>
<body>
    {generate_header_html(css, icons, 'home')}
    
    <section class="hero">
        <div class="hero-content">
            <div class="hero-badge">
                <span>⚡</span> Fresh every morning at 8am
            </div>
            <h1 class="hero-title">Your Daily Dose of Tech News</h1>
            <p class="hero-subtitle">AI-curated stories from Hacker News, TechCrunch, The Verge, Ars Technica, and Reddit. No fluff, just what matters.</p>
            <div class="hero-stats">
                <div class="stat">
                    <div class="stat-value">{len(posts)}</div>
                    <div class="stat-label">Articles</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(CATEGORY_STYLES)}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat">
                    <div class="stat-value">5</div>
                    <div class="stat-label">Sources</div>
                </div>
            </div>
        </div>
    </section>
    
    <div class="main-container" id="articles">
        <main class="articles-section">
            <div class="articles-header">
                <h2 class="section-title">Latest Articles</h2>
                <a href="search.html" class="view-all">Search articles →</a>
            </div>
            <div class="articles-grid">
                {posts_html}
            </div>
        </main>
        
        <aside class="sidebar">
            <div class="newsletter-section">
                <h3 class="newsletter-title">📬 Join 2,500+ tech readers</h3>
                <p class="newsletter-text">Get AI-curated news before everyone else. One email, every morning. No fluff.</p>
                <ul class="newsletter-benefits" style="list-style: none; margin: 16px 0; padding: 0; font-size: 0.85rem; opacity: 0.95;">
                    <li style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">✓ Daily AI-curated tech news</li>
                    <li style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">✓ 5-minute morning read</li>
                    <li style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">✓ Free forever, unsubscribe anytime</li>
                </ul>
                <div class="newsletter-social-proof" style="background-color: rgba(255,255,255,0.15); border-radius: 8px; padding: 12px; margin-bottom: 16px; text-align: center;">
                    <div style="font-size: 1.25rem; font-weight: 700;">2,547 readers</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">joined this month</div>
                </div>
                <form class="newsletter-form" onsubmit="event.preventDefault(); alert('Thanks for subscribing! This is a demo.');">
                    <input type="email" class="newsletter-input" placeholder="Enter your email" required>
                    <button type="submit" class="newsletter-btn">Join Free →</button>
                </form>
                <p class="newsletter-privacy" style="font-size: 0.75rem; opacity: 0.7; margin-top: 12px; text-align: center;">🔒 No spam. No selling. Unsubscribe anytime.</p>
            </div>
            
            <div class="sidebar-section">
                <h3 class="sidebar-title">📂 Categories</h3>
                <ul class="category-list">
                    {categories_html}
                </ul>
            </div>
            
            <div class="sidebar-section">
                <h3 class="sidebar-title">🔌 Powered by</h3>
                <ul class="category-list">
                    <li><a href="https://firecrawl.dev" target="_blank"><span>🔥</span> Firecrawl</a></li>
                    <li><a href="https://ollama.com" target="_blank"><span>🦙</span> Ollama</a></li>
                    <li><a href="https://github.com" target="_blank"><span>🐙</span> GitHub Pages</a></li>
                </ul>
            </div>
            
            <div class="sidebar-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; padding: 20px; margin-top: 24px;">
                <h3 class="sidebar-title" style="color: white;">☕ Support</h3>
                <p style="font-size: 0.875rem; margin-bottom: 16px; opacity: 0.9;">Help keep the bots caffeinated!</p>
                <a href="https://buymeacoffee.com/tannerstech" target="_blank" class="bmc-btn" style="display: inline-block; background: white; color: #764ba2; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.875rem; transition: all 0.2s;">Buy me a coffee</a>
            </div>
        </aside>
    </div>
    
    {generate_footer_html()}
    {generate_search_script()}
</body>
</html>'''
    
    with open(f'{docs_dir}/index.html', 'w') as f:
        f.write(index_html)
    
    # Generate search page
    search_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search | Tanner's Tech News</title>
    <meta name="description" content="Search articles from Tanner's Tech News - AI-curated daily tech roundup">
    <style>{css}</style>
</head>
<body>
    {generate_header_html(css, icons, 'search')}
    
    <main class="search-page">
        <h1 class="search-page-title">🔍 Search Articles</h1>
        
        <div class="search-page-input-wrapper">
            <span class="search-page-input-icon">{icons['search']}</span>
            <input type="text" class="search-page-input" id="searchPageInput" placeholder="Search articles..." autocomplete="off">
        </div>
        
        <div class="search-stats" id="searchStats"></div>
        <div class="search-page-results" id="searchPageResults"></div>
    </main>
    
    {generate_footer_html()}
    
    <script>
        let pagefind;
        const searchInput = document.getElementById('searchPageInput');
        const resultsContainer = document.getElementById('searchPageResults');
        const statsContainer = document.getElementById('searchStats');
        
        document.addEventListener('DOMContentLoaded', async function() {{
            try {{
                pagefind = await import('/_pagefind/pagefind.js');
                await pagefind.init();
                console.log('Pagefind search initialized');
                
                // Check for query param
                const urlParams = new URLSearchParams(window.location.search);
                const query = urlParams.get('q');
                if (query) {{
                    searchInput.value = query;
                    performSearch(query);
                }}
            }} catch (e) {{
                console.log('Pagefind not yet indexed, search will work after indexing');
            }}
            
            searchInput.focus();
        }});
        
        let searchTimeout;
        searchInput.addEventListener('input', function(e) {{
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length < 2) {{
                resultsContainer.innerHTML = '';
                statsContainer.innerHTML = '';
                return;
            }}
            
            searchTimeout = setTimeout(() => performSearch(query), 300);
        }});
        
        async function performSearch(query) {{
            if (!pagefind) {{
                resultsContainer.innerHTML = '<div style="text-align: center; padding: 48px; color: var(--text-muted);">Loading search index...</div>';
                return;
            }}
            
            try {{
                const search = await pagefind.search(query);
                const results = await Promise.all(search.results.map(r => r.data()));
                
                if (results.length === 0) {{
                    statsContainer.innerHTML = '';
                    resultsContainer.innerHTML = '<div style="text-align: center; padding: 48px; color: var(--text-muted);"><p>No results found for "' + escapeHtml(query) + '"</p><p style="font-size: 0.875rem; margin-top: 8px;">Try different keywords or check your spelling</p></div>';
                    return;
                }}
                
                statsContainer.innerHTML = 'Found ' + results.length + ' result' + (results.length !== 1 ? 's' : '') + ' for "' + escapeHtml(query) + '"';
                
                resultsContainer.innerHTML = results.map(r => {{
                    const title = r.meta?.title || r.url;
                    const excerpt = r.excerpt || '';
                    return `<a href="${{r.url}}" class="search-result-card" style="display: block; text-decoration: none;">
                        <div class="search-result-title">${{title}}</div>
                        <div class="search-result-excerpt">${{excerpt}}</div>
                    </a>`;
                }}).join('');
            }} catch (err) {{
                console.error('Search error:', err);
                resultsContainer.innerHTML = '<div style="text-align: center; padding: 48px; color: var(--text-muted);">Search error. Please try again.</div>';
            }}
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
    </script>
    
    
</body>
</html>'''
    
    with open(f'{docs_dir}/search.html', 'w') as f:
        f.write(search_html)
    
    print(f'✅ Generated site with {len(posts)} posts')
    print(f'📁 Site location: {docs_dir}/')
    print(f'🌐 URL: https://tannerclaw.github.io/tanners-tech-news/')
    print(f'\n📊 Categories:')
    for cat, count in sorted_categories:
        print(f'   • {cat}: {count} posts')
    print(f'\n🔍 Search page: {docs_dir}/search.html')

if __name__ == '__main__':
    generate_site()
