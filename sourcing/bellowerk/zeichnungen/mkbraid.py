"""Erzeugt LE-01-flechtung-schritte.svg (A3 quer, farbig): Bleed Knot Schritt fuer Schritt.

Konstruktion nach dem Goldmuster (Fotos 18 Sep 2026) plus Recherche zum "bleed knot"
(auch "blood knot"): Der Riemen wird NICHT in Straenge geschlitzt und nie durchtrennt.
Es wird ein Laengsschlitz geschnitten und der volle Riemen durch sich selbst gezogen.
Dabei dreht sich das Leder, die Fleischseite zeigt nach aussen -> das V-Muster.
"""
import pathlib

W, H = 1587, 1123
GRAIN = "#7a4f2d"     # Narbenseite (aussen, dunkel)
GRAIN_D = "#4e3119"
FLESH = "#c7b49a"     # Fleischseite (rau, hell) - das Erkennungszeichen des Knotens
BRASS = "#c9a44a"
BRASS_D = "#9a7c2f"
INK = "#1a1a1a"
RED = "#c0392b"
GREEN = "#2e7d32"
SH = 76               # Riemenbreite in der Zeichnung


def txt(x, y, s, size=13, col=INK, anchor="start", weight="normal", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}">{s}</text>')


def arrow(x1, y1, x2, y2, col=RED, w=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    L, sp = 15, 0.45
    p1 = (x2 - L * math.cos(a - sp), y2 - L * math.sin(a - sp))
    p2 = (x2 - L * math.cos(a + sp), y2 - L * math.sin(a + sp))
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M {x2} {y2} L {p1[0]:.1f} {p1[1]:.1f} L {p2[0]:.1f} {p2[1]:.1f} Z" fill="{col}"/>')


def strap(x, y, w, h=SH, fill=GRAIN):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{GRAIN_D}" stroke-width="2"/>'


def slit(cx, cy, length, open_h=0, col="#fff"):
    """LAENGSschlitz - laeuft in Riemenrichtung. Geschlossen = Linie, offen = Linse."""
    w = length / 2
    if open_h <= 0:
        return (f'<line x1="{cx - w}" y1="{cy}" x2="{cx + w}" y2="{cy}" stroke="{GRAIN_D}" stroke-width="3"/>'
                f'<circle cx="{cx - w}" cy="{cy}" r="3.5" fill="none" stroke="{GRAIN_D}" stroke-width="2"/>'
                f'<circle cx="{cx + w}" cy="{cy}" r="3.5" fill="none" stroke="{GRAIN_D}" stroke-width="2"/>')
    o = open_h / 2
    return (f'<path d="M {cx - w} {cy} Q {cx} {cy - o} {cx + w} {cy} Q {cx} {cy + o} {cx - w} {cy} Z" '
            f'fill="{col}" stroke="{GRAIN_D}" stroke-width="2"/>')


def vchain(x, y, n, pitch=64, h=SH):
    """Kette fertiger Bleed Knots: helle Fleischseiten-Blaetter auf dunkler Narbenseite."""
    out = [f'<rect x="{x}" y="{y}" width="{n * pitch}" height="{h}" fill="{GRAIN}" stroke="none"/>']
    for i in range(n):
        x0 = x + i * pitch
        out.append(
            f'<path d="M {x0 + 5} {y + 5} Q {x0 + pitch * 0.55} {y + h * 0.30} {x0 + pitch * 0.86} {y + h / 2} '
            f'Q {x0 + pitch * 0.55} {y + h * 0.70} {x0 + 5} {y + h - 5} '
            f'Q {x0 + pitch * 0.30} {y + h / 2} {x0 + 5} {y + 5} Z" '
            f'fill="{FLESH}" stroke="{GRAIN_D}" stroke-width="1.8"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{n * pitch}" height="{h}" fill="none" stroke="{GRAIN_D}" stroke-width="2"/>')
    return "\n      ".join(out)


def ring(cx, cy, ro, ri):
    return (f'<circle cx="{cx}" cy="{cy}" r="{ro}" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{ri}" fill="#fff" stroke="{BRASS_D}" stroke-width="2"/>')


def hook(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<circle cx="26" cy="0" r="24" fill="none" stroke="{BRASS_D}" stroke-width="7"/>'
            f'<path d="M 50 0 h 20 a 13 13 0 0 0 13 -13 v -6" fill="none" stroke="{BRASS_D}" stroke-width="7"/>'
            f'<path d="M 83 -19 a 19 19 0 1 1 26 19 a 19 19 0 1 1 -26 19 v -13" fill="none" '
            f'stroke="{BRASS_D}" stroke-width="7"/></g>')


def panel(x, y, w, h, n, title):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fff" stroke="#c8c8c8" stroke-width="1.5"/>'
            f'<circle cx="{x + 26}" cy="{y + 26}" r="14" fill="{INK}"/>'
            f'<text x="{x + 26}" y="{y + 31}" text-anchor="middle" font-size="15" font-weight="bold" fill="#fff">{n}</text>'
            f'<text x="{x + 50}" y="{y + 32}" font-size="16" font-weight="bold" fill="{INK}">{title}</text>')


P = []
A = P.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'font-family="Arial, Helvetica, sans-serif" fill="{INK}">')
A(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# ---------- Kopf ----------
A(txt(40, 44, 'LE-01 · Sheet 3/3 · THE BLEED KNOT — how every ring and hook is fixed', 25, INK, weight="bold"))
A(txt(40, 70, 'Bellowerk Manufaktur · v3.0 · 18 Sep 2026 · A3 landscape · Taken from the golden sample. The technique is the "bleed knot" (also called blood knot) —', 14))
A(txt(40, 92, 'a known leather technique, no stitching and no rivets. The strap is NEVER cut into strands and NEVER cut through. It is one piece from end to end.', 14, weight="bold"))
A(txt(40, 112, 'Leather: veg-tan cowhide 3.5–4.0 mm = 9–10 oz, firm temper, oiled pull-up. Strap cut 20 mm with a strap cutter. Edges bevelled both sides and burnished, no edge paint.', 13, "#444"))

lx = 1105
A(f'<rect x="{lx - 14}" y="28" width="450" height="80" rx="8" fill="#f7f7f7" stroke="#d5d5d5"/>')
A(txt(lx, 50, 'How to read the drawings:', 13, weight="bold"))
A(f'<rect x="{lx}" y="60" width="40" height="16" fill="{GRAIN}" stroke="{GRAIN_D}" stroke-width="1.5"/>')
A(txt(lx + 48, 73, 'grain side (outside)', 12.5))
A(f'<rect x="{lx + 210}" y="60" width="40" height="16" fill="{FLESH}" stroke="{GRAIN_D}" stroke-width="1.5"/>')
A(txt(lx + 258, 73, 'flesh side (rough)', 12.5))
A(txt(lx, 98, 'The flesh side showing through is how you know the knot is right.', 12.5, "#555"))

PW, PH = 490, 292
R1, R2 = 140, 452

# ================= 1 · Ein Schlitz =================
px, py = 40, R1
A(panel(px, py, PW, PH, 1, 'One slit — that is the whole secret'))
A(strap(px + 30, py + 90, 430))
A(slit(px + 245, py + 128, 114))
A(f'<g stroke="{INK}" stroke-width="1.2">'
  f'<line x1="{px + 188}" y1="{py + 186}" x2="{px + 302}" y2="{py + 186}"/>'
  f'<line x1="{px + 188}" y1="{py + 180}" x2="{px + 188}" y2="{py + 192}"/>'
  f'<line x1="{px + 302}" y1="{py + 180}" x2="{px + 302}" y2="{py + 192}"/></g>')
A(txt(px + 245, py + 176, '30 mm', 13, anchor="middle", weight="bold"))
A(txt(px + 322, py + 178, 'slit runs ALONG the strap', 12.5, "#555"))
A(txt(px + 30, py + 212, 'ONE lengthwise slit, 30 mm long, centred across the width.', 13))
A(txt(px + 30, py + 230, 'Punch both ends Ø 2 mm FIRST, then cut between the two', 13, weight="bold"))
A(txt(px + 30, py + 248, 'holes with a head knife — that way the slit cannot run.', 13, weight="bold"))
A(txt(px + 30, py + 266, 'Nothing else is cut: the strap keeps its full 20 mm width.', 13))

# ================= 2 · Ring auffaedeln, Ende durchziehen =================
px = 40 + (PW + 13)
A(panel(px, py, PW, PH, 2, 'Thread the ring, then the tail through the slit'))
A(strap(px + 30, py + 90, 300))
A(slit(px + 175, py + 128, 114, 46))
A(ring(px + 392, py + 128, 34, 22))
A(f'<path d="M {px + 330} {py + 90} H {px + 392} M {px + 330} {py + 166} H {px + 392}" '
  f'stroke="{GRAIN_D}" stroke-width="2" fill="none"/>')
A(f'<rect x="{px + 330}" y="{py + 90}" width="62" height="76" fill="{GRAIN}" stroke="none"/>')
A(f'<path d="M {px + 330} {py + 90} H {px + 392} M {px + 330} {py + 166} H {px + 392}" stroke="{GRAIN_D}" stroke-width="2"/>')
A(arrow(px + 380, py + 56, px + 196, py + 104))
A(txt(px + 214, py + 46, 'the WHOLE tail goes through the slit', 13, RED, weight="bold"))
A(txt(px + 30, py + 200, 'Put the ring (or the snap hook) on the strap, then push the', 13))
A(txt(px + 30, py + 218, 'entire rest of the lead through the open slit. On a 2.60 m lead', 13))
A(txt(px + 30, py + 236, 'that means pulling metres of leather through — that is normal', 13))
A(txt(px + 30, py + 254, 'and it is why the knots are made before the lead is cut to length.', 13))

# ================= 3 · Festziehen =================
px = 40 + 2 * (PW + 13)
A(panel(px, py, PW, PH, 3, 'Pull tight — the V appears'))
A(strap(px + 30, py + 90, 150))
A(f'<g>{vchain(px + 180, py + 90, 1, 84)}</g>')
A(strap(px + 264, py + 90, 90))
A(ring(px + 388, py + 128, 34, 22))
A(f'<rect x="{px + 354}" y="{py + 90}" width="34" height="76" fill="{GRAIN}" stroke="none"/>')
A(f'<path d="M {px + 354} {py + 90} H {px + 388} M {px + 354} {py + 166} H {px + 388}" stroke="{GRAIN_D}" stroke-width="2"/>')
A(arrow(px + 300, py + 56, px + 232, py + 88, GREEN))
A(txt(px + 240, py + 44, 'flesh side now shows', 13, GREEN, weight="bold"))
A(txt(px + 30, py + 200, 'Pull the tail through until the knot sits tight against the ring.', 13))
A(txt(px + 30, py + 218, 'The leather turns as it passes through itself, so the rough flesh', 13))
A(txt(px + 30, py + 236, 'side comes to the outside and forms a V. That light patch is the', 13))
A(txt(px + 30, py + 254, 'proof the knot is made correctly — it is not a fault.', 13, weight="bold"))

# ================= 4 · Kette =================
px, py = 40, R2
A(panel(px, py, PW, PH, 4, 'Repeat — the chain at the hook ends'))
A(strap(px + 30, py + 88, 60))
A(f'<g>{vchain(px + 90, py + 88, 5, 64)}</g>')
A(strap(px + 410, py + 88, 40))
A(f'<g stroke="{INK}" stroke-width="1.2">'
  f'<line x1="{px + 90}" y1="{py + 186}" x2="{px + 410}" y2="{py + 186}"/>'
  f'<line x1="{px + 90}" y1="{py + 180}" x2="{px + 90}" y2="{py + 192}"/>'
  f'<line x1="{px + 410}" y1="{py + 180}" x2="{px + 410}" y2="{py + 192}"/></g>')
A(txt(px + 250, py + 206, '115 mm · 5–6 V, pitch approx. 20 mm', 13, anchor="middle", weight="bold"))
A(txt(px + 30, py + 234, 'At hook A and hook B the knot is repeated in a row: cut the next', 13))
A(txt(px + 30, py + 252, 'slit, pull the tail through again, tighten. Five to six V over', 13))
A(txt(px + 30, py + 270, '115 mm, evenly spaced — match the golden sample.', 13))

# ================= 5 · Mittelring =================
px = 40 + (PW + 13)
A(panel(px, py, PW, PH, 5, 'Ring 1 and ring 2 — ONE knot, no screw'))
A(strap(px + 30, py + 88, 150))
A(f'<g>{vchain(px + 180, py + 88, 1, 84)}</g>')
A(ring(px + 298, py + 126, 30, 19))
A(f'<rect x="{px + 264}" y="{py + 88}" width="34" height="76" fill="{GRAIN}" stroke="none"/>')
A(f'<path d="M {px + 264} {py + 88} H {px + 298} M {px + 264} {py + 164} H {px + 298}" stroke="{GRAIN_D}" stroke-width="2"/>')
A(strap(px + 328, py + 88, 130))
A(txt(px + 34, py + 186, 'lead continues', 12, "#666", style="italic"))
A(txt(px + 330, py + 186, 'lead continues', 12, "#666", style="italic"))
A(txt(px + 30, py + 234, 'A middle ring gets a SINGLE bleed knot and no Chicago screw.', 13, weight="bold"))
A(txt(px + 30, py + 252, 'The knot alone holds it — that is how the golden sample is made.', 13))
A(txt(px + 30, py + 270, 'Pull it up tight so the ring cannot travel along the strap.', 13))

# ================= 6 · Abschluss =================
px = 40 + 2 * (PW + 13)
A(panel(px, py, PW, PH, 6, 'Finish at the hook ends'))
A(strap(px + 30, py + 88, 60))
A(f'<g>{vchain(px + 90, py + 88, 4, 64)}</g>')
A(strap(px + 346, py + 88, 60))
A(f'<circle cx="{px + 376}" cy="{py + 126}" r="15" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')
A(f'<line x1="{px + 366}" y1="{py + 126}" x2="{px + 386}" y2="{py + 126}" stroke="{BRASS_D}" stroke-width="2.5"/>')
A(f'<g stroke-dasharray="6 4"><line x1="{px + 406}" y1="{py + 88}" x2="{px + 406}" y2="{py + 164}" '
  f'stroke="{GRAIN_D}" stroke-width="2"/></g>')
A(arrow(px + 300, py + 56, px + 372, py + 104))
A(txt(px + 170, py + 44, '1 Chicago screw after the last V', 13, RED, weight="bold"))
A(txt(px + 30, py + 234, 'Only at hook A and hook B: one solid brass Chicago screw after', 13))
A(txt(px + 30, py + 252, 'the last V, tail trimmed 20 mm behind it, edge bevelled. The knots', 13))
A(txt(px + 30, py + 270, 'carry the load — the screw only stops the tail lifting.', 13))

# ================= untere Reihe: die drei Positionen =================
R3 = 758
A(f'<rect x="40" y="{R3}" width="1507" height="330" rx="8" fill="#fff" stroke="#c8c8c8" stroke-width="1.5"/>')
A(txt(62, R3 + 32, 'The three positions on the lead', 17, weight="bold"))

my = R3 + 78


def mini(x, label, sub1, sub2):
    A(txt(x, my - 12, label, 14, weight="bold"))
    A(txt(x, my + 150, sub1, 12.5, "#444"))
    A(txt(x, my + 168, sub2, 12.5, "#444"))


# Karabiner A
mx = 78
mini(mx, 'Hook A — 5–6 knots + 1 screw',
     'Strap through the hook eye, folded back, then the', 'chain of knots. Tail ends after the screw.')
A(f'<circle cx="{mx + 22}" cy="{my + 46}" r="13" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')
A(strap(mx, my + 8, 44))
A(f'<g>{vchain(mx + 44, my + 8, 4, 54)}</g>')
A(strap(mx + 260, my + 8, 26))
A(hook(mx + 286, my + 46, 0.62))

# Mittelring
mx = 520
mini(mx, 'Ring 1 and ring 2 — 1 knot, no screw',
     'One continuous strap runs straight through.', 'Nothing else holds the ring.')
A(strap(mx, my + 8, 96))
A(f'<g>{vchain(mx + 96, my + 8, 1, 76)}</g>')
A(f'<rect x="{mx + 172}" y="{my + 8}" width="26" height="76" fill="{GRAIN}" stroke="none"/>')
A(f'<path d="M {mx + 172} {my + 8} H {mx + 198} M {mx + 172} {my + 84} H {mx + 198}" stroke="{GRAIN_D}" stroke-width="2"/>')
A(ring(mx + 200, my + 46, 28, 18))
A(strap(mx + 228, my + 8, 110))

# Karabiner B + Ring 3
mx = 960
mini(mx, 'Ring 3 + hook B — both in one fold',
     'The strap goes through ring 3 AND the hook eye', 'before the knots start. Ring 30 mm before the eye.')
A(f'<circle cx="{mx + 22}" cy="{my + 46}" r="13" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')
A(strap(mx, my + 8, 44))
A(f'<g>{vchain(mx + 44, my + 8, 4, 54)}</g>')
A(strap(mx + 260, my + 8, 16))
A(ring(mx + 300, my + 46, 32, 21))
A(hook(mx + 330, my + 46, 0.62))

# Hinweiskasten rechts
bx = 1330
A(f'<rect x="{bx}" y="{R3 + 46}" width="200" height="262" rx="8" fill="#f2f7f2" stroke="{GREEN}" stroke-width="2"/>')
A(txt(bx + 18, R3 + 76, 'Check on the', 13.5, GREEN, weight="bold"))
A(txt(bx + 18, R3 + 94, 'first sample', 13.5, GREEN, weight="bold"))
A(txt(bx + 18, R3 + 124, 'Slit length 30 mm is a', 12.5))
A(txt(bx + 18, R3 + 142, 'starting value. Adjust it', 12.5))
A(txt(bx + 18, R3 + 160, 'until the chain measures', 12.5))
A(txt(bx + 18, R3 + 178, '115 mm with 5–6 even V,', 12.5))
A(txt(bx + 18, R3 + 196, 'and the knots sit tight', 12.5))
A(txt(bx + 18, R3 + 214, 'with no gaps.', 12.5))
A(txt(bx + 18, R3 + 244, 'Send photos of one', 12.5))
A(txt(bx + 18, R3 + 262, 'finished knot, front', 12.5))
A(txt(bx + 18, R3 + 280, 'and back, before', 12.5))
A(txt(bx + 18, R3 + 298, 'production.', 12.5))

A('</svg>')

out = pathlib.Path(__file__).parent / 'LE-01-flechtung-schritte.svg'
out.write_text("\n".join(P), encoding="utf-8")
print("geschrieben:", out)
