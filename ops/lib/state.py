"""State management. One place owns persistence: events, snapshot, budget, job queue.

Rules: append-only event log (truth), atomic writes, idempotent enqueue, resumable
claims. Nothing here talks to the network or an LLM."""
import hashlib, json, os, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
QUEUE = ROOT / "queue"
STAGES = ("inbox", "working", "done", "review")


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def atomic_write(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False))
    os.replace(tmp, path)


def append_event(event, **data):
    STATE.mkdir(parents=True, exist_ok=True)
    rec = {"t": _now(), "kind": event, **data}
    with open(STATE / "events.jsonl", "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def events():
    """Tolerates a truncated or corrupt line (crash mid-append) instead of failing forever."""
    p = STATE / "events.jsonl"
    if not p.exists():
        return []
    out = []
    for l in p.read_text().splitlines():
        try:
            if l.strip(): out.append(json.loads(l))
        except ValueError:
            continue
    return out


def snapshot():
    """Derived view. Rebuild from events; never edit by hand."""
    snap = {"runs": 0, "live_calls": 0, "last_run": None, "reviews": 0}
    for e in events():
        if e["kind"] == "run_start": snap["runs"] += 1; snap["last_run"] = e.get("workflow")
        if e["kind"] == "live_call": snap["live_calls"] += 1
        if e["kind"] == "job_review": snap["reviews"] += 1
    atomic_write(STATE / "snapshot.json", snap)
    return snap


# ---- budget (per UTC day) ----
def _budget_path():
    return STATE / "budget.json"


def budget_read():
    p = _budget_path()
    day = time.strftime("%Y-%m-%d", time.gmtime())
    b = json.loads(p.read_text()) if p.exists() else {}
    if b.get("day") != day:
        b = {"day": day, "calls": 0, "est_cost_usd": 0.0}
    return b


def budget_spend(calls=1, est_cost_usd=0.0):
    b = budget_read(); b["calls"] += calls; b["est_cost_usd"] = round(b["est_cost_usd"] + est_cost_usd, 6)
    atomic_write(_budget_path(), b); return b


# ---- queue ----
def job_id(payload):
    return hashlib.sha1(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def find_job(jid):
    for s in STAGES:
        p = QUEUE / s / f"{jid}.json"
        if p.exists():
            return s, p
    return None, None


def enqueue(payload, kind="job"):
    """Idempotent: the same payload never queues twice."""
    jid = job_id(payload)
    stage, _ = find_job(jid)
    if stage:
        return jid, False
    atomic_write(QUEUE / "inbox" / f"{jid}.json", {"id": jid, "kind": kind, "payload": payload, "created": _now()})
    append_event("job_enqueued", id=jid, job_kind=kind)
    return jid, True


def claim(jid=None):
    """Atomically move a job inbox -> working. With jid, only that job (never someone else's).
    Returns (id, job) or None."""
    paths = [QUEUE / "inbox" / f"{jid}.json"] if jid else sorted((QUEUE / "inbox").glob("*.json"))
    for p in paths:
        dst = QUEUE / "working" / p.name
        try:
            os.rename(p, dst)
        except FileNotFoundError:
            continue
        return p.stem, json.loads(dst.read_text())
    return None


def finish(jid, dest="done", result=None):
    assert dest in ("done", "review")
    src = QUEUE / "working" / f"{jid}.json"
    job = json.loads(src.read_text())
    job["result"] = result; job["finished"] = _now()
    atomic_write(QUEUE / dest / f"{jid}.json", job)
    src.unlink()
    append_event("job_" + ("review" if dest == "review" else "done"), id=jid)


def recover():
    """After an interruption: working/ jobs go back to inbox/ so nothing is lost or repeated blindly."""
    n = 0
    for p in (QUEUE / "working").glob("*.json"):
        os.rename(p, QUEUE / "inbox" / p.name); n += 1
    if n: append_event("recovered", jobs=n)
    return n


def listing():
    return {s: sorted(p.stem for p in (QUEUE / s).glob("*.json")) for s in STAGES}
