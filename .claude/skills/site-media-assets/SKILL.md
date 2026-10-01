---
name: site-media-assets
description: Create and optimize thumbnails, posters and share images for the Young Stunners site without slowing it down. Use when adding visuals to the portfolio or updating the OG image.
---

# Site media assets

Goal: show the work visually while keeping the page fast (LCP < 2.5s) and the copy short.

- **Share image**: `brand/og-image.png` (1200x630) is generated from an HTML template with headless Chromium. Re-render it after any brand/stat change.
- **Project thumbnails**: use real frames from the owner's posts only (owner provides files). Do not fabricate screenshots of posts or engagement numbers. Save as WebP, <= 60 KB, 640px wide, under `brand/thumbs/`, with descriptive `alt`.
- **Generated graphics** (backgrounds, icons, sticker-style art) are fine: Gemini (`$GEMINI_API_KEY`), MuAPI, Pixellab. They must not imitate a real person or a client's brand, and must be labelled as illustrations if they sit near proof.
- **Voiceover/previews**: ElevenLabs for a voiceover on a sample reel, only with owner approval and only for content the owner owns.
- **Performance**: `loading="lazy"` and `decoding="async"` on everything below the fold, explicit `width`/`height`, no autoplaying video, no layout shift. Compress with `cwebp`/`sharp` if available.
- Run `site-audit` afterwards.
