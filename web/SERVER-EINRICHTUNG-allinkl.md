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
| 1 | Was liegt heute auf bellowerk.de? | Browser | 5 min | alles Weitere |
| 2 | Tarif Premium buchen | all-inkl.com | 10 min | den ganzen Rest |
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

## 2. Tarif Premium buchen

Bei All-Inkl unter `all-inkl.com` bestellen. Premium deshalb:

- **SSH-Zugang** — damit kann der Shop sauber aufgespielt und aktualisiert werden, statt Dateien
  einzeln per FTP zu schieben.
- **Zehn Domains inklusive** — reicht für bellowerk.de plus die Weiterleitungen
  (herr-bello-und-frau-wuff, hundebetreuung-hamburg).
- PHP in aktueller Fassung, MariaDB-Datenbanken, kostenloses SSL, tägliche Sicherung.

Nach der Bestellung kommt eine Mail mit den KAS-Zugangsdaten. **Die gehören in den
Passwortmanager**, nicht in eine Notiz-App und nicht in einen Chat.

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

Zwei Wege, beide im KAS:

**SSH (besser, im Premium enthalten):** KAS → *Tools* → *SSH-Zugang*. Benutzer anlegen, Kennwort
erzeugen lassen. Damit kann der Shop in einem Rutsch aufgespielt und aktualisiert werden.

**FTP (der einfache Weg):** KAS → *FTP* → *FTP-Benutzer anlegen*.
- Einen **eigenen** Benutzer für den Shop, nicht den Hauptzugang benutzen.
- Zugriff **nur** auf das Verzeichnis der Shop-Domain begrenzen.
- Verbindung immer als **FTPS oder SFTP**, nie als einfaches FTP — einfaches FTP schickt das
  Kennwort unverschlüsselt durchs Netz.

Notiere Hostname, Benutzername, Port. Das Kennwort bleibt im Passwortmanager.

---

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
