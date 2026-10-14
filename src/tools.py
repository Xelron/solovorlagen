# Kostenlose Mini-Rechner – wird von content.py per exec() geladen (nutzt page, ld, faq_ld, faq_html, crumbs, sources, EXTRA_CSS, DISCL, PUB)

TOOL_CSS = """<style>
.calc select,.calc textarea{width:100%;font-size:17px;padding:12px 14px;border:1px solid #C9D2DC;border-radius:10px;background:#FFFDF2;font-family:inherit}
.calc textarea{min-height:72px;resize:vertical}
.calc .row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.calc .row2>div{min-width:0}
@media(max-width:520px){.calc .row2{grid-template-columns:1fr}}
.seg{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}.seg label{display:flex;align-items:center;gap:6px;font-weight:500;margin:0;background:#EEF3F8;padding:8px 12px;border-radius:8px;cursor:pointer}
.copybox{background:#F6F7F4;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:10px 0;display:flex;gap:12px;align-items:flex-start;justify-content:space-between}
.copybox p{margin:0;font-size:16px;overflow-wrap:anywhere}.copybox button,.cbtn{flex:none;background:var(--navy);color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;font-weight:600;cursor:pointer}
.cbtn{margin-top:10px}
.pre{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;background:#fff;border:1px dashed #C9D2DC;border-radius:10px;padding:14px;overflow-wrap:anywhere}
.checks{list-style:none;padding:0;margin:8px 0}.checks li{padding:6px 0 6px 30px;position:relative;font-size:16px}
.checks li:before{position:absolute;left:0;top:5px;width:22px;height:22px;border-radius:50%;text-align:center;line-height:22px;font-size:13px;font-weight:700}
.checks li.ok:before{content:"✓";background:#D4EDDA;color:#0F5132}.checks li.no:before{content:"!";background:#FFF3CD;color:#664D03}.checks li.na:before{content:"–";background:#E3E8EE;color:#5A6573}
.yt{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}.yt td,.yt th{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left}.yt td:last-child,.yt th:last-child{text-align:right}
</style>"""

NUM_JS = r"""var $=function(i){return document.getElementById(i)};
var eur=function(n){return n.toLocaleString('de-DE',{minimumFractionDigits:2,maximumFractionDigits:2})+' €'};
var num=function(v){v=(v||'').replace(/\s|€/g,'');if(v.indexOf(',')>-1)v=v.replace(/\./g,'').replace(',','.');else if((v.match(/\./g)||[]).length>1||/\.\d{3}$/.test(v))v=v.replace(/\./g,'');var n=parseFloat(v);return isNaN(n)?null:n};
function light(c,h,s){return '<div class="light '+c+'">'+h+(s?'<small>'+s+'</small>':'')+'</div>'}
function esc(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function copy(txt,btn){var done=function(){var o=btn.textContent;btn.textContent='Kopiert ✓';setTimeout(function(){btn.textContent=o},1500)};
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(txt).then(done,function(){fb()})}else fb();
 function fb(){var t=document.createElement('textarea');t.value=txt;document.body.appendChild(t);t.select();try{document.execCommand('copy');done()}catch(e){}document.body.removeChild(t)}}
"""

def webapp_ld(name, url, desc):
    return {"@context":"https://schema.org","@type":"WebApplication","name":name,"url":url,"applicationCategory":"FinanceApplication",
            "operatingSystem":"Browser","inLanguage":"de-DE","offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"},"description":desc,"publisher":PUB}

def tool_page(slug, title, desc, appname, body, faq, crumbname):
    url = "https://solovorlagen.de/" + slug
    head = EXTRA_CSS + TOOL_CSS + ld(webapp_ld(appname, url, desc)) + ld(faq_ld(faq)) + ld(crumbs([("Solovorlagen","https://solovorlagen.de/"),("Rechner","https://solovorlagen.de/rechner.html"),(crumbname,url)]))
    page(title, desc, body, slug, head)

# =====================================================================
# 1) Rechnungstext-Generator für Kleinunternehmer
# =====================================================================
RT_FAQ = [
("Welcher Hinweis muss als Kleinunternehmer auf die Rechnung?","Die Rechnung muss einen Hinweis enthalten, dass die Steuerbefreiung für Kleinunternehmer nach § 19 UStG angewendet wird – zum Beispiel: „Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“ Eine bestimmte Formulierung schreibt das Gesetz nicht vor; entscheidend ist, dass der Bezug auf die Kleinunternehmerregelung klar ist."),
("Welche Pflichtangaben braucht eine Kleinunternehmer-Rechnung?","Seit 2025 regelt § 34a UStDV die Mindestangaben: vollständiger Name und Anschrift von dir und deinem Kunden, deine Steuernummer oder USt-IdNr. (oder Kleinunternehmer-Identifikationsnummer), das Ausstellungsdatum, Menge und Art der Lieferung bzw. Art und Umfang der Leistung, der zu zahlende Betrag und der Hinweis auf die Steuerbefreiung für Kleinunternehmer."),
("Brauche ich als Kleinunternehmer eine Rechnungsnummer?","Nach § 34a UStDV ist eine Rechnungsnummer für Kleinunternehmer-Rechnungen nicht vorgeschrieben, ebenso wenig ein Leistungsdatum. Für eine saubere Buchhaltung sind fortlaufende, eindeutige Rechnungsnummern trotzdem dringend zu empfehlen."),
("Darf ich Umsatzsteuer auf der Rechnung ausweisen?","Nein. Als Kleinunternehmer darfst du keine Umsatzsteuer ausweisen. Weist du sie trotzdem aus, schuldest du den ausgewiesenen Betrag dem Finanzamt (§ 14c UStG)."),
("Was gilt bei Rechnungen bis 250 Euro?","Bei Kleinbetragsrechnungen bis 250 Euro (Gesamtbetrag) sind die Angaben zum Kunden nicht erforderlich. Name und Anschrift von dir, Datum, Leistung, Betrag und der Hinweis auf § 19 UStG gehören aber auch hier drauf."),
("Muss ich als Kleinunternehmer E-Rechnungen schreiben?","Nein. Kleinunternehmer sind von der Pflicht zur Ausstellung von E-Rechnungen ausgenommen und dürfen weiter PDF- oder Papierrechnungen schreiben. Empfangen können musst du E-Rechnungen aber – dafür reicht ein E-Mail-Postfach."),
]
RT_HINTS = [
 "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.",
 "Steuerfreie Kleinunternehmerleistung gemäß § 19 Abs. 1 UStG.",
 "Kein Ausweis von Umsatzsteuer, da Kleinunternehmer gemäß § 19 UStG.",
]
rt_hints_html = "".join(f'<div class="copybox"><p id="h{i}">{t}</p><button type="button" data-copy="h{i}">Kopieren</button></div>' for i,t in enumerate(RT_HINTS))
rt_body = f"""<div class="wrap" style="padding-top:40px;padding-bottom:24px">
<p class="eyebrow">Kostenloser Generator · Stand 2026</p>
<h1 class="serif">Rechnung als Kleinunternehmer: Hinweis-Text &amp; Pflichtangaben-Check</h1>
<div class="answer"><p><strong>Kurz gesagt:</strong> Auf jede Rechnung eines Kleinunternehmers gehört ein Hinweis auf die Steuerbefreiung, z.&nbsp;B. <strong>„Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“</strong> Dazu kommen nach <strong>§ 34a UStDV</strong>: Name und Anschrift von dir und deinem Kunden, deine Steuernummer, das Rechnungsdatum, die Leistung und der Betrag. Eine Rechnungsnummer ist nicht vorgeschrieben, aber empfehlenswert.</p></div>
<h2 class="serif" style="margin-top:28px">Hinweis-Text zum Kopieren</h2>
{rt_hints_html}
</div>
<div class="wrap" style="padding-bottom:56px"><div class="split">
<div><form class="calc" onsubmit="return false">
<h2 class="serif" style="margin-top:0;font-size:24px">Rechnungstext erstellen und prüfen</h2>
<label for="sn">Dein Name / Firma</label><input type="text" id="sn" placeholder="z. B. Lena Beispiel Design">
<label for="sa">Deine Anschrift</label><input type="text" id="sa" placeholder="Musterweg 1, 12345 Musterstadt">
<label for="st">Steuernummer oder USt-IdNr.</label><input type="text" id="st" placeholder="z. B. 012/345/67890">
<label for="kn">Kunde (Name / Firma)</label><input type="text" id="kn" placeholder="z. B. Muster GmbH">
<label for="ka">Anschrift des Kunden</label><input type="text" id="ka" placeholder="Kundenstraße 5, 54321 Kundenstadt">
<div class="row2"><div><label for="dt">Rechnungsdatum</label><input type="date" id="dt"></div><div><label for="nr">Rechnungsnummer (empfohlen)</label><input type="text" id="nr" placeholder="RE-2026-001"></div></div>
<label for="ls">Leistung (Art und Umfang)</label><textarea id="ls" placeholder="z. B. Gestaltung Logo inkl. 2 Korrekturschleifen"></textarea>
<div class="row2"><div><label for="ld">Leistungszeitraum (optional)</label><input type="text" id="ld" placeholder="z. B. Oktober 2026"></div><div><label for="bt">Betrag (€)</label><input type="text" id="bt" inputmode="decimal" placeholder="z. B. 480"></div></div>
<label for="hv">Hinweis</label><select id="hv">{"".join(f'<option>{t}</option>' for t in RT_HINTS)}</select>
<p class="hint">Alles bleibt in deinem Browser – nichts wird gespeichert oder übertragen.</p>
<div class="res" id="res" aria-live="polite"></div>
</form></div>
<div>
<h2 class="serif" style="margin-top:0">Pflichtangaben nach § 34a UStDV</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Angabe</th><th>Pflicht?</th></tr>
<tr><td>Name und Anschrift von dir</td><td>Ja</td></tr>
<tr><td>Name und Anschrift des Kunden</td><td>Ja (bis 250 € nicht)</td></tr>
<tr><td>Steuernummer oder USt-IdNr.</td><td>Ja (bis 250 € nicht)</td></tr>
<tr><td>Ausstellungsdatum</td><td>Ja</td></tr>
<tr><td>Leistung: Art und Umfang / Menge</td><td>Ja</td></tr>
<tr><td>Zu zahlender Betrag</td><td>Ja</td></tr>
<tr><td>Hinweis auf § 19 UStG</td><td>Ja</td></tr>
<tr><td>Rechnungsnummer</td><td>Nein – empfohlen</td></tr>
<tr><td>Leistungsdatum</td><td>Nein – empfohlen</td></tr></table></div>
<div class="cta"><h3>Rechnungen nicht mehr von Hand schreiben</h3><p>Der Rechnungs-Generator füllt Kunden, Positionen und den § 19-Hinweis automatisch aus, führt dein Rechnungsbuch mit offenen Posten und erstellt Zahlungserinnerungen.</p><a class="btn" href="rechnung.html">Zum Rechnungs-Generator (15 €)</a></div>
</div></div></div>
<section class="band"><div class="wrap faq">
<h2 class="serif">Häufige Fragen zur Kleinunternehmer-Rechnung</h2>
{faq_html(RT_FAQ)}
<h3>Quellen</h3>{sources([("§ 34a UStDV – Rechnungen von Kleinunternehmern","https://www.gesetze-im-internet.de/ustdv_1980/__34a.html"),("§ 33 UStDV – Rechnungen über Kleinbeträge","https://www.gesetze-im-internet.de/ustdv_1980/__33.html"),("§ 19 UStG – Besteuerung der Kleinunternehmer","https://dejure.org/gesetze/UStG/19.html")])}
<p style="margin-top:24px">Mehr dazu: <a href="kleinunternehmerregelung-grenzen.html">Kleinunternehmerregelung 2026 – alle Grenzen und Regeln</a> · <a href="grenzen-check.html">Umsatzgrenzen-Check</a></p>
{DISCL}
</div></section>
<script>
(function(){{
""" + NUM_JS + r"""
document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){copy($(b.getAttribute('data-copy')).textContent,b)})});
var t=new Date();$('dt').value=t.toISOString().slice(0,10);
function de(d){if(!d)return '';var p=d.split('-');return p[2]+'.'+p[1]+'.'+p[0]}
function run(){
 var v=function(i){return $(i).value.trim()};var b=num(v('bt'));var klein=b!==null&&b<=250;
 var items=[['Dein Name/Firma',v('sn'),1],['Deine Anschrift',v('sa'),1],['Steuernummer oder USt-IdNr.',v('st'),klein?0:1],['Name des Kunden',v('kn'),klein?0:1],['Anschrift des Kunden',v('ka'),klein?0:1],['Rechnungsdatum',v('dt'),1],['Leistung (Art und Umfang)',v('ls'),1],['Betrag',b!==null?'x':'',1],['Hinweis auf § 19 UStG','x',1]];
 var miss=0,li='';items.forEach(function(it){var c=it[1]?'ok':(it[2]?'no':'na');if(c=='no')miss++;li+='<li class="'+c+'">'+it[0]+(c=='na'?' <small>(bei Kleinbetragsrechnung bis 250 € nicht nötig)</small>':'')+'</li>'});
 li+='<li class="'+(v('nr')?'ok':'na')+'">Rechnungsnummer <small>(nicht Pflicht, empfohlen)</small></li>';
 var out=miss?light('y','Noch '+miss+' Pflichtangabe'+(miss>1?'n':'')+' offen','Füll die gelb markierten Punkte aus.'):light('g','Alle Pflichtangaben vorhanden',klein?'Kleinbetragsrechnung (bis 250 €): Kundenangaben und Steuernummer sind hier nicht vorgeschrieben.':'Deine Rechnung erfüllt die Mindestangaben nach § 34a UStDV.');
 out+='<ul class="checks">'+li+'</ul>';
 var L=[];if(v('sn'))L.push(v('sn'));if(v('sa'))L.push(v('sa'));if(v('st'))L.push('Steuernummer: '+v('st'));L.push('');
 if(v('kn'))L.push(v('kn'));if(v('ka'))L.push(v('ka'));L.push('');
 L.push('RECHNUNG'+(v('nr')?' '+v('nr'):''));L.push('Rechnungsdatum: '+de(v('dt')));if(v('ld'))L.push('Leistungszeitraum: '+v('ld'));L.push('');
 L.push(v('ls')||'[Leistung]');L.push('');L.push('Rechnungsbetrag: '+(b!==null?eur(b):'[Betrag]'));L.push('');L.push($('hv').value);
 var txt=L.join('\n');
 out+='<div><b>Vorschau Rechnungstext</b><div class="pre" id="pv">'+esc(txt)+'</div><button type="button" class="cbtn" id="cp">Text kopieren</button></div>';
 $('res').innerHTML=out;$('cp').addEventListener('click',function(){copy(txt,$('cp'))});
}
['sn','sa','st','kn','ka','dt','nr','ls','ld','bt','hv'].forEach(function(i){$(i).addEventListener('input',run);$(i).addEventListener('change',run)});run();
})();
</script>"""
tool_page("rechnungstext-kleinunternehmer.html",
 "Rechnung als Kleinunternehmer 2026: Hinweis § 19 UStG + Pflichtangaben | Solovorlagen",
 "Kostenloser Generator: Kleinunternehmer-Hinweis nach § 19 UStG zum Kopieren, Pflichtangaben-Check nach § 34a UStDV und fertiger Rechnungstext – ohne Anmeldung.",
 "Rechnungstext-Generator für Kleinunternehmer", rt_body, RT_FAQ, "Rechnungstext-Generator")

# =====================================================================
# 2) GWG- & AfA-Rechner 2026
# =====================================================================
GW_FAQ = [
("Bis zu welchem Betrag kann ich 2026 sofort abschreiben?","Wirtschaftsgüter bis 800 Euro netto können als geringwertige Wirtschaftsgüter (GWG) im Jahr der Anschaffung vollständig abgesetzt werden (§ 6 Abs. 2 EStG). Bis 250 Euro netto ist das ohne gesonderte Aufzeichnung möglich. Die Grenzen sind 2026 unverändert."),
("Was ist der Sammelposten?","Wirtschaftsgüter zwischen 250,01 und 1.000 Euro netto können alternativ in einen Sammelposten gebucht und über fünf Jahre mit je einem Fünftel abgeschrieben werden (§ 6 Abs. 2a EStG). Wer den Sammelposten wählt, muss ihn für alle Anschaffungen dieser Preisspanne im selben Jahr nutzen."),
("Gilt die GWG-Grenze brutto oder netto?","Für die Prüfung der Grenzen zählt immer der Nettobetrag, also ohne Umsatzsteuer – auch für Kleinunternehmer. Kleinunternehmer können die Vorsteuer aber nicht abziehen; bei ihnen gehört die Umsatzsteuer zu den Anschaffungskosten. Abgesetzt wird also der Bruttobetrag."),
("Kann ich Computer und Laptops sofort abschreiben?","Für Computerhardware (inkl. Peripherie) und Software kann eine Nutzungsdauer von einem Jahr angesetzt werden (BMF-Schreiben vom 22.02.2022). Damit lassen sich Laptop, PC, Monitor oder Drucker unabhängig vom Preis im Anschaffungsjahr vollständig absetzen."),
("Wie wird über 800 Euro abgeschrieben?","Ohne Sammelposten werden Wirtschaftsgüter über 800 Euro netto linear über die betriebsgewöhnliche Nutzungsdauer abgeschrieben (§ 7 Abs. 1 EStG), im ersten Jahr monatsgenau ab dem Anschaffungsmonat. Die Nutzungsdauer steht in den amtlichen AfA-Tabellen, z. B. Büromöbel 13 Jahre."),
("Gibt es 2026 wieder die degressive Abschreibung?","Ja. Für bewegliche Wirtschaftsgüter, die nach dem 30.06.2025 und vor dem 01.01.2028 angeschafft werden, ist eine degressive AfA von bis zu 30 % (höchstens das Dreifache der linearen AfA) möglich. Sie lohnt sich vor allem bei längerer Nutzungsdauer."),
]
gw_body = f"""<div class="wrap" style="padding-top:40px;padding-bottom:24px">
<p class="eyebrow">Kostenloser Rechner · Stand 2026</p>
<h1 class="serif">GWG-Rechner 2026: Sofort absetzen oder abschreiben?</h1>
<div class="answer"><p><strong>Kurz gesagt:</strong> Bis <strong>800 € netto</strong> kannst du eine Anschaffung 2026 als geringwertiges Wirtschaftsgut <strong>sofort komplett absetzen</strong>. Zwischen 250,01 und 1.000 € geht alternativ der <strong>Sammelposten</strong> (5 Jahre je 20 %). Darüber wird über die Nutzungsdauer abgeschrieben. <strong>Computer und Software</strong> darfst du dank 1-Jahres-Nutzungsdauer immer im Anschaffungsjahr absetzen.</p></div>
</div>
<div class="wrap" style="padding-bottom:56px"><div class="split">
<div><form class="calc" onsubmit="return false">
<label for="pr">Kaufpreis laut Rechnung (€)</label><input type="text" id="pr" inputmode="decimal" placeholder="z. B. 699">
<div class="seg" role="radiogroup" aria-label="Preisart"><label><input type="radio" name="pa" value="b" checked> Bruttopreis (inkl. USt.)</label><label><input type="radio" name="pa" value="n"> Nettopreis</label></div>
<div class="row2"><div><label for="us">Umsatzsteuersatz</label><select id="us"><option value="19">19 %</option><option value="7">7 %</option><option value="0">0 % (z. B. Privatkauf)</option></select></div>
<div><label for="mo">Anschaffungsmonat</label><select id="mo">{"".join(f'<option value="{i}">{m}</option>' for i,m in enumerate(["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],1))}</select></div></div>
<label for="ar">Was hast du gekauft?</label><select id="ar">
<option value="1">Computer, Laptop, Tablet, Monitor, Drucker, Software (1 Jahr)</option>
<option value="5">Smartphone / Handy (5 Jahre)</option>
<option value="7">Kamera / Fotoausrüstung (7 Jahre)</option>
<option value="13">Büromöbel (13 Jahre)</option>
<option value="6">Pkw (6 Jahre)</option>
<option value="x">Anderes – Nutzungsdauer selbst eingeben</option></select>
<div id="ndw" style="display:none"><label for="nd">Nutzungsdauer (Jahre)</label><input type="text" id="nd" inputmode="numeric" placeholder="z. B. 8"></div>
<label class="chk"><input type="checkbox" id="ku" checked> Ich bin Kleinunternehmer (kein Vorsteuerabzug)</label>
<label class="chk"><input type="checkbox" id="sp"> Ich nutze dieses Jahr den Sammelposten</label>
<p class="hint">Die Daten bleiben in deinem Browser und werden nirgends gespeichert.</p>
<div class="res" id="res" aria-live="polite"></div>
</form></div>
<div>
<h2 class="serif" style="margin-top:0">Die Grenzen 2026 auf einen Blick</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Netto-Preis</th><th>Möglichkeiten</th></tr>
<tr><td>bis 250&nbsp;€</td><td>Sofort als Betriebsausgabe, keine Aufzeichnung</td></tr>
<tr><td>250,01–800&nbsp;€</td><td>GWG-Sofortabschreibung (Verzeichnis) <em>oder</em> Sammelposten</td></tr>
<tr><td>800,01–1.000&nbsp;€</td><td>Sammelposten (5 × 20 %) <em>oder</em> lineare AfA</td></tr>
<tr><td>über 1.000&nbsp;€</td><td>Lineare AfA über die Nutzungsdauer (ggf. degressiv bis 30 %)</td></tr>
<tr><td>Computer &amp; Software</td><td>Nutzungsdauer 1 Jahr – im Anschaffungsjahr voll absetzbar</td></tr></table></div>
<div class="cta"><h3>Alle Anschaffungen automatisch im Griff</h3><p>Das Anlagenverzeichnis &amp; der AfA-Rechner ordnen jede Anschaffung automatisch richtig ein, berechnen die Abschreibung für alle Jahre und liefern die Summe für deine EÜR.</p><a class="btn" href="afa.html">Zum AfA-Rechner (12 €)</a></div>
</div></div></div>
<section class="band"><div class="wrap faq">
<h2 class="serif">Häufige Fragen zu GWG und Abschreibung</h2>
{faq_html(GW_FAQ)}
<h3>Quellen</h3>{sources([("§ 6 EStG – Bewertung (Abs. 2 GWG, Abs. 2a Sammelposten)","https://dejure.org/gesetze/EStG/6.html"),("§ 7 EStG – Absetzung für Abnutzung","https://dejure.org/gesetze/EStG/7.html"),("§ 9b EStG – Umsatzsteuerrechtlicher Vorsteuerabzug","https://dejure.org/gesetze/EStG/9b.html")])}
{DISCL}
</div></section>
<script>
(function(){{
""" + NUM_JS + r"""
function rad(n){var r=document.querySelector('input[name='+n+']:checked');return r?r.value:''}
function run(){
 $('ndw').style.display=$('ar').value=='x'?'block':'none';
 var p=num($('pr').value);if(p===null||p<=0){$('res').innerHTML='<p class="hint">Trag oben den Kaufpreis ein – das Ergebnis erscheint sofort.</p>';return}
 var us=+$('us').value/100,brutto=rad('pa')=='b',ku=$('ku').checked,sp=$('sp').checked,mo=+$('mo').value;
 var net=brutto?p/(1+us):p,gross=brutto?p:p*(1+us),ak=ku?gross:net;
 var nd=$('ar').value=='x'?num($('nd').value):+$('ar').value;
 var y=new Date().getFullYear(),rows=[],head,sub,cls='g';
 if(net<=250){head='Sofort absetzen: '+eur(ak)+' im Jahr '+y;sub='Bis 250 € netto ist die Anschaffung sofort eine Betriebsausgabe – ohne Anlagenverzeichnis.';rows=[[y,ak]]}
 else if(sp&&net<=1000){head='Sammelposten: 5 × '+eur(ak/5);sub='Der Sammelposten wird über 5 Jahre mit je 20 % aufgelöst – unabhängig vom Anschaffungsmonat. Gilt dann für alle Anschaffungen zwischen 250,01 und 1.000 € netto in diesem Jahr.';for(var i=0;i<5;i++)rows.push([y+i,ak/5])}
 else if(nd===1){head='Sofort absetzen: '+eur(ak)+' im Jahr '+y;sub='Computerhardware und Software haben eine Nutzungsdauer von 1 Jahr (BMF 22.02.2022) – voller Abzug im Anschaffungsjahr, unabhängig vom Preis. Im Anlagenverzeichnis führen.';rows=[[y,ak]]}
 else if(net<=800){head='Sofort absetzen als GWG: '+eur(ak)+' im Jahr '+y;sub='250,01–800 € netto: geringwertiges Wirtschaftsgut. Voller Abzug im Anschaffungsjahr; ins GWG-/Anlagenverzeichnis aufnehmen. Alternativ wäre der Sammelposten möglich.';rows=[[y,ak]]}
 else{
  if(!nd||nd<1){$('res').innerHTML=light('y','Nutzungsdauer fehlt','Bitte gib die Nutzungsdauer in Jahren ein.');return}
  cls='y';head='Abschreiben über '+nd+' Jahre: '+eur(ak/nd)+' pro Jahr';
  sub='Über '+(net<=1000?'800':'1.000')+' € netto: lineare AfA, im ersten Jahr anteilig ab '+$('mo').options[mo-1].text+'.'+(net<=1000?' Alternativ: Sammelposten (5 × 20 %), wenn du ihn dieses Jahr nutzt.':'')+' Für Käufe bis Ende 2027 ist auch eine degressive AfA bis 30 % möglich.';
  var yr=ak/nd,rest=ak,first=yr*(13-mo)/12;rows.push([y,first]);rest-=first;var k=1;while(rest>0.005){var a=Math.min(yr,rest);rows.push([y+k,a]);rest-=a;k++}
 }
 var t='<table class="yt"><tr><th>Jahr</th><th>Absetzbar</th></tr>';rows.slice(0,8).forEach(function(r){t+='<tr><td>'+r[0]+'</td><td>'+eur(r[1])+'</td></tr>'});if(rows.length>8)t+='<tr><td colspan="2">… insgesamt '+rows.length+' Jahre</td></tr>';t+='</table>';
 var out=light(cls,head,sub)+'<div class="kpis"><div class="kpi"><span>Nettopreis (für die Grenze)</span><b>'+eur(net)+'</b></div><div class="kpi"><span>Absetzbar gesamt'+(ku?' (brutto, da KU)':'')+'</span><b>'+eur(ak)+'</b></div><div class="kpi"><span>Im Jahr '+y+'</span><b>'+eur(rows[0][1])+'</b></div></div>'+t;
 $('res').innerHTML=out;
}
['pr','us','mo','ar','nd','ku','sp'].forEach(function(i){$(i).addEventListener('input',run);$(i).addEventListener('change',run)});
document.querySelectorAll('input[name=pa]').forEach(function(r){r.addEventListener('change',run)});
$('mo').value=new Date().getMonth()+1;run();
})();
</script>"""
tool_page("gwg-rechner.html",
 "GWG-Rechner 2026: Sofort absetzen oder abschreiben? (800 €-Grenze) | Solovorlagen",
 "Kostenloser GWG- und AfA-Rechner 2026: Prüft, ob du eine Anschaffung sofort absetzen kannst (250 €, 800 €, Sammelposten 1.000 €, Computer 1 Jahr) – mit Abschreibungsplan, auch für Kleinunternehmer.",
 "GWG- und AfA-Rechner 2026", gw_body, GW_FAQ, "GWG-Rechner")

# =====================================================================
# 3) Fahrtkosten-Rechner 2026
# =====================================================================
FK_FAQ = [
("Wie viel kann ich 2026 pro gefahrenem Kilometer absetzen?","Für betriebliche Fahrten mit dem privaten Pkw – etwa zu Kunden, Lieferanten oder zum Einkauf – kannst du pauschal 0,30 Euro je gefahrenem Kilometer als Betriebsausgabe ansetzen. Für Motorrad oder Motorroller sind es 0,20 Euro je Kilometer. Hin- und Rückweg zählen beide."),
("Wie hoch ist die Entfernungspauschale 2026?","Seit dem 1. Januar 2026 beträgt die Entfernungspauschale einheitlich 0,38 Euro ab dem ersten Kilometer der einfachen Strecke. Bis 2025 galten für die ersten 20 Kilometer nur 0,30 Euro."),
("Wann gilt für Selbstständige die Entfernungspauschale statt 0,30 €/km?","Fahrten zwischen Wohnung und deiner ersten Betriebsstätte (z. B. eigenes Büro, Laden oder Werkstatt) darfst du nur in Höhe der Entfernungspauschale absetzen – also 0,38 Euro je Kilometer der einfachen Strecke pro Arbeitstag. Alle anderen betrieblichen Fahrten rechnest du mit 0,30 Euro je gefahrenem Kilometer ab."),
("Gibt es einen Höchstbetrag?","Für die Entfernungspauschale gilt ein Höchstbetrag von 4.500 Euro im Jahr. Er gilt nicht, wenn du die Strecke mit dem eigenen oder einem zur Nutzung überlassenen Pkw fährst. Für die 0,30 Euro je Kilometer bei betrieblichen Fahrten gibt es keinen Höchstbetrag."),
("Wie weise ich die Fahrten nach?","Halte für jede betriebliche Fahrt Datum, Ziel, Anlass und Kilometer fest – etwa in einem einfachen Fahrtenbuch oder einer Tabelle. Ein vollständiges Fahrtenbuch nach den strengen Regeln für Firmenwagen ist dafür nicht nötig."),
("Gilt das auch für einen Firmenwagen?","Nein. Gehört das Auto zum Betriebsvermögen, setzt du die tatsächlichen Kosten ab und versteuerst die private Nutzung (z. B. 1-%-Regelung). Die Kilometerpauschalen gelten für Fahrzeuge im Privatvermögen."),
]
fk_body = f"""<div class="wrap" style="padding-top:40px;padding-bottom:24px">
<p class="eyebrow">Kostenloser Rechner · Stand 2026</p>
<h1 class="serif">Fahrtkosten-Rechner 2026 für Selbstständige</h1>
<div class="answer"><p><strong>Kurz gesagt:</strong> Betriebliche Fahrten mit dem Privatauto setzt du 2026 mit <strong>0,30 € je gefahrenem Kilometer</strong> ab (Motorrad: 0,20 €). Für den Weg von der Wohnung zur eigenen Betriebsstätte gilt die <strong>Entfernungspauschale von 0,38 € ab dem ersten Kilometer</strong> der einfachen Strecke. Der Rechner zeigt dir, was im Jahr zusammenkommt.</p></div>
</div>
<div class="wrap" style="padding-bottom:56px"><div class="split">
<div><form class="calc" onsubmit="return false">
<label for="fz">Fahrzeug</label><select id="fz"><option value="0.30">Pkw (0,30 €/km)</option><option value="0.20">Motorrad / Motorroller (0,20 €/km)</option></select>
<h3 style="margin:22px 0 0">1. Betriebliche Fahrten</h3><p class="hint">Kunden, Lieferanten, Einkauf, Post, Bank – gefahrene Kilometer inkl. Rückweg.</p>
<div class="row2"><div><label for="km">Kilometer</label><input type="text" id="km" inputmode="decimal" placeholder="z. B. 250"></div>
<div><label for="zr">pro</label><select id="zr"><option value="12">Monat</option><option value="52">Woche</option><option value="1">Jahr</option></select></div></div>
<h3 style="margin:22px 0 0">2. Weg zur eigenen Betriebsstätte</h3><p class="hint">Nur wenn du ein eigenes Büro, einen Laden oder eine Werkstatt außerhalb der Wohnung hast.</p>
<div class="row2"><div><label for="ef">Einfache Entfernung (km)</label><input type="text" id="ef" inputmode="decimal" placeholder="z. B. 12"></div>
<div><label for="tg">Tage pro Jahr</label><input type="text" id="tg" inputmode="numeric" placeholder="z. B. 200"></div></div>
<label class="chk"><input type="checkbox" id="ei" checked> Ich fahre diese Strecke mit dem eigenen Pkw</label>
<p class="hint">Die Daten bleiben in deinem Browser und werden nirgends gespeichert.</p>
<div class="res" id="res" aria-live="polite"></div>
</form></div>
<div>
<h2 class="serif" style="margin-top:0">Die Sätze 2026</h2>
<div class="tblwrap"><table class="tbl"><tr><th>Fahrt</th><th>Satz 2026</th></tr>
<tr><td>Betriebliche Fahrt, Pkw</td><td>0,30&nbsp;€ je gefahrenem km</td></tr>
<tr><td>Betriebliche Fahrt, Motorrad/Roller</td><td>0,20&nbsp;€ je gefahrenem km</td></tr>
<tr><td>Wohnung → erste Betriebsstätte</td><td>0,38&nbsp;€ je km einfache Strecke, ab km 1</td></tr>
<tr><td>Höchstbetrag Entfernungspauschale</td><td>4.500&nbsp;€/Jahr (nicht mit eigenem Pkw)</td></tr></table></div>
<div class="cta"><h3>Jede Fahrt sauber dokumentiert</h3><p>Das Fahrtenbuch &amp; der Fahrtkosten-Rechner erfassen Datum, Ziel und Anlass, rechnen die Sätze 2026 automatisch und liefern die Jahressumme für deine Steuer.</p><a class="btn" href="fahrtenbuch.html">Zum Fahrtenbuch (12 €)</a></div>
</div></div></div>
<section class="band"><div class="wrap faq">
<h2 class="serif">Häufige Fragen zu Fahrtkosten für Selbstständige</h2>
{faq_html(FK_FAQ)}
<h3>Quellen</h3>{sources([("§ 4 Abs. 5 Nr. 6 EStG – Fahrten Wohnung–Betriebsstätte","https://dejure.org/gesetze/EStG/4.html"),("§ 9 Abs. 2 EStG – Entfernungspauschale","https://dejure.org/gesetze/EStG/9.html")])}
{DISCL}
</div></section>
<script>
(function(){{
""" + NUM_JS + r"""
function run(){
 var s=+$('fz').value,km=num($('km').value)||0,zr=+$('zr').value,ef=num($('ef').value)||0,tg=num($('tg').value)||0,ei=$('ei').checked;
 if(!km&&!(ef&&tg)){$('res').innerHTML='<p class="hint">Trag oben deine Kilometer ein – das Ergebnis erscheint sofort.</p>';return}
 var a=km*zr*s,b=ef*tg*0.38,cap=false;if(!ei&&b>4500){b=4500;cap=true}
 var out=light('g','Absetzbar pro Jahr: '+eur(a+b),'Betriebliche Fahrten '+eur(a)+(b?' + Weg zur Betriebsstätte '+eur(b):'')+'.'+(cap?' Höchstbetrag 4.500 € berücksichtigt.':''));
 out+='<div class="kpis"><div class="kpi"><span>Betriebliche Fahrten / Jahr</span><b>'+eur(a)+'</b></div><div class="kpi"><span>Entfernungspauschale / Jahr</span><b>'+eur(b)+'</b></div><div class="kpi"><span>Pro Monat (Ø)</span><b>'+eur((a+b)/12)+'</b></div></div>';
 out+='<p class="hint">Gerechnet: '+(km?km.toLocaleString('de-DE')+' km × '+zr+' × '+s.toFixed(2).replace('.',',')+' €':'keine betrieblichen Fahrten')+(b?' · '+ef.toLocaleString('de-DE')+' km × '+tg+' Tage × 0,38 €':'')+'. Grob geschätzt sparst du bei 30 % Steuersatz etwa '+eur((a+b)*0.3)+'.</p>';
 $('res').innerHTML=out;
}
['fz','km','zr','ef','tg','ei'].forEach(function(i){$(i).addEventListener('input',run);$(i).addEventListener('change',run)});run();
})();
</script>"""
tool_page("fahrtkosten-rechner.html",
 "Fahrtkosten-Rechner 2026: 0,30 €/km & Entfernungspauschale 0,38 € | Solovorlagen",
 "Kostenloser Fahrtkosten-Rechner für Selbstständige 2026: betriebliche Fahrten mit 0,30 €/km (Motorrad 0,20 €) und Entfernungspauschale 0,38 € ab dem ersten Kilometer – Jahresbetrag sofort berechnet.",
 "Fahrtkosten-Rechner 2026 für Selbstständige", fk_body, FK_FAQ, "Fahrtkosten-Rechner")

# =====================================================================
# Übersicht: rechner.html
# =====================================================================
TOOLS = [
("grenzen-check.html","Umsatzgrenzen-Check 2026","Bin ich noch Kleinunternehmer? 25.000 € / 100.000 € prüfen – mit Ausblick aufs Folgejahr."),
("rechnungstext-kleinunternehmer.html","Rechnungstext-Generator","§ 19-Hinweis zum Kopieren, Pflichtangaben-Check nach § 34a UStDV und fertiger Rechnungstext."),
("gwg-rechner.html","GWG- & AfA-Rechner 2026","Sofort absetzen oder abschreiben? 250 €, 800 €, Sammelposten und Computer-Regel."),
("fahrtkosten-rechner.html","Fahrtkosten-Rechner 2026","0,30 € je km für betriebliche Fahrten und 0,38 € Entfernungspauschale ab km 1."),
]
rc_cards = "".join(f'<a class="pcard" href="{u}"><div class="pbody"><h3>{t}</h3><p>{d}</p><div class="prow"><span class="more">Zum Rechner →</span></div></div></a>' for u,t,d in TOOLS)
rc_body = f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><div class="article" style="max-width:none">
<p class="eyebrow">Kostenlos · ohne Anmeldung · Stand 2026</p>
<h1 class="serif">Kostenlose Rechner für Selbstständige und Kleinunternehmer</h1>
<p class="lead">Schnelle Antworten auf typische Steuer- und Zahlenfragen – direkt im Browser, nichts wird gespeichert.</p>
<div class="grid2">{rc_cards}</div>
{DISCL}
</div></div>"""
page("Kostenlose Rechner für Selbstständige & Kleinunternehmer 2026 | Solovorlagen",
 "Kostenlose Online-Rechner für Selbstständige: Umsatzgrenzen-Check, Rechnungstext-Generator für Kleinunternehmer, GWG-Rechner und Fahrtkosten-Rechner 2026.",
 rc_body, "rechner.html", EXTRA_CSS + ld({"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":"https://solovorlagen.de/"+u,"name":t} for i,(u,t,d) in enumerate(TOOLS)]}))
print("tools ok")
