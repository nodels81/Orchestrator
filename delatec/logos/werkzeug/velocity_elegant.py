"""Velocity, elegant: sechs Verfeinerungen von Logo 05.

Gleiche DNA – extrem breit, kursiv, Schwarz + Acid-Grün – aber leichter, luftiger
und mit dem Grün nur noch als präzisem Akzent.
"""
import math

from konzepte import ACID, CLAIM, SCHWARZ, claim_satz, nach_x
from typo import Schrift, breite, grenzen, hoehe, minus, plus, rechteck, verschieben, vieleck

NEIGUNG = math.tan(math.radians(10))   # Kursivwinkel von Anybody


def anybody(gewicht):
    return Schrift("anybody-latin-wdth-italic.woff2", wdth=150, wght=gewicht)


mona_il = Schrift("mona-sans-latin-wdth-italic.woff2", wdth=125, wght=450)
mona_im = Schrift("mona-sans-latin-wdth-italic.woff2", wdth=125, wght=600)


def schraeg(x0, y0, x1, h):
    """Parallelogramm in Kursivlage: Oberkante von x0 bis x1 bei y0, Höhe h."""
    t = NEIGUNG * h
    return vieleck((x0 + t, y0), (x1 + t, y0), (x1, y0 + h), (x0, y0 + h))


def claim_fein(schrift, soll_breite, sperrung=0.42):
    """Feiner Claim: feste, großzügige Sperrung – die Größe folgt aus der Breite."""
    probe = breite(schrift.satz(CLAIM, 10, sperrung=sperrung))
    return schrift.satz(CLAIM, 10 * soll_breite / probe, sperrung=sperrung)


def wort(gewicht, K=100.0, sperrung=0.04):
    return nach_x(anybody(gewicht).satz("DELATEC", K, sperrung=sperrung), 0)


# 05a  FEIN – leichtere Wortmarke, darunter eine Acid-Haarlinie, Claim fein gesperrt
def v_fein():
    K = 100.0
    w = wort(560, K, 0.06)
    x0, _, x1, _ = grenzen(w)
    linie = schraeg(x0 + 0.02 * K, K + 0.20 * K, x1 - NEIGUNG * 0.05 * K, 0.05 * K)
    claim = claim_fein(mona_il, (x1 - x0) * 0.62)
    claim = nach_x(claim, x1 - breite(claim) - 0.02 * K, K + 0.40 * K)
    return [(w, "tinte"), (linie, "akzent"), (claim, "tinte")]


# 05b  KLINGE – ein schmaler Acid-Keil vor dem Namen, wie ein Tempostrich
def v_klinge():
    K = 100.0
    w = wort(700, K, 0.05)
    w = verschieben(w, 0.78 * K, 0)
    x0, _, x1, _ = grenzen(w)
    keil = schraeg(0, 0, 0.34 * K, K)
    claim = claim_fein(mona_il, (x1 - x0) * 0.60)
    claim = nach_x(claim, x1 - breite(claim) - NEIGUNG * 0.3 * K, K + 0.30 * K)
    return [(keil, "akzent"), (w, "tinte"), (claim, "tinte")]


# 05c  PUNKT – der Name endet in einem Acid-Parallelogramm: auf den Punkt
def v_punkt():
    K = 100.0
    w = wort(640, K, 0.05)
    x0, _, x1, _ = grenzen(w)
    punkt = schraeg(x1 + 0.10 * K, K - 0.20 * K, x1 + 0.10 * K + 0.34 * K, 0.20 * K)
    claim = claim_fein(mona_il, (grenzen(punkt)[2] - x0) * 0.60)
    claim = nach_x(claim, x0, K + 0.30 * K)
    return [(w, "tinte"), (punkt, "akzent"), (claim, "tinte")]


# 05d  BAND – der Balken des Originals, aber schlank und nur unter der zweiten Hälfte
def v_band():
    K = 100.0
    w = wort(760, K, 0.03)
    x0, _, x1, _ = grenzen(w)
    bh = 0.22 * K
    top = K + 0.14 * K
    start = x0 + (x1 - x0) * 0.30
    band = schraeg(start, top, x1 - NEIGUNG * bh, bh)
    claim = claim_fein(mona_im, (x1 - start) * 0.70)
    bx0, by0, bx1, by1 = grenzen(band)
    cx0, cy0, cx1, cy1 = grenzen(claim)
    claim = verschieben(claim, (bx0 + bx1) / 2 - (cx0 + cx1) / 2, (by0 + by1) / 2 - (cy0 + cy1) / 2)
    return [(w, "tinte"), (minus(band, claim), "akzent"), (claim, SCHWARZ)]


# 05e  KONTRAST – DELA schwer, TEC leicht; die Acid-Linie liegt unter TEC
def v_kontrast():
    K = 100.0
    dela = nach_x(anybody(880).satz("DELA", K, sperrung=0.03), 0)
    tec = nach_x(anybody(260).satz("TEC", K, sperrung=0.06), grenzen(dela)[2] + 0.08 * K)
    tx0, _, tx1, _ = grenzen(tec)
    linie = schraeg(tx0 - NEIGUNG * 0.05 * K + 0.02 * K, K + 0.18 * K, tx1 - NEIGUNG * 0.05 * K, 0.05 * K)
    claim = claim_fein(mona_il, (tx1 - grenzen(dela)[0]) * 0.55)
    claim = nach_x(claim, tx1 - breite(claim) - NEIGUNG * 0.3 * K, K + 0.36 * K)
    return [(plus(dela, tec), "tinte"), (linie, "akzent"), (claim, "tinte")]


# 05f  RAHMEN – leichte Wortmarke zwischen zwei Acid-Haarlinien, wie ein Zierstreifen
def v_rahmen():
    K = 100.0
    y_w = 0.30 * K                       # Oberkante der Wortmarke
    w = verschieben(wort(480, K, 0.08), 0, y_w)
    x0, _, x1, _ = grenzen(w)            # x0 = linke Kante auf der Grundlinie
    grund = y_w + K
    h = 0.04 * K

    def linie(y):
        # an Höhe y liegt die Kursivkante um NEIGUNG·(grund−y) weiter rechts
        dx = NEIGUNG * (grund - y - h)
        return schraeg(x0 + dx, y, x1 - NEIGUNG * K + dx, h)
    oben, unten = linie(0), linie(grund + 0.22 * K)
    ux0, _, ux1, _ = grenzen(unten)
    claim = claim_fein(mona_il, (ux1 - ux0) * 0.70)
    claim = nach_x(claim, (ux0 + ux1) / 2 - breite(claim) / 2, grund + 0.44 * K)
    return [(oben, "akzent"), (w, "tinte"), (unten, "akzent"), (claim, "tinte")]


VARIANTEN = {
    "05a-fein": ("Fein", v_fein),
    "05b-klinge": ("Klinge", v_klinge),
    "05c-punkt": ("Punkt", v_punkt),
    "05d-band": ("Band", v_band),
    "05e-kontrast": ("Kontrast", v_kontrast),
    "05f-rahmen": ("Rahmen", v_rahmen),
}


def main():
    """Exportiert alle Varianten (elegant + fiffig) nach ../05-velocity-elegant/ plus Übersicht."""
    from velocity_fiffig import VARIANTEN as FIFFIG
    alle = {**VARIANTEN, **FIFFIG}
    import os
    import subprocess
    import bauen
    from bauen import DUNKEL, HELL, KARTE, datei_svg, einfaerben, einpassen, hubot_b, mona, tafel_svg, text, ziffern
    ziel = bauen.ZIEL / "05-velocity-elegant"
    ziel.mkdir(exist_ok=True)
    for name, (titel, fn) in alle.items():
        for dunkel, zusatz in ((False, ""), (True, "-negativ")):
            datei = ziel / f"delatec-{name}{zusatz}.svg"
            datei_svg(datei, einfaerben(fn(), ACID, dunkel))
            bauen.rendern(datei, datei.with_suffix(".png"), 2400)
    # Übersicht
    B, kopf, zeile = 1800.0, 250.0, 300.0
    H = kopf + zeile * len(alle) + 60
    rechtecke, pfade = [(0, 0, B, H, KARTE, 0)], []
    pfade.append(text(ziffern, "05", 50, 80, 70, SCHWARZ))
    pfade.append(text(hubot_b, "VELOCITY  ·  ELEGANT", 22, 230, 84, SCHWARZ, sperrung=0.18))
    pfade.append(text(mona, "NEUN VERFEINERUNGEN  ·  SCHWARZ + ACID-GRÜN  ·  FAHRZEUGOPTIK & SERVICE",
                      13, 80, 160, "#55555A", sperrung=0.26))
    y = kopf
    for name, (titel, fn) in alle.items():
        pfade.append(text(ziffern, name[:3].upper(), 30, 80, y + 40, SCHWARZ))
        pfade.append(text(hubot_b, titel.upper(), 16, 80, y + 92, SCHWARZ, sperrung=0.18))
        rechtecke.append((330, y + 15, 700, zeile - 30, HELL, 0))
        rechtecke.append((1050, y + 15, 670, zeile - 30, DUNKEL, 0))
        pfade += einpassen(einfaerben(fn(), ACID, False), 385, y + 80, 590, zeile - 160)
        pfade += einpassen(einfaerben(fn(), ACID, True), 1100, y + 80, 570, zeile - 160)
        y += zeile
    (ziel / "uebersicht.svg").write_text(tafel_svg(B, H, rechtecke, pfade))
    bauen.rendern(ziel / "uebersicht.svg", ziel / "uebersicht.png", 1800)
    umgebung = dict(os.environ)
    umgebung.setdefault("NODE_PATH", subprocess.run(["npm", "root", "-g"], capture_output=True,
                                                    text=True).stdout.strip())
    subprocess.run(["node", str(bauen.HIER / "render.js"), *bauen.renderauftraege], check=True, env=umgebung)
    (ziel / "uebersicht.svg").unlink()
    print(f"{len(bauen.renderauftraege)} Dateien gerendert.")


if __name__ == "__main__":
    main()
