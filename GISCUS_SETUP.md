# Giscus Comments Setup

## What is Giscus?
Giscus is a comments system powered by GitHub Discussions. It allows visitors to comment on your blog using their GitHub account, while comments are stored as GitHub Discussions - keeping everything in one place.

## Setup Status

### 1. GitHub Discussions Enabled ✅
- ✅ Discussions enabled for `dano311/tanners-tech-news` repository
- ✅ Using "General" discussion category for blog comments
- Category ID: `DIC_kwDORyQVHM4C5bvj`

### 2. Giscus Configuration ✅
```javascript
data-repo="dano311/tanners-tech-news"
data-repo-id="R_kgDORyQVHA"
data-category="General"
data-category-id="DIC_kwDORyQVHM4C5bvj"
data-mapping="pathname"  // Uses URL pathname as discussion identifier
data-theme="preferred_color_scheme"  // Auto-detects light/dark mode
data-reactions-enabled="1"  // Allows emoji reactions
data-input-position="bottom"
```

### 3. Theme Matching ✅
- Comments automatically adapt to user's system preference (light/dark mode)
- Matches the site's existing CSS variables for seamless integration
- Comments section styled with:
  - Consistent spacing and borders
  - Theme-appropriate colors
  - Mobile-responsive design

### 4. Article Integration ✅
- Giscus comments are now included in every generated article page
- Positioned after the share buttons
- Comments section has a clear heading: "💬 Comments"
- Description text informs users that GitHub Discussions powers the comments

### 5. Manual Step Required: Install Giscus GitHub App ⚠️

**Action Required:** The Giscus GitHub App needs to be installed on the repository for comments to work.

**To complete the setup:**

1. Go to: https://github.com/apps/giscus
2. Click **"Install"** or **"Configure"**
3. Select **`dano311/tanners-tech-news`** repository
4. Choose permissions (recommend: "Only select repositories" → select this one)
5. Click **"Install"**

**Why this is needed:**
- Giscus requires the GitHub App to create and manage discussions on your behalf
- Without this, visitors will see: "giscus is not installed on this repository"
- The app only needs read/write access to Discussions - no code access required

**After installation:**
- Comments will work immediately on all articles
- First comment on any article auto-creates the discussion thread
- You can verify by visiting: https://tanners-tech-news.dyadlabs.us/2026-03-27.html

### 5. How It Works
1. When a visitor views an article, Giscus loads the GitHub Discussion associated with that URL
2. If no discussion exists yet, Giscus creates one automatically
3. Visitors can comment using their GitHub account
4. Comments sync bidirectionally with GitHub Discussions

### 6. Files Modified
- `generate_site.py` - Updated to include Giscus script in article templates
- `docs/2026-03-27.html` - Regenerated with comments section

### 7. Testing
To test the comments:
1. Visit: https://tannerclaw.github.io/tanners-tech-news/2026-03-27.html
2. Scroll to the bottom of the article
3. You should see the "💬 Comments" section
4. If logged into GitHub, you can leave a comment

### 8. Benefits
- No separate comment database - everything is on GitHub
- Spam filtering via GitHub's moderation tools
- Notifications for new comments via GitHub
- Reactions support (👍, ❤️, etc.)
- Free and open source
- Works with static sites (like GitHub Pages)

## Summary

✅ GitHub Discussions enabled for repository  
✅ Giscus script configured with theme matching  
✅ Comments section added to article template  
✅ Site regenerated and deployed  
⚠️ **Pending:** GitHub App installation (requires manual action)

Once the Giscus GitHub App is installed, visitors can leave comments using their GitHub accounts, and all comments will be stored as GitHub Discussions in the repository.
