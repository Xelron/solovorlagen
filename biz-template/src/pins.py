# -*- coding: utf-8 -*-
"""Pin-Grafiken 1000x1500 für Pinterest – Farben und Marke aus config.json.

    python3 src/pins.py              # rendert alle fehlenden Pins aus content/feeds.json
    python3 src/pins.py pin-03 pin-04  # nur diese (überschreibt)
    python3 src/pins.py --force      # alle neu

Braucht Playwright mit Chromium (pip install playwright && playwright install chromium).
Jeder Eintrag in content/feeds.json mit einem Block "pin" wird zu docs/pins/<id>.jpg:
  "pin": {"h1": "Große Zeile", "h2": "Zweite Zeile", "sub": "Kleine Zeile",
          "style": "text" | "img" | "price" | "list",
          "img": "img/produkt.jpg",          # bei style img (Bild aus docs/)
          "value": "19 €", "label": "EINMALIG", # bei style price
          "items": ["Punkt 1", "Punkt 2"]}       # bei style list
"""
import base64, html, json, mimetypes, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitekit as S
from sitekit import CFG, C, B, OUT

CSS = """*{box-sizing:border-box}body{margin:0;width:1000px;height:1500px;font-family:'DejaVu Sans',Arial,sans-serif}
.p{width:1000px;height:1500px;padding:80px 72px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
.serif{font-family:'DejaVu Serif',Georgia,serif;font-weight:700}.brand{font-size:30px;letter-spacing:.06em;display:flex;align-items:center;gap:18px}
.brand svg{width:56px;height:56px}
h1{font-size:92px;line-height:1.05;margin:28px 0 30px}.h2{font-size:52px;line-height:1.15;margin:0 0 24px}.sub{font-size:36px;line-height:1.35}
.url{font-size:34px;font-weight:700}.img{border-radius:28px;overflow:hidden;box-shadow:0 24px 48px rgba(0,0,0,.18)}
.box{border-radius:28px;padding:40px}
.item{display:flex;gap:22px;align-items:center;font-size:38px;padding:12px 0}.item b{width:50px;height:50px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex:none;font-size:30px}
"""


def themes():
    on = C.get("on_primary", "#fff")
    onm = C.get("on_primary_muted", "#ddd")
    return [
        dict(bg=C["primary"], fg=on, mut=onm, acc=C.get("focus", C["accent"]), box="rgba(255,255,255,.12)"),
        dict(bg=C["bg"], fg=C["primary"], mut=C["muted"], acc=C["accent"], box=C.get("surface", "#fff")),
        dict(bg=C.get("accent_dark", C["accent"]), fg="#FFFFFF", mut="rgba(255,255,255,.85)", acc="#FFFFFF", box="rgba(255,255,255,.14)"),
    ]


def _data_uri(rel):
    fp = os.path.join(OUT, rel)
    mime = mimetypes.guess_type(fp)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(open(fp, "rb").read()).decode()


def render(i, item):
    pin = item["pin"]
    t = themes()[i % 3]
    e = html.escape
    style = pin.get("style") or ("img" if pin.get("img") else "text")
    if style == "img" and pin.get("img"):
        mid = f'<div class=img style="height:640px;background:{t["box"]}"><img src="{_data_uri(pin["img"])}" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>'
    elif style == "price":
        mid = (f'<div class=box style="background:{t["box"]}"><div style="font-size:30px;color:{t["mut"]};font-weight:700">{e(pin.get("label", ""))}</div>'
               f'<div class=serif style="font-size:170px;color:{t["fg"]};line-height:1.1">{e(pin.get("value", ""))}</div></div>')
    elif style == "list":
        mid = f'<div class=box style="background:{t["box"]}">' + "".join(
            f'<div class=item style="color:{t["fg"]}"><b style="background:{t["acc"]};color:{t["bg"]}">✓</b>{e(x)}</div>' for x in pin.get("items", [])) + "</div>"
    else:
        mid = f'<div style="border-top:10px solid {t["acc"]};padding-top:40px;font-size:40px;font-weight:700;color:{t["fg"]};display:inline-block;align-self:flex-start">Jetzt lesen →</div>'
    h1 = pin.get("h1") or item["title"]
    big = len(h1) > 30 or max(len(w) for w in h1.split()) > 13
    return f"""<div class=p style="background:{t['bg']};color:{t['fg']}"><div>
<div class="brand serif" style="color:{t['mut']}">{S.logo_svg()}{e(B['name'].upper())}</div>
<h1 class=serif style="color:{t['fg']};{'font-size:70px' if big else ''}">{e(h1)}</h1>
<div class="h2 serif" style="color:{t['acc']}">{e(pin.get('h2', ''))}</div>
<div class=sub style="color:{t['mut']}">{e(pin.get('sub', ''))}</div></div>
{mid}<div class=url style="color:{t['fg']}">{e(S.DOMAIN)}</div></div>"""


def main(argv):
    from playwright.sync_api import sync_playwright
    items = [x for x in json.load(open(os.path.join(S.CONTENT, "feeds.json"), encoding="utf-8")) if x.get("pin")]
    force = "--force" in argv
    ids = [a for a in argv if not a.startswith("-")]
    os.makedirs(os.path.join(OUT, "pins"), exist_ok=True)
    todo = []
    for i, it in enumerate(items):
        dst = os.path.join(OUT, it.get("image") or f"pins/{it['id']}.jpg")
        if ids and it["id"] not in ids:
            continue
        if not ids and not force and os.path.exists(dst):
            continue
        todo.append((i, it, dst))
    if not todo:
        print("Keine Pins zu rendern (vorhandene werden übersprungen, --force rendert alle neu).")
        return
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for i, it, dst in todo:
            pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{render(i, it)}</body></html>")
            pg.wait_for_timeout(150)
            over = pg.evaluate("document.querySelector('.p').scrollHeight") > 1500
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            pg.screenshot(path=dst, type="jpeg", quality=85)
            print(it["id"], "->", os.path.relpath(dst, S.ROOT), "WARNUNG: Text zu lang, läuft über" if over else "")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])
