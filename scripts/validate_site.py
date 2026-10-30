from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ("index.html", "style.css", "script.js", "cv.html")

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.anchors = []
        self.project_cards = 0
        self.local_assets = []
        self.unsafe_blank_links = []
        self.images_without_alt = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        href = attrs.get("href", "")
        if href.startswith("#") and len(href) > 1:
            self.anchors.append(href[1:])
        if tag == "article" and "project-card" in attrs.get("class", "").split():
            self.project_cards += 1
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
        if tag == "a" and attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").lower().split())
            if "noopener" not in rel:
                self.unsafe_blank_links.append(href)
        for key in ("href", "src"):
            value = attrs.get(key, "")
            if value and not value.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
                path = value.split("?", 1)[0].split("#", 1)[0]
                if path:
                    self.local_assets.append(path)

def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)

for filename in REQUIRED_FILES:
    if not (ROOT / filename).is_file():
        fail(f"required file is missing: {filename}")

parsers = {}
for filename in ("index.html", "cv.html"):
    parser = SiteParser()
    try:
        parser.feed((ROOT / filename).read_text(encoding="utf-8"))
        parser.close()
    except Exception as exc:
        fail(f"could not parse {filename}: {exc}")
    parsers[filename] = parser

for filename, parser in parsers.items():
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        fail(f"{filename} has duplicate IDs: {', '.join(duplicates)}")
    missing_anchors = sorted(set(parser.anchors) - set(parser.ids))
    if missing_anchors:
        fail(f"{filename} has missing in-page targets: {', '.join(missing_anchors)}")
    missing_assets = sorted({p for p in parser.local_assets if not (ROOT / p).is_file()})
    if missing_assets:
        fail(f"{filename} has missing local assets: {', '.join(missing_assets)}")
    if parser.unsafe_blank_links:
        fail(f"{filename} has target=_blank links without noopener: {parser.unsafe_blank_links}")
    if parser.images_without_alt:
        fail(f"{filename} has {parser.images_without_alt} images without alt text")

if parsers["index.html"].project_cards != 8:
    fail(f"expected 8 project cards, found {parsers['index.html'].project_cards}")

# Keep the public profile and printable CV aligned on verified training history.
index_html = (ROOT / "index.html").read_text(encoding="utf-8")
cv_html = (ROOT / "cv.html").read_text(encoding="utf-8")
required_training = (
    "Data Analytics (Oct–Dic 2025)",
    "QA Manual Testing (Nov 2025–Feb 2026)",
    "Power BI (Jul 2026)",
    "Python MTA (Sep 2026)",
)
for item in required_training:
    if item not in index_html or item not in cv_html:
        fail(f"training history is missing or inconsistent between portfolio and CV: {item}")

js = (ROOT / "script.js").read_text(encoding="utf-8")
if re.search(r"CV_Agustin_Cabral_(ES|EN)\.pdf", js):
    fail("JavaScript still references missing CV PDF files")
if "if (!['es', 'en'].includes(lang)) return;" not in js:
    fail("language selection must reject unsupported language values")

print("PASS: required site files exist")
print("PASS: index and CV have no duplicate IDs")
print("PASS: all in-page navigation targets exist")
print("PASS: all local assets referenced by index and CV exist")
print("PASS: external target=_blank links include noopener protection")
print("PASS: images have alt attributes")
print("PASS: exactly 8 project cards")
print("PASS: portfolio and CV training history are consistent")
print("PASS: CV download references are not broken")
print("PASS: language selection accepts only ES/EN")
