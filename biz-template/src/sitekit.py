# -*- coding: utf-8 -*-
"""Gemeinsame Bausteine: Konfiguration, Seitengerüst (Header/Footer), Logo, JSON-LD-Helfer.

Wird von gen_site.py, content.py, feeds.py, pins.py und von Inhaltsmodulen in content/ benutzt.
Alles Markenspezifische kommt aus config.json im Projektordner.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "docs")
CONTENT = os.path.join(ROOT, "content")
CONFIG_PATH = os.path.join(ROOT, "config.json")

PH_RE = re.compile(r"\[\[[^\]\n]{1,120}\]\]")


def load_config(path=CONFIG_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


CFG = load_config()
B = CFG["brand"]
C = CFG["colors"]
OP = CFG["operator"]
DOMAIN = B["domain"].strip().lower().removeprefix("https://").removeprefix("http://").strip("/")
BASE = f"https://{DOMAIN}/"
LANG = B.get("lang", "de")
LOCALE = B.get("locale", "de_DE")
LANG_TAG = LOCALE.replace("_", "-")

esc = html.escape


def is_placeholder(v):
    return not v or bool(PH_RE.search(str(v)))


def abs_url(path):
    """Relativer Pfad -> absolute URL auf der eigenen Domain."""
    if not path:
        return BASE
    if path.startswith(("http://", "https://")):
        return path
    return BASE + ("" if path == "index.html" else path.lstrip("/"))


def money(v, cur=None):
    cur = cur or CFG.get("product_defaults", {}).get("currency", "EUR")
    sym = {"EUR": "€", "USD": "$", "CHF": "CHF", "GBP": "£"}.get(cur, cur)
    if v is None or v == "":
        return ""
    if isinstance(v, str):
        return v
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if s.endswith(",00"):
        s = s[:-3]
    return f"{s}&nbsp;{sym}" if sym != "$" else f"{sym}{s}"


def money_txt(v, cur=None):
    return html.unescape(money(v, cur)).replace("\xa0", " ")


# ---------------------------------------------------------------- Logo
def logo_svg(cls="mark", size=None):
    L = CFG["logo"]
    dots = L.get("dots") or []
    dot_svg = "".join(f'<circle cx="46" cy="{20 + 12 * k}" r="4" fill="{d}"/>' for k, d in enumerate(dots[:3]))
    x = 27 if dots else 32
    letter = esc((L.get("letter") or B["name"][:1]).strip()[:2])
    fs = (32 if dots else 36) if len(letter) == 1 else 24
    fit = f' textLength="{26 if dots else 38}" lengthAdjust="spacingAndGlyphs"' if letter[:1].upper() in "MW" or len(letter) > 1 else ""
    sz = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg class="{cls}" viewBox="0 0 64 64"{sz} aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="64" height="64" rx="14" fill="{L["bg"]}"/>'
            f'<rect x="9" y="9" width="46" height="46" rx="10" fill="{L["inner"]}"/>'
            f'<text x="{x}" y="{32 + fs * 0.39:.0f}" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="{fs}" fill="{L["fg"]}"{fit}>{letter}</text>'
            f'{dot_svg}</svg>')


# ---------------------------------------------------------------- JSON-LD
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(u)} for i, (n, u) in enumerate(items)]}


def publisher():
    return {"@type": "Organization", "name": B["name"], "url": BASE, "logo": abs_url("favicon.svg")}


def author():
    """Person, sobald der Inhaber seinen Namen eingetragen hat – sonst die Marke als Organisation."""
    if not is_placeholder(OP.get("name")):
        return {"@type": "Person", "name": OP["name"], "url": abs_url("impressum.html")}
    return publisher()


def article_ld(headline, desc, path, date, updated=None):
    return {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc,
            "inLanguage": LANG_TAG, "datePublished": date, "dateModified": updated or date,
            "author": author(), "publisher": publisher(), "mainEntityOfPage": abs_url(path)}


def faq_html(qas):
    return "".join(f"<h3>{nb(esc(q))}</h3><p>{nb(esc(a))}</p>" for q, a in qas)


def nb(x):
    """Geschütztes Leerzeichen zwischen Zahl und Einheit."""
    return re.sub(r"(\d) (€|%|Euro|Prozent)", lambda m: m.group(1) + "&nbsp;" + m.group(2), x)


def sources_html(lst):
    return '<ul class="src">' + "".join(f'<li><a href="{esc(u)}" rel="noopener">{nb(esc(t))}</a></li>' for t, u in lst) + "</ul>"


def de_date(iso):
    y, m, d = str(iso)[:10].split("-")
    return f"{d}.{m}.{y}"


# ---------------------------------------------------------------- CSS
def build_css():
    F = CFG.get("fonts", {})
    v = {
        "ink": C["ink"], "primary": C["primary"], "accent": C["accent"], "accent-dark": C.get("accent_dark", C["accent"]),
        "muted": C["muted"], "soft": C["soft"], "bg": C["bg"], "surface": C.get("surface", "#fff"), "line": C["line"],
        "on-primary": C.get("on_primary", "#fff"), "on-primary-muted": C.get("on_primary_muted", "rgba(255,255,255,.8)"),
        "input-bg": C.get("input_bg", "#fff"), "focus": C.get("focus", C["accent"]),
        "font-heading": F.get("heading", "Georgia, serif"), "font-body": F.get("body", "system-ui, sans-serif"),
    }
    root = ":root{" + ";".join(f"--{k}:{val}" for k, val in v.items()) + "}\n"
    with open(os.path.join(HERE, "style.css"), encoding="utf-8") as f:
        return "/* generiert aus src/style.css + config.json – nicht direkt bearbeiten */\n" + root + f.read()


# ---------------------------------------------------------------- Bilder
def _webp_variants():
    """WebP-Varianten (1000/500 px) für JPG/PNG in docs/img – nur wenn Pillow installiert ist."""
    try:
        from PIL import Image
    except Exception:
        return
    d = os.path.join(OUT, "img")
    if not os.path.isdir(d):
        return
    for f in os.listdir(d):
        if not f.lower().endswith((".jpg", ".jpeg", ".png")) or f.startswith(("og", "_")):
            continue
        src = os.path.join(d, f)
        b = os.path.splitext(src)[0]
        for suf, w in (("", 1000), ("-500", 500)):
            dst = b + suf + ".webp"
            if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                continue
            im = Image.open(src).convert("RGB")
            im.thumbnail((w, w))
            im.save(dst, "WEBP", quality=80, method=6)


def _pic(h):
    def r(m):
        tag, name = m.group(0), m.group(1)
        if not (os.path.exists(os.path.join(OUT, "img", name + ".webp")) and os.path.exists(os.path.join(OUT, "img", name + "-500.webp"))):
            return tag
        sizes = "(max-width:640px) 100vw, 460px" if "heroimg" in tag else "(max-width:640px) 100vw, 360px"
        return f'<picture><source type="image/webp" srcset="img/{name}-500.webp 500w, img/{name}.webp 1000w" sizes="{sizes}">{tag}</picture>'
    return re.sub(r'<img [^>]*src="img/([\w-]+)\.(?:jpe?g|png)"[^>]*>', r, h)


def _mark_placeholders(body):
    """[[PLATZHALTER]] im sichtbaren Text gelb hervorheben (nicht in Attributen)."""
    return re.sub(r"(\[\[[^\]\n<>\"]{1,120}\]\])(?=[^<>]*<)", r'<mark class="ph">\1</mark>', body)


# ---------------------------------------------------------------- Seitengerüst
WRITTEN = []  # alle geschriebenen Seiten (für Platzhalter-Prüfung)


def og_image():
    s = CFG.get("seo", {})
    if s.get("og_image"):
        return abs_url(s["og_image"])
    if os.path.exists(os.path.join(OUT, "img", "og.png")):
        return abs_url("img/og.png")
    return ""


def nav_links():
    return "".join(f'<a href="{esc(n["href"])}">{esc(n["label"])}</a>' for n in CFG.get("nav", []))


def page(title, desc, body, path, head="", noindex=False):
    canon = abs_url(path)
    ogi = og_image()
    pv = CFG.get("pinterest", {}).get("domain_verify")
    cta = CFG.get("nav_cta")
    email = OP.get("email", "")
    mail_link = "" if is_placeholder(email) else f'<a href="mailto:{esc(email)}">{esc(email)}</a>'
    owner = "" if is_placeholder(OP.get("name")) else " · " + esc(OP.get("company") or OP["name"])
    theme = CFG.get("seo", {}).get("theme_color") or C["primary"]
    h = f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="stylesheet" href="style.css">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="{LOCALE}">
<meta property="og:site_name" content="{esc(B['name'])}">
{f'<meta property="og:image" content="{ogi}">' if ogi else ''}
{f'<meta name="p:domain_verify" content="{esc(pv)}">' if pv else ''}
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{'<link rel="icon" href="favicon-48.png" sizes="48x48" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png">' if os.path.exists(os.path.join(OUT, "favicon-48.png")) else ''}
<meta name="theme-color" content="{theme}">
{head}
</head>
<body>
<header><div class="wrap">
<a class="brand" href="index.html" aria-label="{esc(B['name'])} – Startseite">{logo_svg()}<span class="serif">{esc(B['name'])}</span></a>
<nav aria-label="Hauptnavigation">{nav_links()}{f'<a class="navbuy" href="{esc(cta["href"])}">{esc(cta["label"])}</a>' if cta else ''}</nav>
</div></header>
<main>
{_mark_placeholders(body)}
</main>
<footer><div class="wrap">
<div class="fbrand"><a class="brand" href="index.html">{logo_svg()}<span class="serif">{esc(B['name'])}</span></a>
<p>{_mark_placeholders(esc(B.get('footer_text', B.get('claim', ''))) + '<i></i>')}</p></div>
<nav aria-label="Fußzeile">{nav_links()}<a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a>{mail_link}</nav>
<p class="copy">© {B.get('copyright_year', '')} {esc(B['name'])}{owner}</p>
</div></footer>
</body>
</html>
"""
    h = h.replace("<i></i>", "")
    h = re.sub(r"\n{2,}", "\n", h)
    os.makedirs(os.path.dirname(os.path.join(OUT, path)) or OUT, exist_ok=True)
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(_pic(h))
    WRITTEN.append(path)


# Gemeinsame JS-Helfer für Rechner (Zahlen deutsch parsen/formatieren, Kopieren)
NUM_JS = r"""var $=function(i){return document.getElementById(i)};
var fmt=function(n,d){return n.toLocaleString('de-DE',{minimumFractionDigits:d||0,maximumFractionDigits:d||0})};
var eur=function(n){return n.toLocaleString('de-DE',{minimumFractionDigits:2,maximumFractionDigits:2})+' €'};
var num=function(v){v=(v||'').replace(/\s|€|%/g,'');if(v.indexOf(',')>-1)v=v.replace(/\./g,'').replace(',','.');else if((v.match(/\./g)||[]).length>1||/\.\d{3}$/.test(v))v=v.replace(/\./g,'');var n=parseFloat(v);return isNaN(n)?null:n};
function light(c,h,s){return '<div class="light '+c+'">'+h+(s?'<small>'+s+'</small>':'')+'</div>'}
function esc(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function copy(txt,btn){var done=function(){var o=btn.textContent;btn.textContent='Kopiert ✓';setTimeout(function(){btn.textContent=o},1500)};
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(txt).then(done,function(){fb()})}else fb();
 function fb(){var t=document.createElement('textarea');t.value=txt;document.body.appendChild(t);t.select();try{document.execCommand('copy');done()}catch(e){}document.body.removeChild(t)}}
"""
