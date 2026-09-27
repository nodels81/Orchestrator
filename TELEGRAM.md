# Gustav per Telegram

Mit Telegram erreichst du den Betrieb vom Handy aus, ohne SSH und ohne Mail-Umweg:

- **Aufträge geben:** einfach hinschreiben, Gustav fragt, wer es übernimmt. Oder gleich mit Namen: `@Henrik RFQ für HB-01 an Kingming`.
- **Ergebnisse bekommen:** Sie kommen aufs Handy, mit Knöpfen für **Freigeben · Überarbeiten · Verwerfen**.
- **Nicht warten:** `/jetzt` arbeitet Offenes sofort ab, statt bis zur vollen Stunde zu warten.

Die Mail bleibt, wie sie ist. Telegram ist ein zusätzlicher Weg zu Gustav, kein Ersatz, und es
gibt keinen Weg an Gustav vorbei: Ein Auftrag aus Telegram bekommt dieselbe Nummer, dieselbe
Prüfung durch Almut und dieselbe Mail wie einer von der Konsole, aus der App oder per Mail.

So sieht das aus:

```
Du:      @Henrik RFQ für HB-01 an Kingming, 100 Stück
Gustav:  ✅ A-2026-031 an Henrik (07 Einkauf China) · Frist 04.10.
         Läuft beim nächsten Lauf (heute 15:00 Uhr).        [ ▶️ Jetzt starten ]

Gustav:  📋 Ergebnis liegt vor
         A-2026-031 · Henrik (07 Einkauf China)
         Ziel: RFQ für HB-01 an Kingming, 100 Stück
         ERGEBNIS: Dear Sir or Madam, …
         [ ✅ Freigeben ] [ ✏️ Überarbeiten ]  [ 🗑 Verwerfen ]
```

---

## Einrichtung: einmalig, etwa 10 Minuten

Du brauchst Telegram auf dem Handy und wie immer SSH zum Server. Für Schritt 1 hilft Telegram
auch am PC, dann kopierst du den Token hinüber, statt 46 Zeichen abzutippen. Am
einfachsten geht das über **web.telegram.org**, die Anmeldung läuft per QR-Code vom Handy
(Einstellungen → Geräte → Desktop-Gerät verbinden).

### Schritt 1: Bot beim BotFather anlegen (in Telegram, 3 Minuten)

Der BotFather ist Telegrams offizieller Bot für neue Bots. Er antwortet auf Englisch.

1. In Telegram nach **@BotFather** suchen (mit blauem Haken) und **Start** tippen.
2. `/newbot` senden.
3. *„How are we going to call it?"*: Name eingeben, z. B. `Gustav · Bellowerk`. So heißt der Chat bei dir.
4. *„Choose a username"*: muss auf `bot` enden und weltweit frei sein, z. B. `bellowerk_gustav_bot`.
   Ist er vergeben, etwas anhängen: `bellowerk_gustav_hh_bot`.
5. *„Done! … Use this token to access the HTTP API:"*, darunter steht eine lange Zeile wie
   `7123456789:AAH4k…`. Das ist der **Token**, du brauchst ihn in Schritt 3.
   **Der Token ist ein Schlüssel.** Nicht mailen, nicht in Chats kopieren, keine Screenshots.
6. Empfohlen: `/setjoingroups` → deinen Bot wählen → **Disable**. Dann kann niemand den Bot in eine Gruppe holen.
7. Optional: `/setuserpic` → Bot wählen → Bellowerk-Logo schicken.

### Schritt 2: neuen Stand auf den Server holen

```
ssh root@v2202609413684515441.powersrv.de
cd /opt/bello
sudo git pull
```

### Schritt 3: Einrichtungsskript starten (5 Minuten)

```
sudo bash bin/telegram-einrichten.sh
```

Das Skript arbeitet sechs Schritte ab und fragt dich genau zweimal:

1. **Token einfügen**, der aus Schritt 1. In PowerShell fügt ein Rechtsklick ein. Die Eingabe
   bleibt unsichtbar, das ist Absicht. Das Skript prüft den Token sofort bei Telegram und
   meldet den Namen deines Bots.
2. **„Ist das dein Konto? [j/N]"**. Davor sagt es dir: *„Öffne jetzt Telegram, such nach
   @bellowerk_gustav_bot und tippe auf START."* Tu das am Handy. Dein Bot antwortet
   *„👋 Hallo! Ich habe dich erkannt."*, am Server erscheint dein Name. Mit `j` bestätigen.

Den Rest erledigt das Skript allein:

- Es trägt Token und Kontonummer in `/etc/bello/env` ein (nur root lesbar). In `config.json` steht nur ein Verweis darauf.
- Es richtet den Dienst `bello-telegram` und den Sofortstart ein.
- Zur Probe schickt es dir eine *„Testnachricht von Gustav"* aufs Handy.
- Vor jeder Änderung legt es eine Sicherung an. Es lässt sich beliebig oft starten und ändert dann nur, was fehlt.

> Das Skript **direkt im Terminal** starten, nicht über Claude Code. Der Token gehört in
> keinen Chat, auch nicht in den mit Claude.

### Schritt 4: ausprobieren

1. `/hilfe` an deinen Bot: Er zeigt alles, was er kann.
2. `/stand`: Was wartet auf dich, was ist offen?
3. Ein kleiner Probeauftrag:
   `@Merle Drei Ideen für Zubehör aus Fettleder unter 60 €, nur Stichworte`,
   dann **▶️ Jetzt starten**. Nach ein paar Minuten kommt das Ergebnis mit Knöpfen, dazu wie
   gewohnt die Mail.

---

## Im Alltag

### Einen Auftrag geben

| Du schreibst | Was passiert |
|---|---|
| `@Henrik RFQ für HB-01 an Kingming, 100 Stück` | Auftrag direkt an Henrik (07) |
| `@07 …`, `@Einkauf China …` | Nummer oder Fach gehen auch |
| `Drei Formentwürfe Halsband, nur Form` | Gustav fragt *„Wer soll das übernehmen?"*, du tippst den Namen an |
| `@Einkauf Buchschrauben anfragen` | Das ist mehrdeutig (Insa und Henrik). Gustav bietet nur die zwei an. |

Mehrzeilig geht auch: erste Zeile `@Name …`, darunter die Einzelheiten. Höchstens 2000
Zeichen. Die Frist ist wie überall sieben Tage.

**Diktieren:** Sprachnachrichten kann Gustav nicht hören. Nimm das **Mikrofon auf der
Tastatur**, dann kommt Text an.

### Wann gearbeitet wird

Wie bisher beim stündlichen Lauf von 07 bis 19 Uhr. Wer nicht warten will, tippt
**▶️ Jetzt starten** unter der Bestätigung oder schreibt `/jetzt`. Dann läuft Gustav sofort
los und meldet sich mit *„🏁 Lauf fertig"*, wenn alles durch ist. Arbeitet er gerade schon,
kommen deine Aufträge direkt danach dran.

Tipp: Mehrere Aufträge? Erst alle schicken, dann einmal `/jetzt`. So teilen sie sich einen
Lauf und den Zwischenspeicher, das spart Geld.

### Ergebnisse und Entscheidungen

Jedes Ergebnis kommt als Nachricht mit Knöpfen:

- **✅ Freigeben**: Das Ergebnis ist angenommen.
- **✏️ Überarbeiten**: Gustav fragt *„Was soll … ändern?"*. Deine Antwort geht als neuer Auftrag an dieselbe Abteilung.
- **🗑 Verwerfen**: Der Auftrag ist endgültig raus. Gustav fragt zur Sicherheit einmal nach.

Nach einem technischen Fehler oder einer abgelaufenen Frist gibt es nichts freizugeben. Dann
stehen nur *Überarbeiten* (heißt: noch einmal, gern mit Hinweis) und *Verwerfen* zur Wahl.

Lange Ergebnisse kommen gekürzt, das Ganze hängt als Datei darunter. Zeichnungen kommen als
Bild.

**Auf ein Ergebnis antworten** (Nachricht gedrückt halten → *Antworten*): Gustav bietet an,
deine Antwort als Überarbeitung zu nehmen, oder du gibst sie per Knopf jemand anderem. Beginnt
die Antwort mit `@Thea …`, geht ein neuer Auftrag an Thea, mit Verweis auf das Ergebnis.

Es ist gleich, wo du entscheidest, ob in Telegram, per Mail oder in der App: Es gilt die erste
Entscheidung. Ein alter Knopf entscheidet nichts ein zweites Mal.

### Befehle

Die wichtigsten stehen auch im Menü neben dem Eingabefeld.

| Befehl | Wirkung |
|---|---|
| `/stand` | was auf dich wartet, was offen ist, wann der nächste Lauf kommt |
| `/jetzt` | Offenes sofort abarbeiten |
| `/ergebnis A-2026-031` | ein Ergebnis ganz lesen (ohne Nummer: Auswahl zum Antippen) |
| `/wissen Kingming` | im Gedächtnis nachschlagen: Fakten und frühere Aufträge |
| `/team` | wer macht was |
| `/freigeben A-2026-031 passt so` | freigeben, mit Kommentar |
| `/ueberarbeiten A-2026-031 bitte mit Messingschnalle` | Überarbeitung ohne Rückfrage |
| `/verwerfen A-2026-031 brauchen wir nicht` | verwerfen ohne Rückfrage |
| `/abbrechen` | offene Rückfragen vergessen |
| `/hilfe` | diese Übersicht |

---

## Wie es funktioniert

```
Handy ──> Telegram <── fragt ab ── bello-telegram (Bot auf dem Server)
                                        │  legt Aufträge an, trägt Entscheidungen ein —
                                        │  mit denselben Funktionen wie orchestrator.py
                                        └─ /jetzt: schreibt daten/lauf-anstossen
                                               └─> systemd startet den gewöhnlichen Lauf

Lauf (bello-orchestrator) ── Ergebnis ──> Mail wie bisher  +  Telegram mit Knöpfen
```

- Der Bot fragt Telegram ab. Er öffnet keinen Port, am Server wird nichts nach außen freigegeben.
- Der Bot ruft nie die Claude-API. Kosten entstehen nur im Lauf, wie bisher.
- Die Ergebnisse schickt der Lauf selbst. Sie kommen also auch dann aufs Handy, wenn der Bot
  einmal steht. Fällt Telegram aus, bleibt es bei der Mail, und der Lauf geht weiter.
- Kommt ein Auftrag herein, während ein Lauf arbeitet, geht er nicht verloren. Der Lauf schreibt
  seine Ergebnisse zurück, ohne zu überschreiben, was inzwischen dazukam.

| Was | Wo |
|---|---|
| Bot-Dienst | `bin/telegram_bot.py`, systemd `bello-telegram.service` |
| Versand der Ergebnisse | `orchestrator_telegram.py`, aufgerufen aus dem Lauf |
| Sofortstart | `bello-orchestrator-anstoss.path` achtet auf `daten/lauf-anstossen` |
| Token, Kontonummer | `/etc/bello/env` (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) |
| Verweis darauf | `config.json`, Block `"telegram"` |
| Offene Rückfragen des Bots | `daten/telegram.json` |

---

## Sicherheit

- **Nur dein Konto zählt.** Nachrichten von anderen ignoriert der Bot und vermerkt sie nur im Journal. Er antwortet ihnen nicht einmal.
- **Er kann nur, was oben steht.** Er hat keinen Zugriff auf die Shell, nimmt keine Dateien vom Handy an und gibt kein Geld aus. Wie überall gilt: Keine Abteilung gibt Geld aus, und nach außen gehen nur Entwürfe.
- **Geheimnisse bleiben auf dem Server.** Token und Kontonummer stehen in `/etc/bello/env`, nur für root lesbar. `config.json` enthält nur Verweise, das Repo gar nichts. Ins Journal schreibt der Bot nur Nummern und Abteilungen, keine Auftragstexte und nie den Token.
- **Handy weg oder Token aus Versehen geteilt?** Sofort beim @BotFather `/revoke` senden und den Bot wählen. Damit ist der alte Token wertlos. Danach am Server `sudo bash bin/telegram-einrichten.sh --neu` ausführen und den neuen Token einfügen.
- **Zur Einordnung:** Chats mit Bots sind bei Telegram nicht Ende-zu-Ende-verschlüsselt. Telegram kann sie lesen, so wie Google die Mails. Für Aufträge und Entwürfe passt das. Passwörter und Zugangsdaten gehören trotzdem nie in den Chat.

---

## Wenn etwas nicht geht

Immer zuerst:

```
sudo bash /opt/bello/bin/telegram-einrichten.sh --pruefen
```

Das zeigt Punkt für Punkt, was läuft und was nicht, dazu die letzten Meldungen des Bots.

| Anzeichen | Ursache und Abhilfe |
|---|---|
| Bot antwortet gar nicht | `--pruefen`. Läuft `bello-telegram` nicht: `journalctl -u bello-telegram -n 30` |
| Im Journal: *„Nachricht von fremdem Konto … ignoriert"* | Du schreibst von einem anderen Konto als dem eingerichteten. Abhilfe: `--neu` |
| Im Journal: *„Token ungueltig"* | Der Token wurde zurückgezogen. Abhilfe: `sudo bash bin/telegram-einrichten.sh --neu` |
| Im Journal: *„Telegram nicht erreichbar"* | Der Server kommt nicht zu Telegram: `curl -sI https://api.telegram.org`, dann die netcup-Firewall prüfen |
| *„Der Sofortstart ist auf dem Server nicht eingerichtet"* | Das Einrichtungsskript noch einmal laufen lassen |
| Ergebnisse kommen per Mail, aber nicht aufs Handy | `--pruefen`, Zeile *„der Lauf liest /etc/bello/env"*. Was der Lauf gemeldet hat: `grep TELEGRAM /opt/bello/logs/orchestrator-$(date +%F).log` |
| *„Der angestoßene Lauf hat sich nicht zurückgemeldet"* | `journalctl -u bello-orchestrator -n 50`. Meist kam schon die Mail *„Tageslauf FEHLGESCHLAGEN"*. |

---

## Anhalten und ausbauen

Den Bot pausieren: Er nimmt dann nichts mehr an. Ergebnisse kommen weiter aufs Handy, solange
`config.json` den Block `"telegram"` hat.

```
sudo systemctl disable --now bello-telegram.service
sudo systemctl enable --now bello-telegram.service      # wieder an
```

Ganz ausbauen:

```
sudo bash bin/telegram-einrichten.sh --entfernen
```

Das entfernt den Dienst, den Sofortstart, den Block in `config.json` und die Zeilen in
`/etc/bello/env`, jeweils mit Sicherung vorher. Den Bot selbst löschst du beim @BotFather mit
`/deletebot`.

---

## Was bewusst noch fehlt

- **Sprachnachrichten.** Dafür bräuchte es einen Dienst, der sie abschreibt. Die Diktierfunktion der Tastatur kostet nichts und bleibt auf dem Handy.
- **Bilder und Dateien vom Handy**, etwa Musterfotos für Almuts Prüfung. Das wäre ein sinnvoller nächster Schritt.
- **Freies Gespräch mit einer Abteilung** (*„Henrik, was hältst du von …?"*). Das wäre ein API-Aufruf je Nachricht, ohne Register und ohne Prüfung. Gespräch und Auftrag bleiben deshalb bewusst getrennt; das Gespräch lässt sich später ergänzen.
