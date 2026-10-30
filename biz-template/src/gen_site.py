# -*- coding: utf-8 -*-
"""Baut die komplette Website nach docs/ (GitHub Pages).

    python3 src/gen_site.py

Liest config.json (Marke, Farben, Produkte, Betreiberdaten, Pinterest, IndexNow) und content/
(Ratgeber-Artikel und Rechner). Ohne Abhängigkeiten lauffähig; wenn Pillow installiert ist,
entstehen zusätzlich WebP-Varianten, PNG-Favicons und ein Open-Graph-Bild.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitekit as S
from sitekit import CFG, B, C, OP, OUT, esc, page, ld, money, money_txt, abs_url, is_placeholder
import content as CONTENT
import feeds as FEEDS

os.makedirs(os.path.join(OUT, "img"), exist_ok=True)


# ================================================================ Assets
def write(path, text):
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(text)


write("style.css", S.build_css())
write("favicon.svg", S.logo_svg(cls="favicon"))
write(".nojekyll", "")


def _font(size, serif=True):
    try:
        from PIL import ImageFont
    except Exception:
        return None
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/Library/Fonts/Georgia Bold.ttf", "C:/Windows/Fonts/georgiab.ttf"] if serif
              else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/Library/Fonts/Arial.ttf", "C:/Windows/Fonts/arial.ttf"]):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def _png_icons():
    """favicon-48.png, apple-touch-icon.png und img/og.png (1200x630) – nur mit Pillow."""
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return
    L = CFG["logo"]
    letter = (L.get("letter") or B["name"][:1])[:2]

    def mark(sz):
        k = sz / 64
        im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, sz - 1, sz - 1], radius=int(14 * k), fill=L["bg"])
        d.rounded_rectangle([9 * k, 9 * k, 55 * k, 55 * k], radius=int(10 * k), fill=L["inner"])
        dots = L.get("dots") or []
        cx = 27 if dots else 32
        fs = int((36 if len(letter) == 1 else 26) * k)
        maxw = (26 if dots else 38) * k
        f = _font(fs)
        while fs > 6 and d.textlength(letter, font=f) > maxw:
            fs -= 1
            f = _font(fs)
        d.text((cx * k, 33 * k), letter, font=f, fill=L["fg"], anchor="mm")
        for i, col in enumerate(dots[:3]):
            y = 20 + 12 * i
            d.ellipse([42 * k, (y - 4) * k, 50 * k, (y + 4) * k], fill=col)
        return im

    mark(48).save(os.path.join(OUT, "favicon-48.png"))
    ap = Image.new("RGB", (180, 180), L["bg"])
    m = mark(180)
    ap.paste(m, (0, 0), m)
    ap.save(os.path.join(OUT, "apple-touch-icon.png"))
    if not CFG.get("seo", {}).get("og_image"):
        og = Image.new("RGB", (1200, 630), C["primary"])
        d = ImageDraw.Draw(og)
        m = mark(140)
        og.paste(m, (80, 80), m)
        d.text((80, 300), B["name"], font=_font(84), fill=C.get("on_primary", "#fff"))
        claim = re.sub(r"\[\[.*?\]\]", "", B.get("claim", "")).strip()
        words, lines, cur = claim.split(), [], ""
        for w in words:
            if len(cur + " " + w) > 38:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            lines.append(cur)
        for i, ln in enumerate(lines[:2]):
            d.text((80, 410 + i * 54), ln, font=_font(40, serif=False), fill=C.get("on_primary_muted", "#ddd"))
        d.rectangle([0, 610, 1200, 630], fill=C["accent"])
        d.text((1120, 560), S.DOMAIN, font=_font(30, serif=False), fill=C.get("on_primary", "#fff"), anchor="rm")
        og.save(os.path.join(OUT, "img", "og.png"))


_png_icons()
S._webp_variants()


def placeholder_img(slug, name):
    """Platzhalterbild (SVG) für Produkte ohne eigenes Bild."""
    fn = f"placeholder-{slug}.svg"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
<rect width="1000" height="1000" fill="{C['bg']}"/>
<rect x="60" y="60" width="880" height="880" rx="48" fill="{C['primary']}"/>
<g fill="none" stroke="{C.get('on_primary_muted', '#ccc')}" stroke-opacity=".25" stroke-width="2">{''.join(f'<line x1="60" y1="{y}" x2="940" y2="{y}"/>' for y in range(160, 940, 80))}</g>
<rect x="140" y="300" width="720" height="400" rx="28" fill="{C.get('surface', '#fff')}"/>
<text x="500" y="470" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="{64 if len(name) < 18 else 46}" fill="{C['primary']}">{esc(name)}</text>
<text x="500" y="560" text-anchor="middle" font-family="system-ui,sans-serif" font-size="30" fill="{C['soft']}">Platzhalterbild – eigenes Bild in docs/img/</text>
<text x="500" y="604" text-anchor="middle" font-family="system-ui,sans-serif" font-size="30" fill="{C['soft']}">ablegen und in config.json eintragen</text>
<rect x="140" y="760" width="240" height="18" rx="9" fill="{C['accent']}"/>
</svg>"""
    write(os.path.join("img", fn), svg)
    return fn


# ================================================================ Produkte
PD = CFG.get("product_defaults", {})
P = CFG.get("products", [])
BY = {p["slug"]: p for p in P}
for p in P:
    img = p.get("image") or ""
    p["_img"] = img if img and os.path.exists(os.path.join(OUT, "img", img)) else placeholder_img(p["slug"], p["name"])
    if img and p["_img"] != img:
        print(f"WARNUNG: Bild docs/img/{img} für Produkt {p['slug']} fehlt – Platzhalter verwendet")
    p["_shots"] = [s for s in p.get("shots", []) if os.path.exists(os.path.join(OUT, "img", s))]


def buy(p, cls="btn", label=None):
    co = CFG["checkout"]
    if p.get("checkout_url"):
        return f'<a class="{cls}" href="{esc(p["checkout_url"])}" rel="nofollow">{esc(label or co.get("buy_label", "Jetzt kaufen"))}{"" if label else " – " + money(p["price"])}</a>'
    return f'<span class="{cls} soon" aria-disabled="true">{esc(co.get("soon_label", "Bald verfügbar"))}</span>'


def card(p):
    cmp_ = f' <s style="font-size:15px;opacity:.65">{money(p["compare_price"])}</s>' if p.get("compare_price") else ""
    return f"""<a class="pcard" href="{p['slug']}.html"><img src="img/{p['_img']}" width="1000" height="1000" alt="Produktbild {esc(p['name'])}" loading="lazy">
<div class="pbody"><h3>{esc(p['name'])}</h3><p>{esc(p['short'])}</p><div class="prow"><span class="price">{money(p['price'])}{cmp_}</span><span class="more">Ansehen</span></div></div></a>"""


def faq_section(extra=()):
    qas = list(extra) + [tuple(x) for x in CFG.get("faq", [])]
    if not qas:
        return ""
    return f"""<section class="band"><div class="wrap faq">
<h2 class="serif">{esc(CFG.get('faq_title', 'Häufige Fragen'))}</h2>
{S.faq_html(qas)}
</div></section>"""


ARTICLES, TOOLS = CONTENT.load_all()

# ---------------------------------------------------------------- Startseite
H = CFG["home"]
hero_p = BY.get(H.get("hero_product") or "")
visual = f'<div class="bvisual"><img src="img/{hero_p["_img"]}" width="1000" height="1000" alt="Produktbild {esc(hero_p["name"])}"></div>' if hero_p else ""
cta_html = "".join(f'<a class="btn{" ghost" if k == "cta_secondary" else ""}" href="{esc(H[k]["href"])}">{esc(H[k]["label"])}</a>'
                   for k in ("cta_primary", "cta_secondary") if H.get(k) and not (H[k]["href"] == "rechner.html" and not TOOLS))
tools_band = ""
if TOOLS:
    tools_band = f"""<section class="rechnerband"><div class="wrap">
<h2 class="serif">{esc(CFG.get('rechner', {}).get('title', 'Kostenlose Rechner'))}</h2>
<ul class="rlist">{''.join(f'<li><a href="{t["slug"]}.html"><b>{esc(t["name"])}</b><span>{esc(t["card_text"])}</span></a></li>' for t in TOOLS)}</ul>
</div></section>"""
why = "".join(f'<div class="feat"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in H.get("why", []))
idx = f"""<section class="banner"><div class="wrap bwrap">
<div class="btext">
<h1 class="serif">{esc(H['h1'])}</h1>
<p class="lead">{esc(H['lead'])}</p>
<div class="cta2">{cta_html}</div>
<ul class="facts">{''.join(f'<li>{esc(x)}</li>' for x in H.get('facts', []))}</ul>
</div>
{visual}
</div></section>
{tools_band}
<section class="band" id="produkte"><div class="wrap">
<h2 class="serif">{esc(H.get('products_title', 'Produkte'))}</h2>
<p class="sub2">{esc(H.get('products_sub', ''))}</p>
<div class="pgrid">{''.join(card(p) for p in P)}</div>
</div></section>
{f'<section><div class="wrap"><h2 class="serif">{esc(H.get("why_title", ""))}</h2><div class="grid3">{why}</div></div></section>' if why else ''}
{faq_section()}"""
org_ld = {"@context": "https://schema.org", "@type": "Organization", "name": B["name"], "url": S.BASE, "logo": abs_url("favicon.svg")}
if not is_placeholder(OP.get("email")):
    org_ld["email"] = OP["email"]
site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": B["name"], "url": S.BASE, "inLanguage": S.LANG_TAG}
page(H["title"], H["meta_description"], idx, "index.html", ld(org_ld) + ld(site_ld) + ld(S.faq_ld([tuple(x) for x in CFG.get("faq", [])])))

# ---------------------------------------------------------------- Produktseiten
for p in P:
    includes = [BY[s] for s in p.get("includes", []) if s in BY]
    rows = [("Produkt", p["name"]), ("Art", PD.get("type", "")), ("Format", p.get("format") or PD.get("format", "")),
            ("Inhalt", p.get("content", "")), ("Lieferung", p.get("delivery") or PD.get("delivery", "")),
            ("Preis", f"<strong>{money(p['price'])} einmalig</strong>" + (f" (statt {money(p['compare_price'])})" if p.get("compare_price") else "")),
            ("Für wen", p.get("audience") or PD.get("audience", ""))]
    tbl = "".join(f"<tr><th>{k}</th><td>{v if k == 'Preis' else esc(v)}</td></tr>" for k, v in rows if v)
    shots = "".join(f'<img src="img/{s}" width="1000" height="1000" alt="Beispielansicht {esc(p["name"])}" loading="lazy">' for s in p["_shots"])
    feats = "".join(f'<div class="feat"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in p.get("features", []))
    extra = ""
    if includes:
        extra = ('<section><div class="wrap"><h2 class="serif">Im Paket enthalten</h2><div class="pgrid">' + "".join(card(q) for q in includes) + "</div></div></section>")
    pfaq = [tuple(x) for x in p.get("faq", [])]
    co = CFG["checkout"]
    body = f"""<div class="wrap hero">
<div>
<p class="eyebrow">{esc(p.get('eyebrow', ''))}</p>
<h1 class="serif">{esc(p.get('h1') or p['name'])}</h1>
<p class="lead">{esc(p.get('lead', ''))}</p>
{buy(p)}
<p class="note">{esc(co.get('note', ''))}</p>
</div>
<div><img class="heroimg" src="img/{p['_img']}" width="1000" height="1000" alt="Produktbild {esc(p['name'])}"></div>
</div>
<section class="band"><div class="wrap">
<h2 class="serif">Das bekommst du</h2>
<div class="split"><div><table class="spec">{tbl}</table></div>
{f'<div class="shots">{shots}</div>' if shots else ''}</div>
</div></section>
{f'<section><div class="wrap"><h2 class="serif">Was das Produkt kann</h2><div class="grid2">{feats}</div></div></section>' if feats else ''}
{extra}
{faq_section(pfaq)}
<section id="kaufen" class="band"><div class="wrap buy">
<h2 class="serif">{esc(p['name'])} kaufen</h2>
<p class="sub2">Digitaler Download · sofort nach der Zahlung verfügbar</p>
<div class="price-big serif">{money(p['price'])}</div>
{buy(p, "btn btn-lg", co.get("buy_label", "Jetzt kaufen"))}
<p class="note">{esc(co.get('payment_note', ''))}</p>
</div></section>"""
    lead = p.get("lead", "")
    md = lead if len(lead) <= 158 else lead[:155].rsplit(" ", 1)[0] + " …"
    prod_ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p.get("short", ""),
               "image": abs_url("img/" + p["_img"]), "brand": {"@type": "Brand", "name": B["name"]},
               "offers": {"@type": "Offer", "price": f"{float(p['price']):.2f}", "priceCurrency": PD.get("currency", "EUR"),
                          "availability": "https://schema.org/InStock" if p.get("checkout_url") else "https://schema.org/OutOfStock",
                          "url": abs_url(p["slug"] + ".html")}}
    head = ld(prod_ld) + ld(S.faq_ld(pfaq + [tuple(x) for x in CFG.get("faq", [])])) + ld(S.crumbs_ld([(B["name"], "index.html"), (p["name"], p["slug"] + ".html")]))
    suffix = PD.get("title_suffix")
    page(f"{p['name']}{' – ' + suffix if suffix else ''} | {B['name']}", md, body, f"{p['slug']}.html", head)


# ================================================================ Rechtstexte
def _addr_block():
    lines = [OP.get("name"), OP.get("company"), OP.get("street"), OP.get("zip_city"), OP.get("country")]
    return "<br>\n".join(esc(x) for x in lines if x)


def _mail(e):
    return esc(e) if is_placeholder(e) else f'<a href="mailto:{esc(e)}">{esc(e)}</a>'


imp = f"""<div class="wrap legal">
<h1 class="serif">Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>{_addr_block()}</p>
<h2>Kontakt</h2>
<p>E-Mail: {_mail(OP.get('email', ''))}{('<br>Telefon: ' + esc(OP['phone'])) if OP.get('phone') else ''}</p>
{f'<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: {esc(OP["vat_id"])}</p>' if OP.get('vat_id') else ''}
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>{esc(OP.get('name', ''))}, Anschrift wie oben</p>
<h2>Verbraucherstreitbeilegung</h2>
<p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
</div>"""
page(f"Impressum | {B['name']}", f"Impressum von {B['name']}.", imp, "impressum.html")

co = CFG["checkout"]
checkout_txt = ""
if co.get("provider"):
    role = (f"{esc(co['provider'])} tritt dabei als Wiederverkäufer auf und ist dein Vertragspartner für Bestellung, Zahlung, Rechnung und Auslieferung des Downloads."
            if co.get("reseller") else f"{esc(co['provider'])} wickelt Bestellung und Zahlung für uns ab.")
    checkout_txt = f"""<h2>5. Kauf über {esc(co['provider'])}</h2>
<p>Unsere Produkte werden über {esc(co.get('provider_address') or co['provider'])} verkauft. {role}</p>
<p>Wenn du auf „{esc(co.get('buy_label', 'Jetzt kaufen'))}“ klickst, gelangst du auf das Bestellformular von {esc(co['provider'])}. Die dort eingegebenen Daten verarbeitet {esc(co['provider'])} in eigener Verantwortung.{f' Einzelheiten findest du in der <a href="{esc(co["privacy_url"])}" rel="noopener">Datenschutzerklärung von {esc(co["provider"])}</a>.' if co.get('privacy_url') else ''}</p>
<p>Nach einem Kauf erhalten wir von {esc(co['provider'])} die für die Kaufabwicklung nötigen Angaben, etwa Name, E-Mail-Adresse und Bestelldaten, zum Beispiel um Supportanfragen zu beantworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO. Steuer- und handelsrechtliche Aufbewahrungspflichten bleiben unberührt (Art. 6 Abs. 1 lit. c DSGVO).</p>"""
ds = f"""<div class="wrap legal">
<h1 class="serif">Datenschutzerklärung</h1>
<p>Stand: {esc(CFG.get('legal_stand', ''))}</p>
<h2>1. Verantwortlicher</h2>
<p>Verantwortlich für die Datenverarbeitung auf dieser Website ist:</p>
<p>{_addr_block()}<br>
E-Mail: {_mail(OP.get('email', ''))}</p>
<h2>2. Das Wichtigste in Kürze</h2>
<p>Diese Website setzt keine Cookies, nutzt keine Analyse- oder Tracking-Werkzeuge und lädt keine Inhalte von Drittanbietern wie Schriftarten oder Videos. Die Rechner auf dieser Website rechnen ausschließlich in deinem Browser; eingegebene Werte werden nicht übertragen. Personenbezogene Daten fallen nur an, wenn du die Seite aufrufst (Server-Logfiles), uns eine E-Mail schreibst oder ein Produkt kaufst.</p>
<h2>3. Hosting und Server-Logfiles</h2>
<p>Diese Website wird über GitHub Pages bereitgestellt, einen Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Seite übermittelt dein Browser automatisch Daten, die GitHub in Server-Logfiles verarbeitet, insbesondere:</p>
<ul>
<li>IP-Adresse</li>
<li>Datum und Uhrzeit des Zugriffs</li>
<li>aufgerufene Seite bzw. Datei</li>
<li>Browsertyp, Betriebssystem und Referrer-URL</li>
</ul>
<p>Die Verarbeitung ist technisch notwendig, um die Website auszuliefern und ihre Sicherheit zu gewährleisten. Rechtsgrundlage ist unser berechtigtes Interesse nach Art. 6 Abs. 1 lit. f DSGVO. Dabei können Daten in die USA übertragen werden. GitHub ist nach dem EU-US Data Privacy Framework zertifiziert (Angemessenheitsbeschluss nach Art. 45 DSGVO). Einzelheiten findest du in der <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>
<h2>4. Kontakt per E-Mail</h2>
<p>Wenn du uns eine E-Mail schreibst, verarbeiten wir deine E-Mail-Adresse und den Inhalt deiner Nachricht, um deine Anfrage zu beantworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern deine Anfrage mit einem Kauf oder Vertrag zusammenhängt, ansonsten unser berechtigtes Interesse an der Beantwortung nach Art. 6 Abs. 1 lit. f DSGVO. Wir löschen die Daten, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
{checkout_txt}
<h2>6. Deine Rechte</h2>
<p>Du hast jederzeit das Recht auf:</p>
<ul>
<li>Auskunft über deine gespeicherten Daten (Art. 15 DSGVO)</li>
<li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
<li>Löschung (Art. 17 DSGVO) und Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
<li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
<li>Widerspruch gegen Verarbeitungen, die auf unserem berechtigten Interesse beruhen (Art. 21 DSGVO)</li>
</ul>
<p>Eine formlose E-Mail an {_mail(OP.get('email', ''))} genügt.</p>
<h2>7. Beschwerderecht</h2>
<p>Du kannst dich bei einer Datenschutz-Aufsichtsbehörde beschweren. Für uns zuständig ist: {esc(OP.get('supervisory_authority', ''))}</p>
<h2>8. SSL-/TLS-Verschlüsselung</h2>
<p>Diese Website nutzt aus Sicherheitsgründen eine SSL-/TLS-Verschlüsselung. Du erkennst sie am Schloss-Symbol und an „https://“ in der Adresszeile deines Browsers.</p>
<h2>9. Änderungen</h2>
<p>Wir passen diese Datenschutzerklärung an, wenn sich unser Angebot ändert, etwa bei Einführung eines Newsletters.</p>
</div>"""
if not checkout_txt:
    ds = ds.replace("<h2>6.", "<h2>5.").replace("<h2>7.", "<h2>6.").replace("<h2>8.", "<h2>7.").replace("<h2>9.", "<h2>8.")
page(f"Datenschutzerklärung | {B['name']}", f"Datenschutzerklärung von {B['name']}.", ds, "datenschutz.html")

# ================================================================ Inhalte, SEO-Dateien, Feeds
CONTENT.build(ARTICLES, TOOLS, BY)
FEEDS.build()

# IndexNow-Schlüsseldatei
key = (CFG.get("indexnow_key") or "").strip()
if key:
    write(f"{key}.txt", key)
else:
    print("HINWEIS: indexnow_key in config.json ist leer – new_business.py erzeugt ihn (oder: python3 -c \"import secrets;print(secrets.token_hex(16))\").")

# CNAME für GitHub Pages (nur echte Domains)
if S.DOMAIN and not S.DOMAIN.endswith(("example.com", "example.org")) and not is_placeholder(S.DOMAIN):
    write("CNAME", S.DOMAIN + "\n")

# ================================================================ Platzhalter-Bericht
found = {}
for f in set(S.WRITTEN):
    for m in S.PH_RE.findall(open(os.path.join(OUT, f), encoding="utf-8").read()):
        found.setdefault(m, set()).add(f)
print(f"ok: {len(set(S.WRITTEN))} Seiten, {len(P)} Produkte, {len(ARTICLES)} Artikel, {len(TOOLS)} Rechner -> {os.path.relpath(OUT)}")
if found:
    print("\nWARNUNG – Platzhalter noch nicht ersetzt (vor dem Livegang in config.json / content/ ausfüllen):")
    for k, v in sorted(found.items()):
        print(f"  {k}  ({', '.join(sorted(v)[:4])}{' …' if len(v) > 4 else ''})")
