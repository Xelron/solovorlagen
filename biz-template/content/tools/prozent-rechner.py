# -*- coding: utf-8 -*-
"""BEISPIEL-RECHNER – zeigt, wie ein Web-Rechner als Modul aufgebaut ist.

Jede Datei in content/tools/ (ohne _ am Anfang) wird zu einer eigenen Seite <slug>.html und
automatisch in Rechner-Übersicht, Startseite, Sitemap und llms.txt eingetragen.

  META     Metadaten (title, description, date sind Pflicht; name, card_text, eyebrow, answer,
           faq, sources, llms, order optional)
  BODY     HTML des Rechners (linke Spalte). Klasse "calc" für das Formular verwenden.
  EXPLAIN  HTML der Erklärung (rechte Spalte), optional
  SCRIPT   JavaScript; die Helfer aus sitekit.NUM_JS ($, num, eur, fmt, light, esc, copy) sind schon da.
"""
META = {
    "slug": "prozent-rechner",
    "name": "Prozentrechner",
    "title": "BEISPIEL: Prozentrechner",
    "description": "BEISPIEL-RECHNER: Prozentwert und Preis nach Rabatt direkt im Browser berechnen – zeigt den Aufbau eines Rechners in der Vorlage.",
    "card_text": "BEISPIEL: Prozentwert und Preis nach Rabatt berechnen.",
    "llms": "BEISPIEL-Rechner: Prozentwert (Grundwert × Prozentsatz ÷ 100) und Preis nach Rabatt.",
    "date": "2026-10-30",
    "eyebrow": "Kostenloser Rechner · Beispiel",
    "answer": "**Formel:** Prozentwert = Grundwert × Prozentsatz ÷ 100. Beispiel: 20 % von 80 sind 16.",
    "order": 1,
    "faq": [
        ("Wird meine Eingabe gespeichert?", "Nein. Der Rechner rechnet nur in deinem Browser, es wird nichts übertragen."),
    ],
}

BODY = """<form class="calc" id="calc" onsubmit="return false">
<div class="row2">
<div><label for="gw">Grundwert</label><input type="text" id="gw" inputmode="decimal" value="80" autocomplete="off"></div>
<div><label for="ps">Prozentsatz (%)</label><input type="text" id="ps" inputmode="decimal" value="20" autocomplete="off"></div>
</div>
<p class="hint">Komma oder Punkt als Dezimaltrennzeichen – beides geht.</p>
<div class="res" id="res" aria-live="polite"></div>
</form>"""

EXPLAIN = """<h2 class="serif" style="margin-top:0">So rechnet der Rechner</h2>
<p><strong>Prozentwert</strong> = Grundwert × Prozentsatz ÷ 100</p>
<p><strong>Preis nach Rabatt</strong> = Grundwert − Prozentwert</p>
<p class="note">BEISPIEL: Ersetze diesen Rechner durch einen, der eine typische Frage deiner Zielgruppe beantwortet.</p>"""

SCRIPT = r"""
function calc(){var g=num($('gw').value),p=num($('ps').value),r=$('res');
 if(g===null||p===null){r.innerHTML=light('y','Bitte zwei Zahlen eingeben.');return}
 var w=g*p/100;
 r.innerHTML='<div class="kpis"><div class="kpi"><span>Prozentwert</span><b>'+fmt(w,2)+'</b></div>'
  +'<div class="kpi"><span>Nach Abzug</span><b>'+fmt(g-w,2)+'</b></div>'
  +'<div class="kpi"><span>Nach Aufschlag</span><b>'+fmt(g+w,2)+'</b></div></div>'
  +'<div class="bar" aria-hidden="true"><i style="width:'+Math.max(0,Math.min(100,p))+'%"></i></div>';
}
['gw','ps'].forEach(function(i){$(i).addEventListener('input',calc)});calc();
"""
