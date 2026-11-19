// node video/render.mjs <startFrame> <endFrame> <outDir>   (30 fps, 540x960 CSS at 2x = 1080x1920)
import { createRequire } from 'node:module'; import path from 'node:path'; import fs from 'node:fs';
const require = createRequire(import.meta.url);
const g = require('node:child_process').execSync('npm root -g').toString().trim(); const { chromium } = require(path.join(g, 'playwright'));
const [a, b, out] = [Number(process.argv[2]), Number(process.argv[3]), process.argv[4]]; fs.mkdirSync(out, { recursive: true });
const here = path.dirname(new URL(import.meta.url).pathname);
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const ctx = await browser.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 }); const page = await ctx.newPage();
await page.goto('file://' + path.join(here, 'scene.html')); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(800);
for (let f = a; f < b; f++) {
  await page.evaluate(t => window.setT(t), f / 30);
  await page.screenshot({ path: path.join(out, `f${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 93 });
}
await browser.close();
