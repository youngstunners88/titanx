---
name: frontier-site-push
description: Top-tier, whole-site optimization pass for the Young Stunners site. Use when the owner asks to take the site to the next level, run a deep improvement round, or make it "superb". Combines measurement, product judgment, SEO/AEO/GEO, accessibility, performance, and the gauntlet gates into one loop that ends in a reviewed draft PR.
---

# Frontier site push

A deep, high-judgment pass. Not a checklist: diagnose first, then change the few things that matter most, then prove it with the gates. Read `PRODUCT.md`, `anti-slop-design`, `concise-copy`, and `gauntlet-loop` before editing.

## Non-negotiables
- Never invent metrics, testimonials, client names, prices, or results. Numbers come from the facts line in `index.html` and must stay in sync (`content-integrity`).
- The game's GitHub repo (GM-GAME) is never linked or shown anywhere on the site or docs.
- No paid or third-party generation APIs for media or copy. Use the local tooling in the repo.
- Don't raise the self-imposed daily call cap in `ops/policy.json` to get a gate through.
- Spending money, buying a domain, DNS changes, or sending outreach need owner approval. Draft only.
- Commit and push only to `claude/jolly-fermi-klufze`; open a draft PR; don't merge without the owner.

## Loop
1. **Baseline.** Run `python3 scripts/gauntlet.py` (fast) and the full gate. Record every failure and warning before touching anything.
2. **Diagnose as a visitor, not a checker.** In 5 seconds: does a stranger know who this is, what they do, and what to click? Walk the mobile view, the first video, and the portfolio links. List the top 5 problems ranked by impact on a visitor deciding to book.
3. **Choose 3–5 changes, no more.** Each must name the problem, the evidence, and the expected effect. Reject anything decorative, anything that adds weight, and anything that reads as AI slop.
4. **Implement** in small commits. Keep copy short; keep the paper/ink/red system; keep the hero video first.
5. **Prove.** Re-run the gates. Check: LCP and transfer budget (`site-performance`), axe and tap targets (`site-accessibility`), links (`link-health`), facts/dates sync (`content-integrity`), llms.txt and schema (`seo-aeo-geo-playbook`).
6. **Re-measure and compare** against the baseline. If a gate regressed, fix the cause, don't loosen the gate.
7. **Report.** Before/after table of gate scores, what changed and why, what was deliberately not done, and owner decisions still needed (domain, analytics key, search console verification, real results).

## Done means
Gates green or failures explained with evidence; the top visitor problems from step 2 addressed or explicitly deferred; the PR is a draft with a plain-language summary and no model identifiers in commits or PR text.
