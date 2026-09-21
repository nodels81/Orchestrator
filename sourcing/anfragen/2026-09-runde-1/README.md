# Anfragerunde 1 — September 2026

Erstkontakt-RFQs für **LE-01** (Führleine 2,60 m) und **HB-01** (Halsband). Stand 21.09.2026.

**Noch nicht versendet.** Zwei Dinge fehlen: die Kontaktdaten (Platzhalter `[E-Mail]` und
`[WhatsApp/WeChat]` in allen Texten) und die Freigabe.

## Welcher Text an wen

| Datei | Lieferant | Modelle | Kanal |
|---|---|---|---|
| `A-kingming-wenzhou.txt` | Kingming Pet · Wenzhou Vigorous | LE-01 + HB-01 | Website-Formular · made-in-china |
| `A-wedogy.txt` | Wedogy | LE-01 + HB-01 | Website-Formular |
| `B-szoneier-pnuts.txt` | Szoneier Leather · P-NUTS Pet | HB-01 | Website-Formular |
| `B-yantao.txt` | Dongguan Yantao | HB-01 | made-in-china |

Lieferantenspezifische Abweichungen: **Wedogy** führt standardmäßig Edelstahl, deshalb steht dort
Messing ausdrücklich drin. **Yantao** fertigt Beschläge im Haus, deshalb die Zusatzfrage danach.

## Kein E-Mail-Versand möglich

Keiner dieser sechs Lieferanten hat eine E-Mail-Adresse im Tracker — alle laufen über
Website-Kontaktformular, Alibaba-Chat oder made-in-china. Die Texte sind deshalb zum **Einkopieren
ins Formular** gebaut: Betreff separat, kompakt (944–1283 Zeichen), Anhänge als Liste am Ende.
Formulare begrenzen oft die Zeichenzahl und die Zahl der Uploads — notfalls nur Zeichnungsblatt 1
und Blatt 3 plus ein Foto anhängen und den Rest nachreichen.

## Anhänge

- **LE-01:** `zeichnungen/LE-01-fuehrleine.png`, `LE-01-detail-flechtung.png`,
  `LE-01-flechtung-schritte.png` (Blatt 3 ist der wichtigste Anhang — daran zeigt sich, ob der
  Hersteller den Bleed Knot beherrscht) + `bilder/LE-01-goldmuster-ring-geknotet.jpg`
- **HB-01:** `zeichnungen/HB-01-halsband.png` + `bilder/HB-01-detail-patch.jpg`,
  `HB-01-farben-patch.jpg`

## HB-02 ist NICHT dabei

Das Flechthalsband bleibt draußen, bis geklärt ist, ob das Halsteil geflochten oder geknotet ist —
siehe Warnblock in `specs/HB-02-halsband-geflochten.md`. Geht in Runde 2 mit.

## Termine

- Antwortfrist in den Texten: **30.09.2026**
- **Golden Week 01.–07.10.2026** — chinesische Büros geschlossen. Deshalb muss die Anfrage vorher
  raus und die Frist davor liegen.
- Nachfassen (`vorlagen/02-nachfassen.md`) frühestens **08.10.2026**.

## Nach dem Versand

Je Lieferant eine Zeile in `sourcing/lieferanten/tracker.csv` nachziehen:
`status` → "RFQ gesendet", `letzter_kontakt` → Versanddatum, `kanal` → tatsächlich benutzter Kanal,
`naechster_schritt` → "Nachfassen", `faellig` → 08.10.2026.
