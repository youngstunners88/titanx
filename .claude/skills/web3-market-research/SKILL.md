---
name: web3-market-research
description: Research skill for Young Stunners. Use before changing site copy, services, or positioning to learn what crypto projects look for in a content creator/KOL, what competitors show, and which keywords to target.
---

# Web3 market research

Goal: attract more clients (crypto founders, marketing leads, community managers) to Young Stunners.

## Tools available in this environment (check names only; never print or commit key values)
Run `env | grep -iE 'key|token' | sed 's/=.*//'` to list what is configured. Useful for research:
- **Exa** MCP (`web_search_exa`, `web_fetch_exa`) – semantic search for competitor pages and case studies.
- **TinyFish** MCP (`search`, `fetch_content`, `run_web_automation`) and `TINYFISH_API_KEY` – search, page extraction, browser automation.
- `FIRECRAWL_API_KEY` – crawl/scrape competitor sites to markdown.
- `BROWSER_USE_API_KEY` – interactive browsing when a site needs JS.
- Searchata / Advanced GSC MCPs – keyword and Core Web Vitals data; `pagespeed_insights_run_audit` for performance.
- `POSTHOG_*` – analytics once the site is live (funnel: hero CTA -> brief form -> X DM).
- `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `MUAPI_API_KEY` – image/video/text generation for creative assets.
- `ELEVENLABS_API_KEY` – voiceover for sample videos.

## Workflow
1. **Competitors**: search "crypto KOL agency", "web3 content creator", "crypto UGC/clipping agency". Fetch 3-5 sites. Record: services list, proof (impressions, named clients), process steps, pricing style, CTA wording.
2. **Buyer intent**: what founders ask (cost, speed, verifiability, approval rights, escrow/payment safety).
3. **Gap analysis**: list what Young Stunners already has (38 verifiable portfolio entries, direct creator access) vs. what competitors show.
4. **Output**: a short brief in `docs/research/<date>-<topic>.md` with sources (URLs) and concrete site changes.

## Findings so far (Sep 2026)
Competitors (kolhq, LuvKaizen, Lever, Myosin) all show: a clear service list, named case studies with numbers, a 3-4 step process, and a low-friction call/brief CTA. Pricing is usually "custom" or "starting at". Lever leads with risk-reduction (approve before paying). Young Stunners' edge: direct access to the creator, verifiable live posts, meme-native style.

## Rules
- Never invent metrics, clients, testimonials or prices. Only use numbers the owner has confirmed (50+ projects, 100+ videos) or that can be derived from the portfolio.
- Cite sources for every competitor claim.
- Never write API key values into files, commits or PRs.
