"""Render the wrapped fixtures and compare the output with committed snapshots.

Run from the repository root:

    python3 tests/verify.py            # render and compare
    python3 tests/verify.py --update   # render and rewrite the snapshots

Needs Quarto, R with knitr, and TinyTeX. Each render must exit with status
0. Each snapshot under tests/_snapshots/ holds the parts of one render that
the filter changes: for HTML, every .wrap-group fragment, the breakpoint
style, and the classes of every figure; for the other formats, the
extension's warnings and Quarto's figure markup. The script exits with
status 1 on a failed render or a snapshot difference.

Layout (floats, widths, the stop rule) is checked in a browser with
tests/layout.js, not here.
"""

import difflib
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SNAPSHOTS = TESTS / "_snapshots"

# (fixture, format) pairs to render.
RENDERS = [
    ("fixture", "html"),
    ("fixture", "pdf"),
    ("fixture", "typst"),
    ("fixture", "docx"),
    ("margin", "html"),
    ("defaults", "html"),
    ("stop-rule", "html"),
]

WARNING = re.compile(r"wrapped: .*")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
START_TAG = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^\s=>/]+(?:=\"[^\"]*\")?)+)\s*>")
ATTR = re.compile(r"[^\s=>/]+(?:=\"[^\"]*\")?")


def sort_attributes(html):
    """Sorts the attributes of each start tag. Quarto writes a figure div's
    attributes in an order that changes between renders."""
    return START_TAG.sub(lambda m: "<" + m.group(1) + " " + " ".join(sorted(ATTR.findall(m.group(2)))) + ">", html)


class Fragments(HTMLParser):
    """Collects the source text of each div.wrap-group and the classes of
    each figure div."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = source.splitlines(keepends=True)
        self.offsets = [0]
        for line in self.lines:
            self.offsets.append(self.offsets[-1] + len(line))
        self.depth = 0
        self.start = None
        self.groups = []
        self.figures = []

    def _pos(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag != "div":
            return
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if attrs.get("id", "").startswith("fig-") or "wrapped-image" in classes:
            self.figures.append(f"{attrs.get('id', '(uncaptioned)')}: {' '.join(classes)}")
        if self.start is not None:
            self.depth += 1
        elif "wrap-group" in classes:
            self.start = self._pos()
            self.depth = 1

    def handle_endtag(self, tag):
        if tag != "div" or self.start is None:
            return
        self.depth -= 1
        if self.depth == 0:
            end = self.source.index(">", self._pos()) + 1
            self.groups.append(self.source[self.start:end])
            self.start = None


def html_summary(path):
    source = path.read_text(encoding="utf-8")
    parser = Fragments(source)
    parser.feed(source)
    style = re.search(r"<style>\s*@media \(max-width: [^)]*\).*?</style>", source, re.S)
    parts = ["# figures"] + parser.figures
    parts += ["# breakpoint style", style.group(0) if style else "(none)"]
    for i, group in enumerate(parser.groups, 1):
        parts += [f"# wrap-group {i}", sort_attributes(group)]
    return "\n".join(parts)


def tex_summary(path):
    keep = re.compile(r"\\begin\{(figure|wrappedfigure)\}|\\end\{(figure|wrappedfigure)\}|\\includegraphics|\\caption\{")
    return "\n".join(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if keep.search(line))


def typ_summary(path):
    keep = re.compile(r"^#figure\(|^<fig-|wrap-content|image\(")
    return "\n".join(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if keep.search(line.strip()))


def render(fixture, fmt):
    cmd = ["quarto", "render", f"{fixture}.qmd", "--to", fmt]
    result = subprocess.run(cmd, cwd=TESTS, capture_output=True, text=True)
    log = ANSI.sub("", result.stdout + result.stderr)
    return result.returncode, log


def summary(fixture, fmt, log):
    warnings = sorted(set(m.group(0).strip() for m in WARNING.finditer(log)))
    counts = {w: len(re.findall(re.escape(w), log)) for w in warnings}
    parts = ["# warnings"] + [f"{counts[w]}x {w}" for w in warnings]
    if fmt == "html":
        parts.append(html_summary(TESTS / f"{fixture}.html"))
    elif fmt == "pdf":
        parts += ["# tex", tex_summary(TESTS / f"{fixture}.tex")]
    elif fmt == "typst":
        parts += ["# typ", typ_summary(TESTS / f"{fixture}.typ")]
    text = "\n".join(parts) + "\n"
    return UUID.sub("UUID", text)


def main():
    update = "--update" in sys.argv[1:]
    SNAPSHOTS.mkdir(exist_ok=True)
    failed = []
    for fixture, fmt in RENDERS:
        name = f"{fixture}.{fmt}"
        code, log = render(fixture, fmt)
        if code != 0:
            print(f"FAIL {name}: quarto render exited with status {code}")
            print(log[-2000:])
            failed.append(name)
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
    print(f"all {len(RENDERS)} renders match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
