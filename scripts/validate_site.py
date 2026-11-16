from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ("index.html", "style.css", "script.js", "cv.html", "cv-en.html")

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

# Cloudflare's Git-connected build deploys the committed dist/ directory directly.
# Keep it synchronized with the editable source files at the repository root.
for filename in REQUIRED_FILES:
    source = ROOT / filename
    deployed = ROOT / "dist" / filename
    if not deployed.is_file():
        fail(f"Cloudflare deployment asset is missing: dist/{filename}")
    if source.read_bytes() != deployed.read_bytes():
        fail(f"dist/{filename} is out of sync with {filename}; refresh dist/ before committing")

parsers = {}
for filename in ("index.html", "cv.html", "cv-en.html"):
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

if parsers["index.html"].project_cards != 6:
    fail(f"expected 6 selected project cards, found {parsers['index.html'].project_cards}")

wrangler = (ROOT / "wrangler.jsonc").read_text(encoding="utf-8")
if '"name": "portfolio-agustin"' not in wrangler:
    fail("wrangler.jsonc must target the portfolio-agustin Worker")

index_html = (ROOT / "index.html").read_text(encoding="utf-8")
cv_es = (ROOT / "cv.html").read_text(encoding="utf-8")
cv_en = (ROOT / "cv-en.html").read_text(encoding="utf-8")
css = (ROOT / "style.css").read_text(encoding="utf-8")
js = (ROOT / "script.js").read_text(encoding="utf-8")

for employer in ("Farmafe", "COTO", "Hotel Devoto", "Ravio", "Concorsistemas", "COPAGRAN"):
    if employer not in index_html or employer not in cv_es or employer not in cv_en:
        fail(f"verified work history is missing from portfolio or CV: {employer}")

for token in ("#F3F7F9", "#E2EDF1", "#142B3A", "#087E8B", "#9CBCC1", "#C77D68", "#FF4D00"):
    if token.lower() not in css.lower():
        fail(f"visual palette token is missing: {token}")

if 'href="cv.html"' not in index_html or "cv-en.html" not in js:
    fail("English CV link is missing from portfolio or language switcher")
if 'data-es="' not in index_html or 'data-en="' not in index_html:
    fail("portfolio language attributes are missing")
if "prefers-reduced-motion" not in css:
    fail("reduced-motion support is missing")
if "window.requestAnimationFrame" not in js:
    fail("scroll progress should use requestAnimationFrame")

for filename, html in (("cv.html", cv_es), ("cv-en.html", cv_en)):
    if "<html lang=" not in html or "window.print()" not in html:
        fail(f"{filename} is missing language metadata or print support")

print("PASS: required portfolio and bilingual CV files exist")
print("PASS: HTML documents have no duplicate IDs or broken in-page anchors")
print("PASS: all referenced local assets exist")
print("PASS: external target=_blank links include noopener protection")
print("PASS: exactly six selected projects are presented")
print("PASS: Cloudflare configuration targets the portfolio-agustin Worker")
print("PASS: all six verified employers appear in the portfolio and both CVs")
print("PASS: editorial premium palette is defined")
print("PASS: Spanish and English CV links and language attributes exist")
print("PASS: reduced-motion and scroll-progress behavior are present")
print("PASS: both CVs include language metadata and print support")
