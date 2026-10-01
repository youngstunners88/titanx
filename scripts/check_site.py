#!/usr/bin/env python3
"""Static audit for index.html. Run: python3 scripts/check_site.py
Exit code 1 on any FAIL. Prints names only, never secret values."""
import re, json, os, sys, html, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "index.html").read_text()
fails, warns = [], []
def fail(m): fails.append(m)
def warn(m): warns.append(m)

# --- head
title = re.search(r"<title>(.*?)</title>", src, re.S)
t = html.unescape(title.group(1)).strip() if title else ""
if not t: fail("missing <title>")
elif len(t) > 65: warn(f"title is {len(t)} chars (aim <= 60)")
desc = re.search(r'<meta name="description" content="(.*?)"', src)
d = html.unescape(desc.group(1)) if desc else ""
if not d: fail("missing meta description")
elif not 70 <= len(d) <= 165: warn(f"description is {len(d)} chars (aim 120-160)")
for pat, name in [(r'rel="canonical"', "canonical"), (r'property="og:image"', "og:image"),
                  (r'name="twitter:card"', "twitter:card"), (r'name="viewport"', "viewport"),
                  (r'<html lang=', "html lang"), (r"<main", "<main>")]:
    if not re.search(pat, src): fail(f"missing {name}")
if len(re.findall(r"<h1[ >]", src)) != 1: fail("page must have exactly one <h1>")

# --- JSON-LD
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
types, items = [], []
if not blocks: fail("no JSON-LD")
for b in blocks:
    try:
        data = json.loads(b.replace("<\\/", "</"))
    except Exception as e:
        fail(f"JSON-LD does not parse: {e}"); continue
    for n in data.get("@graph", [data]):
        types.append(n.get("@type"))
        if n.get("@type") == "ItemList":
            items = [i["item"]["name"] for i in n["itemListElement"]]
flat = {x for t in types for x in (t if isinstance(t, list) else [t])}
for need in ("Organization", "WebSite", "WebPage", "ItemList"):
    if need not in flat: fail(f"JSON-LD missing {need}")

# --- portfolio parity
cards = [html.unescape(x).strip() for x in re.findall(r'class="project-name">(.*?)<', src)]
if sorted(cards) != sorted(items): fail(f"ItemList ({len(items)}) != portfolio cards ({len(cards)})")
llms = (ROOT / "llms.txt").read_text() if (ROOT / "llms.txt").exists() else ""
miss = [c for c in cards if c not in llms]
if miss: fail(f"llms.txt missing projects: {miss[:5]}")

# --- required files
for f in ("robots.txt", "sitemap.xml", "llms.txt", "brand/og-image.png", "brand/young-stunners-logo.png"):
    if not (ROOT / f).exists(): fail(f"missing file {f}")

# --- links / images
ids = set(re.findall(r'id="([^"]+)"', src))
for a in set(re.findall(r'href="#([^"]+)"', src)):
    if a not in ids: fail(f"broken anchor #{a}")
for img in re.findall(r"<img [^>]*>", src):
    if "alt=" not in img: fail(f"img without alt: {img[:60]}")
for local in set(re.findall(r'(?:src|href)="((?:brand|logos)/[^"]+)"', src)):
    if not (ROOT / local).exists(): fail(f"missing asset {local}")

# --- verbosity budget (visible words outside project cards)
body = re.sub(r'<div class="projects-grid".*?</div>\s*<p class="empty"', '<p class="empty"', src, flags=re.S)
body = re.sub(r"<script.*?</script>|<style.*?</style>|<head>.*?</head>", "", body, flags=re.S)
words = len(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
BUDGET = 400
if words > BUDGET: fail(f"copy budget exceeded: {words} words > {BUDGET} (outside portfolio cards)")

# --- secret leak scan: env values must not appear in tracked files (names printed only)
leaks = []
tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
texts = {}
for f in tracked:
    p = ROOT / f
    if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif"): continue
    try: texts[f] = p.read_text(errors="ignore")
    except Exception: pass
for k, v in os.environ.items():
    if len(v) >= 16 and re.search(r"KEY|TOKEN|SECRET|API|PASS", k, re.I):
        if any(v in tx for tx in texts.values()): leaks.append(k)
if leaks: fail(f"SECRET VALUE FOUND in tracked files for env var(s): {leaks}")


# --- facts, dates, hygiene (gauntlet round 4)
posts = len(re.findall(r'class="project-link"', src))
m = re.search(r"(\d+) projects · (\d+) posts · (\d+) X links verified live", src)
if not m: fail("facts line missing ('N projects · N posts · N X links verified live')")
else:
    if int(m.group(1)) != len(cards): fail(f"facts line says {m.group(1)} projects, page has {len(cards)}")
    if int(m.group(2)) != posts: fail(f"facts line says {m.group(2)} posts, page has {posts}")
    lj = ROOT / "docs" / "gauntlet" / "links.json"
    if lj.exists():
        ok = sum(1 for r in json.loads(lj.read_text()) if r["status"] == "ok")
        if int(m.group(3)) != ok: fail(f"facts line says {m.group(3)} verified X links, links.json has {ok} ok (rerun linkcheck, update line)")
vis = re.search(r'Last updated <time datetime="([^"]+)"', src)
mod = re.search(r'"dateModified":"([^"]+)"', src)
lm = re.search(r"<lastmod>([^<]+)</lastmod>", (ROOT / "sitemap.xml").read_text()) if (ROOT / "sitemap.xml").exists() else None
if not (vis and mod and lm and vis.group(1) == mod.group(1) == lm.group(1)): fail("dates disagree: visible / JSON-LD dateModified / sitemap lastmod (run scripts/stamp.py)")
if subprocess.run([sys.executable, str(ROOT / "scripts" / "build_llms.py"), "--check"]).returncode != 0: fail("llms.txt out of date (run scripts/build_llms.py)")
for f in ("404.html", "manifest.webmanifest", "brand/favicon-32.png", "brand/apple-touch-icon.png", "brand/fonts/inter-latin.woff2", "brand/fonts/montserrat-latin.woff2"):
    if not (ROOT / f).exists(): fail(f"missing {f}")
if "fonts.googleapis.com" in src or "fonts.gstatic.com" in src: fail("Google Fonts still referenced (self-host instead)")
allowed = ("x.com", "www.instagram.com", "twitter.com", "youngstunners88.github.io", "schema.org", "www.w3.org", "platform.twitter.com", "us-assets.i.posthog.com", "us.i.posthog.com")
for u in set(re.findall(r'(?:src|href)="(https?://[^"]+)"', src)):
    h = re.sub(r"https?://([^/]+)/?.*", r"\1", u)
    if h not in allowed: fail(f"unexpected third-party host in markup: {h}")
for img in re.findall(r"<img [^>]*>", src):
    if "width=" not in img or "height=" not in img: fail(f"img missing width/height: {img[:70]}")
imgs_kb = sum(f.stat().st_size for f in (ROOT / "brand" / "projects").glob("*.webp")) / 1024
if imgs_kb > 400: fail(f"project avatars weigh {imgs_kb:.0f} KB (budget 400)")
if len(src.encode()) > 140_000: fail("index.html over 140 KB")

print(f"words outside cards: {words} (budget {BUDGET}); projects: {len(cards)}")
for w in warns: print("WARN", w)
for f in fails: print("FAIL", f)
print("OK" if not fails else f"{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
