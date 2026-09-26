"""Velocity, fiffig: drei Varianten mit einer versteckten Idee im Detail."""
from konzepte import ACID, _punkte, aussenkontur, loecher, nach_x
from typo import grenzen, matrix, minus, plus, rechteck, schnitt, verschieben, vieleck
from velocity_elegant import NEIGUNG, anybody, breite, claim_fein, mona_il, schraeg


# 05g  QUERSTRICH – nur der Querstrich des A ist grün: die Wasserwaage in der Mitte des Namens
def v_querstrich():
    K = 100.0
    f = anybody(600)
    gesamt, teile = f.satz("DELATEC", K, sperrung=0.06, einzeln=True)
    x_off = -grenzen(gesamt)[0]
    teile = [verschieben(t, x_off, 0) for t in teile]
    A = teile[3]
    aussen = _punkte(aussenkontur(A))
    punze = _punkte(loecher(A)[0])
    y_oben = max(p[1] for p in punze)                     # Unterkante der Punze
    unten_p = sorted(p for p in punze if abs(p[1] - y_oben) < 0.5)
    pl, pr = unten_p[0], unten_p[-1]
    innen = [p for p in aussen if y_oben + 0.5 < p[1] < K - 0.5 and pl[0] - 20 < p[0] < pr[0] + 20]
    y_unten = min(p[1] for p in innen)                    # Oberkante der Öffnung darunter
    ol = min((p for p in innen if abs(p[1] - y_unten) < 0.5))
    orr = max((p for p in innen if abs(p[1] - y_unten) < 0.5))
    # Querstrich = Viereck zwischen den Innenkanten der Beine
    streifen = vieleck((pl[0] - 0.5, y_oben), (pr[0] + 0.5, y_oben), (orr[0] + 0.5, y_unten), (ol[0] - 0.5, y_unten))
    g = 0.02 * K
    gruen = schnitt(streifen, rechteck(-1e4, y_oben + g, 2e4, y_unten - y_oben - 2 * g))
    teile[3] = minus(A, streifen)
    wort = plus(*teile)
    x0, _, x1, _ = grenzen(wort)
    claim = claim_fein(mona_il, (x1 - x0) * 0.58)
    claim = nach_x(claim, x1 - breite(claim) - NEIGUNG * 0.3 * K, K + 0.30 * K)
    return [(wort, "tinte"), (gruen, "akzent"), (claim, "tinte")]


# 05h  SPALTMASS – eine haarfeine, exakt gleichmäßige Fuge läuft durch den Namen,
#      wie das perfekte Spaltmaß zwischen zwei Karosserieteilen. Grün läuft sie aus.
def v_spaltmass():
    K = 100.0
    wort = nach_x(anybody(720).satz("DELATEC", K, sperrung=0.05), 0)
    x0, _, x1, _ = grenzen(wort)
    y, h = 0.57 * K, 0.028 * K
    fuge = rechteck(x0 - 10, y, x1 - x0 + 20, h)
    wort = minus(wort, fuge)
    auslauf = rechteck(x1 + 0.10 * K, y, 0.55 * K, h)
    claim = claim_fein(mona_il, (x1 - x0) * 0.58)
    claim = nach_x(claim, x1 - breite(claim) - NEIGUNG * 0.3 * K, K + 0.30 * K)
    return [(wort, "tinte"), (auslauf, "akzent"), (claim, "tinte")]


# 05i  HOCHGLANZ – der Name spiegelt sich wie in frisch poliertem Lack, die Spiegelung
#      zerfällt in Reflexlinien. Die grüne Linie ist der Horizont.
def v_hochglanz():
    K = 100.0
    wort = nach_x(anybody(560).satz("DELATEC", K, sperrung=0.06), 0)
    x0, _, x1, _ = grenzen(wort)
    horizont_y, hh = K + 0.07 * K, 0.035 * K
    horizont = schraeg(x0 - 0.05 * K, horizont_y, x1 + 0.05 * K, hh)
    achse = horizont_y + hh + 0.07 * K
    spiegel = matrix(wort, d=-1, f=achse + K)             # an der Achse gespiegelt, Kopf nach unten
    linien, y, hb = [], achse, 0.085 * K
    for anteil in (0.55, 0.38, 0.25, 0.14):
        linien.append(rechteck(x0 - 50, y, x1 - x0 + 100, hb * anteil))
        y += hb
    reflex = schnitt(spiegel, plus(*linien))
    claim = claim_fein(mona_il, (x1 - x0) * 0.50)
    claim = nach_x(claim, x1 - breite(claim), y + 0.14 * K)
    return [(wort, "tinte"), (horizont, "akzent"), (reflex, "tinte"), (claim, "tinte")]


VARIANTEN = {
    "05g-querstrich": ("Querstrich", v_querstrich),
    "05h-spaltmass": ("Spaltmaß", v_spaltmass),
    "05i-hochglanz": ("Hochglanz", v_hochglanz),
}
