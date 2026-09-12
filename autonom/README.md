# Autonom — der Betrieb läuft auf dem Server, nicht auf deinem Rechner

Bis jetzt lief der Orchestrator, wenn ihn jemand aufrief. Damit hängt alles daran, dass ein
Rechner an ist. Diese Schicht dreht das um: der Server arbeitet rund um die Uhr weiter, und du
greifst von außen ein — per Mail, vom Handy, ohne SSH.

## Die vier Dienste

| Dienst | Takt | Was er tut |
|---|---|---|
| `bello-lauf` | alle 2 Stunden | Offene Aufträge abarbeiten, Ergebnisse prüfen, bei Bedarf eskalieren |
| `bello-tagesbrief` | täglich 07:00 | Die Morgenmail mit allem, was auf dich wartet |
| `bello-posteingang` | alle 5 Minuten | Dein Postfach lesen und deine Befehle ausführen |
| `bello-waechter` | stündlich | Prüfen, ob das alles wirklich läuft — und sich melden, wenn nicht |

Alle vier sind systemd-Zeitgeber, keine Cron-Einträge. Der Unterschied zählt: `Persistent=true`
holt einen Lauf nach, der wegen eines Neustarts ausgefallen ist. Ein Cron-Eintrag tut das nicht,
er lässt den Termin einfach aus.

## Wie du sie erreichst

Du schreibst eine Mail an die Orchestrator-Adresse. Innerhalb von fünf Minuten kommt die Antwort.

- **Betreff:** muss das Kennwort enthalten. Sonst irgendetwas.
- **Text, erste Zeile:** der Befehl. Alles darunter wird ignoriert, Zitate abgeschnitten.

| Befehl | Wirkung |
|---|---|
| `stand` | Woran gerade gearbeitet wird |
| `brief` | Den Tagesbrief sofort schicken, nicht erst morgen früh |
| `wochenbericht` | Die Wochenübersicht |
| `auftrag <Abteilung> \| <Ziel> [\| JJJJ-MM-TT]` | Neuen Auftrag anlegen |
| `hilfe` | Die Liste |

Beispiel für den Text einer Mail:

```
auftrag 06 Web & Shop | Produktseite für Hamburg No. 1 entwerfen | 2026-09-30
```

## Wie sie dich erreichen

Drei Wege, alle per Mail an die Adresse in `mail.empfaenger`:

1. **Eskalation** — ein Auftrag ist fertig, gescheitert oder technisch gestört. Kommt sofort.
2. **Tagesbrief** — jeden Morgen um 07:00, auch wenn nichts offen ist. Nennt jede offene
   Entscheidung aus `entscheidungen/offen.md` so lange, bis sie abgehakt ist.
3. **Wächter** — nur bei Befund: der Betrieb steht seit über sechs Stunden, ein Dienst ist
   ausgefallen, die Platte wird knapp. Höchstens eine Meldung je Befund und zwölf Stunden,
   sonst käme stündlich dieselbe Mail. Erholt sich etwas, kommt einmal Entwarnung.

Schweigen bleibt der Normalzustand. Wer ständig meldet, wird nicht mehr gelesen.

### Wenn das Postfach nicht erreichbar ist

Zwei Bremsen, weil eine nicht reicht. Die IMAP-Verbindung gibt nach 30 Sekunden auf
(`autonom.timeout_sekunden`). Hängt schon die Namensauflösung, greift dieses Zeitlimit nicht —
dann bricht systemd den Dienst nach `TimeoutStartSec` ab: 120 Sekunden für Posteingang und
Wächter, 300 für den Tagesbrief, 900 für den Lauf. Der nächste Takt versucht es erneut.
Ein Ausfall des Postfachs hält den Betrieb also nicht an, er verzögert ihn nur.

## Sicherheit — bitte einmal lesen

Der Posteingang ist ein Steuerkanal von außen. Zwei Dinge müssen gleichzeitig stimmen:

1. Die Absenderadresse ist genau die aus `mail.empfaenger`.
2. Im Betreff steht das Kennwort aus `autonom.kennwort`.

**Das Kennwort ist der eigentliche Schutz.** Das Feld `From` in einer Mail lässt sich fälschen,
die Absenderprüfung allein hält also niemanden auf. Wer das Kennwort hat, darf Aufträge anlegen
und Berichte abrufen — mehr nicht.

Es gibt bewusst **keinen** Befehl, der eine Shell öffnet, Dateien schreibt, etwas bestellt oder
Geld ausgibt. Das bleibt bei dir. Abgewiesene Mails landen in `logs/posteingang.log` und werden
nicht beantwortet, damit der Server nicht auf gefälschte Absender zurückschreibt.

Schick das Kennwort nicht per Mail. Es steht in `config.json`, Rechte 600.

## Einrichten

Auf dem Server, als root, **nach** `sicherung.sh`:

```bash
cd /opt/bello
bash sicherung.sh          # Pflicht, autonom.sh bricht ohne frisches Archiv ab
bash autonom/autonom.sh
```

Das Skript fragt genau einmal nach: ob es ein erzeugtes Kennwort in `config.json` eintragen darf.
Sonst schreibt es nur die systemd-Einheiten und wirft die Zeitgeber an.

Danach der Reihe nach prüfen:

```bash
venv/bin/python orchestrator_mail.py --test        # kommt eine Mail an?
venv/bin/python autonom/posteingang.py --probe     # liest, führt nichts aus
venv/bin/python autonom/waechter.py --probe        # prüft, sendet nichts
systemctl list-timers 'bello-*'                    # laufen die Zeitgeber?
```

Zum Schluss vom Handy eine Mail mit `stand` schicken und auf die Antwort warten.

## Was dieses Skript nicht anfasst

Dieselbe Liste wie in `uebernahme.sh`, aus demselben Grund:

| Datei | Warum |
|---|---|
| `orchestrator.py` | enthält das Abteilungsverzeichnis; der Server kennt 07 bis 10, dieser Zweig nicht |
| `abteilung_web.py` | wäre eine zweite Web-Abteilung neben der bestehenden 10 Homepage |
| `markenwissen.py` | kann auf dem Server geändert worden sein |
| `config.json` | Geheimnisse; wird gelesen, und nur nach Rückfrage um `autonom` ergänzt |

**Die Nummernkollision bleibt offen.** `06` ist hier Web & Shop und auf dem Server Einkauf. Der
Posteingang nimmt nur Abteilungen an, die `orchestrator.py` auf dem Server kennt — auf einem
Server ohne `06 Web & Shop` wird ein Auftrag dorthin abgewiesen, mit der Liste der bekannten
Abteilungen in der Antwort. Nichts geht kaputt, aber der Auftrag kommt auch nicht an. Siehe
`SERVER-ABGLEICH.md`, Schritt 2.

## Abbauen

```bash
bash autonom/autonom.sh --entfernen
```

Entfernt die Zeitgeber und die Einheiten. `config.json`, `auftraege.json` und `logs/` bleiben.

## Noch nicht gebaut

- **App statt Mail.** Mail läuft auf jedem Handy ohne Installation und war deshalb der erste
  Weg. Ein Telegram-Bot wäre der nächste: schneller, mit Knöpfen statt Tippen, und er kann
  Rückfragen stellen. Braucht einen Bot-Token und eine Entscheidung von dir.
- **Weboberfläche.** Auf dem Server liegt laut Übergabeprompt eine `dashboard.html`. Ob die
  weitergeführt oder ersetzt wird, ist offen.
- **Selbständiges Nachfassen.** Die Agenten arbeiten Aufträge ab, legen aber keine neuen an.
  Ein Agent, der von sich aus Arbeit vorschlägt, braucht vorher eine Grenze, die du setzt.
