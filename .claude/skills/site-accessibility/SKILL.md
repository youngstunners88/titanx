---
name: site-accessibility
description: Accessibility rules and patterns used on the Young Stunners site, enforced by axe-core and tap-target gates. Use when changing markup, controls, colours or motion.
---

# Site accessibility

Gate: axe-core must report 0 violations at 390, 320 and 1280px; every button, tab, nav link, input and project link is >= 44px; no clipped controls; no horizontal overflow.

## Patterns in use
- Skip link to `#main`; one `<h1>`; landmarks `nav`, `main`, `footer`; the mobile sticky CTA is `role="region"` and `visibility:hidden` while hidden (not focusable off-screen).
- Filter chips are a labelled group of `button[aria-pressed]` (not an incomplete tablist). A polite live region announces "Showing N of 38 projects".
- Text links inside paragraphs are underlined (never colour-only).
- Focus is always visible; `prefers-reduced-motion` disables animation and smooth scroll.
- The featured player is a labelled `role="region"` with `aria-live="polite"`; its fallback is a real link.
- Images have alt text (avatars: "<Project> logo"; decorative tile icons use `alt=""`).

## Test notes
Headless smooth-scroll makes instant checks flaky: use `scrollIntoView({behavior:'instant'})` in tests. Lazy images must be forced eager before judging "broken".
