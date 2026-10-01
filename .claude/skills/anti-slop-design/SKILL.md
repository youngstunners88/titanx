---
name: anti-slop-design
description: The Young Stunners visual system (paper, ink, red, sticker shadows) and the automated "AI slop" tells the build rejects. Use before restyling anything or adding sections, cards, icons or copy.
---

# Anti-slop design

The site must look like Young Stunners (logo: black pictograms, white letters, red outline, street sticker), not a generic AI landing page.

## System (index.html `:root`)
- **Palette**: paper `#f6f2e8`, ink `#111`, red `#e10600` (small red text uses `#c20500` for contrast), one accent only.
- **Type**: Montserrat only (variable, self-hosted). Headings 900, h2 uppercase. One family, no pairing.
- **Shape**: 2.5px ink borders, hard offset shadows (`5px 5px 0 ink`), buttons press down on click. No blur, glow or glass.
- **Layout**: left-aligned and asymmetric (heading left, content right); a black band for the videos; a red band for contact. The real logo is the hero art on a white sticker card (hidden on phones).
- **Texture**: a faint halftone dot pattern on the hero only.
- **Content**: real avatars, real counts, real post dates. No stock imagery, icon tiles or emoji.

## Rejected automatically (`scripts/check_site.py`)
emoji or em dashes in visible text | gradient text | backdrop blur | soft glow shadows | icon tiles above headings | purple palette | more than one webfont | filler words (revolutionary, seamless, unlock, elevate, supercharge, game-changing, leverage, empower, journey, landscape, delve, robust, world-class...) | scroll-reveal that hides content until JS runs (removed).

## Rules
- Add a section by copying an existing pattern (`.split` for heading-left layouts). Do not add cards-in-cards, 3-up icon grids, or centered-everything.
- Videos stay first: playable tiles must sit in the first 75% of the viewport on phone and desktop (gate).
- Prefer proof (a number, a date, a live link) over adjectives.
- Check dark and light backgrounds: the logo's white letters need a light surface or a white plate.
