from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REQUIRED_FILES = ("style.css", "script.js", "cv.html")

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.anchors = []
        self.project_cards = 0
        self.local_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        href = attrs.get("href", "")
        if href.startswith("#") and len(href) > 1:
            self.anchors.append(href[1:])
        if tag == "article" and "project-card" in attrs.get("class", "").split():
            self.project_cards += 1
        for key in ("href", "src"):
            value = attrs.get(key, "")
            if value and not value.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
                path = value.split("?", 1)[0].split("#", 1)[0]
                if path:
                    self.local_assets.append(path)

def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)

if not INDEX.is_file():
    fail("index.html is missing")

for filename in REQUIRED_FILES:
    if not (ROOT / filename).is_file():
        fail(f"required file is missing: {filename}")

parser = SiteParser()
parser.feed(INDEX.read_text(encoding="utf-8"))

duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
if duplicates:
    fail(f"duplicate HTML ids: {', '.join(duplicates)}")

missing_anchors = sorted(set(parser.anchors) - set(parser.ids))
if missing_anchors:
    fail(f"navigation targets do not exist: {', '.join(missing_anchors)}")

if parser.project_cards != 8:
    fail(f"expected 8 project cards, found {parser.project_cards}")

missing_assets = sorted({p for p in parser.local_assets if not (ROOT / p).is_file()})
if missing_assets:
    fail(f"local linked files are missing: {', '.join(missing_assets)}")

js = (ROOT / "script.js").read_text(encoding="utf-8")
if re.search(r"CV_Agustin_Cabral_(ES|EN)\.pdf", js):
    fail("JavaScript still references missing CV PDF files")

print("PASS: required files exist")
print("PASS: no duplicate IDs")
print("PASS: all in-page navigation targets exist")
print("PASS: exactly 8 project cards")
print("PASS: all local linked assets exist")
print("PASS: no broken PDF download references")
