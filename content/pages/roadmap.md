Title: Der nächste sinnvolle Schritt.
Slug: roadmap
Kicker: Roadmap & Prioritäten
Summary: Erst eine verlässliche Basis, dann echte Verbindungen und schließlich neue Erlebnisse. Die Reihenfolge orientiert sich an Abhängigkeiten, nicht an erfundenen Lieferterminen.

## Wie diese Roadmap zu lesen ist

Diese Seite beschreibt die beabsichtigte Reihenfolge. Sie ist **kein verbindlicher Lieferplan**. Termine, Budget und Verantwortliche sind noch nicht vereinbart. Der tatsächliche Umsetzungsstand liegt in den Issues der jeweiligen Projekte.

## Jetzt: Orientierung und Veröffentlichung

Das Portal schafft die Grundlage für gemeinsames Verständnis:

- Ein pflegbares Projektregister und deutsche Inhalte zu Architektur und Arbeitsweise.
- Eine einheitliche Darstellung der Projektphasen und offenen nächsten Schritte.
- Ein Python-basierter Build und ein Veröffentlichungsweg für statische Teilprojektseiten.
- Eine klar gekennzeichnete SimWorld-Layout-Demo als Beispiel.

**Nächste Freigabepunkte:** Hosting und Domain festlegen, Verantwortliche benennen, öffentliche Inhalte einschließlich rechtlicher Angaben prüfen. Ein vorbereiteter Deployment-Workflow ist noch keine erfolgte Online-Veröffentlichung.

## Danach: Echte Projektstände anschließen

Das Portal erhält verifizierte Informationen aus den Teilprojekten:

1. Ansprechpartner und Integrationsstände der Kernprojekte bestätigen.
2. Für KI Knowledge, WidgetKit und SimWorld freigegebene, für Unterpfade geeignete statische Vorschauen erstellen.
3. Die Layout-Demos bei Bedarf durch echte Exporte ersetzen und als Testseiten kennzeichnen.
4. Feedback in konkrete Arbeitspakete überführen.

**Erfolgskriterium:** Eine außenstehende Person kann Ziel, Grenzen und Teststand eines Projekts verstehen, ohne Demo und Live-System zu verwechseln.

## Dann: Simulation und Agenten verbinden

Die im Projektkontext vorgesehenen technischen Prioritäten:

1. Bestehende Mesa-/gRPC-Anbindung und ihre tatsächlich abgedeckten Agentenabläufe verifizieren.
2. Einen gemeinsamen Node-Pilot zwischen SimWorld und KI Knowledge mit explizitem Wire-Schema abgrenzen.
3. Persistenz für Läufe und Agenten bei nachgewiesenem Bedarf ergänzen.
4. Explizite Domain-Events wie `sim.tick.completed` und `sim.agent.action.applied` einführen.
5. WebSocket-Streaming als Ersatz oder Ergänzung des Pollings evaluieren.

Eventing und Persistenz benötigen eigene Entscheidungen zu Fehlerbehandlung, Wiederholbarkeit und Betrieb. Sie werden nicht stillschweigend Teil dieses statischen Portals.

## Parallel: Gemeinsame Bausteine konsolidieren

KI Core, YAML Config Wizard, die Editor-UI sowie WidgetKit und seine Django-Integration bilden wiederverwendbare Grundlagen. Ihre Host-Verträge und Grenzen sollen pro Anwendung dokumentiert bleiben.

Stack Control und der Ecosystem-Verbund koordinieren Repositories und Laufzeitdienste. Eine automatische Übernahme ihres aktuellen Betriebsstatus ins Portal ist nicht implementiert; vor einer solchen Integration wären Datenfreigabe, Zugriff und Ausfallverhalten zu entscheiden.

## Perspektive: Erlebnisse und Lernen

Auf einer stabilen Basis können Lern- und Spielmodi entstehen. AR-fähige Clients sind eine spätere Option. FlowCoach benötigt als Konzeptprojekt zunächst einen textbasierten, fachlich begleiteten Durchstich. Bevor zusätzliche Clients gebaut werden, braucht es ein klar abgegrenztes Nutzungsszenario mit messbarem Nutzen.

## Risiken aktiv behandeln

| Risiko | Umgang |
|---|---|
| Zu viele parallele Ideen | Pro Projekt einen sichtbaren nächsten Schritt priorisieren |
| Demo wird als Produkt verstanden | Vorschau-Art und Grenzen direkt am Einstieg kennzeichnen |
| Schnittstellen driften auseinander | Verträge versionieren und im Quellprojekt testen |
| Unklare Zuständigkeit | Verantwortung vor Freigabe benennen |
| Teststand veröffentlicht vertrauliche Daten | Nur freigegebene statische Artefakte importieren und reviewen |
| Veraltete Projektbeschreibung | Register bei Meilensteinen und Reviews aktualisieren |

Die [Arbeitsweise](../projektmanagement/) erklärt, wie aus diesen Prioritäten überprüfbare Aufgaben werden.
