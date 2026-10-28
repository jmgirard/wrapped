r"""Render the wrapped fixtures and compare the output with committed snapshots.

Run from the repository root:

    python3 tests/verify.py            # render and compare
    python3 tests/verify.py --update   # render and rewrite the snapshots

Needs Quarto, R with knitr, TinyTeX, and poppler. Each render must exit with status
0. A snapshot under tests/_snapshots/ records the parts of a render that
show what the filter decided. For every format it holds the extension's
warnings. For HTML it also holds the breakpoint value, the wrap class and
style of every figure or table div and wrapped box, the wrap class, style, and width
of every image, and the members of every .wrap-group. Style declarations
are sorted, so their order does not count. For PDF it also holds the kind,
label, and options of each figure environment and the options of its
\includegraphics, with each \wrappedstop in its place, and for Typst the label of each #figure( call and
whether its image keeps a width. For Typst it also holds each
wrap-content call's options, the figure label or image in its box and its
alt text, the kind of each block beside the box ("p" for a paragraph), the
number of citations there, and the number of calls it could not read. For Word
it also holds each image's width from word/document.xml, and each frame: its
side, width, gap, and anchor, the figure bookmark open before it, whether
each image fills the frame width and its alt text, whether each caption has
the ImageCaption style, and the kind of each block after the frame up to the
paragraph with the clearing break, with the link anchors and author-year
citations in those paragraphs. It also counts framed paragraphs that are
in no frame. The script first writes the reference docs of the docx
fixtures with tests/reference_narrow.py. A revealjs
snapshot holds what an HTML snapshot holds. A fixture that is a folder is a
book project: its snapshot holds the HTML parts of each page under _book/,
and the href of each cross-reference link. For a fixture in MARGIN_IDS, the
script also renders a copy with no filters and records whether the nearest
column-margin div around each named figure has the same classes in both
renders. The script exits with status 1 on a failed render, a snapshot
difference, or a failed layout case or log check.

Some fixtures exist only for the browser checks in tests/layout.js, which
measure layout. Those fixtures are rendered here, so their HTML is current,
and they have no snapshot.

For a fixture in LAYOUT, the script also reads the PDF through LaTeX right
after its render, before the Typst render writes the same path, and checks
where each case's text starts beside and below its wrapped figure. It reads
the boxes of text lines and images with poppler's pdftohtml (brew install
poppler, or apt install poppler-utils). It prints one line for each case it measured.
For a fixture in TYPST_LAYOUT, it reads the PDF through Typst the same way
after its Typst render, and checks each figure's image width and the first
line of its paragraph beside it.

For a fixture in LOGS, rendered with latex-clean: false so its LaTeX log
stays, the script also reads the warnings that wrapped.tex writes to that
log: the count of two-column warnings, and the line of each multicols
warning against the lines of the wrappedfigure environments inside
multicols in the kept .tex.
"""

import difflib
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import reference_narrow

TESTS = Path(__file__).resolve().parent
SNAPSHOTS = TESTS / "_snapshots"

# (fixture, format, compare with a snapshot)
RENDERS = [
    ("fixture", "html", True),
    ("fixture", "pdf", True),
    ("fixture", "typst", True),
    ("fixture", "docx", True),
    ("defaults", "html", True),
    ("defaults", "pdf", True),
    ("defaults", "typst", True),
    ("defaults", "docx", True),
    ("docx-reference", "docx", True),
    ("docx-options", "docx", True),
    ("docx-columns", "docx", True),
    ("docx-gap", "docx", True),
    ("docx-gap-meta", "docx", True),
    ("docx-gap-meta-wide", "docx", True),
    ("docx-overflow", "docx", True),
    ("meta-breakpoint", "html", True),
    ("meta-string", "html", True),
    ("meta-calc-bad", "html", True),
    ("meta-calc-good", "html", True),
    ("meta-calc-var", "html", True),
    ("meta-calc-zero", "html", True),
    ("meta-calc-gap", "html", True),
    ("css-functions", "html", True),
    ("contexts", "html", True),
    ("contexts", "pdf", True),
    ("contexts", "typst", True),
    ("contexts", "docx", True),
    ("table-cell", "html", True),
    ("table-cell", "typst", True),
    ("table-cell", "docx", True),
    ("table-cell-image", "pdf", True),
    ("cap-margin", "html", True),
    ("cap-margin", "pdf", True),
    ("cap-margin", "typst", True),
    ("cap-margin", "docx", True),
    ("cap-margin-meta", "html", True),
    ("cap-margin-meta-fig", "html", True),
    ("page-wide", "html", True),
    ("page-wide", "pdf", True),
    ("page-wide", "typst", True),
    ("page-wide", "docx", True),
    ("page-wide-meta", "html", True),
    ("page-wide-meta", "pdf", True),
    ("page-wide-meta", "typst", True),
    ("page-wide-meta", "docx", True),
    ("margin-meta", "html", True),
    ("margin-meta", "pdf", True),
    ("margin-meta", "typst", True),
    ("margin-meta", "docx", True),
    ("column-meta", "html", True),
    ("column-meta", "pdf", True),
    ("column-order", "pdf", True),
    ("column-order", "typst", True),
    ("column-order-page", "pdf", True),
    ("column-order-page", "typst", True),
    ("column-order-fig-margin", "pdf", True),
    ("column-order-fig-margin", "typst", True),
    ("column-order-margin", "pdf", True),
    ("column-order-margin", "typst", True),
    ("stop-rule", "pdf", True),
    ("stop-rule", "typst", True),
    ("stop-rule", "docx", True),
    ("stop-latex", "pdf", True),
    ("multicols", "pdf", True),
    ("twocolumn-class", "pdf", True),
    ("twocolumn-switch", "pdf", True),
    ("twocolumn", "pdf", True),
    ("twocolumn-list", "pdf", True),
    ("pdf-ua", "pdf", True),
    ("pdf-ua1", "pdf", True),
    ("tex-options", "pdf", True),
    ("typst-break", "typst", True),
    ("typst-ua", "typst", True),
    ("typst-rtl", "typst", True),
    ("typst-options", "typst", True),
    ("typst-wide", "typst", True),
    ("typst-wide-meta", "typst", True),
    ("typst-inset-meta", "typst", True),
    ("typst-gap", "typst", True),
    ("typst-gap-meta", "typst", True),
    ("typst-gap-percent", "typst", True),
    ("typst-gap-default", "typst", True),
    ("typst-overflow", "typst", True),
    ("typst-columns", "typst", True),
    ("zero-meta", "html", True),
    ("zero-meta", "pdf", True),
    ("zero-meta", "typst", True),
    ("zero-width", "html", True),
    ("zero-width", "pdf", True),
    ("zero-width", "typst", True),
    ("book", "html", True),
    ("revealjs", "revealjs", True),
    ("revealjs-margin-meta", "revealjs", True),
    ("revealjs-column-margin", "revealjs", True),
    ("margin", "html", False),
    ("stop-rule", "html", False),
    ("rtl", "html", False),
    ("readme", "html", False),
]

WARNING = re.compile(r"\(W\) (wrapped: .*)")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
WRAP_CLASSES = ("wrap-left", "wrap-right", "wrapped-image")
FLOAT_IDS = ("fig-", "tbl-")


def wrap_classes(classes):
    return " ".join(c for c in classes.split() if c in WRAP_CLASSES) or "-"


def style_text(style):
    """Sorts the declarations of a style attribute, so their order does not
    count."""
    if style is None:
        return "-"
    return "; ".join(sorted(d.strip() for d in style.split(";") if d.strip())) or "-"


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Decisions(HTMLParser):
    """Collects what the filter decides in a rendered HTML page."""

    def __init__(self):
        super().__init__()
        self.figures = []
        self.images = []
        self.groups = []
        self.in_group = False
        self.level = 0  # open elements below the current .wrap-group

    def describe(self, tag, attrs):
        classes = attrs.get("class") or ""
        if tag == "div" and attrs.get("id", "").startswith(FLOAT_IDS):
            return attrs["id"]
        if tag == "div" and "wrapped-image" in classes.split():
            return "wrapped-image"
        if tag == "div" and "cell" in classes.split():
            return "cell"
        return tag

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class") or ""
        if self.in_group:
            if self.level == 0:
                self.groups[-1].append(self.describe(tag, attrs))
            if tag not in VOID:
                self.level += 1
        elif tag == "div" and "wrap-group" in classes.split():
            self.groups.append([])
            self.in_group = True
            self.level = 0
        if tag == "img":
            # revealjs puts the image path in data-src.
            src = Path(attrs.get("src") or attrs.get("data-src", "")).name
            self.images.append(
                f"{src}: wrap={wrap_classes(classes)} style={style_text(attrs.get('style'))} width={attrs.get('width', '-')}"
            )
        if tag != "div":
            return
        if attrs.get("id", "").startswith(FLOAT_IDS) or "wrapped-image" in classes.split():
            name = attrs.get("id", "(box)")
            self.figures.append(f"{name}: {wrap_classes(classes)} style={style_text(attrs.get('style'))}")

    def handle_endtag(self, tag):
        if not self.in_group or tag in VOID:
            return
        if self.level == 0:
            self.in_group = False
        else:
            self.level -= 1

    def handle_comment(self, data):
        if self.in_group and self.level == 0:
            self.groups[-1].append("comment")


def html_summary(path):
    source = path.read_text(encoding="utf-8")
    parser = Decisions()
    parser.feed(source)
    # The value can hold functions, such as min(calc(30em + 1px), 600px), so
    # it runs to the ") {" that ends the query.
    breakpoint = re.search(r"@media \(max-width: ([^{}]*?)\)\s*\{[^{}]*wrap-", source)
    parts = ["# breakpoint", breakpoint.group(1) if breakpoint else "(none)"]
    parts += ["# figures"] + parser.figures
    parts += ["# images"] + parser.images
    parts += ["# groups"] + [", ".join(members) for members in parser.groups]
    return "\n".join(parts)


class MarginContainers(HTMLParser):
    """Finds the nearest enclosing div with the column-margin class of each
    element whose id is in `ids`."""

    def __init__(self, ids):
        super().__init__()
        self.ids = ids
        self.stack = []  # class lists of the open divs
        self.found = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") in self.ids:
            margins = [c for c in self.stack if "column-margin" in c.split()]
            self.found[attrs["id"]] = margins[-1] if margins else "(none)"
        if tag == "div":
            self.stack.append(attrs.get("class") or "")

    def handle_endtag(self, tag):
        if tag == "div" and self.stack:
            self.stack.pop()


def margin_containers(path, ids):
    parser = MarginContainers(ids)
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.found


# Fixtures whose margin figures must sit in the same margin container as in
# a render of the same file without the extension.
MARGIN_IDS = {"contexts": ["fig-margin", "fig-aside", "fig-margin-cell"]}


def margin_summary(fixture):
    """Renders a copy of the fixture with no filters and compares the margin
    container of each figure in MARGIN_IDS with the filtered render."""
    ids = MARGIN_IDS[fixture]
    plain = f"{fixture}-plain"
    source = (TESTS / f"{fixture}.qmd").read_text(encoding="utf-8")
    stripped = re.sub(r"(?m)^filters:\n(  - .*\n)+", "", source)
    # A copy that still names the filter would compare the extension with
    # itself, so every line would read "same".
    if stripped == source:
        return ["(the filters block was not removed from the copy)"]
    (TESTS / f"{plain}.qmd").write_text(stripped, encoding="utf-8")
    try:
        code, log = render(plain, "html")
        if code != 0:
            return [f"(render without the extension exited with status {code})"]
        want = margin_containers(TESTS / f"{plain}.html", ids)
    finally:
        (TESTS / f"{plain}.qmd").unlink()
        (TESTS / f"{plain}.html").unlink(missing_ok=True)
        shutil.rmtree(TESTS / f"{plain}_files", ignore_errors=True)
    got = margin_containers(TESTS / f"{fixture}.html", ids)
    lines = []
    for i in ids:
        with_ext, without = got.get(i, "(missing)"), want.get(i, "(missing)")
        if with_ext == without:
            lines.append(f"{i}: same as without the extension: {with_ext}")
        else:
            lines.append(f'{i}: with the extension "{with_ext}", without "{without}"')
    return lines


def xref_summary(path):
    """The href of each cross-reference link in a rendered HTML page."""
    hrefs = re.findall(r'<a href="([^"]*)" class="quarto-xref"', path.read_text(encoding="utf-8"))
    return "\n".join(f"xref: {h}" for h in hrefs)


def tex_summary(path):
    # The body only: the preamble holds the wrapper and its comments.
    tex = path.read_text(encoding="utf-8").split("\\begin{document}", 1)[-1]
    found = re.finditer(r"\\begin\{(figure|wrappedfigure)\}(?:\[([^\]]*)\])?(.*?)\\end\{\1\}|\\wrappedstop\b", tex, re.S)
    lines = []
    for m in found:
        if m.group(1) is None:
            lines.append("wrappedstop")
            continue
        kind, options, body = m.groups()
        label = re.search(r"\\label\{([^}]*)\}", body)
        image = re.search(r"\\includegraphics(?:\[([^\]]*)\])?", body)
        lines.append(
            f"{kind}: {label.group(1) if label else '-'} [{options or '-'}] "
            f"image=[{(image.group(1) or '-') if image else '(none)'}]"
        )
    return "\n".join(lines)


@dataclass
class Box:
    page: int
    kind: str  # "text" or "image"
    top: float
    left: float
    bottom: float
    right: float
    text: str = ""


# pdftohtml sets 1.5 px for each pt, so 2 pt is 3 px.
NEAR = 3


def pdf_boxes(path):
    """Every text line and image box in a PDF."""
    if not shutil.which("pdftohtml"):
        raise SystemExit("verify.py needs poppler's pdftohtml for the layout check (brew install poppler, or apt install poppler-utils)")
    boxes, heights = [], {}
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "layout"
        result = subprocess.run(["pdftohtml", "-xml", "-q", str(path), str(out)], capture_output=True, text=True)
        if result.returncode != 0:
            raise LayoutError(f"pdftohtml exited with status {result.returncode}: {result.stderr.strip()}")
        root = ET.parse(f"{out}.xml").getroot()
    for page in root.iter("page"):
        n = int(page.get("number"))
        heights[n] = float(page.get("height"))
        for el in page:
            if el.tag not in ("text", "image"):
                continue
            top, left = float(el.get("top")), float(el.get("left"))
            bottom, right = top + float(el.get("height")), left + float(el.get("width"))
            text = "".join(el.itertext()).strip()
            boxes.append(Box(n, el.tag, top, left, bottom, right, text))
    # A page number in the foot is not text of a case.
    boxes = [b for b in boxes if not (b.kind == "text" and b.text.isdigit() and b.top > 0.85 * heights[b.page])]
    return boxes


def line_height(boxes):
    """The distance between the tops of two consecutive lines of the
    paragraph on page 1, the lines that text_edges reads."""
    left = text_edges(boxes)[0]
    tops = sorted(b.top for b in boxes if b.page == 1 and b.kind == "text" and abs(b.left - left) <= NEAR)
    steps = [b - a for a, b in zip(tops, tops[1:])]
    if not steps:
        raise LayoutError("page 1 has fewer than two lines of its paragraph")
    return statistics.median(steps)


def text_edges(boxes):
    """The left and right ends of a full line on page 1, which must hold no image."""
    if any(b.page == 1 and b.kind == "image" for b in boxes):
        raise LayoutError("page 1 holds an image, so it does not show the width of the text block")
    lines = [b for b in boxes if b.page == 1 and b.kind == "text"]
    if not lines:
        raise LayoutError("page 1 has no text, so it does not show the width of the text block")
    widest = max(b.right - b.left for b in lines)
    full = [b for b in lines if b.right - b.left > 0.95 * widest]
    return min(b.left for b in full), max(b.right for b in full)


def find_text(boxes, words):
    found = [b for b in boxes if b.kind == "text" and words in b.text]
    if len(found) != 1:
        raise LayoutError(f"{len(found)} lines hold {words!r}")
    return found[0]


class LayoutError(Exception):
    pass


@dataclass
class Figure:
    image: Box
    bottom: float
    caption: Box = None

    @property
    def page(self):
        return self.image.page


def find_figure(boxes, caption, near):
    """A figure by its caption words, or with caption None, the one image on
    the page of the text box `near`."""
    if caption is None:
        images = [b for b in boxes if b.kind == "image" and b.page == near.page]
        if len(images) != 1:
            raise LayoutError(f"{len(images)} images on page {near.page}, so the uncaptioned figure is not known")
        return Figure(images[0], images[0].bottom)
    cap = find_text(boxes, caption)
    above = [b for b in boxes if b.kind == "image" and b.page == cap.page and b.bottom <= cap.top + NEAR
             and b.left < cap.right and cap.left < b.right]
    if not above:
        raise LayoutError(f"no image above the caption {caption!r}")
    image = max(above, key=lambda b: b.bottom)
    return Figure(image, max(image.bottom, cap.bottom), cap)


def after(boxes, box, leave=None):
    """The text lines after `box` on its page, in reading order, each as a
    list of the boxes that share its top. The box `leave` is left out."""
    rest = sorted((b for b in boxes if b.kind == "text" and b.page == box.page and b.top > box.top + NEAR
                   and b is not leave),
                  key=lambda b: (b.top, b.left))
    lines = []
    for b in rest:
        if lines and abs(b.top - lines[-1][0].top) <= NEAR * 2:
            lines[-1].append(b)
        else:
            lines.append([b])
    return lines


def overlaps(a_left, a_right, b_left, b_right):
    return a_left < b_right and b_left < a_right


def check_beside(fig, line, side, edges, lh):
    if line.page != fig.page:
        raise LayoutError(f"the paragraph is on page {line.page} and the figure on page {fig.page}")
    if not line.top < fig.bottom:
        raise LayoutError("the paragraph starts below the figure")
    if fig.image.top - line.bottom >= lh / 2:
        raise LayoutError("the paragraph ends half a line or more above the figure")
    if overlaps(line.left, line.right, fig.image.left, fig.image.right):
        raise LayoutError("the paragraph overlaps the figure")
    edge = abs(fig.image.left - edges[0]) if side == "left" else abs(fig.image.right - edges[1])
    if edge > NEAR:
        raise LayoutError(f"the figure is {edge:.0f} px from the {side} edge of the text")


def check_below(fig, top, page, what):
    if page < fig.page or (page == fig.page and top < fig.bottom):
        raise LayoutError(f"{what} starts above the figure's bottom")


def check_full(lines, edges, what):
    if len(lines) < 3:
        raise LayoutError(f"{what} has {len(lines)} lines, fewer than 3")
    for line in lines[:-1]:
        left, right = min(b.left for b in line), max(b.right for b in line)
        if abs(left - edges[0]) > NEAR or abs(right - edges[1]) > NEAR:
            raise LayoutError(f"a line of {what} runs from {left:.0f} to {right:.0f} px, not full width")


def stop_case(boxes, edges, lh, caption, para, side, full=None):
    """The checks of a figure, its short paragraph, and the stop text after
    it. With `full`, the words that open the paragraph after the stop
    heading, which must be full width. Returns the figure and the stop line."""
    p = find_text(boxes, para)
    fig = find_figure(boxes, caption, p)
    check_beside(fig, p, side, edges, lh)
    lines = after(boxes, p, leave=fig.caption)
    if not lines:
        raise LayoutError("no stop text after the paragraph on its page")
    stop = lines[0]
    check_below(fig, stop[0].top, stop[0].page, f"the stop text {stop[0].text!r}")
    if full:
        rest = [ln for ln in lines[1:] if ln[0].top >= find_text(boxes, full).top - NEAR]
        check_full(rest, edges, f"the paragraph {full!r}")
    return fig, stop[0]


def plain_figure_case(boxes, edges, lh):
    """Stop-rule case 8: the plain figure and the text after it start below
    the wrapped figure."""
    p = find_text(boxes, "A short paragraph beside figure 8.")
    fig = find_figure(boxes, "Stop-rule case 8.", p)
    check_beside(fig, p, "left", edges, lh)
    plain = find_figure(boxes, "A figure with no wrap class.", p)
    if plain.page != p.page:
        raise LayoutError(f"the paragraph is on page {p.page} and the plain figure on page {plain.page}")
    check_below(fig, plain.image.top, plain.page, "the plain figure")
    texts = [b for b in boxes if b.kind == "text" and "Text after the stop block." in b.text
             and b.page == p.page and b.top > p.top]
    if not texts:
        raise LayoutError("no line 'Text after the stop block.' after the paragraph on its page")
    first = min(texts, key=lambda b: (b.page, b.top))
    check_below(fig, first.top, first.page, "the text after the stop block")


def lines_case(boxes, edges, lh):
    """A wrap-lines value larger than the figure needs moves the heading no
    further than a line from where it is without wrap-lines."""
    gaps = {}
    for name in ("plain", "extra"):
        fig, stop = stop_case(boxes, edges, lh, f"Lines {name}.", f"A short paragraph beside lines {name}.", "right")
        gaps[name] = stop.top - fig.bottom
    if abs(gaps["extra"] - gaps["plain"]) > lh:
        raise LayoutError(f"the heading is {gaps['extra']:.0f} px below the figure with wrap-lines "
                          f"and {gaps['plain']:.0f} px without it")


def page_bottom_case(boxes, edges, lh):
    """A figure that moves to the next page after its paragraphs end there
    has no text beside it, and its stop text starts below it."""
    p = find_text(boxes, "A short paragraph before page bottom moves.")
    fig = find_figure(boxes, "Page bottom.", p)
    if fig.page != p.page + 1:
        raise LayoutError(f"the paragraph is on page {p.page} and the figure on page {fig.page}, not the next")
    cap = find_text(boxes, "Page bottom.")
    beside = [b for b in boxes if b.kind == "text" and b.page == fig.page and b.top < fig.bottom and b is not cap]
    if beside:
        raise LayoutError(f"{beside[0].text!r} starts above the figure's bottom")
    stop = find_text(boxes, "Stop page bottom")
    check_below(fig, stop.top, stop.page, "the stop heading")


def stop_rule_cases():
    for n in range(1, 12):
        if n == 8:
            yield "case 8", plain_figure_case
            continue
        side = "left" if n % 2 == 0 else "right"
        yield f"case {n}", lambda bx, e, lh, n=n, side=side: stop_case(
            bx, e, lh, f"Stop-rule case {n}.", f"A short paragraph beside figure {n}.", side)


def stop_latex_cases():
    for form, caption in (("A", True), ("B", True), ("C", False), ("D", True)):
        for side in ("left", "right"):
            name = f"form {form} {side}"
            yield name, lambda bx, e, lh, name=name, caption=caption, side=side: stop_case(
                bx, e, lh, f"F{name[1:]}." if caption else None, f"A short paragraph beside {name}.", side,
                full=f"Full width text after stop {form} {side}.")
    yield "wrap-lines", lines_case
    yield "page bottom", page_bottom_case


def column_gap(boxes, edges, words):
    """The distance between the left edges of the two columns of the
    multicols whose first line holds `words`."""
    first = find_text(boxes, words)
    middle = (edges[0] + edges[1]) / 2
    lines = [b for b in boxes if b.kind == "text" and b.page == first.page and b.top >= first.top - NEAR]
    right = [b.left for b in lines if b.left > middle]
    if not right:
        raise LayoutError(f"the columns that start with {words!r} have no second column")
    return min(right) - min(b.left for b in lines)


def local_colsep_case(boxes, edges, lh):
    """A group that sets \\columnsep around a wrapped figure leaves it as it
    was outside the group."""
    want = column_gap(boxes, edges, "Reference columns.")
    got = column_gap(boxes, edges, "Columns after the group.")
    if abs(got - want) > NEAR:
        raise LayoutError(f"the columns after the group are {got:.0f} px apart, not {want:.0f} px")


# The wrap-gap of the wide gap figures, 30pt, in pdftohtml's 1.5 px per pt.
WIDE_GAP = 45


def wide_gap_case(side):
    """The text beside a figure with a wide wrap-gap starts that gap from the
    image."""
    def case(boxes, edges, lh):
        p = find_text(boxes, f"A paragraph beside the wide gap {side}.")
        fig = find_figure(boxes, f"Wide gap {side}.", p)
        check_beside(fig, p, side, edges, lh)
        lines = [b for b in boxes if b.kind == "text" and b.page == fig.page and b is not fig.caption
                 and b.top < fig.image.bottom and b.bottom > fig.image.top]
        if side == "left":
            gap = min(b.left for b in lines) - fig.image.right
        else:
            gap = fig.image.left - max(b.right for b in lines)
        if abs(gap - WIDE_GAP) > NEAR:
            raise LayoutError(f"the text is {gap:.0f} px from the image, not {WIDE_GAP} px")
    return case


def column_lines(boxes, fig, edges):
    """The text lines on the figure's page in the image's column, the
    caption left out."""
    middle = (edges[0] + edges[1]) / 2
    left, right = (edges[0], middle) if fig.image.right <= middle + NEAR else (
        (middle, edges[1]) if fig.image.left >= middle - NEAR else edges)
    return [b for b in boxes if b.kind == "text" and b.page == fig.page and b is not fig.caption
            and b.left >= left - NEAR and b.right <= right + NEAR]


def check_alone(boxes, fig, edges):
    """No text line of the image's column sits beside the image."""
    beside = [b for b in column_lines(boxes, fig, edges)
              if b.top < fig.image.bottom and b.bottom > fig.image.top]
    if beside:
        raise LayoutError(f"{beside[0].text!r} is beside the image")


# The width of each figure in the column fixtures, as a share of its column
# or box.
COLUMN_SHARE = 0.4


def normal_case(caption, para):
    """A wrapped figure that keeps a normal figure: no text of its column
    beside its image, and the image a share of the width of the text lines
    around it, its column or box. find_figure finds a caption only below
    its image."""
    def case(boxes, edges, lh):
        fig = find_figure(boxes, caption, find_text(boxes, para))
        check_alone(boxes, fig, edges)
        lines = column_lines(boxes, fig, edges)
        width = max(b.right for b in lines) - min(b.left for b in lines)
        want = COLUMN_SHARE * width
        got = fig.image.right - fig.image.left
        if abs(got - want) > NEAR:
            raise LayoutError(f"the image is {got:.0f} px wide, not {want:.0f} px")
    return case


def in_place_case(caption, before, after_words):
    """A figure in multicols sits in its column between the paragraph
    before it and the paragraph after it, with no text beside it."""
    def case(boxes, edges, lh):
        end = find_text(boxes, before)
        fig = find_figure(boxes, caption, end)
        nxt = find_text(boxes, after_words)
        if not (end.page == fig.page == nxt.page):
            raise LayoutError(f"the paragraphs and the figure are on pages {end.page}, {fig.page}, {nxt.page}")
        if not end.bottom <= fig.image.top + NEAR:
            raise LayoutError("the image starts above the end of the paragraph before it")
        if not fig.bottom <= nxt.top + NEAR:
            raise LayoutError("the paragraph after the figure starts above the figure's bottom")
        if not overlaps(end.left, end.right, fig.image.left, fig.image.right) or not overlaps(
                nxt.left, nxt.right, fig.image.left, fig.image.right):
            raise LayoutError("the figure is not in the column of the paragraphs around it")
        check_alone(boxes, fig, edges)
    return case


def multicols_cases():
    yield "local columnsep", local_colsep_case
    yield "wide gap left", wide_gap_case("left")
    yield "wide gap right", wide_gap_case("right")
    yield "figure in multicols", in_place_case("In multicols.", "Before figure M.", "After figure M.")
    yield "image in multicols", in_place_case(None, "Before image M.", "After image M.")


def twocolumn_class_cases():
    yield "figure", normal_case("Fig C.", "After figure C.")
    yield "figure in a box", normal_case("Fig B.", "After figure B.")
    yield "image", normal_case(None, "After image C.")


def twocolumn_switch_cases():
    yield "before twocolumn", lambda bx, e, lh: check_beside(
        find_figure(bx, "Before twocolumn.", None),
        find_text(bx, "A short paragraph beside the figure before twocolumn."), "right", e, lh)
    yield "in two columns", normal_case("Fig T.", "After figure T.")
    yield "after onecolumn", lambda bx, e, lh: check_beside(
        find_figure(bx, "After onecolumn.", None),
        find_text(bx, "A short paragraph beside the figure after onecolumn."), "left", e, lh)


def find_words(boxes, words):
    """The one text line that holds `words`, with runs of spaces in the line
    read as one space. pdftohtml can write Typst's word gaps as two spaces,
    as in a justified line."""
    found = [b for b in boxes if b.kind == "text" and words in " ".join(b.text.split())]
    if len(found) != 1:
        raise LayoutError(f"{len(found)} lines hold {words!r}")
    return found[0]


# Quarto's Typst page has 6 in of text, so 40% of it is 2.4 in, 172.8 pt,
# which pdftohtml writes as 259 px. 2 in is 144 pt, or 216 px.
TYPST_40 = 259
TYPST_2IN = 216


def typst_width_case(caption, para, want):
    """A Typst figure whose paragraph's first line sits beside its image and
    inside the text edges, and whose image is `want` px wide."""
    def case(boxes, edges, lh):
        fig = find_figure(boxes, caption, None)
        line = find_words(boxes, para)
        if line.page != fig.page:
            raise LayoutError(f"the paragraph is on page {line.page} and the figure on page {fig.page}")
        if not (line.top < fig.image.bottom and fig.image.top < line.bottom):
            raise LayoutError("the paragraph's first line is not beside the image")
        if overlaps(line.left, line.right, fig.image.left, fig.image.right):
            raise LayoutError("the paragraph overlaps the figure")
        if line.left < edges[0] - NEAR or line.right > edges[1] + NEAR:
            raise LayoutError(f"the paragraph's first line runs from {line.left:.0f} to {line.right:.0f} px, "
                              f"outside the text edges {edges[0]:.0f} to {edges[1]:.0f} px")
        got = fig.image.right - fig.image.left
        if abs(got - want) > NEAR:
            raise LayoutError(f"the image is {got:.0f} px wide, not {want:.0f} px")
    return case


def typst_wide_cases():
    yield "40%", typst_width_case("Fig W40.", "Marker forty", TYPST_40)
    yield "no width", typst_width_case("Fig Wnone.", "Marker none", TYPST_40)
    yield "10in", typst_width_case("Fig W10in.", "Marker inches", TYPST_40)
    yield "60em", typst_width_case("Fig W60em.", "Marker ems", TYPST_40)
    yield "2in", typst_width_case("Fig W2in.", "Marker two", TYPST_2IN)


def typst_wide_meta_cases():
    yield "10in takes the 2in default", typst_width_case("Fig M10in.", "Marker default", TYPST_2IN)


# 3 in is 216 pt, or 324 px.
TYPST_3IN = 324


def typst_image_case(caption, want):
    """A Typst figure whose image is `want` px wide, with no test of the
    text beside it."""
    def case(boxes, edges, lh):
        fig = find_figure(boxes, caption, None)
        got = fig.image.right - fig.image.left
        if abs(got - want) > NEAR:
            raise LayoutError(f"the image is {got:.0f} px wide, not {want:.0f} px")
    return case


def typst_gap_cases():
    yield "5in with 1.5in gap", typst_width_case("Fig G5in.", "Marker inches", TYPST_3IN)
    yield "99% with 1em gap", typst_width_case("Fig G99.", "Marker percent", TYPST_3IN)
    yield "4.6in with 25% gap", typst_width_case("Fig G4in.", "Marker share", TYPST_3IN)
    yield "2in with 2em gap", typst_width_case("Fig G2in.", "Marker fits", TYPST_2IN)
    yield "75% with 25% gap", typst_width_case("Fig G70.", "Marker sum", TYPST_3IN)
    yield "40% with gap too wide", typst_image_case("Fig GWide.", TYPST_40)


def typst_gap_meta_cases():
    yield "5in with 1.5in gap takes 40%", typst_width_case("Fig MGap.", "Marker metadata", TYPST_40)
    yield "default with gap too wide", typst_width_case("Fig MDefault.", "Marker fallback", TYPST_40)


# The fixtures whose PDF through LaTeX the layout check reads, with their cases.
LAYOUT = {
    "stop-rule": stop_rule_cases,
    "stop-latex": stop_latex_cases,
    "multicols": multicols_cases,
    "twocolumn-class": twocolumn_class_cases,
    "twocolumn-switch": twocolumn_switch_cases,
}

# The fixtures whose PDF through Typst the layout check reads, with their cases.
TYPST_LAYOUT = {
    "typst-wide": typst_wide_cases,
    "typst-wide-meta": typst_wide_meta_cases,
    "typst-gap": typst_gap_cases,
    "typst-gap-meta": typst_gap_meta_cases,
}


def layout_check(fixture, cases):
    """Prints a line for each case. Returns the names of the failed cases."""
    try:
        boxes = pdf_boxes(TESTS / f"{fixture}.pdf")
        edges, lh = text_edges(boxes), line_height(boxes)
    except LayoutError as err:
        print(f"FAIL layout {fixture}: {err}")
        return [f"layout {fixture}"]
    failed = []
    for name, case in cases[fixture]():
        try:
            case(boxes, edges, lh)
            print(f"ok   layout {fixture} {name}")
        except LayoutError as err:
            print(f"FAIL layout {fixture} {name}: {err}")
            failed.append(f"layout {fixture} {name}")
    return failed


# The fixtures whose LaTeX log the log check reads, rendered with
# latex-clean: false so the log stays: the number of two-column warnings
# and the number of wrapped figures inside multicols.
LOGS = {
    "twocolumn-class": (1, 0),
    "twocolumn-switch": (1, 0),
    "multicols": (0, 2),
    "stop-latex": (0, 0),
}
TWO_COLUMN_WARNING = "Two-column text: figures set as normal figures"
MULTICOLS_WARNING = "Figure in multicols set as normal figure"
LOG_WARNING = re.compile(r"Package wrapped Warning: (.*?)(?: on input line (\d+))?\.")


def multicols_figures(tex):
    """The line numbers of the wrappedfigure environments inside multicols."""
    depth, found = 0, []
    for n, line in enumerate(tex.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("\\begin{multicols"):
            depth += 1
        elif line.startswith("\\end{multicols"):
            depth -= 1
        elif line.startswith("\\begin{wrappedfigure}") and depth > 0:
            found.append(n)
    return found


def log_check(fixture):
    """Checks the wrapped warnings in a fixture's LaTeX log: the two-column
    warning, and a multicols warning that names the line of each wrapped
    figure inside multicols. Returns the names of the failed checks."""
    two_column, in_multicols = LOGS[fixture]
    path = TESTS / f"{fixture}.log"
    if not path.exists():
        print(f"FAIL log {fixture}: no {path.name} after the render")
        return [f"log {fixture}"]
    # TeX breaks a long log line at max_print_line, 79 in TeX Live and 10000
    # in TinyTeX, with no mark, so the log is read with its line breaks
    # removed.
    log = path.read_text(encoding="utf-8", errors="replace").replace("\n", "")
    found = LOG_WARNING.findall(log)
    two = [w for w in found if w[0] == TWO_COLUMN_WARNING]
    multi = sorted(int(n) if n else 0 for msg, n in found if msg == MULTICOLS_WARNING)
    other = [msg for msg, n in found if msg not in (TWO_COLUMN_WARNING, MULTICOLS_WARNING)]
    want = multicols_figures(TESTS / f"{fixture}.tex")
    problems = []
    if len(want) != in_multicols:
        problems.append(f"the .tex has {len(want)} wrapped figures in multicols, not {in_multicols}")
    if len(two) != two_column:
        problems.append(f"{len(two)} two-column warnings, not {two_column}")
    if multi != want:
        problems.append(f"multicols warnings on lines {multi}, not {want}")
    if other:
        problems.append(f"other wrapped warnings: {other}")
    if "`hypcap=true' will be ignored" in log:
        problems.append("a caption package hypcap warning")
    if problems:
        print(f"FAIL log {fixture}: {'; '.join(problems)}")
        return [f"log {fixture}"]
    print(f"ok   log {fixture}")
    return []


# A call in a table cell is indented and opens the cell's `[`, so its lines
# carry the indent of its first line, and its last line closes the cell
# with `],`.
TYPST_WRAP_START = re.compile(r"^[ \t]*\[?#layout\(wrapped-size => wrap-content\(", re.M)
TYPST_WRAP = re.compile(
    r"^(?P<indent>[ \t]*)\[?#layout\(wrapped-size => wrap-content\(([^\n]*), box\(width: 100%\)\[\n"
    r"(.*?)^(?P=indent)\], \[\n(.*?)^(?P=indent)\]\)\)[\],]*$",
    re.M | re.S,
)
# Typst calls that Pandoc and Quarto write as blocks. Any other text, inline
# calls such as #strike[ or #footnote[ included, starts a paragraph.
TYPST_BLOCKS = (
    "#block", "#figure", "#table", "#grid", "#Skylighting", "#wrap-content", "#context", "#layout(",
    "#callout", "#quote", "#line(", "#pagebreak", "#v(", "#align(", "#pad(", "#columns(",
)


def typ_block_kind(block):
    if block.startswith("="):
        return "heading"
    if block.startswith(("- ", "+ ")) or re.match(r"\d+\. ", block):
        return "list"
    if block.startswith("/ "):
        return "terms"
    if block.startswith("```"):
        return "code"
    if block.startswith(TYPST_BLOCKS):
        return "block"
    return "p"


def typ_summary(path):
    # A body figure's #figure( call starts a line, or follows the indent of
    # a table cell, unlike the `[#figure(` in Quarto's template. Each chunk
    # runs to the next call, and the figure's label is the first one in it.
    # The figure's content ends before its `kind:` line.
    source = path.read_text(encoding="utf-8")
    chunks = re.split(r"^[ \t]*#figure\(", source, flags=re.M)[1:]
    lines = []
    for chunk in chunks:
        label = re.search(r"^[ \t]*<((?:fig|tbl)-[\w-]+)>", chunk, re.M)
        content = chunk.split("\nkind: ", 1)[0]
        width = re.search(r"image\([^)]*width:", content) is not None
        lines.append(f"figure: {label.group(1) if label else '-'} image-width={'yes' if width else 'no'}")
    # The filter writes each wrap-content call as raw lines around the box
    # content and the paragraphs, which Typst output separates by blank lines.
    # Each block beside the box is named by its kind, and a count of
    # citations follows. A call that the pattern cannot read is counted.
    lines.append("# wraps")
    calls = TYPST_WRAP.findall(source)
    for _, options, fixed, body in calls:
        label = re.search(r"^[ \t]*<((?:fig|tbl)-[\w-]+)>", fixed, re.M)
        image = re.search(r'image\("([^"]*)"', fixed)
        box = label.group(1) if label else Path(image.group(1)).name if image else "-"
        alt_text = re.search(r'image\([^)]*alt: "([^"]*)"', fixed)
        alt = f'alt="{alt_text.group(1)}"' if alt_text else "no-alt"
        blocks = [typ_block_kind(b.strip()) for b in re.split(r"\n\s*\n", body) if b.strip()]
        # A narrative citation is a #cite( call, and a bracketed one is @key.
        cites = len(re.findall(r"#cite\(|(?<![\w.@])@[\w:-]+", body))
        lines.append(f"{options} | {box} {alt} | {', '.join(blocks)} | cites={cites}")
    unread = len(TYPST_WRAP_START.findall(source)) - len(calls)
    if unread:
        lines.append(f"unread wrap-content calls: {unread}")
    return "\n".join(lines)


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
PIC = "{http://schemas.openxmlformats.org/drawingml/2006/picture}"
EMU_PER_TWIP = 635
# A citation as citeproc writes it in the text: "Smith and Doe (2020)".
AUTHOR_YEAR = re.compile(r"[A-Z][\w-]+(?: and [A-Z][\w-]+| et al\.)? \(\d{4}\)")


def docx_frame(p):
    """The w:framePr of a paragraph with w:wrap="around", in any of its
    w:pPr elements, or None."""
    for ppr in p.findall(f"{W}pPr"):
        frame = ppr.find(f"{W}framePr")
        if frame is not None and frame.get(f"{W}wrap") == "around":
            return frame
    return None


def docx_frames(body):
    """Each frame in the body: consecutive top-level paragraphs with the same
    w:framePr. Each frame records its side, width, gap, and anchor, the
    bookmark open before it ("-" if none), each image's file name, whether
    it fills the frame width, and its alt text, whether each caption
    paragraph has the ImageCaption style, and the kind of each block after
    it up to and including the paragraph that holds the clearing break ("p"
    for a paragraph). It also records the anchors of the links in those
    paragraphs and the number of author-year citations in their text."""
    lines = []
    framed = 0
    children = list(body)
    # The bookmark that opens right before a frame, with no block between.
    bookmark = None
    i = 0
    while i < len(children):
        el = children[i]
        if el.tag == f"{W}bookmarkStart":
            bookmark = el.get(f"{W}name")
            i += 1
            continue
        if el.tag == f"{W}bookmarkEnd":
            i += 1
            continue
        frame = docx_frame(el) if el.tag == f"{W}p" else None
        if frame is None:
            bookmark = None
            i += 1
            continue
        key = sorted(frame.attrib.items())
        paras = []
        while i < len(children) and children[i].tag in (f"{W}p", f"{W}bookmarkStart", f"{W}bookmarkEnd"):
            f = docx_frame(children[i]) if children[i].tag == f"{W}p" else None
            if children[i].tag == f"{W}p" and (f is None or sorted(f.attrib.items()) != key):
                break
            if f is not None:
                paras.append(children[i])
            i += 1
        framed += len(paras)
        width = int(frame.get(f"{W}w"))
        parts = []
        for p in paras:
            extent = p.find(f".//{WP}extent")
            if extent is not None:
                name = Path(p.find(f".//{PIC}cNvPr").get("descr") or "-").name
                fills = abs(int(extent.get("cx")) - width * EMU_PER_TWIP) <= EMU_PER_TWIP
                alt = p.find(f".//{WP}docPr").get("descr")
                parts.append(f"image {name} fills={'yes' if fills else 'no'} alt={alt!r}")
            else:
                styles = [s.get(f"{W}val") for s in p.iter(f"{W}pStyle")]
                parts.append(f"caption style={'ImageCaption' if 'ImageCaption' in styles else '-'}")
        after = []
        links = []
        cites = 0
        while i < len(children):
            el = children[i]
            i += 1
            if el.tag in (f"{W}bookmarkStart", f"{W}bookmarkEnd", f"{W}sectPr"):
                continue
            if el.tag != f"{W}p":
                after.append(el.tag.replace(W, ""))
                continue
            after.append("p")
            links += [h.get(f"{W}anchor") for h in el.iter(f"{W}hyperlink") if h.get(f"{W}anchor")]
            text = "".join(t.text or "" for t in el.iter(f"{W}t"))
            cites += len(AUTHOR_YEAR.findall(text))
            if any(br.get(f"{W}clear") == "all" for br in el.iter(f"{W}br")):
                after.append("clear")
                break
        side = frame.get(f"{W}xAlign")
        gap = frame.get(f"{W}hSpace")
        anchor = frame.get(f"{W}hAnchor")
        lines.append(f"frame {side} w={width} gap={gap} anchor={anchor} | {bookmark or '-'} | "
                     f"{'; '.join(parts)} | {', '.join(after)} | links={','.join(links) or '-'} cites={cites}")
        bookmark = None
    return lines, framed


def docx_summary(path):
    # The width Word shows for each image, in EMU, in document order, then
    # each frame.
    with zipfile.ZipFile(path) as docx:
        xml = docx.read("word/document.xml").decode("utf-8")
    lines = [f"image: cx={cx}" for cx in re.findall(r'<wp:extent cx="(\d+)"', xml)]
    body = ET.fromstring(xml).find(f"{W}body")
    lines.append("# frames")
    frames, framed = docx_frames(body)
    lines += frames
    others = sum(1 for p in body.iter(f"{W}p") if docx_frame(p) is not None) - framed
    if others:
        lines.append(f"framed paragraphs outside a frame: {others}")
    return "\n".join(lines)


def render(fixture, fmt):
    # A fixture that is a folder is a project, rendered whole.
    target = fixture if (TESTS / fixture).is_dir() else f"{fixture}.qmd"
    cmd = ["quarto", "render", target, "--to", fmt]
    env = os.environ.copy()
    if fmt == "pdf" and fixture in LOGS:
        # TeX Live's default log line length, which TinyTeX raises to 10000,
        # so the log check reads warnings that TeX breaks across lines.
        env["max_print_line"] = "79"
    result = subprocess.run(cmd, cwd=TESTS, capture_output=True, text=True, env=env)
    log = ANSI.sub("", result.stdout + result.stderr)
    return result.returncode, log


def summary(fixture, fmt, log):
    found = [m.group(1).strip() for m in WARNING.finditer(log)]
    warnings = sorted(set(found))
    parts = ["# warnings"] + [f"{found.count(w)}x {w}" for w in warnings]
    if (TESTS / fixture).is_dir():
        for page in sorted((TESTS / fixture / "_book").glob("*.html")):
            parts += [f"## {page.name}", html_summary(page), "# xrefs", xref_summary(page)]
    elif fmt in ("html", "revealjs"):
        parts.append(html_summary(TESTS / f"{fixture}.html"))
        if fixture in MARGIN_IDS:
            parts += ["# margin containers"] + margin_summary(fixture)
    elif fmt == "pdf":
        parts += ["# tex", tex_summary(TESTS / f"{fixture}.tex")]
    elif fmt == "typst":
        parts += ["# typ", typ_summary(TESTS / f"{fixture}.typ")]
    elif fmt == "docx":
        parts += ["# docx", docx_summary(TESTS / f"{fixture}.docx")]
    return "\n".join(parts) + "\n"


def main():
    update = "--update" in sys.argv[1:]
    SNAPSHOTS.mkdir(exist_ok=True)
    # docx-reference.qmd and docx-columns.qmd read these reference docs,
    # which are not committed.
    reference_narrow.main()
    failed = []
    for fixture, fmt, compare in RENDERS:
        name = f"{fixture}.{fmt}"
        if fmt == "pdf" and fixture in LOGS:
            # A log left by an earlier run must not pass for this one.
            (TESTS / f"{fixture}.log").unlink(missing_ok=True)
        code, log = render(fixture, fmt)
        if code != 0:
            print(f"FAIL {name}: quarto render exited with status {code}")
            print(log[-2000:])
            failed.append(name)
            continue
        if fmt == "pdf" and fixture in LAYOUT:
            failed += layout_check(fixture, LAYOUT)
        if fmt == "typst" and fixture in TYPST_LAYOUT:
            failed += layout_check(fixture, TYPST_LAYOUT)
        if fmt == "pdf" and fixture in LOGS:
            failed += log_check(fixture)
        if not compare:
            print(f"ok   {name} (rendered, no snapshot)")
            continue
        got = summary(fixture, fmt, log)
        snap = SNAPSHOTS / f"{name}.txt"
        if update:
            snap.write_text(got, encoding="utf-8")
            print(f"WROTE {snap.relative_to(TESTS.parent)}")
            continue
        if not snap.exists():
            print(f"FAIL {name}: no snapshot (run with --update)")
            failed.append(name)
            continue
        want = snap.read_text(encoding="utf-8")
        if got != want:
            print(f"FAIL {name}: output differs from {snap.relative_to(TESTS.parent)}")
            diff = difflib.unified_diff(want.splitlines(), got.splitlines(), "snapshot", "render", lineterm="")
            print("\n".join(list(diff)[:80]))
            failed.append(name)
        else:
            print(f"ok   {name}")
    if failed:
        print(f"{len(failed)} of {len(RENDERS)} renders failed: {', '.join(failed)}")
        return 1
    print(f"all {len(RENDERS)} renders pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
