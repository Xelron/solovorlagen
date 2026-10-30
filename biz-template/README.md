# Vorlage für Online-Businesses (statische Website auf GitHub Pages)

Mit dieser Vorlage baust du die Website für ein kleines Online-Business mit digitalen Produkten:
Startseite, Produktseiten mit Kauf-Button, Ratgeber-Artikel, kostenlose Web-Rechner, Impressum und
Datenschutz, sitemap.xml, robots.txt, llms.txt, Pinterest-RSS-Feeds und IndexNow-Meldung.
Alles läuft als statische Seite auf GitHub Pages – kein Server, keine Datenbank, keine laufenden Kosten
außer der Domain.

Alles Markenspezifische steht in **einer** Datei: `config.json`.
Werte in `[[DOPPELTEN ECKIGEN KLAMMERN]]` sind **Platzhalter**. Sie erscheinen auf der Seite gelb
markiert und `gen_site.py` listet sie nach jedem Build auf. **Solange Platzhalter übrig sind, nicht live schalten.**
Texte mit `BEISPIEL` sind Demo-Inhalte und werden durch eigene ersetzt.

## Aufbau

```
config.json              Marke, Domain, Farben, Logo, Betreiber (Impressum), Navigation,
                         Startseite, Produkte, FAQ, Pinterest-Boards, IndexNow-Schlüssel
new_business.py          legt aus der Vorlage ein neues Business an
src/
  gen_site.py            baut alles nach docs/  ← der eine Build-Befehl
  sitekit.py             Seitengerüst (Header/Footer), Logo-SVG, JSON-LD-Helfer, CSS-Variablen
  content.py             sammelt Artikel und Rechner aus content/, baut Übersichten,
                         sitemap.xml, robots.txt, llms.txt
  mdlite.py              kleiner Markdown-Konverter (ohne Abhängigkeiten)
  feeds.py               Pinterest-RSS-Feeds (nur fällige Pins nach UTC-Datum)
  pins.py                Pin-Grafiken 1000×1500 (Playwright)
  qa.py                  Layout-QA bei 390/820/1280 px + Prüfung toter Links (Playwright)
  style.css              Stylesheet; Farben/Schriften kommen als CSS-Variablen aus config.json
content/
  articles/*.md|*.py     Ratgeber-Artikel (Dateien mit _ am Anfang werden ignoriert)
  articles/_vorlage.md   Vorlage für neue Artikel (Markdown)
  articles/_vorlage.py   Vorlage für Artikel als Python (für berechnete Tabellen/viel HTML)
  tools/*.py             Web-Rechner, je Datei eine Seite
  feeds.json             geplante Pins für die Pinterest-Feeds
docs/                    fertige Website (wird von GitHub Pages ausgeliefert)
  img/                   eigene Produktbilder hier ablegen (JPG/PNG, quadratisch 1000×1000)
  pins/                  Pin-Grafiken
  CNAME                  Domain für GitHub Pages
  <schlüssel>.txt        IndexNow-Schlüsseldatei
.github/workflows/
  feeds.yml              baut täglich die Feeds neu und committet fällige Pins
  indexnow.yml           meldet nach jedem Push die URLs aus der Sitemap an IndexNow
```

`docs/` wird bei jedem Build neu geschrieben – dort nichts von Hand ändern, außer Bilder in
`docs/img/` und `docs/pins/` abzulegen.

## Build-Befehle

```bash
python3 src/gen_site.py      # komplette Seite + Feeds nach docs/ bauen (nur Python 3.9+, keine Pakete nötig)
python3 src/pins.py          # fehlende Pin-Grafiken aus content/feeds.json rendern (--force: alle neu)
python3 src/qa.py            # Layout-QA aller Seiten; --shot datei.png speichert die Startseite bei 390 px
python3 -m http.server -d docs 8000   # lokal ansehen: http://localhost:8000
```

Optional: `pip install pillow` (WebP-Varianten der Produktbilder, PNG-Favicons, Open-Graph-Bild
`img/og.png`) und `pip install playwright && playwright install chromium` (für `pins.py` und `qa.py`).
Ohne diese Pakete baut `gen_site.py` trotzdem alles; es fehlen dann nur die genannten Extras.

## Neues Business anlegen

1. **Anlegen**
   ```bash
   python3 new_business.py ../gartenplaner --name "Gartenplaner" --domain gartenplaner.de \
       --claim "Beete planen ohne Rätselraten" --primary "#2F5D3A" --accent "#D9822B" --git
   ```
   Das kopiert die Vorlage, trägt Name, Domain, Claim, Logo-Buchstabe und Farben in `config.json` ein,
   erzeugt den IndexNow-Schlüssel (`config.json` + `docs/<schlüssel>.txt`), schreibt `docs/CNAME`,
   baut die Seite einmal und macht `git init`. Es wird nichts gepusht.
2. **config.json durchgehen** – von oben nach unten:
   - `brand`: Beschreibung, Footer-Text, Sprache
   - `colors`, `fonts`, `logo`: Aussehen (Logo = Buchstabe + bis zu drei Punkte)
   - `operator`: **Betreiberdaten fürs Impressum** – siehe unten, nur der Inhaber trägt sie ein
   - `checkout`: Zahlungsanbieter (Standard Digistore24) und Texte am Kauf-Button
   - `nav`, `nav_cta`, `home`, `faq`: Navigation, Startseite, allgemeine FAQ
   - `products`: je Produkt Name, `slug` (= Adresse `slug.html`), Preis, `checkout_url`
     (leer = „Bald verfügbar“), `image` und `shots` (Dateinamen in `docs/img/`), Lead, Features, FAQ.
     Optional `compare_price` (durchgestrichener Preis) und `includes` (Liste von Slugs → Paket-Seite
     mit „Im Paket enthalten“)
   - `ratgeber`, `rechner`: Überschriften der Übersichtsseiten, Hinweistext unter Artikeln
   - `pinterest.boards`: ein Feed pro Board (`slug` = Dateiname `feeds/<slug>.xml`, `name` = Board-Name);
     `domain_verify` = Code aus der Pinterest-Website-Bestätigung
3. **Demo-Inhalte ersetzen**: `content/articles/beispiel-ratgeber.md` und `content/tools/prozent-rechner.py`
   löschen oder umschreiben, `content/feeds.json` leeren oder mit eigenen Pins füllen.
4. `python3 src/gen_site.py` – am Ende darf **keine Platzhalter-Warnung** mehr kommen.
   Dann `python3 src/qa.py`.
5. Committen und zu GitHub pushen (siehe einmalige Handgriffe).

### Neuen Artikel hinzufügen

`content/articles/_vorlage.md` nach `content/articles/<adresse>.md` kopieren, Metadaten ausfüllen
(`title`, `description`, `date` sind Pflicht; `updated`, `answer` (Kurzantwort-Kasten), `faq`,
`sources`, `cta_product`, `eyebrow`, `card_text`, `llms`, `draft` optional), Text in Markdown schreiben.
Der Generator trägt den Artikel automatisch in Ratgeber-Übersicht, `sitemap.xml` und `llms.txt` ein
und erzeugt Article-, FAQPage- und Breadcrumb-Daten. Unterstütztes Markdown: `##`/`###` mit
optionalem Anker `{#anker}`, Absätze, **fett**, *kursiv*, Links, Listen, Tabellen, `>` für den
hervorgehobenen Kasten; Zeilen, die mit `<` beginnen, sind rohes HTML.

Für Artikel mit berechneten Tabellen: `_vorlage.py` kopieren (Modul mit `META` und `body(site)`).

### Neuen Rechner hinzufügen

Datei in `content/tools/` nach dem Muster von `prozent-rechner.py` anlegen: `META` (Metadaten),
`BODY` (HTML-Formular mit Klasse `calc`), `EXPLAIN` (Erklärung daneben), `SCRIPT` (JavaScript; die
Helfer `$`, `num`, `eur`, `fmt`, `light`, `esc`, `copy` sind schon da). Er erscheint automatisch auf
der Startseite, in der Rechner-Übersicht, in der Sitemap und in `llms.txt`. Gibt es keinen Rechner,
entfällt `rechner.html`; dann den Eintrag „Rechner“ aus `nav` in `config.json` nehmen.

### Pins planen

Eintrag in `content/feeds.json` ergänzen: eindeutige `id`, `board` (Name oder Slug aus der config),
`title`, `description`, `link` (relativ, z. B. `artikel.html#anker`), `date` (geplanter Zeitpunkt, UTC)
und ein Block `pin` mit dem Text für die Grafik (`h1`, `h2`, `sub`, `style`: `text` | `img` | `price` | `list`).
`python3 src/pins.py` rendert `docs/pins/<id>.jpg`, `python3 src/gen_site.py` baut die Feeds, committen, pushen.
Der Workflow `feeds.yml` nimmt jeden Tag die fällig gewordenen Pins in die Feeds auf; Pinterest holt sie selbst ab.

## Einmalige Handgriffe des Inhabers

Diese Schritte kann nur der Inhaber erledigen (Konten, Verträge, persönliche Daten):

1. **Impressum-Daten eintragen** in `config.json` → `operator`: Name, ggf. Firmenname, Straße,
   PLZ/Ort, E-Mail (Pflicht), optional Telefon und USt-ID, außerdem die für das eigene Bundesland
   zuständige Datenschutz-Aufsichtsbehörde mit Anschrift (`supervisory_authority`) und `legal_stand`.
   Nie erfundene Daten eintragen. Impressum und Datenschutzerklärung sind eine Vorlage für den
   typischen Fall (GitHub Pages, keine Cookies, kein Tracking, Verkauf über einen Reseller) – bei
   Newsletter, Analyse-Tools oder eingebetteten Inhalten muss die Datenschutzerklärung ergänzt werden.
   Im Zweifel rechtlich prüfen lassen.
2. **Domain kaufen** und beim Domain-Anbieter die DNS-Einträge setzen:
   - 4 A-Records für die Domain selbst (`@`):
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - CNAME `www` → `<github-benutzer>.github.io`
   - vorhandene andere A-/AAAA-Records für `@` (z. B. Parkseite des Anbieters) entfernen
3. **GitHub-Repository** anlegen (öffentlich, oder privat mit passendem Tarif), Code pushen.
   Unter *Settings → Pages*: Source „Deploy from a branch“, Branch `main`, Ordner **`/docs`**.
   Custom domain = die Domain aus `config.json` (steht schon in `docs/CNAME`), nach der DNS-Prüfung
   **Enforce HTTPS** aktivieren. Empfohlen: Domain unter *Settings → Pages → Verified domains* im
   GitHub-Profil bestätigen.
4. **GitHub Actions**: *Settings → Actions → General → Workflow permissions* auf „Read and write“
   stellen, damit `feeds.yml` die Feeds committen kann.
5. **Konten**: Zahlungsanbieter (z. B. Digistore24) – Produkte anlegen und die Checkout-URLs in
   `products[].checkout_url` eintragen; Pinterest-Unternehmenskonto – Website bestätigen
   (`pinterest.domain_verify`), Boards wie in `pinterest.boards` anlegen und je Board den Feed
   `https://<domain>/feeds/<slug>.xml` unter „Massenerstellung von Pins / RSS-Feeds“ verbinden;
   optional Google Search Console und Bing Webmaster Tools (Sitemap `https://<domain>/sitemap.xml` einreichen).
6. Geschäftliche Pflichten (Gewerbeanmeldung, Steuer) klärt der Inhaber selbst.

## Prüfliste vor dem Livegang

- `python3 src/gen_site.py` meldet keine Platzhalter mehr, keine `BEISPIEL`-Texte mehr auf der Seite
  (`grep -l BEISPIEL docs/*.html`)
- eigene Produktbilder in `docs/img/` (sonst erscheinen Platzhalterbilder)
- Checkout-Links getestet
- `python3 src/qa.py` → „QA ok“
- `docs/CNAME` und `docs/<indexnow_key>.txt` vorhanden
