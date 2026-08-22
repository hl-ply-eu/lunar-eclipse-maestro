#!/usr/bin/env python3
"""Build a consolidated printable HTML/PDF from the local LEM help mirror."""

from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

ROOT = Path(__file__).resolve().parent.parent
HELP_ROOT = (
    ROOT
    / "mirror"
    / "xjubier.free.fr"
    / "site_pages"
    / "lunar_eclipses"
    / "Lunar_Eclipse_Maestro_Help"
)
OUTPUT_DIR = ROOT / "output"
MIRROR_HREF_ROOT = "../mirror/xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help"

PRIORITY_PAGES = [
    "pgs2/btoc1.html",
    "pgs/c0sem.html",
    "pgs/c1sem.html",
    "pgs2/btoc4.html",
    "pgs2/btoc5.html",
    "pgs2/btoc6.html",
    "pgs2/btoc11.html",
    "pgs2/btoc8.html",
    "pgs2/btoc9.html",
    "pgs2/kbshortcuts.html",
    "pgs2/tips.html",
    "pgs2/btoc2.html",
    "pgs2/btoc3.html",
    "pgs2/btoc7.html",
    "pgs2/btoc10.html",
]

PRINT_CSS = """
@page { size: A4; margin: 18mm 15mm; }
body {
  font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.45;
  color: #111;
}
h1 { font-size: 16pt; margin-top: 0; page-break-after: avoid; }
h2 { font-size: 13pt; margin-top: 1.2em; page-break-after: avoid; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
h3 { font-size: 11pt; page-break-after: avoid; }
section { page-break-before: always; }
section:first-of-type { page-break-before: auto; }
img { max-width: 100%; height: auto; }
table { border-collapse: collapse; width: 100%; font-size: 8pt; }
td, th { border: 1px solid #ccc; padding: 3px 5px; vertical-align: top; }
a { color: #004488; text-decoration: none; }
.toc { page-break-after: always; }
.toc li { margin: 0.2em 0; }
.meta { color: #555; font-size: 9pt; margin-bottom: 1.5em; }
"""


def discover_pgs_order() -> list[str]:
    btoc1 = HELP_ROOT / "pgs2" / "btoc1.html"
    if not btoc1.exists():
        return []
    soup = BeautifulSoup(btoc1.read_text(encoding="iso-8859-1", errors="replace"), "lxml")
    order: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("../pgs/") and href.endswith(".html"):
            rel = "pgs/" + href.split("../pgs/", 1)[1]
            if rel not in order:
                order.append(rel)
    return order


def build_page_list() -> list[Path]:
    if not HELP_ROOT.exists():
        raise FileNotFoundError(f"Help mirror not found: {HELP_ROOT}")

    seen: set[str] = set()
    pages: list[Path] = []

    def add(rel: str) -> None:
        if rel in seen:
            return
        path = HELP_ROOT / rel
        if path.exists():
            seen.add(rel)
            pages.append(path)

    for rel in PRIORITY_PAGES:
        add(rel)

    for rel in discover_pgs_order():
        add(rel)

    for path in sorted(HELP_ROOT.rglob("*.html")):
        rel = path.relative_to(HELP_ROOT).as_posix()
        add(rel)

    return pages


def extract_section(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="iso-8859-1", errors="replace")
    soup = BeautifulSoup(raw, "lxml")

    title = soup.title.get_text(strip=True) if soup.title else path.name
    mainbox = soup.find(id="mainbox")
    if mainbox is None:
        body = soup.body or soup
        content = body.decode_contents()
    else:
        content = mainbox.decode_contents()

    content = re.sub(
        r'href="\.\./([^"]+)"',
        rf'href="{MIRROR_HREF_ROOT}/\1"',
        content,
    )
    content = re.sub(r'src="\.\./([^"]+)"', rf'src="{HELP_ROOT.as_posix()}/\1"', content)

    return title, content


def build_html(pages: list[Path]) -> str:
    sections: list[str] = []
    toc_items: list[str] = []

    for i, path in enumerate(pages, 1):
        title, content = extract_section(path)
        anchor = f"section-{i}"
        toc_items.append(f'<li><a href="#{anchor}">{title}</a></li>')
        sections.append(
            f'<section id="{anchor}">'
            f"<h2>{title}</h2>"
            f"{content}"
            f"</section>"
        )

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Aide Lunar Eclipse Maestro — édition consolidée</title>
  <style>{PRINT_CSS}</style>
</head>
<body>
  <h1>Aide Lunar Eclipse Maestro</h1>
  <p class="meta">
    Édition consolidée pour impression — source : Xavier Jubier —
    <a href="http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html">documentation en ligne</a>
  </p>
  <div class="toc">
    <h2>Sommaire</h2>
    <ol>{''.join(toc_items)}</ol>
  </div>
  {''.join(sections)}
</body>
</html>
"""


def write_pdf(html_path: Path, pdf_path: Path) -> None:
    from weasyprint import HTML

    HTML(filename=str(html_path), base_url=str(HELP_ROOT)).write_pdf(str(pdf_path))


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pages = build_page_list()
    html_out = OUTPUT_DIR / "lem-help-print.html"
    pdf_out = OUTPUT_DIR / "lem-help-complet.pdf"

    html = build_html(pages)
    html_out.write_text(html, encoding="utf-8")
    print(f"Wrote {html_out} ({len(pages)} sections)")

    try:
        write_pdf(html_out, pdf_out)
        print(f"Wrote {pdf_out}")
    except Exception as exc:
        print(f"PDF generation failed: {exc}", file=sys.stderr)
        print("Open lem-help-print.html in a browser and use Print → Save as PDF.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
