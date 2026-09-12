# Serverabgleich — bevor auf /opt/bello wieder gepullt wird

Stand 11.09.2026. Befund aus den Auftragsmails vom 9. und 10. September.

## Der Befund

Der Server ist weiter als dieses Repo. In den Mails tauchen Abteilungen auf, die es hier
nicht gibt, und die Nummerierung stimmt nicht mehr überein:

| Nummer | Auf dem Server (aus den Mails belegt) | In diesem Repo |
|---|---|---|
| 01 | Innovation | Innovation |
| 02 | Produkt & Ausführung | Produkt & Ausführung |
| 03 | — | Vertrieb |
| 04 | — | Social Media |
| 05 | — | Einkauf China |
| 06 | **Einkauf** | **Web & Shop** ← Kollision |
| 07 | **Einkauf China** | fehlt |
| 08 | **Design** ("Thea") | fehlt |
| 09 | **Qualität** | fehlt |
| 10 | **Homepage** | fehlt |

Belegt durch: A-2026-003 (06 Einkauf), A-2026-005 (07 Einkauf China), A-2026-006 und
A-2026-007 (08 Design), A-2026-008 (09 Qualität), A-2026-009 (10 Homepage),
A-2026-010 (02 Produkt & Ausführung).

## Die Gefahr

`orchestrator.py` in diesem Repo enthält ein `ABTEILUNGEN`-Verzeichnis mit nur 01 bis 06.
Ein `git pull` auf `/opt/bello` **überschreibt das Verzeichnis des Servers**. Danach kennt
der Orchestrator die Abteilungen 07 bis 10 nicht mehr, und jeder laufende Auftrag dieser
Abteilungen bricht mit "Unbekannte Abteilung" ab. Die Dateien `abteilung_design.py` und so
weiter blieben zwar liegen, wären aber nicht mehr registriert.

Zusätzlich kollidiert die hier angelegte Abteilung "06 Web & Shop" mit "06 Einkauf" auf dem
Server und macht inhaltlich dasselbe wie das dortige "10 Homepage".

**Also: auf /opt/bello nicht pullen, bevor die folgenden Schritte gelaufen sind.**

## Schritt 1 — Sichern, mit einem Kommando

`sicherung.sh` liegt in diesem Repo und macht die Sicherung vollständig. Es löscht nichts,
pullt nichts und überschreibt nichts.

```bash
cd /opt/bello
bash sicherung.sh
```

Drei Dinge passieren:

1. **Tararchiv** des ganzen Ordners ohne `venv` und Caches nach `/opt/bello-sicherungen/`,
   danach sofort auf Lesbarkeit geprüft. Ein Archiv, das sich nicht öffnen lässt, ist keine
   Sicherung, deshalb bricht das Skript an dieser Stelle ab statt weiterzumachen.
2. **Geheimnisse und Betriebszustand getrennt**: `config.json`, `auftraege.json` und `logs/`
   liegen zusätzlich einzeln daneben, mit Rechten 600. So lässt sich der Zustand
   zurückspielen, ohne das ganze Archiv auszupacken.
3. **Servercode auf einen eigenen Git-Zweig** `server-stand-JJJJ-MM-TT`, festgeschrieben und
   hochgeladen. `config.json` bleibt dabei draußen, dafür sorgt `.gitignore`. Gibt es auf dem
   Server keine Zugangsdaten für GitHub, bleibt der Zweig lokal, und das Skript sagt das.

Am Ende druckt es den Wiederherstellungsweg mit den echten Pfaden aus. Aufheben oder
abfotografieren.

Erst danach pullen.

## Schritt 2 — Nummer für Web & Shop entscheiden

Der Server hat bereits "10 Homepage". Die hier gebaute Abteilung "06 Web & Shop" ist
inhaltlich dasselbe, nur mit dem Regelwerk aus `WEBSITE-PROMPT-ultra.md` dahinter.
Drei Möglichkeiten:

1. **Zusammenlegen**, empfohlen: `abteilung_web.py` ersetzt die Rolle von 10 Homepage,
   behält aber dessen Nummer und Namen. Eine Abteilung für Web, ein Regelwerk.
2. **Umbenennen** auf eine freie Nummer, etwa 11 Web & Shop. Dann gibt es zwei Abteilungen
   für Web, die sich gegenseitig ins Gehege kommen.
3. **Verwerfen** und das Regelwerk stattdessen der bestehenden 10 Homepage als Kontext geben.

Bis das entschieden ist, bleibt `abteilung_web.py` hier liegen und wird nicht auf den
Server gebracht.

## Schritt 3 — Tagesbrief einrichten

**Zur Einordnung, damit hier nichts Falsches stehen bleibt:** In der Fassung des
Orchestrators, die in diesem Repo liegt, gibt es keine feste Morgenmail. Der Servercode ist
aber nicht in Git, also lässt sich von hier aus nicht ausschließen, dass dort bereits ein
Tagesbrief läuft. Im Postfach ist zwischen dem 9. und 11. September keine Mail zu sehen, die
nach einem täglichen Brief aussieht, und am 11. September gar keine. Sollte es auf dem Server
schon etwas Entsprechendes geben, wird `tagesbrief.py` nicht zusätzlich eingerichtet, sondern
mit dem Bestehenden verglichen und das bessere von beiden behalten.

```bash
cd /opt/bello
venv/bin/python tagesbrief.py                 # Textvorschau, sendet nichts
venv/bin/python tagesbrief.py --senden --erzwingen   # einmal testen
crontab -e
```

Eintrag, 07:00 lokale Zeit, täglich:

```
0 7 * * *  cd /opt/bello && venv/bin/python tagesbrief.py --senden >> logs/tagesbrief.log 2>&1
```

Prüfen, ob der bestehende Lauf überhaupt noch startet:

```bash
crontab -l                                    # laufen die Eintraege noch?
grep -i bello /var/log/syslog | tail -20      # hat Cron heute gestartet?
tail -40 /opt/bello/logs/*.log                # was sagt der letzte Lauf?
venv/bin/python orchestrator.py --stand       # gibt es ueberhaupt offene Auftraege?
```

Meldet `--stand` keine offenen Aufträge, dann war das Schweigen richtig: Es gab nichts zu
melden. Der Tagesbrief kommt ab sofort trotzdem, jeden Morgen, und nennt offene
Entscheidungen so lange, bis sie abgehakt sind.

## Schritt 4 — Register pflegen

`entscheidungen/offen.md` ist die Quelle für den Abschnitt "Wartet auf dich" im Tagesbrief.
Erledigt heißt `- [x]`, dann verschwindet der Punkt aus der Mail. Jede Abteilung darf dort
anhängen.
