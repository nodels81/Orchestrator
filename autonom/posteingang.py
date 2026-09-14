"""
posteingang.py — Der Rueckkanal: Bjoern schreibt eine Mail, der Server handelt.

Grund: Der Betrieb laeuft 24/7 auf dem Server, auch wenn kein Rechner an ist.
Damit Bjoern von unterwegs eingreifen kann, ohne SSH und ohne App, liest dieser
Dienst alle paar Minuten das Postfach des Orchestrators und fuehrt genau die
Befehle aus, die unten in BEFEHLE stehen. Die Antwort geht per Mail zurueck.

SICHERHEIT — bitte lesen:
  Ein Absender im Feld "From" ist faelschbar. Er allein schuetzt nichts.
  Deshalb gilt beides gleichzeitig:
    1. Die Absenderadresse muss mail.empfaenger aus config.json sein.
    2. Im Betreff muss das Kennwort aus autonom.kennwort stehen.
  Das Kennwort ist der eigentliche Schutz. Wer es kennt, darf Auftraege
  anlegen — mehr nicht. Es gibt bewusst KEINEN Befehl, der eine Shell oeffnet,
  Dateien schreibt oder Geld ausgibt.

Aufrufe:
  posteingang.py             Einmal abholen und beantworten
  posteingang.py --probe     Zeigen, was passieren wuerde, ohne zu handeln
"""

import email
import imaplib
import io
import os
import re
import ssl
import sys
from contextlib import redirect_stdout
from email.header import decode_header, make_header
from email.utils import parseaddr

# Der Betriebsordner liegt eine Ebene hoeher. Python legt beim Start nur den
# Ordner des Skripts auf den Suchpfad, nicht das Arbeitsverzeichnis — ohne diese
# Zeile findet systemd die Module abteilung_basis, orchestrator und tagesbrief nicht.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abteilung_basis import BASIS, config_laden
from orchestrator_mail import senden

PROTOKOLL = os.path.join(BASIS, "logs", "posteingang.log")
MAX_MAILS_PRO_LAUF = 10


# ---------- Hilfen ----------

def _protokoll(zeile: str) -> None:
    from datetime import datetime
    os.makedirs(os.path.dirname(PROTOKOLL), exist_ok=True)
    stempel = datetime.now().isoformat(timespec="seconds")
    with open(PROTOKOLL, "a", encoding="utf-8") as f:
        f.write(f"{stempel}  {zeile}\n")
    print(zeile)


def _klartext(rohwert: str | None) -> str:
    if not rohwert:
        return ""
    try:
        return str(make_header(decode_header(rohwert)))
    except Exception:
        return rohwert


def _koerper(nachricht) -> str:
    """Nur den reinen Text nehmen. HTML-Teile werden ignoriert."""
    if not nachricht.is_multipart():
        nutzlast = nachricht.get_payload(decode=True) or b""
        return nutzlast.decode(nachricht.get_content_charset() or "utf-8", "replace")
    for teil in nachricht.walk():
        if teil.get_content_type() == "text/plain":
            nutzlast = teil.get_payload(decode=True) or b""
            return nutzlast.decode(teil.get_content_charset() or "utf-8", "replace")
    return ""


def _ohne_zitat(text: str) -> str:
    """Alles ab der ersten Zitatzeile abschneiden, sonst liest man alte Mails mit."""
    zeilen = []
    for zeile in text.splitlines():
        if zeile.startswith(">") or zeile.startswith("Am ") and " schrieb" in zeile:
            break
        if zeile.strip() in ("--", "-- "):
            break
        zeilen.append(zeile)
    return "\n".join(zeilen).strip()


# ---------- Befehle ----------

def _befehl_stand(_rest: str) -> str:
    import orchestrator
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        orchestrator.stand_zeigen()
    text = puffer.getvalue() or "Keine Auftraege."
    try:
        import ausliefern
        text += "\n\n" + ausliefern.stand_text()
    except Exception:
        pass  # Auslieferung noch nicht eingerichtet — der Stand gilt trotzdem.
    return text


def _befehl_wochenbericht(_rest: str) -> str:
    import orchestrator
    return orchestrator.wochenbericht_text()


def _befehl_brief(_rest: str) -> str:
    import tagesbrief
    return tagesbrief.text_bauen()


def _befehl_auftrag(rest: str) -> str:
    """auftrag <Abteilung> | <Ziel> [| JJJJ-MM-TT]"""
    import orchestrator
    teile = [t.strip() for t in rest.split("|")]
    if len(teile) < 2 or not teile[0] or not teile[1]:
        return ('Aufbau: auftrag <Abteilung> | <Ziel> [| JJJJ-MM-TT]\n'
                'Beispiel: auftrag 01 Innovation | Pflegeset PF-01 durchrechnen\n\n'
                "Bekannte Abteilungen:\n"
                + "\n".join(f"  {a}" for a in orchestrator.ABTEILUNGEN))
    frist = teile[2] if len(teile) > 2 and teile[2] else None
    if frist and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", frist):
        return f"Frist '{frist}' ist kein Datum im Format JJJJ-MM-TT."
    try:
        auftrag = orchestrator.auftrag_anlegen(teile[0], teile[1], frist)
    except ValueError as fehler:
        return str(fehler)
    return (f"Angelegt: {auftrag['id']}\n"
            f"Abteilung: {auftrag['abteilung']}\n"
            f"Ziel: {auftrag['ziel']}\n"
            f"Frist: {auftrag['frist']}\n\n"
            "Der naechste Lauf nimmt ihn auf.")


def _befehl_ausliefern(_rest: str) -> str:
    """Auf die Testdomain. Nie auf den Shop — dafuer gibt es 'freigeben'."""
    import ausliefern
    code = ausliefern.ausliefern("test")
    if code == 0:
        return ("Auf die Testdomain ausgeliefert. Eine eigene Mail mit Kennung "
                "und Adresse ist unterwegs.\n\n" + ausliefern.stand_text())
    return ("Die Auslieferung ist gescheitert. Einzelheiten stehen in der "
            "Fehlermail und in logs/ausliefern.log.")


def _befehl_freigeben(rest: str) -> str:
    """Gibt genau die Kennung frei, die vorher auf der Testdomain stand."""
    import ausliefern
    wartend = ausliefern.zustand_laden().get("wartet_auf_freigabe")
    if not wartend:
        return "Es wartet nichts auf Freigabe.\n\n" + ausliefern.stand_text()

    kennung = rest.strip() or None
    if kennung and kennung != wartend:
        return (f"Die Kennung {kennung!r} passt nicht.\n"
                f"Auf Freigabe wartet: {wartend}\n\n"
                "Nichts wurde ausgeliefert. Schreib die Kennung genau so, wie sie "
                "in der Mail steht — sie bindet die Freigabe an den Stand, den du "
                "wirklich gesehen hast.")
    if not kennung:
        return (f"Bitte die Kennung mitschicken:\n\n    freigeben {wartend}\n\n"
                "Ohne Kennung gebe ich nichts frei. Zwischen deinem Blick auf die "
                "Testdomain und dieser Mail kann ein neuer Stand entstanden sein.")

    code = ausliefern.ausliefern("live", kennung)
    if code == 0:
        return f"Freigegeben und auf den Shop gebracht: {kennung}"
    return ("Die Auslieferung auf den Shop ist gescheitert. Wenn eine Sicherung "
            "griff, steht der vorherige Stand wieder. Einzelheiten in der Fehlermail.")


def _befehl_hilfe(_rest: str) -> str:
    return (
        "Befehle. Einer pro Mail, in der ersten Zeile des Textes.\n"
        "Das Kennwort muss im Betreff stehen.\n\n"
        "  stand            Woran wird gerade gearbeitet\n"
        "  brief            Den Tagesbrief sofort schicken\n"
        "  wochenbericht    Die Wochenuebersicht\n"
        "  auftrag <Abteilung> | <Ziel> [| JJJJ-MM-TT]\n"
        "  ausliefern       Den aktuellen Stand auf die Testdomain bringen\n"
        "  freigeben <Kennung>  Den geprueften Stand auf den Shop bringen\n"
        "  hilfe            Diese Liste\n\n"
        "Die Kennung steht in der Mail von der Testdomain. Ohne sie wird nichts\n"
        "freigegeben: zwischen deinem Blick und der Freigabe kann ein neuer Stand\n"
        "entstanden sein, und dann ginge etwas live, das niemand gesehen hat.\n\n"
        "Zwei Kennwoerter: deins darf alles. Das Agentenkennwort darf alles ausser\n"
        "'freigeben' — auf den laufenden Shop schiebst nur du.\n\n"
        "Absichtlich nicht vorhanden: Shell, Dateien schreiben, Geld ausgeben,\n"
        "Bestellungen ausloesen. Das bleibt bei dir."
    )


BEFEHLE = {
    "stand": _befehl_stand,
    "brief": _befehl_brief,
    "tagesbrief": _befehl_brief,
    "wochenbericht": _befehl_wochenbericht,
    "auftrag": _befehl_auftrag,
    "ausliefern": _befehl_ausliefern,
    "freigeben": _befehl_freigeben,
    "hilfe": _befehl_hilfe,
}


# ---------- Ablauf ----------

# Befehle, die das Agentenkennwort NICHT ausfuehren darf.
# "freigeben" schiebt auf den laufenden Shop. Das bleibt bei Bjoern, und zwar
# nicht aus Misstrauen: Der Gmail-Zugang des Agenten sendet aus Bjoerns Konto,
# eine Agentenmail sieht also aus wie eine von ihm. Die Absenderpruefung
# unterscheidet die beiden nicht — das Kennwort ist der einzige Unterschied.
NUR_BJOERN = {"freigeben"}

# mailin.py liest dasselbe Postfach und beantwortet Antworten auf
# "[Bello] A-2026-NNN <Abteilung> — ..."-Threads. Dieselbe Mail darf nicht
# von beiden bearbeitet werden, sonst entstehen zwei Auftraege aus einem
# Satz. Der Betreff trennt sauber: was nach einem Bello-Thread aussieht,
# gehoert mailin.py, alles andere uns. Regex wortgleich aus mailin.py.
MAILIN_BETREFF = re.compile(r"\[Bello\]\s+(A-\d{4}-\d+)\s+(.+?)\s+[\u2014-]")


def _adresse_normal(adresse: str) -> str:
    """Eine Gmail-Adresse auf ihre eine wahre Form bringen.

    Google liefert dasselbe Postfach unter mehreren Schreibweisen aus:
    googlemail.com und gmail.com sind identisch, Punkte im Namensteil werden
    ignoriert, und alles hinter einem Pluszeichen ist eine frei waehlbare
    Ergaenzung. Ein Zeichenvergleich sieht darin vier verschiedene Absender.

    Gefunden, weil eine Mail von pijoern.nodels@googlemail.com abgewiesen wurde,
    obwohl in der Liste pijoern.nodels@gmail.com stand -- dasselbe Postfach.

    Bei allen anderen Anbietern wird nur klein geschrieben: dort ist der
    Namensteil laut Norm unterscheidend, und Punkte zu entfernen wuerde
    fremde Adressen zusammenfallen lassen.
    """
    adresse = (adresse or "").strip().lower()
    if "@" not in adresse:
        return adresse
    name, _, bereich = adresse.rpartition("@")
    if bereich in ("gmail.com", "googlemail.com"):
        name = name.split("+", 1)[0].replace(".", "")
        bereich = "gmail.com"
    return f"{name}@{bereich}"


def _pruefen(config: dict, absender: str, betreff: str) -> tuple[str | None, str]:
    """Gibt (Ablehnungsgrund, Rolle) zurueck. Grund None heisst: in Ordnung.

    Rolle ist "bjoern" oder "agent" — je nachdem, welches Kennwort im Betreff
    stand. Davon haengt ab, welche Befehle erlaubt sind.
    """
    autonom = config.get("autonom", {})
    kennwort = autonom.get("kennwort", "")
    kennwort_agent = autonom.get("kennwort_agent", "")
    erlaubt = _adresse_normal(config.get("mail", {}).get("empfaenger") or "")

    if not kennwort:
        return "autonom.kennwort fehlt in config.json — Eingang ist abgeschaltet", ""
    if not erlaubt:
        return "mail.empfaenger fehlt in config.json", ""
    if _adresse_normal(parseaddr(absender)[1]) != erlaubt:
        return f"Absender {absender!r} ist nicht {erlaubt}", ""

    betreff_klein = betreff.lower()
    if kennwort.lower() in betreff_klein:
        return None, "bjoern"
    if kennwort_agent and kennwort_agent.lower() in betreff_klein:
        return None, "agent"
    return "Kennwort fehlt im Betreff", ""


def _ausfuehren(text: str, probe: bool = False, rolle: str = "bjoern") -> tuple[str, str]:
    """Erste nicht leere Zeile ist der Befehl. Gibt (Befehlsname, Antwort).

    Im Probelauf wird der Befehl nur benannt, nicht ausgefuehrt. Sonst wuerde
    'auftrag' auch beim Probieren einen Auftrag in auftraege.json schreiben.
    """
    zeilen = [z for z in _ohne_zitat(text).splitlines() if z.strip()]
    if not zeilen:
        return "leer", _befehl_hilfe("")
    erste = zeilen[0].strip()
    wort = erste.split()[0].lower().rstrip(":")
    rest = erste[len(wort):].lstrip(" :")
    funktion = BEFEHLE.get(wort)
    if not funktion:
        return wort, f"Unbekannter Befehl {wort!r}.\n\n" + _befehl_hilfe("")
    if rolle == "agent" and wort in NUR_BJOERN:
        return wort, (
            f"Der Befehl {wort!r} ist mit diesem Kennwort nicht erlaubt.\n\n"
            "Auf den laufenden Shop schiebt nur Bjoern, mit seinem eigenen "
            "Kennwort. Alles andere — Auftraege, Stand, Ausliefern auf die "
            "Baustelle — geht."
        )
    if probe:
        return wort, f"(Probelauf — nicht ausgefuehrt) {wort} {rest}".strip()
    return wort, funktion(rest)


def abholen(probe: bool = False) -> int:
    config = config_laden()
    mail = config.get("mail", {})
    autonom = config.get("autonom", {})

    konto = mail.get("absender")
    passwort = mail.get("app_passwort")
    server = autonom.get("imap_server", "imap.gmail.com")
    port = int(autonom.get("imap_port", 993))
    # Ohne Zeitlimit haengt der Dienst bei gestoertem Postfach, bis systemd ihn
    # nach TimeoutStartSec abwuergt. Lieber nach 30 Sekunden aufgeben und es in
    # fuenf Minuten noch einmal versuchen.
    zeitlimit = int(autonom.get("timeout_sekunden", 30))

    if not (konto and passwort):
        _protokoll("[EINGANG] Nicht konfiguriert (mail.absender / mail.app_passwort).")
        return 1

    kontext = ssl.create_default_context()
    try:
        with imaplib.IMAP4_SSL(server, port, ssl_context=kontext,
                               timeout=zeitlimit) as imap:
            imap.login(konto, passwort)
            imap.select("INBOX")
            _, antwort = imap.search(None, "UNSEEN")
            kennungen = antwort[0].split()[:MAX_MAILS_PRO_LAUF]

            if not kennungen:
                print("Nichts Neues im Postfach.")
                return 0

            for kennung in kennungen:
                _, daten = imap.fetch(kennung, "(RFC822)")
                nachricht = email.message_from_bytes(daten[0][1])
                absender = _klartext(nachricht.get("From"))
                betreff = _klartext(nachricht.get("Subject"))

                if MAILIN_BETREFF.search(betreff):
                    # Nicht als gelesen markieren: mailin.py holt sie sich,
                    # und Bjoern soll sie im Postfach weiter sehen.
                    _protokoll(f"[EINGANG] mailin.py ueberlassen | Betreff: {betreff!r}")
                    continue

                grund, rolle = _pruefen(config, absender, betreff)
                if grund:
                    _protokoll(f"[EINGANG] Abgewiesen: {grund} | Betreff: {betreff!r}")
                    if not probe:
                        imap.store(kennung, "+FLAGS", "\\Seen")
                    continue

                wort, antworttext = _ausfuehren(_koerper(nachricht), probe=probe, rolle=rolle)
                if probe:
                    print(f"[Probe] Wuerde ausfuehren: {wort}\n{antworttext}")
                    continue

                _protokoll(f"[EINGANG] Ausgefuehrt: {wort} | Rolle: {rolle} | Betreff: {betreff!r}")
                senden(f"[Bello] Antwort: {wort}", antworttext, config)
                imap.store(kennung, "+FLAGS", "\\Seen")

    except imaplib.IMAP4.error as fehler:
        _protokoll(f"[EINGANG] FEHLER Anmeldung: {fehler}")
        return 1
    except (TimeoutError, OSError) as fehler:
        _protokoll(f"[EINGANG] Postfach nicht erreichbar: {fehler}")
        return 1
    except Exception as fehler:
        _protokoll(f"[EINGANG] FEHLER: {fehler}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(abholen(probe="--probe" in sys.argv))
