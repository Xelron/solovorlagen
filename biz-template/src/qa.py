# -*- coding: utf-8 -*-
"""Layout-QA: startet einen lokalen Server auf docs/ und prüft jede Seite bei 390, 820 und 1280 px.

    python3 src/qa.py                 # alle Seiten
    python3 src/qa.py --shot out.png  # zusätzlich Screenshot der Startseite bei 390 px

Prüft: horizontales Scrollen, herausragende Eingabefelder, abgeschnittene Auswahltexte,
Eingabe-Paare nicht auf einer Linie, fehlende Bilder, JavaScript-Fehler, tote interne Links.
Braucht Playwright mit Chromium. Exit-Code 1 bei Problemen.
"""
import glob, os, re, socket, subprocess, sys, time

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")

CHK = """(()=>{const out=[];
document.querySelectorAll('.row2').forEach((r,k)=>{const ins=[...r.querySelectorAll('input,select')].map(e=>Math.round(e.getBoundingClientRect().top));if(ins.length==2&&Math.abs(ins[0]-ins[1])>2&&r.getBoundingClientRect().width>500)out.push('Eingabefelder nicht auf einer Linie #'+k)});
document.querySelectorAll('input,select,textarea').forEach(e=>{const b=e.getBoundingClientRect(),f=e.closest('form,main');if(f&&b.right>f.getBoundingClientRect().right+1)out.push('Feld ragt heraus '+(e.id||e.name))});
document.querySelectorAll('select').forEach(e=>{if(e.scrollWidth>e.clientWidth+2)out.push('Auswahltext abgeschnitten '+e.id)});
if(document.documentElement.scrollWidth>innerWidth)out.push('horizontales Scrollen ('+document.documentElement.scrollWidth+'px)');
document.querySelectorAll('img').forEach(i=>{if(i.complete&&i.naturalWidth==0)out.push('Bild fehlt '+i.getAttribute('src'))});
return out})()"""


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def dead_links():
    """Interne Links auf nicht vorhandene Dateien/Anker (statisch geprüft)."""
    out = []
    files = {os.path.basename(f): open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(ROOT, "*.html"))}
    for name, h in files.items():
        for href in re.findall(r'href="([^"]+)"', h):
            if href.startswith(("http", "mailto:", "tel:", "#", "data:")) or href.endswith((".css", ".svg", ".png", ".xml")):
                if href.startswith("#") and len(href) > 1 and f'id="{href[1:]}"' not in h:
                    out.append(f"{name}: Anker {href} fehlt")
                continue
            target, _, anchor = href.partition("#")
            if not os.path.exists(os.path.join(ROOT, target)):
                out.append(f"{name}: Link auf fehlende Datei {target}")
            elif anchor and target in files and f'id="{anchor}"' not in files[target]:
                out.append(f"{name}: Anker {href} fehlt")
    return out


def main(argv):
    from playwright.sync_api import sync_playwright
    shot = argv[argv.index("--shot") + 1] if "--shot" in argv else None
    bad = 0
    for d in dead_links():
        bad += 1
        print("LINK", d)
    port = free_port()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            for w, h in [(390, 844), (820, 1180), (1280, 900)]:
                pg = b.new_page(viewport={"width": w, "height": h})
                errs = []
                pg.on("pageerror", lambda e: errs.append("JS-Fehler: " + str(e)))
                pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
                for f in pages:
                    u = os.path.basename(f)
                    pg.goto(f"http://127.0.0.1:{port}/{u}")
                    pg.wait_for_timeout(100)
                    r = pg.evaluate(CHK) + errs
                    if r:
                        bad += 1
                        print(w, u, r)
                    errs.clear()
                if shot and w == 390:
                    pg.goto(f"http://127.0.0.1:{port}/index.html")
                    pg.wait_for_timeout(200)
                    pg.screenshot(path=shot, full_page=True)
                    print("Screenshot:", shot)
                pg.close()
            b.close()
            print(f"{len(pages)} Seiten × 3 Breiten geprüft")
    finally:
        srv.terminate()
    print("QA ok" if not bad else f"QA: {bad} Probleme")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
