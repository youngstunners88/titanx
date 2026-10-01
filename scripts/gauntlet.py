#!/usr/bin/env python3
"""The gauntlet: every gate the site must pass before it ships.

  python3 scripts/gauntlet.py            fast: static + ops tests + lab + interaction
  python3 scripts/gauntlet.py --full     adds link health (network) and copy review (small live spend)
  GAUNTLET_URL=https://... python3 scripts/gauntlet.py   test a deployed URL instead of local files

Writes docs/gauntlet/latest.md and latest.json. Exit 1 if any gate fails."""
import json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "gauntlet"; OUT.mkdir(parents=True, exist_ok=True)
FULL = "--full" in sys.argv
gates = []   # (stage, name, pass, detail)


def gate(stage, name, ok, detail=""):
    gates.append((stage, name, bool(ok), " ".join(str(detail).split())))


def run(cmd, timeout=600, env=None):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout, env={**os.environ, **(env or {})})


# 1. static
r = run([sys.executable, "scripts/check_site.py"])
tail = (r.stdout.strip().splitlines() or [""])[-1]
gate("static", "check_site.py (SEO, schema, facts, dates, budgets, secrets)", r.returncode == 0, tail if r.returncode == 0 else r.stdout[-300:])
# 2. ops tests
r = run([sys.executable, "ops/tests/test_ops.py"])
gate("ops", "ops offline tests", r.returncode == 0, (r.stderr.strip().splitlines() or [""])[-1])
# 3. lab
lab = None
try:
    r = run(["node", "scripts/gauntlet/lab.mjs"], timeout=300)
    lab = json.loads(r.stdout)
except Exception as e:
    gate("lab", "lab harness ran", False, f"{type(e).__name__}: {str(e)[:120]} (needs node + playwright + axe-core)")
if lab:
    for vp, v in lab.items():
        s = f"lab:{vp}"
        gate(s, "LCP <= 2500 ms (local lab)", v["lcpMs"] <= 2500, f"{v['lcpMs']} ms")
        gate(s, "CLS <= 0.1", v["cls"] <= 0.1, v["cls"])
        gate(s, "transfer <= 600 KB", v["transferKB"] <= 600, f"{v['transferKB']} KB, {v['requests']} requests")
        gate(s, "no third-party hosts on load", set(v["hostsKB"]) <= {v["ownHost"]}, [h for h in v["hostsKB"] if h != v["ownHost"]][:4] or "own host only")
        gate(s, "no console errors / failed requests", not v["consoleErrors"] and not v["failedRequests"], (v["consoleErrors"] + v["failedRequests"])[:2])
        gate(s, "no horizontal overflow", not v["overflowX"], v["scrollWidth"])
        gate(s, "no clipped buttons/chips", v["clippedControls"] == 0, v["clippedControls"])
        gate(s, "no broken images", v["brokenImages"] == 0, v["brokenImages"])
        gate(s, "tap targets >= 44px", v["smallTargets"] == 0, v["smallTargetSamples"][:2])
        gate(s, "axe-core: 0 violations", not (v["axe"] or []) if v["axe"] is not None else False, [(a["id"], a["impact"]) for a in (v["axe"] or [])])
        if vp != "tiny":   # 320px phones are an overflow/clipping check only
            gate(s, "first video tile above the fold (<= 75% of viewport)", v["firstVideoTileTop"] is not None and v["firstVideoTileTop"] <= 0.75 * v["viewport"], f"{v['firstVideoTileTop']}px of {v['viewport']}px")
# 4. interaction
try:
    r = run(["node", "scripts/gauntlet/interact.mjs"], timeout=300)
    for t in json.loads(r.stdout)["tests"]:
        gate("interact", t["name"], t["pass"], t["detail"] if not t["pass"] else "")
except Exception as e:
    gate("interact", "interaction harness ran", False, str(e)[:120])
# 5/6. full (stale outputs are deleted first; a failed or missing run fails the gate)
def fresh_json(script, out_name, args=(), timeout=900):
    f = OUT / out_name
    f.unlink(missing_ok=True)
    try:
        r = run([sys.executable, script, *args], timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timed out"
    if r.returncode != 0 or not f.exists():
        return None, (r.stderr.strip().splitlines() or ["failed"])[-1][:120]
    try:
        return json.loads(f.read_text()), ""
    except Exception as e:
        return None, f"unreadable output: {e}"[:120]


if FULL:
    links, err = fresh_json("scripts/gauntlet/linkcheck.py", "links.json")
    if links is None:
        gate("links", "link check ran", False, err)
    else:
        bad = [l for l in links if l["status"] not in ("ok", "unverified")]
        gate("links", "every X post link resolves (oEmbed)", not bad, f"{len(links) - len(bad)} ok/unverified, {len(bad)} bad")
    cr, err = fresh_json("scripts/gauntlet/copy_review.py", "copy-review.json", ["--live"])
    if cr is None:
        gate("copy", "copy review ran (live)", False, err)
    else:
        inconclusive = [c for c in cr if c.get("hype") is None]
        hype = [c for c in cr if "hype" in c["flags"]]
        gate("copy", "every block has a hype decision", not inconclusive, f"{len(inconclusive)} inconclusive")
        gate("copy", "no hype-flagged copy (typed review, live)", not hype, "; ".join(h["text"][:50] for h in hype[:2]))

passed = sum(1 for g in gates if g[2]); total = len(gates)
stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
md = [f"# Gauntlet scorecard", "", f"Run: {stamp} | mode: {'full' if FULL else 'fast'} | target: {os.environ.get('GAUNTLET_URL', 'local files')}", "", f"**{passed}/{total} gates passed**", "", "| Stage | Gate | Result | Detail |", "|---|---|---|---|"]
for st, n, ok, d in gates:
    md.append(f"| {st} | {n} | {'PASS' if ok else '**FAIL**'} | {d[:90].replace('|', '/')} |")
(OUT / "latest.md").write_text("\n".join(md) + "\n")
(OUT / "latest.json").write_text(json.dumps({"run": stamp, "full": FULL, "passed": passed, "total": total, "gates": [{"stage": a, "name": b, "pass": c, "detail": d} for a, b, c, d in gates]}, indent=1))
for st, n, ok, d in gates:
    if not ok: print("FAIL", st, "|", n, "|", d)
print(f"gauntlet: {passed}/{total} gates passed")
sys.exit(0 if passed == total else 1)
