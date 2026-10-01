---
name: site-api-toolkit
description: Map of the API credentials available in this environment (names only) and how to use each one to improve the Young Stunners site. Use before reaching for any external service. Never print or commit key values.
---

# API toolkit for the site

## Hard rules
- **Never print, log, commit or paste a key value.** Reference variables by name only (`$OPENROUTER_API_KEY`). Pass them in headers via the shell env; do not `echo` them, and do not put them in files, PR text or screenshots.
- List what exists with names only: `env | cut -d= -f1 | grep -iE 'key|token|secret|api'`.
- `python3 scripts/check_site.py` scans tracked files for any env secret value and fails if found. Run it before every commit.
- **Do not enumerate or probe credentials beyond what a task needs.** A broad probe was blocked by the harness on 2026-10-01 (read-only probes of accounts/zones). Make the narrowest call that serves the task.
- **Ask the owner before anything that spends money or changes DNS/accounts** (domain purchase, paid generations at volume, publishing).
- Browser/server-side use only. This is a static site: never embed a secret in `index.html`. Public identifiers (PostHog project token for client-side capture) are the only exception, and only the public one.

## Credentials present (names) and what they are for
Status = result of one minimal read-only check on 2026-10-01 (HTTP code only). "Untested" means not checked; confirm before relying on it.

| Variable(s) | Service | Use for the site | Status |
|---|---|---|---|
| `CLOUDFLARE_API_KEY`, `CLOUDFLARE_API_KEY2`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_GLOBAL_API_KEY` | Cloudflare | DNS for a custom domain, CDN/cache, redirects, Web Analytics, Pages | tokens verify OK (200) |
| `NAMESILO_API_KEY` | NameSilo registrar | search/register a domain, set DNS | API call succeeded; domain list not inspected |
| `POSTHOG_PERSONAL_API_KEY`, `POSTHOG_PROJECT_ID`, `POSTHOG_TOKEN` | PostHog | funnel analytics: CTA click, brief submit, X DM open | project API OK (200) |
| `SENTRY_TOKEN`, `SENTRY_ORGANISATION_TOKEN` | Sentry | JS error monitoring | OK (200) |
| `OPENROUTER_API_KEY` | OpenRouter | many LLMs, and **Jev** (`typesafe/jev-1.13`) for typed decisions via `ops/` (verified live 2026-10-01) | OK (200) |
| `GEMINI_API_KEY` | Google Gemini | copy, image generation, query sampling | OK (200) |
| `MINSTRAL_API_KEY`, `MINSTRAL_API_KEY2` | Mistral | cheap LLM for drafts/sampling | key 1 OK (200) |
| `XAI_API` | xAI Grok | Grok sampling for X-native visibility | 403, likely no access; verify |
| `FIRECRAWL_API_KEY` | Firecrawl | competitor crawl to markdown | 401, key rejected; fix before use |
| `TINYFISH_API_KEY` | TinyFish | search, page fetch, browser automation (also an MCP) | MCP works |
| `BROWSER_USE_API_KEY` | Browser Use | scripted browsing, e.g. check X/IG posts still load | OK (200) |
| `V0DEV_API` | v0 | UI component drafts | OK (200) |
| `CRAWLCONSOLE_API` | CrawlConsole | SEO crawl/indexing checks | host reachable only; auth untested |
| `ELEVENLABS_API_KEY`, `ELEVENLABS_API`, `ELEVENLABS_api_KEY2` | ElevenLabs | voiceover for sample videos | first key 401; others untested |
| `MUAPI_API_KEY`, `CLIPY_API_KEY`, `PIXELLAB_SECRET`, `TRIPO_API` | media generation (image/video/clip/pixel/3D) | poster images, short previews, graphics | untested |
| `AGENT_MAIL_API_KEY` | AgentMail | an inbox for the brief form / replies | untested |
| `GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_API_KEY` | GitHub | pushes, PRs, Pages settings | OK |
| `AWS_*`, `POLYGRES_API_KEY`, `BUTLER_API_KEY`, `B_AI_API_KEY`, `TREQ_API_KEY`, `MONID_API_KEY`, `ITCH_API_KEY` | various | not needed for this site | untested, leave alone |

MCP servers also connected: Exa (search/fetch), TinyFish, Searchata (Search Console, Bing, PageSpeed, schema, content briefs), Advanced GSC (Core Web Vitals, SERP, keywords), Windsor.ai (analytics connectors), CoinGecko (token data, currently failing to connect).

## Playbooks (use the narrowest key that works)
- **Research / competitors**: Exa MCP `web_search_exa` + `web_fetch_exa`; TinyFish `search`/`fetch_content`. Save findings to `docs/research/`.
- **Indexing + ranking**: Searchata/Advanced GSC once Search Console is verified; PageSpeed via `pagespeed_insights_run_audit`.
- **Analytics**: add a PostHog snippet using the *public* project token only, capture three events (`cta_click`, `brief_submit`, `portfolio_link_click`). Never use the personal API key in the page.
- **Errors**: Sentry browser loader with the public DSN only.
- **Domain + CDN**: see `custom-domain-setup`.
- **Visibility sampling**: see `ai-visibility-tracking`.
- **Media**: see `site-media-assets`.
- **Brief form inbox**: AgentMail would need server-side code; a static page cannot hold the key. Keep the current copy-to-clipboard + X DM flow unless the owner approves a small proxy (for example a Cloudflare Worker holding the secret).

## ops layer
`ops/` wraps these keys behind `ops/lib/llm.py` (capability chains in `ops/registry.json`, limits in `ops/policy.json`). Prefer `python3 ops/run.py ... --live` over ad-hoc curl: it enforces the daily budget, scrubs key values from errors and defaults to dry-run. `TYPESAFE_API_KEY` is not set; Jev is reached through OpenRouter.
