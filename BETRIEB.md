# Bello – Betriebsanleitung

Kurzfassung für den Alltag. Der Server macht **nur** den KI-Agentenbetrieb, sonst nichts.
Alle Befehle als `root` per SSH auf dem Server.

Der Agent läuft **automatisch jeden Morgen um 07:00**. Er meldet sich per Mail nur,
wenn er eine Entscheidung von dir braucht oder etwas kaputt ist. Stille ist der Normalfall.

---

## Woran wird gerade gearbeitet?

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py --stand
```

Ein `!` vor einer Zeile heißt: **wartet auf deine Entscheidung**.

Wochenüberblick:

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py --wochenbericht
```

Hilfe / alle Aufrufe:

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py --hilfe
```

---

## Einen Auftrag von Hand geben

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py \
  --auftrag "01 Innovation" "Kurze Marktbeobachtung Fettleder-Halsbänder 69–99 €" 2026-10-01
```

Die Belegschaft (im Aufruf nutzt du den Namen in Anführungszeichen, nicht den Vornamen):

| Aufruf | Name | Aufgabe |
|---|---|---|
| `"01 Innovation"` | Merle | Marktbeobachtung, Produktkonzepte |
| `"02 Produkt & Ausführung"` | Konrad | Spezifikation, Stückliste, bemaßte Zeichnung |
| `"03 Vertrieb"` | Silke | Angebote und Kundenantworten als Entwurf |
| `"04 Social Media"` | Lasse | Beitragstexte, Aufnahmeanweisungen |
| `"05 Personal"` | Wiebke | erkennt Bedarf, entwirft neue Abteilungen |
| `"06 Einkauf"` | Insa | allgemeine Lieferantenanfragen (Inland/EU) |
| `"07 Einkauf China"` | Henrik | RFQ / Verhandlung / Muster mit China |
| `"08 Design"` | Thea | entwirft die **Form** (Silhouette, Proportionen, Beschlag-Layout) — vor Konrad |

Der Orchestrator, der alles verteilt, prüft und dir schreibt, heißt **Gustav** (= die
Absenderadresse `gustav.bellowerk@gmail.com`). Die Frist am Ende ist optional (Standard: 7 Tage).

Beim `--auftrag` kannst du die Abteilung auf **drei Arten** angeben — alle gleichwertig:

```
--auftrag "07 Einkauf China" "..."      # langer Name
--auftrag "07" "..."                     # Nummer
--auftrag "Henrik" "..."                 # Vorname
```

Nur `"Einkauf"` allein ist mehrdeutig (Insa **und** Henrik) — dann `"06"`/`"Insa"` bzw.
`"07"`/`"Henrik"` nehmen. Im gespeicherten Auftrag steht immer der lange Name.

Der Auftrag wird beim **nächsten Lauf** abgearbeitet. Sofort abarbeiten:

```
sudo systemctl start bello-orchestrator.service
```

Trockenlauf ohne API-Kosten und ohne Mail:

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py --probelauf
```

---

## Wiebke: neue Abteilungen entwerfen lassen

Wiebke (`"05 Personal"`) ist die Personalabteilung. Sie baut **keine** Agenten selbst —
sie schreibt die komplette Stellenbeschreibung als Entwurf und schickt sie dir per Mail
mit ihren Rückfragen. Du entscheidest.

Auftrag an Wiebke, z. B.:

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py \
  --auftrag "05 Personal" "Brauchen wir eine Abteilung für Lieferantenanfragen (Fettleder, Messing)? Wenn ja, entwirf sie." 2026-09-30
```

Sie liefert: Bedarf, Nummer/Name, den fertigen Rollentext, was die Abteilung abgibt,
Abnahmekriterien, Grenzen, einen ersten Testauftrag und ihre Rückfragen an dich.
Kommt sie zum Schluss „keine neue Abteilung nötig", ist auch das ihr Ergebnis.

**Freigegebene Abteilung einbauen** (Handarbeit, nicht Wiebke):
1. Datei `/opt/bello/abteilung_<name>.py` nach dem Muster von `abteilung_vertrieb.py` anlegen,
   Wiebkes ROLLE-Text als `ROLLE` eintragen, `NUMMER`/`NAME` setzen.
2. In `/opt/bello/orchestrator.py` im Block `ABTEILUNGEN` eine Zeile ergänzen:
   `"06 Name": ("abteilung_<name>", "Klassenname"),`
3. In `abteilung_personal.py` die Liste `BESETZUNG` ergänzen, damit Wiebke sie kennt.
4. `sudo -u bello /opt/bello/.venv/bin/python -m py_compile /opt/bello/*.py` — keine Ausgabe = gut.
5. Probelauf: `--probelauf`, dann Wiebkes ersten Testauftrag geben.

---

## Einkauf China beauftragen

Abteilung 07 kennt Markenbrief, Tech Packs, die Lieferanten-Shortlist und drei Wissensdateien
(`sourcing/wissen/` — Plattformen, Verhandlung, Materialkunde). Sie schreibt sendefertige
englische Nachrichten an Hersteller, verschickt aber **nichts** selbst — jeder Entwurf und
jede Geldfrage kommt als Entscheidung zu dir.

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py \
  --auftrag "07 Einkauf China" "Erstkontakt/RFQ (Vorlage 01) für HB-01 und LE-01 an Kingming Pet, 100 Stück je Modell, Muster zuerst" 2026-09-19
```

Weitere sinnvolle Aufträge: `"Angebote von A und B vergleichen"`, `"Nachfassen bei X (Vorlage 02)"`,
`"Musterbestellung vorbereiten (Vorlage 03) für …"`, `"Musterfeedback an X: Punkt 1 … Punkt 2 …"`.

Materialien liegen in `sourcing/bellowerk/` (Zeichnungen, Fotos, Specs), die du an die
Lieferanten anhängst — Dateinamen nennt der Agent im Entwurf.

---

## Ein Design in Auftrag geben

Thea (08 Design) macht die **Form** — Silhouette, Breitenverlauf, wo die Beschläge sitzen,
Größenlogik — als Entwurf mit einfacher bemaßter Silhouette (SVG unter `daten/zeichnungen/`).
Material und Beschläge sind für sie gesetzt (Fettleder, Messing, Buchschrauben). Die
Feinzeichnung macht danach Konrad (02).

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py \
  --auftrag "Thea" "Drei Formentwürfe Halsband, zwei Führleine. Nur Form. Sollen sich klar unterscheiden." 2026-09-24
```

Danach: die Entwürfe, die dir gefallen, an Konrad weiterreichen —
`--auftrag "Konrad" "Führe Entwurf X aus A-2026-006 aus: Spezifikation, Stückliste, bemaßte Zeichnung"`.

---

## Neue Code-Version holen

`/opt/bello` ist ein git-Repo (`github.com/nodels81/Orchestrator`). Updates:

```
cd /opt/bello
sudo git pull
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/orchestrator.py --probelauf
```

`config.json`, `daten/`, `logs/` und die venv sind per `.gitignore` ausgenommen und bleiben
beim Pull unangetastet. Meldet `git pull` einen Konflikt in einer `.py`-Datei, nicht raten —
melden, dann wird gemergt.

---

## Übersicht auf einen Blick

Nach jedem Tageslauf schreibt der Server eine Übersichtsseite:

```
/opt/bello/daten/dashboard.html
```

Die „Werkbank" zeigt: offene Entscheidungen mit den konkreten Fragen, jede Abteilung
einzeln (Stand, aktueller Auftrag, was von dir gebraucht wird, nächster Schritt), das
Zusammenspiel-Diagramm (wer mit wem), einen Kasten „was der Orchestrator tut", alle
Aufträge und den Systemstand.

Auf den eigenen Rechner holen und im Browser öffnen (aus einem **normalen** PowerShell-Fenster,
nicht aus der SSH-Sitzung):

```
scp root@v2202609413684515441.powersrv.de:/opt/bello/daten/dashboard.html $HOME\Desktop\bello.html
```

Jederzeit von Hand neu erzeugen:

```
sudo -u bello /opt/bello/.venv/bin/python /opt/bello/bin/dashboard.py
```

Eine versionierte Kopie liegt zusätzlich unter `/opt/bello/dashboard/dashboard.html` und geht
mit ins GitHub-Repo, sobald gepusht wird.

---

## Wo liegt was?

| Was | Wo |
|---|---|
| Programm­code | `/opt/bello/*.py` |
| Konfiguration (ohne Geheimnisse) | `/opt/bello/config.json` |
| Geheimnisse (API-Key, Mail-Passwort) | `/etc/bello/env` – nur für root lesbar |
| Auftragsstand | `/opt/bello/daten/auftraege.json` |
| Zeichnungen der Abteilung 02 | `/opt/bello/daten/zeichnungen/` |
| Logs pro Tag | `/opt/bello/logs/orchestrator-JJJJ-MM-TT.log` |
| Backups | `/var/backups/bello/` |

Log von heute ansehen:

```
tail -n 50 /opt/bello/logs/orchestrator-$(date +%F).log
```

Letzter Lauf im systemd-Journal:

```
journalctl -u bello-orchestrator.service -n 50
```

---

## Vom Handy: per Mail-Antwort einen Auftrag geben

Antworte aus der Gmail-App auf eine Ergebnis-Mail einer Abteilung. Die **erste Zeile** steuert:

| Erste Zeile der Antwort | Wirkung |
|---|---|
| `@Konrad Führe Steg und Taille aus` | Auftrag an Konrad (02) |
| `@Henrik Zweiten Lieferanten anschreiben` | Auftrag an Henrik (07) |
| `Auftrag: Noch eine Variante mit +40 %` | Auftrag an die Abteilung aus dem Betreff |
| `Danke, passt` | nichts (kein Schlüsselwort) |

Der Rest der Mail ist Kontext. Du bekommst sofort eine Bestätigung; der Auftrag läuft beim
nächsten 07:00-Lauf. Nur Mails von deiner Adresse werden verarbeitet, nur `[Bello]`-Threads.

Prüfen / anhalten:

```
systemctl list-timers bello-mailin.timer          # wann wird geprüft
sudo systemctl start bello-mailin.service         # jetzt sofort prüfen
sudo systemctl disable --now bello-mailin.timer   # abschalten
```

---

## Den Tageslauf anhalten und wieder starten

Anhalten (Agent macht dann gar nichts mehr):

```
sudo systemctl disable --now bello-orchestrator.timer
```

Wieder anschalten:

```
sudo systemctl enable --now bello-orchestrator.timer
```

Läuft der Timer? Wann das nächste Mal?

```
systemctl list-timers 'bello-*'
```

---

## Geheimnisse eintragen oder ändern

```
sudo nano /etc/bello/env
```

Dort `ANTHROPIC_API_KEY` und `SMTP_PASSWORT` eintragen (je eine Zeile `NAME=Wert`,
keine Anführungszeichen). Danach testen:

```
sudo systemctl start bello-orchestrator.service
journalctl -u bello-orchestrator.service -n 30
```

---

## Eine Sicherung zurückspielen

Backups liegen als `bello-JJJJ-MM-TT_HHMMSS.tar.gz` in `/var/backups/bello/`,
`bello-neueste.tar.gz` zeigt auf das jüngste. Aufbewahrung: 14 Tage.

Inhalt eines Backups ansehen:

```
tar -tzf /var/backups/bello/bello-neueste.tar.gz
```

Kompletten Stand zurückspielen (überschreibt aktuelle Dateien):

```
sudo systemctl stop bello-orchestrator.timer
sudo tar -xzf /var/backups/bello/bello-neueste.tar.gz -C /
sudo chown -R bello:bello /opt/bello/daten /opt/bello/config.json
sudo systemctl start bello-orchestrator.timer
```

Nur den Auftragsstand aus einem bestimmten Backup holen:

```
sudo tar -xzf /var/backups/bello/bello-2026-09-09_063000.tar.gz \
  -C / opt/bello/daten/auftraege.json
sudo chown bello:bello /opt/bello/daten/auftraege.json
```

Sicherung sofort auslösen:

```
sudo systemctl start bello-backup.service
```

---

## „Keine Mail angekommen"

Der Agent schickt Mail über `gustav.bellowerk@gmail.com` an `pijoern.nodels@gmail.com`.

1. **Kommt SMTP überhaupt raus?**

   ```
   nc -zv smtp.gmail.com 587
   ```

   *Hängt / „timed out":* netcup blockiert den Mailversand. Das muss **im netcup
   Server Control Panel** (servercontrolpanel.de) abgeschaltet werden:
   Server auswählen → **Firewall / Mail** → Eintrag **„netcup Mail Block" / „Mailsperre"
   entfernen** → ein paar Minuten warten. Das ist kein Software-Problem, am Server
   selbst lässt sich das nicht lösen.

2. **Testmail schicken:**

   ```
   cd /opt/bello && sudo -u bello --preserve-env=SMTP_PASSWORT \
     bash -c 'set -a; . /etc/bello/env; set +a; .venv/bin/python orchestrator_mail.py --test'
   ```

   - `App-Passwort falsch`: neues Gmail-App-Passwort erzeugen
     (Google-Konto → Sicherheit → 2-Faktor → App-Passwörter) und in `/etc/bello/env`
     bei `SMTP_PASSWORT` eintragen.
   - `Gesendet an ...`: passt. Wenn trotzdem nichts ankommt, im Gmail-Postfach
     von `pijoern.nodels@gmail.com` den Spam-Ordner prüfen.

3. **Schlägt ein Tageslauf fehl**, verschickt der Server automatisch eine Mail
   „[Bello] Tageslauf FEHLGESCHLAGEN" mit den letzten Log-Zeilen. Kommt die nicht,
   aber der Lauf ist rot (`systemctl list-timers`, `journalctl -u bello-orchestrator.service`),
   dann steckt das Problem im Mailweg – siehe Punkt 1.

---

## Grundregel, die im System verankert ist

Der Agent gibt **nie** selbst Geld aus, bestellt nichts, sagt keine Preise nach außen zu.
Jedes Ergebnis, jeder Vorschlag geht als **Entwurf** per Mail an dich und wartet auf
dein „ja". Ein Lauf pro Tag, keine Dauerschleife.
