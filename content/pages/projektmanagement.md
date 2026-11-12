Title: Gemeinsam klar weiterkommen.
Slug: projektmanagement
Kicker: Projektmanagement & Arbeitsweise
Summary: Ein gemeinsamer Rahmen für Ziele, Verantwortlichkeiten, Entscheidungen und überprüfbare Ergebnisse – ohne mehr Prozess als nötig.

## Eine Quelle pro Information

Das Portal erklärt **wozu** ein Projekt existiert und **wie** es ins Ökosystem passt. Das Quell-Repository enthält die ausführbare Wahrheit. Das Issue-Board hält die konkrete Arbeit fest. Entscheidungen werden als kurze Architecture Decision Records im jeweiligen Projekt dokumentiert.

| Information | Zuständiger Ort | Pflegeanlass |
|---|---|---|
| Projektziel, Phase, nächster Schritt | `projects.json` in diesem Portal | Nach einer relevanten Projektentscheidung |
| Architektur und Zusammenhänge | Markdown-Seiten im Portal | Wenn sich Grenzen oder Verträge ändern |
| Aufgaben und Fehler | Issues im jeweiligen Quell-Repository | Bei Beginn, Blockade und Abschluss |
| Technische Entscheidung | Projekt-Dokumentation / ADR | Vor oder mit der Umsetzung |
| Testseite | Statischer Build aus dem Teilprojekt | Nach einem freigegebenen Stand |
| Laufzeitstatus | Monitoring des betriebenen Dienstes | Automatisch, nicht hier nachgebildet |

## Vom Vorhaben zum Ergebnis

### 1. Vorhaben klären

Jedes Vorhaben beginnt mit einer verständlichen Problemstellung, einer Zielgruppe und einem erwarteten Nutzen. Dazu gehören die Grenzen: Was ist ausdrücklich **nicht** Teil dieses Schritts?

### 2. Einen kleinen prüfbaren Schritt schneiden

Ein Arbeitspaket soll ein beobachtbares Ergebnis liefern. Statt „Agenten verbessern“ heißt es beispielsweise: „Eine Beobachtung wird über den vereinbarten Vertrag verarbeitet und liefert eine validierbare Aktion.“

### 3. Umsetzen und zeigen

Arbeit geschieht im Teilprojekt. Änderungen werden dort geprüft und reviewed. Ein statischer UI-Build kann anschließend als Testseite in dieses Portal übernommen werden. Backend-Änderungen brauchen einen separaten Betriebsweg.

### 4. Ergebnis bewerten

Die Abnahme erfolgt gegen vorher formulierte Kriterien. Abweichungen und Feedback werden dokumentiert. Erst danach wird entschieden, welcher nächste Schritt im Projektregister sichtbar wird.

## Einfacher Aufgabenfluss

**Backlog → Bereit → In Arbeit → Review → Erledigt**

„Blockiert“ ist eine explizite Kennzeichnung mit Ursache, zuständiger Person und benötigter Entscheidung. Ein blockiertes Thema wird nicht durch einen optimistischen Status verdeckt. Parallel begonnene Aufgaben bleiben begrenzt; Fertigstellen ist wichtiger als möglichst viel gleichzeitig anzufangen.

## Was in eine Aufgabe gehört

```text
Titel: Ein konkretes Ergebnis, nicht nur ein Thema
Problem / Nutzen:
Projekt / betroffene Schnittstellen:
Verantwortlich:
Umfang:
Nicht im Umfang:
Abhängigkeiten:
Akzeptanzkriterien:
Nachweis / Test:
Dokumentationsbedarf:
```

In diesem Portal liegen passende GitHub-Issue-Vorlagen für Arbeitspakete und Fehlerberichte bereit. Sie werden nutzbar, sobald der Ordner ein GitHub-Repository ist.

## Verantwortlichkeiten

| Rolle | Verantwortung |
|---|---|
| Projektverantwortung | Ziel, Priorität, Abnahme und Projektstatus |
| Umsetzung | Code, Tests, Dokumentation und nachvollziehbare Änderungen |
| Review | Fachliche und technische Prüfung, besonders an Schnittstellen |
| Veröffentlichung | Freigegebenen Build, Zieladresse und Datenfreigabe prüfen |

Eine Person kann mehrere Rollen übernehmen. Die Zuständigkeit muss dennoch benannt sein. Die anfänglichen Einträge „Noch zu benennen“ sind **offene Punkte**, keine automatisch zugewiesenen Verantwortlichkeiten.

## Definition of Ready

- Das Problem und der erwartete Nutzen sind verständlich.
- Umfang und Akzeptanzkriterien sind konkret.
- Relevante Abhängigkeiten und Zuständigkeiten sind bekannt.
- Es ist klar, wie das Ergebnis nachgewiesen wird.

## Definition of Done

- Die vereinbarten Akzeptanzkriterien sind nachgewiesen.
- Relevante Tests und Prüfungen sind erfolgreich.
- Schnittstellen und betroffene Dokumentation sind aktualisiert.
- Keine Zugangsdaten, personenbezogenen Testdaten oder internen Inhalte werden veröffentlicht.
- Falls nötig ist eine eindeutig gekennzeichnete Testseite vorhanden.
- Projektstatus und nächster Schritt spiegeln das Ergebnis wider.

## Entscheidungen statt stiller Annahmen

Größere technische Entscheidungen erhalten eine kurze Notiz: **Kontext, Optionen, Entscheidung, Folgen**. Eine offene Frage bleibt sichtbar, bis sie beantwortet wurde. Eine Demo wird nicht als fertiges Produkt dargestellt.

Für den Portaleinstieg sind zwei Entscheidungen noch offen: das öffentliche Hosting-Ziel und die benannten Projektverantwortlichen. Sie sind vor der ersten öffentlichen Freigabe zu klären.
