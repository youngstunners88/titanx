#!/usr/bin/env python3
"""Ops entry point.  python3 ops/run.py <command>
  route "<text>" [--live]       choose skill + workflow
  workflow <id> [--live] [--input TEXT]
  triage "<message>" [--live]   typed triage of an inbound DM/brief, queues result
  queue | status | recover
Dry-run is the default. --live uses provider keys from the environment (names only)."""
import argparse, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ops.lib import llm, state
from ops.router.route import route

ROOT = Path(__file__).resolve().parent
POLICY = llm.POLICY


def gate(action):
    """Approval-required actions are never executed by the runner."""
    return {"action": action, "allowed": False, "reason": "needs explicit owner approval (ops/policy.json approval_required)"} if action in POLICY["approval_required"] else {"action": action, "allowed": True}


def run_shell(cmd):
    if list(cmd) not in [list(c) for c in POLICY["shell_allowlist"]]:
        return {"ok": False, "error": "command not in policy shell_allowlist"}
    p = subprocess.run(cmd, cwd=ROOT.parent, capture_output=True, text=True)
    return {"ok": p.returncode == 0, "code": p.returncode, "tail": p.stdout.strip().splitlines()[-3:]}


def route_lead(ctx):
    d = ctx["classify"]["decisions"]
    scam = d.get("scam_risk", {}); kind = d.get("kind", {})
    if ctx["classify"]["simulated"] or scam.get("status") != "selected" or kind.get("status") != "selected":
        dest = "review"
    elif scam.get("value") or kind.get("value") == "spam_scam":
        dest = "review"
    else:
        dest = "inbox"
    return {"destination": dest, "kind": kind.get("value"), "reason": "dry-run, scam risk, or low confidence goes to human review; nothing is auto-replied"}


def run_workflow(wid, live=False, text=None):
    wf = json.loads((ROOT / "workflows" / f"{wid}.json").read_text())
    state.append_event("run_start", workflow=wid, live=live)
    ctx, trace = {"input": text}, []
    for s in wf["steps"]:
        t = s["type"]
        if t == "shell": r = run_shell(s["cmd"])
        elif t == "decide":
            r = llm.decide({"message": text or "", "site": text or ""}, s["questions"], live=live)
        elif t == "route_lead": r = route_lead(ctx)
        elif t == "gate": r = gate(s["action"])
        elif t in ("note", "manual"): r = {"text": s["text"]}
        else: r = {"error": f"unknown step type {t}"}
        ctx[s["id"]] = r; trace.append({"step": s["id"], "type": t, "result": r})
    state.append_event("run_end", workflow=wid)
    state.snapshot()
    return {"workflow": wid, "live": live, "trace": trace, "ctx": ctx}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("route"); r.add_argument("text"); r.add_argument("--live", action="store_true")
    w = sub.add_parser("workflow"); w.add_argument("id"); w.add_argument("--live", action="store_true"); w.add_argument("--input")
    t = sub.add_parser("triage"); t.add_argument("text"); t.add_argument("--live", action="store_true")
    sub.add_parser("queue"); sub.add_parser("status"); sub.add_parser("recover")
    a = ap.parse_args(argv)
    if a.cmd == "route": out = route(a.text, a.live)
    elif a.cmd == "workflow": out = run_workflow(a.id, a.live, a.input)
    elif a.cmd == "triage":
        res = run_workflow("lead-triage", a.live, a.text)
        dest = res["ctx"]["route"]["destination"]
        jid, new = state.enqueue({"message": a.text}, kind="lead")
        if new:
            if dest == "review":
                state.claim(); state.finish(jid, "review", res["ctx"]["route"])
        out = {"id": jid, "new": new, "destination": dest, "decision": res["ctx"]["route"]}
    elif a.cmd == "queue": out = state.listing()
    elif a.cmd == "status": out = {"snapshot": state.snapshot(), "budget": state.budget_read(), "providers": {p: llm.key_present(p) for p in llm.REGISTRY["env_names"]}}
    else: out = {"recovered": state.recover()}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
