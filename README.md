# solovorlagen.de

Statische Website von Solovorlagen (GitHub Pages, Ordner `docs/`).

- `src/gen_site.py` erzeugt alle Shop-, Produkt- und Ratgeberseiten nach `docs/` (Inhalte in `src/content.py`, Digistore24-IDs in `src/ds24.json`).
- `docs/impressum.html`, `docs/datenschutz.html`, Bilder und Pins sind statisch.
- Neu bauen: `python3 src/gen_site.py`, danach committen und pushen – GitHub Pages veröffentlicht automatisch.
