# SEO Deployment Checklist

## Before Deployment
- [ ] All meta tags reviewed and customized
- [ ] Social media images created (1200x630 for OG, 1200x600 for Twitter)
- [ ] Images uploaded to `/static/images/` folder
- [ ] Sitemap includes all public pages
- [ ] robots.txt configured correctly
- [ ] Private pages have `noindex, nofollow`

## After Deployment
- [ ] Visit `/sitemap.xml` - verify it works
- [ ] Visit `/robots.txt` - verify it loads
- [ ] Test homepage meta tags with view-source
- [ ] Test Open Graph with Facebook Debugger
- [ ] Test Twitter Card with Twitter Validator
- [ ] Run Google Rich Results Test
- [ ] Check PageSpeed Insights score
- [ ] Verify mobile responsiveness

## Search Engine Submission
- [ ] Create Google Search Console account
- [ ] Add property (domain or URL prefix)
- [ ] Verify ownership (HTML tag or DNS)
- [ ] Submit sitemap: https://yoursite.com/sitemap.xml
- [ ] Create Bing Webmaster Tools account
- [ ] Add site and verify
- [ ] Submit sitemap to Bing

## Analytics Setup
- [ ] Create Google Analytics 4 property
- [ ] Add GA4 tracking code to base.html
- [ ] Set up conversion goals
- [ ] Enable Search Console integration
- [ ] Test data collection

## Ongoing Maintenance (Weekly)
- [ ] Check Google Search Console for errors
- [ ] Review search performance reports
- [ ] Monitor page speed
- [ ] Check for broken links
- [ ] Review crawl stats

## Monthly Tasks
- [ ] Update meta descriptions for better CTR
- [ ] Analyze top-performing keywords
- [ ] Create new content
- [ ] Update sitemap if needed
- [ ] Review competitor rankings

## Important URLs
- Homepage: https://notifier-dpvz.onrender.com/
- Sitemap: https://notifier-dpvz.onrender.com/sitemap.xml
- Robots: https://notifier-dpvz.onrender.com/robots.txt
- Health: https://notifier-dpvz.onrender.com/healthz

## Testing Tools
- Google Rich Results: https://search.google.com/test/rich-results
- Facebook Debugger: https://developers.facebook.com/tools/debug/
- Twitter Validator: https://cards-dev.twitter.com/validator
- PageSpeed Insights: https://pagespeed.web.dev/
- Google Search Console: https://search.google.com/search-console
- Bing Webmaster: https://www.bing.com/webmasters

## Notes
- First indexing can take 1-4 weeks
- Re-crawl can be requested in Search Console
- Monitor rankings with tools like Ahrefs, SEMrush, or free alternatives
- Keep meta descriptions under 160 characters
- Keep title tags under 60 characters
- Focus on content quality over SEO tricks
