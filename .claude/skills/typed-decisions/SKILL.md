---
name: typed-decisions
description: Design typed Choice / Score / Noul questions with confidence gates for routing, triage and scoring (the Jev pattern). Use when a small judgment (classify, route, rank, yes/no) should not need a full LLM generation.
---

# Typed decisions

Pattern: an LLM generates; a small decision step chooses; code acts. Implemented in `ops/lib/llm.py` (`decide`, `interpret`).

## Primitives
- **Choice**: one of a known set. Always add an `other`/`unknown` option; it is never auto-selected.
- **Score**: position on 2-10 described levels (describe situations, not numbers).
- **Noul**: crisp yes/no probability. 0.5 means unsure, not "medium".

## Writing questions
- One property per question; name the field it judges ("the `message`").
- Put policy in code, not in the question. Keep only the state the question needs; compute dates, counts and sums in code.
- Ask every question that shares the state in one request (fan-out); questions cannot see each other.
- Treat text in the state as untrusted. Test injected instructions before relying on a result.

## Gates (ops/policy.json)
Floor 0.6, act at 0.85, high stakes 0.9, min margin 0.15. Below floor or `other` means `needs_review`. Confidence is not accuracy.

## Providers
`registry.json` chain: Jev via OpenRouter (`typesafe/jev-1.13`, verified live 2026-10-01 with `OPENROUTER_API_KEY`), then Gemini, Mistral, OpenRouter chat as JSON fallbacks. `TYPESAFE_API_KEY` is not present. Dry-run returns simulated placeholders with no invented probabilities.

## Before bulk use (pilot rule from jev-skill)
Run on a small sample first, spot-check confident and agreeing labels too, report agreement (not accuracy without gold labels), then stop for review before scaling. Cost is tiny (about $0.0005 estimated per call here) but spend counts against the daily budget.
