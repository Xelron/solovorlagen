from playwright.sync_api import sync_playwright
import csv, datetime, base64, os
B="https://solovorlagen.de/"
P=[
("Kleinunternehmer 2026: Diese 2 Grenzen musst du kennen","25.000 € im Vorjahr · 100.000 € im laufenden Jahr","Was beim Überschreiten passiert – einfach erklärt",None,"kleinunternehmerregelung-grenzen.html","Kleinunternehmer Tipps",
 "Kleinunternehmerregelung 2026: Wer 2025 höchstens 25.000 € Umsatz hatte und 2026 unter 100.000 € bleibt, ist Kleinunternehmer. Über 100.000 € endet die Regelung sofort. Alle Regeln, Beispiele und FAQ im Ratgeber.","kleinunternehmer, kleinunternehmerregelung 2026, umsatzgrenze, selbstständig, steuern selbstständige"),
("Bin ich noch Kleinunternehmer?","Kostenloser Umsatzgrenzen-Check","In 30 Sekunden Klarheit – mit Ausblick aufs nächste Jahr","ampel","grenzen-check.html","Kleinunternehmer Tipps",
 "Kostenloser Online-Rechner: Umsatz eintragen und sofort sehen, ob du 2026 die Kleinunternehmergrenzen einhältst – und ob du nächstes Jahr noch Kleinunternehmer bist. Ohne Anmeldung.","kleinunternehmer check, umsatzgrenze rechner, kleinunternehmerregelung, gründer, nebengewerbe"),
("Über 100.000 € Umsatz?","Dann endet die Kleinunternehmer-regelung sofort","Schon der Umsatz, der die Grenze überschreitet, ist steuerpflichtig",None,"kleinunternehmerregelung-grenzen.html#100000","Kleinunternehmer Tipps",
 "Seit 2025 gibt es keine Schonfrist bis Jahresende mehr: Wer als Kleinunternehmer im laufenden Jahr 100.000 € überschreitet, muss ab sofort Umsatzsteuer ausweisen. Was jetzt zu tun ist, erklärt der Ratgeber.","kleinunternehmer 100000, umsatzsteuer, kleinunternehmerregelung, selbstständig, freelancer"),
("Mehr als 25.000 € Umsatz?","Das passiert im nächsten Jahr","Die Grenze, die viele erst im Januar bemerken",None,"kleinunternehmerregelung-grenzen.html#25000","Kleinunternehmer Tipps",
 "Wer im Jahr mehr als 25.000 € Umsatz macht, bleibt dieses Jahr Kleinunternehmer – ist aber im Folgejahr Regelunternehmer und muss Umsatzsteuer berechnen. So bereitest du dich rechtzeitig vor.","kleinunternehmer 25000, umsatzgrenze, umsatzsteuer, selbstständig, nebenberuflich selbstständig"),
("Stundensatz berechnen","Die Formel für Selbstständige","Mit Rechenbeispiel und typischen Fehlern",None,"stundensatz-berechnen.html","Selbstständig: Preise & Geld",
 "Stundensatz = Umsatzziel ÷ abrechenbare Stunden. So berechnest du als Selbstständiger oder Freelancer einen Stundensatz, der Versicherung, Steuern, Urlaub und Krankheit wirklich abdeckt – Schritt für Schritt erklärt.","stundensatz berechnen, freelancer stundensatz, selbstständig preise, tagessatz, honorar"),
("2.500 € netto?","So viel musst du pro Stunde verlangen","≈ 65 € – und warum es so viel sein muss","rate","stundensatz-berechnen.html#schritte","Selbstständig: Preise & Geld",
 "Für 2.500 € netto im Monat brauchen Selbstständige mit typischen Annahmen rund 65 € pro Stunde. Die komplette Rechnung mit Krankenversicherung, Altersvorsorge, Steuern und abrechenbaren Stunden im Ratgeber.","stundensatz freelancer, selbstständig netto, stundenlohn selbstständig, preise kalkulieren, gründen"),
("5 Fehler beim Stundensatz","…die dich als Selbstständige:r Geld kosten","Nr. 2 machen fast alle",None,"stundensatz-berechnen.html#fehler","Selbstständig: Preise & Geld",
 "Angestellten-Lohn als Maßstab, alle Stunden als abrechenbar gerechnet, Krankenversicherung vergessen, keine Steuerrücklage, kein Puffer: Diese 5 Fehler machen Stundensätze zu niedrig. So vermeidest du sie.","stundensatz fehler, freelancer tipps, selbstständig machen, preise erhöhen, honorar berechnen"),
("Rechnung als Kleinunternehmer","Das muss drauf","Pflichtangaben nach § 34a UStDV",None,"kleinunternehmerregelung-grenzen.html#rechnung","Kleinunternehmer Tipps",
 "Name und Anschrift, Steuernummer, Datum, Leistung, Betrag und der Hinweis auf die Kleinunternehmerregelung: Diese Angaben gehören auf jede Kleinunternehmer-Rechnung. Plus: Musst du E-Rechnungen ausstellen?","rechnung kleinunternehmer, rechnung schreiben, paragraph 19 ustg, e-rechnung, selbstständig"),
("Fahrtkosten 2026","0,30 € pro km Dienstfahrt · 0,38 € Entfernungs-pauschale","Fahrtenbuch-Vorlage für Selbstständige","img/fahrten-01.jpg","fahrtenbuch.html","Excel-Vorlagen für Selbstständige",
 "Fahrten mit dem Privatauto zum Kunden oder ins Büro? Diese Excel-Vorlage erfasst alle Angaben und rechnet die absetzbaren Fahrtkosten 2026 automatisch aus – mit Prüfung auf Lücken im km-Stand.","fahrtenbuch vorlage, fahrtkosten selbstständig, kilometerpauschale 2026, entfernungspauschale, excel vorlage"),
("Sofort absetzen oder abschreiben?","GWG bis 800 € · Sammelposten · AfA","Der AfA-Rechner entscheidet für dich","img/afa-01.jpg","afa.html","Excel-Vorlagen für Selbstständige",
 "Laptop, Schreibtisch, Kamera: Diese Excel-Vorlage entscheidet automatisch zwischen Sofortabzug, GWG-Sofortabschreibung, Sammelposten und linearer AfA – monatsgenau, mit Restbuchwert. Stand 2026.","afa rechner, gwg 800 euro, abschreibung selbstständig, anlagenverzeichnis, euer"),
("Umsatzgrenzen-Ampel","Excel-Vorlage für Kleinunternehmer","Einnahmen eintragen – die Ampel zeigt, wo du stehst","img/produkt.jpg","cockpit.html","Excel-Vorlagen für Selbstständige",
 "Das Kleinunternehmer-Cockpit: Einnahmen und Ausgaben erfassen, Umsatzgrenzen-Ampel für 25.000 € und 100.000 €, EÜR-Übersicht und Steuerrücklage – in einer Excel-Datei. Läuft auch in Google Sheets.","kleinunternehmer excel, einnahmen ausgaben vorlage, euer vorlage, buchhaltung excel, google sheets vorlage"),
("Das Selbstständigen-Paket","5 Excel-Vorlagen zum halben Preis","Cockpit · Rechnungen · Stundensatz · Fahrtenbuch · AfA","img/bundle-01.jpg","paket.html","Excel-Vorlagen für Selbstständige",
 "Alle 5 Solovorlagen in einem Paket für 35 € statt 70 €: Umsatzgrenzen-Ampel, Rechnungs-Generator, Stundensatz-Rechner, Fahrtenbuch und AfA-Rechner. Für Kleinunternehmer und Freelancer in Deutschland.","excel vorlagen selbstständige, kleinunternehmer paket, buchhaltung vorlagen, freelancer tools, gründer"),
]
P2=[
("Rechnung als Kleinunternehmer?","Diesen Satz brauchst du","Hinweis-Text zum Kopieren – kostenlos","quote","rechnungstext-kleinunternehmer.html","Kleinunternehmer Tipps",
 "Jede Kleinunternehmer-Rechnung braucht einen Hinweis auf die Steuerbefreiung, z. B. „Steuerfreie Kleinunternehmerleistung gemäß § 19 Abs. 1 UStG.“ Formulierungen zum Kopieren plus Pflichtangaben-Check nach § 34a UStDV – kostenlos und ohne Anmeldung.","rechnung kleinunternehmer, paragraph 19 ustg, rechnung schreiben, kleinunternehmerregelung, selbstständig"),
("Pflichtangaben-Check","für Kleinunternehmer-Rechnungen","Fehlt etwas? Der Generator zeigt es sofort","checks","rechnungstext-kleinunternehmer.html","Kleinunternehmer Tipps",
 "Name, Anschrift, Steuernummer, Datum, Leistung, Betrag und § 19-Hinweis: Der kostenlose Rechnungstext-Generator prüft deine Kleinunternehmer-Rechnung nach § 34a UStDV und erstellt den fertigen Text. Rechnungsnummer? Nicht Pflicht – aber empfohlen.","rechnung pflichtangaben, kleinunternehmer rechnung vorlage, rechnungsnummer, gründer tipps, freelancer"),
("Laptop gekauft?","Sofort absetzen – egal wie teuer","Computer & Software: Nutzungsdauer 1 Jahr","laptop","gwg-rechner.html","Selbstständig: Preise & Geld",
 "Laptop, PC, Monitor, Drucker oder Software kannst du als Selbstständiger im Jahr der Anschaffung komplett absetzen – dank 1 Jahr Nutzungsdauer. Der kostenlose GWG-Rechner zeigt dir, was du 2026 sofort absetzen darfst.","laptop absetzen, computer abschreibung, gwg, steuern sparen selbstständig, betriebsausgaben"),
("GWG-Grenze 2026","Was darfst du sofort absetzen?","Kostenloser Rechner – auch für Kleinunternehmer","tiers","gwg-rechner.html","Selbstständig: Preise & Geld",
 "Bis 250 € sofort, bis 800 € als GWG, bis 1.000 € im Sammelposten, darüber Abschreibung: Der kostenlose GWG-Rechner 2026 sagt dir in Sekunden, wie du eine Anschaffung absetzt – mit Abschreibungsplan.","gwg grenze 2026, geringwertige wirtschaftsgüter, sammelposten, afa, abschreibung selbstständige"),
("Fahrtkosten 2026","0,30 € je km Dienstfahrt","Kostenloser Rechner für Selbstständige","km","fahrtkosten-rechner.html","Selbstständig: Preise & Geld",
 "Fahrten zum Kunden mit dem Privatauto? 0,30 € je gefahrenem Kilometer sind Betriebsausgabe. 250 km im Monat ergeben 900 € im Jahr. Der kostenlose Fahrtkosten-Rechner 2026 rechnet es für dich aus.","fahrtkosten absetzen, kilometerpauschale 2026, dienstfahrt, selbstständig steuern, betriebsausgaben"),
("Entfernungspauschale 2026","Jetzt 0,38 € ab dem 1. Kilometer","Was sich für Selbstständige ändert",None,"fahrtkosten-rechner.html","Selbstständig: Preise & Geld",
 "Seit 2026 gilt die Entfernungspauschale von 0,38 € schon ab dem ersten Kilometer. Für Selbstständige zählt sie beim Weg zur eigenen Betriebsstätte – alle anderen betrieblichen Fahrten laufen mit 0,30 € je km. Kostenloser Rechner.","entfernungspauschale 2026, pendlerpauschale, fahrtkosten, selbstständig, steuern 2026"),
]
P3=[
("Rechnungen als Kleinunternehmer","Excel-Vorlage mit allen Pflichtangaben","Rechnungsbuch · offene Posten · Zahlungserinnerung","img/rechnung-01.jpg","rechnung.html","Excel-Vorlagen für Selbstständige",
 "Rechnungs-Generator für Kleinunternehmer: Rechnungen mit allen Pflichtangaben nach § 34a UStDV und Hinweis auf die Steuerbefreiung, Kundenliste, Rechnungsbuch mit offenen Posten und fertige Zahlungserinnerung. Excel & Google Sheets.","rechnungsvorlage kleinunternehmer, rechnung excel, rechnung schreiben, zahlungserinnerung, selbstständig"),
]
P4=[
("Wie viel Steuer zurücklegen?","Die Prozentsätze für 2026","Einkommensteuer nach Tarif – mit Rechenbeispielen","pct","steuerruecklage-berechnen.html#tabelle","Selbstständig: Preise & Geld","",""),
("Gründer-Falle im 2. Jahr","Nachzahlung + Vorauszahlung auf einmal","So bist du vorbereitet","double","steuerruecklage-berechnen.html#gruender","Kleinunternehmer Tipps","",""),
("Steuer-Vorauszahlungen","Diese 4 Termine solltest du kennen","Einkommensteuer nach § 37 EStG","cal","steuerruecklage-berechnen.html#vorauszahlungen","Selbstständig: Preise & Geld","",""),
("Herbst-Check für Kleinunternehmer","Schon über 25.000 € Umsatz?","Dann bist du nächstes Jahr kein Kleinunternehmer mehr","gauge","grenzen-check.html#calc","Kleinunternehmer Tipps","",""),
("Stundensatz-Rechner","Excel-Vorlage für Selbstständige","Gesetzlich oder privat versichert – beides wählbar","img/stundensatz-02.jpg|fit","stundensatz.html#kaufen","Excel-Vorlagen für Selbstständige","",""),
("Vom Stundensatz zum Tagessatz","So einfach rechnest du um","Unbezahlte Zeit steckt schon im Stundensatz","day","stundensatz-berechnen.html#tagessatz","Selbstständig: Preise & Geld","",""),
("EÜR & Steuerrücklage","Excel-Vorlage für Kleinunternehmer","Einnahmen eintragen – Gewinn und Rücklage im Blick","img/euer.jpg|fit","cockpit.html#kaufen","Excel-Vorlagen für Selbstständige","",""),
]
P5=[
("EÜR für Kleinunternehmer","Einnahmen − Ausgaben = Gewinn","So funktioniert's – mit Beispielrechnung","euer","euer-kleinunternehmer.html#beispiel","Kleinunternehmer Tipps","",""),
("Rechnung im Dezember, Geld im Januar?","Dann zählt die Einnahme im neuen Jahr","Das Zahlungsdatum entscheidet in der EÜR","zufluss","euer-kleinunternehmer.html#zahlung","Kleinunternehmer Tipps","",""),
("Brutto oder netto?","Kleinunternehmer setzen Ausgaben brutto ab","Denn es gibt keinen Vorsteuerabzug","brutto","euer-kleinunternehmer.html#brutto","Selbstständig: Preise & Geld","",""),
("Fahrtenbuch für dein Privatauto","Excel-Vorlage mit den Sätzen 2026","Jahressumme der Fahrtkosten für die EÜR","img/fahrten-03.jpg|fit","fahrtenbuch.html#kaufen","Excel-Vorlagen für Selbstständige","",""),
("Abschreibungen im Griff","Anlagenverzeichnis & AfA-Rechner","GWG, Computer, lineare AfA – mit Jahressumme","img/afa-02.jpg|fit","afa.html#kaufen","Excel-Vorlagen für Selbstständige","",""),
("Gerade erst gegründet?","Dann liegt die Grenze bei 25.000 €","Kleinunternehmerregelung: keine Hochrechnung aufs volle Jahr","found","kleinunternehmerregelung-grenzen.html#gruendung","Kleinunternehmer Tipps","",""),
("Wie viele Stunden kannst du abrechnen?","Oft nur rund 1.000 im Jahr","Darum muss dein Stundensatz höher sein","hours","stundensatz-berechnen.html#stunden","Selbstständig: Preise & Geld","",""),
]
CSS="""*{box-sizing:border-box}body{margin:0;width:1000px;height:1500px;font-family:'DejaVu Sans',Arial,sans-serif}
.p{width:1000px;height:1500px;padding:80px 72px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
.serif{font-family:'DejaVu Serif',Georgia,serif;font-weight:700}.brand{font-size:30px;letter-spacing:.06em}
h1{font-size:92px;line-height:1.05;margin:28px 0 30px}.h2{font-size:52px;line-height:1.15;margin:0 0 24px}.sub{font-size:36px;line-height:1.35}
.url{font-size:34px;font-weight:700}.img{border-radius:28px;overflow:hidden;box-shadow:0 24px 48px rgba(0,0,0,.18)}
.light{border-radius:20px;padding:26px 30px;font-size:40px;font-weight:700;margin-bottom:16px;display:flex;gap:22px;align-items:center}.dot{width:38px;height:38px;border-radius:50%}
"""
themes=[("#1F3A5F","#FFFFFF","#cfe0f0","#E0A800"),("#F6F7F4","#1F3A5F","#3A4654","#2E7D6B"),("#2E7D6B","#FFFFFF","#e2f2ec","#FFE08A")]
def render(i,t):
    title,h2,sub,extra,link,board,desc,kw=t
    bg,fg,mut,acc=themes[i%3]
    mid=""
    if extra=="ampel":
        mid='<div>'+"".join(f'<div class=light style="background:{b};color:{c}"><span class=dot style="background:{d}"></span>{l}</div>' for b,c,d,l in [("#D4EDDA","#0F5132","#198754","Im grünen Bereich"),("#FFF3CD","#664D03","#E0A800","Grenze bald erreicht"),("#F8D7DA","#842029","#B02A37","Grenze überschritten")])+'</div>'
    elif extra=="rate":
        mid=f'<div style="background:rgba(255,255,255,.12);border-radius:28px;padding:40px"><div style="font-size:30px;color:{mut};font-weight:700">DEIN STUNDENSATZ</div><div class=serif style="font-size:150px;color:{fg};line-height:1.1">65 €</div><div style="font-size:32px;color:{mut}">Tagessatz ≈ 520 €</div></div>'
    elif extra=="quote":
        mid=f'<div style="background:#fff;border-radius:28px;padding:44px;border-left:16px solid {acc}"><div class=serif style="font-size:48px;line-height:1.25;color:#1F3A5F">„Steuerfreie Kleinunternehmer&shy;leistung gemäß § 19 Abs. 1 UStG.“</div><div style="margin-top:22px;font-size:30px;color:#5A6573;font-weight:700">KOPIEREN · EINFÜGEN · FERTIG</div></div>'
    elif extra=="checks":
        mid='<div style="background:#fff;border-radius:28px;padding:34px 40px">'+"".join(f'<div style="display:flex;gap:22px;align-items:center;font-size:36px;color:#1B2430;padding:10px 0"><span style="width:46px;height:46px;border-radius:50%;background:{b};color:{c};display:inline-flex;align-items:center;justify-content:center;font-weight:700">{m}</span>{l}</div>' for b,c,m,l in [("#D4EDDA","#0F5132","✓","Name & Anschrift"),("#D4EDDA","#0F5132","✓","Steuernummer"),("#D4EDDA","#0F5132","✓","Datum & Leistung"),("#FFF3CD","#664D03","!","Hinweis § 19 UStG"),("#E3E8EE","#5A6573","–","Rechnungsnummer (optional)")])+'</div>'
    elif extra=="laptop":
        mid=f'<div style="background:rgba(255,255,255,.12);border-radius:28px;padding:40px"><div style="font-size:30px;color:{mut};font-weight:700">LAPTOP FÜR 1.499 €</div><div class=serif style="font-size:130px;color:{fg};line-height:1.1">100 %</div><div style="font-size:34px;color:{mut}">im Anschaffungsjahr absetzbar</div></div>'
    elif extra=="tiers":
        mid='<div>'+"".join(f'<div class=light style="background:{b};color:{c};justify-content:space-between"><span>{l}</span><span>{r}</span></div>' for b,c,l,r in [("#D4EDDA","#0F5132","bis 250 €","sofort"),("#D4EDDA","#0F5132","bis 800 €","sofort (GWG)"),("#FFF3CD","#664D03","bis 1.000 €","Sammelposten"),("#F8D7DA","#842029","darüber","Abschreibung")])+'<div style="font-size:26px;color:#5A6573;margin-top:6px">Beträge netto · Stand 2026</div></div>'
    elif extra=="km":
        mid=f'<div style="background:rgba(255,255,255,.12);border-radius:28px;padding:40px"><div style="font-size:30px;color:{mut};font-weight:700">250 KM IM MONAT</div><div class=serif style="font-size:150px;color:{fg};line-height:1.1">900 €</div><div style="font-size:34px;color:{mut}">Betriebsausgaben im Jahr</div></div>'
    elif extra=="pct":
        mid='<div style="background:#fff;border-radius:28px;padding:36px 40px"><div style="font-size:28px;color:#5A6573;font-weight:700;margin-bottom:14px">ZU VERST. EINKOMMEN → STEUERSATZ</div>'+"".join(f'<div style="margin:16px 0"><div style="display:flex;justify-content:space-between;font-size:38px;font-weight:700;color:#1B2430"><span>{l}</span><span>{r}</span></div><div style="height:22px;background:#E3E8EE;border-radius:11px;margin-top:10px"><div style="height:22px;width:{w}%;background:{acc};border-radius:11px"></div></div></div>' for l,r,w in [("25.000 €","≈ 11 %",44),("40.000 €","≈ 18 %",72),("60.000 €","≈ 24 %",95)])+'<div style="font-size:24px;color:#5A6573;margin-top:12px">Einkommensteuer 2026 · Einzelveranlagung</div></div>'
    elif extra=="double":
        mid=f'<div>'+f'<div style="background:#fff;border-radius:24px;padding:30px 36px;margin-bottom:18px"><div style="font-size:28px;color:#5A6573;font-weight:700">1 · NACHZAHLUNG</div><div class=serif style="font-size:46px;color:#1F3A5F">für das Gründungsjahr</div></div>'+f'<div style="text-align:center;font-size:70px;font-weight:700;color:{acc};line-height:1">+</div>'+f'<div style="background:#fff;border-radius:24px;padding:30px 36px;margin-top:18px"><div style="font-size:28px;color:#5A6573;font-weight:700">2 · VORAUSZAHLUNGEN</div><div class=serif style="font-size:46px;color:#1F3A5F">für das laufende Jahr</div></div></div>'
    elif extra=="cal":
        mid='<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">'+"".join(f'<div style="background:#fff;border-radius:24px;overflow:hidden;text-align:center;box-shadow:0 12px 28px rgba(0,0,0,.12)"><div style="background:{acc};color:#fff;font-size:34px;font-weight:700;padding:14px">{m}</div><div class=serif style="font-size:110px;color:#1F3A5F;line-height:1.3">10.</div></div>' for m in ["MÄRZ","JUNI","SEPTEMBER","DEZEMBER"])+'</div>'
    elif extra=="gauge":
        lt=bg=='#F6F7F4'; box='#fff' if lt else 'rgba(255,255,255,.12)'; trk='#E3E8EE' if lt else 'rgba(255,255,255,.25)'
        mid=f'<div style="background:{box};border-radius:28px;padding:40px;{"box-shadow:0 12px 32px rgba(31,58,95,.12)" if lt else ""}"><div style="display:flex;justify-content:space-between;font-size:30px;color:{mut};font-weight:700"><span>UMSATZ BISHER</span><span>GRENZE</span></div><div style="display:flex;justify-content:space-between;align-items:baseline"><span class=serif style="font-size:96px;color:{fg}">21.800 €</span><span class=serif style="font-size:44px;color:{fg}">25.000 €</span></div><div style="height:34px;background:{trk};border-radius:17px;margin-top:18px"><div style="height:34px;width:87%;background:{acc};border-radius:17px"></div></div><div style="font-size:30px;color:{mut};margin-top:18px">87 % ausgeschöpft – was kommt bis zum 31.12. dazu?</div></div>'
    elif extra=="day":
        mid=f'<div style="background:#fff;border-radius:28px;padding:44px;text-align:center"><div style="display:flex;justify-content:center;align-items:center;gap:26px;font-size:64px;font-weight:700;color:#1F3A5F"><span>65 €</span><span style="color:{acc}">×</span><span>8 h</span></div><div style="height:6px;background:#E3E8EE;margin:30px 0"></div><div class=serif style="font-size:140px;color:#1F3A5F;line-height:1">520 €</div><div style="font-size:30px;color:#5A6573;margin-top:16px;font-weight:700">TAGESSATZ PRO ABGERECHNETEM TAG</div></div>'
    elif extra=="euer":
        mid='<div style="background:#fff;border-radius:28px;padding:40px 44px">'+"".join(f'<div style="display:flex;justify-content:space-between;font-size:40px;color:#1B2430;padding:14px 0;border-bottom:2px solid #E3E8EE"><span>{l}</span><span style="font-weight:700">{r}</span></div>' for l,r in [("Einnahmen","21.600 €"),("− Ausgaben","3.634 €")])+f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding-top:22px"><span class=serif style="font-size:46px;color:#1F3A5F">= Gewinn</span><span class=serif style="font-size:76px;color:#2E7D6B">17.966 €</span></div><div style="font-size:26px;color:#5A6573;margin-top:12px">Beispiel: Kleinunternehmerin, EÜR 2026</div></div>'
    elif extra=="zufluss":
        card=lambda m,d,l,c,b: f'<div style="flex:1;background:#fff;border-radius:24px;overflow:hidden;text-align:center;box-shadow:0 12px 28px rgba(0,0,0,.14)"><div style="background:{c};color:#fff;font-size:30px;font-weight:700;padding:12px">{m}</div><div class=serif style="font-size:96px;color:#1F3A5F;line-height:1.25">{d}</div><div style="font-size:30px;font-weight:700;color:#1B2430;padding:0 10px 10px">{l}</div><div style="font-size:26px;color:#5A6573;padding:0 10px 22px">{b}</div></div>'
        mid='<div style="display:flex;gap:26px;align-items:center">'+card("DEZ 2026","15.","Rechnung","#5A6573","zählt noch nicht")+f'<div style="font-size:70px;font-weight:700;color:{acc}">→</div>'+card("JAN 2027","8.","Zahlung ✓","#2E7D6B","EÜR 2027")+'</div>'
    elif extra=="brutto":
        mid='<div style="background:#fff;border-radius:28px;padding:40px 44px;box-shadow:0 12px 32px rgba(31,58,95,.12)"><div style="font-size:28px;color:#5A6573;font-weight:700;margin-bottom:10px">BELEG: BÜROSTUHL</div>'+"".join(f'<div style="display:flex;justify-content:space-between;font-size:38px;color:#1B2430;padding:10px 0"><span>{l}</span><span>{r}</span></div>' for l,r in [("Netto","400,00 €"),("+ 19 % USt","76,00 €")])+'<div style="display:flex;justify-content:space-between;align-items:baseline;border-top:3px solid #1F3A5F;margin-top:10px;padding-top:18px"><span class=serif style="font-size:44px;color:#1F3A5F">Absetzbar</span><span class=serif style="font-size:72px;color:#2E7D6B">476,00 €</span></div><div style="font-size:26px;color:#5A6573;margin-top:12px">GWG-Grenze netto geprüft (400 € ≤ 800 €)</div></div>'
    elif extra=="found":
        mid='<div>'+"".join(f'<div style="background:#fff;border-radius:24px;padding:30px 36px;margin-bottom:20px;border-left:16px solid {c}"><div style="font-size:28px;color:#5A6573;font-weight:700">{t}</div><div class=serif style="font-size:64px;color:#1F3A5F">{v}</div><div style="font-size:30px;color:#1B2430">{d}</div></div>' for t,v,d,c in [("GRÜNDUNGSJAHR","25.000 €","im laufenden Jahr – sonst endet die Regelung sofort","#E0A800"),("AB DEM FOLGEJAHR","Vorjahr zählt","Vorjahresumsatz höchstens 25.000 €, laufendes Jahr höchstens 100.000 €","#2E7D6B")])+'</div>'
    elif extra=="hours":
        mid=f'<div style="background:rgba(255,255,255,.12);border-radius:28px;padding:36px 40px">'+"".join(f'<div style="display:flex;justify-content:space-between;font-size:36px;color:{fg};padding:9px 0"><span>{l}</span><span style="font-weight:700">{r}</span></div>' for l,r in [("52 Wochen × 5 Tage","260"),("− Urlaub, Feiertage, Krankheit, Fortbildung","55"),("= Arbeitstage","205"),("× 8 Stunden × 60 % abrechenbar","")])+f'<div style="display:flex;justify-content:space-between;align-items:baseline;border-top:3px solid {mut};margin-top:12px;padding-top:16px"><span class=serif style="font-size:44px;color:{fg}">Abrechenbar</span><span class=serif style="font-size:84px;color:{acc}">984 h</span></div></div>'
    elif extra and extra.startswith("img/") and extra.endswith("|fit"):
        from PIL import Image as _I
        fp=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","docs",extra[:-4]); px=_I.open(fp).convert("RGB").getpixel((5,5))
        mid=f'<div class=img style="height:640px;background:rgb{px};display:flex;align-items:center;justify-content:center"><img src="data:image/jpeg;base64,{base64.b64encode(open(fp,"rb").read()).decode()}" style="height:100%;width:auto;display:block"></div>'
    elif extra and extra.startswith("img/"):
        mid=f'<div class=img style="height:620px"><img src="data:image/jpeg;base64,{base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","docs")+"/"+extra,"rb").read()).decode()}" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>'
    else:
        mid=f'<div style="border-top:10px solid {acc};padding-top:40px;font-size:40px;font-weight:700;color:{fg};white-space:nowrap;display:inline-block">Jetzt lesen →</div>'
    h=f"""<div class=p style="background:{bg};color:{fg}"><div><div class="brand serif" style="color:{mut}">SOLOVORLAGEN</div>
<h1 class=serif style="color:{fg};{'font-size:70px' if (len(title)>30 or max(len(w) for w in title.split())>13) else ''}">{title}</h1><div class="h2 serif" style="color:{acc if bg!='#F6F7F4' else '#2E7D6B'}">{h2}</div><div class=sub style="color:{mut}">{sub}</div></div>
{mid}<div class=url style="color:{fg}">solovorlagen.de</div></div>"""
    return h
import sys
BATCH=int(sys.argv[1]) if len(sys.argv)>1 else 2
LST,OFF,START,CSVN={1:(P,0,datetime.date(2026,10,16),"pinterest-pins.csv"),2:(P2,12,datetime.date(2026,10,17),"pinterest-pins-2.csv"),3:(P3,18,datetime.date(2026,10,18),"pinterest-pins-3.csv"),4:(P4,19,datetime.date(2026,10,25),None),5:(P5,26,datetime.date(2026,11,1),None)}[BATCH]
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':1500})
    for i,t in enumerate(LST):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{render(i+OFF,t)}</body></html>")
        pg.wait_for_timeout(150)
        pg.screenshot(path=os.path.join(ROOT,"docs","pins",f"pin-{i+1+OFF:02d}.jpg"),type="jpeg",quality=85)
        print(i+1+OFF, pg.evaluate("document.querySelector('.p').scrollHeight"))
    b.close()
if CSVN is None: sys.exit(0)  # ab Batch 4: Termine stehen in src/feeds.json, keine CSV
with open(os.path.join(ROOT,CSVN),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    for i,t in enumerate(LST):
        title,h2,sub,extra,link,board,desc,kw=t
        d=START+datetime.timedelta(days=2*i)
        h2c=h2.replace('-regelung','regelung').replace('Entfernungs-pauschale','Entfernungspauschale'); full=title+' – '+h2c if len(title+' – '+h2c)<=100 else title
        w.writerow([full,f"{B}pins/pin-{i+1+OFF:02d}.jpg",board,"",desc[:500],B+link,f"{d.isoformat()}T07:00:00",kw])
print(open(os.path.join(ROOT,CSVN)).read())
