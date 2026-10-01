---
name: seo-aeo-geo-playbook
description: Prioritized playbook for SEO (Google/Bing), AEO (answer engines) and GEO (AI citations) on the Young Stunners site. Use when planning or implementing any search/AI-visibility change.
---

# SEO / AEO / GEO playbook

Evidence and sources: `docs/research/2026-10-01-seo-aeo-geo.md`. Read its backlog first.

## Order of work
1. **Indexed + crawlable** (Search Console, Bing, sitemap, robots allows OAI-SearchBot / PerplexityBot / ClaudeBot / Google-Extended). Nothing else matters until this is true.
2. **Own domain** (see `custom-domain-setup`). Project sites under `github.io/titanx` cannot serve a root robots.txt/sitemap.
3. **Specifics**: real, owner-confirmed numbers and quotes. Never invent.
4. **Answer-first copy**: each section opens with one plain sentence under ~150 characters that names "Young Stunners" and stands alone.
5. **Entity**: Organization JSON-LD with `sameAs` (X @youngstunnersss, Instagram @chris1dragon), same name and handles everywhere.
6. **Freshness**: visible "Last updated" + `dateModified` that match, bumped only on real content change.
7. **Measure**: `ai-visibility-tracking`, PostHog funnel.

## Rules
- Schema must match visible content. No fake ratings, reviews, prices, or hidden FAQs.
- Keep the visible FAQ; do not emit FAQPage JSON-LD on this promotional page (Google retired FAQ rich results on 7 May 2026 and warns against promo FAQ markup).
- llms.txt is cheap and kept in sync, but has no measured citation effect. Do not spend time on it.
- Titles <= 60 chars, descriptions 120-160, one H1, canonical on every page.
- Run `python3 scripts/check_site.py` before every commit (see `site-audit`).
