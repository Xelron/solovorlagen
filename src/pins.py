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
    elif extra and extra.startswith("img/"):
        mid=f'<div class=img style="height:620px"><img src="data:image/jpeg;base64,{base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","docs")+"/"+extra,"rb").read()).decode()}" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>'
    else:
        mid=f'<div style="border-top:10px solid {acc};padding-top:40px;font-size:40px;font-weight:700;color:{fg};white-space:nowrap;display:inline-block">Jetzt lesen →</div>'
    h=f"""<div class=p style="background:{bg};color:{fg}"><div><div class="brand serif" style="color:{mut}">SOLOVORLAGEN</div>
<h1 class=serif style="color:{fg};{'font-size:70px' if (len(title)>30 or max(len(w) for w in title.split())>13) else ''}">{title}</h1><div class="h2 serif" style="color:{acc if bg!='#F6F7F4' else '#2E7D6B'}">{h2}</div><div class=sub style="color:{mut}">{sub}</div></div>
{mid}<div class=url style="color:{fg}">solovorlagen.de</div></div>"""
    return h
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':1500})
    for i,t in enumerate(P):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{render(i,t)}</body></html>")
        pg.wait_for_timeout(150)
        pg.screenshot(path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","docs","pins")+f"/pin-{i+1:02d}.jpg",type="jpeg",quality=85)
        print(i+1, pg.evaluate("document.querySelector('.p').scrollHeight"))
    b.close()
start=datetime.date(2026,10,16)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","pinterest-pins.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
    for i,t in enumerate(P):
        title,h2,sub,extra,link,board,desc,kw=t
        d=start+datetime.timedelta(days=2*i)
        h2c=h2.replace('-regelung','regelung').replace('Entfernungs-pauschale','Entfernungspauschale'); full=title+' – '+h2c if len(title+' – '+h2c)<=100 else title
        w.writerow([full,f"{B}pins/pin-{i+1:02d}.jpg",board,"",desc[:500],B+link,f"{d.isoformat()}T07:00:00",kw])
print(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","pinterest-pins.csv")).read()[:600])
