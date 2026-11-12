import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from portal import PHASES, ROOT, load_projects

AUTHOR = "Kiflow"
SITENAME = "Kiflow"
SITESUBTITLE = "Ideen verbinden. Intelligenz gestalten."
SITEURL = ""
TIMEZONE = "Europe/Berlin"
DEFAULT_LANG = "de"
PATH = str(ROOT / "content")
THEME = str(ROOT / "theme")
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = []
STATIC_PATHS = []
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
DIRECT_TEMPLATES = []
TEMPLATE_PAGES = {"home.html": "index.html", "projects.html": "projekte/index.html"}
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DEFAULT_PAGINATION = False
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = False
JINJA_ENVIRONMENT = {"autoescape": True}
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {"permalink": False},
    },
    "output_format": "html5",
}
PROJECTS = load_projects()
PHASES = PHASES
NAV = [
    ("Ökosystem", "oekosystem/"),
    ("Projekte", "projekte/"),
    ("Projektmanagement", "projektmanagement/"),
    ("Roadmap", "roadmap/"),
]
