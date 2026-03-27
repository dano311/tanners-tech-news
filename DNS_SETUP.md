# 🌐 Dyad Labs - DNS Configuration
## Domain: dyadlabs.us

## Step 1: Add CNAME File to Repo
Create file: `docs/CNAME` with content:
```
tanners-tech-news.dyadlabs.us
```

## Step 2: Configure Cloudflare DNS

Add these DNS records in Cloudflare:

### For tanners-tech-news.dyadlabs.us (blog)
```
Type: CNAME
Name: tanners-tech-news
Target: dano311.github.io
TTL: Auto
```

### For root domain (dyadlabs.us)
```
Type: A
Name: @
Target: 185.199.108.153
Target: 185.199.109.153
Target: 185.199.110.153
Target: 185.199.111.153
TTL: Auto
```

### For www
```
Type: CNAME
Name: www
Target: dyadlabs.us
TTL: Auto
```

## Step 3: Enable HTTPS in GitHub
1. Go to: https://github.com/dano311/tanners-tech-news/settings/pages
2. Check "Enforce HTTPS"
3. Wait 5-10 minutes

## Step 4: SSL/TLS Settings in Cloudflare
1. Go to SSL/TLS tab
2. Set to "Full (strict)"
3. Enable "Always Use HTTPS"

## Final URLs
- Blog: https://tanners-tech-news.dyadlabs.us
- Company: https://dyadlabs.us (when you add site)

## Status Check
Run: dig tanners-tech-news.dyadlabs.us
Should show: dano311.github.io