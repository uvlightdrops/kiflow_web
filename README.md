# Kiflow · Ecosystem Portal

Statische, deutschsprachige Website für das KI-Ökosystem, Projektmanagement und
Teilprojekt-Testseiten. Generator: **[Pelican](https://getpelican.com/)** mit Markdown
und eigenem Jinja-Theme. Kein Node-Build, keine Datenbank, keine externen Fonts.

## Lokal starten

Python 3.11+:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py serve
```

Öffnen: <http://127.0.0.1:8000>. Beenden mit `Ctrl+C`.
Nach Änderungen neu starten, um erneut zu bauen; kein Live-Reload.
Anderer Port: `python main.py serve --port 8010`.

## Pflegen

| Inhalt | Datei / Verzeichnis |
|---|---|
| Startseite | `theme/templates/home.html` |
| Inhaltliche Seiten | `content/pages/*.md` |
| Projekte, Status, nächster Schritt | `projects.json` |
| Navigation und Generator | `pelicanconf.py` |
| Layout und Darstellung | `theme/templates/`, `theme/static/` |
| Freigegebene statische Teilprojekt-Builds | `test-sites/<projekt-id>/` |
| Build und Import | `main.py`, `portal.py` |

Markdown-Seiten haben Metadaten `Title`, `Slug`, `Kicker`, `Summary`.
Für neue Seiten einen eindeutigen Slug verwenden. Navigation in `NAV` ergänzen.
Interne Markdown-Links sind relativ zur erzeugten Seite, z. B. `../projekte/`.
Generiertes `output/` niemals manuell bearbeiten.

### Projektregister

Jedes Objekt in `projects.json` benötigt:

- `id`: eindeutiger URL-Slug, z. B. `mein-projekt`
- `name`, `summary`, `category`, `owner`, `next_step`: nicht leere Texte
- `phase`: `aufbau`, `mvp`, `geplant`, `entwicklung` oder `vorab`
- `tags`: Liste von Texten
- `preview_kind`: `none`, `demo` oder `test`

`demo` und `test` erfordern `test-sites/<id>/index.html`. Ein Registereintrag
allein erzeugt keinen Projekt-Build. Bei neuen Projekten die Einordnung und
passende ID-Überschrift in `content/pages/oekosystem.md` ergänzen; die Projektkarte
verlinkt dorthin. Status ist redaktionell, nicht live.

### Testseite importieren

```bash
python main.py stage ia3-simworld /absoluter/pfad/zum/dist
python main.py check
python main.py build
```

`stage` ersetzt den bisherigen Build dieser ID und setzt `preview_kind` auf `test`.
Die gegebenenfalls bestehende Layout-Demo wird dabei ersetzt. Änderungen an `test-sites/` und
`projects.json` gemeinsam versionieren.

Nur kontrollierte, öffentliche statische Artefakte importieren. Der CLI lehnt
versteckte Dateien, Symlinks und nicht unterstützte Dateitypen ab, erkennt aber
keine Geheimnisse innerhalb von HTML/JS/JSON. Keine `.env`, Credentials,
personenbezogenen Daten oder Source Maps veröffentlichen.

Asset-Pfade im Teilprojekt müssen zum Ziel passen:
`<portal-basis>/test-sites/<projekt-id>/`. Relative Assets sind am einfachsten.
Der Import passt keine Bundle-Pfade oder SPA-Router an. Backend-Dienste benötigen
eigenes Hosting. Testseiten teilen den Origin: keine fremden, ungeprüften Builds.

## Bauen und prüfen

```bash
python main.py check
python -m unittest discover -s tests -v
python main.py build --site-url https://example.org/kiflow
```

Ohne `--site-url` wird für die lokale Domain-Wurzel gebaut. Bei Unterpfaden
immer die vollständige öffentliche Basis-URL übergeben. Die Ausgabe in `output/`
kann von jedem statischen Webserver ausgeliefert werden.

## Online veröffentlichen

Hier ist **noch kein Remote-Repository, keine Domain und kein Hosting verbunden**.
Der Build allein schaltet nichts online.

Für GitHub Pages:

1. Ordner in einem GitHub-Repository versionieren; Standardbranch `main` verwenden
   oder den Branch-Filter in `.github/workflows/pages.yml` anpassen.
2. In **Settings → Pages → Source → GitHub Actions** aktivieren.
3. Betreiber-/Datenschutzinformationen und Verantwortliche ergänzen.
4. Auf `main` pushen oder den Workflow manuell starten.

Der Workflow prüft auch Pull Requests, veröffentlicht aber nur Pushes auf `main`
und manuelle Starts. Die Pages-Basis-URL wird automatisch übernommen. Bei Pages
für private Repositories die tatsächliche öffentliche Sichtbarkeit vorab prüfen.
Neue Testseiten gehen mit demselben Portal-Deployment online.

Alternativ `output/` nach einem Build mit korrekter `--site-url` auf einen
statischen HTTPS-Host übertragen. Keine persönliche Token-Konfiguration nötig.

## Inhaltlicher Stand

Das Register erfasst 17 dokumentierte Projekte und Teilpakete: KI Core,
KI Knowledge, Code Assist, Konfiguration, Widgets, Betriebswerkzeuge, FlowCoach
und die SimWorld-Projektfamilie einschließlich vorbereiteter Node-Pakete.
Die Einordnung basiert auf lokaler Projektdokumentation, nicht auf einem Audit
laufender Dienste. Nächste Schritte sind redaktionelle Vorschläge.
SimWorld und WidgetKit haben explizit statische Layout-Demos, keine Live-Anbindung.

Quellen und Bestandsgrenzen:
[docs/architecture/content-sources.md](docs/architecture/content-sources.md).

Architektur und Grenzen: [docs/architecture/portal.md](docs/architecture/portal.md).
