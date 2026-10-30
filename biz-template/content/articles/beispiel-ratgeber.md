---
title: Beispiel-Ratgeber: So ist ein Artikel aufgebaut
description: BEISPIEL-ARTIKEL – zeigt alle Bausteine eines Ratgebers: Kurzantwort, Zwischenüberschriften, Liste, Tabelle, Produkt-Hinweis, FAQ und Quellen. Vor dem Livegang löschen oder ersetzen.
date: 2026-10-30
updated: 2026-10-30
eyebrow: Ratgeber · Beispiel
answer: Ein guter Ratgeber beantwortet **eine konkrete Frage** gleich im ersten Absatz, erklärt dann die Details mit Beispielen und nennt seine Quellen. Diese Datei zeigt, wie das in Markdown aussieht.
cta_product: starter-vorlage
card_text: BEISPIEL: Aufbau eines Artikels mit Kurzantwort, Tabelle, FAQ und Quellen.
llms: BEISPIEL-Artikel, der den Aufbau eines Ratgebers zeigt (Kurzantwort, Abschnitte, Tabelle, FAQ, Quellen).
faq:
  - q: Wo lege ich neue Artikel ab?
    a: Als Markdown-Datei (.md) oder Python-Datei (.py) im Ordner content/articles/. Der Dateiname wird zur Adresse, z. B. mein-thema.md wird zu mein-thema.html.
  - q: Muss ich die Ratgeber-Übersicht oder die Sitemap anpassen?
    a: Nein. gen_site.py sammelt alle Artikel automatisch ein und trägt sie in Ratgeber-Übersicht, sitemap.xml und llms.txt ein.
sources:
  - title: Google Search Central – Hilfreiche, zuverlässige Inhalte erstellen
    url: https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=de
  - title: schema.org – FAQPage
    url: https://schema.org/FAQPage
---
## Worum geht es? {#worum}

BEISPIEL-TEXT: Hier beschreibst du in zwei, drei Sätzen das Problem deiner Leserinnen und Leser. Bleib konkret: Welche Frage stellen sie sich, und wann?

## Die Bausteine im Überblick {#bausteine}

- **Metadaten** oben zwischen den drei Strichen: Titel, Beschreibung, Datum, FAQ, Quellen
- **Kurzantwort** (`answer:`) erscheint hervorgehoben direkt unter der Überschrift
- **Abschnitte** mit `##` und optionalem Anker `{#anker}` für Direktlinks, z. B. aus Pins
- **Produkt-Hinweis** über `cta_product:` mit dem Slug eines Produkts aus config.json

### Beispieltabelle

| Baustein | Pflicht | Wofür |
|---|---|---|
| title | ja | Überschrift, Seitentitel, Übersicht |
| description | ja | Meta-Beschreibung und Übersichtskarte |
| date | ja | Veröffentlichung, Sitemap, strukturierte Daten |
| faq | nein | FAQ-Abschnitt und FAQPage-Daten |
| sources | nein | Quellenliste am Ende |

## Rechenbeispiel {#beispiel}

> BEISPIEL: Ein Zitatblock mit > wird als hervorgehobener Kasten gesetzt – gut für Rechenbeispiele oder das Ergebnis eines Abschnitts.

Für alles, was Markdown nicht kann, darfst du rohes HTML verwenden: Jede Zeile, die mit `<` beginnt, wird unverändert übernommen.

<p class="note">Dieser Absatz ist rohes HTML mit der Klasse „note“.</p>
