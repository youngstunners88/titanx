---
name: analytics-setup
description: Turn on privacy-friendly analytics for the site (PostHog, cookieless) and read the funnel. Use only when the owner wants analytics and provides or approves the key.
---

# Analytics setup

Off by default. The page contains `<meta name="ys-posthog-key" content="">`. If the owner sets a **public** PostHog project key (starts with `phc_`, designed to be public) there, the page loads PostHog cookieless (`persistence:'memory'`, no autocapture, no session recording) and sends:

`cta_click`, `cta_sticky`, `portfolio_link_click` (project, href), `featured_play`, `featured_fallback`, `brief_submit` (need, chain).

## Rules
- Never put a personal or secret key in the page. `POSTHOG_PERSONAL_API_KEY` stays server-side (reading insights only).
- The owner decides whether to add a tracker; the gauntlet verifies that with no key there are zero analytics requests.
- Mention in the footer or a privacy line if enabled (cookieless events still count as tracking in some regions).
- Useful funnel: page view -> featured_play or portfolio_link_click -> cta_click -> brief_submit. Read it weekly with the AI-visibility log.
