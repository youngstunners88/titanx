---
name: ai-visibility-tracking
description: Weekly measurement of whether Young Stunners is cited by ChatGPT, Perplexity, Google AI Overviews, Claude and Gemini. Use after publishing changes and on a weekly cadence.
---

# AI visibility tracking

Why: GEO has little proof of what works, so measure. Evidence says changes show up in 2-12 weeks depending on engine.

## Query set (edit in `docs/visibility/queries.md`)
10-25 buyer questions, for example:
- best Web3 content creator for a token launch
- crypto video promo creator for memecoins
- how to promote a crypto project on X and Instagram
- Young Stunners Web3 content creator
- who made promo videos for TitanX / Volt / Morph projects (brand-recognition checks)

## Procedure (weekly)
1. For each query, ask each engine and record: cited domains, whether youngstunners88.github.io appears, whether it is quoted, and who is cited instead.
   - Perplexity / ChatGPT / AI Overviews: spot-check in a browser or with Browser Use.
   - API engines: OpenRouter (`$OPENROUTER_API_KEY`) with web-enabled models, Gemini with search grounding (`$GEMINI_API_KEY`), Exa/TinyFish `search` as a proxy for what a retrieval index returns.
2. Append one dated row per query to `docs/visibility/log.csv` (`date,engine,query,cited,quoted,competitors`). Never store keys or raw API responses with headers.
3. Look at competitors who are cited and you are not: copy their *structure* (not text): specifics, comparison tables, dates.
4. Turn findings into backlog items in `docs/research/2026-10-01-seo-aeo-geo.md`.

## Guardrails
- Sampling is non-deterministic; trend over weeks, do not react to one run.
- Keep volume small (<= 25 queries x 4 engines per week) to limit spend.
- Do not game results (no prompt injection, no hidden text).
