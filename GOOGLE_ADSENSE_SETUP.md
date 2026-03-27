# 📊 Google AdSense Setup - 5 Minute Guide

## Step 1: Apply (2 minutes)
1. Go to: https://www.google.com/adsense
2. Click "Get Started"
3. Sign in with your Gmail
4. Enter your site URL: `https://tanners-tech-news.dyadlabs.us`
5. Enter your email (you@yourdomain.com or Gmail)
6. Check "Yes" to get tips
7. Click "Start using AdSense"

## Step 2: Connect Your Site

### Option A: HTML Meta Tag (Easiest)
AdSense will give you a code like:
```html
<meta name="google-adsense-account" content="ca-pub-XXXXXXXXXXXXXXXX">
```

Add this to your site's `<head>` section.

### Option B: ads.txt File
Create file: `docs/ads.txt`
With content:
```
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```
(Replace with your actual publisher ID)

## Step 3: Submit for Review
- Click "Request review" in AdSense dashboard
- Wait 1-2 weeks for approval

## Step 4: Once Approved (After approval)

### Add Ad Units to Site

**Sidebar Ad (300x250):**
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

**In-Article Ad:**
Place between paragraphs in articles

**Sticky Footer (Mobile):**
320x50 mobile banner at bottom

## Expected Revenue

| Visitors/Month | Estimated Earnings |
|----------------|-------------------|
| 1,000 | $10-30 |
| 5,000 | $50-150 |
| 10,000 | $100-300 |
| 50,000 | $500-1,500 |

## Tips for Approval

✅ DO:
- Have 10+ articles/posts
- Original content (your AI articles count!)
- Privacy policy page
- Contact page
- About page
- Clean navigation

❌ DON'T:
- Copy content from others
- Have broken links
- Adult/explicit content
- Copyright violations

## After Approval

1. Add ads.txt to your site
2. Place ad units strategically
3. Monitor performance in AdSense dashboard
4. Optimize placements based on earnings

## Links

- AdSense Dashboard: https://www.google.com/adsense
- AdSense Help: https://support.google.com/adsense
- Policy Center: Check for violations

## Timeline

- **Apply:** Today (5 min)
- **Review:** 1-2 weeks
- **First Earnings:** After approval + traffic

**Ready to apply?** 🚀
