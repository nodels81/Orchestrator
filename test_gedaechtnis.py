"""
test_gedaechtnis.py — Prueft das Gedaechtnis ohne API-Schluessel und ohne Kosten.

Aufruf auf dem Server:  venv/bin/python -m unittest test_gedaechtnis -v
Oder ohne venv:         python3 -m unittest test_gedaechtnis -v
"""

import os
import tempfile
import unittest

import gedaechtnis
from gedaechtnis import Gedaechtnis, _fts_frage, _schluessel, kurzfassung


def auftrag(nummer="A-2026-001", abteilung="05 Einkauf China",
            ziel="RFQ fuer HB-01 an Wenzhou Vigorous", versuche=0):
    return {
        "id": nummer,
        "abteilung": abteilung,
        "ziel": ziel,
        "kriterien": ["Ergebnis ist konkret", "Passt zur Marke"],
        "versuche": versuche,
    }


def ergebnis(text="Anfrage geschrieben und verschickt.", fakten=None, blocker=None):
    return {
        "ergebnis": text,
        "kriterien_erfuellt": [True, True],
        "blocker": blocker,
        "anmerkung": None,
        "zusammenfassung": "",
        "fakten": fakten or [],
    }


class GedaechtnisTest(unittest.TestCase):

    def setUp(self):
        self.ordner = tempfile.TemporaryDirectory()
        self.pfad = os.path.join(self.ordner.name, "test.db")
        self.g = Gedaechtnis(self.pfad)

    def tearDown(self):
        self.g.schliessen()
        self.ordner.cleanup()

    # ---------- Episoden ----------

    def test_episode_ist_wiederfindbar(self):
        self.g.episode_merken(auftrag(), ergebnis("Erstkontakt an Wenzhou Vigorous, 100 Stueck HB-01."))
        treffer = self.g.suchen("Wenzhou Vigorous")
        self.assertEqual(len(treffer["episoden"]), 1)
        self.assertEqual(treffer["episoden"][0]["auftrag_id"], "A-2026-001")

    def test_kontext_bleibt_leer_ohne_bezug(self):
        self.g.episode_merken(auftrag(), ergebnis())
        self.assertEqual(self.g.kontext("Steuererklaerung Umsatzsteuer Voranmeldung"), "")

    def test_kontext_nennt_fruehere_arbeit(self):
        self.g.episode_merken(auftrag(), ergebnis("Anfrage an Wenzhou Vigorous zu HB-01 geschrieben."))
        text = self.g.kontext("Nachfassen bei Wenzhou Vigorous zu HB-01")
        self.assertIn("A-2026-001", text)
        self.assertIn("FRUEHER SCHON BEARBEITET", text)

    def test_gescheiterte_episode_wird_nicht_als_wissen_angeboten(self):
        self.g.episode_merken(auftrag(), ergebnis("Halbe Sache.", blocker="Fehler"), bestanden=False)
        self.assertNotIn("A-2026-001", self.g.kontext("Halbe Sache Wenzhou"))

    # ---------- Fakten mit Gueltigkeit ----------

    def test_fakt_landet_im_kontext(self):
        self.g.fakten_merken(
            [{"subjekt": "Wenzhou Vigorous", "praedikat": "moq", "objekt": "300 Stueck"}],
            quelle="A-2026-001")
        text = self.g.kontext("Angebot von Wenzhou Vigorous pruefen")
        self.assertIn("300 Stueck", text)

    def test_neuer_wert_loest_alten_ab_statt_ihn_zu_loeschen(self):
        self.g.fakten_merken([{"subjekt": "Wenzhou Vigorous", "praedikat": "moq",
                               "objekt": "300 Stueck"}], quelle="A-2026-001")
        self.g.fakten_merken([{"subjekt": "Wenzhou Vigorous", "praedikat": "moq",
                               "objekt": "100 Stueck"}], quelle="A-2026-007")

        text = self.g.kontext("Wenzhou Vigorous Mindestmenge")
        self.assertIn("100 Stueck", text)
        self.assertNotIn("300 Stueck", text)          # der alte Wert stoert nicht mehr

        verlauf = self.g.verlauf("Wenzhou Vigorous", "moq")
        self.assertEqual(len(verlauf), 2)             # aber er ist noch nachlesbar
        self.assertIsNotNone(verlauf[1]["gueltig_bis"])

    def test_mehrwertige_praedikate_bleiben_nebeneinander(self):
        for produkt in ("HB-01", "LE-01"):
            self.g.fakten_merken([{"subjekt": "Wenzhou Vigorous", "praedikat": "fertigt",
                                   "objekt": produkt}], quelle="A-2026-001")
        text = self.g.kontext("Was fertigt Wenzhou Vigorous")
        self.assertIn("HB-01", text)
        self.assertIn("LE-01", text)

    def test_derselbe_fakt_zweimal_bleibt_einmal(self):
        fakt = [{"subjekt": "Wenzhou Vigorous", "praedikat": "moq", "objekt": "100 Stueck"}]
        self.assertEqual(self.g.fakten_merken(fakt, "A-1"), 1)
        self.assertEqual(self.g.fakten_merken(fakt, "A-2"), 0)

    def test_unbrauchbare_fakten_werden_verworfen(self):
        self.assertEqual(self.g.fakten_merken(
            [{"subjekt": "", "praedikat": "moq", "objekt": "100"}, "kaputt", None, 42], "A-1"), 0)

    def test_fakt_als_textzeile(self):
        self.assertEqual(self.g.fakten_merken(["HB-01 | material | Fettleder 3,5 mm"], "A-1"), 1)

    # ---------- Antwortspeicher ----------

    def test_wortgleicher_auftrag_kommt_ohne_api_zurueck(self):
        self.g.antwort_merken(auftrag(), "claude-sonnet-5", ergebnis(),
                              {"ein": 7000, "aus": 900})
        gespeichert = self.g.antwort_holen(auftrag(), "claude-sonnet-5")
        self.assertIsNotNone(gespeichert)
        self.assertIn("Gedaechtnis", gespeichert["anmerkung"])
        self.assertEqual(self.g.statistik()["gespart_gesamt"], 7900)

    def test_anderes_ziel_und_anderes_modell_treffen_nicht(self):
        self.g.antwort_merken(auftrag(), "claude-sonnet-5", ergebnis())
        self.assertIsNone(self.g.antwort_holen(auftrag(ziel="Etwas ganz anderes"), "claude-sonnet-5"))
        self.assertIsNone(self.g.antwort_holen(auftrag(), "claude-opus-5"))

    def test_schluessel_ignoriert_leerzeichen_und_grossschreibung(self):
        self.assertEqual(
            _schluessel(auftrag(ziel="RFQ fuer  HB-01"), "m"),
            _schluessel(auftrag(ziel="rfq FUER HB-01"), "m"))

    # ---------- Sparbuch und Pflege ----------

    def test_cache_treffer_werden_gutgeschrieben(self):
        self.g.episode_merken(auftrag(), ergebnis(),
                              verbrauch={"ein": 200, "aus": 800, "cache_gelesen": 7000})
        s = self.g.statistik()
        self.assertEqual(s["gespart"]["prompt_cache"]["tokens"], 6300)   # neun Zehntel von 7000

    def test_vergessen_raeumt_episoden_und_laesst_fakten_stehen(self):
        self.g.episode_merken(auftrag(), ergebnis())
        self.g.fakten_merken([{"subjekt": "HB-01", "praedikat": "breite", "objekt": "25 mm"}], "A-1")
        self.g.verb.execute("UPDATE episoden SET zeit = '2020-01-01T00:00:00'")
        self.assertEqual(self.g.vergessen(30), 1)
        s = self.g.statistik()
        self.assertEqual(s["episoden"], 0)
        self.assertEqual(s["fakten_aktuell"], 1)
        self.assertEqual(self.g.suchen("Wenzhou")["episoden"], [])       # auch aus der Suche raus


class HilfenTest(unittest.TestCase):
    """Die Suche darf an keiner Eingabe zerbrechen — sonst steht ein Auftrag still."""

    def test_sonderzeichen_werden_entschaerft(self):
        for eingabe in ('RFQ "HB-01" OR (NOT *)', "-- DROP TABLE kanten;", "***", "a AND b"):
            with tempfile.TemporaryDirectory() as ordner:
                with Gedaechtnis(os.path.join(ordner, "t.db")) as g:
                    g.episode_merken(auftrag(), ergebnis())
                    g.suchen(eingabe)
                    g.kontext(eingabe)

    def test_fuellwoerter_und_kurzes_fallen_weg(self):
        self.assertEqual(_fts_frage("und der die das"), "")
        self.assertEqual(_fts_frage(""), "")

    def test_kontext_haelt_das_budget_ein(self):
        with tempfile.TemporaryDirectory() as ordner:
            with Gedaechtnis(os.path.join(ordner, "t.db")) as g:
                for i in range(20):
                    g.episode_merken(auftrag(f"A-{i:03d}"), ergebnis("Wenzhou Vigorous HB-01 " * 200))
                self.assertLessEqual(len(g.kontext("Wenzhou Vigorous HB-01", budget_zeichen=800)), 820)

    def test_kurzfassung_schneidet_am_satzende(self):
        self.assertTrue(kurzfassung("Ein Satz. " * 100, 100).endswith("."))
        self.assertEqual(kurzfassung("Kurz."), "Kurz.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
