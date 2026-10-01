# Repo and document landscape: what we use, adapt or skip

Reviewed 2026-10-01 from the owner's Google Docs (Jev repos, SEO, Jev Engineering, Backlink CLI, SEO transcripts, Repo land, Jevgrep). READMEs were read; code was run only where noted. Cloned repos live outside this repo under `/home/user/<owner>/<repo>` and are not committed.

## Verdicts

**Adopted (in use now)**
- **Jev via OpenRouter** (`typesafe/jev-1.13`): verified live with `OPENROUTER_API_KEY` for lead triage (legit lead to inbox, scam to review). No TypeSafe key is needed. Wired into `ops/lib/llm.py`.
- **wuyoscar/jev-skill** (jev-triage, jev-eval, jev-documents): borrowed the pilot-first rule, honest simulation labelling, and the review-by-default exit codes. Became `lead-triage`, `typed-decisions`.
- **dbreunig/building-with-jev-skill**: question-design rules became `typed-decisions`.
- **smartdio/jev-browser-agent**, **browser-use/jev-ultrafast**: safety and loop patterns became `safe-browsing`.
- **Jev Engineering doc**: "LLM generates, Jev decides, code executes", queue folders, confidence 0.85, per-task cost tracking, independent completion check. Became the `ops/` design.
- **Podcast transcript (Ahrefs x Dan Petrovic)**: became `aeo-citation-mining`.
- **Backlink CLI doc**: became `backlink-prospecting`, minus tools we do not have and with approval gates.
- **obra/superpowers**: kept only the change protocol (plan, small steps, tests, review). Not installed.
- **anthropics/skills (skill-creator, frontend-design)**: skill-creator is already available in this session; its rules shaped the short, single-job skills here.
- **volcengine/OpenViking** and **muratcankoylan/agent-skills-for-context-engineering**: kept the ideas only (summary-first directories, progressive disclosure, state in files). Became "Context rules" in `ops-architecture`.
- **199-biotechnologies/claude-deep-research-skill**: kept the pipeline (scope, plan, retrieve, triangulate, critique, package; check today's date first; persist sources). Added to `web3-market-research`.
- **pbakaus/impeccable** and **nextlevelbuilder/ui-ux-pro-max-skill**: kept the "AI tells" checklist and the PRODUCT.md idea (now `PRODUCT.md`). Their CLIs were not run.

**Later or optional (needs owner approval, a key, or both)**
- **mendableai/firecrawl**: good for crawling competitors, but our `FIRECRAWL_API_KEY` returned 401. Fix the key first; Exa and TinyFish cover the gap.
- **vercel-labs/agent-browser**: fast browser CLI; optional install (third-party). Headless Chromium and Browser Use already work.
- **jkudish/jev-browser**: needs `TYPESAFE_API_KEY` (not present).
- **kapso.ai**: WhatsApp API, a possible future lead channel. Costs and policy need owner sign-off.
- **jlowin/fastmcp**: only if we later expose `ops/` as an MCP server.
- **stanfordnlp/dspy**: prompt optimisation; revisit if we build a metric-driven on-page test loop.
- **cobanov/awesome-jev**: catalog. Candidates: slop-grader (copy audit), hunch/jeff (weighted ranking of prospects), jev-scout (judge search results), jev-social (Instagram/TikTok research, approval needed).

**Skipped (not useful here)**
- Portkey gateway, OmniRoute: a self-hosted gateway is overkill; `registry.json` already gives provider fallback. OmniRoute's free-tier stacking raises terms-of-service risk.
- tavily-mcp (Exa + TinyFish already), n8n and huginn (we schedule with routines), camel-ai/owl, SocratiCode (our repo is one HTML file), unsloth, turboquant_plus, NOMAD, Crucix, agent-reach, unbrowse-openclaw, freebuff, MiroFish post, starknet.io (no client data to justify), jevgrep (code search; single-file repo), typesafe-jev-bridge (needs TypeSafe key; OpenRouter path covers it).
- **Oros42/IMSI-catcher**: cellular-interception tooling with no relation to this project; not used.
- **joedhawan/Helios**: repository not found (404).

## The SEO doc (Kimi)
It was written for a different property (Lil Blunt, smokegame.win): VideoGame schema, itch.io, leaderboard virality. The transferable parts are already in our playbook (JSON-LD, AI-readable about text, meta/OG, sitemap, robots, analytics, 30-day plan). If that game site becomes a project, create a separate repo and reuse `ops/` and the skills.

## Unverified claims from the sources (do not act on without checking)
- Reddit/G2 citations falling to zero in ChatGPT, help-center citations up 32% (a post by a vendor's co-founder).
- Google "OKF" protocol, "preferred sources badge" as a ranking signal (it is a Google news feature; no evidence it applies here).
- Jev pricing ($0.042 per million input tokens) and benchmark figures come from a promotional article. Our measured cost is the OpenRouter bill; we count about $0.0005 per call as an estimate only.
