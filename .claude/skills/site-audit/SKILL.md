---
name: site-audit
description: Run the automated audit and visual check for the Young Stunners site before committing or opening a PR. Use after any edit to index.html, llms.txt, robots.txt or sitemap.xml.
---

# Site audit

1. `python3 scripts/check_site.py` — fails on: missing title/description/canonical/OG/H1, bad JSON-LD, portfolio cards not matching the ItemList or llms.txt, missing assets, broken anchors, images without alt, copy over the 400-word budget, and any env secret value found in tracked files.
2. Screenshot at 1280 and 390 widths and look at them:
   `/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --no-sandbox --disable-gpu --hide-scrollbars --window-size=1280,900 --virtual-time-budget=5000 --screenshot=<scratchpad>/shot.png file:///home/user/titanx/index.html`
   Check that the first project links are visible without scrolling and nothing overflows horizontally.
3. After deploy: `curl -s https://youngstunners88.github.io/titanx/ | grep -c <new-string>` to confirm Pages rebuilt (takes 1-3 minutes). Tell the user to hard-refresh.
4. With keys available, also run PageSpeed (Searchata `pagespeed_insights_run_audit` or the public PageSpeed API) and Core Web Vitals (`check_core_web_vitals`). Target LCP < 2.5s, CLS < 0.1, INP < 200ms on mobile.

Never print env values. The audit prints variable names only.

## Superseded by the gauntlet
Use `python3 scripts/gauntlet.py [--full]` (see `gauntlet-loop`). It runs `check_site.py`, the ops tests, the lab at 390/320/1280px with axe-core, 19 interaction tests, link health and the typed copy review, and writes `docs/gauntlet/latest.md`.
