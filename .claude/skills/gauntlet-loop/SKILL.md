---
name: gauntlet-loop
description: The measure-fix-remeasure loop that decides whether the Young Stunners site may ship. Use before any release, after any change to index.html or assets, and whenever asked to "make the site better".
---

# Gauntlet loop

`python3 scripts/gauntlet.py` (fast) or `--full` (adds link health + live copy review, small spend). Output: `docs/gauntlet/latest.md` and `latest.json`. Exit 1 on any failed gate. `GAUNTLET_URL=https://youngstunners88.github.io/titanx/` tests the deployed site.

## Gates (58 in full mode)
static (SEO, schema, facts, dates, budgets, secret scan) | ops tests | lab at 390, 320 and 1280px (LCP, CLS, transfer <= 600 KB, no third-party hosts, no console errors, overflow, clipping, broken images, 44px targets, axe-core 0 violations, first video tile above the fold) | 19 interaction tests | link health | typed copy review.

## The loop
1. Run the gauntlet. Read only the failing rows.
2. Pick the single weakest gate. Make the smallest change that fixes the cause (not the symptom).
3. Rerun. If another gate broke, revert that part and rethink.
4. When green: run `security-review` and `code-review` on the diff, fix valid findings, rerun.
5. Run `--full`, commit, open the PR, merge only with owner approval, then run against the live URL.
Stop when all gates pass and nothing new is found, or after 3 rounds with no progress (then report the blocker).

## Rules
- Never weaken a gate to pass. Add a gate when a bug escapes (the 320px check was added after review found a gap, and immediately caught a real overflow).
- A skipped stage is not a pass. Missing node/playwright/axe fails the gate.
- Findings that cost money or change accounts follow `ops/policy.json` approvals.
- Setup (once per session): `npm i axe-core --prefix /tmp/axe`; Playwright is installed globally; Pillow via `pip install --target /tmp/pylibs pillow` for asset builds.
