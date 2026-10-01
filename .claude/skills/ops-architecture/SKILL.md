---
name: ops-architecture
description: How the ops/ folder is organised (routing, state, abstraction layer, queue) and how to extend it. Use when adding a workflow, provider, router rule or skill, or when deciding where code or knowledge belongs.
---

# ops architecture

Read `ops/README.md` first. Short version:

- **Route** a request with `python3 ops/run.py route "<text>"`: rules, then a typed LLM decision, then human review.
- **State** is owned by `ops/lib/state.py` only: append-only `events.jsonl`, derived `snapshot.json`, a daily budget, and an idempotent queue `inbox -> working -> done | review`. After an interruption run `recover`; check the last completed action before repeating anything (a confident answer does not prove a file was saved or a message sent).
- **Abstraction**: callers ask `llm.decide()` or `llm.generate()` for a capability. Vendors live in `registry.json`. Never import a vendor SDK or hardcode a URL in a workflow.
- **Policy** in `policy.json` is the only place limits and approval gates are defined.

## Context rules (progressive disclosure)
- Keep each SKILL.md short; put long reference in `docs/` and link it.
- One directory = one concern, each with a README summary so an agent can read the summary before the files.
- Externalise state to files (queue, events, `docs/visibility/log.csv`), not to chat memory.
- Deep research follows scope, plan, retrieve in parallel, triangulate, critique, package. Save sources to the research doc.

## Rules
- Dry-run by default; `--live` only for the narrow call that needs it.
- Anything in `policy.approval_required` is never executed by the runner; ask the owner.
- Never print or commit key values; `scripts/check_site.py` scans for leaks.
- New behaviour needs a test in `ops/tests/test_ops.py`.
