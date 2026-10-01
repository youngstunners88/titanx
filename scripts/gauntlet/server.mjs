// Static file server for the harnesses (127.0.0.1, ephemeral port). Safe path handling.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.txt': 'text/plain', '.xml': 'application/xml', '.json': 'application/json', '.svg': 'image/svg+xml', '.webmanifest': 'application/manifest+json' };
export function inside(root, f) { const rel = path.relative(root, f); return rel !== '..' && !rel.startsWith('..' + path.sep) && !path.isAbsolute(rel); }
export async function serve(root) {
  const srv = http.createServer((req, res) => {
    let p; try { p = decodeURIComponent(req.url.split('?')[0]); } catch { res.writeHead(400); return res.end('bad'); }
    if (p.endsWith('/')) p += 'index.html';
    const f = path.join(root, p);
    if (!inside(root, f) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nf'); }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
  });
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  return { base: `http://127.0.0.1:${srv.address().port}/`, close: () => srv.close() };
}
