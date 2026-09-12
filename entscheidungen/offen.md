# Offene Entscheidungen

Dieses Register geht jeden Morgen um 07:00 als Tagesbrief raus, so lange, bis ein Punkt
abgehakt ist. Genau dafür gibt es die Datei: Entscheidungen gehen sonst in Auftragsmails
unter und tauchen nie wieder auf.

**Pflege von Hand.** Erledigt heißt `- [x]`, dann verschwindet der Punkt aus der Mail.
Neue Punkte legt jede Abteilung selbst an, unter der passenden Überschrift.

## Betrieb

- [ ] Der Server /opt/bello ist weiter als dieses Repo: dort laufen 06 Einkauf, 07 Einkauf China, 08 Design, 09 Qualität und 10 Homepage, die hier fehlen. Servercode nach Git bringen, bevor dort das nächste Mal gepullt wird. Siehe SERVER-ABGLEICH.md
- [ ] Abteilungsnummer für Web & Shop festlegen: hier steht sie als 06, auf dem Server ist 06 bereits Einkauf und 10 bereits Homepage

- [ ] Läuft auf dem Server bereits ein Tagesbrief? Wenn ja, mit tagesbrief.py vergleichen und nur eines von beidem behalten. Screenshots der bisherigen Morgenmails helfen
- [ ] Vor dem nächsten Pull auf /opt/bello: `bash sicherung.sh` ausführen

- [ ] Autonom-Betrieb auf dem Server anwerfen, in dieser Reihenfolge: `bash sicherung.sh`, dann `bash uebernahme.sh`, dann `bash autonom/autonom.sh`. Danach läuft der Betrieb 24/7 ohne deinen Rechner. Siehe autonom/README.md
- [ ] Kennwort für den Posteingang festlegen. `autonom.sh` schlägt eines vor und trägt es nach Rückfrage in config.json ein. Ohne Kennwort bleibt der Mail-Eingang abgeschaltet
- [ ] Falls im Cron noch `tagesbrief.py` steht: Eintrag entfernen, sonst kommt die Morgenmail doppelt. `autonom.sh` warnt, löscht aber nichts
- [ ] Zweiter Kanal neben der Mail: Telegram-Bot mit Knöpfen statt Tippen? Braucht einen Bot-Token von dir. Mail funktioniert ohne alles und ist deshalb zuerst gebaut
- [ ] Solange der Server keine Abteilung "06 Web & Shop" kennt, werden Aufträge dorthin abgewiesen — auch die per Mail. Hängt an der Nummernentscheidung zwei Punkte weiter oben

## Produkt

- [ ] Koppel KO-01: Wird sie gebaut, wenn sich kein Messingwirbel findet? Stahl ist ausgeschlossen
- [ ] Werkstattdurchsicht WD-01 als Leistung für 29 EUR: kommt sie?
- [ ] Pflegeset PF-01 für 44 EUR: kommt es, mit eigener Anleitung?
- [ ] Namensschilder NS-01 und NS-02: Antwort des Herstellers auf Frage 5 der RFQ einholen, ob Einzelgravur auf Zuruf möglich ist

## Website

- [ ] Aufnahmeliste abarbeiten: 11 Fotos, davon zwei Paare neu und getragen. Ohne diese Fotos kein Shopstart. Siehe web/aufnahmen/
- [ ] Echte Prüfdaten für den Prüfbericht liefern: Hund, Tage, Belastung, Befund. Aktuell stehen Platzhalter auf der Seite
- [ ] Lederscan als Textur für die Materialansicht liefern
- [ ] Shopsystem entscheiden: Shopify mit Hydrogen, wie empfohlen, oder Next.js mit Medusa

- [ ] **Kleinunternehmerregelung nach § 19 UStG: ja oder nein?** Zurzeit steht auf jeder Seite "inklusive 19 % Umsatzsteuer". Bei Kleinunternehmerregelung ist das falsch und muss überall geändert werden. Diese eine Antwort läuft durch den ganzen Shop
- [ ] **Wer trägt die Rücksendekosten beim Widerruf?** Muss in Widerrufsbelehrung und Versandseite wortgleich stehen. Zurzeit steht dort beides nebeneinander, einer der Sätze muss weg
- [ ] Anbieterangaben für die Rechtsseiten: Name oder Firma mit Rechtsform, ladungsfähige Anschrift, zweiter Kontaktweg neben der Mail, USt-IdNr. Alles orange unterstrichen in web/recht/. Danach anwaltlich prüfen lassen
- [ ] Abnahmetor Punkt 4: Richtung 03 ist bewusst nur dunkel. Punkt für dieses Projekt streichen oder Hell-Variante bauen? Siehe web/ABNAHME.md
- [ ] Abnahmetor Punkt 6: drei Schriftfamilien bei einem Budget von zwei. Vorschlag: IBM Plex Mono streichen, Artikelnummern und Preise in gesperrtem Archivo setzen. Kostet Charakter, hält das Budget
- [ ] Startseite auf tokens.css umstellen. Sie trägt das Designsystem noch als Kopie, und bei der ersten Korrektur musste dieselbe Änderung schon an zwei Stellen gemacht werden

## Marke

- [ ] Positionierungssatz "aus eigener Werkstatt" bleibt gültig, solange in Hamburg gefertigt wird. Bei der ersten Lieferung aus China ersetzen, Ersatztext liegt in konzepte/kollektion-01-hamburg.md
