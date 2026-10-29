"""Layout checks for the wrapped figures on the docs site's example pages.

Render the site first (`quarto render docs`), then run from the repository
root:

    python3 tests/docs_layout.py

By default it reads the PDF through LaTeX, the PDF through Typst, and a
LibreOffice PDF of the Word file of each page in CASES outside HTML_ONLY,
and exits with status 1 if a figure fails. The options below skip Word or
run the HTML check instead. For each wrapped figure, the figure's page must have:

- a paragraph of at least two lines before the figure (before a code block
  there, for a code cell), each line but the last crossing the figure's
  horizontal span, and
- a paragraph after it with a line beside the figure and a later line below
  the figure's bottom that crosses its span.

A line crosses the span of a right-side figure when its right edge is right
of the figure's left edge, and of a left-side figure when its left edge is
left of the figure's right edge. The figure's bottom is the lower of its
image and its last caption line.

The PDF checks find paragraphs by line spacing, not by their words, since
pdftohtml reads a LibreOffice PDF's text with letters lost and added. A
line in the PDF's most common font, counted by characters, is body text. A line with none of it
is a heading (larger) or code (not larger), and either ends a paragraph.

`python3 tests/docs_layout.py --html` runs the HTML check instead. It
serves the site with tests/layout.js at `/layout.js`, opens each page in
CASES in headless Chromium at 1280x900, runs `straddle()`, and exits with
status 1 if a figure fails or a page is missing. It needs Playwright for
Python and its Chromium (`pip install playwright`, then
`python3 -m playwright install chromium`). `--js` prints the `straddle()`
calls to run by hand in a browser console instead.

Options: `--site DIR` reads a rendered site in DIR in place of docs/_site/.
`--no-word` skips the Word PDFs, so the run needs no `soffice`. `--debug`
prints each figure box and the page's blocks. Any other argument stops the
run with a message.
"""

import functools
import http.server
import json
import statistics
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


FLAGS = {"--js", "--html", "--no-word", "--debug"}


def site_option():
    """The folder after `--site`, or None. Stops on an unknown argument."""
    args, site, i = sys.argv[1:], None, 0
    while i < len(args):
        if args[i] == "--site":
            if i + 1 == len(args) or args[i + 1].startswith("--"):
                sys.exit("--site needs a folder")
            site, i = args[i + 1], i + 2
        elif args[i] in FLAGS:
            i += 1
        else:
            sys.exit(f"unknown argument: {args[i]}")
    return site


SITE = Path(site_option() or ROOT / "docs" / "_site").resolve()
WORD = "--no-word" not in sys.argv

# Per page, one entry per wrapped figure in page order. The PDF checks read
# `side` only. For the HTML check, `above` and `straddle` name words of the
# paragraph before the figure and of the paragraph that runs beside and
# below it.
CASES = {
    "index": [
        {"side": "right", "above": ["box shows"], "straddle": ["One markdown syntax"]},
    ],
    "examples/image-figure": [
        {"side": "right", "above": ["Participants rated"], "straddle": ["puts the figure on the right"]},
    ],
    "examples/div-figure": [
        {"side": "left", "above": ["Each participant practiced"], "straddle": ["puts the figure on the left"]},
    ],
    "examples/uncaptioned-image": [
        {"side": "right", "above": ["A badge, a logo"], "straddle": ["An image with no caption wraps"]},
    ],
    "examples/code-cell": [
        {"side": "right", "above": ["The data are"], "straddle": ["Faster cars"]},
    ],
    "examples/width-gap": [
        {"side": "left", "above": ["has a fixed width"], "straddle": ["The gap between"]},
    ],
    "examples/defaults": [
        {"side": "right", "above": ["key in this page"], "straddle": ["The defaults save"]},
    ],
    "examples/both-sides": [
        {"side": "right", "above": ["This page has two"], "straddle": ["The figure wraps"]},
        {"side": "left", "above": ["The second figure"], "straddle": ["Two wrapped figures"]},
    ],
}

# Pages with no PDF or Word format, checked in HTML only.
HTML_ONLY = {"index"}

TOL = 2  # px, in pdftohtml's 1.5 px per pt


def pdf_paths(page, tmp):
    """The PDFs of a page: LaTeX, Typst, and Word through LibreOffice."""
    base = SITE / page
    paths = {
        "latex": base.with_suffix(".pdf"),
        "typst": base.parent / f"{base.name}-typst.pdf",
    }
    if WORD:
        docx = base.with_suffix(".docx")
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(docx)],
            check=True, capture_output=True,
        )
        paths["word"] = Path(tmp) / f"{base.name}.pdf"
    return paths


def read_pdf(pdf, tmp):
    """Text elements and image boxes, each with its page, and font sizes."""
    out = Path(tmp) / f"{pdf.stem}-{abs(hash(str(pdf)))}"
    subprocess.run(["pdftohtml", "-xml", "-q", str(pdf), str(out)], check=True, capture_output=True)
    root = ET.parse(f"{out}.xml").getroot()
    sizes = {f.get("id"): int(f.get("size")) for f in root.iter("fontspec")}
    texts, images = [], []
    for page in root.iter("page"):
        n = int(page.get("number"))
        for el in page:
            if el.tag not in ("image", "text"):
                continue
            box = {k: int(float(el.get(k))) for k in ("top", "left", "width", "height")}
            box.update(page=n, bottom=box["top"] + box["height"], right=box["left"] + box["width"])
            if el.tag == "image":
                images.append(box)
            elif "".join(el.itertext()).strip():
                box["font"] = el.get("font")
                box["chars"] = len("".join(el.itertext()))
                texts.append(box)
    images.sort(key=lambda b: (b["page"], b["top"]))
    return texts, images, sizes


def lines(elements):
    """Merge text elements into lines by page and the element's middle.

    Inline code sits a few px lower than the text around it in Typst, so an
    element joins a line when its middle is inside the line's box.
    """
    out = []
    for el in sorted(elements, key=lambda e: (e["page"], e["top"], -e["height"])):
        middle = (el["top"] + el["bottom"]) / 2
        for line in out:
            if line["page"] == el["page"] and line["top"] <= middle <= line["bottom"]:
                line["left"] = min(line["left"], el["left"])
                line["right"] = max(line["right"], el["right"])
                line["bottom"] = max(line["bottom"], el["bottom"])
                line["fonts"].add(el["font"])
                break
        else:
            line = {k: el[k] for k in ("page", "top", "bottom", "left", "right")}
            line["fonts"] = {el["font"]}
            out.append(line)
    return sorted(out, key=lambda l: (l["page"], l["top"]))


def blocks(page_lines, body, sizes):
    """Split a page's lines into paragraphs, headings, and code by spacing."""
    tops = [l["top"] for l in page_lines]
    pitch = statistics.median(b - a for a, b in zip(tops, tops[1:]) if b > a)
    out = []
    for line in page_lines:
        if body in line["fonts"]:
            kind = "para"
        elif max(sizes[f] for f in line["fonts"]) > sizes[body]:
            kind = "heading"
        else:
            kind = "code"
        last = out[-1] if out else None
        if last and last["kind"] == kind and line["top"] - last["lines"][-1]["top"] <= 1.25 * pitch:
            last["lines"].append(line)
        else:
            out.append({"kind": kind, "lines": [line]})
    return out, pitch


def crosses(line, fig):
    if fig["side"] == "right":
        return line["right"] > fig["left"] + TOL
    return line["left"] < fig["right"] - TOL


def check(texts, image, side, body, sizes):
    """The problems found for one figure."""
    fig = dict(image, side=side)
    on_page = [t for t in texts if t["page"] == fig["page"]]
    # Caption lines sit inside the image's span, just below it. A text box
    # can reach a few px into the next line's box.
    for t in sorted(on_page, key=lambda t: t["top"]):
        if (t["left"] >= image["left"] - 30 and t["right"] <= image["right"] + 30
                and -6 <= t["top"] - fig["bottom"] <= 40):
            fig["bottom"] = t["bottom"]
            fig["left"] = min(fig["left"], t["left"])
            fig["right"] = max(fig["right"], t["right"])
    outside = [t for t in on_page if not (
        t["left"] >= fig["left"] - TOL and t["right"] <= fig["right"] + TOL
        and t["top"] >= fig["top"] - TOL and t["bottom"] <= fig["bottom"] + TOL)]
    page_blocks, pitch = blocks(lines(outside), body, sizes)
    if "--debug" in sys.argv:
        print(" figure", {k: fig[k] for k in ("page", "top", "bottom", "left", "right")}, "pitch", pitch)
        for b in page_blocks:
            print("  ", b["kind"], [(l["top"], l["left"], l["right"]) for l in b["lines"]])
    # wrapfig narrows the first line beside a figure up to about 1.3 line
    # pitches above the image's top, so "beside" starts 1.5 pitches higher.
    # The last line of the paragraph above starts higher than that, since a
    # paragraph gap comes before the wrap.
    def beside(l):
        return l["top"] > fig["top"] - 1.5 * pitch and l["top"] < fig["bottom"] and not crosses(l, fig)
    first = next((i for i, b in enumerate(page_blocks)
                  if b["kind"] == "para" and any(beside(l) for l in b["lines"])), None)
    if first is None:
        return ["no paragraph beside the figure on its page"]
    problems = []
    i = first - 1
    while i >= 0 and page_blocks[i]["kind"] == "code":
        i -= 1
    if i < 0 or page_blocks[i]["kind"] != "para":
        problems.append("no paragraph above the figure on its page")
    else:
        above = page_blocks[i]["lines"]
        if len(above) < 2:
            problems.append(f"paragraph above has {len(above)} line")
        elif not all(crosses(l, fig) for l in above[:-1]):
            problems.append("a line above does not cross the figure")
    straddles = False
    for b in page_blocks[first:]:
        if b["kind"] != "para":
            break
        side_lines = [l for l in b["lines"] if beside(l)]
        if side_lines and any(l["top"] > side_lines[0]["top"] and l["top"] >= fig["bottom"] - TOL
                              and crosses(l, fig) for l in b["lines"]):
            straddles = True
    if not straddles:
        problems.append("no paragraph runs from beside the figure to below it")
    return problems


class SiteHandler(http.server.SimpleHTTPRequestHandler):
    """Serves the site, and tests/layout.js at `/layout.js`."""

    def translate_path(self, path):
        if path.split("?")[0] == "/layout.js":
            return str(ROOT / "tests" / "layout.js")
        return super().translate_path(path)

    def log_message(self, *args):
        pass


def html_main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("--html needs Playwright for Python: pip install playwright, "
                 "then python3 -m playwright install chromium")
    handler = functools.partial(SiteHandler, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    failed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        tab = browser.new_page(viewport={"width": 1280, "height": 900})
        for page, cases in CASES.items():
            if not (SITE / f"{page}.html").is_file():
                print(f"{page} html: FAIL: page missing")
                failed += 1
                continue
            try:
                tab.goto(f"{base}/{page}.html", wait_until="load")
                results = tab.evaluate(
                    "async (cases) => { await document.fonts.ready;"
                    " return (await import('/layout.js')).straddle(cases); }", cases)
            except Exception as err:
                print(f"{page} html: FAIL: {str(err).splitlines()[0]}")
                failed += 1
                continue
            for n, r in enumerate(results):
                status = "ok" if r["ok"] else "FAIL: " + "; ".join(r["problems"])
                failed += not r["ok"]
                print(f"{page} html figure {n + 1}: {status}")
        browser.close()
    server.shutdown()
    return 1 if failed else 0


def main():
    if "--js" in sys.argv:
        for page, cases in CASES.items():
            print(f"{page}.html: m.straddle({json.dumps(cases)})")
        return 0
    if "--html" in sys.argv:
        return html_main()
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for page, cases in CASES.items():
            if page in HTML_ONLY:
                continue
            for fmt, pdf in pdf_paths(page, tmp).items():
                texts, images, sizes = read_pdf(pdf, tmp)
                weight = Counter()
                for t in texts:
                    weight[t["font"]] += t["chars"]
                body = weight.most_common(1)[0][0]
                # Figure n is image n, so the page must hold no other image.
                for n, case in enumerate(cases):
                    if len(images) != len(cases):
                        problems = [f"{len(images)} images for {len(cases)} figures"]
                    else:
                        problems = check(texts, images[n], case["side"], body, sizes)
                    status = "ok" if not problems else "FAIL: " + "; ".join(problems)
                    failed += bool(problems)
                    print(f"{page} {fmt} figure {n + 1}: {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
