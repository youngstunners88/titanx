#!/usr/bin/env python3
"""Localize and optimize project avatars + site logo. Idempotent.
  PYTHONPATH=/tmp/pylibs python3 scripts/build_assets.py
Rewrites external <img src> in index.html to brand/projects/<slug>.webp (96x96, cover crop),
records provenance in brand/projects/SOURCES.json, and builds logo/favicon variants."""
import html, io, json, re, subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "projects"; OUT.mkdir(parents=True, exist_ok=True)
src = (ROOT / "index.html").read_text()
sources_path = OUT / "SOURCES.json"
sources = json.loads(sources_path.read_text()) if sources_path.exists() else {}


def fetch(url):
    if url.startswith(("http://", "https://")):
        for _ in range(3):
            r = subprocess.run(["curl", "-sL", "-m", "40", url], capture_output=True)
            if r.returncode == 0 and len(r.stdout) > 200:
                return r.stdout
        raise SystemExit(f"download failed: {url}")
    return (ROOT / url).read_bytes()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def to_webp(data, size=96, q=82):
    im = Image.open(io.BytesIO(data)); im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
    w, h = im.size; s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((size, size), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6); return buf.getvalue()


# --- project avatars: one per card, named after the project
changed = 0
seen_slugs = {}
for m in list(re.finditer(r'<div class="project-card.*?<div class="project-count">', src, re.S)):
    blk = m.group(0)
    name = html.unescape(re.search(r'class="project-name">(.*?)<', blk).group(1)).strip()
    im = re.search(r'<img [^>]*src="([^"]+)"', blk)
    if not im or im.group(1).startswith("brand/projects/"):
        continue
    url = im.group(1)
    fn = f"brand/projects/{slug(name)}.webp"
    if seen_slugs.setdefault(fn, name) != name:
        raise SystemExit(f"slug collision: {name!r} and {seen_slugs[fn]!r} both map to {fn}")
    (ROOT / fn).write_bytes(to_webp(fetch(url)))
    sources[fn] = url if url.startswith("http") else "repo:" + url
    src = src.replace(blk, blk.replace(url, fn)); changed += 1
sources_path.write_text(json.dumps(dict(sorted(sources.items())), indent=1))

# --- normalise avatar attrs (explicit size, lazy, async) so layout never shifts
src = re.sub(r'<img loading="lazy" decoding="async" src="(brand/projects/[^"]+)" alt="([^"]*)" style="[^"]*">',
             r'<img loading="lazy" decoding="async" src="\1" alt="\2" width="48" height="48">', src)
src = re.sub(r'<img src="(brand/projects/[^"]+)" alt="([^"]*)" style="[^"]*">',
             r'<img loading="lazy" decoding="async" src="\1" alt="\2" width="48" height="48">', src)
(ROOT / "index.html").write_text(src)

# --- logo variants (transparent PNG has white letter fill -> keep on white plate in CSS)
logo = Image.open(ROOT / "brand" / "young-stunners-logo.png").convert("RGBA")
w, h = logo.size
nav = logo.resize((round(76 * w / h), 76), Image.LANCZOS); nav.save(ROOT / "brand" / "logo-nav.webp", "WEBP", quality=85, method=6)
logo.resize((680, round(680 * h / w)), Image.LANCZOS).save(ROOT / "brand" / "logo-hero.webp", "WEBP", quality=88, method=6)
for px, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png"), (32, "favicon-32.png")]:
    bg = Image.new("RGBA", (px, px), (255, 255, 255, 255)); k = (px * 0.86) / max(w, h)
    lg = logo.resize((round(w * k), round(h * k)), Image.LANCZOS); bg.alpha_composite(lg, ((px - lg.width) // 2, (px - lg.height) // 2))
    bg.convert("RGB").save(ROOT / "brand" / name, optimize=True)
print(f"avatars localized this run: {changed}; files in brand/projects: {len(list(OUT.glob('*.webp')))}")
