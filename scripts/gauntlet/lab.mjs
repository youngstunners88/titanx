// Lab test: node scripts/gauntlet/lab.mjs [--shots DIR] [--offline-external]
// Needs: playwright (global), axe-core (AXE_PATH or /tmp/axe). Prints one JSON object.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const args = process.argv.slice(2);
const shots = args.includes('--shots') ? args[args.indexOf('--shots') + 1] : null;
const blockExternal = args.includes('--block-external');
let chromium;
try { ({ chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright')); }
catch { const g = require('node:child_process').execSync('npm root -g').toString().trim(); ({ chromium } = require(path.join(g, 'playwright'))); }
const axePath = process.env.AXE_PATH || '/tmp/axe/node_modules/axe-core/axe.min.js';
const axeSrc = fs.existsSync(axePath) ? fs.readFileSync(axePath, 'utf8') : null;

import { serve } from './server.mjs';
const srvh = await serve(root);
const base = process.env.GAUNTLET_URL || srvh.base;

const browser = await chromium.launch();
const out = {};
for (const vp of [{ name: 'mobile', width: 390, height: 844, mobile: true }, { name: 'tiny', width: 320, height: 640, mobile: true }, { name: 'desktop', width: 1280, height: 800, mobile: false }]) {
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: vp.mobile ? 2 : 1, isMobile: vp.mobile, hasTouch: vp.mobile });
  const page = await ctx.newPage();
  const errors = [], failed = [], hosts = {}; let bytes = 0, reqs = 0;
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
  page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 160)));
  page.on('requestfailed', r => failed.push(new URL(r.url()).host + ' ' + (r.failure()?.errorText || '')));
  page.on('response', async r => { try { const h = new URL(r.url()).host; reqs++; const b = await r.body().catch(() => null); const n = b ? b.length : 0; bytes += n; hosts[h] = (hosts[h] || 0) + n; } catch {} });
  if (blockExternal) await page.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
  await page.addInitScript(() => {
    window.__m = { lcp: 0, cls: 0, longTasks: 0, tbt: 0 };
    new PerformanceObserver(l => { for (const e of l.getEntries()) window.__m.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__m.cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver(l => { for (const e of l.getEntries()) { window.__m.longTasks++; window.__m.tbt += Math.max(0, e.duration - 50); } }).observe({ type: 'longtask', buffered: true });
  });
  await page.goto(base, { waitUntil: 'load' });
  await page.waitForTimeout(1200);
  const above = await page.evaluate(() => {
    const first = document.querySelector('.project-link'); const r = first ? first.getBoundingClientRect() : null; const f = document.querySelector('.feat'); const fr = f ? f.getBoundingClientRect() : null;
    return { firstProjectLinkTop: r ? Math.round(r.top + scrollY) : null, firstVideoTileTop: fr ? Math.round(fr.top + scrollY) : null, viewport: innerHeight };
  });
  // scroll through to trigger reveal + lazy
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < total; y += vp.height * 0.8) { await page.evaluate(v => scrollTo(0, v), y); await page.waitForTimeout(120); }
  await page.evaluate(() => { document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; }); scrollTo(0, 0); });
  for (let i = 0; i < 30; i++) { const pending = await page.evaluate(() => [...document.images].filter(x => !x.complete).length); if (!pending) break; await page.waitForTimeout(250); }
  await page.waitForTimeout(300);
  const m = await page.evaluate(() => {
    const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
    const small = [...document.querySelectorAll('button, input, select, summary, nav a, .btn, .tab, .more, .project-link')].filter(vis).map(e => { const r = e.getBoundingClientRect(); return { t: (e.innerText || e.placeholder || e.className).trim().slice(0, 24), w: Math.round(r.width), h: Math.round(r.height) }; }).filter(x => x.h < 44 || x.w < 44);
    const imgs = [...document.images].map(i => ({ src: i.currentSrc.slice(-60), ok: i.complete && i.naturalWidth > 0, w: i.naturalWidth, rendered: Math.round(i.getBoundingClientRect().width) }));
    return { ...window.__m, clippedControls: [...document.querySelectorAll('.btn, .tab, .nav-cta, .feat')].filter(e => e.scrollWidth > e.clientWidth + 1).length, overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1, scrollWidth: document.documentElement.scrollWidth, docHeight: document.documentElement.scrollHeight,
      smallTargets: small.length, smallTargetSamples: small.slice(0, 6), brokenImages: imgs.filter(i => !i.ok).length, images: imgs.length,
      oversizedImages: imgs.filter(i => i.ok && i.w > i.rendered * 3 && i.rendered > 0).length, h1: document.querySelectorAll('h1').length };
  });
  let axe = null;
  if (axeSrc) {
    await page.evaluate(s => { (0, eval)(s); }, axeSrc);
    axe = await page.evaluate(async () => { const r = await axe.run(document, { resultTypes: ['violations'] }); return r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help })); });
  }
  if (shots) { fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, `${vp.name}-fold.png`) }); await page.screenshot({ path: path.join(shots, `${vp.name}-full.png`), fullPage: true }); }
  out[vp.name] = { ...above, ...m, lcpMs: Math.round(m.lcp), tbtMs: Math.round(m.tbt), cls: +m.cls.toFixed(4), transferKB: Math.round(bytes / 1024), requests: reqs, hostsKB: Object.fromEntries(Object.entries(hosts).map(([k, v]) => [k, Math.round(v / 1024)])), consoleErrors: errors, failedRequests: failed.slice(0, 8), axe };
  delete out[vp.name].lcp; delete out[vp.name].tbt; delete out[vp.name].longTasks;
  await ctx.close();
}
await browser.close(); srvh.close();
console.log(JSON.stringify(out, null, 1));
