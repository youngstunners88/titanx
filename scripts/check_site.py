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
types, items, graph_nodes = [], [], []
if not blocks: fail("no JSON-LD")
for b in blocks:
    try:
        data = json.loads(b.replace("<\\/", "</"))
    except Exception as e:
        fail(f"JSON-LD does not parse: {e}"); continue
    for n in data.get("@graph", [data]):
        graph_nodes.append(n); types.append(n.get("@type"))
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
BUDGET = 450
if words > BUDGET: fail(f"copy budget exceeded: {words} words > {BUDGET} (outside portfolio cards)")

# --- secret leak scan: env values must not appear in tracked files (names printed only)
leaks = []
tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
SKIP = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".woff2", ".ico")
blob = []
for f in tracked:
    p = ROOT / f
    if p.suffix.lower() in SKIP: continue
    try: blob.append(p.read_text(errors="ignore"))
    except Exception: pass
blob = "\n".join(blob)
for k_, v in os.environ.items():
    if not re.search(r"KEY|TOKEN|SECRET|PASS", k_, re.I) or re.search(r"(URL|URI|PATH|FILE|HOST|DIR)$", k_, re.I): continue
    if len(v) >= 16 and not re.match(r"(https?://|/)", v) and not re.search(r"\s", v) and v in blob:
        leaks.append(k_)
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
for f in ("404.html", "manifest.webmanifest", "brand/favicon-32.png", "brand/apple-touch-icon.png", "brand/fonts/montserrat-latin.woff2"):
    if not (ROOT / f).exists(): fail(f"missing {f}")
if "fonts.googleapis.com" in src or "fonts.gstatic.com" in src: fail("Google Fonts still referenced (self-host instead)")
allowed = ("x.com", "www.instagram.com", "www.smokegame.win", "twitter.com", "youngstunners88.github.io", "schema.org", "www.w3.org", "platform.twitter.com", "us-assets.i.posthog.com", "us.i.posthog.com")
for u in set(re.findall(r'(?:src|href)="(https?://[^"]+)"', src)):
    h = re.sub(r"https?://([^/]+)/?.*", r"\1", u)
    if h not in allowed: fail(f"unexpected third-party host in markup: {h}")
for img in re.findall(r"<img [^>]*>", src):
    if "width=" not in img or "height=" not in img: fail(f"img missing width/height: {img[:70]}")
imgs_kb = sum(f.stat().st_size for f in (ROOT / "brand" / "projects").glob("*.webp")) / 1024
if imgs_kb > 400: fail(f"project avatars weigh {imgs_kb:.0f} KB (budget 400)")
if len(src.encode()) > 140_000: fail("index.html over 140 KB")

# --- round 2: well-formed HTML, anti-slop, AEO/GEO structure
from html.parser import HTMLParser
VOID = {"meta", "link", "img", "input", "br", "hr", "source", "wbr", "col", "area", "base", "embed", "param", "track"}
class _P(HTMLParser):
    def __init__(s): super().__init__(); s.st = []; s.err = []
    def handle_starttag(s, t, a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s, t):
        if t in VOID: return
        if not s.st or s.st[-1] != t: s.err.append(f"unexpected </{t}> (open: {s.st[-3:]}) at line {s.getpos()[0]}")
        else: s.st.pop()
_p = _P(); _p.feed(src)
if _p.err or _p.st: fail(f"HTML not well-formed: {(_p.err or [''])[0]} unclosed={_p.st[:3]}")
vis = re.sub(r"<script.*?</script>|<style.*?</style>", "", src, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", " ", vis))
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
if re.search("[\U0001F300-\U0001FAFF\u25A0-\u25FF\u2600-\u27BF\u2B00-\u2BFF]", text): fail("emoji or pictograph glyph in visible text (AI-slop tell)")
if "\u2014" in text: fail("em dash in visible text (AI-slop tell)")
if "background-clip:text" in style or "-webkit-background-clip:text" in style: fail("gradient text (AI-slop tell)")
if "backdrop-filter" in style: fail("glassmorphism blur (AI-slop tell)")
if re.search(r"box-shadow:0 0 \d{2,}px", style): fail("soft glow shadow (AI-slop tell)")
if re.search(r"\.ico\b|class=\"ico\"", src): fail("icon tile above headings (AI-slop tell)")
fams = set()
for decl in re.findall(r"font-family:([^;}]+)", style) + re.findall(r"--font:([^;}]+)", style):
    for name in decl.split(","):
        name = name.strip().strip("'\"")
        if name and name.lower() not in ("system-ui", "-apple-system", "segoe ui", "sans-serif", "serif", "monospace", "inherit", "var(--font)"): fams.add(name)
if fams - {"Montserrat"}: fail(f"font families other than Montserrat: {sorted(fams - {'Montserrat'})}")
if re.search(r"(purple|violet|#[89a-f][0-9a-f]5cf6)", style, re.I): fail("purple palette (AI-slop tell)")
BANNED = r"\b(revolutionary|cutting-edge|seamless(ly)?|unlock\w*|elevate\w*|supercharge|game-?chang\w*|next-level|leverage|synerg\w*|empower\w*|journey|landscape|delve|tapestry|robust|holistic|world-class|best-in-class)\b"
bad = re.findall(BANNED, text, re.I)
if bad: fail(f"banned filler words in copy: {sorted(set(x[0] if isinstance(x, tuple) else x for x in bad))[:4]}")
# AEO: definitional lede, answer-first FAQ, heading hygiene
lede = re.search(r'<p class="lede">(.*?)</p>', src, re.S)
lt = html.unescape(re.sub(r"<[^>]+>", "", lede.group(1))) if lede else ""
if "Young Stunners" not in lt or not 15 <= len(lt.split()) <= 60: fail(f"lede must define Young Stunners in 15-60 words ({len(lt.split())})")
for q, a in re.findall(r"<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>", src, re.S):
    if len(a.split()) > 40: fail(f"FAQ answer over 40 words: {q[:40]}")
levels = [int(x) for x in re.findall(r"<h([1-6])[ >]", src)]
if any(b - a_ > 1 for a_, b in zip(levels, levels[1:])): fail("heading levels skip")
for hid in re.findall(r"<h2([^>]*)>", src):
    if "id=" not in hid: fail("h2 without id (deep-link anchor)")
# GEO: entity + dated, checkable specifics
org = next((n for n in graph_nodes if isinstance(n.get("@type"), list) and "Organization" in n["@type"]), None)
if not org or len(org.get("sameAs", [])) < 2 or "contactPoint" not in org: fail("Organization needs sameAs (>=2) and contactPoint")
dated = sum(1 for n in graph_nodes if n.get("@type") == "ItemList" for i in n["itemListElement"] if "datePublished" in i["item"])
xposts = sum(1 for n in graph_nodes if n.get("@type") == "ItemList" for i in n["itemListElement"] if "x.com" in i["item"]["url"])
if dated != xposts: fail(f"ItemList: {xposts} X items but {dated} carry datePublished")
sp = re.search(r"X posts dated ([A-Z][a-z]{2} \d{4}) to ([A-Z][a-z]{2} \d{4})", src)
if not sp: fail("date-span fact missing ('X posts dated Mon YYYY to Mon YYYY')")
else:
    import datetime as _dt
    ids = [int(x) for x in re.findall(r"x\.com/[^/\"]+/status/(\d+)", re.search(r'<div class="projects-grid".*?<p class="empty"', src, re.S).group(0))]
    f = lambda i: _dt.datetime.fromtimestamp(((i >> 22) + 1288834974657) / 1000, _dt.timezone.utc)
    want = (min(map(f, ids)).strftime("%b %Y"), max(map(f, ids)).strftime("%b %Y"))
    if (sp.group(1), sp.group(2)) != want: fail(f"date span says {sp.groups()} but post IDs say {want}")
import struct
og = ROOT / "brand" / "og-image.png"
if og.exists():
    w_, h_ = struct.unpack(">II", og.read_bytes()[16:24])
    if (w_, h_) != (1200, 630): fail(f"og-image is {w_}x{h_}, want 1200x630")

if re.search(r"GM-GAME", src, re.I) or "github.com" in src: fail("unreleased game repository must not be linked (owner request)")
# --- round 2 review fixes: numbers agree everywhere, per-item dates, verification date
if "50+" in src: fail("unverifiable '50+' claim in page/metadata (owner claim lives in llms.txt only)")
import datetime as _d
for n in graph_nodes:
    if n.get("@type") == "ItemList":
        for it in n["itemListElement"]:
            u = it["item"].get("url", ""); xm = re.search(r"x\.com/[^/]+/status/(\d+)", u)
            if xm:
                want = _d.datetime.fromtimestamp(((int(xm.group(1)) >> 22) + 1288834974657) / 1000, _d.timezone.utc).strftime("%Y-%m-%d")
                if it["item"].get("datePublished") != want: fail(f"datePublished wrong for {u}: {it['item'].get('datePublished')} != {want}")
lj = ROOT / "docs" / "gauntlet" / "links.json"
vt = re.search(r"X links verified live <time datetime=\"([^\"]+)\"", src)
if lj.exists() and vt:
    checked = max((r.get("checked", "") for r in json.loads(lj.read_text())), default="")
    if checked != vt.group(1): fail(f"facts line says verified {vt.group(1)} but links.json was checked {checked or 'never'} (run scripts/gauntlet/linkcheck.py)")
if "live post" in text and "verified live" not in text: fail("'live post' claim without verification statement")

print(f"words outside cards: {words} (budget {BUDGET}); projects: {len(cards)}")
for w in warns: print("WARN", w)
for f in fails: print("FAIL", f)
print("OK" if not fails else f"{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
