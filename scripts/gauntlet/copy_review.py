#!/usr/bin/env python3
"""Typed-decision review of every visible text block. Live (small cost, counts against ops budget).
  python3 scripts/gauntlet/copy_review.py [--live]     (dry-run lists blocks only)
Writes docs/gauntlet/copy-review.json. Findings are leads for a human/agent, not verdicts."""
import html, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from ops.lib import llm

src = (ROOT / "index.html").read_text()
body = re.sub(r'<div class="projects-grid".*?</div>\s*<p class="empty"', '<p class="empty"', src, flags=re.S)
body = re.sub(r"<script.*?</script>|<style.*?</style>|<head>.*?</head>|<nav.*?</nav>", "", body, flags=re.S)
blocks = []
for sec in re.finditer(r'<(?:header|section|footer)[^>]*?(?:id="([a-z]+)")?[^>]*>(.*?)</(?:header|section|footer)>', body, re.S):
    name = sec.group(1) or "footer/hero"
    for t in re.findall(r"<(?:h1|h2|h3|p|summary)[^>]*>(.*?)</(?:h1|h2|h3|p|summary)>", sec.group(2), re.S):
        txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))).strip()
        if len(txt.split()) >= 4: blocks.append({"section": name, "text": txt})
Q = {
    "hype": {"type": "score", "instructions": "How promotional or hype-heavy is the `text`?",
             "criteria": ["Plain and factual", "Some promotional wording but still concrete", "Hype: superlatives or unverifiable promises"]},
    "concrete": {"type": "noul", "instructions": "Does the `text` state something concrete a reader can check or act on?"},
    "standalone": {"type": "noul", "instructions": "Can the `text` be understood and quoted on its own, without the surrounding page?"},
    "numeric_claim": {"type": "noul", "instructions": "Does the `text` make a numeric or performance claim?"},
}
live = "--live" in sys.argv
out = []
for b in blocks:
    r = llm.decide({"text": b["text"], "section": b["section"]}, Q, live=live)
    d = r["decisions"]
    out.append({**b, "hype": d["hype"].get("value"), "concrete": d["concrete"].get("value"), "standalone": d["standalone"].get("value"),
                "numeric_claim": d["numeric_claim"].get("value"), "simulated": r["simulated"],
                "flags": [k for k, bad in (("hype", (d["hype"].get("value") or 0) >= 1.5), ("not_concrete", d["concrete"].get("value") is False and d["concrete"].get("status") == "selected"),
                                          ("not_standalone", d["standalone"].get("value") is False and d["standalone"].get("status") == "selected")) if bad]})
(ROOT / "docs" / "gauntlet").mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "gauntlet" / "copy-review.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"{len(out)} blocks, live={live}")
for o in out:
    if o["flags"] or "--all" in sys.argv: print(f"[{o['section']}] {o['flags']} hype={o['hype']} num={o['numeric_claim']} :: {o['text'][:90]}")
