---
name: custom-domain-setup
description: Move the Young Stunners site from youngstunners88.github.io/titanx to an owned domain for SEO. Use only after the owner approves a domain name and any purchase.
---

# Custom domain setup

Why: a brand domain is the biggest structural SEO win. On `github.io/titanx`, robots.txt and sitemap.xml are not read from the root, and authority is shared with the github.io host.

## Ask first
Do not buy or change DNS without the owner's explicit approval of the exact domain and price. Suggest 2-3 names (for example youngstunners.xyz, youngstunners.io) and say the cost.

## Steps
1. **Check availability / register** (owner approved): NameSilo API (`$NAMESILO_API_KEY`) `checkRegisterAvailability`, then `registerDomain`. Or register via Cloudflare dashboard. Use the narrowest call; do not list unrelated account data.
2. **DNS** (Cloudflare, `$CLOUDFLARE_API_KEY` with `$CLOUDFLARE_ACCOUNT_ID`): add the zone, set nameservers at the registrar, then GitHub Pages records: apex A records 185.199.108.153 / .109.153 / .110.153 / .111.153 and `www` CNAME to `youngstunners88.github.io`. Set Cloudflare proxy to DNS-only until GitHub issues the certificate.
3. **GitHub**: repo Settings > Pages > custom domain `www.<domain>`, enforce HTTPS. Add a `CNAME` file containing the domain at the repo root. Verify the domain in GitHub account settings (prevents takeover).
4. **Update the site**: canonical, `og:url`, OG/Twitter image URLs, JSON-LD `@id`/`url`, `sitemap.xml` `<loc>`, `robots.txt` `Sitemap:` line, llms.txt links. Search for `youngstunners88.github.io/titanx` and replace everywhere.
5. **Redirect**: the old project URL cannot 301 to a new host on Pages. Keep canonical pointing to the new domain and update X/Instagram bios.
6. **Search Console + Bing**: add the domain property (DNS TXT), submit `https://<domain>/sitemap.xml`, import to Bing.
7. Run `site-audit`.
