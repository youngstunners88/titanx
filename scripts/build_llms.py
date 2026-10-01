#!/usr/bin/env python3
"""Regenerate llms.txt from index.html. python3 scripts/build_llms.py [--check]"""
import html, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
s = (ROOT / "index.html").read_text()
rows, posts = [], 0
for m in re.finditer(r'<div class="project-card.*?<div class="project-count">', s, re.S):
    b = m.group(0)
    n = html.unescape(re.search(r'class="project-name">(.*?)<', b).group(1)).strip()
    c = html.unescape(re.search(r'class="project-category">(.*?)<', b).group(1)).strip()
    l = re.findall(r'class="project-link" href="([^"?]+)', b); posts += len(l)
    rows.append(f"- {n} ({c}), {len(l)} post{'s' if len(l) != 1 else ''}: {l[0] if l else ''}")
upd = re.search(r'Last updated <time datetime="([^"]+)"', s).group(1)
txt = f"""# Young Stunners

> Young Stunners is a Web3 content creator that makes short-form promotional videos and runs X (Twitter) and Instagram campaigns for crypto projects (DeFi, memecoins, NFT and gaming). The portfolio lists {len(rows)} projects and {posts} linked posts.

Last updated: {upd}

## Facts
- Services: viral video content, KOL promotion, token launch campaigns, community growth content
- Ecosystems: Ethereum, BSC, Base, TitanX ecosystem
- Platforms: X (Twitter), Instagram
- Pricing: custom quote per project; clients approve content before it is posted
- Claimed by owner: 50+ projects promoted, 100+ videos created
- Website: https://youngstunners88.github.io/titanx/
- X: https://x.com/youngstunnersss
- Instagram: https://www.instagram.com/chris1dragon
- Posts promote client projects. Nothing here is financial advice.

## Latest project
- Lil Blunt: The Smoke Realm, a free Wild West 2D platformer in the browser on the Internet Computer: https://www.smokegame.win/ (code: https://github.com/youngstunners88/GM-GAME)

## How to hire
Use the brief form on the website, or DM @youngstunnersss on X or @chris1dragon on Instagram with project name, chain, goal and timeline.

## Portfolio (first live post per project; all are public posts)
""" + "\n".join(rows) + "\n"
p = ROOT / "llms.txt"
if "--check" in sys.argv:
    sys.exit(0 if p.exists() and p.read_text() == txt else 1)
p.write_text(txt); print(f"llms.txt: {len(rows)} projects, {posts} posts, updated {upd}")
