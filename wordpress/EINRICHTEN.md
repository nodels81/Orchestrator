# Shop einrichten — Schritt für Schritt

Für `bellowerk.de` auf ALL-INKL.COM, Tarif Premium. Die Domain ist leer, es wird
nichts überschrieben.

Reihenfolge einhalten. Wer WooCommerce vor der SSL-Umstellung installiert, trägt
sich `http://` als Shopadresse ein und darf es hinterher in der Datenbank suchen.

---

## 1 · Im KAS vorbereiten

Kundenmenü von All-Inkl, bevor WordPress angefasst wird.

| Schritt | Wo | Wert |
|---|---|---|
| PHP-Version setzen | Domain → bellowerk.de → Bearbeiten | **8.3** |
| SSL einschalten | Domain → bellowerk.de → SSL-Schutz | Let's Encrypt |
| Weiterleitung auf https | Domain → bellowerk.de | erzwingen |
| Datenbank anlegen | Datenbanken → Neue Datenbank | Name und Passwort notieren |
| Postfach anlegen | E-Mail → Neues Postfach | `info@bellowerk.de` |
| SSH-Zugang aktivieren | Zugangsdaten → SSH | Schlüssel hinterlegen, kein Passwort |

**SSL vor WordPress.** Sonst steht die Seite später unter `http://` in der Datenbank.

---

## 2 · WordPress installieren

Im KAS unter **Software-Installation → WordPress**, Ziel `bellowerk.de`.

Danach in WordPress:

- **Einstellungen → Allgemein**: Titel `Bellowerk Manufaktur`, Untertitel
  `Halsbänder und Leinen aus Fettleder und massivem Messing`. Beide Adressen auf `https://`.
- **Einstellungen → Permalinks**: **Beitragsname**. Ohne das sehen alle Pfade aus wie `?p=123`.
- **Einstellungen → Diskussion**: Kommentare aus. Ein Shop braucht keine.
- **Benutzer**: den Standardbenutzer `admin` löschen oder umbenennen, falls der Installer einen anlegt.

---

## 3 · WooCommerce installieren

**Plugins → Installieren → WooCommerce**. Beim Einrichtungsassistenten:

| Frage | Antwort |
|---|---|
| Standort | Deutschland, Quellenweg 3, 21698 Harsefeld |
| Branche | Mode und Accessoires |
| Produktarten | Physische Produkte |
| Verkaufst du woanders? | Nein |
| Zusatzangebote (Jetpack, Stripe, Mailchimp …) | **alle abwählen** |

Die Zusatzangebote sind der Grund, warum WooCommerce-Installationen langsam
werden. Was gebraucht wird, wird einzeln installiert.

**Danach ebenfalls installieren:**

- **German Market** oder **Germanized** — macht WooCommerce für den deutschen
  Onlinehandel rechtssicher: Grundpreise, Widerrufsbelehrung in der Bestellmail,
  Bestellübersicht vor dem Knopf, korrekte Steuerausweisung. Beide sind in der
  kostenlosen Fassung ausreichend für den Anfang. **Kostet in der Vollfassung Geld —
  Entscheidung Björn, siehe `entscheidungen/offen.md`.**
- **WooCommerce PayPal Payments** — die offizielle PayPal-Anbindung.

---

## 4 · Steuern — die Stelle, an der es teuer wird

**Einstellungen → Steuern.**

| Einstellung | Wert | Warum |
|---|---|---|
| Steuern aktivieren | ja | Regelbesteuerung, keine Kleinunternehmerregelung |
| Preise inklusive Steuer eingeben | **ja** | Die Preise im Katalog sind Endpreise: 89, 99, 129 € |
| Steuer berechnen auf Basis | Lieferadresse des Kunden | |
| Preise im Shop anzeigen | inklusive Steuer | Pflicht nach Preisangabenverordnung |

Dann **Standardsätze** anlegen:

| Land | Satz | Name |
|---|---|---|
| DE | 19,0000 | USt |
| (EU-Länder einzeln) | jeweiliger Satz des Landes | USt |

**Und der Teil, den man vergisst:** Für Länder **außerhalb der EU** — Schweiz,
Norwegen, Vereinigtes Königreich, USA, Kanada, Australien — wird ein Satz von
**0,0000** angelegt. Ausfuhrlieferungen in Drittländer sind umsatzsteuerfrei
(§ 4 Nr. 1a i. V. m. § 6 UStG). Ohne diesen Eintrag zahlt ein Kunde in Boston
deutsche Umsatzsteuer **und** Einfuhrsteuer im Zielland, also doppelt.

**Lieferschwelle EU: 10.000 € netto im Kalenderjahr**, zusammengerechnet über alle
EU-Länder. Darunter reicht der deutsche Satz für alle EU-Länder. Darüber wird der
Satz des Ziellandes fällig, ab dem Paket, das die Schwelle reißt. Dann OSS beim
Bundeszentralamt für Steuern anmelden. **Mit dem Steuerberater klären, nicht raten.**

---

## 5 · Versand

**Einstellungen → Versand.** Vier Zonen, wie auf der Versandseite:

| Zone | Länder | Pauschale | Versandfrei ab |
|---|---|---|---|
| Deutschland | DE | 4,90 € | 120 € |
| EU | alle EU außer DE | 10,90 € | 180 € |
| Europa außerhalb EU | CH, NO, GB | 16,90 € | — |
| Welt | übrige | 18,90 € | — |

**Die 4,90 € für Deutschland sind zu niedrig.** DHL nimmt online 6,19 € für ein
Paket bis 2 kg, 5,19 € für ein Päckchen M. Steht als Entscheidung im Register.

Die Auslandssätze sind Richtwerte nach DHL-Liste. Mit Geschäftskundenvertrag
liegen sie darunter — dann hier anpassen.

---

## 6 · Zahlung

**Einstellungen → Zahlungen.**

- **PayPal** über *WooCommerce PayPal Payments*. Im PayPal-Geschäftskonto die
  API-Zugangsdaten erzeugen und eintragen. Erst im Sandkasten testen.
- **Überweisung** (WooCommerce nennt es *Direktüberweisung*). Bankverbindung
  eintragen. Beschreibung: „Du bekommst die Bankverbindung mit der
  Bestellbestätigung. Wir fertigen, sobald das Geld da ist."
- **Alles andere abschalten.** Kein Nachnahme, kein Scheck.

**Kauf auf Rechnung ist nicht eingerichtet** — noch nicht entschieden.

---

## 7 · Theme hochladen und aktivieren

Auf dem eigenen Rechner oder auf dem VPS:

```bash
cp wordpress/zugang.beispiel.conf wordpress/zugang.conf
chmod 600 wordpress/zugang.conf
# ausfüllen: SFTP_HOST, SFTP_USER, ZIELPFAD

bash wordpress/hochladen.sh          # Trockenlauf, schreibt nichts
bash wordpress/hochladen.sh --echt   # überträgt nach Rückfrage
```

Das Skript prüft jede PHP-Datei mit `php -l`, bevor es etwas überträgt. Kaputtes
PHP kommt nicht auf den Server.

Dann in WordPress: **Design → Themes → Bellowerk → Aktivieren.**

Beim Aktivieren legt das Theme die fünf Rechtsseiten an. Seiten, die es schon
gibt, werden **nicht** überschrieben. Die Meldung im Adminbereich sagt, was
passiert ist.

Danach **Einstellungen → Permalinks einmal speichern** — sonst greifen die Pfade
der neuen Seiten nicht.

---

## 8 · Menüs

**Design → Menüs**, drei Stück:

| Menü | Position | Einträge |
|---|---|---|
| Kopfleiste | `kopf` | Kollektion, Material, Praxistest, Größe finden |
| Fußzeile: Kaufen | `fuss` | Kollektion, Größe finden, Warenkorb, Versand |
| Fußzeile: Werkstatt | `recht` | Praxistest, Material und Pflege, Reparatur |

Die Rechtslinks in der Fußzeile stehen **fest im Theme** und brauchen kein Menü.
Absicht: Ein Menü kann jemand leeren, und dann fehlt das Impressum.

---

## 9 · Produkte einlesen

Nicht von Hand anlegen — die vier Stücke stehen fertig in `wordpress/produkte.csv`.

**Produkte → Alle Produkte → Importieren**, Datei auswählen, durchklicken. Der
Importer erkennt die Spalten selbst. Danach stehen Hamburg No. 1 bis No. 4 im
Katalog, mit Preis, Kurzbeschreibung, Maßtabelle, Materialliste, Pflegehinweis
und der Ausschlussliste.

Die Datei wird erzeugt, nicht gepflegt:

```bash
python3 wordpress/produkte.py            # schreibt produkte.csv neu
python3 wordpress/produkte.py --zeigen   # nur ansehen
```

Preise und Texte für No. 2, 3 und 4 kommen aus `web/vorlagen/seiten_bauen.py` —
derselben Quelle wie die Entwurfsseiten, damit nichts auseinanderläuft. Nur HB-01
steht zusätzlich in `wordpress/produkte.py`, weil seine Seite von Hand gepflegt wird.

### Was der Import bewusst nicht macht

- **Keine Varianten.** Größe und Leder stehen als sichtbare Eigenschaften am
  Produkt, aber jedes Stück ist zunächst ein einfaches Produkt mit einem Preis.
  So steht sofort ein vollständiger Katalog. Für den echten Verkauf: Produkt
  öffnen → Produktdaten auf **Variables Produkt** stellen → Varianten →
  *Alle Varianten erzeugen*. Dann je Variante Bestand und gegebenenfalls
  abweichenden Preis setzen.
- **Keine Bilder.** Es gibt noch keine. Die Bildflächen im Theme tragen bis dahin
  ihre Aufnahmeanweisung.
- **Keine Herkunftsangabe im Produkttext.** Die hängt im Theme am Haken und wird
  auf jeder Produktseite unter den Preis gesetzt. Stünde sie zusätzlich im Text,
  gäbe es sie zweimal — und beim nächsten Textwechsel einmal veraltet.
- **Hamburg No. 5, 6 und 7 fehlen.** Die Stücke sind nicht gebaut. Sie im Shop
  zu zeigen, wäre Ware, die es nicht gibt.

## 10 · Vor dem Freischalten

Nicht online gehen, solange einer dieser Punkte offen ist:

- [ ] USt-IdNr. im Impressum eingetragen
- [ ] Alle orange unterstrichenen Stellen in den Rechtsseiten gefüllt
- [ ] Rechtsseiten anwaltlich geprüft
- [ ] Steuersatz 0 % für Drittländer angelegt und mit einer Testbestellung geprüft
- [ ] Eine vollständige Testbestellung über PayPal-Sandkasten durchgelaufen
- [ ] Bestellbestätigung kommt an, mit Widerrufsbelehrung
- [ ] Bestellknopf heißt „Zahlungspflichtig bestellen"
- [ ] Zustimmungsbanner mit gleichrangigem „Alle ablehnen"
- [ ] Echte Fotos statt der Bildflächen
- [ ] Echte Prüfdaten oder Praxistest-Sektion entfernt
- [ ] Sicherung eingerichtet — All-Inkl sichert täglich, aber einmal geprüft, ob
      sich eine Sicherung auch zurückspielen lässt

Das vollständige Abnahmetor mit 20 Punkten steht in `web/ABNAHME.md`.
