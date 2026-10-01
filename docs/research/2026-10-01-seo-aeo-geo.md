# SEO / AEO / GEO deep dive for youngstunners88.github.io/titanx

Researched 2026-10-01 (Exa web search). Sources are listed at the end. Where sources disagree, this says so.

## What the evidence says

**1. Indexing and access come first.** AI Overviews and AI Mode need only an indexed, snippet-eligible page; there is no extra schema or submission. ChatGPT search uses OAI-SearchBot, and no major AI crawler runs JavaScript. The site is plain static HTML, so the text is already crawlable. Action: get indexed (Search Console + Bing), keep robots allowing OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended.

**2. Answer-first, short, self-contained passages get quoted.** Cited text windows are about 150 characters. Lead each section with the answer, name the subject ("Young Stunners"), no hedging. Question-style headings help. Action: FAQ answers are one or two plain sentences.

**3. Checkable specifics beat generic claims.** Figures with a method and date are the strongest citation driver (Princeton GEO study: statistics +~41% visibility, quotes/citations +30-40%). Action: publish verifiable numbers only (38 portfolio projects each linking a live post). Never invent metrics. Best next step: add real per-campaign results (views, followers gained) once the owner can confirm them.

**4. Freshness is a gate.** Retrieval exposes page age. Action: visible "Last updated" date plus matching `dateModified`; only bump it when content really changes.

**5. Entity clarity.** Organization schema with `sameAs` (X, Instagram) and consistent name/handle everywhere helps engines tie the brand together. Action: done. Next: add the same handle/name on X and Instagram bios and link back to the site.

**6. Schema is hygiene, not a lever.** Google retired FAQ rich results (restricted Aug 2023, gone 7 May 2026). Sources disagree on keeping FAQPage on promotional pages: one says never on promo pages, others say harmless. Decision: keep the visible FAQ for readers and answer engines, but do NOT emit FAQPage JSON-LD on this promotional landing page.

**7. llms.txt has no measured citation effect.** A Nov 2025 study of 300,000 domains found none; Google says Search does not use it. It costs nothing and helps coding agents, so it stays, but it is not a priority.

**8. GitHub Pages limits.** A project site lives under `/titanx/` on the shared github.io host. `robots.txt` and `sitemap.xml` are only honored at a host root, and a brand domain builds authority and clean CTR. A custom domain is the single biggest structural upgrade. Note: moving later needs 301s, so decide early.

**9. Short copy converts better.** Homepage guidance: outcome headline, one primary CTA, proof early, short paragraphs. Portfolio-first for creators. Action: copy cut to about 325 words outside the portfolio, enforced by `scripts/check_site.py` (budget 400).

## Prioritized backlog

| # | Action | Needs | Impact |
|---|--------|-------|--------|
| 1 | Verify site in Google Search Console + Bing Webmaster, submit `sitemap.xml` | owner login or DNS/meta tag | High: nothing ranks until indexed |
| 2 | Register and attach a custom domain (www + apex), update canonical/sitemap/OG/schema | owner approval to buy; see `custom-domain-setup` skill | High |
| 3 | Add real results per campaign (views, follower growth, launch outcomes) | owner data | High for GEO and conversion |
| 4 | Add 2-3 client quotes with names/handles, only if real | owner | High for trust |
| 5 | Per-service pages (`/video-content/`, `/kol-promotion/`) with answer-first copy | build | Medium, adds topical depth |
| 6 | Video thumbnails/posters for top 6 posts, lazy loaded | media; see `site-media-assets` | Medium |
| 7 | Analytics: PostHog events for CTA click, brief submit, X DM open | PostHog key | Medium: tells us what converts |
| 8 | Weekly AI-visibility sampling | see `ai-visibility-tracking` | Measurement |
| 9 | Keep X/Instagram bios consistent and linking to the site | owner | Medium entity signal |

## Sources
- Oppira, How to Get Cited by AI Answer Engines (2026-07)
- Kick Ads, Generative Engine Optimization guide (2026-07), citing the Princeton/Allen AI/IIT Delhi GEO study
- SEMalytics and Shadow GEO checklists (2026-06), AutomateLab checklist (2026-05; cites SERanking llms.txt study)
- Search Engine Land, rise and fall of FAQ schema; metricfixer and Assertive Media on the May 2026 FAQ rich result removal
- Patrick Stox, Jekyll/GitHub Pages SEO; GitHub Docs on custom domains; Filip Mikina on indexing GitHub Pages
- Copy Template Shop and Macrowebber on concise, proof-first landing pages
Several GEO sources are vendor blogs with their own incentives. Treat percentage claims as directional.
