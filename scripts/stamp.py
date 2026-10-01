#!/usr/bin/env python3
"""Bump the 'last updated' date everywhere it must agree. python3 scripts/stamp.py [YYYY-MM-DD]
Only run this when content really changed (freshness must be honest)."""
import datetime, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
d = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
dt = datetime.date.fromisoformat(d); human = f"{dt.day} {dt.strftime('%b %Y')}"
p = ROOT / "index.html"; s = p.read_text()
s = re.sub(r'Last updated <time datetime="[^"]+">[^<]*</time>', f'Last updated <time datetime="{d}">{human}</time>', s)
s = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{d}"', s)
p.write_text(s)
sm = ROOT / "sitemap.xml"; sm.write_text(re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{d}</lastmod>", sm.read_text()))
import subprocess; subprocess.run([sys.executable, str(ROOT / "scripts" / "build_llms.py")], check=True)
print("stamped", d)
