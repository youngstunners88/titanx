#!/usr/bin/env python3
"""Bump the 'last updated' date everywhere it must agree. python3 scripts/stamp.py [YYYY-MM-DD]
Only run this when content really changed (freshness must be honest)."""
import datetime, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
import re as _re
d = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now(datetime.timezone.utc).date().isoformat()
if not _re.fullmatch(r"\d{4}-\d{2}-\d{2}", d): raise SystemExit(f"date must be YYYY-MM-DD, got {d!r}")
dt = datetime.date.fromisoformat(d); human = f"{dt.day} {dt.strftime('%b %Y')}"
p = ROOT / "index.html"; s = p.read_text()
s = re.sub(r'Last updated <time datetime="[^"]+">[^<]*</time>', f'Last updated <time datetime="{d}">{human}</time>', s)
s = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{d}"', s)
p.write_text(s)
sm = ROOT / "sitemap.xml"; sm.write_text(re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{d}</lastmod>", sm.read_text()))
import subprocess; subprocess.run([sys.executable, str(ROOT / "scripts" / "build_llms.py")], check=True)
print("stamped", d)
