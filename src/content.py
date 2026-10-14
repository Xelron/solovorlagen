# -*- coding: utf-8 -*-
# Zusatzseiten: Grenzen-Check, Ratgeber. Wird aus gen_site.py per exec ausgeführt (page, html, json, os, OUT verfügbar).
import json as _json
STAND="14.10.2026"; ISO="2026-10-14"
AUTHOR={"@type":"Person","name":"Felix Merklinger-Lötzsch","url":"https://solovorlagen.de/impressum.html"}
PUB={"@type":"Organization","name":"Solovorlagen","url":"https://solovorlagen.de/","logo":"https://solovorlagen.de/img/logo.png"}
def ld(obj): return '<script type="application/ld+json">'+_json.dumps(obj,ensure_ascii=False)+'</script>'
def faq_ld(qas): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
def faq_html(qas): return "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in qas)
def crumbs(items): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
def article_ld(headline,desc,url):
    return {"@context":"https://schema.org","@type":"Article","headline":headline,"description":desc,"inLanguage":"de-DE",
            "datePublished":ISO,"dateModified":ISO,"author":AUTHOR,"publisher":PUB,"mainEntityOfPage":url}
SRC_KU=[("§ 19 UStG – Gesetzestext (dejure.org)","https://dejure.org/gesetze/UStG/19.html"),
("Deutsche Handwerks Zeitung: Kleinunternehmerregelung 2025 – BMF-Anwendungsschreiben vom 18.03.2025","https://www.deutsche-handwerks-zeitung.de/kleinunternehmerregelung-2025-anwendungsschreiben-beachten-361560/"),
("finanz.de: Kleinunternehmerregelung (Stand 02.10.2026)","https://www.finanz.de/business/kleinunternehmerregelung/"),
("steuertipps.de: Wichtige Änderungen für Kleinunternehmer ab 2025","https://www.steuertipps.de/selbststaendigkeit/wichtige-aenderungen-fuer-kleinunternehmer-ab-2025"),
("§ 34a UStDV – Rechnungen von Kleinunternehmern (dejure.org)","https://dejure.org/gesetze/UStDV/34a.html"),
("BMF-Schreiben vom 18.03.2025 zur Sonderregelung für Kleinunternehmer (PDF-Kopie)","https://www.bistum-trier.de/export/sites/portal/unser-bistum/.galleries/dokumente/2025-03-18-sonderregelung-kleinunternehmer.pdf")]
def sources(lst): return '<ul class="src">'+"".join(f'<li><a href="{u}" rel="noopener">{html.escape(t)}</a></li>' for t,u in lst)+'</ul>'
BYLINE=f'<p class="byline">Von <a href="impressum.html">Felix Merklinger-Lötzsch</a>, Solovorlagen · Stand: <time datetime="{ISO}">{STAND}</time></p>'
DISCL='<p class="note">Dieser Ratgeber erklärt die allgemeine Rechtslage verständlich und ersetzt keine Steuerberatung. Für deine konkrete Situation wende dich an eine Steuerberatung oder dein Finanzamt.</p>'
EXTRA_CSS="""<style>
.article{max-width:760px}.article h2{margin-top:44px;font-size:clamp(24px,3.4vw,30px)}.article h3{margin-top:28px;font-size:19px}
.article p,.article li{font-size:17px;color:var(--ink)}.article li{margin-bottom:6px}
.answer{background:#fff;border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:12px;padding:20px 24px;margin:24px 0}
.answer p{margin:0}.byline{font-size:14px;color:var(--soft);margin:0 0 8px}
.tbl{width:100%;border-collapse:collapse;font-size:16px;margin:16px 0;background:#fff}.tbl th{background:var(--navy);color:#fff;text-align:left;padding:10px 12px}
.tbl td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}.tblwrap{overflow-x:auto}
.cta{background:var(--navy);color:#fff;border-radius:14px;padding:24px;margin:32px 0}.cta h3{color:#fff;margin:0 0 8px}.cta p{color:#dbe6f0;margin:0 0 16px}
.src{font-size:15px}.toc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 24px}.toc li{font-size:16px}
.calc{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;box-shadow:0 12px 32px rgba(31,58,95,.08)}
.calc label{display:block;font-weight:600;margin:14px 0 6px}.calc input[type=text],.calc input[type=date]{width:100%;font-size:18px;padding:12px 14px;border:1px solid #C9D2DC;border-radius:10px;background:#FFFDF2}
.calc .chk{display:flex;gap:10px;align-items:center;font-weight:600;margin-top:16px}.calc .chk input{width:22px;height:22px}
.calc .hint{font-size:14px;color:var(--soft);margin:4px 0 0}
.res{margin-top:22px;display:grid;gap:12px}.light{border-radius:12px;padding:16px 18px;font-weight:600}.light small{display:block;font-weight:400;margin-top:4px;font-size:15px}
.g{background:#D4EDDA;color:#0F5132}.y{background:#FFF3CD;color:#664D03}.r{background:#F8D7DA;color:#842029}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.kpi{background:#EEF3F8;border-radius:10px;padding:12px}.kpi span{display:block;font-size:13px;color:var(--soft)}.kpi b{font-size:20px;color:var(--navy)}
.bar{height:14px;background:#E3E8EE;border-radius:7px;overflow:hidden}.bar i{display:block;height:100%;background:var(--accent)}
</style>"""

# ---------------- Grenzen-Check ----------------
CHECK_FAQ=[
("Wie hoch ist die Kleinunternehmergrenze 2026?","Kleinunternehmer nach § 19 UStG ist 2026, wer im Vorjahr 2025 höchstens 25.000 Euro Gesamtumsatz (netto, ohne Umsatzsteuer) hatte und im laufenden Jahr 2026 höchstens 100.000 Euro erzielt. Die Grenzen gelten seit dem 1. Januar 2025 und sind 2026 unverändert."),
("Was passiert, wenn ich im laufenden Jahr mehr als 100.000 Euro Umsatz mache?","Die Kleinunternehmerregelung endet sofort. Bereits der Umsatz, mit dem die Grenze von 100.000 Euro überschritten wird, unterliegt der Regelbesteuerung. Ab dann musst du Umsatzsteuer ausweisen und Voranmeldungen abgeben."),
("Was passiert, wenn ich mehr als 25.000 Euro Umsatz im Jahr mache?","Im laufenden Jahr bleibst du Kleinunternehmer, solange du unter 100.000 Euro bleibst. Im Folgejahr ist die Kleinunternehmerregelung dann aber nicht mehr möglich, weil der Vorjahresumsatz über 25.000 Euro lag."),
("Was gilt im Gründungsjahr?","Im Jahr der Gründung gilt die Grenze von 25.000 Euro für das laufende Jahr. Eine Hochrechnung auf ein volles Jahr findet nicht mehr statt. Wird die Grenze überschritten, ist schon dieser Umsatz regelbesteuert."),
("Zählen die Grenzen brutto oder netto?","Seit 2025 werden die Grenzen mit dem Nettoumsatz verglichen, also ohne Umsatzsteuer. Für Kleinunternehmer entspricht das in der Regel dem Rechnungsbetrag, weil sie keine Umsatzsteuer ausweisen."),
("Welcher Umsatz zählt für die Grenzen?","Maßgeblich ist der Gesamtumsatz nach vereinnahmten Entgelten, also das tatsächlich eingenommene Geld. Umsätze aus dem Verkauf von Anlagevermögen zählen nicht mit.")]
check_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:24px">
<p class="eyebrow">Kostenloser Rechner · Stand 2026</p>
<h1 class="serif">Umsatzgrenzen-Check für Kleinunternehmer 2026</h1>
<div class="answer"><p><strong>Kurz gesagt:</strong> Kleinunternehmer nach § 19 UStG ist 2026, wer 2025 höchstens <strong>25.000 € Umsatz</strong> (netto) hatte und 2026 nicht über <strong>100.000 €</strong> kommt. Wer die 100.000 € überschreitet, verliert den Status <strong>sofort</strong>. Wer über 25.000 € kommt, ist im <strong>Folgejahr</strong> kein Kleinunternehmer mehr. Mit dem Rechner siehst du in 30 Sekunden, wo du stehst.</p></div>
</div>
<div class="wrap" style="padding-bottom:56px"><div class="split">
<div><form class="calc" id="calc" onsubmit="return false">
<label for="vj">Umsatz im Vorjahr 2025 (netto, €)</label>
<input type="text" id="vj" inputmode="decimal" placeholder="z. B. 18000" autocomplete="off">
<label for="lj">Umsatz bisher in diesem Jahr (netto, €)</label>
<input type="text" id="lj" inputmode="decimal" placeholder="z. B. 14500" autocomplete="off">
<label for="st">Stand (Datum)</label>
<input type="date" id="st">
<label class="chk"><input type="checkbox" id="gr"> Ich habe meine Tätigkeit in diesem Jahr begonnen</label>
<p class="hint">Netto = ohne Umsatzsteuer. Als Kleinunternehmer ist das meist dein Rechnungsbetrag. Die Daten bleiben in deinem Browser und werden nirgends gespeichert.</p>
<div class="res" id="res" aria-live="polite"></div>
</form></div>
<div>
<h2 class="serif" style="margin-top:0">So rechnet der Check</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Grenze</th><th>Betrag</th><th>Wenn überschritten</th></tr>
<tr><td>Vorjahr</td><td>25.000&nbsp;€</td><td>Dieses Jahr kein Kleinunternehmer</td></tr>
<tr><td>Laufendes Jahr</td><td>100.000&nbsp;€</td><td>Regelung endet sofort</td></tr>
<tr><td>Gründungsjahr</td><td>25.000&nbsp;€</td><td>Regelung endet sofort</td></tr>
<tr><td>Ausblick Folgejahr</td><td>25.000&nbsp;€</td><td>Folgejahr kein Kleinunternehmer</td></tr></table></div>
<p class="note">Die Hochrechnung aufs Jahr ist eine einfache Schätzung: bisheriger Umsatz ÷ vergangene Tage × 365.</p>
<div class="cta"><h3>Das ganze Jahr im Blick behalten</h3><p>Das Kleinunternehmer-Cockpit rechnet die Ampel automatisch mit jeder Einnahme mit – dazu Ausgaben, Gewinn, EÜR-Übersicht und Steuerrücklage.</p><a class="btn" href="cockpit.html">Zum Cockpit (19 €)</a></div>
</div></div></div>
<section class="band"><div class="wrap faq">
<h2 class="serif">Häufige Fragen zur Kleinunternehmergrenze</h2>
{faq_html(CHECK_FAQ)}
<p style="margin-top:24px">Ausführlich erklärt: <a href="kleinunternehmerregelung-grenzen.html">Kleinunternehmerregelung 2026 – alle Grenzen und Regeln</a></p>
{DISCL}
</div></section>
<script>
(function(){{
var $=function(i){{return document.getElementById(i)}};
var fmt=function(n){{return n.toLocaleString('de-DE',{{maximumFractionDigits:0}})+' €'}};
var num=function(v){{v=(v||'').replace(/\\s|€/g,'');if(v.indexOf(',')>-1)v=v.replace(/\\./g,'').replace(',','.');else if((v.match(/\\./g)||[]).length>1||/\\.\\d{{3}}$/.test(v))v=v.replace(/\\./g,'');var n=parseFloat(v);return isNaN(n)?null:n}};
var t=new Date();$('st').value=t.toISOString().slice(0,10);
function light(c,h,s){{return '<div class="light '+c+'">'+h+(s?'<small>'+s+'</small>':'')+'</div>'}}
function run(){{
 var vj=num($('vj').value),lj=num($('lj').value),gr=$('gr').checked,d=new Date($('st').value||t);
 if(gr){{$('vj').disabled=true}}else{{$('vj').disabled=false}}
 if(lj===null||(!gr&&vj===null)){{$('res').innerHTML='<p class="hint">Trag oben deine Umsätze ein – das Ergebnis erscheint sofort.</p>';return}}
 var start=new Date(d.getFullYear(),0,1),days=Math.max(1,Math.round((d-start)/864e5)+1),proj=lj/days*365;
 var lim=gr?25000:100000,pct=Math.min(100,lj/lim*100),out='';
 if(!gr&&vj>25000){{out+=light('r','Dieses Jahr kein Kleinunternehmer','Dein Vorjahresumsatz lag über 25.000 €. Die Kleinunternehmerregelung ist in diesem Jahr nicht anwendbar – du musst Umsatzsteuer ausweisen.')}}
 else if(lj>lim){{out+=light('r','Grenze überschritten – Regelung endet sofort','Bereits der Umsatz, mit dem die Grenze von '+fmt(lim)+' überschritten wurde, ist umsatzsteuerpflichtig. Sprich zeitnah mit einer Steuerberatung.')}}
 else if(pct>=80){{out+=light('y','Achtung: Grenze bald erreicht',fmt(lj)+' von '+fmt(lim)+' ausgeschöpft. Noch '+fmt(lim-lj)+' Spielraum.')}}
 else{{out+=light('g','Im grünen Bereich',fmt(lj)+' von '+fmt(lim)+' ausgeschöpft. Noch '+fmt(lim-lj)+' Spielraum.')}}
 if(!(!gr&&vj>25000)){{
  if(lj>25000)out+=light('r','Folgejahr: kein Kleinunternehmer','Du liegst dieses Jahr schon über 25.000 €. Im nächsten Jahr gilt die Regelbesteuerung – Preise und Rechnungen rechtzeitig umstellen.');
  else if(days<45)out+=light('g','Folgejahr: noch zu früh für eine Hochrechnung','Prüfe deinen Stand im Laufe des Jahres erneut – entscheidend ist, ob du am Jahresende über 25.000 € liegst.');
  else if(proj>25000)out+=light('y','Folgejahr: Grenze im Blick behalten','Hochgerechnet kommst du auf etwa '+fmt(proj)+'. Liegt dein Jahresumsatz am Ende über 25.000 €, bist du nächstes Jahr kein Kleinunternehmer.');
  else out+=light('g','Folgejahr: voraussichtlich weiter Kleinunternehmer','Hochgerechnet etwa '+fmt(proj)+' – unter 25.000 €.');
 }}
 out+='<div class="kpis"><div class="kpi"><span>Ausgeschöpft</span><b>'+pct.toFixed(1).replace('.',',')+' %</b></div><div class="kpi"><span>Hochrechnung Jahr</span><b>'+fmt(proj)+'</b></div><div class="kpi"><span>Maßgebliche Grenze</span><b>'+fmt(lim)+'</b></div></div><div class="bar" aria-hidden="true"><i style="width:'+pct+'%"></i></div>';
 $('res').innerHTML=out;
}}
['vj','lj','st','gr'].forEach(function(i){{$(i).addEventListener('input',run);$(i).addEventListener('change',run)}});run();
}})();
</script>"""
check_head=EXTRA_CSS+ld({"@context":"https://schema.org","@type":"WebApplication","name":"Umsatzgrenzen-Check für Kleinunternehmer 2026","url":"https://solovorlagen.de/grenzen-check.html",
 "applicationCategory":"FinanceApplication","operatingSystem":"Browser","inLanguage":"de-DE","offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"},
 "description":"Kostenloser Rechner: Prüft, ob du 2026 die Umsatzgrenzen der Kleinunternehmerregelung (25.000 € Vorjahr, 100.000 € laufendes Jahr) einhältst.","publisher":PUB})+ld(faq_ld(CHECK_FAQ))+ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Grenzen-Check","https://solovorlagen.de/grenzen-check.html")]))
page("Umsatzgrenzen-Check 2026: Bin ich noch Kleinunternehmer? | Solovorlagen",
 "Kostenloser Rechner: Prüfe in 30 Sekunden, ob du 2026 die Kleinunternehmergrenzen von 25.000 € und 100.000 € einhältst – mit Ausblick aufs Folgejahr.",check_body,"grenzen-check.html",check_head)

# ---------------- Ratgeber 1: Kleinunternehmerregelung ----------------
KU_FAQ=[
("Wie hoch ist die Umsatzgrenze für Kleinunternehmer 2026?","Der Gesamtumsatz des Vorjahres darf höchstens 25.000 Euro betragen haben, und im laufenden Jahr darf er 100.000 Euro nicht überschreiten. Beide Werte sind Nettobeträge ohne Umsatzsteuer und gelten seit 2025 unverändert."),
("Endet die Kleinunternehmerregelung sofort, wenn ich 100.000 Euro überschreite?","Ja. Seit 2025 endet die Regelung im laufenden Jahr sofort. Schon der Umsatz, mit dem die 100.000-Euro-Grenze überschritten wird, unterliegt der Regelbesteuerung."),
("Bin ich nächstes Jahr noch Kleinunternehmer, wenn ich dieses Jahr 30.000 Euro Umsatz mache?","Nein. Für das Folgejahr ist die Kleinunternehmerregelung nur möglich, wenn der Vorjahresumsatz höchstens 25.000 Euro betrug. Bei 30.000 Euro giltst du im nächsten Jahr als Regelunternehmer."),
("Wird im Gründungsjahr der Umsatz hochgerechnet?","Nein. Im Gründungsjahr gilt eine Grenze von 25.000 Euro für den tatsächlichen Umsatz des laufenden Jahres. Eine Hochrechnung auf ein volles Kalenderjahr findet nicht mehr statt."),
("Welcher Satz muss als Kleinunternehmer auf die Rechnung?","Ein Hinweis auf die Steuerbefreiung, zum Beispiel „Steuerfrei nach § 19 Abs. 1 UStG (Kleinunternehmerregelung)“ oder „Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“ Außerdem verlangt § 34a UStDV Name und Anschrift beider Seiten, Steuernummer oder USt-IdNr., Ausstellungsdatum, Art und Umfang der Leistung und den Gesamtbetrag. Rechnungsnummer und Leistungszeitraum sind nicht vorgeschrieben, aber empfehlenswert."),
("Müssen Kleinunternehmer E-Rechnungen ausstellen?","Nein. Kleinunternehmer müssen E-Rechnungen seit 2025 empfangen können, dürfen aber weiterhin Rechnungen als PDF oder auf Papier ausstellen."),
("Muss ich als Kleinunternehmer eine Umsatzsteuererklärung abgeben?","Seit 2025 in der Regel nicht mehr, sondern nur noch, wenn das Finanzamt dazu auffordert. Die Einkommensteuererklärung mit Einnahmen-Überschuss-Rechnung bleibt Pflicht."),
("Wie lange bin ich gebunden, wenn ich auf die Kleinunternehmerregelung verzichte?","Wer freiwillig zur Regelbesteuerung wechselt, ist daran für mindestens fünf Kalenderjahre gebunden.")]
ku_url="https://solovorlagen.de/kleinunternehmerregelung-grenzen.html"
ku_desc="Kleinunternehmerregelung 2026 einfach erklärt: Umsatzgrenzen 25.000 € und 100.000 €, was beim Überschreiten passiert, Gründungsjahr, Rechnung, E-Rechnung und Beispiele."
ku_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><article class="article">
<p class="eyebrow"><a href="ratgeber.html">Ratgeber</a> · Umsatzsteuer</p>
<h1 class="serif">Kleinunternehmerregelung 2026: Die Umsatzgrenzen einfach erklärt</h1>
{BYLINE}
<div class="answer"><p><strong>Die Antwort in Kürze:</strong> Kleinunternehmer nach § 19 UStG ist 2026, wer im Vorjahr 2025 höchstens <strong>25.000 € Umsatz</strong> hatte und im laufenden Jahr <strong>100.000 €</strong> nicht überschreitet – beides netto, also ohne Umsatzsteuer. Wird die 100.000-€-Grenze überschritten, endet die Regelung <strong>sofort</strong>: Schon der Umsatz, mit dem die Grenze überschritten wird, ist umsatzsteuerpflichtig. Wer im Jahr einen Gesamtumsatz von mehr als 25.000 € erzielt, ist im <strong>Folgejahr</strong> kein Kleinunternehmer mehr.</p></div>
<p><a href="grenzen-check.html"><strong>→ Kostenloser Umsatzgrenzen-Check:</strong> In 30 Sekunden sehen, wo du stehst.</a></p>
<nav class="toc" aria-label="Inhalt"><strong>Inhalt</strong><ol>
<li><a href="#grenzen">Welche Umsatzgrenzen gelten 2026?</a></li><li><a href="#100000">Was passiert über 100.000 €?</a></li><li><a href="#25000">Was passiert über 25.000 €?</a></li>
<li><a href="#gruendung">Was gilt im Gründungsjahr?</a></li><li><a href="#umsatz">Welcher Umsatz zählt?</a></li><li><a href="#beispiele">Drei Rechenbeispiele</a></li>
<li><a href="#rechnung">Rechnung, E-Rechnung und Steuererklärung</a></li><li><a href="#verzicht">Lohnt sich der Verzicht?</a></li><li><a href="#faq">Häufige Fragen</a></li></ol></nav>

<h2 class="serif" id="grenzen">Welche Umsatzgrenzen gelten 2026?</h2>
<p>Seit dem 1. Januar 2025 gelten neue Grenzen, die 2026 unverändert sind. Für die Kleinunternehmerregelung müssen <strong>beide</strong> Bedingungen erfüllt sein:</p>
<div class="tblwrap"><table class="tbl"><tr><th>Grenze</th><th>Betrag (netto)</th><th>Zeitraum</th><th>Folge bei Überschreiten</th></tr>
<tr><td>Vorjahresgrenze</td><td>25.000&nbsp;€</td><td>Umsatz 2025</td><td>2026 keine Kleinunternehmerregelung</td></tr>
<tr><td>Grenze laufendes Jahr</td><td>100.000&nbsp;€</td><td>Umsatz 2026</td><td>Regelung endet sofort, ab dem Umsatz, der die Grenze überschreitet</td></tr>
<tr><td>Gründungsjahr</td><td>25.000&nbsp;€</td><td>Umsatz im Jahr der Gründung</td><td>Regelung endet sofort</td></tr></table></div>
<p>Bis 2024 lagen die Grenzen bei 22.000 € (Vorjahr) und 50.000 € (laufendes Jahr, als Prognose), jeweils brutto. Seit 2025 wird mit <strong>Nettoumsätzen</strong> gerechnet, und für das laufende Jahr zählt nicht mehr die Prognose, sondern das <strong>tatsächliche Überschreiten</strong>.</p>

<h2 class="serif" id="100000">Was passiert, wenn ich im laufenden Jahr mehr als 100.000 € Umsatz mache?</h2>
<p>Die Kleinunternehmerregelung endet <strong>sofort</strong> – nicht erst zum Jahresende. Bereits der Umsatz, mit dem du die 100.000 € überschreitest, unterliegt der Regelbesteuerung. Ab diesem Zeitpunkt musst du:</p>
<ul><li>auf Rechnungen Umsatzsteuer ausweisen,</li><li>Umsatzsteuer-Voranmeldungen abgeben,</li><li>deine Preise prüfen – denn ohne Anpassung zahlst du die Umsatzsteuer aus deinem bisherigen Preis.</li></ul>
<p>Bis 2024 blieb man in diesem Fall bis Jahresende Kleinunternehmer, sofern die Umsatzprognose zu Jahresbeginn 50.000 € nicht überstieg. Diese Übergangszeit gibt es nicht mehr.</p>

<h2 class="serif" id="25000">Was passiert, wenn ich mehr als 25.000 € Umsatz mache?</h2>
<p>Im <strong>laufenden Jahr</strong> passiert zunächst nichts: Du bleibst Kleinunternehmer, solange du unter 100.000 € bleibst. Im <strong>Folgejahr</strong> ist die Kleinunternehmerregelung dann aber ausgeschlossen, weil dein Vorjahresumsatz über 25.000 € lag. Diese Grenze überrascht viele, weil sie erst im Januar spürbar wird – dann müssen Rechnungen plötzlich Umsatzsteuer enthalten.</p>
<p><strong>Tipp:</strong> Wer im Herbst merkt, dass er die 25.000 € knapp überschreiten wird, sollte frühzeitig Preise, Rechnungsvorlagen und die Kommunikation mit Stammkunden auf das neue Jahr vorbereiten.</p>

<h2 class="serif" id="gruendung">Was gilt im Gründungsjahr?</h2>
<p>Wer seine Tätigkeit im laufenden Jahr neu aufnimmt, hat noch keinen Vorjahresumsatz. Dann gilt: Der Umsatz im Gründungsjahr darf <strong>25.000 €</strong> nicht überschreiten. Eine Hochrechnung auf ein volles Jahr findet nicht mehr statt – es zählt der tatsächliche Umsatz. Wird die Grenze überschritten, endet die Regelung ebenfalls sofort.</p>

<h2 class="serif" id="umsatz">Welcher Umsatz zählt für die Grenzen?</h2>
<ul><li><strong>Gesamtumsatz nach vereinnahmten Entgelten:</strong> Maßgeblich ist das Geld, das tatsächlich eingegangen ist.</li>
<li><strong>Netto:</strong> ohne Umsatzsteuer. Als Kleinunternehmer ist das in der Regel dein Rechnungsbetrag. Bestimmte steuerfreie Hilfsumsätze werden nicht mitgezählt.</li>
<li><strong>Nicht mitgezählt</strong> werden Umsätze aus dem Verkauf von Anlagevermögen, etwa der Verkauf deines alten Firmen-Laptops.</li>
<li><strong>Alle Tätigkeiten zusammen:</strong> Die Grenze gilt pro Person, nicht pro Betrieb. Wer mehrere Gewerbe oder ein Gewerbe und eine freiberufliche Tätigkeit hat, rechnet die Umsätze zusammen.</li></ul>

<h2 class="serif" id="beispiele">Drei Rechenbeispiele</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Situation</th><th>Ergebnis</th></tr>
<tr><td><strong>Anna</strong> hatte 2025 einen Umsatz von 21.000 € und liegt 2026 bis Oktober bei 19.000 €.</td><td>2026 Kleinunternehmerin. Kommt sie bis Dezember über 25.000 €, ist sie 2027 keine Kleinunternehmerin mehr.</td></tr>
<tr><td><strong>Ben</strong> hatte 2025 einen Umsatz von 27.000 €.</td><td>2026 von Anfang an kein Kleinunternehmer – unabhängig vom Umsatz 2026.</td></tr>
<tr><td><strong>Clara</strong> hatte 2025 einen Umsatz von 24.000 € und bekommt 2026 einen Großauftrag; im September überschreitet sie 100.000 €.</td><td>Die Regelung endet im September sofort. Schon der Umsatz, mit dem sie die Grenze überschreitet, unterliegt der Regelbesteuerung. Ab da muss sie Umsatzsteuer ausweisen und ist auch 2027 keine Kleinunternehmerin.</td></tr></table></div>

<h2 class="serif" id="rechnung">Rechnung, E-Rechnung und Steuererklärung</h2>
<h3>Was muss auf die Rechnung?</h3>
<p>Kleinunternehmer-Rechnungen müssen nach § 34a UStDV mindestens enthalten: den vollständigen Namen und die Anschrift von dir und deinem Kunden, deine Steuernummer oder USt-IdNr., das Ausstellungsdatum, Menge und Art der Lieferung bzw. Art und Umfang der Leistung, den Gesamtbetrag und einen Hinweis auf die Steuerbefreiung für Kleinunternehmer, z. B. <em>„Steuerfrei nach § 19 Abs. 1 UStG (Kleinunternehmerregelung)“</em> oder <em>„Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“</em> Rechnungsnummer und Leistungszeitraum sind für Kleinunternehmer nicht vorgeschrieben, für die eigene Buchhaltung aber sehr empfehlenswert.</p>
<h3>Muss ich E-Rechnungen ausstellen?</h3>
<p>Nein. Kleinunternehmer müssen E-Rechnungen seit 2025 <strong>empfangen</strong> können, dürfen aber weiterhin PDF- oder Papierrechnungen <strong>ausstellen</strong>.</p>
<h3>Muss ich eine Umsatzsteuererklärung abgeben?</h3>
<p>Seit 2025 in der Regel nicht mehr – nur noch, wenn das Finanzamt dazu auffordert. Umsatzsteuer-Voranmeldungen entfallen ebenfalls. Die Einkommensteuererklärung mit der Einnahmen-Überschuss-Rechnung (EÜR) bleibt Pflicht.</p>

<h2 class="serif" id="verzicht">Lohnt sich der Verzicht auf die Kleinunternehmerregelung?</h2>
<p>Du kannst freiwillig zur Regelbesteuerung wechseln, bist dann aber <strong>mindestens fünf Kalenderjahre</strong> daran gebunden (§ 19 Abs. 3 UStG). Das kann sich lohnen, wenn du vor allem Geschäftskunden hast (die sich die Umsatzsteuer als Vorsteuer zurückholen) und hohe Anschaffungen planst, bei denen du selbst Vorsteuer ziehen möchtest. Für Selbstständige mit überwiegend Privatkunden ist die Kleinunternehmerregelung meist günstiger, weil ihre Preise ohne Umsatzsteuer attraktiver sind.</p>

<div class="cta"><h3>Grenzen automatisch im Blick behalten</h3><p>Das Kleinunternehmer-Cockpit ist eine Excel-Vorlage mit Umsatzgrenzen-Ampel: Einnahmen eintragen – die Ampel zeigt, wie viel der 100.000 € ausgeschöpft sind und ob die 25.000 € fürs Folgejahr kritisch werden. Dazu Ausgaben, Gewinn, EÜR-Übersicht und Steuerrücklage.</p><a class="btn" href="cockpit.html">Kleinunternehmer-Cockpit ansehen</a></div>

<h2 class="serif" id="faq">Häufige Fragen</h2>
<div class="faq" style="max-width:none">{faq_html(KU_FAQ)}</div>

<h2 class="serif">Quellen</h2>
{sources(SRC_KU)}
{DISCL}
</article></div>"""
ku_head=EXTRA_CSS+ld(article_ld("Kleinunternehmerregelung 2026: Die Umsatzgrenzen einfach erklärt",ku_desc,ku_url))+ld(faq_ld(KU_FAQ))+ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Ratgeber","https://solovorlagen.de/ratgeber.html"),("Kleinunternehmerregelung 2026","https://solovorlagen.de/kleinunternehmerregelung-grenzen.html")]))
page("Kleinunternehmerregelung 2026: Umsatzgrenzen 25.000 € und 100.000 € einfach erklärt",ku_desc,ku_body,"kleinunternehmerregelung-grenzen.html",ku_head)

# ---------------- Ratgeber 2: Stundensatz ----------------
SS_FAQ=[
("Wie berechne ich meinen Stundensatz als Selbstständiger?","Addiere deinen privaten Bedarf (Wunsch-Netto, Kranken- und Pflegeversicherung, Altersvorsorge, Versicherungen), rechne die Einkommensteuer hinzu, addiere die Betriebskosten und einen Puffer. Teile die Summe durch die Zahl der Stunden, die du im Jahr tatsächlich abrechnen kannst."),
("Wie viele Stunden kann ich als Selbstständiger im Jahr abrechnen?","Deutlich weniger als ein Angestellter arbeitet. Nach Abzug von Urlaub, Feiertagen, Krankheit und Fortbildung bleiben oft rund 200 bis 210 Arbeitstage. Davon ist nur ein Teil abrechenbar, weil Akquise, Verwaltung und Buchhaltung nicht bezahlt werden. Mit 8 Stunden pro Tag und 60 Prozent abrechenbarer Zeit sind das etwa 1.000 Stunden im Jahr."),
("Welcher Stundensatz ist für 2.500 Euro netto im Monat nötig?","Mit typischen Annahmen – 450 Euro Kranken- und Pflegeversicherung, 400 Euro Altersvorsorge und Versicherungen, 250 Euro laufende Kosten, 1.500 Euro Anschaffungen pro Jahr, 25 Prozent Steuerquote, 10 Prozent Puffer und 984 abrechenbaren Stunden – liegt der Stundensatz bei rund 65 Euro. Mit eigenen Werten kann das Ergebnis deutlich abweichen."),
("Warum ist der Stundensatz von Selbstständigen so viel höher als ein Angestellten-Stundenlohn?","Selbstständige zahlen Kranken- und Pflegeversicherung und Altersvorsorge allein, bekommen keinen bezahlten Urlaub und keine Lohnfortzahlung bei Krankheit, tragen eigene Betriebskosten und können nur einen Teil ihrer Arbeitszeit abrechnen."),
("Wie rechne ich vom Stundensatz auf den Tagessatz um?","Tagessatz = Stundensatz × abrechenbare Stunden pro Tag. Bei 65 Euro und 8 Stunden sind das 520 Euro pro Tag."),
("Was hat der Stundensatz mit der Kleinunternehmerregelung zu tun?","Wer seinen Stundensatz realistisch kalkuliert, kommt oft auf einen Jahresumsatz über 25.000 Euro. Dann ist man im Folgejahr kein Kleinunternehmer mehr und muss Umsatzsteuer zusätzlich zum Preis berechnen.")]
ss_url="https://solovorlagen.de/stundensatz-berechnen.html"
ss_desc="Stundensatz berechnen als Selbstständiger: Formel, Schritt-für-Schritt-Anleitung mit Rechenbeispiel (2.500 € netto ≈ 65 € pro Stunde), typische Fehler und Tagessatz."
rows=[("Wunsch-Nettoeinkommen","2.500 € / Monat","30.000 €"),("Kranken- und Pflegeversicherung","450 € / Monat","5.400 €"),("Altersvorsorge und Versicherungen","400 € / Monat","4.800 €"),
("= Privatbedarf","","40.200 €"),("Einkommensteuer (Annahme 25 % auf den Gewinn)","40.200 € ÷ 0,75 − 40.200 €","13.400 €"),("= nötiger Gewinn","","53.600 €"),
("Betriebskosten","250 € / Monat + 1.500 € Anschaffungen","4.500 €"),("Puffer 10 %","","5.810 €"),("= Umsatzziel pro Jahr","","63.910 €")]
tbl1="".join(f"<tr><td>{'<strong>'+a+'</strong>' if a.startswith('=') else a}</td><td>{b}</td><td>{'<strong>'+c+'</strong>' if a.startswith('=') else c}</td></tr>" for a,b,c in rows)
ss_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><article class="article">
<p class="eyebrow"><a href="ratgeber.html">Ratgeber</a> · Preise & Kalkulation</p>
<h1 class="serif">Stundensatz berechnen als Selbstständiger: Formel, Beispiel und typische Fehler</h1>
{BYLINE}
<div class="answer"><p><strong>Die Antwort in Kürze:</strong> Stundensatz = (Privatbedarf ÷ (1 − Steuerquote) + Betriebskosten) × (1 + Puffer) ÷ abrechenbare Stunden pro Jahr. Für <strong>2.500 € netto im Monat</strong> kommt man mit typischen Annahmen auf rund <strong>65 € pro Stunde</strong> bzw. 520 € pro Tag – weil Versicherungen, Steuern, Urlaub, Krankheit und unbezahlte Arbeitszeit mitbezahlt werden müssen.</p></div>
<nav class="toc" aria-label="Inhalt"><strong>Inhalt</strong><ol>
<li><a href="#formel">Die Formel</a></li><li><a href="#schritte">Schritt für Schritt mit Beispiel</a></li><li><a href="#stunden">Wie viele Stunden kann ich abrechnen?</a></li>
<li><a href="#fehler">Die 5 häufigsten Fehler</a></li><li><a href="#tagessatz">Tagessatz und Projektpreis</a></li><li><a href="#ku">Stundensatz und Kleinunternehmerregelung</a></li><li><a href="#faq">Häufige Fragen</a></li></ol></nav>

<h2 class="serif" id="formel">Die Formel für deinen Stundensatz</h2>
<p><strong>Stundensatz = Umsatzziel pro Jahr ÷ abrechenbare Stunden pro Jahr</strong></p>
<p>Das Umsatzziel setzt sich zusammen aus:</p>
<ol><li><strong>Privatbedarf:</strong> Wunsch-Netto + Kranken- und Pflegeversicherung + Altersvorsorge + weitere Versicherungen</li>
<li><strong>Steuern:</strong> Der Privatbedarf muss nach Einkommensteuer übrig bleiben → Privatbedarf ÷ (1 − Steuerquote)</li>
<li><strong>Betriebskosten:</strong> Software, Telefon, Büro, Buchhaltung, Anschaffungen</li>
<li><strong>Puffer:</strong> für Auftragsflauten, Zahlungsausfälle und Unvorhergesehenes</li></ol>

<h2 class="serif" id="schritte">Schritt für Schritt: Rechenbeispiel für 2.500 € netto</h2>
<p><strong>Schritt 1 – Umsatzziel ermitteln:</strong></p>
<div class="tblwrap"><table class="tbl"><tr><th>Posten</th><th>Annahme</th><th>pro Jahr</th></tr>{tbl1}</table></div>
<p><strong>Schritt 2 – abrechenbare Stunden ermitteln:</strong> 52 Wochen × 5 Tage = 260 Tage, abzüglich 30 Urlaubstage, 10 Feiertage, 10 Krankheitstage und 5 Fortbildungstage = <strong>205 Arbeitstage</strong>. Bei 8 Stunden pro Tag und 60 % abrechenbarer Zeit sind das <strong>984 Stunden</strong> im Jahr.</p>
<p><strong>Schritt 3 – teilen:</strong> 63.910 € ÷ 984 Stunden = <strong>64,95 € pro Stunde</strong>. Ohne Puffer wären es 59,04 €.</p>
<p>Die Steuerquote von 25 % ist eine grobe Annahme. Die tatsächliche Einkommensteuer hängt von deinem gesamten Einkommen und deinen Abzügen ab – Beiträge zur Kranken- und Altersvorsorge mindern sie zum Teil. Die Rechnung ist daher bewusst vorsichtig.</p>

<h2 class="serif" id="stunden">Wie viele Stunden kann ich wirklich abrechnen?</h2>
<p>Weniger als die meisten denken. Neben Urlaub, Feiertagen und Krankheit fällt Arbeit an, die dir niemand bezahlt: Akquise, Angebote, E-Mails, Buchhaltung, Weiterbildung. Realistisch sind oft <strong>50 bis 70 % abrechenbare Zeit</strong>. Wie stark das den Preis verändert, zeigt die Tabelle (gleiche Annahmen wie oben):</p>
<div class="tblwrap"><table class="tbl"><tr><th>Abrechenbarer Anteil</th><th>Stunden pro Jahr</th><th>Nötiger Stundensatz</th></tr>
<tr><td>40 %</td><td>656</td><td>97 €</td></tr><tr><td>50 %</td><td>820</td><td>78 €</td></tr><tr><td>60 %</td><td>984</td><td>65 €</td></tr><tr><td>70 %</td><td>1.148</td><td>56 €</td></tr><tr><td>80 %</td><td>1.312</td><td>49 €</td></tr></table></div>

<h2 class="serif" id="fehler">Die 5 häufigsten Fehler</h2>
<ol><li><strong>Den Angestellten-Stundenlohn als Maßstab nehmen.</strong> Arbeitgeber zahlen Sozialabgaben, Urlaub und Lohnfortzahlung mit – als Selbstständiger trägst du alles selbst.</li>
<li><strong>Alle Arbeitsstunden als abrechenbar rechnen.</strong> Wer mit 100 % kalkuliert, verdient bei realistischen 60 % fast 40 % weniger als geplant.</li>
<li><strong>Kranken- und Pflegeversicherung vergessen.</strong> Sie ist für viele Selbstständige einer der größten Fixkosten-Posten.</li>
<li><strong>Keine Steuern einplanen.</strong> Die Einkommensteuer wird erst nach Jahresende fällig – und trifft dann ohne Rücklage hart.</li>
<li><strong>Keinen Puffer einrechnen.</strong> Flauten, kranke Kinder oder ein ausgefallener Kunde passieren in jedem Jahr.</li></ol>

<h2 class="serif" id="tagessatz">Tagessatz und Projektpreis</h2>
<p><strong>Tagessatz = Stundensatz × Stunden pro Tag.</strong> Bei 64,95 € und 8 Stunden sind das rund 520 € pro Tag. Für Projektpreise schätzt du die Stunden pro Arbeitsschritt, addierst einen Puffer für Unvorhergesehenes (z. B. 15 %) und multiplizierst mit deinem Stundensatz: 23 geschätzte Stunden × 1,15 × 64,95 € ≈ 1.718 €.</p>

<h2 class="serif" id="ku">Stundensatz und Kleinunternehmerregelung</h2>
<p>Ein realistischer Stundensatz führt schnell zu einem Jahresumsatz über <strong>25.000 €</strong> – im Beispiel sind es knapp 64.000 €. Wer diese Grenze überschreitet, ist im Folgejahr kein Kleinunternehmer mehr und muss Umsatzsteuer zusätzlich zum Preis berechnen. Mehr dazu: <a href="kleinunternehmerregelung-grenzen.html">Kleinunternehmerregelung 2026 – die Grenzen einfach erklärt</a> und der <a href="grenzen-check.html">kostenlose Grenzen-Check</a>.</p>

<div class="cta"><h3>Deinen Stundensatz mit eigenen Zahlen berechnen</h3><p>Der Stundensatz-Rechner ist eine Excel-Vorlage: Werte eintragen, Stunden- und Tagessatz ablesen – mit Aufschlüsselung, Szenario-Tabelle und Projekt-Kalkulation für Angebote.</p><a class="btn" href="stundensatz.html">Stundensatz-Rechner ansehen</a></div>

<h2 class="serif" id="faq">Häufige Fragen</h2>
<div class="faq" style="max-width:none">{faq_html(SS_FAQ)}</div>
{DISCL}
</article></div>"""
ss_head=EXTRA_CSS+ld(article_ld("Stundensatz berechnen als Selbstständiger: Formel, Beispiel und typische Fehler",ss_desc,ss_url))+ld(faq_ld(SS_FAQ))+ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Ratgeber","https://solovorlagen.de/ratgeber.html"),("Stundensatz berechnen","https://solovorlagen.de/stundensatz-berechnen.html")]))
page("Stundensatz berechnen als Selbstständiger: Formel + Beispiel (2026) | Solovorlagen",ss_desc,ss_body,"stundensatz-berechnen.html",ss_head)

exec(open(os.path.join(HERE,"tools.py")).read())

# ---------------- Ratgeber-Übersicht ----------------
rg_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><div class="article">
<h1 class="serif">Ratgeber für Selbstständige und Kleinunternehmer</h1>
<p class="lead">Verständliche Antworten auf die Fragen, die sich Selbstständige wirklich stellen – mit Rechenbeispielen und Quellen.</p>
<div class="grid2">
<a class="pcard" href="kleinunternehmerregelung-grenzen.html"><div class="pbody"><h3>Kleinunternehmerregelung 2026: Die Umsatzgrenzen einfach erklärt</h3><p>25.000 € und 100.000 €, was beim Überschreiten passiert, Gründungsjahr, Rechnung und Beispiele.</p><div class="prow"><span class="more">Lesen →</span></div></div></a>
<a class="pcard" href="stundensatz-berechnen.html"><div class="pbody"><h3>Stundensatz berechnen als Selbstständiger</h3><p>Formel, Rechenbeispiel, abrechenbare Stunden und die 5 häufigsten Fehler.</p><div class="prow"><span class="more">Lesen →</span></div></div></a>
</div>
<h2 class="serif" id="rechner">Kostenlose Rechner</h2>
<div class="grid2">{rc_cards}</div>
</div></div>"""
page("Ratgeber für Selbstständige & Kleinunternehmer | Solovorlagen","Ratgeber für Selbstständige: Kleinunternehmerregelung 2026, Stundensatz berechnen und kostenlose Rechner – Umsatzgrenzen-Check, Rechnungstext, GWG und Fahrtkosten.",rg_body,"ratgeber.html",EXTRA_CSS)

# ---------------- sitemap, robots, llms.txt ----------------
urls=["","rechner.html","grenzen-check.html","rechnungstext-kleinunternehmer.html","gwg-rechner.html","fahrtkosten-rechner.html","kleinunternehmerregelung-grenzen.html","stundensatz-berechnen.html","ratgeber.html","paket.html","cockpit.html","rechnung.html","stundensatz.html","fahrtenbuch.html","afa.html","impressum.html","datenschutz.html"]
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>https://solovorlagen.de/{u}</loc><lastmod>{ISO}</lastmod></url>\n" for u in urls)+"</urlset>\n")
open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *\nAllow: /\n\nSitemap: https://solovorlagen.de/sitemap.xml\n")
open(os.path.join(OUT,"llms.txt"),"w").write("""# Solovorlagen
> Excel-Vorlagen und Ratgeber für Selbstständige und Kleinunternehmer in Deutschland (Stand 2026). Betreiber: Felix Merklinger-Lötzsch, Aßlar.

## Ratgeber
- [Kleinunternehmerregelung 2026: Umsatzgrenzen einfach erklärt](https://solovorlagen.de/kleinunternehmerregelung-grenzen.html): 25.000 € Vorjahr, 100.000 € laufendes Jahr (netto), sofortiges Ende bei Überschreiten, Gründungsjahr ohne Hochrechnung, Rechnungshinweis, E-Rechnung.
- [Stundensatz berechnen als Selbstständiger](https://solovorlagen.de/stundensatz-berechnen.html): Formel, Rechenbeispiel (2.500 € netto ≈ 65 €/Stunde), abrechenbare Stunden, typische Fehler.

## Werkzeuge
- [Umsatzgrenzen-Check 2026](https://solovorlagen.de/grenzen-check.html): kostenloser Online-Rechner zur Kleinunternehmergrenze.
- [Rechnungstext-Generator für Kleinunternehmer](https://solovorlagen.de/rechnungstext-kleinunternehmer.html): Hinweis nach § 19 UStG zum Kopieren, Pflichtangaben nach § 34a UStDV (Rechnungsnummer nicht Pflicht), Kleinbetragsrechnung bis 250 €.
- [GWG-Rechner 2026](https://solovorlagen.de/gwg-rechner.html): Sofortabzug bis 250 €/800 € netto, Sammelposten 250,01–1.000 € (5 × 20 %), Computer/Software Nutzungsdauer 1 Jahr, lineare AfA monatsgenau; Kleinunternehmer setzen brutto ab, Grenze gilt netto.
- [Fahrtkosten-Rechner 2026](https://solovorlagen.de/fahrtkosten-rechner.html): betriebliche Fahrten 0,30 €/km (Motorrad 0,20 €), Entfernungspauschale 0,38 € ab dem 1. km, Höchstbetrag 4.500 € (nicht bei eigenem Pkw).

## Vorlagen
- [Kleinunternehmer-Cockpit](https://solovorlagen.de/cockpit.html), [Rechnungs-Generator](https://solovorlagen.de/rechnung.html), [Stundensatz-Rechner](https://solovorlagen.de/stundensatz.html), [Fahrtenbuch](https://solovorlagen.de/fahrtenbuch.html), [AfA-Rechner](https://solovorlagen.de/afa.html), [Paket](https://solovorlagen.de/paket.html)
""")
print("content ok")
