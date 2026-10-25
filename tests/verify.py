"""Render the wrapped fixtures and compare the output with committed snapshots.

Run from the repository root:

    python3 tests/verify.py            # render and compare
    python3 tests/verify.py --update   # render and rewrite the snapshots

Needs Quarto, R with knitr, and TinyTeX. Each render must exit with status
0. A snapshot under tests/_snapshots/ records the parts of a render that
show what the filter decided. For every format it holds the extension's
warnings. For HTML it also holds the breakpoint value, the wrap class and
style of every figure div and wrapped box, the wrap class, style, and width
of every image, and the members of every .wrap-group. For PDF it also holds
the kind and label of each figure environment. For Typst it holds the label
of each labeled figure. For Word it holds the warnings only. The script exits with status 1 on a failed
render or a snapshot difference.

Some fixtures exist for the browser checks in tests/layout.js, which measure
layout. Those fixtures are rendered here, so their HTML is current, and they
have no snapshot.
"""

import difflib
import re
import subprocess
import sys
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
    ("margin", "html", False),
    ("stop-rule", "html", False),
    ("rtl", "html", False),
    ("readme", "html", False),
]

WARNING = re.compile(r"wrapped: .*")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
WRAP_CLASSES = ("wrap-left", "wrap-right", "wrapped-image")


def wrap_classes(classes):
    return " ".join(c for c in classes.split() if c in WRAP_CLASSES) or "-"


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
        if tag == "div" and attrs.get("id", "").startswith("fig-"):
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
            src = Path(attrs.get("src", "")).name
            self.images.append(
                f"{src}: wrap={wrap_classes(classes)} style={attrs.get('style', '-')} width={attrs.get('width', '-')}"
            )
        if tag != "div":
            return
        if attrs.get("id", "").startswith("fig-") or "wrapped-image" in classes.split():
            name = attrs.get("id", "(box)")
            self.figures.append(f"{name}: {wrap_classes(classes)} style={attrs.get('style', '-')}")

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
    breakpoint = re.search(r"@media \(max-width: ([^)]*)\)\s*\{\s*\.quarto-float\.wrap-left", source)
    parts = ["# breakpoint", breakpoint.group(1) if breakpoint else "(none)"]
    parts += ["# figures"] + parser.figures
    parts += ["# images"] + parser.images
    parts += ["# groups"] + [", ".join(members) for members in parser.groups]
    return "\n".join(parts)


def tex_summary(path):
    tex = path.read_text(encoding="utf-8")
    envs = re.findall(r"\\begin\{(figure|wrappedfigure)\}(.*?)\\end\{\1\}", tex, re.S)
    lines = []
    for kind, body in envs:
        label = re.search(r"\\label\{([^}]*)\}", body)
        lines.append(f"{kind}: {label.group(1) if label else '-'}")
    return "\n".join(lines)


def typ_summary(path):
    labels = re.findall(r"^<(fig-[\w-]+)>", path.read_text(encoding="utf-8"), re.M)
    return "\n".join(f"figure: {label}" for label in labels)


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
