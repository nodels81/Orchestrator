"""test_modelle.py — Modell-Weiche ohne Netz, ohne Schluessel, ohne Kosten.

venv/bin/python -m unittest test_modelle -v
"""

import json
import unittest
from unittest import mock

import modelle

ALT = {"anthropic_api_key": "sk-ant-test", "modell": "claude-sonnet-5"}

NEU = {
    "modelle": {
        "standard": "anthropic:claude-sonnet-5",
        "ausweichen": "anthropic:claude-sonnet-5",
        "zuordnung": {
            "01 Innovation": "kimi:kimi-k2-0905-preview",
            "02 Produkt & Ausführung": "openai:gpt-5",
        },
        "anbieter": {
            "anthropic": {"api_key": "sk-ant-test"},
            "openai": {"api_key": "sk-openai-test"},
            "kimi": {"api_key": "sk-kimi-test"},
            "lokal": {"basis_url": "http://127.0.0.1:11434/v1"},
        },
    }
}


class Kennung(unittest.TestCase):
    def test_anbieter_und_modell(self):
        self.assertEqual(modelle.kennung_zerlegen("kimi:kimi-k2"), ("kimi", "kimi-k2"))

    def test_ollama_tag_bleibt_erhalten(self):
        self.assertEqual(modelle.kennung_zerlegen("lokal:qwen3:32b"), ("lokal", "qwen3:32b"))

    def test_ohne_anbieter_ist_anthropic(self):
        self.assertEqual(modelle.kennung_zerlegen("claude-sonnet-5"),
                         ("anthropic", "claude-sonnet-5"))


class AlteConfig(unittest.TestCase):
    def test_verhaelt_sich_wie_bisher(self):
        self.assertEqual(modelle.reihenfolge(ALT, "05 Einkauf China"),
                         ["anthropic:claude-sonnet-5"])

    def test_schluessel_aus_altem_feld(self):
        self.assertEqual(modelle.schluessel_fuer("anthropic", ALT), "sk-ant-test")

    def test_schluessel_aus_umgebung(self):
        with mock.patch.dict("os.environ", {"MOONSHOT_API_KEY": "sk-env"}):
            self.assertEqual(modelle.schluessel_fuer("kimi", ALT), "sk-env")


class Zuordnung(unittest.TestCase):
    def test_abteilung_bekommt_ihr_modell(self):
        self.assertEqual(modelle.reihenfolge(NEU, "01 Innovation"),
                         ["kimi:kimi-k2-0905-preview", "anthropic:claude-sonnet-5"])

    def test_unbekannte_abteilung_bekommt_standard(self):
        self.assertEqual(modelle.reihenfolge(NEU, "03 Vertrieb"), ["anthropic:claude-sonnet-5"])

    def test_auftrag_ueberstimmt_abteilung(self):
        folge = modelle.reihenfolge(NEU, "01 Innovation", {"modell": "lokal:qwen3:32b"})
        self.assertEqual(folge[0], "lokal:qwen3:32b")

    def test_uebersicht_zeigt_keine_schluessel(self):
        text = modelle.uebersicht(NEU, ["01 Innovation", "05 Einkauf China"])
        self.assertIn("kimi:kimi-k2-0905-preview", text)
        self.assertNotIn("sk-", text)


class _Antwort:
    def __init__(self, daten: dict):
        self._daten = json.dumps(daten).encode("utf-8")

    def read(self):
        return self._daten

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class OpenAIKompatibel(unittest.TestCase):
    def test_anfrage_und_verbrauch(self):
        gesehen = {}

        def urlopen(anfrage, timeout):
            gesehen["url"] = anfrage.full_url
            gesehen["kopf"] = dict(anfrage.header_items())
            gesehen["koerper"] = json.loads(anfrage.data.decode("utf-8"))
            return _Antwort({
                "choices": [{"message": {"content": '{"ergebnis": "ok"}'}}],
                "usage": {"prompt_tokens": 120, "completion_tokens": 30,
                          "prompt_tokens_details": {"cached_tokens": 100}},
            })

        with mock.patch("urllib.request.urlopen", urlopen):
            anbieter = modelle.anbieter_bauen("kimi", NEU)
            text, verbrauch = anbieter.anfragen("kimi-k2", "SYSTEM", "NUTZER", 500)

        self.assertEqual(text, '{"ergebnis": "ok"}')
        self.assertEqual(verbrauch, {"ein": 120, "aus": 30, "cache_gelesen": 100,
                                     "cache_geschrieben": 0})
        self.assertEqual(gesehen["url"], "https://api.moonshot.ai/v1/chat/completions")
        self.assertEqual(gesehen["kopf"]["Authorization"], "Bearer sk-kimi-test")
        self.assertEqual(gesehen["koerper"]["model"], "kimi-k2")
        self.assertEqual(gesehen["koerper"]["messages"][0],
                         {"role": "system", "content": "SYSTEM"})
        self.assertEqual(gesehen["koerper"]["response_format"], {"type": "json_object"})

    def test_lokal_ohne_schluessel_und_ohne_json_modus(self):
        gesehen = {}

        def urlopen(anfrage, timeout):
            gesehen["kopf"] = dict(anfrage.header_items())
            gesehen["koerper"] = json.loads(anfrage.data.decode("utf-8"))
            return _Antwort({"choices": [{"message": {"content": "{}"}}]})

        with mock.patch("urllib.request.urlopen", urlopen):
            modelle.anbieter_bauen("lokal", NEU).anfragen("qwen3:32b", "S", "N", 10)

        self.assertNotIn("Authorization", gesehen["kopf"])
        self.assertNotIn("response_format", gesehen["koerper"])

    def test_fehlender_schluessel_ist_modellfehler(self):
        config = {"modelle": {"anbieter": {"openai": {"api_key": ""}}}}
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(modelle.ModellFehler):
                modelle.anbieter_bauen("openai", config)


class Ausweichen(unittest.TestCase):
    def test_zweites_modell_uebernimmt(self):
        class Kaputt(modelle.Anbieter):
            def anfragen(self, *a, **k):
                raise modelle.ModellFehler("weg")

        class Geht(modelle.Anbieter):
            def anfragen(self, *a, **k):
                return "antwort", {"ein": 1, "aus": 1, "cache_gelesen": 0, "cache_geschrieben": 0}

        def bauen(name, config):
            return Kaputt({}, config) if name == "kimi" else Geht({}, config)

        with mock.patch("modelle.anbieter_bauen", bauen):
            auswahl = modelle.Auswahl(NEU, "01 Innovation")
            text, _, kennung = auswahl.anfragen("S", "N", 10)

        self.assertEqual(text, "antwort")
        self.assertEqual(kennung, "anthropic:claude-sonnet-5")

    def test_alle_weg_ist_fehler(self):
        class Kaputt(modelle.Anbieter):
            def anfragen(self, *a, **k):
                raise modelle.ModellFehler("weg")

        with mock.patch("modelle.anbieter_bauen", lambda n, c: Kaputt({}, c)):
            with self.assertRaises(modelle.ModellFehler):
                modelle.Auswahl(NEU, "01 Innovation").anfragen("S", "N", 10)


if __name__ == "__main__":
    unittest.main()
