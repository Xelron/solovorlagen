# -*- coding: utf-8 -*-
"""RSS-Feeds für Pinterest-Autopublish – ein Feed pro Board (docs/feeds/<slug>.xml).

Boards stehen in config.json unter pinterest.boards, die Pins in content/feeds.json:
  {"id": "pin-01", "board": "<Board-Name oder -Slug>", "title": "...", "description": "...",
   "link": "seite.html#anker", "image": "pins/pin-01.jpg", "date": "2026-11-01T07:00:00",
   "pin": {"h1": "...", "h2": "...", "sub": "...", "img": "img/produkt.jpg"}}   <- "pin" nur für src/pins.py
link/image dürfen relativ sein (werden zu https://<domain>/...). date = geplante Veröffentlichung in UTC.
Es landen nur fällige Einträge (date <= jetzt, UTC) im Feed – so lassen sich Pins vorausplanen.
Der Workflow .github/workflows/feeds.yml baut die Feeds täglich neu; Pinterest holt sie selbst ab.
"""
import datetime as dt, email.utils, html, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitekit as S
from sitekit import CFG, B, OUT, abs_url

FEEDS_JSON = os.path.join(S.CONTENT, "feeds.json")


def load_items():
    if not os.path.exists(FEEDS_JSON):
        return []
    return json.load(open(FEEDS_JSON, encoding="utf-8"))


def build(now=None):
    boards = CFG.get("pinterest", {}).get("boards", [])
    items = load_items()
    now = now or dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    os.makedirs(os.path.join(OUT, "feeds"), exist_ok=True)
    stats = {}
    known = {b["name"] for b in boards} | {b["slug"] for b in boards}
    for i in items:
        if i.get("board") not in known:
            print(f"WARNUNG feeds.json: Eintrag {i.get('id')} hat unbekanntes Board '{i.get('board')}'")
    for b in boards:
        mine = [i for i in items if i.get("board") in (b["name"], b["slug"])]
        due = sorted([i for i in mine if dt.datetime.fromisoformat(i["date"]) <= now], key=lambda i: i["date"], reverse=True)
        x = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">', "<channel>",
             f"<title>{html.escape(B['name'])} – {html.escape(b['name'])}</title>", f"<link>{S.BASE}</link>",
             f'<atom:link href="{abs_url("feeds/" + b["slug"] + ".xml")}" rel="self" type="application/rss+xml"/>',
             f"<description>{html.escape(b.get('description') or b['name'])}</description>",
             f"<language>{S.LANG_TAG.lower()}</language>"]
        for i in due:
            img_url = abs_url(i.get("image") or f"pins/{i['id']}.jpg")
            local = os.path.join(OUT, img_url.replace(S.BASE, "", 1)) if img_url.startswith(S.BASE) else ""
            size = os.path.getsize(local) if local and os.path.exists(local) else 0
            mime = "image/png" if img_url.lower().endswith(".png") else "image/jpeg"
            d = dt.datetime.fromisoformat(i["date"]).replace(tzinfo=dt.timezone.utc)
            x += ["<item>", f"<title>{html.escape(i['title'])}</title>", f"<link>{html.escape(abs_url(i['link']))}</link>",
                  f'<guid isPermaLink="false">{html.escape(S.DOMAIN)}-{html.escape(i["id"])}</guid>',
                  f"<pubDate>{email.utils.format_datetime(d)}</pubDate>",
                  f"<description>{html.escape(i.get('description', ''))}</description>",
                  f'<enclosure url="{img_url}" length="{size}" type="{mime}"/>',
                  f'<media:content url="{img_url}" medium="image" type="{mime}" width="1000" height="1500"/>', "</item>"]
        x += ["</channel>", "</rss>"]
        with open(os.path.join(OUT, "feeds", b["slug"] + ".xml"), "w", encoding="utf-8") as f:
            f.write("\n".join(x) + "\n")
        stats[b["slug"]] = f"{len(due)}/{len(mine)} fällig"
    print("feeds ok", stats)


if __name__ == "__main__":
    build()
