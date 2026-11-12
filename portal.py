"""Validated content shared by the CLI and Pelican configuration."""

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
STATIC_EXTENSIONS = {
    ".html", ".css", ".js", ".mjs", ".json", ".svg", ".png", ".jpg",
    ".jpeg", ".webp", ".avif", ".gif", ".ico", ".woff", ".woff2", ".ttf",
    ".txt", ".xml", ".webmanifest", ".wasm", ".pdf", ".mp4", ".webm",
}
PHASES = {
    "aufbau": "Im Aufbau", "mvp": "MVP-Basis", "geplant": "Geplant",
    "entwicklung": "In Entwicklung", "vorab": "Vorabpaket",
}


def validate_site_url(value: str) -> str:
    if not value:
        return ""
    parsed = urlsplit(value)
    port = parsed.port
    if (
        parsed.scheme not in {"https", "http"} or not parsed.hostname
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or any(character.isspace() for character in value)
        or "\\" in value or any(part in {".", ".."} for part in parsed.path.split("/"))
        or (port is not None and port == 0)
    ):
        raise ValueError("site-url muss eine HTTP(S)-URL ohne Zugangsdaten, Query oder Fragment sein.")
    return value.rstrip("/")


def validate_static_tree(source: Path) -> None:
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f"Kein reguläres statisches Verzeichnis: {source}")
    if not (source / "index.html").is_file():
        raise ValueError(f"index.html fehlt in {source}")
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symbolische Links sind in Testseiten nicht erlaubt: {path}")
        if any(part.startswith(".") for part in path.relative_to(source).parts):
            raise ValueError(f"Versteckte Dateien/Ordner sind in Testseiten nicht erlaubt: {path}")
        if path.is_file() and path.suffix.lower() not in STATIC_EXTENSIONS:
            raise ValueError(f"Keine freigegebene statische Datei: {path}")
        if not path.is_dir() and not path.is_file():
            raise ValueError(f"Spezialdateien sind nicht erlaubt: {path}")


def load_projects() -> list[dict]:
    previews = ROOT / "test-sites"
    if previews.is_symlink() or (previews.exists() and not previews.is_dir()):
        raise ValueError("test-sites muss ein normales Verzeichnis sein.")
    projects = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    if not isinstance(projects, list) or not projects:
        raise ValueError("projects.json muss eine nicht leere Liste enthalten.")
    seen = set()
    required = {"id", "name", "summary", "category", "phase", "owner", "next_step", "tags", "preview_kind"}
    for project in projects:
        if not isinstance(project, dict) or not required <= project.keys():
            raise ValueError(f"Projektdefinition unvollständig; Pflichtfelder: {sorted(required)}")
        for field in required - {"tags"}:
            if not isinstance(project[field], str) or not project[field].strip():
                raise ValueError(f"Projektfeld {field} muss ein nicht leerer Text sein.")
        slug = project["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in seen:
            raise ValueError(f"Ungültige oder doppelte Projekt-ID: {slug}")
        seen.add(slug)
        if project["phase"] not in PHASES:
            raise ValueError(f"Unbekannte Phase für {slug}: {project['phase']}")
        if project["preview_kind"] not in {"none", "demo", "test"}:
            raise ValueError(f"Unbekannte Vorschau-Art für {slug}.")
        if not isinstance(project["tags"], list) or not all(
            isinstance(tag, str) and tag.strip() for tag in project["tags"]
        ):
            raise ValueError(f"tags muss eine Liste von Texten sein: {slug}")
        preview = ROOT / "test-sites" / slug
        if project["preview_kind"] != "none" and not (preview / "index.html").is_file():
            raise ValueError(f"Vorschau für {slug} konfiguriert, aber index.html fehlt.")
    return projects
