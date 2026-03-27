# 🚀 Tanner's Tech News - DEPLOY GUIDE

## Step 1: Authenticate GitHub (Run this)
```bash
gh auth login
# Follow prompts (choose HTTPS, login with browser)
```

## Step 2: Push to GitHub (Then run this)
```bash
cd /home/dan/.openclaw/workspace/tanner-business/tanners-tech-news
git push -u origin main
```

## Step 3: Enable GitHub Pages
1. Go to: https://github.com/tannerclaw/tanners-tech-news/settings/pages
2. Under "Build and deployment"
3. Source: **Deploy from a branch**
4. Branch: **main** / **docs** folder
5. Click Save

## Step 4: Your Site is LIVE! 🎉
**URL:** https://tannerclaw.github.io/tanners-tech-news/

Takes 2-5 minutes to deploy after push.

## Step 5: Daily Automation (Already Set Up!)
- Blog generates at **8:00 AM daily**
- Auto-commits to Git
- Auto-deploys to GitHub Pages
- You just need to `git push` daily (or set up auto-push)

## Custom Domain (Future)
When ready:
1. Buy domain (Namecheap, ~$10/year)
2. Add file: `docs/CNAME` with your domain
3. Configure DNS A records to GitHub Pages IPs
4. Enable HTTPS in settings

## Current Status
✅ Blog content generated  
✅ HTML site built  
✅ GitHub repo created  
⏳ Waiting for: GitHub authentication  
⏳ Waiting for: Enable GitHub Pages

Ready to run `gh auth login`?
