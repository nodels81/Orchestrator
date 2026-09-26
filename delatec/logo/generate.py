"""Erzeugt die DelaTec-Logo-SVGs. Buchstaben sind als Pfade gezeichnet (keine Schrift nötig)."""
ANTHRAZIT = "#1E2227"
ROT = "#E3242B"
WEISS = "#FFFFFF"

# Buchstaben auf 100er Versalhöhe, Strichstärke 20
D = "M0 0H45Q80 0 80 35V65Q80 100 45 100H0Z M20 20V80H43Q60 80 60 60V40Q60 20 43 20Z"
GLYPHEN = {
    "D": (80, D),
    "E": (62, "M0 0H62V20H20V40H55V60H20V80H62V100H0Z"),
    "L": (60, "M0 0H20V80H60V100H0Z"),
    "A": (84, "M0 100L32 0H52L84 100H63L57 80H27L21 100Z M32.5 62H51.5L42 31Z"),
    "T": (66, "M0 0H66V20H43V100H23V20H0Z"),
    "C": (76, "M76 0H40Q0 0 0 40V60Q0 100 40 100H76V80H42Q20 80 20 58V42Q20 20 42 20H76Z"),
}
ABSTAND = {"LA": 8, "AT": 4}  # optische Unterschneidung


def wortmarke(x0, y0, s, farbe_dela, farbe_tec):
    teile, x, vorher = [], 0.0, None
    for i, z in enumerate("DELATEC"):
        breite, pfad = GLYPHEN[z]
        if vorher:
            x += ABSTAND.get(vorher + z, 14)
        farbe = farbe_dela if i < 4 else farbe_tec
        teile.append(f'<path fill="{farbe}" fill-rule="evenodd" transform="translate({x0 + x * s:.2f} {y0}) scale({s})" d="{pfad}"/>')
        x += breite
        vorher = z
    return "\n  ".join(teile), x * s


def bildmarke(x0, y0, groesse, eckradius, cid):
    """Anthrazit-Kachel mit weißem D; oben links ein rotes, frisch lackiertes Segment."""
    s = groesse * 0.8 / 120
    dx = x0 + (groesse - 80 * s) / 2 + 2 * s
    dy = y0 + (groesse - 100 * s) / 2
    return f'''<rect x="{x0}" y="{y0}" width="{groesse}" height="{groesse}" rx="{eckradius}" fill="{ANTHRAZIT}"/>
  <clipPath id="{cid}"><path fill-rule="evenodd" d="{D}"/></clipPath>
  <g transform="translate({dx:.2f} {dy:.2f}) scale({s:.4f})" clip-path="url(#{cid})">
    <rect x="-5" y="-5" width="90" height="110" fill="{WEISS}"/>
    <path fill="{ROT}" d="M-5 -5H85V12L-5 57Z"/>
    <path stroke="{ANTHRAZIT}" stroke-width="5" d="M-5 57L85 12"/>
  </g>'''


def svg(breite, hoehe, inhalt, hintergrund=None):
    bg = f'<rect width="{breite}" height="{hoehe}" fill="{hintergrund}"/>\n  ' if hintergrund else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}">\n'
            f'  <title>DelaTec</title>\n  {bg}{inhalt}\n</svg>\n')


def claim(x, y, breite, farbe):
    return (f'<text x="{x}" y="{y}" fill="{farbe}" font-family="Helvetica, Arial, sans-serif" font-size="15" '
            f'font-weight="600" letter-spacing="4.2" textLength="{breite:.1f}" lengthAdjust="spacing">'
            f'SMART REPAIR · DELLEN · LACK</text>')


def quer(negativ):
    grund = ANTHRAZIT if negativ else None
    schrift = WEISS if negativ else ANTHRAZIT
    marke = bildmarke(0, 0, 120, 26, "dq")
    wort, b = wortmarke(150, 18, 0.62, schrift, ROT)
    inhalt = f"{marke}\n  {wort}\n  {claim(151, 110, b - 2, schrift)}"
    if negativ:
        return svg(150 + b + 40, 180, f'<g transform="translate(20 30)">{inhalt}</g>', grund)
    return svg(150 + b, 120, inhalt)


dateien = {
    "delatec-logo.svg": quer(False),
    "delatec-logo-negativ.svg": quer(True),
    "delatec-icon.svg": svg(120, 120, bildmarke(0, 0, 120, 26, "di")),
    # Instagram-Profilbild: vollflächig, Inhalt sitzt im Kreisausschnitt
    "delatec-instagram-profil.svg": svg(120, 120, bildmarke(0, 0, 120, 0, "dp")),
}
wort, b = wortmarke(0, 0, 1, ANTHRAZIT, ROT)
dateien["delatec-wortmarke.svg"] = svg(round(b), 100, wort)

for name, inhalt in dateien.items():
    open(name, "w").write(inhalt)
    print(name)
