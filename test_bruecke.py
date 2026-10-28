"""
test_bruecke.py — Prueft Anbieter-Schicht, Gegenpruefung und CLI-Bruecke ohne Netz und ohne Kosten.

Aufruf:  python3 -m unittest test_bruecke -v
"""

import io
import json
import os
import subprocess
import tempfile
import unittest
from unittest import mock

import abteilung_basis
import gegenpruefung
import ki_anbieter
import ki_bruecke
from abteilung_einkauf_china import EinkaufChina

CONFIG = {
    "anthropic_api_key": "sk-ant-test",
    "openai": {"api_key": "sk-test", "modell": "gpt-test"},
}


class FakeAnbieter(ki_anbieter.Anbieter):
    def __init__(self, name, antwort):
        super().__init__("fake")
        self.NAME = name
        self.antwort = antwort
        self.aufrufe = []

    def antworten(self, system, nutzer, recherche=False, max_tokens=4000):
        self.aufrufe.append((system, nutzer))
        if isinstance(self.antwort, Exception):
            raise self.antwort
        return self.antwort, ki_anbieter.verbrauch_leer()


def auftrag(**mehr):
    return {"id": "A-1", "abteilung": "05 Einkauf China", "ziel": "RFQ fuer HB-01",
            "kriterien": ["konkret", "passt zur Marke"], "rahmen": "keine Ausgaben", **mehr}


def ergebnis():
    return {"ergebnis": "Entwurf ...", "kriterien_erfuellt": [True, True], "anmerkung": None}


class AuswahlTest(unittest.TestCase):

    def test_standard_ist_claude(self):
        self.assertEqual(ki_anbieter.anbieter_name({}, "05"), "claude")

    def test_ausnahme_je_abteilung_schlaegt_standard(self):
        cfg = {"anbieter": "claude", "anbieter_je_abteilung": {"05": "openai"}}
        self.assertEqual(ki_anbieter.anbieter_name(cfg, "05"), "openai")
        self.assertEqual(ki_anbieter.anbieter_name(cfg, "03"), "claude")

    def test_unbekannter_anbieter_wird_laut(self):
        with self.assertRaises(ValueError):
            ki_anbieter.anbieter_name({"anbieter": "gemini"})

    def test_fehlender_schluessel_nennt_die_quelle(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                ki_anbieter.anbieter_bauen({}, "openai")

    def test_gegenueber_ring_ohne_config(self):
        self.assertEqual(ki_anbieter.gegenueber("claude"), "openai")
        self.assertEqual(ki_anbieter.gegenueber("openai"), "kimi")
        self.assertEqual(ki_anbieter.gegenueber("kimi"), "claude")

    def test_gegenueber_ueberspringt_anbieter_ohne_schluessel(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(ki_anbieter.gegenueber("claude", CONFIG), "openai")
            nur_claude_kimi = {"anthropic_api_key": "a", "kimi": {"api_key": "k"}}
            self.assertEqual(ki_anbieter.gegenueber("claude", nur_claude_kimi), "kimi")

    def test_pruefer_laesst_sich_erzwingen_aber_nie_selbst(self):
        self.assertEqual(ki_anbieter.gegenueber("claude", {"pruefer": "kimi"}), "kimi")
        self.assertEqual(ki_anbieter.gegenueber("kimi", {"pruefer": "kimi"}), "claude")


class OpenAITest(unittest.TestCase):

    def antwort(self, koerper):
        antwort = mock.MagicMock()
        antwort.read.return_value = json.dumps(koerper).encode()
        antwort.__enter__.return_value = antwort
        return antwort

    def test_anfrage_und_verbrauch(self):
        echt = {"choices": [{"message": {"content": '{"ergebnis": "x"}'}}],
                "usage": {"prompt_tokens": 1000, "completion_tokens": 50,
                          "prompt_tokens_details": {"cached_tokens": 800}}}
        anbieter = ki_anbieter.anbieter_bauen(CONFIG, "openai")
        with mock.patch("urllib.request.urlopen", return_value=self.antwort(echt)) as auf:
            text, verbrauch = anbieter.antworten("SYSTEM", "NUTZER")
        anfrage = auf.call_args[0][0]
        self.assertTrue(anfrage.full_url.endswith("/v1/chat/completions"))
        self.assertEqual(anfrage.get_header("Authorization"), "Bearer sk-test")
        gesendet = json.loads(anfrage.data)
        self.assertEqual(gesendet["model"], "gpt-test")
        self.assertEqual(gesendet["messages"][0], {"role": "system", "content": "SYSTEM"})
        self.assertEqual(text, '{"ergebnis": "x"}')
        # Cache-Treffer werden aus "ein" herausgerechnet, wie bei Claude.
        self.assertEqual(verbrauch, {"ein": 200, "aus": 50, "cache_gelesen": 800,
                                     "cache_geschrieben": 0})

    def test_kimi_nutzt_eigene_adresse_schluessel_und_tokenfeld(self):
        cfg = {"kimi": {"api_key": "sk-kimi"}}
        echt = {"choices": [{"message": {"content": "{}"}}],
                "usage": {"prompt_tokens": 500, "completion_tokens": 10, "cached_tokens": 400}}
        anbieter = ki_anbieter.anbieter_bauen(cfg, "kimi")
        with mock.patch("urllib.request.urlopen", return_value=self.antwort(echt)) as auf:
            _, verbrauch = anbieter.antworten("s", "n", max_tokens=123)
        anfrage = auf.call_args[0][0]
        self.assertTrue(anfrage.full_url.startswith("https://api.moonshot.ai/v1/"))
        self.assertEqual(anfrage.get_header("Authorization"), "Bearer sk-kimi")
        gesendet = json.loads(anfrage.data)
        self.assertEqual(gesendet["max_tokens"], 123)
        self.assertNotIn("max_completion_tokens", gesendet)
        self.assertEqual(verbrauch["cache_gelesen"], 400)
        self.assertEqual(verbrauch["ein"], 100)

    def test_http_fehler_zeigt_den_grund(self):
        fehler = ki_anbieter.urllib.error.HTTPError(
            "u", 401, "Unauthorized", {}, io.BytesIO(b'{"error": "bad key"}'))
        anbieter = ki_anbieter.anbieter_bauen(CONFIG, "openai")
        with mock.patch("urllib.request.urlopen", side_effect=fehler):
            with self.assertRaisesRegex(RuntimeError, "401.*bad key"):
                anbieter.antworten("s", "n")


class AbteilungTest(unittest.TestCase):

    def abteilung(self, name="openai", antwort='{"ergebnis": "ok", "kriterien_erfuellt": [true, true]}'):
        fake = FakeAnbieter(name, antwort)
        with mock.patch.object(ki_anbieter, "anbieter_waehlen", return_value=fake):
            abt = EinkaufChina(dict(CONFIG, gedaechtnis=False))
        return abt, fake

    def test_abteilung_laeuft_ueber_den_gewaehlten_anbieter(self):
        abt, fake = self.abteilung()
        erg = abt.bearbeiten(auftrag())
        self.assertEqual(erg["ergebnis"], "ok")
        self.assertEqual(len(fake.aufrufe), 1)

    def test_nacharbeit_sieht_die_ablehnung_der_anderen_ki(self):
        abt, fake = self.abteilung()
        abgelehnt = auftrag(versuche=1, verlauf=[{
            "bestanden": False, "begruendung": "Gegenpruefung durch claude: Zinkbeschlag genannt"}])
        abt.bearbeiten(abgelehnt)
        self.assertIn("Zinkbeschlag genannt", fake.aufrufe[0][1])

    def test_erster_versuch_hat_keinen_ablehnungsblock(self):
        abt, fake = self.abteilung()
        abt.bearbeiten(auftrag())
        self.assertNotIn("ABGELEHNT", fake.aufrufe[0][1])


class GegenpruefungTest(unittest.TestCase):

    def test_pruefer_ist_die_andere_ki(self):
        pruefer = FakeAnbieter("kimi", '{"freigabe": true, "einwaende": []}')
        mit_kimi = dict(CONFIG, kimi={"api_key": "k"})
        urteil = gegenpruefung.pruefen(auftrag(), ergebnis(), mit_kimi, "openai", pruefer)
        self.assertEqual(urteil["pruefer"], "kimi")
        self.assertTrue(urteil["freigabe"])

    def test_ablehnung_mit_einwand(self):
        pruefer = FakeAnbieter("claude", '{"freigabe": false, "einwaende": ["Zink genannt"]}')
        urteil = gegenpruefung.pruefen(auftrag(), ergebnis(), CONFIG, "openai", pruefer)
        self.assertFalse(urteil["freigabe"])
        self.assertIn("Zink genannt", gegenpruefung.begruendung(urteil))

    def test_ablehnung_ohne_begruendung_zaehlt_nicht(self):
        pruefer = FakeAnbieter("claude", '{"freigabe": false, "einwaende": []}')
        urteil = gegenpruefung.pruefen(auftrag(), ergebnis(), CONFIG, "openai", pruefer)
        self.assertTrue(urteil["freigabe"])

    def test_ausfall_blockiert_nicht(self):
        pruefer = FakeAnbieter("claude", RuntimeError("Netz weg"))
        urteil = gegenpruefung.pruefen(auftrag(), ergebnis(), CONFIG, "openai", pruefer)
        self.assertTrue(urteil["freigabe"])
        self.assertFalse(urteil["verfuegbar"])
        self.assertIn("Netz weg", urteil["hinweis"])

    def test_kaputtes_json_blockiert_nicht(self):
        pruefer = FakeAnbieter("claude", "Sieht gut aus!")
        urteil = gegenpruefung.pruefen(auftrag(), ergebnis(), CONFIG, "openai", pruefer)
        self.assertTrue(urteil["freigabe"])
        self.assertFalse(urteil["verfuegbar"])

    def test_prompt_enthaelt_ergebnis_und_ist_stabil(self):
        self.assertEqual(gegenpruefung.system_prompt(), gegenpruefung.system_prompt())
        self.assertIn("Entwurf ...", gegenpruefung.nutzer_text(auftrag(), ergebnis()))


class BrueckeTest(unittest.TestCase):

    def setUp(self):
        self.ordner = tempfile.mkdtemp()
        patch = mock.patch.object(ki_bruecke, "UEBERGABE", self.ordner)
        patch.start()
        self.addCleanup(patch.stop)

    def lauf(self, code=0, ausgabe="Befund", fehler=""):
        return lambda befehl, **kw: subprocess.CompletedProcess(befehl, code, ausgabe, fehler)

    def test_codex_laeuft_lesend(self):
        gesehen = []
        def ausfuehren(befehl, **kw):
            gesehen.append(befehl)
            return subprocess.CompletedProcess(befehl, 0, "Befund", "")
        antwort = ki_bruecke.frage("codex", "Pruefe X", von="claude", ausfuehren=ausfuehren)
        self.assertEqual(antwort, "Befund")
        self.assertEqual(gesehen[0][:4], ["codex", "exec", "--sandbox", "read-only"])
        self.assertIn("Pruefe X", gesehen[0][-1])

    def test_claude_laeuft_im_planmodus(self):
        gesehen = []
        def ausfuehren(befehl, **kw):
            gesehen.append(befehl)
            return subprocess.CompletedProcess(befehl, 0, "ok", "")
        ki_bruecke.frage("claude", "Pruefe Y", von="codex", ausfuehren=ausfuehren)
        self.assertEqual(gesehen[0][:2], ["claude", "-p"])
        self.assertIn("plan", gesehen[0])

    def test_uebergabe_wird_protokolliert(self):
        ki_bruecke.frage("codex", "Pruefe X", von="claude", ausfuehren=self.lauf())
        dateien = os.listdir(self.ordner)
        self.assertEqual(len(dateien), 1)
        self.assertTrue(dateien[0].endswith("-claude-an-codex.md"))
        with open(os.path.join(self.ordner, dateien[0]), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("Pruefe X", text)
        self.assertIn("Befund", text)

    def test_fehlendes_cli_erklaert_die_installation(self):
        def weg(befehl, **kw):
            raise FileNotFoundError(befehl[0])
        with self.assertRaisesRegex(ki_bruecke.BrueckeFehler, "npm i -g"):
            ki_bruecke.frage("codex", "x", ausfuehren=weg)

    def test_fehlercode_wird_gemeldet_und_nicht_protokolliert(self):
        with self.assertRaisesRegex(ki_bruecke.BrueckeFehler, "Code 2.*kaputt"):
            ki_bruecke.frage("codex", "x", ausfuehren=self.lauf(code=2, fehler="kaputt"))
        self.assertEqual(os.listdir(self.ordner), [])

    def test_unbekanntes_ziel(self):
        with self.assertRaises(ki_bruecke.BrueckeFehler):
            ki_bruecke.frage("gemini", "x")

    def test_gegenlesen_nimmt_diff_sonst_letzten_commit(self):
        aufrufe = []
        def git(befehl, **kw):
            aufrufe.append(befehl)
            ausgabe = "" if befehl[1] == "diff" else "commit-inhalt"
            return subprocess.CompletedProcess(befehl, 0, ausgabe, "")
        aufgabe = ki_bruecke.diff_aufgabe(git)
        self.assertIn("commit-inhalt", aufgabe)
        self.assertEqual([a[1] for a in aufrufe], ["diff", "show"])

    def test_gegenlesen_ohne_aenderung(self):
        leer = lambda befehl, **kw: subprocess.CompletedProcess(befehl, 0, "", "")
        with self.assertRaises(ki_bruecke.BrueckeFehler):
            ki_bruecke.diff_aufgabe(leer)


class LaufTest(unittest.TestCase):
    """Orchestrator-Lauf: Bearbeiter gibt ab, Gegenpruefung lehnt ab, Nacharbeit sieht den Grund."""

    def test_ablehnung_der_anderen_ki_fuehrt_zur_nacharbeit(self):
        import orchestrator
        ordner = tempfile.mkdtemp()
        bearbeiter = FakeAnbieter("openai", "")
        abt = mock.MagicMock()
        abt.anbieter = bearbeiter
        abt.bearbeiten.return_value = dict(ergebnis(), blocker=None)
        pruefer = FakeAnbieter("claude", '{"freigabe": false, "einwaende": ["Zink genannt"]}')
        cfg = dict(CONFIG, gegenpruefung=True)
        with mock.patch.object(orchestrator, "ZUSTAND", os.path.join(ordner, "a.json")), \
             mock.patch.object(orchestrator, "config_laden", return_value=cfg), \
             mock.patch.object(orchestrator, "abteilung_laden", return_value=abt), \
             mock.patch.object(orchestrator, "senden"), \
             mock.patch.object(orchestrator, "_wochenbericht_faellig"), \
             mock.patch.object(ki_anbieter, "anbieter_bauen", return_value=pruefer):
            orchestrator.auftrag_anlegen("05 Einkauf China", "RFQ", "2099-01-01")
            orchestrator.lauf()
            daten = orchestrator.zustand_laden()
        a = daten["auftraege"][0]
        self.assertEqual(a["stand"], "nacharbeit")
        self.assertIn("Zink genannt", a["verlauf"][0]["begruendung"])
        self.assertEqual(a["verlauf"][0]["bearbeiter"], "openai")
        self.assertEqual(a["verlauf"][0]["gegenpruefung"]["pruefer"], "claude")


if __name__ == "__main__":
    unittest.main()
