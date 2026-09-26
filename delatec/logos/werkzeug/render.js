// SVG -> PNG mit dem vorinstallierten Chromium.
// Aufruf: node render.js eingabe.svg:ausgabe.png:breitePx [...]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  for (const arg of process.argv.slice(2)) {
    const [quelle, ziel, px] = arg.split(':');
    const svg = fs.readFileSync(quelle, 'utf8');
    const [, w, h] = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
    const faktor = px ? Number(px) / w : 1;
    const page = await browser.newPage({ viewport: { width: Math.ceil(w), height: Math.ceil(h) }, deviceScaleFactor: faktor });
    await page.setContent(`<style>html,body{margin:0}svg{display:block}</style>${svg}`);
    await page.screenshot({ path: ziel, omitBackground: true });
    await page.close();
  }
  await browser.close();
})();
