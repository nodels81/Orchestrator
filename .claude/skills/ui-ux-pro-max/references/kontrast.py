#!/usr/bin/env python3
"""Kontrastverhältnis zweier Farben nach WCAG 2.1 — ohne Abhängigkeiten.

    python3 kontrast.py "#B08D57" "#FFFFFF"
    python3 kontrast.py "#B08D57"            # gegen Weiß und gegen Papier #FAF8F5
"""
import sys

PAPIER = "#FAF8F5"


def _kanal(wert: int) -> float:
    c = wert / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def leuchtdichte(hexfarbe: str) -> float:
    h = hexfarbe.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(z * 2 for z in h)
    if len(h) != 6:
        raise ValueError(f"keine Hex-Farbe: {hexfarbe}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _kanal(r) + 0.7152 * _kanal(g) + 0.0722 * _kanal(b)


def verhaeltnis(vorne: str, hinten: str) -> float:
    a, b = leuchtdichte(vorne), leuchtdichte(hinten)
    hell, dunkel = max(a, b), min(a, b)
    return (hell + 0.05) / (dunkel + 0.05)


def urteil(wert: float) -> str:
    if wert >= 7:
        return "AAA — alles erlaubt"
    if wert >= 4.5:
        return "AA — Fließtext erlaubt"
    if wert >= 3:
        return "nur große Schrift (>=24px / 19px fett), Icons, Rahmen"
    return "DURCHGEFALLEN — nicht für Text"


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    vorne = argv[0]
    hintergruende = argv[1:] or ["#FFFFFF", PAPIER]
    for hinten in hintergruende:
        wert = verhaeltnis(vorne, hinten)
        print(f"{vorne} auf {hinten}: {wert:.2f}:1  —  {urteil(wert)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
