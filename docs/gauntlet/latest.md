# Gauntlet scorecard

Run: 2026-10-01 16:11 UTC | mode: full | target: local files

**58/59 gates passed**

| Stage | Gate | Result | Detail |
|---|---|---|---|
| static | check_site.py (SEO, schema, facts, dates, budgets, secrets) | PASS | OK |
| ops | ops offline tests | PASS | OK |
| lab:mobile | LCP <= 2500 ms (local lab) | PASS | 248 ms |
| lab:mobile | CLS <= 0.1 | PASS | 0 |
| lab:mobile | transfer <= 600 KB | PASS | 348 KB, 43 requests |
| lab:mobile | no third-party hosts on load | PASS | own host only |
| lab:mobile | no console errors / failed requests | PASS | [] |
| lab:mobile | no horizontal overflow | PASS | 390 |
| lab:mobile | no clipped buttons/chips | PASS | 0 |
| lab:mobile | no broken images | PASS | 0 |
| lab:mobile | tap targets >= 44px | PASS | [] |
| lab:mobile | axe-core: 0 violations | PASS | [] |
| lab:mobile | first video tile above the fold (<= 75% of viewport) | PASS | 541px of 844px |
| lab:tiny | LCP <= 2500 ms (local lab) | PASS | 92 ms |
| lab:tiny | CLS <= 0.1 | PASS | 0 |
| lab:tiny | transfer <= 600 KB | PASS | 348 KB, 43 requests |
| lab:tiny | no third-party hosts on load | PASS | own host only |
| lab:tiny | no console errors / failed requests | PASS | [] |
| lab:tiny | no horizontal overflow | PASS | 320 |
| lab:tiny | no clipped buttons/chips | PASS | 0 |
| lab:tiny | no broken images | PASS | 0 |
| lab:tiny | tap targets >= 44px | PASS | [] |
| lab:tiny | axe-core: 0 violations | PASS | [] |
| lab:desktop | LCP <= 2500 ms (local lab) | PASS | 116 ms |
| lab:desktop | CLS <= 0.1 | PASS | 0.0076 |
| lab:desktop | transfer <= 600 KB | PASS | 348 KB, 43 requests |
| lab:desktop | no third-party hosts on load | PASS | own host only |
| lab:desktop | no console errors / failed requests | PASS | [] |
| lab:desktop | no horizontal overflow | PASS | 1280 |
| lab:desktop | no clipped buttons/chips | PASS | 0 |
| lab:desktop | no broken images | PASS | 0 |
| lab:desktop | tap targets >= 44px | PASS | [] |
| lab:desktop | axe-core: 0 violations | PASS | [] |
| lab:desktop | first video tile above the fold (<= 75% of viewport) | PASS | 594px of 800px |
| interact | filter: instagram shows only IG cards | PASS |  |
| interact | filter: aria-pressed updates | PASS |  |
| interact | filter: live count text | PASS |  |
| interact | search: "volt" narrows results | PASS |  |
| interact | search: empty state visible | PASS |  |
| interact | search: input is not injected as HTML | PASS |  |
| interact | card: "show all" expands links | PASS |  |
| interact | keyboard: first focus is skip link | PASS |  |
| interact | player: embed or graceful fallback (never stuck) | PASS |  |
| interact | demo: embed or graceful fallback (never stuck) | PASS |  |
| interact | demo: game link points to smokegame.win and nothing else is exposed | PASS |  |
| interact | privacy: unreleased game repo is not linked anywhere | PASS |  |
| interact | brief: copies a filled brief to clipboard | PASS |  |
| interact | brief: opens x.com/youngstunnersss synchronously in the tap (Safari-safe) | PASS |  |
| interact | brief: shows success toast | PASS |  |
| interact | faq: details open | PASS |  |
| interact | sticky CTA hidden at top | PASS |  |
| interact | sticky CTA shows after hero | PASS |  |
| interact | sticky CTA hides at contact form | PASS |  |
| interact | mobile: no horizontal overflow | PASS |  |
| interact | privacy: no analytics requests without a configured key | PASS |  |
| interact | privacy: no third-party requests on load | PASS |  |
| links | every X post link resolves (oEmbed) | PASS | 130 ok/unverified, 0 bad |
| copy | every block has a hype decision | **FAIL** | 29 inconclusive |
| copy | no hype-flagged copy (typed review, live) | PASS |  |
