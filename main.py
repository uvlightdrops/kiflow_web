"""Build and maintain the Kiflow ecosystem portal."""

import argparse
import functools
import http.server
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from portal import ROOT, load_projects, validate_site_url, validate_static_tree


def build(site_url: str = "") -> Path:
    site_url = validate_site_url(site_url)
    projects = load_projects()
    for project in projects:
        source = ROOT / "test-sites" / project["id"]
        if source.exists():
            validate_static_tree(source)
    output = ROOT / "output"
    # Generate separately so a broken build does not replace the last good site.
    with tempfile.TemporaryDirectory(prefix=".build-", dir=ROOT) as temporary:
        destination = Path(temporary) / "site"
        subprocess.run(
            [
                sys.executable, "-m", "pelican", str(ROOT / "content"),
                "--settings", str(ROOT / "pelicanconf.py"),
                "--output", str(destination),
                "--extra-settings", f"SITEURL={json.dumps(site_url)}",
            ],
            check=True,
            cwd=ROOT,
        )
        for project in projects:
            source = ROOT / "test-sites" / project["id"]
            if source.is_dir():
                shutil.copytree(source, destination / "test-sites" / project["id"])
        if not (destination / "index.html").is_file():
            raise ValueError("Der Generator hat keine Startseite erzeugt.")
        if output.is_symlink() or (output.exists() and not output.is_dir()):
            raise ValueError("output muss ein normales Verzeichnis sein.")
        if output.exists():
            shutil.rmtree(output)
        shutil.move(str(destination), output)
    print(f"Website erstellt: {output}")
    return output


def stage(project_id: str, source: Path) -> None:
    projects = load_projects()
    project = next((item for item in projects if item["id"] == project_id), None)
    if project is None:
        raise ValueError(f"Unbekanntes Projekt: {project_id}")
    if source.is_symlink():
        raise ValueError("Der Quellordner darf kein symbolischer Link sein.")
    source = source.resolve(strict=True)
    validate_static_tree(source)
    destination = ROOT / "test-sites" / project_id
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Quell- und Zielverzeichnis dürfen nicht ineinander liegen.")
    if destination.is_symlink():
        raise ValueError("Das Ziel darf kein symbolischer Link sein.")
    with tempfile.TemporaryDirectory(prefix=".stage-", dir=ROOT) as temporary:
        copied = Path(temporary) / project_id
        shutil.copytree(source, copied)
        validate_static_tree(copied)
        destination.parent.mkdir(exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(copied), destination)
    project["preview_kind"] = "test"
    (ROOT / "projects.json").write_text(
        json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Testseite übernommen: {project_id}. Mit 'python main.py build' veröffentlichen.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="Statische Website erstellen")
    build_parser.add_argument("--site-url", default="", help="Öffentliche URL inkl. optionalem Unterpfad")
    serve_parser = commands.add_parser("serve", help="Neu bauen und lokal ansehen")
    serve_parser.add_argument("--port", type=int, default=8000)
    stage_parser = commands.add_parser("stage", help="Statischen Teilprojekt-Build übernehmen")
    stage_parser.add_argument("project", help="Projekt-ID aus projects.json")
    stage_parser.add_argument("source", type=Path, help="Build-Verzeichnis mit index.html")
    commands.add_parser("check", help="Projektregister und Testseiten prüfen")
    args = parser.parse_args()
    try:
        if args.command == "build":
            build(args.site_url)
        elif args.command == "stage":
            stage(args.project, args.source)
        elif args.command == "check":
            projects = load_projects()
            for project in projects:
                source = ROOT / "test-sites" / project["id"]
                if source.exists():
                    validate_static_tree(source)
            print(f"{len(projects)} Projekte geprüft.")
        else:
            if not 1 <= args.port <= 65535:
                raise ValueError("Port muss zwischen 1 und 65535 liegen.")
            output = build()
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(output))
            with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
                print(f"Lokale Vorschau: http://127.0.0.1:{args.port}", flush=True)
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    pass
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
