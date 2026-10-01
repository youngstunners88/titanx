#!/usr/bin/env python3
"""Check every portfolio post link. X posts via publish.twitter.com/oembed (200 = exists,
404 = deleted/protected). Instagram cannot be verified anonymously (reported as 'unverified').
Writes docs/gauntlet/links.json. Rate-limited; safe to rerun."""
import json, re, subprocess, sys, time, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
src = (ROOT / "index.html").read_text()
rows = []
for m in re.finditer(r'<div class="project-card.*?<div class="project-count">', src, re.S):
    blk = m.group(0); name = html.unescape(re.search(r'class="project-name">(.*?)<', blk).group(1)).strip()
    for u in re.findall(r'class="project-link" href="([^"]+)"', blk): rows.append((name, u))
out = []
for i, (name, u) in enumerate(rows):
    host = re.sub(r"https?://(www\.)?([^/]+)/.*", r"\2", u)
    if host in ("x.com", "twitter.com"):
        canon = re.sub(r"/(video|photo)/\d+.*$", "", u).split("?")[0]   # oEmbed rejects /video/1 suffixes
        r = subprocess.run(["curl", "-sL", "-m", "25", "-o", "/dev/null", "-w", "%{http_code}", "https://publish.twitter.com/oembed?omit_script=1&url=" + canon], capture_output=True, text=True).stdout
        status = {"200": "ok", "404": "gone", "403": "protected", "429": "ratelimited"}.get(r, "error:" + r)
        time.sleep(0.35)
    else:
        status = "unverified"
    out.append({"project": name, "url": u, "status": status, "checked": time.strftime("%Y-%m-%d", time.gmtime())})
    if status == "ratelimited": time.sleep(5)
(ROOT / "docs" / "gauntlet").mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "gauntlet" / "links.json").write_text(json.dumps(out, indent=1))
from collections import Counter
print(Counter(o["status"] for o in out))
for o in out:
    if o["status"] not in ("ok", "unverified"): print(o["status"], o["project"], o["url"])

# keep the page's verification claim in sync with what was just verified
import datetime
ok = sum(1 for o in out if o["status"] == "ok")
today = datetime.datetime.now(datetime.timezone.utc).date()
idx = ROOT / "index.html"; page = idx.read_text()
new = re.sub(r"\d+ X links verified live <time datetime=\"[^\"]+\">[^<]*</time>", f'{ok} X links verified live <time datetime="{today.isoformat()}">{today.day} {today.strftime("%b %Y")}</time>', page)
if new != page: idx.write_text(new); print("facts line refreshed:", ok, "ok,", today)
