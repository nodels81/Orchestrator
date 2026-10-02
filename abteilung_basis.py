"""
abteilung_basis.py — Gemeinsame Mechanik. Muss nie angefasst werden.

Jede Abteilung erbt von Abteilung und liefert dieselbe Status-Struktur zurueck,
damit der Orchestrator maschinell pruefen kann statt zu interpretieren.

Drei Sparmassnahmen stecken hier drin, sichtbar in 'orchestrator.py --gedaechtnis':

  1. PROMPT-CACHE   Markenwissen und Einkaufsunterlagen stehen unveraendert am
                    Anfang jeder Anfrage. Mit cache_control liest die API sie beim
                    zweiten Mal aus dem Zwischenspeicher — rund ein Zehntel der
                    Kosten. Deshalb bleibt der System-Prompt Wort fuer Wort gleich;
                    alles Wechselnde (Auftrag, Gedaechtnis) steht dahinter.
  2. GEDAECHTNIS    Statt aller Unterlagen wandern nur die zum Ziel passenden
                    Fakten und Kurzfassungen frueherer Auftraege in den Prompt.
  3. ANTWORTSPEICHER Ein wortgleicher Auftrag wird ohne API-Aufruf beantwortet.
                    Bei Nacharbeit (versuche > 0) nie — sonst bekaeme die
                    Abteilung ewig dieselbe abgelehnte Antwort zurueck.
"""

import json
import os
import sys

import gedaechtnis as gedaechtnis_modul
import markenwissen
import modelle

BASIS = os.path.dirname(os.path.abspath(__file__))
CONFIG_PFAD = os.path.join(BASIS, "config.json")

# Wie viel Platz das Gedaechtnis im Prompt bekommen darf.
GEDAECHTNIS_BUDGET_ZEICHEN = 2_500


def config_laden() -> dict:
    if not os.path.exists(CONFIG_PFAD):
        raise FileNotFoundError(
            f"{CONFIG_PFAD} fehlt. Vorlage: config.beispiel.json kopieren und ausfuellen."
        )
    with open(CONFIG_PFAD, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as fehler:
            raise ValueError(
                f"{CONFIG_PFAD} ist kein gueltiges JSON ({fehler}). "
                "Haeufigster Grund: fehlendes Komma oder Anfuehrungszeichen."
            ) from fehler


class Abteilung:
    """Basisklasse. Ableitungen setzen NUMMER, NAME, ROLLE."""

    NUMMER = "00"
    NAME = "Basis"
    ROLLE = "Keine Rolle definiert."

    def __init__(self, config: dict | None = None):
        self.config = config or config_laden()
        self.modell = modelle.reihenfolge(self.config, f"{self.NUMMER} {self.NAME}")[0]
        self.gedaechtnis_an = self.config.get("gedaechtnis", True) is not False

    # ---------- Prompt ----------

    def system_prompt(self) -> str:
        """Der feste Teil. Aendert er sich zwischen zwei Aufrufen, ist der
        Zwischenspeicher verloren — hier gehoert nichts Wechselndes hinein."""
        return (
            f"Du bist Abteilung {self.NUMMER} ({self.NAME}) im Betrieb "
            f"{markenwissen.MARKE}.\n\n"
            f"DEINE ROLLE:\n{self.ROLLE}\n\n"
            f"MARKENWISSEN (bindend):\n{markenwissen.als_kontext()}\n\n"
            "REGELN:\n"
            "- Du gibst NUR gueltiges JSON zurueck, kein Vorwort, keine Code-Fences.\n"
            "- Du gibst niemals Geld aus und sagst keine Preise nach aussen zu.\n"
            "- Was du nicht sicher weisst, kennzeichnest du als Schaetzung.\n"
            "- Verstoesst etwas gegen die harten Ausschluesse, lehnst du es ab "
            "und begruendest das im Feld 'anmerkung'.\n"
        )

    def antwortformat(self) -> str:
        return (
            "Antworte ausschliesslich mit diesem JSON-Objekt:\n"
            "{\n"
            '  "ergebnis": "<deine Arbeit, ausformuliert>",\n'
            '  "kriterien_erfuellt": [true, false, ...],\n'
            '  "blocker": null,\n'
            '  "anmerkung": "<Einschraenkungen oder Hinweise, sonst null>",\n'
            '  "zusammenfassung": "<dein Ergebnis in hoechstens zwei Saetzen>",\n'
            '  "fakten": [\n'
            '    {"subjekt": "<worueber>", "praedikat": "<was>", "objekt": "<Wert>"}\n'
            "  ]\n"
            "}\n"
            "Die Liste kriterien_erfuellt hat genau so viele Eintraege wie Kriterien "
            "im Auftrag, in derselben Reihenfolge.\n\n"
            "Zu 'fakten': hoechstens fuenf harte, kurze Aussagen, die spaeter noch "
            "gelten — Mengen, Preise, Fristen, Zusagen, Namen. Beispiel: "
            '{"subjekt": "Wenzhou Vigorous", "praedikat": "moq", "objekt": "100 Stueck HB-01"}. '
            "Keine Absichten, keine Vermutungen, keine Wiederholung des Auftrags. "
            "Weisst du nichts Bleibendes, gib eine leere Liste."
        )

    # ---------- Ausfuehrung ----------

    def bearbeiten(self, auftrag: dict, recherche: bool = False) -> dict:
        kriterien = auftrag.get("kriterien", [])
        auswahl = modelle.Auswahl(self.config, auftrag.get("abteilung") or
                                  f"{self.NUMMER} {self.NAME}", auftrag)
        self.modell = auswahl.kennung

        # Nacharbeit muss neu denken duerfen, sonst wiederholt sich der Fehler.
        gespeichert = self._gespeicherte_antwort(auftrag)
        if gespeichert:
            print("    [Gedaechtnis] Wortgleicher Auftrag bekannt — kein API-Aufruf.")
            return gespeichert

        nutzer = (
            f"AUFTRAG {auftrag.get('id', '?')}\n"
            f"Ziel: {auftrag.get('ziel', '')}\n"
            f"Rahmen: {auftrag.get('rahmen', 'keine Ausgaben')}\n"
            f"Frist: {auftrag.get('frist', 'offen')}\n\n"
            "ABNAHMEKRITERIEN:\n"
            + "\n".join(f"  {i+1}. {k}" for i, k in enumerate(kriterien))
        )
        erinnerung = self._erinnerung(auftrag)
        if erinnerung:
            nutzer += "\n\n" + erinnerung
        nutzer += "\n\n" + self.antwortformat()

        text, verbrauch, self.modell = auswahl.anfragen(
            self.system_prompt(), nutzer, max_tokens=4000, recherche=recherche)
        print(f"    [Modell] {self.modell}")
        ergebnis = self._json_lesen(text, len(kriterien))
        self._merken(auftrag, ergebnis, verbrauch)
        return ergebnis

    def _gespeicherte_antwort(self, auftrag: dict) -> dict | None:
        if not self.gedaechtnis_an or auftrag.get("versuche"):
            return None
        try:
            with gedaechtnis_modul.Gedaechtnis() as g:
                return g.antwort_holen(auftrag, self.modell)
        except Exception as fehler:
            print(f"    [Gedaechtnis] nicht lesbar ({fehler}) — Auftrag laeuft ohne.")
            return None

    def _erinnerung(self, auftrag: dict) -> str:
        if not self.gedaechtnis_an:
            return ""
        try:
            with gedaechtnis_modul.Gedaechtnis() as g:
                return g.kontext(auftrag.get("ziel", ""), auftrag.get("abteilung"),
                                 GEDAECHTNIS_BUDGET_ZEICHEN)
        except Exception as fehler:
            # Ein kaputtes Gedaechtnis darf keinen Auftrag aufhalten.
            print(f"    [Gedaechtnis] nicht lesbar ({fehler}) — Auftrag laeuft ohne.")
            return ""

    def _merken(self, auftrag: dict, ergebnis: dict, verbrauch: dict) -> None:
        if not self.gedaechtnis_an:
            return
        sauber = not ergebnis.get("blocker") and bool(ergebnis.get("ergebnis"))
        quelle = auftrag.get("id") or "Einzeltest"
        try:
            with gedaechtnis_modul.Gedaechtnis() as g:
                g.episode_merken(auftrag, ergebnis, bestanden=sauber, verbrauch=verbrauch)
                g.fakten_merken(ergebnis.get("fakten"), quelle, auftrag.get("abteilung", ""))
                if sauber:
                    g.antwort_merken(auftrag, self.modell, ergebnis, verbrauch)
        except Exception as fehler:
            print(f"    [Gedaechtnis] nicht schreibbar ({fehler}) — Ergebnis bleibt gueltig.")

    def _json_lesen(self, text: str, anzahl_kriterien: int) -> dict:
        roh = text.strip()
        if roh.startswith("```"):
            roh = roh.split("```")[1]
            if roh.startswith("json"):
                roh = roh[4:]
            roh = roh.strip()
        try:
            daten = json.loads(roh)
        except json.JSONDecodeError:
            anfang, ende = roh.find("{"), roh.rfind("}")
            if anfang == -1 or ende == -1:
                return {
                    "ergebnis": text[:2000],
                    "kriterien_erfuellt": [False] * anzahl_kriterien,
                    "blocker": "Antwort war kein JSON",
                    "anmerkung": "Modellantwort konnte nicht gelesen werden.",
                    "zusammenfassung": "",
                    "fakten": [],
                }
            daten = json.loads(roh[anfang:ende + 1])

        erfuellt = daten.get("kriterien_erfuellt") or []
        if len(erfuellt) < anzahl_kriterien:
            erfuellt += [False] * (anzahl_kriterien - len(erfuellt))
        daten["kriterien_erfuellt"] = erfuellt[:anzahl_kriterien]
        daten.setdefault("ergebnis", "")
        daten.setdefault("blocker", None)
        daten.setdefault("anmerkung", None)
        daten.setdefault("zusammenfassung", "")
        if not isinstance(daten.get("fakten"), list):
            daten["fakten"] = []
        return daten


def einzeltest(klasse) -> None:
    """Erlaubt: venv/bin/python abteilung_xyz.py "Ziel ..." [--recherche] [--modell kimi:kimi-k2]"""
    argumente = [a for a in sys.argv[1:] if a != "--recherche"]
    modell = None
    if "--modell" in argumente:
        stelle = argumente.index("--modell")
        modell = argumente[stelle + 1] if stelle + 1 < len(argumente) else None
        del argumente[stelle:stelle + 2]
    if not argumente:
        print(f'Aufruf: python {sys.argv[0]} "Ziel des Auftrags" [--recherche] [--modell anbieter:modell]')
        return
    auftrag = {
        "id": "TEST-001",
        "abteilung": f"{klasse.NUMMER} {klasse.NAME}",
        "ziel": argumente[0],
        "kriterien": ["Ergebnis ist konkret", "Passt zur Marke", "Keine Ausgaben noetig"],
        "frist": "offen",
        "rahmen": "keine Ausgaben",
    }
    if modell:
        auftrag["modell"] = modell
    ergebnis = klasse().bearbeiten(auftrag, recherche="--recherche" in sys.argv)
    print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
