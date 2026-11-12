import contextlib
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote, urljoin, urlsplit

import main
import portal


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        for attribute in ("href", "src"):
            if attributes.get(attribute):
                self.links.append(attributes[attribute])


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.projects = copy.deepcopy(portal.load_projects()[:1])
        self.registry = self.root / "projects.json"
        self.write_projects()
        self.root_patch = patch.object(portal, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def write_projects(self):
        self.registry.write_text(json.dumps(self.projects), encoding="utf-8")

    def test_valid_registry(self):
        self.assertEqual(portal.load_projects(), self.projects)

    def test_invalid_definitions_fail_explicitly(self):
        cases = [
            {"id": "../unsafe"}, {"phase": "almost-done"},
            {"tags": "Python"}, {"tags": [17]}, {"owner": ""},
            {"preview_kind": "live"}, {"preview_kind": "test"},
        ]
        for change in cases:
            with self.subTest(change=change):
                self.projects = [dict(self.projects[0], **change)]
                self.write_projects()
                with self.assertRaises(ValueError):
                    portal.load_projects()
                self.projects = copy.deepcopy(json.loads(
                    (Path(__file__).resolve().parents[1] / "projects.json").read_text()
                )[:1])

    def test_duplicates_and_missing_fields_rejected(self):
        self.projects *= 2
        self.write_projects()
        with self.assertRaisesRegex(ValueError, "doppelte"):
            portal.load_projects()
        self.projects = [{"id": "incomplete"}]
        self.write_projects()
        with self.assertRaisesRegex(ValueError, "unvollständig"):
            portal.load_projects()

    def test_preview_requires_index(self):
        self.projects[0]["preview_kind"] = "demo"
        self.write_projects()
        with self.assertRaisesRegex(ValueError, "index.html"):
            portal.load_projects()

    def test_preview_root_symlink_rejected(self):
        (self.root / "test-sites").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "normales Verzeichnis"):
            portal.load_projects()


class StaticImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "dist"
        self.source.mkdir()
        (self.source / "index.html").write_text("<h1>Test</h1>", encoding="utf-8")
        projects = copy.deepcopy(portal.load_projects()[:1])
        self.project_id = projects[0]["id"]
        (self.root / "projects.json").write_text(json.dumps(projects), encoding="utf-8")
        for module in (main, portal):
            root_patch = patch.object(module, "ROOT", self.root)
            root_patch.start()
            self.addCleanup(root_patch.stop)

    def test_stage_replaces_previous_build_and_marks_test(self):
        target = self.root / "test-sites" / self.project_id
        target.mkdir(parents=True)
        (target / "old.css").write_text("old", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            main.stage(self.project_id, self.source)
        self.assertTrue((target / "index.html").is_file())
        self.assertFalse((target / "old.css").exists())
        self.assertEqual(portal.load_projects()[0]["preview_kind"], "test")
        self.assertTrue((self.source / "index.html").is_file())

    def test_no_index_no_import(self):
        (self.source / "index.html").unlink()
        with self.assertRaisesRegex(ValueError, "index.html"):
            main.stage(self.project_id, self.source)

    def test_sensitive_or_non_static_files_rejected(self):
        for filename in (".env", ".git/config", "private.key", "server.py", "app.js.map"):
            with self.subTest(filename=filename):
                file = self.source / filename
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("not public", encoding="utf-8")
                with self.assertRaises(ValueError):
                    portal.validate_static_tree(self.source)
                file.unlink()
                if file.parent != self.source:
                    file.parent.rmdir()

    def test_symlinks_rejected(self):
        (self.source / "linked.css").symlink_to(self.source / "index.html")
        with self.assertRaisesRegex(ValueError, "Links"):
            portal.validate_static_tree(self.source)

    def test_source_directory_symlink_rejected(self):
        link = self.root / "linked"
        link.symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Link"):
            main.stage(self.project_id, link)

    def test_unknown_project_and_overlapping_source_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unbekanntes Projekt"):
            main.stage("missing", self.source)
        target = self.root / "test-sites" / self.project_id
        target.mkdir(parents=True)
        (target / "index.html").write_text("<h1>Old</h1>")
        with self.assertRaisesRegex(ValueError, "ineinander"):
            main.stage(self.project_id, target)


class SiteUrlTests(unittest.TestCase):
    def test_valid_urls(self):
        for source, expected in [
            ("", ""), ("https://example.org/", "https://example.org"),
            ("https://example.org/kiflow/", "https://example.org/kiflow"),
            ("http://localhost:8000", "http://localhost:8000"),
        ]:
            with self.subTest(source=source):
                self.assertEqual(portal.validate_site_url(source), expected)

    def test_invalid_urls(self):
        for source in (
            "/kiflow", "ftp://example.org", "javascript:alert(1)",
            "https://user:password@example.org", "https://example.org?x=1",
            "https://example.org/#test", "https://example.org/../private",
            "https://example.org/my site", "https://example.org\\bad",
            "http://localhost:not-a-port", "http://localhost:99999", "http://localhost:0",
        ):
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    portal.validate_site_url(source)


class BuildTests(unittest.TestCase):
    def check_build(self, base):
        result = subprocess.run(
            [sys.executable, "main.py", "build", "--site-url", base],
            cwd=portal.ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = portal.ROOT / "output"
        documents = {
            path: Document(path.read_text(encoding="utf-8"))
            for path in output.rglob("*.html")
        }
        previews = sum(project["preview_kind"] != "none" for project in portal.load_projects())
        self.assertGreaterEqual(len(documents), 7 + previews)
        origin = "https://example.org"
        prefix = urlsplit(base).path if base else ""
        for path, document in documents.items():
            relative = path.relative_to(output).as_posix()
            url = f"{origin}{prefix}/{relative}"
            for link in document.links:
                target_url = urlsplit(urljoin(url, link))
                if target_url.scheme not in {"http", "https"} or target_url.netloc != "example.org":
                    continue
                with self.subTest(page=relative, link=link, base=base):
                    target_path = unquote(target_url.path)
                    self.assertTrue(target_path.startswith(prefix + "/"), target_path)
                    target = output / target_path[len(prefix):].lstrip("/")
                    if target.is_dir():
                        target = target / "index.html"
                    self.assertTrue(target.is_file(), f"Broken link: {link} in {relative}")
                    if target_url.fragment:
                        self.assertIn(
                            unquote(target_url.fragment), documents[target].ids,
                            f"Missing anchor {link} in {relative}",
                        )
        home = (output / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("&lt;p&gt;", home)
        self.assertIn("Aus Ideen wird", home)
        projects = (output / "projekte/index.html").read_text(encoding="utf-8")
        self.assertEqual(projects.count("data-project "), len(portal.load_projects()))
        self.assertIn("Layout-Demo öffnen", projects)
        self.assertNotIn("https://fonts.", home)

    def test_root_deployment_and_links(self):
        self.check_build("")

    def test_subpath_deployment_and_links(self):
        self.check_build("https://example.org/kiflow")

    def test_failed_build_preserves_previous_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            output.mkdir()
            original = b"<h1>Last good build</h1>"
            (output / "index.html").write_bytes(original)
            with patch.object(main, "ROOT", root), patch.object(
                main.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "pelican")
            ):
                with self.assertRaises(subprocess.CalledProcessError):
                    main.build()
            self.assertEqual((output / "index.html").read_bytes(), original)
            self.assertFalse(list(root.glob(".build-*")))


if __name__ == "__main__":
    unittest.main()
