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
for sec in re.finditer(r"<(header|section|footer)\b([^>]*)>(.*?)</\1>", body, re.S):
    idm = re.search(r'\bid="([^"]+)"', sec.group(2))
    name = idm.group(1) if idm else sec.group(1)
    for t in re.findall(r"<(?:h1|h2|h3|p|summary)[^>]*>(.*?)</(?:h1|h2|h3|p|summary)>", sec.group(3), re.S):
        txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))).strip()
        if len(txt.split()) >= 4: blocks.append({"section": name, "text": txt})
def questions_for(key):
    f = f"`blocks.{key}`"
    return {
        f"{key}__hype": {"type": "score", "instructions": f"How promotional or hype-heavy is the text at {f}?",
                         "criteria": ["Plain and factual", "Some promotional wording but still concrete", "Hype: superlatives or unverifiable promises"]},
        f"{key}__concrete": {"type": "noul", "instructions": f"Does the text at {f} state something concrete a reader can check or act on?"},
        f"{key}__standalone": {"type": "noul", "instructions": f"Can the text at {f} be understood and quoted on its own, without the surrounding page?"},
        f"{key}__numeric": {"type": "noul", "instructions": f"Does the text at {f} make a numeric or performance claim?"},
    }


live = "--live" in sys.argv
Q, state_blocks = {}, {}
for i, b in enumerate(blocks):
    key = f"b{i}"; state_blocks[key] = b["text"]; Q.update(questions_for(key))
r = llm.decide({"blocks": state_blocks}, Q, live=live)     # ONE request for the whole page
D = r["decisions"]
out = []
for i, b in enumerate(blocks):
    k = f"b{i}"; h, c, st, n = (D[f"{k}__{x}"] for x in ("hype", "concrete", "standalone", "numeric"))
    hv = h.get("value")
    out.append({**b, "hype": hv, "concrete": c.get("value"), "standalone": st.get("value"), "numeric_claim": n.get("value"), "simulated": r["simulated"],
                "flags": [k_ for k_, bad in (("hype", isinstance(hv, (int, float)) and hv >= 1.5),
                                             ("not_concrete", c.get("value") is False and c.get("status") == "selected"),
                                             ("not_standalone", st.get("value") is False and st.get("status") == "selected")) if bad]})
(ROOT / "docs" / "gauntlet").mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "gauntlet" / "copy-review.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"{len(out)} blocks, live={live}")
for o in out:
    if o["flags"] or "--all" in sys.argv: print(f"[{o['section']}] {o['flags']} hype={o['hype']} num={o['numeric_claim']} :: {o['text'][:90]}")
