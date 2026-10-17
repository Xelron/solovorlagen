# solovorlagen.de

Statische Website von Solovorlagen (GitHub Pages, Ordner `docs/`).

- `src/gen_site.py` erzeugt alle Shop-, Produkt- und Ratgeberseiten nach `docs/` (Inhalte in `src/content.py`, Digistore24-IDs in `src/ds24.json`).
- `docs/impressum.html`, `docs/datenschutz.html`, Bilder und Pins sind statisch.
- Neu bauen: `python3 src/gen_site.py`, danach committen und pushen – GitHub Pages veröffentlicht automatisch.

## Pinterest
- Pins werden automatisch per RSS veröffentlicht: `docs/feeds/kleinunternehmer-tipps.xml`, `preise-und-geld.xml`, `excel-vorlagen.xml` (je ein Pinterest-Board).
- Neuer Pin: Bild 1000×1500 nach `docs/pins/pin-NN.jpg` (Generator `src/pins.py`, neuer Batch), Eintrag in `src/feeds.json` (eindeutige id, board-Name exakt, link auf solovorlagen.de, image-URL, date), `python3 src/gen_site.py`, commit, push. Pinterest holt neue Einträge täglich ab.
- Die CSV-Dateien `pinterest-pins*.csv` sind nur noch Archiv (Pins 1–12 wurden per CSV geplant).
