"""Die sieben DelaTec-Logos.

Jedes Logo liefert Ebenen (pfad, rolle). Rollen:
  "tinte"   – Schwarz auf hellem Grund, Weiß auf dunklem Grund
  "akzent"  – die Akzentfarbe des Logos (bleibt immer gleich)
  "#rrggbb" – feste Farbe
Flächen überlappen nie (alles ist ausgespart), deshalb funktioniert jede Version auch
als Folie/Plot und lässt sich sauber invertieren.
"""
from __future__ import annotations

import math

from typo import (Schrift, aus_d, bogentext, breite, drehen, grenzen, hoehe, kreis, linie, minus,
                  plus, rechteck, ring, schnitt, verschieben, vieleck)

SCHWARZ = "#0B0B0C"
WEISS = "#FFFFFF"
ROT = "#E30613"
ORANGE = "#FF5A00"
ACID = "#C8FF00"
BLAU = "#1F4BFF"

hubot_i = Schrift("hubot-sans-latin-wdth-italic.woff2", wdth=125, wght=900)
hubot_b = Schrift("hubot-sans-latin-wdth-normal.woff2", wdth=125, wght=700)
mona = Schrift("mona-sans-latin-wdth-normal.woff2", wdth=125, wght=600)
mona_b = Schrift("mona-sans-latin-wdth-normal.woff2", wdth=125, wght=800)
mona_i = Schrift("mona-sans-latin-wdth-italic.woff2", wdth=125, wght=700)
hubot_xb = Schrift("hubot-sans-latin-wdth-normal.woff2", wdth=125, wght=800)
archivo = Schrift("archivo-latin-wdth-normal.woff2", wdth=125, wght=900)
anybody_i = Schrift("anybody-latin-wdth-italic.woff2", wdth=150, wght=900)
michroma = Schrift("michroma-latin-400-normal.woff2")

CLAIM = "FAHRZEUGOPTIK & SERVICE"


# ------------------------------------------------------------------ Hilfen

def halbebene(ax, ay, bx, by, oben=True, gross=5000):
    """Alles oberhalb (bzw. unterhalb) der Geraden durch A und B."""
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    p0 = (ax - ux * gross, ay - uy * gross)
    p1 = (bx + ux * gross, by + uy * gross)
    s = -gross if oben else gross
    return vieleck(p0, p1, (p1[0], p1[1] + s), (p0[0], p0[1] + s))


def schlitz(ax, ay, bx, by, staerke, gross=5000):
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    return linie(ax - ux * gross, ay - uy * gross, bx + ux * gross, by + uy * gross, staerke)


def ausgerichtet(p, x=0.0, y=0.0):
    """Tintenkasten nach (x, y) schieben."""
    x0, y0, _, _ = grenzen(p)
    return verschieben(p, x - x0, y - y0)


def nach_x(p, x=0.0, y=0.0):
    """Nur waagerecht an die Tintenkante schieben – die Versalhöhe aus dem Satz bleibt
    maßgeblich (sonst rutschen Wörter mit Überhang wie C oder O nach unten)."""
    return verschieben(p, x - grenzen(p)[0], y)


def aussenkontur(p):
    """Nur die äußerste Kontur (Löcher gefüllt)."""
    import pathops
    beste, flaeche = None, -1
    for kontur in p.contours:
        q = pathops.Path()
        kontur.draw(q.getPen())
        a = abs(q.area)
        if a > flaeche:
            beste, flaeche = q, a
    return beste


def loecher(p):
    import pathops
    konturen = []
    for kontur in p.contours:
        q = pathops.Path()
        kontur.draw(q.getPen())
        konturen.append(q)
    konturen.sort(key=lambda q: -abs(q.area))
    return konturen[1:]


def claim_satz(schrift, soll_breite, kappe, text=CLAIM):
    """Claim in fester Versalhöhe; die Sperrung wird so gewählt, dass er genau
    `soll_breite` breit wird. So bleiben die Proportionen jedes Logos gleich,
    egal wie lang der Claim ist."""
    if breite(schrift.satz(text, kappe)) > soll_breite:
        # zu lang selbst ohne Sperrung: dann kleiner setzen
        kappe *= soll_breite / breite(schrift.satz(text, kappe))
        return schrift.satz(text, kappe)
    lo, hi = 0.0, 3.0
    for _ in range(40):
        mitte = (lo + hi) / 2
        if breite(schrift.satz(text, kappe, sperrung=mitte)) < soll_breite:
            lo = mitte
        else:
            hi = mitte
    return schrift.satz(text, kappe, sperrung=(lo + hi) / 2)


# ================================================================== 01 SCHNITT
# Weiterentwicklung des ersten Entwurfs: kursives, schweres D mit messerscharfem
# Schnitt – oben das frisch lackierte Rot. Wortmarke breit, kursiv, schwarz.

def zeichen_01(H=100.0):
    D = hubot_i.zeichen("D", H)
    x0, y0, x1, y1 = grenzen(D)
    ax, ay, bx, by = x0, y0 + 0.68 * H, x1, y0 + 0.10 * H
    spalt = schlitz(ax, ay, bx, by, 0.07 * H)
    oben = halbebene(ax, ay, bx, by, oben=True)
    rot = minus(schnitt(D, oben), spalt)
    rest = minus(minus(D, oben), spalt)
    return [(rot, "akzent"), (rest, "tinte")]


def logo_01(claim=True):
    H = 100.0
    zeichen = zeichen_01(H)
    zx1 = grenzen(plus(*[p for p, _ in zeichen]))[2]
    if not claim:
        # Wortmarke mittig zum Zeichen; der Kursivversatz wandert mit
        k = 0.60 * H
        y = (H - k) / 2
        wort = nach_x(hubot_i.satz("DELATEC", k, sperrung=0.02), zx1 + 0.26 * H - y * math.tan(math.radians(12)), y)
        return zeichen + [(wort, "tinte")]
    wort = nach_x(hubot_i.satz("DELATEC", 0.64 * H, sperrung=0.02), zx1 + 0.26 * H)
    wx0, _, wx1, _ = grenzen(wort)
    claim = claim_satz(mona_i, (wx1 - wx0) * 0.965, 0.176 * H)
    claim = ausgerichtet(claim, wx0, H - hoehe(claim))
    return zeichen + [(wort, "tinte"), (claim, "tinte")]


# ================================================================== 02 PLAKETTE
# Wie die Plakette auf einem handgebauten Motor: ein Schild, das für die Arbeit bürgt.

def fase_rechteck(x, y, b, h, f):
    return vieleck((x + f, y), (x + b - f, y), (x + b, y + f), (x + b, y + h - f),
                   (x + b - f, y + h), (x + f, y + h), (x, y + h - f), (x, y + f))


def logo_02(wortschrift=None, kappe=38.0, sperrung=0.16):
    wortschrift = wortschrift or hubot_xb
    B, H, f = 420.0, 132.0, 20.0
    schild = fase_rechteck(0, 0, B, H, f)
    e, s = 8.0, 2.6
    k = 0.4142  # Fase schrumpft beim Einrücken um e·(√2−1)
    rahmen = minus(fase_rechteck(e, e, B - 2 * e, H - 2 * e, f - e * k),
                   fase_rechteck(e + s, e + s, B - 2 * (e + s), H - 2 * (e + s), f - (e + s) * k))
    innen = e + s + 3.2
    teil = 0.655 * H
    band = schnitt(fase_rechteck(innen, innen, B - 2 * innen, H - 2 * innen, f - innen * k),
                   rechteck(0, teil + 1.8, B, H))
    wort = wortschrift.satz("DELATEC", kappe, sperrung=sperrung)
    wort = nach_x(wort, (B - breite(wort)) / 2, (teil - kappe) / 2 + 3.0)
    bo, bu = grenzen(band)[1], grenzen(band)[3]
    claim = claim_satz(mona_b, 300.0, 10.5)
    claim = ausgerichtet(claim, (B - breite(claim)) / 2, (bo + bu) / 2 - hoehe(claim) / 2)
    fuge = rechteck(innen - 3.2, teil - 1.8, B - 2 * (innen - 3.2), 3.6)
    platte = minus(schild, rahmen, fuge, band, wort)
    return [(platte, "tinte"), (minus(band, claim), "akzent")]


# ================================================================== 03 SIEGEL
# Ein Gütesiegel: rund, dicht, schwer. Oben der Name, unten das Versprechen.

def logo_03():
    R = 100.0
    cx = cy = R
    scheibe = kreis(cx, cy, R)
    rand = ring(cx, cy, 94.6, 92.9)
    trenn = ring(cx, cy, 61.4, 59.7)
    rm = 76.5
    k_oben, k_unten, s_oben, s_unten = 18.5, 9.8, 0.30, 0.10
    oben = bogentext(mona_b, "DELATEC", k_oben, cx, cy, rm, 0, unten=False, sperrung=s_oben)
    unten = bogentext(mona_b, CLAIM, k_unten, cx, cy, rm, 180, unten=True, sperrung=s_unten)
    # Rauten genau in die Mitte der Lücken zwischen oberer und unterer Zeile
    _, b_oben = mona_b.glyphen("DELATEC", k_oben, s_oben)
    _, b_unten = mona_b.glyphen(CLAIM, k_unten, s_unten)
    ende_oben = math.degrees(b_oben / 2 / rm)
    start_unten = 180 - math.degrees(b_unten / 2 / rm)
    w = (ende_oben + start_unten) / 2
    rauten = plus(*[drehen(rechteck(cx + rm * math.sin(math.radians(g)) - 3.8,
                                    cy - rm * math.cos(math.radians(g)) - 3.8, 7.6, 7.6),
                           45 + g, cx + rm * math.sin(math.radians(g)), cy - rm * math.cos(math.radians(g)))
                    for g in (w, -w)])
    teile = zeichen_01(68)
    alle = plus(*[p for p, _ in teile])
    x0, y0, x1, y1 = grenzen(alle)
    dx, dy = cx - (x0 + x1) / 2 - 1.5, cy - (y0 + y1) / 2
    d_rot, d_rest = [verschieben(p, dx, dy) for p, _ in teile]
    flaeche = minus(scheibe, rand, trenn, oben, unten, rauten, d_rot, d_rest)
    return [(flaeche, "tinte"), (plus(rauten, d_rot), "akzent")]


# ================================================================== 04 MITTE
# Reine Wortmarke. Das A steht genau in der Mitte von DELATEC – als rotes Λ ohne
# Querstrich: ein Pfeil nach oben. Genau das passiert beim Ausbeulen.

def lambda_aus_a(schrift, kappe):
    """Das A ohne Querstrich, sauber neu aufgebaut.

    Außenkanten und Kopf kommen aus dem A der Schrift, die Innenkanten laufen als
    gerade Linien von der Spitze der Punze bis auf die Grundlinie. (Die Schrift
    knickt die Innenkante unter dem Querstrich minimal – das gäbe Stufen.)
    """
    A = schrift.zeichen("A", kappe)
    aussen = _punkte(aussenkontur(A))
    punze = _punkte(loecher(A)[0])
    unten = sorted(p for p in aussen if abs(p[1] - kappe) < 0.5)
    oben = sorted(p for p in aussen if abs(p[1]) < 0.5)
    fuss_l, fuss_r = unten[0], unten[-1]
    kopf_l, kopf_r = oben[0], oben[-1]
    pymin, pymax = min(p[1] for p in punze), max(p[1] for p in punze)
    pt = sorted(p for p in punze if abs(p[1] - pymin) < 0.5)
    pb = sorted(p for p in punze if abs(p[1] - pymax) < 0.5)
    tl, tr, bl, br = pt[0], pt[-1], pb[0], pb[-1]

    def auf_grundlinie(a, b):
        t = (kappe - a[1]) / (b[1] - a[1])
        return (a[0] + (b[0] - a[0]) * t, kappe)
    return vieleck(fuss_l, kopf_l, kopf_r, fuss_r, auf_grundlinie(tr, br), tr, tl, auf_grundlinie(tl, bl))


def _punkte(p):
    pts = []
    for _, args in p.segments:
        pts.extend(args)
    return pts


def wortmarke_04(K=100.0):
    links = nach_x(archivo.satz("DEL", K, sperrung=0.04), 0)
    lam = nach_x(lambda_aus_a(archivo, K), grenzen(links)[2] + 0.09 * K)
    rechts = nach_x(archivo.satz("TEC", K, sperrung=0.04), grenzen(lam)[2] + 0.09 * K)
    return plus(links, rechts), lam


def logo_04():
    K = 100.0
    wort, lam = wortmarke_04(K)
    gb = grenzen(wort)[2]
    claim = claim_satz(mona, gb, 0.293 * K)
    claim = ausgerichtet(claim, 0, K + 0.26 * K)
    return [(wort, "tinte"), (lam, "akzent"), (claim, "tinte")]


# ================================================================== 05 VELOCITY
# Schwarz + Acid-Grün. Extrem breit, extrem schnell – wie das Dekor eines Rennwagens.

def logo_05():
    K = 100.0
    wort = nach_x(anybody_i.satz("DELATEC", K, sperrung=0.0), 0)
    x0, y0, x1, y1 = grenzen(wort)
    t = math.tan(math.radians(10))
    bh = 0.34 * K
    top = K + 0.13 * K
    balken = vieleck((x0 + t * bh, top), (x1, top), (x1 - t * bh, top + bh), (x0, top + bh))
    claim = claim_satz(mona_i, (x1 - x0) * 0.78, 0.2735 * K)
    cx0, cy0, cx1, cy1 = grenzen(claim)
    claim = verschieben(claim, (x0 + x1) / 2 - (cx0 + cx1) / 2, top + bh / 2 - (cy0 + cy1) / 2)
    return [(wort, "tinte"), (minus(balken, claim), "akzent"), (claim, SCHWARZ)]


# ================================================================== 06 T-NUT
# Schwarz + Signal-Orange. Ein massives D mit eingefrästem T – DelaTec als Monogramm.
# Die T-Nut ist das Präzisionsprofil aus dem Maschinenbau.

def zeichen_06(H=100.0):
    ws = 0.42 * H
    D = aus_d(f"M0 0H{ws}A{H / 2} {H / 2} 0 0 1 {ws} {H}H0Z")
    q0, q1 = 0.18 * H, 0.40 * H
    qx0, qx1 = 0.18 * H, 0.64 * H
    sx0, sx1 = 0.30 * H, 0.52 * H
    nut = plus(rechteck(qx0, q0, qx1 - qx0, q1 - q0), rechteck(sx0, q1 - 1, sx1 - sx0, H - q1 + 10))
    g = 0.045 * H
    T = plus(rechteck(qx0 + g, q0 + g, qx1 - qx0 - 2 * g, q1 - q0 - 2 * g),
             rechteck(sx0 + g, q1 - g - 1, sx1 - sx0 - 2 * g, H - q1 + g + 1))
    return [(minus(D, nut), "tinte"), (T, "akzent")]


def logo_06(claim=True):
    H = 100.0
    zeichen = zeichen_06(H)
    if not claim:
        k = 0.42 * H
        wort = nach_x(hubot_b.satz("DELATEC", k, sperrung=0.22), 0.92 * H + 0.28 * H, (H - k) / 2)
        return zeichen + [(wort, "tinte")]
    wort = hubot_b.satz("DELATEC", 0.40 * H, sperrung=0.22)
    wort = nach_x(wort, 0.92 * H + 0.28 * H, 0.12 * H)
    wx0, _, wx1, _ = grenzen(wort)
    claim = claim_satz(mona, wx1 - wx0, 0.116 * H)
    claim = ausgerichtet(claim, wx0, 0.88 * H - hoehe(claim))
    return zeichen + [(wort, "tinte"), (claim, "tinte")]


# ================================================================== 07 REFLEX
# Schwarz + Electric-Blau. Ausbeuler lesen Dellen an den Linien der Reflektorlampe.
# Hier spiegeln sich diese Linien auf einem gewölbten D: oben und unten gestaucht,
# in der Mitte breit – wie auf einem polierten Kotflügel.

def zeichen_07(H=100.0, n=11, anteil=0.58):
    B = 0.92 * H
    r = 0.5 * H
    D = aus_d(f"M0 0H{B - r}A{r} {r} 0 0 1 {B - r} {H}H0Z")
    loch = aus_d(f"M{0.25 * H} {0.25 * H}H{B - r}A{0.25 * H} {0.25 * H} 0 0 1 {B - r} {0.75 * H}H{0.25 * H}Z")
    D = minus(D, loch)
    grenzen_y = [H / 2 + H / 2 * math.sin((-1 + 2 * i / n) * math.pi / 2) for i in range(n + 1)]
    linien = []
    for a, b in zip(grenzen_y, grenzen_y[1:]):
        dick = (b - a) * anteil
        m = (a + b) / 2
        linien.append(schnitt(D, rechteck(-10, m - dick / 2, B + 20, dick)))
    return [(plus(*linien), "akzent")]


def logo_07(claim=True):
    H = 100.0
    zeichen = zeichen_07(H)
    if not claim:
        k = 0.38 * H
        wort = nach_x(michroma.satz("DELATEC", k, sperrung=0.18), 0.92 * H + 0.30 * H, (H - k) / 2)
        return zeichen + [(wort, "tinte")]
    wort = michroma.satz("DELATEC", 0.36 * H, sperrung=0.18)
    wort = nach_x(wort, 0.92 * H + 0.30 * H, 0.16 * H)
    wx0, _, wx1, _ = grenzen(wort)
    claim = claim_satz(mona, wx1 - wx0, 0.1095 * H)
    claim = ausgerichtet(claim, wx0, 0.84 * H - hoehe(claim))
    return zeichen + [(wort, "tinte"), (claim, "tinte")]


# ================================================================== Bildzeichen
# Kompakte Varianten für Profilbild, App-Icon, Favicon, Stempel.

def zeichen_02():
    B = H = 200.0
    f = 34.0
    k = 0.4142
    schild = fase_rechteck(0, 0, B, H, f)
    e, s = 10.0, 3.2
    rahmen = minus(fase_rechteck(e, e, B - 2 * e, H - 2 * e, f - e * k),
                   fase_rechteck(e + s, e + s, B - 2 * (e + s), H - 2 * (e + s), f - (e + s) * k))
    innen = e + s + 4.0
    teil = 0.68 * H
    band = schnitt(fase_rechteck(innen, innen, B - 2 * innen, H - 2 * innen, f - innen * k),
                   rechteck(0, teil + 2.2, B, H))
    D = hubot_xb.zeichen("D", 80)
    D = ausgerichtet(D, (B - breite(D)) / 2, innen + (teil - 2.2 - innen - 80) / 2)
    bo, bu = grenzen(band)[1], grenzen(band)[3]
    wort = hubot_xb.satz("DELATEC", 14.0, sperrung=0.14)
    wort = ausgerichtet(wort, (B - breite(wort)) / 2, (bo + bu) / 2 - hoehe(wort) / 2 - 1.5)
    fuge = rechteck(innen - 4.0, teil - 2.2, B - 2 * (innen - 4.0), 4.4)
    platte = minus(schild, rahmen, fuge, band, D)
    return [(platte, "tinte"), (minus(band, wort), "akzent")]


def zeichen_04():
    return [(lambda_aus_a(archivo, 100.0), "akzent")]


def zeichen_05():
    K = 100.0
    D = anybody_i.zeichen("D", K)
    x0, _, x1, _ = grenzen(D)
    t = math.tan(math.radians(10))
    bh, top = 0.30 * K, K + 0.12 * K
    balken = vieleck((x0 + t * bh, top), (x1, top), (x1 - t * bh, top + bh), (x0, top + bh))
    return [(D, "tinte"), (balken, "akzent")]


def profil_04():
    wort, lam = wortmarke_04(100.0)
    return [(wort, "tinte"), (lam, "akzent")]


def profil_05():
    ebenen = logo_05()
    wort, balken, claim = (p for p, _ in ebenen)
    return [(wort, "tinte"), (plus(balken, claim), "akzent")]


def zeichen_07_klein():
    return zeichen_07(100.0, n=9, anteil=0.62)


# name: (logo, akzent, bildzeichen, profilbild)
# profilbild: (quelle, hintergrund, anteil, dunkel)  – anteil = Breite oder Höhe relativ zum Quadrat
LOGOS = {
    "01-schnitt": (logo_01, ROT, zeichen_01, ("zeichen", SCHWARZ, 0.50, True)),
    "02-plakette": (logo_02, ROT, zeichen_02, ("zeichen", SCHWARZ, 0.62, True)),
    "03-siegel": (logo_03, ROT, logo_03, ("logo", "siegel", 1.0, False)),
    "04-mitte": (logo_04, ROT, zeichen_04, (profil_04, SCHWARZ, 0.80, True)),
    "05-velocity": (logo_05, ACID, zeichen_05, (profil_05, SCHWARZ, 0.80, True)),
    "06-t-nut": (logo_06, ORANGE, zeichen_06, ("zeichen", SCHWARZ, 0.50, True)),
    "07-reflex": (logo_07, BLAU, zeichen_07_klein, ("zeichen", SCHWARZ, 0.52, True)),
}

# Versionen ohne Claim – für kleine Formate (Visitenkarte, Stempel, Fahrzeugheck)
OHNE_CLAIM = {
    "01-schnitt": lambda: logo_01(claim=False),
    "04-mitte": profil_04,
    "05-velocity": profil_05,
    "06-t-nut": lambda: logo_06(claim=False),
    "07-reflex": lambda: logo_07(claim=False),
}

TITEL = {
    "01-schnitt": ("Schnitt", "Das kursive D mit messerscharfem Schnitt: oben das frisch lackierte Rot. "
                   "Die Weiterentwicklung des ersten Entwurfs – schneller, schwerer, schärfer."),
    "02-plakette": ("Plakette", "Wie die Plakette auf einem handgebauten Motor: ein Schild, das für die "
                    "Arbeit bürgt. Gefaste Ecken, Rahmenlinie, rotes Band."),
    "03-siegel": ("Siegel", "Ein Gütesiegel – rund, dicht, schwer. Oben der Name, unten das Versprechen, "
                  "in der Mitte das geschnittene D. Passt exakt ins runde Profilbild."),
    "04-mitte": ("Mitte", "Das A steht genau in der Mitte von DELATEC – als rotes A ohne Querstrich: "
                 "ein Pfeil nach oben. Genau das passiert beim Ausbeulen."),
    "05-velocity": ("Velocity", "Schwarz + Acid-Grün. Extrem breit, extrem schnell – wie das Dekor eines "
                    "Rennwagens. Der Balken trägt das Leistungsversprechen."),
    "06-t-nut": ("T-Nut", "Schwarz + Signal-Orange. Ein massives D mit eingefrästem T – DelaTec als "
                 "Monogramm. Die T-Nut ist das Präzisionsprofil aus dem Maschinenbau."),
    "07-reflex": ("Reflex", "Schwarz + Electric-Blau. Dellen erkennt man an den Linien der Reflektorlampe. "
                  "Hier spiegeln sie sich auf einem gewölbten D – wie auf poliertem Lack."),
}
