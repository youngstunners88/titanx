#!/usr/bin/env python3
"""Self-host Montserrat (400-900), latin subset, variable woff2. One family only (anti-slop rule).
Writes brand/fonts/*.woff2 and prints the @font-face CSS (kept inline in index.html)."""
import re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
url = "https://fonts.googleapis.com/css2?family=Montserrat:wght@400..900&display=swap"
css = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
out = []
for m in re.finditer(r"/\* latin \*/\s*@font-face \{(.*?)\}", css, re.S):
    b = m.group(1)
    fam = re.search(r"font-family: '([^']+)'", b).group(1)
    wt = re.search(r"font-weight: ([0-9 ]+);", b).group(1).strip()
    u = re.search(r"url\(([^)]+)\)", b).group(1)
    fn = f"brand/fonts/{fam.lower()}-latin.woff2"
    data = subprocess.run(["curl", "-sf", "-m", "30", u], capture_output=True).stdout
    if data[:4] != b"wOF2" or len(data) < 5000:
        raise SystemExit(f"font download failed for {fam}: not a woff2 file")
    (ROOT / fn).write_bytes(data)
    out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;src:url({fn}) format('woff2')}}")
print("\n".join(out))
