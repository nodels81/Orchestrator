// Rendert die SVGs zu PNG (Playwright + vorinstalliertes Chromium)
const { chromium } = require('playwright');
const fs = require('fs');
const ziele = [
  ['delatec-logo.svg', 'delatec-logo.png', 4],
  ['delatec-logo-negativ.svg', 'delatec-logo-negativ.png', 4],
  ['delatec-icon.svg', 'delatec-icon-512.png', 512 / 120],
  ['delatec-instagram-profil.svg', 'delatec-instagram-profil-1080.png', 9],
];
(async () => {
  const browser = await chromium.launch();
  for (const [quelle, ziel, faktor] of ziele) {
    const svg = fs.readFileSync(__dirname + '/' + quelle, 'utf8');
    const [, w, h] = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
    const page = await browser.newPage({ viewport: { width: Math.round(w), height: Math.round(h) }, deviceScaleFactor: faktor });
    await page.setContent(`<style>html,body{margin:0}svg{display:block}</style>${svg}`);
    await page.screenshot({ path: __dirname + '/' + ziel, omitBackground: true });
    console.log(ziel);
  }
  await browser.close();
})();
