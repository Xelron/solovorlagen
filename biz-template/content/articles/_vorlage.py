# -*- coding: utf-8 -*-
"""Vorlage für einen Artikel als Python-Modul – sinnvoll, wenn der Text berechnete Tabellen
oder viel eigenes HTML braucht. Kopieren nach content/articles/<adresse>.py (ohne Unterstrich).

META hat dieselben Felder wie das Front Matter der Markdown-Artikel.
Statt BODY kann das Modul auch eine Funktion body(site) definieren; `site` ist das Modul
src/sitekit.py (site.esc, site.money, site.CFG, site.nb …).
"""
META = {
    "title": "Titel des Artikels",
    "description": "Ein Satz für Google und die Übersicht.",
    "date": "2026-01-31",
    "updated": "2026-01-31",
    "eyebrow": "Ratgeber",
    "answer": "Kurzantwort in zwei Sätzen.",
    "cta_product": "starter-vorlage",
    "draft": True,
    "faq": [("Frage?", "Antwort.")],
    "sources": [("Name der Quelle", "https://example.com/quelle")],
}


def body(site):
    rows = "".join(f"<tr><td>{n}</td><td>{site.money(n * 12)}</td></tr>" for n in (1, 5, 10))
    return f"""<h2 class="serif" id="tabelle">Berechnete Tabelle</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Menge</th><th>Preis</th></tr>{rows}</table></div>"""
