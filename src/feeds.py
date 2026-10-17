# RSS-Feeds für Pinterest-Autopublish (ein Feed pro Board). Einträge in src/feeds.json.
# Neue Pins: Eintrag in feeds.json ergänzen (id eindeutig, link auf solovorlagen.de, image = Pin-Bild 1000x1500),
# date = geplanter Veröffentlichungszeitpunkt (UTC, ISO). Der Workflow .github/workflows/feeds.yml baut täglich neu.
# python3 src/gen_site.py, committen, pushen. Pinterest holt neue Einträge täglich ab.
import json, os, html as _h, datetime as _dt, email.utils as _eu
_HERE=os.path.dirname(os.path.abspath(__file__)); _OUT=os.path.join(_HERE,"..","docs")
FEEDS={"kleinunternehmer-tipps":"Kleinunternehmer Tipps","preise-und-geld":"Selbstständig: Preise & Geld","excel-vorlagen":"Excel-Vorlagen für Selbstständige"}
_items=json.load(open(os.path.join(_HERE,"feeds.json"),encoding="utf-8"))
os.makedirs(os.path.join(_OUT,"feeds"),exist_ok=True)
for slug,board in FEEDS.items():
    _now=_dt.datetime.now(_dt.timezone.utc).replace(tzinfo=None)
    # nur fällige Einträge (date <= jetzt) – so lassen sich Pins vorausplanen; der tägliche GitHub-Workflow baut die Feeds neu
    its=sorted([i for i in _items if i["board"]==board and _dt.datetime.fromisoformat(i["date"])<=_now],key=lambda i:i["date"],reverse=True)
    x=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">','<channel>',
       f'<title>Solovorlagen – {_h.escape(board)}</title>','<link>https://solovorlagen.de/</link>',
       f'<atom:link href="https://solovorlagen.de/feeds/{slug}.xml" rel="self" type="application/rss+xml"/>',
       f'<description>{_h.escape(board)}: Tipps, Rechner und Vorlagen für Selbstständige und Kleinunternehmer.</description>','<language>de-de</language>']
    for i in its:
        img=os.path.join(_OUT,i["image"].replace("https://solovorlagen.de/",""))
        size=os.path.getsize(img) if os.path.exists(img) else 0
        d=_dt.datetime.fromisoformat(i["date"]).replace(tzinfo=_dt.timezone.utc)
        x+=['<item>',f'<title>{_h.escape(i["title"])}</title>',f'<link>{_h.escape(i["link"])}</link>',f'<guid isPermaLink="false">solovorlagen-{i["id"]}</guid>',
            f'<pubDate>{_eu.format_datetime(d)}</pubDate>',f'<description>{_h.escape(i["description"])}</description>',
            f'<enclosure url="{i["image"]}" length="{size}" type="image/jpeg"/>',f'<media:content url="{i["image"]}" medium="image" type="image/jpeg" width="1000" height="1500"/>','</item>']
    x+=['</channel>','</rss>']
    open(os.path.join(_OUT,"feeds",slug+".xml"),"w",encoding="utf-8").write("\n".join(x)+"\n")
print("feeds ok", {s:sum(1 for i in _items if i["board"]==b) for s,b in FEEDS.items()})
