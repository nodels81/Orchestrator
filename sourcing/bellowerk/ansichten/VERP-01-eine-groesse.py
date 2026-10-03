# -*- coding: utf-8 -*-
"""Erzeugt ansichten/VERP-01-eine-groesse.svg — Nachweis, dass eine Kiste Leine UND Halsband nimmt."""
import math, pathlib

S = 3.0  # px je mm in den Hauptansichten
W, H = 1820, 1190
INNEN_L, INNEN_B, INNEN_H = 260, 180, 85
LEINE_D, HALSBAND_D = 145, 95

def mm(x): return x * S

o = []
a = o.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  'font-family="Arial, Helvetica, sans-serif">')
a('''  <defs>
    <filter id="pappe" x="-5%" y="-10%" width="110%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.07 0.09" numOctaves="4" seed="7" result="r"/>
      <feColorMatrix in="r" type="saturate" values="0" result="g"/>
      <feComponentTransfer in="g" result="k"><feFuncA type="linear" slope="0.45" intercept="0.06"/></feComponentTransfer>
      <feComposite in="k" in2="SourceGraphic" operator="in" result="ka"/>
      <feBlend in="SourceGraphic" in2="ka" mode="multiply"/>
    </filter>
    <filter id="wurf" x="-20%" y="-20%" width="150%" height="160%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#2a251d" flood-opacity="0.20"/>
    </filter>
    <linearGradient id="leder" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#9C9B95"/><stop offset="55%" stop-color="#84837E"/><stop offset="100%" stop-color="#5E5D59"/>
    </linearGradient>
    <linearGradient id="messing" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E4C476"/><stop offset="45%" stop-color="#C9A24E"/><stop offset="100%" stop-color="#8A6A22"/>
    </linearGradient>
    <linearGradient id="kraft" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#D3B68E"/><stop offset="100%" stop-color="#B2946E"/>
    </linearGradient>
  </defs>''')
a(f'  <rect width="{W}" height="{H}" fill="#F3F1EC"/>')
a('  <text x="60" y="56" font-size="27" font-weight="bold" fill="#211C15">'
  'VERP-01 — eine Kiste für alles</text>')
a('  <text x="60" y="86" font-size="16" fill="#5E5648">'
  'Innenmaß 260 × 180 × 85 mm. Dieselbe Kiste nimmt die Führleine LE-01, '
  'das Halsband Hamburg Nr. 1 in jeder Größe — oder beides zusammen. '
  'Maßstab Draufsicht und Schnitt 1:3.</text>')

# ───────────────────────── Hilfsfunktionen ─────────────────────────
def kiste_wand(x, y, w, h):
    """Innenflaeche (w x h px) mit umlaufender Kartonwand."""
    d = 9
    return (f'<g filter="url(#wurf)"><rect x="{x-d}" y="{y-d}" width="{w+2*d}" height="{h+2*d}" rx="4" '
            f'fill="url(#kraft)" filter="url(#pappe)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#E9DCC4" filter="url(#pappe)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#8E7352" stroke-width="1.6"/></g>')

def rolle_oben(cx, cy, d_aussen, d_innen, dicke=4.0, farbe="url(#leder)"):
    """Draufsicht auf eine aufgerollte Lederrolle: konzentrische Windungen."""
    t = []
    ra, ri = mm(d_aussen)/2, mm(d_innen)/2
    t.append(f'<circle cx="{cx}" cy="{cy}" r="{ra}" fill="{farbe}" stroke="#3E3D3A" stroke-width="1.4"/>')
    r = ra
    while r - mm(dicke) > ri:
        r -= mm(dicke)
        t.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="#50504C" stroke-width="0.9" opacity="0.8"/>')
    t.append(f'<circle cx="{cx}" cy="{cy}" r="{ri}" fill="#E9DCC4" stroke="#3E3D3A" stroke-width="1.4"/>')
    return "".join(t)

def windungen_schnitt(x, y, w, h, dicke=4.0):
    """Schnitt durch eine Rolle: die Windungen stehen als Streifen."""
    t = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#leder)" stroke="#3E3D3A" stroke-width="1.4"/>']
    k = x + mm(dicke)
    while k < x + w - 1:
        t.append(f'<line x1="{k:.1f}" y1="{y}" x2="{k:.1f}" y2="{y+h}" stroke="#4A4A46" stroke-width="0.9" opacity="0.75"/>')
        k += mm(dicke)
    return "".join(t)

def krinkel(x, y, w, h, n=90, seed=1, farbe="#C9A771"):
    """Kraft-Krinkelpapier als Fuellmaterial."""
    import random
    r = random.Random(seed)
    t = []
    for _ in range(n):
        px, py = x + r.random()*w, y + r.random()*h
        l = 14 + r.random()*20
        w0 = r.random()*math.pi
        dx, dy = math.cos(w0)*l, math.sin(w0)*l*0.5
        t.append(f'<path d="M{px:.0f},{py:.0f} q{dx*0.5:.0f},{-6-r.random()*8:.0f} {dx:.0f},{dy:.0f}" '
                 f'fill="none" stroke="{farbe}" stroke-width="{1.4+r.random()*1.4:.1f}" '
                 f'opacity="{0.45+r.random()*0.45:.2f}" stroke-linecap="round"/>')
    return "".join(t)

def masslinie(x1, y1, x2, y2, text, seite="unten", fs=15):
    t = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7A6A55" stroke-width="1.1"/>']
    if y1 == y2:
        for x in (x1, x2):
            t.append(f'<line x1="{x}" y1="{y1-6}" x2="{x}" y2="{y1+6}" stroke="#7A6A55" stroke-width="1.1"/>')
        ty = y1 - 9 if seite == "oben" else y1 + 20
        t.append(f'<text x="{(x1+x2)/2}" y="{ty}" font-size="{fs}" fill="#5E5648" text-anchor="middle">{text}</text>')
    else:
        for y in (y1, y2):
            t.append(f'<line x1="{x1-6}" y1="{y}" x2="{x1+6}" y2="{y}" stroke="#7A6A55" stroke-width="1.1"/>')
        t.append(f'<text x="{x1-10}" y="{(y1+y2)/2+5}" font-size="{fs}" fill="#5E5648" text-anchor="end" '
                 f'transform="rotate(-90 {x1-10} {(y1+y2)/2+5})">{text}</text>')
    return "".join(t)

# ───────────────────── 1 · Draufsicht ─────────────────────
PX, PY = 80, 230
iw, ih = mm(INNEN_L), mm(INNEN_B)
a(f'  <g transform="translate({PX},{PY})">')
a('    <text x="0" y="-20" font-size="19" font-weight="bold" fill="#211C15">1 · Draufsicht in die offene Kiste</text>')
a("    " + kiste_wand(0, 0, iw, ih))
a("    " + krinkel(4, 4, iw-8, ih-8, n=120, seed=3))
# Leine links
lx = mm(20) + mm(LEINE_D)/2
a("    " + rolle_oben(lx, ih/2, LEINE_D, 70))
# Messing-Karabiner oben auf der Leinenrolle
for _s in (-1, 1):
    _x0 = lx - mm(LEINE_D)/2 - 4 if _s < 0 else lx + mm(35)
    a(f'    <rect x="{_x0}" y="{ih/2-mm(9)}" width="{mm(LEINE_D)/2-mm(35)+4}" height="{mm(18)}" '
      f'fill="#D9C7A6" stroke="#A98A62" stroke-width="1.2" opacity="0.95"/>')
a(f'    <text x="{lx}" y="{ih/2+5}" font-size="15" fill="#5E5648" text-anchor="middle">LE-01</text>')
# Halsband rechts
hx = iw - mm(20) - mm(HALSBAND_D)/2
a("    " + rolle_oben(hx, ih/2, HALSBAND_D, 60))
a(f'    <rect x="{hx-mm(13)}" y="{ih/2-mm(HALSBAND_D)/2-mm(4)}" width="{mm(26)}" height="{mm(19)}" rx="2.5" '
  f'fill="url(#messing)" stroke="#6E5418" stroke-width="1.4"/>')
a(f'    <rect x="{hx-mm(8)}" y="{ih/2-mm(HALSBAND_D)/2+mm(0.5)}" width="{mm(16)}" height="{mm(9)}" rx="1.5" '
  f'fill="#E9DCC4" stroke="#6E5418" stroke-width="1"/>')
a(f'    <text x="{hx}" y="{ih/2+5}" font-size="15" fill="#5E5648" text-anchor="middle">HB-01</text>')
# Masse
a("    " + masslinie(-9, ih+42, iw+9, ih+42, "260 innen (267 außen)"))
a("    " + masslinie(-42, -9, -42, ih+9, "180 innen"))
a("    " + masslinie(lx-mm(LEINE_D)/2, -26, lx+mm(LEINE_D)/2, -26, "⌀ 145 max.", "oben", 14))
a("    " + masslinie(hx-mm(HALSBAND_D)/2, -26, hx+mm(HALSBAND_D)/2, -26, "⌀ 95 max.", "oben", 14))
a('  </g>')

# ───────────────────── 2 · Schnitt ─────────────────────
QX, QY = 960, 230
sh = mm(INNEN_H)
a(f'  <g transform="translate({QX},{QY})">')
a('    <text x="0" y="-86" font-size="19" font-weight="bold" fill="#211C15">2 · Schnitt A–A — die Größe XL setzt die Höhe</text>')
a("    " + kiste_wand(0, 0, iw, sh))
# Deckel angedeutet
a(f'    <g opacity="0.5"><rect x="-14" y="-56" width="{iw+28}" height="22" rx="3" fill="url(#kraft)" '
  f'filter="url(#pappe)"/><text x="{iw-6}" y="-40" font-size="14" fill="#7A6A55" text-anchor="end">Stülpdeckel, darüber die Banderole</text></g>')
# Krinkelbett unter der Leine
a(f'    <rect x="2" y="{sh-mm(10)}" width="{mm(LEINE_D)+mm(40)}" height="{mm(10)}" fill="#DCC49A" opacity="0.7"/>')
# Leine liegend
a("    " + windungen_schnitt(mm(20), sh-mm(30), mm(LEINE_D), mm(20)))
a(f'    <text x="{mm(20)+mm(LEINE_D)/2}" y="{sh-mm(30)-10}" font-size="14" fill="#5E5648" text-anchor="middle">'
  'LE-01 liegend · 20 hoch</text>')
# Halsband stehend (XL: 80 breit = 80 hoch)
hsx = iw - mm(20) - mm(HALSBAND_D)
a("    " + windungen_schnitt(hsx, sh-mm(80), mm(HALSBAND_D), mm(80)))
a(f'    <text x="{hsx+mm(HALSBAND_D)/2}" y="{sh-mm(80)-10}" font-size="14" fill="#5E5648" text-anchor="middle">'
  'HB-01 XL stehend · 80 hoch</text>')
# Krinkel im Luftraum ueber der Leine
a("    " + krinkel(mm(8), mm(6), mm(125), sh-mm(38), n=60, seed=9))
a("    " + masslinie(iw+36, -9, iw+36, sh+9, "85 innen (92 außen)"))
a(f'    <line x1="0" y1="{sh-mm(80)}" x2="{iw}" y2="{sh-mm(80)}" stroke="#A3452E" stroke-width="1.2" '
  'stroke-dasharray="7 5"/>')
a(f'    <text x="6" y="{sh-mm(80)-6}" font-size="13" fill="#A3452E">80 mm — verbreiterte Mitte XL</text>')
a('  </g>')

# ───────────────────── 3 · Vier Groessen ─────────────────────
GX, GY = 960, 640
a(f'  <g transform="translate({GX},{GY})">')
a('    <text x="0" y="-20" font-size="19" font-weight="bold" fill="#211C15">'
  '3 · Alle vier Größen aufgerollt, gleiche Kiste</text>')
s3 = 1.5
basis = 150
grenze = basis - 85*s3
a(f'    <line x1="0" y1="{grenze}" x2="700" y2="{grenze}" stroke="#A3452E" stroke-width="1.2" stroke-dasharray="7 5"/>')
a(f'    <text x="706" y="{grenze+5}" font-size="13" fill="#A3452E">Innenhöhe 85</text>')
a(f'    <line x1="0" y1="{basis}" x2="700" y2="{basis}" stroke="#8E7352" stroke-width="2"/>')
x = 10
for name, d, hoehe in (("S", 79, 40), ("M", 82, 50), ("L", 84, 60), ("XL", 86, 80)):
    bw, bh = d*s3, hoehe*s3
    a("    " + windungen_schnitt(x, basis-bh, bw, bh))
    a(f'    <text x="{x+bw/2}" y="{basis+20}" font-size="15" font-weight="bold" fill="#211C15" '
      f'text-anchor="middle">{name}</text>')
    a(f'    <text x="{x+bw/2}" y="{basis+38}" font-size="13" fill="#5E5648" text-anchor="middle">'
      f'⌀{d} · {hoehe} hoch</text>')
    x += bw + 48
a(f'    <text x="0" y="{basis+74}" font-size="14" fill="#5E5648">'
  'Die Höhe jeder Rolle ist die Breite der verbreiterten Mitte. '
  'Das kleinste Halsband lässt 45 mm Luft — die füllt das Krinkelpapier.</text>')
a('  </g>')

# ───────────────────── 4 · Fuellmaterial ─────────────────────
FX, FY = 80, 920
karten = [
    ("Kraft-Krinkelpapier natur", "ungebleicht, ungefärbt, 2 mm Schnitt\n20–30 g je Kiste · ca. 0,05 €\n1,80–3,20 USD/kg ab Werk", True, "krinkel"),
    ("Honeycomb-Wickelpapier", "geschlitztes Kraftpapier, umschließt\ndas Produkt statt Luftpolster\nca. 0,07 € je Kiste", False, "honig"),
    ("Holzwolle (Aspen)", "sieht am handwerklichsten aus,\naber staubt auf Fettleder\n3–5× teurer — nur Alternative", False, "holz"),
    ("Seidenpapier ungebleicht", "um das Produkt, mit Siegelmarke\ndas Knüllen ist der halbe Reiz\nca. 0,04 € je Kiste", True, "seide"),
]
a(f'  <g transform="translate({FX},{FY})">')
a('    <text x="0" y="-20" font-size="19" font-weight="bold" fill="#211C15">'
  '4 · Natürliches Füllmaterial — günstig, leicht, sieht teuer aus</text>')
kw, kh, lu = 380, 196, 45
for i, (titel, text, empf, art) in enumerate(karten):
    x = i * (kw + lu)
    a(f'    <g transform="translate({x},0)">')
    a(f'      <rect x="0" y="0" width="{kw}" height="{kh}" rx="6" fill="#FBF8F2" '
      f'stroke="{"#7E8F5A" if empf else "#D8CFC0"}" stroke-width="{2.4 if empf else 1.4}"/>')
    a(f'      <rect x="12" y="12" width="{kw-24}" height="78" rx="4" fill="#EFE4CF"/>')
    a(f'      <clipPath id="c{i}"><rect x="12" y="12" width="{kw-24}" height="78" rx="4"/></clipPath>')
    a(f'      <g clip-path="url(#c{i})">')
    if art == "krinkel":
        a("        " + krinkel(12, 12, kw-24, 78, n=110, seed=21))
    elif art == "honig":
        import math as _m
        hx0 = 20
        while hx0 < kw - 20:
            hy0 = 18
            while hy0 < 92:
                a(f'        <path d="M{hx0},{hy0} l9,5 l0,10 l-9,5 l-9,-5 l0,-10 z" fill="none" '
                  f'stroke="#B99A6E" stroke-width="1.3"/>')
                hy0 += 20
            hx0 += 27
    elif art == "holz":
        import random as _r
        rr = _r.Random(5)
        for _ in range(34):
            y0 = 18 + rr.random()*66
            x0 = 14 + rr.random()*40
            a(f'        <path d="M{x0:.0f},{y0:.0f} c{22+rr.random()*14:.0f},{-12-rr.random()*10:.0f} '
              f'{44+rr.random()*18:.0f},{14+rr.random()*10:.0f} {74+rr.random()*20:.0f},{rr.random()*6-3:.0f} '
              f'c{20+rr.random()*14:.0f},{-11-rr.random()*9:.0f} {42+rr.random()*18:.0f},{13+rr.random()*9:.0f} '
              f'{70+rr.random()*20:.0f},{rr.random()*6-3:.0f}" fill="none" '
              f'stroke="#CDB184" stroke-width="{1.2+rr.random()*0.9:.1f}" opacity="0.85" stroke-linecap="round"/>')
    else:
        for k in range(7):
            a(f'        <path d="M{14+k*52},12 C{34+k*52},40 {-6+k*52},62 {14+k*52},90" fill="none" '
              f'stroke="#DCD2C2" stroke-width="7" opacity="0.9"/>')
    a('      </g>')
    a(f'      <text x="14" y="116" font-size="16" font-weight="bold" fill="#211C15">{titel}</text>')
    for j, zeile in enumerate(text.split("\n")):
        a(f'      <text x="14" y="{138+j*19}" font-size="13.5" fill="#5E5648">{zeile}</text>')
    if empf:
        a(f'      <text x="{kw-14}" y="116" font-size="13" font-weight="bold" fill="#5E7A3A" '
          f'text-anchor="end">Empfehlung</text>')
    a('    </g>')
a('  </g>')
a('</svg>')

ziel = pathlib.Path("/home/user/Orchestrator/sourcing/bellowerk/ansichten/VERP-01-eine-groesse.svg")
ziel.write_text("\n".join(o), encoding="utf-8")
print("geschrieben:", ziel, len("\n".join(o)), "Zeichen")
