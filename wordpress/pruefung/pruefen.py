#!/usr/bin/env python3
"""Misst, ob Warenkorb und Kasse auf schmalen Schirmen überlaufen.

Die beiden HTML-Dateien daneben sind kein Entwurf, sondern Abzüge vom
Markup, das WooCommerce selbst ausgibt — mit seinen Klassennamen, seinen
data-title-Attributen und einem absichtlich langen Ortsnamen. Sie hängen
an den echten Stilen des Themes. Ändert sich shop.css, misst dieser Lauf
die Änderung.

Geprüft wird zweierlei:
  1. Die Seite scrollt nie seitlich (das sieht man sofort).
  2. Auch das Warenkorbformular scrollt nicht seitlich (das sieht man
     nicht sofort — die Seite steht still, nur die Zeilen lassen sich
     schieben, und das merkt man erst beim Kaufen).

    python3 wordpress/pruefung/pruefen.py
"""

import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

ORDNER = pathlib.Path(__file__).parent
SEITEN = ["warenkorb.html", "kasse.html"]
BREITEN = [320, 375, 768, 1280]

# Der Container bringt Chromium mit, aber keinen Playwright-eigenen Abzug.
KANDIDATEN = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
]

UEBERLAUF = """() => {
    const w = document.documentElement.clientWidth;
    const raus = [];
    for (const el of document.querySelectorAll('*')) {
        const r = el.getBoundingClientRect();
        if (r.width === 0) continue;
        if (r.right > w + 1 || r.left < -1) {
            raus.push({
                t: el.tagName.toLowerCase(),
                k: (el.className && el.className.toString ? el.className.toString() : '').slice(0, 60),
                ueber: Math.round(Math.max(r.right - w, -r.left)),
            });
        }
    }
    const f = document.querySelector('.woocommerce-cart-form');
    return {
        scroll: document.documentElement.scrollWidth,
        klient: w,
        formular_scrollt: f ? f.scrollWidth > f.clientWidth + 1 : false,
        raus: raus.slice(0, 6),
    };
}"""


def browserpfad() -> str | None:
    for pfad in KANDIDATEN:
        if pathlib.Path(pfad).exists():
            return pfad
    return None


async def main() -> int:
    pfad = browserpfad()
    maengel = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=pfad) if pfad else await p.chromium.launch()
        for datei in SEITEN:
            for breite in BREITEN:
                seite = await browser.new_page(viewport={"width": breite, "height": 900})
                await seite.goto((ORDNER / datei).as_uri())
                mass = await seite.evaluate(UEBERLAUF)
                await seite.close()

                if mass["scroll"] > mass["klient"] + 1:
                    maengel += 1
                    print(f"UEBERLAUF  {datei} @{breite}: {mass['scroll']} statt {mass['klient']}")
                    for r in mass["raus"]:
                        print(f"           {r['t']}.{r['k']}  +{r['ueber']}px")
                elif mass["formular_scrollt"]:
                    maengel += 1
                    print(f"SEITWAERTS {datei} @{breite}: der Warenkorb laesst sich seitlich schieben")
                else:
                    print(f"ok         {datei} @{breite}")
        await browser.close()

    print()
    print("Alles im Rahmen." if not maengel else f"{maengel} Stelle(n) zu breit.")
    return 1 if maengel else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
