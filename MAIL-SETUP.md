# Eigene Postfächer für die Einkaufsabteilungen verdrahten

Ziel: Einkauf China und Einkauf Europa schicken ihre Anfragen **selbst** aus dem eigenen Postfach
und lesen dort auch die Antworten — ohne dass jemand Texte per Hand kopiert.

| Abteilung | Postfach | Rolle |
|---|---|---|
| Einkauf China | `Ole.Petersen@bellowerk.de` | Ole Petersen |
| Einkauf Europa (DE/PL/EU) | `Merle.Ahrens@bellowerk.de` | Merle Ahrens |

## Schritt 1 — Postfächer beim Provider anlegen

Beim Anbieter der Domain `bellowerk.de` zwei **echte Postfächer** anlegen (keine Weiterleitung,
keine Alias-Adresse — ein Alias kann nicht selbst senden). Für jedes Postfach notieren:
Benutzername, Passwort, SMTP-Server und Port, IMAP-Server und Port.

Übliche Zugangsdaten — maßgeblich ist immer die Hilfeseite des eigenen Anbieters:

| Anbieter | SMTP | IMAP | Besonderheit |
|---|---|---|---|
| IONOS | `smtp.ionos.de:465` (SSL) | `imap.ionos.de:993` | Postfachpasswort reicht |
| Strato | `smtp.strato.de:465` | `imap.strato.de:993` | Postfachpasswort reicht |
| All-Inkl | `wXXXXXX.kasserver.com:465` | dito `:993` | Servername steht im KAS |
| Mailbox.org | `smtp.mailbox.org:465` | `imap.mailbox.org:993` | App-Passwort empfohlen |
| Google Workspace | `smtp.gmail.com:465` | `imap.gmail.com:993` | 2FA an, dann **App-Passwort** erzeugen |
| Microsoft 365 | `smtp.office365.com:587` (STARTTLS) | `outlook.office365.com:993` | einfaches Passwort oft gesperrt, dann geht nur OAuth |

## Schritt 2 — Zugangsdaten eintragen (nicht ins Repo)

`config.json` liegt nur auf dem Server und steht in `.gitignore`. Vorlage ist
`config.beispiel.json`, der neue Block heißt `postfaecher`:

```json
"postfaecher": {
  "einkauf_china": {
    "adresse": "Ole.Petersen@bellowerk.de",
    "anzeigename": "Ole Petersen - Bellowerk Manufaktur",
    "benutzer": "Ole.Petersen@bellowerk.de",
    "passwort": "...",
    "smtp_server": "smtp.DEIN-PROVIDER.de", "smtp_port": 465,
    "imap_server": "imap.DEIN-PROVIDER.de", "imap_port": 993
  },
  "einkauf_eu": { "...": "gleich, mit Merle.Ahrens@bellowerk.de" }
}
```

Wer das Passwort nicht in der Datei haben will, lässt `passwort` leer und setzt stattdessen eine
Umgebungsvariable — sie sticht die Datei:

```bash
export BELLOWERK_EINKAUF_CHINA_PASSWORT='...'
export BELLOWERK_EINKAUF_EU_PASSWORT='...'
```

Regeln: je Postfach ein eigenes Passwort, nie dasselbe wie für Björns Privatkonto, nie in einen
Commit, nie in eine Chatnachricht. Wenn eins doch einmal irgendwo auftaucht: beim Provider ändern,
das ist billiger als jede Diskussion.

## Schritt 3 — Testen

```bash
venv/bin/python postfach.py --test einkauf_china          # Testmail an sich selbst
venv/bin/python postfach.py --posteingang einkauf_china   # Antworten lesen (nur lesend)
```

Kommt die Testmail an, kann die Abteilung senden **und** empfangen.

## Schritt 4 — Anfragen verschicken

Jede fertige Anfrage liegt als eigene Datei in `sourcing/lieferanten/anfragen-2026-09/`.
Das Dateipräfix bestimmt das Postfach: `cn-` → Einkauf China, `pl-`/`de-` → Einkauf Europa.
Betreff, Text und Anhänge holt sich das Programm aus der Datei.

```bash
# erst ansehen, nichts verschicken
venv/bin/python postfach.py --senden sourcing/lieferanten/anfragen-2026-09/cn-07-adityna.md \
    --an inquiry@joydogcollars.com --trocken

# dann wirklich senden
venv/bin/python postfach.py --senden sourcing/lieferanten/anfragen-2026-09/cn-07-adityna.md \
    --an inquiry@joydogcollars.com
```

## Schritt 5 — Damit die Mails ankommen (wichtig für China)

Neue Domains landen gern im Spam. Beim Provider einmal einrichten:

- **SPF**: TXT-Eintrag `v=spf1 include:<Provider-SPF> -all` (der Anbieter nennt den Wert)
- **DKIM**: im Mailmenü aktivieren, der Anbieter setzt den Schlüssel
- **DMARC**: TXT auf `_dmarc.bellowerk.de`, Start mit `v=DMARC1; p=none; rua=mailto:...`

Dazu praktisch: die ersten Tage nur wenige Mails pro Stunde, keine Anhänge über 5 MB, und bei
Alibaba- oder Made-in-China-Kontakten zusätzlich über den Plattform-Chat anschreiben. Bei acht der
dreizehn Lieferanten gibt es ohnehin nur ein Kontaktformular oder Plattform-Chat — dort geht der
Text aus der Datei per Copy-and-paste rein, der Kopf jeder Datei sagt welcher Kanal gilt.

## Was das Programm nicht tut

- Es beantwortet nichts von allein. Antworten liest der Einkauf, bewertet sie und legt sie Björn vor.
- Es gibt kein Geld aus: Musterkosten über 40 EUR und jede Bestellung gehen vorher an Björn.
- Der Gmail-Zugang aus der Claude-Sitzung hängt an Björns Privatkonto und hat kein Absenderfeld —
  aus den bellowerk.de-Postfächern kann darüber **nicht** verschickt werden. Deshalb dieser Weg.
