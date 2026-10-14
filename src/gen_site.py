import html, json, os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,"..","docs")
# Digistore24 product IDs (None = noch nicht angelegt)
DS=json.load(open(os.path.join(HERE,"ds24.json")))
P=[
dict(slug="paket",name="Selbstständigen-Paket",short="Alle 5 Vorlagen zum halben Preis",price="35 €",img="bundle-01.jpg",shots=[],
 eyebrow="Alle 5 Excel-Vorlagen · 50 % gespart",h1="Das komplette Paket für Kleinunternehmer und Freelancer",
 lead="Alle fünf Solovorlagen in einem Download – für 35 € statt 70 €. Preise festlegen, Rechnungen schreiben, Umsatzgrenzen im Blick behalten und die Steuererklärung vorbereiten.",
 content="Ein ZIP mit 5 Ordnern: Kleinunternehmer-Cockpit, Rechnungs-Generator, Stundensatz-Rechner, Fahrtenbuch, Anlagenverzeichnis & AfA-Rechner – jeweils Excel-Vorlage (.xlsx) plus PDF-Kurzanleitung",
 feats=[]),
dict(slug="cockpit",name="Kleinunternehmer-Cockpit",short="Umsatzgrenzen-Ampel, Einnahmen, Ausgaben, EÜR",price="19 €",img="produkt.jpg",shots=["cockpit.jpg","euer.jpg","monate.jpg"],
 eyebrow="Excel-Vorlage zum Download · für Kleinunternehmer",h1="Weißt du, wie nah du an der Umsatzgrenze bist?",
 lead="Seit 2025 endet die Kleinunternehmerregelung sofort, wenn du im laufenden Jahr 100.000 € überschreitest – und ab 25.000 € im Vorjahr fällt sie im Folgejahr weg. Das Cockpit zeigt dir mit einer Ampel, wo du stehst. Dazu Einnahmen, Ausgaben, EÜR-Übersicht und Steuerrücklage.",
 content="5 verknüpfte Tabellenblätter: Start (Einstellungen & Anleitung), Cockpit mit Umsatzgrenzen-Ampel, EÜR-Übersicht, Einnahmen, Ausgaben",
 feats=[("Umsatzgrenzen-Ampel","Zeigt, wie viel der 100.000-€-Grenze ausgeschöpft ist, rechnet aufs Jahr hoch und warnt vor der 25.000-€-Grenze fürs Folgejahr."),
 ("Cockpit mit Monatsübersicht","Einnahmen, Ausgaben, Gewinn und kumulierter Umsatz für jeden Monat, dazu ein Diagramm."),
 ("EÜR-Übersicht","Summen nach 17 Kategorien – die Grundlage für die Anlage EÜR in ELSTER."),
 ("Steuerrücklage","Legt automatisch einen Anteil deines Gewinns als Rücklage beiseite.")]),
dict(slug="rechnung",name="Rechnungs-Generator",short="Rechnungen mit Pflichtangaben, offene Posten, Mahnung",price="15 €",img="rechnung-01.jpg",shots=["rechnung-02.jpg","rechnung-03.jpg"],
 eyebrow="Excel-Vorlage zum Download · für Kleinunternehmer",h1="Rechnungen ohne Formfehler – und immer wissen, wer noch zahlen muss",
 lead="Der Rechnungs-Generator erstellt Rechnungen mit allen Pflichtangaben für Kleinunternehmer und dem Hinweis nach § 19 UStG, vergibt fortlaufende Nummern und behält deine offenen Rechnungen im Blick. Für Säumige gibt es eine fertige Zahlungserinnerung.",
 content="6 Tabellenblätter: Start, Kunden, Rechnungsbuch, Positionen, Rechnung (druckfertig), Zahlungserinnerung",
 feats=[("Alle Pflichtangaben","Nach § 34a UStDV für Kleinunternehmer inklusive § 19-Hinweis – plus Rechnungsnummer und Leistungszeitraum."),
 ("Fortlaufende Nummern","Die nächste freie Nummer wird angezeigt, doppelte Nummern werden markiert."),
 ("Rechnungsbuch","Status Offen, Überfällig oder Bezahlt automatisch – mit Summe der offenen Posten."),
 ("Zahlungserinnerung","Überfällige Rechnung auswählen – der freundliche Brief mit neuer Frist ist fertig.")]),
dict(slug="stundensatz",name="Stundensatz-Rechner",short="Was du verlangen musst, damit es reicht",price="12 €",img="stundensatz-01.jpg",shots=["stundensatz-02.jpg","stundensatz-03.jpg"],
 eyebrow="Excel-Vorlage zum Download · für Selbstständige",h1="Was musst du pro Stunde verlangen?",
 lead="Viele Selbstständige rechnen zu niedrig, weil sie Krankenversicherung, Altersvorsorge, Urlaub, Krankheit und unbezahlte Arbeitszeit vergessen. Der Stundensatz-Rechner nimmt alles mit und zeigt dir deinen realistischen Stunden- und Tagessatz.",
 content="4 Tabellenblätter: Start, Rechner, Szenarien, Projekt-Kalkulation",
 feats=[("Realistischer Stundensatz","Mit Versicherungen, Altersvorsorge, Betriebskosten, Steuern und Puffer."),
 ("Echte Arbeitszeit","Urlaub, Feiertage, Krankheit, Fortbildung und der Anteil abrechenbarer Stunden."),
 ("Wohin dein Geld geht","Aufschlüsselung jeder Stunde – du siehst, warum der Satz so hoch sein muss."),
 ("Szenarien & Angebote","Stundensatz für verschiedene Ziele vergleichen und Projektpreise kalkulieren.")]),
dict(slug="fahrtenbuch",name="Fahrtenbuch & Fahrtkosten-Rechner",short="Fahrtkosten automatisch, Sätze 2026",price="12 €",img="fahrten-01.jpg",shots=["fahrten-02.jpg","fahrten-03.jpg"],
 eyebrow="Excel-Vorlage zum Download · Stand 2026",h1="Jede betriebliche Fahrt zählt – wenn du sie sauber aufschreibst",
 lead="Mit dem Privatauto zum Kunden oder ins Büro? Das Fahrtenbuch erfasst alle nötigen Angaben, rechnet mit 0,30 € pro km für Dienstfahrten und der Entfernungspauschale von 0,38 € und warnt bei Lücken im km-Stand.",
 content="3 Tabellenblätter: Start (Einstellungen), Fahrten, Auswertung",
 feats=[("Alle Angaben","Datum, Start, Ziel, Zweck, km-Stand und Kennzeichen."),
 ("Richtige Sätze 2026","0,30 €/km für Dienstfahrten, 0,38 € Entfernungspauschale – automatisch nur einmal pro Tag."),
 ("Automatische Prüfung","Warnt bei Lücken zum letzten km-Stand und unlogischen Werten."),
 ("Fertig für die EÜR","Monatsübersicht und Gesamtbetrag der Fahrtkosten.")]),
dict(slug="afa",name="Anlagenverzeichnis & AfA-Rechner",short="Sofort absetzen oder abschreiben?",price="12 €",img="afa-01.jpg",shots=["afa-02.jpg","afa-03.jpg"],
 eyebrow="Excel-Vorlage zum Download · Stand 2026",h1="Sofort absetzen oder abschreiben? Die Vorlage rechnet es aus",
 lead="Laptop, Schreibtisch, Kamera: Das Anlagenverzeichnis entscheidet anhand der aktuellen Grenzen automatisch zwischen Sofortabzug, GWG, Sammelposten und Abschreibung – und rechnet monatsgenau inklusive Restbuchwert.",
 content="4 Tabellenblätter: Start, Anlagen, Übersicht, Kategorien",
 feats=[("Automatische Entscheidung","Sofortabzug bis 250 €, GWG bis 800 €, Sammelposten oder lineare AfA."),
 ("1-Jahres-Regel","Für Computerhardware und Software."),
 ("Monatsgenaue AfA","Abschreibung und Restbuchwert zum 31.12. für jedes Wirtschaftsgut."),
 ("Prüfungen","Warnt bei unzulässigem Sammelposten oder fehlender Nutzungsdauer.")]),
]
BY={p["slug"]:p for p in P}
def buy(p,cls="btn",label=None):
    pid=DS.get(p["slug"])
    if pid: return f'<a class="{cls}" href="https://www.checkout-ds24.com/product/{pid}">{label or "Jetzt kaufen – "+p["price"]}</a>'
    return f'<span class="{cls} soon" aria-disabled="true">Bald verfügbar</span>'
CSS=open(os.path.join(HERE,"style.css")).read()
def page(title,desc,body,path,head=""):
    h=f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="style.css">
<link rel="canonical" href="https://solovorlagen.de/{"" if path=="index.html" else path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://solovorlagen.de/{"" if path=="index.html" else path}">
<meta property="og:locale" content="de_DE">
<meta name="p:domain_verify" content="6619a1c3e96181cb258971813ee2eca4"/>
{head}
</head>
<body>
<header><div class="wrap">
<a class="brand serif" href="index.html">Solovorlagen</a>
<nav><a href="index.html#vorlagen">Vorlagen</a><a href="paket.html">Paket</a><a href="grenzen-check.html">Grenzen-Check</a><a href="ratgeber.html">Ratgeber</a></nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<span>© 2026 Solovorlagen · Felix Merklinger-Lötzsch</span>
<nav><a href="grenzen-check.html">Kostenloser Grenzen-Check</a><a href="ratgeber.html">Ratgeber</a><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a><a href="mailto:hallo@solovorlagen.de">hallo@solovorlagen.de</a></nav>
</div></footer>
</body>
</html>
"""
    open(os.path.join(OUT,path),"w").write(h)
FAQ="""<section class="band"><div class="wrap faq">
<h2 class="serif">Häufige Fragen</h2>
<h3>Wie bekomme ich die Datei?</h3><p>Direkt nach der Zahlung über den Download-Link auf der Bestätigungsseite und zusätzlich per E-Mail von Digistore24.</p>
<h3>Funktioniert das mit Google Sheets oder auf dem Mac?</h3><p>Ja. Die Vorlagen sind normale Excel-Dateien (.xlsx) und laufen in Microsoft Excel (Windows und Mac), Google Sheets und LibreOffice.</p>
<h3>Ersetzen die Vorlagen eine Steuerberatung?</h3><p>Nein. Sie verschaffen dir Überblick und nehmen dir Rechnerei ab. Bei Fragen zu deiner persönlichen Situation hilft eine Steuerberatung. Excel-Tabellen sind nicht GoBD-zertifiziert.</p>
<h3>Auf welchem Stand sind die Regeln?</h3><p>Stand 2026. Grenzwerte und Sätze stehen jeweils in eigenen Feldern und lassen sich bei Gesetzesänderungen anpassen.</p>
<h3>Ich habe eine Frage.</h3><p>Schreib an <a href="mailto:hallo@solovorlagen.de">hallo@solovorlagen.de</a>.</p>
</div></section>"""
def card(p):
    return f"""<a class="pcard" href="{p['slug']}.html"><img src="img/{p['img']}" width="1000" height="1000" alt="Produktbild {html.escape(p['name'])}" loading="lazy">
<div class="pbody"><h3>{html.escape(p['name'])}</h3><p>{html.escape(p['short'])}</p><div class="prow"><span class="price">{p['price']}</span><span class="more">Ansehen →</span></div></div></a>"""
# ---- index
singles=[p for p in P if p["slug"]!="paket"]
idx=f"""<div class="wrap hero">
<div>
<p class="eyebrow">Excel-Vorlagen zum Download · Stand 2026</p>
<h1 class="serif">Klare Zahlen für Solo-Selbstständige</h1>
<p class="lead">Fertige Excel-Vorlagen für Kleinunternehmer und Freelancer in Deutschland: Umsatzgrenzen im Blick behalten, Rechnungen schreiben, Stundensatz kalkulieren, Fahrtkosten und Abschreibungen berechnen. Einmal kaufen, sofort herunterladen, kein Abo.</p>
<a class="btn" href="#vorlagen">Vorlagen ansehen</a> <a class="btn" style="background:#1F3A5F" href="grenzen-check.html">Kostenloser Grenzen-Check</a>
<p class="note">Digitale Downloads · läuft in Excel, Google Sheets und LibreOffice</p>
</div>
<div><a href="paket.html" class="bundle">
<img src="img/bundle-01.jpg" width="1000" height="1000" alt="Selbstständigen-Paket: alle 5 Vorlagen für 35 Euro statt 70 Euro">
</a></div>
</div>
<section class="band" id="vorlagen"><div class="wrap">
<h2 class="serif">Die Vorlagen</h2>
<p class="sub2">Jede Vorlage löst ein konkretes Problem – und rechnet alles Wichtige automatisch.</p>
<div class="pgrid">{''.join(card(p) for p in singles)}
<a class="pcard pbundle" href="paket.html"><div class="pbody"><p class="eyebrow" style="color:#cfe0f0">Alle 5 zusammen</p><h3 style="color:#fff;font-size:24px;hyphens:auto;overflow-wrap:break-word">Selbstständigen-Paket</h3>
<p style="color:#dbe6f0">Alle Vorlagen in einem Download – du sparst die Hälfte.</p><div class="prow"><span class="price" style="color:#fff">35 € <s style="font-size:16px;opacity:.7">70 €</s></span><span class="more" style="color:#fff">Ansehen →</span></div></div></a>
</div></div></section>
<section><div class="wrap">
<h2 class="serif">Warum Solovorlagen?</h2>
<div class="grid3">
<div class="feat"><h3>Echte Probleme</h3><p>Jede Vorlage beantwortet eine Frage, die sich Selbstständige wirklich stellen – vom Stundensatz bis zur Abschreibung.</p></div>
<div class="feat"><h3>Sofort einsatzbereit</h3><p>Gelbe Felder ausfüllen, fertig. Jede Vorlage hat ein Startblatt mit Anleitung und Beispielwerten.</p></div>
<div class="feat"><h3>Kein Abo</h3><p>Einmal kaufen, dauerhaft nutzen. Deine Daten bleiben auf deinem Rechner.</p></div>
</div></div></section>
{FAQ}"""
page("Solovorlagen – Excel-Vorlagen für Selbstständige & Kleinunternehmer","Excel-Vorlagen für Kleinunternehmer und Freelancer: Umsatzgrenzen-Ampel, Rechnungs-Generator, Stundensatz-Rechner, Fahrtenbuch, AfA-Rechner. Sofort-Download, kein Abo.",idx,"index.html")
# ---- product pages
for p in P:
    rows=[("Produkt",p["name"]+" – Excel-Vorlage" if p["slug"]!="paket" else "Selbstständigen-Paket – 5 Excel-Vorlagen"),
          ("Art","Digitales Produkt zum Herunterladen. Kein Versand, keine Software-Installation, kein Abo."),
          ("Format","ZIP-Datei mit Excel-Vorlage (.xlsx) und PDF-Kurzanleitung, Sprache Deutsch. Läuft in Microsoft Excel, Google Sheets und LibreOffice." if p["slug"]!="paket" else "ZIP-Datei mit 5 Ordnern, jeweils Excel-Vorlage (.xlsx) und PDF-Kurzanleitung. Sprache Deutsch."),
          ("Inhalt",p["content"]),("Lieferung","Download-Link sofort nach der Zahlung, zusätzlich per E-Mail von Digistore24"),
          ("Preis",f"<strong>{p['price']} einmalig</strong>"+(" (statt 70 € einzeln)" if p["slug"]=="paket" else "")),
          ("Für wen","Selbstständige, Freelancer und Kleinunternehmer in Deutschland")]
    tbl="".join(f"<tr><th>{k}</th><td>{v if k=='Preis' else html.escape(v)}</td></tr>" for k,v in rows)
    shots="".join(f'<img src="img/{s}" width="1000" height="1000" alt="Beispielansicht {html.escape(p["name"])}" loading="lazy">' for s in p["shots"])
    feats="".join(f'<div class="feat"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t,d in p["feats"])
    extra=""
    if p["slug"]=="paket":
        extra='<section><div class="wrap"><h2 class="serif">Im Paket enthalten</h2><div class="pgrid">'+"".join(card(q) for q in singles)+'</div><p class="note" style="margin-top:16px">Einzeln zusammen 70 € – im Paket 35 €.</p></div></section>'
    body=f"""<div class="wrap hero">
<div>
<p class="eyebrow">{html.escape(p['eyebrow'])}</p>
<h1 class="serif">{html.escape(p['h1'])}</h1>
<p class="lead">{html.escape(p['lead'])}</p>
{buy(p)}
<p class="note">Digitales Produkt · Download-Link direkt nach dem Kauf · Einmalzahlung, kein Abo</p>
</div>
<div><img class="heroimg" src="img/{p['img']}" width="1000" height="1000" alt="Produktbild {html.escape(p['name'])}"></div>
</div>
<section class="band"><div class="wrap">
<h2 class="serif">Das bekommst du</h2>
<div class="split"><div><table class="spec">{tbl}</table></div>
{f'<div class="shots">{shots}</div>' if shots else ''}</div>
{'<p class="note" style="margin-top:12px">Screenshots mit Beispieldaten.</p>' if shots else ''}
</div></section>
{f'<section><div class="wrap"><h2 class="serif">Was die Vorlage kann</h2><div class="grid2">{feats}</div></div></section>' if feats else ''}
{extra}
{FAQ}
<section id="kaufen" class="band"><div class="wrap buy">
<h2 class="serif">{html.escape(p['name'])} kaufen</h2>
<p class="sub2">Digitaler Download · sofort nach der Zahlung verfügbar</p>
<div class="price-big serif">{p['price']}</div>
{buy(p,"btn btn-lg","Jetzt kaufen")}
<p class="note">Sichere Zahlung und Rechnung über Digistore24. Preis inkl. gesetzlicher MwSt., sofern anfallend.</p>
{'' if p['slug']=='paket' else '<p class="note"><a href="paket.html">Alle 5 Vorlagen im Paket für 35 € statt 70 € →</a></p>'}
</div></section>"""
    page(f"{p['name']} – Excel-Vorlage | Solovorlagen",p["lead"][:155],body,f"{p['slug']}.html")
print("ok", DS)

exec(open(os.path.join(HERE,"content.py")).read())
