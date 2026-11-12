Title: Ein Ökosystem, das zusammenwirkt.
Slug: oekosystem
Kicker: Architektur & Zusammenhänge
Summary: Kiflow ist der gemeinsame Orientierungsrahmen für KI, Agenten, Simulation und Erlebnisse. Klare Grenzen zwischen den Bausteinen machen das Ganze verständlich und erweiterbar.

## Das gemeinsame Bild

Wir wollen KI nicht nur als einzelne Anwendung betrachten. Interessant wird sie dort, wo Modelle, handelnde Agenten, dynamische Umgebungen und menschliche Perspektiven zusammenkommen. Das Portal macht diese Zusammenhänge sichtbar und gibt jedem Teilprojekt einen nachvollziehbaren Platz.

**Kiflow ist hier zunächst ein Informations- und Veröffentlichungsportal, keine bereits implementierte zentrale KI-Laufzeit.** Die vorhandenen Projektfamilien reichen von KI-Clients und Wissensverarbeitung über wiederverwendbare Konfiguration und UI bis zu Simulation und Betriebswerkzeugen. Das Register beschreibt Projekte und Teilpakete, keine 17 voneinander unabhängigen fertigen Anwendungen.

## Intelligenz {#intelligenz}

### KI Core {#ki-core}

KI Core stellt eine gemeinsame Python-Abstraktion für Modellanbieter bereit, einschließlich Streaming und konfigurationsbezogener Dienste. Anwendungen sollen den Provider-Zugriff wiederverwenden, statt eigene, widersprüchliche Integrationsschichten zu bauen.

### KI Code Assist {#kicli-code-assist}

Die terminalbasierte Assistenz verbindet Projektkontext und KI-Anfragen mit einer Diff-Vorschau. Menschliche Kontrolle vor der Übernahme ist ein zentrales Prinzip. Das Portal dokumentiert diesen Ablauf, führt aber keine generierten Befehle aus.

### Agentenentscheidungen

Die Agentenschicht beantwortet die Frage: **Was tut ein Agent als Nächstes – und warum?** Sie verarbeitet Beobachtungen und liefert Aktionen. Die Ausführung und Validierung dieser Aktionen gehören in die Simulation, nicht in das Sprachmodell oder die Oberfläche.

- Beobachtungen und Aktionen erhalten explizite, versionierte Schemas.
- Deterministische Regeln bilden die verständliche Basis.
- Generative Modelle können später ergänzen, müssen aber hinsichtlich Kosten, Datenschutz und Reproduzierbarkeit bewertet werden.
- Entscheidungen sollen anhand von Eingaben, Regeln und Ergebnissen nachvollziehbar sein.

### Agent Logic {#agent-service}

Die aktuelle Kooperationsdokumentation nennt einen Python-Service mit Mesa und gRPC als vorhandenen Anknüpfungspunkt. Welche Agentenabläufe vollständig integriert sind, muss im Quellprojekt nachgewiesen werden. Ein Modellanbieter oder ein produktiver generativer Agentenbetrieb wird hier nicht vorausgesetzt.

## Wissen {#wissen}

### KI Knowledge {#ki-knowledge}

KI Knowledge verarbeitet Quellen und ihre Beziehungen. Die Projektbeschreibung nennt Ingestion, Wissensgraphen, hybride Suche, wissensbasierten Chat und eine Django-Oberfläche. Die Textwerkstatt ergänzt Markdown-Snapshots, eigene Texte mit Revisionen, Markierungen und expliziten KI-Kontext.

Diese Funktionsbereiche sind dokumentierte Bestandteile des Quellprojekts, **kein Nachweis, dass alle Workflows fertig oder öffentlich erreichbar sind**. Für eine Portal-Testseite werden freigegebene synthetische Beispiele benötigt; das Django-Backend wird separat betrieben.

### KI FlowCoach {#ki-flowcoach}

FlowCoach ist ein Konzept für einen Coaching-Dialog mit kuratiertem Wissenskontext und menschlicher fachlicher Begleitung. Die dokumentierte Konzeptphase umfasst noch keine lauffähige Anwendung oder Provider-Anbindung. Ein erster textbasierter Ablauf soll mit synthetischen Gesprächen arbeiten. Der geplante Assistent ist kein Ersatz für Diagnostik oder professionelle Behandlung.

## Simulation {#simulation}

Simulationen besitzen den autoritativen Weltzustand. Sie definieren Zeit, Regeln und gültige Zustandsübergänge. Agenten schlagen Aktionen vor; die Simulation entscheidet, welche davon wirksam werden.

### IA3 SimWorld {#ia3-simworld}

Der bereitgestellte Ausgangskontext beschreibt eine MVP-Basis mit Tick-Schleife, Zustandsendpunkt, Gateway und einer Weboberfläche. Neuere lokale Dokumentation nennt außerdem Go-Föderation, Mesa/gRPC und vorbereitete gemeinsame Python-Pakete. Diese Dienste liegen **nicht in diesem Portal-Verzeichnis** und wurden hier nicht als laufendes System verifiziert.

| Baustein | Verantwortung | Geplanter / beschriebener Stack |
|---|---|---|
| World Simulation | Weltzustand, Ticks, Aktionsvalidierung | Go |
| Agent Service | Beobachtungen auswerten, Aktionen bestimmen | Python, gRPC |
| API Gateway | HTTP-Zugriff und später Streaming zur UI | Go, HTTP / WebSocket |
| Web Client | Beobachten, steuern, erklären | Next.js, React |
| Infrastruktur | Lokaler Betrieb, später verteilte Dienste | Kubernetes, Helm; PostgreSQL / Redis nach Bedarf |

Der fachliche Ablauf lautet: **UI → Gateway → Simulation → Agentenentscheidung → validierte Zustandsänderung → UI**. Async-Domain-Events über NATS sind eine Ausbauperspektive; eine vollständig integrierte Event-Infrastruktur wird hier nicht behauptet.

## Gemeinsame Konfiguration

### YAML Config Wizard {#yaml-cfg-wizard}

Der Resolver hält Konfigurationsebenen explizit: Defaults, Profile, Stages, Runtime und Umgebungsvariablen. Validierung gehört zur gemeinsamen Basis. App-spezifische Regeln und präzise Schemas bleiben nötig; eine generische Bibliothek kann diese nicht erfinden.

### YAML Config Wizard UI {#yaml-cfg-wizard-ui}

Der frameworkunabhängige Renderer liefert HTML, CSS und JavaScript für einen begrenzten Konfigurationseditor. Die Host-Anwendung besitzt den authentifizierten Endpunkt und die serverseitige Validierung. Eine statische Vorschau darf diesen Endpunkt illustrieren, aber keine echten Zugangsdaten oder Runtime-Werte veröffentlichen.

### IA3 Config Editor {#ia3-config-editor}

Das vorbereitete IA3-Paket stellt eine projektspezifische Startup-Editor-Factory bereit. Es ist bewusst von der generischen UI getrennt. Neustartanforderungen und erlaubte Felder müssen vom jeweiligen Host bestätigt werden.

## Wiederverwendbare Oberflächen

### WidgetKit {#widgetkit}

WidgetKit trennt Widget-Metadaten, hostseitige Datenaufbereitung und Jinja-Rendering. Diese frameworkneutrale Basis kann in mehreren Anwendungen wiederverwendet werden. Die [statische Widget-Demo](../test-sites/widgetkit/) zeigt das Darstellungsprinzip, nicht den laufenden Builder.

### WidgetKit Django {#widgetkit-django}

Die Django-Integration stellt wiederverwendbare Builder- und Layout-Verträge bereit. Host-Anwendungen liefern ihre Registries, Daten und Persistenzadapter. Das Portal übernimmt keine Django-Laufzeit, sondern kann exportierte Demonstrationen zentral zugänglich machen.

## Projektübergreifende Kooperation

### KI Node Core {#ki-node-core}

Frameworkfreie Python-Typen und Adapter-Schnittstellen bilden die vorbereitete Vertragsbasis.

### KI Node HTTP {#ki-node-http}

Der begrenzte HTTP-JSON-Client bildet die vorbereitete Transportbasis.

Die SimWorld-Dokumentation beschreibt diese Pakete als vorbereitete Vorabdistributionen: frameworkfreie Node-Typen und Adapterverträge sowie eine begrenzte HTTP-JSON-Transportbasis. Eine produktive Integration zwischen SimWorld und KI Knowledge besteht daraus **nicht automatisch**.

Vor einem Pilot brauchen beide Projekte einen vereinbarten Fachadapter, ein versioniertes Wire-Schema, Fixtures und klare Zuständigkeiten für Storage und Deduplizierung. Lizenz, Maintainer und spätere externe Distribution bleiben zu klären.

Fachliche Verantwortung bleibt getrennt: **SimWorld besitzt Simulationszustände; KI Knowledge besitzt seine Wissensdomänen.** Gemeinsame Node-Infrastruktur darf diese Grenzen nicht verwischen. NATS, CRDTs und automatische Coordinator-Wahl bleiben spätere Optionen.

## Koordination und Betrieb

### KI Ecosystem {#ki-ecosystem}

Der koordinierende Projektverbund beschreibt die gemeinsamen Komponenten und deren Integration. Das Portal bildet diese Orientierung ab, ersetzt aber nicht die aktuelle Installation und Konfiguration der Quellprojekte.

### Stack Control {#stackctl}

Stack Control ist das gemeinsame Werkzeug für Repository-Koordination und Service-Lifecycle. Die Projektbeschreibung nennt lokale Prozesse, Minikube und Kubernetes mit Helm als Zielarten. Ein Stack wird zentral beschrieben; projektspezifische Loader liefern die aufgelöste Konfiguration.

Dieser Backend-Betrieb ist **ein anderer Weg** als das Publishing dieser Website. Das Portal erzeugt statische Artefakte, während die Quellprojekte ihre Dienste und Abhängigkeiten separat verwalten.

## Erlebnis {#erlebnis}

Eine gute Oberfläche übersetzt technische Zustände in verständliche Zusammenhänge. Ein erster Webzugang soll Beobachtung und Interaktion ermöglichen; Lern- und Spielmodi können darauf aufbauen.

### Experience Layer {#experience-layer}

Die geplante Erlebnis-Schicht umfasst spielerische und pädagogische Zugänge. AR ist eine spätere Perspektive, kein schon verfügbares Produkt. Vor einer Umsetzung werden Zielgruppe, ein konkretes Szenario und ein überprüfbares Lern- oder Erlebnisziel benötigt.

## Wissen und Verbindung {#kiflow-web}

Dieses Portal bündelt Beschreibungen, Projektstatus, Arbeitsweise und Testseiten. **Markdown** enthält die redaktionellen Inhalte, **projects.json** die Projektübersicht und **Pelican** erzeugt daraus statische HTML-Dateien.

Das Portal braucht weder Datenbank noch Modellzugang. Es verwendet keine extern geladenen Schriftarten, Tracking-Skripte oder eingebetteten Drittanbieter-Dienste. Damit bleibt die Basis einfach auslieferbar und lokal nutzbar.

## Technische Grenzen bewusst halten

- Das Portal ist kein Ersatz für Quellcode-Repositories, Tickets oder Laufzeit-Monitoring.
- Statische Testseiten sind keine Backend-Deployments.
- Gemeinsame Schnittstellen gehören in die jeweiligen Quellprojekte; dieses Portal dokumentiert sie.
- Projektstatus wird redaktionell gepflegt und ist keine Verfügbarkeitsanzeige.

Die nächsten Schritte stehen in der [Roadmap](../roadmap/). Statische Ergebnisse werden über den [Publishing-Weg](../publizieren/) zugänglich.
