# -*- coding: utf-8 -*-
# Zusatzseiten: Grenzen-Check, Ratgeber. Wird aus gen_site.py per exec ausgeführt (page, html, json, os, OUT verfügbar).
import json as _json, re as _re
STAND="15.10.2026"; ISO="2026-10-15"
AUTHOR={"@type":"Person","name":"Felix Merklinger-Lötzsch","url":"https://solovorlagen.de/impressum.html"}
PUB={"@type":"Organization","name":"Solovorlagen","url":"https://solovorlagen.de/","logo":"https://solovorlagen.de/img/logo.png"}
def ld(obj): return '<script type="application/ld+json">'+_json.dumps(obj,ensure_ascii=False)+'</script>'
def faq_ld(qas): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
def _nb(x): return _re.sub(r"(\d) (€|%|Euro|Prozent)",lambda m:m.group(1)+" "+m.group(2),x.replace("§ ","§ "))
def faq_html(qas): return "".join(f"<h3>{_nb(html.escape(q))}</h3><p>{_nb(html.escape(a))}</p>" for q,a in qas)
def crumbs(items): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
def article_ld(headline,desc,url,iso=None):
    iso=iso or ISO
    return {"@context":"https://schema.org","@type":"Article","headline":headline,"description":desc,"inLanguage":"de-DE",
            "datePublished":iso,"dateModified":iso,"author":AUTHOR,"publisher":PUB,"mainEntityOfPage":url}
SRC_KU=[("§ 19 UStG – Gesetzestext (dejure.org)","https://dejure.org/gesetze/UStG/19.html"),
("Deutsche Handwerks Zeitung: Kleinunternehmerregelung 2025 – BMF-Anwendungsschreiben vom 18.03.2025","https://www.deutsche-handwerks-zeitung.de/kleinunternehmerregelung-2025-anwendungsschreiben-beachten-361560/"),
("finanz.de: Kleinunternehmerregelung (Stand 02.10.2026)","https://www.finanz.de/business/kleinunternehmerregelung/"),
("steuertipps.de: Wichtige Änderungen für Kleinunternehmer ab 2025","https://www.steuertipps.de/selbststaendigkeit/wichtige-aenderungen-fuer-kleinunternehmer-ab-2025"),
("§ 34a UStDV – Rechnungen von Kleinunternehmern (dejure.org)","https://dejure.org/gesetze/UStDV/34a.html"),
("BMF-Schreiben vom 18.03.2025 zur Sonderregelung für Kleinunternehmer (PDF-Kopie)","https://www.bistum-trier.de/export/sites/portal/unser-bistum/.galleries/dokumente/2025-03-18-sonderregelung-kleinunternehmer.pdf")]
def _nb(x): return _re.sub(r"(\d) (€|%|Euro|Prozent)",lambda m:m.group(1)+" "+m.group(2),x.replace("§ ","§ "))
def sources(lst): return '<ul class="src">'+"".join(f'<li><a href="{u}" rel="noopener">{_nb(html.escape(t))}</a></li>' for t,u in lst)+'</ul>'
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
.src{font-size:15px}@media(max-width:520px){.tbl.sm{font-size:14px}.tbl.sm th,.tbl.sm td{padding:8px 7px}}.toc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 24px}.toc li{font-size:16px}
.calc{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;box-shadow:0 12px 32px rgba(31,58,95,.08)}
.calc label{display:block;font-weight:600;margin:14px 0 6px}.calc input[type=text],.calc input[type=date]{width:100%;height:54px;font-size:18px;padding:12px 14px;border:1px solid #C9D2DC;border-radius:10px;background:#FFFDF2}
.calc input[type=date]{-webkit-appearance:none;appearance:none;display:block;min-width:0;max-width:100%;line-height:1.4;text-align:left;color:inherit;font-family:inherit}
.calc input[type=date]::-webkit-date-and-time-value{text-align:left}
.calc input[type=date]::-webkit-calendar-picker-indicator{margin-left:auto}
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
("Welcher Umsatz zählt für die Grenzen?","Maßgeblich ist der Gesamtumsatz nach § 19 Abs. 2 UStG: die Summe deiner im Inland steuerbaren Umsätze nach vereinnahmten Entgelten, also das tatsächlich eingenommene Geld. Leistungen, die im Ausland steuerbar sind (z. B. viele Dienstleistungen an Unternehmen im Ausland), zählen nicht mit. Ebenfalls nicht mitgezählt werden Umsätze aus dem Verkauf von Anlagevermögen sowie bestimmte steuerfreie Umsätze: solche nach § 4 Nr. 8 Buchst. i, Nr. 9 Buchst. b und Nr. 11 bis 29 UStG (z. B. Heilbehandlungen oder Unterrichtsleistungen) und Finanz- und Grundstücksumsätze nach § 4 Nr. 8 Buchst. a bis h, Nr. 9 Buchst. a und Nr. 10 UStG, wenn sie nur Hilfsumsätze sind.")]
check_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:24px">
<p class="eyebrow">Kostenloser Rechner · Stand 2026</p>
<h1 class="serif">Umsatzgrenzen-Check für Kleinunternehmer 2026</h1>
<div class="answer"><p><strong>Kurz gesagt:</strong> Kleinunternehmer nach § 19 UStG ist 2026, wer 2025 höchstens <strong>25.000 € Umsatz</strong> (netto) hatte und 2026 nicht über <strong>100.000 €</strong> kommt. Wer die 100.000 € überschreitet, verliert den Status <strong>sofort</strong>. Wer über 25.000 € kommt, ist im <strong>Folgejahr</strong> kein Kleinunternehmer mehr. Mit dem Rechner siehst du in 30 Sekunden, wo du stehst.</p></div>
</div>
<div class="wrap" style="padding-bottom:56px"><div class="split">
<div><form class="calc" id="calc" onsubmit="return false">
<div id="vjw"><label for="vj">Umsatz im Vorjahr <span id="vjy">2025</span> (netto, €)</label>
<input type="text" id="vj" inputmode="decimal" placeholder="z. B. 18000" autocomplete="off"></div>
<label for="lj">Umsatz bisher in diesem Jahr (netto, €)</label>
<input type="text" id="lj" inputmode="decimal" placeholder="z. B. 14500" autocomplete="off">
<label for="st">Stand (Datum)</label>
<input type="date" id="st">
<label class="chk"><input type="checkbox" id="gr"> Ich habe meine Tätigkeit in diesem Jahr begonnen</label>
<div id="gdw" style="display:none"><label for="gd">Gründungsdatum (Beginn der Tätigkeit)</label><input type="date" id="gd"></div>
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
<p class="note">Die Hochrechnung aufs Jahr ist eine einfache Schätzung: bisheriger Umsatz ÷ vergangene Tage × Tage im Jahr. Im Gründungsjahr wird ab dem Gründungsdatum gerechnet: Umsatz ÷ Tage seit Gründung × Tage von der Gründung bis 31.12.</p>
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
var iso=function(d){{return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}};
var pd=function(v){{var m=/^(\\d{{4}})-(\\d{{2}})-(\\d{{2}})$/.exec(v||'');return m?new Date(+m[1],+m[2]-1,+m[3]):null}};
var t=new Date();t=new Date(t.getFullYear(),t.getMonth(),t.getDate());$('st').value=iso(t);
function light(c,h,s){{return '<div class="light '+c+'">'+h+(s?'<small>'+s+'</small>':'')+'</div>'}}
function run(){{
 var vj=num($('vj').value),lj=num($('lj').value),gr=$('gr').checked,d=pd($('st').value)||t,Y=d.getFullYear();
 $('vjy').textContent=Y-1;$('vjw').style.display=gr?'none':'block';$('gdw').style.display=gr?'block':'none';
 if((lj!==null&&lj<0)||(!gr&&vj!==null&&vj<0)){{$('res').innerHTML=light('y','Eingabe prüfen','Umsätze können nicht negativ sein.');return}}
 if(lj===null||(!gr&&vj===null)){{$('res').innerHTML='<p class="hint">Trag oben deine Umsätze ein – das Ergebnis erscheint sofort.</p>';return}}
 var start=new Date(Y,0,1),end=new Date(Y,11,31),dd=function(a,b){{return Math.round((b-a)/864e5)}},gd=null,warn='';
 if(gr){{gd=pd($('gd').value);
  if(gd&&gd.getFullYear()!==Y){{warn=light('y','Gründungsdatum prüfen','Das Gründungsdatum liegt nicht im Jahr '+Y+'. Dann ist '+Y+' nicht dein Gründungsjahr – nimm das Häkchen heraus und gib deinen Vorjahresumsatz an.');gd=null}}
  else if(gd&&gd>d){{warn=light('y','Gründungsdatum prüfen','Das Gründungsdatum liegt nach dem Stand-Datum.');gd=null}}
  if(gd)start=gd}}
 var days=Math.max(1,dd(start,d)+1),total=dd(start,end)+1,proj=lj/days*total,noproj=gr&&!gd;
 var lim=gr?25000:100000,pct=Math.min(100,lj/lim*100),out=warn;
 if(!gr&&vj>25000){{out+=light('r','Dieses Jahr kein Kleinunternehmer','Dein Vorjahresumsatz lag über 25.000 €. Die Kleinunternehmerregelung ist in diesem Jahr nicht anwendbar – du musst Umsatzsteuer ausweisen.')}}
 else if(lj>lim){{out+=light('r','Grenze überschritten – Regelung endet sofort','Bereits der Umsatz, mit dem die Grenze von '+fmt(lim)+' überschritten wurde, ist umsatzsteuerpflichtig. Sprich zeitnah mit einer Steuerberatung.')}}
 else if(pct>=80){{out+=light('y','Achtung: Grenze bald erreicht',fmt(lj)+' von '+fmt(lim)+' ausgeschöpft. Noch '+fmt(lim-lj)+' Spielraum.')}}
 else{{out+=light('g','Im grünen Bereich',fmt(lj)+' von '+fmt(lim)+' ausgeschöpft. Noch '+fmt(lim-lj)+' Spielraum.')}}
 if(!(!gr&&vj>25000)){{
  if(lj>25000)out+=light('r','Folgejahr: kein Kleinunternehmer','Du liegst dieses Jahr schon über 25.000 €. Im nächsten Jahr gilt die Regelbesteuerung – Preise und Rechnungen rechtzeitig umstellen.');
  else if(noproj)out+=light('y','Hochrechnung: Gründungsdatum fehlt','Trag oben dein Gründungsdatum ein – dann rechnet der Check ab diesem Tag bis zum 31.12. hoch.');
  else if(gr&&days<45)out+=light('g','Ausblick: noch zu früh für eine Hochrechnung','Prüfe deinen Stand im Laufe des Jahres erneut. Im Gründungsjahr endet die Regelung sofort, sobald dein Umsatz 25.000 € überschreitet.');
  else if(gr&&proj>25000)out+=light('y','Ausblick: 25.000 € könnten dieses Jahr überschritten werden','Hochgerechnet ab deinem Gründungsdatum bis zum 31.12. kommst du auf etwa '+fmt(proj)+'. Im Gründungsjahr endet die Regelung sofort mit dem Umsatz, der 25.000 € überschreitet – und im Folgejahr bist du dann auch kein Kleinunternehmer.');
  else if(gr)out+=light('g','Ausblick: voraussichtlich unter 25.000 €','Hochgerechnet ab deinem Gründungsdatum bis zum 31.12. etwa '+fmt(proj)+' – unter 25.000 €. Dann bist du voraussichtlich auch nächstes Jahr Kleinunternehmer.');
  else if(days<45)out+=light('g','Folgejahr: noch zu früh für eine Hochrechnung','Prüfe deinen Stand im Laufe des Jahres erneut – entscheidend ist, ob du am Jahresende über 25.000 € liegst.');
  else if(proj>25000)out+=light('y','Folgejahr: Grenze im Blick behalten','Hochgerechnet kommst du auf etwa '+fmt(proj)+'. Liegt dein Jahresumsatz am Ende über 25.000 €, bist du nächstes Jahr kein Kleinunternehmer.');
  else out+=light('g','Folgejahr: voraussichtlich weiter Kleinunternehmer','Hochgerechnet etwa '+fmt(proj)+' – unter 25.000 €.');
 }}
 out+='<div class="kpis"><div class="kpi"><span>Ausgeschöpft</span><b>'+pct.toFixed(1).replace('.',',')+' %</b></div><div class="kpi"><span>Hochrechnung bis 31.12.</span><b>'+(noproj?'–':fmt(proj))+'</b></div><div class="kpi"><span>Maßgebliche Grenze</span><b>'+fmt(lim)+'</b></div></div><div class="bar" aria-hidden="true"><i style="width:'+pct+'%"></i></div>';
 $('res').innerHTML=out;
}}
['vj','lj','st','gr','gd'].forEach(function(i){{$(i).addEventListener('input',run);$(i).addEventListener('change',run)}});run();
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
("Welcher Satz muss als Kleinunternehmer auf die Rechnung?","Ein Hinweis darauf, dass die Steuerbefreiung für Kleinunternehmer gilt, zum Beispiel „Steuerfreie Kleinunternehmerleistung gemäß § 19 Abs. 1 UStG.“ Verbreitet ist auch „Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“ Außerdem verlangt § 34a UStDV Name und Anschrift beider Seiten, Steuernummer oder USt-IdNr., Ausstellungsdatum, Art und Umfang der Leistung und den Gesamtbetrag. Rechnungsnummer und Leistungszeitraum sind nicht vorgeschrieben, aber empfehlenswert."),
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
<p>Maßgeblich ist der <strong>Gesamtumsatz</strong> nach § 19 Abs. 2 UStG:</p>
<ul><li><strong>Gesamtumsatz nach vereinnahmten Entgelten:</strong> Maßgeblich ist das Geld, das tatsächlich eingegangen ist.</li>
<li><strong>Netto:</strong> ohne Umsatzsteuer. Als Kleinunternehmer ist das in der Regel dein Rechnungsbetrag.</li>
<li><strong>Nur im Inland steuerbare Umsätze:</strong> Leistungen, deren Leistungsort im Ausland liegt – etwa viele Dienstleistungen an Unternehmen in anderen Ländern –, zählen nicht mit.</li>
<li><strong>Nicht mitgezählt</strong> werden Umsätze aus dem Verkauf von Anlagevermögen, etwa der Verkauf deines alten Firmen-Laptops.</li>
<li><strong>Bestimmte steuerfreie Umsätze</strong> werden abgezogen: Umsätze nach § 4 Nr. 8 Buchst. i, Nr. 9 Buchst. b und Nr. 11 bis 29 UStG (z. B. Heilbehandlungen, bestimmte Unterrichtsleistungen) sowie Finanz- und Grundstücksumsätze nach § 4 Nr. 8 Buchst. a bis h, Nr. 9 Buchst. a und Nr. 10 UStG, wenn sie nur Hilfsumsätze sind.</li>
<li><strong>Alle Tätigkeiten zusammen:</strong> Die Grenze gilt pro Person, nicht pro Betrieb. Wer mehrere Gewerbe oder ein Gewerbe und eine freiberufliche Tätigkeit hat, rechnet die Umsätze zusammen.</li></ul>

<h2 class="serif" id="beispiele">Drei Rechenbeispiele</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Situation</th><th>Ergebnis</th></tr>
<tr><td><strong>Anna</strong> hatte 2025 einen Umsatz von 21.000 € und liegt 2026 bis Oktober bei 19.000 €.</td><td>2026 Kleinunternehmerin. Kommt sie bis Dezember über 25.000 €, ist sie 2027 keine Kleinunternehmerin mehr.</td></tr>
<tr><td><strong>Ben</strong> hatte 2025 einen Umsatz von 27.000 €.</td><td>2026 von Anfang an kein Kleinunternehmer – unabhängig vom Umsatz 2026.</td></tr>
<tr><td><strong>Clara</strong> hatte 2025 einen Umsatz von 24.000 € und bekommt 2026 einen Großauftrag; im September überschreitet sie 100.000 €.</td><td>Die Regelung endet im September sofort. Schon der Umsatz, mit dem sie die Grenze überschreitet, unterliegt der Regelbesteuerung. Ab da muss sie Umsatzsteuer ausweisen und ist auch 2027 keine Kleinunternehmerin.</td></tr></table></div>

<h2 class="serif" id="rechnung">Rechnung, E-Rechnung und Steuererklärung</h2>
<h3>Was muss auf die Rechnung?</h3>
<p>Kleinunternehmer-Rechnungen müssen nach § 34a UStDV mindestens enthalten: den vollständigen Namen und die Anschrift von dir und deinem Kunden, deine Steuernummer oder USt-IdNr., das Ausstellungsdatum, Menge und Art der Lieferung bzw. Art und Umfang der Leistung, den Gesamtbetrag und einen Hinweis darauf, dass die Steuerbefreiung für Kleinunternehmer gilt, z. B. <em>„Steuerfreie Kleinunternehmerleistung gemäß § 19 Abs. 1 UStG.“</em> Verbreitet ist auch <em>„Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“</em> Fertige Formulierungen zum Kopieren gibt es im <a href="rechnungstext-kleinunternehmer.html">Rechnungstext-Generator</a>. Rechnungsnummer und Leistungszeitraum sind für Kleinunternehmer nicht vorgeschrieben, für die eigene Buchhaltung aber sehr empfehlenswert.</p>
<h3>Muss ich E-Rechnungen ausstellen?</h3>
<p>Nein. Kleinunternehmer müssen E-Rechnungen seit 2025 <strong>empfangen</strong> können, dürfen aber weiterhin PDF- oder Papierrechnungen <strong>ausstellen</strong>.</p>
<h3>Muss ich eine Umsatzsteuererklärung abgeben?</h3>
<p>Seit 2025 in der Regel nicht mehr – nur noch, wenn das Finanzamt dazu auffordert. Umsatzsteuer-Voranmeldungen entfallen ebenfalls. Die Einkommensteuererklärung mit der <a href="euer-kleinunternehmer.html">Einnahmen-Überschuss-Rechnung (EÜR)</a> bleibt Pflicht.</p>

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
("Welcher Stundensatz ist für 2.500 Euro netto im Monat nötig?","Mit typischen Annahmen für privat Versicherte – 450 Euro private Kranken- und Pflegeversicherung, 400 Euro Altersvorsorge und Versicherungen, 250 Euro laufende Kosten, 1.500 Euro Anschaffungen pro Jahr, 25 Prozent Steuerquote, 10 Prozent Puffer und 984 abrechenbaren Stunden – liegt der Stundensatz bei rund 65 Euro. Wer freiwillig gesetzlich versichert ist, zahlt rund 21 Prozent vom Gewinn für Kranken- und Pflegeversicherung; mit sonst gleichen Annahmen (kinderlos) sind dann rund 77 Euro nötig. Mit eigenen Werten kann das Ergebnis deutlich abweichen."),
("Warum ist der Stundensatz von Selbstständigen so viel höher als ein Angestellten-Stundenlohn?","Selbstständige zahlen Kranken- und Pflegeversicherung und Altersvorsorge allein, bekommen keinen bezahlten Urlaub und keine Lohnfortzahlung bei Krankheit, tragen eigene Betriebskosten und können nur einen Teil ihrer Arbeitszeit abrechnen."),
("Wie rechne ich vom Stundensatz auf den Tagessatz um?","Tagessatz = Stundensatz × Arbeitsstunden pro Tag. Bei 65 Euro und 8 Stunden sind das 520 Euro pro abgerechnetem Tag. Unbezahlte Zeit für Akquise und Verwaltung steckt bereits im Stundensatz."),
("Was hat der Stundensatz mit der Kleinunternehmerregelung zu tun?","Wer seinen Stundensatz realistisch kalkuliert, kommt oft auf einen Jahresumsatz über 25.000 Euro. Dann ist man im Folgejahr kein Kleinunternehmer mehr und muss Umsatzsteuer zusätzlich zum Preis berechnen. Im Gründungsjahr endet die Regelung sogar sofort, sobald 25.000 Euro überschritten sind, und in jedem Jahr sofort ab 100.000 Euro.")]
ss_url="https://solovorlagen.de/stundensatz-berechnen.html"
ss_desc="Stundensatz berechnen als Selbstständiger: Formel, Schritt-für-Schritt-Anleitung mit Rechenbeispiel (2.500 € netto ≈ 65 € pro Stunde, privat versichert), gesetzliche KV, typische Fehler und Tagessatz."
rows=[("Wunsch-Nettoeinkommen","2.500 € / Monat","30.000 €"),("Kranken- und Pflegeversicherung (Annahme: privat versichert)","450 € / Monat","5.400 €"),("Altersvorsorge und Versicherungen","400 € / Monat","4.800 €"),
("= Privatbedarf","","40.200 €"),("Einkommensteuer (Annahme 25 % auf den Gewinn)","40.200 € ÷ 0,75 − 40.200 €","13.400 €"),("= nötiger Gewinn","","53.600 €"),
("Betriebskosten","250 € / Monat + 1.500 € Anschaffungen","4.500 €"),("Puffer 10 %","","5.810 €"),("= Umsatzziel pro Jahr","","63.910 €")]
tbl1="".join(f"<tr><td>{'<strong>'+a+'</strong>' if a.startswith('=') else a}</td><td>{b}</td><td>{'<strong>'+c+'</strong>' if a.startswith('=') else c}</td></tr>" for a,b,c in rows)
ss_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><article class="article">
<p class="eyebrow"><a href="ratgeber.html">Ratgeber</a> · Preise & Kalkulation</p>
<h1 class="serif">Stundensatz berechnen als Selbstständiger: Formel, Beispiel und typische Fehler</h1>
{BYLINE}
<div class="answer"><p><strong>Die Antwort in Kürze:</strong> Stundensatz = (Privatbedarf ÷ (1 − Steuerquote) + Betriebskosten) × (1 + Puffer) ÷ abrechenbare Stunden pro Jahr. Für <strong>2.500 € netto im Monat</strong> kommt man mit typischen Annahmen (privat krankenversichert) auf rund <strong>65 € pro Stunde</strong> bzw. 520 € pro 8-Stunden-Tag – weil Versicherungen, Steuern, Urlaub, Krankheit und unbezahlte Arbeitszeit mitbezahlt werden müssen.</p></div>
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
<p><strong>Schritt 1 – Umsatzziel ermitteln</strong> (Beispiel: privat krankenversichert mit 450 € Monatsbeitrag):</p>
<div class="tblwrap"><table class="tbl"><tr><th>Posten</th><th>Annahme</th><th>pro Jahr</th></tr>{tbl1}</table></div>
<p><strong>Schritt 2 – abrechenbare Stunden ermitteln:</strong> 52 Wochen × 5 Tage = 260 Tage, abzüglich 30 Urlaubstage, 10 Feiertage, 10 Krankheitstage und 5 Fortbildungstage = <strong>205 Arbeitstage</strong>. Bei 8 Stunden pro Tag und 60 % abrechenbarer Zeit sind das <strong>984 Stunden</strong> im Jahr.</p>
<p><strong>Schritt 3 – teilen:</strong> 63.910 € ÷ 984 Stunden = <strong>64,95 € pro Stunde</strong>. Ohne Puffer wären es 59,04 €.</p>
<p>Die Steuerquote von 25 % ist eine grobe Annahme. Die tatsächliche Einkommensteuer hängt von deinem gesamten Einkommen und deinen Abzügen ab – Beiträge zur Kranken- und Altersvorsorge mindern sie zum Teil. Die Rechnung ist daher bewusst vorsichtig.</p>
<h3>Was ändert sich bei gesetzlicher Krankenversicherung?</h3>
<p>Die 450 € im Beispiel sind eine Annahme für eine private Krankenversicherung. Wer <strong>freiwillig gesetzlich versichert</strong> ist, zahlt keinen festen Betrag, sondern einen Prozentsatz vom Gewinn: 2026 rund <strong>21 %</strong> (ermäßigter Beitragssatz 14,0 % ohne Krankengeld bzw. 14,6 % mit Krankengeld, dazu der kassenindividuelle Zusatzbeitrag, im Durchschnitt 2,9 %, und die Pflegeversicherung mit 3,6 % bzw. 4,2 % für Kinderlose). Beitragspflichtig ist der Gewinn bis zur Beitragsbemessungsgrenze von 5.812,50 € im Monat; für sehr kleine Gewinne gilt ein Mindestbeitrag. Mit sonst gleichen Annahmen (kinderlos, durchschnittlicher Zusatzbeitrag) ergibt das im Beispiel rund <strong>1.135 € im Monat statt 450 €</strong> – der nötige Stundensatz steigt dann von 65 € auf rund <strong>77 €</strong>. Der Stundensatz-Rechner berechnet den gesetzlichen Beitrag automatisch.</p>

<h2 class="serif" id="stunden">Wie viele Stunden kann ich wirklich abrechnen?</h2>
<p>Weniger als die meisten denken. Neben Urlaub, Feiertagen und Krankheit fällt Arbeit an, die dir niemand bezahlt: Akquise, Angebote, E-Mails, Buchhaltung, Weiterbildung. Realistisch sind oft <strong>50 bis 70 % abrechenbare Zeit</strong>. Wie stark das den Preis verändert, zeigt die Tabelle (gleiche Annahmen wie oben):</p>
<div class="tblwrap"><table class="tbl"><tr><th>Abrechenbarer Anteil</th><th>Stunden pro Jahr</th><th>Nötiger Stundensatz</th></tr>
<tr><td>40 %</td><td>656</td><td>97 €</td></tr><tr><td>50 %</td><td>820</td><td>78 €</td></tr><tr><td>60 %</td><td>984</td><td>65 €</td></tr><tr><td>70 %</td><td>1.148</td><td>56 €</td></tr><tr><td>80 %</td><td>1.312</td><td>49 €</td></tr></table></div>

<h2 class="serif" id="fehler">Die 5 häufigsten Fehler</h2>
<ol><li><strong>Den Angestellten-Stundenlohn als Maßstab nehmen.</strong> Arbeitgeber zahlen Sozialabgaben, Urlaub und Lohnfortzahlung mit – als Selbstständiger trägst du alles selbst.</li>
<li><strong>Alle Arbeitsstunden als abrechenbar rechnen.</strong> Wer mit 100 % kalkuliert, aber realistisch nur 60 % abrechnen kann, macht 40 % weniger Umsatz als geplant – der Gewinn sinkt noch stärker, weil Kosten und Versicherungen gleich bleiben.</li>
<li><strong>Kranken- und Pflegeversicherung vergessen.</strong> Sie gehört zum privaten Bedarf und ist für viele Selbstständige einer der größten Posten – bei gesetzlicher Versicherung wächst sie mit dem Gewinn.</li>
<li><strong>Keine Steuern einplanen.</strong> Die Einkommensteuer wird mit dem Steuerbescheid nachgezahlt; danach setzt das Finanzamt meist vierteljährliche Vorauszahlungen fest (10. März, Juni, September, Dezember; § 37 EStG). Ohne Rücklage trifft das doppelt: Nachzahlung fürs Vorjahr plus Vorauszahlungen fürs laufende Jahr.</li>
<li><strong>Keinen Puffer einrechnen.</strong> Flauten, kranke Kinder oder ein ausgefallener Kunde passieren in jedem Jahr.</li></ol>

<h2 class="serif" id="tagessatz">Tagessatz und Projektpreis</h2>
<p><strong>Tagessatz = Stundensatz × Arbeitsstunden pro Tag.</strong> Bei 64,95 € und 8 Stunden sind das rund 520 € pro abgerechnetem Tag. Die unbezahlte Zeit für Akquise und Verwaltung steckt schon im Stundensatz, weil er mit 60 % abrechenbarer Zeit kalkuliert ist. Für Projektpreise schätzt du die Stunden pro Arbeitsschritt, addierst einen Puffer für Unvorhergesehenes (z. B. 15 %) und multiplizierst mit deinem Stundensatz: 23 geschätzte Stunden × 1,15 × 64,95 € ≈ 1.718 €.</p>

<h2 class="serif" id="ku">Stundensatz und Kleinunternehmerregelung</h2>
<p>Ein realistischer Stundensatz führt schnell zu einem Jahresumsatz über <strong>25.000 €</strong> – im Beispiel sind es knapp 64.000 €. Wer diese Grenze überschreitet, ist im Folgejahr kein Kleinunternehmer mehr und muss Umsatzsteuer zusätzlich zum Preis berechnen. Im <strong>Gründungsjahr</strong> gilt die 25.000-€-Grenze schon für das laufende Jahr: Wird sie überschritten, endet die Regelung sofort. Und unabhängig davon endet sie in jedem Jahr sofort, sobald der Umsatz <strong>100.000 €</strong> überschreitet. Mehr dazu: <a href="kleinunternehmerregelung-grenzen.html">Kleinunternehmerregelung 2026 – die Grenzen einfach erklärt</a> und der <a href="grenzen-check.html">kostenlose Grenzen-Check</a>.</p>

<div class="cta"><h3>Deinen Stundensatz mit eigenen Zahlen berechnen</h3><p>Der Stundensatz-Rechner ist eine Excel-Vorlage: Werte eintragen, Stunden- und Tagessatz ablesen – gesetzliche oder private Krankenversicherung wählbar, mit Aufschlüsselung, Szenario-Tabelle und Projekt-Kalkulation für Angebote.</p><a class="btn" href="stundensatz.html">Stundensatz-Rechner ansehen</a></div>

<h2 class="serif" id="faq">Häufige Fragen</h2>
<div class="faq" style="max-width:none">{faq_html(SS_FAQ)}</div>
{DISCL}
</article></div>"""
ss_head=EXTRA_CSS+ld(article_ld("Stundensatz berechnen als Selbstständiger: Formel, Beispiel und typische Fehler",ss_desc,ss_url))+ld(faq_ld(SS_FAQ))+ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Ratgeber","https://solovorlagen.de/ratgeber.html"),("Stundensatz berechnen","https://solovorlagen.de/stundensatz-berechnen.html")]))
page("Stundensatz berechnen als Selbstständiger: Formel + Beispiel (2026) | Solovorlagen",ss_desc,ss_body,"stundensatz-berechnen.html",ss_head)

# ---------------- Ratgeber 3: Steuerrücklage ----------------
SR_ISO="2026-10-19"; SR_STAND="19.10.2026"
SR_BYLINE=f'<p class="byline">Von <a href="impressum.html">Felix Merklinger-Lötzsch</a>, Solovorlagen · Stand: <time datetime="{SR_ISO}">{SR_STAND}</time></p>'
SR_FAQ=[
("Wie viel Prozent sollte ich als Selbstständiger für die Steuer zurücklegen?","Das hängt vom zu versteuernden Einkommen ab. Nach dem Einkommensteuertarif 2026 (Einzelveranlagung) liegt die Einkommensteuer bei 25.000 Euro zu versteuerndem Einkommen bei rund 11 Prozent, bei 40.000 Euro bei 18 Prozent und bei 60.000 Euro bei knapp 24 Prozent. Wer den passenden Satz aus der Tabelle nimmt und ein paar Prozentpunkte Puffer aufschlägt, ist meist auf der sicheren Seite."),
("Müssen Kleinunternehmer Umsatzsteuer zurücklegen?","In der Regel nicht. Kleinunternehmer nach § 19 UStG weisen keine Umsatzsteuer aus. Ausnahme: Für bestimmte Leistungen ausländischer Anbieter, etwa Werbung oder Software-Abos aus dem EU-Ausland, schulden auch sie die Umsatzsteuer selbst (Reverse-Charge, § 13b UStG). Zurücklegen müssen sie vor allem für die Einkommensteuer. Wer die Kleinunternehmerregelung verliert, muss die vereinnahmte Umsatzsteuer zusätzlich beiseitelegen, weil sie ans Finanzamt weitergeleitet wird."),
("Wann muss ich Einkommensteuer-Vorauszahlungen leisten?","Am 10. März, 10. Juni, 10. September und 10. Dezember (§ 37 EStG). Das Finanzamt setzt sie per Bescheid fest, meist auf Basis der letzten Steuerfestsetzung. Festgesetzt werden sie nur, wenn sie mindestens 400 Euro im Jahr und mindestens 100 Euro pro Termin betragen."),
("Warum ist das zweite Jahr der Selbstständigkeit oft so teuer?","Weil mit dem ersten Steuerbescheid zwei Zahlungen zusammenkommen können: die Nachzahlung für das Gründungsjahr und die Vorauszahlungen für das laufende Jahr. Wer im Gründungsjahr nichts zurückgelegt hat, muss dann beides aus den laufenden Einnahmen zahlen."),
("Zahle ich als Selbstständiger auch Gewerbesteuer?","Nur Gewerbetreibende, nicht Freiberufler. Für Einzelunternehmer gilt ein Freibetrag von 24.500 Euro Gewerbeertrag. Darüber wird die Gewerbesteuer bis zum 4-Fachen des Steuermessbetrags auf die Einkommensteuer angerechnet (§ 35 EStG). Bis zu einem Hebesatz von 400 Prozent gleicht sich das rechnerisch weitgehend aus. In vielen Großstädten liegt der Hebesatz darüber; dann bleibt ein Rest, der in die Rücklage gehört."),
("Wo sollte ich die Steuerrücklage parken?","Am besten auf einem separaten Konto, zum Beispiel einem Tagesgeldkonto, auf das du bei jedem Zahlungseingang den festen Prozentsatz überweist. So vermischt sich die Rücklage nicht mit dem Geld für laufende Ausgaben.")]
sr_url="https://solovorlagen.de/steuerruecklage-berechnen.html"
sr_desc="Wie viel Steuer sollten Selbstständige zurücklegen? Tabelle zum Tarif 2026, zwei Rechenbeispiele, Vorauszahlungstermine und die Gründer-Falle im zweiten Jahr."
sr_rows=[(15000,435,"2,9","19"),(20000,1570,"7,9","25"),(25000,2850,"11,4","26"),(30000,4217,"14,1","28"),(40000,7209,"18,0","32"),(50000,10548,"21,1","35"),(60000,14233,"23,7","39")]
sr_tbl="".join(f"<tr><td>{x:,}&nbsp;€</td><td>{e:,}&nbsp;€</td>".replace(",",".")+f"<td>{a}&nbsp;%</td><td>≈&nbsp;{g}&nbsp;%</td></tr>" for x,e,a,g in sr_rows)
sr_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><article class="article">
<p class="eyebrow"><a href="ratgeber.html">Ratgeber</a> · Steuern & Geld</p>
<h1 class="serif">Steuerrücklage berechnen: Wie viel sollten Selbstständige zurücklegen?</h1>
{SR_BYLINE}
<div class="answer"><p><strong>Die Antwort in Kürze:</strong> Lege von jedem Gewinn den Anteil zurück, der deiner voraussichtlichen <strong>Einkommensteuer</strong> entspricht – plus einen Puffer. Nach dem Tarif 2026 sind das bei&nbsp;<strong>25.000&nbsp;€</strong> zu versteuerndem Einkommen rund&nbsp;<strong>11&nbsp;%</strong>, bei&nbsp;<strong>40.000&nbsp;€</strong> rund&nbsp;<strong>18&nbsp;%</strong> und bei&nbsp;<strong>60.000&nbsp;€</strong> knapp&nbsp;<strong>24&nbsp;%</strong> (Einzelveranlagung, ohne Kirchensteuer). Kleinunternehmer müssen in der Regel keine Umsatzsteuer zurücklegen. Wichtig für Gründer: Mit dem ersten Steuerbescheid kommen oft <strong>Nachzahlung und Vorauszahlungen gleichzeitig</strong>.</p></div>
<nav class="toc" aria-label="Inhalt"><strong>Inhalt</strong><ol>
<li><a href="#warum">Warum brauche ich eine Steuerrücklage?</a></li><li><a href="#tabelle">Wie viel Prozent sind es 2026?</a></li><li><a href="#beispiele">Zwei Rechenbeispiele</a></li>
<li><a href="#vorauszahlungen">Wann werden Vorauszahlungen fällig?</a></li><li><a href="#gruender">Die Gründer-Falle im zweiten Jahr</a></li><li><a href="#weitere">Umsatzsteuer, Gewerbesteuer, Kirchensteuer</a></li>
<li><a href="#praxis">So legst du die Rücklage praktisch an</a></li><li><a href="#faq">Häufige Fragen</a></li></ol></nav>

<h2 class="serif" id="warum">Warum brauche ich als Selbstständiger eine Steuerrücklage?</h2>
<p>Angestellten wird die Lohnsteuer jeden Monat automatisch abgezogen. Selbstständige bekommen ihre Einnahmen dagegen <strong>ohne Steuerabzug</strong> – die Einkommensteuer wird erst mit dem Steuerbescheid fällig, oft viele Monate nach Jahresende. Wer das Geld bis dahin ausgegeben hat, gerät in Zahlungsnot. Die Steuerrücklage ist deshalb nichts anderes als eine selbst organisierte „Lohnsteuer“: Von jedem Euro Gewinn wandert ein fester Anteil auf die Seite.</p>

<h2 class="serif" id="tabelle">Wie viel Prozent vom Gewinn sollte ich 2026 zurücklegen?</h2>
<p>Die Einkommensteuer richtet sich nach dem <strong>zu versteuernden Einkommen</strong> – das ist dein Gewinn abzüglich Vorsorgeaufwendungen (z. B. Kranken- und Pflegeversicherung, Altersvorsorge) und weiterer Abzüge. Die Tabelle zeigt die Einkommensteuer nach dem Tarif 2026 (§&nbsp;32a&nbsp;EStG, Grundfreibetrag 12.348&nbsp;€) für eine Einzelveranlagung:</p>
<div class="tblwrap"><table class="tbl sm"><tr><th>Zu versteuern&shy;des Einkommen</th><th>Einkommen&shy;steuer 2026</th><th>Durch&shy;schnitt</th><th>Grenz&shy;steuer&shy;satz</th></tr>{sr_tbl}</table></div>
<p>Der <strong>Durchschnittssteuersatz</strong> ist der Anteil, den du vom zu versteuernden Einkommen insgesamt an Steuer zahlst – er ist die Basis für deine Rücklage. Der <strong>Grenzsteuersatz</strong> zeigt, wie viel von jedem zusätzlichen Euro an Steuer geht. Einen Solidaritätszuschlag zahlen Ledige 2026 erst, wenn die Einkommensteuer über&nbsp;20.350&nbsp;€ liegt, also ab rund&nbsp;75.000&nbsp;€ zu versteuerndem Einkommen.</p>
<p><strong>Faustregel für die Praxis:</strong> Nimm den Durchschnittssatz für dein erwartetes zu versteuerndes Einkommen und schlage ein paar Prozentpunkte Puffer auf. Weil das zu versteuernde Einkommen kleiner ist als der Gewinn, bist du damit meist auf der sicheren Seite. Bei Zusammenveranlagung mit Partner oder Partnerin oder weiteren Einkünften (etwa aus einem Angestelltenjob) kann der Satz deutlich abweichen.</p>

<h2 class="serif" id="beispiele">Zwei Rechenbeispiele</h2>
<p><strong>Lena</strong> ist Grafikdesignerin, <strong>Tom</strong> IT-Freelancer:</p>
<div class="tblwrap"><table class="tbl sm"><tr><th></th><th>Lena</th><th>Tom</th></tr>
<tr><td>Gewinn 2026</td><td>30.000&nbsp;€</td><td>54.000&nbsp;€</td></tr>
<tr><td>Abzüge (Annahme: Vorsorge, Sonderausgaben)</td><td>− 6.000&nbsp;€</td><td>− 9.000&nbsp;€</td></tr>
<tr><td><strong>Zu versteuerndes Einkommen</strong></td><td><strong>24.000&nbsp;€</strong></td><td><strong>45.000&nbsp;€</strong></td></tr>
<tr><td>Einkommensteuer 2026</td><td>2.587&nbsp;€</td><td>8.835&nbsp;€</td></tr>
<tr><td>Anteil am Gewinn</td><td>8,6&nbsp;%</td><td>16,4&nbsp;%</td></tr>
<tr><td><strong>Rücklage pro Monat</strong></td><td><strong>rund&nbsp;216&nbsp;€</strong></td><td><strong>rund&nbsp;736&nbsp;€</strong></td></tr>
<tr><td>Mit 10&nbsp;% Puffer (Anteil am Gewinn)</td><td>rund&nbsp;237&nbsp;€ (≈&nbsp;9,5&nbsp;%)</td><td>rund&nbsp;810&nbsp;€ (≈&nbsp;18&nbsp;%)</td></tr></table></div>
<p>Beide sind freiberuflich tätig (keine Gewerbesteuer), ledig, ohne Kinder, zahlen keine Kirchensteuer und haben keine weiteren Einkünfte. Mit mehr als 25.000&nbsp;€ Umsatz sind beide <strong>keine Kleinunternehmer</strong>: Die Umsatzsteuer, die sie ihren Kunden berechnen, legen sie zusätzlich und vollständig zurück – sie ist in den Zahlen oben nicht enthalten. Die Abzüge sind vereinfachte Annahmen – wie hoch sie bei dir sind, zeigt dein letzter Steuerbescheid oder eine Steuerberatung.</p>

<h2 class="serif" id="vorauszahlungen">Wann werden Einkommensteuer-Vorauszahlungen fällig?</h2>
<p>Nach dem ersten Steuerbescheid setzt das Finanzamt in der Regel <strong>vierteljährliche Vorauszahlungen</strong> fest (§&nbsp;37&nbsp;EStG). Sie sind fällig am:</p>
<div class="tblwrap"><table class="tbl"><tr><th>Termin</th><th>Fällig</th></tr><tr><td>1. Rate</td><td>10. März</td></tr><tr><td>2. Rate</td><td>10. Juni</td></tr><tr><td>3. Rate</td><td>10. September</td></tr><tr><td>4. Rate</td><td>10. Dezember</td></tr></table></div>
<p>Grundlage ist meist die Steuer aus der letzten Veranlagung. Vorauszahlungen werden nur festgesetzt, wenn sie mindestens <strong>400&nbsp;€ im Jahr</strong> und mindestens <strong>100&nbsp;€ pro Termin</strong> betragen. Steigt oder sinkt dein Gewinn deutlich, kannst du beim Finanzamt eine Anpassung beantragen – und das Finanzamt kann die Vorauszahlungen von sich aus erhöhen. Mit einer Rücklage, die zu deinem tatsächlichen Gewinn passt, bist du in beiden Fällen vorbereitet.</p>

<h2 class="serif" id="gruender">Die Gründer-Falle: Warum das zweite Jahr so teuer werden kann</h2>
<p>Im Gründungsjahr fordert das Finanzamt oft noch wenig oder nichts – Vorauszahlungen richten sich nur nach deiner Schätzung im Fragebogen zur steuerlichen Erfassung. Nach der ersten Steuererklärung kommt dann alles auf einmal:</p>
<ol><li><strong>Die Nachzahlung</strong> für das Gründungsjahr, zu zahlen innerhalb eines Monats nach Bekanntgabe des Bescheids.</li>
<li><strong>Die Vorauszahlungen</strong> für das laufende Jahr – die Beträge für bereits verstrichene Termine werden nachgefordert, ebenfalls zahlbar innerhalb eines Monats nach dem Bescheid.</li></ol>
<p>Beispiel: Lena gründet im Januar 2026 und gibt ihre Erklärung im Sommer 2027 ab. Im Herbst 2027 zahlt sie 2.587&nbsp;€ für 2026 nach und dazu die Vorauszahlungen für 2027. Ohne Rücklage fehlen ihr dann auf einen Schlag mehrere tausend Euro. Wer schon ab der ersten Rechnung zurücklegt, zahlt beides entspannt aus der Rücklage.</p>

<h2 class="serif" id="weitere">Was ist mit Umsatzsteuer, Gewerbesteuer und Kirchensteuer?</h2>
<h3>Umsatzsteuer</h3>
<p><strong>Kleinunternehmer</strong> nach §&nbsp;19&nbsp;UStG weisen keine Umsatzsteuer aus und müssen dafür in der Regel nichts zurücklegen. Ausnahme: Für bestimmte Leistungen ausländischer Anbieter, etwa Werbung oder Software-Abos von Unternehmen aus dem EU-Ausland, schulden auch Kleinunternehmer die Umsatzsteuer selbst (Reverse-Charge, §&nbsp;13b&nbsp;UStG). Wer regelbesteuert ist, zum Beispiel weil der Umsatz die <a href="kleinunternehmerregelung-grenzen.html">Kleinunternehmergrenzen</a> überschritten hat, sollte die vereinnahmte Umsatzsteuer <strong>komplett</strong> beiseitelegen – sie gehört dem Finanzamt und wird mit den Voranmeldungen abgeführt (abzüglich Vorsteuer). Ob du noch unter den Grenzen bist, zeigt der <a href="grenzen-check.html">kostenlose Grenzen-Check</a>.</p>
<h3>Gewerbesteuer</h3>
<p>Nur Gewerbetreibende zahlen Gewerbesteuer, Freiberufler nicht. Für Einzelunternehmer gilt ein <strong>Freibetrag von 24.500&nbsp;€</strong> Gewerbeertrag (§&nbsp;11&nbsp;GewStG). Darüber wird die Gewerbesteuer bis zum 4-Fachen des Steuermessbetrags auf die Einkommensteuer angerechnet (§&nbsp;35&nbsp;EStG) – bis zu einem Hebesatz von 400&nbsp;% gleicht sich das rechnerisch weitgehend aus. In vielen Großstädten liegt der Hebesatz darüber; dann bleibt ein Rest, den du zusätzlich einplanen solltest. Die Gewerbesteuer-Vorauszahlungen (15. Februar, Mai, August, November) gehören ebenfalls in die Liquiditätsplanung.</p>
<h3>Kirchensteuer und Solidaritätszuschlag</h3>
<p>Kirchenmitglieder zahlen zusätzlich <strong>8&nbsp;%</strong> (Bayern, Baden-Württemberg) bzw. <strong>9&nbsp;%</strong> (übrige Länder) der Einkommensteuer. Bei Lena wären das bei&nbsp;9&nbsp;% rund&nbsp;233&nbsp;€ im Jahr. Der Solidaritätszuschlag spielt für die meisten Selbstständigen keine Rolle (siehe oben).</p>

<h2 class="serif" id="praxis">So legst du die Rücklage praktisch an</h2>
<ol><li><strong>Satz festlegen:</strong> Durchschnittssteuersatz aus der Tabelle plus Puffer – bei Abzügen wie in den Beispielen z. B. 10–12&nbsp;% vom Gewinn bei rund&nbsp;30.000&nbsp;€ und 18–20&nbsp;% bei rund&nbsp;55.000&nbsp;€. Bei geringeren Abzügen eher etwas mehr.</li>
<li><strong>Separates Konto:</strong> Ein Tagesgeldkonto nur für Steuern, damit das Geld nicht versehentlich ausgegeben wird.</li>
<li><strong>Bei jedem Zahlungseingang überweisen:</strong> Den festen Prozentsatz der Einnahme (nach Abzug der zugehörigen Ausgaben) sofort umbuchen – oder einmal im Monat vom Monatsgewinn.</li>
<li><strong>Vierteljährlich prüfen:</strong> Passt der Satz noch zum Gewinn? Bei einem starken Jahr den Satz erhöhen, denn mit steigendem Gewinn steigt auch der Steuersatz.</li></ol>

<div class="cta"><h3>Gewinn und Steuerrücklage automatisch im Blick</h3><p>Das Kleinunternehmer-Cockpit ist eine Excel-Vorlage: Einnahmen und Ausgaben eintragen – die Vorlage zeigt deinen Gewinn, die EÜR-Übersicht, die Umsatzgrenzen-Ampel und berechnet, welchen Anteil deines Gewinns du für die Steuer zurücklegen solltest.</p><a class="btn" href="cockpit.html">Kleinunternehmer-Cockpit ansehen</a></div>

<h2 class="serif" id="faq">Häufige Fragen</h2>
<div class="faq" style="max-width:none">{faq_html(SR_FAQ)}</div>

<h2 class="serif">Quellen</h2>
{sources([("§ 32a EStG – Einkommensteuertarif ab 2026 (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__32a.html"),
("§ 37 EStG – Einkommensteuer-Vorauszahlung (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__37.html"),
("§ 35 EStG – Steuerermäßigung bei Einkünften aus Gewerbebetrieb (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__35.html"),
("§ 11 GewStG – Steuermesszahl und Freibetrag (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/gewstg/__11.html"),
("§ 3 SolZG 1995 – Freigrenze Solidaritätszuschlag (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/solzg_1995/__3.html"),
("TK: Solidaritätszuschlag 2026 – Freigrenze weiter erhöht","https://www.tk.de/firmenkunden/service/fachthemen/fachthema-beitraege/solidaritaetszuschlag-2075802"),
("§ 19 UStG – Kleinunternehmer (dejure.org)","https://dejure.org/gesetze/UStG/19.html"),
("§ 13b UStG – Leistungsempfänger als Steuerschuldner (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/ustg_1980/__13b.html"),
("§ 36 EStG – Entstehung und Tilgung der Einkommensteuer (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__36.html")])}
<p class="note">Die Steuerbeträge sind mit der Tarifformel des §&nbsp;32a&nbsp;EStG für 2026 berechnet (Einzelveranlagung, abgerundet). Die Prozentwerte zum Grenzsteuersatz sind gerundet.</p>
{DISCL}
</article></div>"""
sr_head=EXTRA_CSS+ld(article_ld("Steuerrücklage berechnen: Wie viel sollten Selbstständige zurücklegen?",sr_desc,sr_url,SR_ISO))+ld(faq_ld(SR_FAQ))+ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Ratgeber","https://solovorlagen.de/ratgeber.html"),("Steuerrücklage berechnen","https://solovorlagen.de/steuerruecklage-berechnen.html")]))
page("Steuerrücklage berechnen 2026: Wie viel Prozent? | Solovorlagen",sr_desc,sr_body,"steuerruecklage-berechnen.html",sr_head)

# ---------------- Ratgeber 4: EÜR für Kleinunternehmer ----------------
EU_ISO="2026-10-26"; EU_STAND="26.10.2026"
EU_BYLINE=f'<p class="byline">Von <a href="impressum.html">Felix Merklinger-Lötzsch</a>, Solovorlagen · Stand: <time datetime="{EU_ISO}">{EU_STAND}</time></p>'
EU_FAQ=[
("Muss ich als Kleinunternehmer eine EÜR machen?","Ja. Die Kleinunternehmerregelung befreit nur von der Umsatzsteuer, nicht von der Einkommensteuer. Den Gewinn ermitteln Kleinunternehmer in der Regel mit der Einnahmen-Überschuss-Rechnung nach § 4 Abs. 3 EStG und übermitteln sie als Anlage EÜR zusammen mit der Einkommensteuererklärung."),
("Reicht eine formlose Aufstellung statt der Anlage EÜR?","Nein. Die Einnahmen-Überschuss-Rechnung muss nach dem amtlich vorgeschriebenen Datensatz elektronisch übermittelt werden, also als Anlage EÜR, zum Beispiel über ELSTER (§ 60 Abs. 4 EStDV). Nur auf Antrag kann das Finanzamt zur Vermeidung unbilliger Härten einen Papiervordruck zulassen."),
("Trage ich als Kleinunternehmer Ausgaben brutto oder netto ein?","Brutto. Kleinunternehmer dürfen keine Vorsteuer abziehen, deshalb ist die gezahlte Umsatzsteuer Teil der Betriebsausgabe. Auch die Einnahmen trägst du mit dem tatsächlich erhaltenen Betrag ein, in die eigene Zeile für umsatzsteuerliche Kleinunternehmer."),
("Zählt bei der EÜR das Rechnungsdatum oder das Zahlungsdatum?","Das Zahlungsdatum. Einnahmen zählen in dem Jahr, in dem das Geld eingeht, Ausgaben in dem Jahr, in dem du sie bezahlst (§ 11 EStG). Ausnahmen sind regelmäßig wiederkehrende Zahlungen wie Miete oder Abos, die bis zu 10 Tage vor oder nach dem Jahreswechsel fällig sind und gezahlt werden: Sie zählen in dem Jahr, zu dem sie wirtschaftlich gehören. Bei Anschaffungen von Anlagegütern zählt das Jahr der Anschaffung, teure Anschaffungen werden über die Nutzungsdauer abgeschrieben."),
("Bis wann muss ich die EÜR für 2026 abgeben?","Zusammen mit der Einkommensteuererklärung 2026. Wer sie selbst erstellt, hat bis zum 2. August 2027 Zeit, weil der 31. Juli 2027 ein Samstag ist. Mit Steuerberatung oder Lohnsteuerhilfeverein endet die Frist am 29. Februar 2028, sofern das Finanzamt die Erklärung nicht früher anfordert."),
("Wie lange muss ich Belege aufbewahren?","Rechnungen und andere Buchungsbelege 8 Jahre, Bücher und Aufzeichnungen wie deine Einnahmen- und Ausgabenliste 10 Jahre (§ 147 Abs. 3 AO). Die Frist beginnt mit dem Ende des Kalenderjahres, in dem der Beleg entstanden bzw. die letzte Eintragung gemacht wurde.")]
eu_url="https://solovorlagen.de/euer-kleinunternehmer.html"
eu_desc="EÜR für Kleinunternehmer einfach erklärt: Zahlungsdatum statt Rechnungsdatum, Ausgaben brutto, Beispielrechnung, Anlage EÜR, Fristen und Belege."
eu_rows=[("Laptop (1.200&nbsp;€ netto)","Computer: Nutzungsdauer 1 Jahr","1.428&nbsp;€"),
("Bürostuhl (400&nbsp;€ netto)","GWG bis 800&nbsp;€ netto: sofort","476&nbsp;€"),
("Software-Abos","12 × 30&nbsp;€","360&nbsp;€"),
("Telefon und Internet (betrieblicher Anteil)","12 × 20&nbsp;€","240&nbsp;€"),
("Fahrten zu Kunden mit dem Privatauto","1.800&nbsp;km × 0,30&nbsp;€","540&nbsp;€"),
("Online-Kurs und Fachzeitschriften-Abo","im Jahr der Zahlung","290&nbsp;€"),
("Berufshaftpflicht","im Jahr der Zahlung","180&nbsp;€"),
("Kontoführung Geschäftskonto","im Jahr der Zahlung","120&nbsp;€")]
eu_tbl="".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in eu_rows)
eu_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><article class="article">
<p class="eyebrow"><a href="ratgeber.html">Ratgeber</a> · Steuern & Geld</p>
<h1 class="serif">EÜR für Kleinunternehmer: So funktioniert die Einnahmen-Überschuss-Rechnung</h1>
{EU_BYLINE}
<div class="answer"><p><strong>Die Antwort in Kürze:</strong> Auch Kleinunternehmer müssen ihren Gewinn ermitteln – mit der <strong>Einnahmen-Überschuss-Rechnung (EÜR)</strong>: Betriebseinnahmen minus Betriebsausgaben = Gewinn. Bei Einnahmen und laufenden Ausgaben zählt das <strong>Zahlungsdatum</strong>, nicht das Rechnungsdatum. Ausgaben trägst du <strong>brutto</strong> ein, weil Kleinunternehmer keine Vorsteuer abziehen. Teure Anschaffungen werden abgeschrieben. Die EÜR wird als <strong>Anlage EÜR elektronisch</strong> mit der Einkommensteuererklärung übermittelt – für 2026 bis zum 2.&nbsp;August&nbsp;2027.</p></div>
<nav class="toc" aria-label="Inhalt"><strong>Inhalt</strong><ol>
<li><a href="#wer">Wer muss eine EÜR machen?</a></li><li><a href="#zahlung">Wann zählt eine Einnahme oder Ausgabe?</a></li><li><a href="#brutto">Brutto oder netto?</a></li>
<li><a href="#ausgaben">Welche Ausgaben darf ich abziehen?</a></li><li><a href="#beispiel">Beispiel: Die EÜR einer Kleinunternehmerin</a></li><li><a href="#elster">Anlage EÜR und Fristen</a></li>
<li><a href="#belege">Belege aufbewahren</a></li><li><a href="#fehler">Die 5 häufigsten Fehler</a></li><li><a href="#faq">Häufige Fragen</a></li></ol></nav>

<h2 class="serif" id="wer">Wer muss als Kleinunternehmer eine EÜR machen?</h2>
<p>Die Kleinunternehmerregelung nach §&nbsp;19&nbsp;UStG befreit nur von der <strong>Umsatzsteuer</strong>. Einkommensteuer zahlst du trotzdem auf deinen Gewinn – und den musst du ermitteln. Freiberufler und Gewerbetreibende, die nicht zur doppelten Buchführung verpflichtet sind, tun das mit der Einnahmen-Überschuss-Rechnung nach §&nbsp;4 Abs.&nbsp;3&nbsp;EStG. Buchführungspflichtig werden Gewerbetreibende erst ab mehr als 800.000&nbsp;€ Umsatz oder 80.000&nbsp;€ Gewinn im Jahr (§&nbsp;141&nbsp;AO; die Pflicht beginnt erst nach einer Mitteilung des Finanzamts). Für Kleinunternehmer, die als Einzelunternehmer oder Freiberufler tätig sind, ist die EÜR deshalb praktisch immer der richtige Weg. Eine GmbH oder UG muss dagegen immer bilanzieren.</p>
<p>Das gilt auch <strong>nebenberuflich</strong>: Wer neben dem Angestelltenjob selbstständig ist und damit mehr als 410&nbsp;€ Einkünfte im Jahr erzielt, muss eine Einkommensteuererklärung abgeben (§&nbsp;46 Abs.&nbsp;2 Nr.&nbsp;1&nbsp;EStG) – mit EÜR.</p>

<h2 class="serif" id="zahlung">Wann zählt eine Einnahme oder Ausgabe?</h2>
<p>In der EÜR gilt das <strong>Zufluss- und Abflussprinzip</strong> (§&nbsp;11&nbsp;EStG): Eine Einnahme zählt in dem Jahr, in dem das Geld auf deinem Konto eingeht – eine Ausgabe in dem Jahr, in dem du sie bezahlst. Das Rechnungsdatum spielt keine Rolle.</p>
<ul><li><strong>Beispiel:</strong> Du stellst am 15.&nbsp;Dezember 2026 eine Rechnung über 1.200&nbsp;€, dein Kunde zahlt am 8.&nbsp;Januar 2027. Die Einnahme gehört in die EÜR <strong>2027</strong>.</li>
<li><strong>Ausnahme – die 10-Tage-Regel:</strong> Regelmäßig wiederkehrende Zahlungen wie Miete, Abos oder Versicherungsbeiträge, die kurz vor oder nach dem Jahreswechsel (bis zu 10 Tage) fällig sind <em>und</em> gezahlt werden, zählen in dem Jahr, zu dem sie wirtschaftlich gehören. Die Anfang Januar fällige, am 28.&nbsp;Dezember gezahlte Januar-Miete fürs Büro gehört also ins neue Jahr.</li>
<li><strong>Ausnahme – Anschaffungen:</strong> Für Anlagegüter – auch geringwertige Wirtschaftsgüter und Computer – zählt das Jahr der Anschaffung (Lieferung), nicht das Jahr der Zahlung. Teure Wirtschaftsgüter, etwa ein Auto oder eine Maschine, setzt du außerdem nicht auf einmal ab, sondern über die Nutzungsdauer (siehe unten).</li></ul>
<p>Das Zahlungsdatum ist übrigens auch für die <a href="kleinunternehmerregelung-grenzen.html">Umsatzgrenzen der Kleinunternehmerregelung</a> maßgeblich – dort zählen ebenfalls die vereinnahmten Entgelte.</p>

<h2 class="serif" id="brutto">Brutto oder netto: Was ist bei Kleinunternehmern anders?</h2>
<p>Regelbesteuerte Unternehmer behandeln Umsatzsteuer und Vorsteuer in der EÜR als eigene Posten. Bei Kleinunternehmern ist es einfacher:</p>
<ul><li><strong>Einnahmen:</strong> Du weist keine Umsatzsteuer aus – der Betrag, den dein Kunde zahlt, ist deine Betriebseinnahme. In der Anlage EÜR gibt es dafür eine eigene Zeile für <em>Betriebseinnahmen als umsatzsteuerlicher Kleinunternehmer</em>.</li>
<li><strong>Ausgaben:</strong> Du darfst keine Vorsteuer abziehen. Die Umsatzsteuer auf deinen Einkäufen ist deshalb Teil der Kosten – du trägst den <strong>Bruttobetrag</strong> ein (§&nbsp;9b&nbsp;EStG).</li>
<li><strong>Grenzen für Anschaffungen:</strong> Ob etwas ein geringwertiges Wirtschaftsgut ist, prüfst du trotzdem anhand des <strong>Nettopreises</strong> – abgesetzt wird dann der Bruttobetrag. Das rechnet der <a href="gwg-rechner.html">kostenlose GWG-Rechner</a> für dich aus.</li></ul>

<h2 class="serif" id="ausgaben">Welche Ausgaben darf ich als Kleinunternehmer abziehen?</h2>
<p>Betriebsausgaben sind alle Aufwendungen, die durch deine selbstständige Tätigkeit veranlasst sind. Die wichtigsten Regeln im Überblick:</p>
<div class="tblwrap"><table class="tbl sm"><tr><th>Ausgabe</th><th>So zählt sie in der EÜR</th></tr>
<tr><td>Laufende Kosten (Software, Telefon, Porto, Kontogebühren, Versicherungen für den Betrieb)</td><td>Im Jahr der Zahlung voll, als Kleinunternehmer brutto</td></tr>
<tr><td>Anschaffung bis 250&nbsp;€ netto</td><td>Im Jahr der Anschaffung voll absetzbar</td></tr>
<tr><td>Anschaffung 250,01–800&nbsp;€ netto</td><td>Im Jahr der Anschaffung voll als GWG (in einem Verzeichnis festhalten) – oder im Sammelposten (dann einheitlich für alle Anschaffungen von 250,01–1.000&nbsp;€ netto des Jahres)</td></tr>
<tr><td>Anschaffung über 800&nbsp;€ netto</td><td>Abschreibung über die Nutzungsdauer; bis 1.000&nbsp;€ netto alternativ Sammelposten (5 × 20&nbsp;%)</td></tr>
<tr><td>Computer, Laptop, Software</td><td>Nutzungsdauer 1 Jahr – im Anschaffungsjahr voll absetzbar (außer im Sammelposten)</td></tr>
<tr><td>Betriebliche Fahrten mit dem Privatauto</td><td>0,30&nbsp;€ je gefahrenem km; Weg zur ersten Betriebsstätte: 0,38&nbsp;€ je vollem Entfernungs-km (einfache Strecke)</td></tr>
<tr><td>Arbeiten von zu Hause</td><td>Homeoffice-Pauschale 6&nbsp;€ je Tag, an dem du überwiegend zu Hause arbeitest, höchstens 1.260&nbsp;€ im Jahr – oder Arbeitszimmer, wenn es der Mittelpunkt deiner Tätigkeit ist</td></tr>
<tr><td>Bewirtung von Geschäftspartnern</td><td>70&nbsp;% der angemessenen Kosten, mit Beleg und Angaben zu Anlass und Teilnehmern; getrennt von anderen Ausgaben aufzeichnen (§&nbsp;4 Abs.&nbsp;7&nbsp;EStG)</td></tr>
<tr><td>Geschenke an Geschäftspartner</td><td>Nur wenn höchstens 50&nbsp;€ je Empfänger und Jahr (Freigrenze: darüber gar nicht absetzbar; bei Kleinunternehmern einschließlich Umsatzsteuer); getrennt aufzeichnen</td></tr>
<tr><td><strong>Nicht</strong> absetzbar: Einkommensteuer, deine eigene Kranken- und Pflegeversicherung, Privatentnahmen</td><td>Gehören nicht in die EÜR. Kranken- und Pflegeversicherung und Altersvorsorge machst du als Vorsorgeaufwendungen in der Einkommensteuererklärung geltend.</td></tr></table></div>
<p>Mehr zu Fahrten: <a href="fahrtkosten-rechner.html">Fahrtkosten-Rechner 2026</a>. Mehr zu Anschaffungen: <a href="gwg-rechner.html">GWG-Rechner</a>.</p>

<h2 class="serif" id="beispiel">Beispiel: Die EÜR einer Kleinunternehmerin</h2>
<p><strong>Mia</strong> ist selbstständige Texterin. 2025 hatte sie 19.000&nbsp;€ Umsatz, ist also 2026 Kleinunternehmerin. 2026 gehen <strong>21.600&nbsp;€</strong> Honorare auf ihrem Konto ein – damit bleibt sie unter 25.000&nbsp;€ und ist auch 2027 Kleinunternehmerin. Eine Dezember-Rechnung über 1.200&nbsp;€, die erst im Januar 2027 bezahlt wird, ist in den 21.600&nbsp;€ nicht enthalten. Ihre Ausgaben 2026, alle brutto:</p>
<div class="tblwrap"><table class="tbl sm"><tr><th>Ausgabe</th><th>Regel</th><th>Betrag</th></tr>{eu_tbl}
<tr><td colspan="2"><strong>Summe Betriebsausgaben</strong></td><td><strong>3.634&nbsp;€</strong></td></tr></table></div>
<div class="tblwrap"><table class="tbl sm"><tr><th>EÜR 2026</th><th>Betrag</th></tr>
<tr><td>Betriebseinnahmen als Kleinunternehmerin</td><td>21.600&nbsp;€</td></tr>
<tr><td>− Betriebsausgaben</td><td>3.634&nbsp;€</td></tr>
<tr><td><strong>= Gewinn</strong></td><td><strong>17.966&nbsp;€</strong></td></tr></table></div>
<p>Der Laptop kostet 1.200&nbsp;€ netto, liegt also über der GWG-Grenze – als Computer hat er aber eine Nutzungsdauer von einem Jahr und ist 2026 voll absetzbar. Der Bürostuhl liegt mit 400&nbsp;€ netto unter 800&nbsp;€ und ist ebenfalls sofort absetzbar. Abgesetzt werden jeweils die Bruttobeträge. Ihre Kranken- und Pflegeversicherung und die Einkommensteuer tauchen in der EÜR nicht auf. Wie viel Mia von ihrem Gewinn für die Steuer zurücklegen sollte, zeigt der Ratgeber <a href="steuerruecklage-berechnen.html">Steuerrücklage berechnen</a>.</p>

<h2 class="serif" id="elster">Wie reiche ich die EÜR ein – und bis wann?</h2>
<p>Die EÜR wird nach amtlich vorgeschriebenem Datensatz <strong>elektronisch</strong> übermittelt (§&nbsp;60 Abs.&nbsp;4&nbsp;EStDV) – in der Praxis als <strong>Anlage EÜR</strong> über Mein ELSTER oder eine Steuersoftware, zusammen mit der Einkommensteuererklärung. Eine formlose Aufstellung reicht nicht. Nur in Härtefällen kann das Finanzamt auf Antrag einen Papiervordruck zulassen.</p>
<div class="tblwrap"><table class="tbl"><tr><th>EÜR für</th><th>Selbst erstellt</th><th>Mit Steuerberatung</th></tr>
<tr><td>2025</td><td>31.07.2026</td><td>01.03.2027</td></tr>
<tr><td>2026</td><td>02.08.2027</td><td>29.02.2028</td></tr></table></div>
<p>Fällt das Fristende auf ein Wochenende oder einen Feiertag, verschiebt es sich auf den nächsten Werktag – deshalb der 2.&nbsp;August&nbsp;2027 und der 1.&nbsp;März&nbsp;2027. Eine <strong>Umsatzsteuererklärung</strong> müssen Kleinunternehmer ab dem Steuerjahr 2025 in der Regel nicht mehr abgeben, nur noch auf Aufforderung des Finanzamts. Die Frist für 2025 ist bereits abgelaufen – wer noch nicht abgegeben hat, sollte das zügig nachholen, sonst kann ein Verspätungszuschlag festgesetzt werden.</p>
<p><strong>Tipp:</strong> Wer seine Einnahmen und Ausgaben übers Jahr nach den Kategorien der Anlage EÜR sortiert, muss am Ende nur noch die Summen in ELSTER übertragen.</p>

<h2 class="serif" id="belege">Wie lange muss ich Belege aufbewahren?</h2>
<p>Seit 2025 gelten verkürzte Fristen (§&nbsp;147 Abs.&nbsp;3&nbsp;AO): <strong>Rechnungen und andere Buchungsbelege 8 Jahre</strong>, <strong>Bücher und Aufzeichnungen</strong> – etwa deine Einnahmen- und Ausgabenliste – <strong>10 Jahre</strong>. Die Frist beginnt jeweils mit dem Ende des Kalenderjahres, in dem der Beleg entstanden ist bzw. die letzte Eintragung gemacht wurde. Digitale Belege bewahrst du digital auf.</p>

<h2 class="serif" id="fehler">Die 5 häufigsten Fehler in der EÜR</h2>
<ol><li><strong>Rechnungsdatum statt Zahlungsdatum.</strong> Eine im Dezember geschriebene, im Januar bezahlte Rechnung gehört ins neue Jahr.</li>
<li><strong>Ausgaben netto eintragen.</strong> Kleinunternehmer verschenken so die Umsatzsteuer, die sie selbst bezahlt haben.</li>
<li><strong>Private Kosten in die EÜR schreiben.</strong> Einkommensteuer, die eigene Kranken- und Pflegeversicherung und Privatentnahmen sind keine Betriebsausgaben.</li>
<li><strong>Teure Anschaffungen sofort voll absetzen.</strong> Über 800&nbsp;€ netto (außer Computer und Software) wird abgeschrieben – bis 1.000&nbsp;€ netto alternativ über den Sammelposten.</li>
<li><strong>Belege nicht sammeln.</strong> Ohne Beleg erkennt das Finanzamt eine Ausgabe im Zweifel nicht an – am besten jeden Beleg gleich ablegen.</li></ol>

<div class="cta"><h3>Einnahmen, Ausgaben und EÜR-Übersicht in einer Datei</h3><p>Das Kleinunternehmer-Cockpit ist eine Excel-Vorlage: Einnahmen mit Zahlungsdatum und Ausgaben eintragen – die EÜR-Übersicht summiert alles nach 20 Kategorien als Grundlage für die Anlage EÜR in ELSTER. Dazu Umsatzgrenzen-Ampel und Steuerrücklage. Für Abschreibungen gibt es das <a href="afa.html" style="color:#fff">Anlagenverzeichnis &amp; den AfA-Rechner</a>.</p><a class="btn" href="cockpit.html">Kleinunternehmer-Cockpit ansehen</a></div>

<h2 class="serif" id="faq">Häufige Fragen</h2>
<div class="faq" style="max-width:none">{faq_html(EU_FAQ)}</div>

<h2 class="serif">Quellen</h2>
{sources([("§ 4 EStG – Gewinnbegriff, Abs. 3 Einnahmen-Überschuss-Rechnung, Abs. 5 nicht abziehbare Betriebsausgaben (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__4.html"),
("§ 11 EStG – Zufluss und Abfluss (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__11.html"),
("§ 6 EStG – Bewertung, Abs. 2 GWG und Abs. 2a Sammelposten (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__6.html"),
("§ 9b EStG – Umsatzsteuerrechtlicher Vorsteuerabzug (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__9b.html"),
("§ 46 EStG – Veranlagung bei Bezug von Einkünften aus nichtselbständiger Arbeit (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estg/__46.html"),
("§ 60 EStDV – Unterlagen zur Steuererklärung (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/estdv_1955/__60.html"),
("§ 141 AO – Buchführungspflicht bestimmter Steuerpflichtiger (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/ao_1977/__141.html"),
("§ 147 AO – Ordnungsvorschriften für die Aufbewahrung von Unterlagen (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/ao_1977/__147.html"),
("§ 149 AO – Abgabe der Steuererklärungen (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/ao_1977/__149.html"),
("§ 19 UStG – Besteuerung der Kleinunternehmer (gesetze-im-internet.de)","https://www.gesetze-im-internet.de/ustg_1980/__19.html"),
("Finanzamt Baden-Württemberg: Abgabefristen für die Jahre 2023–2027","https://finanzamt-bw.fv-bwl.de/,Lde/9361700")])}
{DISCL}
</article></div>"""
eu_head=EXTRA_CSS+ld(article_ld("EÜR für Kleinunternehmer: So funktioniert die Einnahmen-Überschuss-Rechnung",eu_desc,eu_url,EU_ISO))+ld(faq_ld(EU_FAQ))+ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Ratgeber","https://solovorlagen.de/ratgeber.html"),("EÜR für Kleinunternehmer","https://solovorlagen.de/euer-kleinunternehmer.html")]))
page("EÜR für Kleinunternehmer: Anleitung mit Beispiel | Solovorlagen",eu_desc,eu_body,"euer-kleinunternehmer.html",eu_head)

exec(open(os.path.join(HERE,"tools.py")).read())

# ---------------- Ratgeber-Übersicht ----------------
rg_body=f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><div class="article">
<h1 class="serif">Ratgeber für Selbstständige und Kleinunternehmer</h1>
<p class="lead">Verständliche Antworten auf die Fragen, die sich Selbstständige wirklich stellen – mit Rechenbeispielen und Quellen.</p>
<div class="grid2">
<a class="pcard" href="kleinunternehmerregelung-grenzen.html"><div class="pbody"><h3>Kleinunternehmerregelung 2026: Die Umsatzgrenzen einfach erklärt</h3><p>25.000 € und 100.000 €, was beim Überschreiten passiert, Gründungsjahr, Rechnung und Beispiele.</p><div class="prow"><span class="more">Lesen →</span></div></div></a>
<a class="pcard" href="stundensatz-berechnen.html"><div class="pbody"><h3>Stundensatz berechnen als Selbstständiger</h3><p>Formel, Rechenbeispiel, abrechenbare Stunden und die 5 häufigsten Fehler.</p><div class="prow"><span class="more">Lesen →</span></div></div></a>
<a class="pcard" href="steuerruecklage-berechnen.html"><div class="pbody"><h3>Steuerrücklage berechnen: Wie viel zurücklegen?</h3><p>Prozentsätze nach dem Tarif 2026, zwei Rechenbeispiele, Vorauszahlungen und die Gründer-Falle.</p><div class="prow"><span class="more">Lesen →</span></div></div></a>
<a class="pcard" href="euer-kleinunternehmer.html"><div class="pbody"><h3>EÜR für Kleinunternehmer: So funktioniert die Einnahmen-Überschuss-Rechnung</h3><p>Zahlungsdatum statt Rechnungsdatum, Ausgaben brutto, was absetzbar ist, Beispielrechnung, Anlage EÜR und Fristen.</p><div class="prow"><span class="more">Lesen →</span></div></div></a>
</div>
<h2 class="serif" id="rechner">Kostenlose Rechner</h2>
<div class="grid2">{rc_cards}</div>
</div></div>"""
page("Ratgeber für Selbstständige & Kleinunternehmer | Solovorlagen","Ratgeber für Selbstständige: Kleinunternehmerregelung 2026, Stundensatz, Steuerrücklage, EÜR und kostenlose Rechner – Umsatzgrenzen-Check, Rechnungstext, GWG und Fahrtkosten.",rg_body,"ratgeber.html",EXTRA_CSS)

# ---------------- sitemap, robots, llms.txt ----------------
urls=["","rechner.html","grenzen-check.html","rechnungstext-kleinunternehmer.html","gwg-rechner.html","fahrtkosten-rechner.html","kleinunternehmerregelung-grenzen.html","stundensatz-berechnen.html","steuerruecklage-berechnen.html","euer-kleinunternehmer.html","ratgeber.html","paket.html","cockpit.html","rechnung.html","stundensatz.html","fahrtenbuch.html","afa.html"]
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>https://solovorlagen.de/{u}</loc><lastmod>{EU_ISO if u in ("euer-kleinunternehmer.html","ratgeber.html","rechnungstext-kleinunternehmer.html","gwg-rechner.html","fahrtkosten-rechner.html") else SR_ISO if u=="steuerruecklage-berechnen.html" else ISO}</lastmod></url>\n" for u in urls)+"</urlset>\n")
open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *\nAllow: /\n\nSitemap: https://solovorlagen.de/sitemap.xml\n")
open(os.path.join(OUT,"llms.txt"),"w").write("""# Solovorlagen
> Excel-Vorlagen und Ratgeber für Selbstständige und Kleinunternehmer in Deutschland (Stand 2026). Betreiber: Felix Merklinger-Lötzsch, Aßlar.

## Ratgeber
- [Kleinunternehmerregelung 2026: Umsatzgrenzen einfach erklärt](https://solovorlagen.de/kleinunternehmerregelung-grenzen.html): 25.000 € Vorjahr, 100.000 € laufendes Jahr (netto), sofortiges Ende bei Überschreiten, Gründungsjahr 25.000 € ohne Hochrechnung, Rechnungshinweis, E-Rechnung.
- [Stundensatz berechnen als Selbstständiger](https://solovorlagen.de/stundensatz-berechnen.html): Formel, Rechenbeispiel (2.500 € netto ≈ 65 €/Stunde bei privater KV, mit gesetzlicher KV rund 77 €), abrechenbare Stunden, typische Fehler.
- [Steuerrücklage berechnen](https://solovorlagen.de/steuerruecklage-berechnen.html): Einkommensteuer 2026 nach § 32a EStG (Grundfreibetrag 12.348 €; Durchschnitt ca. 11 % bei 25.000 €, 18 % bei 40.000 €, 24 % bei 60.000 € zvE, Einzelveranlagung), Vorauszahlungen 10.3./10.6./10.9./10.12., Gründer-Falle Nachzahlung + Vorauszahlung, Kleinunternehmer ohne USt-Rücklage.
- [EÜR für Kleinunternehmer](https://solovorlagen.de/euer-kleinunternehmer.html): Einnahmen-Überschuss-Rechnung nach § 4 Abs. 3 EStG, Zufluss-/Abflussprinzip (§ 11 EStG, 10-Tage-Regel), Kleinunternehmer tragen Ausgaben brutto ein, GWG-Grenzen netto, Beispiel (21.600 € Einnahmen, 3.634 € Ausgaben, 17.966 € Gewinn), Anlage EÜR elektronisch (§ 60 Abs. 4 EStDV), Fristen 2026: 02.08.2027 bzw. 29.02.2028 mit Beratung, Belege 8 Jahre / Aufzeichnungen 10 Jahre.

## Werkzeuge
- [Umsatzgrenzen-Check 2026](https://solovorlagen.de/grenzen-check.html): kostenloser Online-Rechner zur Kleinunternehmergrenze.
- [Rechnungstext-Generator für Kleinunternehmer](https://solovorlagen.de/rechnungstext-kleinunternehmer.html): Hinweis „Steuerfreie Kleinunternehmerleistung gemäß § 19 Abs. 1 UStG“ zum Kopieren, Pflichtangaben nach § 34a UStDV (Rechnungsnummer nicht Pflicht), Kleinbetragsrechnung bis 250 €.
- [GWG-Rechner 2026](https://solovorlagen.de/gwg-rechner.html): Sofortabzug bis 250 €/800 € netto, Sammelposten 250,01–1.000 € (5 × 20 %), Computer/Software Nutzungsdauer 1 Jahr (außer bei Sammelposten), lineare AfA monatsgenau; Kleinunternehmer setzen brutto ab, Grenze gilt netto.
- [Fahrtkosten-Rechner 2026](https://solovorlagen.de/fahrtkosten-rechner.html): betriebliche Fahrten 0,30 €/km (Motorrad 0,20 €), Entfernungspauschale 0,38 € je vollem km ab dem 1. km, Höchstbetrag 4.500 € (nicht bei eigenem Pkw, bei Motorrad immer); nur für Fahrzeuge im Privatvermögen.

## Vorlagen
- [Kleinunternehmer-Cockpit](https://solovorlagen.de/cockpit.html), [Rechnungs-Generator](https://solovorlagen.de/rechnung.html), [Stundensatz-Rechner](https://solovorlagen.de/stundensatz.html), [Fahrtenbuch](https://solovorlagen.de/fahrtenbuch.html), [AfA-Rechner](https://solovorlagen.de/afa.html), [Paket](https://solovorlagen.de/paket.html)
""")
exec(open(os.path.join(HERE,"feeds.py")).read())
print("content ok")
