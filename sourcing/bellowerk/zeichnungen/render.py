"""Rendert alle SVG-Zeichnungen in diesem Ordner als PNG (2x) mit Chromium via Playwright."""

import asyncio
import os
import pathlib
import re

from playwright.async_api import async_playwright

ORDNER = pathlib.Path(__file__).parent
CHROMIUM = os.environ.get("CHROMIUM_PATH")
ARGS = ["--disable-background-networking", "--disable-sync", "--no-first-run"]


def groesse(svg_text: str) -> tuple[int, int]:
    w = int(re.search(r'width="(\d+)"', svg_text).group(1))
    h = int(re.search(r'height="(\d+)"', svg_text).group(1))
    return w, h


async def main() -> None:
    async with async_playwright() as p:
        kwargs = {"args": ARGS}
        if CHROMIUM:
            kwargs["executable_path"] = CHROMIUM
        browser = await p.chromium.launch(**kwargs)
        for svg in sorted(ORDNER.glob("*.svg")):
            text = svg.read_text(encoding="utf-8")
            w, h = groesse(text)
            page = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await page.set_content(f"<html><body style='margin:0;background:#fff'>{text}</body></html>")
            await page.screenshot(path=str(svg.with_suffix(".png")), clip={"x": 0, "y": 0, "width": w, "height": h})
            await page.close()
            print("gerendert:", svg.with_suffix(".png").name)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
