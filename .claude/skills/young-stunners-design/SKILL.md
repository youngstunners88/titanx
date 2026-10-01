---
name: young-stunners-design
description: Page structure and component rules for the Young Stunners site (index.html): sections, cards, featured player, adding portfolio entries. Use when editing layout or content structure. Visual style lives in anti-slop-design.
---

# Young Stunners page structure

Single-file static site: `index.html` (inline CSS/JS), assets in `brand/`. Visual system: see `anti-slop-design`. Durable facts: `PRODUCT.md`.

## Order (videos first)
nav -> hero (definition lede, 2 CTAs, logo sticker) -> black band "Watch the work" (facts line, playable featured tiles + player) -> filters + 38 project cards -> services (numbered list) -> how it works -> questions -> contact (red band, brief form) -> footer. Primary CTA wording: "Book a campaign", repeated in nav, hero, sticky bar (phones) and contact.

## Components
- **Project card**: `div.project-card[data-type="twitter|instagram"]` > `.project-header` (avatar img 48x48, `h3.project-name`, `.project-category`, `.project-badge`) + `.project-links` (one `a.project-link` per post, text "@handle · Video" or "Reel · View post") + `.project-count`. JS handles filter, search, collapse above 3 links. Keep the count correct (`build_llms.py` and `check_site.py` verify).
- **Add a card**: paste the card, run `scripts/build_assets.py` (localizes the avatar), `scripts/gauntlet/linkcheck.py`, `scripts/build_llms.py`, then update the facts line and JSON-LD via the gauntlet failures.
- **Featured player**: see `featured-player`.
- **New section**: copy `.split` (heading left, content right) with `aria-labelledby` and an `id` on the h2.

## Rules
- Mobile first; no horizontal scroll at 320px; targets >= 44px.
- Never invent metrics, quotes or prices. Keep copy under the word budget (`concise-copy`).
- Run `python3 scripts/gauntlet.py` before every commit.
