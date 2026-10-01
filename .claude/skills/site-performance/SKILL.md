---
name: site-performance
description: Performance budgets and the asset pipeline for the Young Stunners site (images, fonts, logo). Use when adding a portfolio card, changing images or fonts, or when a transfer/LCP gate fails.
---

# Site performance

Baseline on 2026-10-01: 4.9 MB across 3 image hosts and Google Fonts. Now ~310 KB, one origin, LCP ~0.15 s locally.

## Pipeline
- **Avatars**: put the card in `index.html` with any image URL, then `PYTHONPATH=/tmp/pylibs python3 scripts/build_assets.py`. It downloads, crops to a square, makes a 96px WebP into `brand/projects/<slug>.webp`, rewrites the `src`, and records the source in `SOURCES.json`. It refuses slug collisions.
- **Logo**: `brand/young-stunners-logo.png` is the master (transparent letter fill, so always on a white plate). The script derives `logo-nav.webp`, favicon, apple-touch and manifest icons.
- **Fonts**: `python3 scripts/build_fonts.py` self-hosts Inter and Montserrat (latin, variable woff2) and verifies the files are real woff2. The `@font-face` CSS is inline in `index.html`.

## Budgets (enforced)
transfer <= 600 KB | avatars <= 400 KB total | index.html <= 140 KB | zero third-party hosts on load | every `<img>` has width and height | project avatars lazy-loaded, featured tiles eager.

## Don'ts
No hotlinked images or CDN scripts. No autoplay video. No third-party JS until a visitor opts in (the X player loads on click).
