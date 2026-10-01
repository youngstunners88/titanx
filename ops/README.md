# ops: the farm

A small operations layer for the site. Skills hold knowledge; this folder holds machinery.

```
ops/
  policy.json        what is allowed: budgets, thresholds, approval gates, shell allowlist
  registry.json      capability -> provider chain (swap vendors here only)
  router/            rules.json + route.py     decide WHICH skill/workflow handles a request
  lib/
    llm.py           abstraction layer: decide() typed Choice/Score/Noul, generate(); dry-run default
    state.py         persistence: event log, snapshot, budget, idempotent job queue
  workflows/         declarative steps (shell | decide | manual | gate), no code
  queue/             inbox -> working -> done | review   (runtime, gitignored)
  state/             events.jsonl, snapshot.json, budget.json   (runtime, gitignored)
  tests/test_ops.py  offline tests
  run.py             CLI entry point
```

## Separation of concerns
| Concern | Lives in | Never in |
|---|---|---|
| Knowledge, how-to | `.claude/skills/*` | code |
| Permission and limits | `policy.json` | skills or scripts |
| Which tool/provider | `registry.json` | callers |
| Deciding what to do | `router/` | workflows |
| Talking to models | `lib/llm.py` | router, workflows |
| Persistence | `lib/state.py` | everything else |
| Steps of a job | `workflows/*.json` | `llm.py` |

LLMs generate. Typed decisions choose. Code executes. Humans approve anything in `policy.approval_required`.

## Use
```bash
python3 ops/run.py route "make the hero copy shorter"      # -> skill + workflow
python3 ops/run.py workflow page-audit                     # runs scripts/check_site.py
python3 ops/run.py triage "Need a launch video next week"  # dry-run, nothing sent
python3 ops/run.py triage "..." --live                     # typed decision via a provider key
python3 ops/run.py status | queue | recover
python3 ops/tests/test_ops.py
```
Dry-run is the default and never touches the network. `--live` reads provider keys from the environment by name, counts against the daily budget in `policy.json`, and scrubs key values from errors.

## Add something
- **Provider**: add to `registry.json` and `PROVIDERS` handling in `lib/llm.py`. Callers do not change.
- **Workflow**: drop a JSON file in `workflows/`; add a routing rule in `router/rules.json`.
- **Skill**: add `.claude/skills/<name>/SKILL.md` (one job, under ~80 lines, description says when to use it).
- Then run the tests and `python3 scripts/check_site.py`.

## Change protocol (from obra/superpowers, trimmed)
Clarify the goal, write a short plan, make the change in small steps, run tests and the audit, review the diff, then commit. Skip steps only for trivial edits.
