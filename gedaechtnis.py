"""
gedaechtnis.py — Das Gedaechtnis des Betriebs.

Warum es das gibt: Bisher fing jeder Auftrag bei null an. Markenwissen und
Einkaufsunterlagen wurden bei jedem Aufruf komplett neu bezahlt (Abteilung 05:
rund 7.000 Eingabe-Tokens pro Auftrag), und was eine Abteilung gestern
herausgefunden hat, war heute wieder vergessen.

Das Gedaechtnis loest drei Dinge:

  1. EPISODEN  — jedes Ergebnis wird gespeichert und ist durchsuchbar.
  2. FAKTEN    — kurze Aussagen (Lieferant X, MOQ, 100 Stueck) als kleiner
                 Wissensgraph mit Gueltigkeitszeitraum. Ein neuer Preis setzt
                 den alten auf 'gueltig bis heute', statt ihn zu ueberschreiben.
                 So bleibt nachvollziehbar, was wann galt.
  3. ANTWORTEN — ein identischer Auftrag wird aus dem Speicher beantwortet,
                 ohne einen einzigen Token zu verbrauchen.

Statt der kompletten Unterlagen wandern nur die passenden Faktenzeilen und
Kurzfassungen in den Prompt — wenige hundert Zeichen statt zehntausender.

Technik: sqlite3 aus der Standardbibliothek, Volltextsuche ueber FTS5.
Keine zusaetzlichen Pakete, kein Server, keine Cloud. Die Datei
gedaechtnis.db bleibt wie config.json auf dem Server und geht nicht ins Git.
"""

import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timedelta

BASIS = os.path.dirname(os.path.abspath(__file__))
DATENBANK = os.environ.get("BELLO_GEDAECHTNIS") or os.path.join(BASIS, "gedaechtnis.db")

# Wie lange eine gespeicherte Antwort wiederverwendet werden darf.
ANTWORT_HALTBARKEIT_TAGE = 7

# Praedikate, von denen es nur einen gueltigen Wert geben kann. Kommt ein neuer
# Wert, wird der alte auf 'abgeloest' gesetzt statt geloescht — die Historie
# bleibt lesbar ("MOQ war 300, seit 12.09. 100").
EINDEUTIGE_PRAEDIKATE = {
    "preis", "stueckpreis", "moq", "mindestmenge", "lieferzeit", "status",
    "kontakt", "ansprechpartner", "email", "zahlungsziel", "muster", "musterpreis",
}

STOPWORTE = {
    "und", "oder", "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
    "einem", "eines", "fuer", "für", "mit", "von", "vom", "zum", "zur", "auf", "aus",
    "bei", "nach", "ueber", "über", "wird", "werden", "sind", "ist", "war", "hat",
    "haben", "nicht", "kein", "keine", "auch", "noch", "dann", "wenn", "als", "wie",
    "sich", "sowie", "an", "am", "im", "in", "zu", "es", "er", "sie", "wir", "man",
    "the", "and", "for", "with", "from", "this", "that", "our",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS episoden (
    id              INTEGER PRIMARY KEY,
    auftrag_id      TEXT,
    abteilung       TEXT,
    ziel            TEXT,
    zusammenfassung TEXT,
    inhalt          TEXT,
    bestanden       INTEGER DEFAULT 0,
    zeit            TEXT,
    tokens_ein      INTEGER DEFAULT 0,
    tokens_aus      INTEGER DEFAULT 0,
    tokens_cache    INTEGER DEFAULT 0
);

CREATE VIRTUAL TABLE IF NOT EXISTS episoden_fts USING fts5(
    ziel, zusammenfassung, inhalt,
    tokenize = "unicode61 remove_diacritics 2"
);

CREATE TABLE IF NOT EXISTS knoten (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    art     TEXT DEFAULT 'unbekannt',
    zuletzt TEXT,
    UNIQUE(name COLLATE NOCASE)
);

CREATE TABLE IF NOT EXISTS kanten (
    id         INTEGER PRIMARY KEY,
    von        INTEGER NOT NULL REFERENCES knoten(id),
    praedikat  TEXT NOT NULL,
    nach       INTEGER NOT NULL REFERENCES knoten(id),
    aussage    TEXT NOT NULL,
    quelle     TEXT,
    abteilung  TEXT,
    gueltig_ab TEXT,
    gueltig_bis TEXT,
    erfasst    TEXT
);

CREATE INDEX IF NOT EXISTS kanten_aktuell ON kanten(von, praedikat, gueltig_bis);

CREATE VIRTUAL TABLE IF NOT EXISTS kanten_fts USING fts5(
    aussage,
    tokenize = "unicode61 remove_diacritics 2"
);

CREATE TABLE IF NOT EXISTS antworten (
    schluessel TEXT PRIMARY KEY,
    abteilung  TEXT,
    ziel       TEXT,
    ergebnis   TEXT,
    zeit       TEXT,
    treffer    INTEGER DEFAULT 0,
    tokens_ein INTEGER DEFAULT 0,
    tokens_aus INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sparbuch (
    id        INTEGER PRIMARY KEY,
    zeit      TEXT,
    art       TEXT,
    abteilung TEXT,
    tokens    INTEGER DEFAULT 0,
    notiz     TEXT
);
"""


# ---------- Verbindung ----------

def verbindung(pfad: str | None = None) -> sqlite3.Connection:
    verb = sqlite3.connect(pfad or DATENBANK)
    verb.row_factory = sqlite3.Row
    verb.executescript(SCHEMA)
    return verb


def _jetzt() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Gedaechtnis:
    """Ein geoeffnetes Gedaechtnis. Nutzbar als 'with Gedaechtnis() as g:'."""

    def __init__(self, pfad: str | None = None):
        self.pfad = pfad or DATENBANK
        self.verb = verbindung(self.pfad)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.schliessen()

    def schliessen(self) -> None:
        self.verb.commit()
        self.verb.close()

    # ---------- Episoden ----------

    def episode_merken(self, auftrag: dict, ergebnis: dict,
                       bestanden: bool = True, verbrauch: dict | None = None) -> int:
        """Legt das Ergebnis eines Auftrags ab und macht es durchsuchbar."""
        inhalt = str(ergebnis.get("ergebnis", ""))[:20_000]
        zusammenfassung = ergebnis.get("zusammenfassung") or kurzfassung(inhalt)
        verbrauch = verbrauch or {}
        zeiger = self.verb.execute(
            "INSERT INTO episoden (auftrag_id, abteilung, ziel, zusammenfassung, inhalt,"
            " bestanden, zeit, tokens_ein, tokens_aus, tokens_cache)"
            " VALUES (?,?,?,?,?,?,?,?,?,?)",
            (auftrag.get("id"), auftrag.get("abteilung"), auftrag.get("ziel", ""),
             zusammenfassung, inhalt, 1 if bestanden else 0, _jetzt(),
             verbrauch.get("ein", 0), verbrauch.get("aus", 0), verbrauch.get("cache_gelesen", 0)),
        )
        nummer = zeiger.lastrowid
        self.verb.execute(
            "INSERT INTO episoden_fts (rowid, ziel, zusammenfassung, inhalt) VALUES (?,?,?,?)",
            (nummer, auftrag.get("ziel", ""), zusammenfassung, inhalt),
        )
        if verbrauch.get("cache_gelesen"):
            # Zwischengespeicherte Tokens kosten rund ein Zehntel. Neun Zehntel gespart.
            self._buchen("prompt_cache", auftrag.get("abteilung"),
                         int(verbrauch["cache_gelesen"] * 0.9),
                         f"{verbrauch['cache_gelesen']} Tokens aus dem Prompt-Cache")
        self.verb.commit()
        return nummer

    # ---------- Fakten ----------

    def fakten_merken(self, fakten, quelle: str = "", abteilung: str = "") -> int:
        """Nimmt Aussagen auf. Ein neuer Wert loest den alten ab, statt ihn zu loeschen."""
        anzahl = 0
        for roh in fakten or []:
            fakt = _fakt_lesen(roh)
            if not fakt:
                continue
            subjekt, praedikat, objekt = fakt
            von = self._knoten(subjekt)
            nach = self._knoten(objekt)
            aussage = f"{subjekt} — {praedikat}: {objekt}"

            schon_da = self.verb.execute(
                "SELECT id FROM kanten WHERE von=? AND praedikat=? AND nach=? AND gueltig_bis IS NULL",
                (von, praedikat, nach),
            ).fetchone()
            if schon_da:
                continue

            if praedikat.lower() in EINDEUTIGE_PRAEDIKATE:
                self.verb.execute(
                    "UPDATE kanten SET gueltig_bis=? WHERE von=? AND praedikat=? AND gueltig_bis IS NULL",
                    (_jetzt(), von, praedikat),
                )

            zeiger = self.verb.execute(
                "INSERT INTO kanten (von, praedikat, nach, aussage, quelle, abteilung,"
                " gueltig_ab, gueltig_bis, erfasst) VALUES (?,?,?,?,?,?,?,NULL,?)",
                (von, praedikat, nach, aussage, quelle, abteilung, _jetzt(), _jetzt()),
            )
            self.verb.execute("INSERT INTO kanten_fts (rowid, aussage) VALUES (?,?)",
                              (zeiger.lastrowid, aussage))
            anzahl += 1
        self.verb.commit()
        return anzahl

    def _knoten(self, name: str) -> int:
        name = name.strip()[:200]
        self.verb.execute(
            "INSERT INTO knoten (name, zuletzt) VALUES (?,?) "
            "ON CONFLICT(name) DO UPDATE SET zuletzt=excluded.zuletzt",
            (name, _jetzt()),
        )
        zeile = self.verb.execute(
            "SELECT id FROM knoten WHERE name=? COLLATE NOCASE", (name,)
        ).fetchone()
        return zeile["id"]

    def verlauf(self, subjekt: str, praedikat: str | None = None) -> list[sqlite3.Row]:
        """Was galt wann. Auch die abgeloesten Aussagen, juengste zuerst."""
        frage = ("SELECT k.aussage, k.gueltig_ab, k.gueltig_bis, k.quelle FROM kanten k "
                 "JOIN knoten n ON n.id = k.von WHERE n.name = ? COLLATE NOCASE")
        werte: list = [subjekt]
        if praedikat:
            frage += " AND k.praedikat = ?"
            werte.append(praedikat)
        return self.verb.execute(frage + " ORDER BY k.gueltig_ab DESC", werte).fetchall()

    # ---------- Abruf ----------

    def kontext(self, ziel: str, abteilung: str | None = None,
                budget_zeichen: int = 2500) -> str:
        """Der Gedaechtnisblock fuer den Prompt: nur was zum Ziel passt."""
        suche = _fts_frage(ziel)
        if not suche:
            return ""

        fakten = self._suchen(
            "SELECT k.aussage, k.gueltig_ab, k.quelle FROM kanten_fts f "
            "JOIN kanten k ON k.id = f.rowid "
            "WHERE kanten_fts MATCH ? AND k.gueltig_bis IS NULL "
            "ORDER BY bm25(kanten_fts) LIMIT 12", (suche,))

        frage = ("SELECT e.auftrag_id, e.abteilung, e.zeit, e.ziel, e.zusammenfassung "
                 "FROM episoden_fts f JOIN episoden e ON e.id = f.rowid "
                 "WHERE episoden_fts MATCH ? AND e.bestanden = 1 ")
        werte: list = [suche]
        if abteilung:
            frage += "AND e.abteilung = ? "
            werte.append(abteilung)
        episoden = self._suchen(frage + "ORDER BY bm25(episoden_fts) LIMIT 5", tuple(werte))

        if not fakten and not episoden:
            return ""

        zeilen = ["GEDAECHTNIS — bereits bekannt, nicht neu erfinden:"]
        if fakten:
            zeilen.append("")
            zeilen.append("FAKTEN (Stand jeweils in Klammern):")
            for f in fakten:
                datum = (f["gueltig_ab"] or "")[:10]
                herkunft = f" / {f['quelle']}" if f["quelle"] else ""
                zeilen.append(f"  - {f['aussage']}  ({datum}{herkunft})")
        if episoden:
            zeilen.append("")
            zeilen.append("FRUEHER SCHON BEARBEITET:")
            for e in episoden:
                zeilen.append(f"  - {e['auftrag_id']} ({e['abteilung']}, {(e['zeit'] or '')[:10]}): "
                              f"{e['ziel'][:80]}")
                zeilen.append(f"    {e['zusammenfassung']}")
        zeilen.append("")
        zeilen.append("Baue darauf auf. Widerspricht dein Ergebnis einem Fakt, "
                      "sag das ausdruecklich in 'anmerkung'.")

        text = "\n".join(zeilen)
        if len(text) > budget_zeichen:
            text = text[:budget_zeichen].rsplit("\n", 1)[0] + "\n  [gekuerzt]"
        return text

    def _suchen(self, frage: str, werte: tuple) -> list[sqlite3.Row]:
        try:
            return self.verb.execute(frage, werte).fetchall()
        except sqlite3.OperationalError:
            # Unbrauchbarer Suchausdruck darf den Auftrag nie stoppen.
            return []

    def suchen(self, text: str, grenze: int = 10) -> dict:
        """Fuer 'orchestrator.py --wissen': freie Suche im Gedaechtnis."""
        suche = _fts_frage(text)
        if not suche:
            return {"fakten": [], "episoden": []}
        return {
            "fakten": self._suchen(
                "SELECT k.aussage, k.gueltig_ab, k.gueltig_bis, k.quelle FROM kanten_fts f "
                "JOIN kanten k ON k.id = f.rowid WHERE kanten_fts MATCH ? "
                "ORDER BY bm25(kanten_fts) LIMIT ?", (suche, grenze)),
            "episoden": self._suchen(
                "SELECT e.auftrag_id, e.abteilung, e.zeit, e.ziel, e.zusammenfassung "
                "FROM episoden_fts f JOIN episoden e ON e.id = f.rowid "
                "WHERE episoden_fts MATCH ? ORDER BY bm25(episoden_fts) LIMIT ?",
                (suche, grenze)),
        }

    # ---------- Antwortspeicher ----------

    def antwort_holen(self, auftrag: dict, modell: str) -> dict | None:
        """Identischer Auftrag schon einmal sauber beantwortet? Dann ohne API-Aufruf."""
        schluessel = _schluessel(auftrag, modell)
        zeile = self.verb.execute(
            "SELECT * FROM antworten WHERE schluessel=?", (schluessel,)
        ).fetchone()
        if not zeile:
            return None
        alter = datetime.now() - datetime.fromisoformat(zeile["zeit"])
        if alter > timedelta(days=ANTWORT_HALTBARKEIT_TAGE):
            self.verb.execute("DELETE FROM antworten WHERE schluessel=?", (schluessel,))
            self.verb.commit()
            return None

        ergebnis = json.loads(zeile["ergebnis"])
        hinweis = (f"Aus dem Gedaechtnis wiederverwendet "
                   f"(erstmals {zeile['zeit'][:16]}, kein API-Aufruf).")
        ergebnis["anmerkung"] = f"{hinweis} {ergebnis.get('anmerkung') or ''}".strip()
        self.verb.execute(
            "UPDATE antworten SET treffer = treffer + 1 WHERE schluessel=?", (schluessel,))
        self._buchen("antwort_wiederverwendet", auftrag.get("abteilung"),
                     zeile["tokens_ein"] + zeile["tokens_aus"],
                     f"Auftrag {auftrag.get('id')} ohne API-Aufruf beantwortet")
        self.verb.commit()
        return ergebnis

    def antwort_merken(self, auftrag: dict, modell: str, ergebnis: dict,
                       verbrauch: dict | None = None) -> None:
        verbrauch = verbrauch or {}
        self.verb.execute(
            "INSERT OR REPLACE INTO antworten (schluessel, abteilung, ziel, ergebnis, zeit,"
            " treffer, tokens_ein, tokens_aus) VALUES (?,?,?,?,?,0,?,?)",
            (_schluessel(auftrag, modell), auftrag.get("abteilung"), auftrag.get("ziel", ""),
             json.dumps(ergebnis, ensure_ascii=False), _jetzt(),
             verbrauch.get("ein", 0), verbrauch.get("aus", 0)),
        )
        self.verb.commit()

    # ---------- Buchhaltung ----------

    def _buchen(self, art: str, abteilung: str | None, tokens: int, notiz: str) -> None:
        self.verb.execute(
            "INSERT INTO sparbuch (zeit, art, abteilung, tokens, notiz) VALUES (?,?,?,?,?)",
            (_jetzt(), art, abteilung or "", int(tokens), notiz),
        )

    def statistik(self) -> dict:
        zahl = lambda f, *w: (self.verb.execute(f, w).fetchone() or [0])[0] or 0
        gespart = self.verb.execute(
            "SELECT art, SUM(tokens) AS tokens, COUNT(*) AS anzahl FROM sparbuch GROUP BY art"
        ).fetchall()
        return {
            "episoden": zahl("SELECT COUNT(*) FROM episoden"),
            "fakten_aktuell": zahl("SELECT COUNT(*) FROM kanten WHERE gueltig_bis IS NULL"),
            "fakten_abgeloest": zahl("SELECT COUNT(*) FROM kanten WHERE gueltig_bis IS NOT NULL"),
            "knoten": zahl("SELECT COUNT(*) FROM knoten"),
            "antworten": zahl("SELECT COUNT(*) FROM antworten"),
            "tokens_ein": zahl("SELECT SUM(tokens_ein) FROM episoden"),
            "tokens_aus": zahl("SELECT SUM(tokens_aus) FROM episoden"),
            "gespart": {z["art"]: {"tokens": z["tokens"] or 0, "anzahl": z["anzahl"]}
                        for z in gespart},
            "gespart_gesamt": zahl("SELECT SUM(tokens) FROM sparbuch"),
            "datei": self.pfad,
        }

    def vergessen(self, tage: int = 180) -> int:
        """Alte Episoden und abgelaufene Antworten wegraeumen. Fakten bleiben."""
        grenze = (datetime.now() - timedelta(days=tage)).isoformat(timespec="seconds")
        alt = [z["id"] for z in self.verb.execute(
            "SELECT id FROM episoden WHERE zeit < ?", (grenze,)).fetchall()]
        for nummer in alt:
            self.verb.execute("DELETE FROM episoden_fts WHERE rowid=?", (nummer,))
            self.verb.execute("DELETE FROM episoden WHERE id=?", (nummer,))
        self.verb.execute("DELETE FROM antworten WHERE zeit < ?", (grenze,))
        self.verb.commit()
        return len(alt)


# ---------- Hilfen ----------

def _schluessel(auftrag: dict, modell: str) -> str:
    roh = json.dumps({
        "abteilung": auftrag.get("abteilung"),
        "ziel": " ".join((auftrag.get("ziel") or "").lower().split()),
        "kriterien": auftrag.get("kriterien", []),
        "modell": modell,
    }, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(roh.encode("utf-8")).hexdigest()


def _fakt_lesen(roh) -> tuple[str, str, str] | None:
    """Nimmt {'subjekt','praedikat','objekt'} oder 'Subjekt | Praedikat | Objekt'."""
    if isinstance(roh, dict):
        teile = [str(roh.get(s) or "").strip() for s in ("subjekt", "praedikat", "objekt")]
    elif isinstance(roh, str):
        teile = [t.strip() for t in roh.split("|")]
    else:
        return None
    if len(teile) != 3 or not all(teile):
        return None
    return teile[0][:200], teile[1][:80], teile[2][:200]


def _fts_frage(text: str) -> str:
    """Freitext in einen sicheren FTS5-Ausdruck. Alles Fremde faellt weg."""
    woerter = re.findall(r"[0-9A-Za-zÄÖÜäöüß_-]{3,}", text or "")
    begriffe = []
    for wort in woerter:
        klein = wort.lower()
        if klein in STOPWORTE or klein in begriffe:
            continue
        begriffe.append(klein)
    if not begriffe:
        return ""
    # Ab vier Zeichen mit Praefixsuche: 'halsband' findet auch 'halsbaender'.
    return " OR ".join(f'"{b}"*' if len(b) >= 4 else f'"{b}"' for b in begriffe[:12])


def kurzfassung(text: str, grenze: int = 400) -> str:
    """Regelbasierte Kurzfassung — kostet keine Tokens."""
    sauber = " ".join((text or "").split())
    if len(sauber) <= grenze:
        return sauber
    schnitt = sauber[:grenze]
    for zeichen in (". ", "; ", ", "):
        stelle = schnitt.rfind(zeichen)
        if stelle > grenze * 0.6:
            return schnitt[:stelle + 1].strip()
    return schnitt.rstrip() + " ..."


def bericht() -> str:
    """Lesbarer Stand des Gedaechtnisses fuer 'orchestrator.py --gedaechtnis'."""
    with Gedaechtnis() as g:
        s = g.statistik()
    zeilen = [
        "Gedaechtnis des Betriebs",
        f"  Datei:            {s['datei']}",
        f"  Episoden:         {s['episoden']}",
        f"  Fakten gueltig:   {s['fakten_aktuell']}  (abgeloest: {s['fakten_abgeloest']})",
        f"  Begriffe:         {s['knoten']}",
        f"  Antworten:        {s['antworten']}",
        "",
        f"  Tokens verbraucht: {s['tokens_ein']} ein / {s['tokens_aus']} aus",
        f"  Tokens gespart:    {s['gespart_gesamt']}",
    ]
    for art, werte in s["gespart"].items():
        zeilen.append(f"    - {art}: {werte['tokens']} Tokens in {werte['anzahl']} Faellen")
    if not s["gespart"]:
        zeilen.append("    - noch nichts gespart, das Gedaechtnis ist frisch")
    return "\n".join(zeilen)


if __name__ == "__main__":
    print(bericht())
