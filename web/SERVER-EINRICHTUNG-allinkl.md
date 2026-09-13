# Webshop-Server einrichten — All-Inkl, Schritt für Schritt

Für Björn. Alles hier kannst du **jetzt** machen, ohne auf den fertigen Shop zu warten.
Während du das einrichtest, baut die Abteilung Web den WooCommerce-Auftritt fertig.

Entschieden am 12.09.2026: **WooCommerce auf eigenem Webspace bei All-Inkl, Tarif Premium.**
Nicht Shopify, nicht Medusa. Regelbesteuerung, keine Kleinunternehmerregelung.

**Eine Regel vorweg: Kennwörter kommen nie in einen Chat und nie ins Git.** Sie gehören in
deinen Passwortmanager und auf den Server. Wenn ich eines brauche, sage ich, *wohin* du es
einträgst — nicht, dass du es mir schickst.

---

## Reihenfolge auf einen Blick

| # | Schritt | Wo | Dauer | Blockiert was |
|---|---|---|---|---|
| 0 | Ins KAS einloggen | kas.all-inkl.com | 5 min | alles Weitere |
| 1 | Was liegt heute auf bellowerk.de? | Browser | 5 min | Domainumzug |
| ~~2~~ | ~~Tarif Premium buchen~~ | all-inkl.com | — | **erledigt 13.09.** |
| 3 | Domain anbinden oder umziehen | KAS | 10 min + Wartezeit | SSL, Mail |
| 4 | Baustellen-Adresse anlegen | KAS | 5 min | Aufbau ohne Publikum |
| 5 | PHP einstellen | KAS | 5 min | WordPress |
| 6 | Datenbank anlegen | KAS | 5 min | WordPress |
| 7 | SSL einschalten | KAS | 5 min + Wartezeit | Kasse, Zahlung |
| 8 | Zugang für den Aufbau anlegen (SSH/FTP) | KAS | 10 min | Hochladen |
| 9 | Postfach info@bellowerk.de | KAS | 10 min | Bestellmails |
| 10 | WordPress + WooCommerce installieren | KAS | 20 min | Shop |
| 11 | Sicherung einschalten | KAS | 5 min | ruhigen Schlaf |
| 12 | Konten außerhalb: PayPal, DHL | extern | 1–3 Tage | Verkauf |

KAS = das Kunden-Administrations-System von All-Inkl, `https://kas.all-inkl.com`.
Die Menünamen unten sind so, wie sie dort heißen; kleine Abweichungen bitte nicht wundern.

---

## 0. Reinkommen

All-Inkl hat **zwei** Anmeldungen. Die verwechselt man einmal, und dann sucht man eine halbe
Stunde nach dem FTP-Zugang an der falschen Stelle.

| Was du willst | Wo | Anmeldung |
|---|---|---|
| Rechnungen, Vertrag, Tarif | `all-inkl.com` → *Login* → **Mitgliedsbereich** | Kundennummer oder E-Mail + Kennwort aus der Bestellung |
| **Alles Technische**: Domains, FTP, Datenbank, SSL, Mail, WordPress | **`https://kas.all-inkl.com`** | KAS-Login (meist `w01xxxxx`) + KAS-Kennwort |

Für alles in dieser Anleitung brauchst du das **KAS**. Das ist die zweite Zeile.

**Die Zugangsdaten stehen in der Begrüßungsmail von All-Inkl**, die nach der Bestellung kam —
Betreff sinngemäß „Ihre Zugangsdaten" oder „Ihre Vertragsdaten". Darin stehen KAS-Login,
KAS-Kennwort und die Kontonummer. Nicht da? Erst im Spam nachsehen, dann auf
`kas.all-inkl.com` → *Passwort vergessen*.

Beim ersten Einloggen, in dieser Reihenfolge:

1. **Kennwort ändern** und das neue sofort in den Passwortmanager. Das Kennwort aus der Mail
   stand im Klartext in deinem Postfach — das ist keines, mit dem man arbeitet.
2. **Zwei-Faktor-Anmeldung einschalten**, falls angeboten. Über diesen Zugang laufen später
   Shop, Bestellungen und Kundendaten; wer hier reinkommt, kommt überall rein.
3. Einmal durchs Menü scrollen und die sechs Punkte suchen, um die es unten geht:
   **Domain**, **Subdomain**, **FTP**, **Datenbank**, **E-Mail**, **Tools**, **Software**.

### Die Adresse, unter der du sofort etwas sehen kannst

Zu jedem All-Inkl-Konto gehört von Haus aus eine technische Adresse, meist in der Form
`wXXXXXXX.kasserver.com` (die Kennung steht im KAS). Die funktioniert **ab der ersten Minute**,
ohne dass die Domain umgezogen ist.

Das ist unsere Baustelle: darauf entsteht der Shop, während bellowerk.de unberührt bleibt.
Schritt 4 kannst du dir damit sparen oder aufheben, bis die Domain da ist.

---

## Stand: der Shop läuft (13.09.2026)

Auf der Baustelle steht ein vollständiges WordPress mit WooCommerce. Aufgesetzt vom
netcup-Server aus, über SSH mit Schlüssel, ohne einen Klick im Browser.

| | |
|---|---|
| Baustelle | `bau.bellowerk.de`, eigenes Verzeichnis, Let's Encrypt |
| Drüben vorhanden | PHP 8.3.33, WP-CLI 2.12, MariaDB 10.11, `mysql`, `git`, `curl` |
| Eingerichtet | WordPress de_DE, WooCommerce, Euro, Preise inkl. Steuer, Regelbesteuerung |
| Ausgesperrt | Suchmaschinen (`blog_public=0`), bis bewusst umgelegt wird |
| Entfernt | Akismet, Hello Dolly |
| Vorläufig | Theme *Storefront* — es weicht dem eigenen, sobald es fertig ist |

Was als Nächstes kommt: das eigene Theme, die sieben Stücke als Produkte, Steuerzonen für
Drittländer (dort **keine** deutsche Umsatzsteuer), Versandzonen nach der DHL-Liste, und die
fünf Rechtsseiten als echte Seiten.

Noch nicht erledigt und weiterhin die eigentliche Bremse: **die elf Fotos** und die **echten
Prüfdaten**. Ohne sie geht kein Shop live, gleich wie fertig die Technik ist.

---

## Der kurze Weg — entschieden am 13.09.2026

Die lange Liste weiter unten bleibt als Nachschlagewerk stehen. Gemacht wird es aber so:

| Wer | Was |
|---|---|
| **Björn** | vier Dinge im KAS, einmalig, zusammen etwa eine Viertelstunde |
| **der netcup-Server** | alles Übrige, per KAS-API und SSH, wiederholbar |

### Die beiden Maschinen

| | netcup | All-Inkl |
|---|---|---|
| Was | eigener Server, root | Webspace, geteilt |
| Rolle | **Werkstatt** — Orchestrator, Abteilungen, Gedächtnis, der Agent | **Laden** — WordPress, WooCommerce, bellowerk.de |
| Adresse | steht auf dem Server selbst: `curl -4 ifconfig.me` | Servername und Stammverzeichnis stehen im KAS |

**Adressen und Kontokennungen stehen bewusst nicht in dieser Datei.** Das Repo ist öffentlich
(Stand 13.09.2026). Eine Server-IP ist kein Geheimnis, aber sie im Netz danebenzulegen, welcher
Betrieb darauf läuft und womit, erspart einem Angreifer die halbe Arbeit. Die feste IP wird
zweimal gebraucht — als IP-Sperre für die KAS-API und später im SPF-Eintrag — und wird an beiden
Stellen frisch vom Server geholt, statt hier zu stehen.

Der Agent wohnt weiter auf dem netcup-Server unter `/opt/bello`. Auf den Webspace wird er nicht
installiert — das geht dort nicht und ist auch nicht nötig. Er liefert dorthin.

### Deine vier Dinge

1. **KAS-API einschalten.** `kas.all-inkl.com` → *Tools* → *API*. Einschalten, und falls dort ein
   Feld für erlaubte IP-Adressen steht: die feste Adresse des netcup-Servers eintragen. Dann
   nützt der Zugang niemandem, der ihn irgendwo anders einsetzt.
2. **SSH-Zugang einschalten** und den Schlüssel hinterlegen, den der Server dir gleich ausgibt:
   *Tools* → *SSH-Zugang*.
3. **Die KAS-Zugangsdaten auf dem netcup-Server hinterlegen** — nicht hier im Chat:
   ```bash
   install -m 600 /dev/null /etc/bello/kas.env
   nano /etc/bello/kas.env
   # KAS_USER=w01xxxxx
   # KAS_PASSWORD=...
   ```
   Die Datei gehört root, ist per `.gitignore` ausgeschlossen und wird von keinem Skript
   ausgegeben.
4. **Sagen, dass es losgehen kann.** Den Rest fährt der Server.

### Was der Server danach selbst macht

```bash
cd /opt/bello && git pull

# einmalig: Schlüssel erzeugen, öffentlichen Teil ausgeben (der darf in den Chat)
bash web/betrieb/schluessel-fuer-allinkl.sh

venv/bin/pip install zeep
venv/bin/python web/betrieb/kas.py --stand          # Konto auslesen, nichts ändern
venv/bin/python web/betrieb/kas.py --einrichten     # zeigt nur, was es täte
venv/bin/python web/betrieb/kas.py --einrichten --wirklich
```

Damit entstehen Datenbank, Baustellen-Subdomain, der FTP-Zugang fürs Aufspielen und das Postfach.
Danach, über SSH: WordPress, WooCommerce, das eigene Theme, die sieben Stücke, Steuerzonen,
Versandzonen und die Rechtsseiten.

**`--stand` läuft zuerst und ändert nichts.** Ein erster Lauf gegen ein fremdes System ist ein
Lauf zum Zusehen. Und `--einrichten` ohne `--wirklich` sagt nur an, was es vorhätte.

### Was trotzdem bei dir bleibt

Die API kann viel, aber nicht alles, und manches soll sie auch nicht:

- **Tarif und Vertrag** — nur im Mitgliedsbereich
- **Domainumzug** mit AuthCode — das ist eine Willenserklärung, kein Skript
- **SSL freischalten** — ein Klick, siehe Schritt 7
- **Alles, was Geld kostet** — dabei bleibt es, wie überall in diesem Betrieb

---

## 1. Erst nachsehen: was liegt heute auf bellowerk.de?

Steht im offenen Register und ist wirklich der erste Schritt — **von hier aus komme ich nicht
auf die Domain.** Bevor irgendetwas hochgeladen wird:

- `https://bellowerk.de` und `https://www.bellowerk.de` im Browser öffnen. Kommt eine Seite?
  Eine Baustellenseite? Ein Fehler?
- Wo ist die Domain registriert? Bei All-Inkl schon, oder bei einem anderen Anbieter
  (Strato, IONOS, GoDaddy…)?
- Hängen dort **Mail-Postfächer** dran, die du benutzt? Die gehen beim unbedachten Umzug als
  Erstes kaputt — vor dem Umzug sichern.

Schick mir davon einfach einen Screenshot, dann weiß ich, womit wir es zu tun haben.

---

## 2. Tarif Premium — erledigt am 13.09.2026

Gebucht. Premium war aus diesen Gründen richtig:

- **SSH-Zugang** — damit kann der Shop sauber aufgespielt und aktualisiert werden, statt Dateien
  einzeln per FTP zu schieben.
- **Zehn Domains inklusive** — reicht für bellowerk.de plus die Weiterleitungen
  (herr-bello-und-frau-wuff, hundebetreuung-hamburg).
- PHP in aktueller Fassung, MariaDB-Datenbanken, kostenloses SSL, tägliche Sicherung.

Die Zugangsdaten kamen per Mail — siehe Schritt 0.

---

## 3. Domain anbinden oder umziehen

**Fall A — bellowerk.de liegt schon bei All-Inkl:** KAS → *Domain* → prüfen, dass sie auf das
Verzeichnis `/bellowerk.de` zeigt. Fertig.

**Fall B — bellowerk.de liegt woanders:** beim alten Anbieter den **AuthCode** (auch
„Auth-Info" oder „Transfer-Code") anfordern, dann bei All-Inkl den Umzug mit diesem Code
beauftragen. Dauert bei .de-Domains meist einen Tag.

> Kleine Falle: Wenn an der Domain noch Postfächer hängen, die du benutzt, den Umzug erst
> machen, **nachdem** die Postfächer bei All-Inkl angelegt sind (Schritt 9) — sonst fehlt für
> ein paar Stunden die Mail.

**Fall C — du willst ohne Risiko anfangen:** Domain erst mal liegen lassen und alles auf der
Baustellen-Adresse aus Schritt 4 bauen. Das ist der ruhigste Weg, und der, den ich empfehle.

---

## 4. Baustellen-Adresse anlegen

KAS → *Domain* → *Subdomain anlegen*: `bau.bellowerk.de` (oder was dir lieber ist).

Darauf entsteht der Shop, während bellowerk.de weiter das zeigt, was heute dort steht. Umgelegt
wird erst, wenn alles steht, geprüft ist und die Fotos drin sind. Zusätzlich bekommt die
Baustelle einen **Verzeichnisschutz** (KAS → *Tools* → *Verzeichnisschutz*), damit weder
Kundschaft noch Google eine halbfertige Seite sieht.

---

## 5. PHP einstellen

KAS → *Domain* → bei der Domain auf *bearbeiten*:

| Einstellung | Wert | Warum |
|---|---|---|
| PHP-Version | **8.3** (8.4, sobald WooCommerce sie offiziell freigibt) | WooCommerce läuft darauf sauber |
| PHP-Modus | PHP-FPM, falls wählbar | schneller |
| `memory_limit` | 256M | WooCommerce mit Bildern braucht das |
| `max_execution_time` | 120 | Importe und Updates laufen sonst in die Zeitsperre |
| `upload_max_filesize` | 64M | Produktfotos |
| `post_max_size` | 64M | dito |

---

## 6. Datenbank anlegen

KAS → *Datenbank* → *neue Datenbank anlegen*.

- Ein eigener Datenbankbenutzer **nur für den Shop**, kein geteilter.
- Kennwort vom KAS erzeugen lassen, lang, und sofort in den Passwortmanager.
- Notiere dir: Datenbankname, Benutzername, Hostname (bei All-Inkl meist `localhost`).

Diese drei Angaben (ohne das Kennwort) darfst du mir ruhig nennen — mit ihnen allein kommt
niemand irgendwo hinein.

---

## 7. SSL einschalten

KAS → *Domain* → *SSL-Schutz* → **Let's Encrypt**, kostenlos, für bellowerk.de *und*
www.bellowerk.de *und* die Baustellen-Subdomain.

Dazu die Weiterleitung von `http` auf `https` aktivieren. Ohne SSL keine Kasse: ein Shop ohne
Schloss in der Adresszeile verliert die Bestellung, noch bevor jemand den Preis liest, und
PayPal macht ohnehin nicht mit.

Die Ausstellung dauert ein paar Minuten bis eine Stunde.

---

## 8. Zugang für den Aufbau anlegen

**So ist es bei All-Inkl wirklich** (geprüft am 13.09.2026, Tools → SSH-Zugang):

- Ein Konto hat **genau einen** SSH-Zugang, hier `ssh-<kontokennung>`.
- Ein **öffentlicher Schlüssel lässt sich hinterlegen** — im neuen KAS beim Bearbeiten des
  Zugangs. Die Übersichtsseite zeigt das Feld nicht, deshalb erst übersehen.
- Das SSH-Kennwort ist **immer das Kennwort des Haupt-FTP-Benutzers**. Beides hängt zusammen;
  wer das eine ändert, ändert das andere. Mit hinterlegtem Schlüssel braucht man es nicht.
- Nach dem Anlegen steht der Zugang ein paar Minuten auf *in Bearbeitung*. Vorher läuft nichts.

Das heißt: der Zugang lässt sich **nicht** auf ein Verzeichnis begrenzen, er gilt fürs ganze
Konto. Dagegen helfen keine Einstellungen, sondern die Reihenfolge — erst nur auf der
Baustellen-Subdomain bauen, Sicherung vorher an, bellowerk.de zuletzt.

### Mit Schlüssel arbeiten

Entweder im KAS beim Zugang hinterlegen, oder vom netcup-Server aus ablegen — beides führt an
dieselbe Stelle, `~/.ssh/authorized_keys` auf dem Webspace. Der zweite Weg kostet einmal das
Kennwort:

```bash
# auf dem netcup-Server
ssh-copy-id -i ~/.ssh/allinkl_bellowerk.pub ssh-<kontokennung>@<kontokennung>.kasserver.com
```

Danach prüfen, dass es **ohne** Kennwort geht:

```bash
ssh -i ~/.ssh/allinkl_bellowerk ssh-<kontokennung>@<kontokennung>.kasserver.com "pwd && php -v"
```

Ab hier arbeitet der netcup-Server mit dem Schlüssel. Das Kennwort wird nicht mehr gebraucht,
steht nirgends auf der Platte und bleibt in deinem Passwortmanager als Rückweg.

Zum Aufräumen später: `~/.ssh/authorized_keys` auf dem Webspace enthält dann genau diese eine
Zeile. Zugang entziehen heißt: Zeile löschen.

## 9. Postfach info@bellowerk.de

KAS → *E-Mail* → *E-Mail-Postfach anlegen*: `info@bellowerk.de`. Steht so schon im Impressum,
in der Datenschutzerklärung und in der Widerrufsbelehrung — die Adresse muss es also geben,
bevor der Shop online geht.

Dazu im DNS (KAS → *Tools* → *DNS-Einstellungen*) **SPF, DKIM und DMARC** einrichten. All-Inkl
bietet das mit einem Klick an. Ohne diese drei Einträge landen deine Bestellbestätigungen bei
GMX, Web.de und Gmail im Spam — und der Kunde ruft an, statt zu warten.

Sinnvoll noch: `bestellung@`, `widerruf@` als Weiterleitung auf dasselbe Postfach.

---

## 10. WordPress und WooCommerce installieren

KAS → *Software* → *Softwareinstallation* → WordPress, auf die Baustellen-Domain.

Dabei:
- Benutzername **nicht** „admin".
- Langes Kennwort aus dem Passwortmanager.
- Als Sprache Deutsch (Sie/Du ist Geschmack — der Shop duzt, passend zur Marke).

Danach im WordPress-Menü *Plugins* → *WooCommerce* installieren und den Einrichtungsassistenten
durchklicken: Land Deutschland, Währung Euro, Preise **inklusive** Steuer (Regelbesteuerung,
19 %).

Mehr nicht. Kein Theme aussuchen, keine Seitenbaukästen installieren — das Aussehen kommt aus
dem eigenen Theme, das gerade gebaut wird. Jedes Plugin, das du jetzt „zum Probieren"
installierst, müssen wir später wieder auseinanderpflücken.

---

## 11. Sicherung einschalten

KAS → *Tools* → *Backup/Restore*. Prüfen, dass die tägliche Sicherung läuft und wie viele Tage
sie aufbewahrt wird. Einmal ausprobieren, wie eine Wiederherstellung aussieht — bevor du sie
brauchst.

---

## 12. Was außerhalb von All-Inkl läuft

Das dauert am längsten, deshalb **jetzt** anstoßen:

| Was | Wo | Warum jetzt |
|---|---|---|
| **PayPal-Geschäftskonto** | paypal.com | Prüfung dauert Tage. Zahlart Nummer eins im deutschen Handel |
| **DHL-Geschäftskundenvertrag** | dhl.de | Senkt alle vier Versandzonen. Steht als offener Punkt im Register |
| **USt-IdNr.** | Bundeszentralamt für Steuern, online | Fehlt noch im Impressum, und das OSS-Verfahren braucht sie |
| **OSS-Verfahren** | BZSt, mit dem Steuerberater | Folge des weltweiten Versands, ab 10.000 EUR netto EU-Umsatz |
| **Bankverbindung für Vorkasse** | deine Bank | Steht auf der Kasse |
| **Anwaltliche Prüfung der Rechtsseiten** | Anwalt für IT-Recht | Erst wenn Telefonnummer und USt-IdNr. drin sind |

---

## Und was ich in der Zwischenzeit brauche

Nicht vom Server, sondern von dir — das sind die Punkte, die den Shopstart wirklich aufhalten:

1. **Die elf Fotos** aus `web/aufnahmen/aufnahmeliste-und-bildprompts.md`. Ohne echte
   Produktfotos kein Shopstart; generierte Produktbilder sind hier ausgeschlossen.
2. **Echte Prüfdaten** für den Prüfbericht: welcher Hund, wie viele Tage, welche Belastung,
   welcher Befund. Auf der Seite stehen noch Platzhalter.
3. **Antwort auf Schritt 1**: was heute auf bellowerk.de liegt.

---

## Wenn du soweit bist

Sag Bescheid, sobald die Schritte 2 bis 7 stehen. Dann kommt von hier aus:

- das eigene WooCommerce-Theme aus dem fertigen Entwurf,
- die sieben Stücke als Produkte, mit Preis, Größen, Artikelnummer und strukturierten Daten,
- die Steuerzonen, damit die Ausfuhr in Drittländer ohne deutsche Umsatzsteuer läuft,
- die Versandzonen nach der DHL-Liste,
- Impressum, Datenschutz, AGB, Widerruf und Versand als echte Seiten,
- und ein Aufspiel-Befehl, der beim nächsten Mal eine Zeile ist statt eines Nachmittags.
