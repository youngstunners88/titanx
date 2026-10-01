---
name: backlink-prospecting
description: Find relevant link and partnership prospects for Young Stunners, screen them, verify existing links and draft (never send) outreach. Use for link building and directory submissions.
---

# Backlink prospecting

Adapted from the "Backlink CLI" doc (written for a different site, smokegame.win). Same rules, tools matched to what we actually have.

## Tools we have
Exa and TinyFish MCP (find and read pages), Searchata / Advanced GSC (link data once Search Console is verified), Browser Use (careful, see safe-browsing), OpenRouter/Gemini for drafting. Not available: Moz, Hunter.io, Screaming Frog, OpenOutreach keys. Firecrawl's key was rejected (401).

## Workflow (`ops/workflows/prospect-research.json`)
1. Find 20-50 targets: Web3 marketing directories, TitanX and Base/BSC community lists, KOL roundups, project ecosystem pages that list creators. Save to `docs/outreach/prospects.csv`: `domain,why_relevant,contact_route,pitch_angle,status`.
2. Screen with typed Noul questions (relevant? looks like a real publication, not a link farm?). Spot-check confident answers.
3. Draft one short, specific pitch per accepted prospect.
4. **Stop.** Sending is in `policy.approval_required`.

## Rules
- Never spend credits or send email/DMs without approval. No bulk unsolicited DMs.
- Verify a link exists on the donor page before calling it acquired.
- Relevance beats volume; link text and context matter more than count.
- Public routes only (site contact page, published email). No scraping of private data.
- Everything claimed about Young Stunners must be in `PRODUCT.md`.
