// Rend la signature de fin LUKOJI image par image (PNG) via Chromium.
// Entrée : un fichier JSON de spécification produit par lukoji_engine/signature.py.
// Le temps est piloté image par image (Web Animations API en pause) : rendu déterministe.
import { readFileSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const spec = JSON.parse(readFileSync(process.argv[2], 'utf8'));
mkdirSync(spec.outDir, { recursive: true });
const img = (p) => 'data:image/png;base64,' + readFileSync(p).toString('base64');
const el = (o, id) => o ? `<img id="${id}" src="${img(o.src)}" style="position:absolute;left:${o.x}px;top:${o.y}px;width:${o.w}px;height:${o.h}px;opacity:0">` : '';
const s = spec.symbol;
const html = `<!doctype html><html><head><style>
  html,body{margin:0;width:${spec.width}px;height:${spec.height}px;background:${spec.background};overflow:hidden}
  img{image-rendering:auto}
</style></head><body>
<svg id="sym" viewBox="${s.viewBox.join(' ')}" style="position:absolute;left:${s.x}px;top:${s.y}px;width:${s.w}px;height:${s.h}px;overflow:visible" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path id="p" d="${s.d}" stroke="${s.color}" stroke-width="${s.strokeWidth}" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
${el(spec.logotype, 'logotype')}${el(spec.slogan, 'slogan')}
</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: spec.width, height: spec.height }, deviceScaleFactor: 1 });
await page.setContent(html);
await page.evaluate(async (spec) => {
  await Promise.all([...document.images].map(i => i.decode()));
  const ms = (t) => t * 1000;
  const p = document.getElementById('p');
  const L = p.getTotalLength();
  p.style.strokeDasharray = `${L} ${L}`;
  const anims = [];
  const [d0, d1] = spec.symbol.draw;
  anims.push(p.animate([{ strokeDashoffset: L }, { strokeDashoffset: 0 }],
    { delay: ms(d0), duration: ms(d1 - d0), fill: 'both', easing: 'cubic-bezier(0.65,0,0.35,1)' }));
  for (const id of ['logotype', 'slogan']) {
    const o = spec[id]; if (!o) continue;
    const [a, b] = o.t;
    anims.push(document.getElementById(id).animate(
      [{ opacity: 0, transform: `translateY(${o.rise}px)` }, { opacity: 1, transform: 'translateY(0px)' }],
      { delay: ms(a), duration: ms(b - a), fill: 'both', easing: 'cubic-bezier(0.22,1,0.36,1)' }));
  }
  anims.forEach(a => a.pause());
  window.__seek = (t) => anims.forEach(a => { a.currentTime = t * 1000; });
}, spec);

const n = Math.round(spec.duration * spec.fps);
for (let f = 0; f < n; f++) {
  await page.evaluate((t) => window.__seek(t), f / spec.fps);
  await page.screenshot({ path: `${spec.outDir}/${String(f).padStart(5, '0')}.png` });
}
await browser.close();
console.log(JSON.stringify({ frames: n, outDir: spec.outDir }));
