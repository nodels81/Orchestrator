#!/usr/bin/env python3
"""galerie.py — baut /opt/bello/daten/galerie.html (+ galerie/galerie.html) aus allen
Zeichnungen in daten/zeichnungen/. Wird vom Tageslauf-Wrapper aufgerufen. Nur Dateien."""
import html
import json
import os
import re
import datetime

BASIS = "/opt/bello"
DATEN = os.path.join(BASIS, "daten")
QUELLE = os.path.join(DATEN, "zeichnungen")
AUF = os.path.join(DATEN, "auftraege.json")
OUT_LIVE = os.path.join(DATEN, "galerie.html")
OUT_REPO = os.path.join(BASIS, "galerie", "galerie.html")

ID_RE = re.compile(r"^(A-\d{4}-\d+)-(.+)\.svg$")


def esc(s):
    return html.escape(str(s if s is not None else ""))


def auftraege_index():
    idx = {}
    if os.path.exists(AUF):
        try:
            for a in json.load(open(AUF, encoding="utf-8")).get("auftraege", []):
                idx[a["id"]] = a
        except Exception:
            pass
    return idx


def sanitize_svg(s: str) -> str:
    s = re.sub(r"<\?xml.*?\?>", "", s, flags=re.S)
    s = re.sub(r"<!DOCTYPE.*?>", "", s, flags=re.S)
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S | re.I)
    m = re.search(r"<svg[\s\S]*?</svg>", s, re.I)
    return m.group(0) if m else ""


gruppen = {}
for datei in sorted(os.listdir(QUELLE)) if os.path.isdir(QUELLE) else []:
    m = ID_RE.match(datei)
    if m:
        aid, slug = m.group(1), m.group(2)
    else:
        m2 = re.match(r"^(A-\d{4}-\d+)\.svg$", datei)  # ohne slug, z. B. A-2026-004.svg
        if not m2:
            continue
        aid, slug = m2.group(1), ""
    try:
        svg = sanitize_svg(open(os.path.join(QUELLE, datei), encoding="utf-8").read())
    except Exception:
        continue
    if svg:
        gruppen.setdefault(aid, []).append((slug or datei, svg, datei))

idx = auftraege_index()
now = datetime.datetime.now()

karten = []
for aid in sorted(gruppen, reverse=True):
    a = idx.get(aid, {})
    abteilung = a.get("abteilung", "?")
    ziel = a.get("ziel", "")
    angelegt = a.get("angelegt", "")
    try:
        dat = datetime.datetime.fromisoformat(angelegt).strftime("%d.%m.%Y")
    except Exception:
        dat = ""
    bilder = "".join(
        f'<figure><figcaption>{esc(slug.replace("_", " "))}</figcaption>'
        f'<div class="rahmen">{svg}</div></figure>'
        for slug, svg, _ in sorted(gruppen[aid])
    )
    karten.append(f"""
    <section class="auftrag">
      <div class="kopf">
        <span class="aid">{esc(aid)}</span>
        <span class="abt">{esc(abteilung)}</span>
        <span class="dat">{esc(dat)}</span>
      </div>
      <div class="ziel">{esc(ziel[:220])}{'…' if len(ziel) > 220 else ''}</div>
      <div class="bilder">{bilder}</div>
    </section>""")

HTML = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bellowerk · Zeichnungen</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:wght@600;700&display=swap');
  :root{{--paper:#fff;--bg:#f1ebdd;--ink:#2c2822;--muted:#7a7062;--line:#e4dac6;
    --braun:#5c4433;--kupfer:#b06a34}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,"Segoe UI",Roboto,sans-serif;
    padding:26px 18px 60px;max-width:900px;margin:0 auto}}
  h1{{font-family:'Lora',Georgia,serif;font-size:24px;color:var(--braun);font-weight:700}}
  header{{border-bottom:2px solid var(--braun);padding-bottom:13px;margin-bottom:22px}}
  header p{{color:var(--muted);font-size:13px;margin-top:5px}}
  .auftrag{{background:var(--paper);border:1px solid var(--line);border-radius:12px;
    padding:16px 18px;margin-bottom:16px}}
  .kopf{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}
  .aid{{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--muted)}}
  .abt{{font-weight:700;color:var(--kupfer);font-size:13.5px}}
  .dat{{color:var(--muted);font-size:12px;margin-left:auto}}
  .ziel{{font-size:13px;color:#4a4238;margin:6px 0 12px}}
  .bilder{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}
  figure{{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fcfaf5}}
  figcaption{{font-size:11.5px;color:var(--muted);padding:6px 9px;border-bottom:1px solid var(--line);
    background:#faf6ee}}
  .rahmen{{padding:8px}}
  .rahmen svg{{display:block;width:100%;height:auto}}
  .leer{{color:var(--muted);font-style:italic;background:var(--paper);border:1px dashed var(--line);
    border-radius:10px;padding:16px}}
  footer{{margin-top:24px;padding-top:12px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}}
</style></head><body>
<header>
  <h1>Bellowerk — Zeichnungen</h1>
  <p>Alle Silhouetten und Skizzen aus dem Betrieb, neueste zuerst · Stand {now.strftime('%d.%m.%Y %H:%M')}</p>
</header>
{''.join(karten) if karten else '<div class="leer">Noch keine Zeichnungen.</div>'}
<footer>Automatisch nach jedem Tageslauf · <code>/opt/bello/daten/galerie.html</code></footer>
</body></html>
"""

for ziel in (OUT_LIVE, OUT_REPO):
    try:
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        tmp = ziel + ".tmp"
        open(tmp, "w", encoding="utf-8").write(HTML)
        os.replace(tmp, ziel)
    except Exception as e:
        print(f"[galerie] {ziel}: {e}")
print(f"Galerie: {sum(len(v) for v in gruppen.values())} Zeichnungen in {len(gruppen)} Auftraegen -> {OUT_LIVE}")
