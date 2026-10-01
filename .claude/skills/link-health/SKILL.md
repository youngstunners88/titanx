---
name: link-health
description: Verify every portfolio post link still exists and handle dead ones. Use before releases, monthly, and whenever the facts line ("N X links verified live") is touched.
---

# Link health

`python3 scripts/gauntlet/linkcheck.py` checks each X link with X's oEmbed endpoint (200 = exists, 404 = deleted or protected). Instagram cannot be verified anonymously and is reported `unverified`. Results: `docs/gauntlet/links.json`.

## Gotchas
- oEmbed rejects URLs ending `/video/1`. The script strips `/video|photo/N` before checking. (26 "dead" links on the first run were this quirk, not deleted posts.)
- 429 means slow down; the script sleeps. Never conclude "gone" from one error: recheck the canonical URL.

## When a link is genuinely gone
1. Re-test the canonical URL once.
2. Remove only that link, fix the card's "N pieces of content" (run `build_llms.py`), and log it in `docs/gauntlet/removed-links.md` so the owner can restore it.
3. Update the facts line on the page (projects, posts, verified count) so `check_site.py` passes.
4. Never delete a whole project without the owner's say-so; flag it instead.
Last run: 2026-10-01, 123 X links ok, 7 Instagram unverified, 1 removed ($SHOGUN).
