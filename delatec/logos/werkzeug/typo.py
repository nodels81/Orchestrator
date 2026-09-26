"""Vektor-Werkzeug für die DelaTec-Logos.

Setzt Schrift mit HarfBuzz (inkl. Unterschneidung und variabler Achsen) und macht
daraus reine Pfade. Alle Formen laufen durch Skia-PathOps, damit jedes Logo am Ende
aus wenigen, überlappungsfreien Flächen besteht – ohne Schriftart, ohne Masken,
direkt plotter- und folierungstauglich.

Koordinaten: SVG-üblich, y wächst nach unten.
"""
from __future__ import annotations

import io
import math
from functools import lru_cache
from pathlib import Path

import pathops
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

SCHRIFTEN = Path(__file__).parent / "schriften"


# ---------------------------------------------------------------- Pfade

def leer() -> pathops.Path:
    return pathops.Path()


def aus_d(d: str) -> pathops.Path:
    p = pathops.Path()
    parse_path(d, p.getPen())
    return sauber(p)


def sauber(p: pathops.Path) -> pathops.Path:
    """Überlappungen auflösen, Umlaufsinn vereinheitlichen."""
    return pathops.simplify(p, fix_winding=True, clockwise=False)


def plus(*pfade: pathops.Path) -> pathops.Path:
    erg = pathops.Path()
    for p in pfade:
        erg.addPath(p)
    return sauber(erg)


def minus(a: pathops.Path, *b: pathops.Path) -> pathops.Path:
    erg = a
    for p in b:
        erg = pathops.op(erg, p, pathops.PathOp.DIFFERENCE, fix_winding=True, clockwise=False)
    return erg


def schnitt(a: pathops.Path, b: pathops.Path) -> pathops.Path:
    return pathops.op(a, b, pathops.PathOp.INTERSECTION, fix_winding=True, clockwise=False)


def matrix(p: pathops.Path, a=1.0, b=0.0, c=0.0, d=1.0, e=0.0, f=0.0) -> pathops.Path:
    """x' = a·x + c·y + e,  y' = b·x + d·y + f"""
    neu = pathops.Path()
    p.draw(TransformPen(neu.getPen(), (a, b, c, d, e, f)))
    return neu


def verschieben(p, dx=0.0, dy=0.0):
    return matrix(p, e=dx, f=dy)


def skalieren(p, s, sy=None, ox=0.0, oy=0.0):
    sy = s if sy is None else sy
    return matrix(p, a=s, d=sy, e=ox - s * ox, f=oy - sy * oy)


def kursiv(p, grad: float, grundlinie: float):
    """Nach rechts neigen; auf der Grundlinie bleibt alles stehen."""
    t = math.tan(math.radians(grad))
    return matrix(p, c=-t, e=t * grundlinie)


def drehen(p, grad: float, cx=0.0, cy=0.0):
    r = math.radians(grad)
    co, si = math.cos(r), math.sin(r)
    return matrix(p, a=co, b=si, c=-si, d=co,
                  e=cx - co * cx + si * cy, f=cy - si * cx - co * cy)


def spiegeln_x(p, achse=0.0):
    return matrix(p, a=-1, e=2 * achse)


def grenzen(p):
    """(x0, y0, x1, y1)"""
    return p.bounds


def d(p: pathops.Path) -> str:
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    p.draw(pen)
    return pen.getCommands()


# ---------------------------------------------------------------- Grundformen

def rechteck(x, y, b, h, r=0.0):
    if r <= 0:
        return aus_d(f"M{x} {y}H{x + b}V{y + h}H{x}Z")
    r = min(r, b / 2, h / 2)
    k = r * 0.5523
    return aus_d(
        f"M{x + r} {y}H{x + b - r}C{x + b - r + k} {y} {x + b} {y + r - k} {x + b} {y + r}"
        f"V{y + h - r}C{x + b} {y + h - r + k} {x + b - r + k} {y + h} {x + b - r} {y + h}"
        f"H{x + r}C{x + r - k} {y + h} {x} {y + h - r + k} {x} {y + h - r}"
        f"V{y + r}C{x} {y + r - k} {x + r - k} {y} {x + r} {y}Z")


def kreis(cx, cy, r):
    k = r * 0.5523
    return aus_d(
        f"M{cx} {cy - r}C{cx + k} {cy - r} {cx + r} {cy - k} {cx + r} {cy}"
        f"C{cx + r} {cy + k} {cx + k} {cy + r} {cx} {cy + r}"
        f"C{cx - k} {cy + r} {cx - r} {cy + k} {cx - r} {cy}"
        f"C{cx - r} {cy - k} {cx - k} {cy - r} {cx} {cy - r}Z")


def ring(cx, cy, r_aussen, r_innen):
    return minus(kreis(cx, cy, r_aussen), kreis(cx, cy, r_innen))


def vieleck(*punkte):
    (x0, y0), *rest = punkte
    return aus_d(f"M{x0} {y0}" + "".join(f"L{x} {y}" for x, y in rest) + "Z")


def linie(x0, y0, x1, y1, staerke):
    """Gerade Linie als Fläche (stumpfe Enden)."""
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * staerke / 2, dx / n * staerke / 2
    return vieleck((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny))


def kontur(p: pathops.Path, staerke: float, rund=False) -> pathops.Path:
    """Umriss einer offenen oder geschlossenen Form als Fläche."""
    kopie = pathops.Path()
    kopie.addPath(p)
    cap = pathops.LineCap.ROUND_CAP if rund else pathops.LineCap.BUTT_CAP
    join = pathops.LineJoin.ROUND_JOIN if rund else pathops.LineJoin.MITER_JOIN
    kopie.stroke(staerke, cap, join, 10)
    return sauber(kopie)


def offener_pfad(dstr: str) -> pathops.Path:
    p = pathops.Path()
    parse_path(dstr, p.getPen())
    return p


# ---------------------------------------------------------------- Schrift

@lru_cache(maxsize=None)
def _schriftdaten(datei: str) -> bytes:
    """HarfBuzz liest kein WOFF2 – also im Speicher zu TTF entpacken."""
    t = TTFont(SCHRIFTEN / datei)
    t.flavor = None
    puffer = io.BytesIO()
    t.save(puffer)
    return puffer.getvalue()


class Schrift:
    def __init__(self, datei: str, **achsen):
        self.face = hb.Face(hb.Blob(_schriftdaten(datei)))
        self.font = hb.Font(self.face)
        self.upem = self.face.upem
        if achsen:
            self.font.set_variations(achsen)

    def gid(self, zeichen: str) -> int:
        return self.font.get_nominal_glyph(ord(zeichen))

    @property
    def versal(self) -> float:
        return self.font.get_glyph_extents(self.gid("H")).y_bearing

    def zeichen(self, z: str, hoehe: float) -> pathops.Path:
        """Einzelnes Zeichen, Versalhöhe = hoehe, Oberkante y=0, linke Tintenkante x=0."""
        p = self.satz(z, hoehe)
        x0 = grenzen(p)[0]
        return verschieben(p, -x0, 0)

    def satz(self, text: str, hoehe: float, sperrung: float = 0.0,
             merkmale: dict | None = None, einzeln: bool = False):
        """Text mit Versalhöhe `hoehe`; Oberkante der Versalien bei y=0, Grundlinie bei y=hoehe.

        sperrung: zusätzlicher Buchstabenabstand in Versalhöhen.
        einzeln=True liefert zusätzlich die Liste der Einzelzeichen-Pfade.
        """
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, merkmale or {"kern": True})
        s = hoehe / self.versal
        extra = sperrung * self.versal
        gesamt, teile, x = pathops.Path(), [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            teil = pathops.Path()
            pen = TransformPen(teil.getPen(), (s, 0, 0, -s, (x + pos.x_offset) * s, hoehe - pos.y_offset * s))
            self.font.draw_glyph_with_pen(info.codepoint, pen)
            teil = sauber(teil)
            teile.append(teil)
            gesamt.addPath(teil)
            x += pos.x_advance + extra
        gesamt = sauber(gesamt)
        if einzeln:
            return gesamt, teile
        return gesamt


    def glyphen(self, text: str, hoehe: float, sperrung: float = 0.0):
        """Wie satz(), aber als Liste (pfad, x_mitte) je Zeichen – für Text auf Kreisbögen."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True})
        s = hoehe / self.versal
        extra = sperrung * self.versal
        teile, x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            teil = pathops.Path()
            pen = TransformPen(teil.getPen(), (s, 0, 0, -s, (x + pos.x_offset) * s, hoehe - pos.y_offset * s))
            self.font.draw_glyph_with_pen(info.codepoint, pen)
            teile.append((sauber(teil), (x + pos.x_advance / 2) * s))
            x += pos.x_advance + extra
        gesamt = (x - extra) * s
        return teile, gesamt


def bogentext(schrift: "Schrift", text: str, hoehe: float, cx: float, cy: float, r_mitte: float,
              mitte_grad: float = 0.0, unten: bool = False, sperrung: float = 0.0):
    """Text auf einem Kreisbogen. Winkel im Uhrzeigersinn ab 12 Uhr.

    oben: liest im Uhrzeigersinn, Köpfe nach außen. unten: liest gegen den Uhrzeigersinn,
    Köpfe zur Mitte – so stehen beide Zeilen aufrecht.
    """
    teile, gesamt = schrift.glyphen(text, hoehe, sperrung)
    erg = pathops.Path()
    for pfad, xm in teile:
        u = xm - gesamt / 2
        if unten:
            alpha = math.radians(mitte_grad) - u / r_mitte
            rot = alpha - math.pi
        else:
            alpha = math.radians(mitte_grad) + u / r_mitte
            rot = alpha
        px, py = cx + r_mitte * math.sin(alpha), cy - r_mitte * math.cos(alpha)
        co, si = math.cos(rot), math.sin(rot)
        # Glyphmitte (xm, hoehe/2) -> Ursprung, drehen, auf den Kreispunkt setzen
        tx, ty = -xm, -hoehe / 2
        erg.addPath(matrix(pfad, a=co, b=si, c=-si, d=co,
                           e=co * tx - si * ty + px, f=si * tx + co * ty + py))
    return sauber(erg)


def breite(p) -> float:
    x0, _, x1, _ = grenzen(p)
    return x1 - x0


def hoehe(p) -> float:
    _, y0, _, y1 = grenzen(p)
    return y1 - y0


def links_buendig(p, x=0.0):
    return verschieben(p, x - grenzen(p)[0], 0)


def auf_breite(p, soll: float):
    """Gleichmäßig skalieren, bis die Tintenbreite `soll` ist (Oberkante bleibt bei y0)."""
    x0, y0, x1, _ = grenzen(p)
    s = soll / (x1 - x0)
    return matrix(p, a=s, d=s, e=-x0 * s, f=y0 - y0 * s)


# ---------------------------------------------------------------- SVG

def svg(breite_: float, hoehe_: float, ebenen, hintergrund: str | None = None,
        titel: str = "DelaTec") -> str:
    """ebenen: Liste von (pfad, farbe). Jede Farbe wird zu genau einer <path>-Fläche."""
    nach_farbe: dict[str, pathops.Path] = {}
    reihenfolge = []
    for pfad, farbe in ebenen:
        if farbe not in nach_farbe:
            nach_farbe[farbe] = pathops.Path()
            reihenfolge.append(farbe)
        nach_farbe[farbe].addPath(pfad)
    teile = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breite_:g} {hoehe_:g}" '
             f'width="{breite_:g}" height="{hoehe_:g}">', f"  <title>{titel}</title>"]
    if hintergrund:
        teile.append(f'  <rect width="{breite_:g}" height="{hoehe_:g}" fill="{hintergrund}"/>')
    for farbe in reihenfolge:
        teile.append(f'  <path fill="{farbe}" d="{d(sauber(nach_farbe[farbe]))}"/>')
    teile.append("</svg>\n")
    return "\n".join(teile)
