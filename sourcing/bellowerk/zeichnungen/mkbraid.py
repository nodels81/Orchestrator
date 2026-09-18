"""Erzeugt das Schritt-fuer-Schritt-Flechtblatt LE-01-flechtung-schritte.svg (A3 quer, farbig)."""
import pathlib

W, H = 1587, 1123
LEATHER = "#b58050"
LEATHER_D = "#8c5c33"
BRASS = "#c9a44a"
BRASS_D = "#9a7c2f"
C1, C2, C3 = "#c0503a", "#2e6f9e", "#6e8b3d"   # Strang 1 / 2 / 3
INK = "#1a1a1a"
RED = "#c0392b"
GREEN = "#2e7d32"

# Flechtmuster: Spurposition je Strang und Schritt (T=-1, M=0, B=+1)
PAT = {
    0: [-1, 0, 1, 1, 0, -1],
    1: [0, -1, -1, 0, 1, 1],
    2: [1, 1, 0, -1, -1, 0],
}
COL = {0: C1, 1: C2, 2: C3}


def braid(x0, y0, steps, dx=30, lane=17, sw=14):
    """Gibt SVG-Segmente eines 3-Strang-Flechtzopfs mit korrekter Ueber/Unter-Reihenfolge."""
    def pos(s, k):
        return x0 + k * dx, y0 + PAT[s][k % 6] * lane

    out = []
    for k in range(steps):
        entering = [s for s in (0, 1, 2) if PAT[s][(k + 1) % 6] == 0]
        order = [s for s in (0, 1, 2) if s not in entering] + entering
        for s in order:
            x1, y1 = pos(s, k)
            x2, y2 = pos(s, k + 1)
            xm = (x1 + x2) / 2
            d = f"M {x1:.1f} {y1:.1f} C {xm:.1f} {y1:.1f} {xm:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"
            # weisse Unterlegung trennt die Straenge optisch an den Kreuzungen
            out.append(f'<path d="{d}" stroke="#fff" stroke-width="{sw + 7}" fill="none" stroke-linecap="round"/>')
            out.append(f'<path d="{d}" stroke="{COL[s]}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>')
    return "\n      ".join(out)


def strands_flat(x0, y0, length, lane=17, sw=14):
    """Drei parallele Straenge (ungeflochten)."""
    out = []
    for s, off in ((0, -1), (1, 0), (2, 1)):
        y = y0 + off * lane
        out.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + length}" y2="{y}" stroke="{COL[s]}" '
                   f'stroke-width="{sw}" stroke-linecap="round"/>')
    return "\n      ".join(out)


def ring(cx, cy, ro, ri):
    return (f'<circle cx="{cx}" cy="{cy}" r="{ro}" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{ri}" fill="#fff" stroke="{BRASS_D}" stroke-width="2"/>')


def hook(x, y, s=1.0):
    """Karabiner, Oese links bei x."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<circle cx="26" cy="0" r="24" fill="none" stroke="{BRASS_D}" stroke-width="7"/>'
            f'<path d="M 50 0 h 20 a 13 13 0 0 0 13 -13 v -6" fill="none" stroke="{BRASS_D}" stroke-width="7"/>'
            f'<path d="M 83 -19 a 19 19 0 1 1 26 19 a 19 19 0 1 1 -26 19 v -13" fill="none" '
            f'stroke="{BRASS_D}" stroke-width="7"/></g>')


def panel(x, y, w, h, n, title):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fff" stroke="#c8c8c8" stroke-width="1.5"/>'
            f'<circle cx="{x + 26}" cy="{y + 26}" r="14" fill="{INK}"/>'
            f'<text x="{x + 26}" y="{y + 31}" text-anchor="middle" font-size="15" font-weight="bold" fill="#fff">{n}</text>'
            f'<text x="{x + 50}" y="{y + 32}" font-size="16" font-weight="bold" fill="{INK}">{title}</text></g>')


def arrow(x1, y1, x2, y2, col=RED, w=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    L, sp = 15, 0.45
    p1 = (x2 - L * math.cos(a - sp), y2 - L * math.sin(a - sp))
    p2 = (x2 - L * math.cos(a + sp), y2 - L * math.sin(a + sp))
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M {x2} {y2} L {p1[0]:.1f} {p1[1]:.1f} L {p2[0]:.1f} {p2[1]:.1f} Z" fill="{col}"/>')


def txt(x, y, s, size=13, col=INK, anchor="start", weight="normal", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}">{s}</text>')


P = []
A = P.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'font-family="Arial, Helvetica, sans-serif" fill="{INK}">')
A(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# ---------- Kopf ----------
A(txt(40, 44, 'LE-01 · Sheet 3/3 · HOW THE BRAIDED ATTACHMENT IS MADE — step by step', 25, INK, weight="bold"))
A(txt(40, 70, 'Bellowerk Manufaktur · v2.0 · 18 Sep 2026 · A3 landscape · The three strands are coloured only to make them easy to follow — it is ONE piece of leather.', 14))
A(txt(40, 92, 'The same attachment is used at all five positions: hook A, ring 1, ring 2, and ring 3 + hook B together. Binding dimensions are on sheet 1 and sheet 2.', 14))

# Legende
lx = 1080
A(f'<rect x="{lx - 14}" y="30" width="470" height="76" rx="8" fill="#f7f7f7" stroke="#d5d5d5"/>')
A(txt(lx, 52, 'Strands of the same strap:', 13, weight="bold"))
for i, (c, lab) in enumerate(((C1, 'strand 1'), (C2, 'strand 2'), (C3, 'strand 3'))):
    A(f'<rect x="{lx + i * 150}" y="64" width="34" height="13" rx="6" fill="{c}"/>')
    A(txt(lx + i * 150 + 42, 76, lab, 13))
A(txt(lx, 98, 'Brass = ring / hook eye · red arrow = the next move', 12.5, "#555"))

# ---------- Reihe 1: Schritte 1-3 ----------
PW, PH = 490, 290
R1 = 125
for i, (n, t) in enumerate(((1, 'Cut the three strands'), (2, 'Thread the ring, fold back'), (3, 'Crossing 1 — top strand over the middle'))):
    A(panel(40 + i * (PW + 13), R1, PW, PH, n, t))

# Panel 1: flacher Riemen mit Schlitzen
px, py = 40, R1
A(f'<rect x="{px + 40}" y="{py + 95}" width="400" height="56" rx="4" fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
for _s, _off in ((0, 104.3), (1, 123.0), (2, 141.7)):
    A(f'<rect x="{px + 90}" y="{py + _off - 8}" width="330" height="16" fill="{COL[_s]}" opacity="0.85"/>')
A(f'<line x1="{px + 90}" y1="{py + 113.7}" x2="{px + 420}" y2="{py + 113.7}" stroke="#fff" stroke-width="3"/>')
A(f'<line x1="{px + 90}" y1="{py + 132.3}" x2="{px + 420}" y2="{py + 132.3}" stroke="#fff" stroke-width="3"/>')
A(f'<circle cx="{px + 90}" cy="{py + 113.7}" r="4" fill="#fff" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{px + 90}" cy="{py + 132.3}" r="4" fill="#fff" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{px + 420}" cy="{py + 113.7}" r="4" fill="#fff" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{px + 420}" cy="{py + 132.3}" r="4" fill="#fff" stroke="{LEATHER_D}" stroke-width="2"/>')
A(txt(px + 22, py + 105, '1', 14, C1, weight="bold"))
A(txt(px + 22, py + 128, '2', 14, C2, weight="bold"))
A(txt(px + 22, py + 150, '3', 14, C3, weight="bold"))
A(f'<line x1="{px + 90}" y1="{py + 175}" x2="{px + 420}" y2="{py + 175}" stroke="{INK}" stroke-width="1.2"/>')
A(f'<line x1="{px + 90}" y1="{py + 169}" x2="{px + 90}" y2="{py + 181}" stroke="{INK}" stroke-width="1.2"/>')
A(f'<line x1="{px + 420}" y1="{py + 169}" x2="{px + 420}" y2="{py + 181}" stroke="{INK}" stroke-width="1.2"/>')
A(txt(px + 255, py + 193, '115 mm', 13, anchor="middle", weight="bold"))
A(txt(px + 22, py + 225, 'Two lengthwise slits over 115 mm divide the 20 mm strap into', 13))
A(txt(px + 22, py + 243, 'three strands of 6.7 mm. Slit ends punched Ø 2 mm so they', 13))
A(txt(px + 22, py + 261, 'cannot tear. The strap is NEVER cut through.', 13))

# Panel 2: Ring + Falte
px = 40 + (PW + 13)
A(ring(px + 90, py + 123, 34, 22))
A(f'<path d="M {px + 90} {py + 95} H {px + 430} V {py + 151} H {px + 90}" fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<path d="M {px + 118} {py + 163} H {px + 380}" stroke="{LEATHER_D}" stroke-width="20" stroke-linecap="round" opacity="0.55"/>')
A(arrow(px + 380, py + 178, px + 150, py + 178))
A(txt(px + 200, py + 200, 'fold back 150 mm', 13, RED, weight="bold"))
A(txt(px + 22, py + 225, 'Pass the end through the ring (at hook B: through ring 3 AND', 13))
A(txt(px + 22, py + 243, 'the hook eye) and fold it back on itself by 150 mm. From here', 13))
A(txt(px + 22, py + 261, 'on every strand is TWO layers thick — braid them as one.', 13))

# Panel 3: erste Kreuzung
px = 40 + 2 * (PW + 13)
A(ring(px + 80, py + 123, 30, 19))
A(f'<g>{strands_flat(px + 110, py + 123, 90)}</g>')
A(f'<g>{braid(px + 200, py + 123, 2)}</g>')
A(f'<g>{strands_flat(px + 260, py + 123, 150)}</g>')
A(arrow(px + 195, py + 84, px + 235, py + 112))
A(txt(px + 150, py + 78, 'strand 1 over strand 2', 13, RED, weight="bold"))
A(txt(px + 22, py + 225, 'Start the braid: bring the TOP strand over the middle one.', 13))
A(txt(px + 22, py + 243, 'Keep the two layers of each strand flat and together, grain', 13))
A(txt(px + 22, py + 261, 'side out. Pull every crossing tight before the next one.', 13))

# ---------- Reihe 2: Schritte 4-6 ----------
R2 = 440
for i, (n, t) in enumerate(((4, 'Crossing 2 — bottom strand over'), (5, 'THE TRICK — clear the twist'), (6, 'Finish: 9–10 crossings, then screw'))):
    A(panel(40 + i * (PW + 13), R2, PW, PH, n, t))

# Panel 4
px, py = 40, R2
A(ring(px + 80, py + 123, 30, 19))
A(f'<g>{strands_flat(px + 110, py + 123, 60)}</g>')
A(f'<g>{braid(px + 170, py + 123, 3)}</g>')
A(f'<g>{strands_flat(px + 260, py + 123, 150)}</g>')
A(arrow(px + 200, py + 172, px + 240, py + 140))
A(txt(px + 140, py + 194, 'strand 3 over the new middle', 13, RED, weight="bold"))
A(txt(px + 22, py + 225, 'Now the BOTTOM strand crosses over the middle. Repeat these', 13))
A(txt(px + 22, py + 243, 'two moves alternately — this is an ordinary 3-strand braid,', 13))
A(txt(px + 22, py + 261, 'top over middle, bottom over middle.', 13))

# Panel 5: der Trick
px = 40 + (PW + 13)
A(ring(px + 70, py + 118, 28, 18))
A(f'<g>{braid(px + 100, py + 118, 4)}</g>')
# verdrehter Auslauf
A(f'<path d="M {px + 220} {py + 118} C {px + 270} {py + 118} {px + 280} {py + 150} {px + 330} {py + 150} '
  f'L {px + 430} {py + 150}" stroke="{LEATHER_D}" stroke-width="30" fill="none" stroke-linecap="round" opacity="0.5"/>')
A(txt(px + 300, py + 186, 'the strap below twists up', 12.5, "#666", style="italic"))
# Oeffnung markieren + Pfeil hindurch
A(f'<ellipse cx="{px + 196}" cy="{py + 118}" rx="17" ry="22" fill="none" stroke="{GREEN}" stroke-width="3" stroke-dasharray="5 4"/>')
A(arrow(px + 330, py + 86, px + 205, py + 104, GREEN, 4))
A(txt(px + 236, py + 74, 'pass the tail up through here', 13, GREEN, weight="bold"))
A(txt(px + 22, py + 225, 'After every 2 crossings the strap below the braid twists,', 13))
A(txt(px + 22, py + 243, 'because both ends are attached. Clear it: push the free tail', 13))
A(txt(px + 22, py + 261, 'UP THROUGH the opening. The twist disappears — braid on.', 13, weight="bold"))

# Panel 6: fertig
px = 40 + 2 * (PW + 13)
A(ring(px + 70, py + 118, 28, 18))
A(f'<g>{braid(px + 96, py + 118, 10)}</g>')
A(f'<rect x="{px + 396}" y="{py + 96}" width="70" height="44" rx="4" fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{px + 418}" cy="{py + 118}" r="11" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')
A(f'<line x1="{px + 411}" y1="{py + 118}" x2="{px + 425}" y2="{py + 118}" stroke="{BRASS_D}" stroke-width="2.5"/>')
A(f'<line x1="{px + 96}" y1="{py + 164}" x2="{px + 396}" y2="{py + 164}" stroke="{INK}" stroke-width="1.2"/>')
A(f'<line x1="{px + 96}" y1="{py + 158}" x2="{px + 96}" y2="{py + 170}" stroke="{INK}" stroke-width="1.2"/>')
A(f'<line x1="{px + 396}" y1="{py + 158}" x2="{px + 396}" y2="{py + 170}" stroke="{INK}" stroke-width="1.2"/>')
A(txt(px + 246, py + 182, '115 mm · 9–10 crossings', 13, anchor="middle", weight="bold"))
A(txt(px + 22, py + 225, 'Braid to 115 mm, then stop. The tail lies FLAT on the inside;', 13))
A(txt(px + 22, py + 243, 'one Chicago screw 10 mm after the braid, tail trimmed 20 mm', 13))
A(txt(px + 22, py + 261, 'after the screw, edge bevelled. Braid tight — it carries the load.', 13))

# ---------- Reihe 3: die vier Positionen ----------
R3 = 755
A(f'<rect x="40" y="{R3}" width="1507" height="330" rx="8" fill="#fff" stroke="#c8c8c8" stroke-width="1.5"/>')
A(txt(62, R3 + 32, 'What each fold has to capture — the three positions on the lead', 17, weight="bold"))

def mini(x, y, label, sub):
    A(txt(x, y - 14, label, 14, weight="bold"))
    A(txt(x, y + 176, sub, 12.5, "#444"))

# A: Karabiner A
mx, my = 110, R3 + 70
mini(mx, my, 'Hook A — hook eye only', 'Braid points towards the middle of the lead.')
A(hook(mx + 160, my + 46, 0.7))
A(f'<g>{braid(mx + 10, my + 46, 5, 28, 15, 12)}</g>')
A(f'<rect x="{mx - 40}" y="{my + 24}" width="55" height="44" rx="4" fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{mx - 16}" cy="{my + 46}" r="10" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')

# B: Mittelring
mx = 490
mini(mx, my, 'Ring 1 and ring 2 — ring on a bight', 'ONE continuous strap. Braid on the hook-B side.')
A(ring(mx + 22, my + 46, 28, 18))
A(f'<g>{braid(mx + 50, my + 46, 5, 28, 15, 12)}</g>')
A(f'<rect x="{mx + 195}" y="{my + 24}" width="105" height="44" rx="4" fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{mx + 219}" cy="{my + 46}" r="10" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')
A(f'<path d="M {mx - 60} {my + 24} H {mx + 10} M {mx - 60} {my + 68} H {mx + 10}" stroke="{LEATHER_D}" stroke-width="2" fill="none"/>')
A(f'<rect x="{mx - 60}" y="{my + 24}" width="70" height="44" fill="{LEATHER}" stroke="none"/>')
A(f'<path d="M {mx - 60} {my + 24} H {mx + 10} M {mx - 60} {my + 68} H {mx + 10}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(txt(mx - 62, my + 100, 'lead continues', 12, "#666", style="italic"))
A(txt(mx + 200, my + 100, 'lead continues', 12, "#666", style="italic"))

# C: Karabiner B + Ring 3
mx = 870
mini(mx, my, 'Ring 3 + hook B — both in ONE fold', 'Ring centre 30 mm before the hook eye.')
A(f'<g>{braid(mx + 10, my + 46, 5, 28, 15, 12)}</g>')
A(ring(mx + 172, my + 46, 30, 20))
A(hook(mx + 200, my + 46, 0.7))
A(f'<rect x="{mx - 40}" y="{my + 24}" width="55" height="44" rx="4" fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<circle cx="{mx - 16}" cy="{my + 46}" r="10" fill="{BRASS}" stroke="{BRASS_D}" stroke-width="2"/>')

# D: der Knoten am Muster - nicht kopieren
mx = 1030
A(f'<rect x="{mx + 130}" y="{R3 + 44}" width="356" height="262" rx="8" fill="#fdf3f2" stroke="{RED}" stroke-width="2"/>')
kx, ky = mx + 152, R3 + 100
A(txt(kx, ky - 14, 'The knot on the sample', 14, RED, weight="bold"))
A(ring(kx + 30, ky + 46, 30, 19))
A(f'<path d="M {kx + 306} {ky + 30} H {kx + 70} L {kx + 52} {ky + 46} L {kx + 70} {ky + 62} H {kx + 306}" '
  f'fill="{LEATHER}" stroke="{LEATHER_D}" stroke-width="2"/>')
A(f'<path d="M {kx + 96} {ky + 22} q 24 -22 46 0 q 14 16 -6 26" fill="none" stroke="{LEATHER_D}" stroke-width="13" stroke-linecap="round"/>')
A(f'<line x1="{kx + 120}" y1="{ky + 30}" x2="{kx + 120}" y2="{ky + 62}" stroke="#fff" stroke-width="3"/>')
A(f'<g stroke="{RED}" stroke-width="6" stroke-linecap="round"><line x1="{kx + 250}" y1="{ky - 4}" x2="{kx + 286}" y2="{ky + 32}"/>'
  f'<line x1="{kx + 286}" y1="{ky - 4}" x2="{kx + 250}" y2="{ky + 32}"/></g>')
A(txt(kx, ky + 118, 'On the golden sample rings 1 and 2 are held by a', 12.5))
A(txt(kx, ky + 136, 'knot: the end is pulled through a slit in itself.', 12.5))
A(txt(kx, ky + 154, 'DO NOT COPY. Every ring on our lead is', 12.5, RED, weight="bold"))
A(txt(kx, ky + 172, 'braided as shown above — no knots at all.', 12.5, RED, weight="bold"))

A('</svg>')

out = pathlib.Path('/home/user/Orchestrator/sourcing/bellowerk/zeichnungen/LE-01-flechtung-schritte.svg')
out.write_text("\n".join(P), encoding="utf-8")
print("geschrieben:", out, len("\n".join(P)), "bytes")
