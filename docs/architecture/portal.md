# Portal-Architektur

## Entscheidung

Pelican erzeugt HTML aus Markdown und Jinja. Die Wahl passt zu einer
Python-basierten, redaktionell pflegbaren Website mit individuellen Landingpages.
Der Generator benötigt Python nur beim Build; das veröffentlichte Ergebnis
benötigt keine Python-Laufzeit. Pelican ist ein eigenständiges Open-Source-Werkzeug;
die Nutzung als Generator stellt keine Lizenzfreigabe für importierte Inhalte dar.

## Datenfluss

```text
content/pages/*.md ─┐
projects.json ──────┼─ Pelican + Theme ──┐
pelicanconf.py ─────┘                   ├─ output/ ─ statischer Host
test-sites/<id>/ ── Validierung/Kopie ──┘
```

`portal.py` validiert Projektregister, Basis-URL und statische Artefakte.
`main.py` stellt Build, Vorschau, Import und Prüfung bereit. Ein Build wird
zuerst in einem temporären Verzeichnis erzeugt; erst nach erfolgreicher
Generierung wird die bisherige Ausgabe ersetzt. Das ist keine transaktionale
Veröffentlichung auf einem entfernten Host. Gleichzeitige lokale Builds/Imports
sind nicht unterstützt; nicht parallel im selben Checkout ausführen.

Die Projektkarten werden aus dem Register generiert. Redaktionelle Detailtexte
liegen in Markdown. Für neue Projekte muss eine passende Abschnitts-ID auf der
Ökosystem-Seite ergänzt werden; die Linkprüfung schützt vor vergessenen Zielen.

## Grenzen

- Keine Laufzeit-API, Ticketdatenbank, Authentifizierung oder Live-Statusabfrage.
- Keine automatische Synchronisierung mit fremden Repositories.
- Keine Backend-Deployments oder automatische Anpassung fremder Asset-Pfade.
- Kein Secret-Scanner: Importierte Inhalte brauchen Freigabe und Review.
- Keine Isolation zwischen Testseiten desselben Origins.
- Keine personenbezogenen oder geheimen Daten in Build-Artefakten.

## Hosting

GitHub Pages ist als optionaler Veröffentlichungsweg vorbereitet. Die URL wird
erst bei Ausführung des Workflows ermittelt. Eigene Domains werden über die
Pages-Einstellungen/DNS verwaltet; es ist absichtlich keine fiktive Domain
eingetragen. Andere statische Hosts liefern dieselbe Ausgabe aus.

Die inhaltlichen Freigabepunkte zu Betreiberinformationen und Projektzuständigkeit
sind bewusst sichtbar, statt durch erfundene Angaben ersetzt zu werden.
