"""Baut alle Dateien der DelaTec-Logos.

    python bauen.py

Je Logo (Ordner NN-name/):
  delatec-NN-name.svg / .png            Hauptlogo für hellen Grund
  delatec-NN-name-negativ.svg / .png    für dunklen Grund
  delatec-NN-name-ohne-claim(-negativ)  kleine Formate (nicht bei Plakette/Siegel)
  delatec-NN-zeichen.svg / .png         Bildzeichen (Favicon, Stempel, Stick)
  delatec-NN-zeichen-negativ.svg / .png
  delatec-NN-instagram.svg / .png       Profilbild 1080 × 1080
  delatec-NN-praesentation.png          Präsentationskarte
Dazu uebersicht.png mit allen sieben.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from konzepte import LOGOS, OHNE_CLAIM, SCHWARZ, TITEL, WEISS
from typo import Schrift, breite, d, grenzen, kreis, matrix, plus, svg

HIER = Path(__file__).resolve().parent
ZIEL = HIER.parent
HELL, DUNKEL, KARTE = "#F2F2F0", SCHWARZ, "#FFFFFF"

hubot = Schrift("hubot-sans-latin-wdth-normal.woff2", wdth=125, wght=900)
ziffern = Schrift("archivo-latin-wdth-normal.woff2", wdth=125, wght=900)
hubot_b = Schrift("hubot-sans-latin-wdth-normal.woff2", wdth=125, wght=750)
mona = Schrift("mona-sans-latin-wdth-normal.woff2", wdth=125, wght=600)
inter = Schrift("inter-latin-wght-normal.woff2", wght=420)

renderauftraege: list[str] = []


def einfaerben(ebenen, akzent, dunkel):
    tinte = WEISS if dunkel else SCHWARZ
    return [(p, tinte if r == "tinte" else akzent if r == "akzent" else r) for p, r in ebenen]


def einpassen(ebenen, x, y, b, h, mittig=True):
    """Ebenen in das Feld (x, y, b, h) einpassen – proportional, zentriert."""
    x0, y0, x1, y1 = grenzen(plus(*[p for p, _ in ebenen]))
    s = min(b / (x1 - x0), h / (y1 - y0))
    ox = x + (b - (x1 - x0) * s) / 2 if mittig else x
    oy = y + (h - (y1 - y0) * s) / 2
    return [(matrix(p, a=s, d=s, e=ox - x0 * s, f=oy - y0 * s), f) for p, f in ebenen]


def datei_svg(pfad: Path, ebenen, hintergrund=None, rand=0.02, hoehe_px=400.0):
    """Knappes SVG mit kleinem Rand; Höhe auf hoehe_px normiert."""
    x0, y0, x1, y1 = grenzen(plus(*[p for p, _ in ebenen]))
    s = hoehe_px / (y1 - y0)
    r = rand * hoehe_px
    b, h = (x1 - x0) * s + 2 * r, hoehe_px + 2 * r
    ebenen = [(matrix(p, a=s, d=s, e=r - x0 * s, f=r - y0 * s), f) for p, f in ebenen]
    pfad.write_text(svg(round(b, 2), round(h, 2), ebenen, hintergrund))
    return b, h


def rendern(svg_pfad: Path, png_pfad: Path, breite_px: int):
    renderauftraege.append(f"{svg_pfad}:{png_pfad}:{breite_px}")


# ------------------------------------------------------------------ Profilbild

def profil_quelle(name):
    logo_fn, _, zeichen_fn, (quelle, *_rest) = LOGOS[name]
    return {"zeichen": zeichen_fn, "logo": logo_fn}.get(quelle, quelle)


def instagram(name, pfad: Path):
    logo_fn, akzent, zeichen_fn, (quelle, hintergrund, anteil, dunkel) = LOGOS[name]
    ebenen = profil_quelle(name)()
    S = 1080.0
    if hintergrund == "siegel":
        # Siegel füllt den Kreis exakt; darunter eine weiße Scheibe für die Aussparungen
        teile = einpassen(einfaerben(ebenen, akzent, False), 0, 0, S, S)
        unterlage = [(kreis(S / 2, S / 2, S / 2 * 0.965), WEISS)]
        inhalt = unterlage + teile
        hg = SCHWARZ
    else:
        x0, y0, x1, y1 = grenzen(plus(*[p for p, _ in ebenen]))
        m = anteil * S
        b, h = (m, m * (y1 - y0) / (x1 - x0)) if x1 - x0 >= y1 - y0 else (m * (x1 - x0) / (y1 - y0), m)
        inhalt = einpassen(einfaerben(ebenen, akzent, dunkel), (S - b) / 2, (S - h) / 2, b, h)
        hg = hintergrund
    teile = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S:g} {S:g}" width="{S:g}" height="{S:g}">',
             f'  <title>DelaTec</title>', f'  <rect width="{S:g}" height="{S:g}" fill="{hg}"/>']
    teile += [f'  <path fill="{f}" d="{d(p)}"/>' for p, f in inhalt]
    teile.append("</svg>\n")
    pfad.write_text("\n".join(teile))


# ------------------------------------------------------------------ Tafeln

def text(schrift, t, kappe, x, y, farbe, sperrung=0.0):
    p = schrift.satz(t, kappe, sperrung=sperrung)
    return (matrix(p, e=x - grenzen(p)[0] if t.strip() else x, f=y), farbe)


def umbrechen(schrift, t, kappe, max_b):
    zeilen, aktuell = [], ""
    for wort in t.split(" "):
        probe = (aktuell + " " + wort).strip()
        if aktuell and breite(schrift.satz(probe, kappe)) > max_b:
            zeilen.append(aktuell)
            aktuell = wort
        else:
            aktuell = probe
    zeilen.append(aktuell)
    return zeilen


def tafel_svg(b, h, rechtecke, pfade):
    teile = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {b:g} {h:g}" width="{b:g}" height="{h:g}">']
    teile += [f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{hh:g}" rx="{r:g}" fill="{f}"/>'
              for x, y, w, hh, f, r in rechtecke]
    teile += [f'<path fill="{f}" d="{d(p)}"/>' for p, f in pfade]
    teile.append("</svg>\n")
    return "\n".join(teile)


def kreis_ausschnitt(name, cx, cy, r):
    """Profilbild als Kreis, wie Instagram es zeigt."""
    logo_fn, akzent, zeichen_fn, (quelle, hintergrund, anteil, dunkel) = LOGOS[name]
    ebenen = profil_quelle(name)()
    if hintergrund == "siegel":
        return [(kreis(cx, cy, r * 0.965), WEISS)] + einpassen(einfaerben(ebenen, akzent, False),
                                                                cx - r, cy - r, 2 * r, 2 * r), SCHWARZ
    x0, y0, x1, y1 = grenzen(plus(*[p for p, _ in ebenen]))
    m = anteil * 2 * r
    bb, hh = (m, m * (y1 - y0) / (x1 - x0)) if x1 - x0 >= y1 - y0 else (m * (x1 - x0) / (y1 - y0), m)
    return einpassen(einfaerben(ebenen, akzent, dunkel), cx - bb / 2, cy - hh / 2, bb, hh), hintergrund


def praesentation(name, pfad: Path):
    logo_fn, akzent, zeichen_fn, _ = LOGOS[name]
    nr, kurz = name.split("-", 1)
    titel, beschreibung = TITEL[name]
    B, H = 1600.0, 1480.0
    rechtecke, pfade = [(0, 0, B, H, KARTE, 0)], []
    # Kopf
    ziffer = text(ziffern, nr, 64, 80, 70, akzent if akzent != "#C8FF00" else SCHWARZ)
    pfade.append(ziffer)
    tx = grenzen(ziffer[0])[2] + 44
    pfade.append(text(hubot_b, titel.upper(), 26, tx, 72, SCHWARZ, sperrung=0.18))
    for i, zeile in enumerate(umbrechen(inter, beschreibung, 15, B - tx - 120)):
        pfade.append(text(inter, zeile, 15, tx, 120 + i * 30, "#3A3A3C"))
    # Hauptfläche hell
    rechtecke.append((0, 230, B, 700, HELL, 0))
    pfade += einpassen(einfaerben(logo_fn(), akzent, False), 180, 330, B - 360, 500)
    # unten: dunkel | Zeichen | Profilbild
    rechtecke.append((0, 930, 800, 550, DUNKEL, 0))
    pfade += einpassen(einfaerben(logo_fn(), akzent, True), 90, 1030, 620, 350)
    rechtecke.append((800, 930, 400, 550, "#E6E6E3", 0))
    pfade += einpassen(einfaerben(zeichen_fn(), akzent, False), 880, 1070, 240, 240)
    rechtecke.append((1200, 930, 400, 550, HELL, 0))
    kreis_teile, hg = kreis_ausschnitt(name, 1400, 1180, 150)
    pfade.append((kreis(1400, 1180, 150), hg))
    pfade += kreis_teile
    for x, t in ((820, "BILDZEICHEN"), (1220, "PROFILBILD")):
        pfade.append(text(mona, t, 11, x, 1440, "#77777A", sperrung=0.3))
    pfade.append(text(mona, "NEGATIV", 11, 20, 1440, "#8A8A8D", sperrung=0.3))
    pfade.append(text(mona, "POSITIV", 11, 20, 250, "#77777A", sperrung=0.3))
    pfad.with_suffix(".svg").write_text(tafel_svg(B, H, rechtecke, pfade))
    rendern(pfad.with_suffix(".svg"), pfad, 1600)


def uebersicht(pfad: Path):
    B = 1800.0
    kopf, zeile = 250.0, 330.0
    H = kopf + zeile * len(LOGOS) + 60
    rechtecke, pfade = [(0, 0, B, H, KARTE, 0)], []
    pfade.append(text(hubot, "DELATEC", 50, 80, 70, SCHWARZ, sperrung=0.02))
    pfade.append(text(mona, "LOGO-ENTWÜRFE  ·  7 KONZEPTE  ·  FAHRZEUGOPTIK & SERVICE", 14, 80, 150,
                      "#55555A", sperrung=0.28))
    y = kopf
    for name, (logo_fn, akzent, _, _) in LOGOS.items():
        nr = name.split("-", 1)[0]
        titel = TITEL[name][0]
        pfade.append(text(ziffern, nr, 40, 80, y + 40, akzent if akzent != "#C8FF00" else SCHWARZ))
        pfade.append(text(hubot_b, titel.upper(), 17, 80, y + 104, SCHWARZ, sperrung=0.18))
        rechtecke.append((330, y + 15, 700, zeile - 30, HELL, 0))
        rechtecke.append((1050, y + 15, 670, zeile - 30, DUNKEL, 0))
        rand = 45 if name == "03-siegel" else 75
        pfade += einpassen(einfaerben(logo_fn(), akzent, False), 390, y + rand, 580, zeile - 2 * rand)
        pfade += einpassen(einfaerben(logo_fn(), akzent, True), 1105, y + rand, 560, zeile - 2 * rand)
        y += zeile
    pfad.with_suffix(".svg").write_text(tafel_svg(B, H, rechtecke, pfade))
    rendern(pfad.with_suffix(".svg"), pfad, 1800)


# ------------------------------------------------------------------ los

def main():
    vorschau = HIER / "vorschau"
    vorschau.mkdir(exist_ok=True)
    for name, (logo_fn, akzent, zeichen_fn, _) in LOGOS.items():
        nr = name.split("-", 1)[0]
        ordner = ZIEL / name
        ordner.mkdir(exist_ok=True)
        basis = f"delatec-{name}"
        for dunkel, zusatz in ((False, ""), (True, "-negativ")):
            b, h = datei_svg(ordner / f"{basis}{zusatz}.svg", einfaerben(logo_fn(), akzent, dunkel))
            rendern(ordner / f"{basis}{zusatz}.svg", ordner / f"{basis}{zusatz}.png", 2400 if b > h else 1600)
            if name in OHNE_CLAIM:
                datei = ordner / f"{basis}-ohne-claim{zusatz}.svg"
                b, h = datei_svg(datei, einfaerben(OHNE_CLAIM[name](), akzent, dunkel))
                rendern(datei, datei.with_suffix(".png"), 2400 if b > h else 1600)
            if zeichen_fn is logo_fn:
                continue  # das Siegel ist selbst schon das Bildzeichen
            b, h = datei_svg(ordner / f"delatec-{nr}-zeichen{zusatz}.svg", einfaerben(zeichen_fn(), akzent, dunkel))
            rendern(ordner / f"delatec-{nr}-zeichen{zusatz}.svg", ordner / f"delatec-{nr}-zeichen{zusatz}.png",
                    round(1024 * b / max(b, h)))
        instagram(name, ordner / f"delatec-{nr}-instagram.svg")
        rendern(ordner / f"delatec-{nr}-instagram.svg", ordner / f"delatec-{nr}-instagram.png", 1080)
        praesentation(name, vorschau / f"delatec-{nr}-praesentation.png")
    uebersicht(ZIEL / "uebersicht.png")
    umgebung = dict(os.environ)
    umgebung.setdefault("NODE_PATH", subprocess.run(["npm", "root", "-g"], capture_output=True,
                                                    text=True).stdout.strip())
    subprocess.run(["node", str(HIER / "render.js"), *renderauftraege], check=True, env=umgebung)
    # Präsentationskarten gehören in den Logo-Ordner, die Zwischen-SVGs nicht
    for name in LOGOS:
        nr = name.split("-", 1)[0]
        (vorschau / f"delatec-{nr}-praesentation.png").replace(ZIEL / name / f"delatec-{nr}-praesentation.png")
    for rest in vorschau.iterdir():
        rest.unlink()
    vorschau.rmdir()
    (ZIEL / "uebersicht.svg").unlink()
    print(f"{len(renderauftraege)} Dateien gerendert.")


if __name__ == "__main__":
    main()
