// node video/audit.mjs  -> lists text elements that leave the 540x960 safe area (16px margin) or overlap another text element
import { createRequire } from 'node:module'; import path from 'node:path';
const require = createRequire(import.meta.url);
const g = require('node:child_process').execSync('npm root -g').toString().trim(); const { chromium } = require(path.join(g, 'playwright'));
const here = path.dirname(new URL(import.meta.url).pathname);
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await (await browser.newContext({ viewport: { width: 540, height: 960 } })).newPage();
await page.goto('file://' + path.join(here, 'scene.html')); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(500);
const bad = new Map();
for (let f = 0; f < 900; f += 3) {
  const r = await page.evaluate(t => { window.setT(t); const out = [];
    const items = [];
    document.querySelectorAll('#stage *').forEach(el => {
      const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); if (!own) return;
      let o = 1, p = el; while (p && p.id !== 'stage') { o *= parseFloat(getComputedStyle(p).opacity); if (getComputedStyle(p).display === 'none') o = 0; p = p.parentElement } if (o < .85) return;
      const b = el.getBoundingClientRect(); if (!b.width) return;
      const txt = el.textContent.trim().slice(0, 24); items.push({ el, txt, x: b.left, y: b.top, r: b.right, b: b.bottom });
      if (b.left < 14 || b.right > 526 || b.top < 14 || b.bottom > 946) out.push(`CLIP "${txt}" [${b.left | 0},${b.top | 0},${b.right | 0},${b.bottom | 0}]`);
    });
    for (let i = 0; i < items.length; i++) for (let j = i + 1; j < items.length; j++) { const a = items[i], c = items[j]; const ox = Math.min(a.r, c.r) - Math.max(a.x, c.x), oy = Math.min(a.b, c.b) - Math.max(a.y, c.y); if (ox > 6 && oy > 6 && !a.el.contains(c.el) && !c.el.contains(a.el)) out.push(`OVERLAP "${a.txt}" x "${c.txt}"`) }
    return out }, f / 30);
  for (const m of r) { if (!bad.has(m)) bad.set(m, [f / 30, f / 30]); else bad.get(m)[1] = f / 30 }
}
for (const [m, [a, b]] of bad) console.log(`${a.toFixed(1)}-${b.toFixed(1)}s ${m}`);
console.log(bad.size ? `${bad.size} issues` : 'layout audit clean');
await browser.close();
