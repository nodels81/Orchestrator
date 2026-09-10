#!/usr/bin/env python3
"""dashboard.py — baut /opt/bello/daten/dashboard.html (+ dashboard/dashboard.html)
aus dem aktuellen Stand. Wird vom Tageslauf-Wrapper nach jedem Lauf aufgerufen.
Kein Server, nur Dateien."""
import json, os, re, subprocess, datetime, html

BASIS = "/opt/bello"
DATEN = os.path.join(BASIS, "daten")
AUF = os.path.join(DATEN, "auftraege.json")
OUT_LIVE = os.path.join(DATEN, "dashboard.html")
OUT_REPO = os.path.join(BASIS, "dashboard", "dashboard.html")

# nr, vorname, fach, kurzrolle, fachliche Zulieferung -> Zielabteilungsnummern
ABTEILUNGEN = [
    ("01", "Merle",  "Innovation",           "beobachtet den Markt, liefert Produktkonzepte",             ["02"]),
    ("02", "Konrad", "Produkt & Ausführung", "macht aus Konzepten Spezifikation, Stückliste, Zeichnung",  ["06", "07"]),
    ("03", "Silke",  "Vertrieb",             "Angebote und Kundenantworten als Entwurf",                  []),
    ("04", "Lasse",  "Social Media",         "Beitragstexte und Aufnahmeanweisungen für echte Fotos",     []),
    ("05", "Wiebke", "Personal",             "erkennt Personalbedarf, entwirft neue Abteilungen",         ["06", "07"]),
    ("06", "Insa",   "Einkauf",              "allgemeine Lieferantenanfragen und Angebotsvergleiche",     []),
    ("07", "Henrik", "Einkauf China",        "RFQ / Verhandlung / Muster mit chinesischen Herstellern",   []),
    ("08", "Thea",   "Design",               "entwirft die Form: Silhouette, Proportionen, Beschlag-Layout", ["02"]),
    ("09", "Almut",  "Qualität",             "prüft die Arbeit der anderen vor deiner Entscheidung",         []),
]
ORCHESTRATOR = "Gustav"

STAND_META = {
    "wartet auf Bjoern": ("wartet auf dich", "kupfer", 0),
    "nacharbeit":        ("in Nacharbeit",   "amber",  1),
    "offen":             ("offen",           "grau",   2),
    "gestoert":          ("gestört",         "rot",    3),
    "gescheitert":       ("gescheitert",     "rot",    3),
    "abgelehnt":         ("abgelehnt",       "rot",    3),
    "freigegeben":       ("freigegeben",     "oliv",   4),
    "fertig":            ("erledigt",        "oliv",   5),
}
AKTIV_STAENDE = ("offen", "nacharbeit", "wartet auf Bjoern")


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def esc(s):
    return html.escape(str(s if s is not None else ""))


def kurz(text, n=600):
    text = re.sub(r"<<<SVG>>>.*?<<</SVG>>>", "[bemaßte Zeichnung — daten/zeichnungen/]", str(text), flags=re.S)
    text = re.sub(r"<svg.*?</svg>", "[bemaßte Zeichnung]", text, flags=re.S | re.I)
    text = text.strip()
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def dt(s):
    if not s:
        return "—"
    try:
        return datetime.datetime.fromisoformat(s).strftime("%d.%m.%Y %H:%M")
    except Exception:
        return str(s)


HEAD_START = ("OFFENE ENTSCHEIDUNGEN", "RÜCKFRAGEN AN BJ", "RUECKFRAGEN AN BJ",
             "ENTSCHEIDUNGEN FÜR BJ", "ENTSCHEIDUNGEN FUER BJ", "OFFENE PUNKTE FÜR BJ",
             "OFFENE PUNKTE FUER BJ", "OFFENE FRAGEN", "EMPFEHLUNG / REIHENFOLGE",
             "EMPFEHLUNG UND REIHENFOLGE", "EMPFEHLUNG FÜR BJ", "EMPFEHLUNG FUER BJ")
HEAD_STOP = ("NÄCHSTER SCHRITT", "NAECHSTER SCHRITT", "EINBAU", "ANMERKUNG",
             "ERGEBNIS", "LIEFERT", "GRENZEN", "ABNAHMEKRITERIEN", "ERSTER TESTAUFTRAG",
             "BEDARF", "NUMMER UND NAME", "ROLLE", "SPEZIFIKATION", "STÜCKLISTE",
             "STUECKLISTE", "ZEICHNUNG")


def offene_fragen(ergebnis):
    if not ergebnis:
        return []
    out, grab = [], False
    for ln in str(ergebnis).splitlines():
        s = ln.strip()
        up = s.upper().rstrip(":").strip()
        if not grab:
            if any(up.startswith(k) or k in up for k in HEAD_START):
                grab = True
            continue
        if not s:
            if out:
                # Leerzeile nach begonnener Liste = Ende
                break
            continue
        if any(k in up for k in HEAD_STOP) and (":" not in s or s.endswith(":")):
            break
        out.append(s)
        if len(out) >= 10:
            break
    # Nur sinnvolle Zeilen
    return [x for x in out if len(x) > 2][:8]


def naechster_schritt(ergebnis):
    if not ergebnis:
        return ""
    lines = str(ergebnis).splitlines()
    for i, ln in enumerate(lines):
        up = ln.strip().upper()
        if up.startswith(("NÄCHSTER SCHRITT", "NAECHSTER SCHRITT", "4. NÄCHSTER", "4. NAECHSTER")):
            rest = ln.split(":", 1)[1].strip() if ":" in ln else ""
            j = i + 1
            while not rest and j < len(lines) and j < i + 4:
                rest = lines[j].strip()
                j += 1
            return kurz(rest, 180)
    return ""


# ---------- Daten ----------
data = {"auftraege": [], "letzter_lauf": None, "letzter_wochenbericht": None}
if os.path.exists(AUF):
    try:
        data = json.load(open(AUF, encoding="utf-8"))
    except Exception:
        pass
auftraege = data.get("auftraege", [])
heute = datetime.date.today()
now = datetime.datetime.now()
naechster = now.replace(hour=7, minute=0, second=0, microsecond=0)
if naechster <= now:
    naechster += datetime.timedelta(days=1)

timer_an = sh("systemctl is-active bello-orchestrator.timer") == "active"
backup_last = sh("ls -1t /var/backups/bello/bello-*.tar.gz 2>/dev/null | head -1")
backup_n = sh("ls -1 /var/backups/bello/bello-*.tar.gz 2>/dev/null | wc -l") or "0"
disk = sh("df -h / | awk 'NR==2{print $4}'") or "?"
backup_when = "—"
if backup_last:
    try:
        backup_when = datetime.datetime.fromtimestamp(os.path.getmtime(backup_last)).strftime("%d.%m.%Y %H:%M")
    except Exception:
        pass


def sortkey(a):
    return (STAND_META.get(a.get("stand", ""), ("", "", 9))[2], a.get("id", ""))


auftraege_sortiert = sorted(auftraege, key=sortkey)
wartend = [a for a in auftraege if a.get("stand") == "wartet auf Bjoern"]
offen_zahl = len([a for a in auftraege if a.get("stand") in ("offen", "nacharbeit")])
aktiv_nr = {a.get("abteilung", "").split(" ", 1)[0] for a in auftraege if a.get("stand") in AKTIV_STAENDE}


def letzter_auftrag_fuer(nr):
    treffer = [a for a in auftraege if a.get("abteilung", "").startswith(nr + " ")]
    if not treffer:
        return None
    # bevorzugt ein aktiver, sonst der neueste
    aktive = [a for a in treffer if a.get("stand") in AKTIV_STAENDE]
    pool = aktive or treffer
    return sorted(pool, key=lambda a: a.get("angelegt", ""))[-1]


def frist_klasse(a):
    if a.get("stand") == "fertig":
        return ""
    f = a.get("frist")
    try:
        d = datetime.date.fromisoformat(f)
    except Exception:
        return ""
    if d < heute:
        return "frist-rot"
    if (d - heute).days <= 7:
        return "frist-amber"
    return ""


def pill(stand):
    label, farbe, _ = STAND_META.get(stand, (stand, "grau", 9))
    return f'<span class="pill p-{farbe}">{esc(label)}</span>'


VN = {nr: vn for nr, vn, *_ in ABTEILUNGEN}


def agent_label(abteilung):
    nr = str(abteilung).split(" ", 1)[0]
    vn = VN.get(nr, "")
    return f"{vn} · {abteilung}" if vn else str(abteilung)


# ---------- Karten: Deine Entscheidungen ----------
ent_karten = []
for a in wartend:
    v = (a.get("verlauf") or [{}])[-1]
    erg = v.get("ergebnis") or v.get("fehler") or ""
    fragen = offene_fragen(erg)
    schritt = naechster_schritt(erg)
    frag_html = ""
    if fragen:
        frag_html = "<div class='block'><div class='block-t'>Worüber du entscheidest</div><ul>" + \
            "".join(f"<li>{esc(f)}</li>" for f in fragen) + "</ul></div>"
    ent_karten.append(f"""
    <article class="karte">
      <div class="karte-kopf">
        <div><span class="aid">{esc(a.get('id'))}</span> <span class="abt">{esc(agent_label(a.get('abteilung')))}</span></div>
        <div class="frist {frist_klasse(a)}">Frist {esc(a.get('frist','—'))}</div>
      </div>
      <h3>{esc(a.get('ziel'))}</h3>
      <p class="ergebnis">{esc(kurz(erg, 460))}</p>
      {frag_html}
      {f'<div class="block"><div class="block-t">Nächster Schritt</div><p>{esc(schritt)}</p></div>' if schritt else ''}
      <p class="quelle">Volltext in der E-Mail · <code>daten/auftraege.json</code></p>
    </article>""")

# ---------- Werkbank: pro Abteilung ----------
wb_karten = []
for nr, vn, fach, rolle, _ in ABTEILUNGEN:
    a = letzter_auftrag_fuer(nr)
    aktiv = nr in aktiv_nr
    if a:
        v = (a.get("verlauf") or [{}])[-1]
        stand = a.get("stand")
        zeile_auftrag = f"<div class='wb-auf'><span class='aid'>{esc(a.get('id'))}</span> {esc(kurz(a.get('ziel'), 90))}</div>"
        zeile_stand = f"{pill(stand)}"
        if v.get("begruendung"):
            zeile_stand += f" <span class='wb-grund'>{esc(kurz(v.get('begruendung'), 60))}</span>"
        fragen = offene_fragen(v.get("ergebnis") or "") if stand == "wartet auf Bjoern" else []
        frag = ("<div class='wb-fragen'>offen für dich: " +
                "; ".join(esc(kurz(f, 70)) for f in fragen[:3]) + "</div>") if fragen else ""
        schritt = naechster_schritt(v.get("ergebnis") or "")
        nx = f"<div class='wb-next'>→ {esc(schritt)}</div>" if schritt else ""
    else:
        zeile_auftrag = "<div class='wb-auf leer'>noch kein Auftrag</div>"
        zeile_stand = "<span class='pill p-grau'>bereit</span>"
        frag = nx = ""
    wb_karten.append(f"""
      <div class="wb {'wb-aktiv' if aktiv else ''}">
        <div class="wb-kopf"><span class="wb-nr">{nr}</span><span class="wb-name">{esc(vn)}</span><span class="wb-fach">{esc(fach)}</span></div>
        <div class="wb-rolle">{esc(rolle)}</div>
        <div class="wb-status">{zeile_stand}</div>
        {zeile_auftrag}
        {frag}{nx}
      </div>""")

# ---------- Zusammenspiel (SVG) ----------
W, H = 1180, 430
cx = W / 2
bjoern_y, orch_y, dept_y = 40, 120, 300
n = len(ABTEILUNGEN)
x0, x1 = 66, W - 66
xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
node_w, node_h = 112, 44

svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="karte-svg">']
svg.append('<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
           '<path d="M0,0 L6,3 L0,6 Z" fill="#8a7d63"/></marker>'
           '<marker id="ak" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
           '<path d="M0,0 L6,3 L0,6 Z" fill="#b06a34"/></marker></defs>')
# Linien Orchestrator <-> Abteilungen
for i, (nr, vn, fach, _, _) in enumerate(ABTEILUNGEN):
    akt = nr in aktiv_nr
    col = "#b06a34" if akt else "#c9bda3"
    wsw = "2" if akt else "1.2"
    svg.append(f'<line x1="{cx}" y1="{orch_y+22}" x2="{xs[i]}" y2="{dept_y-node_h/2}" '
               f'stroke="{col}" stroke-width="{wsw}" marker-end="url(#{"ak" if akt else "a"})"/>')
# fachliche Zulieferungen (gestrichelt)
pos = {nr: xs[i] for i, (nr, *_r) in enumerate(ABTEILUNGEN)}
for nr, vn, fach, rolle, ziele in ABTEILUNGEN:
    for z in ziele:
        if z in pos:
            x_a, x_b = pos[nr], pos[z]
            my = dept_y + node_h / 2 + 46
            svg.append(f'<path d="M {x_a} {dept_y+node_h/2} Q {(x_a+x_b)/2} {my} {x_b} {dept_y+node_h/2}" '
                       f'fill="none" stroke="#b9a98a" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#a)"/>')
# Björn <-> Orchestrator
svg.append(f'<line x1="{cx}" y1="{bjoern_y+16}" x2="{cx}" y2="{orch_y-16}" stroke="#5c4433" '
           f'stroke-width="1.6" marker-end="url(#a)" marker-start="url(#a)"/>')
svg.append(f'<text x="{cx+10}" y="{(bjoern_y+orch_y)/2+4}" font-size="10" fill="#7a7266">eskaliert · gibt frei</text>')
# Knoten Björn
svg.append(f'<rect x="{cx-52}" y="{bjoern_y-16}" width="104" height="32" rx="16" fill="#5c4433"/>'
           f'<text x="{cx}" y="{bjoern_y+4}" text-anchor="middle" font-size="12.5" fill="#fff" font-weight="700">Björn</text>')
# Knoten Orchestrator
svg.append(f'<rect x="{cx-78}" y="{orch_y-18}" width="156" height="40" rx="10" fill="#6b6f3e"/>'
           f'<text x="{cx}" y="{orch_y+2}" text-anchor="middle" font-size="12.5" fill="#fff" font-weight="700">{ORCHESTRATOR}</text>'
           f'<text x="{cx}" y="{orch_y+16}" text-anchor="middle" font-size="9" fill="#e7edda">Orchestrator · verteilt · prüft · eskaliert</text>')
# Knoten Abteilungen
for i, (nr, vn, fach, _, _) in enumerate(ABTEILUNGEN):
    akt = nr in aktiv_nr
    fill = "#f7ebdd" if akt else "#ffffff"
    stroke = "#b06a34" if akt else "#e4dac6"
    svg.append(f'<rect x="{xs[i]-node_w/2}" y="{dept_y-node_h/2}" width="{node_w}" height="{node_h}" rx="9" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
    a = letzter_auftrag_fuer(nr)
    lab = STAND_META.get(a.get("stand"), ("", "", 9))[0] if a else "bereit"
    svg.append(f'<text x="{xs[i]}" y="{dept_y-7}" text-anchor="middle" font-size="11" font-weight="700" fill="#5c4433">{esc(vn)}</text>')
    svg.append(f'<text x="{xs[i]}" y="{dept_y+4}" text-anchor="middle" font-size="7.5" fill="#8a7d63">{nr} · {esc(fach)}</text>')
    svg.append(f'<text x="{xs[i]}" y="{dept_y+15}" text-anchor="middle" font-size="8" fill="{"#b06a34" if akt else "#a99e88"}">{esc(lab)}</text>')
svg.append(f'<text x="{x0-2}" y="{dept_y+node_h/2+70}" font-size="9" fill="#9a8f7c">'
           f'durchgezogen: Auftrag &amp; Bericht über den Orchestrator · gestrichelt: fachliche Zulieferung</text>')
svg.append("</svg>")
svg_html = "".join(svg)

# ---------- Tabelle ----------
zeilen = []
for a in auftraege_sortiert:
    zeilen.append(f"""
      <tr>
        <td class="mono">{esc(a.get('id'))}</td>
        <td>{esc(agent_label(a.get('abteilung')))}</td>
        <td class="ziel">{esc(kurz(a.get('ziel'), 110))}</td>
        <td>{pill(a.get('stand'))}</td>
        <td class="zentr">{esc(a.get('versuche', 0))}</td>
        <td class="{frist_klasse(a)}">{esc(a.get('frist','—'))}</td>
        <td class="mono klein">{dt(a.get('angelegt'))}</td>
      </tr>""")

status_txt = "läuft" if timer_an else "ANGEHALTEN"
status_farbe = "s-gut" if timer_an else "s-warn"
verarbeitet = len([a for a in auftraege if a.get("versuche", 0) > 0])

HTML = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bello · Werkbank</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,500&display=swap');
  :root{{
    --paper:#fff; --bg:#f1ebdd; --ink:#2c2822; --muted:#847a6c; --line:#e4dac6;
    --oliv:#5f6b3a; --braun:#5c4433; --kupfer:#b06a34; --kupfer-weich:#f7ebdd;
    --amber:#b8862b; --rot:#a5402f; --grau:#8a8172;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:var(--bg);color:var(--ink);
    font:15px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    padding:26px 18px 60px;max-width:1080px;margin:0 auto}}
  h1,h2,h3{{font-family:'Lora',Georgia,serif;font-weight:600}}
  code{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.84em;background:#0000000d;padding:1px 5px;border-radius:4px}}
  header{{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;
    border-bottom:2px solid var(--braun);padding-bottom:15px;margin-bottom:24px}}
  .wortmarke{{font-family:'Lora',serif;font-size:27px;font-weight:700;color:var(--braun);line-height:1}}
  .wortmarke span{{color:var(--kupfer)}}
  .unterzeile{{color:var(--muted);font-size:13px;margin-top:6px}}
  .statuspille{{font-size:13px;font-weight:600;padding:6px 13px;border-radius:999px;white-space:nowrap}}
  .s-gut{{background:#e7edda;color:var(--oliv)}} .s-warn{{background:#f6ddd6;color:var(--rot)}}
  .kennzahlen{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:28px}}
  .kz{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:11px 15px;min-width:120px;flex:1}}
  .kz .zahl{{font-family:'Lora',serif;font-size:22px;font-weight:700;color:var(--braun)}}
  .kz .txt{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-top:2px}}
  .kz.betont{{background:var(--kupfer-weich);border-color:#e8c9a9}} .kz.betont .zahl{{color:var(--kupfer)}}
  section{{margin-bottom:32px}}
  section>h2{{font-size:18px;color:var(--braun);margin-bottom:6px;display:flex;align-items:baseline;gap:10px}}
  section>h2 .anz{{font-size:13px;color:var(--muted);font-weight:400;font-family:inherit}}
  .lead{{color:var(--muted);font-size:13px;margin-bottom:14px}}
  .karte{{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--kupfer);
    border-radius:10px;padding:17px 19px;margin-bottom:13px;box-shadow:0 1px 2px #0000000a}}
  .karte-kopf{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:7px}}
  .aid{{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--muted)}}
  .abt{{font-size:12.5px;color:var(--kupfer);font-weight:600;margin-left:4px}}
  .karte h3{{font-size:15.5px;margin-bottom:9px}}
  .ergebnis{{font-size:13.5px;color:#463f36;white-space:pre-wrap}}
  .block{{margin-top:11px;padding-top:10px;border-top:1px dashed var(--line)}}
  .block-t{{font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--kupfer);font-weight:700;margin-bottom:5px}}
  .block ul{{margin:0 0 0 18px}} .block li{{font-size:13.5px;margin-bottom:3px}}
  .block p{{font-size:13.5px}}
  .quelle{{font-size:11.5px;color:var(--muted);margin-top:10px}}
  .frist{{font-size:12.5px;color:var(--muted)}}
  .frist-rot{{color:var(--rot);font-weight:700}} .frist-amber{{color:var(--amber);font-weight:600}}
  .wb-gitter{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}}
  .wb{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
  .wb-aktiv{{border-color:var(--kupfer);box-shadow:0 0 0 3px var(--kupfer-weich)}}
  .wb-kopf{{display:flex;align-items:baseline;gap:8px}}
  .wb-nr{{font-family:'Lora',serif;font-size:15px;font-weight:700;color:var(--kupfer)}}
  .wb-name{{font-weight:700;font-size:15px}}
  .wb-fach{{font-size:11.5px;color:var(--muted)}}
  .wb-rolle{{font-size:12px;color:var(--muted);margin:2px 0 9px}}
  .wb-status{{margin-bottom:6px}}
  .wb-grund{{font-size:11.5px;color:var(--muted)}}
  .wb-auf{{font-size:12.5px;color:#4a4238}}
  .wb-auf.leer{{color:var(--muted);font-style:italic}}
  .wb-fragen{{font-size:12px;color:var(--braun);margin-top:6px;background:var(--kupfer-weich);padding:6px 8px;border-radius:6px}}
  .wb-next{{font-size:12px;color:var(--oliv);margin-top:5px}}
  .svg-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch;background:var(--paper);border:1px solid var(--line);border-radius:10px}}
  .karte-svg{{display:block;width:100%;min-width:820px;height:auto;padding:8px}}
  .tabelle-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:10px}}
  table{{width:100%;border-collapse:collapse;background:var(--paper);min-width:520px}}
  th,td{{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}}
  th{{background:#faf6ee;font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}}
  tr:last-child td{{border-bottom:none}}
  td.ziel{{color:#514a40;font-size:13px;max-width:330px}}
  .mono{{font-family:ui-monospace,Menlo,monospace;font-size:12px}} .klein{{color:var(--muted)}} .zentr{{text-align:center}}
  .pill{{display:inline-block;font-size:11px;font-weight:700;padding:3px 8px;border-radius:999px;white-space:nowrap}}
  .p-kupfer{{background:#f0d8bf;color:#8f4f22}} .p-amber{{background:#f5e6c4;color:#8a6414}}
  .p-oliv{{background:#e3ecd2;color:#4b5730}} .p-grau{{background:#e9e4d8;color:#6d6454}} .p-rot{{background:#f2d3cc;color:#8f2f22}}
  .system{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;
    background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:16px 18px}}
  .sys-zeile{{font-size:13px}}
  .sys-zeile b{{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:1px}}
  .erkl{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:15px 18px;font-size:13.5px;color:#463f36}}
  .erkl ol{{margin:8px 0 0 18px}} .erkl li{{margin-bottom:4px}}
  footer{{margin-top:32px;padding-top:13px;border-top:1px solid var(--line);color:var(--muted);
    font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}}
  .leer-box{{color:var(--muted);font-style:italic;background:var(--paper);border:1px dashed var(--line);border-radius:10px;padding:15px 18px}}
  @media (max-width:560px){{th:nth-child(7),td:nth-child(7){{display:none}}}}
</style>
</head>
<body>
<header>
  <div>
    <div class="wortmarke">Bello<span>werk</span></div>
    <div class="unterzeile">KI-Agentenbetrieb · Werkbank für Björn · Stand {now.strftime('%d.%m.%Y %H:%M')}</div>
  </div>
  <div class="statuspille {status_farbe}">Tageslauf: {status_txt}</div>
</header>

<div class="kennzahlen">
  <div class="kz betont"><div class="zahl">{len(wartend)}</div><div class="txt">warten auf dich</div></div>
  <div class="kz"><div class="zahl">{offen_zahl}</div><div class="txt">in Arbeit</div></div>
  <div class="kz"><div class="zahl">{len(auftraege)}</div><div class="txt">Aufträge gesamt</div></div>
  <div class="kz"><div class="zahl">{len(ABTEILUNGEN)}</div><div class="txt">Abteilungen</div></div>
  <div class="kz"><div class="zahl">{naechster.strftime('%H:%M')}</div><div class="txt">nächster Lauf {'morgen' if naechster.date() > heute else 'heute'}</div></div>
</div>

<section>
  <h2>Deine Entscheidungen <span class="anz">{len(wartend)} offen</span></h2>
  {''.join(ent_karten) if ent_karten else '<div class="leer-box">Nichts zu entscheiden. Der Betrieb läuft still weiter.</div>'}
</section>

<section>
  <h2>Werkbank <span class="anz">jede Abteilung einzeln</span></h2>
  <div class="lead">Wo jeder Agent gerade steht, was er zuletzt gemacht hat und was von dir gebraucht wird. Kupfer umrandet = arbeitet gerade.</div>
  <div class="wb-gitter">{''.join(wb_karten)}</div>
</section>

<section>
  <h2>Zusammenspiel</h2>
  <div class="lead">Wer mit wem. Björn entscheidet, {ORCHESTRATOR} (der Orchestrator) verteilt und prüft, die Abteilungen liefern zu.</div>
  <div class="svg-wrap">{svg_html}</div>
</section>

<section>
  <h2>Was {ORCHESTRATOR} tut</h2>
  <div class="erkl">
    <b>{ORCHESTRATOR}</b> ist der Orchestrator. Einmal am Tag um 07:00 nimmt er sich jeden offenen Auftrag vor:
    <ol>
      <li>Auftrag an die zuständige Abteilung geben, Ergebnis maschinell gegen die Abnahmekriterien prüfen.</li>
      <li>Bestanden → an dich eskalieren (jedes Ergebnis geht zur Freigabe). Nicht bestanden → einmal Nacharbeit, höchstens {esc(2)}× insgesamt, dann eskalieren.</li>
      <li>Technischer Fehler oder überschrittene Frist → sofort an dich.</li>
      <li>Einmal pro Woche eine Übersicht per Mail. Sonst Stille.</li>
    </ol>
    Er gibt <b>nie</b> selbst Geld aus, bestellt nichts, verschickt nichts nach außen außer der Mail an dich.
    <div style="margin-top:9px;color:var(--muted);font-size:12.5px">
      Zuletzt gelaufen: {dt(data.get('letzter_lauf'))} · verarbeitete Aufträge bisher: {verarbeitet} ·
      letzte Wochenübersicht: {dt(data.get('letzter_wochenbericht'))}
    </div>
  </div>
</section>

<section>
  <h2>Alle Aufträge <span class="anz">{len(auftraege)}</span></h2>
  {'<div class="tabelle-wrap"><table><thead><tr><th>ID</th><th>Abteilung</th><th>Ziel</th><th>Stand</th><th>Vers.</th><th>Frist</th><th>angelegt</th></tr></thead><tbody>' + ''.join(zeilen) + '</tbody></table></div>' if auftraege else '<div class="leer-box">Noch keine Aufträge.</div>'}
</section>

<section>
  <h2>System</h2>
  <div class="system">
    <div class="sys-zeile"><b>Tageslauf</b>{'aktiv, täglich 07:00' if timer_an else 'ANGEHALTEN'}</div>
    <div class="sys-zeile"><b>Nächster Lauf</b>{naechster.strftime('%d.%m.%Y %H:%M')}</div>
    <div class="sys-zeile"><b>Letzter Lauf</b>{dt(data.get('letzter_lauf'))}</div>
    <div class="sys-zeile"><b>Letzte Sicherung</b>{backup_when} ({esc(backup_n)} vorhanden)</div>
    <div class="sys-zeile"><b>Speicher frei</b>{esc(disk)}</div>
    <div class="sys-zeile"><b>Eskalationsmail</b>gustav.bellowerk@gmail.com → pijoern.nodels@gmail.com</div>
    <div class="sys-zeile"><b>Code</b>git-Repo, Update mit <code>git pull</code></div>
  </div>
</section>

<footer>
  <span>Automatisch nach jedem Tageslauf · <code>/opt/bello/daten/dashboard.html</code></span>
  <span>{now.strftime('%d.%m.%Y %H:%M:%S')}</span>
</footer>
</body>
</html>
"""

for ziel in (OUT_LIVE, OUT_REPO):
    try:
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        tmp = ziel + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(HTML)
        os.replace(tmp, ziel)
    except Exception as e:
        print(f"[dashboard] {ziel}: {e}")
print(f"Dashboard: {len(auftraege)} Auftraege, {len(wartend)} wartend, {len(ABTEILUNGEN)} Abteilungen -> {OUT_LIVE}")
