"""Render the wrapped fixtures and compare the output with committed snapshots.

Run from the repository root:

    python3 tests/verify.py            # render and compare
    python3 tests/verify.py --update   # render and rewrite the snapshots

Needs Quarto, R with knitr, and TinyTeX. Each render must exit with status
0. A snapshot under tests/_snapshots/ records the parts of a render that
show what the filter decided. For every format it holds the extension's
warnings. For HTML it also holds the breakpoint value, the wrap class and
style of every figure or table div and wrapped box, the wrap class, style, and width
of every image, and the members of every .wrap-group. Style declarations
are sorted, so their order does not count. For PDF it also holds the kind,
label, and options of each figure environment and the options of its
\includegraphics, and for Typst the label of each #figure( call and
whether its image keeps a width. For Typst it also holds each
wrap-content call's options, the figure label or image in its box, and
one "p" for each paragraph beside the box. For Word
it also holds each image's width from word/document.xml. A revealjs
snapshot holds what an HTML snapshot holds. A fixture that is a folder is a
book project: its snapshot holds the HTML parts of each page under _book/,
and the href of each cross-reference link. For a fixture in MARGIN_IDS, the
script also renders a copy with no filters and records whether the nearest
column-margin div around each named figure has the same classes in both
renders. The script exits with status 1 on a failed render or a snapshot
difference.

Some fixtures exist only for the browser checks in tests/layout.js, which
measure layout. Those fixtures are rendered here, so their HTML is current,
and they have no snapshot.
"""

import difflib
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

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
    ("meta-breakpoint", "html", True),
    ("meta-string", "html", True),
    ("contexts", "html", True),
    ("contexts", "pdf", True),
    ("contexts", "typst", True),
    ("stop-rule", "pdf", True),
    ("stop-rule", "typst", True),
    ("twocolumn", "pdf", True),
    ("twocolumn-list", "pdf", True),
    ("pdf-ua", "pdf", True),
    ("pdf-ua1", "pdf", True),
    ("tex-options", "pdf", True),
    ("typst-break", "typst", True),
    ("typst-ua", "typst", True),
    ("book", "html", True),
    ("revealjs", "revealjs", True),
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
    breakpoint = re.search(r"@media \(max-width: ([^)]*)\)\s*\{[^{}]*wrap-", source)
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
    envs = re.findall(r"\\begin\{(figure|wrappedfigure)\}(?:\[([^\]]*)\])?(.*?)\\end\{\1\}", tex, re.S)
    lines = []
    for kind, options, body in envs:
        label = re.search(r"\\label\{([^}]*)\}", body)
        image = re.search(r"\\includegraphics(?:\[([^\]]*)\])?", body)
        lines.append(
            f"{kind}: {label.group(1) if label else '-'} [{options or '-'}] "
            f"image=[{(image.group(1) or '-') if image else '(none)'}]"
        )
    return "\n".join(lines)


TYPST_WRAP = re.compile(
    r"^#wrap-content\(([^\n]*), box\(width: 100%\)\[\n(.*?)^\], \[\n(.*?)^\]\)$", re.M | re.S
)


def typ_summary(path):
    # A body figure's #figure( call starts a line, unlike the one in Quarto's
    # template. Each call runs to the next one, and its label follows it.
    source = path.read_text(encoding="utf-8")
    chunks = re.split(r"^#figure\(", source, flags=re.M)[1:]
    lines = []
    for chunk in chunks:
        label = re.search(r"^<((?:fig|tbl)-[\w-]+)>", chunk, re.M)
        width = re.search(r"image\([^)]*width:", chunk) is not None
        lines.append(f"figure: {label.group(1) if label else '-'} image-width={'yes' if width else 'no'}")
    # The filter writes each wrap-content call as raw lines around the box
    # content and the paragraphs, which Typst output separates by blank lines.
    lines.append("# wraps")
    for options, fixed, body in TYPST_WRAP.findall(source):
        label = re.search(r"^<((?:fig|tbl)-[\w-]+)>", fixed, re.M)
        image = re.search(r'image\("([^"]*)"', fixed)
        box = label.group(1) if label else Path(image.group(1)).name if image else "-"
        paras = ["p" for block in re.split(r"\n\s*\n", body) if block.strip()]
        lines.append(f"{options} | {box} | {', '.join(paras)}")
    return "\n".join(lines)


def docx_summary(path):
    # The width Word shows for each image, in EMU, in document order.
    with zipfile.ZipFile(path) as docx:
        xml = docx.read("word/document.xml").decode("utf-8")
    return "\n".join(f"image: cx={cx}" for cx in re.findall(r'<wp:extent cx="(\d+)"', xml))


def render(fixture, fmt):
    # A fixture that is a folder is a project, rendered whole.
    target = fixture if (TESTS / fixture).is_dir() else f"{fixture}.qmd"
    cmd = ["quarto", "render", target, "--to", fmt]
    result = subprocess.run(cmd, cwd=TESTS, capture_output=True, text=True)
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
    failed = []
    for fixture, fmt, compare in RENDERS:
        name = f"{fixture}.{fmt}"
        code, log = render(fixture, fmt)
        if code != 0:
            print(f"FAIL {name}: quarto render exited with status {code}")
            print(log[-2000:])
            failed.append(name)
            continue
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
