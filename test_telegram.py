"""test_telegram.py — Telegram-Anbindung und sicheres Register, ohne Netz und ohne Kosten.

Telegram wird durch eine Attrappe ersetzt, die jeden Aufruf festhaelt; systemd
ebenso. Kein Test schickt etwas aufs Handy, keiner ruft die Claude-API.

    .venv/bin/python -m unittest test_telegram -v
"""

import contextlib
import html.parser
import io
import json
import os
import sys
import tempfile
import threading
import time
import types
import unittest
import urllib.error
from datetime import date, datetime
from unittest import mock

# Die Basis bricht ohne das Paket 'anthropic' ab; fuer den Test genuegt eine Huelle.
sys.modules.setdefault("anthropic", types.ModuleType("anthropic"))
sys.modules["anthropic"].Anthropic = lambda **kw: None
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin"))

import orchestrator
import orchestrator_telegram as tg
import telegram_bot as bot

BJOERN = 4242
FREMD = 999
TOKEN = "123456789:" + "A" * 35
WARTET = "wartet auf Bjoern"
CONFIG = {"mail": {}, "qm_gate": [], "telegram": {"bot_token": TOKEN, "chat_id": str(BJOERN)}}


class FakeTelegram:
    """Steht fuer die Bot-API. Haelt jeden Aufruf fest und antwortet wie Telegram."""

    def __init__(self):
        self.aufrufe = []
        self.nummer = 100
        self.antworten = []       # vorbereitete Antworten, eine je Aufruf, sonst "ok"

    def __call__(self, token, methode, daten, dateien, zeitlimit):
        self.aufrufe.append((methode, daten or {}, dateien))
        if self.antworten:
            antwort = self.antworten.pop(0)
            if isinstance(antwort, BaseException):
                raise antwort
            if antwort is not None:
                return antwort
        if methode in ("sendMessage", "sendDocument", "sendPhoto"):
            self.nummer += 1
            return {"ok": True, "result": {"message_id": self.nummer}}
        if methode == "getMe":
            return {"ok": True, "result": {"username": "gustav_test_bot"}}
        if methode == "getUpdates":
            return {"ok": True, "result": []}
        return {"ok": True, "result": True}

    def gesendet(self, methode="sendMessage"):
        return [d for m, d, _ in self.aufrufe if m == methode]

    def texte(self):
        return "\n---\n".join(d.get("text", "") for d in self.gesendet())

    def knopfdaten(self, daten):
        markup = daten.get("reply_markup") or {}
        return [k["callback_data"] for reihe in markup.get("inline_keyboard", []) for k in reihe]


def auftrag(nr, abteilung="07 Einkauf China", stand="offen", ergebnis="Dear Sir, ...",
            ziel="RFQ für HB-01 an Kingming"):
    verlauf = []
    if ergebnis:
        verlauf.append({"zeit": "2026-09-27T10:00:00", "versuch": 1, "bestanden": True,
                        "begruendung": "Alle Kriterien erfuellt.", "ergebnis": ergebnis,
                        "anmerkung": None, "zeichnungen": None})
    return {"id": f"A-2026-{nr:03d}", "abteilung": abteilung, "ziel": ziel,
            "kriterien": ["k1", "k2", "k3"], "frist": "2030-01-01", "rahmen": "keine Ausgaben",
            "stand": stand, "versuche": 1 if ergebnis else 0, "eskaliert": stand == WARTET,
            "verlauf": verlauf, "angelegt": "2026-09-27T09:00:00"}


class Stichtag(date):
    """Auftragsnummern haengen am Jahr. Die Tests rechnen mit 2026, auch spaeter."""

    @classmethod
    def today(cls):
        return cls(2026, 9, 27)


class MitRegister(unittest.TestCase):
    """Jeder Test bekommt sein eigenes, leeres Register in einem Wegwerf-Ordner."""

    def setUp(self):
        self.ordner = tempfile.TemporaryDirectory()
        self.addCleanup(self.ordner.cleanup)
        self.pfad = lambda name: os.path.join(self.ordner.name, name)
        for name, wert in (("ZUSTAND", self.pfad("auftraege.json")), ("date", Stichtag)):
            p = mock.patch.object(orchestrator, name, wert)
            p.start()
            self.addCleanup(p.stop)
        # Laufmeldungen und "Auftrag angelegt" stoeren in der Testausgabe.
        umleitung = contextlib.redirect_stdout(io.StringIO())
        self.ausgabe = umleitung.__enter__()
        self.addCleanup(umleitung.__exit__, None, None, None)

    def register(self, *auftraege, letzter_lauf=None):
        orchestrator.zustand_speichern({"auftraege": list(auftraege), "letzter_lauf": letzter_lauf,
                                        "letzter_wochenbericht": datetime.now().isoformat()})

    def stand(self, auftrag_id):
        a = orchestrator._auftrag_finden(orchestrator.zustand_laden(), auftrag_id)
        return a and a["stand"]


# ---------- Zugang ----------

class Zugang(unittest.TestCase):
    def test_ohne_block_ist_telegram_aus_auch_wenn_die_umgebung_einen_token_hat(self):
        with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": TOKEN, "TELEGRAM_CHAT_ID": "1"}):
            self.assertEqual(tg.zugang({"mail": {}}), ("", []))

    def test_nicht_aufgeloester_platzhalter_zaehlt_als_leer(self):
        config = {"telegram": {"bot_token": "${TELEGRAM_BOT_TOKEN}", "chat_id": "${TELEGRAM_CHAT_ID}"}}
        self.assertEqual(tg.zugang(config), ("", []))
        self.assertIn("Token", tg.diagnose(config))

    def test_vollstaendig(self):
        self.assertEqual(tg.zugang(CONFIG), (TOKEN, [BJOERN]))
        self.assertEqual(tg.diagnose(CONFIG), "")

    def test_mehrere_konten(self):
        self.assertEqual(tg.chat_ids("123, 456"), [123, 456])
        self.assertEqual(tg.chat_ids([123, "kaputt"]), [123])
        self.assertEqual(tg.chat_ids(None), [])


# ---------- Versand (was der Lauf schickt) ----------

class Versand(unittest.TestCase):
    def setUp(self):
        self.fake = FakeTelegram()
        for name, wert in (("_http", self.fake), ("_funkstille_bis", 0.0)):
            p = mock.patch.object(tg, name, wert)
            p.start()
            self.addCleanup(p.stop)
        umleitung = contextlib.redirect_stdout(io.StringIO())
        self.ausgabe = umleitung.__enter__()
        self.addCleanup(umleitung.__exit__, None, None, None)

    def test_ergebnis_kommt_mit_entscheidungsknoepfen(self):
        a = auftrag(31, stand=WARTET)
        self.assertTrue(tg.melden(a, "Ergebnis liegt vor", "ERGEBNIS:\nDear Sir", CONFIG))
        nachricht = self.fake.gesendet()[0]
        self.assertEqual(nachricht["chat_id"], BJOERN)
        self.assertIn("A-2026-031 · Henrik (07 Einkauf China)", nachricht["text"])
        self.assertEqual(self.fake.knopfdaten(nachricht),
                         ["frei:A-2026-031", "ueber:A-2026-031", "verw:A-2026-031"])

    def test_kopf_der_mail_wird_auf_dem_handy_nicht_wiederholt(self):
        a = auftrag(30, stand=WARTET)
        bericht = orchestrator._bericht(a, {"ergebnis": "Dear Sir", "kriterien_erfuellt": [True] * 3},
                                        "Alle Kriterien erfuellt.")
        tg.melden(a, "Ergebnis liegt vor", bericht, CONFIG)
        text = self.fake.gesendet()[0]["text"]
        self.assertNotIn("Auftrag:", text)
        self.assertNotIn("Abteilung:", text)
        self.assertIn("Ziel: RFQ für HB-01 an Kingming", text)       # ohne Buendigkeitsluecke
        self.assertIn("Dear Sir", text)

    def test_ohne_ergebnis_gibt_es_nichts_freizugeben(self):
        a = auftrag(32, stand=WARTET, ergebnis=None)
        tg.melden(a, "Frist ueberschritten", "Frist war gestern", CONFIG)
        knoepfe = self.fake.knopfdaten(self.fake.gesendet()[0])
        self.assertNotIn("frei:A-2026-032", knoepfe)
        self.assertIn("ueber:A-2026-032", knoepfe)

    def test_langer_bericht_kommt_gekuerzt_und_ganz_als_datei(self):
        lang = "\n".join(f"Zeile {i}: " + "Fettleder " * 12 for i in range(200))
        tg.melden(auftrag(33, stand=WARTET), "Ergebnis liegt vor", lang, CONFIG)
        text = self.fake.gesendet()[0]["text"]
        self.assertLessEqual(len(tg.klartext(text)), tg.GRENZE)
        self.assertIn("Vollständig in der Datei", text)
        datei = self.fake.aufrufe[1]
        self.assertEqual(datei[0], "sendDocument")
        self.assertEqual(datei[2]["document"][1].decode("utf-8"), lang.strip())

    def test_zeichnungen_stehen_nicht_als_zahlenwust_im_text(self):
        text = "Stueckliste ...\n<<<SVG>>><svg width='10'><line x1='0'/></svg><<</SVG>>>\nEnde"
        tg.melden(auftrag(34, stand=WARTET), "Ergebnis liegt vor", text, CONFIG)
        gesendet = self.fake.gesendet()[0]["text"]
        self.assertNotIn("svg", gesendet.lower())
        self.assertIn("[Zeichnung]", gesendet)

    def test_modelltext_wird_escaped(self):
        tg.melden(auftrag(35, stand=WARTET), "Ergebnis liegt vor", "Preis < 5 & > 3 <b>", CONFIG)
        self.assertIn("Preis &lt; 5 &amp; &gt; 3 &lt;b&gt;", self.fake.gesendet()[0]["text"])

    def test_markupfehler_faellt_auf_klartext_zurueck(self):
        self.fake.antworten = [{"ok": False, "error_code": 400,
                                "description": "Bad Request: can't parse entities"}]
        tg.Draht(TOKEN, self.fake).nachricht(BJOERN, "<b>fett</b> &amp; gut")
        zweiter = self.fake.gesendet()[1]
        self.assertNotIn("parse_mode", zweiter)
        self.assertEqual(zweiter["text"], "fett & gut")

    def test_melden_wirft_nie(self):
        self.fake.antworten = [RuntimeError("kaputt")]
        self.assertFalse(tg.melden(auftrag(36, stand=WARTET), "Ergebnis liegt vor", "x", CONFIG))

    def test_ohne_einrichtung_wird_nichts_geschickt(self):
        self.assertFalse(tg.melden(auftrag(37), "Ergebnis liegt vor", "x", {"mail": {}}))
        self.assertFalse(tg.senden("x", {"mail": {}}))
        self.assertEqual(self.fake.aufrufe, [])

    def test_token_landet_nie_im_log(self):
        self.fake.antworten = [urllib.error.URLError(f"https://api.telegram.org/bot{TOKEN}/x")]
        tg.melden(auftrag(38, stand=WARTET), "Ergebnis liegt vor", "x", CONFIG)
        self.assertIn("nicht erreichbar", self.ausgabe.getvalue())
        self.assertNotIn(TOKEN, self.ausgabe.getvalue())

    def test_nach_netzfehler_haengt_der_lauf_nicht_an_jeder_meldung(self):
        self.fake.antworten = [OSError("Netz weg")]
        self.assertFalse(tg.melden(auftrag(39, stand=WARTET), "Ergebnis liegt vor", "x", CONFIG))
        versuche = len(self.fake.aufrufe)
        self.assertFalse(tg.melden(auftrag(40, stand=WARTET), "Ergebnis liegt vor", "y", CONFIG))
        self.assertFalse(tg.senden("Wochenuebersicht", CONFIG))
        self.assertEqual(len(self.fake.aufrufe), versuche)       # kein weiterer Versuch
        with mock.patch.object(tg, "_funkstille_bis", 0.0):
            self.assertTrue(tg.melden(auftrag(41, stand=WARTET), "Ergebnis liegt vor", "z", CONFIG))

    def test_zu_viele_nachrichten_einmal_warten(self):
        self.fake.antworten = [{"ok": False, "error_code": 429, "description": "Too Many Requests",
                                "parameters": {"retry_after": 2}}]
        with mock.patch.object(tg.time, "sleep") as schlaf:
            tg.Draht(TOKEN, self.fake).nachricht(BJOERN, "hallo")
        schlaf.assert_called_once_with(2)
        self.assertEqual(len(self.fake.gesendet()), 2)


class Eskalation(MitRegister):
    """Der Lauf meldet per Mail und per Telegram — und haengt nie an Telegram."""

    def setUp(self):
        super().setUp()
        self.mails = []
        for ziel, name, wert in (
                (orchestrator, "senden", lambda betreff, text, config, anhaenge=None: self.mails.append(betreff)),
                (tg, "_funkstille_bis", 0.0)):
            p = mock.patch.object(ziel, name, wert)
            p.start()
            self.addCleanup(p.stop)

    def test_eskalation_geht_an_mail_und_telegram(self):
        fake = FakeTelegram()
        with mock.patch.object(tg, "_http", fake):
            orchestrator.eskalieren(auftrag(40), "Ergebnis liegt vor", "Dear Sir", CONFIG)
        self.assertEqual(len(self.mails), 1)
        self.assertEqual(len(fake.gesendet()), 1)

    def test_telegram_weg_mail_trotzdem(self):
        fake = FakeTelegram()
        fake.antworten = [OSError("Netz weg")]
        a = auftrag(41)
        with mock.patch.object(tg, "_http", fake):
            orchestrator.eskalieren(a, "Ergebnis liegt vor", "Dear Sir", CONFIG)
        self.assertEqual(len(self.mails), 1)
        self.assertEqual(a["stand"], WARTET)


# ---------- Register: nichts geht verloren ----------

class Register(MitRegister):
    def test_was_waehrend_des_laufs_kommt_geht_nicht_verloren(self):
        """Bisher hat der Lauf am Ende seinen alten Stand zurueckgeschrieben und
        damit alles ueberschrieben, was waehrend der Arbeit dazukam."""
        self.register(auftrag(1, ergebnis=None), auftrag(2, stand=WARTET))
        test = self

        class Abteilung:
            cache_lohnt = False

            def __init__(self, name):
                pass

            def bearbeiten(self, a, recherche=False):
                # Waehrenddessen, per Telegram: neuer Auftrag und eine Entscheidung.
                orchestrator.auftrag_anlegen("01", "Neu, waehrend der Lauf arbeitet")
                orchestrator.freigeben("A-2026-002", "per Telegram")
                return {"ergebnis": "fertig", "blocker": None, "anmerkung": None,
                        "zusammenfassung": "", "fakten": [],
                        "kriterien_erfuellt": [True] * len(a["kriterien"])}

        with mock.patch.object(orchestrator, "abteilung_laden", Abteilung), \
                mock.patch.object(orchestrator, "config_laden", lambda: {"mail": {}, "qm_gate": []}), \
                mock.patch.object(orchestrator, "senden", lambda *a, **k: None):
            orchestrator.lauf()

        daten = orchestrator.zustand_laden()
        test.assertEqual([a["id"] for a in daten["auftraege"]],
                         ["A-2026-001", "A-2026-002", "A-2026-003"])
        test.assertEqual(self.stand("A-2026-001"), WARTET)          # im Lauf bearbeitet
        test.assertEqual(self.stand("A-2026-002"), "freigegeben")   # waehrenddessen entschieden
        test.assertEqual(self.stand("A-2026-003"), "offen")         # waehrenddessen angelegt
        test.assertIsNotNone(daten["letzter_lauf"])

    def test_ablehnen_legt_unter_der_sperre_an_ohne_zu_verklemmen(self):
        self.register(auftrag(5, stand=WARTET))
        ergebnis = {}
        faden = threading.Thread(target=lambda: ergebnis.update(
            neu=orchestrator.ablehnen("A-2026-005", "mit Messingschnalle")))
        faden.start()
        faden.join(5)
        self.assertFalse(faden.is_alive(), "ablehnen() haengt an der eigenen Sperre")
        self.assertEqual(ergebnis["neu"]["id"], "A-2026-006")
        self.assertIn("mit Messingschnalle", ergebnis["neu"]["ziel"])

    def test_sperre_haelt_andere_schreiber_an(self):
        self.register()
        faden = threading.Thread(target=orchestrator.auftrag_anlegen, args=("01", "wartet"))
        with orchestrator.sperre():
            faden.start()
            time.sleep(0.3)
            self.assertTrue(faden.is_alive())
            self.assertEqual(orchestrator.zustand_laden()["auftraege"], [])
        faden.join(5)
        self.assertEqual(len(orchestrator.zustand_laden()["auftraege"]), 1)


# ---------- Der Bot ----------

class BotTest(MitRegister):
    def setUp(self):
        super().setUp()
        self.fake = FakeTelegram()
        self.systemd = {"bello-orchestrator-anstoss.path": "active",
                        "bello-orchestrator.service": "inactive"}
        for ziel, name, wert in (
                (bot, "ANSTOSS", self.pfad("lauf-anstossen")),
                (bot, "_systemctl", lambda *a: self.systemd.get(a[-1], "") if a[0] == "is-active" else "")):
            p = mock.patch.object(ziel, name, wert)
            p.start()
            self.addCleanup(p.stop)
        self.bot = bot.Bot(tg.Draht(TOKEN, self.fake), [BJOERN], pfad=self.pfad("telegram.json"))
        self.update_nr = 0

    def schreiben(self, text, von=BJOERN, typ="private", antwort_auf=None, **extra):
        self.update_nr += 1
        msg = {"message_id": 1000 + self.update_nr, "from": {"id": von, "first_name": "Björn"},
               "chat": {"id": von, "type": typ}, **extra}
        if text is not None:
            msg["text"] = text
        if antwort_auf:
            msg["reply_to_message"] = antwort_auf
        self.bot.bearbeiten({"update_id": self.update_nr, "message": msg})

    def druecken(self, daten, nachricht_id, von=BJOERN):
        self.update_nr += 1
        self.bot.bearbeiten({"update_id": self.update_nr, "callback_query": {
            "id": f"cb{self.update_nr}", "from": {"id": von}, "data": daten,
            "message": {"message_id": nachricht_id, "chat": {"id": von, "type": "private"}}}})

    def letzte(self):
        return self.fake.gesendet()[-1]

    # --- wer darf ---

    def test_fremde_werden_ignoriert(self):
        self.schreiben("@Henrik RFQ fuer HB-01", von=FREMD)
        self.druecken("frei:A-2026-001", 5, von=FREMD)
        self.assertEqual(self.fake.gesendet(), [])
        self.assertEqual(orchestrator.zustand_laden()["auftraege"], [])

    def test_gruppen_zaehlen_nicht(self):
        self.schreiben("@Henrik RFQ fuer HB-01", typ="group")
        self.assertEqual(orchestrator.zustand_laden()["auftraege"], [])

    # --- Auftraege ---

    def test_auftrag_mit_namen(self):
        self.schreiben("@Henrik RFQ für HB-01 an Kingming, 100 Stück")
        a = orchestrator.zustand_laden()["auftraege"][0]
        self.assertEqual(a["abteilung"], "07 Einkauf China")
        self.assertEqual(a["ziel"], "RFQ für HB-01 an Kingming, 100 Stück")
        self.assertIn("A-2026-001", self.letzte()["text"])
        self.assertEqual(self.fake.knopfdaten(self.letzte()), ["jetzt"])

    def test_auftrag_gleicht_dem_von_der_kommandozeile(self):
        self.schreiben("@Konrad Führe Steg und Taille aus")
        orchestrator.auftrag_anlegen("02", "Führe Steg und Taille aus")
        telegram, konsole = orchestrator.zustand_laden()["auftraege"]
        for feld in ("id", "angelegt"):
            telegram.pop(feld), konsole.pop(feld)
        self.assertEqual(telegram, konsole)

    def test_freitext_fragt_wer_und_legt_nach_knopfdruck_an(self):
        self.schreiben("Drei Formentwürfe Halsband, nur Form")
        frage = self.letzte()
        self.assertIn("Wer soll das übernehmen?", frage["text"])
        self.assertIn("an:08", self.fake.knopfdaten(frage))
        self.assertEqual(orchestrator.zustand_laden()["auftraege"], [])

        self.druecken("an:08", self.fake.nummer)
        a = orchestrator.zustand_laden()["auftraege"][0]
        self.assertEqual((a["abteilung"], a["ziel"]), ("08 Design", "Drei Formentwürfe Halsband, nur Form"))
        self.assertIn("A-2026-001", self.fake.gesendet("editMessageText")[-1]["text"])

        self.druecken("an:08", self.fake.nummer)          # zweimal gedrueckt: kein zweiter Auftrag
        self.assertEqual(len(orchestrator.zustand_laden()["auftraege"]), 1)

    def test_mehrdeutig_fragt_nur_die_passenden(self):
        self.schreiben("@Einkauf Buchschrauben anfragen")
        self.assertEqual([k for k in self.fake.knopfdaten(self.letzte()) if k.startswith("an:")],
                         ["an:06", "an:07"])

    def test_fach_aus_mehreren_woertern(self):
        self.schreiben("@Einkauf China RFQ fuer LE-01")
        a = orchestrator.zustand_laden()["auftraege"][0]
        self.assertEqual((a["abteilung"], a["ziel"]), ("07 Einkauf China", "RFQ fuer LE-01"))

    def test_auftrag_befehl_ohne_at_nimmt_nur_eindeutige_namen(self):
        self.schreiben("/auftrag Henrik RFQ für LE-01")
        self.assertEqual(orchestrator.zustand_laden()["auftraege"][0]["abteilung"], "07 Einkauf China")
        self.schreiben("/auftrag In drei Tagen Muster prüfen")      # "in" steckt in "Einkauf"
        frage = self.letzte()
        self.assertEqual(len([k for k in self.fake.knopfdaten(frage) if k.startswith("an:")]),
                         len(orchestrator.ABTEILUNGEN))
        self.druecken("an:09", self.fake.nummer)
        self.assertEqual(orchestrator.zustand_laden()["auftraege"][1]["ziel"],
                         "In drei Tagen Muster prüfen")

    def test_zu_lang(self):
        self.schreiben("@Henrik " + "x" * 2100)
        self.assertEqual(orchestrator.zustand_laden()["auftraege"], [])
        self.assertIn("höchstens 2000", self.letzte()["text"])

    def test_sprachnachricht_bekommt_einen_hinweis(self):
        self.schreiben(None, voice={"duration": 3})
        self.assertIn("Mikrofon auf der Tastatur", self.letzte()["text"])

    # --- Entscheidungen ---

    def test_freigeben_per_knopf(self):
        self.register(auftrag(1, stand=WARTET))
        self.druecken("frei:A-2026-001", 50)
        self.assertEqual(self.stand("A-2026-001"), "freigegeben")
        self.assertEqual(self.fake.gesendet("editMessageReplyMarkup")[-1]["reply_markup"],
                         {"inline_keyboard": []})

    def test_alter_knopf_entscheidet_nichts_ein_zweites_mal(self):
        self.register(auftrag(1, stand="freigegeben"))
        self.druecken("ueber:A-2026-001", 50)
        self.assertEqual(len(orchestrator.zustand_laden()["auftraege"]), 1)
        self.assertIn("schon freigegeben", self.fake.gesendet("answerCallbackQuery")[-1]["text"])

    def test_ueberarbeiten_als_antwort(self):
        self.register(auftrag(1, stand=WARTET))
        self.druecken("ueber:A-2026-001", 50)
        frage = self.letzte()
        self.assertTrue(frage["reply_markup"]["force_reply"])
        self.schreiben("Bitte mit Messingschnalle", antwort_auf={"message_id": self.fake.nummer})
        self.assertEqual(self.stand("A-2026-001"), "abgelehnt")
        neu = orchestrator.zustand_laden()["auftraege"][1]
        self.assertIn("Ueberarbeitung zu A-2026-001", neu["ziel"])
        self.assertIn("Bitte mit Messingschnalle", neu["ziel"])
        self.assertEqual(neu["abteilung"], "07 Einkauf China")

    def test_antwort_auf_ein_ergebnis_bietet_die_ueberarbeitung_an(self):
        self.register(auftrag(1, stand=WARTET))
        self.schreiben("Noch eine Variante in Oliv", antwort_auf={
            "message_id": 50, "text": "📋 Ergebnis liegt vor\nA-2026-001 · Henrik (07 Einkauf China)"})
        self.assertEqual(self.fake.knopfdaten(self.letzte())[0], "als-ueber:A-2026-001")
        self.druecken("als-ueber:A-2026-001", self.fake.nummer)
        self.assertEqual(self.stand("A-2026-001"), "abgelehnt")
        self.assertIn("Noch eine Variante in Oliv", orchestrator.zustand_laden()["auftraege"][1]["ziel"])

    def test_neuer_auftrag_als_antwort_behaelt_den_bezug(self):
        self.register(auftrag(1, stand=WARTET))
        self.schreiben("@Thea Form dazu entwerfen", antwort_auf={"message_id": 50, "text": "A-2026-001 · Henrik"})
        self.assertIn("(Bezug: A-2026-001)", orchestrator.zustand_laden()["auftraege"][1]["ziel"])

    def test_verwerfen_braucht_eine_bestaetigung(self):
        self.register(auftrag(1, stand=WARTET))
        self.druecken("verw:A-2026-001", 50)
        self.assertEqual(self.stand("A-2026-001"), WARTET)
        self.assertIn("verw!:A-2026-001", self.fake.knopfdaten(self.fake.gesendet("editMessageReplyMarkup")[-1]))
        self.druecken("verw!:A-2026-001", 50)
        self.assertEqual(self.stand("A-2026-001"), "verworfen")

    def test_befehle_fuer_entscheidungen(self):
        self.register(auftrag(1, stand=WARTET), auftrag(2, stand=WARTET))
        self.schreiben("/freigeben A-2026-001 passt so")
        self.schreiben("/ueberarbeiten a-2026-002 kürzer")
        daten = orchestrator.zustand_laden()
        self.assertEqual(daten["auftraege"][0]["verlauf"][-1]["kommentar"], "passt so")
        self.assertEqual(daten["auftraege"][1]["stand"], "abgelehnt")

    # --- Anzeigen ---

    def test_stand_zeigt_was_wartet(self):
        self.register(auftrag(1, stand=WARTET), auftrag(2, ergebnis=None), auftrag(3, stand="fertig"))
        self.schreiben("/stand")
        text = self.letzte()["text"]
        self.assertIn("Wartet auf dich (1)", text)
        self.assertIn("Offen (1)", text)
        self.assertIn("Erledigt: erledigt 1", text)
        self.assertIn("zeig:A-2026-001", self.fake.knopfdaten(self.letzte()))

    def test_ergebnis_lang_kommt_als_datei_dazu(self):
        self.register(auftrag(1, stand=WARTET, ergebnis="Absatz. " * 800))
        self.schreiben("/ergebnis A-2026-001")
        self.assertLessEqual(len(tg.klartext(self.fake.gesendet()[-1]["text"])), tg.GRENZE)
        self.assertEqual(self.fake.aufrufe[-1][0], "sendDocument")

    def test_hilfe_und_team_sind_gueltiges_markup(self):
        self.schreiben("/hilfe")
        self.schreiben("/team")
        for text in (self.fake.gesendet()[0]["text"], self.fake.gesendet()[1]["text"]):
            pruefer = MarkupPruefer()
            pruefer.feed(text)
            self.assertEqual(pruefer.offen, [], text)
            self.assertLessEqual(pruefer.tags, {"b", "i", "code"})

    def test_unbekannter_befehl(self):
        self.schreiben("/tanzen")
        self.assertIn("/hilfe", self.letzte()["text"])

    # --- Sofortstart ---

    def test_angehaltener_zeitplan_wird_ehrlich_genannt(self):
        self.assertEqual(bot.naechster_lauf(), "stündlich 7–19 Uhr")
        self.systemd["bello-orchestrator.timer"] = "inactive"
        self.assertIn("angehalten", bot.naechster_lauf())

    def test_nichts_offen_nichts_anzustossen(self):
        self.register(auftrag(1, stand=WARTET))
        self.schreiben("/jetzt")
        self.assertFalse(os.path.exists(bot.ANSTOSS))

    def test_ohne_eingerichteten_sofortstart_ehrlich_sagen(self):
        self.register(auftrag(1, ergebnis=None))
        self.systemd["bello-orchestrator-anstoss.path"] = "inactive"
        self.schreiben("/jetzt")
        self.assertFalse(os.path.exists(bot.ANSTOSS))
        self.assertIn("nicht eingerichtet", self.letzte()["text"])

    def test_anstossen_und_rueckmeldung_nach_dem_lauf(self):
        self.register(auftrag(1, ergebnis=None), letzter_lauf="2026-09-27T09:00:00")
        self.druecken("jetzt", 60)
        self.assertTrue(os.path.exists(bot.ANSTOSS))

        self.bot.lauf_beobachten()                     # Lauf noch nicht durch: still
        self.assertIn("angestoßen", self.letzte()["text"])

        daten = orchestrator.zustand_laden()
        daten["auftraege"][0]["stand"] = WARTET
        daten["letzter_lauf"] = "2026-09-27T09:05:00"
        orchestrator.zustand_speichern(daten)
        self.bot.lauf_beobachten()
        self.assertIn("Lauf fertig", self.letzte()["text"])
        self.assertIn("zeig:A-2026-001", self.fake.knopfdaten(self.letzte()))
        self.assertIsNone(self.bot.zustand["beobachten"])

    def test_lief_schon_ein_lauf_wird_einmal_nachgestartet(self):
        self.register(auftrag(1, ergebnis=None), letzter_lauf="2026-09-27T09:00:00")
        self.systemd["bello-orchestrator.service"] = "activating"
        self.schreiben("/jetzt")
        self.assertFalse(os.path.exists(bot.ANSTOSS))  # laeuft schon — erst danach
        self.assertIn("arbeitet gerade schon", self.letzte()["text"])

        daten = orchestrator.zustand_laden()
        daten["letzter_lauf"] = "2026-09-27T09:03:00"   # der alte Lauf ist durch, unserer lag noch
        orchestrator.zustand_speichern(daten)
        gesendet = len(self.fake.gesendet())
        self.bot.lauf_beobachten()
        self.assertTrue(os.path.exists(bot.ANSTOSS))
        self.assertEqual(len(self.fake.gesendet()), gesendet)

        daten["auftraege"][0]["stand"] = "nacharbeit"
        daten["letzter_lauf"] = "2026-09-27T09:08:00"
        orchestrator.zustand_speichern(daten)
        self.bot.lauf_beobachten()
        self.assertIn("in Nacharbeit", self.letzte()["text"])
        self.assertEqual(self.fake.knopfdaten(self.letzte()), ["jetzt"])

    # --- Schleife ---

    def test_position_wird_vor_der_bearbeitung_gesichert(self):
        """Lieber eine Nachricht verlieren als einen Auftrag doppelt anlegen."""

        class Ende(BaseException):
            pass

        gesehen = []
        self.fake.antworten = [
            {"ok": True, "result": [{"update_id": 77, "message": {}}]},
            Ende()]
        def bearbeiten(update):
            with open(self.bot.pfad, encoding="utf-8") as f:
                gesehen.append(json.load(f)["offset"])

        with mock.patch.object(self.bot, "bearbeiten", bearbeiten):
            with self.assertRaises(Ende):
                self.bot.schleife()
        self.assertEqual(gesehen, [78])


class Adressat(unittest.TestCase):
    def test_varianten(self):
        self.assertEqual(bot.adressat("@Henrik: RFQ HB-01")[:2], ("07 Einkauf China", "RFQ HB-01"))
        self.assertEqual(bot.adressat("@07 RFQ")[:2], ("07 Einkauf China", "RFQ"))
        self.assertEqual(bot.adressat("@Produkt & Ausführung Zeichnung")[:2],
                         ("02 Produkt & Ausführung", "Zeichnung"))
        self.assertEqual(bot.adressat("@Henrik\nZeile 1\nZeile 2")[:2],
                         ("07 Einkauf China", "Zeile 1\nZeile 2"))
        self.assertEqual(bot.adressat("@Gustav mach mal"), (None, "mach mal", [], "Gustav"))


class Kennenlernen(unittest.TestCase):
    def test_zeigt_wer_schreibt_und_hakt_die_nachricht_ab(self):
        fake = FakeTelegram()
        fake.antworten = [
            None, None,                                              # getMe, deleteWebhook
            {"ok": True, "result": [{"update_id": 5, "message": {}}]},   # Altes: zaehlt nicht
            {"ok": True, "result": [{"update_id": 6, "message": {
                "from": {"id": BJOERN, "first_name": "Björn", "username": "bjoern"},
                "chat": {"id": BJOERN, "type": "private"}, "text": "hallo"}}]},
        ]
        aus = io.StringIO()
        with mock.patch.object(tg, "_http", fake), \
                mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": TOKEN}), \
                contextlib.redirect_stdout(aus), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(bot.kennenlernen(geduld=5), 0)
        self.assertIn(f"CHAT_ID={BJOERN}", aus.getvalue())
        self.assertIn("NAME=Björn (@bjoern)", aus.getvalue())
        abfragen = [d for m, d, _ in fake.aufrufe if m == "getUpdates"]
        self.assertEqual(abfragen[1]["offset"], 6)      # das Alte uebersprungen
        self.assertEqual(abfragen[-1]["offset"], 7)     # "hallo" abgehakt


class MarkupPruefer(html.parser.HTMLParser):
    """Findet offene Tags — Telegram lehnt unausgeglichenes Markup ab."""

    def __init__(self):
        super().__init__()
        self.offen, self.tags = [], set()

    def handle_starttag(self, tag, attrs):
        self.offen.append(tag)
        self.tags.add(tag)

    def handle_endtag(self, tag):
        if self.offen and self.offen[-1] == tag:
            self.offen.pop()
        else:
            self.offen.append(f"/{tag}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
