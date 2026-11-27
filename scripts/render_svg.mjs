// Rastérise un SVG officiel en PNG transparent via Chromium (Playwright pré-installé).
// La géométrie n'est jamais modifiée : seule la couleur de trait peut être substituée.
// Usage : node scripts/render_svg.mjs <in.svg> <out.png> <largeur_px> [couleur_trait]
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [,, input, output, widthArg, color] = process.argv;
if (!input || !output || !widthArg) { console.error('usage: render_svg.mjs in.svg out.png width [color]'); process.exit(2); }
let svg = readFileSync(input, 'utf8');
const vb = svg.match(/viewBox="\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*"/);
if (!vb) { console.error('viewBox introuvable'); process.exit(3); }
const vw = parseFloat(vb[3]), vh = parseFloat(vb[4]);
const W = parseInt(widthArg, 10), H = Math.round(W * vh / vw);
if (color) svg = svg.replace(/stroke="#[0-9A-Fa-f]{3,8}"/g, `stroke="${color}"`);
svg = svg.replace('<svg ', `<svg width="${W}" height="${H}" `);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
await page.screenshot({ path: output, omitBackground: true, clip: { x: 0, y: 0, width: W, height: H } });
await browser.close();
console.log(JSON.stringify({ output, width: W, height: H, viewBox: [vw, vh] }));
