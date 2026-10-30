# -*- coding: utf-8 -*-
"""Sammelt Ratgeber-Artikel (content/articles/) und Rechner (content/tools/) automatisch ein
und baut daraus Artikel-/Rechnerseiten, Ratgeber- und Rechner-Übersicht, sitemap.xml, robots.txt, llms.txt.

Dateien, deren Name mit _ beginnt, werden ignoriert (z. B. _vorlage.md). Mit `draft: true`
in den Metadaten wird ein Artikel nicht veröffentlicht.
"""
import datetime, glob, importlib.util, os
import sitekit as S
import mdlite
from sitekit import CFG, B, OUT, CONTENT, esc, page, ld, abs_url, is_placeholder


def _norm_pairs(lst, a, b):
    out = []
    for x in lst or []:
        if isinstance(x, dict):
            out.append((x.get(a, ""), x.get(b, "")))
        else:
            out.append(tuple(x))
    return out


def _load_py(path):
    name = "content_" + os.path.splitext(os.path.basename(path))[0].replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _finish(meta, path):
    slug = meta.get("slug") or os.path.splitext(os.path.basename(path))[0]
    meta["slug"] = slug[:-5] if slug.endswith(".html") else slug
    for k in ("title", "description", "date"):
        if not meta.get(k):
            raise SystemExit(f"FEHLER: {os.path.relpath(path)} – Metadatum '{k}' fehlt")
    meta["date"] = str(meta["date"])[:10]
    meta["updated"] = str(meta.get("updated") or meta["date"])[:10]
    meta["faq"] = _norm_pairs(meta.get("faq"), "q", "a")
    meta["sources"] = _norm_pairs(meta.get("sources"), "title", "url")
    meta.setdefault("card_text", meta["description"])
    meta.setdefault("llms", meta["description"])
    meta["_src"] = os.path.relpath(path, S.ROOT)
    return meta


def load_articles():
    arts = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "articles", "*"))):
        base = os.path.basename(path)
        if base.startswith(("_", ".")):
            continue
        if path.endswith(".md"):
            meta, body = mdlite.parse_front_matter(open(path, encoding="utf-8").read())
            meta["_html"] = mdlite.to_html(body)
        elif path.endswith(".py"):
            mod = _load_py(path)
            meta = dict(getattr(mod, "META"))
            meta["_html"] = mod.body(S) if hasattr(mod, "body") else getattr(mod, "BODY", "")
        else:
            continue
        if str(meta.get("draft", "")).lower() in ("true", "1", "ja", "yes"):
            continue
        arts.append(_finish(meta, path))
    arts.sort(key=lambda a: a["date"], reverse=True)
    return arts


def load_tools():
    tools = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "tools", "*.py"))):
        if os.path.basename(path).startswith("_"):
            continue
        mod = _load_py(path)
        meta = dict(mod.META)
        meta.setdefault("name", meta.get("title"))
        meta["_body"] = mod.body(S) if hasattr(mod, "body") else getattr(mod, "BODY", "")
        meta["_script"] = getattr(mod, "SCRIPT", "")
        meta["_explain"] = getattr(mod, "EXPLAIN", "")
        tools.append(_finish(meta, path))
    tools.sort(key=lambda t: t.get("order", 100))
    return tools


def load_all():
    return load_articles(), load_tools()


def byline(a):
    who = esc(B["name"]) if is_placeholder(S.OP.get("name")) else f'<a href="impressum.html">{esc(S.OP["name"])}</a>, {esc(B["name"])}'
    return f'<p class="byline">Von {who} · Stand: <time datetime="{a["updated"]}">{S.de_date(a["updated"])}</time></p>'


def cta_box(slug, products):
    p = products.get(slug or "")
    if not p:
        return ""
    return (f'<div class="cta"><h3>{esc(p["name"])}</h3><p>{esc(p.get("short", ""))}</p>'
            f'<a class="btn" href="{p["slug"]}.html">{esc(p["name"])} ansehen</a></div>')


def build(articles, tools, products):
    R = CFG.get("ratgeber", {})
    RC = CFG.get("rechner", {})
    disclaimer = R.get("disclaimer", "")
    # ------------------------------------------------ Artikelseiten
    for a in articles:
        path = a["slug"] + ".html"
        body = f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><article class="article">
{f'<p class="eyebrow">{esc(a["eyebrow"])}</p>' if a.get('eyebrow') else ''}
<h1 class="serif">{esc(a.get('h1') or a['title'])}</h1>
{byline(a)}
{f'<div class="answer"><p><strong>Kurz gesagt:</strong> {mdlite.inline(a["answer"])}</p></div>' if a.get('answer') else ''}
{a['_html']}
{cta_box(a.get('cta_product'), products)}
{f'<h2 class="serif" id="faq">Häufige Fragen</h2><div class="faq" style="max-width:none">{S.faq_html(a["faq"])}</div>' if a['faq'] else ''}
{f'<h2 class="serif">Quellen</h2>{S.sources_html(a["sources"])}' if a['sources'] else ''}
{f'<p class="note">{esc(disclaimer)}</p>' if disclaimer else ''}
</article></div>"""
        head = ld(S.article_ld(a["title"], a["description"], path, a["date"], a["updated"]))
        if a["faq"]:
            head += ld(S.faq_ld(a["faq"]))
        head += ld(S.crumbs_ld([(B["name"], "index.html"), (R.get("title", "Ratgeber"), "ratgeber.html"), (a["title"], path)]))
        page(a.get("seo_title") or f"{a['title']} | {B['name']}", a["description"], body, path, head)

    # ------------------------------------------------ Rechnerseiten
    for t in tools:
        path = t["slug"] + ".html"
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": abs_url(path),
               "applicationCategory": RC.get("app_category", "UtilitiesApplication"), "operatingSystem": "Browser",
               "inLanguage": S.LANG_TAG, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
               "description": t["description"], "publisher": S.publisher()}
        head = ld(app) + (ld(S.faq_ld(t["faq"])) if t["faq"] else "")
        head += ld(S.crumbs_ld([(B["name"], "index.html"), (RC.get("title", "Rechner"), "rechner.html"), (t["name"], path)]))
        body = f"""<div class="wrap" style="padding-top:40px;padding-bottom:24px">
{f'<p class="eyebrow">{esc(t["eyebrow"])}</p>' if t.get('eyebrow') else ''}
<h1 class="serif">{esc(t['title'])}</h1>
{f'<div class="answer"><p>{mdlite.inline(t["answer"])}</p></div>' if t.get('answer') else ''}
</div>
<div class="wrap" style="padding-bottom:56px"><div class="split">
<div>{t['_body']}</div>
<div class="article">{t['_explain']}</div>
</div>
{f'<div class="faq article"><h2 class="serif">Häufige Fragen</h2>{S.faq_html(t["faq"])}</div>' if t['faq'] else ''}
{f'<div class="article"><h2 class="serif">Quellen</h2>{S.sources_html(t["sources"])}</div>' if t['sources'] else ''}
{f'<p class="note">{esc(disclaimer)}</p>' if disclaimer else ''}
</div>
{f'<script>{S.NUM_JS}{t["_script"]}</script>' if t['_script'] else ''}"""
        page(t.get("seo_title") or f"{t['title']} | {B['name']}", t["description"], body, path, head)

    # ------------------------------------------------ Übersichten
    def acard(x, more):
        return (f'<a class="pcard" href="{x["slug"]}.html"><div class="pbody"><h3>{esc(x.get("name") if more.startswith("Zum") else x["title"])}</h3>'
                f'<p>{esc(x["card_text"])}</p><div class="prow"><span class="more">{more}</span></div></div></a>')

    rg = f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><div class="article" style="max-width:none">
<h1 class="serif">{esc(R.get('h1', 'Ratgeber'))}</h1>
<p class="lead">{esc(R.get('lead', ''))}</p>
<div class="grid2">{''.join(acard(a, 'Lesen →') for a in articles) or '<p>Noch keine Artikel.</p>'}</div>
{f'<h2 class="serif" id="rechner" style="margin-top:48px">{esc(RC.get("title", "Rechner"))}</h2><div class="grid2">' + ''.join(acard(t, 'Zum Rechner →') for t in tools) + '</div>' if tools else ''}
</div></div>"""
    il = {"@context": "https://schema.org", "@type": "ItemList",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": abs_url(a["slug"] + ".html"), "name": a["title"]} for i, a in enumerate(articles)]}
    page(f"{R.get('h1', 'Ratgeber')} | {B['name']}", R.get("lead", ""), rg, "ratgeber.html", ld(il))
    if tools:
        rc = f"""<div class="wrap" style="padding-top:40px;padding-bottom:64px"><div class="article" style="max-width:none">
<h1 class="serif">{esc(RC.get('h1', 'Kostenlose Rechner'))}</h1>
<p class="lead">{esc(RC.get('lead', ''))}</p>
<div class="grid2">{''.join(acard(t, 'Zum Rechner →') for t in tools)}</div>
</div></div>"""
        il = {"@context": "https://schema.org", "@type": "ItemList",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": abs_url(t["slug"] + ".html"), "name": t["name"]} for i, t in enumerate(tools)]}
        page(f"{RC.get('h1', 'Kostenlose Rechner')} | {B['name']}", RC.get("lead", ""), rc, "rechner.html", ld(il))
    elif os.path.exists(os.path.join(OUT, "rechner.html")):
        os.remove(os.path.join(OUT, "rechner.html"))

    # ------------------------------------------------ sitemap.xml
    dates = [a["updated"] for a in articles] + [t["updated"] for t in tools]
    site_date = str(CFG.get("site_updated") or (max(dates) if dates else datetime.date.today().isoformat()))[:10]
    urls = [("index.html", site_date)] + [(p["slug"] + ".html", site_date) for p in products.values()]
    urls += [("ratgeber.html", max([a["updated"] for a in articles], default=site_date))]
    if tools:
        urls += [("rechner.html", max(t["updated"] for t in tools))] + [(t["slug"] + ".html", t["updated"]) for t in tools]
    urls += [(a["slug"] + ".html", a["updated"]) for a in articles]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{abs_url(u)}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    # ------------------------------------------------ robots.txt
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {abs_url('sitemap.xml')}\n")

    # ------------------------------------------------ llms.txt
    op = "" if is_placeholder(S.OP.get("name")) else f" Betreiber: {S.OP['name']}."
    L = [f"# {B['name']}", f"> {B.get('description', '')}{op}", ""]
    if articles:
        L += [f"## {R.get('title', 'Ratgeber')}"] + [f"- [{a['title']}]({abs_url(a['slug'] + '.html')}): {a['llms']}" for a in articles] + [""]
    if tools:
        L += [f"## {RC.get('title', 'Werkzeuge')}"] + [f"- [{t['name']}]({abs_url(t['slug'] + '.html')}): {t['llms']}" for t in tools] + [""]
    if products:
        L += ["## Produkte"] + [f"- [{p['name']}]({abs_url(p['slug'] + '.html')}): {p.get('short', '')} ({S.money_txt(p['price'])})" for p in products.values()] + [""]
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))
