from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = ("index.html", "style.css", "script.js", "cv.html", "cv-en.html")

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.anchors, self.local_assets = [], [], []
        self.unsafe_blank_links = []
        self.images_without_alt = 0
        self.h1_count = 0
        self.project_cards = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if "id" in attrs:
            self.ids.append(attrs["id"])
        href = attrs.get("href", "")
        if href.startswith("#") and len(href) > 1:
            self.anchors.append(href[1:])
        if tag == "article" and "project-card" in attrs.get("class", "").split():
            self.project_cards += 1
        if tag == "img" and not attrs.get("alt", "").strip():
            self.images_without_alt += 1
        if tag == "a" and attrs.get("target") == "_blank":
            if "noopener" not in attrs.get("rel", "").lower().split():
                self.unsafe_blank_links.append(href)
        for key in ("href", "src"):
            value = attrs.get(key, "")
            if value and not value.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
                local = value.split("?", 1)[0].split("#", 1)[0]
                if local:
                    self.local_assets.append(local)

def fail(message):
    print("FAIL: " + message)
    sys.exit(1)

for name in FILES:
    source = ROOT / name
    deployed = ROOT / "dist" / name
    if not source.is_file() or not deployed.is_file():
        fail("required source or dist file missing: " + name)
    if source.read_bytes() != deployed.read_bytes():
        fail("dist/" + name + " is not synchronized with " + name)

documents = {}
for name in ("index.html", "cv.html", "cv-en.html"):
    html = (ROOT / name).read_text(encoding="utf-8")
    parser = SiteParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:
        fail("HTML parse error in " + name + ": " + str(exc))
    if parser.h1_count != 1:
        fail(name + " must contain exactly one h1")
    if not parser.lang:
        fail(name + " is missing html lang metadata")
    if parser.images_without_alt:
        fail(name + " contains images without descriptive alt text")
    if parser.unsafe_blank_links:
        fail(name + " has target=_blank links without noopener")
    if len(parser.ids) != len(set(parser.ids)):
        fail(name + " contains duplicate IDs")
    if set(parser.anchors) - set(parser.ids):
        fail(name + " contains broken in-page anchors")
    for asset in parser.local_assets:
        if not (ROOT / asset).is_file():
            fail(name + " references missing local asset: " + asset)
    documents[name] = html

index = documents["index.html"]
cv_es = documents["cv.html"]
cv_en = documents["cv-en.html"]
css = (ROOT / "style.css").read_text(encoding="utf-8")
js = (ROOT / "script.js").read_text(encoding="utf-8")
wrangler = (ROOT / "wrangler.jsonc").read_text(encoding="utf-8")

if '"name": "portfolio"' not in wrangler or '"workers_dev": true' not in wrangler or '"directory": "./dist"' not in wrangler:
    fail("Wrangler must deploy dist/ as the portfolio Worker on workers.dev")

for name, html in documents.items():
    for forbidden in ("Ripio Once", "Administrativo de Auditoría", "Administrative Audit Assistant", "Abr 2025", "Abr 2026", "Oct 2023"):
        if forbidden.casefold() in html.casefold():
            fail(name + " contains outdated text: " + forbidden)
    if re.search(r"IBM[^<]{0,120}(en curso|in progress)", html, re.I):
        fail(name + " marks an IBM course as in progress")

experience_ranges = (
    (index.split('<section class="section experience-section"', 1)[1].split('<section class="section education-section"', 1)[0], "portfolio"),
    (cv_es.split('<section class="section"><h2>Experiencia laboral</h2>', 1)[1].split("</section>", 1)[0], "Spanish CV"),
    (cv_en.split('<section class="section"><h2>Professional experience</h2>', 1)[1].split("</section>", 1)[0], "English CV"),
)
for section, label in experience_ranges:
    for date in ("Sep 2024 — Feb 2026",):
        if date not in section:
            fail(label + " is missing Farmafe's verified dates")
    if "Feb 2026" not in section or section.count("Feb 2026") != 1:
        fail(label + " has Feb 2026 outside Farmafe or an incorrect count")
for date in ("Abr 2022 — Nov 2023",):
    if date not in index or date not in cv_es:
        fail("Spanish employment dates are inconsistent")
if "Apr 2022 — Nov 2023" not in cv_en:
    fail("English COTO dates are inconsistent")

for employer in ("Farmafe", "COTO", "Hotel Devoto", "Ravio", "Concorsistemas", "COPAGRAN"):
    if any(employer not in html for html in documents.values()):
        fail("verified employer missing across portfolio and CVs: " + employer)

project_area = index.split('<div class="project-grid">', 1)[1].split("</section>", 1)[0]
names = ("Farmacia BI", "API Testing Framework", "Playwright UI Testing", "PriceWatch", "Automatic-OC", "n8n Automation Portfolio")
positions = [project_area.find(name) for name in names]
if any(p < 0 for p in positions) or positions != sorted(positions):
    fail("six projects are missing or not in the requested order")
if len(re.findall(r'class="project-card ', project_area)) != 6:
    fail("portfolio must show exactly six project cards")
for token in ("01", "02", "03", "04", "05", "06", "En desarrollo", "In progress", "Capturas próximamente", "Screenshots coming soon", "Pendiente de validar", "Validation pending", "01 / 06"):
    if token not in index:
        fail("project counter or state missing: " + token)
for html, required in ((cv_es, ("Estado: En desarrollo", "Capturas próximamente", "Estado: Pendiente de validar")), (cv_en, ("Status: In progress", "Screenshots coming soon", "Status: Validation pending"))):
    for phrase in required:
        if phrase not in html:
            fail("CV project status missing: " + phrase)

for html in documents.values():
    if "IBM — Project Management Fundamentals" not in html:
        fail("IBM Project Management Fundamentals is missing")
if "Credly verification URL" not in index or "Credly verification URL" not in cv_es or "Credly verification URL" not in cv_en:
    fail("optional Credly verification insertion point is missing")

for employer in ("Farmafe", "COTO", "Hotel Devoto", "Ravio", "Concorsistemas", "COPAGRAN"):
    if employer not in index or employer not in cv_es or employer not in cv_en:
        fail("experience record mismatch: " + employer)

for color in ("#F3F7F9", "#E2EDF1", "#142B3A", "#087783", "#52777F", "#9C5948", "#FF4D00"):
    if color.lower() not in css.lower():
        fail("visual palette token missing: " + color)
if "prefers-reduced-motion" not in css or ":focus-visible" not in css or "class=\"skip-link\"" not in index:
    fail("keyboard focus, skip navigation or reduced-motion support missing")
if "min-width:360px" not in css or "max-width:430px" not in css:
    fail("explicit 360–430 px mobile rules missing")
if "og:title" not in index or "og:description" not in js or "twitter:description" not in js:
    fail("bilingual social metadata support missing")
if "data-alt-es" not in index or "data-alt-en" not in index or "data-aria-label-es" not in index or "data-aria-label-en" not in index:
    fail("bilingual accessible image or aria labels are missing")
if 'href="cv.html"' not in index or "cv-en.html" not in js or 'data-es="' not in index or 'data-en="' not in index:
    fail("bilingual navigation or language content missing")
if index.count('class="contact-profile-card') != 1:
    fail("contact profile blocks were not consolidated")
contact_area = index.split('class="contact-profiles"', 1)[1].split('class="contact-actions"', 1)[0]
for link in ("https://www.linkedin.com/in/agustincabral13/", "https://github.com/agustiininicabral"):
    if link not in contact_area:
        fail("contact profile missing " + link)
for token in ('href="mailto:agustinkbral2013@gmail.com"', 'href="tel:+541178217296"', 'https://wa.me/541178217296', 'data-copy-email='):
    if token not in index:
        fail("contact action missing: " + token)
if ".hero-image{" not in css or "photo-credit" not in index:
    fail("Fuji photo credit should be retained only while the image is used")
if "window.requestAnimationFrame" not in js:
    fail("scroll progress animation is missing")

for name, expected_lang in (("cv.html", "es-AR"), ("cv-en.html", "en")):
    html = documents[name]
    if '<html lang="' + expected_lang + '">' not in html or "window.print()" not in html or "og:locale" not in html:
        fail(name + " is missing language, social or print metadata")

print("PASS: source and dist files are synchronized")
print("PASS: HTML structure, one h1, IDs, anchors, images and external links")
print("PASS: all six employment records and dates are aligned")
print("PASS: obsolete employers, titles, dates and IBM in-progress states are rejected")
print("PASS: six projects are ordered and their statuses are explicit")
print("PASS: bilingual CV metadata and optional Credly slots are present")
print("PASS: accessible focus, skip navigation, reduced motion and mobile refinements")
print("PASS: contact methods and single LinkedIn/GitHub profile card")
print("PASS: Fuji credit matches the actual hero image usage")
print("PASS: Cloudflare deploy config targets portfolio.agustiincabral.workers.dev")
