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
image and its last caption line. The caption is the first line of text
under the image that overlaps the image's span, if it opens with "Figure"
or is not in the body font, and the lines that follow it inside its span
with text in its font (`caption()`).

The PDF checks find paragraphs by line spacing, not by their words, since
pdftohtml reads a LibreOffice PDF's text with letters lost and added. A
line in the PDF's most common font, counted by characters, is body text. A line with none of it
is a heading (larger) or code (not larger), and either ends a paragraph. A
paragraph also ends where the gap from one line's top to the next passes
the page's line pitch by more than 2 px, and in LaTeX and Typst before a
line indented from its neighbors, as a paragraph's first line is
(`blocks()`). A lost letter can move a line of a LibreOffice PDF right, so
the Word check does not read indents.

`python3 tests/docs_layout.py --html` runs the HTML check instead. It
serves the site with tests/layout.js at `/layout.js`, opens each page in
CASES in headless Chromium at 1280x900, runs `straddle()`, and exits with
status 1 if a figure fails or a page is missing. In HTML, the paragraph
before the figure must also be the last visible block before it, other
than the blocks of the figure's own code cell. It needs Playwright for
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
                box["text"] = "".join(el.itertext())
                box["chars"] = len(box["text"])
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


def blocks(page_lines, body, sizes, indents):
    """Split a page's lines into paragraphs, headings, and code by spacing.

    A block ends where the next line's top is more than the line pitch plus
    TOL below the last line's top. With `--debug` on the docs pages on
    2026-10-29, lines of one paragraph sat within 1 px of the pitch, and
    paragraphs 8 px or more past it. With `indents`, a paragraph also ends
    before a line that starts right of the line before it or the line after
    it by an indent: more than a quarter of the pitch, past a letter set
    slightly into the margin (124 against 125 px on image-figure's LaTeX
    PDF), and no more than two pitches, short of the step between a line
    beside a left-side figure and a line below it.
    """
    tops = [l["top"] for l in page_lines]
    pitch = statistics.median(b - a for a, b in zip(tops, tops[1:]) if b > a)

    def indented(line, other):
        return other is not None and pitch / 4 < line["left"] - other["left"] <= 2 * pitch

    out = []
    for n, line in enumerate(page_lines):
        if body in line["fonts"]:
            kind = "para"
        elif max(sizes[f] for f in line["fonts"]) > sizes[body]:
            kind = "heading"
        else:
            kind = "code"
        last = out[-1] if out else None
        prev = last["lines"][-1] if last else None
        nxt = page_lines[n + 1] if n + 1 < len(page_lines) else None
        if (last and last["kind"] == kind and line["top"] - prev["top"] <= pitch + TOL
                and not (indents and kind == "para" and (indented(line, prev) or indented(line, nxt)))):
            last["lines"].append(line)
        else:
            out.append({"kind": kind, "lines": [line]})
    return out, pitch


def crosses(line, fig):
    if fig["side"] == "right":
        return line["right"] > fig["left"] + TOL
    return line["left"] < fig["right"] - TOL


def caption(on_page, image, body):
    """The text elements of the image's caption, top to bottom.

    Text beside a figure stops short of the image's span, so the text under
    the image that overlaps its span, grouped into lines, starts with the
    caption if there is one. The first line is caption if its first element
    opens with "Figure" or is not in the body font. Each later line is
    caption while it starts no more than 1.5 heights of the line before
    below that line's top, lies inside the first line's span, and holds an
    element in the first element's font.
    """
    # A text box can reach a few px into the box of the line above it.
    under = sorted((t for t in on_page if t["top"] >= image["bottom"] - 6
                    and t["left"] < image["right"] and t["right"] > image["left"]),
                   key=lambda t: (t["top"], t["left"]))
    rows = []
    for t in under:
        middle = (t["top"] + t["bottom"]) / 2
        if rows and rows[-1][0]["top"] <= middle <= rows[-1][0]["bottom"]:
            rows[-1].append(t)
        else:
            rows.append([t])
    if not rows:
        return []
    first = min(rows[0], key=lambda t: t["left"])
    if not (first["text"].startswith("Figure") or first["font"] != body):
        return []
    left = min(t["left"] for t in rows[0])
    right = max(t["right"] for t in rows[0])
    out = list(rows[0])
    for last, row in zip(rows, rows[1:]):
        if (row[0]["top"] - last[0]["top"] > 1.5 * last[0]["height"]
                or min(t["left"] for t in row) < left - TOL
                or max(t["right"] for t in row) > right + TOL
                or not any(t["font"] == first["font"] for t in row)):
            break
        out += row
    return out


def check(texts, image, side, body, sizes, indents):
    """The problems found for one figure."""
    fig = dict(image, side=side)
    on_page = [t for t in texts if t["page"] == fig["page"]]
    for t in caption(on_page, image, body):
        fig["bottom"] = max(fig["bottom"], t["bottom"])
        fig["left"] = min(fig["left"], t["left"])
        fig["right"] = max(fig["right"], t["right"])
    outside = [t for t in on_page if not (
        t["left"] >= fig["left"] - TOL and t["right"] <= fig["right"] + TOL
        and t["top"] >= fig["top"] - TOL and t["bottom"] <= fig["bottom"] + TOL)]
    page_blocks, pitch = blocks(lines(outside), body, sizes, indents)
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
                        # LibreOffice PDFs lose letters at line starts, which
                        # moves a line right as an indent would.
                        problems = check(texts, images[n], case["side"], body, sizes, fmt != "word")
                    status = "ok" if not problems else "FAIL: " + "; ".join(problems)
                    failed += bool(problems)
                    print(f"{page} {fmt} figure {n + 1}: {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
