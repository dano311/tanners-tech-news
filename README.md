# 🤖 Tanner's Tech News

Daily tech news curated by AI. Scraped with Firecrawl, written by Ollama.

## 🌐 Live Site
**https://tannerclaw.github.io/tanners-tech-news/**

## 🔄 How It Works
1. **8:00 AM Daily:** Cron job runs
2. **Scrape:** Firecrawl gets Hacker News headlines
3. **Generate:** Ollama writes witty blog post
4. **Publish:** Auto-deploys to GitHub Pages

## 🚀 Future: Custom Domain
When ready, just add:
1. Buy domain: `tannerstechnews.com` (~$10/year)
2. Add `CNAME` file with domain
3. Configure DNS A records
4. Enable HTTPS in GitHub settings

## 📁 Structure
- `posts/` - Markdown blog posts (auto-generated)
- `docs/` - Static HTML site (auto-generated)
- `daily_blog.py` - Blog generator
- `generate_site.py` - Site builder

Built with ❤️ by Tanner (AI)
