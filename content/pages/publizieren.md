Title: Ein gemeinsamer Ort für Testseiten.
Slug: publizieren
Kicker: Publishing & Vorschauen
Summary: Statische Builds der Teilprojekte werden unter einer gemeinsamen Website erreichbar. Ein klarer Import- und Build-Weg hält Inhalt, Vorschau und Deployment zusammen.

## Was hier veröffentlicht werden kann

Ein Teilprojekt liefert einen **fertigen statischen Build** mit `index.html`, Stylesheets, JavaScript und benötigten Medien. Dieser wird unter `test-sites/<projekt-id>/` ausgeliefert. Die Projektkarte verlinkt auf diesen Stand.

Das funktioniert für HTML-Demos, Dokumentation, exportierte Frontends und kleine interaktive Anwendungen ohne Serverpflicht. **Go-Services, Python-APIs, Next.js-Serverfunktionen, Datenbanken und Modellserver laufen nicht auf einem statischen Host.**

Die mitgelieferte [IA3-Vorschau](../test-sites/ia3-simworld/) ist eine illustrative Layout-Demo. Sie zeigt weder eine laufende Simulation noch echte Agentenentscheidungen.

Auch die [WidgetKit-Galerie](../test-sites/widgetkit/) ist ein statisches Layout-Beispiel mit synthetischen Inhalten, kein aktiver Dashboard-Builder.

## Lokal vorbereiten

Python 3.11 oder neuer wird benötigt:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py serve
```

Die lokale Website ist unter `http://127.0.0.1:8000` erreichbar. Der Server bindet bewusst nur an localhost und ist kein Produktionsserver. Nach Inhaltsänderungen beenden und neu starten; es gibt kein automatisches Live-Reload.

## Ein Teilprojekt übernehmen

1. Projekt im Register `projects.json` anlegen oder eine bestehende ID verwenden.
2. Im Quellprojekt einen statischen Build erstellen und prüfen.
3. Den Build mit dem CLI übernehmen.
4. Portal bauen und Ergebnis im Browser kontrollieren.

```bash
python main.py stage ia3-simworld /pfad/zum/freigegebenen/dist
python main.py check
python main.py build
```

`stage` ersetzt die bisherige Testseite dieser Projekt-ID vollständig und setzt `preview_kind` auf `test`. Der ursprüngliche Quell-Build bleibt unverändert. Ohne `index.html`, bei symbolischen Links, versteckten Dateien oder nicht freigegebenen Dateitypen bricht der Import mit einer Fehlermeldung ab.

**Wichtig:** Diese Strukturprüfung ist kein Geheimnis- oder Sicherheits-Audit. HTML, JavaScript und JSON können ebenfalls vertrauliche Inhalte enthalten. Vor dem Import alle Artefakte prüfen; keine `.env`-Dateien, Tokens, personenbezogenen Daten oder internen Quellkarten veröffentlichen.

## Unterpfade richtig behandeln

Ein Teilprojekt liegt nicht an der Domain-Wurzel. Assets müssen relativ zum Build oder mit dem vollständigen Zielpräfix referenziert werden.

```text
Portal:    https://example.org/kiflow/
Testseite: https://example.org/kiflow/test-sites/ia3-simworld/
```

Ein Link auf `/assets/app.js` wäre dort falsch, sofern diese Datei nicht tatsächlich an der Domain-Wurzel liegt. Der Import schreibt HTML und JavaScript bewusst **nicht** um. Bei SPA-Routern Hash-Routing nutzen oder tatsächlich exportierte HTML-Routen erzeugen; GitHub Pages bietet keine frei konfigurierbare SPA-Rewrite-Regel.

Für einen Next.js-Export im Quellprojekt `output: "export"` und den passenden `basePath` konfigurieren. Servergebundene Funktionen müssen ersetzt oder separat betrieben werden.

## Öffentlich bauen

```bash
python main.py build --site-url https://example.org/kiflow
```

Das vollständige Ergebnis liegt in `output/`. Nur dieses Verzeichnis wird durch den Webhost ausgeliefert. Die URL beeinflusst das Portal-Theme; importierte Testseiten müssen selbst korrekt für ihren Unterpfad gebaut sein.

## GitHub Pages

Der vorbereitete Workflow `.github/workflows/pages.yml` prüft und baut die Website. Er veröffentlicht bei einem Push auf `main` oder einem manuellen Start. Dafür muss dieser Ordner zuerst in einem GitHub-Repository liegen und unter **Settings → Pages → Source** muss **GitHub Actions** aktiviert sein.

Der Workflow ermittelt die Pages-Basis-URL über die GitHub-Aktion, sodass sowohl Repository-Unterpfade als auch eine später konfigurierte eigene Domain berücksichtigt werden. Pull Requests werden geprüft, aber nicht öffentlich deployt. Es werden keine persönlichen Zugriffstokens im Projekt hinterlegt.

**Hier ist noch kein Remote-Repository oder öffentlicher Host verbunden.** Ein lokaler Build veröffentlicht nichts ins Internet. Alternative statische Hosts können ebenfalls den Inhalt von `output/` ausliefern; die Ziel-URL muss beim Build angegeben werden.

## Vertrauensgrenze

Testseiten unter derselben Domain teilen einen Browser-Origin. Nur kontrollierte und freigegebene Builds hier aufnehmen. Ungeprüfte Fremdprojekte oder nicht vertrauenswürdige Vorschauen brauchen getrennte Origins, beispielsweise eigene Subdomains. Das Portal ersetzt keine Laufzeit-Isolation.

Vor der öffentlichen Freigabe auch [Verantwortung und Transparenz](../governance/) bearbeiten.
