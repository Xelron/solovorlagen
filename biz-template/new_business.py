#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Legt aus dieser Vorlage ein neues Online-Business an.

    python3 new_business.py ../mein-business --name "Mein Business" --domain mein-business.de
        [--claim "Kurzer Claim"] [--letter M] [--primary "#2B3A67"] [--accent "#C8553D"]
        [--git] [--no-build]

Was passiert:
  1. Kopiert config.json, src/, content/, .github/, README.md, .gitignore in den neuen Ordner
     (docs/ wird neu gebaut, nichts aus dem Vorlagen-docs/ wird übernommen).
  2. Belegt config.json vor: Name, Domain, Claim, Logo-Buchstabe, optional Farben.
     Betreiberdaten (Name, Adresse, E-Mail) bleiben [[PLATZHALTER]] – die trägt der Inhaber selbst ein.
  3. Erzeugt einen IndexNow-Schlüssel (config.json + docs/<schlüssel>.txt).
  4. Schreibt docs/CNAME mit der Domain (für GitHub Pages).
  5. Baut die Seite einmal (python3 src/gen_site.py), optional git init (--git). Es wird nichts gepusht.
"""
import argparse, colorsys, json, os, re, secrets, shutil, subprocess, sys

TPL = os.path.dirname(os.path.abspath(__file__))
COPY = ["config.json", "src", "content", ".github", "README.md", ".gitignore"]


def darker(hexcol, f=0.82):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, l * f, s)
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))


def replace_strings(obj, old, new):
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, list):
        return [replace_strings(x, old, new) for x in obj]
    if isinstance(obj, dict):
        return {k: replace_strings(v, old, new) for k, v in obj.items()}
    return obj


def main():
    ap = argparse.ArgumentParser(description="Neues Online-Business aus der Vorlage anlegen")
    ap.add_argument("ordner")
    ap.add_argument("--name", required=True, help="Markenname, z. B. 'Gartenplaner'")
    ap.add_argument("--domain", required=True, help="Domain ohne https://, z. B. gartenplaner.de")
    ap.add_argument("--claim", help="Kurzer Claim/Slogan")
    ap.add_argument("--letter", help="Buchstabe im Logo (Standard: erster Buchstabe des Namens)")
    ap.add_argument("--primary", help="Hauptfarbe als Hex, z. B. #2B3A67")
    ap.add_argument("--accent", help="Akzentfarbe (Buttons) als Hex, z. B. #C8553D")
    ap.add_argument("--git", action="store_true", help="git init im neuen Ordner (kein Push)")
    ap.add_argument("--no-build", action="store_true", help="Seite nicht sofort bauen")
    a = ap.parse_args()

    dst = os.path.abspath(a.ordner)
    if os.path.exists(dst) and os.listdir(dst):
        sys.exit(f"FEHLER: {dst} existiert und ist nicht leer.")
    domain = a.domain.strip().lower().removeprefix("https://").removeprefix("http://").strip("/")
    if domain.startswith("www."):
        domain = domain[4:]
        print("Hinweis: www. entfernt – die Hauptadresse ist die Domain ohne www, www leitet GitHub Pages weiter.")
    if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", domain):
        sys.exit(f"FEHLER: '{a.domain}' sieht nicht nach einer Domain aus.")
    for c in (a.primary, a.accent):
        if c and not re.fullmatch(r"#[0-9A-Fa-f]{6}", c):
            sys.exit(f"FEHLER: Farbe '{c}' bitte als #RRGGBB angeben.")

    os.makedirs(dst, exist_ok=True)
    for item in COPY:
        s = os.path.join(TPL, item)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(dst, item), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        elif os.path.exists(s):
            shutil.copy2(s, os.path.join(dst, item))
    for d in ("docs/img", "docs/pins"):
        os.makedirs(os.path.join(dst, d), exist_ok=True)

    cp = os.path.join(dst, "config.json")
    cfg = json.load(open(cp, encoding="utf-8"))
    old = cfg["brand"]["name"]
    cfg = replace_strings(cfg, old, a.name)
    cfg["brand"]["name"] = a.name
    cfg["brand"]["domain"] = domain
    if a.claim:
        cfg["brand"]["claim"] = a.claim
    letter = (a.letter or next((ch for ch in a.name if ch.isalnum()), "X")).upper()[:2]
    cfg["logo"]["letter"] = letter
    if a.primary:
        cfg["colors"]["primary"] = a.primary
        cfg["logo"]["bg"] = a.primary
        cfg["logo"]["fg"] = a.primary
    if a.accent:
        cfg["colors"]["accent"] = a.accent
        cfg["colors"]["accent_dark"] = darker(a.accent)
        if cfg["logo"].get("dots"):
            cfg["logo"]["dots"][0] = a.accent
    key = secrets.token_hex(16)
    cfg["indexnow_key"] = key
    with open(cp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(dst, "docs", "CNAME"), "w") as f:
        f.write(domain + "\n")
    with open(os.path.join(dst, "docs", f"{key}.txt"), "w") as f:
        f.write(key)

    print(f"Angelegt: {dst}\n  Marke: {a.name}  Domain: {domain}  Logo: {letter}  IndexNow-Schlüssel: {key}")
    if not a.no_build:
        subprocess.run([sys.executable, os.path.join(dst, "src", "gen_site.py")], check=True)
    if a.git:
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=dst, check=True)
        print("git init (Branch main) – noch kein Commit, kein Remote, kein Push.")
    print("\nNächste Schritte: siehe README.md, Abschnitt „Neues Business anlegen“ (Platzhalter, Produkte, Domain/DNS, GitHub Pages).")


if __name__ == "__main__":
    main()
