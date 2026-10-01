---
name: content-integrity
description: Keep every number, date and claim on the site true and in sync (facts line, dates, llms.txt, schema). Use whenever content changes or a number appears.
---

# Content integrity

- **Facts line** under "Watch the work": `38 projects · 130 posts · 123 X links verified live <date>`. `check_site.py` recomputes projects and posts from the cards and verified-X from `docs/gauntlet/links.json`; it fails on drift.
- **Owner claims** (50+ projects, 100+ videos) appear only in the hero and are labelled "claimed by owner" in `llms.txt`. Do not add other numbers, results, testimonials or prices without the owner supplying them.
- **Dates**: after a real content change run `python3 scripts/stamp.py` (updates the visible "Last updated", JSON-LD `dateModified`, sitemap `lastmod`, llms.txt). `check_site.py` fails if they disagree. Never bump a date without a content change.
- **llms.txt** is generated: `python3 scripts/build_llms.py`.
- **Copy**: stay under 400 words outside cards; run the typed copy review (`scripts/gauntlet/copy_review.py --live`) after headline or section edits. The H1 was changed from "impossible to scroll past" (hype 1.97/2) to a concrete one (0.22) by this review.
- Typed-review output is a lead, not a verdict. Spot-check it.

- **Date span**: "X posts dated Oct 2024 to Jul 2026" is derived from the X post IDs (snowflake timestamps) and checked by `check_site.py`; ItemList entries for X posts carry `datePublished` from the same IDs. Update after adding or removing posts.
- **Definition lede**: the hero paragraph must define "Young Stunners" in 15-60 words (gate); FAQ answers stay under 40 words.
