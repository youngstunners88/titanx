---
name: young-stunners-design
description: Design system and page-structure rules for the Young Stunners site (index.html). Use when editing layout, styling, sections, or adding portfolio entries.
---

# Young Stunners design system

Single-file static site: `index.html` (inline CSS/JS), assets in `brand/` and `logos/`.

## Brand
- Palette: near-black `#0a0a0c`, surface `#18181c`, brand red `#e10600`, white text. Tokens live in `:root`.
- Type: Montserrat 800/900 for headings (matches the logo), Inter for body.
- **Logo**: `brand/young-stunners-logo.png` has transparent letter fill, so it is unreadable on dark. Always place it on a white plate (`background:#fff` + radius + padding), as in `.nav-logo`, `.hero-logo`, footer.

## Page order (conversion-led)
Hero (outcome headline + 2 CTAs + stats) -> ticker -> Services -> Who it's for -> Process -> Portfolio (proof) -> FAQ -> Contact brief -> footer. Keep one primary CTA ("Book a Campaign") repeated in nav, hero and contact.

## Portfolio entries
Cards are plain HTML in `#projects-grid`: `.project-card[data-type="twitter|instagram"]` with `.project-header`, `.project-links` (one `a.project-link` per post) and `.project-count`. JS handles filter, search, ticker, avatar fallback and collapsing lists over 3 links, so just add the card markup.

## Rules
- Mobile first: no horizontal scroll at 390px; tap targets >= 44px.
- Respect `prefers-reduced-motion`; keep contrast AA; keep focus outlines.
- No fabricated stats, logos, testimonials or prices.
- Verify visually: `chromium --headless --screenshot` at 1280 and 390 widths before committing.
