// Behavioural tests. node scripts/gauntlet/interact.mjs [--shots DIR]. Prints JSON {tests:[{name,pass,detail}]}.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const g = require('node:child_process').execSync('npm root -g').toString().trim(); const { chromium } = require(path.join(g, 'playwright'));
const args = process.argv.slice(2); const shots = args.includes('--shots') ? args[args.indexOf('--shots') + 1] : null;
import { serve } from './server.mjs';
const srvh = await serve(root);
const base = process.env.GAUNTLET_URL || srvh.base;
const b = await chromium.launch(); const tests = []; const t = (name, pass, detail = '') => tests.push({ name, pass: !!pass, detail: String(detail).slice(0, 200) });

async function fresh(vp, extra = {}) { const c = await b.newContext({ ignoreHTTPSErrors: true, viewport: vp, permissions: ['clipboard-read', 'clipboard-write'], ...extra }); const p = await c.newPage(); await p.goto(base); await p.waitForTimeout(500); return { c, p }; }

// desktop
{
  const { c, p } = await fresh({ width: 1280, height: 800 });
  const total = await p.$$eval('.project-card', e => e.length);
  await p.click('.tab[data-filter="instagram"]');
  const igShown = await p.$$eval('.project-card', e => e.filter(x => getComputedStyle(x).display !== 'none').length);
  t('filter: instagram shows only IG cards', igShown === 2, `shown=${igShown}`);
  t('filter: aria-pressed updates', (await p.getAttribute('.tab[data-filter="instagram"]', 'aria-pressed')) === 'true' && (await p.getAttribute('.tab[data-filter="all"]', 'aria-pressed')) === 'false');
  t('filter: live count text', /Showing 2 of 38/.test(await p.textContent('#count')), await p.textContent('#count'));
  await p.click('.tab[data-filter="all"]'); await p.fill('#search', 'volt');
  const volt = await p.$$eval('.project-card', e => e.filter(x => getComputedStyle(x).display !== 'none').length);
  t('search: "volt" narrows results', volt >= 2 && volt < total, `shown=${volt}`);
  await p.fill('#search', 'zzzznomatch'); t('search: empty state visible', await p.isVisible('#empty'));
  await p.fill('#search', '');
  const xssBefore = await p.evaluate(() => document.querySelectorAll('img[onerror]').length); await p.fill('#search', '<img src=x onerror=alert(1)>'); t('search: input is not injected as HTML', (await p.evaluate(() => document.querySelectorAll('img[onerror]').length)) === xssBefore); await p.fill('#search', '');
  // show-all toggle
  const more = await p.$('.more'); await more.click(); t('card: "show all" expands links', (await p.$$eval('.project-links:not(.collapsed) .project-link', e => e.length)) > 3);
  await p.goto(base); await p.keyboard.press('Tab'); t('keyboard: first focus is skip link', (await p.evaluate(() => document.activeElement.className)) === 'skip');
  await p.click('.feat >> nth=0');
  // featured player
  let state = 'timeout';
  for (let i = 0; i < 24; i++) { await p.waitForTimeout(500); state = await p.evaluate(() => { const pl = document.querySelector('#player'); if (pl.querySelector('iframe, .twitter-tweet, twitter-widget')) return 'embed'; if (pl.querySelector('.msg a')) return 'fallback'; return 'loading'; }); if (state !== 'loading') break; }
  t('player: embed or graceful fallback (never stuck)', state === 'embed' || state === 'fallback', state);
  if (shots) { fs.mkdirSync(shots, { recursive: true }); await p.locator('#player').scrollIntoViewIfNeeded(); await p.screenshot({ path: path.join(shots, 'player.png') }); }
  // brief form
  await p.evaluate(() => document.querySelector('#contact').scrollIntoView());
  await p.evaluate(() => { window.__opens = []; const o = window.open; window.open = (...a) => { window.__opens.push({ a, syncBeforeAwait: !window.__awaited }); return o.apply(window, a); }; const w = navigator.clipboard.writeText.bind(navigator.clipboard); navigator.clipboard.writeText = (x) => { window.__awaited = true; return w(x); }; });
  await p.fill('#b-name', '$TEST'); await p.click('#brief button[type=submit]'); await p.waitForTimeout(400);
  const clip = await p.evaluate(() => navigator.clipboard.readText().catch(() => ''));
  t('brief: copies a filled brief to clipboard', /Project: \$TEST/.test(clip) && /Timeline:/.test(clip), clip.slice(0, 60));
  const opens = await p.evaluate(() => window.__opens);
  t('brief: opens x.com/youngstunnersss synchronously in the tap (Safari-safe)', opens.length === 1 && /x\.com\/youngstunnersss/.test(opens[0].a[0]) && opens[0].a[2] === 'noopener' && opens[0].syncBeforeAwait, JSON.stringify(opens).slice(0, 120));
  t('brief: shows success toast', /copied/i.test(await p.textContent('#toast')));
  await p.evaluate(() => document.querySelector('#faq details').setAttribute('open', '')); t('faq: details open', await p.isVisible('#faq details[open] p'));
  await c.close();
}
// mobile
{
  const { c, p } = await fresh({ width: 390, height: 844 }, { isMobile: true, hasTouch: true });
  t('sticky CTA hidden at top', !(await p.evaluate(() => document.querySelector('#sticky').classList.contains('show'))));
  await p.evaluate(() => scrollTo({top:1500,behavior:'instant'})); await p.waitForTimeout(700); t('sticky CTA shows after hero', await p.evaluate(() => document.querySelector('#sticky').classList.contains('show')));
  await p.evaluate(() => document.querySelector('#contact').scrollIntoView({behavior:'instant'})); await p.waitForTimeout(900); t('sticky CTA hides at contact form', !(await p.evaluate(() => document.querySelector('#sticky').classList.contains('show'))));
  t('mobile: no horizontal overflow', !(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)));
  await c.close();
}
// no key => no analytics request
{
  const c = await b.newContext({ ignoreHTTPSErrors: true }); const p = await c.newPage(); const hits = []; p.on('request', r => { if (/posthog|google-analytics|googletagmanager/.test(r.url())) hits.push(r.url()); });
  await p.goto(base); await p.waitForTimeout(800); t('privacy: no analytics requests without a configured key', hits.length === 0, hits.join(','));
  const ext = []; p.on('request', r => { if (!r.url().startsWith('http://127.0.0.1')) ext.push(new URL(r.url()).host); }); await p.reload(); await p.waitForTimeout(800); t('privacy: no third-party requests on load', ext.length === 0, [...new Set(ext)].join(','));
  await c.close();
}
await b.close(); srvh.close();
console.log(JSON.stringify({ tests }, null, 1));
