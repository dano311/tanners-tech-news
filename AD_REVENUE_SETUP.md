# 💰 Ad Revenue Setup for Tanner's Tech News

## Current Status
- Blog is live: https://dano311.github.io/tanners-tech-news/
- "Advertise" section added to footer
- Contact: ads@clawbox.us

## Stripe Integration Plan

### Option 1: Simple Stripe Payment Links (Recommended to start)
**Setup:**
1. Go to https://dashboard.stripe.com/payment-links
2. Create payment links for ad packages:
   - $50/week - Sidebar ad
   - $150/month - Sidebar ad
   - $300/month - Featured article slot
   - $500/month - Homepage hero banner

**Pros:**
- No code required
- Instant setup
- Automatic receipts

### Option 2: Stripe Checkout Integration (Later)
**When traffic grows, embed checkout directly**

### Option 3: Ad Management Platform (Scale)
**When you have 1000+ monthly visitors:**
- Google AdSense (easiest)
- Carbon Ads (tech-focused)
- BuySellAds (marketplace)
- EthicalAds (developer-focused)

---

## Pricing Structure

### Current (Just starting)
**Manual Process:**
- Email ads@clawbox.us
- Pay via Stripe Payment Link
- I manually add the ad

| Package | Price | Placement | Duration |
|---------|-------|-----------|----------|
| Starter | $50/week | Sidebar | 7 days |
| Growth | $150/month | Sidebar | 30 days |
| Featured | $300/month | Article slot | 30 days |
| Hero | $500/month | Homepage banner | 30 days |

### Metrics to Track
Once you have traffic:
- Monthly visitors (Google Analytics)
- Page views
- Click-through rates
- Newsletter subscribers

---

## Setup Steps

### 1. Create Stripe Account (Free)
1. Go to https://stripe.com
2. Sign up with your email
3. Complete verification
4. Get API keys

### 2. Create Payment Links
```
Stripe Dashboard → Payment Links → Create
```

### 3. Update Contact Email
- Currently: ads@clawbox.us
- Forward to your actual email
- Or set up in ProtonMail

### 4. Add Ads Page
Create `/advertise.html` with:
- Pricing table
- Audience stats (when you have them)
- Contact form
- Stripe buy buttons

### 5. First Ad Strategy
- Offer 50% discount to first 3 advertisers
- Target: Indie dev tools, AI products, newsletters
- Manual process until you have workflow

---

## Revenue Goals

**Month 1-3:** $0 (building traffic)
**Month 4-6:** $100-300/month (1-2 advertisers)
**Month 7-12:** $500-1000/month (3-5 advertisers)
**Year 2:** $2000+/month (ad platform)

---

## Next Steps
1. ✅ Add "Advertise" section to footer
2. ⏳ Create Stripe account
3. ⏳ Set up Payment Links
4. ⏳ Create /advertise.html page
5. ⏳ Get traffic (SEO, social, HN)
6. ⏳ Track with Google Analytics
7. ⏳ First advertiser!

**Ready to create Stripe account?**