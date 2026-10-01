---
name: featured-player
description: How the click-to-play featured video row works and how to change the featured posts. Use when the owner wants different videos highlighted or the player misbehaves.
---

# Featured player

Six `button.feat` tiles in `index.html` (`data-tweet`, `data-name`). Clicking one loads X's `widgets.js` (only then), embeds that post with `dnt:true`, dark theme, no conversation. If the widget fails or takes 9 s, the player shows a "Watch on X" link. Rapid clicks are guarded by a sequence token so the latest click always wins.

## Change the featured set
1. Pick posts that are verified live (`docs/gauntlet/links.json`, status ok). Use the numeric status ID.
2. Edit the six tiles: ID, name, and an avatar from `brand/projects/<slug>.webp`.
3. Run the gauntlet. The interaction test checks the player ends in an embed or the fallback, never a stuck "Loading".

## Notes
- No third-party request happens until a visitor presses play (gauntlet gate).
- The sandbox cannot render X embeds (network), so the test accepts the fallback; verify the real embed on the live site.
- Featured posts are third-party content: keep the footer disclaimer ("Posts promote client projects. Nothing here is financial advice.").

## Game demo
`#latest` ("My latest project", Lil Blunt: The Smoke Realm) reuses the same click-to-play loader (`playTweet`) via `button[data-demo]`. Demo post: https://x.com/smokering25/status/2105394557865374145 (verified via oEmbed 2026-10-01). Game: https://www.smokegame.win/ ; code: https://github.com/youngstunners88/GM-GAME. Logo: `brand/lil-blunt-logo.webp` (circle crop with green outline, from the owner's art; regenerate with the crop in git history if the art changes).
