# -*- coding: utf-8 -*-
"""Minimaler Markdown-Konverter + Front-Matter-Parser ohne Abhängigkeiten.

Unterstützt im Text:
  ## Überschrift {#anker}     ### Unterüberschrift {#anker}
  Absätze, **fett**, *kursiv*, `code`, [Link](url)
  - Aufzählung / 1. Nummerierung
  > Zitatblock  -> wird als hervorgehobene Kurzantwort (.answer) gesetzt
  | Tabelle | mit | Kopfzeile |  (zweite Zeile |---|---|)
  Zeilen, die mit < beginnen, werden als rohes HTML übernommen.

Front Matter (zwischen --- und ---), kleines YAML-Subset:
  key: wert
  liste:
    - q: Frage
      a: Antwort
    - einfacher Listeneintrag
"""
import html, re


def _scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_front_matter(text):
    """Gibt (meta: dict, body: str) zurück."""
    if not text.startswith("---"):
        return {}, text
    end = re.search(r"^---\s*$", text[3:], re.M)
    if not end:
        return {}, text
    fm = text[3:3 + end.start()]
    body = text[3 + end.end():].lstrip("\n")
    meta, key, cur = {}, None, None
    for raw in fm.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0 and ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            meta[key] = _scalar(val) if val else []
            cur = None
        elif line.startswith("- ") and key is not None:
            item = line[2:]
            m = re.match(r"^([A-Za-z_]\w*):\s*(.*)$", item)
            if m:
                cur = {m.group(1): _scalar(m.group(2))}
                meta[key].append(cur)
            else:
                cur = None
                meta[key].append(_scalar(item))
        elif cur is not None:
            m = re.match(r"^([A-Za-z_]\w*):\s*(.*)$", line)
            if m:
                cur[m.group(1)] = _scalar(m.group(2))
            else:  # Fortsetzungszeile des letzten Werts
                last = list(cur)[-1]
                cur[last] += " " + line
    return meta, body


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: f'<a href="{html.escape(m.group(2))}"'
               + (' rel="noopener"' if m.group(2).startswith("http") else "") + f">{m.group(1)}</a>", t)
    # geschützte Leerzeichen zwischen Zahl und Einheit
    t = re.sub(r"(\d) (€|%|Euro|Prozent|km|kg|h)\b", lambda m: m.group(1) + "&nbsp;" + m.group(2), t)
    return t


def _heading(line, level, cls):
    txt = line[level + 1:].strip()
    anchor = ""
    m = re.search(r"\s*\{#([\w-]+)\}\s*$", txt)
    if m:
        anchor = f' id="{m.group(1)}"'
        txt = txt[:m.start()]
    return f'<h{level} class="{cls}"{anchor}>{inline(txt)}</h{level}>' if cls else f"<h{level}{anchor}>{inline(txt)}</h{level}>"


def to_html(md):
    lines = md.splitlines()
    out, i = [], 0
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("<"):
            flush(); out.append(line); i += 1; continue
        if s.startswith("### "):
            flush(); out.append(_heading(s, 3, "")); i += 1; continue
        if s.startswith("## "):
            flush(); out.append(_heading(s, 2, "serif")); i += 1; continue
        if s.startswith("> "):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append('<div class="answer"><p>' + inline(" ".join(buf)) + "</p></div>"); continue
        if re.match(r"^[-*] ", s) or re.match(r"^\d+\. ", s):
            flush(); ordered = bool(re.match(r"^\d+\. ", s)); items = []
            while i < len(lines):
                t = lines[i].strip()
                if re.match(r"^[-*] ", t) or re.match(r"^\d+\. ", t):
                    items.append(re.sub(r"^([-*]|\d+\.) ", "", t))
                elif t and lines[i].startswith(("  ", "\t")) and items:
                    items[-1] += " " + t
                else:
                    break
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>"); continue
        if s.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            head = cells[0]
            bodyrows = [r for r in cells[1:] if not all(re.match(r"^:?-{2,}:?$", c) for c in r)]
            t = '<div class="tblwrap"><table class="tbl"><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in bodyrows)
            out.append(t + "</table></div>"); continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)
